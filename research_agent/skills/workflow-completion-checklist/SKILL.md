---
name: workflow-completion-checklist
description: >
  Final evidence audit for a study or durable research deliverable. Use when
  preparing to verify or declare completion, not during orientation,
  planning, scaffolding, or ordinary implementation.
tags: [workflow, quality-check]
---

# Completion audit

Load this skill at final verification. Do not load it at study start. The
workflow gates carry execution state while the study is in progress.

1. Select only the checklist matching the deliverable:
   - EDSL survey or experiment: read
     [edsl-study.md](references/edsl-study.md).
   - Agent-list-only or Concordia work: read the corresponding section of
     [all-checklists.md](references/all-checklists.md).
2. Create or update `checklist.md` from observed evidence. Do not copy
   irrelevant sections or aspirational boxes into the study.
3. Verify the workflow once with `ep workflow verify --root <study-root>`.
   Require `all_gates_passed: true`.
4. Run `ep report check --root <study-root>` when a report exists.
5. Created EDSL objects remain local unless the user explicitly requested publishing.
6. Require only requested report formats. HTML is the default human-readable
   deliverable; do not generate or inspect a PDF unless it was requested or is
   required by the task.

Every checked item needs concrete evidence such as a path, row count, command
result, timestamp, or user approval. Never rerun paid inference merely to
repair optional inspection or reporting.
