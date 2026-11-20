# Council toy-experiment battery (brief 015) — illustrative only

**Status:** ILLUSTRATIVE TOY — stipulated parameters; not calibrated; **not evidence**; no historical test;
the massification phase remains **CLOSED**. These are small, seeded, stdlib-Python toy models built to the
Council's brief-015 specifications (`COUNCIL_TOY_SPECS_015.md`) as mechanism pedagogy and hypothesis
generation. A toy "PASS" means only that its stipulated rules mechanically generate the pattern predeclared
for that toy; it says nothing about the world.

**Provenance:** specs = Council brief 014 follow-on (`COUNCIL_TOY_SPECS_015.md`); base toys = Codex bundles
`codex-massification-5eec11470690.zip` and `luna-01-15-948a07a2567b.zip` (archived here); execution = five
parallel cluster agents on 20 Nov 2026; the closed anchor (`4ba958c` / closeout) is untouched.

## Protocol (all clusters)

Stdlib Python 3.10, fixed seeds, **paired** counterfactuals with identical latent draws, matched starting
conditions, one-factor shocks, **≥100–500 seeds per cell**, thresholds and falsifiers **predeclared** in each
cluster's `PRE_DECLARATIONS.md` before the run, all cells reported (including failures, censored cells, and
disclosed amendments), and every output labelled `ILLUSTRATIVE TOY — stipulated parameters; not calibrated;
not evidence`. Each cluster is deterministic (re-run reproduces `RESULTS.csv` byte-for-byte) and records its
parameter vector in `RUN_MANIFEST.json`.

## Experiments, clusters, and predeclared verdicts

| # | experiment | key result (toy units) | verdict |
|---|---|---|---|
| **A1** | entry-threshold hysteresis | exit/entry seat ratio A = 1.034 (F-high) / 1.025 (F-low), A_diff 0.008 vs ≥0.25; entry/exit distributions near-identical | **FAIL — falsifier fired**: fixed cost buys discreteness, not asymmetry; needs a second friction |
| **A2** | public expansion, net vs gross | 30→50 seats: gross +20, private −10.28, net +9.73, **R = 0.486** (<0.50 rule); 38→39 R=0.550; 30-seat secondary capacity R=0.314 with **42/200 seeds net ≤ 0** | **PASS (boundary)** — expansion can lower total admissions |
| **A3** | entry lag and overshoot | L=4 temporary boom peak vacancy **8.08** (rule ≥8.0), 0.00 at L=0/2 and in permanent cells; overshoot only if lag **outlasts the boom** | **PASS (thin)** |
| **B4** | visibility × mechanism (HC vs signalling) | signalling true output **rises** 0.499→0.627→0.796 as visibility rises; v=1 cell degenerate (0 applicants); employer-valued output falls only v=0→0.5 | 2 tests **NOT MET**, 1 PASS, falsifier not fired — visibility shuts the signalling market, not degrades it |
| **B5** | queue vs human capital | rank sends older-group hires to **0.00** (ref 7.61), output −0.147; skill output +0.405; responsive jobs: allocation gap vanishes exactly, fixed skill gap −0.200 remains (attenuated 63.8%) | 3 PASS, 1 NOT MET (literal "separation disappears") |
| **B6** | eligibility repeal vs blind ranking | gate repeal alone **no-op** (credentialed ≥ offers); blind+repealed uncredentialed offer rate 0.350; sensitivity 25/75 → 0.133 | 2 PASS, 2 NOT MET — gate and visibility are **complements** |
| **C7** | capacity by level (floor/ceiling) | floor +44.43 pp, middle +11.71, ceiling +4.58 (never crosses 0.25); secondary converts **70.2%** of added seats (>50% cap) | 4 PASS, **2 FAIL** — A10 floor-not-ceiling shape survives; saturation sits at the gate, not the level; one wording defect |
| **C8** | enforcement × compulsory law | law with e=0: attendance +1.09 pp; e=1: +18.63 pp, completion +20.29 pp; **enforcement without law = 0.000** | all PASS — the law needs enforcement; enforcement needs the law |
| **C9** | buildings vs teachers at equal budget | rooms-only: +40 physical rooms, **+0.00 staffed, +0.00 completion**; teachers-only best PTR; split best completion +22.2 pp | all PASS — composition matters |
| **D10** | level-first roll-out and crossing order | order moves crossing years and preserves floor→ceiling order; spacing clause fails | **PARTIAL** |
| **D11** | cohort-size shock × capacity | interaction is the phenomenon: a 20% larger cohort delays floor take-off when capacity fails to scale | **SUPPORTED** |
| **D12** | temporary expansion with expectations | expectation mechanism works; hire-magnitude/decay rules fail (~60% of gap persists 5–7 cohorts) | **PARTIAL** |
| **E13** | migration and remittance route | route +15.22 pp completion [14.89,15.54]; remittances +8.05 apps/cycle, +3.54 pp completion; local output −1.7% via selection | all PASS |
| **E14** | sector shock × field access | open-access shock apps +106.5, completers +90.1; gate attenuates to ~30%; but shock **expands** total completers +24.68 (>10 allowance) and closed-vacancy margin over-predicted | core PASS, 2 FAIL |
| **E15** | information and roads | info effect +0.0634/hh at road=1 vs +0.0328 at road=0 (interaction +0.0307 < 0.06); road main +0.2265; queue +0.0481 misses 0.05 floor; roads redistribute to far quartile | 1 PASS, 3 FAIL — interaction is a dose effect, not complementarity |

## What the battery suggests (hypotheses, not findings)

- **Supply response is about frictions, not fixed costs alone**: net≠gross works via all-or-nothing exit
  (A2), but asymmetry needs an explicit lag (A1 negative, A3 positive).
- **A public expansion can lower total admissions** under tight private capacity (A2 at 30-seat capacity).
- **Capacity buys the floor, not the ceiling** reproduces in the toy (C7), with saturation at the gate.
- **Enforcement and law are complements** (C8); **buildings and teachers are not substitutes** at equal budget (C9).
- **Rival signatures are not separated by visibility** in the obvious direction (B4); **gate and visibility are
  complements** (B6) — a one-lever natural experiment can be a null by construction.
- **Demand/access shocks** move outcomes only where access exists (E14), and information needs accessibility (E15).

## Cluster index

| cluster | experiments | code / outputs | seeds |
|---|---|---|---|
| `cluster_A/` | 1–3 provider entry/supply | `code/`, `PRE_DECLARATIONS.md`, `FINDINGS.md`, `RESULTS.csv` (234,400 rows), `RUN_MANIFEST.json` | 200/cell, 26 cells |
| `cluster_B/` | 4–6 rival discrimination | `code/`, `PRE_DECLARATIONS.md`, `FINDINGS.md`, `RESULTS.csv` (84,000 rows), `RUN_MANIFEST.json` | 500/cell, 20 cells |
| `cluster_C/` | 7–9 capacity | `code/`, `PRE_DECLARATIONS.md`, `FINDINGS.md`, `RESULTS.csv` (375 rows), `RUN_MANIFEST.json` | 200/cell |
| `cluster_D/` | 10–12 timing/asymmetry | `code/`, `PRE_DECLARATIONS.md`, `FINDINGS.md`, `RESULTS.csv`, `RUN_MANIFEST.json` | 200–240/cell |
| `cluster_E/` | 13–15 market pull/geography | `code/`, `PRE_DECLARATIONS.md`, `FINDINGS.md`, `RESULTS.csv` (369 rows), `RUN_MANIFEST.json` | 200/cell |

Reproduce a cluster from its `code/` directory (each has a `run_all`/`run_cluster` entry point; several include
a `verify_results.py` that re-derives the verdicts from `RESULTS.csv`).

## Honest limits

These toys stipulate the premium (4.0), budgets/costs, private capacity/fixed cost, rural cost multipliers,
information and enforcement intensities. Several results are **load-bearing on those stipulations** (e.g. B5's
credential-inflation queue, B6's zero credential–skill correlation, A2's all-or-nothing exit, B4's premium
4(1−v) making v=1 degenerate). No toy is calibrated, none uses observed data, and none can test history or
reopen the closed phase's C1–C4. Alternative rules were not run unless predeclared.

## Canonical location (housekeeping)

The canonical home of this battery is **this committed folder** under
`experiments/massification-2026-11-20/10_massification/extensions/codex_2026-11-20/toys_2026-11-20/`.
`extensions_archive/` was a staging workspace used while the clusters ran; it is not canonical and has been
moved out of the repository. Cluster paths in the Council's brief-016 text refer to the pre-commit staging
tree; every artifact it cites is present here with the same hashes (see `SHA256SUMS.txt`).
