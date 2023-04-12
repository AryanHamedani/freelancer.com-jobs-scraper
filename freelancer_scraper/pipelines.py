from itemadapter import ItemAdapter
from freelancer_scraper.tasks import process_and_save_item


class JobItemPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        result = process_and_save_item.delay(
            adapter.asdict(), spider.settings.get("MONGO_DATABASE")
        )
        spider.logger.info(result.get())
        return item
