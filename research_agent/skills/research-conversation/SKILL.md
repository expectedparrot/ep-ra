---
name: research-conversation
description: >
  Designs, runs, and analyzes multi-agent conversation simulations using
  the expectedparrot/conversation package. Use when the user wants to
  simulate a structured dialogue between LLM agents — such as bargaining,
  negotiation, debate, or role-play — run many parallel conversations
  across varied conditions, and analyze outcomes with EDSL. Lighter-weight
  than skill:research-social-simulation; best for focused two-to-five agent
  dialogues with clear conversational goals and measurable outcomes.
tags: [study-type, simulation, qualitative, analysis, external-tool]
---

# Conversation Simulation

This skill walks through designing a multi-agent conversation study in five phases. Each phase produces a concrete artifact. Run them in order.

| Phase | What happens | Artifact |
|-------|-------------|----------|
| 1. Install | Install the `conversation` package from GitHub | Working `import conversation` |
| 2. Design | Define agents, scenario, and stopping conditions | Agent definitions + `Conversation` config |
| 3. Pilot | Run one conversation and verify quality | Transcript + initial analysis |
| 4. Batch | Run many parallel conversations across conditions | `ConversationList` results |
| 5. Analyze | Extract outcomes with EDSL questions and summarize | Results dataframe + report |

## When to use this vs. skill:research-social-simulation

| | `skill:research-conversation` | `skill:research-social-simulation` |
|---|---|---|
| Setup cost | Low — define agents, run | High — build JSON blueprint, configure Concordia |
| Best for | 2–5 agent dialogue with clear goals | Complex multi-agent environments with environmental context |
| Agent cognition | Simple role + goal traits | Rich memory, perception, and action components |
| Experimental design | Vary agent traits across runs | Full factorial design with causal graph |
| Analysis | EDSL questions on transcripts | Statistical causal effects across conditions |
| Iteration speed | Fast — minutes to a working pilot | Slower — blueprint design takes time |

Use this skill when the research question is about what agents *say* in dialogue. Use skill:research-social-simulation when you need richer agent cognition or a full causal experiment.

---

## Phase 1: Install

The `conversation` package is not on PyPI — install directly from GitHub:

```bash
pip install git+https://github.com/expectedparrot/conversation.git
```

Verify:

```python
from conversation import Conversation, ConversationList
print("OK")
```

The package requires EDSL and an Expected Parrot API key (`EXPECTED_PARROT_API_KEY`).

---

## Phase 2: Design the Conversation

### Define agents

Each agent needs a `name` and `traits` that specify its role and goal in the conversation. Keep traits concrete and actionable.

```python
from edsl import Agent, AgentList

seller = Agent(
    name="Seller",
    traits={
        "role": "You are selling a used bicycle. Your minimum acceptable price is $80.",
        "goal": "Sell for as much above your minimum as possible. Say DEAL to close."
    }
)

buyer = Agent(
    name="Buyer",
    traits={
        "role": "You want to buy a used bicycle. Your maximum budget is $120.",
        "goal": "Buy for as little as possible. Say DEAL to close."
    }
)
```

### Configure the conversation

```python
from conversation import Conversation

c = Conversation(
    agent_list=AgentList([seller, buyer]),
    max_turns=12,
    verbose=True,            # prints each turn as it arrives
    stopping_function=None,  # see below
)
```

Key parameters:

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `max_turns` | 20 | Hard cap on turns |
| `stopping_function` | None | Callable `(statements) → bool`; stops early when `True` |
| `next_speaker_generator` | round-robin | Controls turn order |
| `verbose` | False | Print statements live |
| `per_round_message_template` | None | Jinja template injected each turn (useful for game state) |

### Stopping conditions

Define a stopping function when the conversation has a natural endpoint — a deal reached, consensus achieved, or keyword spoken:

```python
def stop_on_deal(statements):
    return bool(statements) and "DEAL" in statements[-1].text.upper()

c = Conversation(
    agent_list=AgentList([seller, buyer]),
    max_turns=12,
    stopping_function=stop_on_deal,
)
```

### Turn-taking strategies

Import from `conversation.next_speaker_utilities`:

```python
from conversation.next_speaker_utilities import (
    default_turn_taking_generator,        # round-robin (default)
    turn_taking_generator_with_focal_speaker,  # one agent speaks more often
    random_turn_taking_generator,          # random each turn
)
```

For most two-agent dialogues, the default round-robin is correct.

---

## Phase 3: Pilot

Run a single conversation and read the transcript before scaling up.

```python
c = Conversation(
    agent_list=AgentList([seller, buyer]),
    max_turns=12,
    verbose=True,
    stopping_function=stop_on_deal,
)
c.converse()
```

`converse()` retries up to 3 times with 5-second delays on transient errors.

### What to check in the pilot

1. **Role adherence** — Does each agent stay in character and pursue its stated goal?
2. **Stopping condition** — Did it fire at the right moment, or too early/late?
3. **Conversation quality** — Is the dialogue coherent and realistic?
4. **Turn balance** — Are agents dominating or being passive in ways that seem wrong?
5. **Outcome observability** — Can you tell from the transcript whether the desired outcome occurred?

If anything looks off, revise agent traits or the stopping function before running the batch.

---

## Phase 4: Batch Simulations

Once the pilot looks good, run many conversations in parallel across varied conditions.

### Pattern: vary agent traits across conditions

```python
from conversation import Conversation, ConversationList
from edsl import Agent, AgentList

def make_bargaining_conversation(seller_min, buyer_max):
    seller = Agent(
        name="Seller",
        traits={
            "role": f"You are selling a used bicycle. Your minimum price is ${seller_min}.",
            "goal": "Sell for as much above your minimum as possible. Say DEAL to close."
        }
    )
    buyer = Agent(
        name="Buyer",
        traits={
            "role": f"You want to buy a used bicycle. Your maximum budget is ${buyer_max}.",
            "goal": "Buy for as little as possible. Say DEAL to close."
        }
    )
    return Conversation(
        agent_list=AgentList([seller, buyer]),
        max_turns=12,
        stopping_function=lambda s: bool(s) and "DEAL" in s[-1].text.upper()
    )

# Define conditions: (seller_min, buyer_max)
conditions = [
    (80, 120),   # surplus = 40, deal likely
    (80, 90),    # surplus = 10, deal possible
    (80, 80),    # no surplus, deal uncertain
    (80, 70),    # negative surplus, no deal possible
]

conversations = [make_bargaining_conversation(sv, bv) for sv, bv in conditions]
```

### Run in parallel

```python
conv_list = ConversationList(conversations)
conv_list.run()  # thread-based parallelism
```

### Replications

For statistical reliability, run each condition multiple times. Wrap the factory in a loop:

```python
n_reps = 5
conversations = [
    make_bargaining_conversation(sv, bv)
    for sv, bv in conditions
    for _ in range(n_reps)
]
conv_list = ConversationList(conversations)
conv_list.run()
```

Confirm the total run count with the user before executing (e.g., "4 conditions × 5 reps = 20 conversations").

---

## Phase 5: Analyze Results

### Export to EDSL

Each `Conversation` exposes two export methods:

- `c.to_results()` — returns an EDSL `Results` object with one row per statement (speaker, text, turn index)
- `c.summarize()` — returns a `Scenario` with the full transcript as a field, suitable for running analysis questions

For a `ConversationList`:

```python
summaries = conv_list.summarize()  # returns ScenarioList — one scenario per conversation
```

### Ask analysis questions on transcripts

```python
from edsl import QuestionYesNo, QuestionNumerical, QuestionFreeText, Survey

q_deal = QuestionYesNo(
    question_name="reached_deal",
    question_text="Did the two parties reach a deal in this conversation? {{ scenario.conversation }}"
)

q_price = QuestionNumerical(
    question_name="final_price",
    question_text=(
        "If a deal was reached in this conversation, what was the agreed price? "
        "Return 0 if no deal was reached. {{ scenario.conversation }}"
    )
)

q_tone = QuestionFreeText(
    question_name="negotiation_style",
    question_text=(
        "In one sentence, how would you characterize the negotiation style "
        "(cooperative, adversarial, etc.)? {{ scenario.conversation }}"
    )
)

results = Survey(questions=[q_deal, q_price, q_tone]).by(summaries).run()
df = results.to_pandas()
print(df[["reached_deal", "final_price", "negotiation_style"]])
```

### Attaching condition metadata

To connect analysis results back to conditions, add metadata to each scenario before running:

```python
from edsl import Scenario, ScenarioList

labeled_summaries = ScenarioList([
    Scenario({**s.data, "seller_min": sv, "buyer_max": bv, "rep": r})
    for (sv, bv), r, s in zip(
        [c for c in conditions for _ in range(n_reps)],
        [i % n_reps for i in range(len(conversations))],
        conv_list.summarize()
    )
])

results = Survey(questions=[q_deal, q_price]).by(labeled_summaries).run()
df = results.to_pandas()
df.groupby("scenario.buyer_max")["answer.reached_deal"].mean()
```

### Analysis patterns

| Research question | Approach |
|---|---|
| Did a deal happen? | `QuestionYesNo` on transcript |
| What was the outcome value? | `QuestionNumerical` on transcript |
| Why did negotiations break down? | `QuestionFreeText` on failed cases |
| How does surplus affect deal rate? | Group `reached_deal` by `buyer_max - seller_min` |
| What language correlates with success? | `QuestionFreeText` asking for key phrases or tactics |

For quantitative comparisons across conditions, use pandas groupby or simple chi-squared / t-tests on the extracted outcomes.

---

## Design Guidance

### Agent trait quality

- Give each agent a **clear private valuation or constraint** that the other agent does not know. This creates genuine information asymmetry.
- Give each agent a **goal** that specifies their optimization target and a **termination signal** (e.g., "say DEAL to close").
- Avoid overly long traits — one or two sentences per trait key is enough.

### Number of turns

Start with `max_turns=10–15` for two-agent bargaining. More turns rarely change outcomes but raise cost. Use a stopping function to exit early when resolved.

### Number of agents

Two-agent conversations are the most interpretable. Three-agent conversations (buyer, seller, mediator) add interesting dynamics but complicate analysis. Beyond five agents, coherence usually degrades.

### When to use `per_round_message_template`

Use this for game-state scenarios where agents need to track evolving information — chip counts, inventory, scores:

```python
# Template receives `round_message` each turn
c = Conversation(
    agent_list=AgentList([alice, bob]),
    max_turns=5,
    per_round_message_template=(
        "Current chip counts: Alice={{ alice_chips }}, Bob={{ bob_chips }}. "
        "Say DEAL to accept the current offer."
    )
)
```

---

## Common Pitfalls

- **Vague traits produce vague dialogue.** "You are a negotiator" gives the agent nothing to work with. Give it a specific valuation, position, and termination signal.
- **Stopping function fires on the wrong speaker.** If both agents can say DEAL, check `statements[-1].speaker` to enforce who has final say, or require both to agree.
- **Not running enough replications.** A single conversation is anecdote, not data. Run at least 5 per condition (10+ for statistical tests on binary outcomes).
- **Forgetting to label conditions in the ScenarioList.** Without metadata, you cannot map results back to conditions. Add condition labels before calling `.by()`.
- **max_turns too low.** If conversations consistently hit the turn cap without resolving, increase `max_turns` or tighten agent goals.
- **Running the full batch before piloting.** Always run one conversation with `verbose=True` first. A broken trait or stopping function wastes the whole batch.

---

## Study Structure

```
bargaining-study/
  README.md
  run_pilot.py          # single conversation with verbose=True
  run_batch.py          # ConversationList across conditions
  analyze.py            # EDSL Survey on summaries
  data/
    raw/                # conversation summaries from conv_list.summarize()
    cooked/             # analysis results DataFrames
  report/
    findings.md
```

---

## Quick Reference

| Task | Code |
|------|------|
| Install | `pip install git+https://github.com/expectedparrot/conversation.git` |
| Single conversation | `c = Conversation(agent_list=AgentList([a, b]), max_turns=10); c.converse()` |
| Stop on keyword | `stopping_function=lambda s: bool(s) and "DEAL" in s[-1].text.upper()` |
| Batch parallel run | `conv_list = ConversationList(conversations); conv_list.run()` |
| Export transcripts | `summaries = conv_list.summarize()  # ScenarioList` |
| Run analysis questions | `Survey([q1, q2]).by(summaries).run()` |
| Results as DataFrame | `results.to_pandas()` |
| Random turn order | `from conversation.next_speaker_utilities import random_turn_taking_generator` |
