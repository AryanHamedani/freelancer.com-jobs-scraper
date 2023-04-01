# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    budget = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    client = scrapy.Field()
    project_id = scrapy.Field()
    days_left = scrapy.Field()
    bids = scrapy.Field()
    customer_other_jobs = scrapy.Field()
    similar_jobs = scrapy.Field()
    project_duration = scrapy.Field()
    rating = scrapy.Field()
    verifications_status = scrapy.Field()
    priority_score = scrapy.Field()