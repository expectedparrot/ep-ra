---
name: edsl-surveys-cost
description: >
  Reference for EDSL survey costs and the low-balance email. Use when a user asks about cost
  before running a job, or about checking or changing their low-balance email threshold.
  For LLM jobs: cost estimation, reasoning-model uncertainty, token overrides, pilot calibration, and skip-logic weights.
  For human surveys: free with .humanize() to your own participants, paid when recruiting
  through Prolific.
tags: [edsl, reference, workflow]
---

# EDSL survey cost

Estimate before paid inference; do not run the job. Cost the effective saved
Jobs artifact through its scaffold estimate target, or directly when no target
owns that task:

```bash
ep jobs cost jobs.ep
```

If execution replaces the embedded model with `--model`, cost the same override
with `ep jobs cost jobs.ep --model <confirmed-model>`. For a ModelList override,
build/cost a Jobs artifact containing that list; the cost command has no
`--model_list` option.

Report total USD, credits, input/output tokens, assumptions, and warnings.
Prices come from the live Expected Parrot model catalog. Make clear that an
estimate is not a billing receipt. Read `estimate_kind`, `lower_bound_usd`,
`expected_usd`, `upper_bound_usd`, and `assumptions.reasoning_tokens` when present.
For `estimate_kind="lower_bound"`, present the amount as a minimum, not an exact
budget or an upper limit. A null expected/upper value means unknown, not zero.
Preserve supplied ranges and assumptions; do not invent a multiplier or treat
approval of an estimate as unlimited spending authority.

For a straightforward fixed survey, use the default estimate. Ask only for
inputs that materially affect the calculation: survey/questions, model(s),
number of agents, scenarios, files, and whether branching can skip substantial
work.

Read [estimation-details.md](references/estimation-details.md) when explaining
question-type formulas, files, warnings, or unsupported image/audio/video cost.

Read [calibration-and-branching.md](references/calibration-and-branching.md)
only when pilot results, token overrides, skip logic, or `Survey.loop_over`
make the default estimate materially inaccurate.

## Human surveys

Hosting a `.humanize()` survey for the user's own participants is free.
Prolific recruitment adds participant payments and platform fees; load
`skill:edsl-prolific-study` for that calculation. Invisible server-side
thinking or image-generation questions still incur owner-paid inference per
response; disclose that before deployment.

## Low balance email

Expected Parrot emails the user when their balance drops below a threshold they
choose (on by default, at $10). If they ask about that email, or want a warning
before a large run uses up their credits, check the setting with:

```bash
ep balance alert
```

Change it only when the user asks. `--threshold` takes US dollars, from 1 to
10,000 with at most two decimal places:

```bash
ep balance alert --threshold 25
ep balance alert --off
ep balance alert --on
```

Each command returns the setting, including `enabled`, `threshold_usd`, and
`threshold_credits`. The email goes out when a charge takes the balance below
the threshold, at most once a day; changing the threshold while the balance is
already below it does not send one. The user can also change it under
Notifications in their account settings.
