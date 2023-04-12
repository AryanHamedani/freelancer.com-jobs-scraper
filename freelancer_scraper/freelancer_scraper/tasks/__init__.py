from freelancer_scraper.celery_app import app, mongo_client
from freelancer_scraper.utils import is_skills_match, generate_bid

@app.task
def is_skills_match_task(description, user_skills):
    return is_skills_match(description, user_skills)


@app.task
def generate_bid_task(description, user_skills):
    return generate_bid(description, user_skills)

@app.task
@app.task
def process_and_save_item(item, mongo_db, user_skills):
    db = mongo_client[mongo_db]
    existing_item = db.jobs.find_one({"url": item["url"]})
    if existing_item:
        return f"Item already exists: {item['url']}"

    description = "".join(item["description"])
    match_result, justification = is_skills_match(description, user_skills)
    item["skills_match"] = match_result
    item["skills_match_justification"] = justification

    if match_result:
        bid_proposal = generate_bid(description, user_skills)
        item["bid_proposal"] = bid_proposal

        # Save the item in the database
        db.jobs.insert_one(item)

    return f"Processed and saved item: {item['url']}"