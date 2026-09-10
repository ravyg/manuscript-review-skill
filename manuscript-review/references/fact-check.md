# Pass 3 — Fact-check

Every claim must be supported; every citation accurate; every number consistent. You verify —
you never edit the paper.

## Claim extraction
Sweep the paper and bucket verifiable claims:
- **Factual** — statements about the world / prior results ("BERT achieves 92.3% on SQuAD 2.0").
- **Methodological** — "our model has X params", "trained for Y epochs", complexity claims.
- **Results** — "we achieve X% on Y", "outperform Z by N points", "state-of-the-art", "first to".
- **Attribution** — "Smith et al. proposed X" — did they? "Unlike prior work, we…" — accurate?

## Verification procedures
**Citations** (live-check if web is available; else audit internal consistency and mark
*unverified*): (1) the work exists (search exact title); (2) authors + year match; (3) the cited
claim actually appears in that work; (4) flag misrepresentations of cited work — common and
damaging.

**Statistics:** cross-reference against original sources; check baselines match the original
papers; verify comparisons are fair (same split, same metric); flag implausible numbers.

**Novelty:** search for prior work doing the same thing; scrutinize "first to" / "SOTA" claims;
flag contribution claimed that actually belongs to prior work.

**Internal consistency:** text numbers vs tables/figures; abstract claims vs actual results;
conclusion claims vs evidence; contradictions across sections.

## Severity
| Level | Meaning |
|---|---|
| 🔴 Critical | Factually wrong, misattributed, or fabricated → must fix |
| 🟡 Warning | Potentially misleading, unverifiable, or overclaimed → investigate |
| 🟢 Verified | Confirmed accurate |
| ⚪ Unchecked | Could not verify (no source/web access) → note for manual check |

Flag **soft overclaiming** too: "dramatically improves" for a 0.5% gain is misleading even if
technically true.

## Output into the findings object
- `fact_check[]` — one row per checked claim: `{claim, location, status, evidence, source}`.
- Critical falsehoods/misattributions → also `priority_fixes[]`.
- If web was unavailable, add that to `meta.capabilities_skipped`.
