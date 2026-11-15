---
name: workflow-model-selection
description: >
  Guides deliberate model selection for EDSL studies, including user-owned local endpoints. Covers task-fit,
  quality vs. cost trade-offs, cross-model comparison, how to check
  available models, spot-checking before full runs, and documenting the
  choice. Use when choosing which LLM to use for an EDSL study.
tags: [workflow, edsl]
---

# Model Selection

Choosing a model is a research design decision, not just a cost optimisation. The model you pick shapes the quality of persona simulation, the richness of open-ended reasoning, and — when you publish — the credibility of your findings. Make the choice deliberately and document it.

---

For a requested user-owned OpenAI-compatible endpoint, follow
[local inference](references/local-inference.md) for endpoint model discovery,
portable model lists, and local execution. The remote-catalog rules below apply
to hosted model selection. That reference also covers heterogeneous `--model-spec`
lists when providers or parameters differ.

## Mandatory first step: decide once, then query once

**You must do this before writing Section 6 of plan.md. No exceptions.**

Model names go stale quickly. For an ordinary text study, make exactly one bounded CLI discovery call before writing the plan:

1. Classify the task as structured, moderate free text, or high-reasoning.
2. Honor an explicitly requested provider/model before inferring a tier from
   task fit and scale. Provider constraints refer to the catalog's `service`,
   not words in the model name: an OpenAI-branded open-weight model served by
   another provider does not satisfy an OpenAI-service constraint.
   When provider comparison is not part of the research question, do not browse
   multiple providers merely to compare their catalogs.
3. Combine provider, family, modality, price sort, and limit in one command.

When a package-owned fixture already declares a model, treat that identifier as
the candidate family and verify it with the single bounded query. Do not first
scan the cheapest models and then search for the fixture model. A vision fixture
with a declared model calls only the corresponding bounded query:

```bash
ep models --service <declared-service> --search <declared-model-fragment> --vision --sort input-price --limit 10
```

For a balanced OpenAI text model, for example:

```bash
ep models --service openai --search mini --text --sort input-price --limit 10
```

Replace the service/family filters based on task fit. `--search` is a
case-insensitive substring filter, not a shell glob. Use `--search mini` or
`--search gemini`, never `*mini*`, `gpt-5*`, or similar wildcard syntax.

The server-backed result is the authority for the exact identifier,
availability, capabilities, and price. Do not run `ep models --help` during a
routine study: this skill already documents the supported filters. Do not
follow the bounded query with another provider listing, a broad catalog
listing, Python inspection, price-threshold reconstruction, or a second query
merely for reassurance. Select the best-fit candidate from the one bounded
result and retain its exact identifier for the plan, scaffold, and report.

`configured: false` does not mean a returned model is unavailable for Expected
Parrot remote inference and does not justify a second query. It only means no
matching local provider credential was detected. For remote `ep run`, keep the
returned identifier and let costing or the approved run report a real
availability error. Never replace a successful bounded result with a broad
“configured models” scan.

Use WebSearch only when the study requires a claim about frontier status,
release chronology, benchmarks, or provider capabilities that `ep models`
does not expose. Do not begin a research study with an unfiltered cheapest-model
scan: it predictably returns small models inappropriate for nuanced persona
responses and provokes follow-up queries. Choose the likely provider from task
fit, then issue one filtered call. Multi-provider and
vision studies may require one bounded CLI query per genuinely distinct
capability set only when the first query cannot answer the design question.

Useful CLI forms are:

```bash
ep models --service anthropic --sort input-price --limit 10
ep models --service google --sort input-price --limit 10
ep models --vision --sort input-price --limit 10
ep models --search gemini --sort input-price --limit 10
```

If a search unexpectedly returns zero models, first recognize it as a filter
problem rather than evidence that the family is unavailable. Remove glob
characters or over-specific punctuation and make at most one corrected bounded
query. If the installed CLI rejects a documented option, run `ep models
--help` once and correct the command. These are exceptional recovery calls,
not part of the normal workflow. Never reproduce filtering or formatting with
`python -c`.

### Step C — Choose based on tier fit

Apply the tier guidance below to select the appropriate model for this study's task complexity and purpose.

---

## Step 1: Lead with a recommendation, ask selectively

Based on the bounded CLI result, task complexity, and purpose, **propose a model
choice in `plan.md`** with clear reasoning. Do not silently default to any model
— but do not pepper the user with questions you can answer from context.

**Infer what you can:**
- If the user mentions a specific provider or model, use it.
- If they mention a client deliverable or publication, lean toward Tier 1/2 and note that cross-model comparison strengthens credibility — include this as a recommendation in the plan.
- If the study is large-scale (many agents, many questions), note cost implications in the plan.
- If the purpose is clearly exploratory or a quick pilot, a Tier 2 or 3 model is probably fine — say so.

**Only ask before finalising the plan when you genuinely cannot infer:**
- **Purpose** (pilot vs. publication) — ask only if context gives no clear signal.
- **Cost constraints** — ask only if scale is large enough that budget materially changes the model choice.

Do not routinely ask whether the user has a preferred provider or whether cross-model comparison interests them. State your recommendation and reasoning; the user can push back.

**Tier guidance** (use the bounded `ep models` result to find current names):
- Tier 1 (frontier): highest reasoning quality — use for nuanced persona simulation, free-text writing tasks, client deliverables
- Tier 2 (balanced): strong quality at lower cost — good default for most studies
- Tier 3 (cost-efficient): lower reasoning depth — only for simple structured surveys at high volume

Do not anchor to any specific provider. Choose based on task fit and what is genuinely strongest at plan time.

---

## Step 2: Match the model to the task

Not all survey tasks need the same model capability. Work through this before proposing a choice:

### Task complexity

| Task type | Requirement | Suggested tier |
|-----------|-------------|----------------|
| Multiple choice, rating scales, simple agree/disagree | Low reasoning load | Tier 2 or 3 acceptable |
| Open-ended free text, opinion justification | Moderate reasoning | Tier 2 minimum |
| Nuanced persona simulation (e.g., complex demographic backstories, ideological consistency) | High reasoning | Tier 1 or 2 |
| Ethical dilemmas, political reasoning, multi-step argument | High reasoning | Tier 1 or 2 |
| Vision / image tasks | Must support vision | Tier 1 or 2, vision-capable only |
| Long documents or complex scenarios in context | Large context window needed | Check model context limits |
| Study where model knowledge IS the variable (e.g., benchmarking what models know) | Comparison across models is the point | Multi-model by design |

### Purpose and stakes

Every study the agent runs should be treated as production quality — do not default to cheaper or weaker models simply because a study is exploratory or a skill demonstration. The correct way to manage cost is to reduce agent count or question count, not to downgrade the model.

| Purpose | Guidance |
|---------|----------|
| Any study | Use a model that is appropriate for the task's reasoning demands — do not self-impose a "test run" penalty |
| Client deliverable or publication | Tier 1 or 2; cross-model comparison across providers strongly recommended |
| Exploring a new research question | Use a strong model to understand the full response space; do not prematurely constrain with a weak model |
| Large-scale study where cost is genuinely constraining | Run a spot-check with the strong model first; only step down after confirming response quality holds |

---

## Step 3: Cost vs. quality — the right framing

**When stating estimated cost in `plan.md`, always decompose it.** "Estimated cost: $0.50–$1.00" means nothing to a user who doesn't know what drives EDSL costs. Write it as: *"$0.50–$1.00 covers running 12 AI personas through 8 questions — roughly $0.05 per agent response. A full re-run would cost the same."* The components are always: number of agents × number of questions × approximate per-call cost. Estimate per-call cost from the model tier (Tier 1 ≈ $0.01–$0.05 per call, Tier 2 ≈ $0.002–$0.01, Tier 3 ≈ $0.0005–$0.002 — verify against current pricing). If you are uncertain, give a range and say so.

Cost is a legitimate consideration but it should not automatically push you to a weaker model. The correct levers are:

- **Reduce agent count** rather than downgrading the model if the task genuinely requires nuance
- **Reduce question count** by focusing on the most important questions
- **Run a smaller pilot first** with the strong model, confirm response quality, then decide whether a cheaper model holds up

A study run with a weak model on a nuanced task may produce bland, generic responses that look like results but carry no real signal. That is worse than a smaller, high-quality run.

---

## Step 4: Lock the selected identifier

Never hardcode model strings from memory—they go stale. Reuse the exact model
identifier returned by the mandatory query above when writing the plan and
scaffolding `study_model_list.py`; do not query the catalog again at
implementation time.

If the user requests a new exact model (including adding one to a comparison),
or changes the provider, tier, or modality after seeing the plan, the design has
materially changed and one new bounded query for that request is appropriate.
The query-once rule applies to an unchanged selection decision, not the whole
conversation. Do not declare a newly requested model unavailable from memory or
an earlier differently filtered result. Verify that request with the catalog;
if it cannot be resolved, pause affected execution and ask for direction.
A routine transition from approved plan to implementation is not a reason to
query again.

Carry every still-applicable user constraint into the revised plan and model
artifact. Before costing/running that artifact, follow
[requested-model verification](references/requested-models.md). An unresolved
request does not authorize omitting a model, substituting a provider, or running
the earlier selection. Changed models require fresh scoped costing and approval.

### Current model tiers (use the working catalog; names change)

| Tier | Capability | Typical use |
|------|-----------|-------------|
| Tier 1 | Highest reasoning, most expensive | Publication research, nuanced personas, complex reasoning, client deliverables |
| Tier 2 | Strong balance of quality and cost | Most studies — good default when no strong reason to go up or down |
| Tier 3 | Cost-efficient, lower reasoning depth | Simple structured surveys at high volume, internal pilots, rapid iteration |

Within each tier, use the current working catalog. Use WebSearch only when the
study's claims depend on recency or external benchmark evidence.

---

## Step 5: Cross-model comparison — when and why

### When cross-model comparison adds value

- **Publication-quality research**: Results that replicate across Claude, GPT, and Gemini are much stronger evidence than single-model results
- **Novel or contested topics**: When you don't know how models will respond, cross-model comparison reveals whether the result is model-specific or robust
- **Client deliverables where credibility matters**: "Four different frontier models agree" is a stronger claim than "one model said this"
- **When the topic touches known model biases**: Different models have different training data and RLHF fine-tuning — comparing them reveals where the signal is real vs. model-specific

### When a single model is fine

- Rapid internal pilots where you're testing the survey instrument, not the results
<!-- lint-allow-model: illustrative example, not a model recommendation -->
- Studies where the model is explicitly a fixed variable ("what does GPT-4o think about X?")
- When cost constraints make multi-model runs impractical and the purpose is exploratory

### How to run multi-model

```python
from edsl import ModelList, Model

# Three providers for strong cross-model confidence
# WebSearch to find current frontier models, then confirm names with ep models
model_list = ModelList([
    Model("..."),  # OpenAI frontier — WebSearch + ep models
    Model("..."),  # Anthropic frontier — WebSearch + ep models
    Model("..."),  # Google frontier — WebSearch + ep models
])

# Two-provider minimum for most studies
model_list = ModelList([
    Model("..."),  # OpenAI frontier — WebSearch + ep models
    Model("..."),  # Anthropic frontier — WebSearch + ep models
])
```

Results will include a `model.model` column allowing you to compare responses by model.

---

## Step 6: Spot-check before the full run

Before committing to a large run, run 2–3 agents through the full survey and read the actual responses:

```bash
# Quick pilot: save a pilot jobs.ep with 2-3 agents, then run through the CLI
ep run edsl_jobs/pilot/jobs.ep --output data/results_pilot.ep
```

```bash
ep results columns --file data/results_pilot.ep
ep results head data/results_pilot.ep --rows 5
```

Check for:
- **Refusals or safety blocks** — if the model refuses certain questions, reframe or switch models
- **Sycophancy** — does the model just agree with implied correct answers rather than simulating the persona?
- **Generic responses** — are free-text answers substantive or boilerplate? Boilerplate suggests the model is too small for the task
- **Persona consistency** — does a conservative 65-year-old respond differently from a progressive 25-year-old on politically sensitive questions? If not, the persona conditioning is not working

If the spot-check reveals thin or implausible responses, consider upgrading the model before running the full job. It is much cheaper to catch this early.

---

## Step 7: Document the choice in the report

The Methods section of every report must state:

1. Which model(s) were used (exact name as confirmed by `ep models`)
2. Why that model was chosen (task fit, quality considerations, cost constraints, cross-model strategy)
3. For multi-model studies: how results compared across models and whether they converged

Write this for a reader who may not know what model tiers mean. "We used GPT-5.2" is not enough -- say what that means for the quality and character of the results. A reader who understands the choice can better evaluate the findings.

See `research_agent/skills/report-authoring/references/transparency.md` for the full transparency standard, including agent configuration tables, verbatim response examples, and the optional "How this study works" explainer for readers new to AI simulation.

**Example Methods text -- single model:**

> Simulated respondents were run using GPT-5.2 (OpenAI). This Tier 1 model was selected because the study requires nuanced persona-conditioned reasoning: agents must maintain consistent demographic perspectives across 14 questions including open-ended justifications. A cheaper model was considered but rejected after a pilot showed more generic free-text responses at that tier. A pilot run of three agents confirmed that GPT-5.2 responses were substantive and persona-consistent before the full job was committed.

**Example Methods text -- multi-model:**

> We ran all agents against two frontier models: GPT-5.2 (OpenAI) and Claude Sonnet 4.6 (Anthropic). Cross-model comparison was used to assess whether findings were robust to model choice or specific to one provider's training data and fine-tuning. Where results converged across models, we report the pooled finding. Where they diverged, we report both and discuss possible explanations in the Limitations section.

**Example Methods text -- cost-driven tier choice:**

> Given the scale of this study (200 agents x 18 questions), we used GPT-5-mini after confirming in a pilot run that responses to these structured rating questions were substantive and persona-consistent at this model tier. GPT-5-mini is a strong Tier 2 model well-suited to structured survey questions; we would use a Tier 1 model for any follow-up study requiring open-ended reasoning depth. Free-text justification questions in a follow-up study will use a Tier 1 model.

---

## Checklist before finalising study_model_list.py

- [ ] Model choice proposed in plan.md with explicit reasoning (task complexity, purpose, scale); user asked follow-up questions only when context was insufficient to make a recommendation
- [ ] Confirmed model name(s) with one bounded `ep models` query per required capability/provider — no hardcoded stale names
- [ ] Model tier matches task complexity (not just lowest cost)
- [ ] Spot-check run with 2–3 agents — responses are substantive and persona-consistent
- [ ] If cross-model comparison is used, at least two providers represented
- [ ] Model choice documented in plan.md before running the full job
- [ ] Model choice will be documented in the report's Methods section

---

## Runtime: Handling unavailable models

If a planned model is unavailable at runtime (missing API key, provider outage, model deprecated), **do NOT silently fall back to a different provider or model.** This is a research design change that requires user consent.

**Required steps:**

1. **Report the specific error** — e.g., "Anthropic API key not found" or "Model X returned 401."
2. **State what this means** — e.g., "The planned cross-model comparison cannot include Anthropic models."
3. **Propose alternatives and ask** — e.g., "I can (a) proceed with OpenAI only, (b) wait while you add the key, or (c) substitute a different provider. Which do you prefer?"
4. **Do not proceed until the user responds.**

A silent model downgrade changes the study design. Proceeding without consent violates the principle that model choice is a deliberate research decision.
