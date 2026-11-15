---
name: report-authoring
description: Author or review written research reports and their plots. Use when producing a report, memo, HTML/PDF write-up, executive summary, or report visualization; owns audience/style, study transparency, and plotting standards through conditional references.
tags: [report, workflow, visualization]
---

# Report authoring

Own the report from brief through verified output. Do not load separate report
skills: the detailed guidance is colocated here and loaded only when relevant.
For an agent-authored report, `writeup/report.md` is always the canonical source;
never hand-write `writeup/report.html`. HTML is a compiled deliverable produced
only after the review decision. Package-owned report applications are the sole
exception and must follow their package skill instead of this authoring flow.

## Required pre-compilation decision

Immediately after the final write to `writeup/report.md` and inspection of its
figures, stop the compilation sequence. The next workflow action must be to load
`skill:report-quality-review` and resolve its `Katz review` decision card. Do not
run Pandoc, `ep report check`, `workflow-verify`, or presentation in the same
batch as the report write. Resume compilation only after the user chooses `Run
review` or `Skip review`.

## Core workflow

1. Honor the plan's `report_detail`. For `concise`, lead with decisions and
   essential evidence and keep item-level diagnostics out of the main body.
   For `full`, include item-level evidence, limitations, validation detail, and
   useful appendices. If no preference was recorded, resolve it before study
   execution as part of plan approval, not as a late report-writing question.
   Infer audience, purpose, format, and tone from the request and prior
   deliverables. Read [style-and-audience.md](references/style-and-audience.md)
   when those choices are unclear or the user requests a specific house style.
2. For an EDSL study, use `ep results review data/results.ep` as the default
   bounded diagnostic. Request larger or targeted extracts only when the review
   identifies a reason. Read [transparency.md](references/transparency.md) for
   external, client, academic, or reproducibility-focused reports.
3. For plots, use `analysis/plot_style.py`, installed by the study scaffold.
   For an older study where it is absent, copy `scripts/plot_style.py` using
   the exact `Base directory for this skill:` reported by the Skill tool. Read
   [plot-standards.md](references/plot-standards.md) only when
   creating or debugging non-trivial charts. Always inspect rendered figures.
4. Write the report once the evidence is assembled. Keep costs internal unless
   the user expects them in the deliverable. Never call Expected Parrot “Coop.”
   Use YAML `title:` metadata and begin body sections at H2 (`##`); never add a
   body H1 when YAML already supplies the title. Calibrate conclusions to the
   completed protocol. Do not say a study "replicates" a finding, rank
   models/groups, or headline effect ratios when required observations differ
   across comparison arms, validation failed, or material plan substitutions
   remain unresolved. Use "exploratory" or "partial demonstration" where
   appropriate, and separate observed behavior from mechanistic explanations
   inferred from a small set of responses.
5. For report tables, use the scaffolded structured CSV or repeated
   `ep results export --column ...`. Do not parse rendered review text or write
   extraction regex for fields already present in Results.
6. Apply the required pre-compilation decision above. If the user approves,
   fix supported issues in Markdown and source figures and preserve the
   normalized review artifact under `analysis/`. If they decline, proceed
   without a review artifact.
7. Determine the compilation route before the first validation call. For a scaffolded survey, finish with
   `make -C <absolute-study-root> workflow-verify`; it builds and checks the
   report before verifying all remaining objective gates. Do not separately run
   `report`, `report-check`, or `qa`. For other studies, use their report target
   when one exists. Without a Makefile/report target, require the packaged
   Expected Parrot assets at `writeup/report.css`; if absent, run the idempotent
   `ep study scaffold <absolute-study-root>` to install them. Then compile from
   `writeup/` with `pandoc report.md -o report.html --standalone
   --embed-resources --css=report.css`. Never compile report HTML with bare
   Pandoc or omit `--embed-resources`: local and published reports must retain
   the branding without an external stylesheet. Confirm `report.html` embeds
   the `--ep-green` CSS variable, then run `ep report check --root
   <study-root>` exactly once. Never run the checker to discover whether HTML
   exists. Use an `artifact` workflow gate for the compiled report.

## Efficiency contract

- Load at most the references needed for this report.
- Batch independent file writes in one tool turn when the tool supports it.
- Batch related read-only checks in one shell call and return concise output.
- Do not inspect the same results twice through overlapping commands.
- Prefer existing scripts and Make targets over generating large inline code.
- Use `make -C <absolute-study-root> present` after successful workflow verification;
  it supplies an absolute path and prevents duplicated relative prefixes.
- Use `skill:report-slides` instead when the requested deliverable is a deck.

Audience defaults are summarized in
[audience-profiles.md](references/audience-profiles.md); read it only when the
audience is known but its expected depth or structure is not.
