# Organizer what-if comparisons

Use the completed Roth report as a fixed baseline. Agree on named changes and
write the scenario JSON using the supported schema from `roth compare --help`
and the package's returned what-if guidance:

```bash
roth compare <baseline-report-directory> --scenarios <scenarios.json> \
  --output <new-comparison-directory>
```

Every scenario starts from the same baseline. Retain the baseline cohort,
preferences, input hashes, and reports. The command does not adopt a scenario,
re-elicit preferences, deliver assignments, or run models.

- Stable matching supports absolute capacities (zero closes a position) and
  proposing-side changes. It does not create preferences to fill new slots.
  Compare original partner ranks; mixed changes in a capacity holder's rank
  vector do not establish a welfare gain or loss.
- Teams support size rules, project closures, and social weight. Supply explicit
  bounds as well as permissions. Allowing teams of four differs from targeting
  four. Closed projects retain their original place in the rank/Borda universe.
- Reviews support coverage counts and reviewer workload bounds. Conflicts and
  eligibility remain fixed. A larger total score with more reviews is additional
  work, not necessarily improved assignments. Constraints-only results are unscored.

Use baseline ranks and score scales for individual comparisons. Objective totals
under different team policies are not directly comparable. Show assignment churn,
workload changes, infeasible scenarios, and solver limits. Different equal-score
optima can cause churn; it is not necessarily unavoidable.

Each optimization scenario has its own time limit. A limit without an incumbent
is distinct from proven infeasibility; a feasible incumbent need not be optimal.
Do not automatically rerun limited scenarios. The evidence is conditional on
preferences held fixed; a new elicitation would be a different study.

[Comparison contract and examples](https://github.com/expectedparrot/roth/blob/30572f698eced5f0aee96ed862045f54ba79638b/docs/comparisons.md)
