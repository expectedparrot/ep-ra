# Report Style and Audience

## Contents

- Determine scope
- Infer style from context
- Send and record the pre-writing brief
- Audience profiles and default detail
- Supplementary formats
- Purpose, recommendations, and unexpected results
- Long reports, continuity, and standalone visuals

Do not write a single sentence of a report until you have confirmed eight things:

1. **Scope** — which work from this session is in the report
2. **Format** — written report, slide deck, email summary, standalone visuals, or memo
3. **Audience** — who is reading it
4. **Purpose** — what the reader should do or decide after reading
5. **Tone** — how formal, direct, or accessible
6. **Length** — approximate size of the deliverable
7. **Detail** — how much methodology, statistics, and caveats to include
8. **Technicality** — how familiar the reader is with AI simulation

Getting these wrong means the report needs to be rewritten. A brief
confirmation before writing is always cheaper than a revision after.

Throughout this process, make concrete recommendations with brief rationale
rather than presenting options. Say "I'd suggest X because Y." The pre-writing
brief should read like advice from a thoughtful colleague, not a form.

**Do not include API costs, credit usage, or dollar amounts in any
deliverable — report, slide deck, executive summary, or one-pager — unless
the task or context makes clear the user expects it.** Costs are tracked
internally in `chat_summary.md` and confirmed with the user before running.
They are internal bookkeeping, not findings. Users generally do not want
clients or stakeholders seeing what a study cost to run.

---

## Step 1: Determine scope

Before thinking about style, establish what goes in the report.

### Single-task sessions

If the session had one clear focus (one survey run, one analysis completed),
scope is usually obvious. State it in the pre-writing brief (Step 3) and
proceed unless the user corrects you.

### Multi-task sessions

If the session covered more than one distinct piece of work — multiple surveys,
a pilot followed by a full run, exploratory analysis alongside a main study,
or tasks that span different topics — do not assume everything belongs in the
report. Some of that work may have been exploratory, debug work, or a separate
deliverable entirely.

**Pilots are development work, not findings. Do not describe pilot iterations
in the report.** A reader does not need to know how many pilots were run, what
changed between them, or that a pilot happened at all. Report only the final
study and its results. Discuss pilot iterations with the user in chat.

Exception: if a design decision made during piloting is directly relevant to
interpreting the final results (e.g., a question was substantially reworded
after a ceiling effect was found, and the reader needs that context to
understand the findings), a single sentence is appropriate. Otherwise, omit.

**When scope is ambiguous, ask before inferring.** This is the one case where
a direct question is always warranted, because writing a report that covers
the wrong scope wastes more time than asking.

Frame it concretely:

> "This session covered [A], [B], and [C]. Should the report cover all three,
> or just [the main finding / a specific part]? I want to make sure I'm not
> including work that was exploratory or that you're covering elsewhere."

If the answer is "just part of it", note explicitly what is being excluded
and why, so the omission is intentional rather than accidental.

### Topic shifts within a continuous session

Users do not always start a new session to signal a new workflow. A user may
finish one task and pivot to something different in the same conversation
without explicitly flagging the change. Watch for these signals:

- The subject or domain shifts noticeably mid-session (different product,
  different research question, different client)
- The user asks you to run something that seems unrelated to what came before
- The user says "now I want to..." or "separately, can you..." or "one more thing"
- A task was clearly exploratory, a one-off test, or a debug run — not
  intended as a deliverable

When a topic shift is apparent, confirm it with the user before proceeding.
This keeps work organized and prevents report scope from drifting:

> "It looks like we're moving to a new topic. Should I treat this as a
> separate workflow from what we were working on before?"

A yes/no answer is all you need. If yes: start fresh — new study directory,
new context for the report. If no: the prior work is still in scope and
the session is continuous.

Do not silently include or exclude work that you are uncertain about.
Surface the ambiguity before writing, either in this confirmation or in
the pre-writing brief.

---

## Step 2: Infer style from context

Work through these signals in priority order. Stop as soon as you have a
confident inference — do not keep searching for alternatives.

### 1. Prior history (strongest signal — check this first)

Scan completed reports under `sessions/` before doing anything else.

If this user has a consistent pattern — always writing for clients, always
producing internal memos, always targeting a research audience — that pattern
is your default. Anchor to it. Do not present other audiences as alternatives
simply because they are theoretically possible. A user who has written ten
client reports is almost certainly writing an eleventh, not suddenly pivoting
to an academic paper.

In the pre-writing brief, name the pattern explicitly rather than asking:

> "I'll write this the same way as your previous reports — professional tone,
> client-facing, findings first, 4-5 pages. Let me know if this one is
> different."

Only deviate from the established pattern when there is a clear, explicit
signal: the user names a different audience, describes a different purpose,
or the current study type is genuinely unlike anything they have done before.

### 2. What the user said in this session

If no history exists, look at how the user described the deliverable and
what they said about the intended reader.

| Phrase | What it signals |
|---|---|
| "report for my client", "client deliverable" | External audience, findings-first |
| "deck", "slides", "present this" | Slide format; produce charts + outline, not prose |
| "share with my team", "internal memo" | Internal audience, candid, medium length |
| "paper", "write-up", "journal submission" | Academic; full methods, long |
| "quick summary", "just the highlights", "email" | Short prose or email format |
| "blog post", "newsletter", "public-facing" | General public; accessible, very short |

When the user's words point clearly to one audience, use that — do not
offer alternatives. Only flag uncertainty if the phrasing is genuinely
ambiguous.

### 3. Study type (weakest signal — use only when nothing else is available)

If there is no history and the user gave no framing, study type provides
a weak prior. Use it to make an initial guess, but treat it as a starting
point for the brief, not a confident inference.

| Study type | Weak prior |
|---|---|
| Message testing, ad copy, brand research | Client likely |
| Concept testing, pricing, conjoint | Client likely |
| Academic survey, policy research | Researcher likely |
| Internal pilot, methodology exploration | Internal team likely |
| Social simulation, agent behavior | Researcher or technical colleague likely |

### Format signals

| Signal | Suggested format |
|---|---|
| "deck", "slides", "present this" | Slide deck — read `skill:report-slides` |
| "send to my client", "share externally" | Written report (PDF) |
| "quick update", "just let me know", "email" | Short prose summary, 3-5 bullets |
| "write it up", "full report", "document this" | Written report (PDF) |
| No signal; prior reports exist | Match prior format |
| No signal; no history | Default to written report; state assumption in brief |

When format resolves to slides, stop here and read `skill:report-slides`
before proceeding. That skill handles template lookup, learning, generation,
verification, and persistence.

### Length and detail signals

| Signal | Likely length/detail |
|---|---|
| "quick", "brief", "summary", "highlights" | 1-2 pages; findings only |
| "full report", "complete write-up" | Full length; complete methodology |
| No signal | Use audience profile default (see table below) |

### Reference materials and style examples

Prior reports in `sessions/` are the best available style reference — check
for them before asking the user anything. If found, note specifically what
you are matching in the pre-writing brief.

If no prior reports exist, ask in the brief:

> "Do you have any existing reports or examples you'd like me to match for
> style and formatting?"

If the user provides materials, read them before writing and note the
patterns that matter: vocabulary register, sentence length, heading style,
how statistics are presented, how charts are captioned, and whether
conclusions are stated directly or hedged. Record these in
`writeup/report_style.md`. The user's house style takes precedence over
the generic defaults in this skill.

---

## Step 3: Send a pre-writing brief and wait for confirmation

Do not start writing after inference. Send a short brief that states all
six dimensions, then wait for explicit or implicit confirmation before
writing anything.

The brief should read like advice from a thoughtful colleague, not a checklist.
State what you plan to do and why, so the user understands the reasoning and
can easily redirect if it is wrong. Include any offer of supplementary formats
(executive summary, one-pager) here — not as a separate later question. Example:

> "Before I start: I'll cover the main survey results and the segment
> analysis — I'll leave out the pilot run since that was just a test.
>
> I'd suggest a written report rather than a slide deck here, since the
> findings have enough nuance that prose will serve the client better than
> bullets. I'm thinking 4-5 pages: key findings first, one chart per major
> result, a short methods section, and methodology details in an appendix.
> I'll aim for a clear recommendation at the end — given the results, there's
> a strong case to make. Plain language throughout, no AI jargon.
>
> I'll also produce a one-page summary your client can share with their
> leadership without the full report — let me know if you'd rather skip that.
>
> Does that match what you need? Happy to adjust format, length, or emphasis."

When there is genuine uncertainty about a single dimension, name it and suggest
the most likely answer rather than asking open-endedly:

> "I'm assuming this is going to an external client — if it's internal, I'd
> write it more candidly and skip the executive summary. Which is it?"

Do not ask more than one open question. State a recommendation for everything
else, and ask only about the one dimension where you cannot infer.

**Do not start writing until the user confirms or explicitly says to proceed.**
A one-word reply of "yes" or "looks good" is sufficient. If the user immediately
asks for the report with no brief in context, send the brief first.

---

## Step 4: Record the confirmed decisions

After confirmation, write the agreed parameters to `writeup/report_style.md`.

`writeup/report_style.md` (one-liner is fine):

```
Format: written report | Audience: client_external | Purpose: support go/no-go decision |
Tone: professional | Length: 4-5 pages | Detail: findings + brief methods |
Technicality: low | Scope: main survey + segment analysis | Recommendations: yes
```

---

## Audience profiles

Five profiles with detailed per-audience writing guidance are in
`references/audience-profiles.md`. Read that file when you need specifics
for a given audience type. The summary tables below cover the common case.

---

## Default length and detail by audience

Use these as starting points in the pre-writing brief. Override if the user
has given an explicit signal (e.g. "quick summary" overrides the academic default).

| Audience | Default length | Reading time | Detail included |
|---|---|---|---|
| Client / External | 3-5 pages | ~10 min | Key findings, one chart per finding, brief methods, appendix for full methodology |
| Internal Team | 5-8 pages | ~15 min | Findings + caveats + next steps, moderate methods, no appendix required |
| Academic / Researcher | 10-20 pages | 30+ min | Full IMRaD structure, complete methodology, all stats, appendices expected |
| General Public | 1-2 pages | 3-5 min | 1-2 headline findings, one visual, no methodology |
| Technical Colleague | 5-10 pages | ~20 min | Full methodology, code references or EP links, findings summarized |

These are defaults, not rules. A client may want a full technical report;
a colleague may want a one-pager. The pre-writing brief is where you state
the default and give the user a chance to override it.

---

## Supplementary formats: executive summary and one-pager

When the primary deliverable is a longer report, proactively offer to produce
an executive summary, a one-pager, or both — without waiting to be asked.
Include the offer in the pre-writing brief, not as a separate question
after the report is written.

### When to offer

**Offer an executive summary when:**
- The main report is 6 or more pages (academic, full internal, or technical)
- The user mentions stakeholders who will not read the full document
- The report is going to a client but was written at technical depth

**Offer a one-pager when:**
- The findings need to travel beyond the immediate audience (a client
  wants to share results with their leadership, board, or another team)
- A slide deck is being produced and a printed leave-behind would be useful
- The user's prior pattern shows they regularly share findings externally

**Do not offer when:**
- The primary deliverable is already short (1-3 pages, email summary,
  general public piece) — a summary of a summary adds no value
- The user has explicitly said they only need one thing
- The audience is general public — the main report already serves this role

### What each is

**Executive summary (1-2 pages):** Sits at the front of or alongside the
full report. Structured: key findings, their implications, and a clear
recommendation if one is warranted. Assumes the reader may then go to the
full report for detail. Written in the same tone as the main report.

**One-pager:** Standalone document designed to be shared without the full
report. 3-4 headline findings, one strong visual, a clear takeaway line.
Can have a lighter visual treatment than the full report. Assumes the
reader will not see the full document.

### How to offer

Name the specific use case so the offer feels considered, not generic:

> "Since this is a full 12-page report, I'd suggest also producing a
> one-page summary your client can share with their leadership — something
> that stands alone without the full document. I can do that alongside the
> main report. Want me to include it?"

> "I'll add a two-page executive summary at the front — useful if not
> everyone on the team will read the full methodology. Let me know if
> you'd rather skip it."

---

## Style dimensions at a glance

| Dimension | Client/External | Internal | Academic | Public | Technical |
|---|---|---|---|---|---|
| Findings-first | YES | YES | NO | YES | NO |
| Methods depth | Light | Medium | Full | None | Full |
| Statistics shown | Sparingly | Yes | All | No | Yes |
| Jargon | None | Minimal | Standard | None | Full OK |
| Verbatim quotes | 1-2 highlights | 2-3 | All relevant | 1 highlight | Optional |
| EP links | Appendix | Methods | Methods | Link out | Prominent |
| AI explainer | Required | Optional | Required (cite) | Required | Omit |
| Limitations | Brief | Candid | Prominent | Brief | Candid |
| Appendices | Methodology | Optional | Expected | None | Methods detail |
| Length | Short | Medium | Long | Very short | Medium-long |

---

## Purpose and recommendations

Before writing conclusions, know what the report is meant to enable:

| Purpose | How it shapes the report |
|---|---|
| Support a decision (go/no-go, choose between options) | Lead with the finding most relevant to the decision; end with a clear recommendation |
| Persuade stakeholders | Frame findings around the case being made; anticipate objections |
| Archive and document | Neutral, exhaustive; methodology as prominent as findings |
| Brief someone not in the room | Context-heavy intro; assume no prior knowledge of the project |
| Share externally / publish | Audience-facing framing; omit internal caveats and process details |

**On recommendations:** Always ask or infer whether the report should end with
actionable recommendations or just findings. When the purpose is a decision
or persuasion, a recommendation is almost always appropriate — suggest including
one rather than waiting to be asked. When the purpose is documentation or
archival, neutral findings are correct.

> "Given the results, I'd suggest ending with a concrete recommendation on
> next steps — want me to include that, or keep it to findings only?"

---

## Handling unexpected or negative results

If the study produced results that are disappointing, surprising, or contrary
to the hypothesis, the framing depends on audience and purpose:

**Client / external:** Do not bury or soften findings, but frame them
constructively. Lead with what was learned rather than what failed. A finding
that "the concept did not test well" is more useful when paired with *why* and
*what would need to change*. Suggest this framing proactively:

> "The concept scored below expectations — I'd suggest framing the findings
> around the specific barriers respondents cited, which gives the client
> something actionable rather than just a negative verdict. Want me to structure
> it that way?"

**Internal / team:** Be candid. Name what did not work and why. A too-optimistic
internal report causes more downstream damage than an honest one.

**Academic:** Report results as found. Do not reframe around a positive
interpretation. Unexpected results are often the most interesting — the
Discussion section is where you explore why.

When results are mixed or ambiguous, say so explicitly. Do not paper over
ambiguity with confident-sounding prose.

---

## Draft-first for long or high-stakes reports

For reports above roughly 6 pages, or any report going to an external client
for the first time, suggest a draft-first approach rather than writing the
whole thing and presenting it:

> "Given the length and the external audience, I'd suggest drafting the
> key findings section first so you can confirm the framing before I write
> the full report. Want to do it that way?"

Draft-first is almost always the right call when:
- The audience is external and tone/framing is important
- The findings are unexpected or sensitive
- The report is long enough that a full rewrite would be costly
- This is the first report you have written for this user or client

---

## Continuity with prior work in the same topic

Before writing, check whether earlier studies exist under the same topic
directory. If they do, ask whether this report should reference them:

> "I see you ran a pilot study on this topic in March. Should this report
> reference those earlier results, or stand entirely on its own?"

If the user wants continuity, carry forward the same section headings,
terminology, and chart style from the prior report so the two documents
read as a series. Note any changes in methodology or scope explicitly so
the reader understands what is and is not comparable.

If the user wants a standalone report, note this decision in `report_style.md`
so future sessions do not re-raise it.

---

## Standalone visuals

The same audience logic applies when producing a chart, table, or visual
without a full report.

Ask: will this visual stand alone (no surrounding prose), or will it be
embedded in a document the reader has context for?

**Standalone:** The title, axis labels, and caption must fully explain the
finding without any surrounding text. Add a one-line takeaway to the caption.
Example: *"Figure 1: Gen Z respondents were 2x more price-sensitive than
Boomers. High price-sensitivity was most common among 18-26 year-olds
(62%) and least common among 59-77 year-olds (31%)."*

**Embedded:** A shorter caption is acceptable, but it must still accurately
describe what is shown.

For client audiences, never deliver a chart with a generic title like
"Satisfaction by Segment." Use a finding-as-title: "Younger subscribers
are far more likely to switch to ad-supported plans."

**After writing `report.md`, present it directly with `ep present` (or the scaffold's `make present` target).**
