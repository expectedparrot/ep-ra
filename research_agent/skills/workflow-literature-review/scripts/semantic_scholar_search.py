#!/usr/bin/env python3
"""
Search Semantic Scholar for academic papers.

Calls the free Semantic Scholar Graph API. For higher rate limits, set
SEMANTIC_SCHOLAR_API_KEY in your environment (free key at
https://www.semanticscholar.org/product/api).

Usage:
    # Keyword search
    python semantic_scholar_search.py "willingness to pay privacy" --limit 10

    # Filter by year range
    python semantic_scholar_search.py "conjoint analysis" --year-start 2018 --year-end 2024

    # Include fields of study filter
    python semantic_scholar_search.py "LLM survey" --fields-of-study "Computer Science"

    # Get details for a specific paper by Semantic Scholar ID
    python semantic_scholar_search.py --paper-id "649def34f8be52c8b66281af98ae884c09aef38b"

    # Get papers that cite a specific paper
    python semantic_scholar_search.py --citations "649def34f8be52c8b66281af98ae884c09aef38b" --limit 20

    # CSV output (easy to paste into a review spreadsheet)
    python semantic_scholar_search.py "choice experiment" --format csv

Output formats: text (default), json, csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://api.semanticscholar.org/graph/v1"

# Fields requested for each paper result
PAPER_FIELDS = ",".join([
    "paperId",
    "externalIds",
    "url",
    "title",
    "abstract",
    "venue",
    "year",
    "referenceCount",
    "citationCount",
    "influentialCitationCount",
    "isOpenAccess",
    "openAccessPdf",
    "fieldsOfStudy",
    "publicationTypes",
    "publicationDate",
    "authors",
])


def _get_headers() -> dict[str, str]:
    headers: dict[str, str] = {"Accept": "application/json"}
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def _fetch(url: str, retries: int = 3) -> Any:
    headers = _get_headers()
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 * (attempt + 1)
                print(f"Rate limited — waiting {wait}s (attempt {attempt + 1}/{retries})", file=sys.stderr)
                time.sleep(wait)
            elif e.code == 404:
                print(f"Not found: {url}", file=sys.stderr)
                return None
            else:
                raise
    print(f"Failed after {retries} attempts: {url}", file=sys.stderr)
    return None


def search_papers(
    query: str,
    limit: int = 10,
    offset: int = 0,
    year_start: int | None = None,
    year_end: int | None = None,
    fields_of_study: str | None = None,
) -> list[dict]:
    """Search for papers by keyword query."""
    params: dict[str, str] = {
        "query": query,
        "limit": str(min(limit, 100)),
        "offset": str(offset),
        "fields": PAPER_FIELDS,
    }
    if year_start or year_end:
        lo = str(year_start) if year_start else ""
        hi = str(year_end) if year_end else ""
        params["year"] = f"{lo}-{hi}"
    if fields_of_study:
        params["fieldsOfStudy"] = fields_of_study

    url = f"{BASE_URL}/paper/search?{urllib.parse.urlencode(params)}"
    data = _fetch(url)
    if data is None:
        return []
    return data.get("data", [])


def get_paper(paper_id: str) -> dict | None:
    """Fetch full details for a single paper by its Semantic Scholar ID or DOI."""
    # Accept DOI format: prepend DOI: prefix if it looks like a DOI
    if paper_id.startswith("10."):
        paper_id = f"DOI:{paper_id}"
    url = f"{BASE_URL}/paper/{urllib.parse.quote(paper_id)}?fields={PAPER_FIELDS}"
    return _fetch(url)


def get_citations(paper_id: str, limit: int = 20) -> list[dict]:
    """Fetch papers that cite the given paper."""
    if paper_id.startswith("10."):
        paper_id = f"DOI:{paper_id}"
    fields = "title,authors,year,citationCount,url,externalIds,abstract,venue"
    params = {"fields": fields, "limit": str(min(limit, 1000))}
    url = f"{BASE_URL}/paper/{urllib.parse.quote(paper_id)}/citations?{urllib.parse.urlencode(params)}"
    data = _fetch(url)
    if data is None:
        return []
    # The citations endpoint returns {"data": [{"citingPaper": {...}}, ...]}
    return [item.get("citingPaper", {}) for item in data.get("data", [])]


def get_references(paper_id: str, limit: int = 20) -> list[dict]:
    """Fetch papers referenced by the given paper."""
    if paper_id.startswith("10."):
        paper_id = f"DOI:{paper_id}"
    fields = "title,authors,year,citationCount,url,externalIds,abstract,venue"
    params = {"fields": fields, "limit": str(min(limit, 1000))}
    url = f"{BASE_URL}/paper/{urllib.parse.quote(paper_id)}/references?{urllib.parse.urlencode(params)}"
    data = _fetch(url)
    if data is None:
        return []
    return [item.get("citedPaper", {}) for item in data.get("data", [])]


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _author_str(authors: list[dict]) -> str:
    names = [a.get("name", "") for a in (authors or [])]
    if len(names) > 3:
        return f"{names[0]} et al."
    return ", ".join(names)


def _doi(paper: dict) -> str:
    return (paper.get("externalIds") or {}).get("DOI", "")


def _open_access_url(paper: dict) -> str:
    pdf = paper.get("openAccessPdf")
    if pdf and isinstance(pdf, dict):
        return pdf.get("url", "")
    return ""


def format_text(papers: list[dict]) -> str:
    lines = []
    for i, p in enumerate(papers, 1):
        doi = _doi(p)
        oa = _open_access_url(p)
        lines.append(f"[{i}] {p.get('title', '(no title)')}")
        lines.append(f"    Authors : {_author_str(p.get('authors', []))}")
        lines.append(f"    Year    : {p.get('year', '?')}")
        lines.append(f"    Venue   : {p.get('venue') or '—'}")
        lines.append(f"    Citations: {p.get('citationCount', 0)}")
        if doi:
            lines.append(f"    DOI     : {doi}")
        lines.append(f"    S2 URL  : {p.get('url', '')}")
        if oa:
            lines.append(f"    Open Access PDF: {oa}")
        if p.get("abstract"):
            abstract = p["abstract"]
            if len(abstract) > 300:
                abstract = abstract[:300].rstrip() + "…"
            lines.append(f"    Abstract: {abstract}")
        fields = p.get("fieldsOfStudy") or []
        if fields:
            lines.append(f"    Fields  : {', '.join(fields)}")
        lines.append("")
    return "\n".join(lines)


def format_csv(papers: list[dict]) -> str:
    import io
    buf = io.StringIO()
    fieldnames = ["title", "authors", "year", "venue", "citationCount",
                  "doi", "url", "open_access_pdf", "abstract", "fields_of_study",
                  "semantic_scholar_id"]
    writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for p in papers:
        writer.writerow({
            "title": p.get("title", ""),
            "authors": _author_str(p.get("authors", [])),
            "year": p.get("year", ""),
            "venue": p.get("venue", ""),
            "citationCount": p.get("citationCount", 0),
            "doi": _doi(p),
            "url": p.get("url", ""),
            "open_access_pdf": _open_access_url(p),
            "abstract": (p.get("abstract") or "").replace("\n", " "),
            "fields_of_study": ", ".join(p.get("fieldsOfStudy") or []),
            "semantic_scholar_id": p.get("paperId", ""),
        })
    return buf.getvalue()


def format_json(papers: list[dict]) -> str:
    return json.dumps(papers, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search Semantic Scholar for academic papers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    # Main mode: keyword search vs. direct paper lookup vs. citations
    group = parser.add_mutually_exclusive_group()
    group.add_argument("query", nargs="?", help="Keyword search query")
    group.add_argument("--paper-id", metavar="ID",
                       help="Fetch a single paper by Semantic Scholar ID or DOI (e.g. 10.1145/...)")
    group.add_argument("--citations", metavar="ID",
                       help="Fetch papers that CITE the given paper ID or DOI")
    group.add_argument("--references", metavar="ID",
                       help="Fetch papers REFERENCED BY the given paper ID or DOI")

    parser.add_argument("--limit", type=int, default=10,
                        help="Maximum number of results (default: 10, max: 100)")
    parser.add_argument("--offset", type=int, default=0,
                        help="Result offset for pagination (default: 0)")
    parser.add_argument("--year-start", type=int, metavar="YEAR",
                        help="Filter: earliest publication year")
    parser.add_argument("--year-end", type=int, metavar="YEAR",
                        help="Filter: latest publication year")
    parser.add_argument("--fields-of-study", metavar="FIELD",
                        help='Filter by field (e.g. "Computer Science", "Economics")')
    parser.add_argument("--format", choices=["text", "json", "csv"], default="text",
                        help="Output format (default: text)")

    args = parser.parse_args()

    if args.paper_id:
        paper = get_paper(args.paper_id)
        papers = [paper] if paper else []
    elif args.citations:
        papers = get_citations(args.citations, limit=args.limit)
    elif args.references:
        papers = get_references(args.references, limit=args.limit)
    elif args.query:
        papers = search_papers(
            args.query,
            limit=args.limit,
            offset=args.offset,
            year_start=args.year_start,
            year_end=args.year_end,
            fields_of_study=args.fields_of_study,
        )
    else:
        parser.print_help()
        sys.exit(1)

    if not papers:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    if args.format == "json":
        print(format_json(papers))
    elif args.format == "csv":
        print(format_csv(papers))
    else:
        print(format_text(papers))
        print(f"({len(papers)} result(s))", file=sys.stderr)


if __name__ == "__main__":
    main()
