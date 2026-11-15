---
name: research-interview-design
description: >
  Design interview guides for human moderators or AI interviewers, and deploy
  AI interviews via QuestionInterview. Covers construct elicitation, probe design,
  guide structure, and humanize deployment. Use when the user wants to create an
  interview guide, run an AI-led interview, or review an existing guide.
tags: [study-type, qualitative, data-collection]
---

# Interview Guide Skill

This skill tells you how to work with the user to produce a high-quality interview guide and deploy it as a humanize survey. The guide should be good enough that a real moderator — or an AI interviewer — could pick it up and conduct a rigorous, probing interview that genuinely advances the research goal.

The most important thing this skill conveys: **the dialogue with the user is where the quality is built.** A guide produced from a one-sentence prompt will always be worse than one that emerged from a real conversation about what the user is actually trying to measure. Don't rush to a draft.

---

## Orient before acting

Interview guide work comes up in many forms. Before doing anything, take stock of what already exists and what the user actually needs — then calibrate accordingly. You may be creating from scratch, proposing interviews as a next step, reviewing something that already exists, adapting a guide for a different interviewer type, helping the user decide whether interviews are even the right approach, or some combination. A few situations worth recognizing:

- **A study just completed and interviews are a natural next step.** The prior findings should directly ground the guide — don't start the construct dialogue from scratch when you already know what the data surfaced. See "Proposing interviews after a study" below.
- **The user has an existing guide and wants feedback or improvement.** The work is review and revision, not creation. See "Reviewing an existing guide" below. Phase 1 may not apply.
- **The user has a guide designed for human moderators and wants an AI interviewer version**, or vice versa. Phase 2 covers both guide types; the construct dialogue may be unnecessary.
- **The user is deciding between a survey and interviews.** Help them think through what each format can and can't produce for their specific goal before committing to either.
- **The user has transcripts from prior interviews** and wants to design a follow-up round — the prior transcripts are context that should inform the new guide's topics and probes.
- **The user mentions "talking to people" or "doing interviews" informally** — consider whether formalizing that into a structured guide would improve what they get from those conversations.
- **You're analyzing interview results** and need to understand what the guide was designed to surface in order to interpret the responses correctly.

In all cases: use whatever context you have before asking questions. If you're proposing this, frame the proposal — don't ask if they want it. If you already know the research objective from prior work, confirm rather than re-elicit. The goal is to arrive at a guide that's genuinely fit for purpose, through whatever path gets there most efficiently for this user.

For a new guide, establish two things before drafting: whether the researcher
already has a guide to adapt, and which high-level requirements or concerns
must shape the interview. Ask only what is still unknown; do not make them
repeat information already supplied. If they have a guide, review that artifact
instead of drafting a competing one from scratch.

---

## Proposing interviews after a study

When a simulation study or structured survey has just completed, interviews are often the right next step — but the case needs to be made, and the guide should be grounded in what the prior study actually found.

**When to propose interviews:**
- The results show a pattern that begs *why* — e.g., one segment scores much lower on trust, or variance within a segment is unexpectedly high
- The closed-ended questions captured the *what* but not the *how* or *why* — scales can show that Gen X employees distrust AI recommendations, but not what that distrust is actually based on
- The simulation surfaced a construct that scales couldn't adequately measure — "where do you draw the line?" is not a scale question
- You want to validate whether the AI simulation reflects real human experience

**How to frame the recommendation:**

Lead with the finding, then the gap it creates, then what interviews would add:

> "The simulation showed [X pattern]. That's interesting, but it raises a question the survey can't answer: [why / what that means in practice / whether real people experience it the same way]. A short set of interviews — [N] people, [X] minutes each — would let us go deeper on exactly that."

Propose the specific use case and ask for confirmation. Don't ask "do you want to do interviews?" as an open question.

**How prior findings shape the guide:**

Every topic section should have a "Prior study context" note explaining what the simulation or survey surfaced and what the interview needs to probe or verify. This is not background — it directly determines which probes matter. If the simulation showed that technical users drew a line at comprehension while non-technical users drew it at authorship, the interviewer needs to know that distinction and probe for which framing the real respondent uses.

The prior findings also anchor Phase 1. You likely already know what construct you're measuring — the question is which aspect of it the prior data left unresolved. Lead with that rather than reopening the construct dialogue from scratch.

---

## Reviewing an existing guide

When the user brings an existing guide and wants feedback, read it fully before responding. Then assess it against the quality criteria in Phase 2 and give concrete, specific feedback — not "the probes could be stronger" but "the probe in Topic 2 doesn't anticipate what to do if the respondent anchors on a single event — add a follow-up that brings them back to the full week."

**What to check:**

1. **Does the opening prime the construct?** If the opening uses the key construct word ("I'm here to understand your happiness"), the respondent is anchored on their global self-assessment before the questions start. Flag and suggest a rewrite that frames the purpose without naming the construct.

2. **Is there a concrete warm-up anchor?** If the guide jumps to attitude or experience questions without first grounding the respondent in a specific recent example, responses will be abstract and less reliable. Suggest one if missing.

3. **Do the probes branch for different response types?** A single generic follow-up ("tell me more") leaves the interviewer with nothing when the respondent is vague, unexpectedly rich, or off-topic. Each topic should anticipate at least two response types with distinct probes.

4. **Do the probes have stated purposes?** If the guide doesn't explain why a probe exists, neither the moderator nor an AI interviewer can adapt it intelligently. Add probe-purpose notes where missing.

5. **Is there a "watch for" section?** If not, add one specific to the construct and audience.

6. **Are the primary questions open, neutral, and single-purpose?** Flag and
   rewrite any question that implies an expected answer, presupposes harm or
   benefit, can be answered yes/no, or combines independent constructs. For
   example, "Did AI make schoolwork less fair, and did you feel pressure to use
   it because others did?" both leads and asks about fairness and peer pressure
   at once. Separate it into neutral turns grounded in the respondent's
   experience. Do not merely note the bias; provide the replacement wording.

7. **Is the sequence right?** Topics should move from concrete/recent/easy to abstract/evaluative/high-stakes. Flag a guide that opens with global self-assessments.

8. **For AI interviewer use:** Are probe purposes stated as behavioral instructions, not just moderator notes? Are the hard rules and follow-up instructions present (see **references/interviewer-conduct.md**)?

**How to give feedback:**

Structure your response as: (1) what works and why, (2) the two or three most important issues with specific fixes, (3) anything missing. Then offer to revise. The goal is a better guide, not a report card.

---

## Phase 1: Surface what the user is actually trying to measure

Before writing a single question, engage the user in a conversation about the construct. This is especially important when the research topic involves a psychological or behavioral construct — happiness, trust, fairness, anxiety, satisfaction, identity, AI literacy, etc. These terms almost always mean more than one thing, and which meaning the user actually wants shapes every probe in the guide.

**What to do:**

Present the key distinctions within the construct. Don't ask "what do you mean by happiness?" — the user probably can't answer that abstractly. Instead, lay out the landscape:

> "Happiness research distinguishes a few different things — frequent positive feelings in daily life, overall life satisfaction, and sense of meaning or purpose. These are related but they're not the same thing, and they require different probing strategies. Which of these is closest to what you're after?"

Then — before writing questions — raise the known measurement problems for the construct the user picks. For hedonic frequency: the peak-end rule (people anchor on memorable moments rather than average experience). For trust: the specificity problem (trust in what, under what conditions). For AI literacy: the confidence-accuracy gap (people think they understand AI better than they do). For identity: the gap between stated and enacted identity.

These aren't pedantic objections — they directly determine what the follow-up probes need to do. Tell the user: "If we don't address [X], the data will show [Y bias] rather than what you're actually trying to measure."

**The goal of this phase is not to gather requirements. It is to help the user understand what they're measuring and why the guide will be designed the way it is.** A user who understands the peak-end rule will understand why the warm-up comes before the frequency question. A user who understands that trust is domain-specific will understand why each probe names a domain.

If you're proposing this as a next step after a prior study, lead with what that study surfaced: "The simulation showed [X pattern] — the interviews are designed to understand *why* that pattern exists, which means we need probes that push below the surface-level response." The user confirms, not a blank questionnaire.

---

## Phase 2: Draft the guide(s)

A human moderator guide and an AI interviewer guide are different documents and should be written separately. A human reads and interprets — you can write diagnostically, with technique notes and "what to listen for" guidance that assumes professional judgment. An AI follows instructions — everything a skilled human would do implicitly must be encoded explicitly. One document trying to serve both ends up doing neither well.

Produce whichever the user needs. If both, write them as separate files.

---

## Interview guide artifacts

**Canonical AI guide:** `edsl_jobs/job_<letter>/interview_guide.md` — same directory as `deploy_interview.py` (e.g. `edsl_jobs/job_a/interview_guide.md`). Use the active job folder for this study (`job_a`, `job_b`, … per **skill:workflow-file-layout**).

- This is the **only** filename for the AI interviewer script used by `QuestionInterview`.
- Do **not** put the AI guide under `writeup/`.
- Do **not** use alternate names (`interview_guide_ai.md`, etc.).
- Edit the markdown file, then load it from `deploy_interview.py` (see Deploying below).

---

### Human moderator guide (`writeup/interview_guide_human.md`)

Written for a person who will use it in a live interview. They can read, adapt, and use judgment — the guide supports them rather than scripting them.

**Structure:**

```
# Interview Guide: [Topic]

**Research objective:** [Specific insight this interview will produce]
**Audience:** [Who is being interviewed]
**Format:** Semi-structured. Follow the structure; adapt based on what the respondent raises.
**Duration:** [X–Y minutes]
```

**Opening:** A framing statement the moderator reads or adapts. Do not use the key construct word — you want the respondent's unanchored response later. Include a warm-up question that anchors the respondent in a specific recent experience before the key questions. This is structural, not social: it gives the respondent a concrete anchor rather than inviting a global self-assessment, and counteracts peak-end bias for experiential measures.

**Topic sections (3–5):** For each topic:

```
## Topic [N]: [Name] ([N] min)

*[Why this topic is here and what it is designed to surface.]*

**Primary question:** "[Open, short, non-leading.]"

**If they [response type A]:**
- "[Probe]"

**If they [response type B — e.g., stay abstract]:**
- "Can you give me a specific example?"
- "When did that last happen?"

**If they [response type C]:**
- "[Probe]"

*Probe purpose: [What these probes are designed to do — which bias they
counteract, which information gap they close.]*

*What to listen for: [What different responses reveal about the respondent.
This is diagnostic guidance — it tells the moderator what they're actually
trying to understand from this topic, not just what to ask next.]*
```

**Closing:** Often the sharpest question in the interview. "What would you want [X] to understand that they clearly don't?" Leave time for it. Let it run.

**Moderator notes:** Technique reminders specific to this topic and audience — how to use silence, how to probe without leading, how to handle a respondent who stays abstract. Cross-topic probes that always work: "Say more about that." / "What did that feel like?" / "What did you do then?"

**"What to watch for" table:** The failure modes specific to this construct and audience — what they look like in practice and what to do about each.

---

### AI interviewer guide (`edsl_jobs/job_<letter>/interview_guide.md`)

**After writing `interview_guide.md`, present it directly with `ep present`.**

This guide serves two purposes, and the user needs to understand both.

First: it is a document the researcher reads and approves. Before anything goes live, show the user this guide and walk them through it — explain what the AI will actually say, what it's listening for, and how it will probe. This is what their respondents will experience. The researcher is not approving an abstract design; they are approving the specific instructions an AI will follow when talking to real people.

Second: its content maps directly into the `interview_guide` parameter of `QuestionInterview`. When the survey is deployed, a real person opens a link, and an AI conducts a live interview with them using these exact instructions — no modification, no interpretation. What the researcher reads in this document is what their respondents will encounter.

When presenting the AI guide for review, make this connection explicit: *"This is the guide the AI interviewer will follow. When your respondents open the survey link, this is what they'll experience — the AI will open with this framing, move through these topics in this order, and use these probes when someone stays vague or anchors on a single event. Does this match what you want them to walk away having been asked?"*

Written as behavioral instructions — the AI does not have implicit professional judgment, so everything must be stated explicitly. Probe purposes are not explanatory notes; they are decision rules. "What to listen for" becomes "if you observe X, do Y."

**Structure:** Same topic sequence as the human guide, but the language is entirely directive.

**Opening instruction:** State what the AI is measuring and what it is not. For example: "You are measuring how frequently the respondent experiences positive feelings — joy, pleasure, contentment. You are not measuring life satisfaction or sense of meaning. Stay focused on feeling states." This prevents construct drift that a human moderator would catch instinctively.

**Topic sections:** For each topic, state the purpose as an instruction, give the primary question, then encode the branching logic explicitly:

```
## [TOPIC NAME]

Purpose: [Why this topic exists and what a complete answer looks like.
The AI needs to know what it is trying to produce, not just what to ask.]

Ask: "[Primary question]"

If the respondent [response type A]: "[Specific probe]"
If the respondent [response type B — stays abstract or general]:
  Probe: "[Concreteness push]" Respect the probing limits below.
If the respondent [response type C]: "[Probe]"

Watch for:
- [Specific failure mode]: [What to do]
- [Specific failure mode]: [What to do]
```

**Probing preferences — resolve before drafting:**

Ask about unresolved preferences: which topics or answer types warrant deeper
probing, how much depth versus breadth the researcher wants, and when to move
on. Recommend a policy suited to their goal and time budget; preserve any
preferences already supplied. Encode the agreed triggers, depth, and stopping
conditions in the guide. The defaults below are adjustable, not fixed limits.

See also **references/interviewer-conduct.md** for hard rules, probing limits, readiness/opening, voice turn-taking, and default structure when the guide is thin.

**Hard rules (always include at the top of the guide):**

1. One question per turn — no "also" / "and finally" stacking.
2. Never repeat an answered question; use the agreed clarification policy for unclear answers (once by default).
3. Your next question must follow from what they just said.
4. When a topic is done, move on.
5. Know the completion flow. If participants are compensated, know the completion code and how to provide it. If you were not given one, say so honestly; never say "I can't provide that."
6. Be neutral; do not sell or lead.
7. Answer logistical questions (payment, completion code) directly if asked.
8. Never end a turn on meta/thinking alone ("I'm exploring what to ask next") — same turn must continue with a question or clear close (especially voice).

**Default follow-up guidance — adapt to the agreed probing policy:**

Participant requests to skip or move on always take precedence. Unless the
researcher specifies otherwise, clarify an unclear answer once and cap each
sub-topic at three back-and-forth exchanges.

1. **Simulate before asking.** Before choosing each follow-up question, generate 2-3 candidates and mentally simulate how this respondent would likely answer each one. Choose the question that would produce the most concrete and specific response, and that doesn't assume what they think or feel. Discard any candidate that could be answered yes/no, that lets the respondent stay at the same level of abstraction, or that puts words in their mouth. Do this silently before every follow-up — not just when the respondent is vague.

2. **Seek one concrete example.** If the answer is abstract and the participant is willing, ask: "Can you think of a specific [day / moment / time] when that was true? Walk me through it."

3. **Notice and name hedging language.** "Kind of," "I guess," "sort of," "it depends," "it's complicated" can warrant one clarification. Probe: "What does it depend on?" / "What makes it complicated?" Accept unresolved ambiguity rather than pressing.

4. **Follow a useful thread.** If time and probing limits permit, ask one follow-up about the most specific or surprising detail before transitioning.

5. **Never lead.** Briefly reflect only what the participant actually said; do not infer feelings or conclusions. Use: "Say more about that." / "What did that feel like?" / "What did you do then?"

**Voice interviews:** When `interview_mode` is `"voice"` or `"both"`, add the voice turn-taking rules from **references/interviewer-conduct.md** — generous pauses, no interrupting participant fillers ("um," "let me think"), brief check-ins at most once during long silence, and never leave a meta bridge ("I'm exploring what to ask next") as the only utterance before waiting.

**Time budget:** State approximate minutes per topic section in the guide. Apply the agreed probing limits and skip nice-to-have topics if running behind.

---

## Phase 3: Explain the logic, then iterate

When you present the draft(s), don't just show the questions. Walk the user through the structural choices and what each is designed to do:

- Why the opening doesn't use the key construct word
- Why the warm-up precedes the core question (and which bias it counteracts)
- Why the topics are in this sequence
- What each set of probes is designed to surface and which failure mode each "watch for" item addresses

This does two things: it builds the user's confidence in the guide, and it gives them the context to give useful feedback. A user who understands the peak-end bias reasoning can tell you "this audience won't have a consistent week — we need a different anchor." A user who just sees questions can't.

**Ask specifically:**
- Do the topics cover what you need, and are they weighted correctly?
- Are the "watch for" items right for this audience?
- Is there anything in the sequence that would prime the respondent in a way that biases what comes later?

Revise until the user is confident. The test: can they explain to a colleague *why* the guide is designed the way it is?

---

## Rendering guides to PDF

Both guides should be rendered to PDF — the human guide so moderators can use it in the field, and the AI guide so the researcher can read and approve it before deployment. The `.md` files are the source of truth and stay editable; the PDFs are the readable deliverables.

```bash
pandoc writeup/interview_guide_human.md -o writeup/interview_guide_human.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt

pandoc edsl_jobs/job_a/interview_guide.md -o edsl_jobs/job_a/interview_guide.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt
```

If pandoc or xelatex is not available, fall back to HTML — it opens in any browser and is easy to share:

```bash
pandoc writeup/interview_guide_human.md -o writeup/interview_guide_human.html \
  --standalone --metadata title="Interview Guide (Moderator)"

pandoc edsl_jobs/job_a/interview_guide.md -o edsl_jobs/job_a/interview_guide.html \
  --standalone --metadata title="Interview Guide (AI Interviewer)"
```

---

## Deploying as a humanize survey

Load `skill:edsl-human-survey` and follow its preview and approval process, then
execute deployment yourself and return the working survey link. Creating
`deploy_interview.py` alone does not complete a deployment request; do not ask
the user to run it. Stop at design only when that is the user's requested scope.

Before calling `.humanize()`, render the full survey with runway (**skill:edsl-human-survey-preview**) and wait for the researcher to confirm it. The interview page shows its framing text and its place in the flow; the guide is reviewed separately.

Once the AI guide and the preview are approved, deploy it as a `QuestionInterview`. Here is what actually happens: a real person receives a survey link, opens it in their browser, and an AI conducts a live interview with them. The AI uses the `interview_guide` as its exact instructions — the topics, probes, branching logic, and follow-up rules the researcher approved are what the respondent experiences.

The `question_text` is a short internal goal, not displayed to respondents. Put participant-facing framing in `intro_screen.instruction` (see **skill:edsl-human-survey**), not in `question_text`. Load `interview_guide.md` from the same directory as the deploy script.

**Showing images during the interview:** A text interviewer can display images inline — stimuli to react to, or a diagram to fall back on when a participant misunderstands something. Attach them as `FileStore` values on a scenario and name the keys in the guide at the point they should appear, including when *not* to show them. Voice interviews cannot display anything. See **skill:edsl-human-survey** — "Showing images mid-interview".

**Prior answers from screeners or demographics:** Survey memory APIs (`set_full_memory_mode()`, etc.) do not apply to humanize. If a later question or the `interview_guide` needs a prior answer, pipe it with `{{ question_name.answer }}` in `question_text` or `interview_guide`. See **skill:edsl-human-survey** — "Memory and piping".

Write `edsl_jobs/job_<letter>/deploy_interview.py`:

```python
from pathlib import Path

from edsl import QuestionInterview, Survey

interview_guide = Path(__file__).with_name("interview_guide.md").read_text(encoding="utf-8")

q = QuestionInterview(
    question_name="[topic_snake_case]",
    question_text="[Short internal interview goal]",
    interview_guide=interview_guide,
)

# Default is a text chat interface. Use humanize_schema to offer voice or let the respondent choose.
# For voice or both, voice_interview_config (spoken language + how the AI sounds) — see skill:edsl-human-survey.
schema = {
    "questions": {
        "[topic_snake_case]": {"interview_mode": "both"}  # "text", "voice", or "both"
    }
}

info = Survey([q]).humanize(human_survey_name="[Name]", humanize_schema=schema)
print(f"Respondent link: {info['respondent_url']}")
print(f"Preview link: {info['preview_url']}")
print(f"Survey dashboard: {info['admin_url']}")
print(f"UUID: {info['uuid']}")  # save this — needed to retrieve responses later
```

### Required deployment handoff

After every successful human interview deployment, give the researcher all
three links together in the chat, using clickable Markdown links:

- `[Preview interview](<preview_url>)` — try the live interview without adding a response to the results.
- `[Participant link](<respondent_url>)` — share with participants after checking the preview.
- `[Survey dashboard](<admin_url>)` — the researcher's management page; not for participants.

For external AI-agent participation, replace the participant link with
`[Agent participation link](<agent_link>)` using the documented derivation in
skill:edsl-human-survey-agent-access. Keep the browser preview and dashboard
links. If both routes are intended, provide both participation links with
distinct labels. The browser preview does not test the agent participation flow.

Replace the placeholders with actual deployment URLs or the documented
agent-link derivation.
Do not use bare URLs, backticks, or a code block for the links. An artifact card
or tool output does not replace this chat handoff. If a URL is missing, inspect
the saved deployment output or retrieve the existing survey's metadata; do not
guess a URL or redeploy to recover it. If recovery fails, report the missing
link and blocker rather than claiming the handoff is complete.

Response retrieval is the Research Agent's job. Tell the researcher they can
ask you to retrieve and analyze interviews when ready. The following code is
for your internal execution when responses are requested, not for the handoff:

```python
from edsl import Coop
results = Coop().get_human_survey_responses("[uuid]")
```

Tell the user what to expect in plain language: each completed interview produces a conversation transcript. Keep transcript field names and retrieval code internal unless requested.

For saved Results, use the native schema and named-agent exporter in
**skill:methods-ai-interview** → `references/transcript-inspection.md`. The object
attribute `result.agent.name` corresponds to flattened `agent.agent_name`;
interview text lives in ordered `content` blocks, not a top-level `text` field.

---

## Geiecke & Jaravel prompt template

For a structured 3-part prompt template based on Geiecke & Jaravel (2026) "Conversations at Scale: Robust AI-led Interviews", including baseline/enhanced/minimal instruction styles, screening question patterns, and a complete worked example, see `references/geiecke-jaravel-template.md`.

Save the assembled guide to `edsl_jobs/job_<letter>/interview_guide.md` before deployment — do not keep it only as an inline string in Python. After writing `interview_guide.md`, present it directly with `ep present`.

---

## Files produced

| File | Purpose |
|------|---------|
| `writeup/interview_guide_human.md` | Human moderator guide — diagnostic, technique-oriented |
| `writeup/interview_guide_human.pdf` | PDF render — printable, shareable with moderators |
| `edsl_jobs/job_<letter>/interview_guide.md` | AI interviewer guide — behavioral instructions passed to `QuestionInterview` |
| `edsl_jobs/job_<letter>/interview_guide.pdf` | PDF render — for researcher review and approval before deployment |
| `edsl_jobs/job_<letter>/deploy_interview.py` | Loads `interview_guide.md` and deploys via humanize |
