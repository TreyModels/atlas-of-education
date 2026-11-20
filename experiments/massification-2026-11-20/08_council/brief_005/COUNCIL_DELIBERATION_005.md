> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# COUNCIL DELIBERATION 005 — iteration-2 partial results

**Panel (AI composites, literature-based):** BRAY (shadow education, mandatory), PAGE (model reasoning), PATRINOS
(education economics; steel-man), CARTWRIGHT (philosophy of social science).
**Input:** `brief_005/BRIEF.md`; artifacts on disk: `02_lit/COUNTRY_CARDS/` (6 cards), `02_lit/SHADOW_TARGETS.csv`
(21 rows, 11 YES), `04_data/TARGETS_SHADOW.csv`, `TARGETS_FLOW.csv`, `05b_experiments/loop2/`
(EXPERIMENTS_L2, SUMMARY_L2, PRE_DECLARATIONS_L2 incl. amendments L2-1…L2-5, ERROR_LOG_L2, code/twoway.py,
runs/L2 and L2_uncalibrated). Runner-1 loop2 (configs, CALIBRATION_TABLE, cohort ledger) absent.

## Agreed

1. **Restatement test: failed at the one fitted cell.** Of 11 `use_as_model_target=YES` shadow rows, exactly one —
   HK senior-secondary 0.85 — is wired into the model, as the calibration target (`twoway.py` config +
   Amendment L2-3 bisection). The match is by construction: restated, not generated. The other ten YES rows are in no
   model target dictionary and are not reported as checks. Stage-matched, the generated PH college-gate take-up 0.899
   stands against a literature upper-secondary review-centre rate of 28.1%, and KHM 0.887 against Grade-9 68.4% and
   primary 41.3% (urban 60.5 / rural 26.4). The register says 11 YES, not the 6 in the signal.
2. **Two-way feedback: asymmetric, not two-way.** Freezing schooling leaves the job path rising (complex vacancies
   PH 71.0→130.9, HK 172.8→235.8, KHM 32.3→80.0); endogenous schooling adds only +4.5/+6.5/+3.1 jobs (≈3–4%).
   Freezing the economy leaves attainment rising +0.028/+0.022/+0.024 (vs +0.067/+0.118/+0.077 live) — a residual
   shadow-supply channel of ≈20–40%, which the error log correctly calls an upper bound (first-order counterfactual).
3. **Provider entry: right direction, non-credible magnitude.** Endogenous entry raises senior-secondary take-up by
   54–67 pp vs fixed supply (PH 0.884/0.219; HK 0.865/0.327; KHM 0.887/0.258), but prices fall to the declared floor
   and provider counts grow 5–90×. Teacher-tutors dominate (76/86/97%) by declared fixed cost/capacity, not by
   provider data.
4. **Direction: one country.** HK demand-led (Ec_dir +0.098, 2sd 0.014); PH/KHM "neither" with effects ≈0 (−0.0008 /
   +0.0008). That is a demonstration, not a pattern.
5. **Positional channel: null in this module.** Null ≠ disconfirmation; state it as "untested by this module".
6. **Cohort flows: UNABLE TO ASSESS** (ledger pending). Internal misses are disclosed and should stay: PH completion
   −0.089; KHM +0.099; KHM formal share +0.140; KHM university proxy +0.175.

## Disagreements preserved

**D1. BRAY vs PAGE — is teacher-tutor dominance a result?**
BRAY: it is the comparative fact the literature leads one to expect (teacher-sold in Cambodia; mixed commercial/teacher
in PH/HK), and the model generates it without fixed shares — worth reporting as a consistency. PAGE: it is produced by
declared fixed-cost/capacity values; without provider data it is a structural possibility, not a finding.
*Resolution:* report as "generated structural possibility, qualitatively consistent with the comparative record; not
validated", and never as a shadow-sector finding.

**D2. PATRINOS vs PAGE — may "HK is demand-led" be said?**
PATRINOS: no, until the holdout and recovery run; it is a within-model classifier outcome that will be checked
against the L2-4/L2-5 tests. PAGE: it is legitimate as a hedged model statement ("in this module, the HK
parameterisation classifies as demand-led"). *Resolution:* hedged sentence only, with the pending tests named.

**D3. CARTWRIGHT vs BRAY — report the shadow miss or "no verified target"?**
BRAY: the PH/KHM over-universalisation is informative — one intercept cannot make the shadow match HK while keeping
PH/KHM at survey levels. CARTWRIGHT: a miss must be disclosed even where the target is soft; but do not present a
miss against an unresolved target as a contradiction. *Resolution:* two-column table — "stage-matched check vs best
available literature number, confidence" and "verified-target miss" — so softness and contradiction are separate.

**D4. All — the fitted HK 0.85 is the loop's stop rule 5 live case.** It must be labelled a calibration and excluded
from any incidence claim; the module may not be described as "matching" the shadow literature.

## Model contest (same module, different readings)

| Reading | What generates the education rise | What generates the job rise | Status |
|---|---|---|---|
| Two-way (module's intended claim) | returns + shadow supply | human-capital feedback | rejected: job side 3–4% |
| Asymmetric (Council) | returns/genuine + shadow channel 20–40% (upper bound) | demand schedule | accepted as description |
| Shadow-sector story | one fitted intercept sets take-up | schedule | not identified; restatement at HK |
| Shadow-provider story | entry costs/capacity | schedule | direction credible; magnitude uncalibrated |

**Intake discrepancies verified:** YES count 11 (signal says 6); entry effect 54–67 pp (signal says 46–66); both
corrected in BRIEF.md §3 and carried to the Lead.
