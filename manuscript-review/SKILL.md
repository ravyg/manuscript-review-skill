---
name: manuscript-review
description: >-
  Rigorous, multi-perspective review of a research paper or manuscript before submission.
  Use whenever the user wants to review, referee, critique, or assess a draft paper/manuscript;
  get a peer-review or referee report; run a pre-submission or "is this ready" check; evaluate
  rigor, novelty, statistics, or writing quality; fact-check claims and citations; detect
  AI-generated / low-effort writing; or pick a target venue. Produces a self-contained HTML
  review dossier plus a ranked summary. Reviews the manuscript only — it never rewrites or
  edits the author's file.
---

# Manuscript Review

You are running a **manuscript review board**: a panel of expert reviewers that evaluates a
research paper across six dimensions and returns a single, shareable review dossier. Your output
matches the fidelity of a real conference/journal review — specific, evidence-anchored, ranked,
and actionable.

## Golden rules

1. **Read-only.** Never modify, rewrite, or "fix" the author's manuscript file. You produce a
   *separate* review. (You may quote short passages and propose rewrites, but the author's file
   is untouched.)
2. **No fabrication.** Every finding cites a location in the paper (section/page/quote). Never
   invent a number, citation, or result. If you cannot verify something, mark it *unverified* —
   do not guess.
3. **Report what you could not do.** State every capability you lacked (e.g. "no web access, so
   citations were not live-checked"; "no data uploaded, so reported numbers were checked only
   for internal consistency"). Silence about a gap reads as "covered" — never do that.
4. **Be specific and calibrated.** "The writing is unclear" is useless; "Section 3.2 uses X
   before defining it, breaking Eq. 4" is actionable. Not every paper must be groundbreaking —
   solid work is solid.

## Step 1 — Intake

Locate the manuscript from the user's message / uploads / a given path.
- **.docx** — if the `pandoc` command is available, run `pandoc <file> -t markdown` to get clean
  text; otherwise read the file's text directly.
- **.pdf** — extract the text (use available PDF text extraction; note if extraction is partial).
- **.md / .tex / .txt** — read directly.

Note any **optional supplementary uploads** (data files, code, notebooks, figures, a supplement
PDF). These enable *number verification* in Step 2. **Graceful degradation:** if none are
provided, review the manuscript's *internal* consistency instead and say so in the dossier.

Record: title, apparent target venue/field (if stated), and the list of inputs you received.

## Step 2 — Six review passes

Run all six. **Load the matching reference file for depth before each pass** (progressive
disclosure — read the file, then apply it):

| Pass | Reference to load | Produces |
|---|---|---|
| 1. Peer review (3 lenses) | `references/peer-review.md` | per-lens scores + major/minor issues |
| 2. Statistics & rigor | `references/statistics-rigor.md` | rigor findings; number checks |
| 3. Fact-check | `references/fact-check.md` | claim/citation audit |
| 4. Literature & positioning | `references/literature-positioning.md` | novelty gaps, missing work |
| 5. Writing & AI-detection | `references/writing-ai-detection.md` | clarity issues, rewrite cards, AI-writing signals |
| 6. Scorecard & venue | `references/scorecard-venue.md` | verdict, scorecard, ranked venues |

**Number verification (Pass 2):** cross-check numbers in the paper against uploaded sources
*only if provided*. Never verify a number against your own assumptions. With no sources, check
that numbers are internally consistent (abstract vs results vs tables) and flag anything
implausible as *unverified*.

**Citation checks (Pass 3):** if web search/fetch is available, live-check that key citations
exist and are represented accurately. If not available, audit internal citation consistency and
mark external claims *unverified*.

### How to run the passes
Run the six passes in sequence in this conversation, each producing its structured slice, then
merge them in Step 3. The passes are independent, so order does not matter — the result is one
merged findings object.

## Step 3 — Assemble findings

Collect every pass into one JSON object with this shape (omit sections you have nothing for):

```json
{
  "meta": {"title": "", "reviewed_on": "YYYY-MM-DD", "field_or_venue": "",
           "inputs": [], "capabilities_used": [], "capabilities_skipped": []},
  "verdict": {"recommendation": "Strong Accept|Weak Accept|Major Revision|Weak Reject|Strong Reject",
              "confidence": "High|Medium|Low", "summary": ""},
  "scorecard": [{"dimension": "Novelty", "score": 7, "max": 10, "note": ""}],
  "priority_fixes": [{"rank": 1, "severity": "critical|major|minor",
                      "title": "", "what": "", "why": "", "fix": ""}],
  "blockers": [{"item": "", "status": "open|partial|resolved"}],
  "reviewers": [{"persona": "Methodologist", "score": 6, "review": ""}],
  "section_findings": [{"section": "Methods", "findings": [""]}],
  "fact_check": [{"claim": "", "location": "", "status": "verified|misleading|false|unverified",
                  "evidence": "", "source": ""}],
  "rewrites": [{"location": "Abstract", "original": "", "suggested": "", "why": ""}],
  "venues": [{"rank": 1, "venue": "", "why": "", "watch_outs": ""}]
}
```

## Step 4 — Build the dossier + summary

**Preferred:** write the findings JSON to a file and run the bundled builder:
```bash
python3 scripts/build_dossier.py findings.json -o manuscript-review-dossier.html
```
It emits a **self-contained** HTML file (inline CSS, works offline, no external loads, copy
buttons on rewrite cards).

**Fallback (no code execution available):** open `assets/dossier-template.html`, fill in the
`{{PLACEHOLDER}}` blocks inline, and save the result. Same output, done by hand.

Then post a **concise ranked summary in chat**: the verdict + confidence, the scorecard line, and
the top 3–5 priority fixes. Point the user to the HTML file for the full dossier. If you skipped
any capability (no web, no data), say so in the summary too.
