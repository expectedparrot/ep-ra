---
name: research-survey
description: >
  Owns general survey and polling design: opinions, preferences, awareness,
  satisfaction, NPS, demographic profiling, and exploratory attitudes. Use
  when designing or running a survey that is not owned by a specialized study
  skill such as conjoint, concept testing, or message testing.
tags: [study-type, market-research, quantitative, opinion]
---

# General survey workflow

Design the smallest useful survey.

## Capability questions during design

For designs combining background AI steps, dynamic options, or adaptive
interviews, first read the short
[composition reference](../edsl-surveys/references/composition-contracts.md).
Consult the owner for design details:

| Design question | Guidance owner |
|---|---|
| Question types, typed answers, and dynamic options | `skill:edsl-surveys` |
| Human pages, informational steps, background inference, and answer piping | `skill:edsl-human-survey` |
| Adaptive interview behavior and participant experience | `skill:methods-ai-interview` |

Read this guidance during design as needed; construction and deployment require
approval. Fixed-question surveys need no additional capability reference.

## Modality decision surface

When AI respondents, humans, both, or external AI agents (an agent outside
Expected Parrot, such as the user's own assistant, answering the survey) are
under consideration or selected and material modality choices remain
unresolved, read [modality-review.md](references/modality-review.md). Use it for the bounded
review required by `skill:workflow-session-start`, including phase transitions.
Do not read it for a narrow edit or when the user has supplied a complete fast
path.

1. Identify the outcome, population or persona range, sample size, and whether
   subgroup comparison matters. Do not ask questions whose answers would not
   change the design.
2. Use one construct per question, balanced options, consistent scales, and
   free text only when reasoning is useful. When the primary outcome is a
   known category such as a favorite color, use multiple choice (including an
   `Other` option if needed) and reserve free text for the follow-up reason;
   do not recover categorical values later with regex.
3. Default to no memory. Pipe one prior answer with
   `{{ question_name.answer }}` only for a direct follow-up.
4. Use scenarios only when the same questions rotate across stimuli, topics,
   or vignettes. A single fixed topic needs no `ScenarioList`.
5. Vary agent traits that could plausibly change the response. Do not describe
   a convenience persona panel as population-representative.
6. Before naming a model in `plan.md`, load
   `skill:workflow-model-selection` and confirm the exact current identifier
   with `ep models` for hosted inference, or the local-endpoint reference for
   self-hosted models; never propose an unconfirmed family alias from memory.
7. Use the neutral scaffold from `skill:workflow-file-layout` first.
   Write and present `plan.md`; obtain approval before applying the survey
   template, and separate spend approval before inference.
8. At implementation, load `skill:edsl-surveys`. Load
   `skill:edsl-surveys-cost` only after `jobs.ep` exists.
9. Run the proportional review from `skill:post-run-review`. For a clean small
   study, consume the scaffold-owned exports and continue directly to its
   already-approved report; do not add a new decision gate.

When the user brings an existing survey for cognitive testing, burden review,
revision, or readiness assessment, load
`skill:research-instrument-pretesting`; Messick owns that workflow. Do not use
the legacy scaffold-owned cognitive-probe procedure.

Read [survey-patterns.md](references/survey-patterns.md) only for a specialized
archetype, panel example, image survey, NPS calculation, or advanced analysis
pattern. A short preference survey does not need that reference.
