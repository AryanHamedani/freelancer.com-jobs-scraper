# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from freelancer_scraper.utils import is_skills_match, generate_bid


class JobItemPipeline:
    def __init__(self, mongo_uri, mongo_db, user_skills):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.user_skills = user_skills

    # user_skills = ["Python", "Data Science", "Machine Learning"]
    # weights = {
    #     "budget": 0.25,
    #     "project_duration": 0.1,
    #     "skills_match": 0.35,
    #     "customer_rating": 0.1,
    #     "bid_competition": 0.1,
    #     "verifications_status": 0.1,
    # }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
            user_skills=crawler.settings.get("USER_SKILLS"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        existing_item = self.db.jobs.find_one({"url": adapter["url"]})
        if existing_item:
            spider.logger.info(f"Item already exists: {adapter['url']}")
            return item
        gpt_response = is_skills_match(
            " ".join(adapter["description"]), user_skills=self.user_skills
        )
        adapter["is_skill_match"] = gpt_response[0]
        adapter["gpt_skill_match_response"] = gpt_response[1]
        if (
            adapter["count_of_bids"] < 50
            and (not adapter["currency_code"] == "INR")
            and gpt_response[0] == 1
        ):
            adapter["is_bided"] = True
            adapter["bid_description"] = generate_bid(
                adapter["description"], self.user_skills
            )
        self.db.jobs.insert_one(adapter.asdict())
        return item
