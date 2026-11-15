---
name: methods-simulation-analysis
description: >
  Analyze and debug social simulation outputs. Examines agent behavior logs,
  checks whether high-level interaction dynamics played out as designed, and
  identifies unexpected outcomes. Use when interpreting simulation results
  or investigating why agents behaved unexpectedly.
tags: [simulation, analysis]
---

# Debug Simulation Skill

This skill helps you analyze and debug Concordia simulation outputs to verify
that high-level simulation ideas from the user have worked correctly.

> For detailed code examples, data structure diagrams, and analysis recipes,
> see `references/log-analysis-patterns.md`.

## Study Structure Integration

When working within a study project, simulation logs live in `$STUDY_ROOT/data/`
(not `/tmp/`). Analysis scripts should go in `$STUDY_ROOT/analysis/` and their
outputs (plots, tables) in `$STUDY_ROOT/writeup/plots/` and `$STUDY_ROOT/writeup/tables/`.
Wire analysis into the Makefile so it runs via `make` targets.

## When to Use This Skill

- After running a simulation to check if it behaved as expected
- When investigating why agents made unexpected decisions
- When verifying that game masters are behaving correctly
- When comparing simulation behavior before/after code changes
- When the user asks "did it work?" about a simulation

## The AI Agent Log Interface

Concordia provides an `AIAgentLogInterface` specifically designed for coding
agents (not humans viewing HTML). Always use this interface instead of HTML
when debugging programmatically.

```python
from concordia.utils.structured_logging import AIAgentLogInterface

# After running simulation
log = simulation.play(return_structured_log=True)
interface = AIAgentLogInterface(log)
```

## Understanding the Log Data Structure

The structured log uses content deduplication: long strings are replaced with
`{'_ref': content_id}` references pointing into a `content_store`. You must
resolve these references to read actual content. Use
`SimulationLog.reconstruct_value()` for this.

Key structural points:
- **Entity entries** have key `Entity [name]` with action in `__act__.Value`
- **GM entries** are organized into phases; the `resolve` phase has the most
  interesting data (event resolutions, component outputs)
- **Custom components** may include a `Measurements` sub-dict with numeric metrics
- **Entity memories** are stored in `entity_memories` at the top level

See `references/log-analysis-patterns.md` for the full JSON layout and
extraction code.

## Two Approaches to Log Analysis

### Approach 1: Exact String Matching (Simple Checks)

For basic verification, search for specific keywords:

```python
entries = interface.search_entries('coffee shop')
found = len(entries) > 0
```

Limitations: brittle to paraphrasing, can't understand context or evaluate
appropriateness.

### Approach 2: LLM-Based Interpretation (Recommended)

For verifying whether the user's intent was achieved, LLM-based analysis is
often the best approach. Extract log content, send to an LLM with structured
questions (YES/NO + REASONING format), and parse the response.

Why this is better: understands semantic meaning, handles language variation,
can assess complex multi-step narratives, mirrors how a human would evaluate
"did it work?"

See `references/log-analysis-patterns.md` for full LLM verification code.

## Common Analysis Patterns

### Fast Overview

Always start here:

```python
overview = interface.get_overview()
# Returns: total_entries, total_steps, entities, components, entry_types
```

### Debugging Workflow: "Find the Bug"

1. Get overview to see the scope
2. Binary search through steps to find where behavior diverged
3. Drill into the specific step with full content
4. Examine the prompt to see what context the LLM received
5. Verify the prompt contains all expected components (memories, observations, instructions)
6. Verify component values reflect correct information flow between players, GMs, and simulation spec
7. Check if the response makes sense given the prompt

## Saving and Loading Logs

```python
import json
from concordia.utils.structured_logging import SimulationLog, AIAgentLogInterface

# Save
with open(f'{STUDY_ROOT}/data/simulation_log.json', 'w') as f:
    f.write(log.to_json())

# Load
log = SimulationLog.from_json(open(f'{STUDY_ROOT}/data/simulation_log.json').read())
interface = AIAgentLogInterface(log)
```

## Quick Reference

| Method | Purpose |
|--------|---------|
| `get_overview()` | High-level stats |
| `get_entity_actions(name)` | Concise action timeline for one entity |
| `get_entity_action_context(name, step)` | Full action + observations + prompt for one step |
| `get_step_summary(step, include_content)` | All entries for one step |
| `get_entity_timeline(entity, include_content)` | All entries for one entity |
| `filter_entries(...)` | Filter by entity/component/type/step |
| `search_summaries(query)` | Fast text search in entry summaries |
| `search_entries(query)` | Deep text search across all reconstructed content |
| `get_entry_content(index)` | Full reconstructed data for one entry |
| `get_component_values(...)` | Extract specific component values with ref resolution |
| `get_entity_memories(name)` | Get an entity's accumulated memories |
| `get_game_master_memories()` | Get game master memories |

## Tips

- **Verify structure before content** - Check that expected entities and game
  masters participated before analyzing what they said
- **Resolve `_ref` references** - Summary fields are often generic; resolve
  deduplicated data to get actual content
- **Use `__act__.Value` for entity actions** - The actual text lives in
  `deduplicated_data.value.__act__.Value`
- **For GM components, look in `resolve`** - Most interesting GM data is in
  `deduplicated_data.value.resolve.<component_name>.__act__`
- **Discover available components first** - Inspect `resolve` phase keys before
  extracting specific values
- **Use LLM-based analysis for high-level verification** - More robust than
  string matching
- Start with `include_content=False` for summaries, drill in with `True`
- **Truncate log text before sending to LLM** - Logs can be very large (100KB+)
- **Use structured output formats** (YES/NO with REASONING) for easy parsing
