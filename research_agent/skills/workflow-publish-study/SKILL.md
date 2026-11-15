---
name: workflow-publish-study
description: >
  Publish a completed study's report.html to Expected Parrot via EDSL FileStore.
  Use when the user wants to share or publish a finished study report.
allowed-tools: Read, Glob, Bash(python *), Bash(make *), Bash(cd *), Write, AskUserQuestion
user-invocable: true
arguments: study_dir
tags: [workflow, publishing]
---

# Publish Study

Publishes a completed study by pushing `writeup/report.html` to Expected Parrot as an EDSL `FileStore` object. The report becomes viewable at its alias URL.

## Step-by-Step

### 1. Verify the study is ready

Before publishing, confirm from the study root:

- `writeup/report.html` exists. If not, run `make writeup/report.html` first.
- The study root directory is known (passed as `study_dir` argument).
- **CSS and images are embedded.** Check that `report.html` does NOT contain `<link rel="stylesheet" href="report.css"` (an external CSS reference). If it does, the report was built without `--embed-resources` and will render unstyled on Expected Parrot. Rebuild it:
  ```bash
  cd <study_root>/writeup && pandoc report.md -o report.html --standalone --embed-resources --css=report.css
  ```
  Also update the Makefile's `report.html` target to include `--embed-resources` so future builds are correct.
- **Theory diagrams must be static SVG, not interactive HTML.** Expected Parrot strips or sandboxes JavaScript, so interactive HTML diagrams (e.g., from `render_collapsible_diagram.py` or `render_theory_diagram.py --format html`) will not work when published. Before publishing, replace any `<iframe>` references or embedded HTML/JS diagram blocks in `report.md` with a static SVG image:
  ```bash
  # Generate the SVG
  python scripts/render_theory_diagram.py theory.json --format svg -o writeup/plots/theory.svg
  ```
  Then reference it in `report.md` as a normal image:
  ```markdown
  ![Theory diagram description](plots/theory.svg)
  ```
  The interactive HTML version is still useful for local exploration -- keep it in `writeup/plots/` for that purpose, but do not embed it in the published report.

### 2. Pick an alias

Suggest a short, descriptive URL slug based on the study topic (e.g., `ep-tagline-testing`, `llm-status-quo-bias`). Use `AskUserQuestion` to confirm:

```
Question: "What alias (URL slug) should this report be published under?"
Header: "Report alias"
Options:
  1. "<suggested-slug>" - "Based on the study topic"
  2. "<alternative-slug>" - "Shorter alternative"
```

Alias rules: lowercase, hyphens only, no spaces or special characters.

### 3. Ask about visibility

Use `AskUserQuestion`:

```
Question: "What visibility should the published report have?"
Header: "Visibility"
Options:
  1. "unlisted" - "Anyone with the link can view it"
  2. "public" - "Discoverable by anyone"
  3. "private" - "Only you can view it"
```

### 4. Publish the HTML FileStore

`ep push` currently accepts git-backed `.ep` packages, not raw HTML files. This
is a documented CLI gap; do not run the invalid command `ep push
writeup/report.html`. Put the following substantive FileStore operation in
`analysis/publish_report.py`, wire it to a `make publish` target, and run that
target only after the user approves visibility:

<!-- ep-cli-lint: allow substantive-analysis -->
```python
from edsl import FileStore

report = FileStore("writeup/report.html")
info = report.push(
    description="Study report: <brief-description>",
    alias="<chosen-alias>",
    visibility="<chosen-visibility>",
)
print(info)
```

```make
.PHONY: publish
publish:
	python analysis/publish_report.py
```

**`fs.push()` returns a dict-like `Scenario`**, not a list. Access fields directly: `info['url']`, `info['alias_url']`, `info['uuid']`.

If the alias already exists, `push()` raises `CoopResponseError`. To overwrite, delete the existing object first, then re-push:
```python
from edsl import Coop
coop = Coop()
# Build the alias URL dynamically (works on production and test servers)
username = coop.get_profile()["username"]
alias_url = f"{coop.url}/content/{username}/<alias>"
coop.delete(alias_url)
# Then push the new version
info = fs.push(alias='<alias>', visibility='unlisted')
```

> **Note**: `fs.push(force=True)` is accepted but currently has no effect — the `force` parameter is not passed through internally. Always use delete-then-push to overwrite.

### 5. Report the result

Tell the user the published URL from `info['alias_url']`. The URL depends on the server being used (production vs test):

```python
# info['alias_url'] returns the correct URL for whatever server is configured
print(info['alias_url'])  # e.g., https://www.expectedparrot.com/content/<username>/<alias>
```

### 6. Add Makefile targets

If the study Makefile does not already have `publish` and `update` targets, add them:

```makefile
.PHONY: publish update

REPORT_ALIAS ?= <chosen-alias>
REPORT_VISIBILITY ?= <chosen-visibility>
REPORT_DESCRIPTION ?= Study report: <brief-description>

publish: writeup/report.html
	python -c "\
from edsl import FileStore; \
fs = FileStore('writeup/report.html'); \
info = fs.push(description='$(REPORT_DESCRIPTION)', alias='$(REPORT_ALIAS)', visibility='$(REPORT_VISIBILITY)'); \
print('Published:', info['alias_url'])"

update: writeup/report.html
	python -c "\
from edsl import Coop, FileStore; \
coop = Coop(); \
username = coop.get_profile()['username']; \
alias_url = f'{coop.url}/content/{username}/$(REPORT_ALIAS)'; \
try: coop.delete(alias_url); print('Deleted old version') \
except Exception: pass; \
fs = FileStore('writeup/report.html'); \
info = fs.push(description='$(REPORT_DESCRIPTION)', alias='$(REPORT_ALIAS)', visibility='$(REPORT_VISIBILITY)'); \
print('Updated:', info['alias_url'])"
```

- `publish` — first-time push. Creates the object on Expected Parrot with the chosen alias.
- `update` — deletes the existing object at the alias, then re-pushes. Use after regenerating the report.

Both depend on `writeup/report.html` so the report is rebuilt if needed.

## Troubleshooting

- **Alias already taken on first publish**: Either use `force=True` to overwrite, choose a different alias, or add a suffix (e.g., `-v2`).
- **No `report.html`**: Run `make writeup/report.html` before publishing.
- **Push fails**: Check that EDSL is installed and the user is authenticated (`ep auth login`).

## Coop API Notes

**Do not guess Coop methods.** The following are the relevant methods for publishing:

| Method | Purpose | `url_or_uuid` accepts |
|--------|---------|----------------------|
| `Coop.push(object, ...)` | Create new object | N/A |
| `Coop.patch(url_or_uuid, ...)` | Update existing object | UUID string or full URL (`https://www.expectedparrot.com/content/<uuid>`) |
| `Coop.get(url_or_uuid)` | Retrieve an object | UUID, full URL, or alias URL (`https://www.expectedparrot.com/content/<username>/<alias>`) |
| `Coop.delete(url_or_uuid)` | Delete an object | UUID or full URL |

**`Coop.search()` does not exist.** To find an object by alias, use `Coop.get()` with the alias URL. To list your objects, use `Coop.list()`.

**`url_or_uuid` must be a UUID or full URL** — bare strings like `content/my-alias` will fail with a validation error. Always use the full URL or the UUID returned by `push()`.

> **Terminology rule:** Always say "Expected Parrot" in user-facing material — never "Coop".
