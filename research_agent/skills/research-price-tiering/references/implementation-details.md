# Price Tiering Implementation Details

Detailed code examples, optimization logic, and report template for the price-tiering workflow. See the parent `SKILL.md` for the high-level workflow and design principles.

## Contents

- [Step 1: Feature and Tier Structure Code](#step-1-feature-and-tier-structure-code)
- [Step 2: Customer Persona Panel Code](#step-2-customer-persona-panel-code)
- [Step 3: Bundle WTP Survey Code](#step-3-bundle-wtp-survey-code)
- [Step 4: Sample and Preview Code](#step-4-sample-and-preview-code)
- [Step 5: Full Survey Run Code](#step-5-full-survey-run-code)
- [Step 6: Price Optimization Code](#step-6-price-optimization-code)
- [Step 7: Report Template](#step-7-report-template)

---

## Step 1: Feature and Tier Structure Code

### Defining features

```python
features = {
    "basic_analytics": "Page views, sessions, and bounce rate dashboard",
    "advanced_analytics": "Funnel analysis, cohort tracking, and custom reports",
    "ab_testing": "Run split tests on landing pages with statistical significance",
    "api_access": "RESTful API with 10,000 requests/month",
    "sso": "SAML-based single sign-on for enterprise identity providers",
    "dedicated_support": "24/7 dedicated account manager and priority ticket queue",
}
```

### Candidate tier structures

Each structure is a dict mapping tier names to lists of feature keys. Tiers are nested -- each higher tier includes everything in lower tiers plus new features.

```python
# Structure A: analytics-gated
structure_a = {
    "Basic":      ["basic_analytics"],
    "Pro":        ["basic_analytics", "advanced_analytics", "ab_testing"],
    "Enterprise": ["basic_analytics", "advanced_analytics", "ab_testing",
                   "api_access", "sso", "dedicated_support"],
}

# Structure B: support-gated
structure_b = {
    "Basic":      ["basic_analytics", "advanced_analytics"],
    "Pro":        ["basic_analytics", "advanced_analytics", "ab_testing", "api_access"],
    "Enterprise": ["basic_analytics", "advanced_analytics", "ab_testing",
                   "api_access", "sso", "dedicated_support"],
}
```

### Building the ScenarioList

Each scenario represents one (structure, tier) combination. The scenario text describes the complete plan so the agent evaluates the bundle holistically.

```python
from edsl import ScenarioList, Scenario

def build_plan_scenarios(structures, features):
    """Build scenarios for bundle WTP survey.

    Each scenario is a complete plan (tier within a structure).
    The agent sees the full feature list and evaluates the bundle.
    """
    scenarios = []
    for struct_name, tiers in structures.items():
        for tier_name, feature_keys in tiers.items():
            feature_list = "\n".join(
                f"- {features[k]}" for k in feature_keys
            )
            scenarios.append(Scenario({
                "structure_name": struct_name,
                "tier_name": tier_name,
                "plan_description": (
                    f"**{tier_name} Plan** — includes:\n{feature_list}"
                ),
                "n_features": str(len(feature_keys)),
            }))
    return ScenarioList(scenarios)
```

> **Why structure_name and tier_name are in the scenario**: Both fields must appear in `question_text` (EDSL requirement). We reference them in the WTP question so agents know which plan they're evaluating.

### Tier costs

Store marginal costs separately:

```python
import json

tier_costs = {
    "Structure A": {"Basic": 0, "Pro": 5, "Enterprise": 25},
    "Structure B": {"Basic": 2, "Pro": 8, "Enterprise": 25},
}

with open("data/raw/tier_costs.json", "w") as f:
    json.dump(tier_costs, f, indent=2)
```

If costs are unknown, default to $0 for all tiers.

---

## Step 2: Customer Persona Panel Code

```python
from edsl import AgentList, Agent

agent_list = AgentList([
    Agent(
        traits={
            "persona": "A solo freelance designer who uses surveys to collect "
                       "client feedback. Very price-sensitive, budget under "
                       "$30/month for any single tool.",
            "segment": "freelancer",
            "market_size": "50000",
        }
    ),
    Agent(
        traits={
            "persona": "A marketing manager at a 50-person SaaS startup. "
                       "Needs A/B testing and analytics. Budget-aware but "
                       "willing to pay for ROI-driving features.",
            "segment": "startup",
            "market_size": "15000",
        }
    ),
    Agent(
        traits={
            "persona": "A VP of Engineering at a 500-person enterprise. "
                       "Requires SSO, API access, and dedicated support. "
                       "Budget is not the primary concern; compliance and "
                       "reliability are.",
            "segment": "enterprise",
            "market_size": "2000",
        }
    ),
])
```

### Market size guidance

| Segment | Typical ratio | Example (100K TAM) |
|---------|--------------|---------------------|
| Solo / freelancer | 50-60% | 50,000 |
| Small team (5-50) | 25-30% | 25,000 |
| Mid-market (50-500) | 10-15% | 15,000 |
| Enterprise (500+) | 2-5% | 3,000 |

The absolute numbers don't matter for comparing structures -- only the ratios between segments. The optimizer produces revenue in dollars that can be scaled by any overall market multiplier.

---

## Step 3: Bundle WTP Survey Code

```python
from edsl import Survey
from edsl.questions import QuestionNumerical, QuestionFreeText

q_wtp = QuestionNumerical(
    question_name="bundle_wtp",
    question_text=(
        "You are evaluating an online software product. Consider this "
        "subscription plan:\n\n"
        "{{ scenario.plan_description }}\n\n"
        "This is the {{ scenario.tier_name }} tier "
        "(part of pricing structure '{{ scenario.structure_name }}').\n\n"
        "What is the maximum monthly amount (in US dollars) you would be "
        "willing to pay for a subscription to this plan? Consider the "
        "features together as a bundle — some features may be more "
        "valuable in combination than alone."
    ),
    min_value=0,
    max_value=500,
)

q_reasoning = QuestionFreeText(
    question_name="wtp_reasoning",
    question_text=(
        "You said you'd pay ${{ bundle_wtp.answer }} per month for the "
        "{{ scenario.tier_name }} plan. In 1-2 sentences, explain what "
        "makes this plan worth that amount (or not worth more) to you."
    ),
)

survey = Survey([q_wtp, q_reasoning])
```

### Calibrating max_value

| Product type | Suggested max_value |
|---|---|
| Consumer app | $50 |
| SMB SaaS tool | $200-300 |
| Enterprise platform | $500-1,000 |
| API / infrastructure | $500 |

### Why bundle WTP is better

- **Complementarities**: An agent who sees "Advanced Analytics + A/B Testing" together values the combination more than the sum of parts -- they can run tests and measure results.
- **Table-stakes features**: An agent won't pay much for "Unlimited Surveys" alone, but a plan without it feels incomplete. Bundle WTP captures this.
- **Realistic evaluation**: Real customers compare plans, not individual features.

---

## Step 4: Sample and Preview Code

```bash
# job_pilot contains the first three plans and one agent per segment.
ep run edsl_jobs/job_pilot/jobs.ep --output data/results_pilot.ep
ep results head data/results_pilot.ep \
  --column scenario.tier_name \
  --column scenario.structure_name \
  --column agent.segment \
  --column answer.bundle_wtp \
  --rows 15
```

### What to check

- **Higher tiers get higher WTP**: If Pro doesn't beat Basic for most agents, the additional features may not be compelling.
- **Segment differentiation**: Enterprise agents should bid higher than freelancers.
- **Price sensitivity works**: Freelancers should bid much less than enterprise.
- **Not at ceiling**: If many agents hit `max_value`, increase it.
- **Plausible magnitudes**: Does $X/month make sense for this product category?

Present results to the user and ask whether the values look reasonable before running the full survey.

---

## Step 5: Full Survey Run Code

Total API calls = (scenarios per structure x number of structures) x agents x models x questions.

For 2 structures x 3 tiers each x 12 agents x 1 model x 2 questions = 144 API calls.

```python
# In run_job.py
from pathlib import Path
from study_survey import survey
from study_scenario_list import scenario_list
from study_agent_list import agent_list
from study_model_list import model_list

_STUDY_ROOT = Path(__file__).resolve().parent.parent.parent
output = _STUDY_ROOT / "data" / "results"
output.parent.mkdir(parents=True, exist_ok=True)

job = survey.by(scenario_list).by(agent_list).by(model_list)

# Cost check
try:
    estimate = job.estimate_remote_job_cost()
    print(f"Estimated cost: ${estimate.total_cost_usd:.4f}")
except Exception as e:
    print(f"Could not estimate cost: {e}")

# Build `jobs.ep` from survey.ep, scenario_list.ep, agent_list.ep, and model_list.ep,
# then run from the Makefile:
# ep run edsl_jobs/job_a/jobs.ep \
#   --remote_inference_description "Survey tool subscription tiers - freelancer startup enterprise" \
#   --results_description "Survey tool subscription tiers - freelancer startup enterprise" \
#   --output data/results.ep
```

---

## Step 6: Price Optimization Code

### 6.1 Load and Pivot Data

```python
from pathlib import Path
from edsl import Results
import numpy as np
import json

STUDY_ROOT = Path(__file__).resolve().parent.parent
results = Results.git.load(str(STUDY_ROOT / "data" / "results.ep"))
df = results.to_pandas()
df["answer.bundle_wtp"] = df["answer.bundle_wtp"].astype(float)

# Extract market sizes per agent
market_sizes = {}
for _, row in df.drop_duplicates("agent.persona").iterrows():
    market_sizes[row["agent.persona"]] = float(row["agent.market_size"])
```

### 6.2 Choice Model

For a given tier structure and price vector, each agent picks the tier that maximizes surplus (bundle_WTP - price), or opts out if all surplus is negative. Revenue is weighted by market size.

```python
def compute_market_revenue(wtp_by_tier, prices, market_sizes_arr, tier_costs=None):
    """Compute total market revenue for a price vector.

    wtp_by_tier: (n_agents, n_tiers) -- each agent's WTP for each tier
    prices:      (n_tiers,)          -- price for each tier
    market_sizes_arr: (n_agents,)    -- market size weight per agent
    tier_costs:  (n_tiers,) or None  -- marginal cost per tier

    Returns: total_revenue (float), choices (n_agents,) array of tier indices
    """
    if tier_costs is None:
        tier_costs = np.zeros(len(prices))

    surplus = wtp_by_tier - prices  # (n_agents, n_tiers)

    # Each agent picks best tier with positive surplus, or opts out
    n_agents, n_tiers = surplus.shape
    choices = np.full(n_agents, -1, dtype=int)  # -1 = opt out
    for i in range(n_agents):
        best_surplus = 0
        best_tier = -1
        for t in range(n_tiers):
            if surplus[i, t] > best_surplus:
                best_surplus = surplus[i, t]
                best_tier = t
        choices[i] = best_tier

    # Revenue = sum over agents of: market_size * (price - cost) for chosen tier
    revenue = 0.0
    for i in range(n_agents):
        t = choices[i]
        if t >= 0:
            revenue += market_sizes_arr[i] * (prices[t] - tier_costs[t])

    return revenue, choices
```

### 6.3 Price Grid Search

Search over candidate prices for each tier. Candidate prices come from the distribution of bundle WTP values.

```python
import itertools

def optimize_prices(wtp_by_tier, market_sizes_arr, tier_costs=None,
                    n_price_candidates=20):
    """Find revenue-maximizing prices for a tier structure.

    wtp_by_tier: (n_agents, n_tiers) -- WTP per agent per tier
    market_sizes_arr: (n_agents,)
    tier_costs: (n_tiers,) or None
    n_price_candidates: granularity of price grid

    Returns: dict with best_prices, best_revenue, all agents' choices
    """
    n_agents, n_tiers = wtp_by_tier.shape
    if tier_costs is None:
        tier_costs = np.zeros(n_tiers)

    # Build candidate prices per tier from WTP quantiles
    candidates_per_tier = []
    for t in range(n_tiers):
        vals = wtp_by_tier[:, t]
        vals = vals[vals > 0]
        if len(vals) == 0:
            candidates_per_tier.append(np.array([tier_costs[t] + 1]))
            continue
        quantiles = np.linspace(0.05, 0.95, n_price_candidates)
        cands = np.quantile(vals, quantiles)
        cands = cands[cands > tier_costs[t]]
        if len(cands) == 0:
            cands = np.array([tier_costs[t] + 1])
        candidates_per_tier.append(np.unique(np.round(cands, 2)))

    best_revenue = -np.inf
    best_prices = None
    best_choices = None

    for price_combo in itertools.product(*candidates_per_tier):
        prices = np.array(price_combo)
        # Enforce strictly increasing prices (Basic < Pro < Enterprise)
        if any(prices[i] >= prices[i + 1] for i in range(n_tiers - 1)):
            continue
        revenue, choices = compute_market_revenue(
            wtp_by_tier, prices, market_sizes_arr, tier_costs
        )
        if revenue > best_revenue:
            best_revenue = revenue
            best_prices = prices.copy()
            best_choices = choices.copy()

    return {
        "best_prices": best_prices.tolist(),
        "best_revenue": best_revenue,
        "choices": best_choices,
    }
```

### 6.4 Run Optimization for Each Structure

```python
structures = {"Structure A": structure_a, "Structure B": structure_b}
tier_labels = ["Basic", "Pro", "Enterprise"]

results_by_structure = {}

for struct_name, tiers in structures.items():
    # Build WTP matrix for this structure: (n_agents, n_tiers)
    struct_df = df[df["scenario.structure_name"] == struct_name]

    agents = sorted(struct_df["agent.persona"].unique())
    n_agents = len(agents)
    n_tiers = len(tier_labels)

    wtp_matrix = np.zeros((n_agents, n_tiers))
    ms_array = np.zeros(n_agents)

    for i, persona in enumerate(agents):
        ms_array[i] = market_sizes[persona]
        for t, tier_name in enumerate(tier_labels):
            row = struct_df[
                (struct_df["agent.persona"] == persona) &
                (struct_df["scenario.tier_name"] == tier_name)
            ]
            if len(row) > 0:
                wtp_matrix[i, t] = row["answer.bundle_wtp"].values[0]

    # Load tier costs for this structure
    with open(STUDY_ROOT / "data" / "raw" / "tier_costs.json") as f:
        all_costs = json.load(f)
    tc = np.array([all_costs.get(struct_name, {}).get(t, 0) for t in tier_labels])

    result = optimize_prices(wtp_matrix, ms_array, tc)

    results_by_structure[struct_name] = {
        **result,
        "wtp_matrix": wtp_matrix,
        "market_sizes": ms_array,
        "agents": agents,
        "tier_costs": tc.tolist(),
    }

    print(f"\n{struct_name}:")
    for t, label in enumerate(tier_labels):
        print(f"  {label}: ${result['best_prices'][t]:.0f}/mo")
    print(f"  Total market revenue: ${result['best_revenue']:,.0f}/mo")
```

### 6.5 Subscriber Analysis (Market-Weighted)

```python
def analyze_subscribers(result, agents, tier_labels, market_sizes, segment_lookup):
    """Analyze subscriber distribution weighted by market size."""
    choices = result["choices"]
    prices = result["best_prices"]

    summary = {}
    for t, label in enumerate(tier_labels):
        mask = choices == t
        count = mask.sum()
        market = market_sizes[mask].sum() if mask.any() else 0
        summary[label] = {
            "agent_count": int(count),
            "market_size": int(market),
            "revenue": market * prices[t],
        }

    opt_mask = choices == -1
    summary["opt_out"] = {
        "agent_count": int(opt_mask.sum()),
        "market_size": int(market_sizes[opt_mask].sum()) if opt_mask.any() else 0,
        "revenue": 0,
    }

    return summary
```

---

## Step 7: Report Template

```markdown
---
title: "Price Tiering Analysis: [Product Name]"
date: YYYY-MM-DD
---

## Background

[What product? Who are the customers? Why this pricing analysis?]

## Executive Summary

[Recommended structure, prices, and projected total monthly revenue.
Which segments subscribe to which tiers. Key trade-offs.]

## Methodology

### Features

[Table of all features.]

### Candidate Tier Structures

[Table comparing which features are in which tier for each structure.]

### Customer Panel

[Agent descriptions with market size weights. Explain the market sizing
rationale -- where did the segment sizes come from?]

### Survey Design

Bundle WTP via QuestionNumerical. Each agent evaluated each complete
plan (not individual features) to capture feature complementarities.
Total survey calls: [N].

### Optimization Method

Price grid search maximizing total market-weighted revenue. For each
candidate structure, searched over [N] price candidates per tier.

### Model

[Model(s) used, with reasoning.]

## Bundle WTP Results

### WTP by Tier and Segment

![WTP heatmap](plots/bundle_wtp_heatmap.png)

[Narrative: how WTP varies by segment and tier. Do higher tiers
command higher WTP? Which segments have the steepest WTP gradient?]

## Price Optimization Results

### Structure Comparison

| Structure | Basic | Pro | Enterprise | Total Monthly Revenue |
|-----------|-------|-----|------------|----------------------|
| A         | $X    | $Y  | $Z         | $NNN,NNN             |
| B         | $X    | $Y  | $Z         | $NNN,NNN             |

### Recommended Structure: [Name]

| Tier | Monthly Price | Features | Subscribers (market) |
|------|--------------|----------|---------------------|
| Basic | $X | [list] | N customers |
| Pro | $Y | Basic + [list] | N customers |
| Enterprise | $Z | Pro + [list] | N customers |

### Revenue Breakdown

![Revenue by tier and segment](plots/revenue_breakdown.png)

[Where does the revenue come from? Which tiers and segments contribute most?]

### Market Coverage

[What fraction of the total addressable market subscribes? How many
potential customers are lost? Is the trade-off between price and
adoption appropriate?]

## Sensitivity Analysis

[How does revenue change with +/- 10-20% price shifts?
Are there near-optimal prices with much higher market coverage?]

## Limitations

- Bundle WTP from AI agent personas, not real customers.
- Market size estimates are approximate -- sensitivity to these matters.
- Choice model assumes agents pick the surplus-maximizing tier; real
  customers may satisfice or be influenced by anchoring.
- The survey asks WTP without competitive alternatives visible.

## Recommendation

[Clear recommendation with price points and caveats.]
```
