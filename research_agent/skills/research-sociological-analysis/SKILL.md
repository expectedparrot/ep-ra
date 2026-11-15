---
name: research-sociological-analysis
description: >
  Analyzes a social scenario through multiple sociological theories, generates
  competing predictions, evaluates which are most likely using EDSL agent panels,
  and produces a structured report. Use when the user describes a social situation
  and wants a rigorous multi-theoretical analysis with ranked predictions.
tags: [study-type, qualitative, academic, simulation]
---

# Sociological Analysis Study

Takes a user-described social scenario and analyzes it through the lens of multiple sociological theories. Each theory produces distinct predictions about what will happen. An EDSL agent panel then evaluates the predictions for plausibility, producing a ranked assessment. The output is a standard report.

## When to Use This

- The user describes a social situation (organizational change, policy intervention, community conflict, market shift, cultural trend) and wants to understand what might happen
- The user wants to see how different theoretical frameworks lead to different conclusions about the same situation
- The user wants predictions grounded in established social science rather than intuition

This is NOT the right skill when the user wants:
- A scenario planning exercise with strategic options -> `skill:research-scenario-planning`
- A multi-agent social simulation with dialogue -> `skill:research-social-simulation`
- A general opinion survey -> `skill:research-survey`

---

## Workflow

### Phase 1: Scenario Elicitation

**Goal:** Get a clear, detailed description of the social scenario.

#### 1a. Parse the user's description

Extract:
- **The situation:** What is happening or about to happen?
- **The actors:** Who are the key individuals, groups, or organizations?
- **The context:** What institutional, cultural, economic, or historical context matters?
- **The question:** What does the user want to understand? (If implicit, make it explicit.)
- **The time horizon:** Over what period are we predicting outcomes?

#### 1b. Clarify if needed

Ask at most 2 clarifying questions. Good clarifying questions for sociological analysis:

- "Who are the key groups involved, and what are their interests?" (if actors are vague)
- "What's the institutional setting -- is this inside an organization, a community, a market, a political arena?" (if context is unclear)
- "Are you more interested in what happens to the individuals involved, or the structural/systemic outcome?" (if the level of analysis is ambiguous)

Do not ask clarifying questions that the theoretical analysis itself will answer. The point is to get enough situation detail that the theories can be applied, not to pre-determine the answer.

#### 1c. Write the scenario brief

Write a 1-2 paragraph scenario description in neutral language. This becomes the input to all subsequent analysis. Store it in `data/scenario_brief.md`.

---

### Phase 2: Theory Selection

**Goal:** Select 4-6 sociological theories that are relevant to the scenario and likely to produce meaningfully different predictions.

#### 2a. Consult the theory reference

See `references/theories.md` for the full catalog of theories with descriptions, core mechanisms, and typical predictions. The catalog is organized by level of analysis (micro, meso, macro) and by tradition.

#### 2b. Selection criteria

Choose theories that:

1. **Are relevant** -- the theory's core mechanism applies to the scenario (e.g., don't pick network theory for a scenario with no network structure)
2. **Produce divergent predictions** -- if two theories predict the same outcome for the same reasons, drop one
3. **Span levels of analysis** -- include at least one micro-level (individual behavior) and one macro-level (structural/systemic) theory
4. **Are well-established** -- stick to theories with substantial empirical support and clear predictive mechanisms

#### 2c. Standard starting set

For most scenarios, start with these and then add or swap based on relevance:

| Theory | Level | Core mechanism |
|---|---|---|
| Rational choice theory | Micro | Actors maximize expected utility given constraints and information |
| Institutional theory | Meso | Behavior is shaped by norms, rules, and taken-for-granted practices; organizations seek legitimacy |
| Social identity theory | Micro/meso | Group membership shapes perception, loyalty, and intergroup behavior |
| Field theory (Bourdieu) | Meso/macro | Actors compete for capital within structured social fields; position determines strategy |
| Structural functionalism | Macro | Social systems tend toward equilibrium; disruptions trigger compensating adjustments |
| Conflict theory | Macro | Outcomes reflect power asymmetries; dominant groups act to preserve advantage |

Swap in alternatives from `references/theories.md` when the scenario calls for it. For example:
- Network-heavy scenario -> add network theory, drop structural functionalism
- Organizational scenario -> add organizational ecology, drop social identity theory
- Cultural change scenario -> add cultural evolution / diffusion of innovations
- Technology scenario -> add actor-network theory or sociotechnical systems theory

#### 2d. Present selections to user

List the chosen theories with a one-sentence rationale for each. Ask if the user wants to add, remove, or substitute any before proceeding.

---

### Phase 3: Theoretical Analysis and Prediction Generation

**Goal:** For each selected theory, analyze the scenario and generate 2-3 specific, falsifiable predictions.

#### 3a. Analysis structure

For each theory, write:

1. **Lens** (2-3 sentences): How does this theory frame the scenario? What does it direct attention to?
2. **Mechanism** (2-3 sentences): What causal mechanism does the theory identify as driving the outcome?
3. **Predictions** (2-3 bullet points): What specific, observable outcomes does the theory predict?

#### 3b. Prediction quality standards

Each prediction must be:

- **Specific:** Names a concrete outcome, not a vague tendency. "Group X will resist the change" is too vague. "Group X will use formal grievance mechanisms to slow implementation by 6+ months" is specific.
- **Observable:** Could in principle be checked against reality. Avoid predictions about internal mental states.
- **Distinct:** Each prediction adds information. If two predictions from the same theory say the same thing differently, merge them.
- **Theory-grounded:** The prediction should follow logically from the theory's mechanism. If it's just common sense dressed in jargon, it's not adding value.

#### 3c. Identify prediction conflicts

After generating predictions from all theories, explicitly note where theories disagree. These conflicts are the most interesting part of the analysis -- they reveal where the theoretical choice actually matters.

Create a conflict table:

| Prediction from Theory A | Prediction from Theory B | Nature of conflict |
|---|---|---|
| Rational choice: Actors will defect from the coalition once costs exceed benefits | Social identity: Actors will maintain coalition loyalty even at personal cost | Opposite predictions about coalition stability |

Store the full analysis in `data/theoretical_analysis.md`.

---

### Phase 4: Prediction Assessment via EDSL

**Goal:** Use an EDSL agent panel to evaluate which predictions are most plausible, producing quantitative confidence scores and qualitative reasoning.

#### 4a. Build the agent panel

Create agents representing different analytical perspectives. These are NOT sociological theorists -- they are informed generalists who can evaluate predictions on their merits. Vary them on:

- **Epistemic style:** empiricist (weights evidence and precedent), theorist (weights logical consistency and mechanism), pragmatist (weights practical constraints and real-world dynamics)
- **Domain expertise:** relevant to the scenario (e.g., for an organizational scenario: management consultant, labor economist, organizational psychologist, industry journalist)
- **Optimism/pessimism:** include agents who are dispositionally more and less optimistic about institutional capacity, human cooperation, etc.

Aim for 8-12 agents. Each agent gets a persona instruction establishing their background and analytical style.

```python
from edsl import Agent, AgentList

agents = AgentList([
    Agent(
        name="Management Consultant",
        traits={
            "epistemic_style": "pragmatist",
            "domain": "organizational change",
            "disposition": "moderately_optimistic",
        },
        instruction="You are a management consultant with 20 years of experience advising large organizations through transformations. You are analytically rigorous but pragmatic -- you care more about what actually happens in practice than what theory predicts. You have seen many change initiatives succeed and fail, and you weight practical constraints heavily."
    ),
    # ... more agents
])
```

#### 4b. Build the survey

The survey presents the scenario brief and each prediction, asking agents to assess plausibility and provide reasoning.

```python
from edsl import (
    Survey, Scenario, ScenarioList,
    QuestionLinearScale, QuestionFreeText, QuestionMultipleChoice
)

# One scenario per prediction
scenarios = ScenarioList([
    Scenario({
        "scenario_brief": scenario_text,
        "theory_name": "Rational choice theory",
        "prediction": "Group X will defect from the coalition within 6 months as compliance costs rise above $Y.",
        "mechanism": "Members are individually rational and will exit when costs exceed benefits of membership.",
        "prediction_id": "rc_01",
    }),
    # ... one per prediction
])

q_plausibility = QuestionLinearScale(
    question_name="plausibility",
    question_text=(
        "Consider this social scenario:\n\n{{ scenario.scenario_brief }}\n\n"
        "A {{ scenario.theory_name }} analysis predicts:\n\n"
        "{{ scenario.prediction }}\n\n"
        "The proposed mechanism is: {{ scenario.mechanism }}\n\n"
        "How plausible is this prediction?"
    ),
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Very implausible", 4: "Uncertain", 7: "Very plausible"},
)

q_confidence = QuestionLinearScale(
    question_name="confidence",
    question_text="How confident are you in your plausibility assessment?",
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Not at all confident", 7: "Very confident"},
)

q_reasoning = QuestionFreeText(
    question_name="reasoning",
    question_text=(
        "In 2-3 sentences, explain why you rated this prediction as you did. "
        "What factors make it more or less plausible? What conditions would "
        "need to hold for it to come true?"
    ),
)

q_conditions = QuestionFreeText(
    question_name="conditions",
    question_text=(
        "What is the single most important condition or assumption that this "
        "prediction depends on? If that condition fails, what happens instead?"
    ),
)

survey = Survey([q_plausibility, q_confidence, q_reasoning, q_conditions])
```

#### 4c. Run the job

```python
from edsl import Model

model = Model("...")  # WebSearch + ep models — see skill:workflow-model-selection
job = survey.by(scenarios).by(agents).by(model)
# Save survey.ep, scenario_list.ep, agent_list.ep, and model_list.ep;
# build jobs.ep, then run through the Makefile/CLI.
```

This produces `n_predictions x n_agents` responses. For 15 predictions and 10 agents, that is 150 responses.

#### 4d. Save results

```bash
ep run edsl_jobs/job_a/jobs.ep --output data/cooked/prediction_assessment_results.ep
```

---

### Phase 5: Analysis

**Goal:** Rank predictions by plausibility, identify consensus and disagreement, and synthesize findings.

#### 5a. Prediction ranking

Compute mean plausibility and confidence per prediction:

```python
import pandas as pd

df = results.select(
    "scenario.prediction_id", "scenario.theory_name", "scenario.prediction",
    "answer.plausibility", "answer.confidence"
).to_pandas()

ranking = (
    df.groupby(["prediction_id", "theory_name", "prediction"])
    .agg(
        mean_plausibility=("plausibility", "mean"),
        std_plausibility=("plausibility", "std"),
        mean_confidence=("confidence", "mean"),
    )
    .sort_values("mean_plausibility", ascending=False)
    .reset_index()
)
```

#### 5b. Theory-level aggregation

Which theories produced the most plausible predictions overall?

```python
theory_scores = (
    df.groupby("theory_name")
    .agg(
        mean_plausibility=("plausibility", "mean"),
        best_prediction=("plausibility", "max"),
        worst_prediction=("plausibility", "min"),
    )
    .sort_values("mean_plausibility", ascending=False)
)
```

#### 5c. Disagreement analysis

Identify predictions where agents disagreed most (high std in plausibility). These are the most uncertain and interesting predictions. Check whether disagreement follows the epistemic_style or domain traits.

#### 5d. Conflict resolution

For each prediction conflict identified in Phase 3c, report which side the panel favored and by how much. This is the core finding: when theories disagree, which prediction does an informed panel find more plausible?

#### 5e. Generate plots

1. **Prediction ranking chart:** Horizontal bar chart of predictions sorted by mean plausibility, color-coded by theory, with error bars (SEM).
2. **Theory comparison chart:** Grouped bar chart showing mean plausibility per theory with individual prediction scores overlaid.
3. **Conflict resolution chart:** For each conflict pair, side-by-side bars showing which prediction was rated more plausible.
4. **Assessor agreement heatmap:** Predictions x agents, colored by plausibility rating. Highlights where disagreement clusters.

Save all plots to `writeup/plots/`.

---

### Phase 6: Report

Write `writeup/report.md` following the standard report conventions. Read `skill:report-authoring` before writing.

#### Report structure

```
# [Title: Sociological Analysis of <Scenario>]

## Executive Summary
- 3-4 bullet points: the scenario, most plausible predictions, which theory performed best, key insight

## 1. The Scenario
- The scenario brief (from Phase 1)
- Context and actors
- The central question

## 2. Theoretical Frameworks
- Brief description of each selected theory and why it was chosen
- Table: theory | level of analysis | core mechanism | relevance to this scenario

## 3. Theoretical Analysis and Predictions
- For each theory: lens, mechanism, predictions
- Prediction conflict table

## 4. Methodology
- How the assessment was conducted (EDSL agent panel)
- Agent panel description and trait table
- Survey instrument summary
- Model rationale
- "How this study works" explainer (if audience needs it)

## 5. Results
### 5.1 Prediction Ranking
- Ranked table of all predictions with mean plausibility and confidence
- Prediction ranking chart
- Discussion of top and bottom predictions

### 5.2 Theory Comparison
- Which theories produced the most plausible predictions?
- Theory comparison chart
- Does any single theory dominate, or do different theories win on different predictions?

### 5.3 Points of Disagreement
- Where did theories conflict, and which side did the panel favor?
- Conflict resolution chart
- Where did assessors disagree with each other, and why?

## 6. Synthesis
- What is the most likely outcome, integrating across theories?
- What conditions or assumptions are the predictions most sensitive to?
- What would a blended prediction look like, drawing on the strongest elements of each theory?

## 7. Limitations
- Standard AI simulation caveats
- The panel assesses plausibility, not probability -- these are informed judgments, not calibrated forecasts
- Theory selection is not exhaustive
- Predictions are point-in-time; social dynamics may shift

## Appendix A: Survey Instrument
## Appendix B: Agent Panel Configuration
## Appendix C: Full Prediction Assessment Data
```

---

## Facilitation Notes

- **Do not let theory selection become a literature review.** The goal is 4-6 relevant theories applied to a concrete situation, not a survey of all of sociology. If the user asks for more theories, push back gently -- adding theories past 6 rarely changes the conclusions and increases cost.

- **Predictions should be surprising.** If every theory predicts the same obvious outcome, the analysis is not doing useful work. Look for theories that predict counterintuitive or conflicting outcomes. If the initial selection produces consensus, swap in a theory that will disagree.

- **The conflict table is the most valuable output.** Users who describe a social scenario usually have an intuitive prediction already. The value of multi-theoretical analysis is showing them where that intuition might be wrong and why. Highlight the conflicts prominently.

- **Keep the scenario brief neutral.** Do not embed assumptions about the outcome in the scenario description. "The company announced layoffs, which will likely damage morale" is biased. "The company announced layoffs affecting 15% of the workforce" is neutral.

- **Agent panel diversity matters more than size.** 8-10 well-differentiated agents with distinct epistemic styles produce more useful variance than 20 similar agents.
