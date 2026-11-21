# HANDOFF PACKET — massification programme, model-debug addendum (2026-11-21)

**LABEL: `DEBUG`.** This packet is for the **external reviewer (Opus/Sol)**. It records what the record shows, what
the paper's claims are, and the debug corrections opened on 2026-11-21. It licenses **no** reproduction claim, makes
**no** causal or direction claim, and does **not** predeclare a successor generator (D150/D154/D167 stand). The
gate-passed write-up is **unedited**; every amendment below is **prospective**.

## (a) The paper on disk

| path | sha256 | notes |
|---|---|---|
| **canonical:** `/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/00_handoff/papers/02_october_massification.md` | `1138d453a79243f573b57f971369a61f598aecc6f4882f7ff052fd1ea90228cf` | 377 lines, 84,592 bytes; corroborated by that tree's `00_handoff/MANIFEST.sha256` (line 9 verifies) |
| **mirror:** `~/massification_package/massification-2026-11-20/00_handoff/papers/02_october_massification.md` | same | byte-identical copy |

The paper is **not under the programme root** (`…/experiments/massification-2026-11-20/00_handoff/` does not exist).

## (b) The paper's claims vs this record — 18 claims, quoted line-by-line in `benchmark_memo/BENCHMARK_MEMO.md` §7.3

| status | count | claim rows |
|---|---:|---|
| **SHOWN** | **0** | — |
| **PARTIALLY SHOWN** | **3** | P-11 (independent re-implementation was performed — and produced a discriminating negative), P-13 (the conversion/GER instrument premise; the re-entry test itself was never run), P-17 (the 2013 RA 10533 policy fact) |
| **NOT SHOWN** | **15** | P-01, P-02, P-03, P-04, P-05, P-06, P-07, P-08, P-09, P-10, P-12, P-14, P-15, P-16, P-18 |

**The explicit caveat, stated once and binding on every citation of this table:** these statuses are statements about
**what this record established**, not about the paper. **The record never tested these claims — this is not a failure
of the paper.** Two structural causes: (i) the paper's own model outputs are `massabm`/`triad` artefacts and this phase
adjudicated **other** objects (the A1 anchor class, model2, the four registers); (ii) five claims need data that are
not on disk (first-time entrants by age; the dated justification corpus; income-gradient microdata; a graduate-supply
shock; a tutoring series) — the same HELD/data-gap bucket that closed the experiment programme (D167). Full verbatim
quotations, line numbers and per-row evidence: `benchmark_memo/BENCHMARK_MEMO.md` §7.3 (Table 7.1).

## (c) CAP-04 — disclosed defect (not fixed) and its sensitivity

**Defect:** an **undeclared** survival floor **0.02** (`clip(..., 0.02, 0.995)` at
`generator_v1_3/code/sim_v1_3.py:826`; copies in v1.2/v1.3/v1.4/v1.5/v1.6) that **binds in 24 tertiary cells
(1970–72, 20 countries)** and changes `completion_cohort` and every downstream level number. It is identical on all
three frozen panels and is **not** the named ceiling-cap defect. Ruling: **do not retro-fix**; disclose.

**Sensitivity (copies only; same seed/inputs; both copies carry the CAP-01 fix; only the floor differs):**
2024 endpoints (`completion_uis`, pp) — anchor PHL-like: primary **+0.000000**, lower **+0.000000**, upper
**+0.000000**, tertiary **−0.000003**; **max |delta| across 30 countries × 4 levels = 0.000228 pp**; **0 cells differ
by > 0.01 pp**. **Result: CAP-04 = burn-in dissipated by 2024** — no published 2024 endpoint would move materially if
the undeclared floor were removed. Evidence: `cap04_sensitivity/FINDINGS.md`, `cap04_sensitivity/results/`.

## (d) Q-5 — the arm-vs-trend reading hazard (resolved; correction prepared, `applied = false`)

**Hazard:** the write-up recorded the A1 anchor class as "losing to the 4.35 pp linear-trend benchmark"
(`4.352883341604888`), while `anchor_table.csv` shows `complementary · capacity_gated` holdout MAE
**4.014780434743067** below it.

**Resolution — (iii) comparing different tables/objects, and the class claim is not supportable as stated.** The
4.352883… benchmark is the **calibration-table** value (fit **1980–2010** / holdout **2011–2024**, n=17); the 12-arm
holdout range is on the **anchor** windows (fit **1999–2013** / holdout **2014–2024**, n=14). On the **like-for-like**
windows the naive linear-trend MAE is **5.614935464535336 pp**, against which **7 of 12 arms beat** and **5 lose** —
the class does **not** uniformly lose. No arm is re-scored, no model re-run. Corrected sentence + gate re-run:
`q5_resolution/Q5_RESOLUTION.md` §4–§5 (prospective; requires the user's approval before any edit).

## (e) B-1 — the benchmark hierarchy (prospective amendment, `applied = false`)

Persistence / linear-trend benchmarks are a **humility floor, not a dynamic test**: beating or losing to a trend says
only that the model adds (or fails to add) predictive content over extrapolation; it is a **necessary benchmark only**.
The programme's dynamic claims must rest on **transitions, asymmetries, crossing timing and distributional change**.
**0 of the 10 inventoried results identify a dynamic** under the four-condition test (dynamic object / out-of-window /
counterfactual-or-distributional / non-level falsifier); 4 are dynamic-type, 6 floor-only. Recommended to the user as a
**one-footnote framing amendment** (framing, not results); recorded in `benchmark_memo/BENCHMARK_MEMO.md` §B-1 and not
applied. The user's critique (verbatim): *"Of course what happened last year predicts what happens next year… I'm
questioning who the fuck cares — that doesn't identify any dynamic other than 'line goes up'."*

## (f) File list and hashes of this debug work-stream

| file | role |
|---|---|
| `PRE_DECLARATIONS.md` | debug contract (sha `748335cf…` → amended `7d8bade9…`, AMENDMENT 1 measure-aware) |
| `cap_audit/CAP_AUDIT.md`, `CAP_AUDIT_TABLE.csv`, `CAP_AUDIT_CELLS.csv` | 34 clamps: 30 declared / 1 artefact (CAP-01) / 3 undetermined; 35-cell confirmation; per-cell rows |
| `fix_rerun/FIX_RERUN.md`, `results/REPAIRED_*` | the fix (one-sided floor, copies only), 35+35 uncapped, m-constancy deltas (a)–(d), 12/12 determinism |
| `cap04_sensitivity/FINDINGS.md`, `results/panels/` | CAP-04 disclosure + burn-in sensitivity (max 0.000228 pp at 2024) |
| `q5_resolution/Q5_RESOLUTION.md` | Q-5 re-derivation, per-arm table, corrected sentence + gate re-run |
| `benchmark_memo/BENCHMARK_MEMO.md` (§0–§7), `BENCHMARK_INVENTORY.csv` | trend = humility floor; 0/10 dynamic; B-1; handoff packet (§7) |
| `RULINGS.md` | the five Lead rulings and how each was applied |
| `HANDOFF_PACKET.md` | this file |

All DEBUG artifacts are deterministic and self-checksummed in their own directories (`SHA256SUMS.txt`); the delivered
panels and the gate-passed `PHASE_WRITEUP.md` are **byte-identical to their shipped state**.

## (g) Reading order for the reviewer

1. This packet. 2. `benchmark_memo/BENCHMARK_MEMO.md` (§1–§6 the critique; §7 the handoff packet with the 18 claims,
   the 10 results, Q-1…Q-7). 3. `cap_audit/CAP_AUDIT.md`. 4. `fix_rerun/FIX_RERUN.md`.
5. `cap04_sensitivity/FINDINGS.md`. 6. `q5_resolution/Q5_RESOLUTION.md`. 7. `RULINGS.md`.
**Open questions the reviewer is asked to address:** the redesign question (recorded, unanswered — the Lead's ruling
is that it belongs here), the CAP-04 admissibility of the 1970–72 burn-in convention, the Q-5 correction's wording,
and the B-1 footnote. **Do not treat 0/18 as a verdict on the paper.**
