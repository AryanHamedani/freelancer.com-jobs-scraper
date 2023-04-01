from sklearn.preprocessing import MinMaxScaler
import openai

openai.api_key = "your-openai-api-key"


def is_skills_match(description):
    user_skills = [
        "Python",
        "Django",
        "Flask",
        "FastAPI",
        "Database Design",
        "PostgreSQL",
        "MongoDB",
        "Celery",
        "Web Development",
        "Back-End Development",
        "RESTful API",
        "Linux",
        "Docker",
        "Web Scraping",
        "BeautifulSoup 4",
        "Selenium",
        "Scrapy",
        "Basic Front-End Development",
        "HTML",
        "CSS",
        "JavaScript",
        "Telegram Bot Design",
        "python-telegram-bot",
        "Pyrogram",
        "Bootstrap",
        "Tailwind",
    ]
    user_skills_str = ", ".join(user_skills)
    prompt_template = (
        "Given the following project description: '{description}', "
        "and considering the following skills: '{user_skills}', "
        "are these skills sufficient to successfully complete the project? "
        "Please provide a brief justification for your answer and respond with 'yes' or 'no' at the end."
    )
    prompt = prompt_template.format(
        description=description, user_skills=user_skills_str
    )
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    match_result = response.choices[0].text.strip().split()[-1].lower()
    return 1 if match_result == "yes" else 0


def skills_match(skills, user_skills):
    return len(set(skills).intersection(user_skills)) / len(skills)


def calculate_priority_score(item, user_skills, weights):
    scaler = MinMaxScaler()
    budget = scaler.fit_transform([[item["budget"]]])[0][0]
    bids = scaler.fit_transform([[item["bids"]]])[0][0]
    skills_match_value = skills_match(item["skills"], user_skills)
    priority_score = (
        weights["budget"] * budget
        + weights["project_duration"] * item["project_duration"]
        + weights["skills_match"] * skills_match_value
        + weights["customer_rating"] * item["rating"]
        + weights["bid_competition"] * (1 - bids)
        + weights["verifications_status"] * item["verifications_status"]
    )
    priority_score = scaler.fit_transform([[priority_score]])[0][0]
    return priority_score
