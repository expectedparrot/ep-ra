---
name: workflow-literature-review
description: >
  Gather, manage, and synthesize academic literature for a research question
  using the dewey CLI bibliography manager. Use when the user wants to ground
  a study in existing academic research, find relevant papers, or build a
  structured bibliography that informs study design.
tags: [study-type, academic, reference, workflow, external-tool]
---

# Literature Review with dewey

dewey is a local, filesystem-backed CLI for managing a bibliography during a literature review. It does not search the internet — you discover papers externally, then use dewey to organize, annotate, link, and track them. All state lives under `.dewey/` inside the study directory.

See `references/dewey-commands.md` for the full command reference and `references/social-science-quality.md` for journal tiers and quality signals.

## Environment check

```bash
dewey --version
```

The ep-agent runtime owns the Dewey installation. Do not install, upgrade, or
replace it during a study. If the command is unavailable, report the environment
problem instead of mutating the sandbox.

---

## Step 1: Clarify the research question and set inclusion criteria

Before searching, write a focused research question with a clear population/domain, phenomenon, and outcome. Save it to `literature/research_question.md`.

Immediately below the question, define your **inclusion and exclusion criteria** — before you search, not after. These prevent selection bias toward papers that confirm your priors.

```markdown
## Inclusion criteria
- Publication type: peer-reviewed journal article OR preprint from arXiv/NBER/SSRN
  by authors at research universities (see references/social-science-quality.md)
- Language: English
- Date: [year] to present (or "all time" for foundational/seminal work)
- Empirical: must report original data or a quantitative synthesis (meta-analysis)
- Relevance: must directly study [core construct] in [target population or domain]

## Exclusion criteria
- Opinion pieces, editorials, practitioner reports, blog posts
- Studies with n < [threshold] unless the design is an RCT or field experiment
- Preprints with no institutional affiliation or from unknown authors
```

You will apply these criteria during abstract screening (Step 4). Writing them first makes screening faster and more consistent.

## Step 2: Initialize the dewey repository

Run once from the study root:

```bash
dewey init
dewey instructions set --file literature/research_question.md
```

## Step 3: Discover papers and log your searches

dewey manages papers; it does not find them. Use these tools:

**Semantic Scholar** (structured, machine-readable — preferred for systematic coverage):
```bash
python research_agent/skills/workflow-literature-review/scripts/semantic_scholar_search.py \
    "willingness to pay privacy" --limit 25 --format csv > literature/candidates.csv

# Filter by year
python research_agent/skills/workflow-literature-review/scripts/semantic_scholar_search.py \
    "conjoint analysis consumer preferences" --year-start 2015 --limit 25

# Snowball forward/backward from a key paper
python research_agent/skills/workflow-literature-review/scripts/semantic_scholar_search.py \
    --citations "10.1257/aer.20201073" --limit 30
python research_agent/skills/workflow-literature-review/scripts/semantic_scholar_search.py \
    --references "10.1257/aer.20201073" --limit 30
```

**WebSearch** (supplement for grey literature and preprints):
```
WebSearch: "{topic}" site:ssrn.com OR site:arxiv.org OR site:nber.org
WebSearch: "{construct}" validated scale measurement instrument
WebSearch: "{topic}" systematic review OR meta-analysis
```

If Semantic Scholar rate-limits or fails after its built-in retries, record the
failure once in the search log and switch search channels. Do not repeatedly run
the same failing query. Use WebSearch for discovery and Crossref, publisher,
DOI, NBER, SSRN, arXiv, or institutional pages to verify bibliographic metadata.

**Run at least 5 searches** from different angles: core topic, key constructs, methods, recent reviews, author snowballing.

**Log every search** in `literature/search_log.md` as you go:

```markdown
## Search log

| Date | Tool | Query | Filters | Results | Added to dewey |
|------|------|-------|---------|---------|----------------|
| 2026-04-09 | S2 | "willingness to pay privacy" | 2015-2026 | 25 | 12 |
| 2026-04-09 | WebSearch | "privacy valuation" site:nber.org | — | 8 | 4 |
```

This log makes the review reproducible and helps you avoid re-running the same search.

## Step 4: Abstract triage (screen before full ingestion)

Do a quick pass over all candidates before adding them to dewey. For each candidate, read the title and abstract and apply your inclusion criteria from Step 1.

- **Pass**: clearly meets criteria → add to dewey
- **Maybe**: unclear from abstract → add to dewey, flag with `dewey state set src_<id> queued` and low priority
- **Fail**: clearly excluded → don't add, or add with `excluded` status if you want a record

Aim to reduce 30-50 candidates to 15-25 for full reading. If you end up with fewer than 10 passing, broaden your search before proceeding.

## Step 5: Add screened papers to dewey

Add each passing candidate as a `.bib` file for metadata, then retrieve readable
full text for every source that will support substantive claims. Prefer Dewey's
URL ingestion, which uses Firecrawl to store clean Markdown; use a PDF when a
public full-text URL is unavailable:

```bash
# From a .bib file
dewey add source literature/sources/paper.bib

# From a public paper or publisher URL (Firecrawl → stored Markdown)
dewey add source "https://example.org/paper"
# Then replace the generated placeholder fields with verified metadata:
dewey bib edit src_<id> --field title --value "..." --field author --value "..."

# From a PDF
dewey add source literature/pdfs/paper.pdf
```

**After adding a PDF**, always complete the placeholder BibTeX immediately — placeholder entries degrade search quality:
```bash
dewey bib show src_<id>
dewey bib edit src_<id> \
    --field title  --value "..." \
    --field author --value "Last, First and Last, First" \
    --field year   --value "2021" \
    --field journal --value "American Economic Review"
```

Check status anytime:
```bash
dewey status
dewey list --status unread
```

## Step 6: Read, appraise, and annotate

Work through sources systematically. For each paper:

```bash
dewey state set src_<id> reading
dewey cat src_<id>          # read stored Markdown if available
dewey path src_<id> --pdf   # local-only fallback
```

Do not infer a paper's methods, results, or limitations from bibliographic
metadata or a search-result snippet. Abstracts are sufficient only for triage.
For an included paper, read stored Markdown or the PDF before writing substantive
notes. If full text cannot be retrieved, keep the source queued or exclude it as
`unavailable-full-text`; do not silently promote it to read.

Write notes using this template. Consistency across papers makes synthesis much easier:

```bash
dewey notes edit src_<id> --append "## Research question
[What does this paper ask?]

## Design and sample
[Method: RCT / survey / field experiment / observational. n=. Population.]

## Key constructs and measures
[What was measured? Validated scale? Which one?]

## Main findings
[Key results with effect sizes where available, e.g. β=0.12, d=0.4, OR=1.8]

## Study quality
[Strengths: pre-registered? Large n? Causal identification?]
[Weaknesses: self-report? convenience sample? short follow-up? demand effects?]

## Relevance to our study
[How does this inform our design, constructs, or expected effects?]"
```

Mark inclusion status after reading. Declare the evidence depth explicitly:
```bash
dewey state mark-read src_<id> --depth full-text
dewey state set src_<id> included   # or: excluded
```

Use `--depth abstract` only for screening records. Abstract-only sources may be
described as screened, not reviewed, and must not support detailed findings or
effect-size claims.

For excluded papers, consider noting why in the notes — it helps if the exclusion is later questioned.

## Step 7: Link papers

Record relationships between papers to make the knowledge graph explicit:

```bash
dewey link add src_<B> src_<A> --type builds_on --note "Extends WTP framing to digital goods"
dewey link add src_<C> src_<A> --type contradicts --note "No privacy premium in EU context"
dewey link add src_<D> src_<A> --type uses_method --note "Same Van Westendorp scale"
dewey link list src_<id>
```

Link types: `builds_on`, `contradicts`, `compares_to`, `uses_method`, `uses_dataset`, `motivates`, `historical_predecessor`, `same_work_as`, `version_of`.

## Step 8: Set review order

Arrange included sources in narrative order — typically foundational theory first, then methodological precedents, then substantive empirical work, then recent updates:

```bash
dewey order set src_<theory> src_<method> src_<empirical1> src_<empirical2> src_<recent>
dewey order add src_<id> --after src_<other>
```

## Step 9: Search your corpus for themes

Before writing, use local search to surface cross-cutting patterns:

```bash
dewey search --notes "validated scale"    # which papers used established instruments?
dewey search --notes "effect size"        # gather quantitative benchmarks
dewey search --status included            # confirm your final set
dewey search --linked-to src_<id>         # what depends on a key paper?
```

## Step 10: Synthesize — write the review

Pull all included notes into `literature/review.md`. The goal is a narrative that goes beyond "Paper A found X; Paper B found Y" — identify patterns, explain contradictions, and build toward your study's contribution.

Label the evidence precisely in the synthesis and final report. Reserve phrases
such as "papers reviewed" for full-text-read sources. Report abstract-only items
as screened leads, and separate direct evidence about the target intervention
from contextual evidence about adjacent infrastructure or markets. Do not merge
effect sizes from materially different interventions into a single range unless
the comparison and its limitations are explicit.

```bash
dewey list --status included --json    # get the full included set
dewey notes show src_<id>              # read each paper's notes in order
dewey link list src_<id>               # check relationships before writing each section
```

```markdown
# Literature Review: {Research Question}

## Overview
{3-4 sentences: what the literature establishes with confidence, where findings
diverge, and what gap motivates the current study. Lead with the consensus,
then the fault lines.}

## Key Themes

### Theme 1: {name}
{Synthesize — don't just list. Explain why papers agree or disagree.
Note when conflicts are explained by design differences (population, measure, context).}
- Author A (Year, Journal): finding [effect size]; note any design limitations
- Author B (Year, Journal): finding [effect size]; contrast with A if relevant

### Theme 2: {name}
...

## Methodological Landscape
{What study designs have been used? What sample sizes are typical?
What validated scales exist for the core constructs?
What causal identification strategies have been used?
What populations are over- or under-studied?}

## Evidence Quality
{Assess the overall strength of evidence: How many studies are there?
Are they mostly correlational or experimental? Are key findings replicated?
Are there pre-registered studies? What are the dominant limitations?}

## Gaps and Contribution
{What hasn't been studied? Where do findings conflict without resolution?
How does the current study address one of these gaps specifically?}

## Implications for Study Design
- Core constructs to measure (cite the validated scale if one exists)
- Expected effect sizes / base rates from prior work
- Confounds to control (cite the paper that identifies each)
- Recommended analysis approach (with precedent)
- Sample size: what n did comparable studies use?

## References
```

Export BibTeX for all included sources:
```bash
dewey list --status included --json | python3 -c "
import json, sys, subprocess
for s in json.load(sys.stdin)['sources']:
    subprocess.run(['dewey', 'cite', s['source_id'], '--format', 'bibtex'])
"
```

## Step 11: Validate and connect to study design

```bash
dewey doctor    # integrity check
dewey status    # final counts — confirm all included sources are read
```

Before claiming completion, verify that every included source has
`read_depth=full-text` and a stored PDF or ready Markdown. If not, narrow the
report to the evidence actually read or clearly label it an abstract-level
scoping review.

After the review:
1. **Inform `plan.md`** — cite literature to justify every major design choice
2. **Adopt validated measures** — use established scales; note if you adapt them
3. **Set priors** — document expected effect sizes and base rates from comparable studies
4. **Identify controls** — include covariates the literature identifies as confounds

## Stopping criteria

Stop searching when new searches return mostly papers already in your corpus (saturation). In practice: if 2-3 consecutive searches across different query strategies yield fewer than 1-2 new papers that pass inclusion criteria, you have likely achieved good coverage. Document the stopping point in the search log.

## File layout

```
study_root/
  .dewey/                        # dewey bibliography database
  literature/
    research_question.md         # research question + inclusion/exclusion criteria
    search_log.md                # log of all searches run
    candidates.csv               # raw Semantic Scholar output
    review.md                    # synthesized literature review
    sources/                     # .bib files
    pdfs/                        # PDF files
  plan.md
```

## Tips

- **Define criteria before you search**, not after — post-hoc criteria selection biases toward papers that confirm your hypothesis.
- **Log every search** — future-you and collaborators need to know what was covered.
- **Triage abstracts first** — don't add every candidate to dewey; screen first, read later.
- **Notes are your review draft** — write them with synthesis in mind; consistent structure across papers makes Step 10 assembly rather than writing from scratch.
- **Prioritize study design over citation count** — a pre-registered RCT with 300 citations beats a correlational study with 3,000.
- **Name the gap explicitly** — the best reviews don't just describe the literature, they identify what's missing and explain why the current study addresses it.
- **Snowball aggressively** — `--citations` / `--references` in the S2 script often surfaces key papers that keyword search misses.
