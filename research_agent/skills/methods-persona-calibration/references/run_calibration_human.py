#!/usr/bin/env python3
"""Persona calibration for real human respondents from Prolific.

For each of N human respondents:
1. Load their survey answers as gold standard.
2. Start with blank persona.
3. Run calibration rounds using 10 calibration-pool questions.
4. After each round, evaluate on 5 true-holdout questions
   (system never sees the human's holdout answers).
5. Save per-respondent results to JSON.
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

OUTPUT_DIR = _STUDY_ROOT / "data" / "cooked"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HUMAN_RESULTS_PATH = _STUDY_ROOT / "refs" / "study_d" / "data" / "human_results.ep"

NUM_ROUNDS = 5
TRAIN_SIZE = 5
SEED = 42
BLANK_PERSONA = "You are a person."

# ---------- question metadata ----------
ALL_QUESTION_NAMES = [q.question_name for q in questions]
QUESTION_TEXTS = {q.question_name: q.question_text for q in questions}
QUESTION_OPTIONS = {}
for q in questions:
    if hasattr(q, "question_options"):
        QUESTION_OPTIONS[q.question_name] = q.question_options

ALL_STRUCTURED = [qn for qn in ALL_QUESTION_NAMES if qn != "free_text_values"]
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


def load_human_respondents():
    """Load all human respondents and their answers."""
    results = Results.git.load(str(HUMAN_RESULTS_PATH))
    respondents = []
    for i, r in enumerate(results):
        answers = {}
        for qname in ALL_QUESTION_NAMES:
            answers[qname] = r.sub_dicts["answer"][qname]
        respondents.append({
            "id": "respondent_" + str(i + 1).zfill(2),
            "answers": answers,
        })
    return respondents


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
        "persona description for a real survey respondent.\n\n"
        "Current persona: \""
        + current_persona
        + "\"\n\n"
        "This persona was asked several survey questions. "
        "Here is where it got answers WRONG compared to the real person:\n\n"
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


def propose_new_persona(current_persona, predicted, gold, train_qnames, cal_holdout_qnames):
    """Use the LLM to propose a new persona based on training mismatches."""
    training_mismatches = []
    for qname in train_qnames:
        if predicted.get(qname) != gold.get(qname):
            training_mismatches.append({
                "question_text": QUESTION_TEXTS[qname],
                "predicted": predicted.get(qname),
                "gold": gold.get(qname),
            })

    # Show calibration holdout questions (not true holdout -- study_c showed no benefit)
    holdout_questions = []
    for qname in cal_holdout_qnames:
        hq = {"question_text": QUESTION_TEXTS[qname]}
        if qname in QUESTION_OPTIONS:
            hq["options"] = QUESTION_OPTIONS[qname]
        holdout_questions.append(hq)

    prompt = build_calibration_prompt(current_persona, training_mismatches, holdout_questions)

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


def calibrate_one_respondent(respondent_id, gold, splits):
    """Run the full calibration loop for a single human respondent."""
    print("\n" + "=" * 60)
    print("RESPONDENT: " + respondent_id)
    print("=" * 60)

    # Round 0: blank baseline
    print("  Round 0: blank baseline...")
    current_persona = BLANK_PERSONA
    answers_r0 = run_survey_with_persona(current_persona)
    cal_acc_r0 = compute_accuracy(answers_r0, gold, STRUCTURED_CALIBRATION_NAMES)
    ho_acc_r0 = compute_accuracy(answers_r0, gold, TRUE_HOLDOUT_NAMES)
    ft_judge_r0 = judge_free_text(
        answers_r0.get("free_text_values", ""),
        gold.get("free_text_values", ""),
    )
    print(
        "    cal=" + str(cal_acc_r0["correct"]) + "/" + str(cal_acc_r0["total"])
        + " holdout=" + str(ho_acc_r0["correct"]) + "/" + str(ho_acc_r0["total"])
        + " ft=" + str(ft_judge_r0.get("score", "N/A")) + "/5"
    )

    rounds_data = [{
        "round": 0,
        "persona": current_persona,
        "answers": answers_r0,
        "calibration_accuracy": cal_acc_r0,
        "holdout_accuracy": ho_acc_r0,
        "free_text_judge": ft_judge_r0,
    }]

    for round_num in range(1, NUM_ROUNDS + 1):
        train_qnames, cal_holdout_qnames = splits[round_num - 1]
        last_answers = rounds_data[-1]["answers"]

        # Propose new persona
        new_persona = propose_new_persona(
            current_persona, last_answers, gold, train_qnames, cal_holdout_qnames
        )
        current_persona = new_persona

        # Run survey
        new_answers = run_survey_with_persona(current_persona)
        cal_acc = compute_accuracy(new_answers, gold, STRUCTURED_CALIBRATION_NAMES)
        ho_acc = compute_accuracy(new_answers, gold, TRUE_HOLDOUT_NAMES)
        ft_judge = judge_free_text(
            new_answers.get("free_text_values", ""),
            gold.get("free_text_values", ""),
        )

        print(
            "  Round " + str(round_num)
            + ": cal=" + str(cal_acc["correct"]) + "/" + str(cal_acc["total"])
            + " holdout=" + str(ho_acc["correct"]) + "/" + str(ho_acc["total"])
            + " ft=" + str(ft_judge.get("score", "N/A")) + "/5"
            + "  persona: " + new_persona[:80] + "..."
        )

        rounds_data.append({
            "round": round_num,
            "persona": current_persona,
            "answers": new_answers,
            "calibration_accuracy": cal_acc,
            "holdout_accuracy": ho_acc,
            "free_text_judge": ft_judge,
            "train_questions": train_qnames,
            "cal_holdout_questions": cal_holdout_qnames,
        })

    return rounds_data


def main():
    # Pre-generate splits
    rng = random.Random(SEED)
    splits = []
    for _ in range(NUM_ROUNDS):
        shuffled = STRUCTURED_CALIBRATION_NAMES.copy()
        rng.shuffle(shuffled)
        splits.append((shuffled[:TRAIN_SIZE], shuffled[TRAIN_SIZE:]))

    # Load human respondents
    respondents = load_human_respondents()
    print("Loaded " + str(len(respondents)) + " human respondents")

    all_results = {}
    for resp in respondents:
        rid = resp["id"]
        gold = resp["answers"]
        rounds_data = calibrate_one_respondent(rid, gold, splits)
        all_results[rid] = rounds_data

        # Save incrementally in case of crash
        output_path = OUTPUT_DIR / "calibration_human.json"
        with open(output_path, "w") as f:
            json.dump(all_results, f, indent=2)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    # Aggregate stats
    for rnd in range(NUM_ROUNDS + 1):
        cal_total = sum(
            all_results[rid][rnd]["calibration_accuracy"]["correct"]
            for rid in all_results
        )
        cal_possible = sum(
            all_results[rid][rnd]["calibration_accuracy"]["total"]
            for rid in all_results
        )
        ho_total = sum(
            all_results[rid][rnd]["holdout_accuracy"]["correct"]
            for rid in all_results
        )
        ho_possible = sum(
            all_results[rid][rnd]["holdout_accuracy"]["total"]
            for rid in all_results
        )
        cal_pct = round(cal_total / cal_possible * 100, 1) if cal_possible > 0 else 0
        ho_pct = round(ho_total / ho_possible * 100, 1) if ho_possible > 0 else 0
        print(
            "Round " + str(rnd)
            + ": cal=" + str(cal_total) + "/" + str(cal_possible) + " (" + str(cal_pct) + "%)"
            + " holdout=" + str(ho_total) + "/" + str(ho_possible) + " (" + str(ho_pct) + "%)"
        )

    print("\nSaved to " + str(OUTPUT_DIR / "calibration_human.json"))


if __name__ == "__main__":
    main()
