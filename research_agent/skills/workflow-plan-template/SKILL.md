---
name: workflow-plan-template
description: >
  Creates or reviews the user-approval plan for a research study before
  method-specific scaffolding or execution. Use when writing plan.md,
  presenting a proposed design, or identifying concrete design trade-offs
  for user approval.
tags: [workflow]
---

# Write the study plan

Write for the user in research language. Show actual questions, personas, and
deliverables rather than EDSL abstractions. A clearly specified request does
not need additional discovery questions.

If the study will run model inference, load `skill:workflow-model-selection`
before drafting this plan and make its one bounded `ep models` query. Section 6
must use the exact identifier returned by the current catalog. Do not name,
recommend, or scaffold a model recalled from memory. If model discovery has not
happened yet, stop and perform it before writing `plan.md`.

Use these seven sections:

1. **What this study will produce** — what the user will know or receive.
2. **How it works** — the study-specific comparison or inferential logic.
3. **The agents** — segments, counts, defining traits, example instructions,
   and why those dimensions and counts matter. Delegate sizing logic to the
   owner study skill.
4. **The survey or task** — verbatim questions, types, options, order, memory,
   and actual stimuli where applicable.
5. **Deliverables and preview** — requested output formats, report sections,
   tables/plots, and a small clearly illustrative preview using this study's
   real labels. Default to HTML; include PDF only when requested or required.
   Record `report_detail: concise` or `report_detail: full`. If the user has not
   expressed a preference, make this one of the Section 7 choices: concise
   (decision-focused findings and essential methods) or full (item-level
   evidence, diagnostics, and appendices). Default to concise only when the
   user delegates the choice.
6. **Model and cost** — confirmed model, task-specific rationale, and estimated
   execution cost or the step that will calculate it.
7. **Decisions for you** — only genuine close calls whose answers would change
   the design. Make each trade-off concrete; always include “Looks good,
   proceed.”

The neutral standard study scaffold must already exist. Write `plan.md` at the
allocated `<study>/plan.md` path—never at the workspace or topic root—present
its absolute path with a standalone `ep present <absolute-study-root>/plan.md`.
Leave stdout and stderr intact: no pipes, output capture, redirection, or
`2>/dev/null`; truncating the response can break the UI's file presentation.
If an earlier attempt was truncated, rerun the bare command before requesting
review. Then use one `AskUserQuestion` whose
options cover Section 7, including report detail when still unknown. Plan approval
authorizes method-specific scaffolding and execution, not paid inference.
Estimate each run and request separate approval before inference.

When requesting plan approval, briefly summarize the deliverable, where execution
will stop, and any work left to the user. Surface consequential scope limits
directly in the approval question; do not assume the user read the full plan.

Read only the relevant reference:

- [deliverable-previews.md](references/deliverable-previews.md) for a complex
  or unfamiliar output preview.
- [decision-points.md](references/decision-points.md) when meaningful close
  calls are hard to identify.
- [simulation-plans.md](references/simulation-plans.md) for Concordia or other
  stateful simulations.
- [pilot-decisions.md](references/pilot-decisions.md) when deciding whether a
  separate pilot is warranted.

For a returning user using shorthand, write and present the full plan file.
Keep the accompanying chat summary to the outcome, model/cost, and decisions
unless they request more detail; do not shorten the `ep present` output.
