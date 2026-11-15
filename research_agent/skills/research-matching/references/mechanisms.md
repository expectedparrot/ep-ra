# Roth mechanism contracts

Use only the section matching the selected scenario. The installed `roth agent
next` and command help provide current input schemas and executable actions.

## One-to-one and many-to-one stable matching

Obtain stable IDs for two distinct rosters, public profiles, eligibility,
strict rankings, unacceptable/unknown options, and the proposing side. For
many-to-one, also obtain capacities and confirm that preferences rank individuals
independently of who else is assigned. Capacity is an upper bound, not a required
fill level; zero closes a position. Only one side may have capacity above one.
Do not truncate an acceptable ranking to the participant's capacity.

Couples, minimum staffing, and preferences over combinations need a different
formulation. Unequal side sizes, vacancies, and empty acceptable lists are valid.
Unknown candidates, rejected candidates, and nonrespondents are different states.
Mutual acceptability is required for an edge in the matching graph.

For real data, `roth init` accepts a market JSON or side files; inspect its help.
Then follow the package's returned commands to import preferences, freeze a named
snapshot, match, and generate a report. Freeze requires every active participant's
preferences and any mandatory confirmation/benchmark. An explicit `--exclude ID`
removes a nonrespondent from that snapshot; explain the changed cohort rather
than treating silence as rejection. Preserve previous revisions.

Deferred acceptance is checked for feasibility and blocking pairs. Stability
concerns the frozen evaluated graph and its submitted or inferred preferences,
not unknown human preferences or unsampled candidates. Explain the proposing
side and the reverse-orientation comparison when available. Show every assigned
partner for capacity holders, plus vacancies and unmatched reasons.

## Teams and projects

Gather student and project rosters, target size, allowed smaller/larger sizes
and bounds, social weight, project and teammate rankings, and hard exclusions.
Every student needs a completed submission. Unlisted options have zero Borda
score but remain assignable; explicit exclusions are forbidden.

This mode forms teams and assigns at most one team to each project. It first
minimizes deviation from the target size, then maximizes normalized weighted
project/teammate preference scores. Allowing larger teams does not force them
when target-size teams remain feasible. State the organizer's objective before
solving and explain who bears the compromises.

Use the `teams validate` and `teams solve` actions returned by guidance. These
operate on explicit files and new output directories, separately from the
stable-matching store. Guidance verifies saved input hashes, assignments, and
scores. Report the solver's optimality claim or limit; a feasible incumbent is
not necessarily optimal. Borda indices are not measured cardinal utility, and
this mechanism has no stability or strategy-proofness guarantee.

## Review assignment

Gather reviewers, submissions and author IDs, team membership, explicit
conflicts, required coverage per submission, and min/max workloads per reviewer.
Authors use the roster ID namespace; a nonreviewing author can have zero workload
bounds. Self-review, team conflicts, and explicit unacceptable assignments are
hard exclusions.

Choose Borda rankings, explicit scores, or deliberate constraints-only allocation.
Unranked/unscored eligible submissions remain assignable with zero score; missing
submission records remain incomplete. Do not invent preferences for the
constraints-only case. Follow `reviews` validation/solve guidance and independent
checks of coverage, workloads, conflicts, assignments, and saved hashes.

The optimizer can assign multiple reviews in both directions. This does not
make it a stable many-to-many matching mechanism. Wider workload bounds permit
unequal loads; report them. Delegated reviewer scoring is outside the current
implementation, although Humanize collection is supported.

## Sources

- [Agent guidance](https://github.com/expectedparrot/roth/blob/30572f698eced5f0aee96ed862045f54ba79638b/docs/agent.md)
- [Capacity matching](https://github.com/expectedparrot/roth/blob/30572f698eced5f0aee96ed862045f54ba79638b/docs/many-to-one.md)
- [Teams](https://github.com/expectedparrot/roth/blob/30572f698eced5f0aee96ed862045f54ba79638b/docs/teams.md)
- [Review assignment](https://github.com/expectedparrot/roth/blob/30572f698eced5f0aee96ed862045f54ba79638b/docs/reviews.md)
