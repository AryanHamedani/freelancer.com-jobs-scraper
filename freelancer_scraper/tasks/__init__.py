from freelancer_scraper.celery_app import app, mongo_client

@app.task
def process_and_save_item(item, mongo_db):
    db = mongo_client[mongo_db]
    existing_item = db.jobs.find_one({"url": item["url"]})
    if existing_item:
        return f"Item already exists: {item['url']}"
    db.jobs.insert_one(item)

    return f"Processed and saved item: {item['url']}"