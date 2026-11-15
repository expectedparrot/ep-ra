---
name: research-qualitative-data-analysis
description: >
  Builds, imports, browses, and analyzes text corpora with the installed
  Bewley CLI. Use when collecting documents, articles, interviews, transcripts,
  or field notes into a research corpus, exploring source texts before coding,
  or developing themes, coded evidence, memos, and qualitative findings.
tags: [study-type, qualitative, analysis, content-analysis]
---

# Qualitative Analysis with Bewley

Use the locked `bewley` CLI as workflow and state owner. Do not recreate its
event model, open-coding pipeline, quote resolution, or renderers in skill-local
Python.

## Choose this method

Use Bewley for a research corpus of source texts, including collection,
import, organization, and browsing before any coding is requested. It also
owns interpretive categories, coded passages, and claims traced to source
evidence. Load `skill:workflow-web-scraping` when acquiring texts from websites;
collection feeds the corpus and does not require a codebook or paid inference.
Use `skill:methods-thematic-analysis` for lightweight
classification of many short responses and `skill:methods-transcripts-to-personas`
when the deliverable is an AgentList rather than qualitative findings.

## Runtime and project

Bewley is provided by the locked ep-agent environment. Never install or upgrade it during
a study. Create the study through `skill:workflow-file-layout`:

```bash
ep study scaffold \
  sessions/topic_<alias>/study_a --template qualitative-analysis
```

The owned project lives at `analysis/bewley_project/`. Copy or materialize
source files under its `corpus/`; never add absolute or outside-root paths.

From the Bewley project root, begin with:

```bash
bewley guide
bewley next
```

Treat each schema-2.0 JSON envelope as authoritative. Branch on `status`, retain
`argv` for provenance, and execute only reviewed `next_steps`. Each suggested
action declares mutation, network, and approval requirements. Do not invoke
`--help`, inspect package code, parse human output, or guess the next command.
Use `--human` only for material being shown to the user.

## Analytical workflow

For corpus-only work, preserve source text and provenance, register the
documents, run `bewley fsck`, and export the requested corpus browser. Stop
there when that is the approved scope; do not require coding, analytic memos,
model selection, or an inference pilot just to collect or read documents.

When the user requests qualitative analysis:

1. Clarify the research question, corpus, privacy needs, metadata, and desired
   annotation unit. Default to speaker-turn or paragraph spans for interviews.
2. Pilot 3–5 representative documents before scaling.
3. Preserve speaker labels and source metadata; add documents through Bewley.
4. Develop a sparse codebook with explicit inclusion rules. Review candidate
   codes and evidence with the user before applying them broadly.
5. Apply codes to exact line or byte spans. Use document-level codes only for
   genuinely document-level properties.
6. Record analytic interpretation in memos; query coded evidence and refine the
   code hierarchy without discarding event history.
7. Export compact quote tables, counts, HTML exploration, and theory artifacts.
8. Run `bewley fsck` before downstream reporting.

## Open coding and paid inference

Bewley packages open-coding work as portable EDSL Jobs but never runs models.
Confirm a current model through `skill:workflow-model-selection`, generate the
job through the surfaced `next_step`, estimate it, obtain approval, and run it
explicitly:

```bash
ep jobs cost <jobs.ep>
ep run <jobs.ep> --model <confirmed-model> --output <results.ep>
```

Then use the Bewley ingestion action. Preserve Jobs, Results, model, candidate
code CSV, and cost provenance. Never rerun paid inference to fix ingestion,
annotation, export, or reporting. Audio/video transcription is also networked
and requires explicit approval.

## Evidence and reporting

Do not treat command success as evidence success. Validate exported quote rows
contain a stable document identifier, code, exact excerpt text, and relevant
participant metadata. If exact text is absent, omit representative quotations
rather than inventing or paraphrasing support.

Use package-owned exports as inputs to `skill:report-authoring`. Distinguish
participant evidence, analyst interpretation, negative cases, and limitations.
Keep source materials and outputs local unless publication is explicitly
requested.

## Completion

For corpus-only work, completion requires registered readable documents,
source provenance, a clean integrity check, and the requested export. Verify
the browser contains uncoded documents; do not add dummy annotations to make
them visible.

For coded analysis, completion requires an intact event log, reviewed codebook,
traceable annotations, analytic memos, nonempty evidence exports, clean
`bewley fsck`, a local HTML evidence browser, and a report whose findings link
to coded excerpts.
