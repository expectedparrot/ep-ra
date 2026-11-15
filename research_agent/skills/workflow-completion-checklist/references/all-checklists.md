# Full study checklist reference

## Contents

- EDSL study checklist
- Agent-list study checklist
- Concordia simulation checklist
- Evidence rules
- Final deliverables

Every study gets a `checklist.md` in its root directory. Create it when you start the study. Work through it as you go. You may NOT output `[STUDY_COMPLETE]` until every item is checked with evidence.

## Creating the checklist

At study start, write the appropriate template to `checklist.md` based on the study type.

### EDSL Study Checklist

Use this template for studies that use EDSL surveys/experiments:

```markdown
# Study Checklist

## Setup
- [ ] Study structure created via `ep study scaffold`
- [ ] README.md has PURPOSE, Author, Timestamp

## Model Selection
- [ ] Model discussed with user (purpose, provider preference, cross-model interest, cost constraints)
      Evidence: <!-- e.g., "user confirmed <model> for quality; no cross-model requirement" -->
- [ ] Model name(s) confirmed with a bounded `ep models` query; external search used only when the study depends on frontier/benchmark claims
      Evidence: <!-- paste the model name(s) used -->
- [ ] Model tier matches task complexity (not lowest cost by default)
      Evidence: <!-- e.g., "Tier 2 — open-ended persona simulation, Tier 3 would produce thin responses" -->
- [ ] Spot-check pilot run (2–3 agents) completed before full run — responses are substantive and persona-consistent
      Evidence: <!-- brief note on what you observed, or "N/A — no agents used" -->
- [ ] Model choice documented in report Methods section
      Evidence: <!-- quote the Methods sentence, or paste it below -->

## Survey Design
- [ ] Memory mode decision made deliberately for each question group
      Evidence: <!-- state the choice: no memory / piping / targeted / full — and why -->
- [ ] If any memory mode other than the default is used, it is documented in the Methods section of the report
      Evidence: <!-- quote the Methods paragraph, or "no memory modes used" -->

## Data Integrity
- [ ] All survey data comes from actual EDSL runs (no mock/fake/synthetic data)
      Evidence: <!-- e.g., data/results.ep, 312 rows, run at 2025-06-15T14:32Z -->
- [ ] Inference completed successfully and `data/results.ep` was saved
      Evidence: <!-- ep run exit status and results path -->
- [ ] Saved results reviewed once with bounded `ep results review data/results.ep`
      Evidence: <!-- paste compact row count, missingness, distributions, and cost -->
- [ ] A saved validation script confirms the exact planned row count, required answer fields, non-null coverage, and required uniqueness constraints
      Evidence: <!-- script path and successful command output; do not use an approximate line count -->
- [ ] Optional inspection completed, or its failure was reported separately without rerunning inference
      Evidence: <!-- make inspect output, or separate inspection error -->
- [ ] Every number, table, and chart in the report traces to a file in `data/`
      Evidence: <!-- list the source files -->

## Analysis
- [ ] `skill:post-run-review` invoked immediately after the run completed, BEFORE analysis and reporting began — findings presented to the user
      Evidence: <!-- e.g., review presented after run at 2025-06-15T14:40Z; execution gaps fixed; user chose to proceed -->
- [ ] All analysis scripts live in `analysis/` and run via `make`
      Evidence: <!-- e.g., make PLOTS TABLES succeeds -->
- [ ] Plots written to `writeup/plots/`, tables to `writeup/tables/`
- [ ] `plot_style.py` copied into `analysis/` and imported in every plot script
      Evidence: <!-- e.g., confirmed in plot_*.py files -->

## Visual Quality

### Setup
- [ ] `plot_style.py` imported at the top of every plot script
      Evidence: <!-- confirmed in all plot_*.py files -->
- [ ] `check_plots.py` copied into `analysis/`
      Evidence: <!-- analysis/check_plots.py present -->

### Figure sizing
- [ ] Single-axes multi-bar charts (Likert, stacked percent) use `figsize_likert(n_rows)`
      Evidence: <!-- NOT figsize_stacked() — confirm in each Likert script -->
- [ ] Multi-panel charts use `FIGSIZE["two_wide"]` etc. or `figsize_stacked(n)` for subplot panels
      Evidence: <!-- confirm in each multi-panel script -->

### Fonts
- [ ] Font family is DejaVu Serif (matches LaTeX/pandoc report body font)
      Evidence: <!-- plot_style.py rcParam confirmed -->
- [ ] No text anywhere in any plot is smaller than 10pt (tick labels) or 9pt (annotations)
      Evidence: <!-- confirmed in scripts and/or check_plots.py output -->
- [ ] Likert / horizontal bar charts: y-tick label size explicitly set to 13pt
      Evidence: <!-- `ax.tick_params(axis="y", labelsize=13)` confirmed -->

### Titles
- [ ] Single-panel charts use `plot_style.set_chart_title(ax, title, subtitle)` — NOT a mix of `fig.suptitle()` and `ax.set_title()`
      Evidence: <!-- both title lines anchored to axes center, confirmed in scripts -->
- [ ] Multi-panel charts use `fig.suptitle()` for the overall title and `ax.set_title()` per panel
      Evidence: <!-- correct pattern confirmed in multi-panel scripts -->

### Legends
- [ ] No legend is floating inside the data area where a bar or line could reach it
      Evidence: <!-- all legends anchored below axes with bbox_to_anchor or fig.legend() -->

### Overlap — text and data
- [ ] No annotation text is positioned in the path of any line or bar
      Evidence: <!-- visually verified; annotations moved to clear areas if needed -->
- [ ] End-of-line labels on line charts are staggered if any two final values are within 4 percentage points
      Evidence: <!-- END_LABEL_OFFSETS dict or equivalent in line chart scripts -->
- [ ] No bar annotation labels overlap each other or bleed off the chart edge
      Evidence: <!-- verified visually and/or via check_plots.py -->
- [ ] Annotation text near data has a white or contrasting background box so it is always legible
      Evidence: <!-- bbox=dict(facecolor='white', ...) confirmed in scripts with annotations -->

### Grammar and labels
- [ ] All instances of "e.g." are written "e.g.," (with trailing comma)
      Evidence: <!-- confirmed in all plot scripts and report.md -->
- [ ] Axis labels include units where relevant (%, score range, currency, etc.)
      Evidence: <!-- confirmed -->

### Automated checks
- [ ] `check_plots.py` run — zero errors, all warnings reviewed and resolved
      Evidence: <!-- paste full output -->
- [ ] All plots saved at 150 DPI minimum with `bbox_inches="tight"` (enforced by `plot_style.save()`)
      Evidence: <!-- confirmed in check_plots.py DPI output -->
- [ ] No labels, titles, or annotations clipped at image edges
      Evidence: <!-- check_plots.py clipping check passed -->

### Report references
- [ ] Every plot in `report.md` has a descriptive alt text string in `![...](...)`
      Evidence: <!-- confirmed — not left blank or as "chart" -->
- [ ] Every plot in `report.md` is followed within 2 lines by a `Figure N:` caption
      Evidence: <!-- check_plots.py caption check passed -->
- [ ] Figure numbers are sequential with no gaps or duplicates
      Evidence: <!-- confirmed -->

## Validation (include only if the user wants it and it is feasible)

Add this section only if validation is something the user actually cares about and has the means to pursue. Many users have no interest or ability to collect human data — for them this section does not apply. See `research_agent/skills/methods-response-validation/SKILL.md`.

- [ ] Validation approach agreed with user and noted in plan.md
      Evidence: <!-- one sentence on what was done and why -->
- [ ] `validate_results.py` copied into `analysis/` and run — no errors or warnings
      Evidence: <!-- paste key output, or "no issues found" -->
- [ ] Known-group directions verified manually — group differences go the expected way
      Evidence: <!-- e.g., "conservative agents scored 2.1 vs liberal agents 4.3 on policy_support — correct direction" -->
- [ ] If existing human data was used: comparison run, output saved to `data/validation/`
      Evidence: <!-- source cited, key statistic -->
- [ ] If a human sample was collected: results saved to `data/validation/human_results.ep`
      Evidence: <!-- n= respondents, Prolific study ID or open-link UUID -->
- [ ] Validation described in plain language in report Methods section
      Evidence: <!-- section heading -->
- [ ] Any divergence between LLM and human results addressed in Limitations section
      Evidence: <!-- "no divergence found" or brief description -->

## Report
- [ ] Report begins with research context (Background section explaining what is being studied and why)
      Evidence: <!-- e.g., Background section describes the company, product, and purpose -->
- [ ] `writeup/survey.md` generated — full question text, type, and answer options for every question
      Evidence: <!-- e.g., "writeup/survey.md written, 12 questions" -->
- [ ] Survey instrument referenced (or reproduced) in report Appendix — readers can see exact question wording
      Evidence: <!-- e.g., "Appendix A present in report.md" -->
- [ ] Agent trait table present in Methods — trait names, values used, and plain-language descriptions (not just count totals)
      Evidence: <!-- e.g., "Table in Methods section covering age_group, price_sensitivity, etc." -->
- [ ] Agent instruction string quoted or paraphrased in Methods
      Evidence: <!-- paste or quote the instruction string, or "no instruction — agents have no system prompt" -->
- [ ] Model rationale written in Methods — covers which model, WHY chosen for this task, and whether a pilot confirmed response quality
      Evidence: <!-- quote the rationale sentence(s) -->
- [ ] Verbatim response examples included for key free-text questions — at least 2-3 examples attributed to agent type
      Evidence: <!-- e.g., "Inline examples in Results section for Q4, Q7, Q11" -->
- [ ] Publication decision honored: objects remain local unless the user explicitly requested publishing
      Evidence: <!-- "local only" or list explicitly requested E[P] URLs -->
- [ ] `writeup/report.md` exists and is the single report file
- [ ] If publication was requested, `writeup/report.md` links to the published EDSL objects
- [ ] `ep report check --root .` passes after compilation
      Evidence: <!-- paste output -->
- [ ] Every plot and representative pages from each requested PDF were rendered and visually inspected
      Evidence: <!-- list images/pages inspected, or leave incomplete and report the rendering blocker -->
- [ ] PDF version exists
      Evidence: <!-- filename -->
- [ ] HTML version exists
      Evidence: <!-- filename -->

```

### Agent List Study Checklist

Use this template when the primary deliverable is an EDSL `AgentList` (no survey run, no simulation). Most Visual Quality items do not apply — omit them unless the study includes distribution plots.

```markdown
# Study Checklist

## Setup
- [ ] Study structure created via `ep study scaffold`
- [ ] README.md has PURPOSE, Author, Timestamp

## Model Selection
- [ ] Model documented in report Methods section (name, version, rationale)
      Evidence: <!-- quote the Methods sentence, or "N/A — no model used" -->
      Note: do NOT include API costs or dollar amounts in the report — costs are
      tracked internally but never appear in deliverables.

## Agent List Integrity
- [ ] AgentList serializes and deserializes without error (`AgentList.from_dict(al.to_dict())`)
      Evidence: <!-- e.g., "round-trip confirmed in run_job.py output" -->
- [ ] All trait value counts sum to N (total agent count)
      Evidence: <!-- e.g., "distribution table verified: all columns sum to 80" -->
- [ ] No duplicate agents (identical trait combinations)
      Evidence: <!-- e.g., "confirmed: len(set(tuple(a.traits.items()) for a in agents)) == N" -->
- [ ] `name` is not used as a trait key
      Evidence: <!-- confirmed in script -->
- [ ] `instruction` string reviewed and appropriate for intended downstream use
      Evidence: <!-- paste the instruction string, or "no instruction — omitted intentionally" -->
- [ ] All trait values consistently cased (no "Male" vs "male" mixing, no trailing spaces)
      Evidence: <!-- confirmed in script or data/cooked file -->

## Codebook
- [ ] Agent Design table present in report (one row per trait: name, type, values, description)
      Evidence: <!-- section heading in report.md -->
- [ ] Every trait in the AgentList appears in the Agent Design table
      Evidence: <!-- confirmed -->

## Sources
- [ ] Distribution proportions cited or justified in report Methods section
      Evidence: <!-- name the source(s) used -->

## Analysis
- [ ] Distribution table script lives in `analysis/` and runs via `make`
      Evidence: <!-- e.g., make TABLES succeeds -->
- [ ] Table written to `writeup/tables/agent_distribution.csv`
- [ ] If distribution plots were produced: `plot_style.py` imported and `check_plots.py` run
      Evidence: <!-- "no plots" or paste check_plots.py output -->

## Report
- [ ] Background section present (why this list was created, what it will be used for)
      Evidence: <!-- section heading in report.md -->
- [ ] Methods section present (how dimensions and distributions were chosen, sources cited)
      Evidence: <!-- section heading in report.md -->
- [ ] Agent Design table present (full trait codebook)
      Evidence: <!-- section heading in report.md -->
- [ ] Distribution section present with !include table and explanatory paragraph
      Evidence: <!-- section heading in report.md -->
- [ ] Limitations section present
      Evidence: <!-- section heading in report.md -->
- [ ] Usage section present (load snippet plus prose guidance on downstream use)
      Evidence: <!-- section heading in report.md -->
- [ ] Publication decision honored: AgentList remains local unless the user explicitly requested publishing
      Evidence: <!-- "local only" or explicitly requested E[P] URL -->
- [ ] If publication was requested, `writeup/report.md` links to the published AgentList
      Evidence: <!-- URL or "not requested" -->
- [ ] `ep report check --root .` passes
      Evidence: <!-- paste output -->
- [ ] PDF version exists
      Evidence: <!-- filename -->
- [ ] HTML version exists
      Evidence: <!-- filename -->

```

### Simulation Study Checklist

Use this template for studies that use Concordia social simulations:

```markdown
# Study Checklist

## Setup
- [ ] Study structure created via `ep study scaffold --type simulation`
- [ ] README.md has PURPOSE, Author, Timestamp

## Data Integrity
- [ ] All simulation data comes from actual Concordia runs (no mock/fake/synthetic data)
      Evidence: <!-- e.g., data/simulation_log_haggling_fruitville.json, 15 steps, run at 2026-02-15T14:32Z -->
- [ ] Simulation logs saved to `data/`
      Evidence: <!-- list the log files -->
- [ ] Every number, table, and chart in the report traces to a file in `data/`
      Evidence: <!-- list the source files -->

## Analysis
- [ ] Log analysis completed
      Evidence: <!-- e.g., analysis/analyze_logs.py produces expected outputs -->
- [ ] All analysis scripts live in `analysis/` and run via `make`
      Evidence: <!-- e.g., make PLOTS TABLES succeeds -->
- [ ] Plots written to `writeup/plots/`, tables to `writeup/tables/`
- [ ] `plot_style.py` copied into `analysis/` and imported in every plot script
      Evidence: <!-- e.g., confirmed in plot_*.py files -->

## Visual Quality

### Setup
- [ ] `plot_style.py` imported at the top of every plot script
      Evidence: <!-- confirmed in all plot_*.py files -->
- [ ] `check_plots.py` copied into `analysis/`
      Evidence: <!-- analysis/check_plots.py present -->

### Figure sizing
- [ ] Single-axes multi-bar charts (Likert, stacked percent) use `figsize_likert(n_rows)`
      Evidence: <!-- NOT figsize_stacked() — confirm in each Likert script -->
- [ ] Multi-panel charts use `FIGSIZE["two_wide"]` etc. or `figsize_stacked(n)` for subplot panels
      Evidence: <!-- confirm in each multi-panel script -->

### Fonts
- [ ] Font family is DejaVu Serif (matches LaTeX/pandoc report body font)
      Evidence: <!-- plot_style.py rcParam confirmed -->
- [ ] No text anywhere in any plot is smaller than 10pt (tick labels) or 9pt (annotations)
      Evidence: <!-- confirmed in scripts and/or check_plots.py output -->
- [ ] Likert / horizontal bar charts: y-tick label size explicitly set to 13pt
      Evidence: <!-- `ax.tick_params(axis="y", labelsize=13)` confirmed -->

### Titles
- [ ] Single-panel charts use `plot_style.set_chart_title(ax, title, subtitle)` — NOT a mix of `fig.suptitle()` and `ax.set_title()`
      Evidence: <!-- both title lines anchored to axes center, confirmed in scripts -->
- [ ] Multi-panel charts use `fig.suptitle()` for the overall title and `ax.set_title()` per panel
      Evidence: <!-- correct pattern confirmed in multi-panel scripts -->

### Legends
- [ ] No legend is floating inside the data area where a bar or line could reach it
      Evidence: <!-- all legends anchored below axes with bbox_to_anchor or fig.legend() -->

### Overlap — text and data
- [ ] No annotation text is positioned in the path of any line or bar
      Evidence: <!-- visually verified; annotations moved to clear areas if needed -->
- [ ] End-of-line labels on line charts are staggered if any two final values are within 4 percentage points
      Evidence: <!-- END_LABEL_OFFSETS dict or equivalent in line chart scripts -->
- [ ] No bar annotation labels overlap each other or bleed off the chart edge
      Evidence: <!-- verified visually and/or via check_plots.py -->
- [ ] Annotation text near data has a white or contrasting background box so it is always legible
      Evidence: <!-- bbox=dict(facecolor='white', ...) confirmed in scripts with annotations -->

### Grammar and labels
- [ ] All instances of "e.g." are written "e.g.," (with trailing comma)
      Evidence: <!-- confirmed in all plot scripts and report.md -->
- [ ] Axis labels include units where relevant (%, score range, currency, etc.)
      Evidence: <!-- confirmed -->

### Automated checks
- [ ] `check_plots.py` run — zero errors, all warnings reviewed and resolved
      Evidence: <!-- paste full output -->
- [ ] All plots saved at 150 DPI minimum with `bbox_inches="tight"` (enforced by `plot_style.save()`)
      Evidence: <!-- confirmed in check_plots.py DPI output -->
- [ ] No labels, titles, or annotations clipped at image edges
      Evidence: <!-- check_plots.py clipping check passed -->

### Report references
- [ ] Every plot in `report.md` has a descriptive alt text string in `![...](...)`
      Evidence: <!-- confirmed — not left blank or as "chart" -->
- [ ] Every plot in `report.md` is followed within 2 lines by a `Figure N:` caption
      Evidence: <!-- check_plots.py caption check passed -->
- [ ] Figure numbers are sequential with no gaps or duplicates
      Evidence: <!-- confirmed -->

## Report
- [ ] Report begins with research context (Background section explaining what is being studied and why)
      Evidence: <!-- e.g., Background section describes the simulation scenario and research question -->
- [ ] Agent/entity configuration described in Methods — traits, goals, roles, and instruction strings shown
      Evidence: <!-- e.g., "Methods section includes entity trait table and instruction strings" -->
- [ ] Model rationale written in Methods — which model(s) were used and why, with pilot or test-run confirmation
      Evidence: <!-- quote the rationale sentence(s) -->
- [ ] Representative verbatim dialogue or action excerpts included — readers can see what agents actually said/did
      Evidence: <!-- e.g., "Dialogue excerpts in Results section, 3-4 per key scenario event" -->
- [ ] `writeup/report.md` exists and is the single report file
- [ ] `ep report check --root .` passes
      Evidence: <!-- paste output -->
- [ ] PDF version exists
      Evidence: <!-- filename -->
- [ ] HTML version exists
      Evidence: <!-- filename -->

```

## Rules

1. **Create at study start.** The checklist is one of the first files you write, right after scaffolding.

1b. **Re-read before session end.** Loading this skill at session start is not enough. Before ending a session or outputting `[STUDY_COMPLETE]`, **re-read `checklist.md`** and verify every item, including the error log review.

2. **Update as you go.** Check items off when they're done, filling in the evidence comment. Don't batch all checks at the end.

3. **Evidence is mandatory.** Each checked item must have a concrete reference — a filename, row count, timestamp, command output, or similar. Never check a box without evidence.

4. **No mock data — ever.** If a survey hasn't been run, run it. If it failed, fix it and re-run. If cost is a concern, reduce agent or scenario count. A report built on made-up data is worse than no report at all.

5. **Completion gate.** Before outputting `[STUDY_COMPLETE]`, verify every box is checked. If any item is unchecked, finish it first.

6. **Add study-specific items.** If the study has unique requirements (e.g., predecessor provenance, specific computed objects), add checklist items for those.

## Final deliverables

A completed study must have all three:
- `writeup/report.md`
- PDF version of the report
- HTML version of the report

Only when all checklist items are checked AND all three deliverables exist, output `[STUDY_COMPLETE]`.
