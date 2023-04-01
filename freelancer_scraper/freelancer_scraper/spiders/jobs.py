import scrapy
from freelancer_scraper.items import JobItem
from freelancer_scraper.utils import is_skills_match

class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["www.freelancer.com"]
    start_urls = [
        "https://www.freelancer.com/jobs/ajax/?results=100",
        "https://www.freelancer.com/jobs/api-developmet/?results=100",
        "https://www.freelancer.com/jobs/api/?results=100",
        "https://www.freelancer.com/jobs/beautifulsoup/?results=100",
        "https://www.freelancer.com/jobs/celery/?results=100",
        "https://www.freelancer.com/jobs/chart-js/?results=100",
        "https://www.freelancer.com/jobs/chatgpt/?results=100",
        "https://www.freelancer.com/jobs/coding/?results=100",
        "https://www.freelancer.com/jobs/data-collection/?results=100",
        "https://www.freelancer.com/jobs/database-development/?results=100",
        "https://www.freelancer.com/jobs/database-programming/?results=100",
        "https://www.freelancer.com/jobs/development/?results=100",
        "https://www.freelancer.com/jobs/django/?results=100",
        "https://www.freelancer.com/jobs/docker/?results=100",
        "https://www.freelancer.com/jobs/ecommerce/?results=100",
        "https://www.freelancer.com/jobs/mongodb/?results=100",
        "https://www.freelancer.com/jobs/mysql/?results=100",
        "https://www.freelancer.com/jobs/postgresql/?results=100",
        "https://www.freelancer.com/jobs/python/?results=100",
        "https://www.freelancer.com/jobs/rest-api/?results=100",
        "https://www.freelancer.com/jobs/selenium/?results=100",
        "https://www.freelancer.com/jobs/scrapy/?results=100",
        "https://www.freelancer.com/jobs/telegram-api/?results=100",
        "https://www.freelancer.com/jobs/web-application/?results=100",
        "https://www.freelancer.com/jobs/web-development/?results=100",
        "https://www.freelancer.com/jobs/web-scraping/?results=100",
        "https://www.freelancer.com/jobs/web-api/?results=100",
        "https://www.freelancer.com/jobs/website-build/?results=100",
        "https://www.freelancer.com/jobs/data-scraping/?results=100",
        "https://www.freelancer.com/jobs/data-processing/?results=100",
        "https://www.freelancer.com/jobs/data-entry/?results=100",
        "https://www.freelancer.com/jobs/data-mining/?results=100",
    ]

    def parse(self, response):
        item_links = response.xpath(
            "//a[contains(@class, 'JobSearchCard-primary-heading-link')]/@href"
        ).getall()

        for link in item_links:
            yield response.follow(link, callback=self.parse_item)

        paginations_partial_url = response.xpath(
            "//div[@id='bottom-pagination']//a/@href"
        ).getall()

        for partial_url in paginations_partial_url:
            pagination_url = response.urljoin(partial_url + "?results=100")
            yield response.follow(pagination_url, callback=self.parse)

    def parse_item(self, response):
        item = JobItem()
        item["title"] = response.xpath(
            '//main[@id="main"]//h1[contains(@class, "PageProjectViewLogout-header-title")]/text()'
        ).get()
        item["url"] = response.url
        item["status"] = response.xpath(
            '//main[@id="main"]//div[contains(@class, "PageProjectViewLogout-header-label")]/span/text()'
        ).get()
        item["budget"] = response.xpath('//span[text()="Budget "]/../text()').get()
        item["description"] = response.xpath(
            '//p[text()="Job Description: "]/following-sibling::*[following::p/strong[text()="Skills:"]]/text()'
        ).getall()
        item["skills"] = response.xpath(
            '//strong[text()="Skills:"]/../a/text()'
        ).getall()
        item["project_id"] = response.xpath(
            '//strong[text()="Project ID:"]/../text()'
        ).get()
        item["bids"] = response.xpath(
            '//h2[contains(text(), "bidding on average")]/text()'
        ).get()
        description = " ".join(item["description"])
        item["skills_match"] = is_skills_match(description)
        return item
