# EP Platform Education Principles

These principles define how to introduce Expected Parrot to a new user during a
tutorial session. They are not a script — they are guidelines for when and how to
raise each concept naturally, as it becomes visible in the workflow.

The goal: by the end of the tutorial, the user understands that they are working on
a research platform, not using a chatbot. The agent is the interface; EP is the thing.

---

## The framing that matters most

Expected Parrot is research infrastructure — not a tool that generates answers and
disappears, but a platform where research lives. Everything built during the tutorial
has a permanent home there: permanent URLs, citable objects, open to inspection.

This framing should come through early — before anything runs — and be reinforced
throughout, not stated once and dropped.

The implicit message the user should carry away: *I built something today, and it
lives somewhere.*

---

## Principle 1: Introduce EP before running anything

Early in the tutorial — after the user has picked a topic but before any study is
designed — introduce what EP is and why it matters. Keep it brief. The point is to
set context, not deliver a lecture.

Cover:
- EP is a research platform; everything built today has a permanent home there
- It runs on EDSL, an open-source Python library — the methodology is transparent
  and reproducible regardless of whether the user writes code
- The user will be able to see, share, and extend everything produced today

Invite them to browse the EP library while the study is being set up. Seeing real
published studies from other researchers is more persuasive than any description.

---

## Principle 2: Show the survey builder when the survey is ready

When a survey or study instrument is created and published to EP, give the user the
link and direct them to open it. The builder is a visual interface — they can see
the questions laid out, click through the flow, and share the link with a colleague
for a second opinion.

This is the first moment the user touches EP directly rather than hearing about it.

Explain: this is a citable, shareable artifact before a single response has been
collected. That is different from a document on a local computer.

---

## Principle 3: Mention EDSL when running

When a job is running, briefly show or describe the EDSL code underneath it. This
does not require the user to read Python. The point is:

- Nothing is a black box
- The methodology is inspectable
- A developer or technical collaborator can extend it
- It is open-source — on GitHub, used by researchers and developers around the world

Even for users who will never write code themselves, this matters: their research
methodology is transparent and reproducible. That has value in academic contexts
(peer review, replication), enterprise contexts (auditability, hand-off to engineers),
and any context where the methodology might be questioned.

---

## Principle 4: Show results URL when results land

When results are collected and published to EP, give the user the URL immediately.
Explain what that URL contains: not just the summary, but the full study — the
instrument, the agent designs, the raw data. Anyone with the link can inspect the
methodology and reproduce the study.

This is the moment to contrast EP with a spreadsheet or a PDF: a shared EP URL is
a shared study, not a shared file.

---

## Principle 5: Human surveys — both pathways

After AI persona results are in, introduce the human research connection. Cover both
pathways:

**Prolific integration:** Expected Parrot connects directly to Prolific for participant
recruitment. The same survey can be deployed to real human respondents in one step —
same questions, same structure, no reformatting. Responses come back as standard EP
results objects, directly comparable to the AI run.

**Custom panels:** The survey link can also be shared directly — with the user's own
participants, a community, colleagues, or anyone they want to reach. There is no
requirement to use Prolific. Responses arrive in EP as they come in, and the agent
can analyze them when ready.

**Why this matters:** The AI persona run and the human run are not separate workflows.
They are the same survey, the same platform, the same result format. AI first to
pilot and iterate; humans to validate and extend. That is the intended research
workflow on EP.

---

## Principle 6: Close with the shareable study URL

At the end of the tutorial, present the full study URL on EP as the primary takeaway.
Explain what it contains and what happens when someone else opens it:

- They see the report
- They can navigate to the survey instrument, the agent panel, the raw data
- They can clone the study and run their own version
- They can see exactly what was done — methodology is transparent, not just conclusions

This is the viral mechanism: every shared URL is a complete study someone can inspect,
learn from, and extend. Encourage the user to share it.

The shareable URL is also the implicit answer to "what is EP?" — when someone receives
it and clicks through, they experience the platform directly.

---

## What EP is not

Do not describe EP as an "answer company" or position the agent as a service that
produces answers. The agent is a guide to the platform. The platform is the thing.

Do not oversell. Let the platform demonstrate itself through the objects the user
builds and publishes during the tutorial. The URL at the end does more persuasion
than any description.

---

## Audience notes

The platform framing resonates differently for different users — adjust the emphasis:

**Academic users:** Reproducibility, citability, transparent methodology, peer review
compatibility. The fact that a co-author can inspect the exact instrument and agent
design is significant. So is the ability to publish a study as a citable research
artifact.

**Enterprise users:** Auditability, shareability across teams, no vendor lock-in (EDSL
is open-source), the ability to hand the code to a developer for extension or
integration.

**Non-coders:** The open-source foundation matters even if they never write code —
their work is built on transparent infrastructure, not a black box. A developer on
their team can extend it. A reviewer can audit it.

**All users:** The human survey pathway. Regardless of domain, the ability to go from
AI pilot to human validation on the same platform — with the same survey — is a
core value proposition.
