# Longitudinal battery 2026-11-20 — education, literacy, ECI and growth (user-directed re-run)

**Status: PREDECLARED BEFORE ANY RUN.** Thresholds and falsifiers fixed at this file's sha256 (recorded in
`RUN_MANIFEST.json`). **Descriptive/associational only — no causal claim, no push/pull direction claim (R13/D77).**
The user's question (restated from the 2015 UIS/Excel experience): *years of schooling did not seem to move with
GDP growth, but literacy did; what actually co-moves with what, longitudinally, and does economic complexity (ECI)
gate the education→growth link — with thresholds where the economy has not "kickstarted"?*
This is a **new user-directed analysis**, not a reopening of the closed phase's claims (D76): it uses the on-disk
30-country panel and the ECI panel, and it makes no claim about massification reproduction.

## 1. Data (on disk, read-only), window 1995–2024 (ECI availability)

- `09_relations/data/panel_wdi_long.csv` — 30 countries, 62 indicators, 1971–2024. Used:
  `SE.ADT.LITR.ZS` (adult literacy, % 15+; 275 rows / 28 countries), `SE.ADT.1524.LT.ZS` (youth literacy; 315/28),
  `SE.PRM.CMPT.ZS` (primary completion; 522), `SE.SEC.CMPT.LO.ZS` (lower-secondary completion; 517),
  `SE.SEC.CUAT.UP.ZS` (upper-secondary attainment %25+; 418/30), `SE.TER.CUAT.BA.ZS` (tertiary attainment; 225/27),
  `NY.GDP.MKTP.KD.ZG` (GDP growth, annual; 900), `NY.GDP.PCAP.PP.CD` (GDP pc PPP; 900),
  `SP.URB.TOTL.IN.ZS` (urban; 900), `SL.SRV.EMPL.ZS` (services; 450 / 15 countries — sparse; reported only).
- `09_relations/data/economic_complexity_panel_30ctys.csv` — 30 countries, 1995–2024: `eci_sitc` (primary ECI),
  `eci_hs92` (robustness), `eci_hs12`.
- Window: **1995–2024** (ECI availability). Sample: the 30 on-disk countries. Africa coverage is **5 countries
  (EGY, KEN, MAR, NGA, ZAF)** — any "Africa" reading is out of scope; a Sub-Saharan extension is a DATA ASK.

### Declared derived proxy — `MYS_proxy` (mean years of schooling)

True mean-years-of-schooling is **not on disk** for the 30-country panel. Declared proxy (crude, cumulative
attainment approximation, `derived`):

`MYS_proxy = 6 + 6·(SE.SEC.CUAT.LO.ZS/100) + 3·(SE.SEC.CUAT.UP.ZS/100) + 4·(SE.TER.CUAT.BA.ZS/100)`

(assumes 6 years of primary for all; adds 6 for at-least-lower-secondary, 3 for at-least-upper-secondary, 4 for
tertiary). It is **not** a measured MYS and is used only as the "years-of-schooling" side of the horse race; every
row using it is labelled `derived` and states the formula. No imputation: cells are used only where all components
are observed (listwise deletion, counts reported).

## 2. Estimands and specifications (all run and reported; every null reported)

- **S1 cross-section** (time-averaged 1995–2024): `growth_avg ~ literacy_avg + MYS_avg + ECI_avg + log(GDPpc_1995)`.
  n ≈ countries with all cells (reported).
- **S2 country FE + year FE, annual**: `growth ~ literacy + MYS_proxy + ECI + urban` (unbalanced panel).
- **S3 5-year block averages** (non-overlapping 1995–99 … 2020–24), country FE.
- **S4 long differences**: (2015–24 mean) − (1995–2004 mean): `Δgrowth ~ Δliteracy + ΔMYS + ΔECI`.
- **S5 interaction**: `growth ~ literacy + MYS + ECI + literacy×ECI + MYS×ECI`.
- **S6 ECI-tercile split** (terciles formed on within-country-demeaned ECI): literacy and MYS slopes per tercile;
  high-ECI minus low-ECI slope difference with bootstrap CI (1000 reps, seeded).
- **S7 reverse check** (descriptive symmetry, no direction claim): `Δliteracy`, `ΔMYS`, `ΔECI` on **lagged**
  `growth` (lag 5), same FE.
- **S8 co-movement matrix**: within-country correlations among growth, literacy, youth literacy,
  primary/lower-sec completion, upper-sec/tertiary attainment, MYS_proxy, ECI, urban — every pair, with n and
  permutation p-values (seeded); no direction claim.
- **Robustness** (reported alongside): `eci_hs92` instead of `eci_sitc`; exclude HKG and SGP (city-states);
  exclude 2020–21 (COVID); youth literacy instead of adult literacy.

**Estimator:** OLS with country-clustered SEs (CR1); FE via within transformation; standardized coefficients
reported for the horse race (so magnitudes are comparable across differently-scaled variables). `n` and number of
clusters always reported. Where a series is too sparse the cell is `DATA LIMITED` (never imputed).

## 3. Predeclared hypotheses, thresholds and falsifiers

**H1 — the 2015 horse race (literacy vs years of schooling).**
*Threshold:* in S2 (country FE), **literacy** has a positive coefficient with CI excluding 0 **and** `MYS_proxy`
is either (a) not significant (CI includes 0) or (b) has a standardized |coef| < 0.5 × literacy's.
**Falsifier → NOT SUPPORTED:** `MYS_proxy` positive and significant while literacy is not; or both null; or
literacy significant only in S1 cross-section but not in S2/S3/S4.
*Reading if supported:* "with these data, literacy moves with growth and the schooling-years proxy does not" —
descriptive, not causal.

**H2 — ECI matters.**
*Threshold:* `ECI` positive with CI excluding 0 in S2 and S3. **Falsifier:** CI includes 0 in both, or sign flips
between S2 and S3.

**H3 — threshold/gating ("the economy has not kickstarted").**
*Threshold:* in S6 the literacy (or completion) slope in the **high-ECI tercile** is larger than in the
**low-ECI tercile** by ≥ 50% of the low-tercile magnitude, with the same sign and a bootstrap CI excluding 0 for
the difference. **Falsifier → NOT SUPPORTED:** the difference is not in that direction, or the CI includes 0.
*Reading if supported:* "the education–growth association is steeper in more complex economies" — descriptive;
**not** an Africa claim, **not** a causal claim.

**H4 — what moves together (S8).**
No threshold: report the full within-country co-movement matrix. A pair is flagged `stable` only if |r| ≥ 0.4
with permutation p < 0.05 and the sign is stable across adult/youth literacy and across the two levels tested.
Nothing here is a direction claim.

**Verdict vocabulary:** `SUPPORTED` / `NOT SUPPORTED` / `PARTIAL` / `DATA LIMITED` / `UNABLE`. All specifications
are reported including nulls. **No causal language.** The audits' corrected push-pull orientation is recorded
(income growth → tertiary GER is the correctly-oriented association; education→growth null) and is **not** treated
as a direction result (R13).

## 4. Reporting rules

1. Predeclared thresholds frozen at this file's sha256; no post-hoc change.
2. Every row labelled `derived` (MYS_proxy, ECI merges) or `observed`; the MYS_proxy formula printed next to any
   row that uses it.
3. `n`, countries, years, clusters on every estimate; `DATA LIMITED`/`UNABLE` reported, never dropped or imputed.
4. Deterministic scripts, declared seeds for bootstrap/permutation; the Lead re-runs and requires byte-identical
   results.
5. No causal or direction claim; no claim about Africa; closed phase untouched (D76).
