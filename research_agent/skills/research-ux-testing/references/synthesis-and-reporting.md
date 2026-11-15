# Synthesis & reporting — turning runs into deliverables

Post-study analysis for completed uxtest runs. Prerequisite: traces under
`uxtest_store/studies/<id>/runs/*/trace.jsonl` and analysis in `analysis/`. All
commands here read existing evidence; only `--launch`/inference steps spend EDSL
credits.

**These produce evidence, not the final deliverable.** The study's deliverable is
`writeup/report.md` (see `skill:report-authoring` and `skill:workflow-file-layout`),
which you write by synthesizing and citing the artifacts below. uxtest's own
`report.html`/`uxr_report.html` are intermediate evidence, not the report you
hand over.

## Contents

- [Narrative (stakeholder) report](#1-narrative-stakeholder-report)
- [Cross-study synthesis (batch)](#2-cross-study-synthesis-batch)
- [Export runs as EDSL agents](#3-export-runs-as-rich-edsl-agents)
- [Interview the trace agents](#4-interview-the-trace-agents-follow-up-questions)
- [Human-validation survey (humanize)](#5-human-validation-survey-humanize)
- [Saliency overlays](#6-saliency-overlays-attention-evidence)
- [Regenerate base analysis](#regenerate-base-analysis-no-cost)

---

## 1. Narrative (stakeholder) report

`report` reads existing traces/screenshots/findings/scores and writes a
narrative. It uses pandoc for the HTML/PDF formats.
```
uxtest report <study-id>                       # -> analysis/narrative_report.md
uxtest report <study-id> --format md,html,pdf
uxtest report <study-id> --output-dir <dir>    # redirect out of the store
```
When **you** (the agent) write the narrative instead, read the packaged guide
first: `uxtest docs show report-writer-agent`. It covers which artifacts to
cite, how to use `action_outcome` and `stop_quality`, and how not to overclaim
from synthetic browser evidence.

Read at least: `study.yaml`, `analysis/scores.json`, `analysis/findings.json`,
`analysis/log.html`, `runs/*/meta.json`, `runs/*/trace.jsonl` (and any
`comparisons/<c>.html`). Write Markdown first, then compile.

Report structure (unless asked otherwise): 1) title + one-paragraph summary;
2) context (product, page, audience, why); 3) method (personas, devices, runs,
step budget, Playwright + EDSL remote inference); 4) what happened (journeys,
first clicks, paths, confusion, stopping points); 5) results (outcomes, failure
modes, strongest findings); 6) 3–6 conclusions tied to observed behavior;
7) follow-on steps (separate product/site work from tool/model limits);
8) appendix (study/run ids, artifact paths).

Style: lead with what was learned; distinguish UX friction from runtime errors,
and site findings from model/tool limits; no statistical-validity claims from
small synthetic samples; say "synthetic visitors" / "persona runs"; only cite
screenshots that exist in traces/findings.

## 2. Cross-study synthesis (batch)

Deduplicate recurring findings and roll several studies into one report.
```
uxtest batch report <name> \
  --title "Cross-Study Report" \
  --study <id-a> --study <id-b> \
  --comparison uxtest_store/comparisons/<c>.html \
  --format md,html,pdf \
  [--output-dir <dir>]
```
Or run fixtures then synthesize from a manifest:
```
uxtest batch run <manifest>.yaml     # manifest lists id, title, formats, fixtures[]
```
Batch reports classify each action (`url_navigation`, `menu_opened`,
`no_visible_change`, …) and run resolution (`done`,
`enough_evidence_but_continued`, `looping`, `blocked_by_auth`, …), so
non-navigation clicks aren't all treated as failures. Output →
`uxtest_store/comparisons/`.

## 3. Export runs as rich EDSL agents

One EDSL `Agent` per run, carrying persona, task, outcome, journey,
visible-text snippets, actions, thinking, frustration, and screenshots as
`FileStore`s. This is the bridge back to EDSL-native workflows (e.g.
`skill:edsl-agent-lists`).
```
uxtest agents export <study-id>              # -> analysis/agent_list.py (+ manifest)
python uxtest_store/studies/<id>/analysis/agent_list.py   # inspect without inference
uxtest agents export <study-id> --output <path>
```
`build_agent_list()` in the script returns an `AgentList` for downstream EDSL
jobs.

## 4. Interview the trace agents (follow-up questions)

Ask EDSL follow-up questions of those rich per-run agents.
```
uxtest interview <study-id> \
  --question "What made the company feel serious or not?" \
  --question "What would you need before converting?"
python uxtest_store/studies/<id>/analysis/agent_interview.py            # dry run
python uxtest_store/studies/<id>/analysis/agent_interview.py --launch   # spends credits
```
Good for: what each visitor believed after screen 1, which proof was actually
seen before converting, which screenshots to quote, where personas disagree.

## 5. Human-validation survey (humanize)

Turn selected screenshots into an EDSL `humanize()` survey real people answer
(it does not record human browser sessions).
```
uxtest humanize-export <study-id> \
  --template task-discovery \      # task-discovery | credibility | conversion | comprehension
  --screenshots representative \   # first | last | first-last | high-frustration | all
  --max-screenshots 8
python uxtest_store/studies/<id>/analysis/humanize_survey.py           # prints counts, safe
python uxtest_store/studies/<id>/analysis/humanize_survey.py --launch  # creates the survey
```
Tune presentation via `HUMANIZE_SCHEMA["survey"]["custom_css"]` in the generated
script — do not downscale the original trace screenshots. Use the manifest to
see exactly which run/persona/step/screenshot each item came from, then compare
human stated intent against the synthetic traces.

## 6. Saliency overlays (attention evidence)

Visual-attention overlays for study screenshots. Requires a REAL external
saliency model command (uxtest never fabricates maps; it fails if none is set),
passed explicitly as a command template:
```
uxtest saliency run <study-id> --engine command \
  --command-template "python /path/inference.py --img_path {input} --output_path {output_dir} ..." \
  --screenshots representative --max-screenshots 12
```
Output → `analysis/saliency/` (manifest records the exact command, return code,
overlay, and which run/step/action each came from). Do not fabricate attention
maps or recreate an agent-side eye-tracking pipeline when no saliency engine is
available; report that the requested modality could not be produced.

## Regenerate base analysis (no cost)

If findings/scores look stale, rebuild from traces before synthesizing:
```
uxtest analyze <study-id> --include-interrupted
uxtest uxr <study-id>
```
