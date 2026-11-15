# EDSL study completion audit

Use only applicable items and record evidence directly in `checklist.md`.

## Execution

- The approved `plan.md` matches what ran.
- Saved EDSL objects and `data/results.ep` are non-empty.
- The actual row count equals the planned row count.
- Required answer fields exist and are non-null.
- `ep results review data/results.ep` was used for one bounded review.
- Actual cost was recorded.
- Existing results are protected from accidental reruns.

## Analysis and report

- Every reported number, table, and plot traces to saved results or analysis
  outputs.
- Analysis scripts live under `analysis/` and run through the Makefile.
- The Methods section identifies the agents, survey, model, and memory choice.
- Limitations clearly say this is an AI-persona simulation, not a human sample.
- `ep report check --root <study-root>` passes.
- Each user-requested output format exists and is non-empty. HTML is sufficient
  unless another format was requested.
- Created EDSL objects remain local unless publication was explicitly requested.

## Handoff

- `README.md` records reproducible commands and actual execution facts.
- `ep workflow verify --root <study-root>` reports
  `all_gates_passed: true`.
