---
name: methods-opinion-clustering
description: >
  Build a numeric response matrix from any tabular source (EDSL Results, a CSV export, or a pandas DataFrame),
  run PCA and k-means clustering to discover latent opinion groups, characterize each cluster by its mean
  responses and agent traits, and produce labeled scatter plots and cluster-profile heatmaps.
  Use when a survey has produced many numeric or ordinal responses and you want to discover latent opinion segments.
tags: [methods, quantitative, analysis, visualization, opinion]
---

# Opinion Clustering and Dimensionality Reduction

Use this skill when a survey has produced many numeric or ordinal responses across a large agent panel and you want to discover whether latent opinion groups exist — segments of agents who think similarly on multiple issues at once.

This is distinct from simply comparing group means. Clustering finds naturally occurring segments in the response space without assuming any grouping in advance.

## When to use this skill

- Your survey has at least four numeric/ordinal questions (LinearScale, Likert, Rank) per agent
- You want to know whether opinion segments exist beyond the persona groups you defined
- You want to visualize where agents sit relative to each other in opinion space
- You want to characterize "who thinks what" by linking clusters back to agent traits

## Not the right skill

| Need | Use instead |
|------|-------------|
| Compare mean responses across predefined groups | Standard `results.to_pandas()` group-by analysis |
| Thematic analysis of free-text responses | `research_agent/skills/methods-thematic-analysis/SKILL.md` |
| Psychometric scale skill:methods-response-validation | `research_agent/skills/methods-psychometric-testing/SKILL.md`  |
| Simple cross-tabs of two questions | Standard pandas pivot tables |

## What it produces

- **PCA scatter plot** (in `writeup/plots/`) — 2D projection of agents, colored by cluster
- **Cluster profile heatmap** (in `writeup/plots/`) — mean standardized responses per cluster per question
- **Cluster summary table** (in `writeup/tables/`) — cluster ID, size, mean scores, dominant trait values
- **Agent cluster assignments** (in `writeup/tables/`) — every agent with their assigned cluster ID
- **Elbow curve** (in `writeup/plots/`) — inertia vs. k, used to justify cluster count selection

Name output files to reflect the survey or scale being clustered (e.g., `remote_work_pca_scatter.png`, `remote_work_cluster_summary.csv`). Follow `research_agent/skills/workflow-file-layout/SKILL.md` for directory placement.

---

## Prerequisites

The ep-agent runtime owns EDSL, pandas, and matplotlib. Do not install or
upgrade those packages during a study. Verify the base stack:

```bash
python3 -c "import edsl, pandas, matplotlib"
```

Install only the specialized dependency needed for this workflow if it is
missing; do not include the runtime-owned packages in these commands:

```bash
python3 -c "import sklearn" || pip install scikit-learn
# Optional, only when the user wants a UMAP projection:
python3 -c "import umap" || pip install umap-learn
```

If the base-stack check fails, report the environment problem rather than
mutating the sandbox.

---

## Step 1: Load data and extract the response matrix

The source of the data does not matter — EDSL Results, a CSV export from Qualtrics or SurveyMonkey, or any other tabular file all work.

### From an EDSL Results object

```python
from edsl import Results
import pandas as pd

results = Results.git.load("data/raw/results.ep")
df = results.to_pandas()

# Answer columns follow the pattern "answer.<question_name>"
answer_cols = [c for c in df.columns if c.startswith("answer.")]
trait_cols = [c for c in df.columns if c.startswith("agent.")]
```

### From a CSV file (Qualtrics, SurveyMonkey, or any export)

```python
import pandas as pd

df = pd.read_csv("data/raw/survey_responses.csv")

# Identify which columns are your scale items and which are respondent attributes
answer_cols = ["trust_gov", "trust_media", "trust_science"]  # your scale item columns
trait_cols = ["age", "education", "region"]                  # respondent attribute columns
```

### Select numeric columns for clustering

Clustering requires numeric inputs. Use scale/Likert/rank responses. Do not include free-text, binary yes/no (unless encoded 0/1), or ID columns.

```python
import pandas as pd

numeric_cols = [c for c in answer_cols if pd.api.types.is_numeric_dtype(df[c])]
print(f"Numeric columns available for clustering: {numeric_cols}")
```

### Build the response matrix

One row per agent, one column per question:

```python
# If multiple models or scenarios, filter first
# For a single-model, single-scenario study this is just:
response_matrix = df[numeric_cols].copy()
response_matrix.index = df.index

print(f"Response matrix: {response_matrix.shape[0]} agents x {response_matrix.shape[1]} questions")
print(response_matrix.head())
```

---

## Step 2: Handle missing values and encode ordinal responses

```python
# Check for missing values
print(response_matrix.isnull().sum())

# Drop rows with any missing values (or impute with column median)
response_matrix = response_matrix.dropna()

# If YesNo questions were included, encode them
# response_matrix["answer.supports_policy"] = (
#     response_matrix["answer.supports_policy"].map({"yes": 1, "no": 0})
# )
```

---

## Step 3: Standardize

Standardization is required when questions use different scales (e.g., 1-5 vs. 1-10). Even for same-scale questions, it ensures equal weighting:

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X = scaler.fit_transform(response_matrix)
print(f"Standardized matrix shape: {X.shape}")
```

---

## Step 4: PCA — reduce to 2D and examine variance explained

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.rcParams["font.family"] = "DejaVu Sans"

# Fit PCA on all components first to examine variance
pca_full = PCA()
pca_full.fit(X)

explained = pca_full.explained_variance_ratio_
cumulative = explained.cumsum()

# Scree plot
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(range(1, len(explained) + 1), explained * 100, alpha=0.7, label="Individual")
ax.plot(range(1, len(explained) + 1), cumulative * 100, "o-", color="red", label="Cumulative")
ax.axhline(80, color="gray", linestyle="--", linewidth=0.8, label="80% threshold")
ax.set_xlabel("Principal component")
ax.set_ylabel("Variance explained (%)")
ax.set_title("PCA scree plot")
ax.legend()
plt.tight_layout()
plt.savefig("writeup/plots/pca_scree.png", dpi=150, bbox_inches="tight")
plt.close()

print(f"PC1: {explained[0]*100:.1f}%  PC2: {explained[1]*100:.1f}%  "
      f"Combined: {(explained[0]+explained[1])*100:.1f}%")
```

### Project to 2D for visualization

```python
pca_2d = PCA(n_components=2)
X_2d = pca_2d.fit_transform(X)
print(f"Variance captured by 2 components: {pca_2d.explained_variance_ratio_.sum()*100:.1f}%")
```

---

## Step 5: Choose k — elbow method

Run k-means for a range of k values and plot inertia to find the elbow:

```python
from sklearn.cluster import KMeans

inertias = []
k_range = range(2, min(10, len(response_matrix) // 3))

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(list(k_range), inertias, "o-")
ax.set_xlabel("Number of clusters (k)")
ax.set_ylabel("Inertia (within-cluster sum of squares)")
ax.set_title("Elbow curve — choose k at the bend")
plt.tight_layout()
plt.savefig("writeup/plots/elbow_curve.png", dpi=150, bbox_inches="tight")
plt.close()
```

**Present the elbow curve to the user and ask them to confirm k before proceeding.** If no clear elbow, default to k=3 for exploratory studies.

---

## Step 6: Fit final k-means and assign cluster labels

```python
k = 3  # Replace with user-confirmed value

km_final = KMeans(n_clusters=k, random_state=42, n_init=10)
cluster_labels = km_final.fit_predict(X)

# Attach cluster labels to the response matrix and agent traits
result_df = response_matrix.copy()
result_df["cluster"] = cluster_labels

# Merge in agent traits
traits_df = df[trait_cols].loc[response_matrix.index]
result_df = result_df.join(traits_df)

result_df.to_csv("writeup/tables/agent_clusters.csv")
print(result_df["cluster"].value_counts().sort_index())
```

---

## Step 7: PCA scatter plot colored by cluster

```python
palette = ["#E74C3C", "#3498DB", "#2ECC71", "#9B59B6", "#F39C12"]
cluster_colors = [palette[c % len(palette)] for c in cluster_labels]

fig, ax = plt.subplots(figsize=(7, 6))
for c in range(k):
    mask = cluster_labels == c
    ax.scatter(
        X_2d[mask, 0], X_2d[mask, 1],
        c=palette[c], label=f"Cluster {c+1} (n={mask.sum()})",
        alpha=0.8, s=60, edgecolors="white", linewidths=0.5,
    )

ax.set_xlabel(f"PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% variance)")
ax.set_ylabel(f"PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% variance)")
ax.set_title("Agent opinion space — clusters colored")
ax.legend(title="Cluster", framealpha=0.9)
plt.tight_layout()
plt.savefig("writeup/plots/pca_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
```

---

## Step 8: Cluster profile heatmap

The profile heatmap shows the mean (standardized) response per cluster per question — the clearest way to characterize what each cluster believes:

```python
# Mean standardized responses per cluster
X_df = pd.DataFrame(X, columns=numeric_cols, index=response_matrix.index)
X_df["cluster"] = cluster_labels
cluster_means = X_df.groupby("cluster")[numeric_cols].mean()

# Shorten column labels for display
short_labels = [c.replace("answer.", "").replace("_", " ").title() for c in numeric_cols]
cluster_means.columns = short_labels
cluster_means.index = [f"Cluster {i+1}" for i in cluster_means.index]

fig, ax = plt.subplots(figsize=(max(8, len(numeric_cols) * 1.0), max(4, k * 0.8)))
im = ax.imshow(cluster_means.values, aspect="auto", cmap="RdBu_r", vmin=-2, vmax=2)
ax.set_xticks(range(len(short_labels)))
ax.set_xticklabels(short_labels, rotation=45, ha="right", fontsize=9)
ax.set_yticks(range(k))
ax.set_yticklabels(cluster_means.index)
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
plt.colorbar(im, cax=cax, label="Mean standardized response")
ax.set_title("Cluster opinion profiles (standardized)")
for i in range(k):
    for j in range(len(short_labels)):
        ax.text(j, i, f"{cluster_means.values[i, j]:.2f}",
                ha="center", va="center", fontsize=7,
                color="white" if abs(cluster_means.values[i, j]) > 1.2 else "black")
plt.tight_layout()
plt.savefig("writeup/plots/cluster_profile_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
```

---

## Step 9: Characterize clusters by agent traits

Understand which demographic or persona groups map to which clusters:

```python
# For each cluster, compute the distribution of each trait
summary_rows = []
for c in range(k):
    cluster_df = result_df[result_df["cluster"] == c]
    row = {"cluster": f"Cluster {c+1}", "n": len(cluster_df)}
    for trait_col in trait_cols:
        short = trait_col.replace("agent.", "")
        mode_val = cluster_df[trait_col].mode()
        row[short] = mode_val.iloc[0] if not mode_val.empty else "N/A"
    summary_rows.append(row)

summary = pd.DataFrame(summary_rows)
summary.to_csv("writeup/tables/cluster_summary.csv", index=False)
print(summary.to_string(index=False))
```

---

## Optional: UMAP for non-linear dimensionality reduction

If the PCA scatter shows poor cluster separation (clusters overlap heavily), try UMAP, which preserves local neighborhood structure better than PCA for non-linear patterns:

```python
from umap import UMAP

reducer = UMAP(n_components=2, random_state=42)
X_umap = reducer.fit_transform(X)

fig, ax = plt.subplots(figsize=(7, 6))
for c in range(k):
    mask = cluster_labels == c
    ax.scatter(X_umap[mask, 0], X_umap[mask, 1],
               c=palette[c], label=f"Cluster {c+1}", alpha=0.8, s=60)
ax.set_xlabel("UMAP-1")
ax.set_ylabel("UMAP-2")
ax.set_title("UMAP projection — clusters colored")
ax.legend()
plt.tight_layout()
plt.savefig("writeup/plots/umap_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
```

Note: UMAP results are not deterministic and depend on hyperparameters (`n_neighbors`, `min_dist`). Treat the visualization as exploratory, not definitive.

---

## Interpreting and naming clusters

After characterizing clusters by trait distributions and mean responses, give each cluster a descriptive name for the report. Common naming patterns:

- **By ideology**: "Free-market optimists", "Equity-focused progressives", "Pragmatic centrists"
- **By domain**: "Privacy-first users", "Convenience-oriented users"
- **By orientation**: "Risk-tolerant investors", "Security-seeking savers"

Document the naming rationale in the report methods section.

---

## Study structure

```
<study_dir>/
  plan.md
  checklist.md
  data/
    raw/
      results.ep
  analysis/
    <topic>_clustering.py             # Name reflects the topic
  writeup/
    report.md
    plots/
      <topic>_pca_scree.png
      <topic>_pca_scatter.png
      <topic>_elbow_curve.png
      <topic>_cluster_profile_heatmap.png
      <topic>_umap_scatter.png        # Optional
    tables/
      <topic>_agent_clusters.csv
      <topic>_cluster_summary.csv
```

Follow `research_agent/skills/workflow-file-layout/SKILL.md` for directory conventions. Use a descriptive prefix (e.g., `remote_work_`, `trust_`) so output files are identifiable if the study has multiple analyses.

---

## Limitations and caveats

### Cluster count is a judgment call
The elbow method rarely produces a definitive k. Always present the elbow curve to the user and explain the trade-off: fewer clusters are more interpretable; more clusters are more granular. For exploratory studies, k=3 is a good default.

### Agents are not humans
Persona-based agents may cluster more neatly than real human populations because they are generated from trait combinations rather than organic individual differences. Report results as "patterns among simulated personas" not as population-level estimates.

### Standardization prerequisite
If questions use wildly different scales (e.g., one is 0-100 and another is 1-5), always standardize. Skipping standardization will cause the high-range question to dominate the clustering.

### Minimum sample size
K-means is unreliable with fewer than 30 agents per expected cluster. For a study expecting k=3 clusters, run at least 90 agents. Check the cluster sizes in Step 6 — any cluster with fewer than 10 agents should trigger caution.

### Results may not replicate across models
If the study was run with a single model, clusters may reflect that model's internal biases rather than genuine opinion variation. Cross-model consistency is a useful check: re-run a subset with a different model and check whether cluster membership is stable.
