---
name: research-premortem
description: Facilitates a structured prospective-hindsight analysis for a concrete plan, launch, decision, or strategy using the installed Premortem CLI and EDSL jobs. Use when the user wants stakeholder-specific failure modes, a causal graph, mitigations, a research agenda, and a decision-oriented report before committing.
tags: [study-type, qualitative, simulation]
---

# Premortem

Use the locked `premortem` command as the workflow owner. Do not recreate its
state machine, schemas, prompts, or report bundle in ad hoc Python.

## Runtime contract

The ep-agent environment installs Premortem from a pinned GitHub revision. Do
not run `pip install`, `uv pip install`, or `uv tool install` during a study.
Verify the locked tools once:

```bash
premortem --help
ep check
```

If either command is missing, report an environment defect rather than mutating
the environment. Read [premortem-cli-quickref.md](references/premortem-cli-quickref.md)
only if a surfaced `next_action` needs option details. Read
[quality-standards.md](references/quality-standards.md) when reviewing personas,
failure reasons, the causal graph, mitigations, or the audience-facing report.

## Fit

Use Premortem when there is a concrete initiative to imagine failing and the
user wants causes or mitigations before commitment. Route external strategic
futures to `skill:research-scenario-planning`, option comparison to
`skill:research-decision-support`, and ordinary opinion measurement to
`skill:research-survey`.

## Start and follow state

After `skill:workflow-session-start`, create the standard study root through
`skill:workflow-file-layout`. Initialize Premortem inside that root, then run:

```bash
premortem agent-start
```

Treat its JSON envelope as authoritative. Follow `next_actions` until the CLI
requires user approval or the workflow completes. Use one command at a time
when its output determines the next action; batch only independent read-only
commands.

Every command returns a versioned JSON envelope with `ok`, `data`, `warnings`,
and `next_actions`. Do not guess the next command, inspect package internals, or
parse human-formatted output. Use `--human` only for material explicitly being
presented to the user.

## Method guardrails

- State the imagined failure as a concrete future fact, not a possibility.
- Describe the failed outcome without prescribing its causes.
- Use distinct stakeholder roles with different incentives and information.
- Review personas with the user before eliciting failure reasons.
- Collect and review reasons before building the causal graph or mitigations.
- Consolidate generic or duplicate reasons; target a readable graph of roughly
  eight causal nodes.
- Make mitigations concrete: owner, timing, trigger, and affected causal node.
- Preserve CLI-managed `.premortem/` state as the source of truth.

## Generated inference

Premortem generates portable, model-free EDSL Jobs packages. Confirm a current
model through `skill:workflow-model-selection`, estimate the generated job with
`ep jobs cost`, obtain spend approval, and run it explicitly:

```bash
premortem job generate <phase> --output <phase>.jobs.ep
ep jobs cost <phase>.jobs.ep
ep run <phase>.jobs.ep --model <confirmed-model> --output <phase>-results.ep
premortem ingest <phase> --from <phase>-results.ep
premortem workflow
```

Never rerun paid inference to repair ingestion, validation, graph, or report
errors. Preserve Results artifacts and fix the downstream stage.

## Validation and reporting

Use `premortem status` when resuming and after ingestion. Run:

```bash
premortem workflow validate
premortem report context
```

The validation output must be clean before final reporting. The report-context
bundle is the canonical evidence and writing brief, not the final deliverable.
Immediately before the first write to `writeup/report.md`, load
`skill:report-authoring`; it owns Expected Parrot styling, transparency, review,
compilation, and checks. Author the report from the context bundle and the report
requirements in [quality-standards.md](references/quality-standards.md).

`premortem report html` is a package-owned convenience view for inspecting the
structured state. Never use it as `writeup/report.html`, present it as the final
report, or treat it as a substitute for narrative authoring. The canonical
audience-facing source is `writeup/report.md`; compile and present its branded
HTML through `skill:report-authoring`. Keep all outputs local unless the user
explicitly requests publication.

## Completion

Completion requires approved personas, ingested reasons, a validated causal
graph, scored priority nodes, concrete mitigations, a focused research agenda,
saved inference provenance and costs, an agent-authored `writeup/report.md`, and
a checked local HTML report whose claims trace to the report-context bundle. Do
not declare completion if only the Premortem convenience HTML exists.
