#!/usr/bin/env python3
"""Multi-persona iterative calibration with true holdout evaluation.

For each of 4 target personas:
1. Load gold standard answers from initial run.
2. Start with blank persona.
3. Run 8 calibration rounds using 10 calibration-pool questions.
4. After each round, also evaluate on 5 true-holdout questions
   (system sees the questions but NEVER the gold answers).
5. Save per-persona results to JSON.
"""
import ast
import json
import random
import subprocess
import sys
from pathlib import Path

from edsl import (
    Agent,
    AgentList,
    QuestionFreeText,
    Results,
    Scenario,
    ScenarioList,
    Survey,
)

# ---------- paths ----------
_STUDY_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_STUDY_ROOT / "edsl_jobs" / "job_a"))
from study_survey import (  # noqa: E402
    survey,
    questions,
    CALIBRATION_POOL_NAMES,
    TRUE_HOLDOUT_NAMES,
    STRUCTURED_CALIBRATION_NAMES,
)
from study_model_list import model_list  # noqa: E402
from study_agent_list import PERSONAS, BLANK_PERSONA  # noqa: E402

OUTPUT_DIR = _STUDY_ROOT / "data" / "cooked"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_ROUNDS = 8
TRAIN_SIZE = 5
SEED = 42

# ---------- question metadata ----------
ALL_QUESTION_NAMES = [q.question_name for q in questions]
QUESTION_TEXTS = {q.question_name: q.question_text for q in questions}
QUESTION_OPTIONS = {}
for q in questions:
    if hasattr(q, "question_options"):
        QUESTION_OPTIONS[q.question_name] = q.question_options

# All structured questions (calibration + holdout, excluding free text)
ALL_STRUCTURED = [
    qn for qn in ALL_QUESTION_NAMES if qn != "free_text_values"
]
_LOCAL_RUN_NUMBER = 0


def run_local_via_ep_cli(run_survey, stem, scenarios=None, agents=None):
    """Execute a local calibration job through the same saved-Jobs CLI path."""
    global _LOCAL_RUN_NUMBER
    _LOCAL_RUN_NUMBER += 1
    prefix = OUTPUT_DIR / f"{stem}_{_LOCAL_RUN_NUMBER:04d}"
    survey_path = str(prefix) + "_survey.ep"
    models_path = str(prefix) + "_models.ep"
    jobs_path = str(prefix) + "_jobs.ep"
    results_path = str(prefix) + "_results.ep"
    run_survey.git.save(survey_path)
    model_list.git.save(models_path)
    command = ["ep", "jobs", "build", "--survey", survey_path, "--models", models_path]
    if scenarios is not None:
        scenarios_path = str(prefix) + "_scenarios.ep"
        scenarios.git.save(scenarios_path)
        command.extend(["--scenarios", scenarios_path])
    if agents is not None:
        agents_path = str(prefix) + "_agents.ep"
        agents.git.save(agents_path)
        command.extend(["--agents", agents_path])
    command.extend(["--output", jobs_path])
    subprocess.run(command, check=True)
    subprocess.run(["ep", "run", jobs_path, "--local", "--output", results_path], check=True)
    return Results.git.load(results_path)


def load_gold_answers(persona_name, persona_text):
    """Load gold standard answers for a specific persona."""
    results = Results.git.load(str(_STUDY_ROOT / "data" / "initial_results.ep"))
    gold = {}
    for r in results:
        if r.sub_dicts["agent"]["persona"] == persona_text:
            for qname in ALL_QUESTION_NAMES:
                gold[qname] = r.sub_dicts["answer"][qname]
    if not gold:
        raise ValueError("Could not find persona " + persona_name + " in initial results")
    return gold


def run_survey_with_persona(persona_text):
    """Run the full 15-question survey with a given persona."""
    agent = Agent(name="calibrating", traits={"persona": persona_text})
    results = run_local_via_ep_cli(
        survey, "persona_survey", agents=AgentList([agent])
    )
    answers = {}
    for qname in ALL_QUESTION_NAMES:
        answers[qname] = results.select("answer." + qname).to_list()[0]
    return answers


def compute_accuracy(predicted, gold, question_set):
    """Compute accuracy on a given set of structured question names."""
    structured = [qn for qn in question_set if qn != "free_text_values"]
    matches = {}
    for qname in structured:
        matches[qname] = predicted.get(qname) == gold.get(qname)
    total = sum(matches.values())
    return {
        "per_question": matches,
        "correct": total,
        "total": len(structured),
    }


def judge_free_text(predicted_text, gold_text):
    """Use an LLM to judge semantic similarity of free-text responses."""
    judge_q = QuestionFreeText(
        question_name="judgment",
        question_text=(
            "You are evaluating whether two free-text responses express similar "
            "values and concerns. Rate on a scale of 1-5 where 1 means completely "
            "different themes and 5 means nearly identical themes and tone.\n\n"
            "Response A (gold standard): {{ scenario.gold_text }}\n\n"
            "Response B (candidate): {{ scenario.predicted_text }}\n\n"
            'Respond with ONLY a JSON object with keys "score" (integer 1-5) '
            'and "reasoning" (brief explanation).'
        ),
    )
    scenario = Scenario({"gold_text": gold_text, "predicted_text": predicted_text})
    judge_survey = Survey([judge_q])
    result = run_local_via_ep_cli(
        judge_survey, "free_text_judge", scenarios=ScenarioList([scenario])
    )
    raw = result.select("answer.judgment").to_list()[0]
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        try:
            parsed = ast.literal_eval(str(raw))
            if isinstance(parsed, dict):
                return parsed
        except (ValueError, SyntaxError):
            pass
        return {"score": None, "reasoning": str(raw)}


def build_calibration_prompt(current_persona, training_mismatches, holdout_questions):
    """Build the calibration prompt as a plain string (no Jinja2)."""
    mismatch_lines = []
    for m in training_mismatches:
        mismatch_lines.append(
            "- Question: \""
            + m["question_text"]
            + "\"\n"
            + "  Your persona answered: \""
            + str(m["predicted"])
            + "\"\n"
            + "  The true answer is: \""
            + str(m["gold"])
            + "\""
        )

    holdout_lines = []
    for h in holdout_questions:
        opts_str = ""
        if h.get("options"):
            opts_str = "\n  Options: " + str(h["options"])
        holdout_lines.append("- \"" + h["question_text"] + "\"" + opts_str)

    mismatch_block = (
        "\n".join(mismatch_lines)
        if mismatch_lines
        else "(All training questions were answered correctly.)"
    )
    holdout_block = "\n".join(holdout_lines)

    prompt = (
        "You are a persona engineer. Your job is to write a rich, detailed "
        "persona description for a survey respondent.\n\n"
        "Current persona: \""
        + current_persona
        + "\"\n\n"
        "This persona was asked several survey questions. "
        "Here is where it got answers WRONG:\n\n"
        + mismatch_block
        + "\n\n"
        "Now, the persona also needs to answer these HELD-OUT questions "
        "correctly (you do NOT know the correct answers -- your persona must "
        "have the right foundational traits to naturally produce correct "
        "answers):\n\n"
        + holdout_block
        + "\n\n"
        "Write a NEW, improved persona description (2-4 sentences) that:\n"
        "1. Has foundational demographic and personality traits that would "
        "naturally lead to the correct answers on the training questions "
        "shown above.\n"
        "2. Is general enough in its core traits that it would also answer "
        "the held-out questions authentically.\n"
        "3. Does NOT simply list the correct answers or memorize specific "
        "survey responses. Instead, describe WHO this person IS -- their "
        "background, worldview, values, and life circumstances.\n"
        "4. Builds on what was correct about the current persona and fixes "
        "what was wrong.\n\n"
        "Write ONLY the persona description, nothing else. Start with "
        '"You are...".'
    )
    return prompt


def propose_new_persona(current_persona, predicted, gold, train_qnames, holdout_qnames):
    """Use the LLM to propose a new persona based on training mismatches.

    Note: holdout_qnames here refers to the CALIBRATION holdout (within the
    10 calibration-pool questions), NOT the true holdout. The true holdout
    questions are also shown as additional held-out questions the persona
    must answer, but their gold answers are never revealed.
    """
    training_mismatches = []
    for qname in train_qnames:
        if predicted.get(qname) != gold.get(qname):
            training_mismatches.append(
                {
                    "question_text": QUESTION_TEXTS[qname],
                    "predicted": predicted.get(qname),
                    "gold": gold.get(qname),
                }
            )

    # Holdout = calibration holdout questions + true holdout questions
    # (all shown without answers)
    all_holdout_qnames = list(holdout_qnames) + TRUE_HOLDOUT_NAMES
    holdout_questions = []
    for qname in all_holdout_qnames:
        hq = {"question_text": QUESTION_TEXTS[qname]}
        if qname in QUESTION_OPTIONS:
            hq["options"] = QUESTION_OPTIONS[qname]
        holdout_questions.append(hq)

    prompt = build_calibration_prompt(
        current_persona, training_mismatches, holdout_questions
    )

    rewrite_q = QuestionFreeText(
        question_name="new_persona",
        question_text="{{ scenario.calibration_prompt }}",
    )
    scenario = Scenario({"calibration_prompt": prompt})
    rewrite_survey = Survey([rewrite_q])
    result = run_local_via_ep_cli(
        rewrite_survey, "persona_rewrite", scenarios=ScenarioList([scenario])
    )
    new_persona = result.select("answer.new_persona").to_list()[0]
    return new_persona.strip()


def calibrate_one_persona(persona_name, persona_text, gold, splits):
    """Run the full calibration loop for a single persona."""
    print("\n" + "=" * 60)
    print("PERSONA: " + persona_name)
    print("=" * 60)

    # Round 0: blank baseline
    print("\n--- Round 0: Blank persona baseline ---")
    current_persona = BLANK_PERSONA
    answers_r0 = run_survey_with_persona(current_persona)
    cal_acc_r0 = compute_accuracy(answers_r0, gold, STRUCTURED_CALIBRATION_NAMES)
    ho_acc_r0 = compute_accuracy(answers_r0, gold, TRUE_HOLDOUT_NAMES)
    ft_judge_r0 = judge_free_text(
        answers_r0.get("free_text_values", ""),
        gold.get("free_text_values", ""),
    )

    print(
        "Calibration accuracy: "
        + str(cal_acc_r0["correct"])
        + "/"
        + str(cal_acc_r0["total"])
    )
    print(
        "True holdout accuracy: "
        + str(ho_acc_r0["correct"])
        + "/"
        + str(ho_acc_r0["total"])
    )
    print("Free-text similarity: " + str(ft_judge_r0.get("score", "N/A")) + "/5")

    rounds_data = []
    rounds_data.append(
        {
            "round": 0,
            "persona": current_persona,
            "answers": answers_r0,
            "calibration_accuracy": cal_acc_r0,
            "holdout_accuracy": ho_acc_r0,
            "free_text_judge": ft_judge_r0,
        }
    )

    for round_num in range(1, NUM_ROUNDS + 1):
        print("\n--- Round " + str(round_num) + " ---")

        train_qnames, cal_holdout_qnames = splits[round_num - 1]
        print("  Train: " + str(train_qnames))
        print("  Cal holdout: " + str(cal_holdout_qnames))

        last_answers = rounds_data[-1]["answers"]

        # Propose new persona
        print("  Proposing new persona...")
        new_persona = propose_new_persona(
            current_persona, last_answers, gold, train_qnames, cal_holdout_qnames
        )
        print("  New persona: " + new_persona[:120] + "...")
        current_persona = new_persona

        # Run full survey
        print("  Running survey...")
        new_answers = run_survey_with_persona(current_persona)
        cal_acc = compute_accuracy(new_answers, gold, STRUCTURED_CALIBRATION_NAMES)
        ho_acc = compute_accuracy(new_answers, gold, TRUE_HOLDOUT_NAMES)
        ft_judge = judge_free_text(
            new_answers.get("free_text_values", ""),
            gold.get("free_text_values", ""),
        )

        print(
            "  Calibration accuracy: "
            + str(cal_acc["correct"])
            + "/"
            + str(cal_acc["total"])
        )
        print(
            "  True holdout accuracy: "
            + str(ho_acc["correct"])
            + "/"
            + str(ho_acc["total"])
        )
        print(
            "  Free-text similarity: "
            + str(ft_judge.get("score", "N/A"))
            + "/5"
        )

        # Per-question detail
        for qname in ALL_STRUCTURED:
            match = "OK" if new_answers[qname] == gold[qname] else "MISS"
            tag = "[HOLDOUT]" if qname in TRUE_HOLDOUT_NAMES else ""
            print(
                "    "
                + qname
                + ": "
                + str(new_answers[qname])
                + " (gold: "
                + str(gold[qname])
                + ") ["
                + match
                + "] "
                + tag
            )

        rounds_data.append(
            {
                "round": round_num,
                "persona": current_persona,
                "answers": new_answers,
                "calibration_accuracy": cal_acc,
                "holdout_accuracy": ho_acc,
                "free_text_judge": ft_judge,
                "train_questions": train_qnames,
                "cal_holdout_questions": cal_holdout_qnames,
            }
        )

    return rounds_data


def main():
    # Pre-generate train/holdout splits (same for all personas)
    rng = random.Random(SEED)
    splits = []
    for _ in range(NUM_ROUNDS):
        shuffled = STRUCTURED_CALIBRATION_NAMES.copy()
        rng.shuffle(shuffled)
        splits.append((shuffled[:TRAIN_SIZE], shuffled[TRAIN_SIZE:]))

    all_results = {}

    for persona_name, persona_text in PERSONAS.items():
        gold = load_gold_answers(persona_name, persona_text)

        print("\nGold standard for " + persona_name + ":")
        for qname in ALL_QUESTION_NAMES:
            val = gold[qname]
            if isinstance(val, str) and len(val) > 80:
                val = val[:80] + "..."
            print("  " + qname + ": " + str(val))

        rounds_data = calibrate_one_persona(
            persona_name, persona_text, gold, splits
        )
        all_results[persona_name] = rounds_data

    # Save all results
    output_path = OUTPUT_DIR / "calibration_all_personas.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print("\nSaved all calibration data to " + str(output_path))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for persona_name, rounds_data in all_results.items():
        print("\n" + persona_name + ":")
        for rd in rounds_data:
            r = rd["round"]
            cal = str(rd["calibration_accuracy"]["correct"]) + "/" + str(rd["calibration_accuracy"]["total"])
            ho = str(rd["holdout_accuracy"]["correct"]) + "/" + str(rd["holdout_accuracy"]["total"])
            ft = str(rd["free_text_judge"].get("score", "N/A"))
            print(
                "  Round "
                + str(r)
                + ": cal="
                + cal
                + " holdout="
                + ho
                + " free-text="
                + ft
                + "/5"
            )


if __name__ == "__main__":
    main()
