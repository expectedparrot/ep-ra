# Blueprint Visualization Specification

## Contents

- [Input](#input)
- [Output Sections](#output-a-single-html-file-with-5-sections)
- [CSS Guidelines](#css-guidelines)
- [Script Structure](#script-structure)
- [Example](#example)

---

Given a blueprint JSON, generate a Python script that produces a single self-contained HTML file visualizing the full experimental design. The HTML should be openable in any browser with no external dependencies.

Available libraries: `graphviz`, `matplotlib`, `networkx`, `json`, `html`, `base64`, standard library.

---

## Input

The blueprint is a JSON file (or JSON string) with the structure produced by the blueprint design process. It contains:
- `scenario_description`
- `agents_in_scenario`
- `variables` (list of names)
- `edge_dict` (cause → outcome mappings)
- `variable_dict` (detailed variable definitions, keyed by name)

The JSON may be wrapped in the `StructuralCausalModelBuilder` serialization format, where the top level is `{"class": "StructuralCausalModelBuilder", "args": { ... }}`. If so, unwrap by reading from `args`.

Within `variable_dict`, each variable has a `class` field (`EndogenousVariable` or `ExogenousVariable`) and an `args` sub-object containing the variable's details.

When reading `edge_dict`, handle the `__set__` wrapper — the system serializes Python sets as `{"__set__": [list]}`.

---

## Output: a single HTML file with 5 sections

### Section 1: Header banner

A styled banner at the top showing:
- Scenario description (large title)
- Agent names as pills/badges
- Variable count summary: "N variables (M exogenous causes → K endogenous outcomes)"

### Section 2: Causal DAG (Graphviz SVG)

Use the `graphviz` Python library to render the causal graph as an SVG, then embed it inline in the HTML.

**Graph construction:**
1. Create a `graphviz.Digraph` with `rankdir="LR"` (left-to-right flow).
2. Set graph attributes: `bgcolor="transparent"`, `fontname="Helvetica"`, `pad="0.5"`.
3. For each **exogenous** variable, add a node with:
   - `shape="box"`, `style="rounded,filled"`, `fillcolor="#e8f4f8"`, `color="#2196F3"`, `fontcolor="#1565C0"`
   - Label: the variable name, wrapped at ~30 characters using `\n`.
   - A subtitle line in smaller font showing the variable type and units, e.g., `<BR/><FONT POINT-SIZE="9" COLOR="#666666">binary · binary</FONT>`. Use an HTML label (`< >` syntax) to achieve this.
4. For each **endogenous** variable, add a node with:
   - `shape="box"`, `style="rounded,filled"`, `fillcolor="#fff3e0"`, `color="#FF9800"`, `fontcolor="#E65100"`
   - Same label wrapping and subtitle treatment.
5. For each edge in `edge_dict`, add an edge with `color="#455a64"`, `penwidth="1.5"`, `arrowsize="0.8"`.
6. Render to SVG string with `graph.pipe(format='svg').decode('utf-8')`.
7. Embed the SVG directly in the HTML.

### Section 3: Variable detail cards

Render each variable as an HTML card. Use a two-column responsive grid (CSS grid or flexbox).

**Endogenous variable card** — orange/amber accent:
```
┌──────────────────────────────────────────────┐
│  ◉ OUTCOME                                    │
│  <variable name>                               │
│                                                │
│  Type      binary (binary decision)            │
│  Levels    0, 1                                │
│                                                │
│  Operationalization                            │
│  <operationalization text>                     │
│                                                │
│  Measurement                                   │
│  Ask <agent>: "<question>"                     │
│  Aggregation: <method>                         │
│                                                │
│  Caused by                                     │
│  [cause1 pill] [cause2 pill] [cause3 pill]     │
└──────────────────────────────────────────────┘
```

**Exogenous variable card** — blue accent:
```
┌──────────────────────────────────────────────┐
│  ◈ CAUSE                                      │
│  <variable name>                               │
│                                                │
│  Type      continuous (centimeters)            │
│  Levels    below 160, 160-170, ...             │
│  Scope     individual → job applicant          │
│                                                │
│  Operationalization                            │
│  <operationalization text>                     │
│                                                │
│  Experimental variation                        │
│  Attribute: "<attribute_name>"                 │
│  Agent: <varied_agent>                         │
│  Values: val1 | val2 | val3 | ...   (public)  │
│  Public name: "<public_name>"                  │
│                                                │
│  Effects → [outcome pill]                      │
└──────────────────────────────────────────────┘
```

Style details:
- Cards have a left border (4px) in the accent color (blue for exogenous, amber for endogenous).
- Background: white with subtle shadow.
- "Caused by" and "Effects" items rendered as small rounded pills with the target variable's accent color.
- The attribute values in the exogenous card rendered as a horizontal row of monospace pills/chips.

### Section 4: Experimental design matrix

An HTML table with:
- **Header row:** Variable | Agent | Attribute | Treatment values (one column per value, or a single "Values" column with chips)
- **One row per exogenous variable**
- Cell styling: header row with dark background (#37474f, white text), alternating row colors, treatment value cells in monospace.
- A visibility icon or badge in each row: 🔓 public / 🔒 private.
- Below the table, a summary line: **"Total experimental cells: N"** (product of all attribute_values counts) with the multiplication shown (e.g., "2 × 5 × 8 = 80").

### Section 5: Agent profiles

One card per agent, arranged horizontally.

Each card shows:
- **Agent name** as a header
- **Goal** (if available in blueprint)
- **Constraint** (if available)
- **Own varied attributes:** For each exogenous variable where this agent is the `varied_agent`, list the attribute name and values as chips, with a 🔒/🔓 badge.
- **Receives from others:** For each exogenous variable where `public_or_private_var.choice == "public"` and this agent is NOT the `varied_agent`, list the `public_name` and `public_values`.

If goal/constraint are not present in the blueprint, omit those rows.

---

## CSS guidelines

Use inline `<style>` in the HTML `<head>`. Target a clean, modern look:

```css
body          { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background: #f5f5f5; color: #212121; max-width: 1200px;
                margin: 0 auto; padding: 2rem; }
h1            { font-size: 1.6rem; }
.badge        { display: inline-block; padding: 2px 10px; border-radius: 12px;
                font-size: 0.85rem; margin: 2px; }
.agent-badge  { background: #e0e0e0; color: #424242; }
.card         { background: #fff; border-radius: 8px; padding: 1.25rem;
                margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.card-exo     { border-left: 4px solid #2196F3; }
.card-endo    { border-left: 4px solid #FF9800; }
.chip         { display: inline-block; padding: 2px 8px; border-radius: 4px;
                font-family: monospace; font-size: 0.85rem; margin: 1px;
                background: #f5f5f5; border: 1px solid #e0e0e0; }
table         { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
th            { background: #37474f; color: #fff; padding: 8px 12px;
                text-align: left; }
td            { padding: 8px 12px; border-bottom: 1px solid #e0e0e0; }
tr:nth-child(even) { background: #fafafa; }
.section-title { font-size: 1.2rem; font-weight: 600; margin: 2rem 0 1rem;
                 color: #37474f; border-bottom: 2px solid #e0e0e0;
                 padding-bottom: 0.3rem; }
.card-grid    { display: grid; grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
                gap: 1rem; }
.agent-grid   { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 1rem; }
.label        { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;
                color: #757575; margin-top: 0.75rem; margin-bottom: 0.25rem; }
```

---

## Script structure

The generated Python script should:

```python
import json, sys, html
import graphviz

def load_blueprint(path):
    """Load and unwrap the blueprint JSON."""
    with open(path) as f:
        raw = json.load(f)
    if isinstance(raw, str):
        raw = json.loads(raw)
    if "class" in raw and "args" in raw:
        raw = raw["args"]
    return raw

def unwrap_edges(edge_dict):
    """Convert __set__ wrappers to plain lists."""
    out = {}
    for cause, targets in edge_dict.items():
        if isinstance(targets, dict) and "__set__" in targets:
            out[cause] = targets["__set__"]
        elif isinstance(targets, list):
            out[cause] = targets
        else:
            out[cause] = list(targets)
    return out

def get_var_args(var_entry):
    """Extract the args dict from a variable_dict entry."""
    if "args" in var_entry:
        return var_entry["args"]
    return var_entry

def is_exogenous(var_entry):
    return var_entry.get("class") == "ExogenousVariable"

def render_dag_svg(bp, edges):
    """Build and render the Graphviz DAG, return SVG string."""
    ...

def build_html(bp):
    """Assemble the full HTML string."""
    ...

def main():
    path = sys.argv[1]
    bp = load_blueprint(path)
    output = sys.argv[2] if len(sys.argv) > 2 else path.replace('.json', '_viz.html')
    html_str = build_html(bp)
    with open(output, 'w') as f:
        f.write(html_str)
    print(f"Wrote {output}")

if __name__ == "__main__":
    main()
```

Usage: `python visualize_blueprint.py blueprint.json [output.html]`

---

## Example

For the "lawyer interview" blueprint, the output HTML should render as:

**Header:**
> # A person is interviewing for a job as a lawyer
> `job applicant` `employer`
> 4 variables (3 exogenous causes → 1 endogenous outcome)

**DAG:** A left-to-right graph with three blue rounded boxes on the left each with an arrow pointing to one amber rounded box on the right.

**Cards:** Four cards — one amber-bordered outcome card, three blue-bordered cause cards.

**Experimental matrix:**

| Variable | Agent | Attribute | Values | Visibility |
|---|---|---|---|---|
| whether the applicant passed the bar exam | job applicant | your bar exam status | `not passed` `passed` | public |
| the interviewer's level of friendliness | employer | number of positive phrases to use | `2` `7` `12` `17` `22` | private |
| the job applicant's height | job applicant | your height in centimeters | `160` `165` `170` `175` `180` `185` `190` `195` | public |

**Total experimental cells: 80** (2 x 5 x 8)

**Agent profiles:** Two cards side by side showing each agent's attributes and what they receive from others.
