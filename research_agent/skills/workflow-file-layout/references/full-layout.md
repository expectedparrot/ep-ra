# Full study layout reference

Complete reference for how to organize files and directories when running studies.

## Directory Layout

All work lives in `sessions/`. Inside sessions, files are organized by **topic** (a general area of study). Each topic gets a directory with a descriptive alias derived from the user's request.

Example: "I want to study status quo bias among older people" → `topic_status-quo-bias-age`

If the directory already has topic folders, make sure your topic name is unique.

Within each topic, create one or more **studies** — self-contained collections of files that do something (create an agent list, run a simulation, etc.). Studies are named with snake-case post-fix indices: `_a`, `_b`, etc.

```
sessions/
  topic_<alias>/
    README.md
    study_a/
    study_b/
    study_c/
```

## Creating a Study

Use the `ep study scaffold` tool to scaffold the structure:

```bash
ep study scaffold sessions/topic_<alias>/<study_name>
```

For EDSL studies (default), this creates these directories:

```
refs/
data/
  raw/
  cooked/
  uploaded/
edsl_jobs/
  job_a/
  job_b/
analysis/
computed_objects/
writeup/
  tables/
  plots/
  numbers/
```

The scaffold does not create blank placeholders. Author `README.md`,
`requirements.txt`, EDSL source files, analysis scripts, and report Markdown
only when their real contents are known. It installs the non-empty standard
Makefile and report-rendering assets separately.

For simulation studies (`ep study scaffold <path> --type simulation`), the `edsl_jobs/` directory is replaced with `simulations/`:

```
simulations/
  sim_a/
refs/
data/
  raw/
  cooked/
  uploaded/
analysis/
computed_objects/
writeup/
  tables/
  plots/
  numbers/
```

**Simulation file placement rules:**
- Simulation logs (JSON) are saved to `data/` (same location as EDSL results)
- HTML visualizations are saved to `data/` or `writeup/plots/`
- Analysis scripts go in `analysis/`, outputs to `writeup/`
- Concordia simulation code goes in `simulations/`. Read `research_agent/skills/research-social-simulation/SKILL.md` for runner patterns.

## Report Formatting

**Report assets**: Every study needs the CSS stylesheet, LaTeX header, logo,
and Lua table filter in its `writeup/` directory.

Report assets are packaged with EDSL and copied by `ep study scaffold`. For an
older study missing them, rerun the idempotent scaffold command:

```bash
ep study scaffold <study_root>
```

Use this template for the report targets in the Makefile:

```makefile
# --- Report ---
writeup/report.html: writeup/report.md $(PLOTS) $(TABLES)
	cd writeup && pandoc report.md -o report.html --standalone --embed-resources --css=report.css

writeup/report.pdf: writeup/report.md writeup/report_header.tex writeup/fix-table-widths.lua $(PLOTS) $(TABLES)
	cd writeup && pandoc report.md -o report.pdf --pdf-engine=xelatex --include-in-header=report_header.tex --lua-filter=fix-table-widths.lua

report: writeup/report.html writeup/report.pdf
```

`report_header.tex` provides the PDF equivalent of the HTML branding from `report.css`: green section headings, an "Expected Parrot" running header on every page, and green hyperlinks.

`fix-table-widths.lua` is a Lua filter that prevents column overflow in PDF tables. Without it, pandoc generates unconstrained `l` columns and long cell text (multi-word headers, compound names, many columns) runs into adjacent columns and overlaps. The filter distributes column widths proportionally so LaTeX wraps text within each cell instead of overflowing.

**No duplicate title**: The `report.md` file uses a YAML frontmatter block with `title:` and `date:`. Pandoc renders the `title` as an H1 heading automatically. Do NOT also include an `# H1` heading in the body — this causes the title to appear twice. Start the body with `## Summary` or another H2.

Correct format:
```markdown
---
title: "My Study Title"
date: 2026-01-15
---

## Summary

The body starts here with an H2...
```

Wrong format (title appears twice):
```markdown
---
title: "My Study Title"
date: 2026-01-15
---

# My Study Title

## Summary
...
```

## Rules

1. **Always create this file structure** for each study. Also create `checklist.md` (see `research_agent/skills/workflow-completion-checklist/SKILL.md`). Do not initialize or modify a Git repository unless the user explicitly requests publishing or version-control work.

2. **Use README.md as your lab notebook** — write what you did at each step:
   ```markdown
   PURPOSE
   Author
   Timestamp
   LOG Entries
   ```

3. **Preserve existing work.** Write a new file directly when it does not yet
   exist. Read an existing file before changing it and do not overwrite
   unrelated user content. The scaffold deliberately avoids blank placeholders.

4. **Keep study work reproducible.** Record meaningful progress in `README.md` and keep executable work in scripts and Makefile targets.

5. **Do not run Python code directly or inline.** Never run EDSL jobs, analysis, or any study code as inline Bash/Python commands — all code must be written to files and executed via `make` targets. This includes EDSL survey/object construction, `jobs.ep` creation via `ep jobs build`, and results generation via `ep run ... --output data/results.ep` (write to study files in `edsl_jobs/`, run with `make data`). Analysis scripts also belong in `analysis/` and should be wired into Makefile targets such as `make plots`. Code that is not in a file is not reproducible.

6. **Snake-case names for outputs.** Name scripts after what they produce:
   - `table_growth_over_time.py` → `writeup/tables/growth_over_time.csv`
   - `plot_growth_over_time.py` → `writeup/plots/growth_over_time.png`
   - Each has a corresponding Makefile recipe.

7. **PLOT and TABLES phony targets** in the Makefile are dependencies for the overall report.

8. **Follow-up studies reference predecessors in place by default.** Record each predecessor's absolute path and, when available, its study/session identifier in `writeup/planning.md` or `chat_summary.md`. Read the predecessor's `chat_summary.md` first, then access only the files needed from its original location.

   When a portable or immutable reference is necessary, copy only the required artifacts into `refs/<predecessor_study_name>/` and add `refs/<predecessor_study_name>/provenance.json` containing:
   - original study path and study/session identifier;
   - copy timestamp in ISO 8601 format;
   - each copied file's source and destination path.

   Do not copy an entire predecessor study unless the user explicitly requests a self-contained bundle.

9. **Intermediate datasets** (transformed raw data, fitted models, etc.) go in `computed_objects/`.

10. **Add packages to `requirements.txt`** as needed.

    The scaffolded Makefile runs `python` and `ep` through the repository's
    locked uv project. Keep it compatible with GNU Make 3.81, the version
    shipped by macOS. Do not use grouped-target syntax. If one script produces
    multiple files, give the recipe to one primary output and make companion
    outputs depend on that primary. Run `make --version` and `make -n <target>`
    before executing a newly written target.

11. **EDSL code goes in the `edsl_jobs/` directory.** Read `research_agent/skills/edsl-study-files/SKILL.md` for the standard file templates and export conventions. **Concordia simulation code goes in the `simulations/` directory.** Read `research_agent/skills/research-social-simulation/SKILL.md` for runner patterns.

12. **User-uploaded data** goes in `data/uploads`. Data is also added to the repo unless too large.

13. **Use the SearchExpectedParrot tool** to search Expected Parrot for EDSL objects. Use it directly instead of writing Python scripts with `Coop().list()`.

14. **Single report file rule**: Only ONE report markdown in `writeup/` — that is `report.md`. To elaborate on results or extend the report, edit `report.md` rather than creating new files. Allowed `.md` files in `writeup/`: `report.md`, `survey.md` (auto-generated), `planning.md` (working notes), `appendix.md` (supplementary material). After compiling, run `ep report check --root <study_dir>`.

15. **Validation invariants are frozen protocol.** After plan approval, do not
weaken a threshold, remove a required answer, replace an objective verifier, or
set a tolerance equal to an observed failure count merely to make a gate pass.
Preserve the failed verification result. A scientifically justified change
requires a documented protocol amendment, an explanation to the user, and
fresh approval before it governs new inference; it does not retroactively
validate the existing run.

## Observability Scripts

These helper scripts live in `research_agent/skills/workflow-file-layout/scripts/` and support session-level logging:

- **`log_cost.py`** — Appends estimated vs. actual cost to `costs.jsonl` in the study root. For new EDSL `.ep` workflows, prefer the CLI form `ep costs log --output costs.jsonl --actual-from data/results.ep --note "full run"` after the Makefile's `ep run ... --output data/results.ep` target completes.
