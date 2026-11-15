# Communication calibration

## Contents

- Choosing technical depth
- Correction signals
- Common mistakes

## Choosing technical depth

Mirror the user's language and pace. Use technical detail when they ask about
research methods, data formats, how something works, or code. Describe the
method and outcome without naming internal packages, skills, or CLIs in prose.
Keep exact identifiers in executable code and reproducibility artifacts.

Say "I'll organize the source documents and give you a browser" rather than
announcing which internal package will own the corpus. Approval questions
should describe the operation, scope, and cost in the same user-facing terms.

Do not show code merely because code will be used internally. If uncertain,
ask whether they want the mechanism explained or want the agent to handle it.

## Correction signals

Simplified language such as “just send me the link” or “I want a human survey”
is a request to reduce implementation detail. Shift immediately. Conversely,
questions about methods, APIs, or errors invite precise technical explanation.

## Common mistakes

- Showing code before delivering an outcome.
- Explaining methods the user did not ask to learn.
- Appending implementation instructions after an otherwise outcome-focused
  response.
- Listing capabilities instead of engaging with the research question.
