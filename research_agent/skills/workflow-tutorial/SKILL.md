---
name: workflow-tutorial
description: >
  Explains what this system can do and how it works, in plain language.
  Use when the user asks about capabilities, wants a tutorial, or says
  something like "what can you do?" or "how does this work?"
tags: [workflow, reference]
---

# System Tutorial

When the user asks what this system can do, walk them through it conversationally. Tailor depth to their apparent familiarity — a first-time user gets the full picture; someone who has run studies before gets a refresher on the parts they ask about.

## What this system is

This is a research assistant that designs, runs, and analyzes studies using AI agent panels — simulated respondents with realistic personas. Instead of recruiting human participants for every question, you describe what you want to learn and the system builds a study, runs it against AI agents, and delivers a report.

The underlying engine is EDSL (Expected Parrot Domain-Specific Language), a Python framework for survey and simulation research. You do not need to know EDSL to use this system — describe your research goal in plain language and the system handles the technical details.

## What you can study

The system supports a range of research types. Mention these conversationally based on what seems relevant to the user — do not read out a list unless asked.

**Surveys and polling** — attitude measurement, awareness tracking, NPS, satisfaction, opinion polling, demographic profiling. The bread and butter.

**Concept testing** — screen, compare, or rank multiple product/service/feature concepts against an agent panel to see which resonates and why.

**Message testing** — A/B test copy variants (email subjects, ad copy, taglines) with statistical analysis of which performs best.

**Pricing research** — Van Westendorp, Gabor-Granger, or tiered pricing optimization to find optimal price points.

**Conjoint analysis** — discrete choice experiments that measure how people trade off product attributes like features, price, and brand.

**Design comparison** — visual A/B testing of two design variants using side-by-side evaluation.

**Eye tracking simulation** — heatmaps showing where people look first on an image, ad, or page design.

**Website feedback** — structured UX, design, and accessibility feedback on live websites via screenshot analysis.

**Slide deck review** — per-slide feedback with dimension scores, rankings, and optional eye-tracking heatmaps.

**Interview design** — create interview guides for human moderators or deploy AI-led interviews.

**Social simulation** — agent-based social simulations (negotiations, coordination games, group dynamics) using the Concordia framework.

**Data labeling** — classify or tag rows of tabular data using LLM-powered survey instruments.

## How a typical study works

1. **You describe what you want to learn.** A research question, a business decision, a product you are evaluating — whatever the goal is.
2. **The system proposes a plan.** This includes the agent personas, the survey or simulation design, expected outputs, and decision points where your input matters. You review and adjust before anything runs.
3. **The study runs.** AI agents with the designed personas respond to the survey or participate in the simulation.
4. **You get a report.** Analysis, visualizations, and findings — typically as a self-contained HTML document. The system checks its own work before delivering.

At every stage you can steer: change personas, rewrite questions, adjust the model, or pivot the approach entirely.

## What to say to get started

You do not need to use any special syntax or commands. Just describe what you want to learn. Examples:

- "I want to test three tagline options for our new product launch"
- "How price-sensitive are small business owners to our SaaS pricing?"
- "Compare these two landing page designs"
- "I need to understand how different investor types evaluate AI startups"
- "Run a quick poll on remote work preferences across job roles"

The system will figure out which study type fits and propose a plan.
