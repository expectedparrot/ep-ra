---
name: workflow-web-scraping
description: >
  Web scraping and structured data extraction via Firecrawl MCP tools.
  Use when the user needs to scrape websites, crawl pages, or extract
  structured data from web content.
tags: [workflow, external-tool, data-collection]
---

# Firecrawl Web Scraping

Firecrawl is available as an MCP server, providing tools for scraping, crawling, and extracting structured data from websites. Any agent with `mcp__firecrawl__*` in its tool list can use these tools.

## Available Tools

| Tool | Purpose |
|------|---------|
| `mcp__firecrawl__firecrawl_scrape` | Scrape a single URL to clean markdown |
| `mcp__firecrawl__firecrawl_extract` | Extract structured data from pages using an LLM prompt |
| `mcp__firecrawl__firecrawl_map` | Discover all indexed URLs on a site |
| `mcp__firecrawl__firecrawl_search` | Search the web and optionally extract content from results |
| `mcp__firecrawl__firecrawl_crawl` | Start an async crawl of a site with advanced options |
| `mcp__firecrawl__firecrawl_check_crawl_status` | Check progress of an async crawl |

## When to Use Firecrawl vs WebFetch

- **Firecrawl**: JavaScript-rendered pages, structured data extraction (tables, lists, directories), crawling multiple pages, sites that block simple fetches.
- **WebFetch**: Simple static pages where you just need text content. No API cost.

Prefer Firecrawl when you need **structured extraction** or when WebFetch returns incomplete/broken content.

For a text corpus, preserve the original full text and source URLs. JSON
extraction can summarize descriptions; do not substitute those summaries for
source documents. Fetch detail pages when listings truncate the text, and
verify a sample against the source before claiming full-text coverage. If
full text needs more paid retrieval, offer that choice rather than silently
reducing the requested content to save credits.

## Common Patterns

### Scrape a Single Page

```
Tool: mcp__firecrawl__firecrawl_scrape
Input: {"url": "https://example.com/team"}
```

Returns clean markdown of the page. Good for team pages, about pages, product listings.

### Extract Structured Data

```
Tool: mcp__firecrawl__firecrawl_extract
Input: {
  "urls": ["https://example.com/team"],
  "prompt": "Extract each team member's name, title, and bio as a JSON array"
}
```

Returns structured JSON. This is the most powerful tool for building agent lists from web content -- the LLM extracts exactly the fields you specify.

### Discover All Pages on a Site

```
Tool: mcp__firecrawl__firecrawl_map
Input: {"url": "https://example.com"}
```

Returns a list of all indexed URLs. Useful for finding all relevant pages before scraping specific ones.

### Search + Extract

```
Tool: mcp__firecrawl__firecrawl_search
Input: {
  "query": "board of directors site:example.com",
  "scrapeOptions": {"formats": ["markdown"]}
}
```

Combines web search with content scraping.

## Building AgentLists from Scraped Data

The typical workflow:

1. **Discover**: Use `firecrawl_map` or `firecrawl_search` to find relevant pages
2. **Extract**: Use `firecrawl_extract` with a prompt describing the fields you need
3. **Build**: Convert the extracted data into an EDSL AgentList

```python
# After extracting structured data from Firecrawl:
from edsl import Agent, AgentList

agents = AgentList([
    Agent(name=person["name"], traits={
        "role": person["role"],
        "background": person["bio"],
        "organization": person["org"],
    })
    for person in extracted_data
])
```

## Configuration

Firecrawl is configured as an MCP server in `.mcp.json` at the repo root. The API key is read from the `FIRECRAWL_API_KEY` environment variable in `.env`.

## Handling Large Responses

Firecrawl search and scrape results can exceed the agent's context window (100K+ characters). To avoid context overflow:

- **Cap `limit` on `firecrawl_search`** to 5–10 results. The default can return dozens of full-page scrapes.
- **Never copy a large response into generated source code.** For a discovered
  machine-readable URL, save its bytes directly under the study's `data/raw/`
  directory with a bounded downloader, record a checksum, and make a short
  parser read that file. Source data and executable code are separate
  artifacts.
- **Use `firecrawl_extract` instead of `firecrawl_search`** when you know the target URL — it returns only the structured fields you ask for, not full page content.

## Cost Awareness

Firecrawl consumes credits. Before a paid operation, define the URLs, tool,
page/result limits, and requested output. Prefer specific URLs over broad
crawls. Present an available estimate or credit count; state when the exact
charge is unknown instead of guessing a dollar amount.

Use `AskUserQuestion` to offer the bounded paid operation and a free/manual
alternative such as simple fetching or user-provided files. For example:
"I can retrieve these five article URLs using paid web extraction. The exact charge is not
available here. Approve one scrape per URL, or use manual downloads?"
When pricing is unavailable, explicit approval of that disclosed uncertainty
and operation is sufficient; do not stall at a warning. A page limit bounds
the work, not a guaranteed dollar ceiling. If the user requires a hard budget,
use an enforceable tool limit or obtain pricing before promising that ceiling.

Once approved, execute within the stated scope without asking again for each
already-approved URL. Request new approval for extra pages, retries, or a
different paid operation. A request to collect texts alone is not spend
approval. If Firecrawl is unavailable or declined, continue with the agreed
alternative and report any collection gaps.
