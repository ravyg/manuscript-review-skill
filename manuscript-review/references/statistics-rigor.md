# Pass 2 — Statistics & rigor

Judge whether the quantitative claims are earned. Verify numbers **only** against uploaded
sources; never against your own assumptions. With no sources, check internal consistency and
mark external numbers *unverified*.

## Rigor checklist
- **Appropriate tests.** Is each statistical test justified for the data and question? Are
  assumptions (normality, homoscedasticity, independence) checked or at least acknowledged?
- **Effect sizes + CIs, not just p.** A result reported as significant with no effect size or
  confidence interval is incomplete. Lead with effect size, p second.
- **Multiple comparisons.** If many tests/configs/layers/metrics were tried and the best was
  reported, is there a correction (Bonferroni/Holm/FDR) or a max-statistic permutation, or a
  held-out confirmation? Selecting the winner then quoting its nominal p is "winner's curse."
- **Variance / replication.** Are results averaged over multiple seeds/trials (report mean ± sd)?
  A single-run number with no variance is fragile.
- **Baselines & ablations.** Random / majority / simple-heuristic / SOTA baselines present?
  Ablations isolating each component's contribution?
- **Small samples.** With small n, a non-significant dispersion/heterogeneity test means "failed
  to detect," not "there is none." Ask for bootstrap CIs / leave-one-out jackknife.
- **Data leakage.** Was test data ever visible during training/selection? Are splits clean?
- **Reproducibility.** Seeds, hardware, runtime, dependency versions, code/data availability.

## Common linear-algebra / representation-geometry traps (if relevant)
- **Pseudoinverse ≠ regularization.** If a Gram/covariance matrix is full-rank, G⁺ = G⁻¹ exactly
  — no denoising; an ill-conditioned inverse amplifies the smallest-eigenvalue direction. Ask for
  eigenstructure/condition number and a ridge sweep.
- **Fake independence.** A "diagonal by chance" `(1/k)^d` argument assumes independent axes; if
  the basis is collinear (high condition number, cosines near 1) it is false. Use permutation.
- **Ablations need uncertainty.** `permutations=0` gives bare point estimates. Require p/CI, ≥2
  near/distant controls, and committed outputs so numbers are reproducible.

## Output into the findings object
- Rigor problems → `priority_fixes[]` (severity by how much they threaten the conclusions).
- Number checks → `fact_check[]` entries with `status` = verified / misleading / unverified and
  `evidence` (what you compared against). Note explicitly if no source was available.
- Add a scorecard note for the **Rigor** dimension.
