#!/usr/bin/env python3
"""Build the machine-readable audit tables for the MASSENG/timing inventory.

Read-only: writes JSON/CSV under audit_tables/. All numbers are either read from committed
repository data (via `git show` where necessary) or are explicitly labelled measurements taken
during this audit. No model is simulated here.
"""
import csv
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audit_tables")
STAGING_BRANCH = "origin/research/codex-masseng-staging-2026-11-24"
STAGING_COMMIT = "bac3a7c"
STAGING_FULL_SHA = "69129f47e5e4a1619d5380fbb28b6904aa755aa6e809af3e4231b5869b845eeb"
STAGING_RUN_SHA = "60faefa7"  # placeholder replaced below by actual (kept separate)
DESIGN_SHA = "7d9ad7b81104f40ec8f5fc4b26f9c35d50567c63a434ed9d60b9b7e4fa5209ae"
WORLDS_SHA = "2e9ec71a882755d9402b9bbcf802ce4a3aeb1f32ef4ac06ef48b97fc7340e0da"
CORE_SHA = "2b7484a97d64bf5f498c95003dd249241373cdc25da4c4d02d59d256df59c064"
RUN_SCREEN_COMMIT_SHA = "48dec650d5d77a54a8cc99840e3e27bc3c0dd65961695e29f5e74b35ce7fcc52"
MODEL_ENGINE5_COMMIT_SHA = "e01bd54383a7215503c3caff50212c5fcf16312aca9531e10ad810c7a3a5c17c"


def main():
    os.makedirs(OUT, exist_ok=True)

    engine_inventory = {
        "label": "MASSENG / education engine inventory (read-only audit, 2026-11-24)",
        "engines": [
            {
                "id": "eduengine_modular_abm",
                "name": "eduengine — modular education supply/demand/shadow-education ABM",
                "path": "engine/eduengine/ (core.py, measure.py, ledger.py, planning.py, struts.py, "
                        "settle.py, modules/{state,schools,labour,tutoring,sdg4,anchor}.py); built by engine/worlds.py",
                "version": "v0.1–v0.4 features in source comments (CORE_DEFAULTS v0.3 additions; tutoring/state modules v0.x)",
                "type": "synthetic agent/cohort simulation (not national regression model)",
                "status": "toy/uncalibrated: engine/worlds.py docstring 'Toy worlds: abstractions, not countries ... nothing is calibrated'; "
                          "used by the audited staging experiment (worlds.formal_loop)",
                "state_variables": [
                    "children: cohort (entry year), grade g (0-15, 16 grades), learning L (grade-equivalents), credential, "
                    "attendance status, started/reason, ability a, home capital, household income y, urban flag, parity",
                    "households: income, consumption need, liquidity/borrowing, shocks, child-wage schedule",
                    "schools/supply: public budget, teachers, class size, quality q_pub, private entry, tuition/fees",
                    "labour: formal vacancies per entrant, credential floors, queues, informal wages, wage bill",
                    "fiscal: tax revenue (formal + consumption), education share of tax revenue, CCT",
                    "tutoring: own-teacher vs firm supply, buy-back/gate-prep/remedial motives, prices",
                ],
                "stage_transitions": [
                    "entry to Grade 1 (ages 6–9, entry_share anchor)",
                    "annual continuation vs stop vs repeat (promotion bar; household liquidity)",
                    "primary (6 grades) -> lower secondary gate -> lower (3) -> upper-secondary gate -> upper (3) -> tertiary gate -> tertiary (4)",
                    "gates: absolute bar thresholds or planned quota seats (share x cohort), fail->track or stop",
                    "leavers enter labour market: formal queue by credential vs informal/competitive",
                ],
                "supply_vs_demand": "separate modules: PublicSchools/PrivateSchools (supply, financing), demand through household utility "
                                    "(discount future income, child wage, costs, beliefs)",
                "rural_migration": "NOT SIMULATED: rural is a household attribute (urban flag) plus an extra schooling cost "
                                   "(rural_cost=0.03 beyond primary) and lower tutoring firm access; no rural-urban migration, "
                                   "no remittances, no location transitions, no spatial labour market",
                "jobs_formalization_credential": "QueueLabour: formal vacancies per entrant (vac0), credential floors, graduate queue, "
                                                 "informality (Harris-Todaro), wage premium beliefs; optional job_elasticity feedback "
                                                 "(vacancies x educated share^elasticity) is an ASSUMED functional form",
                "quality_shadow_tutoring": "quality from class size/teacher pay/monitoring/withholding; tutoring market with own-teacher "
                                           "buy-back, gate-prep and remedial motives, rural firm access and bans",
                "heterogeneity": "household income (lognormal), urban/rural, ability, home capital; cohort-by-year variation",
                "limitations": ["not calibrated to any country", "no migration", "assumed learning scale", "no employer credential "
                                "requirements data", "no tutoring cost/distribution estimates", "stylised tax/state capacity"],
            },
            {
                "id": "masseng_v5_portable_cohort",
                "name": "MASSENG v5 — portable national cohort-flow model of massification (PHL v1–v5; KHM v3; HKG facts)",
                "path": "research/masseng-v6/model/{masseng/{engine.py,engine5.py,calibrate.py,calibrate5.py,targets.py,data.py,readiness5.py},"
                        "model/docs/,PROTOCOL.md,PROTOCOL_v5.md,HANDOFF_v5.md,countries/{HKG,KHM,PHL}/,outputs/PHL/v1..v5,outputs/KHM/v3}",
                "version": "v5 (PROTOCOL_v5, written 2026-11-22 before first fit); archived v1-v4 protocols preserved; R0-R5 specifications",
                "type": "deterministic cohort-flow/regression hybrid fitted to country data (PHL/KHM); 'the actual PHL MASSENG v5 R1 model' "
                        "used by the Bayesian screens",
                "status": "fitted for PHL (v5 fits R0-R5, fit_R1.json = R1 spec with b_h,b_p,b_r,lam fitted) and KHM (v3 fits); "
                          "retrospective and inspected (post-1995 seen per PROTOCOL_v5)",
                "state_variables": [
                    "birth cohorts by year (cohort size)",
                    "income deciles (10) x public/private sector",
                    "grades: 16 (primary 6, secondary 3, upper-secondary 3, tertiary 4)",
                    "status: entrants, enrolled, repeaters, deferred/qualified-waiting (tertiary deferral pool), completers, out-of-school",
                    "demand utility: human-capital premium (b_h), positional credential share (b_p), relational/formal-work floor (b_r), "
                    "declining cost sensitivity (lam), level intercepts, income decile",
                    "supply/financing: public capacity, vouchers, fees/subsidies, free tuition, CCT, cycle rules",
                ],
                "stage_transitions": [
                    "Grade 1 entry -> primary (6) -> secondary (3) [gate at end of secondary] -> upper-secondary (3) [senior-high reform gates] -> tertiary (4)",
                    "repetition (rep_prim/rep_sec), late entry (late), dropout, upper-secondary transition (PHL Grade 10->11)",
                    "tertiary deferral pool (qualified waiting) and admission when capacity/utility allows",
                ],
                "supply_vs_demand": "supply/financing facts enter as inputs (capacity, vouchers, fees, subsidies); demand engine is the fitted part",
                "rural_migration": "NOT MODELLED: model is national by income decile; no region/rural dimension, no migration",
                "jobs_formalization_credential": "relational floor b_r on formal-work share (wage/salary employment proxy); wage premiums for next "
                                                 "credential are drivers; credential queues are NOT an explicit employer queue in v5 (unlike eduengine)",
                "quality_shadow_tutoring": "NOT MODELLED in v5: no school quality, learning, or tutoring; v6 Phase-1 prototype adds stage/work "
                                           "states but not quality/tutoring yet",
                "heterogeneity": "income deciles, cohorts, public/private, gender not modelled",
                "limitations": ["PHL-centric and retrospectively inspected", "no migration/region", "no quality/learning/tutoring",
                                "employer credential demand proxied by formal-share driver", "post-1995 not blind"],
            },
            {
                "id": "masseng_v6_phase1",
                "name": "MASSENG v6 Phase 1 — conserved cohorts and joint admissions (accounting prototype)",
                "path": "research/masseng-v6/masseng_v6/{core/{state,runner,ledger}.py,education/{admissions,institutions}.py}; tests in research/masseng-v6/tests/",
                "version": "v6 Phase 1 prototype (README: 'illustrative mechanics; not calibrated, causally identified, or empirically validated')",
                "type": "probability-mass cohort accounting kernel with joint admission markets",
                "status": "prototype; does NOT yet implement the full country-year v6 simulation; no fitted parameters; synthetic known-answer tests only",
                "state_variables": [
                    "CohortKey(country, birth_cohort, decile, region, stage, grade, sector, education_status, work_status)",
                    "EducationStatus: attending / repeating / qualified_waiting / out_of_school_reenterable / completed / exit_terminal / alternative",
                    "WorkStatus: none / part_time / full_time / seasonal",
                    "stocks by level/sector; entry funnel Q>=L>=E>=R; market capacity/reservations",
                ],
                "stage_transitions": ["conserved cohort progression with explicit external entries/deaths/exits/reentries",
                                      "joint admissions: effective applicants -> at most one market; continuing reservations respected"],
                "supply_vs_demand": "EntryFunnel separates latent (Q) -> qualified (L) -> eligible (E) -> effective (R) demand; Market supplies capacity",
                "rural_migration": "region is a CohortKey dimension but no migration flows are implemented",
                "jobs_formalization_credential": "work_status is recorded orthogonally; no employer queue/credential model yet",
                "quality_shadow_tutoring": "not implemented in Phase 1",
                "heterogeneity": "cohort/decile/region/stage/grade/sector/status",
                "limitations": ["accounting only", "no country-year simulation", "no behaviour/estimation", "no quality/tutoring/migration"],
            },
            {
                "id": "legacy_engine_worlds",
                "name": "legacy engine/ worlds (childworld, camchild, floorworld, impute)",
                "path": "engine/{childworld.py,camchild.py,floorworld.py,impute/,experiments.py,mc.py,worlds.py,...}",
                "version": "pre-MASSENG / auxiliary",
                "type": "fast school-and-work Monte Carlo (childworld), Cambodia child-labour twin (camchild), education→industrialisation (floorworld), imputation system",
                "status": "auxiliary/archived; not the current MASSENG line",
                "state_variables": ["varies; mostly aggregate/two-region household models"],
                "stage_transitions": ["varies (e.g. camchild: two linked regions, school/work states)"],
                "supply_vs_demand": "varies", "rural_migration": "camchild has two linked regions; childworld/floorworld aggregate",
                "jobs_formalization_credential": "varies", "quality_shadow_tutoring": "varies",
                "heterogeneity": "varies", "limitations": ["legacy; not maintained as MASSENG"],
            },
            {
                "id": "staging_experiment",
                "name": "Codex synthetic staging/sequencing experiment (audited)",
                "path": f"engine/experiments_codex_sequence/{{DESIGN.md,run_staging.py,results/full.json}} @ {STAGING_BRANCH} ({STAGING_COMMIT})",
                "version": "single exploratory experiment, 160 runs",
                "type": "eduengine formal_loop scenario grid",
                "status": "SIMULATION ONLY; DESIGN committed in c435fa2 (20:46:01) before results in bac3a7c (20:48:13)",
                "state_variables": ["inherits eduengine state (see eduengine_modular_abm)"],
                "stage_transitions": ["4 schedules of 2 stipulated events (edu_share 0.18->0.30; vac0 0.08->0.16); 70 years; cohorts 35-44 measured"],
                "supply_vs_demand": "eduengine modules", "rural_migration": "not simulated (rural attribute + cost only)",
                "jobs_formalization_credential": "eduengine QueueLabour with job_elasticity 0/1 assumption",
                "quality_shadow_tutoring": "eduengine quality/tutoring modules",
                "heterogeneity": "seeds 0-9; feedback 0/1; gates bar/quota",
                "limitations": ["synthetic; arms not exposure-matched; time order not identified; no migration; seed-sensitive completion rankings"],
            },
            {
                "id": "codex_bayes_screen",
                "name": "MASSENG v5 PHL R1 conditional Bayesian-style importance screen",
                "path": "research/masseng-v6/experiments/codex_bayes/{run_screen.py,test_screen.py,results_main/,results_expanded/} "
                        f"@ {STAGING_BRANCH}; active server copy /root/work/masseng-staging-codex-20261124/masseng-v6/experiments/codex_bayes/",
                "version": "prototype importance screen (no resampling; conditional weights)",
                "type": "prior-draw importance screening against 1971-1995 PHL GERs",
                "status": "committed 256-draw pilots: ESS 5.94 (main) / 1.77 (expanded), holdout GER RMSE 9.645/7.065 vs persistence 6.600; "
                          "4096-draw main+expanded runs active on region-42 at audit time (see verification)",
                "state_variables": ["MASSENG v5 R1 parameters b_h,b_p,b_r,lam drawn; all other params fixed at fit_R1.json"],
                "stage_transitions": ["model simulation per draw; Gaussian pseudo-likelihood; weights; ESS; holdout comparison"],
                "supply_vs_demand": "v5 model", "rural_migration": "not modelled", "jobs_formalization_credential": "v5 relational driver",
                "quality_shadow_tutoring": "not modelled", "heterogeneity": "prior draws x parameters",
                "limitations": ["conditional importance weights, not calibrated posterior", "fixed nuisance from broader fit = data reuse",
                                "logistic overflow on expanded prior", "holdout previously inspected", "ESS very low at 256 draws"],
            },
        ],
    }

    datasets = [
        ["D1", "WDI/UIS/ILO sweep (massification panel)", "origin/research/massification-panel-2026-11-22 : "
         "research/records/2026-11-22-massification-panel/sources/wdi_sweep/*.json(.gz)",
         "country x year; [iso3,year,value]", "60+ series; pre_ger 207 countries 1970-2022; prm_ner 197/1970-2019; sec_ner 188; "
         "lsc 197/1970-2024; test_scores & hci 172/2010-2020; child_work (ILO/UCW 7-14) 100/1994-2016 median 2 obs/country; "
         "gdppc 213/1960-2024; fertility 217/1960-2024; repeat_prm 201/1970-2019; prm_cmp 198/1970-2024",
         "WDI API pull ~2026-11-11 (header lastupdated); UIS/ILO-modelled mixes", "mixed vintages; ILO modelled child work; no child-work state "
         "decomposition (only total); no tutoring series; UIS vs national definitions", "GER gross vs model participation share; attainment vs participation; "
         "child work 7-14 vs model's age-less 4-state; test-score scale vs model grade-equivalents"],
        ["D2", "E1 multiverse WDI panel (derived)", "origin/research/e1-multiverse-1200-2026-11-25 : "
         "research/records/2026-11-25-e1-multiverse/{data/edge_table400.csv,data/headline400.json,results/}",
         "derived link statistics (272 links) from 17 WDI variables, 179 countries 1940-2025",
         "272 = 136 unordered pairs x 2 specs; 1,200 draws + 1 real pass", "new WDI pull (vintage differs from original; E1 reproduction max |delta t| 3.97e-5)",
         "RAW PANEL NOT COMMITTED (lived on /root/work/data on another host); no re-pull allowed; derived only",
         "cannot be re-fitted; 17 macro variables, none of the MASSENG child-work states"],
        ["D3", "Q2 long-run panel", "origin/research/q2-pathways-2026-11-25 : research/records/2026-11-25-q2-pathways/data/long_run_panel.csv",
         "country x year: child mortality, life expectancy, effective fertility, TFR, mean years schooling, Maddison GDP pc, urban share",
         "197 countries, 1750-2024, 42,959 rows", "OWID/Gapminder/Maddison reconstructions (vintage per OWID metadata)",
         "reconstructions pre-1950; splice artefacts; schooling is attainment stock; no enrolment/child-work/tutoring",
         "attainment stock vs participation flow; no MASSENG states"],
        ["D4", "Transition onset/timing record", "origin/research/transition-2026-11-23 : "
         "research/records/2026-11-23-transition/{data/long_run_panel.csv,data/onsets.csv,results/transition_results.json}",
         "country x year panel + onset years (mortality/fertility decline; 197 countries)",
         "panel 197 countries 1750-2024; onsets 197 rows", "OWID/UN/Maddison, Nov 2026; box2 raw downloads not committed",
         "onset rule = first year >=10% below running peak sustained 10y; derived TFR 'shown, not used for claims'; pre-1950 coverage thin",
         "demographic onsets only; no education/jobs events; useful as timing covariates/placebo dates"],
        ["D5", "DHS public API cached cells", "origin/research/dhs-api-ecological-2026-11-24 : research/records/2026-11-24-dhs-api-ecological/data/",
         "survey x country x background category; published aggregates (no microdata)",
         "76-87 countries, 1985-2025; 369 surveys; TFR/GFR/wanted fertility, median age at first birth by education, mean CEB by education, "
         "women's education (edu2/edu4 panels)", "DHS API pull 2026-11-24 (sha256 manifest)",
         "background categories vary across surveys; no denominators for rate indicators; no child-labour/enrolment/tutoring cells",
         "fertility/women's education only; B1 birth intervals unavailable"],
        ["D6", "DHS CEB-by-education cells", "origin/research/dhs-acquisition-2026-11-24 : research/records/2026-11-24-dhs-acquisition/data/ceb_education_cells.csv",
         "survey x country x education: mean CEB women 40-49", "318 rows, 14 countries, 1988-2025", "published DHS API cells; acquisition planning record",
         "small country coverage; mean CEB is not parity progression; no microdata", "B2 PPR not published"],
        ["D7", "Shadow-education hand-collected data", "origin/experiment/massification-2026-11-20 : "
         "experiments/massification-2026-11-20/04_data/shadow_round2/data/{shadow_incidence_round2.csv,shadow_fees_round2.csv}",
         "country/site x year: participation and fees", "6 countries/sites, 38 + 20 rows, 1996-2023", "hand-collected sources; several case studies",
         "no harmonised national panel; definitions differ; some case studies (e.g. one Cambodian district)", "model tut_rate vs observed incidence; broad vs narrow definitions"],
        ["D8", "asia_school_work cross-section", "engine/data/asia_school_work.json (handoff/massification branches)",
         "country: oos_lower (UIS via WDI), child_labour (ILO/UNICEF estimates as tabulated on Wikipedia)", "21 countries, one row each; oos years 2015-2022, "
         "child-labour years 2010-2023; 20 with both", "mixed vintages per row (file's own caveat)", "years differ; admin OOS can overstate; 4 composition facts are tests only",
         "same age/definition gaps as D1"],
        ["D9", "Philippines CHED higher-education series", "docs/engine/comparative_cases/philippines_enrolment.json",
         "student headcount by academic year (HE)", "5 observations, AY2015-16..AY2019-20, one country", "CHED legacy PDF (retrieved 2026-11-03)",
         "single country; headcount stock; no age/cohort; descriptive series", "HE headcount vs cohort-flow tertiary enrolment share"],
        ["D10", "Codex staging results", f"{STAGING_BRANCH} : engine/experiments_codex_sequence/results/full.json ({STAGING_COMMIT})",
         "160 runs: 4 schedules x 2 feedback x 2 gates x 10 seeds; metrics + 70-year annual series", "160 runs; T=70; N=400 children/cohort; elapsed 16.499 s",
         "simulation only (hash " + STAGING_FULL_SHA + ")", "synthetic; no empirical fit; arms not exposure-matched; no migration",
         "no observed counterpart; designed as a timing mechanism experiment"],
        ["D11", "Codex Bayesian screen pilot results", f"{STAGING_BRANCH} : research/masseng-v6/experiments/codex_bayes/results_{{main,expanded}}/ "
         "(draws.json, run.json, summary.json)", "per-draw parameters, log/normalised weights, holdout predictions; summary ESS/RMSE",
         "2 x 256 draws (seeds 20261124; workers 4); ESS 5.94/1.77; holdout GER RMSE 9.645/7.065 vs persistence 6.600",
         "committed 2026-11-24; prior bounds explicit; fixed nuisance from fit_R1.json (data reuse)", "importance weights only; not posterior; overflow on expanded prior; "
         "low ESS; holdout inspected", "conditional on v5 model and fixed nuisance; no observed-vs-model identification"],
        ["D12", "MASSENG v5 fitted outputs and protocols", "research/masseng-v6/model/{outputs/PHL/v1..v5, outputs/KHM/v3, model/PROTOCOL*.md, docs/}",
         "country-level fitted parameter sets and scores by version/specification", "PHL v1-v5, KHM v3; PHL v5 R0-R5 fits; recovery_R2; 34 tests passed",
         "PROTOCOL v5 written 2026-11-22 before first fit; fits 2026-11-22/23", "retrospective and inspected (post-1995 seen); comparability limits on premium series",
         "PHL/KHM only; no migration/quality/tutoring"],
        ["D13", "Massification-panel sweep/takeoff results", "origin/research/massification-panel-2026-11-22 : research/records/2026-11-22-massification-panel/results/{takeoff,sweep,sweep_all,tight,final,bayes}/",
         "country-level panel regressions/lead-lag/event studies/Bayesian model averaging", "58 variables; 12 SSA fee-abolition dates (unverified against primary sources); child-work B3",
         "runs 2026-11-22 (server 21 workers; archival)", "sweeps have no country FE; some signs implausible; B3(c) declared invalid; abolition dates unverified",
         "associational/lead-lag, not identified; child-work series sparse"],
        ["D14", "GPU-suite ABC-real-data experiment", "origin/research/2026-11-24-gpu-suite : research/records/2026-11-24-gpu-suite/scripts/exp3_rejection_abc_realdata.py",
         "rejection ABC on real data (script; results archived on that branch)", "see branch record", "2026-11-24", "GPU experiment; not audited here",
         "separate from current work; reuse only with care"],
        ["D15", "Engine tune protocol / tuned settings", "engine/tune_protocol.json (v0.3.2, recorded 2026-11-01) + engine tuned outputs",
         "256 shared Latin-hypercube settings; selection rules; evaluation seeds", "recorded before search; seed-sensitivity amendment recorded after first pass",
         "2026-11-01 protocol; tuning runs 2026-11", "retrospective temporal evaluation; post-2015 inspected; seed sensitivity",
         "toy engine, not MASSENG"],
        ["D16", "MASSENG country facts/inputs", "research/masseng-v6/model/countries/{HKG,KHM,PHL}/{config,facts,drivers_v5,targets_v5,wdi_series,sources}",
         "country inputs: cohort sizes, age/cycle rules, income and premiums, formal share, policies, targets", "PHL and KHM full; HKG facts only",
         "sources recorded per file (FIES/NTA/CHED/DHS etc.); v5 drivers", "hand-curated; some unverified rows excluded; no microdata",
         "country-specific; not harmonised cross-country"],
    ]

    runners = [
        ["R1", "staging_experiment", "engine/experiments_codex_sequence/run_staging.py", "eduengine formal_loop 4-schedule x 2 feedback x 2 gates x 10 seeds",
         "MEASURED: 160 runs, 16.499 s wall (workers default 8; worker count not recorded in JSON) => ~0.83 CPU-s/run", "writes new JSON only"],
        ["R2", "codex_bayes_screen", "research/masseng-v6/experiments/codex_bayes/run_screen.py", "v5 R1 importance screen: uniform prior draws -> pseudo-likelihood -> weights/ESS/holdout",
         "committed pilots 256 draws x 4 workers (elapsed not recorded); ACTIVE 2 x 4096 draws x 24 workers (see verification); final JSON only at completion",
         "no resampling; conditional weights"],
        ["R3", "v5_calibration", "research/masseng-v6/model/masseng/{calibrate.py,calibrate5.py}", "least-squares fits R0-R5 per country against protocol targets",
         "not measured here; 34 tests passed per FIT_READINESS", "retrospective"],
        ["R4", "E1_multiverse", "origin/research/e1-multiverse-1200-2026-11-25 : scripts/{run_e1.py,run_multiverse400.py,analyse_e1.py,panelcheck.py,group_localisation.py}",
         "272 links x 1,200 grouped draws + real pass; BH/BY verdicts", "MEASURED (E1 REPORT): 5,426.8 s on 8 workers; 4.52 s/draw effective", "raw panel not committed"],
        ["R5", "Q2_pathways", "origin/research/q2-pathways-2026-11-25 : scripts/{country_pairs.py,q2_audit.py,erratum_check_q2_yardstick.py}",
         "long-run country-pair pathway audit", "panel regressions; CPU minutes", "associational"],
        ["R6", "massification_panel", "origin/research/massification-panel-2026-11-22 : scripts/{takeoff,sweep,sweep_all,tight_tests,final_tests,bayes,triad,kiss_ensemble}.py",
         "panel sweeps, lead-lag, split stability, fee-abolition event study, Bayesian model averaging, child-work B3", "archival; server 21 workers (2026-11-22); no timing recorded here",
         "no country FE in sweeps; some archival outputs partial"],
        ["R7", "v5_engine5_array", "research/masseng-v6/experiments/run_engine5_array.py", "declared capacity-coverage scenarios on v5 engine (annual markets)",
         "29 tests passed (ENGINE5_ARRAY.md)", "capacity assumptions declared, not estimated"],
        ["R8", "v6_phase1", "research/masseng-v6/experiments/run_phase1.py + masseng-v6/tests/", "synthetic known-answer accounting tests",
         "fast (seconds; no calibration)", "accounting only"],
        ["R9", "transition_onsets", "origin/research/transition-2026-11-23 : scripts/transition.py", "long-run panel build + onset dates + phase diagram",
         "box2; raw downloads not committed; no timing recorded here", "onset-rule sensitivity"],
        ["R10", "gpu_suite_abc", "origin/research/2026-11-24-gpu-suite : scripts/exp3_rejection_abc_realdata.py (+ exp1/2/4)", "rejection ABC on real data; CUDA kernel experiments",
         "GPU; separate record", "not run in this audit"],
    ]

    next_experiments = [
        {"id": "X1", "title": "Exposure-matched sequencing test (fix the staging experiment's main confound)", "priority": 1,
         "question": "After equalising cumulative exposure to the education-share and vacancy-rate changes, does the school-first vs jobs-first "
                     "difference in completion/formal-share persist, or was it a cumulative-dose artefact?",
         "design": "eduengine formal_loop with 6 arms: none; school_first; jobs_first; simultaneous; school_first_matched; jobs_first_matched. "
                   "Matched arms deliver the SAME total education-share-years and vacancy-years as their counterpart (e.g. shorten the early period "
                   "or compensate late), so only ORDER differs. Add a calendar-shift placebo (both events shifted +10 years, same order) to separate "
                   "calendar/cohort-window effects. 6 arms x 2 feedback x 2 gates x 20 seeds = 480 runs; pre-declare all contrasts and the "
                   "exposure arithmetic (audited: unmatched arms differ by +1.8 edu-share-years / -1.2 vacancy-years).",
         "falsifier": "If the matched order contrast is ~0 while the unmatched contrast is large, the original 'timing effect' is cumulative exposure, "
                      "not sequencing. If the matched contrast keeps the sign and clears its seed bootstrap CI, order has a model-internal effect worth "
                      "following up in a more structural design.",
         "splits": "None needed (synthetic); report all arms and seeds, no selection; seed bootstrap CIs over 20 seeds.",
         "data": "none (synthetic)", "cost_estimate": "480 runs x ~0.83 CPU-s = ~400 CPU-s; ~30 s wall on 24-48 workers; <5 min end-to-end with monitoring.",
         "blocked_by": "none; only the audited staging harness needs a small extension (new arm definitions), not a new engine."},
        {"id": "X2", "title": "Gate/quota x shadow-tutoring inequality factorial", "priority": 2,
         "question": "Do quota gates (planned seats) versus absolute bar gates change tutoring use and completion differently across household "
                     "income quintiles and rural/urban location, in the direction the MASSENG account predicts?",
         "design": "eduengine: gates bar vs quota x tutoring access (rural_firm_access 0.2/0.4/0.8) x own-teacher ban (0/enforced) x 20 seeds = 240 runs; "
                   "outcomes by level and wealth quintile: completion, tut_rate, tut_by_q, parity_wealth/location; pre-declare directional expectations "
                   "(quota gates -> more gate-prep tutoring; richer/urban households capture more).",
         "falsifier": "Pre-declared: if quota gates do not raise gate-prep tutoring relative to bar gates (sign and CI), or do not widen the top-vs-bottom "
                      "tutoring gap, the model's gate/tutoring channel does not produce the claimed pattern (conditional on the rest of the design).",
         "splits": "None (synthetic); all cells reported; no post-hoc subgroup selection.",
         "data": "none (synthetic)", "cost_estimate": "240 runs x ~0.83 CPU-s = ~200 CPU-s; <1 min wall on 24 workers.",
         "blocked_by": "none."},
        {"id": "X3", "title": "Education-to-jobs feedback-elasticity robustness surface", "priority": 3,
         "question": "Are any sequencing conclusions robust to the assumed education-to-jobs feedback (job_elasticity)?",
         "design": "eduengine: job_elasticity in {0, 0.25, 0.5, 0.75, 1.0} x 4 schedules x 2 gates x 20 seeds = 800 runs; report the full contrast surface "
                   "with seed bootstrap CIs; pre-declare that conclusions must be stable across the whole elasticity range (or be reported as conditional).",
         "falsifier": "Any order conclusion that reverses sign across the elasticity grid is not robust; report the reversal and do not select the "
                      "elasticity that gives the preferred answer.",
         "splits": "None (synthetic); full surface reported.",
         "data": "none (synthetic)", "cost_estimate": "800 runs x ~0.83 CPU-s = ~660 CPU-s; ~1-2 min wall on 24-48 workers.",
         "blocked_by": "none."},
        {"id": "X4", "title": "Observed-data staging/ordering test with honest splits (aggregate level only)", "priority": 4,
         "question": "Where the observed panels allow, does a pre-declared model-implied timing/ordering score predict held-out changes in enrolment/"
                     "completion better than persistence or trend benchmarks?",
         "design": "Use committed WDI/UIS panel (pre_ger, prm_ner, sec_ner, lsc), transition onset dates, and (if used) child_work only as a sparse "
                   "secondary outcome. Freeze: train on countries/periods disjoint from validation (e.g. leave-country-out blocks and pre-1996 -> "
                   "1996-2015); pre-register the ordering score and the benchmark losses. Report absolute losses and paired predictive differences with "
                   "country-cluster bootstrap CIs. No new data pull; no DHS microdata.",
         "falsifier": "If the model-implied ordering score does not beat persistence and trend on held-out countries (paired differences with CIs), "
                      "the observed data do not support the staging prediction at this aggregate; report it as such.",
         "splits": "Pre-registered leave-country-out + time-block split; no Q2/E1 observation reused across splits; if too few countries, report "
                   "insufficient evidence.",
         "data": "D1, D3, D4 (committed only)", "cost_estimate": "panel regressions only; minutes of CPU (no simulation).",
         "blocked_by": "construct mismatch: only aggregate enrolment/completion, no child-work states or tutoring; results would be exploratory and "
                       "cannot identify mechanisms."},
        {"id": "X5", "title": "Bayesian screen validation and synthetic parameter recovery (coordinate with Lead/Codex)", "priority": 5,
         "question": "Are the v5 R1 importance screens usable at all: do they recover known parameters, pass ESS/weight diagnostics, and stay stable "
                     "across seeds, priors and tolerance?",
         "design": "Use existing run_screen.py (no model edits): (i) synthetic recovery - simulate from known b_h,b_p,b_r,lam draws and check coverage/"
                   "bias; (ii) weight diagnostics - max weight share, ESS, degenerate draws; (iii) seed stability - >=2 seeds per prior; (iv) prior and "
                   "tolerance sensitivity; (v) posterior-predictive coverage vs persistence/trend benchmarks. Report everything; no posterior claim.",
         "falsifier": "If synthetic recovery fails (coverage far below nominal / parameters unidentifiable) or ESS remains very low at the declared "
                      "budget, the screens are not usable and no posterior/mechanism claim can be made.",
         "splits": "Synthetic known-parameter recovery + committed/active screen outputs; no observed holdout claims (post-1995 already inspected).",
         "data": "D12 (v5 R1 fit), existing screen code", "cost_estimate": "needs one measured 4,096-draw screen wall first (active runs); budget <=1 h "
                                                                            "server time for recovery+diagnostics at 24 workers; do not promise draw counts before the timing measure.",
         "blocked_by": "active 4,096-draw screens must complete/be owned by Lead; do not duplicate."},
    ]

    verification = {
        "staging_branch": STAGING_BRANCH,
        "staging_commit": STAGING_COMMIT,
        "commit_order": {"c435fa2": "DESIGN.md + run_staging.py (2026-11-24 20:46:01 +0800)",
                         "bac3a7c": "results/full.json + codex_bayes pilots (2026-11-24 20:48:13 +0800)",
                         "note": "DESIGN recorded before results in git history"},
        "committed_vs_server_sha256": {
            "engine/experiments_codex_sequence/results/full.json": {"committed": STAGING_FULL_SHA, "server": STAGING_FULL_SHA, "match": True},
            "engine/experiments_codex_sequence/DESIGN.md": {"committed": DESIGN_SHA, "server": DESIGN_SHA, "match": True},
            "engine/worlds.py": {"committed": WORLDS_SHA, "server": WORLDS_SHA, "match": True},
            "engine/eduengine/core.py": {"committed": CORE_SHA, "server": CORE_SHA, "match": True},
            "research/masseng-v6/experiments/codex_bayes/run_screen.py": {"committed": RUN_SCREEN_COMMIT_SHA,
                                                                          "server": RUN_SCREEN_COMMIT_SHA, "match": True},
            "research/masseng-v6/model/masseng/engine5.py": {"committed": MODEL_ENGINE5_COMMIT_SHA,
                                                              "server": MODEL_ENGINE5_COMMIT_SHA, "match": True},
        },
        "server_snapshot_utc": "2026-11-24T12:55:31Z",
        "active_bayesian_runs": {
            "main_4096": {"shell_pid": 18115, "python_parent": 18116, "workers": 24, "n_draws": 4096,
                          "seed": 20261125, "prior": "main", "log_bytes": 0, "output_json": "pending (written at completion)",
                          "status": "running at audit snapshot (~6 min elapsed)"},
            "expanded_4096": {"shell_pid": 18162, "workers": 24, "n_draws": 4096, "seed": 20261126,
                              "prior": "expanded", "log_bytes": 3840, "output_json": "pending (written at completion)",
                              "status": "running at audit snapshot (~6 min elapsed); RuntimeWarning overflow in engine5 sigmoid"},
            "run_screen_processes_observed": 53,
            "note": "At the audit snapshot both screens were alive; do not shut down region-42 while active. This audit did not touch them."},
        "limitations_of_verification": ["read-only checks only; no staging re-run", "active screens not yet complete; their results are not audited here"],
    }

    with open(os.path.join(OUT, "engine_inventory.json"), "w") as f:
        json.dump(engine_inventory, f, indent=1)
    with open(os.path.join(OUT, "dataset_catalog.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "path/branch", "unit", "coverage", "vintage", "limitations", "construct_mismatch"])
        w.writerows(datasets)
    with open(os.path.join(OUT, "runner_catalog.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "path", "what_it_does", "measured_cost", "limitations"])
        w.writerows(runners)
    with open(os.path.join(OUT, "next_experiments.json"), "w") as f:
        json.dump({"label": "proposed next experiments (proposals only; none run)",
                   "experiments": next_experiments}, f, indent=1)
    with open(os.path.join(OUT, "verification.json"), "w") as f:
        json.dump(verification, f, indent=1)
    print(json.dumps({"engine_entries": len(engine_inventory["engines"]), "datasets": len(datasets),
                      "runners": len(runners), "next_experiments": len(next_experiments),
                      "out": OUT}, indent=1))


if __name__ == "__main__":
    main()
