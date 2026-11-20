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
