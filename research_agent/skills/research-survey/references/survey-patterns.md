# Survey patterns reference

## Contents

- Common survey archetypes
- Survey design principles
- Agent panel design
- Running the study
- Analysis patterns
- Memory and scenario guidance
- Image scenarios
- Quick reference

Use this workflow for the common case: the user wants to survey AI agent panels on a topic and the study does not fit a specialized template.

## When to Use This vs. Specialized Skills

| If the user wants to... | Use this skill instead |
|---|---|
| Test message/copy variants | `skill:research-message-testing` |
| Compare product concepts | `skill:research-concept-testing` |
| Measure feature trade-offs (conjoint) | `skill:research-conjoint` |
| Find optimal price points | `skill:research-price-tiering` |
| Get website, interface, screenshot, or design feedback | `skill:research-ux-testing` |
| Attitudes, opinions, awareness, satisfaction, NPS, exploratory | **This skill** |

---

## Common Survey Archetypes

### 1. Opinion Poll

What do people think about X? Use linear scales for agreement and free text for reasoning.

```python
from edsl import Survey, QuestionLinearScale, QuestionFreeText, QuestionMultipleChoice

q_support = QuestionLinearScale(
    question_name="support_level",
    question_text="How much do you support {{ scenario.policy }}?",
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Strongly oppose", 4: "Neutral", 7: "Strongly support"},
)
q_importance = QuestionLinearScale(
    question_name="importance",
    question_text="How important is {{ scenario.policy }} to you personally?",
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Not at all important", 7: "Extremely important"},
)
q_impact = QuestionMultipleChoice(
    question_name="expected_impact",
    question_text="What impact do you think {{ scenario.policy }} would have on your community?",
    question_options=["Very positive", "Somewhat positive", "No impact", "Somewhat negative", "Very negative"],
)
q_reasoning = QuestionFreeText(
    question_name="reasoning",
    question_text="In 2-3 sentences, explain why you feel this way about {{ scenario.policy }}.",
)

survey = Survey([q_support, q_importance, q_impact, q_reasoning])
```

### 2. Satisfaction / NPS

How satisfied are users with X? Use a 0-10 scale for NPS and multiple choice for drivers.

```python
from edsl import Survey, QuestionLinearScale, QuestionMultipleChoice, QuestionFreeText

q_nps = QuestionLinearScale(
    question_name="recommend_score",
    question_text="On a scale of 0 to 10, how likely are you to recommend {{ scenario.product }} to a friend or colleague?",
    question_options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    option_labels={0: "Not at all likely", 10: "Extremely likely"},
)
q_satisfaction = QuestionLinearScale(
    question_name="overall_satisfaction",
    question_text="How satisfied are you with {{ scenario.product }} overall?",
    question_options=[1, 2, 3, 4, 5],
    option_labels={1: "Very dissatisfied", 3: "Neutral", 5: "Very satisfied"},
)
q_drivers = QuestionMultipleChoice(
    question_name="primary_driver",
    question_text="What is the single biggest factor driving your satisfaction (or dissatisfaction) with {{ scenario.product }}?",
    question_options=["Price/value", "Quality/reliability", "Customer service", "Ease of use", "Features", "Brand trust"],
)
q_improve = QuestionFreeText(
    question_name="improvement",
    question_text="What one change would most improve your experience with {{ scenario.product }}?",
)

survey = Survey([q_nps, q_satisfaction, q_drivers, q_improve])
```

**NPS classification**: Promoters (9-10), Passives (7-8), Detractors (0-6). NPS = % Promoters - % Detractors.

### 3. Awareness / Perception

What do people know about X? Use multiple choice for aided awareness and free text for unaided associations.

```python
from edsl import Survey, QuestionMultipleChoice, QuestionFreeText, QuestionLinearScale

q_unaided = QuestionFreeText(
    question_name="unaided_associations",
    question_text="When you think of {{ scenario.category }}, what brands or products come to mind first? List up to three.",
)
q_aided = QuestionMultipleChoice(
    question_name="aided_awareness",
    question_text="Have you heard of {{ scenario.brand }}?",
    question_options=["Yes, I use it regularly", "Yes, I have tried it", "Yes, but I have never tried it", "No, I have not heard of it"],
)
q_perception = QuestionLinearScale(
    question_name="brand_perception",
    question_text="How would you rate your overall perception of {{ scenario.brand }}?",
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Very negative", 4: "Neutral", 7: "Very positive"},
)
q_associations = QuestionFreeText(
    question_name="brand_associations",
    question_text="What three words best describe {{ scenario.brand }} to you?",
)

survey = Survey([q_unaided, q_aided, q_perception, q_associations])
```

### 4. Exploratory / Attitudinal

How do different segments feel about a complex topic? Mix scales, MC, and free text.

```python
from edsl import Survey, QuestionLinearScale, QuestionMultipleChoice, QuestionFreeText

q_agree = QuestionLinearScale(
    question_name="agreement",
    question_text="To what extent do you agree: {{ scenario.statement }}",
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Strongly disagree", 4: "Neither agree nor disagree", 7: "Strongly agree"},
)
q_framing = QuestionMultipleChoice(
    question_name="framing",
    question_text="Which framing best matches your view on {{ scenario.topic }}?",
    question_options=["Individual rights issue", "Public health issue", "Economic issue", "Moral/ethical issue", "Not sure"],
)
q_priority = QuestionLinearScale(
    question_name="priority",
    question_text="How high a priority should {{ scenario.topic }} be for policymakers?",
    question_options=[1, 2, 3, 4, 5],
    option_labels={1: "Not a priority", 5: "Top priority"},
)
q_explain = QuestionFreeText(
    question_name="explanation",
    question_text="Explain the reasoning behind your views on {{ scenario.topic }} in 2-3 sentences.",
)

survey = Survey([q_agree, q_framing, q_priority, q_explain])
```

---

## Survey Design Principles

1. **Question order**: general before specific, factual before opinion, easy before hard. Start with broad attitude questions, then drill into specifics.
2. **Scale consistency**: pick one scale width (5-point or 7-point) and use it for all Likert-type items in the same survey. Mixing widths confuses analysis.
3. **Avoid double-barreled questions**: "Do you like the price and quality?" should be two separate questions.
4. **Balance framing**: include both positively and negatively worded items to detect acquiescence bias (tendency to agree with everything).
5. **Keep surveys short**: aim for 8-12 questions, maximum 15. Longer surveys produce lower-quality responses from AI agents.
6. **One construct per question**: each question should measure exactly one thing.
7. **Anchor your scales**: always use `option_labels` on `QuestionLinearScale` to label at least the endpoints and midpoint.

---

## Agent Panel Design for Surveys

The panel should vary the dimensions most likely to produce meaningfully different responses.

### By archetype

| Archetype | Key traits to vary |
|---|---|
| Opinion poll | Demographics (age, gender, education), political lean, region, ideology |
| Satisfaction / NPS | Usage intensity, customer tenure, segment (enterprise/SMB/consumer) |
| Awareness / perception | Category familiarity, media consumption, age cohort |
| Exploratory | Whichever dimensions are most likely to reveal different perspectives on the topic |

### Example: 20-agent US voter panel for a policy opinion poll

```python
from edsl import Agent, AgentList

panel_specs = [
    {"persona": "Young progressive urban professional", "age": 28, "political_lean": "liberal", "education": "college", "region": "Northeast"},
    {"persona": "Retired conservative from a rural area", "age": 68, "political_lean": "conservative", "education": "high_school", "region": "South"},
    {"persona": "Suburban moderate parent", "age": 42, "political_lean": "moderate", "education": "college", "region": "Midwest"},
    {"persona": "Urban minority small business owner", "age": 35, "political_lean": "moderate", "education": "some_college", "region": "West"},
    {"persona": "College student interested in politics", "age": 20, "political_lean": "liberal", "education": "in_college", "region": "Northeast"},
    {"persona": "Blue-collar union worker", "age": 50, "political_lean": "moderate", "education": "trade_school", "region": "Midwest"},
    {"persona": "Evangelical Christian homemaker", "age": 45, "political_lean": "conservative", "education": "college", "region": "South"},
    {"persona": "Tech industry libertarian", "age": 32, "political_lean": "libertarian", "education": "graduate", "region": "West"},
    {"persona": "Retired military veteran", "age": 62, "political_lean": "conservative", "education": "some_college", "region": "South"},
    {"persona": "Academic researcher at a public university", "age": 55, "political_lean": "liberal", "education": "graduate", "region": "Northeast"},
    {"persona": "Rural farmer and landowner", "age": 58, "political_lean": "conservative", "education": "high_school", "region": "Midwest"},
    {"persona": "Single mother working in healthcare", "age": 38, "political_lean": "moderate", "education": "college", "region": "South"},
    {"persona": "First-generation immigrant entrepreneur", "age": 40, "political_lean": "moderate", "education": "college", "region": "West"},
    {"persona": "Young Black activist and community organizer", "age": 26, "political_lean": "liberal", "education": "college", "region": "South"},
    {"persona": "Wealthy suburban retiree", "age": 70, "political_lean": "moderate", "education": "graduate", "region": "Northeast"},
    {"persona": "Gig economy worker without benefits", "age": 29, "political_lean": "liberal", "education": "some_college", "region": "West"},
    {"persona": "Small-town police officer", "age": 44, "political_lean": "conservative", "education": "some_college", "region": "Midwest"},
    {"persona": "Environmental nonprofit director", "age": 48, "political_lean": "liberal", "education": "graduate", "region": "West"},
    {"persona": "Latino construction worker and family man", "age": 36, "political_lean": "moderate", "education": "high_school", "region": "South"},
    {"persona": "Appalachian coal country resident", "age": 52, "political_lean": "conservative", "education": "high_school", "region": "South"},
]

agent_list = AgentList([Agent(traits=spec) for spec in panel_specs])
```

> **Sizing the panel:** Ask: (1) How many segments do I need to compare? (2) Do I need within-segment variation, or just between-segment differences? For most surveys: 3-5 agents per segment gives enough within-segment consistency checking. If you have 4 segments → 12-20 agents. If segments aren't relevant (single population, no cross-tabs) → 10-15 agents covering the trait range. Pilot with 1-2 per segment first to verify differentiation.

> **Matching population demographics**: The above panel covers key segments but doesn't match census proportions (we have equal numbers of liberal/moderate/conservative agents, even though the US population skews differently). This is fine for detecting *patterns* — we'll see if liberals and conservatives respond differently. If you need census-matched *point estimates* ("X% of Americans support..."), use post-hoc weighting (apply census weights when computing aggregates) or mixture calibration (`skill:methods-calibrating-agents`).

---

## Running the Study

Follow the standard EDSL study workflow:

1. **Preview**: run 2-3 scenarios against 3-5 agents to verify question wording and response quality.
2. **Check**: do scores vary across agents and scenarios? Are free-text answers substantive?
3. **Estimate cost**: after `jobs.ep` exists, run `ep jobs cost edsl_jobs/job_a/jobs.ep` before the full panel.
4. **Run**: `ep run edsl_jobs/job_a/jobs.ep --remote_inference_description "..." --results_description "..." --output data/results.ep` — **always pass both descriptions, set to the same string; don't omit them** (rationale → `skill:edsl-surveys`, "Running a survey — labeling the job").
5. **Validate and inspect**: run `ep results summary data/results.ep` and
   `ep results columns --file data/results.ep`; then load Results in an analysis
   script only if substantive analysis requires Python.

```python
from edsl import Model, ModelList, ScenarioList, Scenario

# Scenarios for topic rotation (if applicable)
scenario_list = ScenarioList([
    Scenario({"policy": "Universal basic income"}),
    Scenario({"policy": "Carbon tax on fossil fuels"}),
    Scenario({"policy": "Free public university tuition"}),
])

model_list = ModelList([Model("...")])  # confirm current model via ep models

# Save survey.ep, scenario_list.ep, agent_list.ep, and model_list.ep from their
# study files. The Makefile builds jobs.ep and runs the results target.
```

```bash
# Preview or full run should be Makefile/CLI-driven, not an inline job.run().
ep jobs build \
  --survey edsl_jobs/job_a/survey.ep \
  --scenarios edsl_jobs/job_a/scenario_list.ep \
  --agents edsl_jobs/job_a/agent_list.ep \
  --models edsl_jobs/job_a/model_list.ep \
  --output edsl_jobs/job_a/jobs.ep

ep run edsl_jobs/job_a/jobs.ep \
  --remote_inference_description "Policy support - UBI carbon tax tuition - 150 agents" \
  --results_description "Policy support - UBI carbon tax tuition - 150 agents" \
  --output data/results.ep
```

```bash
ep results head data/results.ep \
  --column scenario.policy \
  --column agent.persona \
  --column answer.support_level \
  --column answer.importance \
  --column answer.reasoning \
  --rows 10
```

---

## Analysis Patterns

### Distribution plots

Stacked horizontal bar charts work well for Likert items. Group by scenario or agent segment.

```python
import pandas as pd

df = results.select(
    "scenario.policy", "agent.political_lean",
    "answer.support_level", "answer.importance"
).to_pandas()
```

### Cross-tabulation by segment

```python
cross_tab = df.groupby(["scenario.policy", "agent.political_lean"])["answer.support_level"].mean().unstack()
```

### NPS calculation

```python
def classify_nps(score):
    if score >= 9:
        return "Promoter"
    elif score >= 7:
        return "Passive"
    else:
        return "Detractor"

df["nps_category"] = df["answer.recommend_score"].apply(classify_nps)
nps_by_segment = df.groupby("agent.segment")["nps_category"].value_counts(normalize=True).unstack()
```

### Free-text thematic analysis

For surveys with `QuestionFreeText` responses, use `skill:methods-thematic-analysis` to identify recurring themes across agent segments.

### Agreement/disagreement heatmaps

Create a matrix of mean agreement scores: rows = topics/statements, columns = agent segments. Use `seaborn.heatmap()` with a diverging colormap centered on the scale midpoint.

---

## Memory Mode Guidance

**Default to no memory.** Most survey questions measure independent constructs and should not see prior answers.

- **No memory** (default): use for standard surveys where each question stands alone.
- **Piping**: use `{{ question_name.answer }}` in `question_text` when a follow-up needs one specific prior answer (e.g., "You said you support X. Why?").
- **Looping** (`Survey.loop_over`): use when follow-ups must repeat once *per item* of a list answer rather than once about the list as a whole — respondent lists their brands, then you ask 2 questions about each. Requires a `max_items` cap.
- **Full memory**: only for true conversational surveys where every prior exchange shapes the next answer. This is rare in general surveys.

See `skill:edsl-surveys` for the full memory mode decision guide.

---

## Scenario Usage

### When to use scenarios

- **Topic rotation**: same questions about different subjects (e.g., attitudes toward 5 different policies). Each policy becomes a scenario.
- **Vignette studies**: same questions after reading different descriptions. Each vignette becomes a scenario.
- **Stimulus testing**: same evaluation questions for different stimuli. Each stimulus becomes a scenario.

### When NOT to use scenarios

- **Single-topic surveys**: if the survey is about one fixed topic, do not create scenarios. Hardcode the topic in `question_text`.

### Scenario example: topic rotation

```python
from edsl import Scenario, ScenarioList

scenario_list = ScenarioList([
    Scenario({"topic": "Climate change policy", "statement": "The government should prioritize reducing carbon emissions over economic growth."}),
    Scenario({"topic": "Healthcare policy", "statement": "Healthcare should be provided as a universal public service."}),
    Scenario({"topic": "Education policy", "statement": "College tuition should be free at public universities."}),
])
```

> **IMPORTANT**: every field in the ScenarioList must appear in at least one question's `question_text` as `{{ scenario.field_name }}`, or EDSL raises `JobsCompatibilityError`. See `skill:edsl-quirks`.

### Image Scenarios

When the user provides an image (logo, design, screenshot, product photo, advertisement, etc.) and wants agent reactions, **use the actual image** via `Scenario.from_image()`:

```python
from edsl import Scenario, ScenarioList

# User provided: logo.png
scenario = Scenario.from_image("logo.png")
img_key = list(scenario.keys())[0]
scenario_list = ScenarioList([Scenario({"logo": scenario[img_key]})])
```

Then pass `{{ scenario.logo }}` to **every question** that needs agents to see the image:

```python
q1 = QuestionLinearScale(
    question_name="first_impression",
    question_text="Please look at this logo: {{ scenario.logo }}\n\nWhat is your first impression (1-7)?",
    question_options=[1, 2, 3, 4, 5, 6, 7],
    option_labels={1: "Very negative", 7: "Very positive"},
)

q2 = QuestionFreeText(
    question_name="style",
    question_text="Looking at this logo: {{ scenario.logo }}\n\nDescribe the visual style in 2-3 sentences.",
)
```

**CRITICAL**: LLMs have no cross-question memory. If you omit `{{ scenario.logo }}` from Q2, Q3, etc., those questions will not see the image. See `skill:edsl-scenario-lists` for details.

**When to use text descriptions instead**:
- The model doesn't support vision (rare — check the `works_with_images` field from `ep models` first)
- The research design specifically studies reactions to *verbal descriptions* of visuals (not reactions to the visuals themselves)
- The user explicitly requests a description-based approach

**If you consider using a description instead of a user-provided image**, you MUST:
1. Discuss this with the user BEFORE writing the plan
2. Explain why you're considering it (technical limitation? design rationale?)
3. Show them what the description would say
4. Get explicit approval
5. Document the choice in the Methods section of the plan

**Never silently substitute** a text description for a user-provided image. This fundamentally changes what the study measures (reactions to your interpretation vs. reactions to the actual visual). The user gave you an image because they want agents to react to the image.

---

## Quick Reference

| Task | Code |
|------|------|
| Linear scale (7-point) | `QuestionLinearScale(question_name="q", question_text="...", question_options=[1,2,3,4,5,6,7], option_labels={1: "Low", 7: "High"})` |
| NPS scale (0-10) | `QuestionLinearScale(question_name="nps", question_text="...", question_options=list(range(11)), option_labels={0: "Not likely", 10: "Extremely likely"})` |
| Multiple choice | `QuestionMultipleChoice(question_name="q", question_text="...", question_options=["A", "B", "C"])` |
| Free text | `QuestionFreeText(question_name="q", question_text="...")` |
| Build agent panel | `AgentList([Agent(traits={...}) for spec in specs])` |
| Define scenarios | `ScenarioList([Scenario({"topic": t}) for t in topics])` |
| Preview run | `ep run edsl_jobs/job_a/jobs.ep --remote_inference_description "... - preview" --results_description "... - preview" --output data/results_preview.ep` |
| Full run | `ep run edsl_jobs/job_a/jobs.ep --remote_inference_description "..." --results_description "..." --output data/results.ep` |
| Save results | `ep run ... --output data/results.ep` |
| Inspect results | `ep results summary data/results.ep` |
| To pandas | `results.select("scenario.*", "answer.*").to_pandas()` |
| Estimate cost | `job.estimate_remote_job_cost()` — see `skill:edsl-surveys-cost` |
