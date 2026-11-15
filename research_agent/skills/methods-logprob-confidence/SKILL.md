---
name: methods-logprob-confidence
description: >
  Extract next-token log probabilities from OpenAI models using use_code and logprobs for classification confidence scoring.
  Use when the user wants to measure model confidence in a classification task or get probability distributions over answer options.
tags: [methods, quantitative, analysis]
---

# Token Probabilities with EDSL

Use this skill when a user wants to measure **model confidence** in a classification task — i.e., get the probability the model assigns to each answer option, not just the top choice.

## How It Works

EDSL can extract log probabilities from OpenAI models by combining two features:

1. **`use_code=True`** on a `QuestionMultipleChoice` — forces the model to respond with a single-token numeric code (`0`, `1`, `2`, …) instead of the full option text. This ensures the answer is always a single token.
2. **`logprobs=True`** on the `Model` — tells the OpenAI API to return log probabilities for the top tokens in the response.

Together, these let you read off the probability the model assigned to each answer option.

> **Provider constraint**: `logprobs` is an OpenAI-specific API feature. Use an OpenAI model — pick one with `service == "openai"` from `ep models`; do not hardcode a name from memory. Anthropic and other providers do not expose log probabilities through EDSL.

---

## Complete Working Example

### Step 1: Set up the question with `use_code=True`

```python
from edsl import QuestionMultipleChoice, Agent, Model

q = QuestionMultipleChoice(
    question_name="sentiment",
    question_text=(
        "Classify the sentiment of the following text:\n\n"
        "{{ scenario.text }}"
    ),
    question_options=["Positive", "Negative", "Neutral"],
    use_code=True,
    include_comment=False,
)
```

With `use_code=True`, EDSL instructs the model to answer with just the option index:
- `0` = "Positive"
- `1` = "Negative"
- `2` = "Neutral"

Setting `include_comment=False` prevents the model from generating additional explanation tokens, keeping the response to a single code token.

### Step 2: Configure the model with `logprobs=True`

```python
m = Model("gpt-4.1", temperature=1, logprobs=True)
```

- `temperature=1` gives the model's natural (unmodified) probability distribution — the best default for measuring confidence. Lower temperatures sharpen the distribution; `temperature=0` (greedy) concentrates nearly all mass on one token.
- `logprobs=True` enables the OpenAI API's logprobs field in the response.

### Step 3: Run the survey

```python
from edsl import Scenario, ScenarioList

scenarios = ScenarioList([
    Scenario({"text": "I love this product, it's amazing!"}),
    Scenario({"text": "Terrible experience, would not recommend."}),
    Scenario({"text": "The package arrived on Tuesday."}),
])

results = q.by(scenarios).by(m).run()
```

### Step 4: Extract probabilities from the raw response

```python
import math

# Build the code-to-label mapping
options = {str(i): label for i, label in enumerate(q.question_options)}
# {'0': 'Positive', '1': 'Negative', '2': 'Neutral'}

for i, result in enumerate(results):
    raw = result["raw_model_response"]["sentiment_raw_model_response"]
    top_logprobs = raw["choices"][0]["logprobs"]["content"][0]["top_logprobs"]

    print(f"\n--- Scenario {i}: {scenarios[i]['text'][:50]}...")
    for token_info in top_logprobs:
        label = options.get(token_info["token"])
        if label:
            prob = math.exp(token_info["logprob"])
            print(f"  {label}: {prob:.3f}")
```

Example output:
```
--- Scenario 0: I love this product, it's amazing!...
  Positive: 0.987
  Neutral: 0.011
  Negative: 0.002

--- Scenario 1: Terrible experience, would not recommend....
  Negative: 0.954
  Neutral: 0.032
  Positive: 0.014

--- Scenario 2: The package arrived on Tuesday....
  Neutral: 0.891
  Positive: 0.078
  Negative: 0.031
```

---

## Collecting Probabilities into a DataFrame

For analysis, build a tidy DataFrame with one row per scenario and one column per option probability:

```python
import math
import pandas as pd

options = {str(i): label for i, label in enumerate(q.question_options)}
rows = []

for i, result in enumerate(results):
    raw = result["raw_model_response"]["sentiment_raw_model_response"]
    top_logprobs = raw["choices"][0]["logprobs"]["content"][0]["top_logprobs"]

    row = {"scenario_index": i, "text": scenarios[i]["text"]}
    for token_info in top_logprobs:
        label = options.get(token_info["token"])
        if label:
            row[f"prob_{label}"] = math.exp(token_info["logprob"])

    # The chosen answer
    row["answer"] = result["answer"]["sentiment"]
    rows.append(row)

df = pd.DataFrame(rows)
print(df)
```

---

## Using with Agents

You can combine with agents to see how different personas affect classification confidence:

```python
agents = [
    Agent(traits={"persona": "optimistic person"}),
    Agent(traits={"persona": "pessimistic person"}),
    Agent(traits={"persona": "neutral analyst"}),
]

results = q.by(scenarios).by(agents).by(m).run()
```

Then extract probabilities the same way, adding the agent persona to each row.

---

## Using with Multiple Models

Compare confidence across different OpenAI models:

```python
from edsl import ModelList

models = ModelList([
    Model("gpt-4.1", temperature=1, logprobs=True),
    Model("gpt-4.1-mini", temperature=1, logprobs=True),
])

results = q.by(scenarios).by(models).run()
```

Access the model name for each result via `result["model"]["model"]`.

---

## Key Parameters Reference

| Parameter | Where | Purpose |
|-----------|-------|---------|
| `use_code=True` | `QuestionMultipleChoice(...)` | Forces single-token code output (`0`, `1`, `2`, …) |
| `include_comment=False` | `QuestionMultipleChoice(...)` | Suppresses explanation text after the code |
| `logprobs=True` | `Model(...)` | Enables log probability output from OpenAI |
| `temperature=1` | `Model(...)` | Recommended — gives the model's natural confidence distribution |

## Accessing the Raw Response

The raw model response is stored at:

```python
raw = result["raw_model_response"]["<question_name>_raw_model_response"]
```

The logprobs structure (OpenAI format):

```python
raw["choices"][0]["logprobs"]["content"][0]["top_logprobs"]
# Returns a list of dicts: [{"token": "0", "logprob": -0.013, ...}, ...]
```

Convert log probability to probability: `math.exp(logprob)`

## Gotchas

- **OpenAI models only** — Anthropic, Google, and other providers do not return logprobs through EDSL.
- **`temperature` affects the distribution** — `temperature=1` reflects the model's natural confidence. `temperature=0` (greedy) collapses nearly all mass onto one token, making probabilities uninformative. Values between 0 and 1 sharpen; values above 1 flatten.
- **Not all tokens may appear in `top_logprobs`** — OpenAI returns up to 5 top tokens by default. If an option has very low probability, it may be absent from the list.
- **Token mapping depends on `use_code=True`** — Without it, the model outputs the full option text (e.g., "Positive"), which may be multiple tokens, making logprobs extraction unreliable.
- **The code-to-label mapping is positional** — Code `"0"` maps to the first option, `"1"` to the second, etc. Build the mapping from `question_options` as shown above.
