---
name: research-decision-support
description: >
  Compare fixed alternatives with MCDA using
  explicit criteria, stakeholder weights, performance evidence, weighted-sum,
  or ELECTRE III. Use for vendor, site, grant, portfolio, procurement, hiring,
  or policy choices where the options already exist and stakeholders value
  criteria differently. Use skill:research-product-design when the options are
  configurations whose dimensions or values are themselves being designed.
tags: [study-type, quantitative, analysis, external-tool, edsl]
---

# Decision support with MCDA

Use MCDA as the decision-state, elicitation, ingestion, aggregation, and
analysis owner. Do not recreate its Jobs or calculations in skill scripts.

## Runtime and routing

The environment pins compatible MCDA and EDSL revisions. Never install or
upgrade them during a study. `mcda` is standalone, never an `ep` subcommand.
After `skill:workflow-session-start`, load this owner before probing MCDA or
giving method-specific advice. Verify once:

```bash
mcda capabilities
ep check
```

Use `mcda -C <project> guide` at entry and `mcda -C <project> next` after each
material stage. Their JSON envelope and `next_steps` are authoritative. Read
[method-selection-guide.md](references/method-selection-guide.md) only when the
choice between weighted-sum and ELECTRE III is consequential or unclear.

Route configurable designs to `skill:research-product-design`, finished-concept
response to `skill:research-concept-testing`, attribute preference estimation to
`skill:research-conjoint`, futures to `skill:research-scenario-planning`, and
failure pathways to `skill:research-premortem`.

## Plan, initialize, and freeze

Use `skill:workflow-file-layout`, then `skill:workflow-plan-template`. Write and
approve `<study>/plan.md` before initializing MCDA. The plan must identify:

- decision owner, fixed candidates, and optional status-quo reference;
- 3–8 discriminating leaf criteria, direction, units, and evidence source;
- participants and whether weights are supplied, human-elicited, or proposed
  for explicit approval;
- which performance values are factual versus simulated judgments;
- analysis method, missing-data policy, report detail, and definition of done.

IDs use letters, digits, and underscores and cannot start with a digit. After
approval, initialize inside the study and inspect the guide:

```bash
cd <absolute-study-root> && mcda init decision --description "<question>"
mcda -C <absolute-study-root>/decision guide
```

Initialize MCDA before workflow setup so verifier paths exist. Use three compact
gates: `plan-approved`, `analysis-ready`, and `report-validated`. Make the last
two `agent-attestation` gates because result IDs and paths are generated later.

## Build auditable decision state

Follow `next_steps` while preserving these review boundaries:

1. Confirm candidate and reference alternatives before `alt add`.
2. Present criteria, directions, units, hierarchy, and double-counting risks
   before `crit add` or `crit add-group`.
3. Add participants and traits. Keep criterion weights separate from alternative
   performance: weights express importance; assessments estimate performance.
4. Record weights with `weights set` only after the user approves their source
   and interpretation. Raw sibling weights need not sum to 100.
5. Record sourced objective performance directly with `perf set`. Preserve its
   provenance in the plan/report and do not ask a model to rediscover supplied
   facts.
6. For subjective performance, use `mcda -C <project> assessment build --id
   <round_id> --criteria <subjective-id,...>`. Select only criteria requiring
   agent judgment so factual fields are not re-elicited. Confirm the manifest's
   selected and excluded criteria. Do not hand-build surveys, Jobs, manifests,
   ingestion scripts, or ID mappings.

Use reference alternatives for a status quo that should inform comparison but
not become the default candidate recommendation. Treat simulated stakeholder
scores as hypotheses, not evidence of population preferences or real-world
performance.

## Paid inference boundary

MCDA generates portable Jobs and ingests Results; `ep` owns costing and paid
execution. Follow the exact paths and commands returned by `assessment build`.
Before each paid run or retry:

1. Load `skill:workflow-model-selection` and make its bounded model query.
2. Preview the exact assessment and verify expected answer counts.
3. Run `ep jobs cost <absolute-jobs-path> --model <model>`.
4. Present the package path, model, scope, and estimate for approval.
5. Run the approved package once with `ep run` and an explicit Results path.
6. Call `mcda assessment ingest` with that exact Results package.

Require `imported_answers` to equal the manifest's `expected_answers` before
analysis. Zero or partial import is an upstream contract failure. Preserve the
Results and stop: never extract answers manually, generate a Python bridge, or
replay them through `mcda perf set`.

Use literal absolute Jobs paths so approval accounting can match cost and run.
Never substitute `ep inspect`, manual token arithmetic, ambient Python, or the
legacy skill scripts for package costing or ingestion. Changed Jobs, model,
retry, or additional assessment requires fresh costing and approval.

## Analyze and deliver

Use weighted-sum for a transparent compensatory score. Use ELECTRE III when
indifference/preference thresholds, vetoes, and incomparability are meaningful;
record thresholds before running it. When useful, run both and explain method
disagreement rather than forcing consensus. Inspect candidate and
reference-inclusive rankings and trace claims to resolved weights, performance,
contributions, credibility, relations, and source records.

Run analysis with `--role primary` and participant/sensitivity
reruns with `--role robustness`. If `guide` reports ambiguous primary selection,
follow `analyze primary set <analysis-id>`.

After analysis, run `mcda -C <project> report guide` and require
`ready_for_report_agent: true`; resolve its blockers and treat its canonical
evidence and writing rules as authoritative. Run `mcda -C <project> report template`
once for the non-narrative skeleton. MCDA owns this handoff, not the
final narrative; do not reconstruct it from raw state.

Immediately before authoring the narrative, load `skill:report-authoring`. Write
`<study>/writeup/report.md`, compile it to HTML, and run `ep report check --root
<absolute-study-root>` exactly once. Report the decision context, alternatives,
criteria, weight provenance, performance evidence, both candidate and reference
results, uncertainty/incomparability, robustness checks, and next validation.
Attest `analysis-ready` with the exact MCDA result path and successful ranking;
attest `report-validated` only after the report check passes. Finish with one
`ep workflow verify` and require `all_gates_passed: true`. Do not publish without
permission.
