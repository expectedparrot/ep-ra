---
name: research-message-testing
description: >
  A/B tests message variants (email subjects, ad copy, taglines) against
  AI agent panels with statistical analysis of which variant performs best.
  Use when the user wants to test or compare multiple message or copy variants.
tags: [study-type, market-research, quantitative]
---

# Message/Copy Testing with EDSL

Use this workflow when a user wants to test multiple message variants -- email subject lines, ad headlines, taglines, product descriptions, or any short-form copy -- against a panel of AI agents representing a target audience. Each variant becomes an EDSL scenario; a survey evaluates each variant on standardized metrics; results reveal which variant performs best and why.

## Overview

The message-testing workflow has seven steps:

1. **Define** the message variants as a ScenarioList
2. **Build** the evaluation survey (standardized metrics + custom questions)
3. **Define** the agent panel (target audience personas)
4. **Sample** a small subset and preview results
5. **Run** the full test
6. **Analyze** results (quantitative scores, qualitative themes, segment analysis)
7. **Report** findings with a winning-variant recommendation

This follows the standard EDSL study structure. The study directory uses the normal scaffold from `ep study scaffold`.

---

## Step 1: Define message variants

Each message variant becomes a Scenario with a `message_variant` field and a `variant_label` for easy reference. Three patterns:

- **Inline**: build a `ScenarioList` from a list of dicts (most common)
- **From CSV**: `ScenarioList.from_csv("data/uploaded/variants.csv")`
- **Multi-dimensional**: cross message variants with context variables for factorial designs

> **IMPORTANT**: Every field in the ScenarioList must be referenced in at least one question's `question_text` using `{{ scenario.field_name }}` syntax, or EDSL raises a `JobsCompatibilityError`.

See `references/setup-examples.md` for full code examples of all three patterns.

---

## Step 2: Build the evaluation survey

The standard message-testing battery measures five dimensions:

| Metric     | Type         | Scale | Description                        |
|------------|--------------|-------|------------------------------------|
| Appeal     | LinearScale  | 1-7   | How appealing the message is       |
| Clarity    | LinearScale  | 1-7   | How clear the message is           |
| Persuasion | LinearScale  | 1-7   | How persuasive the message is      |
| Action     | YesNo        | --    | Would prompt action                |
| Impression | FreeText     | --    | Open-ended overall impression      |

Customize by adding domain-specific metrics (e.g., trust, relevance), changing the scale, or adding a preference ranking question.

**Randomize message options** if testing multiple messages/concepts via a multiple choice question to control for order bias. Use `questions_to_randomize=["message_preference"]` in the Survey constructor.

See `references/setup-examples.md` for the full standard battery and customization examples.

---

## Step 3: Define the agent panel

Build an AgentList representing the target audience. Three patterns:

- **Inline demographics**: define agents with persona, age, segment traits
- **From CSV**: `AgentList.from_csv("data/uploaded/personas.csv")`
- **Programmatic**: generate from trait combinations (age groups x attitudes)

> **Sizing the panel:** For message testing, you need enough agents to see if message effects hold across different personas — not to estimate population proportions. Start with: 1 agent per key segment for technical check, then 2-3 per segment to verify the effect is robust. If segments aren't relevant (messages are broad-appeal), 8-12 diverse agents is usually enough. Pilot with ~5 agents to verify messages differentiate.

See `references/setup-examples.md` for full code examples.

---

## Step 4: Sample and preview

Before running the full test, run a small subset to verify the survey works and results look sensible.

```bash
# job_pilot contains two scenarios and three agents.
ep run edsl_jobs/job_pilot/jobs.ep \
  --remote_inference_description "Earth Day subject lines — preview" \
  --results_description "Earth Day subject lines — preview" \
  --output data/results_pilot.ep
ep results head data/results_pilot.ep \
  --column scenario.variant_label \
  --column agent.persona \
  --column answer.appeal \
  --column answer.clarity \
  --column answer.persuasion \
  --column answer.action \
  --column answer.impression \
  --rows 10
```

### What to check in the preview

- Do the scores vary across variants? (If all identical, questions may need sharpening.)
- Do different agent personas respond differently? (If not, personas may need more differentiation.)
- Are free-text impressions substantive and relevant?
- Do the scale anchors make sense for the domain?

Present the sample results to the user and ask whether the results look reasonable, whether any question wording or scale should change, and whether the agent panel should be adjusted.

---

## Step 5: Run the full test

After user approval, run all variants against the full agent panel.

**Always pass both `remote_inference_description` and `results_description` to `ep run`, set to the same string; don't omit them** — see `skill:edsl-surveys` ("Running a survey — labeling the job").

> **Cost check**: Before running, confirm with the user. State the number of scenarios, agents, and models, and the total number of survey runs (scenarios x agents x models).

```bash
ep jobs build \
  --survey edsl_jobs/job_a/survey.ep \
  --scenarios edsl_jobs/job_a/scenario_list.ep \
  --agents edsl_jobs/job_a/agent_list.ep \
  --models edsl_jobs/job_a/model_list.ep \
  --output edsl_jobs/job_a/jobs.ep

ep run edsl_jobs/job_a/jobs.ep \
  --remote_inference_description "Earth Day email subject lines - 5 variants x 150 agents" \
  --results_description "Earth Day email subject lines - 5 variants x 150 agents" \
  --output data/results.ep
```

Run via the Makefile: `make data`

---

## Step 6: Analyze results

Create analysis scripts in `analysis/`, with outputs to `writeup/plots/` and `writeup/tables/`. Standard analyses:

- **Mean scores by variant** — grouped bar chart
- **Action rate by variant** — bar chart with percentage labels
- **Score heatmap** — variants x metrics matrix
- **Segment analysis** — composite scores broken down by agent segment
- **Qualitative themes** — grouped free-text impressions

See `references/analysis-and-reporting.md` for full analysis scripts and Makefile integration.

---

## Step 7: Report

The report in `writeup/report.md` should include: Background, Executive Summary, Methodology (variants, panel, metrics, model), Quantitative Results (scores, action rate, heatmap), Segment Analysis, Qualitative Insights, Recommendation, and Files Generated.

See `references/analysis-and-reporting.md` for the full report template.

---

## Quick Reference

| Task | Code |
|------|------|
| Define variants inline | `ScenarioList([Scenario({"variant_label": "A", "message_variant": "..."}) for ...])` |
| Load variants from CSV | `ScenarioList.from_csv("data/uploaded/variants.csv")` |
| Appeal question (1-7) | `QuestionLinearScale(question_name="appeal", question_text="..{{ scenario.message_variant }}..", question_options=[1,2,3,4,5,6,7])` |
| Yes/no action question | `QuestionYesNo(question_name="action", question_text="..{{ scenario.message_variant }}..")` |
| Free-text impression | `QuestionFreeText(question_name="impression", question_text="..{{ scenario.message_variant }}..")` |
| Build agent panel | `AgentList([Agent(traits={"persona": "...", "segment": "..."}) for ...])` |
| Run sample | `ep run edsl_jobs/job_a/jobs.ep --remote_inference_description "... - preview" --results_description "... - preview" --output data/results_preview.ep` |
| Preview results | `ep results head data/results_preview.ep --rows 10` |
| Run full test | `ep run edsl_jobs/job_a/jobs.ep --remote_inference_description "..." --results_description "..." --output data/results.ep` |
| Save results | `ep run ... --output data/results.ep` |
| Inspect results | `ep results summary data/results.ep` |
| Scores to pandas | `results.select("scenario.variant_label", "answer.*").to_pandas()` |
| Group by variant | `df.groupby("scenario.variant_label")[["answer.appeal"]].mean()` |
