# Massification, the economy, and shadow education — research execution package

**Prepared for:** Dr. Trey Menefee · **Date:** 20 November 2026 · **Time zone:** Asia/Shanghai
**Programme:** the DeepSeek handoff package for *Massification and Its Mechanisms* (Menefee & Nordtveit,
October 2026 working paper; June single-author draft).

This package is the fleet's execution of that handoff: an honest audit of the code Trey already built,
a literature/model extraction, a sourced country-data ledger, a pre-declared experiment suite, and a
synthetic expert-council review of the results. It is a **research execution record**, not a validation
of any theory, not a country study, and not causal evidence.

---

## 1. Read this first

| order | file | what it answers |
|---|---|---|
| 1 | [`SUMMARY_FOR_TREY.md`](SUMMARY_FOR_TREY.md) | plain-language: what ran, what was learned, strongest negative result, what to do next |
| 2 | [`PROVENANCE.md`](PROVENANCE.md) | where every artifact came from; source hashes; site-safety check for the GitHub push |
| 3 | [`EXPERIMENTS.md`](EXPERIMENTS.md) | all 12 completed experiment records + 1 pilot, one per template |
| 4 | [`LITERATURE_LEDGER.md`](LITERATURE_LEDGER.md) / [`MODEL_CARDS.md`](02_lit/MODEL_CARDS.md) | what the 20 sources actually model; exact equations; what is verified vs abstract-only |
| 5 | [`DATA_LEDGER.md`](DATA_LEDGER.md) / [`CLAIM_VERIFICATION.md`](04_data/CLAIM_VERIFICATION.md) | real country numbers; manuscript numbers verified / corrected |
| 6 | [`MODEL_INVENTORY.md`](MODEL_INVENTORY.md) / [`REPRODUCTION_MATRIX.md`](03_audit/REPRODUCTION_MATRIX.md) | every engine Trey built, what runs, and which manuscript numbers reproduce |
| 7 | [`08_council/`](08_council/) | synthetic expert-council deliberations on the results |
| 8 | [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) | what remains, with feasible data and decision thresholds |

## 2. What actually executed

**Thirteen completed experiment cells** (plus a Phase-0 validation gate), one pilot, a parallel
adversarial batch, and two Council-commissioned follow-ups:

| batch | cells | status |
|---|---|---|
| A — main suite (`experiment-runner`) | E0 Phase-0 gate, E2 cohort accounting, E3 liquidity, E5 memory, E7 gate density, E8 floor/race at 4 reps, E10 learning-vs-test, E13 graduate supply, **E13b matched-elasticity rival**, E14 actor knockouts, E15 state motives, E18 China school-support, **E18b fair substitution test** | 13 completed |
| A — country/transfer | E19 + E20 (Philippine trajectory, Korea-like transfer) | **pilot only**; Hong Kong DATA BLOCKED |
| A — follow-up | **E13c level-matched rival** | completed (36/36 stage-2 runs): Prediction 2 survives in formal-access form |
| B — adversarial replication (`experiment-runner-2`) | B1 independent matched-rival replication, B2 floor/race at 4 reps, B3 allocation-rule knockout, B4 10/20/30/40-year trajectories, B5 credential information/recognition | 5 completed |

Never claimed: E4, E9, E11, the recovery study, cross-cutting parameter-uncertainty sampling, the
E16 corruption channel, and all atlas-engine cells
(`floorworld`, `childworld`, `relfloor`, `firms`, `tutoring_abm`) were **not run** in this window.

## 3. What is new, and what broke

- **Reproduced** (fresh runs, not archived output): the 6-arm floor/race table, the graduate-supply
  shock, actor knockouts, gate tutoring shares and the basic-bar sweep, floorworld's 8-test screen.
  Full verdicts in `03_audit/REPRODUCTION_MATRIX.md`.
- **Challenged by this run** (do not put these in print unqualified):
  1. **The graduate-supply income discriminator fails; the formal-access version survives.** With a
     formal/informal margin in both worlds, a competitive CES market also produces diploma-income
     losses at σ ≤ 1 (E13b; replicated independently in B1, where the σ=0.5 cell is numerically
     unstable). After level-matching the two worlds (E13c), the surplus world still shows Δ formal
     probability −0.151 while the rival never shows a material fall (≤ 0.5 pp at σ=2). Claim
     **formal access**, not absolute income; both are simulation-only.
  2. **The China school-support / Double Reduction direction is unidentified, not resolved.** With a
     universal, free, *additive* +0.5 sd support module, paid tutoring spend rose (+18%) and shifted to
     apex gates; with a substitution channel (support damps tutoring's marginal value), paid spend fell
     sharply (−1,292 / −341 / −1,241 across universal, targeted and capacity-limited arms) with no
     learning loss. The sign is set by the substitution elasticity between school support and
     commercial tutoring — an unmeasured parameter. Do not present E18 or E18b as a measured Double
     Reduction effect.
  3. **The relational floor's contribution to *persistence* is at seed noise once ranking is held
     fixed**; what remains is the floor's *movement* (adaptive vs fixed) and the allocation rule.
  4. **The default, uncalibrated Philippine model misses the manuscript's own targets** (e.g.
     basic→college transition 0.227 vs ~0.70 claimed). Calibration is required before any country claim.
- **Corrected in the manuscripts** (from the data ledger): the Philippine 67.0% (2022) completion
  figure is a stale vintage (current UIS: 68.3% 2022, 71.9% 2023, 75.0% 2024; the 67.5% 2013 baseline
  is verified exactly); "more than half lost before secondary completion" is contradicted by the same
  series; HKDSE is standards-referenced, not norm-referenced; the Cambodia "6%" is resolved — 6.6% of
  *employed persons 15+* hold a university degree (urban 13.8%, rural 2.9%), not a share of jobs.
- **Citation problems**: the Ng & Yip (2020) citation in both drafts is likely Gee (2012) conflated;
  Breen–Goldthorpe is cited in neither manuscript; Yang (2026) was abstract-only so its CES equation
  is unverified. Details in `02_lit/SOURCES.json` and `08_council/brief_001/`.

## 4. Honesty rules used

- Stored outputs are labelled *archived*; only re-executed numbers are labelled *reproduced*.
- Every simulated number is labelled simulation. No model output is presented as an observation.
- Pre-declarations were written before each run; failures and amendments are in
  `05_experiments/ERROR_LOG.md`, not deleted.
- Unrun cells are marked `proposed`; blocked data is marked `DATA BLOCKED`, not filled with guesses.
- The synthetic council is labelled as such: panelists are AI composites grounded in published work,
  not statements by the named scholars.

## 5. Layout

```
00_handoff/            the original handoff package (MANIFEST.sha256 verified OK)
01_sources/            read-only: massification_project (triad + massabm) and the Atlas worktree @55732f4
02_lit/                literature ledger, model cards, manuscript comparison, claim register, raw fetches
03_audit/              model inventory, reproduction matrix, provenance, logs, runs
04_data/               data ledger, claim verification, tidy CSVs, raw API/downloads
05_experiments/        batch A: pre-declarations, experiments, summary table, manifest, error log, runs/
05b_experiments/       batch B: adversarial replication + long-run trajectories
06_report/             provenance, council briefs, assembly notes
07_logs/               build_manifest.py and lead logs
08_council/            charter, personas, brief_001/, brief_002/
SUMMARY_FOR_TREY.md    plain-language findings
RUN_MANIFEST.json      environment, inputs, hashes, commands, failures
```

## 6. Reproduce

```bash
PY="/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
# Phase-0 / experiments
cd 05_experiments && "$PY" runs/E18/run_E18.py      # example cell; each runs/<EID>/ has its script
# rebuild the package manifest
cd .. && "$PY" 07_logs/build_manifest.py
# literature fetches
cd 02_lit/notes && "$PY" fetch_sources.py
```

Every experiment cell records its exact command, seeds, N, runtime and source hashes in
`05_experiments/RUN_MANIFEST.json` and `05_experiments/runs/<EID>/run_meta.json`.

## 7. Delivery

- **Local package:** this directory.
- **GitHub:** the user authorised pushing results into an **experimental folder only**. Target branch
  `experiment/massification-2026-11-20`, path `experiments/massification-2026-11-20/`. The Atlas page
  builds from `src/` and `public/` only (verified in `PROVENANCE.md` §2), so this cannot touch it.
  `main` is not modified.
