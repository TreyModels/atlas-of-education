# Lab battery 2026-11-20 — findings (secondary & post-secondary, geo scale × economy)

**Status: OBSERVED/DERIVED descriptive analysis; no causal or direction claims.** Ten predeclared experiments
(`PRE_DECLARATIONS.md`, sha 148d814e2f6f8f6a) run once on data on disk; all specifications and nulls reported;
thresholds fixed before the run. Results in `results/`; code `code/lab.py`; manifest `RUN_MANIFEST.json`.

## Verdict summary

| # | question | key estimate | predeclared verdict |
|---|---|---|---|
| E1 | income/urban/services gradient, upper-sec GER (6 systems, 1995–2024) | within slope **+56.1** GER pp per log GDP (se 19.6; CI +17.7…+94.4; n=93, 5 countries); between +159.9 (n=5, uninterpretable) | **strong within association** — driven by CHN/KHM growth; robustness drop-CHN +71.4, drop-HKG +34.9, total-secondary +51.5 |
| E2 | structural conditions at milestone crossings | no milestone is structure-typical: max fraction inside cross-country GDP IQR = **0.60** (3/5); medians vary widely (e.g., secondary≥90 GDP p.c. median ~$19.2k, IQR $29.7k) | **not typical** — crossing structure is heterogeneous |
| E3 | PHL regional equalization (17 regions, 2 cohorts) | Gini~MYS slope **−0.055** (1960–64 cohort) → **−0.051** (1990–94); Gini fell ≥0.02 in **17/17** regions | **equalizing** |
| E4 | city-state vs large-country shape (HKG vs CHN/PHL/KHM) | duration ratio large/HKG **1.10** (no clear); volatility ratio large/HKG **0.33** → large countries smoother (HKG more volatile) | city-state **not faster**; large **smoother** — n≤4, descriptive |
| E5 | structure and tertiary expansion (30 countries) | within services slope **−0.49** (se 0.22) but sign flips without log GDP **+1.82** | **not robust** (collinearity suppression); no stable association |
| E6 | formalisation and upper-secondary completion (6 systems) | within r completion×wage-share = **+0.59 at lag 5** (n=39, 4 countries); lag0 +0.64 | **association** (descriptive; only 4 systems have completion) |
| E7 | state capacity around lower-secondary crossings | only **delivery** capacity has coverage; delivery Δ **−0.15 SD**; fiscal/enforcement missing | **DATA LIMITED** — cannot test the 3-dimension rule |
| E8 | PHL infrastructure strain during secondary expansion | dPTR on dGER slope **+0.24** (se 0.19) | **no strain** (below the >1.0 rule) |
| E9 | remittances, spending and enrolment growth (6 systems) | spending −0.046 (se 0.031); secondary growth −0.0007 (se 0.0013); tertiary growth −0.0024 (se 0.0014) | **no association** |
| E10 | external replication of E1 (30 countries) | 30-country pooled slope **+14.7** (se 8.3; CI −1.6…+31.0; n=14) vs E1 **+56.1** | **does not replicate** — E1 is not transferable at the 30-country scale |

## What looks real (descriptive)

1. **Within-system, upper-secondary enrolment rises strongly with income** in this six-system panel — but the
   slope is enormous (≈56 GER pp per log point) and sensitive to China's growth path; the between-country
   estimate is uninterpretable (5 points). **No cross-country replication** at the 30-country scale (E10).
2. **The Philippine regional record is equalizing across cohorts**: education Gini fell in every region and the
   cross-region Gini–schooling gradient is negative in both cohorts (E3). This is the cleanest result in the battery.
3. **Crossings are structurally heterogeneous**: no milestone has a typical income/urbanisation/agri profile
   (E2); there is no single "crossing package".
4. **Scale changes volatility, not speed** in this tiny sample: HKG crossed in similar time but was more volatile
   (E4); city-state advantage is not visible in duration.
5. **Formalisation tracks completion contemporaneously** (E6), but the association is not a mechanism and only
   four systems have completion series.
6. **No strain visible in PHL PTR** during secondary expansion (E8), consistent with capacity being built ahead
   of/alongside enrolment rather than lagging it.

## What did not survive

- **Services-share → tertiary expansion** (E5): statistically significant only under a collinear specification;
  the sign flips when income is dropped → **not robust**.
- **Remittances → spending/enrolment** (E9): null in all three specs on the six-system panel.
- **Capacity around crossings** (E7): cannot be tested — fiscal/enforcement series are missing at the needed
  windows; reporting it as "capacity-linked" would be a data artefact.
- **E1's magnitude as a general law**: fails the 30-country replication (E10) and is driven by China/KHM.

## Limits

Small n (5–6 systems for E1/E6/E9; 4 for E4; 14 usable 30-country upper-sec observations for E10); upper-secondary
GER is sparse; completion series only 4 systems; capacity dimensions mostly blocked; all results descriptive and
predeclared, robustness checks are labelled post-hoc; `status` (observed/derived/check) carried from sources.
Nothing here reopens the closed phase's C1–C4; E1/E10 are consistent with the earlier wrong-sign scaling finding
(model class lacks a supply channel), not evidence about the world.
