# Social Science Publication Quality Guide

## Contents
- [What counts as a credible source](#what-counts-as-a-credible-source)
- [Reputable journals by field](#reputable-journals-by-field)
- [Credible preprints](#credible-preprints)
- [Evidence hierarchy](#evidence-hierarchy)
- [Appraising individual studies](#appraising-individual-studies)
- [Red flags](#red-flags)

---

## What counts as a credible source

For this context (social science research informing survey/experiment design), prioritize:

1. **Peer-reviewed journal articles** in reputable field journals (see list below)
2. **Working papers from NBER, arXiv (econ/cs), or SSRN** by authors at research universities — these are often published work in progress and frequently cited before formal publication
3. **Pre-prints from recognized researchers** — check: Do the authors have a faculty position at a doctoral-granting university? Do they have prior publications in reputable venues?

Do not treat as primary literature:
- Industry white papers, consulting reports, or think-tank publications (useful for context, not evidence)
- Journalism, blog posts, or op-eds
- Conference proceedings from minor venues without peer review
- Dissertations (can be cited, but treat as low-weight until published)

---

## Reputable journals by field

These lists are not exhaustive. When in doubt, check: Is the journal indexed in SSCI or Scopus? Does it have a multi-year impact factor? Is it published by a major academic press (APA, AEA, Elsevier, Springer, Sage, MIT Press, Oxford, Cambridge)?

### Economics
**Top-5 general** (highest bar; empirical work here is very well vetted):
American Economic Review · Quarterly Journal of Economics · Journal of Political Economy · Econometrica · Review of Economic Studies

**Top field journals:**
- Labor/behavioral: Journal of Labor Economics, American Economic Journal (AEJ: Applied, Micro, Macro, Policy)
- Public/health: Journal of Public Economics, Journal of Health Economics
- Industrial org: RAND Journal of Economics, Journal of Industrial Economics
- Finance: Journal of Finance, Review of Financial Studies, Journal of Financial Economics
- Development: Journal of Development Economics, American Economic Journal: Applied Economics

### Psychology
**Top general:** Psychological Science · Journal of Personality and Social Psychology (JPSP) · Journal of Experimental Psychology: General · Psychological Review · Annual Review of Psychology

**Behavioral / decision:** Journal of Behavioral Decision Making · Organizational Behavior and Human Decision Processes · Journal of Experimental Social Psychology · Cognition

**Applied/health:** Health Psychology · Journal of Applied Psychology · Social Psychology and Personality Science

### Marketing and consumer behavior
Journal of Marketing Research (JMR) · Journal of Consumer Research (JCR) · Journal of Marketing · Marketing Science · Journal of the Academy of Marketing Science · Journal of Consumer Psychology

### Management and organizational behavior
Management Science · Administrative Science Quarterly · Academy of Management Journal · Strategic Management Journal · Journal of Management · Organization Science

### Sociology
American Journal of Sociology · American Sociological Review · Social Forces · Sociological Science · Annual Review of Sociology

### Political science
American Political Science Review · American Journal of Political Science · Journal of Politics · Political Psychology · Public Opinion Quarterly

### Information systems and human-computer interaction
MIS Quarterly · Information Systems Research · Journal of Management Information Systems · CHI (ACM proceedings — peer-reviewed and well-regarded)

### Public health and epidemiology
American Journal of Public Health · American Journal of Epidemiology · Social Science & Medicine · Health Affairs · PLOS Medicine

### Multidisciplinary (very high prestige)
Nature · Science · Nature Human Behaviour · PNAS · PLOS ONE (open access, broad but peer-reviewed)

---

## Credible preprints

### NBER Working Papers (nber.org)
High credibility. NBER is a selective research organization; working papers are by invitation-only NBER affiliates (faculty at top economics departments). Many are in review at or forthcoming in top journals. Treat NBER WPs as credible evidence — note they are not yet peer-reviewed.

### arXiv — Economics (econ.GN, econ.EM, etc.)
Growing rapidly. Quality varies widely — anyone can post. Check author affiliations (faculty page at a research university? Prior publications?). Preprints from researchers at top departments with prior publication records are credible; anonymous or unaffiliated authors are not.

### arXiv — Computer Science (cs.AI, cs.CY, cs.HC)
High volume. For AI/LLM-related social science questions, look for authors at AI research labs (DeepMind, Google Brain, MSR, FAIR, OpenAI) or top CS departments. Conference papers (NeurIPS, ICML, ACL, FAccT, CHI) that appear on arXiv are usually peer-reviewed; standalone arXiv-only papers need author credential check.

### SSRN (ssrn.com)
Widely used in economics, law, finance, and management. Quality varies. Check author affiliation and citation count (SSRN shows downloads; Google Scholar shows citations). Papers posted by faculty at doctoral-granting institutions are generally credible.

### OSF Preprints (osf.io)
Psychology, social science, education. Often associated with pre-registration. Check if the preprint has a registered protocol — this is a strong positive quality signal.

---

## Evidence hierarchy

For establishing causal claims (which is usually what matters for study design), rank evidence in this order:

1. **Meta-analysis / systematic review** — quantitative synthesis of many studies; most reliable for establishing effect sizes and moderators
2. **Pre-registered randomized experiment** (RCT, field experiment, lab experiment with pre-registration) — causal identification, minimal researcher degrees of freedom
3. **Unregistered randomized experiment** — causal, but higher risk of p-hacking or selective reporting
4. **Natural experiment / quasi-experiment** (instrumental variables, difference-in-differences, regression discontinuity) — credible causal identification from observational data
5. **Cross-sectional survey with controls** — establishes associations; causal interpretation requires strong theoretical justification
6. **Qualitative or single case study** — useful for mechanism and construct development; not quantitative evidence of effects

For descriptive claims (prevalence, base rates, attitudes), a well-sampled representative survey is often the strongest available evidence regardless of design.

---

## Appraising individual studies

When reading a paper, evaluate these dimensions and record them in your dewey notes:

### Internal validity (did the study measure what it claims?)
- Is the design appropriate for the claim (correlation vs. causation)?
- Is there a credible identification strategy for causal claims?
- Was the study pre-registered? (Check OSF, AsPredicted, AEA RCT Registry)
- Are there demand characteristics, social desirability, or experimenter effects?
- Is the operationalization of key constructs face-valid? (Does the measure actually capture the concept?)

### External validity (does it generalize?)
- What is the sample? Is it a convenience sample (MTurk, students) or a representative / probability sample?
- Is it a convenience sample (MTurk, students) or a representative / probability sample?
- Is the context generalizable? (Lab vs. field, hypothetical vs. real stakes)
- What is the population studied, and does it match your target population?

### Statistical quality
- Is the sample size adequate given the expected effect size? (Underpowered studies overestimate effects)
- Are effect sizes reported, not just p-values?
- Are confidence intervals provided?
- Is there a multiple comparisons correction if many outcomes were tested?
- Does the paper report null results, or does it only show significant findings? (Publication bias risk)

### Replication and robustness
- Has this finding been replicated? By whom? (Same lab vs. independent replication)
- Are results robust across different model specifications or subgroups?
- Does the paper report robustness checks?

---

## Red flags

Be skeptical of a paper if:
- Effect sizes are very large for a social science finding (d > 0.8, r > 0.5 for observational work) without a strong mechanism — may reflect p-hacking or publication bias
- The sample is all-student or all-MTurk and the claim is about the general population
- The paper was published in a pay-to-publish predatory journal (check Beall's List or journal ISSN)
- There are no confidence intervals or effect sizes — just p-values
- The study is a single cross-sectional survey making causal claims without identification strategy
- The paper has been the subject of replication failures (check PubPeer, Retraction Watch, Google Scholar for citing papers)
- Pre-registration is claimed but the registered protocol wasn't followed (HARKing: hypothesizing after results known)
- The preprint has been online for years with no journal submission — may have failed peer review
