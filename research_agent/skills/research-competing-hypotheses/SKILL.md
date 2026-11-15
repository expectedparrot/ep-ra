---
name: research-competing-hypotheses
description: Conducts an auditable Analysis of Competing Hypotheses with the installed Langley CLI. Use when the user needs to compare multiple explanations against a shared body of evidence, investigate causes without prematurely confirming a favored theory, assess intelligence or incident hypotheses, test linchpin evidence and assumptions, identify what could change the assessment, or produce a traceable ACH matrix and report.
tags: [study-type, qualitative, analysis, external-tool, edsl]
---

# Analysis of Competing Hypotheses with Langley

Use Langley as the hypothesis, evidence, matrix, sensitivity, provenance, EDSL
proposal, validation, and analytic-report owner. Do not recreate ACH scoring,
schemas, state, prompts, or report artifacts in study scripts.

## Fit and boundaries

Use ACH when two or more plausible explanations must be tested against the same
evidence and disconfirmation matters. Route prospective failure analysis to
`skill:research-premortem`, external futures to `skill:research-scenario-planning`,
fixed-option value tradeoffs to `skill:research-decision-support`, and evidence
retrieval or synthesis without competing causal explanations to
`skill:research-literature-review`.

Langley does not find or verify evidence. When current external evidence is
needed, use `skill:workflow-web-scraping`, preserve source provenance, and keep
observations distinct from arguments, assumptions, context, and expected-but-
absent observations. ACH inconsistency scores are transparent heuristics, never
probabilities, proof, or an automatic verdict.

## Start and follow the package

After `skill:workflow-session-start`, load `skill:workflow-file-layout` and
`skill:workflow-plan-template`. Approve a plan that fixes the focal question,
scope, evidence boundary, decision owner, review checkpoints, optional model
assistance, report detail, and definition of done.

Initialize Langley inside the approved study and let the package route each
material action:

```bash
langley --project-dir <study>/ach init --title "<title>" \
  --question "<question>" --scope "<scope>"
langley --project-dir <study>/ach guide
langley --project-dir <study>/ach next
```

Run `guide` immediately after `init`, before adding hypotheses. Then use `next`
after each material mutation.

Use `data.action.argv` returned by `langley next` to select the command; repeat
after each mutation. The routed argv intentionally omits task-specific required
values, so run that command's `--help` once and supply them—do not invent option
names. Treat JSON `data`, `artifacts`, `warnings`, `errors`, and `next_steps` as
authoritative. Use `langley status` to resume and only request topics returned
by `langley docs list`. Do not inspect installed source or guess command shapes.

## Facilitate the ACH workflow

- Preserve at least two reasonable, distinguishable hypotheses until evidence
  justifies refinement or archive; record rationale and cited inconsistencies.
- Add evidence with source, credibility, importance, and deception risk. For an
  absence, record why it should have been observable and what search occurred.
- Assess one complete evidence row across every active hypothesis. Seek
  inconsistency; do not count generic consistency as confirmation.
- After setting every row, run `langley --project-dir <study>/ach matrix analyze`
  before drafting a conclusion.
- Review diagnosticity, matrix gaps, non-diagnostic evidence, missing evidence,
  assumptions, alternative interpretations, and possible denial or deception.
- Draft a conclusion that discusses every active hypothesis, residual
  uncertainty, critical evidence, and critical assumptions. The analyst may
  differ from the heuristic ranking only with an explicit rationale.
- Run sensitivity tests on linchpins without mutating the base matrix. Define
  observable indicators, thresholds, sources, and owners that could change the
  assessment.

Keep `.langley/` as the source of truth. Do not edit its events, cache,
proposals, or report manifests directly. Use revision guards returned by the
package when concurrent work is possible.

## Optional model assistance

Langley generates portable, model-free EDSL Jobs for hypothesis proposals,
evidence proposals, matrix rows, red-teaming, and indicators. Model answers are
pending proposals, not accepted analytical judgments.

When `langley next` recommends a job:

1. Load `skill:workflow-model-selection` and make one bounded model query.
2. Execute Langley's routed job-generation command, writing Jobs to an `.ep`
   path (never `.json`).
3. Follow its exact `ep inspect` and `ep jobs cost` handoff.
4. Present the job path, context transmitted, model, calls, cost, and time risk;
   obtain explicit approval.
5. Execute only the approved `ep run` argv, with a foreground timeout of 600000
   ms, then ingest the exact Results artifact.
6. Run `langley --project-dir <study>/ach proposal compare --job <job-id>` once,
   then explicitly accept or reject every proposal with a rationale. Never
   bulk-accept merely because agents agree. The review commands are `compare`,
   `accept`, and `reject`; there is no `proposal review` command.

A changed job, model, iteration count, scope, or retry requires fresh costing
and approval. Never rerun inference to repair ingestion, proposal review,
validation, or reporting. Preserve Jobs, Results, hashes, model provenance,
dissent, rejected proposals, and stale-proposal diagnostics.

## Fragile input contracts

Let Langley own schemas. Before writing an input file, run the routed command's
`--help` or its preceding inspection command and follow the returned fields.
In particular:

- `hypothesis add` requires `--name` and `--description` (not `--label`).
- Matrix cells rated `consistent` or `inconsistent` require an integer
  `strength`; `neutral` and `not_applicable` use no strength.
- Conclusion assessments identify hypotheses with `hypothesis_id`.
- Run `sensitivity suggest`, then submit one sensitivity test for every
  `data.candidates` entry before strict validation—even candidates described as
  low-diagnosticity or less important. Do not select only the "key" candidates.
  A validation failure identifying an untested linchpin is a real
  incomplete-analysis signal, not a command failure to work around.

Before the first matrix, conclusion, sensitivity, or indicator input, read
[input-contracts.md](references/input-contracts.md). Never discover a schema by
submitting `{}`, partial data, invalid enum values, or a guessed subcommand.
Likewise, do not execute a future workflow gate merely to confirm that it fails;
inspect its command help and let final verification execute it once artifacts
exist.

## Validate and deliver

Require strict Langley validation before treating the analysis as complete:

```bash
langley --project-dir <study>/ach validate --strict
langley --project-dir <study>/ach report generate --name final
langley --project-dir <study>/ach report show --name final
```

Langley's `analysis.json`, `matrix.csv`, `report.md`, and `manifest.json` are the
canonical analytic materials. Immediately before writing the branded narrative,
load `skill:report-authoring`; the main agent owns `<study>/writeup/report.md`
and HTML. Explain the least-inconsistent assessment without calling it true,
show why alternatives rank lower, disclose source weaknesses and matrix gaps,
summarize sensitivity results, residual uncertainty, and indicators, and make
every claim traceable to Langley artifacts.

Use workflow gates `plan-approved`, `analysis-ready`, and `report-validated`.
Attest analysis only after strict validation, a current conclusion, completed
linchpin tests, indicators, and a verified Langley report manifest. Finish with
`ep report check` and one `ep workflow verify`; require
`all_gates_passed: true`. Keep outputs local unless publication is explicitly
approved.
