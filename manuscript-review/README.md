# manuscript-review (Claude Skill)

A portable [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) that runs
a **multi-perspective review of a research paper** and produces a self-contained HTML dossier plus
a ranked chat summary. It reviews the manuscript **read-only** — it never edits the author's file.

Designed for **claude.ai** and **Cowork**: a single, self-contained skill you upload and use — no
extra agents, servers, or setup required.

## What it does
Six review passes → one dossier:
peer review (3 lenses) · statistics & rigor · fact-check & citations · literature & positioning ·
writing quality & AI-writing detection · scorecard, verdict & venue recommendation.

If the user also uploads data/code/figures, it cross-checks the paper's numbers against them;
with none, it checks internal consistency and says so.

## Install & use (claude.ai / Cowork)
1. In **Settings → Skills → Add skill**, upload this `manuscript-review/` folder (or a zip of it).
2. Start a chat, **attach a manuscript** (PDF / DOCX / Markdown), and say *"review this paper."*
   The skill triggers automatically and returns the HTML dossier + a ranked summary.

## Contents
```
manuscript-review/
├── SKILL.md                     # the orchestration protocol (entry point)
├── references/                  # deep methodology, loaded per pass
│   ├── peer-review.md
│   ├── statistics-rigor.md
│   ├── fact-check.md
│   ├── literature-positioning.md
│   ├── writing-ai-detection.md
│   └── scorecard-venue.md
├── assets/dossier-template.html # inline-fill fallback when no code execution
├── scripts/build_dossier.py     # pure-stdlib HTML dossier builder
├── LICENSE                      # MIT
└── CITATION.cff                 # how to cite this skill
```

## Building the dossier manually
```bash
python3 scripts/build_dossier.py findings.json -o dossier.html
```
`findings.json` schema is documented in `SKILL.md` (Step 3). No dependencies; output opens offline.

## License & citation

[MIT](LICENSE) © Ravish Gupta and Fangyi Zhu. Machine-readable metadata is in
[`CITATION.cff`](CITATION.cff). Please cite this skill:

> Gupta, R., & Zhu, F. (2026). *Manuscript Review (Claude Skill)* (Version 0.1.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.22698078

```bibtex
@software{gupta_zhu_manuscript_review_2026,
  author    = {Gupta, Ravish and Zhu, Fangyi},
  title     = {Manuscript Review (Claude Skill)},
  year      = {2026},
  version   = {0.1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22698078},
  url       = {https://doi.org/10.5281/zenodo.22698078}
}
```
