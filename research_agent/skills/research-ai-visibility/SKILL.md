---
name: research-ai-visibility
description: >
  Measures how a brand and its competitors appear in AI-generated answers with
  the installed Aivis CLI. Use for AI visibility, answer-engine optimization
  research, share of voice, mention and recommendation rates, brand framing,
  citation influence, prompt-cluster comparisons, or repeated model tracking.
  Do not use for ordinary web SEO rankings or consumer-product telemetry.
tags: [study-type, market-research, quantitative, external-tool, edsl]
---

# AI visibility research with Aivis

Use Aivis as the sole owner of the prompt library, tracked brands, collection
configuration, immutable samples, versioned judge observations, metrics, and
analysis handoff. Do not rebuild its collection, extraction, metric, or storage
logic in EDSL or ad hoc Python.

## Establish the measurement claim

Use this method when the question is how named brands appear in answers from
specified API models. Explain at the outset that API responses are proxy trend
lines—not replicas of consumer AI products with browsing, memory,
personalization, or product-specific instructions. Route website usability to
`skill:research-ux-testing`, message reactions to
`skill:research-message-testing`, and general web search or SEO auditing to the
appropriate discovery workflow.

Before initializing, confirm or propose:

- focal brand, aliases, and genuinely comparable competitors;
- the audience decisions represented by the prompts and a small set of prompt
  clusters;
- engines, repetitions, cadence, and whether this is a baseline or repeat run;
- the decision the evidence should inform, report detail, and budget boundary;
- privacy constraints, because raw provider responses may be sensitive.

Avoid promotional or brand-leading prompts. Include category, recommendation,
comparison, and problem-led language only when each reflects a real discovery
journey. Do not imply population representativeness from prompt coverage.

## Follow the package workflow

After `skill:workflow-session-start`, create the approved study root with
`skill:workflow-file-layout`. The locked environment already contains Aivis;
do not install it or inspect package source. Orient once:

```bash
aivis version
aivis capabilities
aivis guide
aivis --help
```

Treat JSON `data`, `warnings`, `errors`, and `next_steps` as authoritative. Use
command `--help` only when a concrete interface remains unresolved. Initialize
inside the study root and keep `.aivis/` as the source of truth:

```bash
aivis init --brand "<brand>" --competitors "<a>,<b>" --no-generate
aivis prompts add "<representative prompt>" --cluster <cluster>
aivis prompts list
aivis configure --engines <engine>[,<engine>] --samples-per-prompt <n>
```

Prefer `aivis prompts import` for an approved prompt CSV. Never edit store JSON
by hand, mutate finalized sample files, or publish raw responses without the
user's authorization. Preserve `.aivis/data/`; keep `.aivis/raw/`,
`.aivis/screenshots/`, and `.aivis/.lock` uncommitted.

## Plan and approve paid collection

Run these in order:

```bash
aivis run --dry-run
aivis doctor
```

Finish all prompt and configuration mutations before preflight; do not run
`configure`, `run --dry-run`, or `doctor` in parallel. Use `--sample` only to
randomly limit the number of active prompts for a run—it does not set
repetitions. Use `configure --samples-per-prompt` for repetitions. Do not probe
bare command groups or guess dotted `config set` keys.

Present the exact prompts, engines, samples per prompt, collection-call count,
judge-call bounds, product-fidelity caveat, and expected cost when available.
Require `data.remote_inference: true` in the dry-run result and
`data.expected_parrot_auth: true` from doctor. If either is false, stop and fix
the project configuration or Coop authentication; do not fall back to direct
provider keys.
Obtain explicit approval before `aivis run`. A changed prompt library, engine
set, repetition count, or retry is a new paid scope and needs fresh approval.
Do not substitute `ep run`: Aivis owns its EDSL collection boundary.

After collection, inspect `aivis report --run last`. If extraction is incomplete, use
`aivis extract --estimate` before obtaining approval for additional judge work.
Do not treat an incomplete or partial run as complete merely because some
samples exist.

## Analyze and deliver

Generate the bounded handoff rather than loading the flat-file store:

```bash
aivis report-context --run last --out analysis/aivis_report_context.json
```

Lead with `reportability`, planned and successful sample coverage, engine
failures, and denominators. Use supplied metric values exactly; do not
recompute them from excerpts. Compare share of voice, mention rate,
recommendation rate, recommendation conditional on mention, and first position
only where their denominators support the comparison. Distinguish engine,
cluster, and prompt-level patterns. Cite the handoff's evidence and sample IDs
for claims about particular answers; do not infer causality from citation
co-occurrence or call a single excerpt representative.

Aivis owns analytic evidence, not the stakeholder narrative. Load
`skill:report-authoring` immediately before writing
`<study>/writeup/report.md`; the research agent owns the branded HTML. State
the engine and prompt scope, run date, repetitions, coverage, judge version,
small-sample warnings, API-product caveat, and practical next measurement.
Never frame simulated answer visibility as consumer exposure, market share, or
proof that an intervention caused a change.

## Golden rules

- Let Aivis own collection, extraction, metrics, and stored evidence.
- Dry-run and doctor before every approved paid scope.
- Preserve immutable samples and private raw responses.
- Use `report-context`; never scrape or manually aggregate the store.
- Qualify results to the observed prompts, engines, and successful samples.
