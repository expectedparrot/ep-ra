# Pilot decisions

Propose a separate pilot when wording, persona differentiation, stimulus
handling, or scenario behavior is untested and a full-run mistake would be
costly. Specify the pilot's size, success criteria, expected cost, and what it
can change.

Also propose a small stratified compatibility pilot when a study combines a
new question type or output contract with multiple models/providers, especially
reasoning models or structured/numerical answers. Include at least one case per
model and representative simple and complex items. Success requires inspecting
parsed answers alongside raw generated output, checking answer completeness and
validation, and confirming adequate output-token headroom. Do not scale merely
because the expected number of result rows exists.

Skip a separate pilot when:

- the full run is already very small;
- only an instrument is being authored;
- the design was previously validated and changed only mechanically.

Record the judgment in the plan. If a pilot is warranted, make it the default
first execution phase. Plan approval does not authorize either the pilot or
the full paid run; request approval after showing the corresponding estimate.
