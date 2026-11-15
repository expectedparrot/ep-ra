# Blueprint Design: 12-Step Process

## Contents

- [Step 1: Identify the Agents](#step-1-identify-the-agents)
- [Step 2: Generate Outcome Variables](#step-2-generate-outcome-variables)
- [Step 3: Operationalize the Outcome Variable](#step-3-operationalize-the-outcome-variable)
- [Step 4: Classify Variable Type, Units, and Levels](#step-4-classify-variable-type-units-and-levels)
- [Step 5: Create Measurement Questions](#step-5-create-measurement-questions)
- [Step 6: Identify Causal Variables](#step-6-identify-causal-variables-exogenous-causes)
- [Step 7: Build Each Causal Variable](#step-7-build-each-causal-variable)
- [Step 8: Define Agent Interaction Protocol](#step-8-define-agent-interaction-protocol)
- [Step 9: Define Agent Goals and Constraints](#step-9-define-agent-goals-and-constraints)
- [Step 10: Determine Additional Agent Attributes](#step-10-determine-additional-agent-attributes)
- [Step 11: Construct the Causal Graph](#step-11-construct-the-causal-graph-edge-dictionary)
- [Step 12: Assemble the Blueprint JSON](#step-12-assemble-the-blueprint-json)
- [Worked Example](#worked-example)

---

Given a natural-language scenario description, produce a **blueprint** — a structured JSON document that fully specifies the agents, variables, causal structure, experimental conditions, and measurement protocol needed to run the simulation.

Work through the following steps in order. Each step produces a specific piece of the blueprint. At the end, assemble the pieces into the final JSON.

---

## Step 1: Identify the Agents

Given the scenario description, determine who the individual human agents are.

**Rules:**
- Every agent must be a singular individual with a named role (e.g., "buyer", "seller" — not "person 1", "person 2").
- Never list a plurality as a single agent. If there are multiple jurors, list them as "juror 1", "juror 2", etc.
- Only include agents who would speak during the scenario.
- There must be at least two agents.

**Output:** a list of agent role names.

**Example:**
- Scenario: "A person interviewing for a job as a lawyer"
- Agents: `["job applicant", "employer"]`

---

## Step 2: Generate Outcome Variables

Propose interesting outcome variables that could be measured from the scenario.

**Rules:**
- Outcomes must be measurable during or by the end of a single simulation run. They cannot depend on events before or after the scenario.
- Outcomes must not be directional (e.g., "final price of the car", not "high final price").
- Each outcome must refer to a single agent or the scenario as a whole — never a subset of multiple agents.
- Outcomes must be easily operationalizable as continuous, ordinal, count, or binary variables. No nominal categoricals (e.g., not "the destination chosen" but "the price of the vacation").
- Cannot refer to elapsed time (seconds, minutes), though counts of statements are fine.
- The most interesting outcomes are typically about how the main point of the scenario concluded.

**Output:** a list of candidate outcome variable names. Select one to be the primary outcome for the blueprint.

---

## Step 3: Operationalize the Outcome Variable

For the chosen outcome, define exactly how it will be quantified.

**Rules:**
- Select exactly one operationalization.
- Be explicit about how the variable is quantified and how the quantity is obtained.
- The operationalization must translate the variable into exactly one of: binary, continuous, count, or ordinal.
- Ordinal variables must have all values explicitly listed (not a numerical scale). Generally no more than 5 categories.
- Information can only be gathered from: (a) the text transcript of the simulation, or (b) post-scenario questions to the agents.
- Cannot rely on external rubrics or standards unless fully spelled out.
- The variable's value must be determinable by the end of the simulation (not after).

**Output:**
```json
{
  "operationalization": "description of how variable is quantified",
  "method_to_obtain_quantity": "how to get the value (transcript analysis, agent questions, etc.)"
}
```

---

## Step 4: Classify Variable Type, Units, and Levels

For the operationalized outcome:

### 4a. Classify type
Determine if the variable is `continuous`, `binary`, `count`, or `ordinal`.
- Scales → ordinal
- Counts of something → count
- Categories with order (low/medium/high) → ordinal
- Time, currency, numerical values → continuous
- Exactly two possible values → binary

### 4b. Determine units
- Monetary → "dollars"
- Time → "seconds"
- Made-up scale → "likert scale"
- Count → "count of [quantity]"
- Original category → "level of [category]"

### 4c. Create levels
- **Continuous/count:** Create ~5 ordinal bins with numerical cutoffs. Use ranges (e.g., "0-20", "21-40"), not single values. Include a "+" or "above" option if there is no natural maximum. Make bins appropriately sized for the domain (a mug price should be "0-5", "5-10", "10-20", "20+" — not "0-50", "50-100").
- **Ordinal:** List all possible values (e.g., `["low", "medium", "high"]`).
- **Binary:** List both values, smallest/worst first (e.g., `["0", "1"]`).
- All levels must be mutually exclusive and ordered smallest to largest.

---

## Step 5: Create Measurement Questions

Design post-scenario questions to obtain the variable's value from the agents.

**Rules:**
- Questions must be clear and unambiguous — agents cannot ask for clarification.
- Prefer asking agents directly over transcript analysis (agents answer honestly and have perfect memory).
- Use "oracle" as the agent name for questions answered by transcript analysis. The oracle only sees the transcript, not agents' inner thoughts.
- Ask as few questions as possible. Only ask more than one if absolutely necessary (e.g., the variable is a sum/average).
- Maximum one question per agent (including oracle).
- If the variable is ordinal with specific levels, the question must present those levels as the only acceptable answers.
- Specify an aggregation method if multiple questions are needed: min, max, average, mode, median, or sum. If only one question, state "no aggregation necessary."

**Output:**
```json
{
  "agent_name": ["question for this agent"],
  "aggregation": "method or 'no aggregation necessary'"
}
```

---

## Step 6: Identify Causal Variables (Exogenous Causes)

For the outcome variable, identify causes that can be experimentally manipulated.

**Rules:**
- Causes must be determined **before** the scenario begins (they are exogenous treatments).
- Must not be about perceptions, impressions, or opinions formed during the scenario.
- Must be non-directional ("buyer's income", not "high income of the buyer").
- Must refer to a single named agent or the scenario as a whole — never multiple agents or an unnamed agent.
- Must not refer to multiple values/preferences (not "the mother's preferences" but "whether the mother likes beaches").
- Must be simple to operationalize as continuous, ordinal, count, or binary. No nominal categoricals.
- Cannot refer to the number of agents, agents not in the scenario, or interactions between agents.
- Should support at least 5 levels of variation for ordinal operationalization.
- Must be new — not already in the model as an outcome or other variable.

**Output:** a list of cause variable names. Typically select 1-3 for the blueprint.

---

## Step 7: Build Each Causal Variable

For each selected cause, repeat a process similar to Steps 3-4, plus additional steps specific to exogenous variables:

### 7a. Operationalize the cause
Same rules as Step 3, but emphasize that the variable is determined before the scenario. Instead of `method_to_obtain_quantity`, specify `method_to_vary` — how values will be used to create experimental variation.

### 7b. Classify type, units, levels
Same as Step 4.

### 7c. Check if truly exogenous
Verify the variable is determined before (not during) the scenario. Attributes of agents (skills, experiences, emotions, status) are pre-scenario. If it turns out to be determined during the scenario, reclassify it as endogenous and treat it like another outcome.

### 7d. Determine scope: individual agent or scenario-wide
- **Individual:** variation applies to one specific agent (e.g., "buyer's reservation price" → individual, buyer).
- **Scenario:** variation applies to all agents equally (e.g., "size of the room" → scenario).

### 7e. Induce variation through an attribute

**For individual-scope variables:**
- Choose which agent receives the varied attribute.
- Create an attribute name in second person or neutral form — not third person (e.g., "your annual income", not "buyer's annual income").
- Map variable levels to concrete attribute values the agent will be told.
- For continuous/count variables: use numerical values and provide at least 7 values.
- For ordinal variables: use descriptive words, not numbers (e.g., "bad", "decent", "good" — not "1", "2", "3"). The agent receives no context beyond the attribute, so values must be self-explanatory.
- If levels are ranges, pick a single representative value within each range.
- Keep the attribute as close to the original variable name as possible in meaning and units.

**For scenario-scope variables:**
- Same rules, but the attribute will be given to all agents.
- The attribute name must not reference any specific agent in third person.

### 7f. Align variation across causes
If there are multiple exogenous causes, check that their experimental value ranges make sense together. For example, if "seller's value for the mug" is varied over $50-$400 but "buyer's budget" is varied over $5-$25, no deal will ever happen and the experiment yields false negatives. Adjust ranges so they overlap appropriately. Ensure at least 7 values for continuous/count variables.

### 7g. Determine public vs. private
Decide whether each varied attribute should be known to all agents (public) or only the relevant agent (private).
- Make the decision based on what would be realistic and observable in the real-world scenario.
- Physically visible attributes (height, clothing) → public.
- Strategic information (reservation price, budget) → private.
- If public, provide a third-person name for the attribute as seen by other agents (e.g., "your bar exam status" becomes "the bar exam status of the job applicant" for the employer).

---

## Step 8: Define Agent Interaction Protocol

Choose how agents communicate from these options:

| Type | Description |
|---|---|
| **ordered** | Agents speak in a fixed, repeating order |
| **random** | Random speaker each turn (no consecutive repeats) |
| **center ordered** | One central agent alternates with ordered non-central agents |
| **center random** | One central agent alternates with random non-central agents |
| **oracle before** | An external oracle reads the transcript and picks the next speaker |
| **oracle after** | All agents respond each turn; an oracle picks which response is "real" |

Choose whichever makes the conversation most realistic. For a simple two-person scenario, "ordered" is typically correct.

If "ordered" or "center ordered", also specify the speaking order.
If "center ordered" or "center random", specify which agent is the central agent.

---

## Step 9: Define Agent Goals and Constraints

For each agent:

### Goal
- One goal per agent, written in second person as an instruction.
- Must be rational, expressible during the simulation, and under the agent's control.
- Cannot be about initiating or limiting interactions with other agents.

### Constraint
- Zero or one constraint per agent.
- Only include constraints that are absolutely necessary to prevent irrational behavior (e.g., "you will not accept a price below your value for the mug").
- Written in second person.
- Must be about limiting decisions, not prescribing actions.
- If no constraint is obviously necessary, use "you have no constraints."

---

## Step 10: Determine Additional Agent Attributes

For each agent, determine what minimal background information they need beyond what they already know. Agents already know:
- The scenario description and their role
- Their own goal and constraint
- The presence and roles of other agents
- Their experimentally varied attributes (from Step 7e)

They do NOT know:
- Other agents' goals, constraints, or private attributes
- Anything about the variables, operationalizations, or experimental design

Only include information that is **absolutely essential** for the agent to participate.

---

## Step 11: Construct the Causal Graph (Edge Dictionary)

Define the causal edges: each exogenous cause points to the outcome(s) it affects.

```json
{
  "cause_variable_name": ["outcome_variable_name"],
  "another_cause": ["outcome_variable_name"]
}
```

---

## Step 12: Assemble the Blueprint JSON

Combine everything into a single structured document:

```json
{
  "scenario_description": "the original scenario text",
  "agents_in_scenario": ["agent1", "agent2"],
  "variables": ["outcome_var", "cause_var_1", "cause_var_2"],
  "edge_dict": {
    "cause_var_1": ["outcome_var"],
    "cause_var_2": ["outcome_var"]
  },
  "interaction_type": "ordered",
  "agent_order": ["agent1", "agent2"],
  "variable_dict": {
    "outcome_var": {
      "type": "endogenous",
      "name": "...",
      "operationalization_dict": {
        "operationalization": "...",
        "method_to_obtain_quantity": "..."
      },
      "variable_type": "binary|continuous|count|ordinal",
      "units": "...",
      "levels": ["..."],
      "causes": ["cause_var_1", "cause_var_2"],
      "agent_measure_question_dict": {
        "agent_name": ["question"]
      },
      "measurement_aggregation": "..."
    },
    "cause_var_1": {
      "type": "exogenous",
      "name": "...",
      "operationalization_dict": {
        "operationalization": "...",
        "method_to_vary": "..."
      },
      "variable_type": "binary|continuous|count|ordinal",
      "units": "...",
      "levels": ["..."],
      "descendant_outcomes": ["outcome_var"],
      "scenario_or_agent_var": {
        "variable_scope": "individual|scenario",
        "relevant_entity": "agent_name|scenario"
      },
      "attribute_variation": {
        "attribute_name": "the attribute as told to the agent",
        "attribute_values": ["val1", "val2", "..."],
        "varied_agent": "agent_name|scenario"
      },
      "public_or_private_var": {
        "choice": "public|private",
        "public_name": "third-person name or 'private'",
        "public_values": ["val1", "val2"]
      }
    }
  },
  "agents": {
    "agent1": {
      "goal": "...",
      "constraint": "...",
      "additional_attributes": ["..."]
    },
    "agent2": {
      "goal": "...",
      "constraint": "...",
      "additional_attributes": ["..."]
    }
  }
}
```

---

## Worked Example

**Scenario:** "A person is interviewing for a job as a lawyer"

1. **Agents:** `["job applicant", "employer"]`
2. **Outcome:** "the decision of the employer to hire or not hire"
3. **Operationalization:** binary — 1 if hired, 0 if not. Obtained by asking the employer.
4. **Type/units/levels:** binary, "binary decision", `["0", "1"]`
5. **Measurement:** Ask employer: "have you decided to hire the job applicant?" → yes=1, no=0
6. **Causes:** "whether the applicant passed the bar exam", "the job applicant's height"
7. **Bar exam cause:**
   - Operationalization: binary, 1=passed, 0=not passed
   - Scope: individual → job applicant
   - Attribute: "your bar exam status" → `["not passed", "passed"]`
   - Public: yes → "the bar exam status of the job applicant"
8. **Height cause:**
   - Operationalization: continuous in centimeters
   - Scope: individual → job applicant
   - Attribute: "your height in centimeters" → `["160", "165", "170", "175", "180", "185", "190", "195"]`
   - Public: yes → "the height of the job applicant in centimeters"
9. **Interaction:** ordered → `["job applicant", "employer"]`
10. **Goals:** job applicant: "present yourself as a strong candidate"; employer: "evaluate the candidate's qualifications"
11. **Causal graph:** bar exam → hiring decision; height → hiring decision
