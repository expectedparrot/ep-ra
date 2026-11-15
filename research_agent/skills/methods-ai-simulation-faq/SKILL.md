---
name: methods-ai-simulation-faq
description: >
  Answers common questions about homo silicus, social simulation with LLMs, methodology, literature, strengths, limitations, and best practices.
  Use when the user asks why LLM-based simulation works, what kinds of studies are possible, or needs methodological grounding for a report.
tags: [edsl, reference]
---

# FAQ: Homo Silicus & Social Simulation with LLMs

Reference for answering questions about using LLMs as simulated survey respondents and experimental subjects — the approach sometimes called "homo silicus," "silicon subjects," or "synthetic respondents."

## When to use this skill

- When a user asks "why does this work?" or "how can LLMs answer survey questions?"
- When a user asks "what can you help me with?" or "what kinds of studies can you run?" → use the **Capabilities** section below
- When writing a study report that needs to explain the methodology to readers
- When the user wants to understand caveats and limitations
- When grounding a study in the relevant academic literature

---

## Capabilities: what kinds of studies can you run?

Use this section when a user is exploring what's possible — especially first-time users who arrive with a vague goal. Describe each study type in one concrete sentence, grounded in what the output actually is.

| Study type | What it produces | Example prompt |
|---|---|---|
| **Survey study** | A PDF/HTML report with charts and tables showing how AI personas with different traits (age, job, politics, etc.) answer your questions — useful for concept testing, opinion polling, message testing | "I want to know how different kinds of voters would respond to three different immigration policy framings" |
| **Agent list** | A reusable panel of AI personas you can run through many surveys — like recruiting a standing research panel you can reuse across studies | "Build me a set of 20 realistic Gen Z consumer personas I can use for product research" |
| **Data labeling** | A CSV of your rows with a new AI-generated label column — useful for classifying open-ended text, customer feedback, or any structured data at scale | "I have 500 customer support tickets — label each one as a billing issue, technical issue, or other" |
| **Simulation** | A narrative log of AI agents interacting in a scenario you define — useful for exploring negotiation dynamics, team decision-making, or social behavior | "Simulate a hiring committee evaluating three candidates with different backgrounds" |
| **Website feedback** | A grid of screenshot-based AI feedback on your site's pages — useful for UX research and design iteration before user testing | "Get feedback on my landing page from 10 different user personas" |
| **Eye-tracking heatmap** | A density heatmap showing where AI agent attention concentrates on an image or page — useful for visual design and layout decisions | "Show me where users are likely to look first on this product page" |
| **Transcript-to-personas** | An AgentList built from your interview transcripts — turns qualitative research into reusable AI personas that reflect real interviewee voices | "I have 12 customer interview transcripts — turn them into agent personas" |
| **Referee report** | Simulated academic peer review of a paper PDF, covering methodology, contribution, and weaknesses | "Simulate peer review of this draft paper" |
| **Message testing** | Side-by-side comparison of how different personas respond to different message framings or versions of your content | "Test three subject line variants on our email campaign with different customer segments" |
| **Literature review** | A structured summary of what the academic literature says on a topic, with citations | "What does the research say about AI in hiring decisions?" |

When a user expresses an open-ended goal ("I want to understand my customers better", "I'm trying to test a new product concept"), use this table to propose the most relevant study type with a one-sentence rationale. Do not list all options — pick the best fit and mention one alternative if it's a genuine close call.

---

---

## What is homo silicus?

"Homo silicus" is a term coined by Horton (2023) for LLM agents used as stand-ins for human survey respondents or experimental subjects. The core idea: large language models trained on vast corpora of human text have absorbed enough about human attitudes, behaviors, and social patterns that they can produce survey responses that are plausible — and in many documented cases, statistically close to what real humans produce.

This is **not** a claim that LLMs "think" like humans or "are" human. It is a pragmatic observation: for many survey and experimental tasks, LLM-generated responses exhibit distributions, correlations, and treatment effects that approximate human data well enough to be useful for research design, piloting, and — with appropriate validation — substantive analysis.

---

## Why does this work?

### The training data argument

LLMs are trained on billions of tokens of human-authored text: news articles, forum discussions, social media posts, books, academic papers, product reviews, and more. This text implicitly encodes:

- **Demographic correlations** — how people of different ages, genders, occupations, and political leanings tend to express opinions
- **Attitudinal structures** — which beliefs tend to cluster together (e.g., political ideology and policy preferences)
- **Behavioral regularities** — how people describe their purchasing decisions, moral reasoning, risk preferences, etc.
- **Social norms and conventions** — what kinds of responses are typical in different survey contexts

When you give an LLM a persona ("You are a 35-year-old teacher in Ohio who votes Republican") and ask it a survey question, it draws on these absorbed patterns to generate a response consistent with that persona. It is doing sophisticated pattern completion, conditioned on the persona description.

### The persona conditioning mechanism

EDSL "agents" work by prepending a persona description to the LLM's context. This is effective because:

1. **LLMs are excellent at role-playing** — they can maintain consistent personas across many questions
2. **Trait descriptions activate relevant knowledge** — specifying demographic or attitudinal traits shifts the response distribution in predictable, directionally correct ways
3. **The effect is compositional** — combining traits (e.g., "young + liberal + urban") produces responses that reflect the intersection, not just an average

### Empirical evidence

Multiple studies have shown that LLM-generated responses can closely match human data:

- **Horton (2023)** — "Large Language Models as Simulated Economic Agents: What Can We Learn from Homo Economicus?" Demonstrated that GPT-3/4 reproduce classic economic experimental results (ultimatum games, dictator games, public goods games, etc.)
- **Argyle et al. (2023)** — "Out of One, Many: Using Language Models to Simulate Human Samples." Showed that GPT-3, conditioned on demographic backstories from the ANES, produces attitude distributions that closely match real ANES respondents (the "silicon sampling" paper).
- **Brand et al. (2023)** — "Using GPT for Market Research." Found that GPT-generated conjoint analysis results were directionally consistent with human conjoint data.
- **Horton & Gillis (2024)** — Showed LLM-based pilot experiments can predict the sign and relative magnitude of treatment effects that are later confirmed with human subjects.

---

## Key literature

### Foundational papers

| Paper | Key contribution |
|-------|-----------------|
| Horton (2023), "Large Language Models as Simulated Economic Agents" | Introduced "homo economicus" framing for LLMs; showed GPT reproduces classic experimental economics results |
| Argyle et al. (2023), "Out of One, Many" | Demonstrated "silicon sampling" — conditioning GPT on ANES demographics produces attitude distributions matching real Americans |
| Park et al. (2023), "Generative Agents" | Showed LLM agents can simulate believable human behavior in interactive environments |
| Aher, Arriaga & Kalai (2023), "Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies" | Replicated several classic social science experiments using LLMs |

### Methodology and validation

| Paper | Key contribution |
|-------|-----------------|
| Brand et al. (2023), "Using GPT for Market Research" | Validated LLM conjoint analysis against human conjoint data |
| Horton & Gillis (2024) | LLM pilots predict direction and relative magnitude of human treatment effects |
| Dillion et al. (2023) | Tested LLM moral judgments against human moral psychology data |
| Binz & Schulz (2023), "Using Cognitive Psychology to Understand GPT-3" | Systematic comparison of GPT-3 against cognitive psychology benchmarks |

### Critical perspectives and limitations

| Paper | Key contribution |
|-------|-----------------|
| Santurkar et al. (2023), "Whose Opinions Do Language Models Reflect?" | LLMs' default opinions skew toward certain demographics (younger, liberal, educated) |
| Bisbee et al. (2024) | Highlighted that LLM responses can be sensitive to prompt wording in ways that differ from human sensitivity |
| Agnew et al. (2024) | Catalogued failure modes and biases in LLM-as-subject research |

---

## When homo silicus works well

The approach tends to perform best when:

1. **Attitudes are well-represented in training data** — Topics that are widely discussed publicly (politics, consumer preferences, common moral dilemmas) work better than niche or private topics
2. **The population of interest is well-represented** — LLMs reflect the demographics and viewpoints present in their training data, which skews toward English-speaking, internet-using, relatively educated populations
3. **You're measuring relative effects, not absolute levels** — Treatment effects (A vs. B) are often more reliable than point estimates of absolute attitudes
4. **The task has clear social/cultural conventions** — Survey questions with well-understood norms produce more realistic responses
5. **You use diverse agent personas** — A single LLM with no persona gives one "average" viewpoint; conditioning on many diverse personas better captures population heterogeneity

---

## Known limitations and caveats

### Distributional biases

- **Default skew**: Without persona conditioning, LLMs tend to produce responses characteristic of younger, liberal, educated, English-speaking individuals (Santurkar et al., 2023)
- **Underrepresented groups**: Populations poorly represented in training data (elderly, non-English-speaking, very low-income, specific cultural minorities) may be simulated less accurately
- **Extreme tails**: LLMs may underrepresent extreme or unusual viewpoints, producing distributions that are too "centrist" or "moderate"

### Methodological concerns

- **No ground truth for novel questions**: When a question hasn't been asked of real humans, there's no way to validate the LLM responses
- **Prompt sensitivity**: Small changes in question wording, persona description, or context can shift responses in ways that may not mirror human sensitivity patterns
- **Sycophancy**: LLMs may produce responses they "think" the researcher wants, especially if the question framing implies a preferred answer
- **Lack of genuine experience**: LLMs don't have bodies, emotions, or lived experience — questions about physical sensations, personal trauma, or deeply experiential topics are poorly suited
- **Temporal anchoring**: Training data has a cutoff; attitudes about recent events may not reflect actual current public opinion

### What NOT to claim

- Do NOT claim LLM responses "are" human responses
- Do NOT claim results are representative of any specific human population without validation
- Do NOT use LLM-only data for policy recommendations without human validation
- Do NOT assume treatment effects found with LLMs will have the same magnitude in human populations (direction is more reliable than magnitude)

---

## Best practices

### Study design

1. **Always specify agent personas** — Don't rely on the LLM's default viewpoint. Create diverse agents with demographic and attitudinal traits relevant to your research question.
2. **Use scenarios for treatments** — Vary experimental conditions through EDSL scenarios, not through changes to agent traits.
3. **Pilot with LLMs, validate with humans** — The strongest use case is: run an LLM study first to refine instruments and generate hypotheses, then confirm with a human sample using `humanize`.
4. **Include attention checks** — Even for LLMs, attention-check questions help verify the agent is "reading" the prompt correctly.
<!-- lint-allow-model: illustrative example, not a model recommendation -->
5. **Run multiple models** — If results hold across different LLMs (e.g., Claude, GPT-4, Gemini), they are more likely to reflect genuine patterns rather than model-specific artifacts.

### Reporting

When writing up results from LLM-based studies, always:

1. **State clearly that respondents are LLM agents**, not humans
2. **Describe the agent construction** — what traits were specified, how many agents, what model(s)
3. **Acknowledge limitations** — particularly around representativeness and the lack of ground truth
4. **Frame appropriately** — "suggestive evidence," "pilot findings," "exploratory analysis" rather than definitive claims about human behavior
5. **Cite the methodological literature** — reference the papers that establish this approach

### Common framing for reports

> This study uses LLM-based simulated respondents ("homo silicus") to explore [research question]. Following the methodology established by Horton (2023) and Argyle et al. (2023), we construct AI agents with diverse demographic profiles and administer surveys using the EDSL framework. While these simulated responses should not be interpreted as direct evidence of human attitudes, prior work has shown that LLM agents conditioned on demographic backstories produce response distributions that often approximate those of real human populations. We treat these results as exploratory/suggestive evidence that can inform future research with human subjects.

---

## Frequently asked questions

### "Isn't this just making up data?"

No. The key distinction is that LLMs are not generating random responses — they are drawing on patterns learned from billions of tokens of real human text. The responses are synthetic, but they are *informed* by real human behavior at massive scale. Think of it as a sophisticated form of interpolation across the training corpus, conditioned on the persona and question.

### "Why not just survey real humans?"

You should, when it matters. LLM simulation is best used as a complement to, not a replacement for, human research. Its advantages are speed (minutes vs. weeks), cost (pennies vs. dollars per response), and flexibility (easy to iterate on instruments). Use LLMs for rapid prototyping and piloting, then validate with humans via `humanize` + Prolific.

### "Which LLM should I use?"

Model selection is a research design decision. The short answer: match the model tier to the task's reasoning demands, use WebSearch to identify the current frontier model, confirm the exact name with `ep models`, run a small spot-check pilot before the full job, and document the choice in the Methods section.

For the full decision guide — including task-fit criteria, quality vs. cost framing, cross-model comparison strategy, and Methods documentation templates — read `research_agent/skills/workflow-model-selection/SKILL.md`.

Key principles:
- Larger, more capable models produce more nuanced persona simulation and richer open-ended reasoning
<!-- lint-allow-model: illustrative example, not a model recommendation -->
- Cross-model agreement (e.g. Claude + GPT-4o both converging) substantially strengthens confidence in findings
- Cost should be managed by reducing agent or question count, not by reflexively downgrading to a weaker model
- Always confirm current model names with WebSearch + `ep models` — hardcoded names go stale

### "How many agents do I need?"

**The key is diversity of agent traits, not raw count.** Once you've covered the range of relevant personas, adding more agents produces diminishing returns.

**Reasoning by study type:**

- **Simple survey (no segments):** How many distinct persona types matter for this topic? Count the dimensions that matter (age, political lean, income...) and design agents that cover the meaningful combinations in that space.

- **Segmented study:** How many segments do you need to compare, and do you need within-segment variation? If you need to verify that segment patterns are robust (not just one agent's quirk), use multiple agents per segment. If you just need coverage, one per segment may suffice.

- **Multi-condition experiment:** How many experimental cells do you have? You need enough agents per cell to see if effects replicate across different personas within that condition. The multiplier depends on whether you're checking for effect existence or estimating effect magnitude.

- **Social simulation:** Depends entirely on scenario design (how many roles, how many experimental conditions you're testing). Read `skill:research-social-simulation` for the reasoning framework.

The right answer comes from working through this logic for your specific study, then applying the study-specific guidance in the relevant `research-*` skill.

**Why AI needs fewer respondents than human surveys:** Human surveys fight *sampling error* (your 500 respondents might not represent the population) and *response noise* (mood, attention, interpretation). AI agents have much lower response variance — rerun the same persona and you'll see similar (not identical) answers, with variation coming from model temperature not from the human factors that dominate survey noise. You need enough distinct persona *types* to capture perspective range, not statistical power to overcome sampling error.

**Red flags you're over-sampling:** Applying human survey power calculations ("need 400 for significance"), using 100+ agents for a single-condition survey, requesting "as many as possible" without a coverage rationale.

### "What does over-sampling cost?"

**Over-sampling scales cost linearly with no new insights.** If you determine (using the reasoning above) that you need N agents, running 5N agents costs ~5× more and reveals nothing new. Running 25N costs ~25× more. This is opposite to human surveys, where larger N often does reveal new patterns by reducing sampling error.

**To estimate actual cost for your study:** Use `job.estimate_remote_job_cost()` before running (see `skill:edsl-surveys-cost`). Cost varies by model, question types, and whether questions include memory/images/files.

### "How do I make results match the target population?"

First, clarify what "match" means:

1. **Coverage** — agent panel includes the right *types* of people (young/old, urban/rural, etc.)
2. **Proportions** — agent panel has the right *mix* (51% female, 12% aged 18-24, etc.)

Coverage comes from thoughtful persona design. Proportions come from weighting.

**Three approaches:**

| Approach | When to use | How it works |
|---|---|---|
| Design-time proportions | Simple demographics, known population parameters | Build panel with census-matched proportions from the start (e.g., if population is 50/50 male/female, make half your agents male and half female) |
| Post-hoc weighting | Need marginal proportions, computing simple aggregates | Run unweighted diverse panel, apply census weights when computing means: `(answer × weight).sum() / weight.sum()` |
| Mixture calibration | Need joint distribution match, have target data to calibrate against | `skill:methods-calibrating-agents` — optimize mixture weights to minimize distance to target distribution |

**When proportions don't matter:** Treatment effect studies (does A differ from B?), exploratory research (what's the range of views?), instrument pilots (testing question wording). Coverage matters; proportions don't.

**When proportions do matter:** Reporting point estimates ("X% of Americans support..."), comparing to prior human survey with known demographics, stakeholder expectations for representativeness, vote/market share simulation.

### "How many agents for a pilot?"

**The pilot's job** is to catch design errors before the full run — question wording issues, agents not differentiating, technical problems. Size it to accomplish that, not to produce generalizable findings.

**Ask: What could go wrong that the pilot needs to catch?**

- **Just checking technical setup?** (questions render, scenarios work, no errors) → Minimum possible: one agent tests the machinery
- **Checking within-segment consistency?** (do agents with similar traits respond similarly?) → Need at least two agents per segment to compare
- **Checking between-segment differentiation?** (do different segments respond differently?) → Need enough agents per segment that you can see whether the pattern holds across multiple agents in that segment vs. whether it's just one agent's quirk

The pilot size follows from what you need to validate. If you just need to verify the survey runs without errors, run the absolute minimum. If you need to verify your segmentation logic works, you need enough agents to test that hypothesis.

**Pilots are cheap relative to full runs.** Don't under-size out of cost concerns; under-size only if the full run is itself tiny (then just run it once). Use `job.estimate_remote_job_cost()` to see actual pilot cost for your specific design.

### "Can LLMs do experiments, not just surveys?"

Yes. LLMs can participate in behavioral experiments: ultimatum games, prisoner's dilemmas, trolley problems, framing experiments, anchoring studies, and more. Horton (2023) and Aher et al. (2023) demonstrated this extensively. EDSL scenarios make it straightforward to implement between-subjects experimental designs.

### "What about within-subject designs?"

EDSL's survey memory system allows agents to "remember" their earlier answers, enabling within-subject designs where later questions depend on earlier responses. This works well for measuring consistency, preference reversals, and order effects.

### "How do I handle topics the LLM refuses to answer?"

Some topics (violence, illegal activity, explicit content) may trigger LLM safety filters. This is a genuine limitation. You may need to frame questions carefully, use models with more permissive policies for research, or acknowledge that certain topics are not amenable to this methodology.
