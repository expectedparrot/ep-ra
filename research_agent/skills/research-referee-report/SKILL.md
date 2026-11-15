---
name: research-referee-report
description: >
  Runs evidence-linked academic peer review and referee-report workflows with
  Katz. Use when reviewing a manuscript, working paper, preprint, study, or
  paper repository; finding methodological or presentation problems; ingesting
  existing referee comments; or assessing revisions against an earlier review.
tags: [study-type, academic, quality-check, external-tool]
---

# Katz manuscript review

Katz owns manuscript preparation, version anchoring, section maps, spotters,
EDSL Jobs, result auditing and ingestion, issue investigation, revision history,
and HTML reports. Use its JSON responses as the source of truth. Do not recreate
the ledger, prompts, spotters, or report explorer in local scripts.

## Start and scope

Run these read-only commands first:

```bash
katz version
katz capabilities
katz agent bootstrap
katz agent next
```

Confirm the manuscript and desired review depth before registration. Prefer an
existing Markdown manuscript. Katz can prepare PDF or LaTeX sources, but the
derived Markdown must be checked against the source for reading order, tables,
equations, figures, citations, and omissions before it becomes canonical.

For a source outside a Git repository, use the package-owned workspace command:

```bash
katz workspace new <workspace> --from <source> --model <confirmed-model>
```

For an existing repository, follow the exact action returned by `katz agent
next`. Katz requires committed canonical text because every finding is anchored
to a Git version. Never attach uncommitted manuscript bytes to the current HEAD.

Write and present `<study>/plan.md` when operating inside a research-agent study
scaffold. Plan approval authorizes preparation and review setup, not paid model
inference. For a standalone manuscript repository, the registered Katz state is
the durable review record.

## Execute the package workflow

After each material step, rerun:

```bash
katz agent next
```

Execute only the returned command after considering its `mutates_state`,
`requires_network`, `requires_user_approval`, blockers, and reason. Use `katz
guide` and `katz docs show <topic>` only when more package guidance is needed;
do not load the full command reference routinely.

The normal lifecycle is:

1. Initialize Katz and register committed canonical manuscript text.
2. Inspect the section map and correct preparation errors.
3. Enable recommended and paper-specific spotters.
4. Build and audit a small model-compatibility pilot.
5. Build the complete model-free Jobs package.
6. Investigate draft findings against manuscript and repository evidence.
7. Validate the ledger and generate the report.

Katz findings are candidates, not facts. A matching quotation proves location,
not correctness. Do not promote a draft finding without investigation. Missing
or failed checks are not evidence that the manuscript has no issue.

## Paid inference boundary

Load `skill:workflow-model-selection` before choosing a model. For every pilot,
full review, retry, or changed package/model:

```bash
ep inspect <jobs.ep>
ep jobs cost <jobs.ep> --model <confirmed-model>
```

Present the exact Jobs path, model, scenario/call count, estimated cost, and
time risk, then obtain explicit approval. Run only the approved package and keep
the Bash call in the foreground with a 600000 ms timeout:

```bash
ep run <jobs.ep> --model <confirmed-model> --output <results.ep>
```

Follow Katz's returned audit and ingestion commands exactly. Never rerun paid
inference to repair ingestion, ledger, investigation, or reporting problems.
Preserve Jobs, every Results/retry object, audit diagnostics, and run records.

## Investigate and deliver

Use `katz issue next` to obtain a complete investigation packet. Read enough of
the canonical manuscript and repository context to decide whether each finding
is confirmed, rejected, or uncertain. Merge genuine duplicates before final
synthesis; preserve issue IDs and evidence anchors.

Before delivery require:

```bash
katz validate
katz report generate --output writeup/artifacts/paper_explorer.html
```

The Katz HTML is the traceable issue explorer. For a research-agent study, write
the reader-facing referee report at `writeup/report.md` and compile it through
the standard report workflow. It should summarize the contribution, give an
overall assessment, synthesize major and minor concerns, pose open questions,
and note material strengths. Every substantive concern must trace to confirmed
issues or direct manuscript evidence. Distinguish confirmed, rejected,
uncertain, and incomplete checks, and keep the tone constructive.

Keep all artifacts local unless the user explicitly requests publication.
