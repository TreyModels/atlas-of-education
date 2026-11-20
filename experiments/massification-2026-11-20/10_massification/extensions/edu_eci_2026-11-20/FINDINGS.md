# FINDINGS — education → economic complexity (ECI), 30-country panel 1995–2024

**Status: DESCRIPTIVE / ASSOCIATIONAL. No causal claim. No direction claim** (the reverse-order spec is reported
symmetrically). Predeclared before the run: `PRE_DECLARATIONS.md` sha256
`e2a707a9b67e525a1f483fc42d71555d882af31478f348f22a2943396c5bc230`; the script refuses to run if that hash changes.
Every estimate, including nulls and errors, is in `results/RESULTS_ALL.csv` (272 rows).

**Why this exists.** The user's hypothesis, relayed via the dashboard: *more education → more economic complexity
(ECI); growth is a different thing; ECI is the preferred outcome.* This is **not** a test of ECI → growth (that was
negative, `longitudinal_2026-11-20`). It asks whether the **level of education** moves with the **complexity of the
economy**, with the existing on-disk anchor result (ECI ~ primary completion, t−10 = 0.593) as a cross-check rather
than a thing to re-litigate.

---

## 1. Plain-English answer

**Directionally, yes for the schooling FLOW — but the predeclared bar is not met robustly.**

- **Primary completion** is the one consistent story: it is **positive in every FE/block cell** at both 5 and 10
  years, significantly so in the unadjusted 5-year-block spec at 5 years (+0.0058, p=0.037) and at 10 years
  (+0.0080, p=0.032), and close to conventional significance in the country+year FE spec (+0.0058, p=0.11 at 10y).
  Verdict per the frozen rule: **PARTIAL at 5 years, PARTIAL at 10 years — ROBUST** to using the alternative ECI
  measure (`eci_hs92`). The magnitude is small: **+1 pp of primary completion ≈ +0.003 to +0.008 ECI points**, and
  once log GDP pc and urbanisation are controlled the estimate roughly halves and loses significance.
- **Lower-secondary completion** is directionally positive at 5 years but weak (**PARTIAL, ROBUST**); at 10 years it
  is flat (**NOT SUPPORTED**).
- **Youth literacy** is the only **SUPPORTED** cell (5-year lag: +0.0115, p=0.010 without controls; +0.0068, p=0.024
  with controls) — but it is **NOT ROBUST**: under `eci_hs92` every cell is insignificant. One supported cell out of
  14, not robust, is not a result to build on.
- **Adult literacy** — the stock the existing work already found uninformative — is **not supported at 10 years**
  (negative) and only PARTIAL at 5 years, where the sign flips once income is controlled. This is consistent with
  the earlier on-disk finding: **the schooling flow tracks complexity; the literacy stock does not.**
- **Upper-secondary and tertiary attainment show nothing — or less than nothing.** Upper-secondary is negative and
  insignificant everywhere; tertiary attainment is **negative-significant** in the country+year FE spec
  (−0.0143, p=0.016 unadjusted; −0.0155, p=0.006 adjusted). Read plainly: within countries, tertiary
  attainment growth has *not* been accompanied by rising measured complexity — consistent with the programme's
  massification-without-complexity reading, but it is an association, not a direction claim.
- **No evidence that education "builds complexity from a low base."** The predeclared heterogeneity test (baseline-ECI
  median split, upper-secondary attainment, S2 with controls) gives LOW-vs-HIGH slope differences of **−0.0045
  [−0.024, +0.019]** at 5 years and **−0.0075 [−0.031, +0.021]** at 10 years — no difference in either direction.
- **Reverse-order descriptive check:** ECI lagged 10 years is **negatively** associated with upper-secondary
  attainment (−4.68, p=0.016) and insignificantly with primary completion (+1.58, ns) and adult literacy (−0.84, ns).
  Reported for symmetry only; **no direction claim** either way.

**Bottom line for the user:** the hypothesis is *not established* in this panel. The best available description is
"more primary completion goes with modestly more measured complexity, and that association is fragile to income
controls"; the upper levels do not show it, and there is no threshold-from-a-low-base pattern.

## 2. Verdict matrix (primary outcome `eci_sitc`; frozen rule `PRE_DECLARATIONS.md` §4)

| level | lag 5 | lag 10 |
|---|---|---|
| **adult literacy** `lit` | PARTIAL (not robust) | NOT SUPPORTED |
| **youth literacy** `lit_youth` | **SUPPORTED** (not robust) | NOT SUPPORTED |
| **primary completion** `prm_cmpt` | PARTIAL (robust) | **PARTIAL (robust)** |
| **lower-secondary completion** `lsec_cmpt` | PARTIAL (robust) | NOT SUPPORTED |
| **upper-secondary attainment** `cuat_up` | NOT SUPPORTED | NOT SUPPORTED |
| **tertiary attainment** `cuat_ba` | NOT SUPPORTED (negative-significant in S2) | NOT SUPPORTED (negative in S2) |
| **MYS proxy** (DERIVED) | NOT SUPPORTED | PARTIAL (sign-unstable; do not read) |

Tally: **1 SUPPORTED / 5 PARTIAL / 8 NOT SUPPORTED**; **12 of 14 cells ROBUST** to the alternative ECI measure, the
two exceptions being the two PARTIAL/SUPPORTED literacy-stock cells. 14 cells is a multiplicity: the rule is a
declared descriptive bar, **not** a hypothesis-test family, and no false-discovery correction is claimed.

## 3. The four component cells (coefficients; ECI points per pp of education)

| level, lag | S2 FE no ctrl | S2 FE + ctrl | 5-yr block no ctrl | 5-yr block + ctrl |
|---|---|---|---|---|
| prm_cmpt, 10 | +0.00583 (p=0.109) | +0.00367 (p=0.083) | **+0.00800 (p=0.032)** | +0.00289 (p=0.441) |
| prm_cmpt, 5 | +0.00340 (p=0.222) | +0.00115 (p=0.640) | **+0.00576 (p=0.037)** | +0.00063 (p=0.836) |
| lit_youth, 5 | **+0.01154 (p=0.010)** | **+0.00683 (p=0.024)** | **+0.01546 (p=0.039)** | −0.00165 (p=0.791) |
| cuat_up, 10 | −0.01208 (p=0.186) | −0.00663 (p=0.343) | +0.00501 (p=0.657) | −0.00631 (p=0.437) |
| cuat_ba, 5 | **−0.01433 (p=0.016)** | **−0.01550 (p=0.006)** | −0.00451 (p=0.457) | −0.01008 (p=0.199) |

Controls C1 = log GDP pc + urbanisation. Full matrix (all 7 levels × 2 lags × 4 cells × 2 outcomes), including every
n and cluster count, in `results/RESULTS_ALL.csv`.

## 4. The existing-result cross-check — exact, and what it does not settle

| check | coefficient | se | n | countries | period |
|---|---|---|---|---|---|
| **E5 replication** (`eci_hs92 ~ log primary completion, t−10`, two-way FE, the existing file's own row-shift lag) | **0.5932271376** | **0.1757698583** | **253** | **23** | 2005–2024 |
| E5 target published in `09_relations/LITERACY_ECI_DEMOGRAPHY.md` | 0.5932271376 | 0.1757698583 | 253 | 23 | 2005–2024 |
| same specification, **true calendar-year** 10-year lag, 1995–2024 window | 0.5690534891 | 0.2317801262 | 320 | 27 | 2005–2024 |

The existing anchor **reproduces exactly** — data assembly is consistent with the earlier analysis. The true-year-lag
version is very close (0.569) on a larger sample (27 countries, 320 obs), so the anchor survives the lag-implementation
difference. **But the anchor is a log specification on `eci_hs92` with no income control**; the predeclared
level-specification matrix above gives primary completion only **PARTIAL** on `eci_sitc`. So: the anchor is real,
positive and replicable — and **specification-dependent**. Both facts belong in any write-up.

## 5. What this cannot claim

- **No causal claim and no direction**: S5 is reported only so both orderings are visible; the data are consistent
  with joint determination of complexity and schooling.
- **No claim outside the 30-country Asia+comparator panel, 1995–2024.**
- **A null is not "education does not matter"**: literacy is survey-sparse, completion series are UIS-modelled, ECI is
  a modelled index, and the ECI–income relation is strong enough to absorb education in adjusted specs.
- **The MYS proxy is derived**, not observed; its rows are sign-unstable and are not read.
- **The completion > GER measurement issue** (`facts/STYLIZED_FACTS.md` §12; `10_massification/data/
  DATA_NOTES_MASSIFICATION.md`) means completion-based education series and GER-based series are not interchangeable —
  which matters here because the schooling-flow result is carried by completion series.

## 6. Reproduction and provenance

`PRE_DECLARATIONS.md` (frozen, hash-checked at runtime) → `code/run_edu_eci.py` → `results/`: `RESULTS_ALL.csv` (272
rows: S1 long differences, S2 annual two-way FE, S3 5-year blocks, S4 within/between, S5 reverse, S6 heterogeneity +
country bootstrap, both ECI measures, both control sets), `VERDICT_MATRIX.csv`, `ROBUSTNESS_HS92.csv`,
`HETEROGENEITY.csv`, `CROSSCHECK_EXISTING.csv`, `RUN_MANIFEST.json` (hashes of predeclaration, data, code, results).
Deterministic: one PCG64 stream, seed 20261120; two clean runs write byte-identical results CSVs.

**Data (observed unless labelled):** `09_relations/data/panel_wdi_long.csv` (WDI/UIS indicators),
`09_relations/data/economic_complexity_panel_30ctys.csv` (Growth Lab ECI, Harvard Dataverse
`doi:10.7910/DVN/XTAQMC`, CC0). **Derived:** `mys_proxy = 6 + 6*(SE.SEC.CUAT.LO.ZS/100) + 3*(SE.SEC.CUAT.UP.ZS/100)
+ 4*(SE.TER.CUAT.BA.ZS/100)`.
