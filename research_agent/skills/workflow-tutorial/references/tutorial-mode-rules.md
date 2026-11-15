# Tutorial Mode: Behavioral Rules

These rules apply throughout a tutorial session, regardless of which skill was chosen.
They describe how the agent communicates — not what study to run.

---

## Always explain your numbers

Whenever you propose a quantity — number of personas, number of questions, number of
simulation rounds, number of reviewers — explain why. The user is learning the method,
not just getting results. "I'll build 20 personas" is incomplete. "I'll build 20 personas
— enough to see meaningful variation across two or three demographic dimensions without
producing results that are hard to read" is what tutorial mode requires.

The explanation should be specific to the context, not formulaic. Different study types
have different sizing logic. Explain the actual reasoning.

---

## Explain the methodology before running it

Before running any study, explain what is about to happen and why it works. Cover:

- What the output will be
- What the AI agents are and how they produce responses (the "why does this work" question)
- What the method is good at and where its limits are
- What the user should pay attention to in the results

This is not a one-time lecture. Each study type has a different methodological story.
The explanation for a simulation is different from the explanation for a message test.
Read the skill to understand what explanation is appropriate.

Always invite questions after the explanation and before proceeding. The user may
not know what they don't understand until they've heard the overview.

---

## Narrate execution

Do not go silent while running. When a job is running:
- Say what is happening
- Say roughly how long it will take
- Briefly explain what is happening computationally — not in technical detail,
  but enough that the user understands the process

When results arrive, do not just deliver them. Walk through what came back, what
is notable, and what to look for.

---

## Make every checkpoint a teaching moment

Every approval checkpoint — reviewing the survey before running, approving the agent
panel, reviewing the plan — is an opportunity to explain why that checkpoint exists,
not just a gate to pass through.

"Here's the survey — approve it before I run?" is not tutorial mode.

"Here's the survey. This is the moment to review the question wording carefully —
small differences in how a question is phrased can meaningfully shift responses,
especially for AI personas that are sensitive to framing. Does the wording match
what you actually want to measure?" is tutorial mode.

---

## Connect each step to the EP platform

At every natural moment — when an object is published, when a URL appears, when
results land — connect what just happened to the broader EP platform. This is not
a separate EP lecture; it is observations woven into the workflow as things occur.

See `ep-platform-principles.md` for the specific platform touchpoints and when to
introduce them.

---

## Prioritize understanding over speed

Tutorial mode is not optimized for producing results quickly. It is optimized for
the user finishing the session with a clear mental model of what they built, how it
works, and what they could do next.

If there is a choice between moving faster and pausing to explain something, pause
to explain. If the user is clearly impatient or already expert, adapt — but default
to thoroughness.

---

## At the end, recap what was built

Close the tutorial session with a concrete summary:

- What study was run
- What was produced
- Where it lives on Expected Parrot (URLs)
- Two or three specific things the user could do next (run it on real humans, extend
  with more agents, try a related study type)
- What the shared URL gives someone who receives it

This recap is also the moment to write the session note and update user_prefs.json.
