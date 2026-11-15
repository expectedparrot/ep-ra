---
name: research-digital-twins
description: >
  Route and execute digital-twin studies according to available evidence. Use
  Zwill for held-out respondent prediction when respondent-level microdata
  exists; route to skill:research-marginal-twins and UMRISS when microdata is
  absent and the study must construct an auditable synthetic population from
  reported or explicitly synthetic aggregate targets. Use for twin
  construction, validation, AgentList delivery, leakage or baseline checks,
  and digital-twin reports.
tags: [study-type, validation, external-tool, edsl]
---

# Digital-twin routing

Choose the evidence regime before loading package documentation:

| Available evidence | Owner | Permitted claim |
|---|---|---|
| Respondent-level answers with held-out truth | Continue here with Zwill | Individual-level predictive validity, only if the validation gate passes |
| Reported aggregate marginals or crosstabs, but no respondent microdata | Load `skill:research-marginal-twins` and stop this workflow | A calibrated synthetic population consistent with tested aggregate moments—not recovered respondents |
| No observed microdata or aggregate targets | Load `skill:research-marginal-twins` only if the user approves model-synthetic targets | Scenario or prior-driven synthetic population; no empirical validation claim |
| Hand-authored traits only | Use `skill:edsl-agent-lists` | Deliberate-coverage personas, not digital twins validated against people |

Do not fabricate row-level records from marginals and send them to Zwill. Do not call hand-authored personas respondent twins. If data availability is unclear, inspect the supplied artifacts or ask one concise question before choosing the owner.

# Respondent-level twins with Zwill

Use the locked `zwill` package as the state, method, and artifact owner. Do not recreate its import adapters, scoring, baselines, leakage checks, bootstrap logic, or report renderer in study scripts.

## Orient from the package

Run these once, in order, from the intended Zwill project directory:

```bash
zwill version
zwill capabilities
zwill skills path digital-twin-study-runner
zwill guide
zwill next
```

All commands return a schema-2 JSON envelope. Treat `data`, `warnings`, `errors`, and `next_steps` as authoritative. Follow `next_steps`; after each material stage run `zwill next [--survey <survey>]`. Inspect command help before inventing an option.

The package-bundled `digital-twin-study-runner` skill and guides are version-matched method documentation. Load them only when the task reaches that method:

- `zwill guide show import-format` for input schemas or matrix ingestion.
- `zwill guide show interpreting-results` before making a validity claim.
- `zwill guide show prompt-pipelines` only for construction-strategy experiments.
- `zwill guide show study-reference` only for cross-survey studies.
- `zwill guide show rank` only for rank or MaxDiff outcomes.

Never install packages or mutate the locked launcher environment during a run.

## Establish the claim before building

Distinguish two tasks:

1. **Constructing respondent agents:** create an auditable AgentList from supplied evidence for exploration. Validate file integrity and construction coverage, but never call it representative or respondent-valid without held-out human truth.
2. **Validating twins:** predict held-out answers for real respondents from permitted prior evidence, then compare against observed truth and appropriate baselines.

For validation, ask the user to approve the held-out questions, context and leakage exclusions, respondent sample and seed, construction approaches, current provider-qualified models, and decision criterion. Show the prediction count:

`respondents × held-out questions × approaches × models`

Use `skill:workflow-file-layout` with `--template digital-twins` to allocate the study shell before writing the plan. Record the choices at exactly `<study>/plan.md`, never at the topic root. Scaffolding creates inert local files and does not authorize execution. Use `skill:workflow-model-selection` for a bounded current-model lookup, present `<study>/plan.md`, and obtain approval before running the workflow.

## Preserve the execution boundary

Zwill builds Jobs and imports Results. `ep` owns credentials, costing, remote execution, and Results packages.

Before every paid run:

1. Export or obtain the exact Jobs path from Zwill.
2. Estimate it with `ep jobs cost <jobs.ep>`.
3. Present model, call count, cost estimate, and time risk.
4. Obtain explicit user approval.
5. Run `ep run <jobs.ep> --output <results.ep>`.
6. Import that exact Results artifact with the Zwill command returned by `next_steps`.

Never expose held-out answers, target marginals, target-revealing follow-ups, identifiers, or weights as personality evidence. Audit imported prompts and raw responses before inspecting performance.

## Require rigorous validation

For respondent-validity claims, require the package-owned validation flow, including:

- clean leakage audit or explicit exclusions;
- a conditional baseline on the same scored respondents;
- paired bootstrap intervals for twin-minus-baseline differences;
- calibration and malformed-row review;
- prompt/run audit before score interpretation.

Lead with proper scoring rules and individual-level skill versus the conditional baseline. Accuracy is only a sanity check. A positive claim requires the paired interval to clear zero in the improving direction and no unresolved leakage. Otherwise describe the result as exploratory, aggregate-only, or unsupported.

## Complete the study

Keep Zwill state under `<study>/data/zwill_project/`. Build the package-owned consolidated report under `<study>/writeup/zwill-report/` and preserve its machine-readable evidence. Author any stakeholder interpretation from those artifacts; do not create another model job to narrate them.

Before completion:

```bash
make -C <study> twin-next ZWILL_SURVEY=<survey>
make -C <study> twin-report ZWILL_SURVEY=<survey>
make -C <study> workflow-verify ZWILL_SURVEY=<survey>
make -C <study> present ZWILL_SURVEY=<survey>
```

Report separately:

- agent-orchestration cost and time;
- study inference cost and prediction count;
- sample restrictions and malformed rows;
- leakage, baseline, uncertainty, and calibration findings;
- the exact local report and Zwill project paths.
