---
name: research-price-tiering
description: >
  Design profit-maximizing tiered pricing by eliciting bundle WTP from
  market-weighted customer personas, then optimizing prices to maximize
  total market revenue. Use when the user wants to design tiered pricing
  or find optimal price points for product plans.
tags: [study-type, market-research, quantitative]
---

# Price Tiering with EDSL

Use this workflow when a user has a product with discrete features and wants to design **tiered pricing** (e.g., Basic / Pro / Enterprise). The system surveys AI agent personas for willingness-to-pay for complete feature bundles (not individual features), then optimizes price points to maximize total market revenue weighted by segment size.

> **Detailed code examples, optimization functions, and the report template are in `references/implementation-details.md`.** This file covers the design principles, workflow steps, and key decisions at a summary level.

---

## Key Design Principles

### 1. Bundle WTP, not per-feature WTP

Do not ask "what would you pay for Feature X alone?" and sum values. Features have complementarities and substitution effects. Instead, ask agents to value **complete plans** -- "what would you pay for a plan that includes these features together?"

### 2. Market-weighted total revenue

Each agent persona has an estimated **market size** (number of potential customers in that segment). The optimizer maximizes:

```
Total Revenue = sum over segments of:
  market_size[segment] x adoption_rate(price) x price
```

This prevents setting high prices that extract surplus from a few enterprise buyers while losing the entire small-business market.

### 3. Candidate tier structures, not brute-force search

Define 2-4 plausible tier structures based on domain knowledge. Survey bundle WTP for each, optimize prices, and compare. Real product teams don't algorithmically search all possible feature arrangements.

---

## Workflow Overview

The price-tiering workflow has seven steps:

1. **Define** the product features and candidate tier structures
2. **Build** the customer persona panel with market size weights
3. **Design** the bundle WTP survey
4. **Sample** a small subset and preview results
5. **Run** the full WTP survey
6. **Optimize** prices for each tier structure
7. **Report** findings with a recommended structure and price points

This follows the standard EDSL study structure.

---

## Step 1: Define Features and Candidate Tier Structures

Define the product features as a dict of `{key: description}`. Then define 2-4 candidate tier structures, each mapping tier names to lists of feature keys. Tiers must be nested: Basic <= Pro <= Enterprise.

Build a `ScenarioList` where each scenario is one (structure, tier) combination. The scenario includes `structure_name`, `tier_name`, and `plan_description` (a formatted feature list). All scenario fields must appear in `question_text`.

Store marginal costs per tier in a separate JSON file (`data/raw/tier_costs.json`). Default to $0 if unknown.

---

## Step 2: Build Customer Personas with Market Size

Each `Agent` has a `market_size` trait representing the number of potential customers in that segment. This is how the optimizer weights revenue.

**Sizing the panel:** Price optimization requires within-segment WTP variation (not all enterprise buyers have identical budgets). Use 3-5 agents per segment — enough to capture WTP spread without over-sampling. If you have 3 segments (solo, team, enterprise), that's 9-15 agents total. Pilot with 1 per segment to verify WTP questions work, then scale to 3-5 per segment. All agents in a segment share the same `market_size`.

**Market size defaults** (if user cannot provide estimates):

| Segment | Typical share of TAM |
|---------|---------------------|
| Solo / freelancer | 50-60% |
| Small team (5-50) | 25-30% |
| Mid-market (50-500) | 10-15% |
| Enterprise (500+) | 2-5% |

Only the ratios between segments matter, not absolute numbers.

---

## Step 3: Design the Bundle WTP Survey

Use `QuestionNumerical` for bundle WTP (name: `bundle_wtp`) and `QuestionFreeText` for reasoning. The WTP question should:

- Present the full plan description via `{{ scenario.plan_description }}`
- Reference `{{ scenario.tier_name }}` and `{{ scenario.structure_name }}`
- Ask for maximum monthly WTP in US dollars
- Instruct the agent to evaluate features as a bundle

**Calibrating max_value**: Consumer app ~$50, SMB SaaS ~$200-300, Enterprise platform ~$500-1,000.

---

## Step 4: Sample and Preview

Run a small subset (3 scenarios, 3 agents) to verify:

- Higher tiers get higher WTP
- Enterprise agents bid higher than freelancers
- Values are not at ceiling (`max_value`)
- Magnitudes are plausible for the product category

Present results to the user before running the full survey.

---

## Step 5: Run the Full WTP Survey

Total API calls = (scenarios per structure x structures) x agents x models x questions. For 2 structures x 3 tiers x 12 agents x 1 model x 2 questions = 144 calls.

Use `ep jobs cost edsl_jobs/job_a/jobs.ep` before running. **Always pass both `remote_inference_description` and `results_description` to `ep run`, set to the same string; don't omit them** — see `skill:edsl-surveys` ("Running a survey — labeling the job").

```bash
ep run edsl_jobs/job_a/jobs.ep \
  --remote_inference_description "Survey tool subscription tiers - freelancer startup enterprise" \
  --results_description "Survey tool subscription tiers - freelancer startup enterprise" \
  --output data/results.ep
```

---

## Step 6: Optimize Prices (Market-Weighted)

The optimization has these components:

1. **Load and pivot data**: Build a WTP matrix of shape `(n_agents, n_tiers)` from the results DataFrame. Extract market sizes per agent.

2. **Choice model**: For a given price vector, each agent picks the tier maximizing surplus (WTP - price), or opts out if all surplus is negative. Revenue = sum of `market_size[i] x (price[t] - cost[t])` for each agent's chosen tier.

3. **Price grid search**: Generate candidate prices from WTP quantiles per tier. Search all combinations, enforcing strictly increasing prices (Basic < Pro < Enterprise). Pick the combination maximizing total market revenue.

4. **Run for each structure**: Loop the optimizer over each candidate structure's WTP data and compare total revenue.

5. **Subscriber analysis**: For each structure, report how many market-weighted customers land in each tier and how revenue breaks down.

See `references/implementation-details.md` for the full `compute_market_revenue()`, `optimize_prices()`, and `analyze_subscribers()` functions.

---

## Step 7: Report

The report should compare tier structures and present market-weighted results. Key sections:

- **Executive Summary**: Recommended structure, prices, projected monthly revenue
- **Methodology**: Features, tier structures, customer panel with market sizes, survey design, optimization method
- **Bundle WTP Results**: Heatmap of WTP by segment and tier
- **Price Optimization Results**: Structure comparison table, recommended structure with prices, revenue breakdown, market coverage
- **Sensitivity Analysis**: Revenue impact of +/- 10-20% price shifts
- **Limitations**: AI personas (not real customers), approximate market sizes, surplus-maximizing choice model, no competitive alternatives

See `references/implementation-details.md` for the full report template.

---

## Study Structure

```
study_x/
  data/
    raw/
      tier_costs.json                <- marginal cost per tier per structure
      market_sizes.json              <- segment market sizes (if separate file)
    results.ep                       <- EDSL bundle WTP results
  computed_objects/
    optimization_result.json         <- prices, revenue, choices per structure
  edsl_jobs/
    job_a/
      study_scenario_list.py         <- plan/bundle scenarios
      study_agent_list.py            <- agents with market_size
      study_survey.py                <- bundle WTP survey
      study_model_list.py
      run_job.py
  analysis/
    optimize_prices.py               <- market-weighted price optimization
    plot_bundle_wtp_heatmap.py       <- WTP by segment x tier
    plot_revenue_breakdown.py        <- revenue by tier and segment
    plot_demand_curves.py            <- adoption vs. price curves
  writeup/
    report.md
    plots/
```

---

## Gotchas

1. **Bundle WTP should increase with tier level.** If Pro < Basic for an agent, the plan description may be confusing. Check in the preview step.

2. **Market size dominates.** With 50K freelancers and 2K enterprise buyers, losing freelancers to a small price increase costs far more revenue than gaining per-enterprise. Calibrate market sizes carefully.

3. **The choice model matters.** Agents pick the tier with highest surplus. An agent valuing Basic at $50 and Pro at $55 picks Basic at $30/$40 (surplus $20 vs $15). They won't upgrade for a small WTP increase unless the price gap is even smaller.

4. **Feature costs not in scenarios.** EDSL requires all scenario fields in question text. Tier costs go in a separate JSON file.

5. **max_value calibration.** Set based on the highest-tier bundle for the product category, not individual features.

6. **Don't over-optimize on small panels.** Use results directionally ("Basic should be $X-Y range"), not as exact price points.

7. **Comparing structures is the main value.** "Structure A generates 30% more revenue than B" is often more actionable than exact prices.

8. **Multiple agents per segment.** Use 3+ agents per segment. Average WTP within a segment before optimizing, or weight each agent by `market_size / n_agents_in_segment`.

9. **Scenario field gotcha.** All scenario fields (`structure_name`, `tier_name`, `plan_description`, `n_features`) must appear in a question via `{{ scenario.field }}` or EDSL raises `JobsCompatibilityError`.

---

## Quick Reference

| Task | Code |
|------|------|
| Build plan scenarios | `build_plan_scenarios(structures, features)` |
| Bundle WTP question | `QuestionNumerical(question_name="bundle_wtp", question_text="...{{ scenario.plan_description }}...", min_value=0, max_value=500)` |
| Agent with market size | `Agent(traits={"persona": "...", "segment": "...", "market_size": "50000"})` |
| Market-weighted revenue | `compute_market_revenue(wtp_matrix, prices, market_sizes_arr)` |
| Optimize prices | `optimize_prices(wtp_matrix, market_sizes_arr, tier_costs)` |
| Compare structures | Loop `optimize_prices()` over each structure's WTP data |
| Save results | `ep run edsl_jobs/job_a/jobs.ep --output data/results.ep` |
| Load results | `Results.git.load("data/results.ep")` |
