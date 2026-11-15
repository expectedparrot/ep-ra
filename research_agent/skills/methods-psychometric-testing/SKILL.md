---
name: methods-psychometric-testing
description: Compatibility router for reliability, item-total, scale coherence, and exploratory instrument diagnostics. Use when the user asks to psychometrically test or prune a multi-item survey scale; route the work to Messick rather than implementing calculations in ad hoc scripts.
tags: [methods, quantitative, analysis, psychometrics]
---

# Route psychometric testing to Messick

Load `skill:research-instrument-pretesting` and follow its Messick workflow.
Messick owns scale definitions, evidence sources, reverse-scoring declarations,
reliability and item diagnostics, revision decisions, and claim-bounded
validation. Do not copy formulas into a study script or install analysis
packages during a run.

Require an explicit scale definition and intended score interpretation before
analysis. Treat simulated-pilot reliability as simulation evidence, not proof of
human reliability or dimensionality. Consequential human claims require suitable
human evidence, but lack of human data does not block a useful simulation-first
pretest and revision report.
