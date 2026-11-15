---
name: research-literature-review
description: >
  Conducts a structured literature review on a research question and produces
  a standalone report. Use when the user wants a literature review as a
  deliverable in its own right — not as a step inside a larger study.
  Follows the same EP report format as other research studies.
tags: [study-type, academic, reference, workflow]
---

# Literature Review Study

This skill produces a standalone literature review report. The intellectual work — searching, screening, reading, annotating, linking, and synthesizing — is done by `skill:workflow-literature-review`. This skill adds the study scaffolding and report rendering that turns that work into a finished EP deliverable.

## When to use this vs. `skill:workflow-literature-review`

| Situation | Use |
|-----------|-----|
| Literature review is the final deliverable | **This skill** |
| Literature review is an input to a study you're about to run | `skill:workflow-literature-review` directly |
| You already have a study directory and just need to search and synthesize | `skill:workflow-literature-review` directly |

---

## Phase 1: Scaffold the study

Determine the topic alias and next available study letter, then scaffold:

```bash
ep study scaffold \
    sessions/topic_<alias>/study_<letter>
```

Create or update the topic-level `README.md`:

```markdown
# PURPOSE
<One-sentence description of the research question or domain>

# Author
<Name>

# Timestamp
<Today's date>

# LOG
- <date>: Created literature review study
```

---

## Phase 2: Do the literature review

Follow `skill:workflow-literature-review` in full, working inside the study directory just created. That skill covers:

- Defining inclusion/exclusion criteria
- Initializing the dewey bibliography repository
- Discovering papers (Semantic Scholar + WebSearch)
- Logging all searches in `literature/search_log.md`
- Abstract triage before full ingestion
- Reading, appraising, and annotating each paper in dewey
- Linking papers by relationship type
- Setting review order
- Searching the annotated corpus for themes

When that process is complete, you will have:
- `.dewey/` — the full bibliography database
- `literature/research_question.md` — question and inclusion criteria
- `literature/search_log.md` — search history
- `literature/review.md` — the synthesized review (written in the final step of `skill:workflow-literature-review`)

---

## Phase 3: Write the report

Write `writeup/report.md` by adapting the synthesis from `literature/review.md` into the EP report format. This is not a copy-paste — shape it into a polished, self-contained document.

```markdown
---
title: "Literature Review: <Research Question>"
date: <YYYY-MM-DD>
---

## Summary

<3–4 sentences: what the literature establishes, where it is contested,
and what gap this review identifies. This is the abstract — write it last.>

## Research Question

<The focused research question, including the population/domain,
phenomenon, and outcome as defined in literature/research_question.md>

## Scope and Methods

<Inclusion/exclusion criteria used. Databases and search tools used.
Number of candidates identified, screened, and included. Date range covered.
This section makes the review reproducible.>

## Key Themes

### <Theme 1>
<Cross-paper synthesis — explain why papers agree or diverge, not just
what each found. Include effect sizes where available.>
- Author (Year, Journal): finding [effect size if available]
- Author (Year, Journal): contrasting or supporting finding

### <Theme 2>
...

## Methodological Landscape

<What study designs have been used? What are typical sample sizes?
What validated instruments or scales exist for the core constructs?
What populations have been studied — and what gaps remain?>

## Evidence Quality

<Overall strength of the literature: number of studies, proportion
experimental vs. correlational, whether key findings have been replicated,
dominant limitations across the literature.>

## Gaps and Contribution

<What has not been studied? Where do findings conflict without resolution?
What question a follow-on study should address and why.>

## Implications for Future Research

<Specific, actionable recommendations for study design:>
- Constructs to measure (with validated scale recommendations)
- Expected effect sizes or base rates from prior work
- Confounds to control (cite the papers that identify them)
- Recommended analysis approaches (with precedent)
- Sample size guidance from comparable studies

## References

<BibTeX entries for all included sources — export from dewey:>
```

Export the reference list:
```bash
dewey list --status included --json | python3 -c "
import json, sys, subprocess
for s in json.load(sys.stdin)['sources']:
    subprocess.run(['dewey', 'cite', s['source_id'], '--format', 'bibtex'])
"
```

---

## Phase 4: Render and verify

Copy report assets and render:

```bash
ep study scaffold <study_root>
```

Add Makefile targets:

```makefile
# --- Report ---
writeup/report.html: writeup/report.md
	cd writeup && pandoc report.md -o report.html --standalone --embed-resources --css=report.css

writeup/report.pdf: writeup/report.md writeup/report_header.tex writeup/fix-table-widths.lua
	cd writeup && pandoc report.md -o report.pdf --pdf-engine=xelatex \
	    --include-in-header=report_header.tex --lua-filter=fix-table-widths.lua

report: writeup/report.html writeup/report.pdf
```

Build and verify:

```bash
make report
ep report check --root <study_root>
```

---

## Final file layout

```
study_root/
  .dewey/                         # dewey bibliography database
  literature/
    research_question.md          # question + inclusion/exclusion criteria
    search_log.md                 # log of all searches run
    review.md                     # working synthesis (input to report)
    sources/                      # .bib files
    pdfs/                         # PDFs
  writeup/
    report.md                     # polished EP report (the deliverable)
    report.html                   # rendered HTML
    report.pdf                    # rendered PDF
  README.md
  Makefile
```
