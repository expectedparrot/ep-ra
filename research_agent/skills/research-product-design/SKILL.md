---
name: research-product-design
description: >
  Explore, generate, evaluate, and shortlist product, service, feature,
  packaging, policy, or strategy options with the locked Zwicky CLI. Use when
  the user wants to map a design space, define dimensions and values, eliminate
  incoherent combinations, compare configurations across stakeholders or
  criteria, test utility or pairwise preferences, examine price and Pareto
  tradeoffs, or choose concepts to prototype. Route fixed non-decomposable
  choices such as vendors or locations to skill:research-decision-support.
tags: [study-type, qualitative, market-research, external-tool, edsl]
---

# Product design and option evaluation with Zwicky

Use Zwicky as the sole project store and consistency, sampling, jobs, and
analysis owner.

## Runtime contract

The environment pins compatible Zwicky and EDSL revisions. Never
install or upgrade either during a study. Verify once:

```bash
zwicky --help
ep check
```

`zwicky` is standalone. Never try `ep zwicky`, `python -m zwicky`, `pip show
zwicky`, or source inspection. Avoid routine `--help` probes; use `zwicky guide`
and the quick reference only for a genuine gap.

For bounded CCA, issue direct `zwicky cca set` commands together and trust exit
status. Do not pipe JSON into Python, generate a shell loop, or parse
acknowledgements; inspect `zwicky cca list` once after the batch.

Use `zwicky guide` as the contract. Read
[zwicky-cli-quickref.md](references/zwicky-cli-quickref.md) only for a genuine
gap.

## Fit and boundaries

Put supplied and generated options in the same box. Route:

- fixed, non-decomposable choices such as vendors, sites, or grant portfolios
  to `skill:research-decision-support`;
- finished-concept response to `skill:research-concept-testing`;
- stable-attribute preference estimation to `skill:research-conjoint`;
- external futures to `skill:research-scenario-planning`;
- failure pathways to `skill:research-premortem`.

Simulated evaluations are hypotheses, not proof.

## Start from the product decision

After `skill:workflow-session-start`, use `skill:workflow-file-layout`. Load
`skill:workflow-plan-template`, write `<study>/plan.md`, present it, and obtain
approval before initializing Zwicky. Record the owner, decision, constraints,
stakeholders, evidence boundary, depth, and deliverables.

Then initialize visible package state inside the approved study:

```bash
cd <absolute-study-root> && zwicky init product-design --problem "<decision question>"
zwicky -C <absolute-study-root>/product-design guide
```

The positional argument to `zwicky init` is a project **name**, not a destination path.
Treat the JSON response from `guide` as authoritative; follow it after material
stages. Never edit `.zwicky/` directly or guess legacy commands.

Initialize the Zwicky project **before** creating the study workflow; preflight
requires its directory. Then create three gates in one `ep workflow setup`
call. Use `agent-attestation` for generated future state.

## Design funnel

Frame the decision; propose independent dimensions and exclusive values;
present constraints before recording them; enumerate and sample
deterministically; then evaluate only as deeply as needed. Use
stakeholder/criteria utility for Pareto, disagreement, sensitivity, and
shortlisting; pairwise preference for choice or price sensitivity; and
D-optimal sampling plus Bayesian follow-up for costly spaces. Preserve IDs and
uncertainty. Never make a package score the automatic decision.

For a named-criteria assessment, pass every registered criterion explicitly:

```bash
zwicky -C <project-dir> utility build --sample <sample-id> --criteria <id-a>,<id-b>
```

Never omit `--criteria` after registering criteria; omission deliberately builds
the legacy single `utility` criterion. Before sensitivity or Pareto shortlisting,
confirm `analysis.json` contains the expected criterion IDs. If it does not,
stop with a package-contract defect—do not call incompatible commands or create
a manual shortlist.

Obtain review before constraints, paid evaluation, and the final shortlist.

## Preserve the paid-inference boundary

Zwicky builds portable EDSL Jobs; `ep` owns authentication, costing, inference,
and Results. Before every paid run:

Select a current model through `skill:workflow-model-selection`. Cost every
exact package with `ep jobs cost`, report the combined estimate, obtain approval
for the named package set and model, run each once with explicit outputs, and
ingest the exact Results into their originating assessment.

Never rerun inference to repair downstream work. Changed Jobs, models, retries,
or shards require fresh costing and approval.

Use the literal absolute Jobs path in every cost and run command. Do not hide
package identity behind shell variables such as `$ASMNT` or `$JOBS`; the audit
harness must be able to match each costed package to its approved execution.
Cost all packages before the single approval card, then run exactly that set:

```bash
ep jobs cost /absolute/path/jobs-panel-01.ep --model <model>
ep jobs cost /absolute/path/jobs-panel-02.ep --model <model>
# AskUserQuestion names both paths, the model, and the combined estimate.
ep run --jobs /absolute/path/jobs-panel-01.ep --model <model> --output /absolute/path/results-panel-01.ep
ep run --jobs /absolute/path/jobs-panel-02.ep --model <model> --output /absolute/path/results-panel-02.ep
```

`ep inspect` is useful for structure but is not a cost estimate. Never replace
`ep jobs cost` with manual token arithmetic. The commands above are documented;
do not probe `ep run --help`, `ep costs --help`, `ep results cost --help`, or
`ep inspect --help` during a routine product-design study.

## Validate and deliver

Use `zwicky report guide` and `zwicky report template` as the writing handoff.
Write `<study>/writeup/report.md`, compile `<study>/writeup/report.html`, then
run `ep report check --root <absolute-study-root>` exactly once. Never use a
failed pre-compilation check as a way to discover that HTML is required.
Preserve assumptions, exclusions, costs, uncertainty, and next tests. Do not
publish without permission.

Use three gates: `plan-approved`, `analysis-ready`, and `report-validated`.
Because IDs and paths are generated later, make the last two
`agent-attestation` gates. Attest `analysis-ready` with the exact `analysis.json`
path and successful analysis, disagreement, and sensitivity evidence. Attest
`report-validated` after `ep report check --root <absolute-study-root>` passes,
citing the canonical `<study>/writeup/report.html`. Keep the report at the study
root, not inside the Zwicky project.

Do not copy, mirror, or symlink artifacts to satisfy a mistaken gate, or replace
frozen gates. Report incorrect evidence instead of relocating artifacts; do not invent `zwicky utility show`.
