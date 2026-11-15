---
name: research-instrument-pretesting
description: Pretest, revise, and assess an existing EDSL Survey instrument with the installed Messick CLI. Use when a user brings a survey for static review, cognitive testing, burden or reading-complexity assessment, response-option and branching checks, simulated or human piloting, scale diagnostics, revision comparison, or evidence-bounded readiness for human fielding.
tags: [study-type, quantitative, qualitative, validation, external-tool]
---

# Instrument pretesting with Messick

Use Messick as the sole owner of instrument revisions, intended interpretations
and uses, burden and structural diagnostics, pretest plans, evidence provenance,
issues, decisions, scale analysis, validation claims, and analytic report
context. EDSL owns Survey objects and inference; Humanize owns optional human
fielding; the main agent owns the final branded report.

Do not recreate Messick analyses in study scripts, edit `.messick/`, conflate
simulated and human evidence, or call an instrument globally “valid.” Validation
is always bounded to a declared interpretation, population, use, and evidence
tier. A simulation-only pretest can complete without human evidence.

## Plan the evidence tier

After `skill:workflow-session-start`, load `skill:workflow-file-layout` and
`skill:workflow-plan-template`. Preserve the user’s original Survey as an
immutable artifact. Before initialization, obtain approval for:

- the intended construct, interpretation, population, and use;
- static, simulated-cognitive, simulated-behavioral, or optional human evidence;
- consequential decisions or acceptance criteria;
- respondent design, model, cost boundary, and report detail.

Do not make human evidence a universal gate. Recommend it only when the intended
claim or stakes require it.

## Follow the package control loop

After plan approval, initialize visible Messick state inside the study, then
load its guide and first state-derived action in this order:

```bash
messick --project-dir <study> init --title "<study title>"
messick --project-dir <study> agent guide
messick --project-dir <study> agent next
```

Treat `data.recommended_action` as authoritative. Execute its `argv` from its
`cwd`, resolving only declared `input_schema` values. Run `messick agent next`
after every material mutation. Do not guess commands, inspect package source,
parse `--human` output, or skip ahead because another command appears possible.

Use package actions to import the exact Survey, record `intent.json`, inspect
the instrument, measure burden and reachable paths when relevant, adjudicate
issues, plan the selected pretest, analyze ingested evidence, compare revisions
or sources, evaluate the declared intent, and generate bounded report context.
Use `messick validate --strict` before delivery.

The Messick report context is the bounded analytic handoff. Do not run
`ep results export` or guess Results column names to reconstruct evidence that
Messick already normalized into that context. If a required report fact is
absent, stop and report the package contract gap instead of probing raw Results.

## Paid simulation handoff

Messick generates portable model-free Jobs but never runs inference. For the
exact returned Jobs artifact:

1. Load `skill:workflow-model-selection` once and select one current model.
2. Run `ep inspect <Jobs.ep>` and review transmitted context.
3. Run `ep jobs cost <Jobs.ep>`.
4. Present the model, calls, exact package, cost, and likely time; obtain approval.
5. Run the approved package once with an explicit new Results path.
6. Ingest that exact Results path through Messick and resume `messick agent next`.

Any changed model, Jobs, scope, or retry requires fresh exact costing, approval,
and a new Results path. Start with a small cognitive pilot. Describe simulated
responses as diagnostic hypotheses, never observations of human cognition.

## Optional human evidence

Use `messick fielding plan` only after the user authorizes human fielding. Load
`skill:edsl-human-survey` for Humanize mechanics. Preserve consent, sample, and
fielding provenance; never send private human responses or open text to a model
without explicit authorization. Ingest human and simulated sources separately,
and compare them only through an explicit Messick source comparison.

## Revise and report

Instrument changes create a new Survey revision; never replace the registered
original. Record why each issue was revised, removed, accepted, rescored, or
reordered, then compare revisions through Messick.

When the user asks for a revised instrument, save it as an EDSL Survey artifact,
import it as a new Messick revision, and use that canonical revision—not a
freehand report section—as the source for the revised item list and item count.
Before delivery, confirm that every stated count matches the revision's
`ordered_question_ids` and that the report contains each ID exactly once.

Generate `messick report context` and `messick report template`, then load
`skill:report-authoring`. Author `<study>/writeup/report.md` and HTML from the
package artifacts. Report question-level findings, burden estimates, evidence
sources, revisions, unresolved limitations, and the strongest defensible next
step. Finish with `ep report check` and one `ep workflow verify`; require
`all_gates_passed: true`. Keep everything local unless publication is approved.
