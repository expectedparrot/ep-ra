---
name: workflow-study-index
description: >
  Scan the sessions directory and print a numbered table of all topics
  and studies. Use when the user asks what studies exist or wants to
  browse available topics.
tags: [workflow]
---

# List Studies

Scan the `sessions/` directory and display a formatted table of every topic and study.

## When to use

- When the user asks what studies exist, what's been done, or wants to pick a study to work on.
- When the user says "list studies", "show studies", "what topics do we have", or similar.

## Steps

1. **Scan topics.** List all `topic_*` directories under `sessions/`.

2. **Scan studies within each topic.** For each topic, list its subdirectories (e.g., `study_a`, `study_b`, `olive_garden_sneeze_guards`).

3. **Determine study type.** Check whether the study contains `edsl_jobs/` (→ EDSL) or `simulations/` (→ Simulation).

4. **Extract a one-line description.** Read the first H1 heading (`# ...`) from `plan.md` in each study. Strip the leading `# Plan: ` or `# ` prefix to get a short title. If `plan.md` doesn't exist, use `"(no plan)"`.

5. **Check for a report.** Note whether `writeup/report.md` exists (→ Yes / No).

6. **Print a markdown table** with these columns:

| # | Topic | Study | Type | Description | Report |
|---|-------|-------|------|-------------|--------|
| 1 | corn-chips-elasticity | study_a | EDSL | Estimating the Elasticity of Demand for Corn Chips | Yes |
| 2 | corn-chips-elasticity | study_b | EDSL | Follow-up with demographic variation | Yes |
| 3 | ban-the-box-interview | study_a | Simulation | Ban-the-Box hiring simulation | Yes |

**Formatting rules:**
- Strip the `topic_` prefix from the topic column.
- Number rows sequentially starting at 1.
- Sort by topic name, then by study name within each topic.
- Keep descriptions short — truncate at 60 characters if needed and add `...`.

## Implementation

You can do this entirely with Bash + Read. Here is a reference approach:

```bash
idx=1
echo "| # | Topic | Study | Type | Description | Report |"
echo "|---|-------|-------|------|-------------|--------|"
for topic_dir in sessions/topic_*/; do
  topic=$(basename "$topic_dir" | sed 's/^topic_//')
  for study_dir in "$topic_dir"*/; do
    [ -d "$study_dir" ] || continue
    study=$(basename "$study_dir")

    # Type
    if [ -d "${study_dir}simulations" ]; then
      stype="Simulation"
    else
      stype="EDSL"
    fi

    # Description from plan.md
    if [ -f "${study_dir}plan.md" ]; then
      desc=$(head -1 "${study_dir}plan.md" | sed 's/^#\+ *//' | sed 's/^Plan: *//' | cut -c1-60)
    else
      desc="(no plan)"
    fi

    # Report exists?
    if [ -f "${study_dir}writeup/report.md" ]; then
      has_report="Yes"
    else
      has_report="No"
    fi

    echo "| $idx | $topic | $study | $stype | $desc | $has_report |"
    idx=$((idx + 1))
  done
done
```

Print the table directly so the user can see it. Do not write it to a file unless asked.
