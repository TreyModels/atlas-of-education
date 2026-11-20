# Y5 — Portability design data-completeness audit (CHN, HKG)

**Design-only. No model run. No portability claim. C1–C4 untouched (D75/R22).**
Audit date 2026-11-20 (UTC 2026-11-20T13:21Z). Predeclaration read-only at sha256
`8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1` (verified by the script).

## Verdict: **DATA-COMPLETE** — 0 NEW-ASK

Threshold (verbatim): *"data-complete" only if every D75 input is present-on-disk or already-ruled-held
(no NEW data ask); falsifier = any NEW-ASK -> design marked BLOCKED-ON-DATA for that input.*

All six D75 inputs are supplied on disk for **both** CHN and HKG (6/6 inputs; 12/12 input-country rows).
No input falls to a held-only row and none is a new ask. `n` = 6 inputs audited; clusters = 2 countries.

## Per-input status (one row per input × country in `results/transfer_checklist.csv`)

| # | D75 input | CHN | HKG | On-disk evidence (file; indicator/row; years; n) |
|---|---|---|---|---|
| I1 | initial cohorts | present-on-disk | present-on-disk | `UNIVERSALIZATION_SERIES.csv` `cohort_population_0_14` 1995–2024 n=30 each (derived SP.POP.TOTL × SP.POP.0014.TO.ZS); `population_total` n=30 each. Latest 2024: CHN 225,546,074 / HKG 790,619 |
| I2 | observed economy series | present-on-disk | present-on-disk | `JOBS_AND_MARKETS_PANEL.csv` `SL.AGR.EMPL.ZS`, `SL.EMP.WORK.ZS`, `SL.SRV.EMPL.ZS`, `SL.UEM.1524.ZS`, `NY.GDP.PCAP.PP.CD` n=30 1995–2024 each; `SE.XPD.TOTL.GD.ZS` CHN n=5 (1995–2023), HKG n=25 (1996–2024); all `status=observed` |
| I3 | policy dates/pushes | present-on-disk | present-on-disk | `POLICY_TIMELINE.csv`: CHN 1 dated push (1986 Compulsory Education Law, 9-year 6+3); HKG 4 (1971 free primary, 1978 9-year free/compulsory, 2008 12-year free, 2012 3-3-4). All `status=policy_fact` |
| I4 | capacity trajectory | present-on-disk | present-on-disk | `STATE_CAPACITY.csv`: PTR primary/secondary CHN n=18/20 (1995–2018), HKG n=22/19 (1996–2018); teachers primary/secondary CHN n=25/26, HKG n=28/27 (→2024); education spending (%GDP, UIS) CHN n=27 (1971–2024), HKG n=42 (1971–2025); per-student PPP$ CHN n=3, HKG n=25/24 |
| I5 | level-gate mapping | present-on-disk | present-on-disk | `UNIVERSALIZATION_TIMING.csv`: CHN 20 gate rows (5 levels × thresholds 15/50/90/95; measures GER/NER/GER_reconstructed; 6 left-censored, 1 right-censored ">2019"); HKG 25 rows (22 numeric dated, 10 left-censored, 3 `unable` completion gates) |
| I6 | measurement definitions | present-on-disk | present-on-disk | In-file `unit`/`definition`/`source_detail` populated on every CHN/HKG series row (SERIES 351/438, JOBS 892/988, STATE_CAPACITY 261/262 & 382/386, TIMING derivation_method 20/20 & 25/25) + `DATA_NOTES_MASSIFICATION.md` "Definition traps" register |

## NEW-ASK: none

- Nothing was fetched, drafted or sent. No external request of any kind was made.
- The existing HELD queue is **reaffirmed, not extended**: PSA microdata, WB Enterprise Surveys, annual
  capacity/enforcement, real per-pupil spending, subnational sector employment, the named expansion file
  (D76/D92). Y5 creates no new request label.
- `SCHOOL_EXPANSION.csv` was checked: 27 rows, `iso3=PHL` only — it covers neither CHN nor HKG. The named
  expansion file therefore remains an already-held enhancement; it is **not** required for the declared
  partial capacity path (PTR/teacher counts/fiscal shares, D53/R26) that is present for both countries.

## Disclosed caveats (no threshold moved)

1. **Capacity trajectory = the declared partial path**, not observed annual classrooms/enforcement. CHN
   per-student spending has only 3 observations (1998, 2023, 2024); HKG has 25/24. Both flagged, not imputed.
2. **HKG has no UIS completion series.** Three HKG completion-based gate rows are `status=unable` in the
   timing file — declared unavailable, not a data ask. D75 fixes HKG as timing-only/levels check-only via
   NER≥90 (1974) and NER≥95 (1979), which are present and threshold-specific.
3. **CHN censoring is on disk**: left-censored primary gates and the right-censored upper-secondary GER≥90
   row (>2019); D75's −27 y miss from the 1986 law must be reported as is.
4. **Policy rows are `policy_fact` at declared confidence "fact (not re-verified this pass)"** (HKG-2012 from
   the workspace ledger) — confidence is recorded, not upgraded.
5. `SL.*` rows are ILO modelled estimates in WDI, not national LFS tabulations; measures are never spliced
   (gross ≠ net, completion ≠ enrolment, UIS ≠ WDI vintage).

## What this does and does not mean

`DATA-COMPLETE` means the D75 transfer design is **not blocked on data**. It does **not** authorize or
perform a run and it makes **no portability claim** (D75/R22). Any later CHN/HKG run still requires a new
Council decision and a fresh predeclaration under the six D75 constraints; the standing scaling FAIL and the
DIAGNOSTIC-TRANSFER vocabulary (never PASS) remain binding. Phase stays CLOSED (D76); C1–C4 are not reopened.

## Provenance / reproducibility

- `code/run.py` sha256 `2312ad61ea7161b8c5ebf9328e545c9f7300605cfaca10b29efae5bd3e7eb4b1`.
- Run twice in the same environment: exit 0 both times; `results/*.csv` **byte-identical**:
  - `CLUSTER_RESULTS.csv` sha256 `a63bc188a82b79021b7eeaee0d013bb352560952c4452e3cb3b453ca419ce458`
  - `transfer_checklist.csv` sha256 `2a512622a68c11649a66dd5f255462787cee94068fef8e80906eeed0892760eb`
- Python 3.11.17, pandas 3.1.1, numpy 2.4.6; no RNG (seed: none), no network, no clock in result cells.
- Input file hashes are in `RUN_MANIFEST.json` and match `data/SHA256SUMS.txt`.
