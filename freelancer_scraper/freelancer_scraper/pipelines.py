# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from freelancer_scraper.tasks import process_and_save_item


class JobItemPipeline:
    def __init__(self, mongo_uri, mongo_db, user_skills):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.user_skills = user_skills

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

        # Call the Celery task for processing and saving the item
        result = process_and_save_item.delay(
            adapter.asdict(), spider.settings.get("MONGO_DATABASE"), self.user_skills
        )
        spider.logger.info(result.get())
        return item
