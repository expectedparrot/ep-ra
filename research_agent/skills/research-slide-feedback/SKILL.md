---
name: research-slide-feedback
description: >
  Collect structured agent feedback on every slide in a deck (from a folder
  of images or a PDF), producing per-slide dimension scores and a summary
  ranking table.
  Use when the user wants to evaluate or critique a presentation deck.
tags: [study-type, qualitative, visualization]
---

# Slide Deck Feedback

Use this skill when a user wants structured critique of a presentation deck — each slide evaluated on dimensions like clarity, visual hierarchy, and message strength — with results aggregated into a ranked summary table.

Each slide is treated as a standalone image; feedback is collected per slide, then aggregated across the deck.

## When to use this skill

- User wants to know which slides are weakest and why
- User wants first-impression scores for every slide
- User wants to compare two versions of a deck (e.g., before vs. after redesign)

## Not the right skill

| Need | Use instead |
|------|-------------|
| Feedback on a website, interface screenshot, or prototype | `skill:research-ux-testing` |
| Side-by-side comparison of interface designs or pages | `skill:research-ux-testing` |
| Behavioral testing of a live website | `skill:research-ux-testing` |

## What it produces

- **EDSL results file** (in `data/raw/`) — full results for all slides and agents
- **Slide scores table** (in `writeup/tables/`) — slide number, per-dimension scores, overall rank
- **Dimension scores heatmap** (in `writeup/plots/`) — heatmap of scores by slide and dimension
- **Suggestions table** (in `writeup/tables/`) — free-text improvement suggestions per slide

Name output files to reflect the deck being evaluated (e.g., `pitch_deck_slide_scores.csv`, `pitch_deck_scores_heatmap.png`). Follow `research_agent/skills/workflow-file-layout/SKILL.md` for directory placement.

---

## Prerequisites

The ep-agent runtime owns these dependencies. Do not install or upgrade them
during a study. Verify the Python imports and Poppler executable:

```bash
python3 -c "import edsl, PIL, matplotlib, pdf2image"
pdftoppm -v
```

If either check fails, report the environment problem rather than mutating the
sandbox.

---

## Step 1: Prepare slide images

### From a folder of images

If the user has already exported slides as PNG or JPG files, place them in `captures/slides/`:

```
captures/slides/
  slide_01.png
  slide_02.png
  ...
  slide_N.png
```

Ensure the files sort alphanumerically in deck order (zero-pad slide numbers).

### From a PDF

Convert a PDF deck to per-slide images using `pdf2image`:

```python
from pdf2image import convert_from_path
import os

pdf_path = "data/uploaded/deck.pdf"
output_dir = "captures/slides"
os.makedirs(output_dir, exist_ok=True)

pages = convert_from_path(pdf_path, dpi=150)
for i, page in enumerate(pages, start=1):
    page.save(f"{output_dir}/slide_{i:02d}.png", "PNG")

print(f"Converted {len(pages)} slides to {output_dir}/")
```

### From Google Slides or PowerPoint

Export to PDF first (File → Download → PDF), then use the PDF path above.

---

## Step 2: Confirm slide list with user

Before running the full study, show the user the list of slide files and the planned dimensions. Present cost estimate and get approval.

```python
import os
from pathlib import Path

slide_dir = Path("captures/slides")
slides = sorted(slide_dir.glob("*.png")) + sorted(slide_dir.glob("*.jpg"))
print(f"Found {len(slides)} slides:")
for s in slides:
    print(f"  {s.name}")
```

---

## Step 3: Build the per-slide survey

Each slide becomes a Scenario with the slide image and its slide number. A standard question battery evaluates clarity, visual hierarchy, key message recall, information density, and overall impression.

### Build scenarios from slide images

```python
from edsl import Scenario, ScenarioList

scenarios = []
for i, slide_path in enumerate(slides, start=1):
    s = Scenario.from_image(str(slide_path))
    img_key = list(s.keys())[0]
    scenarios.append(Scenario({
        "slide_image": s[img_key],
        "slide_number": str(i),
        "slide_filename": slide_path.name,
    }))

scenario_list = ScenarioList(scenarios)
```

### Standard slide evaluation survey

```python
from edsl import Survey, QuestionLinearScale, QuestionFreeText, QuestionMultipleChoice

q_clarity = QuestionLinearScale(
    question_name="clarity",
    question_text=(
        "Look at slide {{ scenario.slide_number }} of this presentation:\n"
        "{{ scenario.slide_image }}\n\n"
        "How visually clear and easy to read is this slide? "
        "Rate from 1 (very unclear) to 7 (very clear)."
    ),
    question_options=list(range(1, 8)),
    option_labels={1: "Very unclear", 7: "Very clear"},
)

q_hierarchy = QuestionLinearScale(
    question_name="visual_hierarchy",
    question_text=(
        "Slide {{ scenario.slide_number }}: {{ scenario.slide_image }}\n\n"
        "How effective is the visual hierarchy — does your eye know where to go first? "
        "Rate from 1 (no clear hierarchy) to 7 (very clear hierarchy)."
    ),
    question_options=list(range(1, 8)),
    option_labels={1: "No clear hierarchy", 7: "Very clear hierarchy"},
)

q_message = QuestionLinearScale(
    question_name="message_strength",
    question_text=(
        "Slide {{ scenario.slide_number }}: {{ scenario.slide_image }}\n\n"
        "How clearly does this slide communicate a single key message? "
        "Rate from 1 (message is unclear or absent) to 7 (message is immediately obvious)."
    ),
    question_options=list(range(1, 8)),
    option_labels={1: "Unclear", 7: "Immediately obvious"},
)

q_density = QuestionMultipleChoice(
    question_name="information_density",
    question_text=(
        "Slide {{ scenario.slide_number }}: {{ scenario.slide_image }}\n\n"
        "How would you describe the amount of information on this slide?"
    ),
    question_options=["Too sparse", "About right", "Slightly too much", "Way too much"],
)

q_suggestion = QuestionFreeText(
    question_name="top_suggestion",
    question_text=(
        "Slide {{ scenario.slide_number }}: {{ scenario.slide_image }}\n\n"
        "What is the single most important improvement you would make to this slide? "
        "Be specific (one sentence)."
    ),
)

survey = Survey([q_clarity, q_hierarchy, q_message, q_density, q_suggestion])
```

> **IMPORTANT**: Every field in the ScenarioList (`slide_image`, `slide_number`, `slide_filename`) must be referenced in at least one question's `question_text`, or EDSL raises a `JobsCompatibilityError`. Reference `slide_filename` in a question if you want it passed through, or remove it from the Scenario.

If `slide_filename` is not referenced in any question, remove it from the Scenario dict:

```python
Scenario({
    "slide_image": s[img_key],
    "slide_number": str(i),
})
```

---

## Step 4: Build the agent panel

For slide feedback, a small panel of persona types is usually sufficient. Match personas to the intended audience of the deck (e.g., investors, conference attendees, hiring managers):

```python
from edsl import AgentList, Agent

agents = AgentList([
    Agent(traits={"role": "investor", "expertise": "early-stage startups"},
          instruction="You are evaluating this pitch deck as a potential investor."),
    Agent(traits={"role": "first-time viewer", "expertise": "general professional"},
          instruction="You are seeing this presentation for the first time as a professional audience member."),
    Agent(traits={"role": "designer", "expertise": "visual communication"},
          instruction="You are evaluating the design quality and visual communication of this slide."),
])
```

---

## Step 5: Sample run, then full run

Always run on the first two slides before committing to the full deck:

```python
from edsl import Model

model = Model("...")  # Vision-capable model required — WebSearch + ep models (works_with_images field) to confirm

# Build a sample jobs.ep with two scenarios, then run:
# ep jobs cost edsl_jobs/job_sample/jobs.ep
# ep run edsl_jobs/job_sample/jobs.ep --output data/raw/sample_results.ep

# Review sample
import pandas as pd
from edsl import Results
sample_results = Results.git.load("data/raw/sample_results.ep")
df_sample = sample_results.to_pandas()
print(df_sample[["scenario.slide_number", "agent.role",
                  "answer.clarity", "answer.message_strength",
                  "answer.top_suggestion"]].to_string())
```

Present to user for approval, then run full deck:

```python
# Estimate and run through the Makefile/CLI; confirm with user before proceeding.
# ep jobs cost edsl_jobs/job_a/jobs.ep
# ep run edsl_jobs/job_a/jobs.ep --output data/raw/results.ep
```

---

## Step 6: Aggregate and analyze

### Build the slide scores table

```python
import pandas as pd

df = full_results.to_pandas()

numeric_dims = ["clarity", "visual_hierarchy", "message_strength"]

# Average across agents for each slide and dimension
agg = (
    df.groupby("scenario.slide_number")[
        [f"answer.{d}" for d in numeric_dims]
    ]
    .mean()
    .round(2)
    .reset_index()
)
agg.columns = ["slide_number"] + numeric_dims
agg["overall_score"] = agg[numeric_dims].mean(axis=1).round(2)
agg = agg.sort_values("slide_number", key=lambda x: x.astype(int))
agg["rank"] = agg["overall_score"].rank(ascending=False).astype(int)

agg.to_csv("writeup/tables/slide_scores.csv", index=False)
print(agg.sort_values("rank").to_string(index=False))
```

### Dimension scores heatmap

```python
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.rcParams["font.family"] = "DejaVu Sans"

pivot = agg.set_index("slide_number")[numeric_dims].T
fig, ax = plt.subplots(figsize=(max(8, len(agg) * 0.6), 4))
im = ax.imshow(pivot.values, aspect="auto", cmap="RdYlGn", vmin=1, vmax=7)
ax.set_xticks(range(len(agg)))
ax.set_xticklabels([f"Slide {n}" for n in pivot.columns], rotation=45, ha="right")
ax.set_yticks(range(len(numeric_dims)))
ax.set_yticklabels([d.replace("_", " ").title() for d in numeric_dims])
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
plt.colorbar(im, cax=cax, label="Score (1-7)")
ax.set_title("Slide scores by dimension")
for i in range(len(numeric_dims)):
    for j in range(len(agg)):
        ax.text(j, i, f"{pivot.values[i, j]:.1f}", ha="center", va="center",
                fontsize=8, color="black")
plt.tight_layout()
plt.savefig("writeup/plots/slide_scores_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
```

### Top suggestions per slide

```python
suggestions = (
    df.groupby("scenario.slide_number")["answer.top_suggestion"]
    .apply(list)
    .reset_index()
)
suggestions.columns = ["slide_number", "suggestions"]

# Save for report
suggestions.to_csv("writeup/tables/slide_suggestions.csv", index=False)
```

---

## Comparing two decks

To compare an original deck against a revised version, run this workflow twice — once per deck — with the same agent panel and model. Then compute per-slide score deltas:

```python
df_v1 = pd.read_csv("writeup/tables/slide_scores_v1.csv")
df_v2 = pd.read_csv("writeup/tables/slide_scores_v2.csv")

delta = df_v1.copy()
for dim in numeric_dims:
    delta[dim] = (df_v2[dim] - df_v1[dim]).round(2)
delta["overall_score"] = (df_v2["overall_score"] - df_v1["overall_score"]).round(2)
delta.to_csv("writeup/tables/score_delta.csv", index=False)
```

---

## Study structure

```
<study_dir>/
  plan.md
  checklist.md
  data/
    uploaded/
      <deck_name>.pdf            # Original deck (if provided as PDF)
    raw/
      <deck_name>_results.ep
  captures/
    slides/
      slide_01.png
      slide_02.png
      ...
  analysis/
    <deck_name>_slide_feedback.py
  writeup/
    report.md
    plots/
      <deck_name>_scores_heatmap.png
    tables/
      <deck_name>_slide_scores.csv
      <deck_name>_slide_suggestions.csv
```

Use a descriptive prefix for the deck name (e.g., `pitch_deck_`, `onboarding_deck_`). Follow `research_agent/skills/workflow-file-layout/SKILL.md` for directory conventions.

---

## Model selection guidance

This skill requires a vision-capable model. Use WebSearch to identify the current vision-capable frontier model, then confirm the exact name with `ep models` — the `works_with_images` field tells you which models support vision.

| Use case | Recommended tier | Notes |
|----------|-----------------|-------|
| Full deck evaluation | Tier 1 vision-capable | Best vision quality; higher cost per slide |
| Large deck or cost-sensitive | Tier 2 vision-capable | Acceptable for rating questions; weaker on free-text suggestions |
| Eye-tracking pass | Tier 1 vision-capable | Vision quality matters for grid interpretation |

Use WebSearch to find current vision-capable model names, then confirm exact strings with `ep models` (filter on the `works_with_images` field).

Estimate total cost before running: a deck of 20 slides × 3 agents × 5 questions will typically cost $0.50–$2.00 depending on model.

---

## Known issues

### Slide ordering
If slides are not zero-padded (e.g., `slide_1.png`, `slide_10.png`, `slide_2.png`), `sorted()` will produce alphabetic not numeric order. Always zero-pad filenames or sort with a key:

```python
slides = sorted(slide_dir.glob("*.png"), key=lambda p: int(p.stem.split("_")[-1]))
```

### Token limits on dense slides
Slides with very small text (e.g., dense data tables, code listings) may exceed the model's effective vision resolution. In these cases, split the slide into top and bottom halves as two separate scenarios, or note in the report that the model may not have read fine-grained text.

### PDF rendering quality
`pdf2image` at `dpi=150` produces 1275×825px images from a standard 8.5×11 slide at 150dpi. Increase to `dpi=200` if text is rendering blurry. Higher DPI increases file size and token cost.
