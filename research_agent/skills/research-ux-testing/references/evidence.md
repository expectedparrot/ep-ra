# Evidence — store layout, traces, outcomes

## Contents
- The `uxtest_store/` store
- What to inspect first
- trace.jsonl structure
- Reading outcomes (not the same as runtime errors)
- Debugging checklist

## The `uxtest_store/` store

In the study layout this lives at `data/uxtest_store/` (uxtest creates and finds
it there automatically when you run from the study root).

```
uxtest_store/
├── config.yaml        Store-wide default settings (model, viewport, browser)
├── personas/          Reusable persona templates (*.yaml), referenced by name
├── studies/
│   └── <study-id>/
│       ├── study.yaml     Study definition (id, title, task, success_criteria, personas)
│       ├── runs/          RAW output — the source of truth
│       │   └── run-NNN-<persona>-<hash>/
│       │       ├── meta.json      outcome, timing, persona, variant, final URL
│       │       ├── trace.jsonl    one JSON object per browser step (see below)
│       │       └── screenshots/   step-001.png, step-002.png, …
│       └── analysis/      DERIVED, regenerable from runs/
│           ├── findings.json  scores.json
│           ├── report.html    log.html    uxr_report.html
│           ├── study_plan.md  human_test_protocol.md
│           ├── eval.json/html
│           └── animations/index.html
├── comparisons/       Cross-study / multi-variant synthesis HTML (+ batch reports)
├── cache/             Reserved; currently unused by the code
└── locks/             Per-study lock files (concurrency guard; normally empty)
```

Two layers: `studies/<id>/analysis/` = findings **within one study**;
`comparisons/` = **across** variants/studies. `locks/<id>.lock` exists only while
a study runs (prevents two processes racing the same study's run-id allocation,
pruning, and analysis rewrite); it auto-breaks if the owning process died on the
same host. `cache/` is a placeholder — the real caches are EDSL's own (in EDSL's
home dir) and, for prior packages, a `figma/cache/` subdir.

## What to inspect first

```
uxtest_store/comparisons/<comparison>.html          # variant/study rollup
uxtest_store/studies/<id>/analysis/report.html       # evidence report
uxtest_store/studies/<id>/analysis/log.html          # step-level debug: prompts, screenshots, model answers
uxtest_store/studies/<id>/analysis/uxr_report.html   # UXR-styled report
uxtest_store/studies/<id>/analysis/findings.json     # structured findings
uxtest_store/studies/<id>/analysis/scores.json       # outcomes, frustration, synthetic SUS, stop_quality
```
Raw traces when reports look wrong:
```
uxtest show <study-id> --json
uxtest show <study-id> <run-id> --trace --json
uxtest trace <study-id>            # (--edsl-jobs to see remote job refs)
```

## trace.jsonl structure

JSONL — one object per browser step. Each line has five conceptual layers:

- **Envelope + flattened fields:** `schema_version`, `event_type:"step"`,
  `step`, `ts`, `url`, `page_title`, and `thinking`/`frustration`/`status`
  (promoted from `model_decision` for easy scanning).
- **`observation`** — what the browser captured: `screenshot`
  (relative path), `visible_text_preview`, `headings`, `interactive_elements`
  (count) + `_sample`, `a11y_audit`.
- **`action`** — the chosen action `{type, ref, text, value}`; type ∈
  click/type/scroll/find/select/back/wait/none.
- **`result`** — what happened after executing it: `action_outcome`
  (the key UX signal — e.g. `url_navigation`, `hash_change`, `new_tab`,
  `menu_opened`, `same_page_state_change`, `scroll`, `no_visible_change`),
  `navigation`, `url_change_type`, `state_change`, `console_errors`, `final_url`.
- **`stop_signal`** — `{enough_evidence, should_stop_if_exploratory}`.

Each step also carries **`model_decision`** — the full provenance behind the
choice (the persona sent to the model, the exact prompt, the parsed decision).
You rarely need it: the fields that matter for reading a run — `thinking`,
`frustration`, `action`, and `action_outcome` — are already surfaced in the
layers above. Reach into `model_decision` only to audit exactly why one step
went the way it did.

Screenshots are stored by reference (a path under the run's `screenshots/`),
never inlined in the JSONL.

## Reading outcomes (not the same as runtime errors)

- `done` — task complete or success criteria detected.
- `gave_up` — gave up or repeated the same action too many times.
- `max_steps` — step budget exhausted.
- `error` — execution error.
- `interrupted` — stale/incomplete run recovered by the store.

For exploratory studies, `max_steps`/`gave_up` can still hold useful evidence —
read the trace before concluding the site failed.

`scores.json` also carries `stop_quality`: `done`,
`enough_evidence_but_continued`, `looping`, `blocked_by_auth`,
`blocked_by_no_visible_advance`, `unresolved`, `error`.

## Debugging checklist

1. Check the command exit code.
2. Inspect `scores.json` outcomes.
3. Open `log.html`, look at the last step of failed runs.
4. Separate execution errors from UX friction.
5. Check for a missing ref or a static heading the model tried to click.
6. Check repeated clicks that didn't navigate (`action_outcome: no_visible_change`).
7. Check whether an external site opened and the task should have ended.
8. Narrow the task or lower `max_steps` if the agent is wandering.
