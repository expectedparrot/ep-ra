---
name: research-matching
description: >
  Match participants and allocate teams, projects, or reviews with the installed
  Roth CLI. Use for two-sided one-to-one or capacity-constrained matching,
  joint team formation and project assignment, reviewer allocation with conflicts
  and workloads, preference collection, or organizer what-if comparisons.
  Collective voting and evaluating a manuscript's content use other skills.
tags: [study-type, quantitative, analysis, data-collection, external-tool]
---

# Matching and assignment with Roth

Roth owns rosters, organizer policies, preference history, fielding artifacts,
matching snapshots, optimization, verification, and native reports. Use its
installed CLI rather than rebuilding the mechanism or editing internal state.
Local matching and optimization need no model calls. Roth is a standalone
command, not an `ep` subcommand.

## Select the structure

Reuse the user's supplied rules and preferences. Establish only missing choices
that affect the mechanism; participant labels such as “students” or “mentors”
do not determine it.

| Structure | Scenario | Essential distinction |
|---|---|---|
| Two sides, at most one partner each | `one-to-one` | Deferred acceptance on strict, mutually acceptable rankings |
| One side accepts several partners | `many-to-one` | Fixed upper capacities and responsive individual rankings |
| Form teams and assign each a distinct project | `teams` | Minimize size deviation, then maximize weighted Borda scores |
| Several reviews per person and per submission | `reviews` | Coverage and workload constraints with hard conflicts |

Read [mechanisms.md](references/mechanisms.md) for the selected mode's inputs,
limits, and interpretation. Roommate matching within one pool, stable
many-to-many matching, teams without projects, and multiple teams per project
are unsupported. Explain the mismatch instead of inventing projects or copying
capacity slots to force another structure.

Route room/rent, goods, chores, credit, or fare division to
`skill:research-fair-division`; dividing rent is different from pairing roommates.
Route collective winners or rankings to `skill:research-voting`, criterion-based
option scoring to `skill:research-decision-support`, and manuscript critique to
`skill:research-referee-report`. Assigning reviewers does not review the paper.

## Follow the package control loop

Use the existing study layout and plan conventions from
`skill:workflow-file-layout` and `skill:workflow-plan-template` when creating a
study. Inspect current state before creating or rerunning anything:

```bash
roth version
roth agent next
roth --project <study> agent next --scenario <selected-scenario>
```

`agent next` works before initialization and is read-only. Read `data.instruction`,
`data.questions`, `data.actions`, top-level `next_steps`, and errors. Execute
applicable returned `argv` within the user's existing authorization; fill only
unresolved inputs. Then execute `data.rerun`, which preserves chosen paths and
collection mode. Use `roth guide`, `roth capabilities`, or command `--help` when
an interface remains unclear. Do not guess commands from another package.

Global `--project` precedes the command. Explicit artifact paths are relative
to the command's working directory, independently of `--project`; returned
argument arrays use absolute paths. Respect fresh output directories and retain
previous preferences, snapshots, and reports.

## Collect preferences and solve

Select `--collection rankings` for supplied completed rankings, `human` for
participant collection, or `delegated` for organizer-authorized model inference
in stable matching. Missing preferences are not permission to use canned data.
Examples and fixture sources must remain labeled synthetic.

For human surveys or delegated scoring, read
[collection.md](references/collection.md) before building artifacts. Generating
an artifact does not publish it, invite participants, or run models. Delegated
team and review scoring are not implemented.

For stable matching, follow import, required confirmation, freeze, match, and
report guidance. For teams/reviews, follow the file-based validation and solve
workflow. Read the resulting coverage, verification, and solver status. An
infeasible problem needs organizer rule changes; a time-limited feasible result
needs an explicit accept/retry decision, not an automatic retry loop.

## Explain and deliver

Present original inputs, assignments, preference sources, and compromises.
For stable matching, include unmatched participants, vacancies, realized ranks,
proposer sensitivity, and the frozen graph to which stability applies. For
teams/reviews, report workload/coverage, hard constraints, unranked assignments,
and solver limits; do not claim stability, strategy-proofness, or measured welfare.

When requested, use [comparisons.md](references/comparisons.md) for organizer
what-if analysis that preserves the baseline. Computation and reporting do not
adopt a scenario or deliver assignments to participants.

Keep Roth's native HTML report and evidence artifacts. For a broader research
writeup, load `skill:report-authoring` and explain the package's verified results
without recomputing them. Organizer reports contain private preferences; review
what will be shared before publication. When `data.complete` is true, the package
work is complete but the agent must still explain the outcome to the user.
