import scrapy
from freelancer_scraper.items import JobItem
from freelancer_scraper.utils import is_skills_match
import re


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

    def parse_item(self, response):
        item = JobItem()
        item["title"] = response.xpath(
            '//main[@id="main"]//h1[contains(@class, "PageProjectViewLogout-header-title")]/text()'
        ).get()
        item["url"] = response.url
        item["status"] = response.xpath(
            '//main[@id="main"]//div[contains(@class, "PageProjectViewLogout-header-label")]/span/text()'
        ).get()
        budget = response.xpath('//span[text()="Budget "]/../text()').get()
        match = re.search(r"([^\d]*)(\d+)-(\d+)\s*(\w+)", budget)
        if match:
            min_price = int(match.group(2))
            max_price = int(match.group(3))
            currency_code = match.group(4)
        else:
            min_price = max_price = currency_code = None
        item["min_budget"] = min_price
        item["max_budget"] = max_price
        item["currency_code"] = currency_code
        item["description"] = response.xpath(
            '//p[text()="Job Description: "]/following-sibling::*[following::p/strong[text()="Skills:"]]/text()'
        ).getall()
        item["skills"] = response.xpath(
            '//strong[text()="Skills:"]/../a/text()'
        ).getall()
        item["project_id"] = response.xpath(
            '//strong[text()="Project ID:"]/../text()'
        ).get()
        bid_sentence = response.xpath(
            '//h2[contains(text(), "bidding on average")]/text()'
        ).get()
        freelancers_match = re.search(r"(\d+)\s*freelancers", bid_sentence)
        freelancer_count = (
            int(freelancers_match.group(1)) if freelancers_match else None
        )
        average_bid_match = re.search(r"average\s*[^\d]*(\d+)", bid_sentence)
        average_bid_price = (
            int(average_bid_match.group(1)) if average_bid_match else None
        )
        item["count_of_bids"] = freelancer_count
        item["average_of_bids"] = average_bid_price
        item["rating"] = response.xpath(
            "//span[contains(@class, 'Rating')]/@data-star_rating"
        ).get()
        review_count_sentence = response.xpath(
            "//span[contains(@class, 'Rating-review')]/text()"
        ).get()
        item["count_of_reviews"] = int(re.findall(r"\d+", review_count_sentence)[0])
        item["verification_status"] = {
            "profile_completion": bool(
                response.xpath('//li[@data-qtsb-label="profile-complete"]').get()
            ),
            "payment_verified": bool(
                response.xpath('//li[@data-qtsb-label="payment-verified"]').get()
            ),
            "email_verified": bool(
                response.xpath('//li[@data-qtsb-label="email-verified"]').get()
            ),
            "phone_verified": bool(
                response.xpath('//li[@data-qtsb-label="phone-verified"]').get()
            ),
            "deposit_verified": bool(
                response.xpath('//li[@data-qtsb-label="deposit-made"]').get()
            ),
        }
        return item
