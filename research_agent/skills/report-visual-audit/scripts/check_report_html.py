#!/usr/bin/env python3
"""Post-compilation preflight check for report.html.

Parses the compiled HTML and checks for silent rendering failures that
pandoc does not report as errors:

  1. Empty blockquotes (e.g., from [bracket]: "text" link-ref bug)
  2. Missing images (img src that doesn't resolve)
  3. Duplicate H1 headings (title appears twice)
  4. Uncaptioned figures (images not followed by Figure N: caption)
  5. Orphaned link-reference patterns in source markdown

Usage:
    python check_report_html.py --study-root /path/to/study
    python check_report_html.py                # defaults to cwd

Exit codes:
    0 — all checks pass
    1 — one or more errors found
"""

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class ReportHTMLChecker(HTMLParser):
    """Single-pass HTML parser that collects issues."""

    def __init__(self):
        super().__init__()
        self.issues: list[str] = []
        self._in_blockquote = False
        self._blockquote_depth = 0
        self._blockquote_text = ""
        self._h1_count = 0
        self._img_srcs: list[str] = []
        self._all_text_after_img: dict[int, str] = {}
        self._img_index = -1
        self._chars_since_img = 0

    def handle_starttag(self, tag, attrs):
        if tag == "blockquote":
            if self._blockquote_depth == 0:
                self._blockquote_text = ""
            self._blockquote_depth += 1
            self._in_blockquote = True
        elif tag == "h1":
            self._h1_count += 1
        elif tag == "img":
            attr_dict = dict(attrs)
            src = attr_dict.get("src", "")
            self._img_srcs.append(src)
            self._img_index = len(self._img_srcs) - 1
            self._chars_since_img = 0
            self._all_text_after_img[self._img_index] = ""

    def handle_endtag(self, tag):
        if tag == "blockquote":
            self._blockquote_depth -= 1
            if self._blockquote_depth == 0:
                self._in_blockquote = False
                stripped = self._blockquote_text.strip()
                if not stripped:
                    self.issues.append(
                        "ERROR  Empty blockquote detected — likely a "
                        "> [bracket]: \"text\" link-reference bug. "
                        "Use > **bold:** \"text\" instead."
                    )

    def handle_data(self, data):
        if self._in_blockquote:
            self._blockquote_text += data
        # Track text after most recent image (for caption detection)
        if self._img_index >= 0 and self._chars_since_img < 500:
            self._all_text_after_img[self._img_index] += data
            self._chars_since_img += len(data)

    def finalize(self, html_path: Path):
        """Run post-parse checks."""
        # Duplicate H1
        if self._h1_count > 1:
            self.issues.append(
                f"ERROR  {self._h1_count} H1 headings found — pandoc "
                f"generates one from title: frontmatter. Remove the "
                f"duplicate # heading from report.md body."
            )

        # Missing images
        writeup_dir = html_path.parent
        for src in self._img_srcs:
            if src.startswith("data:"):
                continue  # embedded image, skip
            img_path = writeup_dir / src
            if not img_path.exists():
                self.issues.append(
                    f"ERROR  Image not found: {src}"
                )

        # Uncaptioned figures
        figure_re = re.compile(r"Figure\s+\d+", re.IGNORECASE)
        for idx, text in self._all_text_after_img.items():
            src = self._img_srcs[idx]
            if src.startswith("data:"):
                continue
            # Check first 300 chars after the image for a Figure caption
            snippet = text[:300]
            if not figure_re.search(snippet):
                self.issues.append(
                    f"WARN   Image '{src}' may be missing a "
                    f"'Figure N:' caption within 2 lines."
                )


def check_source_markdown(md_path: Path) -> list[str]:
    """Check the source .md for known pandoc pitfalls."""
    issues = []
    if not md_path.exists():
        return issues

    lines = md_path.read_text().splitlines()
    # Pattern: blockquote line starting with [bracket text]:
    link_ref_in_bq = re.compile(r"^>\s*\[.+?\]\s*:")
    for i, line in enumerate(lines, 1):
        if link_ref_in_bq.match(line):
            issues.append(
                f"ERROR  Line {i}: Blockquote starts with "
                f"'> [text]:' — pandoc will parse this as a link "
                f"reference definition, producing an empty blockquote. "
                f"Use '> **text:**' instead."
            )
    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Post-compilation preflight check for report.html"
    )
    parser.add_argument(
        "--study-root", default=".",
        help="Path to the study root directory (default: cwd)"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    study = Path(args.study_root).resolve()
    html_path = study / "writeup" / "report.html"
    md_path = study / "writeup" / "report.md"

    if not html_path.exists():
        print(f"No report.html found at {html_path}")
        sys.exit(1)

    # Check compiled HTML
    checker = ReportHTMLChecker()
    checker.feed(html_path.read_text())
    checker.finalize(html_path)

    # Check source markdown
    md_issues = check_source_markdown(md_path)

    all_issues = checker.issues + md_issues
    errors = [i for i in all_issues if i.startswith("ERROR")]
    warnings = [i for i in all_issues if i.startswith("WARN")]

    print(f"Checking: {html_path}\n")

    if not all_issues:
        print("  All checks passed.\n")
    else:
        for issue in all_issues:
            print(f"  {issue}")
        print()

    print(
        f"Result: {len(errors)} error(s), {len(warnings)} warning(s)"
    )

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
