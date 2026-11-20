# STATUS — relations layer (09_relations), task-21, P4-conditional / P4-pending

**Agent:** `pattern-scout` · closed 2026-11-20 under Council brief 008. Scope limited to `09_relations/`.

## COMPLETE

| Deliverable | Status | Content |
|---|---|---|
| `RELATION_CANDIDATES.csv` | **complete, 30 rows** | 30 candidate relations: outcome, driver, mechanism, sign, estimate, SE/range, unit, sample countries/years, method, identification grade, country-type heterogeneity, data source (file+spec), literature source, model mapping, confidence, test experiment. Grades: 1 plausibly-causal (R07), 21 correlational, 7 not-identifiable/blocked, 1 verified causal target imported (R28). |
| `DATA_PATTERNS.md` | **complete** | 66 panel specifications (two-way FE + first differences), 110 heterogeneity splits, 19 event-window estimates, 17 shadow-education gradient rows, with sample sizes, SEs, periods and caveats. All numbers generated from `data/*.csv`, not typed by hand. |
| `MODEL_PLUG_MAP.md` | **complete** | Exact plug points in `twoway.py` (eps_ec, d_ec, births, n_cm/e_cm/F_cm, T_S/T_C, inc_sig, cap_*, F_*) and `massabm` (cost_*, cap_cost, tuition_path, cct_path, bar_board, N); functional forms; in-model validation experiments; an explicit "do not plug in" list. |
| `COUNTRY_TYPOLOGY.md` | **complete (first pass)** | Six conditional relations (T1–T6) with split-sample numbers; the unifying condition ("is the state the binding constraint on places?"); per-preset table (PHL/KHM/HK/CHN/KOR-JPN). |
| `data/` | **complete** | `panel_wdi_wide.csv` (30 ctys × 1970–2024 × 45 indicators, observed only), `panel_wdi_long.csv`, `panel_results.csv` (66 specs), `panel_heterogeneity.csv` (110 specs), `event_windows.csv`, `event_windows_gmr.csv`, `shadow_gradients.csv`, `country_typology.csv`. |
| `scripts/` | **complete** | `fetch_wdi_parallel.sh`, `fetch_wdi_panel.sh`, `build_panel.py`, `panel_lib.py` (two-way FE + CR1 clustering, from scratch), `analyze_panel.py`, `analyze_hetero_events.py`, `analyze_events_gmr.py`, `make_datapatterns.py`, `build_register.py`. Every CSV is regenerable by running them in order. |
| `raw/wdi/*.json` | **complete** | 128 raw World Bank API payloads archived (indicator × country chunk), so the panel can be rebuilt offline. |

## PARTIAL

| Deliverable | What is missing |
|---|---|
| `LITERATURE_ELASTICITIES.md` | Written as a **stub with the verified anchors only** (from `02_lit/ECON_TARGETS.csv` and `02_lit/ECON_LIT.md`): returns 8.8%, EAP 8.7%, Clemens et al. wage ratio 3.99, Abarcar & Theoharides 9.0. The requested domains — spending→enrolment causal studies, school construction (Duflo 2001), teacher supply, CCTs, migration/remittances, private schooling, tutoring demand/fees — are **not yet compiled with page/table citations**. One row (R30, school construction) is in the register but flagged UNVERIFIED because the original was not retrieved. |
| Event windows | PHL K-12, PHL free tuition, CHN 1986, THA 1999, MYS 1996, IDN 1994 tested. **HKG 1971/1978, KOR 1974/2004, JPN, KHM 1996/2001 events are blocked**: the observed-only GMR panel has <13 usable secondary-GER observations per window (series start ~1998). Never imputed. Needs EDB (HK), KEDI (KOR), MoEYS (KHM) national series. |
| Data pulls for the 4 target countries | The wide panel is 30 countries but only 45 indicators. Missing: ILOSTAT informality (`SL.ISV.IFRM.ZS` returned an error payload — archived as bad file), EMIS dropout, national teacher-pay series, learning outcomes (PISA/TIMSS). |

## NOT DONE / BLOCKED

1. **Returns→tutoring (R26)** — not identifiable: 4 countries, 3 shadow survey years, no common instrument. Stays a prior (0.9).
2. **Tutoring price elasticity (R29)** — no credible estimate located (`ECON_TARGETS.csv` row 23 = unusable). Stays a prior (−1.1).
3. **Remittances→schooling (R15)** — cross-country FE gives a null; needs PHL household microdata (FIES/APIS are credentialed; `04_data/TARGETS_FLOW.csv` records the block).
4. **Causal spending→enrolment** — no instrument available in this pass; the register carries a correlational Asia-conditional elasticity and says so.
5. **Learning quality as an outcome** — no learning measure in the 30-country panel; the PTR→learning chain is untested here.

## Provenance notes

- All panel numbers: WDI live API access 2026-11-20, raw payloads archived. Observed cells only — `value is None` rows are dropped, never filled.
- The 04_data files (`gmr_observed_6countries_1970_2024.csv`) were used **observed-only**; the imputed companion file was never read as observations.
- Shadow numbers are copied from `04_data/shadow_round2/` with their original source, table and confidence; case-study (KHM) and low-confidence (China 2022) rows are labelled as such.

---

# ADDENDUM A1 (2026-11-20, after task close): literacy × GDP × ECI + population pyramids

Requested by Dr. Menefee after the task closed: *"a correlation between literacy rates and GDP and ECI... a lot of lit rate increases are just old illiterates dying. we need pop size and pyramids too."*

## COMPLETE for the addendum

| Deliverable | Status | Content |
|---|---|---|
| `LITERACY_ECI_DEMOGRAPHY.md` | **complete** | ECI (Growth Lab, Harvard Dataverse, CC0) × GDP × literacy tests E1–E17; cohort-replacement decomposition D1–D2; population pyramids; caveats. |
| `RELATION_CANDIDATES.csv` | **extended to 40 rows** (R31–R40) | literacy×GDP, ECI×GDP, ECI×flow vs stock, ECI→growth null, Growth-Lab-projection null, cohort replacement, youth-literacy production, pyramid measurement caveat, within-cohort residual. |
| `data/` | **complete** | `panel_wdi_eci.csv`, `eci_literacy_results.csv`, `eci_growth_crosssection.csv`, `literacy_cohort_decomposition.csv`, `literacy_decomposition_regressions.csv`, `population_pyramids.csv`, `literacy_country_examples.csv`. |
| `raw/` | **complete** | `eci_growth_proj_rankings.csv` (Growth Lab), `eci_data_dictionary.csv`, plus the new WDI payloads (literacy, CBR/CDR/LE, population). |
| `scripts/analyze_literacy_eci.py`, `scripts/append_register_literacy_eci.py` | **complete** | end-to-end reproducible. |

## Headline of the addendum

1. **Median 62–66% of observed adult-literacy gains is cohort replacement**, not learning (24 countries, 241 country-periods; entrant-flow coefficient 1.655, se 0.526). A literacy rise is largely old illiterates dying and young literates entering.
2. **Literacy does not track GDP within country** (3.91, se 2.67, ns) and **does not track ECI** (0.001, se 0.005, ns), while **ECI does track the schooling FLOW** — primary completion t−10: 0.593 (se 0.176). Flow, not stock.
3. **ECI's published growth premium does not replicate here**: 10y growth on ECI = −0.068 (se 0.067, year-FE cross-section) and −0.158 (0.101, two-way FE); the Growth Lab `growth_proj` also fails (−0.004, se 0.020). Sample/period-specific or wrong; do not use ECI as a growth driver without resolving.
4. **Pyramid caveat**: PHL 1980→2020 literacy +15.2pp while 0–14 share fell 44.3→30.7; CHN +31.2pp with 65+ 4.6→12.6. Report attainment by cohort, never as an aggregate rate alone.

## PARTIAL / blocked in the addendum

- **5-year age bands unavailable**: WDI API v2 does not serve `SP.POP.1519.TO.ZS` / `SP.POP.2024.TO.ZS` (invalid value), so the pyramid is 3-band and the 15–24 share is proxied from births 15 years earlier (derived, flagged).
- **China literacy too sparse** in WDI (one usable period) — needs the census series 1982/1990/2000/2010/2020.
- **No adult literacy series for KOR/JPN/HKG** — the developed benchmarks are absent from the literacy decomposition.
- **The exit component is bounded, not estimated** (the dying cohort's literacy is unobserved); the 0.62–0.66 replacement share is conditional on that bound.
- **KHM/LAO/LKA/VNM show replacement >1** — within-cohort literacy loss or series revision; cannot separate the two without the original census tabulations.

---

# ADDENDUM A2 (task-28): economic complexity as a model metric

**Status: COMPLETE.** Deliverables added:

| Deliverable | Status | Content |
|---|---|---|
| `data/economic_complexity_panel.csv` | **complete** | 180 rows (CHN/HKG/JPN/KHM/KOR/PHL x 1995-2024), 27 columns: ECI SITC/HS92/HS12 + ranks, growth_proj, in_rankings, `eci_pctile`, `eci_z_year`, `eci_growth_5y`, `complexity_gap` (ECI minus income-implied ECI), `complexity_quadrant`, and merged gdppc / tertiary GER / secondary GER / completion / spending / wage-and-salaried share / vulnerable share / youth literacy / urban / population / fertility. Ready to ingest; no proxies used. |
| `data/economic_complexity_panel_30ctys.csv` | **complete** | ECI column set for all 30 panel countries (1995-2024) used in the panel tests. |
| `data/complexity_results.csv` | **complete** | C1-C12: ECI -> tertiary GER, completion, formal share, growth, secondary GER, upper-secondary, literacy; ECI-vs-income horse races. |
| `data/complexity_conditioning.csv` | **complete** | X1-X8: ECI x spending interactions, ECI x income, ECI x schooling -> growth (returns channel), completion -> wage share. |
| `data/complexity_metric_choice.csv` | **complete** | coverage, cross-variant correlation, within-R2 and stability comparison for eci_sitc vs eci_hs92. |
| `RELATION_CANDIDATES.csv` | **49 rows** | R41-R49 appended (ECI -> tertiary/completion/secondary/formal/growth/literacy, ECI x spending null, ECI x schooling negative, metric choice). |
| `DATA_PATTERNS.md` §9, `COUNTRY_TYPOLOGY.md` §7, `MODEL_PLUG_MAP.md` §E | **complete** | complexity specs, the complexity typology cells, and the plug map with the "do not plug" list. |

**Headline answers:** (1) coverage for the six countries is complete 1995-2024 for SITC and HS92. (2) Complexity does NOT condition the spending->enrolment channel
(interaction 0.081, se 0.080); it DOES condition the education->growth channel negatively (tertiary x ECI -0.077, se 0.020). (3) Best single metric: `eci_hs92`
(primary) with `eci_sitc` as robustness (r = 0.983); never ranks, growth_proj or spliced HS12.

**Partial/caveats:** the formal-share channel (R44) is sign-only (p=0.15); the education->growth interaction (R48) is correlational and could be convergence rather than
complexity; complexity is a country-level index, not a mechanism.
