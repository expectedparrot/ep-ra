# Controlled model-response benchmarks

Use this mode only when the task is to test model choices or reaction-history
effects, rather than complete an allocation for actual participants.

`ariel benchmark build` creates a rent-choice benchmark over authored numerical
cases, A/B orderings, and prompt variants. Inspect `--help`, select current models
through `skill:workflow-model-selection`, and set repetitions explicitly. Use
`ariel benchmark next <plan.json>` for the generated cost, execution, and import
commands. Review the actual trial/answer counts and scope before paid execution.

Keep objective correctness separate from subjective fairness ratings. Preserve
trial identities, instrument and parameter bindings, original Results, and the
full planned denominator. Authored fixtures do not measure model quality, and
a diagnostic set is not representative-population evidence.

`benchmark ingest --allow-partial-answers` can retain missing answers only when
every planned trial and required provenance is present. Missing objective answers
count as not correct in the full denominator; missing fairness answers remain
missing. This option is specific to benchmark ingestion and does not relax
complete-round participant field ingestion. Preserve error reports; do not rerun
failed trials simply to improve the measured score.

For the optional history comparison, `benchmark history` builds matched
follow-ups from prior Results, including mistakes. The history arm sees its own
actual answers and comments; the control does not. Neither gets correctness
labels or answer keys. Record corrections, regressions, and persistent errors.
Self-reported changes do not rewrite prior preferences or an allocation.

[Benchmark protocol](https://github.com/expectedparrot/ariel/blob/449dcaf9c7fff888f1dcb27e10b61551ec01dcf3/examples/benchmark/README.md)
