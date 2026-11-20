# Lab battery 2026-11-20_b — consolidated findings (X1–X15)

**Status: DESCRIPTIVE / ILLUSTRATIVE — no causal and no direction claims.** Fifteen experiments were
**predeclared before running** (`PRE_DECLARATIONS.md`, sha256 `c214dddfe51ef0ff9d0173752fe11f74a91e165605ebba45bc405d9fe6381af6`)
and executed by a five-cluster **Z.AI GLM-5.3-Flash worker fleet** with disjoint write scopes; the Lead
consolidated, re-ran every script (byte-identical, see `RUN_MANIFEST.json`), adjudicated two predeclaration
ambiguities and ran one **disclosed post-hoc amendment** (cluster 5). The massification phase remains **CLOSED**
at PARTIAL/DESCRIPTIVE/EQUIVALENT (`06_report/MASSIFICATION_CLOSEOUT.md`, D76); this battery does **not** reopen
C1–C4 and makes no claim about the world beyond the observed/derived descriptive associations reported here.

**Labels:** `observed` (on-disk measured series), `derived` (computed from observed series via a declared proxy),
`simulated` (stipulated toy — not evidence). All cells are in `RESULTS.csv` (18 rows = 15 predeclared + 3
amendment) and per-experiment detail is in each cluster's `results/`.

## Results table (all 15 predeclared cells)

| # | cluster | question | key estimate | predeclared verdict |
|---|---|---|---|---|
| **X1** | 1 absorption | tertiary GER vs formal-absorption proxy, 6 systems 1995–2024 | within slope **−0.86** (se 1.56; CI −3.91…+2.20; n=139, G=6); services proxy −1.90 (CI −5.92…+2.13) | **NOT SUPPORTED** (CI includes 0; falsifier-precedence reading of an ambiguous threshold — see §Disclosures) |
| **X2** | 1 absorption | 30-country replication of X1 | within slope **+0.80** (se 0.61; CI −0.40…+2.00; n=654, G=30) — inside X1's CI but **opposite sign** | **NOT SUPPORTED** (replication sign criterion fails) |
| **X3** | 1 absorption | derived queue depth (`BA+ attainment ÷ wage-share`) vs tertiary GER, 30 countries | **+0.366** (CI +0.198…+0.534; n=190, G=26); log-log +0.637; first-diff +0.255 — 3/3 CIs exclude 0 | **SUPPORTED** (descriptive; proxy ratio) |
| **X4** | 2 tertiary crossings | structure typicality at tertiary (≥15%, ≥50%) vs secondary (≥50%, ≥90%) crossings | inside-IQR counts: tertiary set 3/5 on all 3 vars; secondary set 2/6 on all 3 | **NOT SUPPORTED** (both sets fail ≥4/6 on ≥2/3) |
| **X5** | 2 tertiary crossings | same economic-structure package at tertiary-50 vs secondary-90? | median difference / pooled IQR: GDP **0.914** (different), urban **0.795** (different), services **0.296** (same); dated n: tertiary-50 4, secondary-90 3 | **DATA LIMITED** (below the declared n≥4 per set minimum; directional table reported, no package claim) |
| **X6** | 2 tertiary crossings | secondary→tertiary spacing vs structure at secondary crossing | only n=3 countries with both crossings dated (HKG gap −4 y w/ disclosed substitution; PHL 48 y; CHN 44 y) | **UNABLE** (n<4 floor; no ρ reported) |
| **X7** | 3 geo-size | system size (`log population`) vs tertiary/secondary GER, 30 countries | TER SIZE between **−1.74** (CI −5.38…+1.90, n=30); within −5.64 (CI −34.14…+22.86, n=656, G=30); SEC also null | **NOT SUPPORTED** (size association indistinguishable from 0) |
| **X8** | 3 geo-size | HKG city-state vs CHN/PHL/KHM: duration and volatility | duration usable only for CHN (13.0 y vs HKG 19.5 y → ratio 0.667); PHL/KHM **UNABLE** (censored); volatility ratios 0.50/0.51/0.26 vs HKG (HKG SD inflated by a series break) | **NOT SUPPORTED** (both ratios <1.2); n≤4/side — descriptive only |
| **X9** | 3 geo-size | declared number-of-markets proxy vs tertiary GER | within+LGDP: 6 systems **+0.056** (CI −0.009…+0.121, n=139); 30 countries **+0.035** (CI +0.0005…+0.070, n=656) | **PARTIAL** (supports in one sample only; MARKET/URBAN-only specs agree in sign) |
| **X10** | 4 PHL regional | regional convergence in mean years of schooling across cohorts | Spearman ρ(ΔMYS, MYS₀) = **−0.444**; **17/17** regions improved | **SUPPORTED** (descriptive; proxy — regional tertiary enrolment unobserved) |
| **X11** | 4 PHL regional | regional education inequality across cohorts (national tertiary GER as context only) | **17/17** regions ΔGini ≤ −0.02; ρ(ΔGini, Gini₀) = **−0.622** | **SUPPORTED** (descriptive; proxy) |
| **X12** | 4 PHL regional | whose schooling grew more (bottom vs top quartile of initial attainment) | ratio of median ΔMYS Q1/Q4 = **1.098** (Q1 1.34 vs Q4 1.22) | **SUPPORTED** (mild pro-poor gradient; descriptive proxy) |
| **X13** | 5 fragmentation (SIM) | does splitting into more markets delay the ceiling crossing? | predeclared run: **undefined** — the frozen demand recursion was contractive; 100% right-censored in every K cell | **SIMULATED-THRESHOLD-MISSED** (predeclaration defect; see Amendment B1) |
| **X14** | 5 fragmentation (SIM) | does splitting smooth the approach? | predeclared run: V = **1.000** (no ceiling ever binds; volatility identical across K by construction) | **SIMULATED-THRESHOLD-MISSED** (same defect) |
| **X15** | 5 fragmentation (SIM) | heterogeneity dose (fraction of binding-below-demand markets) | predeclared run: **undefined** (all f-cells censored) | **SIMULATED-THRESHOLD-MISSED** (same defect) |

### Amendment B1 (cluster 5) — POST-HOC DISCLOSED, thresholds unchanged, SIMULATED

The predeclared recursion `d_{t+1} = d_t·r·(1−d_t/dmax)` with `r=0.08<1` is contractive: demand decays and the
50% crossing is unreachable, so the predeclared thresholds were not evaluable. That is a **Lead predeclaration
defect**, disclosed, and the predeclared verdicts stand as the formal ones. Amendment B1 changes **only** the
demand rule to the growing form `d_{t+1}=d_t·(1+0.08·(1−d_t/dmax))`, keeping every frozen threshold, the K grid,
the f grid, the 200-seed cells and the paired-seed design identical:

| # | amended estimate | verdict (same frozen thresholds) |
|---|---|---|
| X13 | Δ = median crossing year K=32 − K=1 = **+1.00 y** (CI 0.00…1.00) | **PARTIAL** (1 ≤ Δ < 3) |
| X14 | V = median volatility K=1 / K=32 = **1.231** (CI 1.201…1.251) | **PARTIAL** (1.1 ≤ V < 1.5) |
| X15 | Spearman ρ(crossing year, f) = **1.000** over finite cells f = 0…0.75 | **PARTIAL** (ρ ≥ 0.90, but f=1.0 cell is 100% censored so the predeclared delay rule is undefined) |

**Exploratory (no threshold):** in the amended toy the share of seeds that ever cross rises from **77.0% (K=1) to
100% (K=8/16/32)** — fragmentation moves the **extensive margin** (whether the system universalizes at all) much
more than the timing (+1 y) or the smoothness (V=1.23). Median crossing years: K=1 28, K=32 29. The binding-market
dose delays monotonically in the finite cells (f=0: 29 y; 0.25: 31 y; 0.50: 35 y; 0.75: 43 y; 1.0: never within
80 y). **This is a property of the stipulated toy only.**

## The five most decision-relevant findings (one per cluster)

1. **Post-secondary absorption is not detectable with these proxies, but the derived queue ratio moves** (cluster
   1, X1–X3). Tertiary expansion shows no within association with the formal-absorption proxy in six systems (CI
   includes 0) and **fails sign replication at 30-country scale** (+0.80 vs −0.86) — so a "post-secondary
   absorption" story cannot rest on these proxies. The one surviving cell is the derived queue-depth ratio
   (BA+ attainment ÷ wage-share), which rises with tertiary GER in all three fixed 30-country specifications
   (levels +0.366, log-log +0.637, first-difference +0.255). It is a proxy ratio, descriptive, and **not** evidence
   of graduate unemployment or a causal absorption failure.
2. **Tertiary crossings do not share the secondary crossing's structure package, and the contrast is
   data-starved** (cluster 2, X4–X6). No milestone set is structure-typical (tertiary 3/5, secondary 2/6 on all
   three variables vs the ≥4/6 rule). The tertiary-50 vs secondary-90 contrast points to a *different* package on
   income (0.91 IQR) and urbanisation (0.79 IQR) but is **DATA LIMITED** (4 vs 3 dated crossings), and the
   spacing test is **UNABLE** (n=3). Honest reading: a single "crossing package" cannot be established for either
   level on this timing map, and the tertiary comparison is not identified.
3. **System size does not scale schooling cross-sectionally, and the city-state comparison is not testable**
   (cluster 3, X7–X9). Population size is null in both between and within dimensions at 30-country scale (TER
   between −1.74, CI −5.38…+1.90; within −5.64, CI −34.14…+22.86). The only usable HKG-vs-large duration pair
   (CHN) gives ratio 0.667 — HKG took **longer** (19.5 vs 13.0 y) — and HKG's volatility is inflated by a series
   break; the market-count proxy is PARTIAL (30-country only). Any "scaling law" reading of system size is **not
   supported** on this evidence base.
4. **The PHL regional record is the cleanest and most consistent result** (cluster 4, X10–X12). Schooling rose in
   **17/17** regions, education Gini fell ≥0.02 in **17/17** regions, and the gain is mildly larger in initially
   lower-attainment regions (Q1/Q4 = 1.098). **Binding limitation:** regional tertiary enrolment is **not
   observed**; these are attainment/inequality proxies around a national tertiary expansion (GER 16.3 in 1971 →
   47.4 in 2024, context only), descriptive, no causal read.
5. **Fragmentation (SIMULATED, amended toy) acts on the extensive margin, not the timing** (cluster 5,
   X13–X15 / Amendment B1). Splitting a system into more markets barely changes *when* it crosses (+1.0 y) or
   *how smoothly* (volatility ratio 1.23), but raises the **probability of crossing at all** (77% → 100% of
   seeds). A hypothesis for future design, **not evidence**: the extensive-margin channel is the one worth
   specifying in an observed fragmentation test.

## Disclosures and Lead adjudications

- **Z.AI worker fleet:** five GLM-5.3-Flash subagents (one per cluster), disjoint directories, predeclaration hash
  fixed before dispatch; each ran its own deterministic script and reported. The Lead re-ran all five scripts and
  the amendment script — **all byte-identical** (`RUN_MANIFEST.json` → `determinism_rerun`).
- **X1 predeclaration ambiguity (Lead adjudication, disclosed):** the text's "PARTIAL if only one of the two
  conditions" clause conflicts with the explicit falsifier "within CI includes 0 → NOT SUPPORTED"; the worker's
  first reading was PARTIAL. Falsifier-precedence adopted (**NOT SUPPORTED**); the PARTIAL reading is retained in
  the X1 note. No threshold was changed.
- **X2 literal-falsifier mismatch (disclosed):** the point estimate is *inside* the X1 CI but has the opposite
  sign, so the falsifier's literal condition ("outside the CI with opposite sign") does not fire while the
  replication sign criterion fails. Conservative verdict: **NOT SUPPORTED**.
- **X4 denominator (disclosed):** with 5 usable tertiary crossings the absolute "≥4/6" rule is applied as "≥4
  countries"; the proportion reading (3/5 = 60% < 67%) gives the same verdict.
- **X8 measurement caveat:** HKG's tertiary-GER annual-change volatility is dominated by a series discontinuity;
  the volatility ratios are reported but not interpretable as behavioural smoothness.
- **Cluster 5 AMENDMENT B1** (above): post-hoc, disclosed, thresholds unchanged; the predeclared result stands as
  the formal one.
- **Cluster 2 schema:** X4's two milestone-set verdicts were normalised to one verdict per row for `RESULTS.csv`;
  per-set verdicts are in the X4 note.

## Limits

Small n throughout (6 systems; 30-country unbalanced WDI/ILO modelled panel; n≤4 for the city-state comparison;
17 PHL regions, 2 cohorts; n=3 for the secondary→tertiary spacing test); **all proxies are declared, none is a
measured absorption rate, a real number of markets, or a measured queue**; completion/attainment series are
partly modelled; crossings are read from `UNIVERSALIZATION_TIMING.csv` with its own censoring/band definition;
the 30-country ECI panel is 1995–2024 only. All results are descriptive/associational. Nothing here reopens the
closed phase's C1–C4; X1/X2 are consistent with the earlier wrong-sign scaling finding (a model-class limit, not
evidence about the world), not a new claim about it.
