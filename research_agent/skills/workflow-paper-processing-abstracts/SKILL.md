---
name: workflow-paper-processing-abstracts
description: >
  Given a list of paper titles, retrieves verbatim abstracts and metadata from
  reliable scholarly sources and writes an abstract-only CSV with source URLs.
  Use when the user wants abstract-level bibliographic data for named papers
  without summarizing from memory or downloading full text unless asked.
tags: [workflow, academic, data-collection, external-tool, file-organization]
---

# Paper processing — abstracts only

Given a plain-text list of paper titles, find reliable abstract metadata for each paper and produce a CSV containing **abstract-level information only**.

Do **not** summarize papers from memory. Retrieve abstracts from reliable sources and record where each abstract came from.

For bibliography management and synthesis after collection, see **skill:workflow-literature-review**.

---

## Input

A plain-text list of paper titles, one per line. Example:

```
Attention Is All You Need
BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
Language Models are Few-Shot Learners
```

---

## Output

Create `data/papers/abstracts.csv` with **exactly** these columns:

`#,Title,Authors,Year,Verbatim Abstract,Abstract Source`

| Column | Definition |
|--------|------------|
| `#` | Row number (1-based, sequential). |
| `Title` | Canonical paper title from the source. |
| `Authors` | Author list as shown by the source. |
| `Year` | Publication year. |
| `Verbatim Abstract` | Exact abstract copied from the source. |
| `Abstract Source` | URL or source name where the abstract was found. |

Use proper CSV escaping for commas, quotes, and line breaks inside abstracts.

---

## Core rules

1. **Only collect abstracts** — no full paper text unless the user explicitly requests it (see below).
2. **Do not summarize** — copy the abstract verbatim; do not paraphrase or rewrite.
3. **Minimal cleanup only** — fix obvious formatting artifacts (repeated whitespace, broken line breaks); do not edit wording.
4. **Prefer official or stable sources**, in this priority order:
   1. Official publisher or conference page
   2. arXiv, ACL Anthology, OpenReview, PubMed, DOI landing page
   3. Semantic Scholar or other scholarly index
   4. University-hosted metadata page
   5. Other credible academic source (avoid random PDFs, blogs, GitHub, citation mirrors unless nothing better exists)
5. If multiple versions exist, prefer the most canonical or official version.
6. If no abstract is found: leave `Verbatim Abstract` blank and set `Abstract Source` to `Not found`.
7. If the title is ambiguous, pick the most likely academic match and make the source URL make the choice clear.

---

## Procedure

### Step 1: Parse input titles

Read the user-provided list. Treat each non-empty line as one target paper unless the user specifies another format.

Normalize formatting only:

- Extra spaces
- Numbered list prefixes (`1.`, `2)`)
- Bullet points (`-`, `*`)
- Wrapping quotation marks

Do **not** materially change the paper title at this stage.

### Step 2: Search for each paper

For each title, search the web using the exact title in quotes where possible.

Recommended patterns (try in order):

1. `"<paper title>" abstract`
2. `"<paper title>" authors`
3. `"<paper title>" arxiv`
4. `"<paper title>" DOI`

### Step 3: Identify the best source

Apply the source priority in Core rules. Open the chosen page and confirm the title match before extracting metadata.

### Step 4: Extract metadata

For each paper, record:

- Canonical title
- Authors
- Year
- Verbatim abstract (minimal whitespace cleanup only)
- Abstract source (prefer a stable URL)

### Step 5: Write the CSV

Write `data/papers/abstracts.csv` with the required columns. Create parent directories if needed.

Example not-found row:

```csv
1,"Unknown Paper Title","","","","Not found"
```

If only partial metadata is available, fill what you have and source each field clearly.

### Step 6: Report completion

Return the CSV path to the user and a short note:

- Number of papers processed
- Number of abstracts found
- Number of abstracts not found

Do not include long paper summaries unless separately requested.

---

## Optional triage table

If the user asks for progress or a diagnostic view, produce a table:

| Paper title | Link | Summary | Status |

- **Status** is one of: `Abstract only`, `Full paper`, `Neither`.
- **Summary** describes what was found (e.g., "Abstract found on arXiv"), not the paper's intellectual content.

Example:

| Paper title | Link | Summary | Status |
|-------------|------|---------|--------|
| Attention Is All You Need | https://arxiv.org/abs/1706.03762 | Abstract found on arXiv. | Abstract only |

The main deliverable remains the abstract-only CSV.

---

## Full paper text (only if requested)

If the user asks for full paper texts in addition to abstracts:

1. Retrieve full text only from lawful, openly accessible sources.
2. Prefer PDFs from: arXiv, ACL Anthology, OpenReview, PubMed Central, publisher open-access pages, authors' official pages.
3. **Do not bypass paywalls** or use unauthorized copies.
4. Save extracted text under `data/papers/text/` as `NNN_title_slug.txt` (safe lowercase slugs, zero-padded row number).
5. Keep `data/papers/abstracts.csv` separate from full-text files.
6. Report per paper: abstract only, full paper text, or neither.

Example layout:

```
data/
  papers/
    abstracts.csv
    text/
      001_attention_is_all_you_need.txt
      002_bert_pretraining_deep_bidirectional.txt
```

---

## Quality checks

Before returning results, verify:

- [ ] Every input title has exactly one output row.
- [ ] Row numbers are sequential starting at 1.
- [ ] The CSV has exactly the six required columns.
- [ ] Abstracts are verbatim, not summarized.
- [ ] Each found abstract has a source URL or name.
- [ ] No full paper text appears in the abstract CSV.
- [ ] Full-text files (if requested) live only under `data/papers/text/`.

---

## Failure handling

| Situation | Action |
|-----------|--------|
| Paper not found | Keep original title; blank unknown fields; `Abstract Source` = `Not found`. |
| Partial metadata | Fill available fields; source each value. |
| Ambiguous title | Best academic match; source URL must disambiguate. |
| Paywalled full text | Abstract-only in CSV; do not scrape behind paywalls. |
