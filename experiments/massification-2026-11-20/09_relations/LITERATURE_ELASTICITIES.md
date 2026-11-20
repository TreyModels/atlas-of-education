# LITERATURE_ELASTICITIES — credible estimates from the literature, and the gaps

**Author:** `pattern-scout` · 2026-11-20 · task-21 · **PARTIAL (P4-pending)**. This file compiles only estimates that were
**verified at source in this project** — i.e. present in `02_lit/ECON_TARGETS.csv` / `02_lit/ECON_LIT.md` (compiled by
`lit-archivist`, full text or verified citation) or in `02_lit/COUNTRY_CARDS/` / `04_data/shadow_round2/`. The domains that
were requested but not compiled this session are named as gaps at the end rather than filled from memory.

**Rule applied:** every number below carries its source and access status. `FULL-TEXT` = read in this project; `TARGET` = a
verified calibration target; `UNVERIFIED` = cited but not retrieved — never to be promoted to a parameter.

---

## 1. Returns to schooling → enrolment and tutoring demand

| Quantity | Estimate | Identification | Source (verified) | External validity |
|---|---|---|---|---|
| Private return to one additional year of schooling, world | **8.8%/yr** (headline "about 9") | compilation of Mincer cross-sections 1950–2014, ~139 economies; **not causal** | Psacharopoulos & Patrinos (2018), WB PRWP 8402, p.1 + annex — FULL-TEXT | Best available placeholder; inherits every Mincer problem |
| Private return, East Asia & Pacific | **8.7%** | same | WPS8402 regional table — FULL-TEXT | Use for PHL/KHM/CHN/KOR until country annex extracted |
| Social return, EAP | **6.9%**; social returns >10% at secondary+ | same, public-cost adjusted | WPS8402 — FULL-TEXT | A check, not a target |
| Social vs private by income level | private: low 9.3 / middle 9.2 / high 8.2; social: low 5.0 / middle 7.0 / high 9.2 | same | WPS8402 annex — FULL-TEXT | Social returns *rise* with income; private returns fall slightly |
| Ability bias / causal-return critique | **NOT VERIFIED** — Clark & Nielsen (2024) not retrievable | — | ECON_LIT §1.3 | The size of ability bias is an unverified number in the argument |
| Country Mincer returns for PHL/KHM/CHN/KOR | **NOT SUPPLIED** | — | ECON_LIT §1.2 | Do not hard-code a country return |

**Relation to the register:** R26 (returns→tutoring) is **not identifiable** from the shadow data on disk (4 countries, 3 survey years). The
literature gives the *level* of returns but no estimate of the tutoring response to returns. `twoway.py`'s `+0.9*log1p(ret_S)` remains a prior.

## 2. Spending → enrolment, school construction, teacher supply

**Status: GAP.** No estimate was verified at source this session for (a) the effect of public education spending on enrolment,
(b) school construction (the canonical study is Duflo 2001, AER 91(4), on Indonesia's 1973–74 INPRES programme — **cited but not
retrieved**, hence R30 is flagged UNVERIFIED in the register, not used), or (c) teacher-supply effects on enrolment.
What this project *does* have is the panel evidence in `DATA_PATTERNS.md`: a spending→secondary-GER elasticity of **0.111** (se 0.065)
within 30-country FE, **0.189** in Asia, ~0 elsewhere. That is a correlational estimate, graded as such in R01.

## 3. The economy side — migration, formality, nurse supply

| Quantity | Estimate | Identification | Source | Note |
|---|---|---|---|---|
| PHL→US place premium, identical workers | **3.99×** (range 3.71–4.36; alt specs 3.80/4.36) | Mincer on >2m formal wage-earners, 43 countries, PPP; selection-corrected with New Immigrant Survey | Clemens, Montenegro & Pritchett (2008) WB PRWP 4671 — FULL-TEXT; `ECON_TARGETS` row 3 (TARGET) | PHL is at the cross-country median (Bolivia 3.98) |
| Nurses licensed in origin per additional nurse migrant | **9.0** | US visa-expansion DiD; province-year exam/entry panel; structural ratio | Abarcar & Theoharides (2024, REStat; NBER SI slides 2021) — FULL-TEXT; `ECON_TARGETS` row 4 (TARGET) | **The sharpest validation target in the project**: massabm produces 0.25 |
| Effect of US visa expansion on licensed nurses | **+3.9 per 100k = 126%** of pre-mean 3.1 | DiD around the expansion | Abarcar & Theoharides — FULL-TEXT | Supply response runs through programme entry *and* pass rates (implied pass rate 38.4%) |
| Non-nursing disciplines during the expansion | **decline** | same | Abarcar & Theoharides | Crowding/relative-price effect the model should reproduce |
| Firms citing inadequate workforce skills as a major obstacle | **10.1%** all firms (2009 7.8%); services **11.0%** | repeated cross-section, perception-based | World Bank (2017) *Developing Socioemotional Skills for the Philippines*, Table 2.1 — FULL-TEXT | Perception, not a requirement schedule |

**Not identified (confirmed gaps, ECON_LIT §7):** the elasticity of formal employment to educated labour supply (for any of our countries);
formal↔informal transition hazards; the informal earnings gap; the causal effect of credential requirements on hiring; the cost of
non-recognition of a credential abroad.

## 4. Shadow education — fees, providers, and the parameters nobody has estimated

| Quantity | Estimate | Source (verified) | Use |
|---|---|---|---|
| Korea private-education expenditure per student | **434,000 won/month** (553,000 per participating student); national total 27.1tn won (2023) | MODS/KEDI survey 2023, official English release — FULL-TEXT; `ECON_TARGETS` row 15 (TARGET) | Calibration target for `p_tut` in a KOR preset |
| Korea participation rate | **78.5%** (elem 86.0 / middle 75.4 / high 66.4) | MODS/KEDI 2023 Table 2 — FULL-TEXT; `ECON_TARGETS` row 16 (TARGET) | Calibration target; see R23 |
| Korea income gradient of tutoring spend | 183k won (<3m won/month) → **671k won** (≥8m won) | MODS/KEDI 2023 income table — FULL-TEXT | **Income elasticity ≈ 1.33** (derived, R22) — the strongest shadow relation in the register |
| Share of Korean secondary tutoring expenditure driven by competition | **77%** (89% in the final year) | Kang 2026, structural dynamic tournament model — FULL-TEXT; `ECON_TARGETS` row 22 | Declared `calibration-only`: a structural counterfactual, not an observed share |
| Cambodia tutoring fee | **US$0.08–0.25/hour**; 300–1,000 Riel; one-to-one up to US$100/month | Brehm & Silova WP39/2014 — FULL-TEXT; `ECON_TARGETS` row 17 | Fee level calibratable; 6-school case study, not national |
| Cambodia provider structure | own teachers teaching their own pupils in public buildings; **41.5%** of urban primary teachers name tutoring as out-of-school work; tutoring earnings ≈ **2/3 of monthly base salary** | Benveniste et al. 2008 via Brehm & Silova — SECOND-HAND | `twoway.py` `n_tt`/`e_tt` anchor: teacher-tutoring is the dominant Cambodian provider |
| Nepal tutoring fee | median **300 NPR/month** (govt), 400 (private); ≈ **US$3.9/month ≈ 23% of a month's GDP pc** | Jayachandran 2014, Appendix Table 2 — FULL-TEXT; `ECON_TARGETS` row 19 | Price point for a low-income setting |
| Nepal: share of students taking school-provided tutoring | **49%** | Jayachandran 2014 household survey — FULL-TEXT; `ECON_TARGETS` row 20 | Take-up benchmark at low income |
| Teacher effort when tutoring is for-profit | **−5.3pp** likelihood of not teaching the full period | student×subject FE, propensity trimming, SE clustered by school | Jayachandran 2014 — FULL-TEXT; `ECON_TARGETS` row 21 (TARGET) | The *diversion* mechanism in `tutoring_abm`; **causal**, best-identified shadow parameter |
| Hong Kong gate gradient | 35.1% (S1–3) → 46.6% (S4–5) → **70.3%** (S6–7) | Bray & Kwok (2003) EER 22:611-620, Table 1 p.616 — FULL-TEXT | R21: +35.2pp at the senior gate; the model's `R_gate` channel |
| Japan juku attendance | **41.8%** prefecture mean (range 22.1 Akita – 57.9 Tokyo), grade 6, 2018 | Rappleye & Komatsu (2020) EPAA 28(67), Table 2 — FULL-TEXT | R24: 2.62× urban/rural |
| China 2014 tutoring participation | **29.8%** primary+lower secondary | Liu & Bray (2020) *Educational Studies* 46(2):170-187, ERIC abstract | Medium confidence (survey table not retrieved) |
| China post-Double-Reduction | reported **<20%** participation | China Education Daily 2022-03-03 headline | **LOW** — newspaper headline, instrument unstated; not usable as an estimate (R25) |

**What the literature does NOT supply (and the model therefore cannot estimate):**
- **Price elasticity of demand for tutoring — NOT FOUND anywhere** (ECON_TARGETS row 23 = unusable; ECON_LIT §6.4). `twoway.py`'s
  `−1.1*(p/ret)` is a declared prior with no empirical basis. Sweep it; do not calibrate it.
- **Returns→tutoring response** — no study located.
- **The causal effect of the Double Reduction** on household investment — sources blocked (R25).
- **Private/commercial-provider entry elasticities** — no quantitative entry or concentration data retrieved.

## 5. Guidance for the modellers (what may and may not be calibrated)

**May be calibrated (observed, verified):** Korea participation 78.5% and spend 434k won; HK stage gradient 35.1/46.6/70.3; Japan
urban range 22.1–57.9; PHL place premium 3.99; nurse multiplier 9.0; Jayachandran teacher-effort −5.3pp; fee levels in KHM/NPL/KOR.

**May only be swept (priors, no estimate):** tutoring price elasticity; returns→tutoring coefficient; spending→enrolment elasticity
(Asia-conditional, correlational); `eps_ec` (the panel points *negative*, R13).

**Must not be used at all without new data:** any country-specific Mincer return for PHL/KHM/CHN/KOR; any causal claim from the
Double Reduction; the informality/formal-job elasticity; the credential-requirement effect.

## 6. Gap list for a next pass (P4-pending)

1. Extract the **country Mincer tables** from WPS8402's annex (exists, not extracted) for PHL/KHM/CHN/KOR.
2. Retrieve **Duflo (2001)** and the school-construction literature; verify R30 or drop it.
3. Retrieve the **CCT evaluations** (Fiszbein & Schady 2009; PHL 4Ps impact evaluations) → spending/transfer→enrolment causal anchor.
4. Retrieve **remittances→schooling** studies (the Yang/Clemens line) → R15.
5. Retrieve **private-schooling market entry** evidence (Andrabi et al. Pakistan LEAPS; India) → R09 causal anchor.
6. The blocked event windows (HK 1971/78, KOR 1974/2004, KHM 1996/2001) need national series, not more literature.
