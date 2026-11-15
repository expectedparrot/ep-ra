#!/usr/bin/env python3
"""Export named QuestionInterview transcripts from native saved EDSL Results."""

import argparse
import json
from pathlib import Path
import re
import string
import sys


def normalize_transcript(answer):
    """Preserve turn order, including turns without textual content."""
    if not isinstance(answer, list):
        raise ValueError("Expected a native list of interview turns; do not parse serialized text")
    turns = []
    for index, turn in enumerate(answer):
        if not isinstance(turn, dict):
            raise ValueError(f"Interview turn {index} must be a dictionary")
        blocks = turn.get("content") or []
        if not isinstance(blocks, list):
            raise ValueError(f"Interview turn {index} content must be a list")
        turns.append({
            "turn_index": index,
            "role": turn.get("role", "unknown"),
            "text": "\n".join(
                block["text"] for block in blocks
                if isinstance(block, dict) and block.get("type") == "text"
                and isinstance(block.get("text"), str)
            ),
        })
    return turns


def extract_interviews(results, question, agents=(), traits=()):
    wanted = set(agents)
    found = set()
    records = []
    for result in results:
        name = result.agent.name
        if wanted and name not in wanted:
            continue
        if question not in result.answer:
            raise ValueError(f"Question {question!r} missing for agent {name!r}")
        records.append({
            "agent_name": name,
            "agent_traits": {key: result.agent.traits.get(key) for key in traits},
            "question_name": question,
            "model": result.model.model,
            "inference_service": result.model._inference_service_,
            "iteration": result["iteration"],
            "turns": normalize_transcript(result.answer[question]),
        })
        found.add(name)
    if wanted - found:
        raise ValueError(f"Requested agents not found: {', '.join(sorted(wanted - found))}")
    if not records:
        raise ValueError("No interview results matched")
    return records


def markdown_inline(value):
    """Keep labels on one line and render Markdown punctuation literally."""
    text = " ".join(str(value).splitlines())
    return re.sub(f"([{re.escape(string.punctuation)}])", r"\\\1", text)


def markdown_block(text, language="text"):
    """Choose a fence that cannot be closed by the quoted content."""
    fence = "`" * max(3, 1 + max((len(run) for run in re.findall(r"`+", text)), default=0))
    return f"{fence}{language}\n{text}\n{fence}\n"


def render(records, output_format):
    if output_format == "jsonl":
        return "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    sections = []
    for record in records:
        sections.append(f"## {markdown_inline(record['agent_name'])} — {markdown_inline(record['question_name'])}\n")
        metadata = {key: value for key, value in record.items() if key != "turns"}
        sections.append(markdown_block(json.dumps(metadata, ensure_ascii=False), "json"))
        for turn in record["turns"]:
            sections.append(f"**{turn['turn_index']} · {markdown_inline(turn['role'])}**\n")
            sections.append(markdown_block(turn["text"]))
    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("--question", required=True)
    parser.add_argument("--agent", action="append", default=[])
    parser.add_argument("--agent-trait", action="append", default=[])
    parser.add_argument("--format", choices=("jsonl", "markdown"), default="jsonl")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    from edsl import Results

    try:
        records = extract_interviews(
            Results.load(str(args.results)), args.question, args.agent, args.agent_trait,
        )
        output = render(records, args.format)
    except (ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
