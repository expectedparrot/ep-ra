# Execution modes and recovery

Read this for partial results, a supplied run manifest, remote failures, or
requested job alerts. Ordinary studies continue through their scaffold phase
commands. For user-owned model endpoints, follow
[local inference](../../workflow-model-selection/references/local-inference.md).

## Remote failures and partial results

Inspect the CLI JSON status, warnings, authoritative job status and successful/
failed interview counts. Remote `failed`, `cancelled`, and `partial_failed`
outcomes fail the normal `ep run` success path. `--allow-partial` permits usable
partially failed results only when at least one interview succeeded; it does
not turn a wholly failed job into success.

If incomplete data is acceptable under the approved design, select
`--allow-partial` for that run and use a clearly named Results artifact. Disclose
the missing coverage in review and reporting; never attest a completeness gate
solely because a file exists or the process exited zero. Inspect local runs too:
they can save successful rows with `run_status="partial"` and a `PARTIAL_RESULTS`
warning. Unknown remote status can leave a recovery artifact; verify status
before treating it as completed data.

After a run fails, inspect the existing job before deciding on new inference:

```bash
ep jobs status <job_uuid>
ep jobs errors <job_uuid> --output analysis/job-errors.md
ep jobs errors <job_uuid> --format json --output analysis/job-task-history.json
```

The JSON form contains task histories, including prompts, raw responses and
tracebacks. Keep it with the study's diagnostic artifacts. A request to inspect
failure evidence does not authorize resubmission. Adding `--allow-partial` to a
new `ep run` is still a new run, not a download of the old job. Use the existing
job's result-retrieval command when recovering saved successes. Obtain fresh
scoped costing/approval before a retry and preserve prior attempts.

## Supplied run manifests

Use the manifest helper when a package or approved workflow already supplies a
`runs` manifest; do not replace ordinary scaffold execution with a custom one.

```bash
ep run-manifest workflow/jobs/run-manifest.json --result-base <study-root>
```

Without `--execute`, this only checks saved result row counts against positive
`prediction_count` values (or `scenario_count * model_count`) and returns an
`INCOMPLETE_RUNS` error with details for incomplete entries. This count check
does not establish correct answers or matching provenance; retain post-run QA.
Each entry also supplies `job_path` and `result_path`. Relative result paths
use `--result-base`; relative job paths use the command's working directory.
Prefer absolute job paths when the manifest's location differs from that cwd.

After costing and approval for the exact incomplete jobs, `--execute --parallel 3`
can run them. Complete result packages are reused; partial packages are moved
to a preserved filename before the corresponding job is submitted again. This
is not a guarantee of running only the missing interviews or avoiding costs.
Existing preserved partial files cause an error rather than being overwritten.

## Status-filtered job alerts

EDSL's Python `alert_on_completion_config` supports, for example:

```python
alert_config = {
    "email": True,
    "filters": {"status": ["failed", "partial_failed"]},
}
```

Valid terminal statuses are `completed`, `failed`, `cancelled`, and
`partial_failed`; a string or nonempty list is accepted. Omitting the filter
matches every terminal status. These are inference-job alerts, distinct from
respondent invitation/reminder campaigns owned by
`skill:edsl-human-survey-notifications`. The current `ep run` CLI does not expose
this configuration. If it is required for a CLI-managed study, identify that
integration gap; do not invent a flag or bypass the scaffold with `job.run()`.
Configure email/webhook delivery only when the user requests it.

## Interactive Results inspection

For a requested interactive review, `ep open data/results.ep` provides a table
with dimension/column controls and a transcript view. Use it to explore saved
results; no inference is needed. For a deterministic named interview export,
keep using the helper in `skill:methods-ai-interview`. Visual inspection does
not replace the scaffold's bounded post-run review and reusable exports.

Sources: EDSL `docs/en/latest/remote_inference.mdx`, `AGENTS.md`,
`edsl/cli_commands/run_manifest.py`, `edsl/jobs/data_structures.py`.
