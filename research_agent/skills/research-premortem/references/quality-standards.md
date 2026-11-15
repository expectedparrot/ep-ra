# Pre-mortem Quality Standards

Common pitfalls and quality benchmarks for each phase.

## Contents

1. Failure statement pitfalls
2. Persona quality
3. Failure narrative quality
4. Causal graph quality
5. Mitigation quality
6. Report quality

---

## 1. Failure Statement Pitfalls

| Pitfall | Example | Fix |
|---------|---------|-----|
| Hedging | "The project might not succeed" | "The project was shut down after 18 months" |
| Embedding causes | "Failed because of poor planning" | Describe consequences, not causes |
| Too vague | "It didn't work out" | Add vivid specifics: enrollment numbers, partner departures, reputational damage |
| Too narrow | "We missed the Q3 deadline" | Describe the full scope of failure: cascading consequences, stakeholder reactions |

**Test:** Can you read the failure statement and feel a genuine pang of "oh no"? If not, it's not vivid enough.

---

## 2. Persona Quality

**Good persona indicators:**
- Has a specific institutional position (not just "manager")
- Has named conflicting incentives (wants X but constrained by Y)
- You can imagine meeting this person at the organization
- Their perspective will produce failure narratives that differ from other personas

**Bad persona indicators:**
- Could be at any organization ("senior stakeholder")
- No conflicting incentives (purely one-dimensional)
- Interchangeable with another persona in the set
- Generic consulting-speak in their description

**Diversity checklist:**
- At least one internal champion of the initiative
- At least one skeptic or person with conflicting incentives
- At least one person affected by (not driving) the initiative
- At least one external perspective (partner, customer, regulator)
- Span hierarchical levels (frontline, middle management, leadership)

---

## 3. Failure Narrative Quality

**Good narrative indicators:**
- Names specific processes, systems, dates, or figures
- Tells a causal story: X happened, which caused Y, which led to Z
- Reflects the persona's specific position and concerns
- Episodic reasons describe event chains; structural reasons describe systemic dynamics
- 200+ words per narrative (rich, not bullet-point)

**Bad narrative indicators:**
- Could apply to any organization ("communication broke down")
- No causal chain — just a list of bad things
- Reads like a management textbook, not a war story
- All personas produce essentially the same narratives

**Specificity test:** Replace the organization name with a competitor's. If the narrative still reads the same, it's too generic.

---

## 4. Causal Graph Quality

**Target:** ~8 nodes, ~10 edges.

**Good graph indicators:**
- Readable at a glance (<30 seconds to trace all paths)
- Clear root causes (nodes with no incoming edges) that suggest intervention points
- Visible convergence (multiple paths leading to the same intermediate effects)
- Labels use domain-specific language, not generic terms
- Each node is traceable back to specific persona narratives

**Bad graph indicators:**
- 15+ nodes (too complex to be actionable)
- Long chains with no branching or convergence (just a linear sequence)
- Generic labels ("poor planning", "lack of resources", "communication issues")
- Orphan nodes with no connections
- No clear root causes vs. terminal outcomes

**Node type distribution:**
- 3-4 root causes (no incoming edges)
- 2-3 intermediate effects
- 1-2 terminal outcomes (the final failure states)

---

## 5. Mitigation Quality

**Good mitigation indicators:**
- References specific graph nodes it would break or weaken
- Specifies WHO would do WHAT by WHEN
- Is actionable before the initiative launches (not "monitor and respond")
- Addresses root causes, not just symptoms

**Bad mitigation indicators:**
- "Improve communication" (too vague)
- "Monitor risks closely" (not actionable)
- Doesn't map to any graph node
- Addresses a symptom rather than a root cause
- Requires resources or authority that don't exist

**Categorization:**
- **Quick wins:** Low cost, immediate, address single nodes
- **Structural changes:** Higher cost, longer timeline, address root causes
- **Research items:** Uncertainties that need empirical investigation before acting

---

## 6. Report Quality

The final report is a decision narrative, not a dump of CLI state. Use the
canonical report-context bundle as evidence, then follow `skill:report-authoring`
to write `writeup/report.md` and compile the branded deliverable. The package's
convenience HTML is useful for inspection only.

**Required narrative shape:**
- Open with the decision, the imagined failure, and the central structural trap.
- Identify the root causes and explain how they reinforce or converge rather
  than presenting an unconnected risk list.
- Describe the most consequential causal pathways in prose, grounded in the
  graph and persona narratives.
- Distinguish immediate safeguards from structural mitigations; name owners,
  timing, triggers, and the causal nodes each mitigation weakens.
- Close the decision analysis with unresolved empirical questions and what
  findings would change the recommendation.

**Useful report structure:**
1. Executive summary: core problem, root causes, convergence, and highest-leverage mitigations
2. Initiative and definitive failure statement
3. Method and synthetic stakeholder panel
4. Stakeholder perspectives and failure narratives
5. Causal graph and critical pathways
6. Ranked mitigations
7. Research agenda
8. Limitations
9. Appendices with fuller narratives or proposals when useful

Adapt headings and length to the audience rather than copying this outline
mechanically. Preserve the causal story and decision logic even in a concise
report.

**Transparency requirements (per `skill:report-authoring`):**
- Agent panel configuration table
- Model rationale
- 2-3 verbatim persona narrative excerpts as blockquotes
- Limitations section covering AI simulation caveats
- Clear statement that personas are synthetic perspectives, not real stakeholders

**Expected Parrot deliverable checks:**
- `writeup/report.md` is the canonical source.
- Compiled HTML embeds the scaffolded Expected Parrot CSS and its `--ep-green`
  brand variable.
- The final report is compiled, checked, and presented through the
  report-authoring workflow—not copied from `premortem report html`.
- Charts and causal diagrams are rendered artifacts rather than raw Mermaid or
  source code.

**The report should answer these questions:**
1. What is the initiative and what does definitive failure look like?
2. Who are the stakeholders and what are their concerns?
3. What are the most critical causal pathways to failure?
4. What can be done to prevent failure?
5. What do we not know that we should find out?

**Reject the report as incomplete when:**
- It is mostly bullets, tables, or schema fields with no causal narrative.
- It summarizes themes without showing how failure unfolds over time.
- Claims cannot be traced to the context bundle, graph, or quoted narratives.
- It lacks Expected Parrot branding or presents the convenience renderer as the
  final deliverable.
