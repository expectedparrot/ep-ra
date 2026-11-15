---
name: post-run-review
description: Mandatory results quality review after every study run and before first analysis of reopened results. Re-examine user inputs, study design, and results for gaps, weaknesses, and improvement opportunities. Present a structured written assessment to the user with ranked suggestions before proceeding. Use whenever a survey, simulation, or labeling run completes, or when beginning analysis of an existing results file that has not yet been reviewed.
tags: [workflow, quality-check, validation]
---

# Post-Run Review

For partial results, job error histories, or an explicitly requested interactive
Results transcript view, use the
[execution reference](../edsl-surveys/references/execution-and-recovery.md).
A saved artifact or zero exit code alone does not establish full completion.

After every survey or simulation run, perform a proportional review before
analysis. The review is mandatory; a long critique and an extra user decision
are not. Its purpose is to catch material execution or design problems without
turning a clean routine study into another research project.

## Fast path for small, clean studies

Use this path when the study has at most 20 result rows and 3 questions, the
planned validation passes, and the approved plan already calls for a report.

1. Run the scaffold-owned batch once: `make -C <absolute-root> post-run`. Set
   `REPORT_GROUP_BY=agent.<trait>` only when the approved analysis requires one
   primary segment comparison.
2. Use `data/report-data.json` plus the owned CSV/JSON exports. Do not issue additional `ep results` queries, embed all responses in inline Python, or
   load another diagnostic skill unless a concrete anomaly requires it.
3. Compare the bounded evidence with the approved plan. Record a concise
   internal assessment: invariant status, any material mismatch, and one honest
   limitation. Do not present the full review template below.
4. If there is no execution gap or high-severity concern, continue directly to
   the already-approved report. Do not ask “write the report or revise?” and do
   not solicit optional scope expansion before completing it.
5. If there is an execution gap, repair it without rerunning paid inference
   unless inference itself is invalid. If there is a high-severity improvement
   opportunity that would change the approved design or spend, present only
   that concrete decision and wait.

The full four-layer review below is for pilots, larger or complex studies,
reopened results with unclear provenance, and runs whose fast-path evidence
shows a material anomaly.

## Pilot mode vs. full-run mode

This review applies after both pilot runs and full study runs, but with a
different mandate in each case.

**Pilot mode** — the primary question is: *is the design ready for a full run?*
The review should produce a written critique AND a recommended next step: run
another pilot with changes, proceed to the full run, or stop and discuss. Do not
present a pilot review as mere reassurance — if the design has problems, say so
and propose specific fixes. Multiple pilots are normal and expected.

A recommendation to proceed is not execution authority. If the researcher asks
to analyze, summarize, or report the pilot, work only from its saved Results.
Never build or launch the full run as a side effect. Before any full run, show
the full run's own exact estimate in a separate `AskUserQuestion`, ask whether
to run that specific package, and stop for a fresh affirmative answer. Pilot,
plan, design-change, analysis, and report approvals do not count.

For each gap or problem identified, provide all three of the following or do not
raise it:

1. **The specific observation** — a concrete finding from these results, not a
   general statement. "Free-text responses were thin" is not enough. "8 of 10
   agents opened their answer to Q4 with 'As a [persona]...' and gave
   near-identical two-sentence responses" is.
2. **Why it matters** — what it affects: the validity of findings, coverage of
   key segments, usefulness of the data for the user's stated goal.
3. **The proposed fix, written out in full** — the actual revised question text,
   the rewritten agent trait, the new scenario wording. "Consider revising Q3"
   is not a proposed fix. "Rewrite Q3 as: [verbatim new text]" is.

After presenting findings and proposed changes to the user:

1. Wait for the user to approve the specific changes.
2. Implement the approved changes — rewrite the questions, revise agent
   instructions, adjust the design.
3. Update `plan.md` to reflect the approved changes.
4. Show the user a brief summary of every change made.
5. Only then propose running the next pilot.

Do not propose running another pilot on an unchanged design. It will produce the
same problems and waste the user's time and money.

**Full-run mode** — the primary question is: *do the results answer the user's
goals, and what are the gaps?* Follow all four layers below. Present findings
before analysis begins.

In both cases: load this skill explicitly via the Skill tool at the moment the
run completes. Do not rely on memory of having read it earlier in the session.

## The fundamental distinction: execution gaps vs. improvement opportunities

Every finding from the review falls into one of two categories. How you respond depends on which it is.

**Execution gaps** — things that were already approved in the plan but were not correctly carried out. The user asked for something; you did not deliver it. Examples: a segment specified in the plan was not included in the agent list; a question was approved but silently reworded; data the user provided was not fully used as inputs; a scenario condition described in the plan was omitted from the run.

→ **Fix these immediately, without asking.** The user already approved them. Do not present an execution gap as a choice — correct it and note what was fixed in the review output.

**Improvement opportunities** — things that would make the study better or larger, but go beyond what was approved. These include: new segments or personas not in the original plan, additional questions, different question framing, an expanded dataset, a new comparison condition, a different model, scope extensions suggested by what the results revealed.

→ **Present these clearly and seek user approval.** Do not act on them unilaterally. The user may have constraints you don't know about, or they may simply not want to spend more time or money. Lay them out, rank them, and let the user decide.

When in doubt about which category something falls into: if fixing it requires spending more credits or running new code not in the approved plan, treat it as an improvement opportunity and ask.

---

## When to run this

Run this review immediately after:
- `ep run` completes successfully and the Results artifact is saved
- A Concordia simulation completes and logs are saved
- A labeled dataset is returned from a data-labeling run

Do not wait until after analysis or reporting. The review informs what analysis to run and whether the study needs to be revised first.

If the scaffold-owned post-run command stops on QA, that failure triggers this
review; it does not authorize bypassing the phase with custom analysis. Preserve
the failed gate and diagnose it before computing substantive estimates.

Before a full review, get one bounded diagnostic without Python:

```bash
ep results review data/results.ep
```

The review includes schema, missingness, bounded distributions, representative
rows, and cost. Run targeted `select`, `values`, or `sample` commands only when
the review identifies a concrete question. Keep three states independent:
inference completion, artifact validation, and
optional inspection. If validation or inspection fails, preserve and report the
successful inference state. Never rerun paid inference to repair a preview,
column selection, export, analysis, or presentation failure.

For interview Results, reuse the runner's working extraction code or the
named-transcript exporter in **skill:methods-ai-interview**. Its transcript
inspection reference documents the native schema and flattened column names;
use it for sample interviews and report appendices before trying schema guesses.

---

## What to review

Work through each of these layers in order. Not every item will apply to every study — use judgment, but be thorough. When in doubt, include the check.

---

### Layer 1: Re-examine the user's original inputs

Go back to what the user actually gave you before this study began. This includes:

- The original request (re-read it)
- Any data or files the user uploaded or referenced (re-read them if available)
- Any constraints, goals, or context they stated in the conversation
- The plan you proposed and they approved

Ask: **Does what we built actually answer what they asked?**

Specific checks:
- Did the research question get answered, or did the study circle around it without hitting the core?
- Were all the populations, segments, or conditions the user cared about included?
- If the user provided a CSV, set of quotes, prior study results, or other inputs: did the study design make full use of that material, or did it use only part of it?
- Were any constraints (budget, scope, audience) respected, and did those constraints cause any meaningful gaps?
- Did implementation substitute a different data source, synthetic data,
  population, model, or method from the approved plan? Surface even a disclosed
  substitution before analysis. A convenient replacement is protocol drift,
  not a mechanical implementation detail.
- If the user stated a goal ("I want to understand why customers churn"), does the study actually produce evidence bearing on that goal, or does it answer an adjacent question?

Write down any mismatches between what was asked and what was built.

---

### Layer 2: Review the study design

Evaluate the design choices made in the plan — agents, survey instrument, scenarios, model — against what the results actually needed.

#### Agent coverage
- Were all relevant segments or persona types represented? Are there obvious groups missing — demographic, attitudinal, behavioral — that would change the conclusions?
- Were the agent trait dimensions the right ones? Did varying those dimensions produce meaningful response differences? If two dimensions produced nearly identical response patterns, one of them may have been the wrong axis.
- Was the agent count sufficient? Could the main comparisons have been made with confidence, or were there cells with only 1–2 agents where the comparison is too thin to trust?
- Did the agent instruction strings produce genuine persona differentiation, or did most agents sound like the same voice with slightly different labels? (Check free-text responses for this.)

#### Survey or scenario design
- Did every question contribute to the analysis? Were there questions that produced no useful variation — everyone answered the same way — that could be cut or rewritten?
- Were there important questions that were not asked? Things a thoughtful analyst would want to know that the current instrument does not address?
- Was question order appropriate? Could any question have primed or anchored the response to a later one?
- For scale questions: were there floor or ceiling effects (responses piled at one end of the scale)?
- For multiple-choice questions: did any options go almost entirely unchosen, suggesting they were poor distractors or the concept was misframed?
- For free-text questions: were the responses substantive and varied, or did agents produce near-identical boilerplate? Run the homogeneity detection script from `research_agent/skills/free-text-homogeneity/SKILL.md` and record opener rates and shared-prefix findings. If >30% of responses share a common opener or structural template, flag this as a finding in the review. Suggest specific mitigations: adding `answering_instructions` to the question, rewriting generic question prompts as specific/concrete ones, or adding voice/style guidance to agent instructions. See that skill for the full mitigation menu. Even if homogeneity is low, note what was found — the user should know before the report is written.
- For simulation studies: did the scenario activate the intended dynamics? Did agents engage meaningfully, or did episodes end prematurely or loop without resolution?

#### Model performance
- Did the model produce responses at the quality level the study required?
- For free-text questions: were the open-ended responses specific, persona-consistent, and informative — or thin and generic?
- For scale questions: did the model seem to be anchoring to the middle of the scale systematically (acquiescence bias)?
- If a pilot was run: did the full run match the pilot quality, or did quality degrade at scale?

---

### Layer 3: Review the results themselves

Read the actual results before drawing conclusions.

#### Differentiation
- Did agents with different traits actually respond differently? If conservative and liberal agents gave the same answers on political questions, something is broken upstream — either the agent construction, the question wording, or both. Flag any dimension that failed to differentiate.
- Was the pattern of differentiation meaningful, or did it look like noise? (E.g., "technical" agents rated technical confidence slightly higher but only by 0.2 points on a 7-point scale — is that real?)

#### Surprising or anomalous findings
- Were there any results that went against your expectation given the agent design? Do not paper over these. Surface them — they are either genuinely interesting or signs of a design problem.
- Were there any results that seem implausibly extreme (every agent giving the same extreme response) or implausibly uniform (no variation at all)?
- Were there any results that suggest the question was misunderstood or the scenario was interpreted differently than intended?

#### Coverage gaps
- Are there important comparisons the current data cannot support? E.g., the study compared segment A vs. B, but not A vs. C — and C might be the most important comparison for the user's goal.
- Are there subgroup analyses that would be revealing but require more agents to be credible?

#### Data quality
- Were there any missing, malformed, or incomplete responses? How many, and do they cluster in any particular agent or question?
- Did any questions return empty strings or non-answers at a rate that suggests a prompt engineering problem?

#### Comparable support
- For every comparison across models, groups, scenarios, or conditions, do the
  compared estimates use the same required questions/items and observations?
- Differential missingness is part of the result, not permission to compare
  whatever subsets remain. Fewer observations or logical constraints can make
  a model appear artificially better.
- Restore completeness through an approved retry when possible. Otherwise use
  an explicitly defined common-support intersection and report both coverage
  and sensitivity. If neither supports the planned estimand, stop that
  comparison and describe it as unsupported.
- Never call unequal-support estimates directly comparable, use their ratio as
  a headline result, or claim a model ranking from them.

---

### Layer 4: Scope expansion — what this study could grow into

Based on everything above, identify the most valuable directions for expanding or improving the study. These are not problems — they are opportunities. Be specific.

For each suggestion, state:
1. What the gap or opportunity is
2. What specifically would be added or changed
3. What new insight it would produce that the current study cannot
4. Approximate cost or effort increase (even a rough sense: "small", "similar cost", "2x cost")

Examples of the kind of suggestion to make:
- "The study only asked how satisfied agents are — a follow-up question asking *why* they are dissatisfied would let us move from a score to a cause."
- "All agents are US-based. If this product is also sold in the EU, adding 8–10 EU-market personas would reveal whether the purchase barrier pattern holds cross-market."
- "The current scenario describes the product as already purchased. A pre-purchase scenario — where agents are deciding whether to buy — might reveal very different objections."
- "The free-text responses for Q7 (biggest concern) were thin. Running Q7 with a higher-tier model, or adding a follow-up probing question, would produce richer qualitative data."
- "The study treats price sensitivity as a fixed trait. A conjoint design varying actual price points would reveal the willingness-to-pay threshold more precisely."
- "You provided a CSV of 200 customer complaint tickets. Only 20 were used as scenarios. Running the full 200 would give a more complete picture of the complaint distribution."

Include at least 2–3 scope expansion suggestions in every review. More is better if the material warrants it.

---

## Format for presenting findings to the user

After completing the review — and after silently fixing any execution gaps — write a structured assessment and present it to the user. Do not bury the lead — start with the most important finding.

Use this structure:

---

**Post-run review: [Study name or short description]**

**Overall assessment:** [One sentence: e.g., "The study answered the core question well but has three significant design gaps worth addressing before reporting."]

**What worked**
- [2–4 specific things the design got right — not boilerplate praise, specific observations about this study]

**Execution gaps fixed**

List anything that was in the approved plan but was not correctly executed, and note what was corrected. If nothing was found, omit this section entirely.

- [e.g., "The plan specified a 25–34 age segment that was missing from the agent list — added 4 agents and rerun."]
- [e.g., "Three agents returned empty responses on Q8 — reran those agents."]

**Findings and improvement opportunities**

| # | Layer | Finding | Severity | Type |
|---|-------|---------|----------|------|
| 1 | Results | [e.g., "Conservative and liberal agents gave nearly identical answers on Q3 — the question may not be activating the political dimension"] | High | Improvement opportunity |
| 2 | Inputs | [e.g., "You provided a transcript of 5 customer interviews — only the first two were reflected in the agent design; the other three raised distinct concerns not tested"] | High | Improvement opportunity |
| 3 | Design | [e.g., "Q5 had a ceiling effect — 92% of agents chose the top option"] | Medium | Improvement opportunity |
| 4 | Design | [e.g., "Free-text Q7 responses: 40% share a common opener — low persona differentiation"] | Medium | Improvement opportunity |

Severity: **High** = affects the validity or usefulness of findings; **Medium** = limits scope or nuance; **Low** = cosmetic or minor.
Type: **Execution gap** (already fixed) or **Improvement opportunity** (awaiting your decision).

**Suggestions for revision or follow-up**

Ranked by value. These all require your approval before action.

1. **[Suggestion title]** — [What to do and why. What insight it unlocks. Rough cost/effort.]
2. **[Suggestion title]** — [Same.]
3. **[Suggestion title]** — [Same.]
[Add more as warranted]

**Recommended next step**
[One of: "Proceed to analysis as-is", "Minor revision before analysis", "Rerun with specific changes before reporting", "Significant redesign recommended"]

---

For a full review, then ask the user:

> How would you like to proceed? Options: [list the top 2–3 specific actions from the suggestions], or proceed to analysis and report as-is.

Wait for the user's response before doing anything further.

---

## Rules

1. **This review is mandatory and proportional.** Use the fast path when its
   criteria hold; reserve the full template and user pause for material risk.

2. **Fix execution gaps immediately; seek approval for improvements.** If the review finds something that was in the approved plan but not correctly executed, fix it now without asking — the user already asked for it. If the review finds ways to make the study better that go beyond the approved plan, present them clearly and wait for approval. Do not conflate these two categories. Do not ask the user to approve something they already approved.

3. **Be honest about weaknesses.** The purpose of the review is not to reassure the user that the study was good. If something is genuinely problematic, say so clearly and early.

4. **Distinguish design problems from result findings.** A floor effect on Q5 is a design problem. An unexpected finding that conservative agents prefer the premium option is a result finding. Both belong in the review but under different headings.

5. **Re-read user inputs.** Do not rely on memory of what the user said. If they uploaded a file, re-read it. If they gave you a brief or context at the start of the session, go back and re-read it. The most common gap is a mismatch between what the user actually cared about and what the study measured.

6. **Scope expansion suggestions must be specific.** "Consider adding more agents" is not a suggestion. "Add 8 agents representing the 25–34 age group, split across price-sensitive and brand-loyal, at an estimated cost of ~$1.20" is a suggestion.

7. **Present findings before analysis.** If the study has high-severity improvement opportunities, the user may want to act on them before investing in full analysis and a report. Give them that choice explicitly.
