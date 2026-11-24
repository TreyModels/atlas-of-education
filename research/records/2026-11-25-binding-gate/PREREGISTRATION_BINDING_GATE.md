# PRE-REGISTRATION — binding-gate (tournament) sweep

Committed BEFORE any run of this experiment. Engine: `eduengine` at `/root/work/edsystem/engine`
(commit family `4679ddb`), runner `phase_sweep_binding.py` (the pre-registered grid runner plus two CLI
overrides: `--quota-share`, `--bar-levels`; no physics changed).

## Why
The pre-registered phase sweep showed the `bar` gate is **non-binding in this engine** (q1 gate-fail
share ≤ 1.3% at all vacancy levels), so the bar arm is not a tournament and cannot instantiate the
"exam-gate arms race" mechanism. The operator's question ("fee abolition + small formal sector +
rationed exam gate → shadow-education arms race?") presupposes a *binding* gate. The quick-grid
ABSENT verdict is therefore silent on the mechanism, not evidence against it. This experiment makes the
gate actually bind and tests the interaction directly.

## Design (fixed)
- **Seat scarcity via the quota shoulder:** seats as a share of the cohort `S ∈ {0.25, 0.35, 0.45, 0.55, 0.70}`
  (runner `--quota-share S`; the quota arms inherit `S`, the flanking bar arms are unchanged).
- **Secondary binding-bar arm:** bar score thresholds fixed at `14,15,16,17` (`--bar-levels`), a level at
  which the gate-fail share should be large; run at the same X/Y grid for comparison.
- **Grid:** X = the 10 pre-registered vacancy levels (`0.02 … 0.50`); Y = fee ∈ {0.00, 0.04, 0.08, 0.12, 0.16, 0.19}
  (0.00 = E8 abolition slice); seeds 0–4; N=400, T=70, measure_from=35.
- **Runs:** 10 × 6 × 5 = 300 per seat share → 1,500 quota runs; 300 in the bar arm; 1,800 total.
- Determinism: fixed seeds; a duplicate run must reproduce rows byte-identically.

## Hypotheses (tested, not asserted)
- **H1 (binding-only race).** As `S` falls (gate binds harder): q1→q5 **tutoring gap** and q1 **gate-fail
  share** rise. Statistic: Spearman ρ across the five `S` values of the mean tutoring gap; supported if
  ρ < 0 **and** gap(S=0.25) − gap(S=0.70) > 0 with non-overlapping seed CIs.
- **H2 (E8 × scarcity interaction — the operator's question).** The fee-abolition effect on the tutoring
  gap, `Δ_gap = gap(fee=0.19) − gap(fee=0.00)`, is larger when seats are scarce:
  `(Δ_gap at S=0.25) − (Δ_gap at S=0.70) > 0` with non-overlapping seed CIs. This is the primary test.
- **H3 (equifinality under scarcity).** Cells with equal `completion_lower` but different tutoring
  intensity exist across `S`; report count, do not assert a mechanism beyond the accounting caveat that
  completion is partly pinned by seat share.

## Decision rule (fixed before the run)
- H2 **SUPPORTED** if the interaction contrast is positive and seed CIs do not overlap; **NOT SUPPORTED**
  otherwise; **UNDERPOWERED** if seed CIs overlap but point estimates are ordered as predicted.
- H1 as stated. H3 descriptive only.
- Any verdict is **SIMULATION ONLY**, no causal language. Negative results are reported as results.

## Cost / stop rule
~2–4 min total at 10 workers. If any single `S` run errors or exceeds 10 min, stop, keep the partial
outputs, report the failure rather than re-running.
