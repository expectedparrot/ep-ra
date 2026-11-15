---
name: edsl-surveys
description: >
  Explains EDSL question types, informational steps, answer piping, and survey composition, and
  implements approved designs as saved EDSL objects and jobs. Use for EDSL
  capability questions during design, or for writing questions, agents,
  scenarios, models, memory rules, and jobs after design approval.
tags: [edsl, reference]
---

# Implement an EDSL survey

During design, read [composition contracts](references/composition-contracts.md)
for mixed survey/interview flows, messages, and groups. Construction starts
after approval.

## When the researcher wants to edit the survey themselves

Treat "let me edit it" and similar requests as a visual Builder handoff, not a
request for EDSL constructors, Python snippets, or source-editing instructions.
Load `skill:edsl-object-publishing` and follow its **Hand off a survey for
editing in the Builder** section through push, wait, pull, inspection, and jobs
rebuild. A request to self-edit is not permission to upload local content: the
publishing owner must explain the remote handoff and receive explicit consent
before `ep push`.

Use saved source files and the stable CLI boundary:

1. Use the survey scaffold from `skill:workflow-file-layout`. Its manifest
   names this skill as required and lists every `next_edits` source. Read them
   once and replace only their marked study-data sections; keep their working
   construction and save architecture. Never improvise an inline Python job.
2. Each script exports its object and, under `if __name__ == "__main__"`, uses
   `survey.git.save("survey.ep")` or
   `agent_list.git.save("agent_list.ep")`. Never use `.save(...)`; it produces
   a serialized filename such as `.ep.json.gz`, not the package expected by
   the scaffold. Construct named personas as
   `Agent(name="Priya", traits={"age": 34, "occupation": "marine biologist"})`;
   `name` is reserved and must never appear inside `traits`.
3. After all `next_edits` sources are complete, execute
   `phase_commands.after_source_edits` exactly once. It initializes and attests
   gates with approval evidence, builds all EDSL objects and `jobs.ep`, and
   estimates cost. Never run `workflow-setup`, `edsl-objects`, or `estimate`
   separately, and never reconstruct `ep jobs build`.
4. Obtain spend approval, then execute `phase_commands.after_spend_approval`
   exactly once. The
   scaffold supplies descriptions and preserves existing non-empty results.
   For failed or partial inference, follow
   [recovery](references/execution-and-recovery.md) before a retry. The approved
   `make -C <root> retry-data RETRY_REASON="..."` archives prior Results and costs.
5. After inference, execute the scaffold manifest's `after_inference` command,
   normally `make -C <absolute-study-root> post-run`, exactly once. It owns the
   bounded review, complete exports, costs, QA, and plots. For an additional
   structured column, use `ep results export ... --column ... --output <path>`;
   do not rerun overlapping inspection targets or parse review prose.
6. Immediately before writing the report, load `skill:report-authoring`. At
   completion execute `phase_commands.after_report`. Do not
   attest or verify objective gates individually; the target checks the report
   and verifies every remaining command gate in order.

For advanced behavior, read the relevant reference:

- `skill:edsl-human-survey`: [Grouped pages and messages](../edsl-human-survey/references/grouped-pages-and-messages.md): multi-question pages and routable informational steps.
- [probabilistic-responses.md](references/probabilistic-responses.md): elicited distributions and host-side resolution for AI respondents.
- [survey-reference.md](references/survey-reference.md): pinned options, loops, advanced
  memory, flow rules, and complex question behavior.
- [full-reference.md](references/full-reference.md): generated images,
  instructions, unusual question types, or an API detail not covered above.
- [survey-lifecycle.md](references/survey-lifecycle.md): preview, iteration,
  publication timing, and human-versus-AI execution decisions.

Load `skill:edsl-quirks` only after a concrete compatibility problem.
