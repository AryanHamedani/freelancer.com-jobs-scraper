# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    max_budget = scrapy.Field()
    min_budget = scrapy.Field()
    currency_code = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    project_id = scrapy.Field()
    count_of_bids = scrapy.Field()
    average_of_bids = scrapy.Field()
    rating = scrapy.Field()
    count_of_reviews = scrapy.Field()
    verification_status = scrapy.Field()
