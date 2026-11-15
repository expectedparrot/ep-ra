---
name: research-forecasting
description: "Research the probability of a defined future event with Vorhersage, preserve evidence and model assumptions, and author a sourced forecast report. Use for deadline forecasts, forecast revisions, and one-case prediction-market comparisons; strategic scenario exploration without an event probability belongs to skill:research-scenario-planning."
tags: [study-type, quantitative, external-tool]
---

# Forecasting

Vorhersage owns the question, research workflow, evidence, declared calculations,
and immutable forecast history. The research agent owns research, judgment, and
the audience-facing report. Vorhersage is a standalone CLI, not an `ep` command.

## Orient and define

Use the study root established through the normal session/file-layout workflow.
Keep the project under `<study>/analysis/forecast/`. Read the installed contract:

```bash
vorhersage version
vorhersage guide
vorhersage report context --help
```

The runtime needs a Vorhersage revision supporting `report context`. If the
command is missing, report the environment requirement; do not mutate the locked
environment or substitute a package-generated HTML report.

Agree on the event, deadline/timezone, YES/NO rules, and authoritative resolution
sources. Distinguish demonstrations, partial releases, and public availability
when they resolve differently. Start with the agreed definition and your agent
name as `--forecaster`; use `show --json` to resume an existing study. The live
`guide` supplies command syntax and the current research contract.

Use `--workflow timeline` when prerequisites and remaining durations define the
event. Timeline runs have fixed cutoffs: capture evidence before defining that
run, preserving actual timestamps. Standard prospective runs advance their
cutoff during research. Do not backdate findings to make them eligible.

## Follow research and review

Use `next --project PROJECT --output TASK.json`, then
`submit --project PROJECT --task TASK.json --answer ANSWER.json --json`.
Read the task's instruction, context, and payload schema; author only its payload.
Use `--usage` for measured usage. Keep IDs and retry bookkeeping in the task file.
Do not reconstruct the state machine or inspect installed package source.

Intake identifies missing facts and their model inputs. If several influential
facts are known to the human, offer a short personal survey through `ep humanize`
or collect them in chat. Follow the installed guide's response-capture and
revision instructions; user answers are self-reports, not population base rates.

Capture one claim and supporting passage per finding. Separate observation from
inference. Inquiry coverage can satisfy research domains without repeated work.
For empirical base rates, use registered comparable episodes and censoring;
ongoing proposals are not completed failures or independent trials by default.

Keep scenario weights separate from conditional event probabilities. Version
research-to-model mappings when assessing or repairing the model. Complete the
model challenge by inspecting evidence transfers and scenario boundaries, then
resolve concerns into investigations, awaited evidence, or explicit assumptions.
Use sensitivity to prioritize obtainable evidence. Schema acceptance establishes
consistency, not substantive support. Issue only after review; new evidence after
issuance uses `revise`, preserving the original forecast.

For a requested market comparison, use the installed workbench guide and one
case at a time. Keep prices hidden until research is sealed and exposure recorded.
Report market agreement separately from accuracy on a resolved outcome.

## Hand off evidence, then author the report

```bash
vorhersage report context --project <study>/analysis/forecast \
  --output <study>/analysis/forecast-report-context.json
```

For a portfolio add `--run RUN_ID`; for a workbench use `--case CASE_ID`. Do not
choose an arbitrary latest run. Read the context's `reportability`, selected
prediction, model, evidence, challenges, and writing guidance. If unfinished,
continue research or clearly deliver the requested work-in-progress report.
Read needed omitted details from the companion full-material file. Preserve its
snapshot hash and source IDs for traceability; use supplied calculations exactly.

Immediately before narrative writing, load `skill:report-authoring`. Author
`<study>/writeup/report.md`, explaining the forecast and reasoning for the reader.
Use that skill's branding, optional quality-review decision, compilation, and
checks to produce `<study>/writeup/report.html`. The legacy Vorhersage HTML is an
inspection view; the report-context JSON is evidence, neither is the final report.
Do not constrain the narrative to task headings or call another model merely to
turn the handoff into prose. Include consequential assumptions, source links,
uncertainty, and revision triggers. Readiness does not establish calibration;
sensitivity bounds are not confidence intervals. Present the checked report
through the normal study completion workflow.
