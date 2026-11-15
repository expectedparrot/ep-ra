# Evidence-backed workflow gates

## Contents

- Lifecycle
- Verification types
- Gate quality
- Invalidating stale evidence

## Lifecycle

After explicit approval of `plan.md` and its definition of done:

1. For a scaffolded survey, run `make -C <absolute-study-root> workflow-setup
   APPROVAL_EVIDENCE="<concise approval evidence>"`; the scaffold owns the
   verifier commands and attests `plan-approved`. Do not reconstruct gate JSON.
2. Otherwise initialize, bulk-set, and freeze in one call:
   `ep workflow setup --name <name> --root <root> --json ... --evidence <approved-plan-evidence>`.
3. Attest `plan-approved` with `--by user` and conversation evidence when the
   setup is not scaffold-owned.
4. At completion, run `ep workflow verify --root <root>` once to verify every
   consecutive objective gate; require `all_gates_passed: true`.

Before `workflow setup` freezes any command verifier, execute that exact command
once from the gate's declared working directory and require exit code zero.
Resolve environment variables before storing the verifier: prefer an absolute
artifact path or a study-root-relative path over shell variables. Never freeze
a guessed package subcommand. Use durable package artifacts for gates when the
package does not expose a documented validation command.

`gate set` requires a top-level specification object. Use
`--json '{"gates":[...]}'`. Do not pass a raw array with `--json '[...]'`; the
CLI rejects it with `WORKFLOW_SPEC_INVALID` even if the gate objects are valid.

If a command rejects valid-looking input, inspect its contract once:

```bash
ep workflow setup --help
ep workflow verify --help
```

The CLI emits JSON by default. Successful responses use the envelope
`{"status":"ok","data":{...},"warnings":[]}`. Workflow fields such as
`name`, `gates`, `current_gate`, and `all_gates_passed` are under `data`; they
are not top-level fields. `verify` and `status` do not accept a separate
`--json` flag in the pinned workflow CLI.

## Verification types

- `user-approval`: consequential user decisions; attest with `--by user`.
- `agent-attestation`: judgments that cannot be checked mechanically; record
  concrete evidence and attest with `--by agent`.
- `file-exists`: only when existence alone is sufficient; verify it.
- `artifact`: a file that must exist and meet `min_bytes`; verify it.
- `command`: substantive reproducible checks; verify it.

Use `artifact` for non-empty deliverables and `command` for substantive checks.
For package-owned analyses, prefer a documented package validation/readiness
command. If none exists, validate the package's canonical analysis artifact
directly with a bounded, read-only command; do not invent a `show`, `check`, or
`validate` subcommand.

Gate names must be kebab-case. Each gate has `name`, `description`, and nested
`verification`. `freeze` is a workflow command, not a gate subcommand.

Canonical sequence:

```bash
ep workflow setup --name color-survey --root sessions/color-survey \
  --json '{"gates":[...]}' --evidence "User approved plan.md"
ep workflow gate attest plan-approved --root sessions/color-survey --by user --evidence "Approved in conversation"
ep workflow verify --root sessions/color-survey
```

## Gate quality

Gates are compact memory checkpoints, not a task list. Default to three:
`plan-approved`, valid results/analysis, and a validated final deliverable. Use
two when there is no distinct deliverable and four only when the request has
genuinely independent deliverables. Fold post-run review, plotting, compilation,
and visual inspection into those checkpoints instead of creating a gate for
each phase. Validate substantive artifacts with a command that runs their real
build and validators. `test -s` may be one check, but it is not sufficient by
itself for a substantive report.

For a survey run, the results gate should execute a saved validation script
that checks the exact planned row count, required answer fields, non-null
coverage, and any uniqueness requirements. Avoid line-count approximations.

For a report with plots, use an automated command gate that includes the
applicable checks:

```bash
make report && ep report check --root . && python analysis/check_plots.py --study-root .
```

Automated checks do not establish visual correctness. Inspect every plot and
representative pages from each requested PDF as part of report production, but
do not add a separate gate solely for that inspection. If rendering or
inspection tooling fails, report the limitation; successful compilation and a
non-empty PDF are not substitutes for inspection.

Keep evidence short: an approval quote, artifact path, or verifier command is
enough. Use the lifecycle batch commands unless debugging a failed gate or
invalidating stale evidence. Do not narrate each workflow transition to the
user.

## Invalidating stale evidence

If an upstream artifact changes, clear its gate with a concrete reason before
continuing so downstream passed evidence is invalidated.

If a frozen verifier is mechanically broken, repair only the unpassed verifier
definition while preserving gate names, order, and descriptions:

```bash
ep workflow repair --root <root> --json '{"gates":[...]}' \
  --reason "Verifier referenced an unavailable checkout path"
```

The repair is audit-logged. Do not use it to weaken or remove approved gates.
