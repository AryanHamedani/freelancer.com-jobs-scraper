from sklearn.preprocessing import MinMaxScaler
import re
import openai

openai.api_key = "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"


def is_skills_match(description, user_skills):
    user_skills_str = ", ".join(user_skills)
    prompt_template = (
        "Given the following project description: '{description}', "
        "and considering the following skills: '{user_skills}', "
        "are these skills sufficient to successfully complete the project? "
        "Please provide a brief justification for your answer and respond with 'yes' or 'no' at the start."
    )
    prompt = prompt_template.format(
        description=description, user_skills=user_skills_str
    )
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=2047,
        n=1,
        stop=None,
        temperature=0.5,
    )
    match_result = re.search(r"\b(?:Yes)\.?\b", response.choices[0].text.strip())

    return 1 if match_result else 0, response.choices[0].text.strip()


def generate_bid(description, user_skills):
    prompt_template = (
        "As Alireza Chehereh, a senior full stack developer, generate a concise and professional bid proposal "
        "for a project on freelancer.com. "
        "Given the following project description: '{description}', "
        "and considering the following skills: '{user_skills}', "
        "please generate a brief and persuasive bid proposal for the project. "
        "In your response, demonstrate understanding of the project requirements, "
        "explain how the listed skills will be utilized."
    )
    user_skills_str = ", ".join(user_skills)
    prompt = prompt_template.format(
        description=description, user_skills=user_skills_str
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2047,
        n=1,
        stop=None,
        temperature=0.5,
    )

    bid_proposal = response.choices[0].text.strip()

    return bid_proposal


# def calculate_priority_score(item, user_skills, weights):
#     scaler = MinMaxScaler()
#     budget = scaler.fit_transform([[item["budget"]]])[0][0]
#     bids = scaler.fit_transform([[item["bids"]]])[0][0]
#     skills_match = is_skills_match("".join(item["description"]), user_skills)
#     priority_score = (
#         weights["budget"] * budget
#         + weights["skills_match"] * skills_match_value
#         + weights["customer_rating"] * item["rating"]
#         + weights["bid_competition"] * (1 - bids)
#         + weights["verifications_status"] * item["verifications_status"]
#     )
#     priority_score = scaler.fit_transform([[priority_score]])[0][0]
#     return priority_score
