---
name: research-estimation
description: >
  Research numerical quantities with Stanton, combining sourced inputs and
  unit-aware models into estimates with uncertainty and preserved revision history.
  Use when the user asks for a sourced count, amount, rate, cost, market size,
  Fermi estimate, competing numerical estimation routes, or explicitly requests
  Stanton. Survey execution costs and EDSL Jobs/inference budgets belong to
  skill:edsl-surveys-cost; defined future-event probabilities belong to skill:research-forecasting.
tags: [study-type, quantitative, analysis, external-tool]
---

# Numerical estimation with Stanton

[Stanton](https://github.com/expectedparrot/stanton) owns numerical models,
saved draws, provenance, research reviews, and issued conclusions. The agent
owns external research, judgment, and narrative reporting. Stanton is a
standalone CLI, never an `ep` subcommand. Use it for uncertain quantities,
including future amounts; use `skill:research-forecasting` for the probability
of a defined future event and `skill:research-scenario-planning` for strategic
futures.

For survey execution costs or EDSL Jobs/inference budgets, load
`skill:edsl-surveys-cost` and use its artifact-based costing workflow, even if
the request mentions Stanton. Do not replace execution-cost estimates with a
Stanton model. Other empirical costs, such as construction costs or market
spending, remain numerical-estimation tasks.

## Start or resume

The ep-agent runtime installs Stanton from a pinned GitHub revision, including
its optional EDSL fielding bridge. Use the installed command; do not install or
upgrade packages during a study. If it is missing, report the environment defect.

```bash
stanton guide
```

Read the complete guide before empirical estimation. It supplies the current
research contract and command forms. Use `stanton schema` and command `--help`
for payloads and options instead of recreating schemas or inspecting internals.

Use the study root established through `skill:workflow-session-start` and
`skill:workflow-file-layout`. Keep the project at `<study>/analysis/estimation`
and its external research record at `<study>/analysis/estimation/RESEARCH.md`.
For a new project, use `skill:workflow-plan-template` to write `<study>/plan.md`
and obtain explicit user approval before initializing method-specific Stanton
state or writing its research artifacts. Once the plan is approved:

```bash
stanton init <study>/analysis/estimation --title "<estimation question>"
stanton next --project <study>/analysis/estimation
```

For an existing project, read its research record and run `stanton status` and
`stanton next` with `--project PATH`. Preserve its history. Follow project-specific
guidance, inspecting returned warnings and errors; `next` is advisory and does
not certify research completion. Pass `--project PATH` explicitly throughout.

## Research and model

Follow the guide's high-effort research default unless the user explicitly
limits the work. Define the observable, population, geography, units, reference
period, and counting rules. Record source observation periods separately from
publication and access dates. Maintain the guide's `RESEARCH.md` evidence ledger,
including source ancestry, unsuccessful searches, discrepancies, alternative
routes, stress tests, and the stopping rationale.

Investigate contradictions and seek substantively different evidence. Multiple
websites repeating one count are one source family. Attempt another estimation
route when defensible; explain why it cannot be supported when that is the case.
Distinguish observed inputs from judgment and explain distribution choices.

Use `define`, `anchor`, `estimate`, and `relate` to model the quantity. Anchors
require both `--source` and `--asof`; relation expressions should be shell-quoted.
Use the guide for forks, mixtures, conditional scenarios, paths, or allocations
when the question needs them. Preserve these numerical distinctions:

- Shared uncertain inputs should be the same leaf quantity across relations.
  Notes and shared citations do not create numerical correlation. Forks copy
  relations, while leaves remain global; changing a leaf affects future runs
  across forks.
- Mixtures retain competing strategies; their intervals do not establish method
  agreement. Record weights and shared evidence explicitly.
- Units do not establish matching populations, dates, or real/nominal currency.
  Choose distribution support deliberately, especially for rates in `[0, 1]`.
- Bounds warn by default. `--clip` conditions joint draws; it does not clamp
  values and should not be added just to make a warning disappear.
- Saved runs freeze inputs. Model and note edits require a fresh run before a
  current review or conclusion can be issued.

Test consequential assumptions with saved baseline and changed-input runs.
Different seeds, more draws, or comparing two strategies do not constitute
sensitivity tests. Restore the intended model after tests.

## Review and issue the conclusion

Before the final sample, append a substantive research summary with
`stanton note TARGET "..." --project PATH`. Include evidence, dependence,
sensitivity findings, unresolved issues, and why stopping is justified. A link
to `RESEARCH.md` alone is insufficient because archives omit arbitrary files.

After sampling the final model, use its returned run ID:

```bash
stanton research template TARGET --run RUN_ID --output REVIEW.json --project PATH
stanton schema research_review
```

Fill the template from actual research, preserving its bindings. Include scope,
source-to-quantity mappings and dates, discrepancies, evidence dependencies,
saved sensitivity comparisons, and remaining gaps. Then:

```bash
stanton research check --from REVIEW.json --project PATH
stanton research review REVIEW_NAME --from REVIEW.json --project PATH
stanton research show REVIEW_NAME --project PATH
stanton report issue REPORT_NAME --review REVIEW_NAME --method strategy:main --coverages .8,.9 --project PATH
stanton report show REPORT_NAME --project PATH
stanton validate --project PATH
```

Replace `strategy:main` with the actual `strategy:FORK` or `mixture` selected
on evidence. Inspect `research check` findings and fix problems or record honest
warning dispositions before saving the immutable review. Set status in the
review payload, not on `report issue`. Material research gaps require
`provisional` status and visible limitations; acknowledging them cannot make
the research complete. Continue feasible consequential research within the
user's scope. Revise with new runs, reviews, and report names, retaining history.

Sampling and validation establish computational consistency, not source truth,
empirical calibration, or research quality. Use the issued presentation's exact
numbers, scope, dates, and interval labels: p10–p90 is 80%; p5–p95 is 90%.
Changing a headline requires a revised saved model and issuance.

## Report and preserve

Export `stanton report context TARGET --run RUN_ID --output CONTEXT.json --project PATH`
and read it together with the selected issued report. Keep the final run/review/
report IDs explicit. Preserve source dependence, competing strategy results,
key assumptions, provisional status, and limitations in the narrative.

Immediately before writing the audience-facing report, load
`skill:report-authoring`. Author `<study>/writeup/report.md` from the evidence
and issued presentation, then use that skill's branding, review, compilation,
and checks for `<study>/writeup/report.html`. The context JSON is evidence for
the report. Save a portable history with `stanton save ARCHIVE.stanton.gz
--project PATH` and retain `RESEARCH.md` and source artifacts separately.

## Optional elicitation and evaluation

Read the relevant sections of the live guide when needed. Survey compilation
creates EDSL artifacts but does not execute inference or contact respondents.
Use `skill:edsl-surveys` or `skill:edsl-human-survey` for requested fielding;
import responses as proposals, review conflicts, and apply selected slots
together because model changes invalidate remaining proposals. Respondent
answers are not automatically pooled or calibrated population evidence.

For observed outcomes or fitted uncertainty adjustments, use Stanton's
resolution, scoring, cohort, and calibration commands. Preserve frozen event
membership and train/test splits; fit on training evidence and report held-out
results separately. Do not describe retrospective scores as prospective accuracy.
