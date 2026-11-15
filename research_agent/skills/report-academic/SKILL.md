---
name: report-academic
description: >
  Writes a complete, self-contained academic paper following discipline-specific
  conventions. Use when the user wants to produce a research paper, journal
  submission, or academic write-up. Asks whether the paper follows economics,
  management/organization science, or computer science conventions, then guides
  structure, tone, and section content accordingly. Includes literature review
  guidance and ensures all referenced prior work is described in full within
  the paper itself.
tags: [report, academic, workflow]
---

# Academic Paper Writing

This skill guides the production of a complete academic paper. Before writing
anything, you must confirm the discipline and paper parameters. The discipline
determines structure, style, and section conventions.

---

## Step 1: Confirm discipline and paper parameters

Ask the user three questions (combine into one message):

1. **Discipline** — economics, management/organization science, or computer
   science? If another field, name it — the conventions will be adapted.
2. **Research question** — what is the central question or contribution?
3. **Audience and venue** — is this for a specific journal, conference, or
   course? Target venue shapes length, style, and emphasis.

Example prompt to the user:

> "Before I start: which discipline should I follow — economics, management /
> organization science, or computer science? And what is the core research
> question or contribution? If you have a target journal or conference in mind,
> mention it — that will shape the length and framing."

Do not begin drafting until you have answers to all three.

---

## Step 2: Confirm the section structure for the chosen discipline

Present the planned section structure and wait for confirmation before writing.

### Economics

Standard structure for empirical or theoretical economics papers:

1. Abstract (150–200 words; structured around question, method, and findings)
2. Introduction (3–5 pages; motivate, state contribution, preview findings)
3. Related Literature
4. Model or Theoretical Framework *(omit if purely empirical)*
5. Data and Methodology
6. Results
7. Robustness Checks and Extensions *(may be a subsection of Results)*
8. Discussion
9. Conclusion
10. Appendices (proofs, additional tables, robustness output)

Key conventions:
- Introduction carries the weight: state the contribution explicitly and early.
  ("This paper makes three contributions…")
- Literature review is typically brief (1–2 pages) and positioned after the
  introduction, framed around how this paper *differs* from prior work, not
  just what prior work found.
- Results section is highly structured: each finding gets its own subsection
  with a table, coefficient interpretation, and an economic magnitude statement.
- Avoid "we believe" or "we feel"; use "we find", "the results suggest",
  "the estimates indicate".

### Management / Organization Science

Standard structure for empirical management papers (AMJ, ASQ, Strategic Management Journal style):

1. Abstract (150–250 words; problem, theory, sample, key finding)
2. Introduction (motivate gap, state theoretical contribution, preview hypotheses)
3. Theoretical Background and Hypotheses
4. Methods (Data and Sample; Measures; Analytic Strategy)
5. Results
6. Discussion (summary of findings, theoretical contributions, practical
   implications, limitations, future research)
7. Conclusion *(sometimes merged into Discussion)*
8. Appendices (measurement items, robustness, additional analyses)

Key conventions:
- Theory section is prominent and comes before methods. Hypotheses are stated
  formally and numbered (H1, H2, …).
- Methods section describes each variable in detail including operationalization
  and source.
- Discussion section explicitly revisits each hypothesis and states whether it
  was supported.
- Use hedged language for contributions: "This study contributes to…",
  "The findings extend…", "We suggest that…"

### Computer Science

Standard structure for systems, ML, or empirical CS papers (NeurIPS, ICML, ACL, USENIX style):

1. Abstract (100–200 words; problem, approach, key result, significance)
2. Introduction (motivation, problem statement, bulleted list of contributions,
   paper organization)
3. Related Work (or Background)
4. Approach / Method / System Design
5. Experimental Setup (datasets, baselines, metrics, implementation details)
6. Results and Analysis
7. Discussion and Limitations
8. Conclusion
9. References
10. Appendix (proofs, extended results, implementation details)

Key conventions:
- Contributions are listed explicitly and concisely in the Introduction, often
  as bullets. ("Our main contributions are: (1)… (2)… (3)…")
- Related Work may appear after the Introduction or near the end; ask the user.
- Results section uses tables and figures as primary carriers of information;
  prose interprets them.
- Algorithm boxes, pseudocode, or system diagrams are standard.
- Concise, precise, and direct prose. Avoid rhetorical framing.

---

## Step 3: Literature review — self-contained rule

**The paper must be entirely self-contained. Do not cite a study without
describing it.**

This is the core constraint that governs how prior work is handled:

- If a prior study is important enough to mention, describe it in the body of
  the paper. Do not assume the reader will fetch it.
- For each study that matters to the argument, include: what question the study
  addressed, what method or data it used, what it found, and why it is relevant
  to the current paper.
- If a study is only tangentially related, a two-sentence summary is enough.
  If it is central — a direct predecessor, a competing finding, or the primary
  theoretical foundation — give it a full paragraph.
- Construct descriptions from first principles based on the topic. Do not
  fabricate author names, journals, or results. If the user provides source
  material, draw from it. If not, describe what a representative study in that
  tradition would typically address and find, and mark the description as
  illustrative.
- Do not include a bibliography section that lists studies without describing
  them. Every study named in the text must be described where it is named.

### Conducting the literature review

Before writing the literature review section, do the following:

1. **Identify the core intellectual lineage.** What are the two or three
   streams of prior work that this paper sits within or responds to?
2. **Identify the gap.** What does prior work leave unresolved, and how does
   this paper address it?
3. **For each stream:** describe the central question that stream addresses,
   the dominant methods used, the range of findings, and where consensus
   exists or is contested.
4. **For key studies within each stream:** provide a full description (see
   self-contained rule above).
5. **Close with the gap statement.** The final paragraph of the literature
   review should state clearly what is missing from prior work and why this
   paper fills it.

Ask the user before writing the literature review:

> "For the literature review, I'll describe the key prior studies in full
> within the text rather than just citing them. Do you have specific studies
> or research streams you want covered? If so, share any source material
> and I'll draw from it. If not, I'll construct descriptions of representative
> work in the area."

---

## Step 4: Write each section

Write sections in order, one at a time. After each major section, pause and
ask the user if they want to adjust before proceeding. For long papers (10+
pages), do not write the entire draft in one pass.

### Abstract

Write last, but placeholder early. The abstract is a standalone summary:
four to six sentences covering (1) the problem, (2) the approach or data,
(3) the key finding, and (4) the implication or contribution. Do not introduce
content not in the paper.

### Introduction

The introduction has three jobs:
1. Motivate the question — why does it matter and to whom?
2. State the contribution — what does this paper do that prior work does not?
3. Preview the structure and findings — give the reader a map.

For economics and CS papers, the contribution statement should be explicit
("this paper makes the following contributions"). For management papers, it
is typically woven into the prose rather than bulleted.

Do not end the introduction with "the rest of the paper is organized as
follows" as the only structural signal — include the preview of findings there.

### Methodology

This section must be detailed enough for replication. Include:

- Data sources, collection method, and sample construction
- Variable definitions and operationalization
- Identification strategy or estimation approach (economics)
- Model architecture and training details (CS/ML)
- Hypothesis-to-measure mapping (management)
- Any robustness or sensitivity choices made in advance

Write methods before results. Do not blend findings into the methods section.

### Results

Present results in a logical order, not the order the analysis was run.
Lead each subsection with the finding, then support it with statistics,
tables, or figures. Interpret every number — do not leave tables to speak
for themselves.

For every primary finding, address:
- What the result is
- Whether it is statistically and practically significant
- How it relates to the hypothesis or research question
- Any caveats or boundary conditions

### Discussion

The discussion interprets the findings in relation to the broader literature.
Structure it as:
1. Summary of main findings
2. Theoretical contributions — what does this add to the literature streams
   described in the literature review?
3. Practical or policy implications
4. Limitations — be candid; list real limitations, not boilerplate
5. Future research directions

### Conclusion

One to two pages. Restate the core question, summarize the findings and their
significance, and close with the broader implication. Do not introduce new
results or evidence in the conclusion.

---

## Step 5: Tone and style by discipline

| Dimension          | Economics         | Management          | Computer Science    |
|--------------------|-------------------|---------------------|---------------------|
| Voice              | Analytical, direct | Hedged, relational  | Precise, concise    |
| Hedging            | Minimal            | Moderate            | Minimal             |
| Contribution claim | Explicit, early    | Embedded in prose   | Bulleted list       |
| Theory prominence  | Varies             | High                | Low–medium          |
| Stat presentation  | Coefficients, SEs  | Betas, p-values     | Metrics, benchmarks |
| Figures/tables     | Tables dominant    | Mixed               | Figures dominant    |
| Passive voice      | Acceptable         | Discouraged         | Common for methods  |
| Length             | 30–50 pages        | 30–50 pages         | 8–15 pages          |

Regardless of discipline:
- Use precise language. Never use vague terms like "many", "several", or
  "a lot" when a number or qualifier is available.
- Define every technical term on first use.
- Avoid rhetorical questions.
- Every claim requires either a logical derivation, empirical evidence, or
  an in-text description of a study that supports it.

---

## Step 6: Quality checks before finalizing

Before declaring the paper complete, verify:

- [ ] Abstract accurately reflects the paper's content
- [ ] Every study mentioned is described in full within the text
- [ ] Contribution is stated clearly and early in the Introduction
- [ ] Methods section contains enough detail for replication
- [ ] Every result is interpreted — no bare tables
- [ ] Discussion connects findings back to literature streams
- [ ] Limitations are candid, not boilerplate
- [ ] Conclusion does not introduce new material
- [ ] Section headings and structure match the agreed discipline conventions
- [ ] Tone is consistent throughout (no section-by-section voice shifts)

Run through this checklist explicitly and report results to the user before
delivering the final draft.
