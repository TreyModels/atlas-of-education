# Cluster 1 — Post-secondary absorption (X1–X3)

**Status: DESCRIPTIVE / ASSOCIATIONAL — proxies only; no causal and no direction claims.** Absorption is **not
measured** on disk; `ABSORB_F` (wage-and-salaried employment share, ILO modelled) and `ABSORB_S` (services
employment share) are predeclared **proxies**. `QUEUE = BA+ attainment share ÷ wage-share × 100` is a derived
queue-depth proxy, not a measured queue. All estimates: OLS with country-clustered (CR1) SEs; 95% CI normal;
`within` = country-demeaned; `between` = country means. Every specification declared in
`../PRE_DECLARATIONS.md` (sha256 `c214dddf…`) was run; all rows are in `results/`, including nulls.

## X1 — tertiary expansion vs formal absorption, 6 systems (1995–2024) — **NOT SUPPORTED**

| spec | coefficient | 95% CI | n | clusters |
|---|---|---|---|---|
| within: TER ~ LGDP+URBAN+**ABSORB_F** | **−0.858** | [−3.915, +2.198] | 139 | 6 |
| between: TER ~ LGDP+URBAN+ABSORB_F | −1.322 | [−3.577, +0.932] | 139 | 6 |
| within: TER ~ LGDP+URBAN+**ABSORB_S** | −1.897 | [−5.922, +2.129] | 139 | 6 |
| between: TER ~ LGDP+URBAN+ABSORB_S | +0.246 | [−0.323, +0.815] | 139 | 6 |

The within association between tertiary GER and the formal-absorption proxy is **not distinguishable from zero**
(CI includes 0), and the services proxy gives the same (negative) sign but also a CI including 0. The between
estimate has only 6 country points and is not interpretable.

**Disclosed predeclaration ambiguity (Lead adjudication).** The frozen X1 threshold text says *"PARTIAL if only one
of the two"* conditions (CI excludes 0; sign agrees across proxies) holds, but the explicit falsifier says *"within
CI includes 0 → NOT SUPPORTED"*. These conflict here (sign agrees, CI includes 0). The **falsifier-precedence
reading is adopted → NOT SUPPORTED**; the alternative reading would be PARTIAL. Both readings are recorded; **no
threshold was changed**. The worker's first report used the PARTIAL reading; the Lead's adjudication is recorded in
`code/run.py` and in `RUN_MANIFEST.json`.

## X2 — 30-country replication (1995–2024) — **NOT SUPPORTED**

| spec | coefficient | 95% CI | n | clusters |
|---|---|---|---|---|
| within: TER ~ LGDP+URBAN+ABSORB_F | **+0.797** | [−0.402, +1.996] | 654 | 30 |
| between: TER ~ LGDP+URBAN+ABSORB_F | +0.010 | [−0.419, +0.439] | 654 | 30 |

The 30-country point estimate lies **inside** the X1 within 95% CI but with the **opposite sign** (−0.858 in the
six-system panel vs +0.797 here), so the replication criterion (sign agreement) fails. Note the literal falsifier
wording — *"outside the CI with opposite sign"* — does not fire because the point is inside the interval; the
sign-disagreement criterion governs. **NOT SUPPORTED is the conservative replication verdict** (disclosed).

## X3 — graduate-queue depth vs tertiary expansion, 30 countries — **SUPPORTED**

`QUEUE` (BA+ holders per 100 wage-and-salaried jobs) rises with tertiary GER in **all three** fixed specifications:

| specification | coefficient on TER | 95% CI | n | clusters |
|---|---|---|---|---|
| (a) levels, country FE (demeaned) | 0.366 | [0.198, 0.534] | 190 | 26 |
| (b) log1p(QUEUE) on log(TER) | 0.637 | [0.539, 0.735] | 190 | 26 |
| (c) first differences | 0.255 | [0.015, 0.494] | 164 | 24 |

Sign-stable positive with CI excluding 0 in 3/3 specs → SUPPORTED per the frozen rule (QUEUE usable cells = 225
≥ 60). **Reading:** within countries, the ratio of tertiary-attainment stock to formal-wage jobs rises as tertiary
enrolment expands — i.e. the *derived* queue-depth proxy deepens. This is **not** evidence of graduate
unemployment or of a causal absorption failure: the attainment stock is a slow WDI-modelled series and the
wage-share is ILO-modelled; the association is descriptive and may reflect measurement/definition drift.

## What this cluster does and does not say

- **Does:** none of the declared absorption-proxy associations replicates across the 6-system and 30-country
  panels with a stable sign at the primary specification; the derived queue-depth ratio does rise with tertiary
  enrolment in the 30-country panel under all three fixed specs.
- **Does not:** measure absorption, graduate employment, or returns; establish a direction (push vs pull remains
  barred, R13/D77); support any causal or policy claim. 6-system cells are small-n (6 clusters) and the 30-country
  panel is unbalanced WDI/ILO modelled data.

## Reproduction

`code/run.py` is deterministic (no RNG used by the estimator); two consecutive runs produced byte-identical
result CSVs (verified by the battery consolidation step and recorded in `RUN_MANIFEST.json`).
