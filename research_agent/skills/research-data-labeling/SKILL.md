---
name: research-data-labeling
description: >
  Build auditable, reproducible LLM-assisted labels for rows of a tabular
  dataset using the Labeling CLI and EDSL. Use for classification, tagging,
  extraction, gold-label comparison, multi-rater agreement, aggregation, or
  labeled-data export. Do not use for discovering an inductive qualitative
  codebook from raw transcripts; route that work to skill:research-qualitative-data-analysis.
tags: [methods, data-collection, quantitative]
---

# Auditable data labeling with Labeling

Labeling is the single state owner for row-level labeling studies. It owns
`labeling.yaml`, the append-only `.labeling/` audit store, samples, generated
Jobs, recorded runs, label sources, gold data, metrics, aggregates, exports, and
bounded report inputs. `ep` exclusively executes portable `Jobs.ep` files.
Do not recreate these capabilities with ad hoc EDSL or pandas scripts, inspect
installed package source, or edit `.labeling/` by hand.

## Orient from the package

The locked runtime already contains Labeling. Do not install it. Start with:

```bash
labeling docs show getting-started
```

Treat bundled docs as authoritative. Run `labeling next` after each material
phase and execute its structured `cwd` + `argv` actions. Use a subcommand's
`--help` only when the returned action leaves an interface unresolved. Never
inspect `.labeling/` manifests or installed source to recover state.

## Decide whether Labeling fits

Use it when there is a CSV or a clear row-per-item dataset and each row needs
one or more explicit structured judgments. Establish:

- input CSV and stable unique ID column;
- prompt-visible columns and columns hidden to prevent target leakage;
- label questions, types, options, ambiguity policy, and boundary examples;
- model/rater configuration and the cost/latency/quality priority;
- human or gold labels, if available, and the desired quality metric;
- aggregation and final export requirements.

If categories are still unknown, first use
`skill:research-qualitative-data-analysis` with Bewley on a small sample to
develop the codebook, then encode the stable rubric in Labeling.

## Canonical workflow

1. Create the normal study scaffold and place source data under
   `<study>/data/uploaded/` without modifying the raw file.
2. Run every project-scoped Labeling command from the study root. Labeling has
   no global `--project-root` option. Initialize `.` there so relative dataset
   paths resolve inside the study, then edit `labeling.yaml` deliberately:

   ```bash
   cd <absolute-study-root>
   labeling init . --csv data/uploaded/<dataset.csv> --id-column <id-column>
   labeling inspect
   labeling validate
   ```

3. Generate Jobs, create a small reproducible sample, and ask Labeling for its
   exact execution plan:

   ```bash
   labeling generate
   labeling sample --n <small-n> --strategy random --seed <integer-seed>
   labeling plan sample --latest
   ```

   Reproducibility comes from an explicit seed; `deterministic` is not a sample
   strategy.

4. Apply this indivisible protocol to the sample artifact:

   ```text
   labeling plan sample --latest
   → ep inspect <literal-sample-Jobs.ep>
   → ep jobs cost <same-literal-sample-Jobs.ep>
   → approval naming that artifact, rows, questions, model, and estimate
   → exact returned ep run command
   → labeling record run --kind sample --results <exact-results.ep>
   ```

   Never approve before the plan exists, change the Jobs path between cost and
   execution, or treat study-plan approval as spend approval.
5. Review representative labels, disagreements, ambiguous cases, and rubric
   failures with the user. If accepted, register that decision for safe reuse:

   ```bash
   labeling record run --kind sample --results <sample-results.ep>
   labeling preview latest --human
   labeling approve sample
   labeling next
   ```

6. Revise and resample instead if rejected. If accepted, repeat the **entire**
   paid protocol for the full phase—no earlier estimate or approval carries
   forward:

   ```text
   labeling plan full --reuse-approved-sample
   → ep inspect <literal-remaining-Jobs.ep>
   → ep jobs cost <same-literal-remaining-Jobs.ep>
   → fresh approval naming that artifact and estimate
   → exact returned ep run command
   → labeling record run --kind full --results <exact-results.ep>
   ```

7. `record run` returns a stable first-class label-source ID. Pass that ID
   directly to Labeling's `gold`, `metrics`, `aggregate`, and `export` commands.
   Never use `ep results`, write parsing code, export/re-import the run, or read
   `.labeling/` internals. Treat `ok: false` or zero matched metric rows as a
   blocker; inspect Labeling's source/question coverage diagnostics and recover
   through `labeling next`.
   Import separately supplied gold CSVs through the dedicated interface—not
   generic `labels import`—mapping source columns explicitly:

   ```bash
   labeling gold import <gold.csv> --id-column <id> \
     --label-columns <source-column>:<question-name> --name <gold-source-id>
   ```

8. Use `labeling export` for final labeled data. Then obtain bounded reporting
   inputs with:

   ```bash
   labeling report context --output analysis/labeling_report_context.json
   labeling report template --output analysis/labeling_report_template.md
   ```

   The research agent—not Labeling—owns `<study>/writeup/report.md`, the final
   branded `<study>/writeup/report.html`, reader framing, conclusions, and
   presentation. Never run a package command that claims either canonical path.
   Keep both handoff files outside `writeup/` so `ep report check` sees only the
   canonical report sources. If a package-only analytical HTML is explicitly useful, write it to the
   distinct default `writeup/labeling_package_report.html`.

## Required safeguards

- Preserve stable row IDs and raw source columns.
- Never expose target, gold, or leakage columns to the rater prompt.
- Never skip sample review or silently scale from sample to full inference.
- Never rerun approved sample rows in the full phase when reuse is available.
- Do not report accuracy without compatible gold labels; use agreement and
  disagreement diagnostics when gold is absent.
- Record every executed `Results.ep` in Labeling before export or reporting.
- Preserve `.labeling/` as the audit trail across revisions and reruns.
