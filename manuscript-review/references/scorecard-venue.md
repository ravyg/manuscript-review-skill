# Pass 6 — Scorecard, verdict & venue

Synthesize the other five passes into an overall judgment and a venue recommendation. This pass
runs last and consumes the findings from passes 1–5.

## Scorecard (score each 1–10, with a one-line justification)
- **Novelty** — is the contribution clearly new and significant?
- **Rigor** — is the methodology sound, statistically valid, and reproducible?
- **Clarity** — is it well-written and well-structured?
- **Impact** — will it influence the field / who benefits?
- **Completeness** — thorough experiments, ablations, baselines, honest limitations?

Populate `scorecard[]` with `{dimension, score, max: 10, note}`.

## Verdict
Set `verdict`:
- `recommendation`: Strong Accept | Weak Accept | Major Revision | Weak Reject | Strong Reject
- `confidence`: High | Medium | Low
- `summary`: 3–5 sentences — what the paper does, its strongest point, and the single biggest
  thing standing between it and acceptance.

## Priority fixes & blockers
- Rank all `priority_fixes[]` most-severe first (critical → major → minor). Each stays actionable
  (`what` / `why` / `fix`).
- Distill the must-clear items into `blockers[]` with `status` (open/partial/resolved) so the
  authors have a checklist.

## Venue recommendation
Populate `venues[]` (ranked) with `{rank, venue, why, watch_outs}`. Consider:
- Topic/scope alignment; venue tier & acceptance rate; contribution style (systems vs theory vs
  applications); submission deadline & review timeline; what the venue has recently accepted.
- Read a themed collection's/track's **scope** before recommending it — a paper that misses the
  scope (e.g. a themed "multimodal + real-world validation" call) risks desk rejection. Don't
  force-fit.
- If web is available, check current CFPs/deadlines; otherwise note recommendations are from
  general knowledge and should be deadline-checked.

## Best-paper levers (only if the paper is already strong)
Strong narrative arc; a surprising/counterintuitive finding; comprehensive experiments;
reproducibility (code+data); broader impact tied to real-world significance; clean figures and
tight writing. List the 2–3 highest-leverage moves in `priority_fixes[]` as `severity: minor`.
