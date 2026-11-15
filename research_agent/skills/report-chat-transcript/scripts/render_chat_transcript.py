#!/usr/bin/env python3
"""Render simulation dialogue turns as chat-bubble HTML.

Usage:
    python render_chat_transcript.py path/to/sim_log.json [output.html]

The output is a self-contained HTML snippet (divs with inline styles) that
can be viewed standalone or embedded as raw HTML in a pandoc markdown report.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Turn extraction
# ---------------------------------------------------------------------------

def extract_turns_from_log(log_path: str) -> list[tuple[str, str, dict]]:
    """Read a Concordia simulation JSON log and extract dialogue turns.

    Returns a list of (speaker, message, metadata) tuples.  *metadata* may
    contain keys like ``phase``, ``step``, and ``timestamp``.

    The function uses regex matching on action summaries and does **not**
    require the concordia package.
    """
    with open(log_path, "r", encoding="utf-8") as f:
        log_data = json.load(f)

    turns: list[tuple[str, str, dict]] = []

    # Concordia logs come in several shapes.  We try the most common ones.
    entries = []
    if isinstance(log_data, list):
        entries = log_data
    elif isinstance(log_data, dict):
        # Try common top-level keys
        for key in ("entries", "log", "actions", "events", "data"):
            if key in log_data and isinstance(log_data[key], list):
                entries = log_data[key]
                break
        if not entries:
            # Fallback: flatten all list values
            for v in log_data.values():
                if isinstance(v, list):
                    entries = v
                    break

    # Patterns for extracting speaker and message from action strings
    # e.g. "Alice said: Hello there" or "Bob: I agree"
    say_patterns = [
        re.compile(r"^(.+?)\s+said[:\s]+(.+)$", re.DOTALL),
        re.compile(r"^(.+?)\s+says[:\s]+(.+)$", re.DOTALL),
        re.compile(r"^(.+?):\s+(.+)$", re.DOTALL),
    ]

    for entry in entries:
        speaker = None
        message = None
        metadata: dict[str, Any] = {}

        if isinstance(entry, str):
            text = entry
        elif isinstance(entry, dict):
            # Pull metadata fields
            for mkey in ("phase", "step", "timestamp", "time", "round"):
                if mkey in entry:
                    metadata[mkey] = entry[mkey]

            # Find the text payload
            text = ""
            for tkey in ("action", "text", "summary", "content", "message",
                         "utterance", "description"):
                if tkey in entry and isinstance(entry[tkey], str):
                    text = entry[tkey]
                    break

            # Some logs have explicit speaker fields
            for skey in ("speaker", "agent", "actor", "name", "player"):
                if skey in entry and isinstance(entry[skey], str):
                    speaker = entry[skey]
                    break

            if speaker and text:
                message = text
        else:
            continue

        # If we don't have speaker/message yet, try regex on text
        if message is None:
            text_to_parse = text if isinstance(entry, str) else text
            for pat in say_patterns:
                m = pat.match(text_to_parse.strip())
                if m:
                    speaker = m.group(1).strip()
                    message = m.group(2).strip()
                    break

        if speaker and message:
            turns.append((speaker, message, metadata))

    return turns


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

_DEFAULT_COLORS = {
    "left_bg": "#dbeafe",       # light blue
    "left_name": "#1e40af",     # dark blue
    "right_bg": "#fee2e2",      # light coral/pink
    "right_name": "#b91c1c",    # dark red
    "phase_line": "#9ca3af",    # gray-400
    "annotation": "#6b7280",    # gray-500
    "container_bg": "#f9fafb",  # gray-50
}


def render_transcript_html(
    turns: list[tuple[str, str, dict]],
    output_path: str | None = None,
    *,
    left_speaker: str | None = None,
    colors: dict[str, str] | None = None,
    title: str | None = None,
) -> str:
    """Render dialogue turns as chat-bubble HTML.

    Parameters
    ----------
    turns : list of (speaker, message, metadata) tuples
    output_path : optional file path to write the HTML to
    left_speaker : name of the speaker whose bubbles appear on the left.
        If *None*, the first speaker encountered is placed on the left.
    colors : optional dict overriding keys from ``_DEFAULT_COLORS``
    title : optional title displayed above the chat container

    Returns
    -------
    str : the HTML snippet
    """
    c = {**_DEFAULT_COLORS, **(colors or {})}

    # Determine left speaker
    if left_speaker is None and turns:
        left_speaker = turns[0][0]

    # Build bubble HTML
    bubbles: list[str] = []
    last_phase = None

    for speaker, message, meta in turns:
        # Phase divider
        phase = meta.get("phase")
        if phase and phase != last_phase:
            bubbles.append(
                f'<div style="display:flex;align-items:center;margin:18px 0 10px 0;">'
                f'<div style="flex:1;height:1px;background:{c["phase_line"]};"></div>'
                f'<span style="padding:0 12px;font-size:12px;color:{c["phase_line"]};'
                f'font-family:system-ui,sans-serif;white-space:nowrap;">{_esc(phase)}</span>'
                f'<div style="flex:1;height:1px;background:{c["phase_line"]};"></div>'
                f'</div>'
            )
            last_phase = phase

        is_left = (speaker == left_speaker)

        bg = c["left_bg"] if is_left else c["right_bg"]
        name_color = c["left_name"] if is_left else c["right_name"]
        align = "flex-start" if is_left else "flex-end"
        text_align = "left" if is_left else "right"
        radius = "18px 18px 18px 4px" if is_left else "18px 18px 4px 18px"

        # Annotation line (step, timestamp, etc.)
        annotation_parts = []
        for akey in ("step", "round", "timestamp", "time"):
            if akey in meta:
                annotation_parts.append(f"{akey}: {meta[akey]}")
        annotation_html = ""
        if annotation_parts:
            annotation_text = _esc(" | ".join(annotation_parts))
            annotation_html = (
                f'<div style="font-size:11px;color:{c["annotation"]};'
                f'margin-top:4px;font-family:system-ui,sans-serif;">'
                f'{annotation_text}</div>'
            )

        bubble = (
            f'<div style="display:flex;justify-content:{align};margin-bottom:12px;">'
            f'<div style="max-width:70%;text-align:{text_align};">'
            f'<div style="font-size:12px;font-weight:700;color:{name_color};'
            f'margin-bottom:2px;font-family:system-ui,sans-serif;">{_esc(speaker)}</div>'
            f'<div style="background:{bg};padding:10px 14px;border-radius:{radius};'
            f'font-size:14px;line-height:1.45;font-family:system-ui,sans-serif;'
            f'color:#1f2937;">{_esc(message)}</div>'
            f'{annotation_html}'
            f'</div></div>'
        )
        bubbles.append(bubble)

    title_html = ""
    if title:
        title_html = (
            f'<div style="font-size:16px;font-weight:700;margin-bottom:14px;'
            f'font-family:system-ui,sans-serif;color:#374151;">{_esc(title)}</div>'
        )

    html = (
        f'<div style="background:{c["container_bg"]};border:1px solid #e5e7eb;'
        f'border-radius:12px;padding:20px;max-width:640px;margin:24px auto;'
        f'font-family:system-ui,sans-serif;">\n'
        f'{title_html}\n'
        + "\n".join(bubbles)
        + "\n</div>\n"
    )

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    return html


def _esc(text: str) -> str:
    """Minimal HTML escaping."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <log.json> [output.html]", file=sys.stderr)
        sys.exit(1)

    log_path = sys.argv[1]
    turns = extract_turns_from_log(log_path)

    if not turns:
        print(f"No dialogue turns found in {log_path}", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
    else:
        base = os.path.splitext(log_path)[0]
        out_path = f"{base}_chat.html"

    html = render_transcript_html(turns, out_path)
    print(f"Wrote {len(turns)} turns to {out_path}")
