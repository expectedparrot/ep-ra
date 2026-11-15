"""
transcript_to_persona.py
========================
Converts user interview transcripts (.docx) into an EDSL AgentList where each
Agent has traits extracted from the transcript and all agents share a common
codebook (derived from the taxonomy) and instruction.

Architecture (3-pass map-reduce):
  Pass 1 (MAP)   – Per transcript: extract narrative persona + raw attributes
  Pass 2 (REDUCE)– Across all: synthesize dimension taxonomy
  Pass 3 (MAP)   – Per persona: apply taxonomy labels
  Assembly        – Build AgentList with shared codebook and instruction

Usage:
  python transcript_to_persona.py --input-dir ./transcripts/ --output-dir ./personas/
  python transcript_to_persona.py --input-dir ./transcripts/ --pass 1  # run only pass 1
  python transcript_to_persona.py --resume ./personas/                 # resume from pass 2

Requirements:
  pip install edsl python-docx
"""

import argparse
import json
import glob
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from edsl import (
    QuestionFreeText,
    QuestionList,
    QuestionMultipleChoice,
    Survey,
    Scenario,
    ScenarioList,
    Model,
    Agent,
    AgentList,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# No default model on purpose: a hardcoded name goes stale and would then be used
# silently. --model is required; confirm a current name with
# ep models. See skill:workflow-model-selection.

# How many dimensions to aim for in taxonomy synthesis
TARGET_DIMENSION_COUNT = 8

# Maximum transcript length (in chars) before chunking/summarizing
MAX_TRANSCRIPT_CHARS = 80_000


def run_via_ep_cli(survey: Survey, model: Model, output_dir: str, stem: str,
                   description: str, scenarios: Optional[ScenarioList] = None):
    """Persist, price, confirm, and execute one pipeline pass via the EP CLI."""
    from edsl import ModelList, Results

    survey_path = os.path.join(output_dir, f"{stem}_survey.ep")
    models_path = os.path.join(output_dir, f"{stem}_models.ep")
    jobs_path = os.path.join(output_dir, f"{stem}_jobs.ep")
    results_path = os.path.join(output_dir, f"{stem}_results.ep")
    survey.git.save(survey_path)
    ModelList([model]).git.save(models_path)
    command = ["ep", "jobs", "build", "--survey", survey_path, "--models", models_path]
    if scenarios is not None:
        scenarios_path = os.path.join(output_dir, f"{stem}_scenarios.ep")
        scenarios.git.save(scenarios_path)
        command.extend(["--scenarios", scenarios_path])
    command.extend(["--output", jobs_path])
    subprocess.run(command, check=True)
    subprocess.run(["ep", "jobs", "cost", jobs_path], check=True)
    if input(f"Run paid {stem}? Type 'yes' to continue: ").strip().lower() != "yes":
        raise SystemExit(f"Run cancelled. Saved job: {jobs_path}")
    subprocess.run([
        "ep", "run", jobs_path,
        "--remote_inference_description", description,
        "--results_description", description,
        "--output", results_path,
    ], check=True)
    return Results.git.load(results_path)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_transcript(filepath: str) -> str:
    """Load a .docx transcript and return its full text."""
    from docx import Document

    doc = Document(filepath)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def load_transcripts(input_dir: str) -> ScenarioList:
    """Load all .docx files from a directory into an EDSL ScenarioList."""
    files = sorted(glob.glob(os.path.join(input_dir, "*.docx")))
    if not files:
        print(f"No .docx files found in {input_dir}")
        sys.exit(1)

    scenarios = []
    for fp in files:
        filename = os.path.basename(fp)
        text = load_transcript(fp)

        # Truncate very long transcripts with a note
        if len(text) > MAX_TRANSCRIPT_CHARS:
            text = text[:MAX_TRANSCRIPT_CHARS] + "\n\n[TRANSCRIPT TRUNCATED]"

        scenarios.append(Scenario({
            "filename": filename,
            "transcript": text,
        }))

    print(f"Loaded {len(scenarios)} transcripts from {input_dir}")
    return ScenarioList(scenarios)


def save_json(data, filepath: str):
    """Write data to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  Saved: {filepath}")


def load_json(filepath: str):
    """Read data from a JSON file."""
    with open(filepath) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Pass 1: Extract narrative personas + raw attributes (MAP)
# ---------------------------------------------------------------------------

def build_pass1_survey() -> Survey:
    """
    Build the per-transcript extraction survey.

    Question flow (with piping):
      1. narrative_persona  ← reads raw transcript
      2. personality_profile ← reads narrative (piped)
      3. knowledge_profile   ← reads narrative (piped)
      4. goals_and_pain      ← reads narrative (piped)
      5. raw_attributes      ← reads narrative (piped), extracts dimension signals
    """

    q_narrative = QuestionFreeText(
        question_name="narrative_persona",
        question_text="""You are a user researcher synthesizing an interview transcript into
a narrative persona for use as an AI agent.

Read the following interview transcript carefully:

{{ scenario.transcript }}

Write a rich, third-person narrative persona (600-1200 words) that captures:
- WHO this person is (role, background, context)
- WHAT they're trying to accomplish and why
- HOW they currently work (tools, workflows, habits)
- Their decision-making style and heuristics
- Frustrations, workarounds, and unmet needs
- Their language patterns, vocabulary level, and communication style
- Emotional responses and what motivates/demotivates them
- Their relationship to technology and willingness to adopt new tools

Write as a vivid character portrait — not a list of attributes.
Preserve the person's voice by weaving in characteristic phrases or expressions.
Refer to the person as "This person" throughout — do NOT use their real name or a pseudonym.""",
    )

    q_personality = QuestionFreeText(
        question_name="personality_profile",
        question_text="""Based on the persona below, write a concise personality profile
suitable for configuring an AI agent to simulate this person.

Persona:
{{ narrative_persona.answer }}

Cover:
- Communication style (formal/casual, verbose/terse, direct/diplomatic)
- Emotional temperament (patient/impatient, optimistic/skeptical, etc.)
- Risk tolerance and openness to change
- How they handle ambiguity and uncertainty
- Social dynamics (leader/follower, collaborative/independent)

Write 150-300 words in third person. Be specific and behavioral, not abstract.""",
    )

    q_knowledge = QuestionFreeText(
        question_name="knowledge_profile",
        question_text="""Based on the persona below, write a knowledge and expertise profile.

Persona:
{{ narrative_persona.answer }}

Cover:
- Domain expertise (what they know deeply)
- Technical proficiency (specific tools, platforms, skills)
- Knowledge gaps (what they don't know or misunderstand)
- How they learn new things (self-taught, formal training, peer learning)
- Information sources they trust and distrust

Write 150-300 words in third person. Be specific — name tools, concepts, domains.""",
    )

    q_goals = QuestionFreeText(
        question_name="goals_and_pain",
        question_text="""Based on the persona below, write a goals and pain points profile.

Persona:
{{ narrative_persona.answer }}

Cover:
- Primary goals (what they're trying to achieve in their role)
- Secondary/aspirational goals
- Key pain points and frustrations (be specific)
- Workarounds they've developed
- What "success" looks like to them
- What would make them switch tools or change behavior

Write 150-300 words in third person.""",
    )

    q_raw_attrs = QuestionList(
        question_name="raw_attributes",
        question_text="""Based on the persona below, extract a list of factual attributes
that could be used as dimensions to categorize and compare this person against
other interview subjects.

Persona:
{{ narrative_persona.answer }}

For each attribute, use the format "DIMENSION_NAME: value" — for example:
- "team_size: 3-5 people"
- "decision_authority: needs_manager_approval"
- "technical_skill: intermediate"
- "primary_use_case: data_analysis"
- "industry: healthcare"
- "years_experience: 5-10"
- "adoption_stage: evaluating"

Extract as many meaningful attributes as you can find evidence for in the persona.
Be specific with values — use short, standardizable labels rather than sentences.""",
        max_list_items=30,
    )

    q_interviewer = QuestionFreeText(
        question_name="interviewer_name",
        question_text="""Look at the transcript below and identify the interviewer's
or moderator's first name (the person asking the questions — NOT the interviewee).

{{ scenario.transcript }}

Return ONLY the first name, nothing else. If you cannot determine the name,
return "Unknown".""",
    )

    survey = Survey(questions=[
        q_narrative,
        q_personality,
        q_knowledge,
        q_goals,
        q_raw_attrs,
        q_interviewer,
    ])

    return survey


def run_pass1(scenarios: ScenarioList, model: Model, output_dir: str) -> dict:
    """
    Run Pass 1: extract personas from all transcripts.
    Returns a dict of {filename: {narrative, personality, knowledge, goals, raw_attributes}}.
    """
    print("\n" + "=" * 60)
    print("PASS 1: Extracting narrative personas + raw attributes")
    print("=" * 60)

    survey = build_pass1_survey()
    results = run_via_ep_cli(
        survey, model, output_dir, "pass1",
        f"Transcript personas pass 1 - {len(scenarios)} transcripts", scenarios,
    )

    personas = {}
    filenames = results.select("filename").to_list(flatten=True)
    narratives = results.select("narrative_persona").to_list(flatten=True)
    personalities = results.select("personality_profile").to_list(flatten=True)
    knowledges = results.select("knowledge_profile").to_list(flatten=True)
    goals_list = results.select("goals_and_pain").to_list(flatten=True)
    raw_attrs_list = results.select("raw_attributes").to_list(flatten=True)
    interviewer_list = results.select("interviewer_name").to_list(flatten=True)

    for i, fn in enumerate(filenames):
        personas[fn] = {
            "filename": fn,
            "narrative": narratives[i],
            "personality": personalities[i],
            "knowledge": knowledges[i],
            "goals_and_pain": goals_list[i],
            "raw_attributes": raw_attrs_list[i],
            "interviewer_name": interviewer_list[i],
        }

    # Save intermediate results
    save_json(personas, os.path.join(output_dir, "pass1_personas.json"))

    # Also save all raw attributes flattened for pass 2
    all_attrs = []
    for fn, p in personas.items():
        for attr in p["raw_attributes"]:
            all_attrs.append({"filename": fn, "attribute": attr})
    save_json(all_attrs, os.path.join(output_dir, "pass1_raw_attributes.json"))

    print(f"\nPass 1 complete: {len(personas)} personas extracted")
    return personas


# ---------------------------------------------------------------------------
# Pass 2: Synthesize dimension taxonomy (REDUCE)
# ---------------------------------------------------------------------------

def build_pass2_survey(all_attributes_text: str, persona_count: int) -> Survey:
    """
    Build the taxonomy synthesis survey.
    This runs once across all aggregated raw attributes.
    """

    q_dimensions = QuestionList(
        question_name="dimension_names",
        question_text=f"""You are designing a taxonomy for classifying user personas derived
from {persona_count} interview transcripts.

Here are ALL the raw attributes extracted across all personas:

{all_attributes_text}

Identify {TARGET_DIMENSION_COUNT}-{TARGET_DIMENSION_COUNT + 4} dimension names that:
1. Are applicable to MOST personas (not just one)
2. Have meaningful variation across the population
3. Would be useful for configuring AI agent behavior
4. Cover different facets: demographics, behavior, psychology, goals, context

Return a list of dimension names in snake_case (e.g., "technical_proficiency",
"decision_authority", "adoption_readiness").

Prefer dimensions that discriminate — avoid dimensions where everyone would
have the same value.""",
        max_list_items=TARGET_DIMENSION_COUNT + 4,
    )

    q_taxonomy = QuestionFreeText(
        question_name="taxonomy_definition",
        question_text="""You identified these dimensions: {{ dimension_names.answer }}

Now, for EACH dimension, define:
1. A brief description (1 sentence)
2. The set of possible labels/values (3-6 discrete options)
3. What behavioral signal each label maps to

Format your response as a structured list. Example:

DIMENSION: technical_proficiency
Description: The person's comfort and skill with technical tools and concepts.
Labels:
  - novice: Struggles with basic tools; needs hand-holding
  - intermediate: Comfortable with standard tools; can follow technical docs
  - advanced: Builds custom workflows; writes scripts or code
  - expert: Deep technical knowledge; could build the product themselves

Cover all {{ dimension_names.answer | length }} dimensions.""",
    )

    return Survey(questions=[q_dimensions, q_taxonomy])


def parse_taxonomy_text(taxonomy_text: str) -> dict:
    """
    Parse the structured taxonomy text into a dict.
    Expected format per dimension:
        **DIMENSION: name** (or DIMENSION: name)
        Description: ...
        Labels:
        - label: description
        - label: description
    """
    import re

    parsed = {}
    # Split into dimension blocks
    blocks = re.split(r'\*{0,2}DIMENSION:\s*', taxonomy_text)
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split('\n')
        # First line is dimension name (possibly with trailing **)
        dim_name = lines[0].strip().rstrip('*').strip()

        description = ""
        labels = []
        label_descriptions = {}

        for line in lines[1:]:
            line = line.strip()
            if line.lower().startswith('description:'):
                description = line.split(':', 1)[1].strip()
            elif line.startswith('- ') and ':' in line:
                # Label line: "- label_name: description text"
                label_part = line[2:]  # strip "- "
                label_name, label_desc = label_part.split(':', 1)
                label_name = label_name.strip()
                label_desc = label_desc.strip()
                labels.append(label_name)
                label_descriptions[label_name] = label_desc

        if dim_name:
            parsed[dim_name] = {
                "description": description,
                "labels": labels,
                "label_descriptions": label_descriptions,
            }

    return parsed


def run_pass2(personas: dict, model: Model, output_dir: str) -> dict:
    """
    Run Pass 2: synthesize a dimension taxonomy from all raw attributes.
    Returns the taxonomy dict.
    """
    print("\n" + "=" * 60)
    print("PASS 2: Synthesizing dimension taxonomy")
    print("=" * 60)

    # Aggregate all raw attributes
    all_attrs = []
    for fn, p in personas.items():
        all_attrs.extend(p["raw_attributes"])

    # Deduplicate and format
    unique_attrs = sorted(set(all_attrs))
    all_attributes_text = "\n".join(f"- {a}" for a in unique_attrs)

    print(f"  Aggregated {len(all_attrs)} raw attributes ({len(unique_attrs)} unique)")

    # Run taxonomy synthesis
    survey = build_pass2_survey(all_attributes_text, len(personas))
    results = run_via_ep_cli(
        survey, model, output_dir, "pass2",
        f"Transcript personas pass 2 - {len(personas)} personas",
    )

    dimensions = results.select("dimension_names").to_list(flatten=True)
    taxonomy_text = results.select("taxonomy_definition").to_list(flatten=True)[0]

    print(f"  Identified {len(dimensions)} dimensions: {dimensions}")

    # Parse the structured text directly
    parsed = parse_taxonomy_text(taxonomy_text)

    # Keep only dimensions that were fully parsed (have labels)
    dimensions = [d for d in dimensions if d in parsed and parsed[d]["labels"]]
    print(f"  Successfully parsed {len(dimensions)} dimensions with labels")

    taxonomy = {
        "dimensions": dimensions,
        "definitions": parsed,
        "raw_taxonomy_text": taxonomy_text,
    }

    save_json(taxonomy, os.path.join(output_dir, "pass2_taxonomy.json"))

    print(f"\nPass 2 complete: taxonomy with {len(dimensions)} dimensions")
    return taxonomy


# ---------------------------------------------------------------------------
# Pass 3: Apply taxonomy labels to each persona (MAP)
# ---------------------------------------------------------------------------

def build_pass3_survey(taxonomy: dict) -> Survey:
    """
    Build the labeling survey. For each dimension in the taxonomy,
    create a QuestionMultipleChoice asking the model to classify the persona.
    """
    questions = []

    definitions = taxonomy.get("definitions", {})

    for dim_name in taxonomy["dimensions"]:
        dim_def = definitions.get(dim_name, {})
        labels = dim_def.get("labels", ["unknown"])
        description = dim_def.get("description", dim_name)

        # Build label descriptions for the prompt
        label_descs = dim_def.get("label_descriptions", {})
        options_text = "\n".join(
            f"  - {label}: {label_descs.get(label, '')}" for label in labels
        )

        q = QuestionMultipleChoice(
            question_name=f"dim_{dim_name}",
            question_text=f"""Classify this persona on the dimension "{dim_name}".

Dimension description: {description}

Options:
{options_text}

Persona narrative:
{{{{ scenario.narrative }}}}

Personality: {{{{ scenario.personality }}}}
Knowledge: {{{{ scenario.knowledge }}}}
Goals: {{{{ scenario.goals_and_pain }}}}

Choose the single best label for this persona.""",
            question_options=labels,
        )
        questions.append(q)

    # Also ask for a confidence/notes field
    q_notes = QuestionFreeText(
        question_name="labeling_notes",
        question_text="""You just classified a persona across multiple dimensions.

For any dimensions where the classification was ambiguous or the persona
doesn't fit neatly into a single label, note which dimensions and why.
If all classifications were clear, say "All classifications clear."

Be brief (1-3 sentences).""",
    )
    questions.append(q_notes)

    return Survey(questions=questions)


def run_pass3(
    personas: dict, taxonomy: dict, model: Model, output_dir: str
) -> list:
    """
    Run Pass 3: label each persona using the taxonomy.
    Returns a list of labeled persona dicts.
    """
    print("\n" + "=" * 60)
    print("PASS 3: Applying taxonomy labels to personas")
    print("=" * 60)

    # Build scenarios from persona narratives
    scenarios = ScenarioList([
        Scenario({
            "filename": fn,
            "narrative": p["narrative"],
            "personality": p["personality"],
            "knowledge": p["knowledge"],
            "goals_and_pain": p["goals_and_pain"],
        })
        for fn, p in personas.items()
    ])

    survey = build_pass3_survey(taxonomy)
    results = run_via_ep_cli(
        survey, model, output_dir, "pass3",
        f"Transcript personas pass 3 - {len(scenarios)} personas", scenarios,
    )

    # Extract results
    filenames = results.select("filename").to_list(flatten=True)
    notes = results.select("labeling_notes").to_list(flatten=True)

    labeled_personas = []
    for i, fn in enumerate(filenames):
        persona_data = personas[fn].copy()
        persona_data["labels"] = {}

        for dim_name in taxonomy["dimensions"]:
            col_name = f"dim_{dim_name}"
            values = results.select(col_name).to_list(flatten=True)
            persona_data["labels"][dim_name] = values[i]

        persona_data["labeling_notes"] = notes[i]
        labeled_personas.append(persona_data)

    save_json(labeled_personas, os.path.join(output_dir, "pass3_labeled_personas.json"))

    # Also save a summary table
    summary = []
    for lp in labeled_personas:
        row = {"filename": lp["filename"]}
        row.update(lp["labels"])
        summary.append(row)
    save_json(summary, os.path.join(output_dir, "pass3_label_summary.json"))

    print(f"\nPass 3 complete: {len(labeled_personas)} personas labeled")
    return labeled_personas


# ---------------------------------------------------------------------------
# Final output: assemble agent-ready persona files
# ---------------------------------------------------------------------------

def assemble_agent_list(
    labeled_personas: list, taxonomy: dict, output_dir: str
) -> AgentList:
    """
    Build an EDSL AgentList from labeled personas with shared codebook
    and instruction derived from the taxonomy.
    """
    print("\n" + "=" * 60)
    print("ASSEMBLING AgentList")
    print("=" * 60)

    # Build codebook from taxonomy definitions — maps trait keys to descriptions
    definitions = taxonomy.get("definitions", {})
    codebook = {
        "persona": "Narrative persona synthesized from interview transcript",
        "personality": "Personality and communication style profile",
        "knowledge": "Knowledge, expertise, and technical proficiency profile",
        "goals_and_pain": "Goals, pain points, and unmet needs",
        "_file_name": "Source transcript filename",
        "_interviewer": "Name of the interviewer/moderator",
    }
    for dim_name in taxonomy["dimensions"]:
        dim_def = definitions.get(dim_name, {})
        description = dim_def.get("description", dim_name)
        labels = dim_def.get("labels", [])
        codebook[dim_name] = f"{description} (possible values: {', '.join(labels)})"

    # Build individual Agent objects
    agents = []
    for lp in labeled_personas:
        filename = lp["filename"]
        # Extract real name from filename (e.g. "Current User_ Brent_ENGLISH..." -> "Brent")
        stem = Path(filename).stem
        parts = stem.split("_")
        # Name is typically the second segment; strip extra info like " - Small Business"
        raw_name = parts[1].strip() if len(parts) > 1 else stem
        agent_name = raw_name.split(" - ")[0].strip()

        traits = {
            "persona": lp["narrative"],
            "personality": lp["personality"],
            "knowledge": lp["knowledge"],
            "goals_and_pain": lp["goals_and_pain"],
            "_file_name": filename,
            "_interviewer": lp.get("interviewer_name", "Unknown"),
            **lp["labels"],
        }
        agents.append(Agent(name=agent_name, traits=traits))

    agent_list = AgentList(
        data=agents,
        codebook=codebook,
        instruction=(
            "You are answering questions as if you were a human. "
            "Do not break character. Use your persona, personality, "
            "knowledge, and goals to inform your responses."
        ),
    )

    # Save taxonomy and agent list for reference
    save_json(taxonomy, os.path.join(output_dir, "taxonomy.json"))
    agent_list.git.save(os.path.join(output_dir, "agent_list.ep"))

    print(f"\nDone! AgentList with {len(agent_list)} agents assembled")
    return agent_list


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    input_dir: str,
    output_dir: str,
    model_name: str,
    only_pass: Optional[int] = None,
    resume: bool = False,
) -> Optional[AgentList]:
    """Run the full 3-pass pipeline (or a specific pass). Returns an AgentList."""

    os.makedirs(output_dir, exist_ok=True)
    model = Model(model_name, max_tokens=4000)

    # --- Pass 1 ---
    if only_pass is None or only_pass == 1:
        if resume and os.path.exists(os.path.join(output_dir, "pass1_personas.json")):
            print("Resuming: loading Pass 1 results from disk")
            personas = load_json(os.path.join(output_dir, "pass1_personas.json"))
        else:
            scenarios = load_transcripts(input_dir)
            personas = run_pass1(scenarios, model, output_dir)

        if only_pass == 1:
            print("\nPass 1 complete. Run with --pass 2 or no --pass flag to continue.")
            return None
    else:
        personas = load_json(os.path.join(output_dir, "pass1_personas.json"))

    # --- Pass 2 ---
    if only_pass is None or only_pass == 2:
        if resume and os.path.exists(os.path.join(output_dir, "pass2_taxonomy.json")):
            print("Resuming: loading Pass 2 results from disk")
            taxonomy = load_json(os.path.join(output_dir, "pass2_taxonomy.json"))
        else:
            taxonomy = run_pass2(personas, model, output_dir)

        if only_pass == 2:
            print("\nPass 2 complete. Run with --pass 3 or no --pass flag to continue.")
            return None
    else:
        taxonomy = load_json(os.path.join(output_dir, "pass2_taxonomy.json"))

    # --- Pass 3 ---
    if only_pass is None or only_pass == 3:
        if resume and os.path.exists(
            os.path.join(output_dir, "pass3_labeled_personas.json")
        ):
            print("Resuming: loading Pass 3 results from disk")
            labeled_personas = load_json(
                os.path.join(output_dir, "pass3_labeled_personas.json")
            )
        else:
            labeled_personas = run_pass3(personas, taxonomy, model, output_dir)
    else:
        return None

    # --- Assemble ---
    return assemble_agent_list(labeled_personas, taxonomy, output_dir)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Convert interview transcripts to AI agent personas using EDSL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full pipeline
  python transcript_to_persona.py --input-dir ./transcripts/ --output-dir ./personas/

  # Run only pass 1 (extraction)
  python transcript_to_persona.py --input-dir ./transcripts/ --output-dir ./personas/ --pass 1

  # Resume from where you left off
  python transcript_to_persona.py --input-dir ./transcripts/ --output-dir ./personas/ --resume

  # Use a different model
  python transcript_to_persona.py --input-dir ./transcripts/ --output-dir ./personas/ --model <model>
""",
    )
    parser.add_argument(
        "--input-dir", required=True, help="Directory containing .docx transcript files"
    )
    parser.add_argument(
        "--output-dir",
        default="./persona_output",
        help="Directory for output files (default: ./persona_output)",
    )
    parser.add_argument(
        "--model",
        required=True,
        help="LLM model to use. Required: no default, since a hardcoded one goes "
             "stale and would be used silently. Confirm a current name with "
             "ep models.",
    )
    parser.add_argument(
        "--pass",
        type=int,
        choices=[1, 2, 3],
        dest="only_pass",
        help="Run only a specific pass (1=extract, 2=taxonomy, 3=label)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from existing intermediate files",
    )

    args = parser.parse_args()

    run_pipeline(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        model_name=args.model,
        only_pass=args.only_pass,
        resume=args.resume,
    )


if __name__ == "__main__":
    main()
