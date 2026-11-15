---
name: methods-response-validation
description: >
  Tiered validation framework for EDSL studies. Covers internal sanity checks
  (no humans needed), comparison to existing human data, and collecting a human
  validation sample via humanize/Prolific. Use when the user wants to validate
  synthetic responses against human benchmarks or run internal consistency checks.
tags: [methods, quantitative, analysis, validation]
---

# Validation

LLM-generated survey responses are synthetic. Validation is how you assess whether they are meaningful — whether the patterns they show correspond to something real. This skill describes a tiered menu of validation options, from zero-cost internal checks to full human comparison.

## Using this skill

Read the user's intent before deciding whether and how to raise validation. Users vary enormously:

- Some are purely ideating and have no interest in validation — do not interrupt their flow
- Some know exactly what validation they want and will ask for it directly
- Some are building toward a deliverable where validation would genuinely strengthen their work, but haven't thought about it
- Some cannot collect human data at all (no budget, no access, topic is model-specific) — for them, only internal checks are feasible
- Some already have human data on hand and would benefit from a comparison

The right response depends entirely on where the user is. If they seem to be building something consequential and haven't raised validation, a brief natural mention may be appropriate — not a formal question, just an offer. If they're clearly exploring or have no need for it, say nothing. If they ask, engage fully with what's actually available to them.

**Validation ≠ scale.** Running 1,000 AI agents instead of 20 does NOT validate findings — it gives more precise estimates of patterns that might not be real. Running 20 AI agents + 75 humans DOES validate. When a user asks for large N "to be confident," clarify what actually builds confidence: diverse persona coverage, cross-model checks, human validation sample, known-group validity. Confidence comes from triangulation, not from repeating the same AI personas.

---

## If you plan to validate against humans, design for it upfront

Validation is much cleaner when the LLM and human surveys are comparable from the start. If the user intends to collect a human comparison sample — even loosely — flag these considerations during planning, before the survey is finalised:

- **Same question order.** Humans experience questions sequentially; make sure the order matches what the LLM agents see.
- **No survey memory modes for human-deployable surveys.** `set_full_memory_mode()` and related APIs inject prior Q&A into LLM agent context only — they do not run in humanize (see **skill:edsl-human-survey** — "Memory and piping"). If a later question needs a prior answer, use piping (`{{ q_name.answer }}`). Using full memory in the LLM survey but piping (or nothing) for humans creates a confound when comparing results.
- **Same response scales and option labels.** Don't abbreviate or reword options for the LLM version; use the exact text humans will see.
- **Scenario compatibility.** Scenarios can be passed to human respondents via `survey.by(scenarios).humanize(scenario_list_method="randomize")`. Plan for this if scenarios are part of the study design.

These don't need to be raised unless validation is genuinely on the table. If it is, catch them before the survey runs — not after.

---

## Validation options

The sections below are organized for the agent's reference — the tier labels are internal shorthand and should never be used with the user. When discussing validation with a user, describe what it involves in plain language ("we could run the same survey on 50–100 real people via Prolific to see if the patterns hold") not tier numbers or framework jargon.

### Internal checks (free, no human data needed)

These run on your EDSL results alone and can catch obvious problems before anyone sees the report.

**Use the reusable script.** Copy `validate_results.py` from this skill into the study's `analysis/` directory and run it after generating results:

```bash
cp research_agent/skills/methods-response-validation/scripts/validate_results.py analysis/validate_results.py

# Basic run (checks distribution plausibility and variance):
python analysis/validate_results.py

# With a known-group comparison (repeat --known-groups for multiple):
python analysis/validate_results.py \
    --known-groups agent.political_leaning answer.policy_support \
    --known-groups agent.income_level answer.price_sensitivity
```

The script checks what can be checked automatically and flags issues. It cannot determine whether known-group differences go in the right direction — that requires your judgment. Exit code 0 = no issues, 1 = issues found.

#### Known-group validity

The most important internal check. Agents with different trait specifications should respond differently in expected directions. If they do not, something is wrong — the survey instrument, the agent construction, or both.

Examples:
- Agents specified as "politically conservative" should rate left-wing policies lower than agents specified as "politically liberal"
- Agents with "price-sensitive" traits should prefer lower-cost options more strongly than "luxury-oriented" agents
- Agents specified as healthcare workers should rate clinical questions with more nuance than agents with no relevant background

Run this by comparing mean responses across agent subgroups and checking that the direction matches your prior expectation.

**If subgroups do not differ when they clearly should, do not simply flag it and move on.** This is a signal that something is wrong upstream. Work through this before proceeding:

1. **Check the agent construction first.** Are the differentiating traits specific enough? "conservative" is vague; "strongly conservative, votes Republican, opposes government regulation" is more likely to activate the relevant response pattern. Revise and re-run the pilot.
2. **Check the question wording.** Is the question framed in a way that activates the trait? A question that could be answered the same way regardless of political leaning will show no group difference — that may be a question design problem, not an agent problem.
3. **If neither fix resolves it**, the topic may genuinely not be amenable to LLM persona simulation. Note this clearly in the report and consider whether the study's findings are still meaningful.

Catching this during a small pilot (2–3 agents per subgroup) is far cheaper than discovering it after a full run.

#### Cross-model consistency

Run a subset of agents (10–20) on two or more models. If results are similar across models, they are more likely to reflect genuine patterns rather than one model's idiosyncrasies. If they diverge substantially, note it and do not over-interpret the single-model findings.

See `research_agent/skills/workflow-model-selection/SKILL.md` for how to set up multi-model runs.

#### Distribution plausibility

Check that response distributions look reasonable:
- Are responses uniformly spread across all options (suggesting random answering or a poorly worded question)?
- Are responses piled at one extreme (floor/ceiling effect)?
- Do open-ended responses vary meaningfully across agents, or do they read as generic paraphrases of the question?

#### Internal consistency

For multi-item constructs (e.g. five questions all measuring "brand trust"), check that agents who score high on one item tend to score high on others. A Cronbach's alpha or simple pairwise correlation is sufficient.

---

### Compare to existing human data (free if data exists)

If the user has prior human data on the same topic — from an earlier study, a client, or a published source — compare the LLM distributions to the human distributions. If you don't know whether they have any, and it seems relevant to ask, ask naturally — not as a checklist item.

#### What to compare

Focus on **direction and relative magnitude**, not exact match:

- Do the LLM response proportions rank options in the same order as the human data?
- Do the LLM treatment effects (A vs. B differences) go in the same direction as human treatment effects?
- Are the LLM means within a plausible range of human means?

Exact numerical match is not the standard — LLMs will not reproduce population-representative marginals, particularly for underrepresented groups. Direction and relative ordering are the meaningful signal.

#### Statistical methods

```python
import numpy as np
from scipy.stats import spearmanr, pearsonr

# Compare response proportion vectors
llm_props   = np.array([0.12, 0.28, 0.35, 0.25])   # LLM distribution
human_props = np.array([0.10, 0.30, 0.38, 0.22])   # Human distribution

# Rank correlation (most informative)
rho, p = spearmanr(llm_props, human_props)
print(f"Spearman rho = {rho:.2f}, p = {p:.3f}")

# Mean absolute deviation
mad = np.mean(np.abs(llm_props - human_props))
print(f"Mean absolute deviation = {mad:.3f}")

# For treatment effects: compare effect sizes
llm_effect   = llm_condition_b_mean   - llm_condition_a_mean
human_effect = human_condition_b_mean - human_condition_a_mean
print(f"LLM effect: {llm_effect:.2f}, Human effect: {human_effect:.2f}")
print(f"Direction match: {(llm_effect > 0) == (human_effect > 0)}")
```

Save comparison outputs to `data/validation/` and reference them in the report.

---

### Collect a human validation sample (costs money and time)

If no human data exists, the same EDSL survey can be deployed to real respondents via `survey.humanize()` — either as an open link or through Prolific for a paid screened sample. If you raise this with the user, describe it in plain terms and let them decide; don't present it as a formal step.

**How many respondents do you need?** Far fewer than most people think. The goal is not to establish population-representative norms — it is to check whether the direction of effects holds. That is a much lower bar:

- For binary directional checks (does group A score higher than group B?), n=30–50 total gives reasonable power when the true effect is large — which it should be if the LLM simulation is working at all.
- For comparing response distributions across 4–5 options, n=50–100 is enough to see whether the rank ordering of options matches.
- If you want to detect subtler disagreements or compare across multiple subgroups, aim for 150–200.

A Prolific sample of 75 respondents at $2.00 each costs $150 plus Prolific fees — a small price for meaningful evidence that the findings are not purely model artefacts.

#### Option A: Open link (free, unscreened)

```python
from edsl import Survey

info = survey.humanize(
    human_survey_name="Validation Sample — [Study Name]",
    survey_visibility="unlisted",
)
print(info["respondent_url"])  # share via email, social media, etc.
```

Good for: quick sanity check, internal teams, convenience samples.

#### Option B: Prolific (paid, screened)

```python
from edsl import Coop

coop = Coop()
info = survey.humanize(human_survey_name="Validation Sample — [Study Name]")

study = coop.create_prolific_study(
    human_survey_uuid=info["uuid"],
    name="Validation: [Study Name]",
    description="5-minute survey on [topic]",
    num_participants=75,
    estimated_completion_time_minutes=5,
    participant_payment_cents=200,   # $2.00 — $24/hr, well above Prolific minimum
    filters=[age_filter, ...],       # match agent demographic range if relevant
)
```

Good for: publication-quality validation, client deliverables, demographic matching to agent pool.

See `research_agent/skills/edsl-human-survey/SKILL.md` for the full Prolific API reference including filters.

#### Retrieving and comparing results

```python
from edsl import Coop

coop = Coop()
human_results = coop.get_human_survey_responses(info["uuid"])
# or for Prolific:
human_results = coop.get_prolific_study_responses(info["uuid"], study["study_id"])

# Now compare to LLM results using the statistical methods above
```

Save human results to `data/validation/human_results.ep`.

Compare against completed responses only, which is the default. If dropout matters
to the validation (for example, whether people abandon at a question the LLM
answers without trouble), fetch with `include_partial=True` and use
`agent.response_status` and `agent.last_activity_at` to see where respondents
stopped; keep those rows out of the LLM-vs-human comparison itself.

---

## What to do when LLM and human results diverge

Divergence is informative, not a failure. Report it honestly and discuss what it might mean:

- **Direction matches but magnitude differs**: Common and expected. LLMs often show attenuated or amplified effects relative to humans. Note the discrepancy and frame LLM findings as directional.
- **Direction disagrees on some items**: Investigate whether those items involve topics underrepresented in training data, require lived experience, or touch known LLM biases (e.g. cultural, regional, experiential).
- **Complete disagreement**: A serious signal. Either the agent construction is misspecified, the survey instrument is problematic, or the topic is genuinely unsuited to LLM simulation. Do not publish without discussing this prominently.

Never hide divergence. It is part of the scientific record.

---

## Reporting validation

If validation was done, include a Validation subsection in the report's Methods section. Write it in plain language describing what was actually done — do not use "tier" terminology.

**Internal checks only:**
<!-- lint-allow-model: illustrative example, not a model recommendation -->
> Validation was conducted through internal checks. Known-group validity was assessed by comparing responses across agent subgroups with contrasting trait specifications (e.g., conservative vs. liberal agents on policy questions); results showed expected directional differences on all items. Cross-model consistency was assessed by running a 15-agent subset on both GPT-4o and Claude Sonnet; response distributions were highly correlated (Spearman rho = 0.94). No human comparison was conducted for this exploratory study.

**With existing human data:**
> LLM response distributions were compared to published Pew Research data on [topic] (N = 1,502, fielded [date]). Response proportions were highly rank-correlated with the human benchmark (Spearman rho = 0.89), and treatment effects were directionally consistent in 7 of 8 comparisons. The exception ([item]) is discussed in the Limitations section.

**With a collected human sample:**
> A validation sample of 75 Prolific respondents completed the same survey (screened for [criteria], paid $2.00, estimated 5 minutes). LLM and human response distributions were correlated at rho = 0.82 across multiple-choice items. Treatment effects were directionally consistent in all cases, though LLM effect sizes were approximately 1.4x larger in magnitude than the human sample. This attenuation pattern is consistent with prior work (Horton, 2023) and is noted in the Limitations section.
