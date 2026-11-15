# Ariel's method contracts

Use `ariel guide --type TYPE` for the actual specification and input format.
These limits describe the pinned package, not all fair-division methods.

## Rent

A study has 2–50 participants and exactly one room each. Every participant's
nonnegative valuations must sum to total rent. Utility is room value minus rent
paid. Missing valuations are not zero. Establish `price_policy`: `nonnegative`
disallows subsidies and can be infeasible; `unrestricted` permits negative rents.
Hard affordability budgets, room exclusions, couples, and shared rooms are not
implemented. Do not turn these constraints into small numerical preferences.

Ariel finds an assignment maximizing total assigned room value, then maximizes
the minimum participant utility subject to envy-freeness and rent balance. Its
independent verifier checks the assignment, payment policy, balance, and pairwise
envy conditions; maximin optimality remains solver-reported. Under the stated
model, envy-freeness implies Pareto efficiency, not strategy-proofness or acceptance.

Cent rounding preserves total rent and receives its own envy check. Report any
rounding-induced envy and retain unrounded prices; do not describe rounded
payments as exactly envy-free merely because the original solution was.

## Goods

Values are additive, nonnegative integers. Ariel computes exact maximum Nash
welfare and checks envy-freeness up to one item (EF1) and Pareto efficiency by
enumeration. At most 100,000 assignments are supported. Respect rejection of
larger or unsupported problems rather than representing an approximation as
this exact method.

For goods, EF1 means envy disappears after removing at most one item from the
envied bundle. It does not mean every participant receives their favorite item
or is satisfied. Native elicitation uses a 1,000-point value budget, not prices.

## Bivalued chores

Costs add across chores and must be either 1 or a common integer
`difficult_cost`. The package uses small-instance exact search for an EF1,
Pareto-efficient allocation, limited to 10,000 assignments. It does not implement
a general continuous-cost or scalable chore-allocation method.

For chores, EF1 removes at most one item from the envious participant's own
bundle. No monetary compensation is modeled. Keep cost assessments distinct
from a participant's later fairness rating.

## Project credit

Use 3–12 contributors and positive relative assessments of other contributors.
There are no self-assessments. The current elicitation uses independent integer
peer weights on a common scale, not a fixed-sum budget; preserve the recorded
instrument version when reopening older rounds.

The impartial-division calculation uses other people's assessments and exact
rational accounting. In a three-person case, disagreement can leave some credit
unassigned. Show that residual; do not renormalize it away or claim that a
mechanical property verifies the truth of contribution assessments.

## Shared fares

Use 2–7 passengers and a complete supplied monotone coalition-cost table. Ariel
calculates exact Shapley shares and independently verifies them by permutations,
with budget, solo-fare, coalition, and rounding checks. It does not look up maps,
route distances, or fares.

Shapley shares need not pass solo-fare bounds or coalition stability for every
admissible table. Present those check outcomes individually rather than treating
successful computation as a universal fairness certificate. A participant's
confirmation of a table does not independently establish its factual accuracy.
A requested table correction requires a corrected specification before allocation.

[Published method documentation](https://github.com/expectedparrot/ariel/blob/449dcaf9c7fff888f1dcb27e10b61551ec01dcf3/README.md#mathematical-contract)
[Design and primary references](https://github.com/expectedparrot/ariel/blob/449dcaf9c7fff888f1dcb27e10b61551ec01dcf3/DESIGN.md)
