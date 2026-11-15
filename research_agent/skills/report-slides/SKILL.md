---
name: report-slides
description: >
  Generates PowerPoint slide decks using the sonesta CLI, learns company
  templates from user-provided examples, and records template knowledge with
  the study. Use whenever the user wants a presentation deck rather
  than a written report, or wants to convert a finished report into slides.
tags: [report, workflow, external-tool]
---

# Slide Deck Generation (sonesta)

This skill covers the full workflow for producing `.pptx` slide decks using
[sonesta](https://github.com/expectedparrot/sonesta), an agent-focused CLI
for deterministic, local-first PowerPoint generation. Read this skill whenever
`skill:report-authoring` resolves format to "slides", or the user asks for a deck,
presentation, or wants to convert a written report into slides.

---

## Step 0: Verify sonesta

The ep-agent runtime owns the Sonesta installation. Do not install, upgrade,
clone, or inspect package source during a study. Verify the CLI is available:

```bash
sonesta --help
```

If this fails, report an environment problem rather than mutating the study
sandbox. All subsequent commands invoke `sonesta` directly.

---

## Step 1: Check for a study-local brand template

Before asking the user for anything, check the current study's
`refs/slide_template/` directory:

```
refs/slide_template/
  template.json       # extracted + verified style properties
  reference_slides/   # original example images
    slide_01.png
```

If a verified template exists, say so:

> "I have your Acme Corp template on file — I'll use that. Let me know if it
> has changed or if you'd like a different style."

Check `template.json` for `"verified": true`. This is explicit study input,
not hidden cross-study memory. If the user identifies a predecessor study,
follow the predecessor rules in `workflow-file-layout`: reference it in place,
or copy only the required template artifacts with provenance when portability
is required. If the template was generated
but never confirmed, treat it as a draft and say so. If no template exists,
proceed to Step 2.

---

## Step 2: Learn from user-provided examples

If no stored template exists, ask for brand examples before generating:

> "Do you have example slides or a company template I should match? A PPTX
> file, PDF, or even 2–3 slide images is enough to extract the key style
> properties."

Extract: background colors, primary/secondary brand colors, title/body fonts,
logo presence and position, footer pattern. See `references/template-schema.md`
for the full list of properties to capture.

Save extracted properties to
`<study_root>/refs/slide_template/template.json` immediately and save provided
examples under `<study_root>/refs/slide_template/reference_slides/`. Set
`"verified": false` until the user confirms the output in Step 5.

If the user provides a PPTX file, extract colors and fonts from it using the
Python snippet in `references/template-schema.md`.

---

## Step 3: Read the source material

If converting an existing report, read it fully before planning slides
(typically `writeup/report.md`). Identify:

- Central finding or thesis
- Top-level sections → candidate slides
- Charts, tables, or figures already present
- Key statistics worth highlighting

If building from scratch (no existing report), gather the content outline from
the user before proceeding.

---

## Step 4: Confirm the slide structure

Draft an outline and confirm it with the user before generating anything:

> "Here's the structure I'm planning:
> 1. Title slide
> 2. Key finding (headline stat)
> 3. [Section 1]
> 4. [Section 2]
> ...
> N. Methodology (appendix)
>
> Does that match what you need, or would you like to adjust?"

One key finding per slide. Aim for one headline + 3–5 bullets or one chart
per content slide.

---

## Step 5: Build the deck with sonesta

### Initialize a project

```bash
mkdir -p .sonesta_build && cd .sonesta_build
sonesta init .
sonesta new presentation report
```

Output lands at `presentations/report/presentation.json`.
The new presentation already contains a `title` slide. Use that slide for the
deck title; do not run `new slide ... title` a second time.

### Add slides

**Use `--preset blank` for all slides.** This gives you full control over
element positioning and avoids overlap from preset slot elements. See
`references/sonesta-patterns.md` §2-3 for details on why.

```bash
sonesta new slide \
  presentations/report/presentation.json <slide-id> --preset blank
```

Use short kebab-case IDs (e.g., `key-finding`, `demographics`).

**Critical: the slide `title` field.** Each slide has a `title` field that
renders as a fixed text box at y=0.3" (24pt bold). If you also add a
positioned headline element in the same area, they will overlap. Read
`references/sonesta-patterns.md` §2 before adding content.

See `references/sonesta-patterns.md` for complete element commands covering:
headline text, bullet lists, images, charts, tables, and speaker notes.

Apply brand properties from `template.json` when adding elements — use
`--style headline` / `--style body` and match colors and fonts to the stored
template values.

### List and inspect as you build

```bash
sonesta slides list \
  presentations/report/presentation.json

sonesta slides elements \
  presentations/report/presentation.json <slide-id>
```

### Validate before rendering

```bash
sonesta validate \
  presentations/report/presentation.json --format json
```

Fix any errors (duplicate element IDs, missing required fields, out-of-bounds
coordinates) before rendering.

### Render

```bash
sonesta render \
  presentations/report/presentation.json --format json
```

Output: `.sonesta/builds/report/report.pptx`

Copy to the canonical location:

```bash
cp .sonesta_build/.sonesta/builds/report/report.pptx writeup/report.pptx
ls -lh writeup/report.pptx
```

---

## Step 6: Verify output with the user

Ask the user to review the deck. Frame the review around what was inferred:

> "Here's the deck. A few things I inferred I'd like you to check:
> - **Primary color**: used #1a3c6e for headers — correct?
> - **Body font**: used Calibri — does that match your template?
> - **Logo placement**: placed top-right on each slide — right?
>
> Let me know what needs adjusting and I'll update both the slides and the
> stored template."

Apply corrections immediately, then update `template.json` before finishing.

---

## Step 7: Update the study-local template

After the user confirms or corrects:

- Set `"verified": true` for confirmed properties
- Update values for corrected properties
- Update `"last_updated"` to today's date
- Add a `"notes"` entry for anything not captured in structured fields

---

## Reference files

- `references/sonesta-patterns.md` — complete CLI command examples for every
  element type (text, bullets, image, table, chart, notes)
- `references/template-schema.md` — full `template.json` schema and color
  extraction helpers
