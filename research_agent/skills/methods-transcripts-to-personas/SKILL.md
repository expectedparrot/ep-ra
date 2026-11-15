---
name: methods-transcripts-to-personas
description: >
  Convert interview transcripts (.docx) into a taxonomy-labeled EDSL AgentList
  using a 3-pass map-reduce pipeline. Use when the user has interview
  transcripts and wants to create EDSL agents that represent the interviewees.
tags: [methods, qualitative, data-collection]
---

# Transcripts to Personas

Use this workflow when a user has `.docx` interview transcripts and wants to create an EDSL `AgentList` where each agent represents one interviewee. The pipeline automatically synthesizes a taxonomy from the transcripts, then labels every persona on each dimension.

A "transcript study" is a study whose purpose is to produce an AgentList. It follows the standard `topic_<alias>/study_<letter>/` structure, and follow-up studies can consume the resulting `agent_list.ep` from its original path or from a documented immutable copy.

---

## Before running this method

**Ask about context:**
- Where did these transcripts come from? (customer interviews, research project, focus groups?)
- What's the goal for the agent panel? (follow-up survey, simulation, exploratory analysis?)
- Are there specific traits, segments, or tensions you're hoping the taxonomy will capture?
- Any concerns about how the personas might be constructed or what the taxonomy might miss?

**Explain the approach:**
The pipeline uses a 3-pass process: (1) extract narrative personas and raw attributes from each transcript, (2) synthesize a shared taxonomy of dimensions and labels across all transcripts, (3) classify each persona on every dimension. The taxonomy emerges from the data — you'll see it after Pass 2 and can give feedback before finalizing.

**Discuss design choices:**
- Do you want interviewer names preserved as metadata, or should they be anonymized?
- Should the personas be written in first person ("I am...") or third person ("This person is...")? Default is third person to maintain distance from real individuals.

More context about your research goals helps the pipeline surface the right distinctions. Providing context doesn't bias the taxonomy — it helps ensure the dimensions that emerge are actually useful for your purpose.

---

## Study Setup

### 1. Scaffold the study

```bash
ep study scaffold sessions/topic_<alias>/study_a
```

### 2. Place transcripts

Copy the user's `.docx` files into `data/raw/transcripts/`:

```bash
mkdir -p data/raw/transcripts
cp /path/to/interviews/*.docx data/raw/transcripts/
```

### 3. Copy the pipeline script

```bash
mkdir -p edsl_jobs/job_a
cp research_agent/skills/methods-transcripts-to-personas/scripts/transcripts_to_personas.py edsl_jobs/job_a/
```

### 4. Create the run wrapper

Write `edsl_jobs/job_a/run_job.py`:

```python
"""Wrapper that runs the transcripts-to-personas pipeline with study-relative paths."""
import shutil
from pathlib import Path
from transcripts_to_personas import run_pipeline

_STUDY_ROOT = Path(__file__).resolve().parent.parent.parent
_INPUT_DIR = _STUDY_ROOT / "data" / "raw" / "transcripts"
_INTERMEDIATES_DIR = _STUDY_ROOT / "computed_objects"
_COOKED_DIR = _STUDY_ROOT / "data" / "cooked"

def main():
    # Run the full pipeline, writing all outputs to computed_objects/
    agent_list = run_pipeline(
        input_dir=str(_INPUT_DIR),
        output_dir=str(_INTERMEDIATES_DIR),
    )

    if agent_list is None:
        print("Pipeline did not complete. Check intermediate files in computed_objects/.")
        return

    # Copy final artifacts to data/cooked/
    _COOKED_DIR.mkdir(parents=True, exist_ok=True)
    for filename in ("agent_list.ep", "taxonomy.json", "pass3_label_summary.json"):
        src = _INTERMEDIATES_DIR / filename
        if src.exists():
            shutil.copy2(src, _COOKED_DIR / filename)
            print(f"  Copied {filename} -> data/cooked/{filename}")

    print(f"\nDone. AgentList with {len(agent_list)} agents at data/cooked/agent_list.ep")

if __name__ == "__main__":
    main()
```

### 5. Wire up the Makefile

Add an `agents` target to the study Makefile:

```makefile
# --- Transcript-to-persona pipeline ---
agents: data/cooked/agent_list.ep

data/cooked/agent_list.ep: edsl_jobs/job_a/run_job.py $(wildcard data/raw/transcripts/*.docx)
	cd edsl_jobs/job_a && python run_job.py
```

Keep the standard report targets (`PLOTS`, `TABLES`, `report`) as usual.

---

## Pipeline Architecture

The script `transcripts_to_personas.py` uses a 3-pass map-reduce approach:

1. **Pass 1 (MAP)** -- Per transcript: extract narrative persona ("This person..."), personality profile, knowledge profile, goals/pain points, raw dimension attributes, and interviewer name.
2. **Pass 2 (REDUCE)** -- Across all personas: synthesize a dimension taxonomy (e.g., `technical_proficiency`, `decision_authority`) with discrete labels per dimension.
3. **Pass 3 (MAP)** -- Per persona: classify each persona on every taxonomy dimension using `QuestionMultipleChoice`.
4. **Assembly** -- Build an `AgentList` with shared `codebook` and `instruction`.

Expect 3-5 minutes for ~10 transcripts.

---

## Output Files

After the pipeline runs, the study directory will contain:

### Intermediate files (`computed_objects/`)

| File | Description |
|------|-------------|
| `pass1_personas.json` | Extracted narrative personas and raw attributes |
| `pass1_raw_attributes.json` | Flattened attributes for taxonomy synthesis |
| `pass2_taxonomy.json` | Dimension taxonomy with labels |
| `pass3_labeled_personas.json` | Personas with taxonomy labels applied |
| `pass3_label_summary.json` | Summary table: one row per persona, one column per dimension |

### Final artifacts (`data/cooked/`)

| File | Description |
|------|-------------|
| `agent_list.ep` | Serialized `AgentList` (load via `AgentList.git.load()`) |
| `taxonomy.json` | Final taxonomy with dimensions, labels, and descriptions |
| `pass3_label_summary.json` | Label summary table (useful for the report) |

---

## Agent Structure

Each `Agent` in the resulting `AgentList` has:

- **`persona`** -- Narrative persona (uses "This person" -- no real names)
- **`personality`** -- Communication and temperament profile
- **`knowledge`** -- Expertise and technical proficiency profile
- **`goals_and_pain`** -- Goals, frustrations, and unmet needs
- **`_file_name`** -- Source transcript filename (metadata)
- **`_interviewer`** -- Interviewer/moderator name (metadata)
- **Taxonomy dimensions** -- One trait per dimension (e.g., `technical_proficiency: "advanced"`)

The shared **codebook** maps every trait key to a human-readable description. The shared **instruction** tells agents to stay in character.

---

## Using the AgentList in Follow-up Studies

A follow-up study (e.g., `study_b`) can consume the AgentList directly:

### 1. Create the follow-up study

```bash
ep study scaffold sessions/topic_<alias>/study_b
```

### 2. Record the predecessor

Add the absolute `study_a` path and any study/session identifier to `study_b/writeup/planning.md`. Read `study_a/chat_summary.md` first. If a portable immutable copy is required, copy only `data/cooked/agent_list.ep` into `study_b/refs/study_a/data/cooked/` and add the provenance manifest required by `skill:workflow-file-layout`.

### 3. Load the AgentList in job code

In `edsl_jobs/job_a/study_agent_list.py`:

```python
from pathlib import Path
from edsl import AgentList

_STUDY_ROOT = Path(__file__).resolve().parent.parent.parent
_AGENT_LIST_PATH = Path("<absolute_path_to_study_a>") / "data" / "cooked" / "agent_list.ep"

agent_list = AgentList.git.load(str(_AGENT_LIST_PATH))
```

### 4. Filter by taxonomy dimension

```python
# Get only agents with advanced+ technical proficiency
technical = [a for a in agent_list if a.traits.get("technical_proficiency") in ("advanced", "expert")]
filtered_list = AgentList(technical)
```

---

## Report

The report for a transcript study should document the agent panel. Use this structure for `writeup/report.md`:

```markdown
---
title: "Interview Transcript Agent Panel"
date: YYYY-MM-DD
---

## Summary

Brief overview: number of transcripts processed, purpose of the agent panel,
and the taxonomy that emerged.

## Data Source

- Number of transcripts: N
- Format: .docx interview transcripts
- Source: [description of the interview project]

## Taxonomy

Describe each taxonomy dimension, its possible labels, and what behavioral
signals each label captures. Include the full taxonomy table.

## Agent Panel Overview

- Total agents: N
- Taxonomy dimensions: K

### Label Distributions

For each dimension, show the count of agents per label. Use tables or bar charts.

### Example Personas

Include 2-3 representative persona excerpts (anonymized) that illustrate
the range of the panel.

## Files Generated

| File | Description |
|------|-------------|
| `data/cooked/agent_list.ep` | Serialized AgentList |
| `data/cooked/taxonomy.json` | Taxonomy definitions |
| `data/cooked/pass3_label_summary.json` | Label summary table |
```

---

## Study Structure Reference

```
topic_<alias>/
  study_a/                           <- transcript processing study
    data/
      raw/transcripts/               <- .docx files
      cooked/
        agent_list.ep                <- final AgentList
        taxonomy.json                <- final taxonomy
        pass3_label_summary.json     <- label summary
    edsl_jobs/
      job_a/
        transcripts_to_personas.py   <- pipeline script
        run_job.py                   <- wrapper
    computed_objects/                 <- all intermediate pass files
    writeup/
      report.md
    Makefile
    plan.md
    checklist.md
  study_b/                           <- follow-up survey using the agents
    edsl_jobs/
      job_a/
        study_agent_list.py          <- loads from the predecessor path recorded in planning.md
```

---

## Quick Reference

| Task | How |
|------|-----|
| Scaffold study | `ep study scaffold sessions/topic_<alias>/study_a` |
| Place transcripts | Copy `.docx` files to `data/raw/transcripts/` |
| Copy pipeline script | `cp research_agent/skills/methods-transcripts-to-personas/scripts/transcripts_to_personas.py edsl_jobs/job_a/` |
| Run pipeline | `make agents` |
| Resume after failure | Add `--resume` flag in `run_job.py` call |
| Run single pass | Modify `run_job.py` to pass `only_pass=N` |
| Load result AgentList | `AgentList.git.load("data/cooked/agent_list.ep")` |
| Use in follow-up study | Record predecessor path and load in place; copy only required artifacts when portability is needed |
