# PRE-DECLARATIONS — education → economic complexity (ECI), 30-country panel

**Frozen before the run.** Written 2026-11-20 (Asia/Shanghai) in response to the user's clarification, relayed via
the dashboard: *"more education → more economic complexity (ECI). Growth is a different thing. ECI over GDP as the
outcome."* This file fixes the specifications, thresholds and verdict rule **before** any estimate is computed.
Nothing below is changed after seeing results. The sha256 of this file is recorded in `results/RUN_MANIFEST.json`
and the run refuses to proceed if the hash does not match.

**Status vocabulary:** DESCRIPTIVE / ASSOCIATIONAL. **No causal claim. No push/pull direction claim.** The
reverse-order spec (S5) is reported symmetrically so no direction is implied. All education variables are observed
WDI/UIS series except `mys_proxy`, which is a **DERIVED** approximation and is labelled as such everywhere it
appears. No imputation: listwise deletion only; every n and cluster count is reported.

---

## 1. Question

Does more education move with **higher economic complexity** — the user's hypothesis — in the 30-country panel
1995–2024? This is a **different question from ECI → growth** (already tested and negative, `longitudinal_2026-11-20`).

## 2. Data (fixed paths, observed unless labelled)

| role | file | variable | status |
|---|---|---|---|
| panel source | `09_relations/data/panel_wdi_long.csv` (long: iso3, indicator, year, value) | WDI/UIS indicators | observed |
| ECI | `09_relations/data/economic_complexity_panel_30ctys.csv` (Growth Lab, Harvard Dataverse `doi:10.7910/DVN/XTAQMC`, CC0) | `eci_sitc` (primary), `eci_hs92` (robustness) | observed |
| controls | `panel_wdi_long.csv` | `log GDPpc` = ln(`NY.GDP.PCAP.KD`, clip 1e-3); `urban` = `SP.URB.TOTL.IN.ZS` | observed |

Window: **1995–2024**, 30 countries. **Outcome: `eci_sitc`.** Robustness outcome: `eci_hs92`.

### Education regressors (7)

| key | WDI series | label |
|---|---|---|
| `lit` | `SE.ADT.LITR.ZS` adult literacy 15+ | observed |
| `lit_youth` | `SE.ADT.1524.LT.ZS` youth literacy 15–24 | observed |
| `prm_cmpt` | `SE.PRM.CMPT.ZS` primary completion rate | observed |
| `lsec_cmpt` | `SE.SEC.CMPT.LO.ZS` lower-secondary completion | observed |
| `cuat_up` | `SE.SEC.CUAT.UP.ZS` upper-secondary attainment (% 25+) | observed |
| `cuat_ba` | `SE.TER.CUAT.BA.ZS` tertiary attainment (% 25+) | observed |
| `mys_proxy` | declared formula: `6 + 6*(SE.SEC.CUAT.LO.ZS/100) + 3*(SE.SEC.CUAT.UP.ZS/100) + 4*(SE.TER.CUAT.BA.ZS/100)` | **DERIVED** |

All education variables enter **in levels** (percentage points) so coefficients are comparable across levels
("ECI points per pp"). Exceptions: the declared cross-check in §6 uses logs, because the existing file did.

### Lags

**L = 5 and L = 10 years, implemented as true calendar-year lags** (`y_{t}-y_{t-L}` within country, joined on year;
rows missing either endpoint are dropped, never interpolated). Rationale: the existing file's key result uses a
10-year lag, but its implementation shifts *rows* not years on an unbalanced panel — the cross-check in §6
quantifies any difference.

## 3. Specifications (all predeclared; all cells reported)

- **S1 — long differences (cross-section).** For each country: ΔECI = mean(2015–2024) − mean(2005–2014); Δedu = mean(2010–2019) − mean(2000–2009) (education change starts a decade earlier). OLS on the country cross-section; controls as in the control set; heteroskedasticity-robust (HC1) SE. Expected **DATA LIMITED** at 30 countries with sparse education series; reported as declared, not redefined.
- **S2 — annual two-way FE.** `ECI_{c,t} = β·edu_{c,t−L} + controls + country FE + year FE + ε`; CR1 SE clustered on country; the workhorse spec.
- **S3 — 5-year non-overlapping blocks.** Block means (1995–99, 2000–04, …, 2020–24); `ECI_block = β·edu_(block−L) + country FE + ε`; CR1 clustered on country. (Mirrors the longitudinal S3 convention.)
- **S4 — within/between decomposition.** *Between:* country means regressed on lagged country means (HC1, n = countries). *Within:* annual values demeaned by country and year, same lag; CR1 clustered.
- **S5 — reverse order (descriptive, symmetric).** `edu_{c,t} = β·ECI_{c,t−L} + controls + country FE + year FE + ε`, CR1 clustered. Reported for symmetry; **no direction claim either way.**
- **S6 — heterogeneity by baseline complexity.** Baseline = mean `eci_sitc` 1995–1999 per country; split at the **sample median** into LOW and HIGH baseline groups. S2 (C1) run by group with L = 10 (and L = 5 as robustness). Slope difference tested by country-level bootstrap (B = 1000, PCG64 seed 20261120) reporting a percentile 95% CI. No sign expectation is imposed; the user's question — does education build complexity **from a low base** — is answered by the sign and magnitude of the LOW-vs-HIGH difference, not by the verdict rule.

**Control sets:** `C0` = none; `C1` = `log GDPpc` + `urban`. Both are reported for every spec so the reader sees what
controls do. (GDPpc is arguably a mediator of complexity; C1 is therefore presented as the conservative/adjusted
version, C0 as the unadjusted one — both shown, neither hidden.)

## 4. Verdict rule (frozen; primary outcome `eci_sitc`)

For each level `L` and lag `ℓ ∈ {5,10}`:
1. **DATA LIMITED** if the S2 or S3 cells required by rule 2 have n < 20 or < 8 country clusters.
2. **SUPPORTED** if the coefficient is **positive with a 95% CI excluding 0 in ≥ 2 of the 4 cells** {S2, S3} × {C0, C1} **and** at least one of the two C1 cells (S2-C1, S3-C1) is positive-significant.
3. **PARTIAL** if (a) positive-significant in exactly 1 of the 4 cells, or (b) positive in both C1 cells with neither CI excluding 0.
4. **NOT SUPPORTED** otherwise.
5. **BLOCKED** if the level has no usable cells at all.

The 14 (7 levels × 2 lags) cells are **multiplicity-flagged**: no false-discovery correction is claimed; the
verdict rule is a declared descriptive bar, not a hypothesis test family. Any "SUPPORTED" label is descriptive.
Robustness: the whole rule is recomputed on `eci_hs92`; a verdict **ROBUST** iff unchanged. No sign flips are
hidden — every cell is written to `results/RESULTS_ALL.csv`.

## 5. Cross-check of the existing result (declared, not a new test)

`09_relations/LITERACY_ECI_DEMOGRAPHY.md` E5: `eci_hs92 ~ log(prm_cmpt_{t−10})`, two-way FE, n = 253, 23
countries, **0.593 (se 0.176, p = 0.001)**. The new script reproduces that exact specification cell — including its
row-shift lag implementation and its full 1960–2024 panel — as `CROSSCHECK_EXISTING.csv`. It must match the
published number to within rounding; if it does not, the discrepancy is reported and the data assembly is
investigated before any new result is read. A true calendar-year 10-year lag version of the same specification is
reported alongside, so the two lag implementations are compared explicitly.

## 6. Output contract

`results/RESULTS_ALL.csv` (one row per spec × level × lag × control set × outcome; columns: spec, outcome, level,
lag, controls, coef, se, t, p, ci_lo, ci_hi, n, n_ctry, n_blocks, period, verdict_cell, label, note);
`results/VERDICT_MATRIX.csv` (level × lag verdicts, primary outcome, with the four component cells);
`results/ROBUSTNESS_HS92.csv` (same matrix, `eci_hs92`, ROBUST flag);
`results/HETEROGENEITY.csv` (S6 slopes by baseline group + bootstrap difference);
`results/CROSSCHECK_EXISTING.csv`; `results/RUN_MANIFEST.json` (hashes of this file, data files, code, results);
`FINDINGS.md`. Determinism: one PCG64 stream, seed 20261120, floats written at `%.10g`; **two clean runs must be
byte-identical**.

## 7. What this analysis cannot claim

It cannot say education *causes* complexity; it cannot say either direction; it cannot speak for countries outside
the 30-country Asia+comparator panel; it cannot use `mys_proxy` as an observation; it cannot read a null as
"education does not matter" (measurement, sparsity, and the joint determination of ECI with income all remain
live). It is a descriptive association map for the user's hypothesis, with the existing on-disk result used as an
anchor, not re-litigated.
