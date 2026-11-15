---
name: report-quality-review
description: Offer an optional quality review of a completed research report before it is presented, using a one-shot whole-report Jobs package, analysis-specific spotters, several frontier models, and all locally referenced report images. Use whenever writeup/report.md and its figures are complete but final HTML compilation, workflow verification, or presentation has not occurred.
tags: [report, workflow, quality-check, external-tool]
---

# Pre-delivery report review

Use Katz's lightweight whole-report review. Do not initialize a manuscript
ledger, chunk the report, enable academic paper spotters, or invoke the
`skill:research-referee-report` workflow. Katz owns review configuration, attachments,
Jobs construction, and normalized issues. The main agent owns fixes and the
final report.

`Katz` is an internal implementation and CLI name. Never expose it in
user-facing questions, option descriptions, progress updates, or report text;
describe this simply as a quality review or pre-delivery quality review.

## Prepare the review

Require a complete `writeup/report.md` and every plot or generated image it
references. Preview Katz's analysis-type detection and selected spotters:

```bash
katz report review-plan --report <study>/writeup/report.md
```

Accept the detected type when its spotters fit the analysis. Otherwise rerun
with the closest supported `--analysis-type`; do not edit Katz prompts or build
an ad hoc review rubric in the study.

Before querying model catalogs or creating ModelList/Jobs artifacts, ask the
user with `AskUserQuestion` whether they want the optional quality review. Use
the header `Quality review` and the exact option labels `Run review` and `Skip
review`. Present the purpose, detected analysis type and spotters, expected
three model calls, a clearly labeled approximate cost, and a numeric duration
estimate with units (for example, `about 2 minutes`). Do not
describe skipping as unsafe or incomplete. If the user declines, return to
`skill:report-authoring` immediately; do not build review artifacts.

In plain language, ask whether they want to run the review or skip it.

The user's `Run review` answer approves spending only up to the estimate shown.
After building the exact package below, ask again only if its exact cost exceeds
that estimate.

Create the standard report-review panel in one command. The `ep` profile owns
current frontier-capable model selection, image capability, distinct-provider
coverage, and the cached working-model catalog. Do not load
`skill:workflow-model-selection` or make separate model-discovery calls:

```bash
ep models create --profile report-review --count 3 \
  --output <study>/edsl_jobs/report-review.models.ep

katz report review-jobs \
  --report <study>/writeup/report.md \
  --models <study>/edsl_jobs/report-review.models.ep \
  --output <study>/edsl_jobs/report-review.jobs.ep
```

Katz automatically attaches local Markdown images. Repeat `--image` only for a
generated image that matters to the report but is not referenced in Markdown.
Inspect the returned model, attachment, and spotter manifests before inference.

## Confirm and run the review

Inspect and cost the exact embedded-model Jobs package:

```bash
ep inspect <study>/edsl_jobs/report-review.jobs.ep
ep jobs cost <study>/edsl_jobs/report-review.jobs.ep
```

Inspect the returned exact cost, model list, call count, and attachments. If all
are within what the user approved, run the Jobs package once. If the cost is
higher or the package materially differs, present the exact values and obtain a
fresh approval first:

```bash
ep run <study>/edsl_jobs/report-review.jobs.ep \
  --output <study>/data/report-review.results.ep

katz report review-ingest \
  --results <study>/data/report-review.results.ep \
  --report <study>/writeup/report.md \
  --output <study>/analysis/report-review.json
```

Do not rerun because reviewers disagree. Preserve every model's assessment and
the normalized issue artifact.

## Adjudicate and finish

Read the bounded `analysis/report-review.json`. Verify each proposed issue
against the report and study artifacts. Fix supported errors and warnings;
reject speculative, ungrounded, or preference-only comments. Never change a
result merely to satisfy reviewer consensus.

Inspect `complete`, `review_count`, and `parse_failures`. Zero parsed reviews is
a failed optional review, never "zero issues." Incomplete coverage is partial.
Disclose the parsed/requested count in the next update and final handoff. Do not
claim parse failure is unrelated to report quality. Preserve diagnostics. A
retry requires fresh costing and approval; otherwise state that deterministic
checks passed but the optional review did not.

After edits, regenerate any affected plots, compile the final HTML, run the
normal deterministic report check and workflow verification, and only then
present the report. If a fix substantially changes the analysis or introduces
new evidence, treat it as a new report draft and repeat review with fresh cost
approval. Ordinary wording and consistency fixes do not require another paid
review.
