---
name: methods-persona-calibration
description: >
  Iteratively refine an LLM persona description to match a specific individual's
  survey responses, using a train/holdout split and LLM-driven rewriting.
  Use when the user wants to build a persona that accurately represents a real
  person's attitudes based on their survey answers.
tags: [simulation, quantitative, data-collection]
---

# Iterative Persona Calibration

Build an LLM persona that accurately represents a specific individual by iteratively refining a persona description against their survey responses. The method uses "gradient descent on persona descriptions" — each round, an LLM examines where the current persona gets answers wrong and rewrites the persona to fix mismatches while preserving generalization.

This complements skill:methods-calibrating-agents (population-level mixture optimization) by operating at the **individual level**: instead of weighting a mixture of personas to match aggregate distributions, this method crafts a single persona to match one person's response pattern.

---

## Before running this method

**Ask about context and goals:**
- What decision or analysis will these calibrated personas inform?
- Where did the target responses come from? (human survey, prior LLM run, synthetic data?)
- Do you care more about maximizing holdout accuracy (predictive power) or maintaining interpretable persona descriptions (understandability)?
- Are there specific traits or attitudes you expect the personas to capture, or concerns about what might be missed?

**Explain the approach:**
Starting from a blank persona, the method iteratively refines the description by showing an LLM where the persona gets survey answers wrong and asking it to rewrite. Each round uses a train/holdout split: only training mismatches are shown to the calibrator, so holdout accuracy measures real generalization, not memorization. Expect rapid convergence for attitudinal questions, but know that biographical facts (income, location) can't be reliably inferred from attitudes alone.

**Discuss design choices:**
- How many calibration rounds? (More for LLM targets that converge cleanly, fewer for noisy human targets.)
- Should the calibrator see the text of true holdout questions (without answers)? No proven benefit for political/attitudinal surveys, but may help in specialized domains.
- Do you want to calibrate every respondent, or sample a subset first to gauge feasibility?

More context about what you're trying to learn helps frame expectations — for example, if you're testing whether a persona *can* represent someone vs. building personas for downstream use, that changes how we interpret calibration failures.

---

## When to Use

- You have **individual-level survey responses** (from Prolific, a panel, or an LLM-generated target) and want a persona that reproduces them.
- You want personas that **generalize** to unseen questions, not just memorize known answers.
- You need to measure how well an LLM can represent a specific person's attitudes.

**Not appropriate when:**
- You want to match a **population distribution** (use skill:methods-calibrating-agents instead).
- You have no ground-truth responses to calibrate against.
- The target is a fictional archetype rather than an actual respondent.

---

## Method Overview

### The Calibration Loop

1. **Start blank.** Initial persona = `"You are a person."`
2. **Survey.** Run the persona through a diagnostic survey.
3. **Split.** Randomly split calibration questions into a training set and a held-out set each round. A separate set of **true holdout** questions is never revealed.
4. **Show mismatches.** For each training question the persona got wrong, show the calibration LLM the current persona, the wrong answer, and the correct answer.
5. **Rewrite.** Ask the LLM to write a new 2-4 sentence persona that would naturally produce the correct training answers while being general enough for holdout questions.
6. **Re-survey.** Run the new persona through the full survey. Measure accuracy on calibration questions and true holdout questions separately.
7. **Repeat** for several rounds.

### Key Design Principles

- **Train/holdout split prevents memorization.** The calibration prompt only shows mismatches on training questions. Holdout accuracy measures genuine trait recovery.
- **True holdout questions are never revealed.** Their answers are only used for evaluation, never shown to the calibrator. This is the honest measure of generalization.
- **Reshuffle each round.** Different random splits per round ensure the persona must capture foundational traits, not optimize for a fixed subset.
- **Persona descriptions, not answer lists.** The calibration prompt explicitly instructs: "Do NOT list correct answers. Describe WHO this person IS."

---

## Survey Design

The method works with **any survey the user already has**. The user brings their survey — it could be a political attitudes battery, a consumer preferences questionnaire, a personality inventory, or anything else. The method then partitions that survey's questions into two roles:

- **Calibration pool**: The questions whose answers are used to drive persona improvement. Each round, these are further split into a training set (mismatches shown to the calibrator) and a within-calibration holdout set (not shown).
- **True holdout** (optional but recommended): A subset of questions whose answers are **never** shown to the calibrator, used purely to measure generalization. If the user wants to know whether the recovered persona generalizes beyond the training signal, reserve some questions for this purpose.

If the user doesn't want a true holdout set (e.g., they have a short survey and want to use all questions for calibration), that's fine — just note that calibration accuracy will overstate generalization since there's no independent test.

See `references/study_survey.py` for the 15-question instrument used in the original studies, but the method is not tied to this specific survey.

### Design decision: include true holdout question text in the calibration prompt?

In the original studies, an ablation tested whether showing the calibrator the **text** of true holdout questions (without their answers) improved generalization. It did not — both conditions achieved identical holdout accuracy. The bottleneck was what could be inferred from attitudes, not what questions to optimize for.

However, this was tested on a single set of political/attitudinal questions. In other domains, showing the holdout question text might help if the questions require specialized knowledge the calibrator wouldn't otherwise consider. **Ask the user** whether they want the calibrator to see the holdout question text (without answers) or run fully blind. If unsure, default to including the text — it doesn't hurt and may help in domains not yet tested.

---

## The Calibration Prompt

This is the core of the method — the prompt that asks an LLM to propose an improved persona. The full prompt is built as a plain string (not an f-string — see skill:edsl-quirks) and injected via EDSL `Scenario` to avoid Jinja2 conflicts.

```text
You are a persona engineer. Your job is to write a rich, detailed
persona description for a survey respondent.

Current persona: "<current_persona>"

This persona was asked several survey questions. Here is where it
got answers WRONG:

- Question: "<question_text>"
  Your persona answered: "<predicted_answer>"
  The true answer is: "<gold_answer>"
- ...
(or: "All training questions were answered correctly.")

Now, the persona also needs to answer these HELD-OUT questions
correctly (you do NOT know the correct answers -- your persona must
have the right foundational traits to naturally produce correct
answers):

- "<holdout_question_text>"
  Options: [...]
- ...

Write a NEW, improved persona description (2-4 sentences) that:
1. Has foundational demographic and personality traits that would
   naturally lead to the correct answers on the training questions
   shown above.
2. Is general enough in its core traits that it would also answer
   the held-out questions authentically.
3. Does NOT simply list the correct answers or memorize specific
   survey responses. Instead, describe WHO this person IS -- their
   background, worldview, values, and life circumstances.
4. Builds on what was correct about the current persona and fixes
   what was wrong.

Write ONLY the persona description, nothing else. Start with
"You are...".
```

This prompt is passed to the LLM via a `Scenario`:

<!-- ep-cli-lint: allow substantive-analysis -->
```python
rewrite_q = QuestionFreeText(
    question_name="new_persona",
    question_text="{{ scenario.calibration_prompt }}",
)
scenario = Scenario({"calibration_prompt": prompt})
result = Survey([rewrite_q]).by(ScenarioList([scenario])).by(model_list).run(
    disable_remote_inference=True
)
new_persona = result.select("answer.new_persona").to_list()[0].strip()
```

See `references/run_calibration.py` for the `build_calibration_prompt()` function that assembles this from the round's training mismatches and holdout questions.

---

## Implementation

See `references/run_calibration.py` for the complete multi-persona calibration loop. Key functions:

### Running the survey

```python
def run_survey_with_persona(persona_text):
    agent = Agent(name="calibrating", traits={"persona": persona_text})
    # Save a one-agent jobs.ep, run it through the Makefile/CLI, then load:
    results = Results.git.load("data/calibration_persona_results.ep")
    answers = {}
    for qname in ALL_QUESTION_NAMES:
        answers[qname] = results.select("answer." + qname).to_list()[0]
    return answers
```

### Judging free-text similarity

For free-text questions, an LLM judge rates semantic similarity on a 1-5 scale between the persona's response and the gold standard. The judge prompt is also injected via `Scenario`. The response is parsed as JSON with a fallback to `ast.literal_eval()`.

---

## What Works and What Doesn't

### Works well
- **Attitudinal questions** (politics, values, policy preferences): Calibrated personas significantly outperform chance on true holdout questions for both LLM targets and real humans.
- **Rapid convergence**: Typically jumps from near-zero to majority-correct in one round.
- **Rich, non-memorizing personas**: Final personas describe worldview and life circumstances, never mention specific survey answers.
- **Near-miss errors**: After the first round, mistakes are adjacent on ordinal scales ("Much worse" vs "Somewhat worse"), not category errors.

### Doesn't work well
- **Biographical facts** (income, community type, media habits): Cannot be reliably inferred from attitudes alone.
- **Atypical personas**: Cross-cutting profiles (e.g., high-income anti-capitalist) oscillate across rounds and resist stable calibration.
- **Real humans vs LLM personas**: Real people are internally inconsistent in ways LLMs are not. Expect substantially lower holdout accuracy for real respondents.

### Key finding

> LLM personas are more internally consistent than real people. When using LLM personas as proxies for human respondents, expect that real humans will be noisier, less archetypal, and harder to predict.

---

## Study Structure

```
study_root/
  edsl_jobs/job_a/
    study_survey.py       # diagnostic survey (calibration + holdout pools)
    study_agent_list.py   # target personas or blank persona
    study_model_list.py   # model configuration
    run_job.py            # initial survey run
  analysis/
    run_calibration.py    # calibration loop
    plot_convergence.py   # accuracy vs round
    plot_heatmap.py       # per-question correctness grid
  data/
    initial_results.ep
    cooked/calibration_rounds.json
  writeup/
    report.md
```

---

## Calibrating Against Human Respondents

When calibrating against real survey data (e.g., from Prolific):

1. Run the same survey on Prolific via Expected Parrot's humanize integration (see skill:edsl-human-survey).
2. Load human results: `Results.git.load("data/human_results.ep")`
3. Extract each respondent's answers and run the calibration loop per respondent.
4. Consider using fewer rounds than for LLM targets — human targets converge more slowly and noisily.
5. Save incrementally in case of crashes (many respondents × several rounds = many API calls).

See `references/run_calibration_human.py` for the human-calibration variant.

---

## Quick Reference

| Parameter | Guidance |
|-----------|----------|
| Survey | Whatever survey the user brings; partition into calibration pool and optional true holdout |
| True holdout questions | Optional; reserve some questions if the user wants an honest generalization measure |
| Train/holdout split per round | Roughly half-and-half of the structured calibration questions |
| Number of rounds | More for LLM targets (they converge fast), fewer for human targets (diminishing returns) |
| Model | Tier 1 — calibration requires strong inference about persona traits |
| Seed | Fixed per study, produces a different split each round |
| Include holdout question text? | Ask the user; no proven benefit for political/attitudinal surveys, but may help in other domains |
