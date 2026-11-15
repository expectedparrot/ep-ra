---
name: methods-calibrating-agents
description: >
  Calibrate a weighted mixture of LLM agent personas to match target response
  distributions using convex optimization over a theory-constrained trait space.
  Use when the user wants to find agent mixture weights that reproduce an
  empirical population distribution (e.g., survey responses, experimental data).
tags: [simulation, quantitative, data-collection]
---

# Calibrating Agent Mixtures to Match Target Distributions

This methodology comes from "General Social Agents" (Manning & Horton, arXiv:2508.17407). The core insight: each LLM agent persona produces a fixed response distribution, and the set of all achievable mixture distributions forms a **convex hull** over those agent distributions. The optimization finds the point in that hull closest to the empirical target. No single agent can represent a heterogeneous population, but a sparse weighted mixture typically can.

---

## When to Use

- You have a **target distribution** -- empirical response frequencies from a survey, experiment, or dataset (e.g., "60% chose option A, 25% chose B, 15% chose C").
- You want to find a **mixture of agent personas** (a set of weighted agents) whose blended LLM-predicted response distribution closely matches that target.
- The trait space is informed by **theory** -- domain knowledge about what dimensions of personality, preferences, or background might drive the observed behavior. "Theory" is used loosely: for a yogurt survey the theory might be taste preferences and purchasing habits; for a dictator game, selfishness and fairness norms.

**Not appropriate when:**
- You just need a single "best answer" (use a standard EDSL survey instead).
- The target is a point estimate, not a distribution.
- You want to calibrate to individual-level data rather than aggregate distributions (this skill calibrates to aggregate response frequencies).
- You believe a single agent persona can represent the population (populations are heterogeneous -- use the mixture approach).

---

## Methodology Overview

The workflow has four main steps:

1. **Build the candidate agent grid** -- Define theoretically relevant trait dimensions and candidate values, then take the Cartesian product to produce an `AgentList`.
2. **Get each agent's predicted distribution** -- Two methods:
   - **logprobs mode**: Fast, one API call per agent. Requires `use_code=True` (single-token response) and an OpenAI model. Only works for binary/few-option questions.
   - **sampling mode**: Robust, runs each agent n times. Works with any model and any question type. More expensive but general.
3. **Optimize mixture weights** -- Use scipy to find weights w_i >= 0 (sum to 1) that minimize total variation distance between the weighted mixture distribution and the target. This is a convex optimization problem.
4. **Save outputs** -- Mixture weights, mixture agents (AgentList with weight in traits), per-agent distributions, and calibration diagnostics.

The key difference from a single-agent approach: instead of picking the one "best" agent, we solve for the optimal blend. A population where 40% are price-sensitive and 60% are brand-loyal cannot be represented by any single persona, but a mixture of two agents with weights (0.4, 0.6) can match it exactly.

---

## Step 1: Define the Trait Space

The trait space is a JSON file mapping dimension names to lists of candidate values. Each dimension should be grounded in domain knowledge about what drives the target behavior.

### Example: Dictator Game

A dictator game experiment asks subjects how much of $10 to give to a stranger. Theory suggests selfishness and fairness norms matter.

```json
{
  "selfishness": ["very selfish", "somewhat selfish", "neutral", "somewhat generous", "very generous"],
  "fairness_norm": ["believes in strict equality", "believes in proportional fairness", "believes giving is optional"],
  "age_group": ["young adult", "middle-aged", "senior"]
}
```

This produces 5 x 3 x 3 = 45 candidate agents.

### Example: Yogurt Preference Survey

```json
{
  "taste_preference": ["prefers fruity flavors", "prefers plain/natural", "prefers indulgent/dessert-like"],
  "health_consciousness": ["very health-conscious", "moderately health-conscious", "not health-conscious"],
  "price_sensitivity": ["very price-sensitive", "somewhat price-sensitive", "not price-sensitive"]
}
```

This produces 3 x 3 x 3 = 27 candidate agents.

### Guidelines for Trait Space Design

- **3-5 dimensions** is typical. More dimensions means exponentially more candidates.
- **3-6 levels per dimension** balances granularity with grid size.
- Each level should be a plain-language description that reads naturally in a persona string (e.g., "very price-sensitive" not "price_sensitivity=high").
- Dimensions should be **theoretically motivated** -- they should plausibly affect the behavior being measured.
- Keep the total grid manageable: under ~1000 candidates. Use `--max-candidates N` for random subsampling of larger grids.
- Think about which trait combinations should get weight in the final mixture. If you expect most of the population to cluster around a few types, include fine-grained levels near those types.

### Pilot Before Full Grid

Before committing to the full grid run, test 5-10 manually chosen agents to verify that:
- Logprobs extraction works (if using logprobs mode) and returns valid distributions.
- Persona strings produce sensible, differentiated responses — agents at opposite ends of a trait dimension should give meaningfully different answers.
- The question/option format yields clean single-token responses (if using `use_code=True`).

This catches trait space design issues early, before spending on the full grid.

---

## Step 2: Target Distribution Format

The target distribution is a CSV with columns `question_name`, `option`, and `probability`:

```csv
question_name,option,probability
yogurt_brand,Brand A,0.40
yogurt_brand,Brand B,0.35
yogurt_brand,Brand C,0.15
yogurt_brand,Brand D,0.10
```

For multi-question calibration, include all questions:

```csv
question_name,option,probability
yogurt_brand,Brand A,0.40
yogurt_brand,Brand B,0.35
yogurt_brand,Brand C,0.15
yogurt_brand,Brand D,0.10
flavor_pref,Strawberry,0.30
flavor_pref,Vanilla,0.25
flavor_pref,Blueberry,0.25
flavor_pref,Plain,0.20
```

Probabilities for each question should sum to 1.0. If they come from empirical counts, normalize them before writing the CSV.

---

## Step 3: Build the Candidate Agent Grid

Use `itertools.product` over trait space values to generate all combinations, then construct an `AgentList`. Each agent gets a natural-language persona composed from its trait values.

```python
import itertools, json
from edsl import Agent, AgentList

with open("trait_space.json") as f:
    trait_space = json.load(f)

dims = list(trait_space.keys())
agents = []
for i, combo in enumerate(itertools.product(*[trait_space[d] for d in dims])):
    traits = dict(zip(dims, combo))
    traits["persona"] = "You are a person who is " + ", ".join(combo) + "."
    agents.append(Agent(name=f"candidate_{i:04d}", traits=traits))

agent_list = AgentList(agents)
agent_list.git.save("candidate_grid.ep")
```

> **Persona construction**: Each trait value should be a phrase that reads naturally in the sentence "You are a person who is [value]." Avoid abbreviations or codes. Test a few persona strings manually before running the full grid.

---

## Step 4: Get Each Agent's Predicted Distribution

There are two methods for obtaining each agent's response distribution. Choose based on your constraints.

### Method A: Logprobs (fast, single-token only)

One API call per agent. Requires `use_code=True` (maps options to single-digit codes so the response is a single token) and an OpenAI model with `logprobs=True`. Only works when the question has few enough options that the answer is a single token.

```python
from edsl import QuestionMultipleChoice, Survey, Model

q = QuestionMultipleChoice(
    question_name="yogurt_brand",
    question_text="Which yogurt brand do you prefer?",
    question_options=["Brand A", "Brand B", "Brand C", "Brand D"],
    use_code=True,
    include_comment=False,
)

survey = Survey([q])
model = Model("gpt-4.1", temperature=1, logprobs=True)

# Run all candidates through a saved jobs.ep -- one API call per agent
# ep run edsl_jobs/logprob/jobs.ep --output calibration_output/logprob_results.ep
from edsl import Results
results = Results.git.load("calibration_output/logprob_results.ep")

# Extract distributions from logprobs
import math

options_map = {str(i): label for i, label in enumerate(q.question_options)}

for result in results:
    raw = result["raw_model_response"]["yogurt_brand_raw_model_response"]
    top_logprobs = raw["choices"][0]["logprobs"]["content"][0]["top_logprobs"]

    predicted = {label: 1e-10 for label in q.question_options}
    for token_info in top_logprobs:
        label = options_map.get(token_info["token"])
        if label:
            predicted[label] = math.exp(token_info["logprob"])

    # Normalize (logprobs may not cover all options)
    total_p = sum(predicted.values())
    predicted = {k: v / total_p for k, v in predicted.items()}
```

See `research_agent/skills/methods-logprob-confidence/SKILL.md` for the full pattern on extracting logprobs.

### Method B: Repeated Sampling (robust, any model)

Run each agent n times and count empirical frequencies. Works with any model (OpenAI, Anthropic, etc.) and any question type. No `use_code` requirement.

```python
from edsl import Model

model = Model("gpt-4.1-mini", temperature=1)
job = survey.by(agent_list).by(model)

# n=30 means 30 responses per agent
# ep run edsl_jobs/sampling/jobs.ep --n 30 --output calibration_output/sampling_results.ep
results = Results.git.load("calibration_output/sampling_results.ep")

# Count answers per agent to build empirical distribution
from collections import defaultdict, Counter

agent_counts = defaultdict(Counter)
for result in results:
    agent_name = result["agent"]["agent_name"]
    answer = result["answer"]["yogurt_brand"]
    if answer is not None:
        agent_counts[agent_name][answer] += 1

# Normalize to probabilities
agent_distributions = {}
for agent_name, counts in agent_counts.items():
    total = sum(counts.values())
    agent_distributions[agent_name] = {opt: c / total for opt, c in counts.items()}
```

### Choosing a Method

| Aspect | logprobs | sampling |
|--------|----------|----------|
| Speed | 1 API call per agent | n API calls per agent |
| Cost | ~50x cheaper | n x more expensive |
| Model support | OpenAI only | Any model |
| Question type | Binary/few options, `use_code=True` | Any question type |
| Accuracy | Exact (model's distribution) | Approximate (sampling noise at small n) |
| When to use | Default for multiple-choice with few options | When logprobs unavailable, or question has many options or free text |

---

## Step 5: Optimize Mixture Weights

This is the core step that distinguishes the mixture approach from single-agent selection. Given each agent's predicted distribution, solve for weights w_i >= 0 (summing to 1) that minimize total variation distance between the weighted mixture and the target.

```python
import numpy as np
from scipy.optimize import minimize

def optimize_mixture(agent_distributions, target):
    """Find mixture weights minimizing TV distance to target.

    agent_distributions: {agent_name -> {question_name -> {option: prob}}}
    target: {question_name -> {option: prob}}
    """
    agent_names = sorted(agent_distributions.keys())
    n_agents = len(agent_names)

    # Build flat target vector and distribution matrix
    col_labels = []
    target_vec = []
    for qname in sorted(target.keys()):
        for opt in sorted(target[qname].keys()):
            col_labels.append((qname, opt))
            target_vec.append(target[qname][opt])
    target_vec = np.array(target_vec)

    # P[i, j] = agent i's predicted probability for (question, option) j
    P = np.zeros((n_agents, len(col_labels)))
    for i, aname in enumerate(agent_names):
        dists = agent_distributions[aname]
        for j, (qname, opt) in enumerate(col_labels):
            P[i, j] = dists.get(qname, {}).get(opt, 1e-10)

    # Minimize total variation: 0.5 * sum |P^T w - target|
    def objective(w):
        mixture = P.T @ w
        return 0.5 * np.sum(np.abs(mixture - target_vec))

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
    bounds = [(0.0, 1.0)] * n_agents
    w0 = np.ones(n_agents) / n_agents

    result = minimize(
        objective, w0, method="SLSQP",
        bounds=bounds, constraints=constraints,
        options={"maxiter": 1000, "ftol": 1e-12},
    )

    # Extract agents with nonzero weight
    threshold = 0.001
    weights = {
        agent_names[i]: float(result.x[i])
        for i in range(n_agents)
        if result.x[i] > threshold
    }
    return weights
```

The optimization is convex (total variation of a mixture is convex in the weights), so SLSQP converges reliably. Typical mixtures are sparse: out of hundreds of candidates, only 3-10 agents get nonzero weight.

---

## Step 6: Interpret and Use Results

### Output Files

| File | Description |
|------|-------------|
| `candidate_grid.ep` | Full `AgentList` of all candidates |
| `logprob_results.ep` | Raw EDSL Results (logprobs mode) |
| `sampling_results.ep` | Raw EDSL Results (sampling mode) |
| `agent_distributions.csv` | Per-agent predicted distributions for all questions |
| `mixture_weights.csv` | Agent names, optimized weights, and trait values |
| `calibrated_mixture.ep` | `AgentList` of agents with nonzero weight, each with a `_weight` trait (underscore prefix so EDSL does not render it in prompts) |
| `calibration_summary.json` | Metadata: method, fit metrics, target vs mixture comparison, timing |

### Loading the Calibrated Mixture

```python
from edsl import AgentList

mixture = AgentList.git.load("calibration_output/calibrated_mixture.ep")

# Each agent has a _weight trait (underscore prefix = not rendered in prompts)
for agent in mixture:
    print(f"{agent.name}: weight={agent.traits['_weight']:.3f}")
```

The `_weight` trait uses an underscore prefix so that EDSL does not include it when rendering the agent's persona in survey prompts. The weight is available programmatically for weighted analysis of results.

### Using the Mixture in Follow-up Studies

Run a follow-up survey with the mixture as a normal `AgentList`, then weight results by each agent's `_weight` trait when computing aggregate statistics (e.g., map agent names to weights via `{a.name: a.traits["_weight"] for a in mixture}` and use weighted groupby).

---

## Script Usage

The `calibrate_agents.py` script in `research_agent/skills/methods-calibrating-agents/scripts/` automates the full pipeline:

```bash
# Logprobs mode (fast, OpenAI + use_code only):
python calibrate_agents.py \
    --target-csv target.csv \
    --trait-space-json trait_space.json \
    --method logprobs --model <openai-model>   # logprobs is OpenAI-only

# Repeated sampling mode (robust, any model):
python calibrate_agents.py \
    --target-csv target.csv \
    --trait-space-json trait_space.json \
    --method sampling --model <model> --n-samples 30
```

For the full argument table and resume support details, see `references/script_reference.md`.

---

## Study Structure

For the full directory layout when used in a study project, see `references/study_structure.md`. Key paths: user provides `data/raw/target_distribution.csv` and `data/raw/trait_space.json`; outputs land in `computed_objects/calibration/`. Follow-up studies should record the predecessor path and load the calibrated mixture in place, copying only that artifact with provenance when portability is required.

---

## Gotchas

The three most important pitfalls (see `references/gotchas.md` for the full list):

1. **Mixture, not single agent** -- No single agent can represent a heterogeneous population. Always use the mixture optimization step. Even if one agent fits one question, it will fail on others because its preferences are internally consistent in ways the population's are not.

2. **`use_code=True` required for logprobs** -- Logprobs mode requires single-token responses. Setting `use_code=True` maps options to digit codes (0, 1, 2, ...) so the model responds with one token. Without this, logprobs extraction will fail.

3. **The "too rational" problem** -- When the target data reflects violations of expected utility theory (e.g., the Allais paradox, framing effects), the model may be systematically "too rational." LLM agent preferences tend to respect standard rationality axioms, so the target distribution may be **unreachable** — the convex hull of agent distributions does not contain it. When this happens, the residual total variation distance will remain high. This is a fundamental limitation, not a tuning problem. Check `calibration_summary.json` for fit metrics and per-question residuals.

---

## Quick Reference

| Task | Code / Command |
|------|----------------|
| Define trait space | Create `trait_space.json`: `{"dim": ["level1", "level2", ...]}` |
| Define target | Create `target.csv`: `question_name,option,probability` |
| Run full pipeline (logprobs) | `python calibrate_agents.py --target-csv t.csv --trait-space-json ts.json --method logprobs --model <openai-model>` |
| Run full pipeline (sampling) | `python calibrate_agents.py --target-csv t.csv --trait-space-json ts.json --method sampling --model <model> --n-samples 30` |
| Load calibrated mixture | `AgentList.git.load("calibrated_mixture.ep")` |
| Extract logprobs manually | See `research_agent/skills/methods-logprob-confidence/SKILL.md` |
| Compute total variation | `0.5 * sum(abs(p - q) for p, q in zip(target, predicted))` |
| Resume interrupted run | Re-run same command; completed steps are skipped |
| Subsample large grid | `--max-candidates 500` |
| Check fit quality | Read `calibration_summary.json`, look at `mixture_total_variation` (see thresholds below) |
| Use non-OpenAI model | `--method sampling --model <any-model>` |

---

## Fit Quality Thresholds

After optimization, check `mixture_total_variation` in `calibration_summary.json`:

| Total Variation | Interpretation | Action |
|-----------------|---------------|--------|
| < 0.05 | Excellent fit | Proceed with mixture |
| 0.05 - 0.15 | Acceptable fit | Review per-question residuals; consider adding trait dimensions if specific questions have high error |
| > 0.15 | Poor fit | Revisit trait space design. Possible causes: too few dimensions, wrong dimensions, or the "too rational" problem (target outside the convex hull). Also check if a near-uniform mixture was returned — this signals the trait space is not sufficiently discriminating |

If the optimizer returns near-uniform weights (all agents get similar weight), the trait space is likely not capturing the dimensions that drive the target distribution. Redesign with more theoretically grounded dimensions.
