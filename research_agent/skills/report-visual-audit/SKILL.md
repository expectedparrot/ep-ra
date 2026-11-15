---
name: report-visual-audit
description: >
  Report-level visual audit. Verifies all images in report.md have correct
  captions, are properly referenced, and pass visual QA. Use when the report
  is nearly complete and you need a systematic visual review before compiling
  to PDF.
tags: [report, quality-check, visualization]
---

# Check Writeup Visuals

This skill describes how to perform a complete visual audit of a finished report before it is compiled to PDF.

It complements `scripts/check_writeup.py` (which checks prose structure, links, and section headers) with a visual quality pass.

## When to run this

Run this **after** all plots have been generated and **before** compiling the report to PDF. It is a required step in the study checklist (Visual Quality section).

## The audit has three parts

### Part 1: Automated checks (check_plots.py)

Run the automated checker first to catch objective issues:

```bash
python analysis/check_plots.py
```

This catches: low DPI, small images, blank plots, edge clipping, unreferenced files, and missing captions. See `research_agent/skills/report-plot-checker/SKILL.md` for full details.

Fix all **errors** before proceeding. Address **warnings**.

### Part 2: Image reference audit

Open `writeup/report.md` and do a manual pass through every image embed:

```markdown
![Alt text](plots/figure_name.png)
```

For each one, verify:

**a) The file exists:**
```bash
ls writeup/plots/figure_name.png
```

**b) The alt text is descriptive** (not just "chart" or left blank):
- Bad:  `![](plots/brand_comfort.png)`
- Good: `![Bar chart showing brand data comfort by price sensitivity](plots/brand_comfort.png)`

**c) A caption follows within 2 lines:**
```markdown
![...](plots/brand_comfort.png)

Figure 3: Viewer comfort sharing brand purchasing data with Netflix, by price sensitivity segment (n=12 agents).
```

**d) The caption accurately describes the chart** — read the chart and the caption together. If the caption says "by income level" but the chart shows price sensitivity, that's an error.

**e) Figure numbers are sequential** — Figure 1, Figure 2, Figure 3, ... with no gaps or duplicates.

### Part 3: Visual quality inspection

Use the Read tool to view each PNG file. For each plot, work through this checklist:

#### Readability
- [ ] Figure title (if present) is readable at normal screen zoom
- [ ] Axes labels (x and y) are readable — at least 12pt equivalent
- [ ] Tick labels are readable — at least 10pt equivalent
- [ ] Legend text is readable — at least 10pt equivalent
- [ ] Data labels / bar annotations are readable — at least 9pt equivalent

If you have to zoom in to read any label, the font is too small. Fix by increasing `figsize` or using `plot_style.py` rcParams.

#### Text overlap
- [ ] No tick labels overlap each other
- [ ] No bar annotations overlap each other or bleed off the chart
- [ ] Legend does not cover data
- [ ] Subplot titles do not overlap with data in the panel below

Common fixes:
- Overlapping x-tick labels: `plot_style.fix_xtick_labels(ax)` or `plot_style.wrap_labels()`
- Legend covers data: move legend with `ax.legend(loc="upper right", bbox_to_anchor=(1, 1))` or use `fig.legend()` outside the grid
- Bar annotations overflow: reduce `fmt` precision, increase `figsize`, or set a higher `min_val` threshold in `label_bars()`

#### Clipping
- [ ] Figure title (suptitle) is fully visible within the image bounds
- [ ] No axis labels cut off at the image edge
- [ ] Color bar (if present) is fully visible

Fix: `plot_style.save(fig, path)` uses `bbox_inches='tight'` automatically. For suptitle specifically, call `fig.suptitle(..., y=1.02)` and add `fig.tight_layout(rect=[0, 0, 1, 0.97])`.

#### Layout
- [ ] Subplots have enough space between them (titles don't overlap data in adjacent panel)
- [ ] Color choices are distinguishable (test: would the chart still make sense in greyscale?)
- [ ] No unnecessary chart elements (3D effects, unnecessary gridlines, heavy borders)

#### Data integrity
- [ ] Axis labels include units where relevant (e.g. "% of respondents", "Score (1-5)", "USD")
- [ ] If bars/slices show percentages, they sum to ~100% within each group
- [ ] Zero is included on the y-axis for bar charts showing absolute quantities (unless the variation is the story)

## Output

Document the audit in `writeup/visual_audit.md`:

```markdown
# Visual Audit

Date: YYYY-MM-DD
Auditor: analyze-results / review-report agent

## check_plots.py output
<!-- paste output -->

## Image reference audit
| Figure | File exists | Alt text | Caption | Caption accurate | Fig # sequential |
|--------|------------|----------|---------|-----------------|-----------------|
| Fig 1  | YES        | YES      | YES     | YES             | YES             |
| ...    |            |          |         |                 |                 |

## Visual quality inspection
| Plot | Readable | No overlap | No clipping | Layout OK | Data integrity |
|------|----------|------------|-------------|-----------|----------------|
| ...  |          |            |             |           |                |

## Issues found and fixed
<!-- List each issue and its resolution -->

## Status: PASS / FAIL
```

## Post-compilation HTML preflight (check_report_html.py)

**Run this AFTER compiling report.html, BEFORE delivering to the user.** This catches silent rendering failures that pandoc does not report as errors.

```bash
ep report check --root .
```

Checks:
- **Empty blockquotes** — the `> [bracket]: "text"` link-reference bug that silently eats content
- **Missing images** — `<img>` tags whose `src` doesn't resolve
- **Duplicate H1 headings** — title frontmatter + body `#` heading
- **Uncaptioned figures** — images not followed by a `Figure N:` caption
- **Dangerous source patterns** — scans report.md for `> [text]:` lines before they become invisible

Exit code 1 if any errors found. Must exit 0 before delivering the report.

## Integration with other checks

Three checks must all pass before a study report is considered complete:

```bash
# 1. Report source and compiled HTML
ep report check --root <study_root>

# 2. Plot quality
python analysis/check_plots.py --study-root .

```

If both exit 0 and the visual inspection passes, the report is ready for delivery.
