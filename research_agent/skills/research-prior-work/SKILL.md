---
name: research-prior-work
description: >
  Ingests and documents an existing research project the user uploads
  (papers, data, reports, code). Creates a topic and study, records the
  files, and writes a report.md summarizing context and conclusions.
  Use when the user has completed research they want to archive,
  document, or build on within the EP system.
tags: [study-type, academic, reference]
---

# Prior Work Ingestion

Use this skill when a user provides materials from an **already-completed** research project and wants them recorded in the EP study system. The goal is to create a well-organized archive with a report that captures what was done and what was found, so future studies can reference it directly.

## When to use this skill

- User uploads a paper, report, dataset, or code from a finished project
- User says "I did this study already" or "here's my prior work"
- User wants to document existing research so it can be referenced later
- User is importing external research (their own or others') into the EP system

## Not the right skill

| Need | Use instead |
|------|-------------|
| Search for academic literature on a topic | `skill:workflow-literature-review` |
| Run a new survey or experiment | `skill:research-survey`, `skill:research-conjoint`, etc. |
| Browse what studies already exist | `skill:workflow-study-index` |

---

## Workflow

### Phase 1: Orient and understand the materials

Before creating anything, read and understand what the user has provided.

1. **Inventory the uploads.** List every file the user has provided (PDFs, CSVs, images, code, etc.). Note file types, sizes, and apparent purpose.

2. **Read the materials.** Extract the key information:
   - What research question was addressed?
   - What methods were used?
   - What data was collected or analyzed?
   - What were the main findings and conclusions?
   - Who did the work and when?
   - Are there limitations or open questions noted?

3. **Confirm understanding with the user.** Before proceeding, present a brief summary of what you understood from the materials and ask if anything is missing or incorrect. This is especially important if the materials are ambiguous or incomplete.

### Phase 2: Create the topic and study

4. **Determine the topic alias.** Derive a descriptive kebab-case alias from the research subject. Check `sessions/` for existing topics -- if the prior work belongs under an existing topic, use that topic instead of creating a new one.

5. **Create the study directory.** Use `ep study scaffold` to scaffold the structure:

   ```bash
   ep study scaffold \
       sessions/topic_<alias>/study_<letter>
   ```

   Choose the next available study letter. If this is a new topic, start with `study_a`.

6. **Create the topic-level README** (if new topic):

   ```markdown
   # PURPOSE
   <One-sentence description of the research area>

   # Author
   <User name or "Imported from external source">

   # Timestamp
   <Today's date>

   # LOG
   - <date>: Created topic and imported prior work into study_<letter>
   ```

### Phase 3: Record the files

7. **Place files in the correct locations** following `skill:workflow-file-layout` conventions:

   | File type | Destination |
   |-----------|-------------|
   | Raw data (CSV, JSON, Excel) | `data/raw/` |
   | Processed/cleaned data | `data/cooked/` |
   | User-uploaded originals (PDFs, docs) | `data/uploaded/` |
   | Analysis scripts (Python, R) | `analysis/` |
   | Intermediate results | `computed_objects/` |
   | Images, figures from prior work | `writeup/plots/` |

8. **Preserve file provenance.** Keep original filenames where practical and document each file's source and destination in `README.md`.

9. **Update README.md** with a log entry for each file added, noting what it is and where it was placed.

### Phase 4: Write the report

10. **Write `writeup/report.md`** using the standard EP report format. The report should synthesize the prior work -- not just describe the files, but explain the research in a way that is useful to someone designing a follow-up study.

    ```markdown
    ---
    title: "Prior Work: <Descriptive Title>"
    date: <YYYY-MM-DD>
    ---

    ## Summary

    <2-3 paragraph overview: what was studied, how, and what was found>

    ## Research Context

    ### Research Question
    <The question(s) the prior work addressed>

    ### Motivation
    <Why this research was conducted -- the gap or need it filled>

    ## Methods

    <Description of the methodology: study design, sample, instruments,
    analysis approach. Be specific enough that someone could understand
    what was done without reading the original materials.>

    ## Key Findings

    <Main results, organized by theme or research question. Include
    specific numbers, effect sizes, or qualitative conclusions where
    available.>

    ## Limitations and Open Questions

    <Known limitations of the prior work. Questions that remain
    unanswered. Opportunities for follow-up research.>

    ## Archived Materials

    | File | Location | Description |
    |------|----------|-------------|
    | <filename> | `data/raw/` | <what it contains> |
    | ... | ... | ... |

    ## Implications for Future Work

    <What a follow-up study should consider. What hypotheses remain
    untested. What methods could be improved.>
    ```

11. **Copy report assets** into `writeup/`:

    ```bash
    ep study scaffold <study_root>
    ```

12. **Wire up the Makefile** with report targets:

    ```makefile
    # --- Report ---
    writeup/report.html: writeup/report.md
        cd writeup && pandoc report.md -o report.html --standalone --embed-resources --css=report.css

    writeup/report.pdf: writeup/report.md writeup/report_header.tex writeup/fix-table-widths.lua
        cd writeup && pandoc report.md -o report.pdf --pdf-engine=xelatex --include-in-header=report_header.tex --lua-filter=fix-table-widths.lua

    report: writeup/report.html writeup/report.pdf
    ```

### Phase 5: Verify

13. **Verify the study** by running the visual audit:

    ```bash
    ep report check --root <study_root>
    ```

---

## Handling different input types

### Papers (PDF)

- Place the PDF in `data/uploaded/`
- Read it to extract research question, methods, findings
- If the paper contains tables or figures worth preserving separately, extract them to `writeup/plots/` or `writeup/tables/`

### Datasets

- Place raw data in `data/raw/`
- If the user provides a data dictionary or codebook, place it alongside the data
- Note column meanings and data provenance in the report

### Code / notebooks

- Place analysis scripts in `analysis/`
- Note dependencies in `requirements.txt`
- If the code produces outputs, document what it generates in the report

### Presentations or informal writeups

- Place originals in `data/uploaded/`
- Extract the key points into the report -- don't just reference the file, synthesize the content

### Mixed materials

When the user provides multiple file types, process them all. The report should weave them together into a coherent narrative about the prior work.

---

## Follow-up studies

Once prior work is archived, future studies should record its absolute path and any study/session identifier in `writeup/planning.md` or `chat_summary.md`, then read its `chat_summary.md` and required artifacts in place. If portability is necessary, copy only the required immutable artifacts into `refs/<study>/` and include the provenance manifest described in `skill:workflow-file-layout` rule 8.

---

## Quick reference

| Step | Action | Output |
|------|--------|--------|
| Orient | Read and understand materials | Mental model of the research |
| Scaffold | `ep study scaffold` | Study directory structure |
| Record | Place and document files | Organized archive |
| Report | Write `writeup/report.md` | Synthesis of prior work |
| Verify | `ep report check --root <study_root>` | Report checks pass |
