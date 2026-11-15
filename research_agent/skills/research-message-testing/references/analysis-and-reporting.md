# Message Testing: Analysis and Reporting

Detailed code examples for analyzing results and generating reports.

## Contents

- [Analysis scripts](#analysis-scripts)
- [Makefile integration](#makefile-integration)
- [Report template](#report-template)

---

## Analysis scripts

Create analysis scripts in `analysis/`, with outputs going to `writeup/plots/` and `writeup/tables/`.

### Mean scores by variant (grouped bar chart)

```python
# analysis/plot_scores_by_variant.py
from pathlib import Path
from edsl import Results
import matplotlib.pyplot as plt
import numpy as np

STUDY_ROOT = Path(__file__).resolve().parent.parent
results = Results.git.load(str(STUDY_ROOT / "data" / "results.ep"))

metrics = ["appeal", "clarity", "persuasion"]
df = results.select(
    "scenario.variant_label",
    *[f"answer.{m}" for m in metrics],
).to_pandas()

# Compute means per variant
variants = sorted(df["scenario.variant_label"].unique())
means = {m: [] for m in metrics}
for v in variants:
    subset = df[df["scenario.variant_label"] == v]
    for m in metrics:
        means[m].append(subset[f"answer.{m}"].astype(float).mean())

x = np.arange(len(variants))
width = 0.25
fig, ax = plt.subplots(figsize=(10, 6))
for i, m in enumerate(metrics):
    ax.bar(x + i * width, means[m], width, label=m.capitalize())

ax.set_xlabel("Variant")
ax.set_ylabel("Mean Score (1-7)")
ax.set_title("Mean Scores by Variant")
ax.set_xticks(x + width)
ax.set_xticklabels(variants)
ax.legend()
ax.set_ylim(0, 7.5)
plt.tight_layout()

output = STUDY_ROOT / "writeup" / "plots" / "scores_by_variant.png"
output.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output, dpi=150)
print(f"Saved {output}")
```

### Action rate by variant (bar chart)

```python
# analysis/plot_action_rate.py
from pathlib import Path
from edsl import Results
import matplotlib.pyplot as plt

STUDY_ROOT = Path(__file__).resolve().parent.parent
results = Results.git.load(str(STUDY_ROOT / "data" / "results.ep"))

df = results.select("scenario.variant_label", "answer.action").to_pandas()

# Compute action rate (fraction answering "Yes")
variants = sorted(df["scenario.variant_label"].unique())
rates = []
for v in variants:
    subset = df[df["scenario.variant_label"] == v]
    rate = (subset["answer.action"] == "Yes").mean()
    rates.append(rate)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(variants, rates, color="steelblue")
ax.set_xlabel("Variant")
ax.set_ylabel("Action Rate")
ax.set_title("Would Take Action (% Yes) by Variant")
ax.set_ylim(0, 1.05)
for bar, rate in zip(bars, rates):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.02,
        f"{rate:.0%}",
        ha="center",
    )
plt.tight_layout()

output = STUDY_ROOT / "writeup" / "plots" / "action_rate.png"
output.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output, dpi=150)
print(f"Saved {output}")
```

### Score heatmap: variants x metrics

```python
# analysis/plot_heatmap.py
from pathlib import Path
from edsl import Results
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

STUDY_ROOT = Path(__file__).resolve().parent.parent
results = Results.git.load(str(STUDY_ROOT / "data" / "results.ep"))

metrics = ["appeal", "clarity", "persuasion"]
df = results.select(
    "scenario.variant_label",
    *[f"answer.{m}" for m in metrics],
).to_pandas()

# Pivot to variant x metric means
pivot = df.groupby("scenario.variant_label")[[f"answer.{m}" for m in metrics]].mean()
pivot.columns = [m.capitalize() for m in metrics]

fig, ax = plt.subplots(figsize=(8, max(4, len(pivot) * 0.8)))
im = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto", vmin=1, vmax=7)

ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)
ax.set_title("Score Heatmap: Variants x Metrics")

# Annotate cells
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        ax.text(j, i, f"{pivot.values[i, j]:.1f}", ha="center", va="center")

from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
plt.colorbar(im, cax=cax, label="Mean Score")
plt.tight_layout()

output = STUDY_ROOT / "writeup" / "plots" / "heatmap.png"
output.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output, dpi=150)
print(f"Saved {output}")
```

### Agent segment analysis

Do different personas prefer different variants?

```python
# analysis/table_scores_by_segment.py
from pathlib import Path
from edsl import Results
import pandas as pd

STUDY_ROOT = Path(__file__).resolve().parent.parent
results = Results.git.load(str(STUDY_ROOT / "data" / "results.ep"))

metrics = ["appeal", "clarity", "persuasion"]
df = results.select(
    "scenario.variant_label",
    "agent.segment",
    *[f"answer.{m}" for m in metrics],
).to_pandas()

# For each numeric metric, cast to float
for m in metrics:
    df[f"answer.{m}"] = df[f"answer.{m}"].astype(float)

# Pivot: segment x variant, mean of composite score
df["composite"] = df[[f"answer.{m}" for m in metrics]].mean(axis=1)
pivot = df.pivot_table(
    values="composite",
    index="agent.segment",
    columns="scenario.variant_label",
    aggfunc="mean",
)

output = STUDY_ROOT / "writeup" / "tables" / "scores_by_segment.csv"
output.parent.mkdir(parents=True, exist_ok=True)
pivot.round(2).to_csv(output)
print(f"Saved {output}")
print(pivot.round(2).to_string())
```

### Qualitative theme summary

```python
# analysis/summarize_impressions.py
from pathlib import Path
from edsl import Results

STUDY_ROOT = Path(__file__).resolve().parent.parent
results = Results.git.load(str(STUDY_ROOT / "data" / "results.ep"))

df = results.select(
    "scenario.variant_label", "answer.impression"
).to_pandas()

# Group free-text impressions by variant for the report
output = STUDY_ROOT / "writeup" / "tables" / "impressions_by_variant.csv"
output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)
print(f"Saved {output}")

# Print a summary for each variant
for variant in sorted(df["scenario.variant_label"].unique()):
    subset = df[df["scenario.variant_label"] == variant]
    print(f"\n--- Variant {variant} ---")
    for _, row in subset.iterrows():
        print(f"  - {row['answer.impression'][:200]}")
```

---

## Makefile integration

```makefile
.PHONY: data PLOTS TABLES report all

data: data/results.ep

data/results.ep: edsl_jobs/job_a/jobs.ep
	ep run edsl_jobs/job_a/jobs.ep --output data/results.ep

PLOTS: writeup/plots/scores_by_variant.png writeup/plots/action_rate.png writeup/plots/heatmap.png

writeup/plots/scores_by_variant.png: analysis/plot_scores_by_variant.py data/results.ep
	python analysis/plot_scores_by_variant.py

writeup/plots/action_rate.png: analysis/plot_action_rate.py data/results.ep
	python analysis/plot_action_rate.py

writeup/plots/heatmap.png: analysis/plot_heatmap.py data/results.ep
	python analysis/plot_heatmap.py

TABLES: writeup/tables/scores_by_segment.csv writeup/tables/impressions_by_variant.csv

writeup/tables/scores_by_segment.csv: analysis/table_scores_by_segment.py data/results.ep
	python analysis/table_scores_by_segment.py

writeup/tables/impressions_by_variant.csv: analysis/summarize_impressions.py data/results.ep
	python analysis/summarize_impressions.py

writeup/report.html: writeup/report.md PLOTS TABLES
	cd writeup && pandoc report.md -o report.html --standalone --embed-resources --css=report.css

writeup/report.pdf: writeup/report.md writeup/report_header.tex writeup/fix-table-widths.lua PLOTS TABLES
	cd writeup && pandoc report.md -o report.pdf --pdf-engine=xelatex --include-in-header=report_header.tex --lua-filter=fix-table-widths.lua

report: writeup/report.html writeup/report.pdf

all: data PLOTS TABLES report
```

---

## Report template

The report in `writeup/report.md` should follow this structure:

```markdown
---
title: "Message Testing: [Topic/Campaign]"
date: YYYY-MM-DD
---

## Background

[2-3 sentences explaining the research context: What company/product is this
for? What is the product and who is the target audience? Why are we testing
messages? A reader with no prior context should understand the purpose of
this study after reading this section.]

## Executive Summary

[1-2 paragraphs: which variant won, by how much, and the key reason why.
Lead with the recommendation.]

## Methodology

### Variants Tested

| Label | Message |
|-------|---------|
| A     | [text]  |
| B     | [text]  |
| C     | [text]  |

### Evaluation Panel

[Describe the agent panel: number of agents, key segments represented,
and why they match the target audience.]

### Metrics

| Metric     | Type         | Scale | Description                        |
|------------|--------------|-------|------------------------------------|
| Appeal     | LinearScale  | 1-7   | How appealing the message is       |
| Clarity    | LinearScale  | 1-7   | How clear the message is           |
| Persuasion | LinearScale  | 1-7   | How persuasive the message is      |
| Action     | YesNo        | --    | Would prompt action                |
| Impression | FreeText     | --    | Open-ended overall impression      |

### Model

[Model(s) used for evaluation.]

## Quantitative Results

### Overall Scores

![Mean scores by variant](plots/scores_by_variant.png)

[Narrative: which variant scored highest on each metric, notable gaps.]

### Action Rate

![Action rate by variant](plots/action_rate.png)

[Narrative: which variant drives the highest action intent.]

### Score Heatmap

![Heatmap](plots/heatmap.png)

[Narrative: overall pattern -- does one variant dominate across all metrics,
or do different variants excel on different dimensions?]

## Segment Analysis

[Table or chart showing how different audience segments responded.
Highlight any segments where the winning variant differs.]

## Qualitative Insights

[Themes from the free-text impressions. What did agents like about the
winning variant? What were common criticisms of weaker variants?]

## Recommendation

[Clear recommendation: which variant to use, any caveats, and suggested
next steps (e.g., test with real users, iterate on the winner).]

## Files Generated

| File | Description |
|------|-------------|
| `data/results.ep` | Raw EDSL results |
| `writeup/plots/scores_by_variant.png` | Mean scores grouped bar chart |
| `writeup/plots/action_rate.png` | Action rate bar chart |
| `writeup/plots/heatmap.png` | Variant x metric heatmap |
| `writeup/tables/scores_by_segment.csv` | Composite scores by segment |
| `writeup/tables/impressions_by_variant.csv` | Free-text impressions |
```
