---
name: methods-thematic-analysis
description: >
  Inductively discover themes in a column of free-text responses (from an EDSL
  Results object, a CSV export, or any tabular source), then label every
  response against the discovered codebook. Use when the user has free-text
  data and wants to identify recurring themes, produce a codebook, or quantify
  theme frequencies with representative quotes.
tags: [methods, qualitative, analysis, content-analysis]
---

# Thematic Analysis of Free-Text Responses

Use this skill whenever you have **a column of free-text responses** and want to go beyond raw quotes — finding the themes that recur, labeling every response, and quantifying how common each theme is.

The source of the responses does not matter: they can come from an EDSL survey, a Qualtrics or SurveyMonkey CSV export, a scraped dataset, or any other tabular file.

The workflow has two passes:
1. **Discovery pass** — sample a subset of responses, ask a model to propose a thematic codebook
2. **Labeling pass** — apply the codebook to every response using the data-labeling pattern

This produces a fully coded dataset suitable for reporting, even when no codebook existed at the start.

## When to use this skill

- You have a column of free-text responses (from any source) and want to find recurring themes
- You want representative quotes for each theme
- You want a sentiment distribution alongside thematic coding
- A codebook does not yet exist (inductive approach) or you have a predefined one (deductive approach)

## Not the right skill

| Need | Use instead |
|------|-------------|
| Label structured (non-text) fields in a CSV | `research_agent/skills/research-data-labeling/SKILL.md` |
| Code interview transcripts from .docx files | `research_agent/skills/methods-transcripts-to-personas/SKILL.md` |
| Extract structured fields (names, dates, amounts) | `research_agent/skills/research-data-labeling/SKILL.md` with `QuestionExtract` |

## Consider bewley for deeper qualitative work

This skill treats thematic analysis as a classification task: label each response with one or more themes, then count frequencies. That works well for large datasets of short responses where the goal is quantitative summaries (bar charts, cross-tabs, heatmaps).

But if the goal is **genuine qualitative analysis** — understanding *how* themes develop within a text, tracing relationships between codes, or producing an auditable evidence trail — consider using `skill:research-qualitative-data-analysis` (the bewley CLI) instead, or as a complement.

**When bewley adds value over EDSL-only thematic analysis:**

| Dimension | EDSL approach (this skill) | Bewley approach |
|-----------|---------------------------|-----------------|
| Annotation granularity | Whole-response or whole-paragraph labels | Line-level or byte-range annotations anchored to exact text |
| Narrative structure | Lost — a paragraph gets a label regardless of where themes appear within it | Preserved — you can see how themes sequence within a document |
| Evidence trail | Model assigns a label; no record of *why* | Every code linked to a specific quote; auditable and exportable |
| Code relationships | Co-occurrence counts only | Hierarchies (parent-child), links between codes, theory diagrams |
| Analytical memos | Not supported | First-class objects attached to codes, documents, or the project |
| Output format | CSV tables and matplotlib charts | Interactive HTML quote explorer, collapsible theory diagrams, JSON exports |
| Best for | Large corpora (100+ responses), quantitative reporting, cross-group comparisons | Smaller corpora (5-50 documents), deep reading, theory building, publishable qualitative research |

**Hybrid approach (recommended for medium-sized corpora):** Use EDSL for the discovery pass (Step 2 of this skill — it is excellent at generating candidate codes from a sample). Then import those codes into bewley and do line-level annotation across all documents. The quantitative plots can still be generated from bewley's export data, but you also get the interactive theory diagram and quote explorer that make the analysis auditable and the report more convincing.

## What it produces

- **Coded responses CSV** (in `data/coded/`) — every response with assigned theme(s) and sentiment label
- **Approved codebook** (in `data/coded/`) — the discovered or applied theme definitions
- **Theme frequency table** (in `writeup/tables/`) — theme name, count, percentage, example quote
- **Theme bar chart** (in `writeup/plots/`) — horizontal bar chart of theme frequencies
- **Sentiment pie chart** (in `writeup/plots/`) — sentiment distribution (if sentiment step run)

Name output files to reflect the survey or question they cover (e.g., `biggest_challenge_coded.csv`, `challenge_theme_frequencies.csv`). Follow the study file organization conventions in `research_agent/skills/workflow-file-layout/SKILL.md`.

---

## Prerequisites

The ep-agent runtime owns these dependencies. Do not install or upgrade them
during a study. Verify the imports before analysis:

```bash
python3 -c "import edsl, pandas, matplotlib"
```

If the check fails, report the environment problem rather than mutating the
sandbox.

---

## Step 1: Load the free-text responses

The starting point is simply a Python list of strings — one string per response. How you get there depends on your data source.

### From an EDSL Results object

```python
from edsl import Results
import pandas as pd

results = Results.git.load("data/raw/results.ep")
df = results.to_pandas()

# EDSL stores answers as "answer.<question_name>"
print([c for c in df.columns if c.startswith("answer.")])

free_text_col = "answer.your_question_name"
responses = df[free_text_col].dropna().tolist()
print(f"{len(responses)} non-null responses loaded")
```

### From a CSV file (Qualtrics, SurveyMonkey, or any export)

```python
import pandas as pd

df = pd.read_csv("data/uploaded/survey_export.csv")

# Inspect columns to find the free-text column
print(df.columns.tolist())

# Replace "Your open-ended question here" with the actual column header
responses = df["Your open-ended question here"].dropna().tolist()
print(f"{len(responses)} non-null responses loaded")
```

Either path produces the same `responses` list for all subsequent steps.

---

## Step 2: Discovery pass — propose a codebook from a sample

Draw a random sample of responses and ask a model to propose a thematic codebook. Use a single `QuestionFreeText` directed at the model, passing the full sample as a single scenario.

```python
from edsl import Survey, QuestionFreeText, ScenarioList, Scenario, Model

# Sample up to 50 responses for theme discovery
import random
sample = random.sample(responses, min(50, len(responses)))
sample_text = "\n---\n".join(f"Response {i+1}: {r}" for i, r in enumerate(sample))

q_discover = QuestionFreeText(
    question_name="codebook_proposal",
    question_text=(
        "You are a qualitative researcher. Read the following open-ended survey responses "
        "and identify the main recurring themes. For each theme:\n"
        "- Give it a short label (2-5 words)\n"
        "- Write a one-sentence definition\n"
        "- Note any sub-themes if relevant\n\n"
        "Aim for 4-8 themes that are mutually exclusive and exhaustive. "
        "Include an 'Other / Unclear' theme as a catch-all.\n\n"
        "RESPONSES:\n{{ scenario.sample_text }}"
    ),
)

scenario = ScenarioList([Scenario({"sample_text": sample_text})])
model = Model("...")  # WebSearch + ep models — never hardcode a model name

result = Survey([q_discover]).by(scenario).by(model).run()
codebook_raw = result.to_pandas()["answer.codebook_proposal"].iloc[0]
print(codebook_raw)
```

### Review and edit the proposed codebook

Save the raw proposal to a file, review it, and edit it before proceeding:

```python
import os
os.makedirs("data/coded", exist_ok=True)
with open("data/coded/codebook_draft.md", "w") as f:
    f.write(codebook_raw)
```

Open the draft, review it, trim or merge themes, then save the approved version (e.g., `data/coded/codebook.md`). **Always present the codebook to the user for approval before running the full labeling pass.**

---

## Step 3: Build a labeling survey using the approved codebook

Once the codebook is approved, translate each theme into a labeling question. The recommended approach uses one `QuestionMultipleChoice` for the primary theme and one `QuestionYesNo` for each secondary theme of interest. For simple cases, a single multiple-choice question suffices.

### Simple: single primary theme

```python
from edsl import Survey, QuestionMultipleChoice, ScenarioList, Scenario

# Read your approved codebook themes
themes = [
    "Cost concerns",
    "Ease of use",
    "Customer support",
    "Feature requests",
    "Positive experience",
    "Other / Unclear",
]

q_theme = QuestionMultipleChoice(
    question_name="primary_theme",
    question_text=(
        "Read the following survey response and assign it to the most appropriate theme.\n\n"
        "THEMES:\n"
        "- Cost concerns: respondent mentions price, affordability, or value for money\n"
        "- Ease of use: respondent mentions usability, learning curve, or interface\n"
        "- Customer support: respondent mentions help, support staff, or response time\n"
        "- Feature requests: respondent asks for new or missing functionality\n"
        "- Positive experience: respondent expresses general satisfaction\n"
        "- Other / Unclear: does not fit any of the above\n\n"
        "RESPONSE:\n{{ scenario.response_text }}"
    ),
    question_options=themes,
)

survey = Survey([q_theme])
```

### With sentiment

Add a sentiment question to the same survey pass to avoid an extra job:

```python
from edsl import QuestionMultipleChoice

q_sentiment = QuestionMultipleChoice(
    question_name="sentiment",
    question_text=(
        "What is the overall sentiment of this response?\n\n"
        "RESPONSE:\n{{ scenario.response_text }}"
    ),
    question_options=["Positive", "Neutral", "Negative", "Mixed"],
)

survey = Survey([q_theme, q_sentiment])
```

### Build the scenario list from responses

Each response becomes one scenario. The field name must match what you reference in `question_text`:

```python
scenario_list = ScenarioList([
    Scenario({"response_text": r}) for r in responses
])
```

> **IMPORTANT**: Every field in the ScenarioList must appear in at least one `question_text` using `{{ scenario.field_name }}` syntax, or EDSL raises a `JobsCompatibilityError`.

---

## Step 4: Run a sample first, then full labeling

Always run on a small sample before committing to the full dataset:

```python
from edsl import Model

model = Model("...")  # WebSearch + ep models — never hardcode a model name

# Sample run
sample_scenarios = ScenarioList(scenario_list[:10])
# Build a sample jobs.ep, estimate cost, and run through the CLI:
# ep jobs cost edsl_jobs/job_sample/jobs.ep
# ep run edsl_jobs/job_sample/jobs.ep --output data/raw/sample_results.ep
from edsl import Results
sample_results = Results.git.load("data/raw/sample_results.ep")
sample_df = sample_results.to_pandas()
print(sample_df[["scenario.response_text", "answer.primary_theme", "answer.sentiment"]].to_string())
```

Present the sample output to the user. Once approved, run the full dataset:

```python
# Confirm with user before running:
# ep jobs cost edsl_jobs/job_a/jobs.ep
# ep run edsl_jobs/job_a/jobs.ep --output data/raw/labeling_results.ep
```

---

## Step 5: Export and analyze

### Export coded CSV

```python
df = full_results.to_pandas()

coded = df[["scenario.response_text", "answer.primary_theme", "answer.sentiment"]].copy()
coded.columns = ["response_text", "primary_theme", "sentiment"]
coded.to_csv("data/coded/responses_coded.csv", index=False)
```

### Theme frequency table

```python
import pandas as pd

theme_counts = coded["primary_theme"].value_counts().reset_index()
theme_counts.columns = ["theme", "count"]
theme_counts["pct"] = (theme_counts["count"] / len(coded) * 100).round(1)

# Add a representative quote for each theme
def pick_quote(theme):
    subset = coded[coded["primary_theme"] == theme]["response_text"]
    if subset.empty:
        return ""
    # Pick the shortest non-trivial quote as representative
    candidates = subset[subset.str.len() > 20].sort_values(key=lambda x: x.str.len())
    return candidates.iloc[0] if not candidates.empty else subset.iloc[0]

theme_counts["example_quote"] = theme_counts["theme"].apply(pick_quote)
theme_counts.to_csv("writeup/tables/theme_frequencies.csv", index=False)
print(theme_counts.to_string(index=False))
```

### Theme bar chart

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"] = "DejaVu Sans"

fig, ax = plt.subplots(figsize=(8, 4))
colors = plt.cm.Blues_r([i / len(theme_counts) for i in range(len(theme_counts))])

ax.barh(theme_counts["theme"], theme_counts["pct"], color=colors)
ax.set_xlabel("Percentage of responses (%)")
ax.set_title("Theme distribution across responses")
ax.invert_yaxis()
for i, (_, row) in enumerate(theme_counts.iterrows()):
    ax.text(row["pct"] + 0.3, i, f"{row['pct']:.1f}%", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("writeup/plots/theme_bar.png", dpi=150, bbox_inches="tight")
plt.close()
```

### Sentiment pie chart (if sentiment question was asked)

```python
sentiment_counts = coded["sentiment"].value_counts()
colors_sentiment = {"Positive": "#4CAF50", "Neutral": "#9E9E9E",
                    "Negative": "#F44336", "Mixed": "#FF9800"}

fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(
    sentiment_counts.values,
    labels=sentiment_counts.index,
    autopct="%1.1f%%",
    colors=[colors_sentiment.get(s, "#AAAAAA") for s in sentiment_counts.index],
    startangle=90,
)
ax.set_title("Sentiment distribution")
plt.tight_layout()
plt.savefig("writeup/plots/sentiment_pie.png", dpi=150, bbox_inches="tight")
plt.close()
```

---

## Step 6: Deductive approach (predefined codebook)

If the user already has a codebook, skip the discovery pass entirely. Translate their codebook directly into a labeling survey (Step 3) and proceed.

For qualitative research where the codebook was developed from interview transcripts in `.docx` format, see `research_agent/skills/methods-transcripts-to-personas/SKILL.md` instead — that skill handles the full `.docx` → taxonomy → AgentList pipeline.

---

## Multi-label coding

If responses can belong to more than one theme, use `QuestionCheckBox` instead of `QuestionMultipleChoice`:

```python
from edsl import QuestionCheckBox

q_themes_multi = QuestionCheckBox(
    question_name="themes_present",
    question_text=(
        "Which of the following themes are present in this response? "
        "Select all that apply.\n\n"
        "RESPONSE:\n{{ scenario.response_text }}"
    ),
    question_options=themes,
)
```

---

## Study structure

```
<study_dir>/
  plan.md
  checklist.md
  data/
    uploaded/                    # Original CSV or data files (if not from EDSL)
    raw/
      results.ep                 # EDSL survey results (if source is EDSL)
      labeling_results.ep        # Labeling pass results
    coded/
      codebook_draft.md          # Auto-proposed codebook (pre-review)
      codebook.md                # Approved codebook
      <question>_coded.csv       # Every response with theme + sentiment labels
  analysis/
    analyze_themes.py            # Name to reflect the question being analyzed
  writeup/
    report.md
    plots/
      <question>_theme_bar.png
      <question>_sentiment_pie.png
    tables/
      <question>_theme_frequencies.csv
```

Name scripts and output files to reflect which question or column they analyze. Follow `research_agent/skills/workflow-file-layout/SKILL.md` for directory placement.

---

## Model selection guidance

| Task | Recommended tier | Notes |
|------|-----------------|-------|
| Discovery pass (codebook proposal) | Tier 1 or 2 | Higher-quality reading; run once on a sample |
| Labeling pass (all responses) | Tier 2 or 3 | Fast and cheap; quality is sufficient for classification |
| Sentiment only (no themes) | Tier 3 | Very cheap; high accuracy for 3-4 class sentiment |

Use WebSearch to find current model names for each tier, then confirm exact strings with `ep models`.

---

## Known issues

### Codebook drift
If the labeling model encounters a response that does not fit any theme, it will assign "Other / Unclear" or hallucinate a theme label not in your list. Mitigate by using `QuestionMultipleChoice` (which constrains to valid options) rather than `QuestionFreeText` for the labeling question.

### Long responses
Responses over 500 words may cause the model to truncate its reading. Truncate inputs in the scenario if needed:
```python
Scenario({"response_text": r[:800]})
```

### Inter-rater reliability
If publication-quality reliability is needed, run the labeling pass with two different models and compute Cohen's kappa on the disagreements. No EDSL-specific skill exists for this; use `sklearn.metrics.cohen_kappa_score` on the resulting DataFrames.
