#!/usr/bin/env python3
"""Embed chat transcript HTML into a pandoc markdown report.

Usage:
    python embed_chat_in_report.py <chat.html> <report.md>

Replaces every ``<!-- CHAT_TRANSCRIPT -->`` marker in *report.md* with the
raw HTML content from *chat.html*.  The replacement is done in-place.

This is intended for the HTML build of the report.  For PDF output, keep a
markdown blockquote version of the transcript alongside the marker.
"""

import sys
from pathlib import Path

PLACEHOLDER = "<!-- CHAT_TRANSCRIPT -->"


def embed_chat(chat_html_path: str, report_md_path: str) -> int:
    """Replace CHAT_TRANSCRIPT placeholders in *report_md_path*.

    Returns the number of replacements made.
    """
    chat_html = Path(chat_html_path).read_text(encoding="utf-8")
    report = Path(report_md_path).read_text(encoding="utf-8")

    count = report.count(PLACEHOLDER)
    if count == 0:
        return 0

    updated = report.replace(PLACEHOLDER, chat_html)
    Path(report_md_path).write_text(updated, encoding="utf-8")
    return count


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} <chat.html> <report.md>",
            file=sys.stderr,
        )
        sys.exit(1)

    chat_path = sys.argv[1]
    report_path = sys.argv[2]

    if not Path(chat_path).exists():
        print(f"Error: {chat_path} not found", file=sys.stderr)
        sys.exit(1)
    if not Path(report_path).exists():
        print(f"Error: {report_path} not found", file=sys.stderr)
        sys.exit(1)

    n = embed_chat(chat_path, report_path)
    if n == 0:
        print(
            f"Warning: no '{PLACEHOLDER}' marker found in {report_path}",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        print(f"Replaced {n} placeholder(s) in {report_path}")
