# Plot Standards

All analysis scripts that generate report plots MUST follow these standards. The shared `plot_style.py` module (in this skill's `scripts/` directory) enforces most of them automatically.

## Quick start

### Step 1 — Copy plot_style.py into the study

When scaffolding a study's analysis/ directory, copy `plot_style.py` from this skill:

```bash
PLOT_SKILL_DIR="<absolute base directory reported when this skill loaded>"
cp "$PLOT_SKILL_DIR/scripts/plot_style.py" analysis/plot_style.py
```

Replace the placeholder with the exact `Base directory for this skill:` path
reported by the Skill tool. Do not derive bundled-resource paths with
`git rev-parse`; a study workspace need not be inside a Git checkout.

### Step 2 — Import it at the top of every plot script

```python
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import plot_style  # noqa: F401  — applies rcParams as side-effect

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
```

That single import applies all font sizes, color cycles, and save defaults globally. No other setup is needed.

## Mandatory rules

These are enforced in `plot_style.py` via `rcParams`. Do not override them in individual scripts unless you have a specific reason (and document it).

### Font sizes

| Element | Minimum | Set by rcParams |
|---|---|---|
| Figure title (suptitle) | 15pt | `figure.titlesize: 15` |
| Axes title | 14pt | `axes.titlesize: 14` |
| Axes labels (x/y) | 12pt | `axes.labelsize: 12` |
| Tick labels | 10pt | `xtick.labelsize / ytick.labelsize: 10` |
| Legend text | 10pt | `legend.fontsize: 10` |
| Bar / annotation labels | 9pt minimum | use `label_bars()` helper |

**Never set `fontsize` below 9pt anywhere in a plot script.** If a label doesn't fit, abbreviate the text or rotate it — do not shrink the font.

### Figure sizes

Use the `FIGSIZE` dict from `plot_style` for standard layouts:

```python
fig, ax = plt.subplots(figsize=plot_style.FIGSIZE["single"])     # one panel
fig, axes = plt.subplots(1, 2, figsize=plot_style.FIGSIZE["two_wide"])  # two panels side by side
```

For stacked panels, use the helper:

```python
fig, axes = plt.subplots(n_rows, 1, figsize=plot_style.figsize_stacked(n_rows))
```

Do **not** hard-code `figsize=(8, 4)` etc. — use the named constants so that sizes are consistent across the study.

### Saving

Always save using `plot_style.save(fig, path)`:

```python
plot_style.save(fig, PLOT_OUT)
```

This automatically applies:
- `dpi=150`
- `bbox_inches="tight"`
- `pad_inches=0.15`
- `tight_layout()` (called before saving)

If you must call `fig.savefig()` directly, you must include all of the above arguments.

### Layout

Always call `fig.tight_layout()` **or** use `layout="constrained"` (but not both — they conflict). `plot_style.save()` calls `tight_layout()` for you.

Do not set `plt.subplots_adjust()` manually unless you are adding a shared legend outside the grid — in that case, document the values.

## Handling long labels

Long category names on axes cause overlapping text. Use the helpers in `plot_style.py`:

```python
# Option 1: Auto-rotate if any label is long
plot_style.fix_xtick_labels(ax, max_chars=12, rotation=30)

# Option 2: Word-wrap labels before setting them
wrapped = plot_style.wrap_labels(["Very long category name", "Another"], width=12)
ax.set_xticklabels(wrapped)
```

For horizontal bar charts, long y-tick labels are usually fine — they have more space.

## Color palettes

Use palettes from `plot_style` to keep colors consistent within a study:

```python
# 5-point Likert (red → green)
colors = plot_style.LIKERT5_COLORS

# 2-group contrast
colors = plot_style.DIVERGING2

# General categorical (up to 8 groups)
colors = plot_style.CATEGORICAL
```

If you use custom colors, document why in a comment.

## Bar / annotation labels

Use the helpers to add data labels:

```python
# Vertical bars
bars = ax.bar(x, values)
plot_style.label_bars(ax, bars, fmt="{:.0f}%")

# Horizontal bars
bars = ax.barh(y, values)
plot_style.label_hbars(ax, bars, fmt="{:.1f}")
```

These functions skip labels on bars narrower than 3% (avoids clutter) and enforce a minimum font size of 9pt.

## Stacked percent bar charts (Likert)

### Choosing the right figsize — common mistake

**Never use `figsize_stacked()` for a Likert chart.** That function is for subplot panels (each row is a separate axes). Using it for a single-axes multi-bar chart gives e.g. 12x14 inches for 5 bars — the bars become thin slivers and all text reads small even at correct point sizes.

Use `figsize_likert(n_rows)` instead:

```python
fig, ax = plt.subplots(figsize=plot_style.figsize_likert(n_rows))
```

`figsize_likert(5)` produces ~14x9 inches. Bars are ~1.3 inches tall and all labels are readable without zooming.

### Also set y-tick label size explicitly

The rcParams default tick label size (10pt) is too small when the category names on the y-axis are the primary navigation of the chart. Always set:

```python
ax.tick_params(axis="y", labelsize=13)
```

### Use `stacked_pct_hbar()` — never implement stacked bars manually. Call it once per row:

```python
for role in ROLES:
    plot_style.stacked_pct_hbar(
        ax,
        label=role,                        # the y-axis category string
        fractions=SATISFACTION[role],      # must sum to ~100
        colors=plot_style.LIKERT5_COLORS,
        option_labels=["Very dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very satisfied"],
        min_pct_for_text=7,                # skip label if segment < 7%
    )
```

### Known pitfall: ax.text() with categorical y-axes

When a horizontal bar chart uses string labels on the y-axis (as all stacked Likert charts do), passing a literal `0` as the y-coordinate to `ax.text()` will place ALL labels at the first category — they collapse and overlap. Always pass the label string itself as the y-coordinate:

```python
# WRONG — all text collapses to first category
ax.text(x, 0, "label")

# CORRECT — text renders at the correct row
ax.text(x, label, "label")   # label is the string category name
```

`stacked_pct_hbar()` handles this correctly internally. This pitfall only applies if you write `ax.text()` calls manually on a categorical barh chart.

## Heatmap colorbars

**Never use `plt.colorbar(im, ax=ax, ...)`** — this shrinks the axes to make room and causes the colorbar to overlap cell annotations when the figure is tight.

Always use `make_axes_locatable` to carve out a dedicated strip:

```python
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
plt.colorbar(im, cax=cax, label="Your label here")
```

This allocates a fixed-width strip to the right of the axes without disturbing the data area, and works correctly with `bbox_inches="tight"` on save.

## Legend placement

Legends placed inside the axes (`loc="upper right"` etc.) will be overlapped by any bar or line that reaches into that corner. Always anchor legends **outside** the data area:

```python
# Below the axes (most common — works for any chart type)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),   # negative y puts it below the axes
    ncol=2,
    framealpha=0.95,
)
# bbox_inches='tight' in plot_style.save() will capture it automatically.
```

For figure-level legends (e.g. Likert charts where the legend describes shared colors):

```python
fig.legend(handles, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=5)
fig.subplots_adjust(bottom=0.12)   # reserve space so legend isn't clipped
```

**Never use `loc="upper right"` or `loc="upper left"` when any bar or line could reach above ~75% of the y-axis range.** With a y-axis of 0–100, a bar at 81% will overlap a legend box that starts at ~88%.

## Checklist before committing a plot script

Before considering a plot script done, verify:

- [ ] `import plot_style` is at the top (after sys.path.insert)
- [ ] Likert / multi-bar single-axes charts use `figsize_likert(n)`, not `figsize_stacked(n)`
- [ ] Other charts use `plot_style.FIGSIZE[...]` or `figsize_stacked(n)` for subplot panels
- [ ] All text in `ax.text()` / `ax.annotate()` calls has `fontsize >= 11`
- [ ] No manual `fontsize` smaller than the rcParams minimum for that element
- [ ] Likert charts: `ax.tick_params(axis="y", labelsize=13)` set explicitly
- [ ] Saved with `plot_style.save(fig, PLOT_OUT)` (or equivalent)
- [ ] Long x-tick labels handled with `fix_xtick_labels()` or `wrap_labels()`
- [ ] Legend placed outside the data area (below axes or figure-level)
- [ ] Heatmap colorbars use `make_axes_locatable` / `cax=` pattern, not `plt.colorbar(im, ax=ax)`
- [ ] For categorical barh charts: `ax.text()` y-coordinate uses the label string, not `0`
- [ ] **After generating all plots**, invoke `skill:report-plot-checker` to run automated visual validation (DPI, clipping, font sizes). Do not skip this step.

## Example: minimal bar chart script

```python
"""
plot_example.py
Produces writeup/plots/example.png
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import plot_style

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

STUDY_ROOT = pathlib.Path(__file__).resolve().parent.parent
PLOT_OUT   = STUDY_ROOT / "writeup" / "plots" / "example.png"

def main():
    categories = ["Group A", "Group B", "Group C"]
    values     = [42, 67, 31]

    fig, ax = plt.subplots(figsize=plot_style.FIGSIZE["single"])
    bars = ax.bar(categories, values, color=plot_style.CATEGORICAL[:3])
    plot_style.label_bars(ax, bars, fmt="{:.0f}%")

    ax.set_ylabel("Percentage")
    ax.set_title("Example Chart")
    fig.suptitle("Study Title Here")

    plot_style.fix_xtick_labels(ax)
    plot_style.save(fig, PLOT_OUT)

if __name__ == "__main__":
    main()
```
