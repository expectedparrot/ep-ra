# Concordia Setup and Reference

## Contents

- [Installation](#installation-from-expected-parrot-fork)
- [Quick Orientation](#quick-orientation)
- [Available Games and Scenarios](#available-games-and-scenarios)
- [Running Simulations](#running-simulations)
- [Building Custom Simulations](#building-a-custom-simulation-from-scratch)
- [Available Prefabs](#available-entity-prefabs)
- [Simulation Engines](#simulation-engines)
- [Analyzing Simulation Logs](#analyzing-simulation-logs)

---

## Installation from Expected Parrot Fork

To install Concordia with EDSL support from the Expected Parrot fork:

```bash
git clone git@github.com:expectedparrot/concordia.git
cd concordia
pip install -e ".[edsl]"
```

This installs Concordia in editable mode with the EDSL language model backend,
which provides access to 20+ model providers via Expected Parrot's infrastructure.

To also install the Anthropic backend:

```bash
pip install -e ".[edsl]" anthropic
```

To install with all optional dependencies:

```bash
pip install -e ".[edsl,dev,google,openai,amazon]"
```

## Quick Orientation

| Path | What it contains |
|------|-----------------|
| `examples/games/run.py` | Unified game runner (entry point for all games) |
| `examples/games/{game}/configs/` | Scenario configurations per game |
| `examples/games/{game}/simulation.py` | Game-specific simulation logic |
| `examples/social_media/run.py` | Social media forum simulation runner |
| `concordia/prefabs/entity/` | Agent prefab blueprints |
| `concordia/prefabs/game_master/` | Game Master prefab blueprints |
| `concordia/prefabs/simulation/` | Simulation orchestration |
| `concordia/components/` | Modular building blocks (agent + GM) |
| `concordia/environment/engines/` | Execution engines (sequential, simultaneous, etc.) |
| `concordia/utils/structured_logging.py` | Log analysis interface |

## Available Games and Scenarios

### haggling
Price negotiation over fruit. Buyer proposes, seller accepts/rejects.

Scenarios: `fruitville`, `vegbrooke`, `fruitville_gullible`, `puppet`,
`vegbrooke_strange_game`, `vegbrooke_stubborn`

### haggling_multi_item
Multi-item negotiation variant.

Scenarios: `fruitville_multi`, `cumulative_score`, `fruitville_gullible`,
`puppet`, `vegbrooke`

### pub_coordination
Friends deciding which pub to watch a game at. Social coordination with
information asymmetry.

Scenarios: `london`, `london_mini`, `london_closures`, `edinburgh`,
`edinburgh_closures`, `edinburgh_tough_friendship`, `capetown`, `puppet`

### social_media
Asynchronous forum discussion simulation. Run via `examples/social_media/run.py`.

## Running Simulations

### Run an existing game

```bash
python -m concordia.examples.games.run \
  --game=haggling \
  --scenario=fruitville \
  --api_type=openai \
  --model_name=<model>

# Test mode (no LLM needed)
python -m concordia.examples.games.run \
  --game=haggling \
  --scenario=fruitville \
  --disable_language_model
```

**Run flags:**
- `--game`: `haggling`, `haggling_multi_item`, `pub_coordination`
- `--scenario`: scenario name (see lists above)
- `--api_type`: `openai`, `google_aistudio`, `mistral`, `ollama`, etc.
- `--model_name`: model identifier; confirm a current one for your `--api_type` rather than copying a name from docs
- `--api_key`: API key (or set via environment variable)
- `--disable_language_model`: use mock model for testing
- `--focal_player_prefab`: override agent type

**Output files** are written to `/tmp/`:
- `simulation_results_{game}_{scenario}.html` - interactive HTML visualization
- `simulation_log_{game}_{scenario}.json` - structured JSON log for analysis

## Building a Custom Simulation from Scratch

Use this pattern to create simulations programmatically from a blueprint:

```python
from concordia.prefabs import entity as entity_prefabs
from concordia.prefabs import game_master as game_master_prefabs
from concordia.prefabs.simulation import generic as simulation
from concordia.typing import prefab as prefab_lib
from concordia.utils import helper_functions

# 1. Load prefabs
prefabs = {
    **helper_functions.get_package_classes(entity_prefabs),
    **helper_functions.get_package_classes(game_master_prefabs),
}

# 2. Define instances
instances = [
    prefab_lib.InstanceConfig(
        prefab="basic__Entity",
        role=prefab_lib.Role.ENTITY,
        params={"name": "Alice", "goal": "Make new friends"},
    ),
    prefab_lib.InstanceConfig(
        prefab="dialogic__GameMaster",
        role=prefab_lib.Role.GAME_MASTER,
        params={"name": "conversation rules",
                "next_game_master_name": "conversation rules"},
    ),
]

# 3. Create config and run
config = prefab_lib.Config(
    default_premise="Alice and Bob meet at a coffee shop.",
    default_max_steps=20,
    prefabs=prefabs,
    instances=instances,
)
sim = simulation.Simulation(config=config, model=model, embedder=embedder)
results = sim.play(return_structured_log=True)
```

## Available Entity Prefabs

- `basic__Entity` - Standard "Three Key Questions" agent
- `basic_with_plan__Entity` - Adds long-term planning
- `basic_scripted__Entity` - Follows a script
- `conversational__Entity` - Optimized for dialogue
- `rational__Entity` - Rational decision-making agent
- `minimal__Entity` - Bare-bones, customizable
- `puppet__Entity` - Externally controlled (for testing)

## Available Game Master Prefabs

- `generic__GameMaster` - General purpose
- `dialogic__GameMaster` - Pure conversation
- `dialogic_and_dramaturgic__GameMaster` - Scene-based narratives
- `situated__GameMaster` - Location-based
- `situated_in_time_and_place__GameMaster` - With time tracking
- `game_theoretic_and_dramaturgic__GameMaster` - Matrix games
- `marketplace__GameMaster` - Economic simulations
- `interviewer__GameMaster` / `open_ended_interviewer__GameMaster` - Questionnaires
- `scripted__GameMaster` - Pre-scripted sequences

## Simulation Engines

- **Sequential** - Turn-based, one agent per step (default, best for narrative)
- **Simultaneous** - Batch mode, all agents act in parallel (best for game theory)
- **Asynchronous** - Non-blocking concurrent (best for forums)
- **Parallel Questionnaire** - Fast parallel survey
- **Sequential Questionnaire** - Context-dependent survey

## Analyzing Simulation Logs

### Load and inspect a log

```python
import json
from concordia.utils.structured_logging import SimulationLog, AIAgentLogInterface

with open('/tmp/simulation_log_haggling_fruitville.json') as f:
    data = json.load(f)

log = SimulationLog.from_dict(data)
interface = AIAgentLogInterface(log)

# High-level overview
overview = interface.get_overview()
print(overview)
```

### Key analysis methods

| Method | Purpose |
|--------|---------|
| `get_overview()` | High-level stats (steps, entities, components) |
| `get_entity_actions(name)` | Concise action timeline for one agent |
| `get_entity_action_context(name, step)` | Full prompt + observations for one step |
| `get_step_summary(step, include_content)` | Everything that happened at a step |
| `get_entity_timeline(entity, include_content)` | Full timeline for one agent |
| `filter_entries(...)` | Filter by entity/component/type/step |
| `search_entries(query)` | Deep text search across all content |
| `search_summaries(query)` | Fast text search in summaries only |
| `get_component_values(...)` | Extract specific component values |
| `get_entity_memories(name)` | Agent's accumulated memories |
| `get_game_master_memories()` | GM memories |
| `get_entry_content(index)` | Full reconstructed data for one entry |

### Content deduplication

The structured log deduplicates long strings using `{'_ref': content_id}` references into a `content_store`. The `AIAgentLogInterface` resolves these automatically, but if working with raw JSON you must resolve refs manually:

```python
content_store = data['content_store']

def resolve_refs(obj):
    if isinstance(obj, dict):
        if '_ref' in obj:
            return content_store.get(obj['_ref'], f'<UNRESOLVED:{obj["_ref"]}>')
        return {k: resolve_refs(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_refs(v) for v in obj]
    return obj
```

### Common analysis patterns

**Agent action timeline:**
```python
actions = interface.get_entity_actions('Alice')
for a in actions:
    print(f"Step {a['step']}: {str(a['action'])[:200]}")
```

**Why did an agent do something?**
```python
context = interface.get_entity_action_context('Alice', step=3)
print(f"Action: {context['action']}")
print(f"Observations: {context['observations']}")
print(f"Prompt: {context['action_prompt']}")
```

**LLM-based verification:**
```python
entries = interface.filter_entries(include_content=True)
log_text = '\n'.join([
    f"Step {e.get('step')}: {e.get('summary')} {e.get('content', '')}"
    for e in entries
])[:10000]

prompt = f"""Analyze this simulation log and answer:
1. Did agents behave coherently? [YES/NO]
2. Did the game mechanics function correctly? [YES/NO]
LOG:
{log_text}
"""
response = model.sample_text(prompt, max_tokens=200)
```

**Compare two runs:**
```python
def extract_trajectory(path, component_name, value_key='Value'):
    with open(path) as f:
        data = json.load(f)
    log = SimulationLog.from_dict(data)
    trajectory = []
    for entry in log.entries:
        if entry.entry_type != 'step':
            continue
        full = log.reconstruct_value(entry.deduplicated_data)
        resolve = full.get('value', {}).get('resolve', {})
        comp = resolve.get(component_name, {})
        if comp:
            act = comp.get('__act__', comp)
            trajectory.append({'step': entry.step, 'value': act.get(value_key, '')})
    return trajectory
```
