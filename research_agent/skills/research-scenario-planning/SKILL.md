---
name: research-scenario-planning
description: Explore strategic decisions under external uncertainty with the installed Kahn CLI and structured two-axis scenario planning. Use when the user wants multiple plausible futures rather than a forecast, including environmental forces, critical uncertainties, four scenario narratives, early-warning signals, strategic option robustness, AI-assisted research or narratives, and a decision-oriented scenario report.
tags: [study-type, qualitative, market-research, external-tool, edsl]
---

# Scenario planning with Kahn

Use Kahn as the project state, phase, validation, EDSL Jobs, ingestion, and
analytic-artifact owner. Do not recreate its schemas, workflow, option scoring,
prompts, or report data in study scripts.

## Fit and claim boundary

Use Kahn for decisions shaped by external uncertainty that need plausible
futures, robust options, and warning signals. Route failures to
`skill:research-premortem`, competing explanations to
`skill:research-competing-hypotheses`, criterion tradeoffs to
`skill:research-decision-support`, and configuration spaces to
`skill:research-product-design`.

Scenarios are not predictions. Do not attach probabilities, expected values, or
claims of likelihood without a separate defensible method.

## Start and follow Kahn

After `skill:workflow-session-start`, use `skill:workflow-file-layout`, then
`skill:workflow-plan-template`. Approve a plan that states the decision owner,
focal question, horizon, domain, evidence sources, user-review checkpoints,
optional inference, report detail, and claim limits.

Request initialization inside the approved study:

```bash
kahn guide
kahn next --project-dir <study>/scenario-plan
```

Execute `data.action.argv` exactly from `data.action.cwd`, which may be an
existing ancestor before initialization. Retain the absolute `--project-dir`.
Supply only `data.action.input_schema` inputs via their `flag` or `position`,
including every `required` field; never invent flags or substitute mutations.
After each mutation, including failures, obtain a fresh successful `kahn next`
response before another mutation. Never batch a mutation with its prerequisite
`next` call. Check exit status before decoding; failures may return plain text.
Treat JSON `status`, `data`, `warnings`, `errors`, and `next_steps` as authoritative;
never parse `--human`. Use `kahn docs show workflow` for facilitation and
`kahn docs show cli-reference` for unclear action syntax. Do not inspect installed
source or guess commands.

Keep every command on the same explicit absolute `--project-dir`. Preserve
Kahn-managed state and save package snapshots before consequential revisions.

## Facilitate consequential judgments

- Capture 8–15 external forces across multiple PESTEL domains, including
  predictable trends and at least two genuinely uncertain high-impact drivers.
- Ask the user to review the force inventory before locking it.
- Select two high-impact, low-predictability, reasonably independent axes;
  define concrete, plausible, value-neutral poles and run Kahn’s independence
  check before user approval.
- Build four distinct scenarios. Give each a name, tagline, present-tense
  narrative, predetermined elements, opportunities, threats, and at least three
  observable warning signals.
- Add 3–6 actionable options, including a no-regret move or hedge and a bold or
  contingent bet. Evaluate every option across every scenario with a rationale.
- Review robustness, fragility, contingent actions, and monitoring triggers
  rather than optimizing for a preferred future.

Before every irreversible phase advance, execute Kahn’s returned checks,
present the substantive judgment to the user, save a named snapshot, and obtain
approval. Never revise locked package state directly.

## Optional model assistance

Kahn generates model-free EDSL Jobs for force research, narratives, and option
evaluation. Use assistance when valuable; follow Kahn's returned paths and steps.

For every proposed run:

1. Load `skill:workflow-model-selection`; make one bounded current-model query.
   Select a model that handles structured output reliably for both narratives
   and option evaluations.
2. Generate and inspect the exact Jobs artifact with `ep inspect`.
3. Cost it with `ep jobs cost`.
4. Present the package path, transmitted context, model, calls, cost, and time
   risk; obtain explicit approval.
5. Execute the approved foreground `ep run` with a 600000 ms timeout and an
   explicit Results path.
6. Ingest those exact Results through Kahn and resume with `kahn next`.

A changed package, model, scope, iteration count, retry, or extra scenario
requires a fresh exact `ep jobs cost` and approval. Every retry must write to a
new Results path; never overwrite or reuse an earlier Results package. Never
rerun inference to repair ingestion, validation, or reporting. Preserve Jobs,
every Results attempt, hashes, and model provenance.

## Validate and deliver

When `kahn next` reaches reporting, run the package-returned validation and report
commands. Kahn’s `output/summary.md`, strategy matrix, recommendations, signal
dashboard, and exported artifacts are canonical analytical evidence. Use
`kahn report export --format html` only for its optional standalone rendering.

Immediately before writing the final branded narrative, load
`skill:report-authoring`. The main agent owns `<study>/writeup/report.md` and
HTML. It must explain the focal decision, axes and independence, all four
futures and signals, option robustness and fragility, contingent actions,
limitations, evidence sources, and model/orchestration costs while repeating
that scenarios are plausible futures rather than forecasts.

Use workflow gates `plan-approved`, `analysis-ready`, and `report-validated`.
Attest analysis only after Kahn validation and current package artifacts. Finish
with `ep report check` and one `ep workflow verify`; require
`all_gates_passed: true`. Keep outputs local unless publication is approved.
