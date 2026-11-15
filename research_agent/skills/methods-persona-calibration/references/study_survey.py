"""Expanded diagnostic survey for multi-persona calibration.

15 questions total:
  - 10 calibration-pool questions (questions 1-10, same as study_a)
  - 5 true-holdout questions (questions 11-15, answers never shown to calibrator)
"""
from edsl import (
    Survey,
    QuestionMultipleChoice,
    QuestionLinearScale,
    QuestionFreeText,
)

# ---- Calibration pool (10 questions) ----

q_age = QuestionMultipleChoice(
    question_name="age_range",
    question_text="What is your age range?",
    question_options=["18-29", "30-44", "45-64", "65+"],
)

q_education = QuestionMultipleChoice(
    question_name="education",
    question_text="What is the highest level of education you have completed?",
    question_options=[
        "High school or less",
        "Some college or trade school",
        "Bachelor's degree",
        "Graduate degree",
    ],
)

q_party = QuestionMultipleChoice(
    question_name="party_id",
    question_text="Generally speaking, do you think of yourself as a...",
    question_options=["Democrat", "Republican", "Independent", "Something else"],
)

q_vote = QuestionMultipleChoice(
    question_name="vote_2020",
    question_text="Who did you vote for in the 2020 presidential election?",
    question_options=["Joe Biden", "Donald Trump", "Other candidate", "Did not vote"],
)

q_guns = QuestionMultipleChoice(
    question_name="gun_policy",
    question_text="Which comes closer to your view on gun policy?",
    question_options=[
        "Protect the right to own guns",
        "Control gun ownership",
        "Both equally",
    ],
)

q_climate = QuestionMultipleChoice(
    question_name="climate_action",
    question_text="Which comes closer to your view?",
    question_options=[
        "Climate change is a crisis requiring immediate action",
        "Climate change is real but proposed solutions cost too many jobs",
        "Climate change is not a serious problem",
    ],
)

q_trust = QuestionLinearScale(
    question_name="trust_institutions",
    question_text=(
        "How much do you trust major institutions (government, media, universities) "
        "to act in the interest of people like you?"
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "No trust at all", 7: "Complete trust"},
)

q_religion = QuestionMultipleChoice(
    question_name="religion_attendance",
    question_text="How often do you attend religious services?",
    question_options=[
        "Weekly or more",
        "A few times a month",
        "A few times a year",
        "Seldom or never",
    ],
)

q_trajectory = QuestionMultipleChoice(
    question_name="life_trajectory",
    question_text="Compared to 30 years ago, do you think life in America is...",
    question_options=[
        "Much better",
        "Somewhat better",
        "About the same",
        "Somewhat worse",
        "Much worse",
    ],
)

q_values = QuestionFreeText(
    question_name="free_text_values",
    question_text=(
        "In a few sentences, describe what matters most to you in life "
        "and what you are most concerned about for the future."
    ),
)

# ---- True holdout (5 questions) ----

q_immigration = QuestionMultipleChoice(
    question_name="immigration",
    question_text="Which comes closer to your view on immigration?",
    question_options=[
        "Immigrants strengthen the country",
        "Immigrants are a burden",
        "It depends on the circumstances",
    ],
)

q_income = QuestionMultipleChoice(
    question_name="income_bracket",
    question_text="What is your approximate annual household income?",
    question_options=[
        "Under $30k",
        "$30k-$60k",
        "$60k-$100k",
        "Over $100k",
    ],
)

q_social_media = QuestionMultipleChoice(
    question_name="social_media",
    question_text="How would you describe your social media use?",
    question_options=[
        "I use it daily",
        "I check it occasionally",
        "I rarely or never use it",
    ],
)

q_criminal_justice = QuestionMultipleChoice(
    question_name="criminal_justice",
    question_text="Which is a bigger problem in the criminal justice system?",
    question_options=[
        "Not enough law and order",
        "Too many people unfairly imprisoned",
        "Both are equal problems",
    ],
)

q_community = QuestionMultipleChoice(
    question_name="community_type",
    question_text="How would you describe where you live?",
    question_options=[
        "Large city",
        "Suburb",
        "Small town",
        "Rural area",
    ],
)

# ---- Assemble ----

calibration_pool_questions = [
    q_age,
    q_education,
    q_party,
    q_vote,
    q_guns,
    q_climate,
    q_trust,
    q_religion,
    q_trajectory,
    q_values,
]

true_holdout_questions = [
    q_immigration,
    q_income,
    q_social_media,
    q_criminal_justice,
    q_community,
]

questions = calibration_pool_questions + true_holdout_questions

CALIBRATION_POOL_NAMES = [q.question_name for q in calibration_pool_questions]
TRUE_HOLDOUT_NAMES = [q.question_name for q in true_holdout_questions]
STRUCTURED_CALIBRATION_NAMES = [
    q.question_name
    for q in calibration_pool_questions
    if q.question_name != "free_text_values"
]

survey = Survey(questions)
