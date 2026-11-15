---
name: edsl-object-search
description: >
  Search, browse, and pull EDSL objects (Surveys, Results, AgentLists, Prompts, etc.) from Expected Parrot cloud.
  Use when the user wants to find, retrieve, or browse existing EDSL objects stored on Expected Parrot.
tags: [edsl, reference]
---

# Search & Pull EDSL Objects from Expected Parrot

Search, browse, and retrieve EDSL objects stored on Expected Parrot with the
supported `ep` CLI.

## Workflow

### 1. Parse the Input

Determine what the user wants:

- **UUID** (36-char hex with dashes, pattern `8-4-4-4-12`): go directly to step 4 (Retrieve)
- **URL** (starts with `http`): extract UUID or alias, go to step 4
- **Recent or relative reference** (e.g., "my latest survey", "the results I
  just ran"): read
  [recent-content-discovery.md](references/recent-content-discovery.md). Use
  current-session evidence first, then bounded remote metadata and content
  inspection when needed.
- **Search query with type hint** (e.g., "surveys about hiring", "results for experiment"): extract the object type and search keywords, go to step 2
- **Search query without type hint** (e.g., "customer satisfaction"): search across all types, go to step 2
- **Nothing or vague**: use `AskUserQuestion` to ask:

```
Question: "What are you looking for?"
Header: "Search"
Options:
  - "Browse my objects" / "See your own objects on Expected Parrot"
  - "Search community" / "Search public objects shared by others"
  - "Pull by UUID" / "Retrieve a specific object by its UUID or URL"
```

Then follow up with type/keyword questions as needed.

### 2. Search

Search directly with the CLI:

```bash
ep search --query "keyword" --type survey --page 1 --page_size 10
ep search --query "keyword" --visibility public --community
```

**Type extraction hints** — map natural language to `object_type`:
- "survey(s)" → `"survey"`
- "result(s)" → `"results"`
- "agent(s)" / "agent list(s)" → `"agent_list"` (or `"agent"` for single)
- "scenario(s)" / "scenario list(s)" → `"scenario_list"` (or `"scenario"` for single)
- "question(s)" → `"question"`
- "model(s)" → `"model"` or `"model_list"`
- "cache(s)" → `"cache"`
- "notebook(s)" → `"notebook"`
- "macro(s)" → `"macro"` or `"composite_macro"`
- "prompt(s)" / "instructions" → `"prompt"`

**Supported object types** (all 14):
`agent`, `agent_list`, `cache`, `model`, `model_list`, `notebook`, `prompt`, `question`, `results`, `scenario`, `scenario_list`, `survey`, `macro`, `composite_macro`

### 3. Select

If multiple results are returned, present them to the user with `AskUserQuestion`:

- Show up to 4 options (the top results) with description snippets as labels and type/owner as descriptions
- Include a "Search again" option if the results don't look right
- If there are more pages, mention it: "Showing page 1 of N (M total results)"

If only one result, confirm with the user before pulling, or proceed directly if the match is clearly what they asked for.

### 4. Retrieve

Inspect or save the selected object by UUID/URL and expected type:

```bash
ep inspect <uuid-or-url> --type survey
ep inspect <uuid-or-url> --type agent_list --save data/agent_list.ep
```

After pulling, display a summary based on the object type:

| Object Type | Summary to Show |
|-------------|-----------------|
| `survey` | Question count, question names, has rules/memory |
| `results` | Row count, column names (answer/agent/scenario columns) |
| `agent_list` | Agent count, trait names, sample agent traits |
| `agent` | Agent name, trait names and values |
| `scenario_list` | Scenario count, key names, sample values |
| `scenario` | Key names and values |
| `question` | Question type, name, text, options (if applicable) |
| `cache` | Entry count |
| `model` / `model_list` | Model name(s), parameters |
| `notebook` | Cell count |
| `macro` / `composite_macro` | Description, components |
| `prompt` | Character and line count, text |

**Summary examples:**

```python
# Survey
print(f"Survey with {len(obj)} questions: {obj.question_names}")

# Results
df = obj.to_pandas()
answer_cols = [c for c in df.columns if c.startswith('answer.')]
agent_cols = [c for c in df.columns if c.startswith('agent.')]
scenario_cols = [c for c in df.columns if c.startswith('scenario.')]
print(f"Results: {len(df)} rows, {len(answer_cols)} questions, {len(agent_cols)} agent traits, {len(scenario_cols)} scenario vars")

# AgentList
print(f"AgentList with {len(obj)} agents, traits: {obj.trait_keys}")

# ScenarioList
print(f"ScenarioList with {len(obj)} scenarios, keys: {list(obj[0].keys()) if len(obj) > 0 else []}")
```

### 5. Save

Ask the user if and where to save locally:

```
Question: "Save this object locally?"
Header: "Save"
Options:
  - "Yes, default filename" / "Save as {slug}.ep ({slug}.json for a prompt) in current directory"
  - "Yes, custom filename" / "Choose a filename and location"
  - "No" / "Don't save, just inspect"
```

Generate a default filename from the description:

```python
import re

def slugify(text, max_length=60):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = text.strip('-')
    if len(text) > max_length:
        text = text[:max_length].rsplit('-', 1)[0]
    return text

filename = slugify(description) + ".ep"
```

Save using the `.git.save()` method:

```python
obj.git.save(filename)
print(f"Saved to: {filename}")
```

A prompt has no `.ep` format. Use `slugify(description) + ".json"` as the
filename and save it with `obj.save(filename)`.

If "custom filename", use `AskUserQuestion` to get the desired filename, then save.

### 6. Report

Summarize what was done:

- What was found (object type, description, owner)
- File path if saved
- Quick-reference for loading it back:

```python
# To load this object later:
from edsl import {ClassName}
obj = {ClassName}.git.load("{filename}")

# Or pull fresh from the cloud:
obj = {ClassName}.pull("{uuid}")
```

For a prompt, replace the `.git.load` line with `Prompt.load("{filename}")`.
`Prompt.pull` works as shown.

## Class Name Mapping

Map object types to import names for the load-back reference:

| Object Type | Class Name |
|-------------|-----------|
| `survey` | `Survey` |
| `results` | `Results` |
| `agent` | `Agent` |
| `agent_list` | `AgentList` |
| `scenario` | `Scenario` |
| `scenario_list` | `ScenarioList` |
| `question` | `Question` |
| `cache` | `Cache` |
| `model` | `Model` |
| `model_list` | `ModelList` |
| `notebook` | `Notebook` |
| `prompt` | `Prompt` |
| `macro` | `Macro` |
| `composite_macro` | `CompositeMacro` |

## Pagination

If there are multiple pages of results:

```python
# Check pagination
if objects.total_pages > 1:
    print(f"\nShowing page {objects.current_page} of {objects.total_pages} ({objects.total_count} total)")
    print("Use /search-objects to search again or ask for 'next page'")
```

To get the next page, re-run with `page=page+1`.

## Error Handling

- **No results found**: Suggest broadening the search (remove type filter, try different keywords, try `community=True`)
- **UUID not found**: Check if it's a valid UUID format, suggest searching by description instead
- **Authentication error**: Remind user to set up their Expected Parrot API key (`EXPECTED_PARROT_API_KEY` env var or run `ep auth login --api_key <key>`)
- **Network error**: Suggest checking internet connection and trying again

## Examples

### Search for surveys about customers
User says "find surveys about customers" → extract type `survey`, query
`customers` → run `ep search --type survey --query "customers"` → read
`data.objects` → show results → user picks one → inspect and offer to save.

### Pull by UUID
User provides a UUID → detect UUID format → run `ep inspect <uuid> --type
<lowercase-object-type>` → show summary → offer to save.

### Browse community objects
User says "browse objects" → ask what they're looking for → user picks
"Search community" → ask for type/keywords → run `ep search --community ...`
→ show results.
