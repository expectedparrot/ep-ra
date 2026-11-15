# Message Testing: Setup Examples

Detailed code examples for defining variants, building surveys, and creating agent panels.

## Defining message variants

### Inline variants (most common)

```python
from edsl import ScenarioList, Scenario

variants = [
    {"variant_label": "A", "message_variant": "Unlock your potential with our new course"},
    {"variant_label": "B", "message_variant": "Master new skills in just 4 weeks"},
    {"variant_label": "C", "message_variant": "Join 10,000+ professionals who leveled up"},
]

scenario_list = ScenarioList([Scenario(v) for v in variants])
```

### From a CSV

```python
from edsl import ScenarioList

scenario_list = ScenarioList.from_csv("data/uploaded/variants.csv")
# CSV should have columns: variant_label, message_variant
```

### Multi-dimensional testing

Test message variants crossed with context variables (e.g., message x audience segment description, message x product category):

```python
from edsl import ScenarioList, Scenario

messages = [
    {"variant_label": "A", "message_variant": "Save 20% today only"},
    {"variant_label": "B", "message_variant": "Members get exclusive early access"},
]

contexts = [
    {"context": "shopping for running shoes"},
    {"context": "shopping for formal wear"},
]

# Cross-product: every message x every context
scenario_list = ScenarioList(
    [Scenario({**m, **c}) for m in messages for c in contexts]
)
```

> **IMPORTANT**: Every field in the ScenarioList must be referenced in at least one question's `question_text` using `{{ scenario.field_name }}` syntax, or EDSL raises a `JobsCompatibilityError`. If you use multi-dimensional scenarios, reference all fields in at least one question.

---

## Building the evaluation survey

### Standard question battery

```python
from edsl import (
    Survey,
    QuestionLinearScale,
    QuestionYesNo,
    QuestionFreeText,
)

q_appeal = QuestionLinearScale(
    question_name="appeal",
    question_text=(
        "How appealing is the following message?\n\n"
        "Message: {{ scenario.message_variant }}"
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Not at all appealing", 7: "Extremely appealing"},
)

q_clarity = QuestionLinearScale(
    question_name="clarity",
    question_text=(
        "How clear is the following message?\n\n"
        "Message: {{ scenario.message_variant }}"
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Very unclear", 7: "Perfectly clear"},
)

q_persuasion = QuestionLinearScale(
    question_name="persuasion",
    question_text=(
        "How persuasive is the following message?\n\n"
        "Message: {{ scenario.message_variant }}"
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Not at all persuasive", 7: "Extremely persuasive"},
)

q_action = QuestionYesNo(
    question_name="action",
    question_text=(
        "Would this message prompt you to take action "
        "(click, sign up, purchase, learn more)?\n\n"
        "Message: {{ scenario.message_variant }}"
    ),
)

q_impression = QuestionFreeText(
    question_name="impression",
    question_text=(
        "What is your overall impression of this message? "
        "What works well and what could be improved?\n\n"
        "Message: {{ scenario.message_variant }}"
    ),
)

survey = Survey(
    [q_appeal, q_clarity, q_persuasion, q_action, q_impression])
```

### Customizing the survey

**Add domain-specific metrics:**

```python
q_trust = QuestionLinearScale(
    question_name="trust",
    question_text=(
        "How trustworthy does this message feel?\n\n"
        "Message: {{ scenario.message_variant }}"
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Not trustworthy", 7: "Highly trustworthy"},
)
```

**Add a preference ranking** (when comparing a small set of variants):

```python
from edsl import QuestionRank

q_rank = QuestionRank(
    question_name="preference_rank",
    question_text="Rank these messages from most to least appealing.",
    question_options=[
        "Unlock your potential with our new course",
        "Master new skills in just 4 weeks",
        "Join 10,000+ professionals who leveled up",
    ],
)
```

**Change the scale** (e.g., 1-5 instead of 1-7):

```python
q_appeal_5pt = QuestionLinearScale(
    question_name="appeal",
    question_text="How appealing is this message?\n\nMessage: {{ scenario.message_variant }}",
    question_options=[1, 2, 3, 4, 5],
    option_labels={1: "Not appealing", 5: "Very appealing"},
)
```

**Reference context variables** (for multi-dimensional tests):

```python
q_relevance = QuestionLinearScale(
    question_name="relevance",
    question_text=(
        "How relevant is this message to someone who is {{ scenario.context }}?\n\n"
        "Message: {{ scenario.message_variant }}"
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Not relevant", 7: "Highly relevant"},
)
```

---

## Defining the agent panel

### Pattern 1: Demographic combinations (inline)

```python
from edsl import AgentList, Agent

agents = AgentList([
    Agent(
        traits={
            "persona": "A 28-year-old marketing professional in a mid-size city, "
                       "active on social media, early adopter of new tools.",
            "age": "28",
            "segment": "young_professional",
        }
    ),
    Agent(
        traits={
            "persona": "A 45-year-old senior manager at a Fortune 500 company, "
                       "skeptical of marketing claims, values data and ROI.",
            "age": "45",
            "segment": "senior_executive",
        }
    ),
    Agent(
        traits={
            "persona": "A 35-year-old small business owner, budget-conscious, "
                       "looking for practical solutions that save time.",
            "age": "35",
            "segment": "small_business_owner",
        }
    ),
    Agent(
        traits={
            "persona": "A 22-year-old college student, price-sensitive, "
                       "influenced by peer recommendations and social proof.",
            "age": "22",
            "segment": "student",
        }
    ),
])
```

### Pattern 2: From a persona CSV

```python
from edsl import AgentList

agent_list = AgentList.from_csv("data/uploaded/personas.csv")
# CSV columns become agent traits. Must include a "persona" column.
```

### Pattern 3: Programmatic panel from trait combinations

```python
from edsl import AgentList, Agent

age_groups = ["25-34", "35-44", "45-54"]
attitudes = ["tech-savvy early adopter", "pragmatic mainstream buyer", "skeptical late adopter"]

agent_list = AgentList([
    Agent(
        traits={
            "persona": f"A {age} year old who is a {attitude}.",
            "age_group": age,
            "attitude": attitude,
        }
    )
    for age in age_groups
    for attitude in attitudes
])
```

> **Panel size guidance**: A typical test uses 5-15 agents. More agents give richer segment analysis but increase cost linearly. Start small (3-5 agents) in the preview step, then expand for the full run.
