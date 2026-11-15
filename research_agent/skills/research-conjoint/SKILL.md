---
name: research-conjoint
description: >
  Designs and runs conjoint analysis and discrete-choice studies with the
  installed Green CLI. Use for product attribute tradeoffs, part-worths,
  attribute importance, willingness-to-pay, preference segments, market-share
  simulation, price sensitivity, or configuration optimization using simulated
  agents, human respondents, or imported choice data.
tags: [study-type, market-research, quantitative, external-tool, edsl]
---

# Conjoint analysis with Green

Use Green as the definition, provenance, design, fielding-handoff, ingestion,
estimation, and analytic-report owner. Never recreate its profiles, EDSL survey,
choice encoding, MNL/HB/latent-class estimators, part-worths, WTP, simulations,
or plots in skill scripts.

## Route and initialize

Use conjoint when respondents choose among decomposable configurations and the
goal is quantitative tradeoffs. Route finished-concept reactions to
`skill:research-concept-testing`, internal fixed-option decisions without a
respondent panel to `skill:research-decision-support`, and undeveloped
configuration spaces to `skill:research-product-design` first.

After `skill:workflow-session-start`, load this owner and verify once:

```bash
green version
ep check
```

Use `skill:workflow-file-layout`, then `skill:workflow-plan-template`. Before
initializing Green, approve a plan that fixes:

- the decision, target population, and fielding source;
- 3–7 independent attributes, realistic levels/ranges, and prohibitions;
- whether rejection is realistic (`option none`);
- tasks per respondent, alternatives per task, versions, and seed;
- the first estimator and requested outputs;
- report detail, cost boundary, and definition of done.

Initialize inside the approved study, then let Green route every material step:

```bash
green --project-dir <study>/conjoint init --type generic-conjoint \
  --description "<decision focus>"
green --project-dir <study>/conjoint guide
green --project-dir <study>/conjoint next
```

Run `green next` after each stage and execute its returned action rather than
guessing command shapes. Read JSON `data`, `artifacts`, `warnings`, `errors`,
and `next_steps`. Never use `--force` without explicit approval.

## Elicit and define

Most users need help converting a fuzzy product question into attributes.
Suggest a compact starting design and obtain confirmation; do not demand a
complete specification. Prefer 3–5 levels per categorical attribute and a
continuous price/cost range when WTP or revenue matters. Add prohibitions only
for genuinely impossible combinations and enable `option none` when opting out
is realistic.

Use only Green commands for dimensions, levels, constraints, interactions,
reference levels, agent lists, and validation. Batch large panels through
`agent add-batch`; preserve respondent traits needed for segmentation. Run
`green validate` before generating a design.

Default to deterministic full-factorial generation with 12 tasks, 3
alternatives, one version, and a recorded seed unless the approved plan differs.
Inspect Green's actual task count and warnings; do not assume the requested
count survived prohibitions or a small profile space.

## Fielding boundary

Use `design codegen` to create inspectable work under `green_jobs/`. Treat its
`green-edsl-handoff-v1` manifest as authoritative. Do not write a parallel
survey, Jobs package, runner, normalizer, or ID mapping.

Before paid model-agent fielding:

1. Load `skill:workflow-model-selection` and make one bounded model query.
2. Run the manifest's exact build action and inspect the generated design/job.
3. Run `green plan field` and present design, respondents, tasks, predicted
   model calls, outputs, runtime risk, exact model, and exact package path.
4. Cost the exact built Jobs package with `ep jobs cost`.
5. Obtain approval for that model, package, scope, and estimate.
6. Execute the manifest's exact approval-gated `ep run` action once.
7. Normalize/import through the exact action returned by `green next`.

Changed design, panel, model, Jobs, retry, or scope requires a fresh plan, cost,
and approval. Never substitute generated `run_survey.py` model execution for the
explicit `ep` cost/run boundary.

For human fielding, generated `--humanize` creates a Coop survey URL, but Green
does not yet retrieve human responses. Preserve the survey identifiers and stop
at that boundary unless results have been exported for supported import; never
claim the human study is complete merely because the URL exists.

For existing choice data, use Green's supported importer and retain source
provenance. Use `simulate stub` only for local contract testing, never as study
evidence.

## Estimate and analyze

Require `data quality` to pass before estimation. Start with MNL for the pooled
baseline. Use HB only when respondent-level utilities materially support the
decision, and latent class only when preference segments are the headline.
Follow Green's approval signal for expensive estimation.

Produce only decision-relevant package outputs:

- `report partworths` and `report importance` for the baseline;
- `report wtp` when a valid continuous price dimension exists;
- `report segments` when traits and sample support comparison;
- market simulation/sensitivity/optimization only for explicitly defined
  candidate products and decision questions.

Save required analytic reports with `green report save`. Treat `.green/` and
saved report `data.json`, `meta.json`, and `report.md` as authoritative evidence.
Do not manually refit or recompute results in pandas/sklearn.

## Deliver

Immediately before narrative writing, load `skill:report-authoring`. Green owns
the analytic materials; the main agent owns `<study>/writeup/report.md` and its
branded HTML. Explain design, population, fielding mode, model, quality,
part-worths, importance, WTP/share results, uncertainty, simulation limits, and
the decision implication without presenting simulated preferences as human
population estimates.

Use three workflow gates: `plan-approved`, `analysis-ready`, and
`report-validated`. Attest analysis only with passing Green validation/quality,
the fitted-model path, and saved report artifacts. Finish with `ep report check`
and one `ep workflow verify`; require `all_gates_passed: true`. Do not publish
without permission.
