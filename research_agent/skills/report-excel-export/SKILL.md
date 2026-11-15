---
name: report-excel-export
description: >
  Exports research data, tables, and charts to a polished Excel workbook using
  the herndon CLI. Use when the user wants an .xlsx file containing their study
  results, data tables, or visualizations, or wants to convert an existing
  report into a spreadsheet deliverable.
tags: [report, workflow, external-tool]
---

# Excel Export (herndon)

This skill covers the full workflow for producing `.xlsx` workbooks using
[herndon](https://github.com/expectedparrot/herndon), an agent-focused CLI
for deterministic, local-first Excel generation from structured JSON specs.
Read this skill whenever the user asks for an Excel file, spreadsheet export,
or wants data and charts delivered as `.xlsx`.

---

## Step 0: Verify herndon

The ep-agent runtime owns the Herndon installation. Do not install, upgrade,
clone, or inspect package source during a study. Verify the documented CLI is
available:

```bash
herndon --help
```

If this fails, report the environment problem rather than mutating the sandbox.

---

## Step 1: Gather the data to export

Before building anything, identify what goes into the workbook. Scan the
session directory for:

- **Data tables**: CSV files, EDSL results, DataFrames saved as JSON
- **Charts**: any visualizations the user has generated or requested
- **Summary statistics**: key metrics, aggregated results
- **Raw response data**: individual survey or simulation responses

Organize what you find into candidate sheets. A typical research export has:

| Sheet | Contents |
|---|---|
| Overview | Title, study description, key findings |
| Summary | Aggregated results table with totals/averages |
| Data | Full response data, one row per observation |
| Charts | Visualizations (bar, line, pie) alongside their source data |

Ask the user if this is unclear:

> "I found [describe data]. Here's how I'd organize the workbook — does this
> look right, or would you like a different structure?"

---

## Step 2: Confirm the workbook structure

Draft a sheet outline and confirm before generating:

> "Here's the Excel workbook I'm planning:
> 1. **Overview** — study title, description, key metrics
> 2. **Results** — summary table with [columns]
> 3. **Detail** — full response data ([N] rows)
> 4. **Charts** — [chart types] visualizing [metrics]
>
> Should I adjust anything before I build it?"

Keep each sheet focused on one concern. If data is large (100+ rows), put it
on its own sheet rather than mixing with charts.

---

## Step 3: Initialize the herndon project

Set up the project in a build directory:

```bash
mkdir -p .herndon_build && cd .herndon_build
herndon init .
herndon new workbook report_export
```

This creates `workbooks/report_export/workbook.json`. Set metadata:

```bash
herndon workbooks set-title workbooks/report_export/workbook.json "Study Results"
herndon workbooks set-output workbooks/report_export/workbook.json \
  .herndon/builds/report_export/report_export.xlsx
```

---

## Step 4: Build the sheets

Create sheets in reading order. For each sheet:

1. Create the sheet
2. Write data (ranges for blocks, cells for individual values)
3. Add tables for filterable data
4. Add charts where appropriate
5. Set column widths and freeze panes

### Create a sheet

```bash
herndon new sheet workbooks/report_export/workbook.json overview
```

### Write data

Use `set-range` for tabular blocks — this is the primary data-entry method:

```bash
herndon sheets set-range workbooks/report_export/workbook.json overview A2 \
  --data-json '[["Category","Count","Pct"],["Agree",145,0.58],["Disagree",105,0.42]]' \
  --row-styles '{"0":"header"}'
```

Use `set-cell` for titles, formulas, and standalone values:

```bash
herndon sheets set-cell workbooks/report_export/workbook.json overview A1 \
  --value "Study Results" --style title
herndon sheets set-cell workbooks/report_export/workbook.json overview B5 \
  --formula "=SUM(B2:B4)" --style currency_total
```

### Add a table

Tables give the user auto-filter and structured references in Excel:

```bash
herndon sheets add-table workbooks/report_export/workbook.json overview results_table \
  --ref A2:C4 \
  --name ResultsData
```

### Add charts

See `references/herndon-patterns.md` for full chart command examples. Quick
reference for the most common types:

**Bar/column chart:**

```bash
herndon sheets add-chart workbooks/report_export/workbook.json overview bar1 \
  --type bar --anchor E2 --title "Responses by Category" \
  --series-json '[{"label":"Count","values":"'\''Overview'\''!$B$3:$B$4","categories":"'\''Overview'\''!$A$3:$A$4","color":"#2563EB"}]'
```

**Pie chart:**

```bash
herndon sheets add-chart workbooks/report_export/workbook.json overview pie1 \
  --type pie --anchor E10 --title "Response Distribution" \
  --show-data-labels --show-percent-labels \
  --series-json '[{"label":"Count","values":"'\''Overview'\''!$B$3:$B$4","categories":"'\''Overview'\''!$A$3:$A$4","color":"#0F766E"}]'
```

**Line chart (for trends):**

```bash
herndon sheets add-chart workbooks/report_export/workbook.json trends line1 \
  --type line --anchor D2 --title "Score Over Time" \
  --y-axis-title "Score" --legend-position r \
  --series-json '[{"label":"Mean","values":"'\''Trends'\''!$B$2:$B$6","categories":"'\''Trends'\''!$A$2:$A$6","color":"#7C3AED"}]'
```

### Format the sheet

Set column widths for readability and freeze the header row:

```bash
herndon sheets freeze workbooks/report_export/workbook.json overview --rows 2 --cols 0
```

Column widths are set in the sheet JSON directly — edit the `column_widths`
object to set widths proportional to content.

---

## Step 5: Validate and render

Always validate before rendering:

```bash
herndon validate workbooks/report_export/workbook.json --format json
```

Fix any errors (unknown styles, bad references, missing assets). Then render:

```bash
herndon render workbooks/report_export/workbook.json --format json
```

Copy the output to the project directory:

```bash
cp .herndon_build/.herndon/builds/report_export/report_export.xlsx writeup/report_export.xlsx
ls -lh writeup/report_export.xlsx
```

---

## Step 6: Verify with the user

Present the result and flag what was inferred:

> "Here's the Excel workbook. A few things to check:
> - **Sheet layout**: [describe sheets and what's on each]
> - **Charts**: [describe chart types and what they show]
> - **Data completeness**: [N rows / N columns of raw data included]
>
> Open it in Excel and let me know if anything needs adjusting."

If the user requests changes, use `herndon sheets` subcommands to modify in
place, then re-validate and re-render.

---

## Key herndon concepts

- **JSON specs are the source of truth** — never edit `.xlsx` directly; always
  modify the JSON and re-render.
- **Render order**: column widths → ranges → cells → merges → tables → charts
  → freeze panes. Cells overwrite range values at the same address.
- **Chart references** must use sheet-qualified ranges with the displayed sheet
  title: `'Sheet Title'!$A$2:$A$5`.
- **Series colors** are hex strings (e.g., `"#2563EB"`).
- **Stacked charts**: use `--stacked` or `--percent-stacked` (mutually
  exclusive, bar/column only).
- **Images**: embed via `set-cell` with `--image-path`, `--w`, `--h` (inches).
  Only PNG and JPEG supported.

---

## Reference files

- `references/herndon-patterns.md` — complete CLI command reference for all
  sheet operations (cells, ranges, tables, charts, images, merges, freeze)
