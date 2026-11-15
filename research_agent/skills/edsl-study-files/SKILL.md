---
name: edsl-study-files
description: >
  Templates for the standard EDSL study files — survey, scenarios, agents, models, CLI-built jobs, and Makefile-run results.
  Use when setting up a new EDSL study job directory or reviewing file conventions.
tags: [edsl, reference, data-collection]
---

`ep study scaffold` creates job directories but does not pre-create EDSL
source files. Write each new study file directly. If a target file already
exists, read it first and preserve unrelated work.

# EDSL Study File Templates

Reference for the standard files in an EDSL study job directory. Each Python file exports a named object and, when run as a script, saves the object in the EDSL `.ep` file format with `obj.git.save(...)`. The Makefile then builds `jobs.ep` from those object files with `ep jobs build` and creates `results.ep` with `ep run`. Do not call `job.run()` inside Python study files.

| File | Purpose | Exports |
|------|---------|---------|
| `study_survey.py` | Defines questions and survey with rules/memory | `survey` |
| `study_scenario_list.py` | Defines scenario variations | `scenario_list` |
| `study_agent_list.py` | Defines respondent personas | `agent_list` |
| `study_model_list.py` | Optional complex model construction; prefer `ep models create` | `model_list` |
| `Makefile` | Builds `jobs.ep` and runs `ep run edsl_jobs/job_a/jobs.ep --output data/results.ep` | `edsl_jobs/job_a/jobs.ep`, `data/results.ep` |

## `study_survey.py`

Defines and exports a `survey` object. Read `research_agent/skills/edsl-surveys/SKILL.md` for the full question type reference.

```python
from edsl import (
    Survey,
    QuestionMultipleChoice,
    QuestionFreeText,
    QuestionLinearScale,
)

q_cuisine = QuestionMultipleChoice(
    question_name="favorite_cuisine",
    question_text="Which cuisine do you enjoy most?",
    question_options=["Italian", "Japanese", "Mexican", "Indian", "Thai"]
)

q_dish = QuestionFreeText(
    question_name="favorite_dish",
    question_text="What is your favorite {{ favorite_cuisine.answer }} dish?"
)

q_frequency = QuestionLinearScale(
    question_name="frequency",
    question_text="How often do you eat {{ favorite_cuisine.answer }} food?",
    question_options=[1, 2, 3, 4, 5],
    option_labels={1: "Rarely", 5: "Very Often"}
)

q_why = QuestionFreeText(
    question_name="why",
    # When piping an answer that would be ambiguous on its own, restate the
    # original question and options so the LLM has full context.
    question_text="You were previously asked 'Which cuisine do you enjoy most?' "
    "(Italian, Japanese, Mexican, Indian, Thai) and you said "
    "'{{ favorite_cuisine.answer }}'. What draws you to that cuisine?"
)

# No memory mode needed here: follow-up questions reference q_cuisine's answer
# directly via piping ({{ favorite_cuisine.answer }}), which is the preferred approach.
# If a follow-up must repeat once per item of a *list* answer (e.g. they name several
# cuisines and you want the same 2 questions about each), use
# Survey([...]).loop_over("cuisines", ask=[...], max_items=N) — see skill:edsl-surveys.
# Only add a memory mode when questions genuinely need context that piping cannot provide
# — and only for agent .run() jobs. Humanize surveys use piping, not memory APIs.
# See research_agent/skills/edsl-surveys/SKILL.md — Survey Memory System — and skill:edsl-human-survey.
survey = Survey([q_cuisine, q_dish, q_frequency, q_why])

if __name__ == "__main__":
    survey.git.save("survey.ep")
```

## `study_scenario_list.py`

Defines and exports a `scenario_list`. If no scenarios are needed, export an empty `ScenarioList`.

> **IMPORTANT**: Every field in your `ScenarioList` must be referenced in at least one **question's `question_text`** using `{{ scenario.field_name }}` syntax, or EDSL will raise a `JobsCompatibilityError`. For example, a scenario with key `"topic"` needs a question containing `{{ scenario.topic }}`. Note: `Instruction` text does NOT count — only `question_text` satisfies this requirement.

> **Experimental conditions belong in scenarios, not in agent list chunking.** When an experiment has treatment arms (e.g., different framings, prices, stimuli), put the treatment as a scenario field and let EDSL cross all agents with all conditions. Do not split the agent list into subsets and run each subset against a different condition — this confounds agent traits with treatments and produces biased results.

```python
from edsl import Scenario, ScenarioList

scenario_list = ScenarioList([
    Scenario({"topic": "artificial intelligence"}),
    Scenario({"topic": "climate change"}),
])

if __name__ == "__main__":
    scenario_list.git.save("scenario_list.ep")
```

When no scenarios are needed:
```python
from edsl import ScenarioList
scenario_list = ScenarioList()

if __name__ == "__main__":
    scenario_list.git.save("scenario_list.ep")
```

## `study_agent_list.py`

Defines and exports an `agent_list`. Read `research_agent/skills/edsl-agent-lists/SKILL.md` for creation patterns (from CSV, DataFrame, combinations, etc.).

> **IMPORTANT**: `name` is a reserved keyword for `Agent()`. Use `Agent(name='...', traits={...})` — never put `name` inside the `traits` dict. Putting `name` in traits will raise `AgentNameError`.

```python
from edsl import Agent, AgentList

agent_list = AgentList([
    Agent(traits={"persona": "health-conscious millennial", "age": 28}),
    Agent(traits={"persona": "traditional home cook", "age": 55}),
])

if __name__ == "__main__":
    agent_list.git.save("agent_list.ep")
```

When no agents are needed:
```python
from edsl import AgentList
agent_list = AgentList()

if __name__ == "__main__":
    agent_list.git.save("agent_list.ep")
```

## `study_model_list.py`

Defines and exports a `model_list` specifying which LLMs to use.

**Before writing this file, read `research_agent/skills/workflow-model-selection/SKILL.md`.** Model choice is a research design decision — discuss it with the user, match the model tier to the task complexity and purpose, and confirm the current model name using WebSearch + `ep models`. Do not silently default to any single model.

For an ordinary one- or multi-model list, skip Python and create the artifact
directly after confirming current model names:

```bash
ep models create \
  --model "<confirmed-model-name>" \
  --output edsl_jobs/job_a/model_list.ep
```

Use `study_model_list.py` only when model-specific parameters or programmatic
configuration cannot be expressed by `ep models create --model-spec` or its
documented parameter flags.

The `.git.save(filename)` method writes an EDSL `.ep` file. Use clear object filenames:
`survey.ep`, `scenario_list.ep`, `agent_list.ep`, `model_list.ep`, `jobs.ep`, and `results.ep`.

## Makefile Targets

The Makefile creates source objects, then creates results by invoking the EDSL CLI:

```make
.PHONY: data inspect edsl-objects

data: data/results.ep

edsl-objects: \
	edsl_jobs/job_a/survey.ep \
	edsl_jobs/job_a/scenario_list.ep \
	edsl_jobs/job_a/agent_list.ep \
	edsl_jobs/job_a/model_list.ep \
	edsl_jobs/job_a/jobs.ep

edsl_jobs/job_a/survey.ep: edsl_jobs/job_a/study_survey.py
	cd edsl_jobs/job_a && python study_survey.py

edsl_jobs/job_a/scenario_list.ep: edsl_jobs/job_a/study_scenario_list.py
	cd edsl_jobs/job_a && python study_scenario_list.py

edsl_jobs/job_a/agent_list.ep: edsl_jobs/job_a/study_agent_list.py
	cd edsl_jobs/job_a && python study_agent_list.py

edsl_jobs/job_a/model_list.ep: edsl_jobs/job_a/study_model_list.py
	cd edsl_jobs/job_a && python study_model_list.py

edsl_jobs/job_a/jobs.ep: \
	edsl_jobs/job_a/survey.ep \
	edsl_jobs/job_a/scenario_list.ep \
	edsl_jobs/job_a/agent_list.ep \
	edsl_jobs/job_a/model_list.ep
	ep jobs build \
		--survey edsl_jobs/job_a/survey.ep \
		--agents edsl_jobs/job_a/agent_list.ep \
		--scenarios edsl_jobs/job_a/scenario_list.ep \
		--models edsl_jobs/job_a/model_list.ep \
		--output edsl_jobs/job_a/jobs.ep

data/results.ep: edsl_jobs/job_a/jobs.ep
	mkdir -p data
	@if test -s "$@"; then \
		echo "Existing results preserved: $@"; \
	else \
		ep run edsl_jobs/job_a/jobs.ep \
			--remote_inference_description "<topic - panel size>" \
			--results_description "<topic - panel size>" \
			--output data/results.ep; \
	fi

# Read-only: consumes saved results and never invokes ep run.
inspect: data/results.ep
	ep results review data/results.ep
```

For asynchronous remote runs, split submission and retrieval:

```bash
ep run edsl_jobs/job_a/jobs.ep --background
ep jobs results <job_uuid> --output data/results.ep
```

Or wait in the Makefile target:

```bash
ep run edsl_jobs/job_a/jobs.ep --background --wait --output data/results.ep
```

Do not use `--background --output` without `--wait`; the CLI rejects it because results do not exist yet.

### Checking balance

If a user asks about their credit balance, or if a job fails with `"insufficient funds"`, check it with:

```bash
ep balance
```

Tell the user their current balance and let them know they can add credits at [expectedparrot.com](https://www.expectedparrot.com).

### Logging cost after a run

Before the run, estimate cost with:

```bash
ep jobs cost edsl_jobs/job_a/jobs.ep
```

After `ep run` completes, log the actual cost from `data/results.ep` so you can calibrate future estimates:

```bash
ep costs log --output costs.jsonl --actual-from data/results.ep --note "full run"
```

This appends a line to `costs.jsonl` in the study root with timestamp, costs, and the estimated/actual ratio.

> **IMPORTANT**: Do not add Python preview code. Inspect the saved artifact with
> Start with bounded `ep results review`; use `select`, `values`, or `first`
> only for a concrete follow-up.

## Working with Results

After running a job, inspect it with CLI commands. Discover the exact schema
before selecting columns; do not guess flattened names.

```bash
ep results review data/results.ep
ep results select --file data/results.ep \
  --column scenario.message_frame \
  --column answer.q_support \
  --limit 5
ep results values data/results.ep --column answer.q_support
ep results first data/results.ep --column answer.q_support
```

Column name prefixes:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `answer.<question_name>` | Response to each question | `answer.q_support` |
| `scenario.<field>` | Scenario field values | `scenario.message_frame` |
| `agent.<trait>` | Agent trait values | `agent.age` |
| `model.model` | Which model produced the response | `model.model` |

### Accessing a single Result in substantive analysis

`results[i]` returns a `Result` object. Access fields through `sub_dicts`, NOT
with dot-separated string keys:

```python
sample = results[0]
sample.sub_dicts['scenario']['message_frame']  # correct
sample.sub_dicts['answer']['q_support']        # correct
sample.combined_dict['message_frame']          # also works (flat, no prefix)

# WRONG — raises KeyError:
# sample['scenario.message_frame']
```

The snippet above belongs inside an analysis script that already needs Python.
Do not create a script solely to display or extract that value; use
`ep results first` or `ep results select` instead.

## Running

Run the EDSL job via the Makefile. The Makefile should call `ep run ... --output data/results.ep`:
```
make data
make inspect
```

**Never run EDSL jobs as inline Bash or Python commands.** All EDSL code — survey construction, agent lists, scenario lists, model lists, Jobs construction, and results generation — must be written to study files or Makefile targets and executed via `make data`. The paid model run should happen through the Makefile's `ep run ... --output data/results.ep` target so it is reproducible and re-runnable.

`make inspect` is read-only and must depend on the saved results artifact. It
must never invoke `ep run`, directly or through another dependency.
The `data/results.ep` recipe must preserve an existing non-empty result even if
Make considers the target stale. A new paid run requires an explicit user-approved
refresh that first archives the prior result.
