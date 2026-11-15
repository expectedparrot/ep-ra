# Pilot and Full-Run Review Gates

## After a pilot run — mandatory before anything else

When a pilot run completes and results are printed:

1. **Stop. Do not ask the user about next steps yet.**
2. **Use the Skill tool to load `skill:post-run-review` now** and apply it in pilot
   mode (see below).
3. Go back and re-read: the user's original request, the approved plan, and the
   pilot results together. Ask: does what ran actually serve what was asked?
4. Produce a written critique. For each gap or problem, provide all three:
   - **The specific observation** — a concrete finding from these results, not a
     general statement ("8 of 10 agents gave near-identical responses to Q4",
     not "free-text was thin")
   - **Why it matters** — what it affects: validity, segment coverage, usefulness
     for the user's stated goal
   - **The proposed fix written out in full** — the actual revised question text,
     rewritten agent trait, or new scenario wording. "Consider revising Q3" is
     not a fix. "Rewrite Q3 as: [verbatim text]" is.
5. Explicitly recommend the next step — one of:
   - **Run another pilot** with the revised design (if meaningful changes were made)
   - **Proceed to full run** (only if the design held up well)
   - **Stop and discuss** (if there are fundamental issues)
6. Present the critique and proposed changes to the user. Wait for approval.
7. Once the user approves: implement the changes, show a brief summary of every
   change made, then propose the next pilot.

Approval of the critique or proposed changes is not approval for another paid
run. A request to analyze, summarize, or report the pilot authorizes only work
on the saved pilot Results. Before a new pilot or full run, present the exact
cost for that run in a separate `AskUserQuestion`, identify the exact package,
and stop for fresh approval. Do not batch that question with execution.

Do not propose running another pilot on an unchanged design — it will produce
the same problems and tells you nothing new. Multiple iterations are normal and
expected; each one should be on a meaningfully revised design.

---

## After a full run — mandatory before analysis

When a full study run completes and results are saved:

1. **Stop. Do not proceed to analysis or report writing.**
2. **Use the Skill tool to load `skill:post-run-review` now** and apply the full
   review framework.
3. Work through all four layers: re-examine user inputs, review study design,
   review results, identify scope expansion opportunities.
4. Present findings to the user before beginning any analysis.
