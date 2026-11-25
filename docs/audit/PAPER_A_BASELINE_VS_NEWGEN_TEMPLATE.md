# PAPER A — BASELINE vs NEW-GENERATION COMPARISON TEMPLATE (two columns)

**Status:** template only. Fill the **new-generation** column from executed runs. **Two columns only** — there is no
Codex column: Codex is the independent auditor; it did not run a competing Paper A version.

**Columns**

1. **Gemini docx baseline** — the manuscript's number = **AUTHOR-REPORTED BASELINE**. Not a target, not a result.
2. **New generation (ours)** — repaired engine `98baf6b`, pre-registered, hashed, with uncertainty. Label
   `REPRODUCED SIMULATION` (or `VERIFIED EMPIRICAL` for the E8 empirical estimates) and say **uncalibrated** where
   applicable.
3. **Difference** — state the direction; mark `match` / `mismatch` / `not-comparable`.
4. **Reason** — the mechanical reason (generation, D2 repair, different N/T, different gate list, missing data,
   estimand difference, etc.).

**Rules**

* Every new-generation row cites artifact + sha256 + engine commit + seed count.
* `not-comparable` is legitimate and must state why (different design/estimand/data).
* Do not average across generations. Do not substitute one generation's number into another's table.
* The verified E8 empirical estimates are the only rows where the baseline is already independently confirmed; the
  new-generation re-run hardens provenance, it does not change the numbers.

---

## A. Five headline computations

| # | quantity | Gemini docx baseline (AUTHOR-REPORTED) | New generation (ours) | difference | reason / status |
|---|---|---|---|---|---|
| (a) | E8 impact ATT (e = 0) | **+12.44 pp** | **+12.322 pp** (fresh-WDI CS-style group-time ATT; bootstrap mean 12.308, 95% CI [4.48, 22.64]; Fisher p 0.0044/0.0040) — **REPRODUCED EMPIRICAL ANALYSIS** | **match in magnitude** (−0.12 pp) | 8 clusters → wide CI; fresh vintage; equal weights/no DR covariates (declared) |
| (a) | E8 post mean (e = +1..+6) | **+25.26 pp** | **+25.083 pp** (fresh-WDI CS-style) — **REPRODUCED EMPIRICAL ANALYSIS** | **match** (−0.18 pp) | CS-style replicates; simple-DiD +2.54 is estimator sensitivity (report as sensitivity) |
| (a) | E8 event path | +23.82 / +25.94 / +22.12 / +25.19 / +28.56 / +25.92 | *fill* — verified same | *fill* | committed record; report leads too |
| (a) | E8 Fisher RI p (date / country) | .0001 / .0003–.0006 | *fill* — verified 9.999e-05 / 5.999e-04 / 2.9997e-04 | *fill* | B = 10,000/family; resolution floor |
| (a) | E8 gender D (95% CI) | −3.94 pp [−8.72, +0.29] | *fill* — verified same | *fill* | near-boundary non-detection; paired CI |
| (b) | Bulge `t*` ATT (SE.SEC.ENRR) | manuscript HONEST_NULL (no jump claimed) | **−0.956 pp** at `t*`; post +0.30; Fisher p **0.251 / 0.384** — **UNRESOLVED** (no-effect evidence) | **not-comparable** (different outcome/indicators) | fresh WDI; no detectable jump; consistent with honest-null framing |
| (b) | Bulge sample/permutations | 7,290 obs; 2,500/scheme | fresh WDI, 2,500/scheme (2,495 effective country perms) | *not-comparable* | estimator/outcome differences |
| (c) | H2 fee×scarcity (contest grid) | **+0.1086** (CI +0.0924, +0.1248; p = 1.9e-11) | *fill* (≥5,000-run pre-registered run) | *fill* | legacy 1,640-run had no committed artifact; repaired engine re-prices expected P |
| (c) | H2 quota grid | **−0.0145** (CI −0.0214, −0.0076) | *fill* | *fill* | same |
| (c) | H1 (S=.25 − .70) contest fee=0 | **+0.3430** (Spearman −1.00) | *fill* | *fill* | same |
| (c) | Inverted-U by `vac0` | +0.0138 / +0.1865 / +0.2573 / −0.0232 | *fill* | *fill* | same |
| (d) | 10-param baseline rank / cond | 5/10; 3.48e12 | *fill* (analytic Jacobian, multi-seed, declared perturbations) | *fill* | Paper A model spec must be written; condition numbers are diagnostics only |
| (d) | 7-param bijection rank / cond | 5/7; 1.09e13 | *fill* | *fill* | same |
| (d) | 5-param core rank / cond | 5/5; 14.41 | *fill* | *fill* | same |
| (d) | +income micro-moments | 6/7; 3435.49 | *fill* | *fill* | local rank only |
| (d) | +income +school-quality | 7/7; 43.81 ("full identifiability") | *fill* | *fill* | independent affiliated computation gives **local 5/5**, not 7/7; do not claim global |
| (e) | Forecast 7-horizon RMSE | 5.13 / 4.68 pp vs persistence 23.93 | **EXPLORATORY-INVALID — RERUN REQUIRED; do not cite** | *not-comparable* | calibration bisection misframed → zero-effect artefact |
| (e) | Forecast impact ATT | +11.60 / +13.48 pp | **EXPLORATORY-INVALID — do not cite** | *not-comparable* | rerun required |
| (e) | Calibration | fee_public=.150 on 74.88 % pre-GER; zero post fitting | **EXPLORATORY-INVALID — do not cite** | *not-comparable* | rerun with documented training-only calibration |

---

## B. Paper B tables (same convention, for consistency)

| # | quantity | Gemini docx baseline (AUTHOR-REPORTED) | New generation (ours, repaired 540 `455649da…`) | difference | reason |
|---|---|---|---|---|---|
| B1 | HK baseline elite Q5 | 30.0 % | **25.01 %** | *fill* | 420 vs 540 generation; D2 repair |
| B2 | KR baseline elite Q5 | 24.6 % | **22.13 %** | *fill* | same |
| B3 | KR K–12 participation | 76.5 % | **58.38 %** | *fill* | neither generation recovers 76.5 % |
| B4 | KR Q5−Q1 gap | 34.1 pp | **29.71 pp** (target 32.1) | *fill* | D2 artefact; residual needs Gate-2 calibration |
| B5 | KR Q5/Q1 ratio | 3.19× | **2.11×** (target 3.4) | *fill* | over-correction below target |
| B6 | CF1b spend / elite | 82.1 / 74.1; 25.1 / 22.9 | **97.21 / 99.25; 23.72 / 22.00** | *fill* | **CF1b no longer passes** |
| B7 | CF4a spend / elite | not in docx table | **70.58 / 23.44 (HK); 72.48 / 21.47 (KR)** | *fill* | **CF4a Win-Win both** — reversal |
| B8 | CF4b spend / elite | not in docx table | **89.98 / 23.11 (HK); 105.54 / 22.09 (KR)** | *fill* | fails spend |
| B9 | CF3b spend / elite | 52.8 / 54.9; 36.3 / 27.5 | **70.88 / 72.55; 23.64 / 21.48** | *fill* | wage compression no longer regressive |

Full Paper B regenerated numbers: `results/audit/paper_b_540_regenerated_tables.csv` (sha256 `da40a2ee…c5c1`);
narrative in `PAPER_B_TABLE_REGENERATION.md`.

---

## C. Completion checklist (when new-generation results land)

- [ ] pre-registration commit hash recorded
- [ ] engine commit + file hashes recorded
- [ ] config + seed-list hash recorded
- [ ] output sha256 recorded; exit code 0; wall time
- [ ] seed uncertainty and parameter uncertainty separated
- [ ] at least one baseline and one sensitivity grid
- [ ] declared perturbation grid for identifiability (d)
- [ ] every difference to the docx baseline has a written reason
- [ ] labels: AUTHOR-REPORTED BASELINE / NEW GENERATION
- [ ] no cell filled from memory
