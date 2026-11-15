# Sonesta CLI Patterns

Complete command examples for building slides with the runtime-owned `sonesta`
CLI. If `sonesta --help` fails, report the environment problem; do not install
or clone Sonesta during a study.

## Contents
1. Project setup
2. Slide title field vs. headline elements (IMPORTANT)
3. Slide presets and when to use each
4. Slide management
5. Headline text
6. Bullet list
7. Image (chart or photo)
8. Table
9. Speaker notes
10. Remove an element
11. Validate and render
12. Coordinate reference
13. Text spacing
14. Default brand (Expected Parrot)

---

## 1. Project setup

```bash
mkdir -p .sonesta_build && cd .sonesta_build
sonesta init .
sonesta new presentation report
```

Presentation spec: `presentations/report/presentation.json`

`new presentation` creates the `title` slide automatically. Edit that slide
instead of adding another slide with the `title` id.

Rendered output: `.sonesta/builds/report/report.pptx`

---

## 2. Slide title field vs. headline elements (IMPORTANT)

Every slide JSON has a `"title"` field that is **separate from elements**.
The renderer always draws this title as a **fixed text box** at x=0.5",
y=0.3", 24pt bold, using the theme heading font. It renders **before** any
elements, so elements placed in the same region will overlap.

**Rules to avoid overlap:**

- **Use `--preset blank` for all slides.** This avoids the preset creating
  default slot elements (`body`, `subtitle`) that conflict with your
  positioned elements.
- **Do NOT add headline elements at y < 1.0".** The title field occupies
  y=0.3" to ~0.9". If you add a positioned headline element in this zone,
  it will overlap.
- **Choose one approach per slide:**
  - **Option A (recommended):** Leave the `title` field empty (don't pass
    `--title` when creating the slide). Add your own positioned headline
    element starting at y=0.4". This gives you full control over position,
    font size, and style.
  - **Option B:** Set the `title` field to your heading text. It renders
    automatically at y=0.3", 24pt bold. Do NOT add a separate headline
    element. Start body content at y=1.2" or below.
- **Never do both.** Do not set `"title": "My Heading"` AND add a headline
  element at y=0.4" — they will stack on top of each other.

---

## 3. Slide presets and when to use each

| Preset  | Creates | Best for |
|---------|---------|----------|
| `blank` | No elements at all | Full manual control (recommended) |
| `body`  | Slot-based `body` text element | Simple text-only slides |
| `title` | Slot-based `body` element at 18pt | Title/section divider slides |

**Prefer `--preset blank` for all slides.** The `body` and `title` presets
create slot-based elements that use template-defined positions. If you then
add your own positioned elements, you get overlapping content. With `blank`,
you control every element's position explicitly.

If you do use `--preset body`, the default slot element has
`element_id: "body"`. Either use `update-text` to populate it (and don't add
conflicting elements), or `remove-element` to delete it before adding your
own.

---

## 4. Slide management

```bash
# Add a slide (always use --preset blank for full control)
sonesta new slide \
  presentations/report/presentation.json <slide-id> --preset blank

# List all slides
sonesta slides list \
  presentations/report/presentation.json

# List elements on a slide
sonesta slides elements \
  presentations/report/presentation.json <slide-id>

# Rename a slide
sonesta slides rename \
  presentations/report/presentation.json <old-id> <new-id>

# Reorder: move slide after another
sonesta slides move \
  presentations/report/presentation.json <slide-id> --after <other-id>

# Duplicate a slide
sonesta slides duplicate \
  presentations/report/presentation.json <slide-id> <new-id>

# Remove a slide (and its files)
sonesta slides remove \
  presentations/report/presentation.json <slide-id> --delete-files
```

---

## 5. Headline text

```bash
sonesta slides add-text \
  presentations/report/presentation.json <slide-id> headline \
  --text "Your headline here" \
  --x 0.5 --y 0.4 --w 12.333 --h 0.8 --style headline
```

To update existing text:

```bash
sonesta slides update-text \
  presentations/report/presentation.json <slide-id> headline \
  --text "Updated headline"
```

---

## 6. Bullet list

```bash
sonesta slides add-text \
  presentations/report/presentation.json <slide-id> bullets \
  --bullets-json '["Finding one","Finding two","Finding three"]' \
  --x 0.5 --y 1.6 --w 12.333 --h 5.4 --style body
```

---

## 7. Image (chart or photo)

```bash
sonesta slides add-image \
  presentations/report/presentation.json <slide-id> chart \
  --path analysis/plots/my_chart.png \
  --x 0.5 --y 1.6 --w 12.333 --h 5.4 --fit contain
```

Fit modes: `contain` (default, letterboxed), `cover` (fills, may crop),
`stretch` (distorts to fill).

---

## 8. Table

There is **no `--headers-json` flag**. Include the header row as the first
row in `--rows-json`. The `--first-row-header` flag is on by default.

```bash
sonesta slides add-table \
  presentations/report/presentation.json <slide-id> results-table \
  --rows-json '[["Group","N","Mean","p-value"],["A",120,3.4,"<0.001"],["B",115,2.9,"0.04"]]' \
  --x 0.5 --y 1.6 --w 12.333 --h 3
```

Optional column widths (must sum to `w`):

```bash
  --column-widths-json '[3.0, 2.0, 3.5, 3.833]'
```

---

## 9. Speaker notes

```bash
# Set notes
sonesta slides set-notes \
  presentations/report/presentation.json <slide-id> \
  --text "Presenter talking points go here."

# Read notes
sonesta slides notes \
  presentations/report/presentation.json <slide-id>

# Clear notes
sonesta slides clear-notes \
  presentations/report/presentation.json <slide-id>
```

---

## 10. Remove an element

```bash
sonesta slides remove-element \
  presentations/report/presentation.json <slide-id> <element-id>
```

---

## 11. Validate and render

```bash
# Validate
sonesta validate \
  presentations/report/presentation.json --format json

# Render full deck
sonesta render \
  presentations/report/presentation.json --format json

# Render a single slide (for preview)
sonesta render-slide \
  presentations/report/presentation.json <slide-id> --format json
```

Copy output to final location:

```bash
cp .sonesta_build/.sonesta/builds/report/report.pptx writeup/report.pptx
```

---

## 12. Coordinate reference

Sonesta uses inches. Standard widescreen slide: **13.333 × 7.5 in** (16:9).

> ⚠️ The slide is 13.333" wide, NOT 10". Using 10" coordinates fills only ~75% of the slide.
> Always size content relative to 13.333" width. Recommended margins: 0.5" left/right.

| Region          | x    | y   | w      | h   |
|-----------------|------|-----|--------|-----|
| Full slide      | 0    | 0   | 13.333 | 7.5 |
| Title area      | 0.5  | 0.4 | 12.333 | 1.0 |
| Body area       | 0.5  | 1.6 | 12.333 | 5.4 |
| Left half       | 0.5  | 1.6 | 5.9    | 5.4 |
| Right half      | 7.0  | 1.6 | 5.9    | 5.4 |
| Footer strip    | 0.5  | 6.8 | 12.333 | 0.5 |
| Logo (bottom-R) | 12.0 | 6.8 | 1.0    | 0.5 |

## 13. Text spacing

Spacing properties available on text elements and paragraphs:

**On `TextElement`:**
- `line_spacing` (float) — line height multiplier; default `1.3`. E.g. `1.5` for more open text.

**On `TextParagraph`:**
- `space_before` (int, points) — space above this paragraph. Defaults: `10pt` for level-0 bullets, `3pt` for level-1+.
- `space_after` (int, points) — space below this paragraph.

Example with custom spacing:
```bash
sonesta slides add-text \
  presentations/report/presentation.json slide-id bullets \
  --bullets-json '[{"text":"Main point","bullet":true,"level":0,"space_before":14},
                  {"text":"Detail","bullet":true,"level":1,"space_before":4}]' \
  --x 0.5 --y 1.6 --w 12.333 --h 5.4 --style body
```

## 14. Default brand (Expected Parrot)

- **Font**: Plus Jakarta Sans (heading and body)
- **Primary green**: `#00663A`
- **Accent green**: `#1DA66A`
- **Text**: `#1f2937`
- **Background**: `#FFFFFF`
- **Logo**: `refs/slide_template/ep_logo.png` — place at x=12.0, y=6.75, w=1.0, h=0.56
- **Template file**: `refs/slide_template/template.json`
