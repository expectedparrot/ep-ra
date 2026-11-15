# Concept Testing Code Examples

## Independent Evaluation Survey Questions (Job A)

Full question definitions for the independent evaluation survey. All questions reference the four scenario fields: `concept_name`, `concept_description`, `key_benefit`, `target_use_case`.

```python
from edsl import Survey, QuestionLinearScale, QuestionFreeText

q_appeal = QuestionLinearScale(
    question_name="appeal",
    question_text=(
        "Consider the following product concept:\n\n"
        "**{{ scenario.concept_name }}**: {{ scenario.concept_description }}\n\n"
        "Key benefit: {{ scenario.key_benefit }}\n"
        "Target use case: {{ scenario.target_use_case }}\n\n"
        "How appealing is this concept to you on a scale of 1 to 7?"
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Not at all appealing", 7: "Extremely appealing"},
)

q_uniqueness = QuestionLinearScale(
    question_name="uniqueness",
    question_text=(
        "Consider the following product concept:\n\n"
        "**{{ scenario.concept_name }}**: {{ scenario.concept_description }}\n\n"
        "Key benefit: {{ scenario.key_benefit }}\n"
        "Target use case: {{ scenario.target_use_case }}\n\n"
        "How unique or different is this concept compared to what is "
        "currently available? Rate on a scale of 1 to 7."
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Not at all unique", 7: "Extremely unique"},
)

q_purchase_intent = QuestionLinearScale(
    question_name="purchase_intent",
    question_text=(
        "Consider the following product concept:\n\n"
        "**{{ scenario.concept_name }}**: {{ scenario.concept_description }}\n\n"
        "Key benefit: {{ scenario.key_benefit }}\n"
        "Target use case: {{ scenario.target_use_case }}\n\n"
        "How likely would you be to purchase this product? "
        "Rate on a scale of 1 to 7."
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Definitely would not buy", 7: "Definitely would buy"},
)

q_clarity = QuestionLinearScale(
    question_name="clarity",
    question_text=(
        "Consider the following product concept:\n\n"
        "**{{ scenario.concept_name }}**: {{ scenario.concept_description }}\n\n"
        "Key benefit: {{ scenario.key_benefit }}\n"
        "Target use case: {{ scenario.target_use_case }}\n\n"
        "How clear and easy to understand is this concept? "
        "Rate on a scale of 1 to 7."
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Very confusing", 7: "Perfectly clear"},
)

q_most_appealing = QuestionFreeText(
    question_name="most_appealing",
    question_text=(
        "Consider the following product concept:\n\n"
        "**{{ scenario.concept_name }}**: {{ scenario.concept_description }}\n\n"
        "Key benefit: {{ scenario.key_benefit }}\n"
        "Target use case: {{ scenario.target_use_case }}\n\n"
        "What is the single most appealing thing about this concept?"
    ),
)

q_concerns = QuestionFreeText(
    question_name="concerns",
    question_text=(
        "Consider the following product concept:\n\n"
        "**{{ scenario.concept_name }}**: {{ scenario.concept_description }}\n\n"
        "Key benefit: {{ scenario.key_benefit }}\n"
        "Target use case: {{ scenario.target_use_case }}\n\n"
        "What concerns or reservations would you have about this product?"
    ),
)

survey_independent = Survey([
    q_appeal, q_uniqueness, q_purchase_intent, q_clarity,
    q_most_appealing, q_concerns,
])
```

> **CRITICAL**: Do **not** set `set_full_memory_mode()` on the independent evaluation survey.

## Analysis Scripts

### Mean scores per concept per dimension

```python
import pandas as pd
from edsl import Results

results = Results.git.load("data/results_independent.ep")
df = results.select(
    "scenario.concept_name",
    "agent.segment",
    "answer.appeal",
    "answer.uniqueness",
    "answer.purchase_intent",
    "answer.clarity",
).to_pandas()

score_cols = [
    "answer.appeal", "answer.uniqueness",
    "answer.purchase_intent", "answer.clarity",
]
summary = df.groupby("scenario.concept_name")[score_cols].mean().round(2)
print(summary)
```

### Ranking distribution

```python
import ast
from edsl import Results

results_rank = Results.git.load("data/results_ranking.ep")
df_rank = results_rank.select(
    "agent.segment",
    "answer.concept_ranking",
).to_pandas()

# Parse ranking lists
df_rank["rankings"] = df_rank["answer.concept_ranking"].apply(ast.literal_eval)
df_rank["top_choice"] = df_rank["rankings"].apply(lambda x: x[0])

top_choice_counts = df_rank["top_choice"].value_counts()
print("Top choice distribution:")
print(top_choice_counts)
```

### Segment analysis

```python
segment_scores = df.groupby(
    ["agent.segment", "scenario.concept_name"]
)[score_cols].mean().round(2)
print(segment_scores)
```

### Qualitative theme extraction

```python
df_qual = results.select(
    "scenario.concept_name",
    "answer.most_appealing",
    "answer.concerns",
).to_pandas()

for concept in df_qual["scenario.concept_name"].unique():
    subset = df_qual[df_qual["scenario.concept_name"] == concept]
    print(f"\n--- {concept} ---")
    print("Appeals:", subset["answer.most_appealing"].tolist())
    print("Concerns:", subset["answer.concerns"].tolist())
```
