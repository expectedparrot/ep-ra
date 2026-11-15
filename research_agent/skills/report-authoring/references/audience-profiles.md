# Audience Profiles — Detailed Reference

Full per-audience writing guidance. Summarized in `SKILL.md`; read this
file when you need the detailed rules for a specific audience type.

---

## 1. Client / External Stakeholder

**Who:** Someone outside your organization, or a senior internal stakeholder
who commissioned the work. Typically not a researcher. Reading to make a
decision or share with their own audience.

**Tone:** Professional and direct. Confident without being casual.
No hedging unless the finding genuinely warrants it.

**Structure:** Findings first. Lead with the most important result and its
implication. Methods go in a brief section after findings, or in an appendix.
The "How this study works" explainer (from `skill:report-authoring`)
is required.

**Detail:** Key results only. One or two representative verbatim quotes per
major finding — enough to make findings concrete, not enough to overwhelm.
Appendices for the full survey instrument, agent table, EP links.

**Technicality:** Assume no familiarity with EDSL, AI simulation, or survey
methodology. Never say "agent" without explaining it. Never say "ScenarioList",
"EDSL", "Coop", or "homo silicus". Say "AI-simulated respondents" or "virtual
panelists". Avoid statistics jargon (don't say "Likert scale" — say "a
1-to-7 agreement scale").

**Length:** Shorter is almost always better. Aim for a report a busy person
can read in 10 minutes. Use charts aggressively — a well-labeled bar chart
conveys more than two paragraphs.

**Charts:** Titles and labels must be self-explanatory without reading the
surrounding prose. Add a takeaway line to each chart caption.

---

## 2. Internal Team / Management

**Who:** Colleagues on the same project or direct managers. They have context
on why the study was run. Reading to understand results, flag issues, or
decide next steps.

**Tone:** Professional but direct. Can be more candid about limitations and
tradeoffs than a client report. Uncertainty is OK to name.

**Structure:** Brief framing (why we ran this, what we asked), then findings,
then implications/next steps. Methodology can be a sidebar or appendix unless
it was the point of the work.

**Detail:** More detail than a client report — include caveats, note where
results were unexpected, flag decisions that need team input.

**Technicality:** Can assume familiarity with the project context. May be
able to assume familiarity with AI simulation if the team runs studies
regularly — read the session context for signals. Use plain terminology by default;
explain EDSL-specific concepts briefly on first use.

**Length:** Medium. Long enough to be useful for someone who missed the
planning discussions, short enough to read in a focused sitting.

---

## 3. Academic / Researcher

**Who:** A peer, a journal reviewer, a conference audience, or a policy
researcher. They will scrutinize methodology, statistics, and limitations.

**Tone:** Formal. Precise. Appropriately hedged — do not overstate findings.

**Structure:** Standard academic structure: Introduction, Methods, Results,
Discussion, Limitations, Appendices. Methods section must be complete and
replicable. Limitations section is prominent, not buried.

**Detail:** Full. Include complete survey instrument, full agent configuration
table, model rationale with version numbers, all statistical results
(means, SDs or SEMs, sample sizes). Appendices are expected.

**Technicality:** Readers are research-literate but may not be AI-native.
Explain what AI simulation is and cite the relevant literature (Horton 2023,
Argyle et al. 2023). Be precise about what "n=30 agents" means. Never elide
the distinction between simulated and real respondents.

**Length:** As long as it needs to be. No artificial compression. Use
appendices liberally.

---

## 4. General Public / External Publication

**Who:** Blog readers, newsletter subscribers, journalists, social media
audiences. No research background assumed.

**Tone:** Accessible, engaging. Conversational without being glib. Lead
with why this matters to a non-specialist.

**Structure:** Story-first. Open with a hook (an interesting finding or
a provocative question), then explain how you found it, then give implications.
No jargon gates — every technical term must be explained on first use.

**Detail:** Findings only. One standout chart or visual. One or two
memorable quotes. No appendices, no full methodology — link to the full
report if available on Expected Parrot.

**Technicality:** None assumed. The "How this study works" explainer from
`skill:report-authoring` is required and should appear early, before the
findings. Keep it to 3-4 sentences.

**Length:** Short. Aim for something that reads in 3-5 minutes. Use
subheadings to let scanners get the main points without reading everything.

---

## 5. Technical Colleague / EDSL-Familiar

**Who:** Someone who knows EDSL, runs their own studies, and is reading
primarily to understand your methodology or reuse your approach.

**Tone:** Collegial and precise. Can assume shared vocabulary.

**Structure:** Methods-forward is fine. Can include code snippets or
references to specific EDSL objects. EP links are especially useful here.

**Detail:** Full methodology. Agent configuration table with trait dict
snippets. Model rationale including pilot decisions. All EP links. Point
to anything reusable — the agent list, the survey object.

**Technicality:** High. No need to explain what EDSL is, what an agent is,
or how a job is run. Brief explanations for any novel technique or
non-standard configuration.

**Length:** As long as the methodology requires. A full methods section
is more valuable than a findings summary for this audience.
