# Pass 5 — Writing quality & AI-writing detection

Evaluate the prose as a demanding reader would, and flag machine-generated / low-effort writing.
Propose rewrites as *suggestions* — never edit the author's file.

## Writing evaluation (four sub-passes)
- **Clarity.** Undefined jargon; sentences >30 words; paragraphs without a clear topic sentence;
  notation used before definition; redundancy ("novel and new", "important and significant").
- **Precision.** Unscoped claims ("always", "proves") that should be hedged ("in our
  experiments", "provides evidence"); ambiguous "this"/"it" referents; numbers that disagree with
  the results; inconsistent terminology (one concept, several names).
- **Flow.** Do paragraphs follow logically? Does the intro promise what the paper delivers? Does
  the conclusion reflect actual (not aspirational) results? Does the abstract match the paper?
- **Impact.** Weak opening hook; vague contribution statement; buried key result; a title that
  isn't specific/searchable.

### Style tells (prefer the left column)
| Prefer | Flag |
|---|---|
| "We propose X, which achieves Y" | "We propose a novel framework" (says nothing) |
| "Table 2 shows that…" | "As can be seen from Table 2…" (wordy) |
| "X outperforms Y by 3.2% on Z" | "X significantly outperforms Y" (vague) |
| "This has two limitations" | "This is not without limitations" (hedge) |

## AI-writing / low-effort signals (report as signals, not proof)
- Uniform, template-like paragraph shapes; heavy "Furthermore/Moreover/Additionally" scaffolding.
- Empty intensifiers and hedge-stacking; generic sentences with no specific numbers or citations.
- Section-boundary boilerplate ("In this section, we…") and restated-abstract conclusions.
- Contradictions between confidently-worded claims and the actual results.
- Placeholder residue ("[TBD]", "___", "insert citation"), broken/garbled URLs, malformed refs.

Report these as **observations with examples**, calibrated ("several signals consistent with
AI-assisted drafting"), never as an accusation or a definitive verdict.

## Output into the findings object
- Concrete before→after suggestions → `rewrites[]`: `{location, original, suggested, why}`.
- Systemic writing problems → `priority_fixes[]`; local ones → `section_findings[]`.
- Scorecard note for the **Clarity** dimension; AI-writing signals summarized there or in
  `section_findings` under "Writing".
