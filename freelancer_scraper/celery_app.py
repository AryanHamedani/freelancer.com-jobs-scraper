from pymongo import MongoClient
from celery import Celery

app = Celery(
    "freelancer_scraper",
    broker="pyamqp://guest@localhost//",
    backend="redis://localhost",
    include=["freelancer_scraper.tasks"],
)

app.conf.update(
    task_routes={
        "freelancer_scraper.tasks.process_and_save_item": {"queue": "processing"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

mongo_client = MongoClient()