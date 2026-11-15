---
name: methods-prompt-optimization
description: >
  Optimize prompts and text artifacts using GEPA's LLM-guided Pareto-efficient evolutionary search, powered by EDSL.
  Use when the user wants to iteratively optimize a prompt, message, or text artifact using automated LLM evaluation.
tags: [methods, edsl, quantitative, external-tool]
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
arguments: optimization_goal
---

# Prompt Optimization with GEPA

This skill helps you set up and run prompt/text optimization using [GEPA](https://github.com/gepa-ai/gepa) (Genetic-Pareto), an LLM-based optimization framework. This fork uses [EDSL](https://docs.expectedparrot.com/) as the LLM backend, providing built-in caching, rate-limiting, and remote inference.

> **Model names in the examples below** are the placeholders `TASK_MODEL` and `REFLECTION_MODEL` (defined in the first example). GEPA takes two models: a cheap/fast one that runs the task many times, and a stronger one that proposes improvements. Resolve both to current names per `skill:workflow-model-selection` — do not copy a literal model name out of these snippets.

## Installation

Install GEPA from the Expected Parrot fork (which includes EDSL integration). **Do NOT use `[full]` extras** — that pulls in litellm, which prevents the EDSL fallback:

```bash
# CORRECT — EDSL backend will be used
pip install "gepa @ git+https://github.com/expectedparrot/gepa.git@edsl-backend"

# WRONG — litellm gets installed, make_lm() uses litellm instead of EDSL
pip install "gepa[full] @ git+https://github.com/expectedparrot/gepa.git@edsl-backend"
```

If litellm is already installed, `make_lm()` will silently use it instead of EDSL. To fix: `pip uninstall litellm` or reinstall gepa without `[full]`.

EDSL is owned by the ep-agent runtime. Do not install or upgrade it during a
study. Verify it with `python3 -c "import edsl"`; if that fails, report the
environment problem rather than mutating the sandbox.

Set your Expected Parrot API key:

```bash
export EXPECTED_PARROT_API_KEY="your-key-here"
```

GEPA will automatically use EDSL as the LLM backend when litellm is not installed. No separate API keys are needed.

## When to Use GEPA

Use GEPA when:
- You have a prompt or text artifact that could be improved
- You can define an evaluator that scores candidate texts
- You want interpretable, LLM-guided optimization (not random mutation)
- You have limited evaluation budget (100-500 calls, not thousands)
- You need to optimize across multiple objectives simultaneously

## Two Main APIs

### 1. `gepa.optimize()` -- Prompt Optimization

For optimizing system prompts in chat-based tasks where you have input/answer pairs.

```python
import gepa

# Confirm current model names first (see skill:workflow-model-selection);
# these are placeholders, not recommendations.
TASK_MODEL = "<task-model>"              # cheap/fast: runs the task many times
REFLECTION_MODEL = "<reflection-model>"  # stronger: proposes prompt improvements

trainset = [
    {"input": "What is 2+2?", "answer": "4", "additional_context": {}},
    {"input": "What is the capital of France?", "answer": "Paris", "additional_context": {}},
]

valset = [
    {"input": "What is 3*7?", "answer": "21", "additional_context": {}},
]

seed_prompt = {"system_prompt": "You are a helpful assistant. Answer concisely."}

result = gepa.optimize(
    seed_candidate=seed_prompt,
    trainset=trainset,
    valset=valset,
    task_lm=TASK_MODEL,          # confirm current names; see skill:workflow-model-selection
    reflection_lm=REFLECTION_MODEL,
    max_metric_calls=50,
)

print("Best prompt:", result.best_candidate["system_prompt"])
```

Key parameters:
- `seed_candidate`: `dict[str, str]` mapping component names to initial text
- `trainset` / `valset`: lists of dicts with `"input"`, `"answer"`, and `"additional_context"` keys
- `task_lm`: model string for running the task (a cheap/fast current model is usually right)
- `reflection_lm`: model string for the reflection/mutation step
- `max_metric_calls`: evaluation budget

### 2. `optimize_anything()` -- Universal Text Optimization

For optimizing any text artifact with a custom evaluator. More flexible than `optimize()`.

```python
from gepa.optimize_anything import (
    optimize_anything,
    GEPAConfig,
    EngineConfig,
    ReflectionConfig,
)

def evaluate(candidate: str, example: dict | None = None) -> tuple[float, dict]:
    """Score a candidate prompt on a single example.

    NOTE: In single-task mode (dataset=None, valset=None), GEPA calls
    the evaluator WITHOUT an example argument. Always make `example`
    optional with a default of None.
    """
    # Run your system with the candidate
    output = my_system(candidate, example["input"] if example else candidate)
    score = 1.0 if example and example["answer"] in output else 0.0
    return score, {"output": output}

result = optimize_anything(
    seed_candidate="Solve the problem step by step.",
    evaluator=evaluate,
    dataset=trainset,
    valset=valset,
    objective="Maximize accuracy on math problems",
    config=GEPAConfig(
        engine=EngineConfig(
            max_metric_calls=100,
            run_dir="outputs/my_optimization",
            parallel=True,
            max_workers=8,
        ),
        reflection=ReflectionConfig(
            reflection_lm=REFLECTION_MODEL,
        ),
    ),
)

print("Best candidate:", result.best_candidate)
```

**Three optimization modes** (determined by `dataset` / `valset`):

1. **Single-Task** (`dataset=None, valset=None`): Solve one hard problem. The candidate *is* the solution.
2. **Multi-Task** (`dataset=<list>, valset=None`): Solve a batch of related problems with cross-task transfer.
3. **Generalization** (`dataset=<list>, valset=<list>`): Build a generalizable prompt/artifact that works across unseen examples.

## Setting Up an Optimization Problem

### Step 1: Define Your Seed Candidate

The starting text to optimize. Can be a string (for `optimize_anything`) or a dict of named components (for `optimize`):

```python
# Single component
seed = "You are a helpful math tutor. Show your work."

# Multiple components
seed = {
    "system_prompt": "You are a helpful math tutor.",
    "reasoning_guide": "Think step by step before answering.",
}
```

### Step 2: Prepare Your Data

Training examples that the optimizer uses to evaluate candidates, and validation examples to measure generalization:

```python
trainset = [
    {"input": "Solve: 2x + 3 = 7", "answer": "2", "additional_context": {}},
    {"input": "Factor: x^2 - 4", "answer": "(x-2)(x+2)", "additional_context": {}},
    # 3-10 examples is often enough
]

valset = [
    {"input": "Solve: 3x - 1 = 8", "answer": "3", "additional_context": {}},
]
```

### Step 3: Define Your Evaluator (for `optimize_anything`)

A function that takes a candidate and an optional example, returns a score (higher is better) and optional side information. **Always make `example` optional** so the evaluator works in single-task mode too:

<!-- ep-cli-lint: allow substantive-analysis -->
```python
def evaluate(candidate: str, example: dict | None = None) -> tuple[float, dict]:
    output = run_my_llm(candidate, example["input"])
    score = compute_score(output, example["answer"])
    side_info = {
        "output": output,
        "expected": example["answer"],
        "feedback": "Correct!" if score > 0.5 else "Wrong answer",
    }
    return score, side_info
```

The side information is fed to the reflection LLM so it can diagnose *why* a candidate failed and propose targeted improvements.

### Step 4: Configure and Run

```python
result = optimize_anything(
    seed_candidate=seed,
    evaluator=evaluate,
    dataset=trainset,
    valset=valset,
    objective="Maximize correctness on algebra problems",
    config=GEPAConfig(
        engine=EngineConfig(
            max_metric_calls=100,      # evaluation budget
            run_dir="outputs/algebra",  # save state for resumption
            parallel=True,
            max_workers=8,
        ),
        reflection=ReflectionConfig(
            reflection_lm=REFLECTION_MODEL,   # model for proposing improvements
        ),
    ),
)

print(f"Best: {result.best_candidate}")
print(f"Score: {result.val_aggregate_scores[result.best_idx]:.2%}")
```

## EDSL Caching Pitfall

When GEPA uses the EDSL backend, all LLM calls go through EDSL's `.run()`, which **caches by default**. This means:

- The reflection model (which proposes mutations) returns identical text every iteration
- Evaluation scores are deterministic even if you want stochastic agent responses

The EDSL-backend fork now creates reflection/refiner LMs with `fresh=True` automatically. However, if you write a **custom evaluator** that calls EDSL's `.run()` internally, you must pass `fresh=True` yourself to get varied scores across iterations:

```python
def evaluate(candidate: str, example: dict | None = None) -> tuple[float, dict]:
    results = survey.by(agents).by(Model(TASK_MODEL, service_name="openai", temperature=1)).run(fresh=True)
    # ... score the results
```

## Temperature Guidance

- **Evaluation model**: Set `temperature=1` for stochastic agent responses (essential when using an EDSL survey panel as the evaluator, otherwise all iterations score identically).
- **Reflection model**: Use moderate temperature (~0.7). Too high (1.0) can produce empty or unparseable mutation proposals. Too low (0.0) combined with fresh=True still lacks diversity.
- Without `temperature > 0`, `fresh=True` alone may not produce sufficient variation.

## Pattern: EDSL Survey Panel as GEPA Evaluator

A powerful pattern is using GEPA to evolve message variants (e.g., service descriptions, ad copy) with an EDSL survey panel as the evaluator. This combines `skill:methods-prompt-optimization` with `skill:research-message-testing`:

1. Build an EDSL `AgentList` representing your target audience
2. Write a `Survey` that presents the candidate text and measures response (e.g., interest, purchase intent)
3. Wrap the survey run in a GEPA evaluator function
4. Use `optimize_anything()` in single-task mode to evolve the text

<!-- ep-cli-lint: allow substantive-analysis -->
```python
def evaluate(candidate: str, example: dict | None = None) -> tuple[float, dict]:
    survey = Survey([QuestionLinearScale(..., question_text=f"...{candidate}...")])
    results = (survey.by(agent_list)
               .by(Model(TASK_MODEL, service_name="openai", temperature=1))
               .run(fresh=True))
    scores = results.select("answer.interest").to_list()
    mean_score = sum(s for s in scores if s is not None) / max(len([s for s in scores if s is not None]), 1)
    return mean_score, {"raw_scores": scores}
```

## Stop Conditions

Control when optimization stops:

```python
from gepa import MaxMetricCallsStopper, NoImprovementStopper, CompositeStopper

result = gepa.optimize(
    ...,
    stop_callbacks=CompositeStopper([
        MaxMetricCallsStopper(200),       # max evaluations
        NoImprovementStopper(10),         # stop if no improvement for 10 iterations
    ]),
)
```

Available stoppers: `MaxMetricCallsStopper`, `NoImprovementStopper`, `ScoreThresholdStopper`, `TimeoutStopCondition`, `FileStopper`, `SignalStopper`.

## Candidate Selection Strategies

Control how candidates are selected for mutation:

- `"pareto"` (default): Random from Pareto frontier -- maintains diversity
- `"current_best"`: Always mutate the best overall candidate
- `"epsilon_greedy"`: Epsilon-random exploration
- `"top_k_pareto"`: Pareto selection among top-K candidates

```python
result = gepa.optimize(
    ...,
    candidate_selection_strategy="pareto",
)
```

## Workflow

When the user asks to optimize a prompt or text artifact:

1. **Understand the goal**: What text is being optimized? What does "better" mean?
2. **Identify the evaluator**: How will candidates be scored? Is there ground truth?
3. **Prepare data**: Gather or generate training/validation examples.
4. **Choose the API**: Use `optimize()` for simple prompt optimization with input/answer pairs. Use `optimize_anything()` for custom evaluators or non-prompt artifacts.
5. **Set budget**: Start with `max_metric_calls=50-100` for exploration, increase if needed.
6. **Write the script**: Generate a Python script that sets up and runs the optimization.
7. **Run it**: Execute with `python script.py` (or `uv run python script.py` if in a uv project).

## Output

Generate a Python script that:
1. Installs/imports GEPA
2. Defines the seed candidate
3. Defines training and validation data
4. Defines the evaluator (if using `optimize_anything`)
5. Configures and runs the optimization
6. Prints the best candidate and its score
