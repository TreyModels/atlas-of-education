# Longitudinal battery 2026-11-20 — literacy vs schooling-years vs ECI vs growth

**Status: DESCRIPTIVE / ASSOCIATIONAL — no causal claim, no push/pull direction claim.** This is the user-directed
re-run of the 2015 UIS/Excel question ("years of schooling didn't move with growth, literacy did"), made
longitudinal and using ECI. **Predeclared before running** (`PRE_DECLARATIONS.md`, sha256
`bff1c3ec39cdd76d984e04038cafac6124073714642e2794c0fc87eba7270d91`); executed by a DeepSeek Flash worker; Lead
re-ran and verified. It does **not** reopen the closed massification phase (D76) and makes no massification claim.

## Plain-English answer

**Your 2015 hunch survives only partially — and in an interesting way.** In the 30-country panel (1995–2024,
country + year fixed effects):

- **Literacy vs years-of-schooling.** In the annual within-country spec neither is statistically distinguishable
  from zero (literacy 0.45 standardized, CI −0.43…+1.32; the schooling-years proxy 0.87, CI −1.50…+3.24). But in the
  **5-year block** spec the sign pattern matches your memory: **literacy +1.52 (CI 0.54…2.50)** while the
  **schooling-years proxy is −1.59 (CI −2.24…−0.94)**. Verdict **H1 = PARTIAL**: the direction you remember is there
  at lower frequency, but it is not a stable annual within-country result.
- **ECI does not pay the expected growth premium in this sample.** It is not positive-significant in either
  within-country spec; in the 5-year blocks it is **negative-significant** (−2.59, CI −4.11…−1.07) — the opposite
  of the complexity-growth canon's predeclared sign; the unconditional within-country growth~ECI correlation is also
  negative (r = −0.153, p = 0.001, n = 895). **H2 = NOT SUPPORTED** (fails the predeclared positive-sign rule).
- **The "economy hasn't kickstarted" threshold is not supported.** ECI-tercile literacy slopes are +0.022 (low),
  +0.370 (mid), −0.014 (high); high−low = −0.036 (bootstrap CI −0.65…+1.64). No monotone gating. **H3 = NOT
  SUPPORTED.** This is a 30-country Asia+comparator sample — **not** a claim about Africa.
- **What moves together.** 17 of 45 within-country pairs reach |r| ≥ 0.4 with permutation p < 0.05 and stable sign —
  but the strongest are largely compositional/mechanical (attainment ↔ attainment-based MYS proxy r=0.92;
  adult literacy ↔ youth literacy r=0.91; tertiary attainment ↔ MYS r=0.83; lower-secondary completion ↔
  urbanisation r=0.67). **H4 = SUPPORTED as a descriptive co-movement map**, not as a growth result.
  **Growth is the weakly-attached variable:** all nine growth pairs in the matrix are |r| < 0.21 and negative
  (growth~MYS −0.203, growth~ECI −0.153, growth~lit −0.091, growth~cuat_ba −0.191, growth~cuat_up −0.132,
  growth~urban −0.089, growth~lit_youth −0.079, growth~lsec_cmpt −0.029, growth~prm_cmpt −0.006). Within these
  countries, GDP growth co-moves weakly with *every* education/complexity series tested — so the horse race is
  unresolved on the growth side, and no series should be read as "the" growth driver.

## Specification table (standardized coefficients, CR1 clustered by country)

| spec | literacy | MYS_proxy (derived) | ECI | n | clusters |
|---|---|---|---|---|---|
| S1 cross-section, 1995–2024 means | 0.273 [−0.09, 0.63] | −0.285 [−1.12, 0.55] | −0.025 [−0.54, 0.49] | 25 | 25 |
| S2 annual, country+year FE | 0.447 [−0.43, 1.32] | 0.871 [−1.50, 3.24] | −0.581 [−1.63, 0.47] | 127 | 23 |
| S3 5-year blocks, country FE | **1.520 [0.54, 2.50]** | **−1.591 [−2.24, −0.94]** | **−2.589 [−4.11, −1.07]** | 62 | 25 |
| S4 long differences (2015–24 − 1995–2004) | DATA LIMITED | DATA LIMITED | DATA LIMITED | 5 | 5 |

`MYS_proxy = 6 + 6·(lower-sec attainment/100) + 3·(upper-sec attainment/100) + 4·(tertiary attainment/100)`; a
crude **derived** approximation of mean years of schooling, not a measured series. Annual growth is noisy and the
literacy series is survey-sparse (275 rows / 28 countries over 30 years) — a null in the annual spec is a statement
about resolution, not about literacy's real effect. S4 is `DATA LIMITED` (5 countries with all cells in both
periods: CHN, LKA, MNG, MYS, SGP; predeclared minimum n≥20 and ≥8 clusters) — reported, not redefined.

## The literature caveat (important)

The repo's `LITERATURE_LEDGER.md` contains **zero** entries for Hanushek, Woessmann, cognitive skills, ECI,
Hidalgo–Hausmann, Scho­fer, Becker, Mincer or growth — it is a private-tutoring ledger. So the expectations side of
this note **cannot** be attributed to literature on disk: the horse race is the user's 2015 **programme prior**
(D93), and the ECI-growth canon is **unverified** here. Every row in `lit/EXPECTATIONS.csv` is labelled
PROGRAMME-PRIOR / UNVERIFIED / BLOCKED — no STANDARD-CITATION row. **A data ask**: add the knowledge-capital and
Hidalgo–Hausmann sources to the ledger before any write-up attributes the horse race to the literature.

## Limits

30 countries (Asia + comparators), 1995–2024; unbalanced; literacy survey-sparse; MYS is a derived proxy; annual
growth noisy; ECI is a modelled index; **no causal claim, no direction claim, no Africa claim**; the audits' finding
that ECI→growth is negative in this sample (audit `literacy_*`, and the regression audit's corrected push-pull
orientation) is consistent with H2/H3 and must not be spun as support for the complexity-growth canon.

## Files

`PRE_DECLARATIONS.md` (frozen), `stats/` (all specs, `RESULTS.csv`, worker `FINDINGS.md`, `RUN_MANIFEST.json`,
`code/run.py`), `lit/` (`EXPECTATIONS.csv`, `SYNTHETIC_TARGETS.md`, `PLAIN_ENGLISH.md`), `README.md`,
`RUN_MANIFEST.json`, `SHA256SUMS.txt`.
