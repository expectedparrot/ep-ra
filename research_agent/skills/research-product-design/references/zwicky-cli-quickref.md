# Zwicky CLI quick reference

Use JSON output for agent work. Add `--human` only when presenting output. Run
`zwicky -C <project-dir> guide` after every material stage and prefer its
returned next command over this reference.

## Project and morphological box

```bash
cd <absolute-study-root> && zwicky init product-design --problem "..."
zwicky -C <absolute-study-root>/product-design guide
zwicky -C <absolute-study-root>/product-design status
zwicky -C <project-dir> dim add <name> --values a,b,c
zwicky -C <project-dir> value add <dimension> <value>
zwicky -C <project-dir> cca set <value-a> <value-b> --verdict incompatible|tension|ok --reason "..."
zwicky -C <project-dir> cca gaps
zwicky -C <project-dir> rule add --values value-a,value-b,value-c --reason "..."
zwicky -C <project-dir> config generate
zwicky -C <project-dir> config stats
zwicky -C <project-dir> config infer --select value-a,value-b
zwicky -C <project-dir> diagnose
```

`zwicky init` accepts a project name, not an absolute output path. Initialize
from the parent directory, then use an absolute `-C` path.

## Sampling and adaptive evaluation

```bash
zwicky -C <project-dir> sample create --method coverage --size 20 --strength 2 --seed 123
zwicky -C <project-dir> sample create --method d-optimal --size 100 --features main-plus-pairwise --seed 123
zwicky -C <project-dir> model fit --assessment <utility-id> --criterion <criterion> --features main-plus-pairwise
zwicky -C <project-dir> sample create --method bayesian --size 50 --surrogate <model-id> --acquisition ucb --seed 456
```

## Stakeholders, criteria, and utility

```bash
zwicky -C <project-dir> stakeholders add --name "..." --description "..." --kind "..."
zwicky -C <project-dir> criteria add <name> --question "..." --direction maximize|minimize --evaluators a,b
zwicky -C <project-dir> utility build --sample <sample-id> --scale 7 --criteria criterion-a,criterion-b
zwicky -C <project-dir> utility preview <utility-id>
zwicky -C <project-dir> utility ingest <utility-id> --results <results-a.ep> <results-b.ep>
zwicky -C <project-dir> utility analyze <utility-id>
zwicky -C <project-dir> utility disagreement <utility-id>
zwicky -C <project-dir> utility sensitivity <utility-id> --criteria a,b --draws 1000 --seed 123
zwicky -C <project-dir> utility shortlist <utility-id> --criteria a,b --size 6
zwicky -C <project-dir> utility plot <utility-id> --type pareto --x a --y b --output writeup/pareto.svg
```

When a stakeholder represents an existing population, add `--agent-list
<agent-list.ep>`. Cost and run every Jobs package returned for distinct panels.

## Pairwise preferences, price, and reporting

```bash
zwicky -C <project-dir> preference design --sample <sample-id> --pairs 40 --price-levels 6,8,10 --evaluators buyers
zwicky -C <project-dir> preference build <preference-design-id>
zwicky -C <project-dir> preference ingest <preference-id> --results <results.ep>
zwicky -C <project-dir> preference fit <preference-id>
zwicky -C <project-dir> images ingest --results <image-results.ep> --name "Option renders"
zwicky -C <project-dir> presentations ingest --results <writeup-results.ep> --name "Concept writeups"
zwicky -C <project-dir> report guide
zwicky -C <project-dir> report template
```

Inspect current help when package guidance omits a needed option. Zwicky owns
the evidence store and report guidance; the agent owns the final narrative.
