"""
calibrate_agents.py
===================
Calibrate a **mixture of LLM agents** to match target response distributions.

Given empirical response frequencies (e.g., from a human experiment), this script
searches over a theory-constrained trait space to find a weighted combination of
agent personas whose blended distribution matches the data.

Methodology from: "General Social Agents" (Manning & Horton, arXiv:2508.17407)

Key idea: No single agent persona can reproduce an aggregate population
distribution (people are heterogeneous). Instead, we find mixture weights
w_1, ..., w_N over candidate agents such that sum(w_i * p_i) ≈ target.

Pipeline:
  Step 1: Build candidate agent grid from trait space (Cartesian product)
  Step 2: Get each agent's predicted distribution (logprobs OR repeated sampling)
  Step 3: Solve for optimal mixture weights (convex optimization)
  Step 4: Save mixture agents, weights, and diagnostics

Two modes for getting agent distributions (Step 2):
  --method logprobs   : One API call per agent. Requires use_code=True (single-
                        token response) and an OpenAI model. Fast and cheap but
                        only works when the response is a single token.
  --method sampling   : Run each agent n times (--n-samples). Works with any
                        model and any question type. More expensive but robust.

Outputs:
  - candidate_grid.ep            (full AgentList)
  - logprob_results.ep           (raw EDSL results, logprobs mode)
  - sampling_results.ep          (raw EDSL results, sampling mode)
  - agent_distributions.csv      (per-agent predicted distributions)
  - mixture_weights.csv          (agent names, weights, traits)
  - calibrated_mixture.ep        (AgentList of agents with nonzero weight)
  - calibration_summary.json     (metadata, fit diagnostics)

Usage:
  # Logprobs mode (fast, OpenAI + use_code only):
  python calibrate_agents.py \\
      --target-csv target.csv \\
      --trait-space-json trait_space.json \\
      --method logprobs --model <openai-model>   # logprobs is OpenAI-only

  # Repeated sampling mode (robust, any model):
  python calibrate_agents.py \\
      --target-csv target.csv \\
      --trait-space-json trait_space.json \\
      --method sampling --model <model> --n-samples 30
"""

import argparse
import csv
import itertools
import json
import math
import os
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

# ---------------------------------------------------------------------------
# Divergence metrics (for reporting, not optimization)
# ---------------------------------------------------------------------------

EPSILON = 1e-10


def kl_divergence(target: dict, predicted: dict, options: list) -> float:
    """D_KL(target || predicted)."""
    div = 0.0
    for opt in options:
        p = target.get(opt, 0.0)
        q = predicted.get(opt, EPSILON)
        if p > 0:
            div += p * math.log(p / max(q, EPSILON))
    return div


def total_variation(target: dict, predicted: dict, options: list) -> float:
    """0.5 * sum(|p - q|). Bounded [0, 1]."""
    return 0.5 * sum(
        abs(target.get(opt, 0.0) - predicted.get(opt, 0.0)) for opt in options
    )


def chi_squared(target: dict, predicted: dict, options: list) -> float:
    """sum((p - q)^2 / q)."""
    div = 0.0
    for opt in options:
        p = target.get(opt, 0.0)
        q = predicted.get(opt, EPSILON)
        div += (p - q) ** 2 / max(q, EPSILON)
    return div


METRICS = {"kl": kl_divergence, "tv": total_variation, "chi2": chi_squared}

# ---------------------------------------------------------------------------
# Step 1: Build candidate agent grid
# ---------------------------------------------------------------------------


def build_candidate_grid(
    trait_space: dict, max_candidates: int = 0
) -> "AgentList":
    """Build an AgentList from the Cartesian product of trait dimensions."""
    from edsl import Agent, AgentList

    dimensions = list(trait_space.keys())
    value_lists = [trait_space[dim] for dim in dimensions]

    combos = list(itertools.product(*value_lists))
    total_combos = len(combos)
    print(
        f"  Trait space: {' x '.join(str(len(v)) for v in value_lists)}"
        f" = {total_combos} combinations"
    )

    if max_candidates > 0 and total_combos > max_candidates:
        print(f"  Subsampling to {max_candidates} candidates (from {total_combos})")
        combos = random.sample(combos, max_candidates)

    agents = []
    for i, combo in enumerate(combos):
        traits = dict(zip(dimensions, combo))
        persona_parts = [str(v) for v in combo]
        traits["persona"] = (
            "You are a person who is " + ", ".join(persona_parts) + "."
        )
        agents.append(Agent(name=f"candidate_{i:04d}", traits=traits))

    agent_list = AgentList(agents)
    print(f"  Built {len(agent_list)} candidate agents")
    return agent_list


# ---------------------------------------------------------------------------
# Step 2a: Get distributions via logprobs (fast, single-token only)
# ---------------------------------------------------------------------------


def build_survey_from_target(target: dict) -> "Survey":
    """Build an EDSL Survey with one QuestionMultipleChoice per target question."""
    from edsl import QuestionMultipleChoice, Survey

    questions = []
    for qname, option_probs in target.items():
        options = list(option_probs.keys())
        q = QuestionMultipleChoice(
            question_name=qname,
            question_text=f"Which option do you choose? Options: {', '.join(options)}",
            question_options=options,
            use_code=True,
            include_comment=False,
        )
        questions.append(q)
    return Survey(questions)


def run_via_ep_cli(survey, agent_list, model, output_dir: str, stem: str,
                   description: str, n: int = 1):
    """Build, price, confirm, and run a saved Jobs object through the EP CLI."""
    from edsl import ModelList, Results

    survey_path = os.path.join(output_dir, f"{stem}_survey.ep")
    agents_path = os.path.join(output_dir, f"{stem}_agents.ep")
    models_path = os.path.join(output_dir, f"{stem}_models.ep")
    jobs_path = os.path.join(output_dir, f"{stem}_jobs.ep")
    results_path = os.path.join(output_dir, f"{stem}_results.ep")
    survey.git.save(survey_path)
    agent_list.git.save(agents_path)
    ModelList([model]).git.save(models_path)
    subprocess.run([
        "ep", "jobs", "build", "--survey", survey_path, "--agents", agents_path,
        "--models", models_path, "--output", jobs_path,
    ], check=True)
    subprocess.run(["ep", "jobs", "cost", jobs_path, "--iterations", str(n)], check=True)
    if input("Run this paid job? Type 'yes' to continue: ").strip().lower() != "yes":
        raise SystemExit(f"Run cancelled. Saved job: {jobs_path}")
    command = [
        "ep", "run", jobs_path,
        "--remote_inference_description", description,
        "--results_description", description,
        "--output", results_path,
    ]
    if n != 1:
        command.extend(["--n", str(n)])
    subprocess.run(command, check=True)
    return Results.git.load(results_path)


def run_logprobs_survey(survey, agent_list, model_name: str, output_dir: str):
    """Run survey once per agent with logprobs=True."""
    from edsl import Model

    model = Model(model_name, temperature=1, logprobs=True)
    description = f"Agent calibration logprobs - {len(agent_list)} agents"
    results = run_via_ep_cli(
        survey, agent_list, model, output_dir, "logprob", description
    )
    print(f"  Got {len(results)} results")
    return results


def extract_logprob_distributions(results, survey, target) -> dict:
    """Extract per-agent predicted distributions from logprobs results.

    Returns:
        Dict mapping agent_name -> {question_name -> {option: probability}}
    """
    question_meta = {}
    for q in survey.questions:
        qname = q.question_name
        if qname in target:
            question_meta[qname] = {
                "options_map": {str(i): label for i, label in enumerate(q.question_options)},
                "options_list": q.question_options,
            }

    agent_distributions = {}
    for i in range(len(results)):
        result = results[i]
        agent_obj = result["agent"]
        agent_name = agent_obj.name

        if agent_name in agent_distributions:
            continue  # already processed (multi-question surveys have one result per agent)

        dists = {}
        for qname, meta in question_meta.items():
            raw_key = f"{qname}_raw_model_response"
            raw = result["raw_model_response"][raw_key]
            top_logprobs = raw["choices"][0]["logprobs"]["content"][0]["top_logprobs"]

            predicted = {label: EPSILON for label in meta["options_map"].values()}
            for token_info in top_logprobs:
                label = meta["options_map"].get(token_info["token"])
                if label:
                    predicted[label] = math.exp(token_info["logprob"])

            # Normalize
            total_p = sum(predicted.values())
            predicted = {k: v / total_p for k, v in predicted.items()}
            dists[qname] = predicted

        agent_distributions[agent_name] = dists

    return agent_distributions


# ---------------------------------------------------------------------------
# Step 2b: Get distributions via repeated sampling (robust, any model)
# ---------------------------------------------------------------------------


def run_sampling_survey(survey, agent_list, model_name: str, n_samples: int,
                        output_dir: str):
    """Run survey n times per agent to get empirical frequencies."""
    from edsl import Model

    model = Model(model_name, temperature=1)
    description = f"Agent calibration sampling - {len(agent_list)} agents x {n_samples}"
    results = run_via_ep_cli(
        survey, agent_list, model, output_dir, "sampling", description, n_samples
    )
    print(f"  Got {len(results)} results")
    return results


def extract_sampling_distributions(results, survey, target) -> dict:
    """Extract per-agent distributions from repeated-sampling results.

    Counts answers across n repetitions and normalizes to frequencies.

    Returns:
        Dict mapping agent_name -> {question_name -> {option: probability}}
    """
    question_meta = {}
    for q in survey.questions:
        qname = q.question_name
        if qname in target:
            question_meta[qname] = q.question_options

    # Accumulate counts: agent_name -> question_name -> {option: count}
    counts = {}
    for i in range(len(results)):
        result = results[i]
        agent_obj = result["agent"]
        agent_name = agent_obj.name

        if agent_name not in counts:
            counts[agent_name] = {
                qname: {opt: 0 for opt in opts}
                for qname, opts in question_meta.items()
            }

        for qname in question_meta:
            answer = result["answer"][qname]
            if answer is not None and answer in counts[agent_name][qname]:
                counts[agent_name][qname][answer] += 1

    # Normalize to probabilities
    agent_distributions = {}
    for agent_name, q_counts in counts.items():
        dists = {}
        for qname, opt_counts in q_counts.items():
            total = sum(opt_counts.values())
            if total > 0:
                dists[qname] = {opt: c / total for opt, c in opt_counts.items()}
            else:
                # No valid answers -- uniform fallback
                n_opts = len(opt_counts)
                dists[qname] = {opt: 1.0 / n_opts for opt in opt_counts}
        agent_distributions[agent_name] = dists

    return agent_distributions


# ---------------------------------------------------------------------------
# Step 3: Mixture optimization
# ---------------------------------------------------------------------------


def optimize_mixture(
    agent_distributions: dict,
    target: dict,
    sparsity_penalty: float = 0.0,
) -> dict:
    """Find mixture weights that minimize total variation distance to target.

    Solves:  min_{w} 0.5 * sum |sum_i w_i * p_i(q,o) - target(q,o)|
             + sparsity_penalty * ||w||_1  (but sum(w)=1 so this = penalty)
    subject to: w_i >= 0, sum(w_i) = 1

    Since total variation of a mixture is convex in the weights, this is a
    well-behaved optimization problem.

    Args:
        agent_distributions: {agent_name -> {question_name -> {option: prob}}}
        target: {question_name -> {option: prob}}
        sparsity_penalty: L1 penalty to encourage sparse mixtures (optional).

    Returns:
        Dict with keys:
          - weights: {agent_name: weight} for agents with weight > 0.001
          - mixture_distribution: {question_name -> {option: prob}}
          - total_variation: TV distance of the mixture vs target
          - kl_divergence: KL divergence of mixture vs target
          - all_weights: full weight vector (for diagnostics)
    """
    agent_names = sorted(agent_distributions.keys())
    n_agents = len(agent_names)

    # Build flat target and distribution matrix
    # Columns: all (question, option) pairs
    col_labels = []
    target_vec = []
    for qname in sorted(target.keys()):
        for opt in sorted(target[qname].keys()):
            col_labels.append((qname, opt))
            target_vec.append(target[qname][opt])

    target_vec = np.array(target_vec)
    n_cols = len(col_labels)

    # Distribution matrix: rows = agents, cols = (question, option) probabilities
    P = np.zeros((n_agents, n_cols))
    for i, aname in enumerate(agent_names):
        dists = agent_distributions[aname]
        for j, (qname, opt) in enumerate(col_labels):
            P[i, j] = dists.get(qname, {}).get(opt, EPSILON)

    # Objective: minimize 0.5 * sum |P^T w - target|
    def objective(w):
        mixture = P.T @ w  # shape (n_cols,)
        return 0.5 * np.sum(np.abs(mixture - target_vec))

    # Constraints
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
    bounds = [(0.0, 1.0)] * n_agents

    # Initial guess: uniform
    w0 = np.ones(n_agents) / n_agents

    result = minimize(
        objective,
        w0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000, "ftol": 1e-12},
    )

    if not result.success:
        print(f"  WARNING: Optimization did not converge: {result.message}")

    w_opt = result.x

    # Compute mixture distribution
    mixture_vec = P.T @ w_opt
    mixture_dist = {}
    for j, (qname, opt) in enumerate(col_labels):
        if qname not in mixture_dist:
            mixture_dist[qname] = {}
        mixture_dist[qname][opt] = float(mixture_vec[j])

    # Compute fit metrics
    tv = 0.0
    kl = 0.0
    for qname in target:
        options = list(target[qname].keys())
        tv += total_variation(target[qname], mixture_dist[qname], options)
        kl += kl_divergence(target[qname], mixture_dist[qname], options)
    # Average across questions
    n_questions = len(target)
    tv /= n_questions
    kl /= n_questions

    # Extract nonzero weights
    threshold = 0.001
    nonzero = {
        agent_names[i]: float(w_opt[i])
        for i in range(n_agents)
        if w_opt[i] > threshold
    }

    print(f"  Mixture has {len(nonzero)} agents with weight > {threshold}")
    print(f"  Total variation (avg per question): {tv:.4f}")
    print(f"  KL divergence (avg per question):   {kl:.4f}")

    return {
        "weights": nonzero,
        "mixture_distribution": mixture_dist,
        "total_variation": tv,
        "kl_divergence": kl,
        "all_weights": {agent_names[i]: float(w_opt[i]) for i in range(n_agents)},
        "optimization_success": result.success,
        "optimization_message": result.message,
    }


# ---------------------------------------------------------------------------
# Individual agent scoring (retained for diagnostics)
# ---------------------------------------------------------------------------


def score_individual_agents(
    agent_distributions: dict,
    target: dict,
    metric_name: str,
) -> list:
    """Score each individual agent by divergence from target.

    Returns sorted list (best first) for diagnostic purposes.
    """
    metric_fn = METRICS[metric_name]
    scores = []

    for agent_name, dists in agent_distributions.items():
        per_q = {}
        for qname, target_dist in target.items():
            options = list(target_dist.keys())
            predicted = dists.get(qname, {opt: 1.0 / len(options) for opt in options})
            per_q[qname] = metric_fn(target_dist, predicted, options)

        aggregate = sum(per_q.values()) / len(per_q) if per_q else 0.0
        scores.append({
            "agent_name": agent_name,
            "aggregate_divergence": aggregate,
            "per_question_divergence": per_q,
            "per_question_predicted": dists,
        })

    scores.sort(key=lambda x: x["aggregate_divergence"])
    return scores


# ---------------------------------------------------------------------------
# Step 4: Save outputs
# ---------------------------------------------------------------------------


def save_outputs(
    mixture_result: dict,
    individual_scores: list,
    agent_list: "AgentList",
    agent_distributions: dict,
    target: dict,
    trait_space: dict,
    output_dir: str,
    args,
    elapsed: float,
):
    """Save mixture weights, agent distributions, and diagnostics."""
    from edsl import Agent, AgentList

    # --- Mixture weights CSV ---
    weights_path = os.path.join(output_dir, "mixture_weights.csv")
    dimensions = list(trait_space.keys())
    fieldnames = ["agent_name", "weight"] + dimensions

    # Get traits from the original agent list
    agent_traits = {}
    for agent in agent_list:
        traits = {}
        for k, v in agent.traits.items():
            if k != "persona":
                traits[k] = v
        agent_traits[agent.name] = traits

    with open(weights_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for aname, weight in sorted(
            mixture_result["weights"].items(), key=lambda x: -x[1]
        ):
            row = {"agent_name": aname, "weight": round(weight, 6)}
            row.update(agent_traits.get(aname, {}))
            writer.writerow(row)

    print(f"  Saved mixture weights to {weights_path}")

    # --- Mixture agents (AgentList with _weight in traits) ---
    # Uses underscore prefix (_weight) so EDSL does not render it in survey
    # prompts. The trait is available programmatically for weighted analysis.
    mixture_agents = []
    for agent in agent_list:
        weight = mixture_result["weights"].get(agent.name, 0.0)
        if weight > 0.001:
            new_traits = dict(agent.traits)
            new_traits["_weight"] = round(weight, 6)
            mixture_agents.append(Agent(name=agent.name, traits=new_traits))

    mixture_agent_list = AgentList(mixture_agents)
    mixture_path = os.path.join(output_dir, "calibrated_mixture.ep")
    mixture_agent_list.git.save(mixture_path)
    print(f"  Saved {len(mixture_agents)} mixture agents to {mixture_path}")

    # --- Agent distributions CSV ---
    dist_path = os.path.join(output_dir, "agent_distributions.csv")
    q_names = sorted(target.keys())
    dist_fields = ["agent_name"]
    for qname in q_names:
        for opt in sorted(target[qname].keys()):
            dist_fields.append(f"pred_{qname}_{opt}")
    dist_fields.extend(dimensions)

    with open(dist_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=dist_fields, extrasaction="ignore")
        writer.writeheader()
        for score_entry in individual_scores:
            aname = score_entry["agent_name"]
            row = {"agent_name": aname}
            for qname in q_names:
                predicted = score_entry.get("per_question_predicted", {}).get(qname, {})
                for opt in sorted(target[qname].keys()):
                    row[f"pred_{qname}_{opt}"] = round(predicted.get(opt, 0.0), 6)
            row.update(agent_traits.get(aname, {}))
            writer.writerow(row)

    print(f"  Saved agent distributions to {dist_path}")

    # --- Summary JSON ---
    summary = {
        "method": args.method,
        "model": args.model,
        "metric_for_individual_ranking": args.metric,
        "n_candidates": len(agent_distributions),
        "n_mixture_agents": len(mixture_result["weights"]),
        "mixture_total_variation": mixture_result["total_variation"],
        "mixture_kl_divergence": mixture_result["kl_divergence"],
        "best_individual_agent": individual_scores[0]["agent_name"],
        "best_individual_score": individual_scores[0]["aggregate_divergence"],
        "optimization_success": bool(mixture_result["optimization_success"]),
        "trait_space": trait_space,
        "target_questions": list(target.keys()),
        "elapsed_seconds": round(elapsed, 1),
    }
    if args.method == "sampling":
        summary["n_samples"] = args.n_samples

    # Add mixture distribution vs target comparison
    summary["fit"] = {}
    for qname in target:
        summary["fit"][qname] = {
            "target": target[qname],
            "mixture": mixture_result["mixture_distribution"][qname],
        }

    summary_path = os.path.join(output_dir, "calibration_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved summary to {summary_path}")


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def load_target_csv(path: str) -> dict:
    """Load target distribution CSV (question_name, option, probability)."""
    target = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            qname = row["question_name"].strip()
            option = row["option"].strip()
            prob = float(row["probability"])
            if qname not in target:
                target[qname] = {}
            target[qname][option] = prob

    for qname, dist in target.items():
        total = sum(dist.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(
                f"Probabilities for '{qname}' sum to {total:.4f}, expected ~1.0"
            )

    print(f"  Loaded target: {len(target)} question(s)")
    for qname, dist in target.items():
        opts_str = ", ".join(f"{opt}={p:.2f}" for opt, p in dist.items())
        print(f"    {qname}: {opts_str}")
    return target


def load_trait_space(path: str) -> dict:
    """Load trait space JSON: {"dim": ["val1", "val2", ...], ...}"""
    with open(path) as f:
        trait_space = json.load(f)

    total = 1
    for dim, values in trait_space.items():
        if not isinstance(values, list) or len(values) == 0:
            raise ValueError(f"Dimension '{dim}' must be a non-empty list")
        total *= len(values)

    print(f"  Loaded trait space: {len(trait_space)} dimensions, {total} combinations")
    for dim, values in trait_space.items():
        print(f"    {dim}: {values}")
    return trait_space


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args():
    parser = argparse.ArgumentParser(
        description="Calibrate a mixture of LLM agents to match target distributions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--target-csv", required=True)
    parser.add_argument("--trait-space-json", required=True)
    parser.add_argument("--survey-ep", dest="survey_ep", default=None,
                        help="Pre-built EDSL Survey (.ep)")
    parser.add_argument("--output-dir", default="./calibration_output")
    parser.add_argument(
        "--model", required=True,
        help="Model name, e.g. from ep models. Required: there "
             "is deliberately no default, since a hardcoded one goes stale and would "
             "be used silently. Note --method logprobs needs an OpenAI model.",
    )
    parser.add_argument(
        "--method", choices=["logprobs", "sampling"], default="logprobs",
        help="How to estimate each agent's distribution (default: logprobs)",
    )
    parser.add_argument(
        "--n-samples", type=int, default=30,
        help="Samples per agent in sampling mode (default: 30)",
    )
    parser.add_argument(
        "--metric", choices=list(METRICS.keys()), default="kl",
        help="Metric for ranking individual agents (default: kl)",
    )
    parser.add_argument("--top-k", type=int, default=5,
                        help="Show top-k individual agents in diagnostics")
    parser.add_argument("--max-candidates", type=int, default=0,
                        help="Subsample grid if > 0")
    return parser.parse_args()


def main():
    args = parse_args()
    start_time = time.time()

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # --- Load inputs ---
    print("\n=== Loading inputs ===")
    target = load_target_csv(args.target_csv)
    trait_space = load_trait_space(args.trait_space_json)

    # --- Load or build survey ---
    if args.survey_ep:
        from edsl import Survey
        print(f"\n=== Loading survey from {args.survey_ep} ===")
        survey = Survey.git.load(args.survey_ep)
        print(f"  {len(survey.questions)} question(s)")
    else:
        print("\n=== Building survey from target CSV ===")
        survey = build_survey_from_target(target)
        print(f"  {len(survey.questions)} question(s)")

    # --- Step 1: Build candidate grid ---
    grid_path = os.path.join(output_dir, "candidate_grid.ep")
    if os.path.exists(grid_path):
        from edsl import AgentList
        print(f"\n=== Step 1: Loading candidate grid from {grid_path} ===")
        agent_list = AgentList.git.load(grid_path)
        print(f"  {len(agent_list)} candidates")
    else:
        print("\n=== Step 1: Building candidate agent grid ===")
        agent_list = build_candidate_grid(trait_space, args.max_candidates)
        agent_list.git.save(os.path.join(output_dir, "candidate_grid.ep"))

    # --- Step 2: Get agent distributions ---
    if args.method == "logprobs":
        results_path = os.path.join(output_dir, "logprob_results.ep")
        if os.path.exists(results_path):
            from edsl import Results
            print(f"\n=== Step 2: Loading logprob results from {results_path} ===")
            results = Results.git.load(results_path)
        else:
            print(f"\n=== Step 2: Running logprobs survey ({args.model}) ===")
            results = run_logprobs_survey(survey, agent_list, args.model, output_dir)

        print("  Extracting distributions from logprobs...")
        agent_distributions = extract_logprob_distributions(results, survey, target)

    elif args.method == "sampling":
        results_path = os.path.join(output_dir, "sampling_results.ep")
        if os.path.exists(results_path):
            from edsl import Results
            print(f"\n=== Step 2: Loading sampling results from {results_path} ===")
            results = Results.git.load(results_path)
        else:
            print(f"\n=== Step 2: Running sampling survey ({args.model}, n={args.n_samples}) ===")
            results = run_sampling_survey(
                survey, agent_list, args.model, args.n_samples, output_dir
            )

        print("  Extracting distributions from sample counts...")
        agent_distributions = extract_sampling_distributions(results, survey, target)

    print(f"  Got distributions for {len(agent_distributions)} agents")

    # --- Step 3a: Individual agent scoring (diagnostic) ---
    print(f"\n=== Step 3a: Individual agent ranking ({args.metric}) ===")
    individual_scores = score_individual_agents(agent_distributions, target, args.metric)
    print(f"  Best individual:  {individual_scores[0]['agent_name']} "
          f"({args.metric}={individual_scores[0]['aggregate_divergence']:.4f})")
    print(f"  Worst individual: {individual_scores[-1]['agent_name']} "
          f"({args.metric}={individual_scores[-1]['aggregate_divergence']:.4f})")

    # --- Step 3b: Mixture optimization ---
    print(f"\n=== Step 3b: Optimizing mixture weights ===")
    mixture_result = optimize_mixture(agent_distributions, target)

    # Print mixture composition
    print("\n  Mixture composition:")
    for aname, weight in sorted(
        mixture_result["weights"].items(), key=lambda x: -x[1]
    ):
        # Find agent traits
        for agent in agent_list:
            if agent.name == aname:
                traits_str = ", ".join(
                    f"{k}={v}" for k, v in agent.traits.items() if k != "persona"
                )
                print(f"    {aname} (w={weight:.3f}): {traits_str}")
                break

    # Print fit
    print("\n  Mixture fit vs target:")
    for qname in sorted(target.keys()):
        print(f"    {qname}:")
        for opt in target[qname]:
            t = target[qname][opt]
            m = mixture_result["mixture_distribution"][qname][opt]
            print(f"      {opt}: target={t:.3f}  mixture={m:.3f}  diff={m-t:+.3f}")

    # --- Step 4: Save ---
    print(f"\n=== Step 4: Saving outputs ===")
    elapsed = time.time() - start_time
    save_outputs(
        mixture_result=mixture_result,
        individual_scores=individual_scores,
        agent_list=agent_list,
        agent_distributions=agent_distributions,
        target=target,
        trait_space=trait_space,
        output_dir=output_dir,
        args=args,
        elapsed=elapsed,
    )

    print(f"\n=== Done! ({elapsed:.1f}s) ===")


if __name__ == "__main__":
    main()
