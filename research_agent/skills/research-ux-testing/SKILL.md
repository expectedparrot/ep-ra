---
name: research-ux-testing
description: >
  Own all synthetic UX research through uxtest: behavioral browser journeys,
  first impressions, content comprehension, conversion and findability, static
  screenshot review, visual attention and saliency, accessibility-oriented
  review, Figma studies, and comparisons across pages, variants, devices, or
  releases. Use for any request to review, compare, or usability-test a website,
  page, interface, prototype, or web screenshot.
tags: [study-type, external-tool, data-collection, simulation, qualitative]
---

# UX research with uxtest

`uxtest` is the single state owner for website and interface UX research. It
uses Playwright for real browser interaction and EDSL remote inference for
synthetic-persona decisions, and stores raw traces, screenshots, findings,
scores, and derived reports under `uxtest_store/`.

Do not recreate legacy screenshot-capture, grid-overlay, design-comparison, or
eye-tracking pipelines in this repository. Use the corresponding packaged
uxtest workflow.

## Choose the smallest workflow

| Research need | Packaged workflow |
|---|---|
| First impression, first click, hesitation | `task-discovery` |
| Offer, audience, claims, labels, jargon | `content-comprehension` |
| Demo, signup, checkout, pricing, contact | `conversion-path-testing` |
| Navigation and expected content location | `information-architecture` |
| Feature, API, integration, or workflow proof | `feature-findability` |
| Enterprise buyer/evaluator evidence | `enterprise-buying-research` |
| Page, competitor, variant, device, before/after | `competitive-benchmark-studies` |
| First-run activation | `onboarding-activation` |
| Authenticated role-specific task | `post-login-workflow-testing` |
| Inclusive UX risks | `accessibility-inclusive-ux` |
| Repeated release checks | `longitudinal-regression` |
| Static screenshot defects or visual critique | `image-review` |
| Attention visualization | packaged saliency workflow |
| Figma design or prototype | packaged Figma workflow |

Slide decks remain owned by `skill:research-slide-feedback`; generic charts
and completed reports remain owned by their report-review skills.

## 1. Discover current commands

The installed package documentation is authoritative for CLI syntax and schema.
Inspect it rather than guessing commands or configuration keys:

```bash
uxtest doctor
uxtest --version
uxtest docs list
uxtest docs show root
uxtest docs show <study-type>
uxtest examples list
```

Read the selected guide in full. Do not truncate it: fixtures, success criteria,
and important caveats often appear late in the document. Commands return a
versioned JSON envelope; check `ok`, `error`, `artifacts`, and `data`.

For a bundled example, the bounded happy path is exactly:

1. `uxtest doctor`
2. `uxtest docs show <study-type>`
3. `uxtest examples copy <study-root>/uxtest_jobs --name <example-name>`
4. initialize the store, register/validate the copied fixture, and run it

Do not inspect `site-packages`, import private package helpers, grep package
source, or enumerate CLI help when these documented commands succeed. Do not use
`examples path`; copy the example into the durable study instead.

If `uxtest doctor` reports missing Chromium, stop and report the reproducibility
problem. Do not mutate the locked launcher environment during a study.

## 2. Plan the study

Before spending, define:

- the UX question and smallest matching workflow;
- target URL, file, screenshot, or Figma artifact;
- personas that differ on dimensions relevant to the question;
- device/variant matrix;
- observable success criteria;
- maximum steps and run count;
- selected current image/browser-capable model;
- expected inference cost and approval evidence.

Before any `ep models` command, load `skill:workflow-model-selection` and use
its single bounded query exactly once. Do not probe `ep models` beforehand,
run `--help`, or repeat the catalog query after loading that skill.

Do not claim statistical population validity from small synthetic samples. Call
them synthetic visitors or persona runs.

## 3. Create the study

Use `uxtest study new` for a one-off study. Use a registered fixture when the
study should be repeatable, compared across variants, or rerun as a regression.
For fixtures, initialize the store first and adapt a packaged example:

```bash
uxtest init
uxtest examples list
uxtest examples copy ./uxtest-examples --name <example-name>
uxtest fixture register ./uxtest-examples/<fixture> --name <study-name>
uxtest fixture validate <study-name>
```

For a non-scaffolded uxtest study, initialize the three compact `ep workflow`
gates in one call after plan approval. Include `--evidence` in that first and
only `ep workflow setup` call; do not probe the command by first running an
incomplete setup.

Keep reusable fixture source in `uxtest_jobs/` at the study root. Use only fields
documented by the selected packaged guide. Put the decision model in the fixture
override instead of global mutable configuration.

For local HTML, use uxtest's documented `server` block and deterministic
`setup_steps`. Never edit the page being evaluated merely to make the test pass;
that changes the object of study.

## 4. Smoke-test, estimate, and run

Start with one persona, one device, and a small `max_steps`. Inspect the trace
before expanding. Each behavioral step can spend inference credits.

Use the exact run command returned or documented by uxtest. Typical forms are:

```bash
uxtest study run <study-id> --driver edsl --max-steps 8 --max-concurrent-runs 2
uxtest fixture run <fixture-id>
uxtest ci uxtest_jobs/<study>.yaml
```

Keep concurrency low against public sites. Parallelism reduces wall time but
does not reduce inference count or cost.

For a captured screenshot, use `uxtest image-review captures` and
`uxtest image-review run --capture <capture-hash>`. For manual inference control,
use the `next_command` returned by `image-review prepare`, then ingest results.

## 5. Inspect evidence before interpreting

Raw run traces are the source of truth; reports are derived and regenerable.
Inspect:

```bash
uxtest status
uxtest study list
uxtest show <study-id> --json
uxtest trace <study-id> --edsl-jobs
uxtest analyze <study-id> --include-interrupted
uxtest journey <study-id>
uxtest uxr <study-id>
```

Start with `analysis/log.html` for step-level prompts, screenshots, decisions,
and browser outcomes. Cross-check `findings.json`, `scores.json`, and the raw
`trace.jsonl`. Distinguish genuine UX friction from runtime failures, and inspect
`action_outcome` and `stop_quality` before interpreting a stalled run.

For static visual review, comparisons, Figma, or saliency, follow the exact
packaged guide and retain its provenance-bearing artifacts in the same store.

## 6. Produce the final report

Use `uxtest report guide <study-id>` and `uxtest report template <study-id>`, then
load `skill:report-authoring`. The uxtest dashboards and logs are evidence, not
automatically the final stakeholder deliverable.

Write `writeup/report.md` first under the normal study directory. Compile from
inside `writeup/` so relative screenshot paths resolve, producing
`writeup/report.html`, then run `ep report check --root <study-root>`. Never
author only the compiled HTML or backfill a placeholder Markdown file merely to
satisfy validation. Embed specific trace screenshots and link claims to run/step
evidence. State sample size, model, devices, failures, unresolved runs, and
limitations. Present the compiled local HTML with `ep present`.

## Golden rules

- Use uxtest for every website/interface UX modality; do not revive bespoke
  agent-side capture, comparison, grid, or heatmap scripts.
- Treat `trace.jsonl` and captured screenshots as source evidence.
- Discover CLI syntax from installed docs and returned `next_command` values.
- Never inspect installed uxtest source or private Python helpers when the
  documented agent commands succeed.
- Test the artifact the user supplied; use setup state rather than editing it.
- Smoke-test before scaling persona/device matrices.
- Preserve `uxtest_store/`; reports must be regenerable from raw evidence.
- Never expose credentials in fixtures or traces; use documented auth-state and
  redaction facilities for authenticated studies.

## References

Use these for ep-agent integration details after reading the selected package
guide:

- `references/environment.md` — environment and store placement
- `references/fixtures.md` — reusable fixtures, personas, costs, regression
- `references/evidence.md` — trace and report evidence hierarchy
- `references/synthesis-and-reporting.md` — synthesis and follow-up workflows
