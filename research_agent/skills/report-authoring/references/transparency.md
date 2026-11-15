# Report Transparency

## Contents

- Mandatory pre-writing gate
- Survey instrument
- Agent configuration
- Model rationale
- Verbatim responses
- Expected Parrot links
- Method explainer
- Visual standards
- Free-text homogeneity disclosure

Reports are not just summaries of findings. They are the primary way readers understand *what was done* — and for many readers, they are an introduction to how AI simulations work at all. A transparent report lets readers evaluate the methodology, reproduce the study, and learn from it.

This skill covers five requirements:

1. The survey instrument -- show the actual questions (if a survey was run)
2. The agent configuration -- show how agents were set up
3. The model rationale -- explain why this model was chosen and what that means for the results
4. Representative verbatim responses -- ground the analysis in what agents actually said
5. Expected Parrot links -- give readers direct access to the study objects you produced

A sixth element (a "How this study works" explainer) is recommended for any report that will be read by people unfamiliar with AI simulations.

---

## MANDATORY: Complete this gate before writing report.md

**Do not open `writeup/report.md` until every item below is checked.** This is the recurring failure mode: writing the report from analysis output alone, skipping structure and transparency requirements entirely.

Work through each item in order:

- [ ] **Compilation flags confirmed.** The Makefile compiles HTML with `--css=report.css --embed-resources --standalone` and PDF with `--pdf-engine=xelatex --include-in-header=report_header.tex --lua-filter=fix-table-widths.lua`. These files are created by `ep study scaffold` and must be used. Do not run bare `pandoc report.md -o report.pdf`.
- [ ] **Survey appendix generated.** Run the `write_survey_md()` snippet (see Section 1 below) to produce `writeup/survey.md` before writing the report. Incorporate or reference it from the Appendix section.
- [ ] **Agent table drafted.** Write out the agent configuration table (trait names, values, n per segment) before writing prose. This forces you to be explicit about what was built.
- [ ] **EP links in hand — OR a recorded local-only decision.** By default, push ALL objects — survey, agent list, scenario list, AND results — to Expected Parrot and record every URL before writing the Methods section. Do not write "links to be added" placeholders. See `research_agent/skills/edsl-object-publishing/SKILL.md` for the push pattern. The report must include a "Study objects on Expected Parrot" section with one link per published object. **Exception:** if the user explicitly declined publishing (a legitimate choice), this gate is satisfied without EP links — instead, note in Methods that the study objects are kept locally with the study files (reference the local audit trail), and omit the "Study objects on Expected Parrot" section. Do not push objects the user asked to keep private/local.
- [ ] **Verbatim quotes identified.** Pull at least 2-3 representative free-text responses per key question before writing the results narrative. Paste them into a scratch area. Do not write the narrative first and add quotes later -- quotes should shape the narrative, not decorate it.
- [ ] **Blockquote format confirmed.** Verbatim agent responses must appear as `>` blockquotes in report.md, attributed to the agent type. Do not embed them inline in prose paragraphs.
- [ ] **"Coop" scan.** Before compiling, run `grep -i coop writeup/report.md` and confirm zero matches. "Coop" must never appear in any report or client-facing deliverable. Use "Expected Parrot" everywhere.
- [ ] **Free-text homogeneity check.** If the study included free-text questions, run the opener/prefix detection from `research_agent/skills/free-text-homogeneity/SKILL.md` and record the results. Draft the Limitations disclosure before writing the report narrative (see Section 8 below).
- [ ] **Visual QA: bar chart labels.** Any bar chart with error bars must position value labels ABOVE the error bar top, not above the bar mean. Use `label_y = mean + 1.96 * sem + margin` (not `label_y = mean + margin`). Verify in the rendered PNG before compiling the PDF.

Only after all items are checked: open report.md and begin writing.

---

## 1. Survey Instrument

Every report must include the complete survey instrument: every question, its type, and its answer options or scale where applicable. Without this, readers cannot evaluate whether the questions were well-formed, leading, or appropriate for the research question.

**Where it goes:** Generate `writeup/survey.md` automatically after constructing the survey, and reference it from the report's Appendix. Alternatively, reproduce the instrument directly in an Appendix section of `report.md`.

**How to generate `writeup/survey.md` from EDSL:**

```python
def write_survey_md(survey, filepath):
    lines = ["# Survey Instrument\n\n"]
    for i, q in enumerate(survey.questions, 1):
        lines.append(f"## Question {i}: `{q.question_name}`\n\n")
        lines.append(f"**Type:** {q.question_type}  \n")
        lines.append(f"**Text:** {q.question_text}\n\n")
        if hasattr(q, "question_options") and q.question_options:
            lines.append("**Options:**\n\n")
            for opt in q.question_options:
                lines.append(f"- {opt}\n")
            lines.append("\n")
        if hasattr(q, "min_value") and q.min_value is not None:
            lines.append(f"**Scale:** {q.min_value} to {q.max_value}\n\n")
    with open(filepath, "w") as f:
        f.writelines(lines)

# Call immediately after building the survey
write_survey_md(survey, "writeup/survey.md")
```

**Reference it from the report Appendix:**

> Appendix A reproduces the complete survey instrument. Questions used a mix of Likert scales (1-7), multiple-choice, and free-text formats; see that section for full question wording.

Then in the Appendix, either include the text inline or embed the file with a pandoc `!include`. A brief sample entry:

> **Q3 (QuestionLinearScale):** "How satisfied are you with your current Netflix subscription?" (1 = Not at all satisfied, 7 = Extremely satisfied)

**Why this matters:** Question wording is everything in survey research. "How satisfied are you?" and "How often do you feel frustrated?" can measure the same construct differently. Readers cannot evaluate findings without seeing the exact questions.

---

## 2. Agent Configuration

The report must include a table showing how agents were defined. This is distinct from the distribution table -- it shows the *definition* of each agent type (what traits they had, what values, what instruction they received), not just how many of each type were created.

**Required: Agent Trait Table in the Methods section**

| Trait | Values used | Description |
|-------|-------------|-------------|
| `age_group` | Gen Z (18-26), Millennial (27-42), Gen X (43-58), Boomer (59-77) | Generational cohort (Pew Research definitions) |
| `price_sensitivity` | Low, Medium, High | Stated sensitivity to subscription price changes |
| `subscription_tier` | Standard with Ads, Standard, Premium | Current Netflix plan |

Every trait that appears in the EDSL `traits` dict must appear in this table. Do not omit traits because they seem obvious.

**The instruction string:** If agents were given an `instruction` parameter (the system-level persona prompt), include it in full or close paraphrase. This is often where persona conditioning happens and it is never obvious from the trait list alone.

Example:

> Agents were given the following instruction: "You are a US-based Netflix subscriber. Answer all questions from the perspective of your demographic profile and viewing habits. Be specific and realistic -- draw on experiences that someone with your background would plausibly have had."

**Why this matters:** Two studies can use the same trait names with completely different agent behavior depending on the instruction string. Readers need both to assess whether the persona conditioning was appropriate.

---

## 3. Model Rationale

The Methods section must explain *why* a particular model was chosen -- not just which model was used. This serves two purposes: it lets readers evaluate whether the model was appropriate, and it teaches them what model choice means for AI simulation quality.

**The rationale must cover three things:**

1. Which model(s) and exact version(s) were used
2. Why this model was appropriate for this specific task (complexity, persona depth, question types)
3. Whether a pilot spot-check confirmed response quality before the full run

**Good rationale (substantive):**

> All simulated respondents were run using GPT-5.2 (OpenAI). This Tier 1 model was selected because the study requires nuanced persona-conditioned reasoning: agents must maintain consistent demographic perspectives across 14 questions, including open-ended justifications where generic responses would undermine the findings. A pilot run of three agents confirmed substantive and persona-consistent responses before the full job was submitted. A cheaper Tier 2 model was evaluated but produced noticeably more generic free-text answers in the pilot.

**Acceptable rationale (lighter task):**

> We used Claude Sonnet 4.6 (Anthropic), a strong Tier 2 model, because the survey consisted primarily of rating scales and multiple-choice questions that do not require frontier-level reasoning depth. A pilot confirmed adequate response quality at this tier.

**What to avoid:**

<!-- lint-allow-model: illustrative example, not a model recommendation -->
Do not write: "We used GPT-4o for this study." This tells readers nothing about the reasoning or what it means for result quality.

**Cross-model studies:** State what comparison was intended (robustness check, provider comparison, publication credibility) and what it revealed. Where results converged, say so. Where they diverged, discuss why.

**Connecting model choice to result interpretation:** When model choice has implications for how results should be read (e.g., a Tier 2 model may produce less nuanced free-text), note this briefly in the Limitations section.

---

## 4. Verbatim Response Examples

Aggregate statistics (means, percentages, frequencies) are efficient but opaque. Readers cannot assess whether agent responses were realistic, whether persona conditioning worked, or whether free-text answers were thoughtful -- without seeing actual examples.

**Requirement:** Include at least 2-3 verbatim agent responses for:
- Each free-text question used in the main analysis
- Any result that might seem surprising or counterintuitive (verbatim responses help readers understand why)

**Where they go:** Inline in the results narrative is strongest. An Appendix section labeled "Sample Responses" is an acceptable alternative for longer instruments.

**How to extract from EDSL results:**

```python
# Sample responses for a specific question, by agent type
sample = (
    results
    .filter("agent.age_group == 'Gen Z'")
    .select("agent.age_group", "agent.price_sensitivity", "answer.q_main_reason")
    .to_pandas()
    .head(3)
)

# Or pull one response per agent type
for group in ["Gen Z", "Millennial", "Gen X", "Boomer"]:
    row = results.filter(f"agent.age_group == '{group}'").select("answer.q_main_reason").first()
    print(f"{group}: {row}")
```

**Format in the report (prose block):**

> To illustrate, here are representative responses to Q7 ("What is the main reason you would or would not switch to an ad-supported plan?"):
>
> **Gen Z, high price sensitivity:** "Honestly, four minutes of ads per hour is nothing if I'm saving $7 a month. I already skip ads on YouTube constantly -- it's just muscle memory at this point."
>
> **Gen X, low price sensitivity:** "I pay for the premium tier specifically to avoid this. Ads interrupt the experience. If I'm watching something I care about, I don't want to be pulled out of it."
>
> **Millennial, medium price sensitivity:** "It really depends on the show. For background viewing or reality TV I could tolerate it. For something I'm actually invested in, no."

> **NEVER start a blockquote line with `[square brackets]`.** Pandoc parses `> [text]: "..."` as a link reference definition, not as a blockquote — the line silently disappears from the rendered output. Use **bold** for attributions instead: `> **Agent type:** "quote text"`.

**Why this matters:** Verbatim responses let readers see what the model actually produced and form their own judgment about whether the persona conditioning was realistic and whether the responses carry genuine signal.

---

## 5. Expected Parrot Links

The Methods section should include links to the key study objects you produced on Expected Parrot. Which objects are relevant depends on the task -- a survey study will have a survey, agents, and results; an agent-list study may have only an agent list; a scenario study may have a scenario and results. Include whatever you actually produced and published.

**Where they go:** A dedicated "Study objects on Expected Parrot" paragraph or small table in the Methods section, immediately after the model rationale.

**Common object types and when to publish:**

| Object | When to publish | Link label |
|---|---|---|
| Survey | After building, before running | "Survey (Expected Parrot)" |
| AgentList | After building, before running | "Agent panel (Expected Parrot)" |
| Scenario / ScenarioList | After building, before running | "Scenarios (Expected Parrot)" |
| Results | After the job completes | "Full results (Expected Parrot)" |

**Formatting:** Always use markdown links with short descriptive text — never paste bare URLs into the report. Bare URLs are long and break across lines in PDF output, creating broken hyperlinks.

**Example Methods paragraph:**

> The study objects are available on Expected Parrot:
>
> - [Survey](https://www.expectedparrot.com/content/...)
> - [Agent panel (30 agents)](https://www.expectedparrot.com/content/...)
> - [Results](https://www.expectedparrot.com/content/...)

**When to publish Results:** After `make data` creates `data/results.ep`, run
`ep push data/results.ep --alias <meaningful-alias> --description "..."
--visibility <confirmed-visibility>`, capture the returned URL, and record it in
the report.

**Why this matters:** Without links to the published objects, a report about an AI simulation study is not reproducible. The study objects are all opaque to the reader. Links make the study auditable and let future studies build on the objects directly.

---

## 6. "How this study works" explainer (recommended)

For any report that will be read by people unfamiliar with AI simulations, include a brief explainer near the top of the Methods section. This is particularly important for client deliverables and anything shared externally.

**Template text (customize as needed):**

> This study uses AI agent simulation -- a methodology in which large language models (LLMs) are configured with demographic and attitudinal traits and asked to respond to survey questions from the perspective of those personas. Each "agent" is not a real person but a language model prompted to reason and respond as someone with a specific profile (e.g., a 28-year-old Millennial with medium price sensitivity who currently subscribes to Netflix's Standard tier). This approach, sometimes called "homo silicus" simulation (Horton, 2023; Argyle et al., 2023), enables rapid exploration of how different demographic groups might respond to a product or policy -- while acknowledging that AI-simulated responses are not a substitute for real human data. The relationship between AI simulation results and actual human survey results is discussed in the Limitations section.

Omit this if the reader is clearly already familiar with the methodology.

---

---

## 7. Visual standards for plots

These rules apply to every chart produced for a report. They exist because errors in chart rendering are easy to miss in code review and embarrassing in client presentations.

### Bar charts with error bars

**Do not position value labels above the bar mean when error bars are present.** The error bar extends above the mean; a label at `mean + margin` will appear inside or overlapping the error bar cap, making both hard to read.

**Correct pattern:**
```python
# Always clear the error bar top, not just the bar top
label_y = row["mean"] + row["sem"] * 1.96 + 0.12
ax.text(i, label_y, f"{row['mean']:.2f}", ha="center", va="bottom", ...)
```

**Wrong pattern (do not use):**
```python
# This puts the label inside the error bar
label_y = row["mean"] + 0.15
ax.text(i, label_y, ...)
```

Also: set `ylim` top high enough that labels above the tallest error bar are not clipped. Add ~0.5–1 units of headroom above the maximum `mean + 1.96*sem` value.

### Heatmap x-axis labels

When a heatmap has 4+ columns and the column labels are more than ~15 characters, the labels will overlap at default figsize. Use short tick labels ("Pair 1", "Pair 2", etc.) on the axis, and add a key/legend table or subtitle below the chart with the full descriptions. Never use multi-line long strings as x-axis tick labels without rotation.

### Legend reference lines

If a reference line (e.g., `axhline`) is meaningful enough to add to a chart, it must appear in the legend. Call `ax.legend()` AFTER adding the reference line, not before.

### Chart checklist (run before saving each figure)

- [ ] No label overlaps with error bars or other chart elements
- [ ] X-axis tick labels are readable without rotation unless rotation is intentional and set explicitly
- [ ] All reference lines (dashed lines, etc.) have a legend entry or direct annotation
- [ ] Legend font size is at least 10pt
- [ ] Y-axis has enough headroom above the tallest element (label + error bar top)
- [ ] Figure captions are written below each image in report.md (not just alt-text)

---

## 8. Free-text homogeneity disclosure

If the study included free-text questions, the Limitations section must disclose the homogeneity issue. This is not optional — omitting it leaves readers to discover the pattern themselves, which damages credibility more than honest disclosure does.

**What to write:** Run the detection script from `research_agent/skills/free-text-homogeneity/SKILL.md` after the run and record the opener rates and shared-prefix findings. Then write a Limitations paragraph using the template from that skill, substituting the specific numbers you found.

**Severity guidance:**
- If >30% of responses share a common opener, or if shared 5-word prefixes exist, name it explicitly in the disclosure.
- If homogeneity is mild (no shared openers, no structural pattern), a brief acknowledgment is still required but can be short: "As with all AI simulation studies, responses show some degree of stylistic overlap due to the model's learned writing conventions; this did not affect the substantive findings."

**Correct example:**

<!-- lint-allow-model: illustrative example, not a model recommendation -->
> Limitations. The free-text responses were generated by GPT-4o. Consistent with known properties of large language models, responses show surface-level stylistic similarity: approximately 38% begin with "Honestly," regardless of agent persona. This reflects the model's learned writing conventions rather than a failure of persona conditioning — the content of responses (the positions taken, specific concerns cited, and trade-offs identified) does vary meaningfully across segments, as shown in the results. The quantitative scale findings are not affected by this issue. Readers should treat the verbatim examples as illustrative of substantive differences, not as authentic samples of how differently-profiled real people would express themselves.

**Wrong approach:**
Do not silently select the three most stylistically distinct quotes as your verbatim examples and skip the disclosure. Do not write "responses were varied and substantive" if the detection check shows significant homogeneity. Do not claim "agents produced distinct voices" unless there is evidence for this (e.g., a multi-model run).

---

## Pre-writing gate checklist (repeat of mandatory section above)

- [ ] Compilation flags confirmed -- HTML uses `--css=report.css --embed-resources --standalone`, PDF uses `--pdf-engine=xelatex --include-in-header=report_header.tex --lua-filter=fix-table-widths.lua`
- [ ] `writeup/survey.md` generated with full question text, types, and options for every question
- [ ] Survey appendix referenced from the report Appendix section
- [ ] Agent configuration table drafted -- trait names, values used, n per segment, plain-language descriptions
- [ ] Instruction string quoted or paraphrased in Methods
- [ ] Expected Parrot links in hand for ALL published objects (survey, agent list, scenario list, results) -- push before writing, not after
- [ ] Verbatim quotes identified and extracted before writing narrative
- [ ] Verbatim quotes formatted as `>` blockquotes, attributed to agent type
- [ ] Model rationale written -- which model, why chosen for this task, pilot confirmation
- [ ] If the intended readership may be unfamiliar with AI simulations: "How this study works" explainer included near top of Methods
- [ ] "Coop" scan: `grep -i coop writeup/report.md` returns zero matches
- [ ] Free-text homogeneity: detection script run, opener rates recorded, Limitations disclosure drafted (see Section 8)
- [ ] Bar chart labels: all value labels positioned above error bar tops (not above bar means)
- [ ] Heatmap axis labels: all tick labels are readable without overlap
