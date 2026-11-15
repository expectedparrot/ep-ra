# Entity Prefab Selection Guide

## Contents

- [Overview](#overview)
- [Prefab Comparison Table](#prefab-comparison-table)
- [Detailed Prefab Descriptions](#detailed-prefab-descriptions)
- [Decision Framework](#decision-framework)
- [Cost and Speed Estimates](#cost-and-speed-estimates)
- [Game Master Prefabs](#game-master-prefabs)

---

## Overview

Entity prefabs determine how much "thinking" an agent does before each action. More components produce richer, more naturalistic behavior — but at the cost of more LLM calls per turn. Choosing the right prefab is a key design decision that affects both the quality of the simulation and the time/cost to run it.

The choice should be presented to the user as part of the plan (Section 7: Decisions for you).

---

## Prefab Comparison Table

| Prefab | LLM calls/turn | Components | Best for | Trade-off |
|--------|---------------|------------|----------|-----------|
| `minimal__Entity` | **1** | Instructions, Observation, Memory | Fast pilots, simple response tasks, high-volume experiments | Fastest but shallowest — agents react to observations without reflection |
| `basic__Entity` | **4** | + SituationPerception, SelfPerception, PersonBySituation | Most experiments — good balance of reasoning and speed | Agents reason about identity and situation; no conversation pacing |
| `conversational__Entity` | **6-7** | + LastSentence, ConversationDynamics, RelevantMemories | Dialogue-heavy scenarios where natural pacing matters | Richest conversation flow (converge/diverge); slowest |
| `basic_with_plan__Entity` | **5-6** | basic + long-term planning | Multi-step strategic scenarios (negotiations, games) | Adds planning component; slightly slower than basic |
| `rational__Entity` | **4-5** | Specialized for rational decision-making | Game-theoretic scenarios, price negotiation | Optimized for choices with clear payoffs |
| `puppet__Entity` | **0** | Fixed responses (scripted) | Testing, baselines, NPC-like background agents | No LLM calls — deterministic responses from a script |

---

## Detailed Prefab Descriptions

### `minimal__Entity` (1 LLM call/turn)

**Components:**
1. Instructions (constant — no LLM call)
2. Observation → Memory (writes observation to memory — no LLM call)
3. Last N Observations (retrieves recent observations — no LLM call)
4. Memory (associative memory — no LLM call)
5. **Action generation (1 LLM call)** — concatenates all component outputs and generates response

**What the agent "sees" before acting:**
- Its standing instructions and goal
- Recent observations (what happened in the simulation)
- Memory of past events

**What it does NOT do:**
- Does not reflect on "What situation am I in?"
- Does not reflect on "What kind of person am I?"
- Does not reason about conversational dynamics
- Does not retrieve similar memories

**When to use:**
- Rapid prototyping and testing
- High-volume experiments where cost/time is the binding constraint
- Scenarios where the interaction is simple (e.g., single-turn responses)
- Background agents who don't need deep reasoning

**Customizable:** Supports `extra_components` and `extra_components_index` params to add custom components without writing a new prefab.

---

### `basic__Entity` (4 LLM calls/turn)

**Components:**
1. Instructions (constant)
2. Goal (constant, if provided)
3. Observation → Memory
4. **SituationPerception (1 LLM call)** — "What situation is {name} in right now?"
5. **SelfPerception (1 LLM call)** — "What kind of person is {name}?"
6. **PersonBySituation (1 LLM call)** — "What would a person like {name} do in a situation like this?"
7. Last N Observations
8. Memory
9. **Action generation (1 LLM call)**

**What the agent "sees" before acting:**
- Everything minimal sees, PLUS:
- A synthesized understanding of its current situation
- A reflection on its own identity/personality
- A reasoning step about what someone like them would do here

**When to use:**
- **Default choice for most experiments.** Good balance of reasoning quality and speed.
- Scenarios where agents need to stay in character across turns
- Any experiment where you want agents to reason about their persona

---

### `conversational__Entity` (6-7 LLM calls/turn)

**Components:** Everything in basic, PLUS:
4. **SituationPerception (1 LLM call)**
5. **SelfPerception (1 LLM call)**
6. **LastSentence (1 LLM call)** — "Is there something in the last comment that {name} could respond to?"
7. **ConversationDynamics (1 LLM call)** — Evaluates whether to Converge (stay on topic) or Diverge (broaden)
8. **RelevantMemories (1 LLM call)** — Retrieves memories similar to current situation
9. **Action generation (1 LLM call)**
10. Optional: ConversationStyle (constant, no LLM call)

**Unique features:**
- **Converge/Diverge mechanism:** The ConversationDynamics component explicitly reasons about whether the current micro-topic is productive or exhausted. This creates natural conversation pacing — agents don't get stuck on one topic or jump erratically.
- **Hook detection:** The LastSentence component identifies what in the previous message the agent can respond to, creating more coherent back-and-forth.
- **Configurable conversation style:** Pass `conversation_style` param to shape tone.

**When to use:**
- Dialogue-heavy simulations where conversation quality is a primary output
- Studies where you want to analyze conversation dynamics (topic shifts, pacing)
- Scenarios with extended multi-turn interaction (>5 turns)
- When the report will include transcript excerpts that readers will evaluate

**When NOT to use:**
- High-volume experiments (the cost adds up fast)
- Scenarios where agents primarily make choices rather than converse
- When speed is more important than conversation richness

---

### `basic_with_plan__Entity` (5-6 LLM calls/turn)

Everything in basic, plus a long-term planning component. The agent periodically updates a plan and uses it to guide actions. Good for multi-step strategic scenarios.

### `rational__Entity` (4-5 LLM calls/turn)

Specialized for rational decision-making in game-theoretic contexts. Used as the background player prefab in haggling scenarios.

### `puppet__Entity` (0 LLM calls/turn)

Returns fixed responses from a script. Useful for:
- Testing simulation infrastructure without LLM costs
- Creating deterministic baseline agents
- NPC-like background characters with scripted behavior

---

## Decision Framework

Present this as a choice to the user during plan design (Phase 1, Step 9 or Phase 3):

**Ask:** "How much should each agent 'think' before responding?"

| If the user wants... | Recommend |
|---|---|
| Fast results, many conditions | `minimal__Entity` or `basic__Entity` |
| Natural, realistic dialogue | `conversational__Entity` |
| Strategic multi-step behavior | `basic_with_plan__Entity` |
| Good balance (default) | `basic__Entity` |
| Scripted baseline comparison | `puppet__Entity` for one agent |

**Mixed prefabs:** Different agents CAN use different prefabs in the same simulation. For example, a "confident" agent might use `basic__Entity` while a "nervous" agent uses `conversational__Entity` (to capture more hesitation and self-reflection). Or one agent could be a `puppet__Entity` to serve as a controlled baseline.

---

## Cost and Speed Estimates

All estimates assume EDSL remote inference (~10-15 seconds/call).

### Per-turn cost breakdown

| Component | Calls | Time per turn |
|-----------|-------|---------------|
| Entity: minimal | 1 | ~12s |
| Entity: basic | 4 | ~48s |
| Entity: conversational | 6-7 | ~80s |
| Game Master: dialogic | 6 | ~72s |

### Per-step total (one agent acts + GM resolves)

| Entity prefab | Total calls/step | Time per step |
|---------------|-----------------|---------------|
| minimal + dialogic GM | ~7 | ~85s |
| basic + dialogic GM | ~10 | ~120s |
| conversational + dialogic GM | ~13 | ~155s |

### Full experiment estimates (15 conditions, ~10 turns each, 2 agents)

| Setup | Total calls | Sequential | 4 parallel | Est. cost |
|-------|------------|------------|------------|-----------|
| minimal + dialogic | ~2,100 | ~3.5 hrs | ~55 min | ~$1.50 |
| basic + dialogic | ~3,000 | ~5 hrs | ~1.3 hrs | ~$2.00 |
| conversational + dialogic | ~3,900 | ~7 hrs | ~1.8 hrs | ~$2.80 |

**The two speed levers are:** (1) prefab choice (~2x between minimal and conversational) and (2) parallelism (~4x with 4 workers). Combined, switching from sequential conversational to 4-parallel minimal cuts a 15-condition experiment from ~7 hours to ~55 minutes.

---

## Game Master Prefabs

The game master also has prefab options that affect speed and behavior:

| GM Prefab | Purpose | LLM calls/step |
|-----------|---------|----------------|
| `dialogic__GameMaster` | Pure conversation — manages turn-taking, termination, and event resolution | ~6 |
| `dialogic_and_dramaturgic__GameMaster` | Adds scene management and visual narration | ~8 |
| `generic__GameMaster` | General purpose | ~5 |
| `situated__GameMaster` | Location-based (agents move between places) | ~7 |
| `interviewer__GameMaster` | Structured questionnaire delivery | ~4 |
| `scripted__GameMaster` | Pre-scripted event sequences | ~2 |

**For most social simulation experiments, `dialogic__GameMaster` is the right choice.** It handles conversation turn-taking, termination detection, and event resolution without unnecessary overhead.

### GM speed optimizations

The `dialogic__GameMaster` supports these params that affect speed:

- `acting_order: 'fixed'` — Skips the LLM call to decide who speaks next (saves 1 call/step). Use this when turn order is predetermined.
- `acting_order: 'random'` — Random speaker selection without LLM (saves 1 call/step).
- `acting_order: 'game_master_choice'` — LLM decides who speaks next (default, costs 1 extra call/step). Use for naturalistic multi-party conversations.
- `can_terminate_simulation: False` — Disables the termination check (saves 1 call/step). Use when you want the simulation to run for exactly `max_steps`.

---

## Parallelism: Running Multiple Conditions Concurrently

Each Concordia simulation is an independent process. The EDSL remote inference backend handles parallelism natively — when you submit multiple simulations, each one's LLM calls go through EDSL's job runner, which can process them concurrently.

### Why parallelism works well here

Each Concordia simulation is fully independent — no shared state between conditions. And EDSL's remote inference server can handle many concurrent jobs. The per-call latency (~10-15s) is the bottleneck, not throughput, so running N simulations in parallel gives roughly N-fold speedup.

Within a single simulation, steps are sequential (each depends on the previous), so the parallelism comes from running **multiple conditions at once**.

### Recommended: multiprocessing across conditions

```python
import multiprocessing

def run_one_condition(condition, model_name):   # pass an explicit, current model
    """Run a single simulation condition. Each process gets its own model."""
    from concordia.contrib import language_models
    import sentence_transformers

    model = language_models.language_model_setup(
        api_type="edsl", model_name=model_name
    )
    st_model = sentence_transformers.SentenceTransformer("all-mpnet-base-v2")
    embedder = lambda x: st_model.encode(x, show_progress_bar=False)

    result = build_and_run(condition, model, embedder)
    return result

# Run all conditions in parallel
with multiprocessing.Pool(processes=len(conditions)) as pool:
    results = pool.map(run_one_condition, conditions)
```

**Memory note:** Each parallel process loads its own sentence-transformer model (~400MB). With 15 parallel processes, that's ~6GB of RAM for embedders alone. If memory is tight, reduce the pool size (4-8 workers is usually a good balance).

### Alternative: ThreadPoolExecutor (lighter weight)

Since the work is I/O-bound (waiting on remote API calls), threading also works well and avoids the memory overhead of separate processes:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {
        executor.submit(run_one_condition, cond): cond
        for cond in conditions
    }
    for future in as_completed(futures):
        cond = futures[future]
        result = future.result()
        print(f"Condition {cond} complete: {result}")
```

### Sequential with progress tracking (simplest)

For small experiments where wall-clock time is acceptable:

```python
for i, condition in enumerate(conditions):
    print(f"Condition {i+1}/{len(conditions)}: {condition}")
    result = run_one_condition(condition)
    results.append(result)
    save_results(results)  # save after each condition for crash recovery
```

### Speed impact of parallelism

| Workers | 15 conditions (conversational) | 15 conditions (basic) | 15 conditions (minimal) |
|---------|-------------------------------|----------------------|------------------------|
| 1 (sequential) | ~7 hrs | ~5 hrs | ~3.5 hrs |
| 4 | ~1.8 hrs | ~1.3 hrs | ~55 min |
| 8 | ~55 min | ~40 min | ~28 min |
| 15 (all parallel) | ~28 min | ~20 min | ~14 min |

Scaling is roughly linear because EDSL's remote server handles concurrent jobs well. The main constraint is local RAM for embedders (~400MB per worker).
