---
name: research-concept-testing
description: Tests product, service, or feature concepts with simulated respondents to measure appeal, clarity, differentiation, purchase intent, concerns, and comparative preference. Use when screening one concept or comparing several concepts with a target audience.
tags: [study-type, market-research, quantitative]
---

# Concept Testing

Own the research design and route execution through the standard study
workflow. Keep concept descriptions balanced, measure both ratings and reasons,
and make recommendations traceable to saved results.

## Required handoff order

Before writing `plan.md` for any inference study:

1. Load `skill:workflow-model-selection` and make its one bounded `ep models` query.
2. Load `skill:workflow-plan-template` and write the plan using only the
   confirmed model identifier.
3. Obtain plan approval.
4. Load `skill:workflow-file-layout` and create the survey scaffold with its
   absolute `<skill-base>` command.
5. Load `skill:edsl-surveys` only when editing the scaffold's marked survey and
   persona sections.

Never choose a model from memory or put an unverified identifier in the plan.
Immediately after plan approval, run `prepare` with that approval as evidence;
its estimate is the basis for the separate spend decision. Do not build and
estimate separately, and do not wait for spend approval before `prepare`.

## Choose the smallest valid design

### One concept

Use one survey job. Ask a compact battery covering:

- appeal, clarity, differentiation, and purchase intent on consistent scales;
- the most appealing element;
- the primary concern;
- one concrete improvement.

Do not introduce forced ranking or multi-job machinery when there is nothing to
compare.

### Multiple concepts

Use two jobs when relative preference matters:

- independent evaluation: each concept is a scenario rated without memory;
- comparative evaluation: show all concepts and request a forced ranking plus
  rationale.

Read [code-examples.md](references/code-examples.md) only for this multi-concept
survey construction or when implementing concept-level and segment analysis.
Every scenario field must appear in question text, not only instructions. Keep
descriptions similar in length and specificity, and do not enable full memory
for independent ratings.

## Panel and scale

Represent the approved target market with named personas and only traits that
could plausibly affect the decision. Use enough agents to cover the requested
segments; do not inflate the panel merely to make the study look substantial.
State the number of agents, concepts, questions, and resulting inference calls
in the plan and estimate.

## Execute through owned targets

After scaffolding, edit only the returned `next_edits`. Then use absolute Make
invocations:

```bash
make -C <study-root> prepare APPROVAL_EVIDENCE="<plan approval>"
make -C <study-root> data
make -C <study-root> post-run REPORT_GROUP_BY=agent.<primary-segment>
```

Omit `REPORT_GROUP_BY` when no segment comparison was approved. Treat
`data/report-data.json`, the owned exports, and QA output as the default analysis
inputs. Do not write ad hoc Python result queries unless those bounded artifacts
identify a concrete unanswered question.

Use the scaffold's standard plots first. Author a custom plot script only when
the approved decision requires a relationship those plots do not show.

Write the report, then use:

```bash
make -C <study-root> complete
```

## Analysis contract

For one concept, report distributions and means, respondent variation, bounded
qualitative evidence, material segment differences, limitations, and actionable
improvements. For multiple concepts, add concept-level score comparison,
ranking agreement, and whether the recommendation is robust across segments.

Do not declare a winner solely from an average. Weigh purchase intent, appeal,
clarity, qualitative concerns, and comparative ranking. Distinguish observed
results from interpretation and do not invent market-size or real-consumer
claims from simulated respondents.

## Completion criteria

- The exact model was confirmed before the plan.
- The approved panel and questions match the constructed EDSL objects.
- Paid inference was run at most once unless the user approved a retry.
- `post-run` produced bounded report data, exports, costs, and passing QA.
- The report answers the user's decision and states simulation limitations.
- `complete` reports all workflow gates passing and presents the local HTML.
