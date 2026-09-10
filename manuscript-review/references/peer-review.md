# Pass 1 — Peer review (3 lenses)

Simulate a panel of three distinct reviewers. Let them disagree where a real panel would.

## The three lenses
- **Reviewer 1 — Methodologist.** Experimental design, statistical validity, reproducibility.
  Concerns: missing baselines, insufficient ablations, improper tests, data leakage, no error
  analysis, results that don't actually support the claims.
- **Reviewer 2 — Domain Expert.** Novelty, positioning, completeness of related work,
  significance. Concerns: incremental contribution, missing related work, overclaimed novelty,
  narrow evaluation, limited applicability.
- **Reviewer 3 — Clarity Advocate.** Writing, logical flow, figure quality, accessibility.
  Concerns: unclear motivation, poor notation, inconsistent terminology, buried key results,
  missing intuition/examples.

## Procedure
1. **Evidence extraction first (no opinions yet).** Pull: the central question/hypothesis; a
   2–3 sentence method summary; key findings and what the authors say they mean; and 3–5 direct
   quotes anchoring the primary claims (with section references).
2. **Evaluate per lens** across: methodology & rigor; novelty & contribution; clarity &
   presentation; significance & impact.
3. **Score each reviewer 1–10** and write a 2–3 paragraph review in that reviewer's voice.
4. **Meta-review (area chair):** synthesize, surface disagreements, give an overall
   recommendation.

## Scoring rubric
| Score | Label | Criteria |
|---|---|---|
| 9–10 | Strong Accept | Novel, rigorous, clear, significant |
| 7–8 | Weak Accept | Solid, minor issues, clear contribution |
| 5–6 | Borderline | Merit but notable weaknesses; needs revision |
| 3–4 | Weak Reject | Significant methodology/novelty/clarity issues |
| 1–2 | Strong Reject | Fundamental flaws or insufficient contribution |

## Output into the findings object
- `reviewers[]` — one entry per lens: `{persona, score, review}`.
- `priority_fixes[]` — each major issue as `{severity, title, what, why, fix}`; every criticism
  gets a concrete suggested fix.
- Minor issues → `section_findings[]` grouped by section.

## Guidelines
Be specific (quote the location). Be constructive (fix with every criticism). Be fair
(acknowledge genuine strengths). Be calibrated (solid ≠ groundbreaking, and that's fine).
