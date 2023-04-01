# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from freelancer_scraper.utils import calculate_priority_score


class JobItemPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    user_skills = ["Python", "Data Science", "Machine Learning"]
    weights = {
        "budget": 0.25,
        "project_duration": 0.1,
        "skills_match": 0.35,
        "customer_rating": 0.1,
        "bid_competition": 0.1,
        "verifications_status": 0.1,
    }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
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
        adapter["priority_score"] = calculate_priority_score(
            adapter.asdict(), self.user_skills, self.weights
        )
        self.db.jobs.insert_one(adapter.asdict())
        return item
