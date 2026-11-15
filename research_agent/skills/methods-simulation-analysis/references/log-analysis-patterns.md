# Concordia Log Analysis: Detailed Patterns and Code Examples

## Contents

- [Log Data Structure Details](#log-data-structure-details)
- [Deduplication and Reference Resolution](#deduplication-and-reference-resolution)
- [Entry Data Layout](#entry-data-layout)
- [Extracting Entity Actions](#extracting-entity-actions)
- [Extracting GM Component Values](#extracting-gm-component-values)
- [Entity Memories](#entity-memories)
- [Manual Extraction from Raw JSON](#manual-extraction-from-raw-json)
- [Analysis Patterns](#analysis-patterns)
- [Common Questions and Recipes](#common-questions-and-recipes)
- [Comparing Simulation Runs](#comparing-simulation-runs)

---

## Log Data Structure Details

> **IMPORTANT:** The structured log uses content deduplication. Long strings in
> log entries are replaced with `{'_ref': content_id}` references that point
> into a separate `content_store`. You **must** resolve these references to
> read the actual content.

### Deduplication and Reference Resolution

When you load a structured log from JSON:

```python
from concordia.utils.structured_logging import SimulationLog

# Within a study, logs are in $STUDY_ROOT/data/
with open(f'{STUDY_ROOT}/data/simulation_log.json') as f:
    data = json.load(f)

log = SimulationLog.from_dict(data)
```

The JSON has this top-level structure:
```python
{
    'content_store': { 'hash_id': 'actual_text', ... },
    'entries': [ { 'step': 2, 'entity_name': '...', 'deduplicated_data': {...} }, ... ],
    'entity_memories': { ... },
    'game_master_memories': [ ... ]
}
```

Each entry's `deduplicated_data` contains nested dicts where long strings have
been replaced by `{'_ref': 'hash_id'}`. To get the actual text, use
`SimulationLog.reconstruct_value()`:

```python
entry = log.entries[0]
full_data = log.reconstruct_value(entry.deduplicated_data)
```

### Entry Data Layout

Each entry's `deduplicated_data` has a `key` and a `value`. The `value` is a
nested dict of component outputs. For entity entries, the key pattern is
`Entity [name]` and the value contains:

```python
{
    'key': 'Entity [Alice]',
    'value': {
        'Instructions': {'Key': "Alice's Identity", 'Value': '...'},
        '__act__': {
            'Summary': '...',
            'Value': 'Alice said hello...',  # The actual entity action
            'Prompt': '...',  # The full prompt sent to the LLM
        },
        ...
    }
}
```

For game master entries, the value is organized into **phases**, each
containing outputs from every GM component that ran during that phase:

```python
{
    'key': 'game_master_name',
    'value': {
        'terminate': { ... },
        'next_game_master': { ... },
        'make_observation': { ... },
        'next_acting': { ... },
        'next_action_spec': { ... },
        'resolve': {           # <-- Most interesting phase
            '__act__': { ... },
            '__resolution__': {
                'Key': '...',
                'Summary': '...',   # Event resolution summary
                'Value': '...',     # Full resolved event text
                'Prompt': '...',
            },
            'LineageResourceTracker': {
                '__act__': {
                    'Key': '...',
                    'Value': '...',          # Component's text output
                    'Measurements': { ... }, # Optional numeric metrics
                },
            },
            'tension_tracker': { '__act__': { 'Value': '0.6' } },
            'ritual_propriety_observer': { '__act__': { 'Value': '...' } },
            ...
        },
    }
}
```

> **IMPORTANT:** The `resolve` phase is typically where the most interesting
> data lives -- event resolutions. When analyzing GM behavior,
> always look in `resolve` first.

> **IMPORTANT:** Custom components may include a `Measurements` sub-dict
> alongside their `Value`. This contains numeric metrics (e.g.,
> `{'compound_health': 120, 'granary_stores': 0}`) that are useful for
> quantitative tracking across steps.

## Extracting Entity Actions

The simplest way to get what entities actually did:

```python
interface = AIAgentLogInterface(log)

actions = interface.get_entity_actions('Alice')
for a in actions:
    print(f"Step {a['step']}: {str(a['action'])[:200]}")
```

To understand *why* an entity took a specific action:

```python
context = interface.get_entity_action_context('Alice', step=3)
if context:
    print(f"Action: {context['action']}")
    print(f"Observations: {context['observations']}")
    print(f"Prompt: {context['action_prompt']}")
```

For more flexible extraction, use `get_component_values()`:

```python
interface.get_component_values(
    component_key='Observation',
    value_key='Value',
    entity_name='Alice',
    step_range=(1, 5),
)
```

## Extracting GM Component Values

To extract values from specific game master components, navigate the
phase -> component -> `__act__` nesting:

```python
for entry in log.entries:
    if entry.entry_type != 'step':
        continue
    full_data = log.reconstruct_value(entry.deduplicated_data)
    resolve = full_data.get('value', {}).get('resolve', {})
    if not resolve:
        continue

    # Event resolution text
    resolution = resolve.get('__resolution__', {})
    if resolution:
        event_text = resolution.get('Value', '')
        print(f"Step {entry.step} event: {event_text[:200]}")

    # Custom component values (e.g., tension_tracker)
    tracker = resolve.get('tension_tracker', {})
    if tracker:
        act = tracker.get('__act__', tracker)
        tension_val = act.get('Value', '')
        print(f"Step {entry.step} tension: {tension_val}")

    # Components with Measurements
    resource = resolve.get('LineageResourceTracker', {})
    if resource:
        act = resource.get('__act__', resource)
        measurements = act.get('Measurements', {})
        if measurements:
            print(f"Step {entry.step} metrics: {measurements}")
```

To inspect the keys of the `resolve` phase:

```python
entry = next(e for e in log.entries if e.entry_type == 'step')
full_data = log.reconstruct_value(entry.deduplicated_data)
resolve_keys = list(full_data.get('value', {}).get('resolve', {}).keys())
print(f"Available GM components: {resolve_keys}")
```

## Entity Memories

The structured log also stores all entity memories accumulated during the
simulation:

```python
log_data = json.load(open(f'{STUDY_ROOT}/data/simulation_log.json'))
memories = log_data.get('entity_memories', {})
for name, mems in memories.items():
    print(f"{name}: {len(mems)} memories")
    for m in mems[-3:]:  # Last 3 memories
        print(f"  > {str(m)[:150]}")
```

## Manual Extraction from Raw JSON

If working directly with the raw JSON file without loading into a
`SimulationLog`, you can resolve references manually:

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

for entry in data['entries']:
    dd = entry.get('deduplicated_data', {})
    if not dd:
        continue
    resolved = resolve_refs(dd)
    value = resolved.get('value', {})
    entity = entry.get('entity_name', '?')
    step = entry.get('step', '?')

    if entry.get('entry_type') == 'entity' and isinstance(value, dict):
        act = value.get('__act__', {})
        if isinstance(act, dict):
            action_text = act.get('Value', '')
            if action_text and len(str(action_text)) > 10:
                print(f'Step {step} [{entity}]: {action_text[:400]}')
```

## Analysis Patterns

### Pattern: Verifying Structural Correctness

Before analyzing narrative content, verify the simulation structure matches
expectations. This catches configuration bugs before wasting time on content:

```python
overview = interface.get_overview()
entities = overview['entities']
total_steps = overview['total_steps']

# Check expected agents participated
expected_agents = ['Alice', 'Bob']
for agent in expected_agents:
    timeline = interface.get_entity_timeline(agent)
    assert len(timeline) > 0, f"{agent} has no entries!"
    print(f"{agent}: {len(timeline)} entries across steps")

# Check expected game masters ran
expected_game_masters = ['negotiation_rules', 'combat_rules']
for game_master in expected_game_masters:
    timeline = interface.get_entity_timeline(game_master)
    print(f"Game Master '{game_master}': {len(timeline)} entries")
```

### Pattern: Drilling into a Specific Step

If you want to see exactly what happened concurrently at a specific time point:

```python
step_data = interface.get_step_summary(step=3, include_content=True)
for entry in step_data:
    print(f"Entity: {entry['entity_name']}")
    print(f"Event: {entry['entry_type']}")
    print(f"Summary: {entry['summary']}")
    if entry.get('prompt'):
        print(f"Prompt: {entry['prompt'][:500]}...")
    if entry.get('response'):
        print(f"Response: {entry['response']}")
```

### Pattern: Following an Entity's Timeline

To understand one agent's journey across the entire simulation:

```python
alice_timeline = interface.get_entity_timeline('Alice', include_content=True)
for entry in alice_timeline:
    print(f"Step {entry['step']}: {entry['summary']}")
```

### Pattern: Extracting Specific Component Values

```python
actions = interface.get_component_values()
for action in actions:
    print(f"Step {action['step']} [{action['entity_name']}]: {action['value']}")

# Customize which component and key to extract
interface.get_component_values(
    component_key='Observation',
    value_key='Value',
    entity_name='Alice',
    step_range=(1, 5),
)
```

### Pattern: Filtering by Criteria

```python
# Find entries from a specific component
memory_entries = interface.filter_entries(component_name='memory')

# Find entries in a step range
late_game = interface.filter_entries(step_range=(10, 20))
```

### Pattern: LLM-Based Verification (For Complex Checks)

```python
def verify_simulation(interface, model, checks):
    """
    Verify simulation outcomes using LLM-based analysis.

    Args:
        interface: AIAgentLogInterface instance
        model: Language model for analysis
        checks: List of verification questions

    Returns:
        dict with results for each check
    """
    entries = interface.filter_entries(include_content=True)
    log_text = '\n'.join([
        f"Step {e['step']}: {e.get('summary', '')} "
        f"{extract_observations(e.get('metadata', {}))}"
        for e in entries
    ])

    results = {}
    for check_name, question in checks.items():
        prompt = f"""Based on this simulation log, answer: {question}

LOG:
{log_text[:8000]}

Answer YES or NO, then explain briefly.
"""
        response = model.sample_text(prompt, max_tokens=100)
        results[check_name] = 'YES' in response.upper()

    return results

# Example usage
checks = {
    'hp_mechanics': 'Are HP values mentioned and do they change during combat?',
    'energy_costs': 'Do actions cost Energy?',
    'narrative_progress': 'Does the story progress meaningfully?',
}
results = verify_simulation(interface, model, checks)
```

### Pattern: Searching for Keywords

For fast searching by entry summary only:

```python
matches = interface.search_summaries('coffee shop')
```

For deep searching across all reconstructed content:

```python
matches = interface.search_entries('coffee shop')
for e in matches:
    print(f"Step {e['step']} [{e['entity_name']}]: {e.get('summary', '')}")
```

### Pattern: Deep Inspection of a Single Entry

```python
content = interface.get_entry_content(entry_index=5)
print(content['data'])
```

### Pattern: Accessing Final Entity Memories

```python
memories = interface.get_entity_memories('Alice')
for m in memories[-5:]:
    print(f"  > {str(m)[:150]}")
```

## Common Questions and Recipes

### "Did the agent do X?"

**Option A: Keyword Matching (Limited Use)**

This works when actions use **choice-based action specs** where the exact action
text is known:

```python
# Only reliable when agent chose from fixed options like
# ["greet", "ignore", "attack"]
alice_timeline = interface.get_entity_timeline('Alice')
for entry in alice_timeline:
    if 'greet' in entry['summary'].lower():
        print(f"Found greeting at step {entry['step']}: {entry['summary']}")
```

> **Note:** This approach is fragile for free-response actions where the agent
can phrase things many ways.

**Option B: LLM-Based Interpretation (Recommended for Free Response)**

```python
alice_timeline = interface.get_entity_timeline('Alice', include_content=True)
alice_actions = '\n'.join([
    f"Step {e['step']}: {e.get('summary', '')} {e.get('response', '')}"
    for e in alice_timeline
])

prompt = f"""Based on Alice's actions below, answer: Did Alice greet Bob?

ALICE'S ACTIONS:
{alice_actions}

Consider any form of greeting: saying hello, waving, introducing herself, etc.

Answer: [YES/NO]
REASONING: [brief explanation]
"""
response = model.sample_text(prompt, max_tokens=100)
did_greet = 'YES' in response.upper()
```

### "Did the mechanic work correctly?" (LLM-based)

```python
prompt = f"""Analyze this RPG simulation log.

{log_text}

Questions:
1. HP_MENTIONED: Are HP values shown to characters? [YES/NO]
2. HP_CHANGES: Do HP values change when combat occurs? [YES/NO]
3. ENERGY_CHANGES: Do Energy values change when actions are taken? [YES/NO]
4. CHANGES_SENSIBLE: Are changes appropriate (damage reduces HP, etc)? [YES/NO]

Respond with answers and one sentence of reasoning.
"""
response = model.sample_text(prompt, max_tokens=200)
```

### "Did the narrative progress or get stuck?"

```python
# Combat naturally has similar actions - don't flag as repetitive
prompt = f"""Analyze this simulation for narrative quality.

{log_text}

IMPORTANT: In combat, similar actions (attacking, defending) are NORMAL.
Combat is NOT repetitive if HP/Energy change or new tactics are tried.

1. STORY_PROGRESSES: Does the story advance? [YES/NO]
2. STUCK_IN_LOOP: Is it truly stuck (no consequences, no evolution)? [YES/NO]
"""
```

### "What happened at step N?"

```python
entries = interface.get_step_summary(5, include_content=True)
for e in entries:
    print(f"[{e['entity_name']}] {e['entry_type']}: {e['summary']}")
```

## Comparing Simulation Runs

When comparing runs (e.g., different experimental conditions), extract parallel
metrics from both structured logs and compare side-by-side:

```python
def extract_trajectory(structured_path, component_name, value_key='Value'):
    with open(structured_path) as f:
        structured = json.load(f)
    log = SimulationLog.from_dict(structured)
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

tension_a = extract_trajectory('run_a_structured.json', 'tension_tracker')
tension_b = extract_trajectory('run_b_structured.json', 'tension_tracker')
for a, b in zip(tension_a, tension_b):
    print(f"Step {a['step']}: A={a['value']}  B={b['value']}")
```
