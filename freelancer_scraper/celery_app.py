from pymongo import MongoClient
from celery import Celery
import os

app = Celery(
    "freelancer_scraper",
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND"),
    include=["freelancer_scraper.tasks"],
)

mongo_client = MongoClient(os.environ.get("MONGO_URI"))