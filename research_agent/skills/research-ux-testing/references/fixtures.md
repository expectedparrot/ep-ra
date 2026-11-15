# Fixtures & personas

## Contents
- Full fixture shape
- Overrides — pin the model in the fixture
- Personas
- What a study costs
- Eval / regression

A fixture is a YAML file describing a study. Keep fixtures in `uxtest_jobs/` at
the study root (parallel to `edsl_jobs/`) and run one with
`uxtest ci uxtest_jobs/<study>.yaml` (always run `uxtest init` first). `ci` takes
an explicit path so any location works, but `uxtest_jobs/` keeps fixtures visible
and version-controlled alongside the rest of the study.

## Full fixture shape

```yaml
id: my-study                       # study id slug
name: My Study                     # human name
mode: live-site-conversion         # or live-site
comparison_title: My Study
comparison_output: my-study.html   # written to uxtest_store/comparisons/
study_title: My Study ({variant})  # {variant} is interpolated per variant
url_template: https://example.com/ # target; supports {host}/{port}/{variant}
task: >
  What the persona is trying to do, in plain language.
success_criteria: >
  What counts as reaching the goal.
personas:                          # names resolved against uxtest_store/personas/
  - first-time-visitor
  - regular-borrower
runs_per_persona: 1
driver: edsl                       # edsl (remote model) | heuristic | scripted
max_steps: 8                       # per-run ceiling; also the per-run job ceiling
max_concurrent_runs: 1             # parallel runs WITHIN a variant (see below)
keep_runs: 8                       # retained runs per study
analysis_driver: local            # local = deterministic scoring, no extra jobs
eval_policy: report_only           # report_only | threshold
overrides:                         # per-study config overrides (beat config.yaml defaults)
  model: <model>                    # pin the decision model HERE, not in config.yaml
                                    # confirm a current name; do not copy this literally
animation_delay: 250
animation_max_width: 640
variants:
  - name: desktop
    device: desktop                # desktop | iphone | pixel
  - name: mobile
    device: iphone
    overrides: {model: <model>}     # optional per-variant model override
    personas: [first-time-visitor] # optional per-variant persona override
checks:
  - id: reaches_goal
    type: trace_contains           # or final_url
    text_any: [reserve, study room, booking]
    description: What this check verifies.
```

## Overrides — pin the model in the fixture

Set the decision model in the fixture, not by editing `uxtest_store/config.yaml`.
Precedence (low → high): `config.yaml` defaults → fixture `overrides:` →
per-variant `overrides:`. Always include at least `overrides: {model: <id>}` so
the study pins its model explicitly.

## Personas

Custom personas are YAML in `uxtest_store/personas/`, referenced **by name** from the
fixture. A fixture name that is neither an existing file nor a built-in errors
out ("Persona X does not exist"). Built-ins auto-provision: `seniors`,
`low-confidence`, `mobile-first`, `price-sensitive`.

Persona schema:
```yaml
schema_version: 1
name: first-time-visitor
description: New patron who has never used the library website before
attributes:                        # -> becomes the EDSL Agent's traits
  role: prospective library visitor
  primary_goal: find hours and how to reserve a study room
  tech_literacy: medium
  reading_style: skims
  patience: medium
  device_familiarity: desktop
accessibility: {}                  # e.g. {prefers_large_targets: true}
goals_bias: >                      # -> becomes the EDSL Agent's instruction
  What this persona wants and how they read a page.
frustration:                       # used by local scoring, not sent to the model
  threshold: 6
  per_step_decay: 1
```
At runtime uxtest builds `Agent(traits=attributes, name=name,
instruction=goals_bias)`. Design personas that differ on the dimension under
test. `frustration` and `accessibility` are the only fields not carried onto the
EDSL Agent.

### AgentList interop

Because personas are just serialized EDSL Agents, an `AgentList` round-trips:
export each Agent to a persona YAML (attributes←traits, goals_bias←instruction),
or build an `AgentList` from completed runs with `uxtest agents export`. Keep the
AgentList as source of truth in your
own tree and regenerate `uxtest_store/personas/*.yaml` from it if you prefer an
EDSL-native authoring flow.

## What a study costs

Every browser **step** is decided by one remote EDSL inference on Expected Parrot
and billed to Expected Parrot credits (the browser runs in the sandbox; the
per-step decisions are remote). One "remote job" = one browser-step decision. For
a fixture with `P` personas, `V` variants, `R` runs/persona, and `max_steps` `S`:

- **Ceiling:** `P × V × R × S` jobs (every run burns all steps).
- **Realistic:** runs that finish early use fewer steps (reserving a study room
  might take ~3 steps, not 8), so expect well below the ceiling.
- `analysis_driver: local` adds **zero** remote jobs (scoring is local).

To spend less, cut scope: fewer personas/variants, lower `max_steps`, or run one
study at a time. **Always smoke-test with 1 persona / 1 device first.**
(`max_concurrent_runs` changes wall-clock only, not job count or cost.)

## Eval / regression

```yaml
expected_flaws: expected_flaws.yaml
eval_policy: threshold
minimum_recovered_expected: 1
```
Run `uxtest eval <study-id> --expect <flaws>.yaml --variant <v> --policy threshold`.
Use `report_only` for exploratory studies (evidence over pass/fail).
