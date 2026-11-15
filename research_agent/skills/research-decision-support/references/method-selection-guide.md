# Analysis Method Selection Guide

## When to Use Each Method

### Weighted-Sum

Choose weighted-sum when:

- You need a **clear total ordering** with a single score per alternative
- Criteria are **compensatory** — strong performance on one criterion can offset weak performance on another
- Stakeholders expect a **simple, explainable** recommendation
- You do not have meaningful indifference/preference/veto thresholds
- The decision is relatively straightforward and a "best overall" answer is useful

Output: each alternative gets a normalized score (0 to 1). Higher is better. Always produces a complete ranking.

### ELECTRE III

Choose ELECTRE III when:

- Some criteria are **non-compensatory** — a sufficiently bad value should disqualify an alternative regardless of how well it performs elsewhere (veto dynamics)
- You want to distinguish between "A is clearly better than B" and "A and B involve genuine trade-offs" (**incomparability**)
- Stakeholders have natural **threshold intuitions** — "a cost difference under $25K doesn't matter" (indifference), "a cost difference over $75K is clearly meaningful" (preference), "a cost difference over $175K is a dealbreaker" (veto)
- Multi-stakeholder divergence is high and you want to surface where the group genuinely disagrees vs. where there is consensus
- You want a **robust** recommendation that acknowledges ambiguity rather than hiding it behind a fragile score difference

Output: pairwise outranking relations (outranks, outranked-by, indifferent, incomparable), credibility matrix, and a distillation-based ranking that may include ties.

### Recommendation: Run Both

In most cases, **run both methods and compare**:

```bash
mcda analyze run --method weighted-sum
mcda analyze run --method electre-iii
```

- If both methods agree on the top alternative, the recommendation is robust.
- If they disagree, the disagreement itself is informative — it usually means the top alternatives involve genuine trade-offs that a simple score obscures.
- Present both results to stakeholders and use the divergence to structure the final discussion.

## Lambda Selection for ELECTRE III

The lambda (concordance cut) parameter controls how demanding the outranking standard is:

| Lambda | Effect |
|---|---|
| 0.55 | Permissive — more outranking relations, fewer incomparabilities |
| 0.65 | Moderate |
| 0.75 | Default — balanced |
| 0.85 | Strict — fewer outranking relations, more incomparabilities |
| 0.90 | Very strict — only the strongest outranking relations survive |

**Sensitivity sweep**: test several lambda values to see which conclusions are robust:

```bash
for lambda in 0.55 0.65 0.75 0.85 0.90; do
  mcda analyze run --method electre-iii --lambda $lambda
done
```

If the top candidate changes across the sweep, the recommendation is sensitive to the threshold — flag this for the decision-maker.

## Interpreting Results

### Weighted-Sum Output

- `scores`: total weighted score per alternative
- `weighted_contributions`: per-criterion breakdown showing what drives each score
- `normalized_perf`: criterion values normalized to [0, 1] for comparison

Key question: *Are the score differences meaningful?* A gap of 0.01 between first and second place is not a confident recommendation.

### ELECTRE III Output

- `relations`: for each pair, one of: `outranks`, `outranked_by`, `indifferent`, `incomparable`
- `credibility`: how credible is it that A outranks B? (0 to 1)
- `candidate_ranking`: groups of alternatives at each rank (ties possible)

Key question: *What is incomparable and why?* Incomparability usually means the alternatives make different trade-offs across criteria. This is the most valuable insight from ELECTRE — it tells the decision-maker where judgment is still needed.
