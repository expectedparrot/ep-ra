# Herndon CLI Patterns

Complete command reference for building Excel workbooks with herndon. Organized
by operation type.

## Contents

- [1. Project and Workbook Setup](#1-project-and-workbook-setup)
- [2. Sheet Creation and Management](#2-sheet-creation-and-management)
- [3. Writing Data — Cells and Ranges](#3-writing-data--cells-and-ranges)
- [4. Tables](#4-tables)
- [5. Charts](#5-charts)
- [6. Images](#6-images)
- [7. Merges and Freeze Panes](#7-merges-and-freeze-panes)
- [8. Validation and Rendering](#8-validation-and-rendering)
- [9. Inspection](#9-inspection)
- [10. Sheet JSON Structure](#10-sheet-json-structure)

---

## 1. Project and Workbook Setup

```bash
# Initialize a new project
herndon init ./my-project

# Create a workbook
herndon new workbook my_report

# Set workbook metadata
herndon workbooks set-title workbooks/my_report/workbook.json "Report Title"
herndon workbooks set-theme workbooks/my_report/workbook.json brand
herndon workbooks set-output workbooks/my_report/workbook.json \
  .herndon/builds/my_report/my_report.xlsx
```

---

## 2. Sheet Creation and Management

```bash
WB=workbooks/my_report/workbook.json

# Create a new sheet
herndon new sheet $WB overview

# List sheets
herndon sheets list $WB

# Reorder: move sheet after another
herndon sheets move $WB detail --after summary

# Rename a sheet
herndon sheets rename $WB old_id new_id

# Duplicate a sheet
herndon sheets duplicate $WB overview overview_copy

# Remove a sheet
herndon sheets remove $WB draft_sheet --delete-files
```

---

## 3. Writing Data — Cells and Ranges

### Individual cells

```bash
# Plain value
herndon sheets set-cell $WB overview A1 --value "Title" --style title

# Formula
herndon sheets set-cell $WB overview B10 --formula "=SUM(B2:B9)" --style currency_total

# Numeric value
herndon sheets set-cell $WB overview C2 --value 42
```

### Ranges (bulk data)

Ranges write a 2D block starting at an anchor cell. This is the primary
method for writing tabular data.

```bash
herndon sheets set-range $WB overview A2 \
  --data-json '[
    ["Category", "Count", "Percentage"],
    ["Strongly Agree", 45, 0.30],
    ["Agree", 42, 0.28],
    ["Neutral", 30, 0.20],
    ["Disagree", 18, 0.12],
    ["Strongly Disagree", 15, 0.10]
  ]' \
  --row-styles '{"0": "header"}' \
  --col-styles '{"2": "percent"}'
```

**Style maps**: `row_styles` and `col_styles` are zero-indexed string keys
mapping to named style IDs. Row styles apply to entire rows in the range;
column styles apply to entire columns. Cell-level `set-cell` overrides both.

**Render order**: ranges render before cells. If you write a range at A2 and
then set-cell at A2, the cell value wins.

---

## 4. Tables

Excel tables give auto-filter, structured references, and banded row styling.

```bash
herndon sheets add-table $WB overview results_table \
  --ref A2:C7 \
  --name ResultsData \
  --style TableStyleMedium2
```

- `table_id`: internal identifier (kebab or snake_case)
- `name`: Excel-visible table name (no spaces)
- `ref`: must cover the header row and all data rows
- `style`: any built-in Excel table style (e.g., `TableStyleMedium2`,
  `TableStyleLight1`)
- Tables must not overlap with merged cell ranges

---

## 5. Charts

### Supported types

`bar`, `column`, `line`, `pie`, `scatter`

### Common options

| Flag | Description |
|---|---|
| `--type` | Chart type (required) |
| `--anchor` | Top-left cell for placement (required) |
| `--title` | Chart title text |
| `--w` / `--h` | Size in inches (default varies) |
| `--series-json` | JSON array of series objects |
| `--stacked` | Stacked bar/column |
| `--percent-stacked` | 100% stacked bar/column |
| `--show-data-labels` | Show value labels on data points |
| `--show-percent-labels` | Show percentage labels (pie) |
| `--show-legend` / `--legend-position` | Legend visibility and position (`r`, `b`, `l`, `t`) |
| `--x-axis-title` / `--y-axis-title` | Axis labels |
| `--value-format` | Number format string for labels |

### Series JSON structure

```json
[
  {
    "label": "Series Name",
    "values": "'Sheet Title'!$B$2:$B$6",
    "categories": "'Sheet Title'!$A$2:$A$6",
    "color": "#2563EB"
  }
]
```

- `values` and `categories` use sheet-qualified absolute references
- The sheet name in the reference must match the sheet's `title` field
- `color` is an optional hex color string

### Pie chart

```bash
herndon sheets add-chart $WB overview pie1 \
  --type pie \
  --anchor E2 \
  --title "Response Distribution" \
  --w 7 --h 5 \
  --show-data-labels \
  --show-percent-labels \
  --legend-position r \
  --series-json '[{
    "label": "Count",
    "values": "'\''Overview'\''!$B$3:$B$7",
    "categories": "'\''Overview'\''!$A$3:$A$7",
    "color": "#0F766E"
  }]'
```

### Bar chart

```bash
herndon sheets add-chart $WB results bar1 \
  --type bar \
  --anchor E2 \
  --title "Scores by Group" \
  --w 8 --h 5 \
  --legend-position b \
  --y-axis-title "Group" \
  --x-axis-title "Score" \
  --series-json '[{
    "label": "Mean Score",
    "values": "'\''Results'\''!$B$2:$B$5",
    "categories": "'\''Results'\''!$A$2:$A$5",
    "color": "#2563EB"
  }]'
```

### Column chart

```bash
herndon sheets add-chart $WB results col1 \
  --type column \
  --anchor E2 \
  --title "Responses by Category" \
  --series-json '[{
    "label": "Count",
    "values": "'\''Results'\''!$B$2:$B$6",
    "categories": "'\''Results'\''!$A$2:$A$6",
    "color": "#7C3AED"
  }]'
```

### Line chart

```bash
herndon sheets add-chart $WB trends line1 \
  --type line \
  --anchor D2 \
  --title "Score Trend" \
  --w 8 --h 5 \
  --y-axis-title "Score" \
  --legend-position r \
  --series-json '[
    {"label": "Group A", "values": "'\''Trends'\''!$B$2:$B$7", "categories": "'\''Trends'\''!$A$2:$A$7", "color": "#2563EB"},
    {"label": "Group B", "values": "'\''Trends'\''!$C$2:$C$7", "categories": "'\''Trends'\''!$A$2:$A$7", "color": "#DC2626"}
  ]'
```

### Stacked / percent-stacked

```bash
# Stacked bar
herndon sheets add-chart $WB mix stacked1 \
  --type bar --stacked \
  --anchor F2 --title "Composition" \
  --series-json '[...]'

# 100% stacked column
herndon sheets add-chart $WB mix pct1 \
  --type column --percent-stacked \
  --anchor F2 --title "Share of Total" \
  --legend-position b --show-data-labels \
  --series-json '[...]'
```

`--stacked` and `--percent-stacked` are mutually exclusive. Only supported for
bar and column types.

### Scatter chart

```bash
herndon sheets add-chart $WB analysis scatter1 \
  --type scatter \
  --anchor E2 \
  --title "Price vs. Demand" \
  --x-axis-title "Price ($)" \
  --y-axis-title "Units Sold" \
  --series-json '[{
    "label": "Observed",
    "values": "'\''Analysis'\''!$B$2:$B$20",
    "categories": "'\''Analysis'\''!$A$2:$A$20",
    "color": "#059669"
  }]'
```

### Updating and removing charts

```bash
# Update an existing chart
herndon sheets update-chart $WB overview pie1 --title "Updated Title"

# Remove a chart or other element
herndon sheets remove-element $WB overview pie1
```

---

## 6. Images

Embed PNG or JPEG images via cell anchoring:

```bash
herndon sheets set-cell $WB overview H1 \
  --image-path assets/logo.png --w 1.6 --h 0.55
```

- `--w` and `--h` are in inches (required when using `--image-path`)
- Relative paths resolve from the project root
- Place images in the `assets/` directory

List and inspect assets:

```bash
herndon assets list --format json
herndon assets inspect assets/logo.png --format json
```

---

## 7. Merges and Freeze Panes

### Merges

```bash
# Merge a range
herndon sheets set-merge $WB overview A1:C1

# Remove a merge
herndon sheets clear-merge $WB overview A1:C1
```

Merges must not overlap with table ranges.

### Freeze panes

```bash
# Freeze header rows
herndon sheets freeze $WB overview --rows 2 --cols 0

# Freeze first column and header
herndon sheets freeze $WB data --rows 1 --cols 1
```

---

## 8. Validation and Rendering

### Validate

```bash
herndon validate workbooks/my_report/workbook.json --format json
```

Checks: schema shape, duplicate IDs, missing themes, invalid addresses,
formula syntax, chart references, merge/table overlap, unknown styles, missing
images.

### Render

```bash
herndon render workbooks/my_report/workbook.json --format json
```

Output: `.xlsx` file at the path set in `workbook.json` build config, plus a
`manifest.json` in the build directory.

---

## 9. Inspection

```bash
# Inspect the workbook
herndon inspect workbooks/my_report/workbook.json --format json

# Inspect a single sheet
herndon inspect workbooks/my_report/sheets/001-overview.json --format json
```

Inspection emits normalized JSON useful for verifying structure before render.

---

## 10. Sheet JSON Structure

Complete sheet JSON for reference. All fields are optional except `sheet_id`
and `title`.

```json
{
  "sheet_id": "overview",
  "title": "Overview",
  "freeze_rows": 2,
  "freeze_cols": 0,
  "zoom": 100,
  "column_widths": {"A": 22, "B": 16},
  "row_heights": {"1": 22},
  "cells": [
    {"cell": "A1", "value": "Title", "style": "title"},
    {"cell": "B8", "formula": "=SUM(B3:B7)", "style": "currency_total"},
    {"cell": "H1", "image_path": "assets/logo.png", "w": 1.6, "h": 0.55}
  ],
  "ranges": [
    {
      "anchor": "A2",
      "data": [
        ["Category", "Amount"],
        ["Rent", 2400],
        ["Travel", 900]
      ],
      "row_styles": {"0": "header"},
      "col_styles": {"1": "currency"}
    }
  ],
  "merges": [],
  "tables": [
    {
      "table_id": "expense_table",
      "name": "ExpenseData",
      "ref": "A2:B8",
      "header_row": true,
      "auto_filter": true,
      "style": "TableStyleMedium2"
    }
  ],
  "charts": [
    {
      "chart_id": "expense_pie",
      "chart_type": "pie",
      "title": "Spend by Category",
      "anchor": "D2",
      "w": 7,
      "h": 5,
      "series": [
        {
          "label": "Amount",
          "values": "'Overview'!$B$3:$B$7",
          "categories": "'Overview'!$A$3:$A$7",
          "color": "#0F766E"
        }
      ],
      "show_legend": true,
      "legend_position": "r",
      "show_data_labels": true,
      "show_percent_labels": true
    }
  ]
}
```
