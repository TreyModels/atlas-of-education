# PRE-DECLARATION S1 NOTE (controller) — pre-run clarification of the country-ordering check

**Written:** 2026-11-20, AFTER `PRE_DECLARATIONS.md` was frozen (sha256 `cf8c61cb…`) and BEFORE any v1.3 run.
**This note changes NO threshold and NO parameter.** It records a conflict in the on-disk shadow record that the
dispatch brief did not carry, and fixes how one frozen check is to be *read*. It is binding on the v1.3 run.

## What the on-disk record actually says about the country ordering

The dispatch brief described the expected ordering as "HKG high, PHL mid, KHM low". The on-disk figures do **not**
establish that ordering, because the three headline rates are from different stages and sampling frames:

| country | headline rate | stage / sample | status on disk |
|---|---|---|---|
| HKG | **85%** (c.2010/2011) | **senior secondary**; second-hand quotation; source itself says surveys are not statistically robust | `02_lit/COUNTRY_CARDS/HKG.md:15`; `04_data/TARGETS_SHADOW.csv` row "senior secondary" |
| KHM | **68.4%** (2012-13) | **Grade 9**, two-school case study (1 urban, 1 rural), not national | `02_lit/SHADOW_TARGETS.csv`; `02_lit/COUNTRY_CARDS/KHM.md:15` |
| PHL | **46.5%** (2010) | **all basic education**, single select-sample survey (574/1,235), not nationally representative | `02_lit/SHADOW_TARGETS.csv`; `02_lit/COUNTRY_CARDS/PHL.md:15` |

At face value these give KHM (68.4) **>** PHL (46.5), which contradicts "PHL mid, KHM low". The stages are not
comparable (senior secondary vs Grade 9 vs all-basic), so **no country ordering is identifiable from these rates.**

## How the frozen checks are to be read

1. **c4a (HKG D ∈ [0.75, 0.95]) is the only empirical anchor**, and it is a wide band deliberately (±10 pp) because the
   source is second-hand, senior-secondary-only and of low survey robustness. It is a **reproduction of a declared
   level**, not a validation of any real system.
2. **c4b (D*_HKG − D*_PHL ≥ 0.10; D*_PHL − D*_KHM ≥ 0.05) is a DECLARED SYNTHETIC-REPRODUCTION CHECK on the model's
   cohort-incidence statistic D\***, driven by observed out-of-school exposure (§7 cohort weights), **not** a claim that
   the on-disk headline rates order the countries that way. If it fails, the FAIL and the exposure-vs-demand channel
   decomposition are reported; it is not rescued.
3. **c3 ("near-zero at primary") is a structural/consistency check of the module** (no gate, no rank competition,
   `V_g0 = 0`), **not an empirical prediction**. Observed primary-stage tutoring — PHL 23.8%, KHM 41.3% — is **out of
   this module's scope** and is not explained by it; it remains a declared gap, not a hidden residual.
4. The declared ex-ante risk in `PRE_DECLARATIONS.md` §8 stands: the gate channel and the return channel can pull in
   opposite directions for KHM; the ordering, if any, is carried by **cohort exposure**, not by demand intensity.

**No run may begin until this note is in the module and the v1.2 panel exists** (c6's no-re-fit guard).
