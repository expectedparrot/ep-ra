---
name: research-social-simulation
description: >
  Designs, runs, and analyzes multi-agent social simulations as experiments.
  Use when the user wants to simulate a social scenario (negotiation, interview,
  coordination) with LLM agents, vary experimental conditions, and analyze
  causal effects on outcomes. Covers blueprint creation, visualization,
  pilot runs, full factorial experiments, and results analysis.
tags: [study-type, simulation, quantitative, analysis]
---

# Social Simulation Skill

This skill walks the user through a complete social simulation experiment in six phases. Each phase produces a concrete artifact. Move through phases sequentially — the output of each feeds the next.

## Phase Overview

| Phase | What happens | Artifact |
|-------|-------------|----------|
| 1. Blueprint design | Collaboratively define agents, variables, causal structure, and measurement | `blueprint.json` |
| 2. Visualize blueprint | Generate an HTML visualization of the experimental design | `blueprint_viz.html` |
| 3. Pilot run | Run ONE simulation (single condition) via Concordia to validate the setup | Simulation log + HTML |
| 4. Pilot analysis | Analyze the pilot run — check agent behavior, measurement validity, conversation quality | Analysis summary |
| 5. Full experiment | Run the full factorial design across all experimental conditions | Log files per condition |
| 6. Results analysis | Analyze outcomes across conditions, estimate causal effects, generate report | Results report |

---

## Phase 1: Blueprint Design

Walk the user through designing the simulation as a structured JSON blueprint. This is the most interactive phase.

**Mode selection:** Ask the user whether they want interactive mode (collaborative, step-by-step) or autonomous mode (quick draft). If the user's intent is already clear, skip the question.

Follow the 12-step blueprint design process described in `references/blueprint-design.md`. The steps are:

1. Identify agents (who speaks in the scenario)
2. Generate candidate outcome variables
3. Operationalize the chosen outcome
4. Classify variable type, units, and levels
5. Create measurement questions
6. Identify causal variables (exogenous treatments)
7. Build each causal variable (operationalize, classify, determine scope, create attribute variation, align ranges, set public/private)
8. Define agent interaction protocol
9. Define agent goals and constraints
10. Determine additional agent attributes
11. Construct the causal graph
12. Assemble the final blueprint JSON

**Output:** Save the blueprint as `blueprint.json` in the working directory.

---

## Phase 2: Visualize Blueprint

Generate a self-contained HTML visualization of the blueprint so the user can review the experimental design at a glance.

Follow the visualization spec in `references/blueprint-visualization.md` to produce a Python script that renders:
- Header with scenario description and agent badges
- Causal DAG (Graphviz SVG)
- Variable detail cards (outcome and cause cards)
- Experimental design matrix with total cell count
- Agent profile cards

**Output:** Run the script to produce `blueprint_viz.html`. Open it for the user to review. If the user wants changes, go back to Phase 1 and revise the blueprint.

---

## Phase 3: Pilot Run

Run a single simulation to validate that the setup works before committing to the full experiment.

### 3a. Pick a single condition

Choose one set of treatment values — typically the "middle" or most representative values for each exogenous variable. This tests the simulation machinery without burning resources on all conditions.

### 3b. Set up Concordia simulation

Using the blueprint, create a Concordia simulation script. See `references/concordia-setup.md` for the full API reference. Key steps:

1. **Install Concordia** (if not already installed):
   ```bash
   pip install -e ".[edsl]"  # from the Expected Parrot fork
   ```

2. **Map blueprint to Concordia config:**
   - **Choose entity prefab** — this is a key design decision affecting quality vs. speed. See `references/entity-prefabs.md` for the full comparison. Present the choice to the user:

     | Prefab | LLM calls/turn | Best for |
     |--------|---------------|----------|
     | `minimal__Entity` | 1 | Fast pilots, high-volume experiments |
     | `basic__Entity` | 4 | Most experiments (default) |
     | `conversational__Entity` | 6-7 | Dialogue-heavy scenarios where pacing matters |

   - Each agent in the blueprint → an `InstanceConfig` with the chosen prefab
   - Agent goals → `params.goal`
   - Agent attributes (including treatment values) → incorporated into the agent's premise or `params`
   - Interaction protocol → choose appropriate Game Master prefab and engine:
     - `ordered` → `dialogic__GameMaster` with `acting_order: 'fixed'` (fastest — skips next-actor LLM call)
     - `random` → `dialogic__GameMaster` with `acting_order: 'random'`
     - Multi-agent with central speaker → `dialogic__GameMaster` with `acting_order: 'game_master_choice'`
   - Scenario description → `default_premise`

3. **Add measurement:** After the simulation runs, ask measurement questions to agents (from the blueprint's `agent_measure_question_dict`) using the interviewer Game Master or post-simulation prompts.

4. **Write the simulation script** as `run_pilot.py`.

### 3c. Run the pilot

```bash
python run_pilot.py
```

**Output:** Simulation log JSON and HTML visualization in `/tmp/` (or working directory).

---

## Phase 4: Pilot Analysis

Analyze the pilot run to decide whether the experimental design is sound before scaling up.

### What to check

1. **Conversation quality:** Did agents have a coherent, realistic conversation? Read the transcript.
2. **Role adherence:** Did each agent stay in character and pursue their goal?
3. **Measurement validity:** Did the measurement questions produce sensible values? Could the outcome variable be determined?
4. **Treatment uptake:** Did the agent actually use/reference the treatment attribute in their behavior?
5. **Scenario realism:** Does the interaction feel like a plausible version of the described scenario?

### How to analyze

Use the `AIAgentLogInterface` from `concordia.utils.structured_logging`:

```python
from concordia.utils.structured_logging import SimulationLog, AIAgentLogInterface
import json

with open('simulation_log.json') as f:
    data = json.load(f)

log = SimulationLog.from_dict(data)
interface = AIAgentLogInterface(log)

# Overview
print(interface.get_overview())

# What did each agent do?
for agent in blueprint['agents_in_scenario']:
    actions = interface.get_entity_actions(agent)
    for a in actions:
        print(f"Step {a['step']}: {str(a['action'])[:200]}")

# Why did agent X do Y at step N?
context = interface.get_entity_action_context('agent_name', step=3)
```

### Decision point

Present findings to the user. Ask:
- **Proceed:** The pilot looks good — move to the full experiment.
- **Revise:** Go back to Phase 1 to adjust the blueprint (e.g., change measurement questions, adjust attribute values, modify agent goals).
- **Re-run:** Same design, just re-run the pilot (e.g., if there was a transient LLM issue).

---

## Phase 5: Full Experiment

Run the complete factorial experiment across all treatment conditions defined in the blueprint.

### 5a. Generate the condition grid

From the blueprint, compute the full factorial design:
- For each exogenous variable, enumerate its `attribute_values`.
- Take the Cartesian product of all variables' values.
- Each combination is one experimental condition (cell).

Report the total number of cells to the user (e.g., "2 × 5 × 8 = 80 conditions") and confirm before proceeding.

### 5b. Create the experiment runner

Write `run_experiment.py` that:

1. Loads the blueprint JSON.
2. Iterates over all conditions in the factorial grid.
3. For each condition:
   - Creates a Concordia config with the appropriate treatment values injected into agent attributes.
   - Runs the simulation.
   - Collects measurement outcomes via post-simulation questions.
   - Saves the structured log with condition metadata.
4. Aggregates all results into a single `experiment_results.json` with one row per condition containing:
   - All treatment variable values
   - All measured outcome values
   - Metadata (run timestamp, model used, number of conversation turns)

Consider parallelism: multiple conditions can run concurrently. See `references/entity-prefabs.md` (Parallelism section) for patterns using multiprocessing or ThreadPoolExecutor. With EDSL remote inference, 3-5 parallel workers gives roughly linear speedup.

### 5c. Run the experiment

```bash
python run_experiment.py
```

Monitor progress and report completion.

**Output:** `experiment_results.json` — a structured dataset of all conditions and outcomes.

---

## Phase 6: Results Analysis

Analyze the experimental data to estimate causal effects and generate a report.

### 6a. Descriptive statistics

- Distribution of the outcome variable across all runs.
- Mean/median outcome by level of each treatment variable.
- Cross-tabulations for categorical variables.

### 6b. Causal analysis

For each edge in the causal graph:
- **Binary/ordinal treatments:** Compare outcome distributions across treatment groups. Use appropriate tests (t-test, Mann-Whitney, chi-squared) depending on variable types.
- **Continuous treatments:** Fit regression models (OLS for continuous outcomes, logistic for binary).
- **Multiple treatments:** Fit a model with all treatments as predictors to estimate independent effects.
- Report effect sizes, confidence intervals, and p-values.

### 6c. Interaction effects

If there are multiple exogenous variables, check for interactions:
- Does the effect of variable A depend on the level of variable B?
- Visualize with interaction plots.

### 6d. Conversation-level analysis

For a sample of interesting conditions (e.g., extreme outcomes, surprising results):
- Read transcripts to understand *why* the outcome occurred.
- Identify qualitative patterns in agent behavior.

### 6e. Generate results report

Produce a summary report with:
- Experimental design overview (reference the blueprint visualization)
- Sample size and conditions
- Main effects table with effect sizes
- Key visualizations (outcome distributions, treatment effects, interactions)
- Notable qualitative findings from transcript review
- Limitations and suggested follow-ups

**Output:** Results report (markdown or HTML) and supporting visualizations.

---

## Reference Files

Detailed specifications are in the `references/` subdirectory:

| File | Contents |
|------|----------|
| `references/blueprint-design.md` | The 12-step blueprint creation process with rules, examples, and JSON schema |
| `references/blueprint-visualization.md` | HTML visualization specification with CSS, section layouts, and Graphviz config |
| `references/concordia-setup.md` | Concordia installation, API reference, prefabs, game types, and log analysis |
| `references/entity-prefabs.md` | Entity prefab comparison, decision framework, cost/speed estimates, parallelism patterns |
