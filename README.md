# Manuscript Review

A pre-submission review tool for research papers. Upload a draft and it reads the methods,
statistics, citations, and writing, then returns **one report that ranks what to fix** — the
kind of things a reviewer would flag. It runs inside Claude as a "skill," is read-only (never
changes your file), and is free and open source (MIT).

## Install into Claude (~2 minutes)

1. **Download the skill:**
   [**manuscript-review-skill-v0.1.0.zip**](https://github.com/ravyg/manuscript-review-skill/releases/latest/download/manuscript-review-skill-v0.1.0.zip)
2. In **claude.ai**: **Settings → Skills → Add**, and upload the zip. *(Requires a Claude Pro or
   Team plan; the same Skills list is used by Cowork.)*
3. Start a chat, **attach your manuscript** (PDF/DOCX), and say **"review this paper."** The
   report comes back automatically.

> Optional: upload your data/code alongside the paper and it will also check the paper's numbers
> against them.

## What it checks

- **Statistics** — uncorrected multiple comparisons, missing effect sizes / confidence intervals,
  underpowered tests, weak baselines.
- **Citations** — whether each reference exists and actually supports the claim; catches
  misattributions.
- **Writing** — concrete line edits, not vague "make it clearer."
- **Positioning** — how the work sits against related papers, plus a shortlist of fitting journals.
- It also flags what it *couldn't* verify, so nothing is oversold.

**Output:** one ranked report — most important problems first, each with a specific fix — plus a
self-contained HTML dossier you can share.

## Good to know

It's a fast first pass, not a replacement for expert peer review — check its claims before acting
on them. Only submit drafts you have the right to share, and follow your target venue's policy on
AI assistance.

## What's in this repo

```
manuscript-review/         # the skill (upload this, packaged in the release zip)
├── SKILL.md               # the review protocol
├── references/            # methodology for each review pass
├── assets/                # HTML dossier template
└── scripts/               # pure-stdlib dossier builder
```

## License & citation

[MIT](LICENSE). If you use it, please cite:

> Gupta, R., & Zhu, F. (2026). *Manuscript Review*. Zenodo. https://doi.org/10.5281/zenodo.22698077
