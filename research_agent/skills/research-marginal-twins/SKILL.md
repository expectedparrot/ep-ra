---
name: research-marginal-twins
description: Build auditable synthetic populations from reported survey marginals, crosstabs, or explicitly model-synthetic moment targets with the locked UMRISS CLI. Use when digital twins are requested but respondent-level microdata is unavailable, including support-bank construction, marginal or joint calibration, omitted-marginal validation, weighted AgentList export, and downstream probabilistic surveys.
tags: [study-type, validation, quantitative, external-tool, edsl, report]
---

# Aggregate-target digital twins with UMRISS

Use the locked `umriss` package as the state, construction, calibration, validation, and report owner. Do not recreate its support design, probability parsing, mixture fitting, feasibility checks, or report plots in study scripts.

## Claim boundary

UMRISS constructs a calibrated synthetic population from aggregate constraints. It does **not** reconstruct the unknown people who produced those aggregates.

- With reported survey marginals or crosstabs, preserve their exact source and wording.
- With model-synthetic priors or moments, label every target as synthetic and obtain user approval before treating it as a calibration constraint.
- With neither microdata nor targets, stop and choose whether to acquire observed aggregates or elicit explicitly synthetic targets.
- Never invent pseudo-respondent rows from marginals.

Route respondent-level records with held-out truth back to `skill:research-digital-twins` and Zwill. Route hand-authored coverage personas without aggregate targets to `skill:edsl-agent-lists`.

## Orient from the package

Run once from the intended UMRISS project directory:

```bash
umriss version
umriss capabilities
umriss guide
umriss next
```

Every command returns a versioned JSON envelope. Treat `data`, `warnings`, `errors`, and `next_steps` as authoritative. Follow `next_steps`, and run `umriss next --tag <tag> [--metadata <battery-or-path>]` after every material stage. Inspect command help before inventing an option.

The locked EDSL revision already contains UMRISS’s probabilistic-response contract. Never install packages or change EDSL during a study run.

## Plan the identifiable target

Before execution, record at `<study>/plan.md`:

- population, source, wave, question wording, options, and aggregate targets;
- whether each target is observed or model-synthetic;
- support design and coverage rationale;
- support count and seed;
- marginal and any joint constraints;
- model panel and response-probability method;
- omitted-marginal or other validation design;
- feasibility, effective-support, maximum-weight, and residual gates;
- intended downstream use and prohibited claims.

Target marginals must never appear in individual support-generation prompts. Measure support uniformity before fitting. Aggregate marginals generally do not identify a unique joint distribution; keep joint assumptions explicit and test sensitivity when they matter.

## Preserve the execution boundary

UMRISS prepares Jobs and registers Results. `ep` owns credentials, costing, remote execution, and Results artifacts.

Before every paid run, including retries:

1. Obtain the exact Jobs path from UMRISS.
2. Run `ep jobs cost <jobs.ep>`.
3. Present models, call count, estimate or estimate range, and time risk.
4. Obtain explicit user approval.
5. Run `ep run <jobs.ep> --output <results.ep>`.
6. Register that exact Results package with `umriss support register-results` or the package-returned command.

Do not silently accept incomplete model panels, malformed probability vectors, missing support IDs, or uncovered items. Use package-generated retry artifacts and repeat the cost/approval boundary.

## Validate before delivery

Use package-owned checks appropriate to the design:

- support coverage and blueprint fidelity before calibration;
- target feasibility and residual diagnostics;
- effective support, maximum individual weight, and optimizer convergence;
- leave-one-item-out prediction when the battery has enough items;
- comparisons with uniform, unweighted, and available prior baselines;
- sensitivity to support design, regularization, and synthetic target choices.

Treat omitted-item failures as findings. If only one item or no observed holdout exists, report fit-to-target diagnostics without calling them out-of-sample validation.

## Deliver

Preserve the UMRISS project, prompts, Jobs, Results registrations, support bank, weights, diagnostics, validation outputs, reports, and weighted EDSL AgentList. Present the package-owned HTML report and state separately:

- agent-orchestration and study-inference costs;
- observed versus synthetic target provenance;
- moment fit and validation results;
- identification and sensitivity limitations;
- appropriate and prohibited uses of the exported population.
