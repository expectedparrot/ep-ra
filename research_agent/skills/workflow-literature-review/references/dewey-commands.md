# dewey Command Reference

## Contents
- [Project commands](#project-commands) — init, status, doctor
- [Source commands](#source-commands) — add, list, show, remove
- [BibTeX commands](#bibtex-commands) — bib show/set/edit, cite
- [State commands](#state-commands) — state set/show/set-priority/mark-read
- [Notes commands](#notes-commands) — notes show/set/edit
- [Link commands](#link-commands) — link add/list/remove
- [Order commands](#order-commands) — order show/set/add/remove
- [Instructions commands](#instructions-commands) — instructions show/set/append
- [Representation commands](#representation-commands) — render md, cat, path
- [Search and index commands](#search-and-index-commands) — search, index rebuild/stats
- [Data models](#data-models)
- [JSON output contract](#json-output-contract)

---

## Project commands

### `dewey init`
Initialize a new dewey repository in the current directory.

```bash
dewey init
dewey init --json
```

Creates `.dewey/` with `config.json`, `instructions.md`, `review_order.json`, `sources/`, `indexes/search.sqlite`, `logs/activity.jsonl`. Fails if `.dewey/` already exists.

### `dewey status`
Summarize repository health.

```bash
dewey status
dewey status --json
```

Reports: source count, sources with PDFs, sources with Markdown ready, status counts by workflow stage, ordered sources, total links, stale/failed Markdown count, index health.

### `dewey doctor`
Validate repository integrity.

```bash
dewey doctor
dewey doctor --json
```

Checks: required files exist, every `entry.bib` parses, metadata/state schemas valid, links reference real sources, order references real sources, PDF hash matches if present, index openable.

Exits nonzero on integrity failure.

---

## Source commands

### `dewey add source <path>`
Add a source from a `.bib` or `.pdf` file.

```bash
dewey add source refs/paper.bib
dewey add source papers/paper.pdf
dewey add source papers/paper.pdf --no-md           # skip Markdown generation
dewey add source papers/paper.pdf --copy            # copy PDF into .dewey/
dewey add source papers/paper.pdf --reference       # store original path only
dewey add source papers/paper.pdf --force-duplicate # add even if hash already exists
dewey add source papers/paper.pdf --bibtex-key mykey
```

**PDF behavior:** computes SHA-256, detects duplicate, copies or references PDF, attempts Markdown generation via `paper2md`, creates placeholder BibTeX (`@misc` with filename stem as title).

**BibTeX behavior:** parses exactly one entry, creates source directory.

### `dewey list`
List all sources.

```bash
dewey list
dewey list --json
dewey list --status reading
dewey list --status included
dewey list --has-pdf
dewey list --has-md
dewey list --ordered
```

Default columns: source_id, bibtex_key, status, title, year, markdown_status.

### `dewey show <source-id>`
Show full record for one source.

```bash
dewey show src_335517b63c54
dewey show src_335517b63c54 --json
```

Includes: paths, metadata, state, raw BibTeX, parsed BibTeX, outgoing and incoming links.

### `dewey remove source <source-id>`
Delete a source.

```bash
dewey remove source src_335517b63c54 --yes
dewey remove source src_335517b63c54 --yes --json
```

Deletes source directory, removes from review order, cleans up inbound links, updates index.

---

## BibTeX commands

### `dewey bib show <source-id>`
Print canonical BibTeX entry.

```bash
dewey bib show src_335517b63c54
dewey bib show src_335517b63c54 --json
```

### `dewey bib set <source-id> --file <path>`
Replace the entire BibTeX entry from a file (must contain exactly one entry).

```bash
dewey bib set src_335517b63c54 --file corrected.bib
```

### `dewey bib edit <source-id> --field <name> --value <value>`
Edit specific BibTeX fields. Multiple `--field`/`--value` pairs in one command.

```bash
dewey bib edit src_335517b63c54 \
    --field title  --value "Attention Is All You Need" \
    --field author --value "Vaswani, Ashish and Shazeer, Noam" \
    --field year   --value "2017" \
    --field journal --value "NeurIPS"

# Remove a field
dewey bib edit src_335517b63c54 --unset note
```

Special field names: `key` (changes BibTeX key), `entry_type` (changes `@article` → `@inproceedings` etc.).

### `dewey cite <source-id>`
Output citation material.

```bash
dewey cite src_335517b63c54                      # BibTeX (default)
dewey cite src_335517b63c54 --format key         # BibTeX key only
dewey cite src_335517b63c54 --format json
```

---

## State commands

Workflow states (in typical progression): `unread` → `queued` → `reading` → `read` → `included` / `excluded`.

### `dewey state set <source-id> <status>`

```bash
dewey state set src_335517b63c54 reading
dewey state set src_335517b63c54 included
dewey state set src_335517b63c54 excluded
```

Setting `included` sets `included=true` in `state.json`; `excluded` sets `included=false`.

### `dewey state show <source-id>`

```bash
dewey state show src_335517b63c54
dewey state show src_335517b63c54 --json
```

### `dewey state mark-read <source-id> --depth <full-text|abstract|metadata-only>`
Set status to `read`, record `last_read_at`, and declare the evidence depth.
`full-text` is the default and requires a PDF or ready Markdown; use `abstract`
explicitly for title/abstract screening.

```bash
dewey state mark-read src_335517b63c54 --depth full-text
```

### `dewey state set-priority <source-id> <int>`
Set integer priority (lower = higher priority).

```bash
dewey state set-priority src_335517b63c54 1
```

---

## Notes commands

Notes are freeform Markdown stored in `.dewey/sources/<id>/notes.md`. dewey never overwrites notes except on explicit notes commands.

### `dewey notes show <source-id>`

```bash
dewey notes show src_335517b63c54
dewey notes show src_335517b63c54 --json
```

### `dewey notes set <source-id> --file <path>`
Replace notes entirely from a file.

```bash
dewey notes set src_335517b63c54 --file my_notes.md
```

### `dewey notes edit <source-id> --append <text>`
Append text to existing notes.

```bash
dewey notes edit src_335517b63c54 --append "Key finding: privacy premium ~$4/month. n=1,200."
```

---

## Link commands

Links record directional semantic relationships between sources. Only outgoing links are stored canonically; incoming links are computed.

### `dewey link add <from-id> <to-id> --type <type>`

```bash
dewey link add src_B src_A --type builds_on --note "Extends the WTP framing to mobile"
dewey link add src_C src_A --type contradicts
```

Link types: `builds_on`, `contradicts`, `compares_to`, `uses_method`, `uses_dataset`, `motivates`, `historical_predecessor`, `same_work_as`, `version_of`.

### `dewey link list <source-id>`
Show outgoing and computed incoming links.

```bash
dewey link list src_335517b63c54
dewey link list src_335517b63c54 --json
```

### `dewey link remove <from-id> <to-id> --type <type>`

```bash
dewey link remove src_B src_A --type builds_on
```

---

## Order commands

Manual review order: arrange sources for the order you'll discuss them in the review.

### `dewey order show`

```bash
dewey order show
dewey order show --json
```

### `dewey order set <source-id>...`
Replace the entire order.

```bash
dewey order set src_A src_B src_C src_D
```

All source IDs must exist; no duplicates allowed.

### `dewey order add <source-id> --before <other-id>`
### `dewey order add <source-id> --after <other-id>`
Insert a source at a relative position. If already in order, it is moved.

```bash
dewey order add src_new --after src_A
dewey order add src_survey --before src_A
```

### `dewey order remove <source-id>`
Remove from order without deleting the source.

```bash
dewey order remove src_335517b63c54
```

---

## Instructions commands

Project-level instructions travel with the bibliography in `.dewey/instructions.md`.

### `dewey instructions show`

```bash
dewey instructions show
```

### `dewey instructions set --file <path>`

```bash
dewey instructions set --file literature/research_question.md
```

### `dewey instructions append <text>`

```bash
dewey instructions append "Exclude non-English papers."
```

---

## Representation commands

### `dewey render md <source-id>`
Generate or regenerate Markdown from managed PDF using `paper2md`.

```bash
dewey render md src_335517b63c54
dewey render md --all          # regenerate for all sources with PDFs
```

Fails if no PDF exists. Updates `markdown_status` in `metadata.json`.

### `dewey cat <source-id>`
Print the working Markdown representation.

```bash
dewey cat src_335517b63c54
```

Fails if no Markdown exists (`markdown_status` must be `ready`).

### `dewey path <source-id> --<artifact>`
Return the filesystem path to a specific artifact. Exactly one flag required.

```bash
dewey path src_335517b63c54 --pdf
dewey path src_335517b63c54 --md
dewey path src_335517b63c54 --notes
dewey path src_335517b63c54 --bib
```

---

## Search and index commands

Search is local FTS5 (SQLite). Multiple filters combine with AND logic. Case-insensitive.

### `dewey search [query]`

```bash
dewey search "effect size"                         # full-text (title, bib, notes, markdown)
dewey search --title "scaling law"
dewey search --author "kahneman"
dewey search --bibtex "conjoint"
dewey search --notes "validated scale"
dewey search --fulltext "self-attention"
dewey search --status included
dewey search --has-pdf
dewey search --has-md
dewey search --linked-to src_A                     # sources that link to src_A
dewey search --link-type builds_on

# Combine filters
dewey search "privacy" --status read --has-md
```

### `dewey index rebuild`
Rebuild the entire search index from canonical files.

```bash
dewey index rebuild
```

Run after bulk imports or if search results seem wrong.

### `dewey index stats`

```bash
dewey index stats
```

---

## Data models

### Source statuses
| Status | Meaning |
|--------|---------|
| `unread` | Newly added, not yet assessed |
| `queued` | Marked for reading |
| `reading` | Currently being read |
| `read` | Finished reading |
| `included` | Selected for the bibliography |
| `excluded` | Explicitly rejected |

### Markdown statuses
| Status | Meaning |
|--------|---------|
| `missing` | No PDF, or conversion never attempted |
| `ready` | Successfully generated |
| `failed` | `paper2md` failed; see `artifacts/pdf2md.stderr.log` |
| `stale` | PDF was updated since Markdown was generated |

### Link types
| Type | Meaning |
|------|---------|
| `builds_on` | Extends or applies prior work |
| `contradicts` | Argues against findings |
| `compares_to` | Compares results or approaches |
| `uses_method` | Applies a technique from the source |
| `uses_dataset` | Uses data from the source |
| `motivates` | The source inspired this work |
| `historical_predecessor` | Earlier version by same or related authors |
| `same_work_as` | Identical or duplicate entry |
| `version_of` | Variant of the same work (preprint vs. published) |

---

## JSON output contract

All commands support `--json`. Use it when parsing output programmatically.

Success:
```json
{ "ok": true, "action": "source.add", "source_id": "src_...", ... }
```

Failure:
```json
{ "ok": false, "action": "source.add", "error": { "code": "file_not_found", "message": "..." } }
```

Exit codes: `0` success, `1` generic failure, `2` invalid input, `3` integrity error, `4` not found.
