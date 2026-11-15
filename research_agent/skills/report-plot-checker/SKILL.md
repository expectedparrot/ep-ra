---
name: report-plot-checker
description: >
  Automated visual quality checker for report plots. Runs check_plots.py
  against writeup/plots/ to detect low DPI, blank images, edge clipping,
  unreferenced files, and missing captions. Use when finalizing a report to
  catch rendering problems before compilation.
tags: [report, quality-check, visualization]
---

# Visual QA

After generating plots, run the visual QA checker to catch common rendering problems before the report is finalized.

## Setup

Copy `check_plots.py` from this skill's scripts directory into the study's `analysis/` folder:

```bash
cp research_agent/skills/report-plot-checker/scripts/check_plots.py analysis/check_plots.py
```

It requires Pillow and NumPy, both declared in the ep-agent locked runtime.

## Running the checker

From the study root:

```bash
python analysis/check_plots.py
```

Or with an explicit path:

```bash
python analysis/check_plots.py --study-root /path/to/study
```

`--study-root` is an option; the checker does not accept a positional study
path. If the copied script may be from a different revision, inspect
`python analysis/check_plots.py --help` before invoking it.

For machine-readable output (useful in scripts or Makefile targets):

```bash
python analysis/check_plots.py --json
```

Exit codes: `0` = no errors, `1` = one or more errors found.

## What it checks

### Per-image checks

| Check | Severity | Description |
|---|---|---|
| `dpi` | error / warning | DPI below 120 = error; below 150 = warning |
| `dimensions` | error / warning | Width < 600px or height < 300px = error; > 6000px = warning |
| `blank` | error / warning | Mean pixel > 248 (nearly white) = error; < 2% dark pixels = warning |
| `clipping` | warning | Non-white pixels within 8px of image edge — may indicate cut-off labels or titles |
| `aspect_ratio` | warning | Ratio > 8:1 (too wide) or < 0.3:1 (too tall) |
| `caption` | warning | Image in report.md not followed by a "Figure N:" caption within 3 lines |

### Report-level checks

| Check | Severity | Description |
|---|---|---|
| `unreferenced` | warning | PNG exists in writeup/plots/ but not referenced in report.md |
| `missing_file` | error | Image referenced in report.md but the file does not exist |

## Interpreting results

### Errors — must fix before study is complete

- **dpi < 120**: Regenerate the plot with `dpi=150`. If using `plot_style.save()`, this is automatic.
- **dimensions too small**: Increase `figsize`. Use `plot_style.FIGSIZE` constants.
- **blank image**: The plot script failed silently. Check for exceptions in the script, missing data, or an empty DataFrame being passed to the plot.
- **missing_file**: A plot referenced in `report.md` was never generated. Run the analysis script.

### Warnings — should fix before study is complete

- **dpi warning (120-149)**: Bump to 150 for consistency.
- **clipping**: Add `bbox_inches='tight'` or increase `pad_inches`. Check that `suptitle` doesn't escape the figure.
- **unreferenced**: Either add the plot to `report.md` or delete the file if it's not needed.
- **no caption**: Add a `Figure N: Description` line below each image in `report.md`.
- **aspect ratio**: Adjust `figsize` to better match the content.

## Adding to the Makefile

Add a `qa` target to the study's `Makefile`:

```makefile
qa:
	python analysis/check_plots.py

check: PLOTS TABLES qa
```

Then run `make check` to generate plots, tables, and run QA in one step.

## Limitations

The checker uses heuristics — it cannot:

- Detect overlapping text annotations inside a rendered image (this requires matplotlib introspection at generation time, not post-hoc image analysis)
- Verify that axis labels are semantically correct
- Detect colorblindness issues

For text-overlap issues, the fix is upstream: use `plot_style.fix_xtick_labels()`, `wrap_labels()`, and reduce annotation density. See `research_agent/skills/report-authoring`.

## Workflow integration

Run `check_plots.py` as part of the checklist gate:

1. Run `make PLOTS` to generate all plots
2. Run `python analysis/check_plots.py` — fix all errors, address warnings
3. Only then tick the Visual Quality checklist items in `checklist.md`
