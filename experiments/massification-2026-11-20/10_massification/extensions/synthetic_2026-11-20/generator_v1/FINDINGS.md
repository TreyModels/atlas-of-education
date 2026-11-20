# FINDINGS — what the SYNTHETIC generator v1 does, what it reproduces, and what it fails

**`LABEL: SYNTHETIC.` Every number in this file was produced by a declared-assumption simulator. None of it
is evidence about the world, none of it is an estimate, and none of it licenses a causal claim. No real
country is modelled. The only observed numbers that entered the code are the declared PHL targets listed in
[`PARAMS.md`](PARAMS.md) §2.**

---

**In plain English.** I built a synthetic world of 30 fake countries running 1970–2025, in which schooling
is a pipeline of cohorts (primary → lower secondary → upper secondary → tertiary), graduates queue for four
formal job rungs whose number and mix depend on how complex the economy is, everyone who does not get a
formal rung lands in an informal block, and output grows from sector productivity plus a one-off step each
time a worker moves from informal work into a formal rung. One country, `SYN00_PHL_LIKE`, is a declared
parameterisation intended to resemble the published Philippine signature: a narrow office sector, a clerical
hiring boom in the 2000s, and a K-12-style break in the upper-secondary pipeline. In that country the
generator puts universal primary completion in 2017, universal lower-secondary in 2024, and leaves
upper-secondary stuck near 75 % and never crossing 90 — the "floor and middle move, the ceiling does not"
asymmetry. It also reproduces the user's 2015 pattern in the cross-section: adult literacy is strongly
associated with growth while a years-of-schooling proxy is associated with about a ninth as much. But when I
tried to *remove* the machinery that is supposed to cause that pattern — the takeoff regime and the job
ladder — the literacy association barely moved. So the generator reproduces the pattern without reproducing
its stated cause, and that is the most important thing in this file.

Panel: 30 countries × 56 years × 4 levels = 6 720 rows, seed `20261120`, ≈1 s per run,
deterministic to the byte.

---

## 1. Check results (the predeclared A–F table)

| check | verdict | headline numbers |
|---|---|---|
| **A** PHL signature | **PASS — but target-encoded** | primary first ≥90 **2017**; lower-sec first ≥90 **2024** (2023 = 87.2); upper-sec never ≥90, max **75.1**, 2024 = 75.1; tertiary GER **15.3 → 50.3** (1971→2025); floor→middle gap **7 y**; ceiling residual **14.9 pp** |
| **B** literacy vs years of schooling | **FAIL (2 of 3 conditions)** | pooled decade-FE: `b_lit` = **+2.37** (p < 1e−4), `b_yos` = **+0.26** (p < 1e−4) — the headline pattern holds; the **takeoff ablation gives `b_lit` = +2.29**, i.e. the association *survives* removing the mechanism (condition B3 fails) |
| **C** no horse race at primary | **PASS (half structural)** | primary-margin return vs queue pressure = **−0.49** (with literacy control; no *positive* rank premium); credential ladder `w_rung2/w_rung1` vs pressure = **+4.76** (p < 1e−6). The rung-1 rank factor is 1.0 by construction — the flatness is a design restriction, not a result |
| **D** ECI gating | **PASS** | +10 % schooling push: Δgrowth per unit X(1980) = **+0.022 pp** (p = 6e−8); high-X tercile **+0.029 pp** vs low-X **+0.005 pp** (ratio 6.2) |
| **E** composition > totals | **PASS** | twins with identical graduates (within 1.4 %): growth **3.10 % vs 2.50 %**, queue pressure **0.0001 vs 0.0028** (95 % apart) |
| **F** accounting | **PASS** | GER ∈ [2.83, 105.0]; completion ∈ [2.10, 95.11]; shares sum to 1 within 2e−16; cohort conservation residual 2e−16; no negative stocks |

`reproduction_checks_v1.csv` is the machine-readable version; `reproduction_checks_detail_v1.csv` carries
the six A sub-conditions and the B/C/D component numbers.

---

## 2. What reproduces

1. **The shape of the asymmetry, in one run.** Primary and lower-secondary cross the 90 % line seven years
   apart; the ceiling plateaus at 75 % and never crosses. Nobody rescues the ceiling: it is capped by upper
   secondary *seats* (0.845–0.875 of the cohort), not by a fitted completion ceiling.
2. **The participation/completion split.** PHL primary GER sits at 101–105 from 1970 while completion runs
   70–95: the same system, two different objects. GER is bounded and the bound is a gate (`ger_cap` = 105).
3. **Composition beats totals (E).** Two economies with the same graduates, differing only in sector mix,
   diverge by 0.6 pp of annual growth and by a factor of ~25 in queue pressure. This is the
   Philippines-versus-diversified point in miniature, and it is a controlled comparison rather than a
   cross-country correlation.
4. **Gating (D).** The same schooling push buys about six times as much growth in high-complexity economies,
   where the technical and professional rungs exist, as in low-complexity ones where they do not.
5. **The queue does wage work.** As lower-secondary+ graduates pile up against fixed rungs, the
   clerical-to-elementary wage ratio rises with queue pressure (coefficient +4.8 on log wages), which is
   credential inflation appearing as a price rather than as a residual.

## 3. What does not reproduce

1. **Completion above gross enrolment is impossible in this architecture.** Observed PHL 2024: primary
   completion 98.3 with GER 94.0; lower-secondary 92.4 with GER ≈88; upper-secondary 75.0 with GER ≈66. The
   generator's cohort-flow identity makes completion a share of the *entering* cohort, so it can never
   exceed the entering GER — and it tops out at **94.0** for primary, **90.4** for lower-secondary. Either
   the observed series use a different denominator (the UIS completion rate is measured on children 3–5
   years *above* grade age, not on the GER age band) or the identity is wrong. v1 cannot tell which, and
   cannot produce the observed levels without a measurement-factor parameter I refused to add.
2. **The K-12 dip does not appear anywhere.** Upper-secondary completion rises monotonically to 75.1 with no
   dip, and tertiary GER goes 42.1 (2016) → 43.9 (2018) — the wrong direction. The declared pipeline break
   is real in the code (it removes 7–10 % of upper-secondary completions in 2018–2021) but it is swamped:
   the tertiary eligible pool is ~1.5× an annual completer cohort while tertiary intake is only ~0.45×, so a
   two-year break in the inflow never binds. **Layer responsible: the tertiary eligibility gate (Layer 1),
   which is too loose to transmit a ceiling shock downward.**
3. **The ceiling peaks in the wrong year.** Observed upper-secondary peaks in 2017 (76.4) and dips to 68.3 by
   2022; the generator's max is 2024. Check A's band test passes, its shape test would not.
4. **Literacy's growth association is over-determined (B).** Removing the takeoff switch changes `b_lit` from
   +2.37 to +2.29; removing the entire job ladder (only the elementary rung survives) gives +2.10. The
   association is carried by the correlation between literacy and the income/complexity path, which drives
   sector productivity directly — **not** by the takeoff/occupation structure the architecture nominates.
   The pre-industrial subsample also shows a *positive* literacy–growth slope (+1.75, p < 1e−4),
   which the architecture says should be ~0; within the industrializing/diversified subsample it is
   actually slightly *negative* (r = −0.15). So the user's 2015 pattern is reproduced for the wrong reason.
5. **The middle level's own shape is off.** Lower-secondary completion 1999 = 57.0 (observed 58.9) and 2013 =
   71.4 (observed 71.3) are close, but 2017 = 77.3 (observed 81.3) and the series is too flat between 2014
   and 2020. This is the cost of encoding the crossing year rather than the whole path.

## 4. Which assumption is load-bearing

**The upper-secondary seat cap.** Set it to 0.845–0.875 and the ceiling is arithmetically incapable of
crossing 90 whatever the floor does; set it on the same growth path as the floor (0.58 → 1.00, as
lower-secondary has) and upper-secondary completion follows the floor to ~95 and the entire anchor
asymmetry disappears. Nothing else in the model is close to as powerful: not the queue, not the rank
premium, not the takeoff switch, not the sector mix.

That is uncomfortable, because the seat cap is the one object I *stipulated* rather than derived (from
CAP-04's "capacity buys the floor, not the ceiling", which the fact register itself labels a model-side
ruling that the data cannot separate at n = 6). So the honest statement is: **v1 reproduces the asymmetry by
assuming the asymmetry.** The second most load-bearing object is the declared floor survival path, which is
interpolated through the PHL completion anchors and therefore target-encoded.

What is *not* load-bearing: the rung ladder. Check D says the ladder matters for how much growth a schooling
increment buys; check B's ablation says it does not matter for whether literacy correlates with growth at
all. Both can be true, and together they are the most useful thing the generator produced: the ladder
governs the *marginal return* to more schooling, not the *level* association between literacy and growth.

## 5. Two failures I would put in front of a reader

**(i) The association survives the removal of its own mechanism.** B was designed as a three-part test; the
two headline parts pass (literacy strongly, years of schooling weakly) and the ablation part fails badly. A
generator that produced the user's 2015 pattern *and* lost it when the takeoff structure was switched off
would have been evidence that the structure is what makes the pattern. This one produces the pattern no
matter what, which means the pattern in synthetic data is not diagnostic of the mechanism. That is a
negative result about the *test*, not about the world — and it is the reason the "literacy positive,
schooling weak" result here should not be read as support for any account of massification.

**(ii) "Universalisation" is measure-dependent and the generator proves it by failing.** The observed PHL
series has completion above GER at all three levels in 2024. A cohort-flow model cannot do that; a system
with over-age enrolment and an age-band completion measure can. The gap between the two is not a modelling
nicety — it is the difference between "primary became universal in 1971" (GER) and "in 2017" (completion),
which is the ambiguity `MUST_REPRODUCE` R2 flags. v1 lands on the cohort-flow side of that ambiguity and
therefore reports *later* dates than a GER-based model, but it cannot reach the observed 98.3 without
switching denominators.

---

## 6. Labelling, provenance, and what a reader may do with this

- Every output row carries `label = SYNTHETIC`; every file in this directory says so in its first lines.
- **Not evidence.** No claim about the Philippines, about any country, about education policy, or about
  causation. The `SYN00_PHL_LIKE` country is a declared target-chasing parameterisation; its agreement with
  the published signature is partly *by construction* and is labelled as such in check A's note.
- **Not a fit.** No least squares, no calibration run, no likelihood anywhere. The two places where an
  observed number sets a value are listed exhaustively in `PARAMS.md` §2a.
- **Reproducible.** Same seed → byte-identical CSVs, verified by two fresh runs; `RUN_MANIFEST.json` records
  the code sha256, the parameter block, the encoded targets, python/numpy versions, and the check summary.
- **Where to look next.** If this architecture is to be tested rather than demonstrated, the seat-cap
  stipulation has to be replaced by something derived from the economy side (who hires upper-secondary
  completers, and at what wage), and the tertiary eligibility gate has to be tight enough to transmit a
  ceiling shock. Until then v1 is a well-labelled toy that can fail its own checks — which is the only kind
  worth building.
