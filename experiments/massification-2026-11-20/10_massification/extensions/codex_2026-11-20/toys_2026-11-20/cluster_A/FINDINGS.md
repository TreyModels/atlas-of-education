# FINDINGS — Cluster A toys (#1–#3): entry threshold, net vs gross, entry lag

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.**

Every number below is a property of the rules imposed in `PRE_DECLARATIONS.md`, not a measurement of any education
system. "PASS" means only "the toy's output matches the pattern predeclared for the toy". The massification phase
stays CLOSED; nothing here reopens C1–C4, and the only admissible real test remains the observed provider-entry
supply-response cell (brief 014 §3.1).

Run: 200 seeds per cell (`seed_i = 20261120 + i`, i = 0…199), stdlib Python 3.10.2, 26 cells, 234,400 result rows,
0 censored cells, all values finite. Paired design: every arm and counterfactual of a seed reuses that seed's
identical latent cohort (budgets, opportunity costs, lottery order), one-factor shocks, matched period-1 start.

---

## 1. Entry-threshold hysteresis

**Question.** Does a fixed-cost entry threshold (`qty·(tuition − varcost) ≥ F`) with exit-when-unmet produce an
asymmetric supply response — exit faster/stronger than entry — after a ±20% demand shock?

**Design.** 100 households, 30 public seats, 4 private providers × 8 seats, tuition 2.00, variable cost 1.00
(contribution 1.00/seat). `F_low = $4.00` (break-even 4 seats), `F_high = $8.00` (break-even 8 seats = one full
provider). Premium path t = 1…4: `1.00, 1.20, 1.20, 1.00` (up) or `1.00, 0.80, 0.80, 1.00` (down). Four arms
{F_low, F_high} × {up, down}, all on the same 200 cohorts. Exit/entry is contemporaneous (no lag) and capacity is a
fixed lump per provider (the base toy's fixed `PRIVATE_CAPACITY` reading). A "build-to-demand" capacity variant is
reported as a declared robustness cell.

**Key numbers (means over 200 seeds).**

| | F_low | F_high |
|---|---|---|
| t1 private installed seats / admissions | 19.16 / 17.87 | 15.12 / 15.12 |
| t1 private vacancy / backlog | 1.30 / 0.66 | 0.00 / 3.40 |
| t1 providers (mean) | 2.395 | 1.890 |
| up-shock: private seats t2 (change) | 28.60 (+9.44) | 24.60 (+9.48) |
| down-shock: private seats t2 (change) | 9.48 (−9.68) | 5.32 (−9.80) |
| up-shock: private admissions t2 | 27.35 | 24.60 |
| down-shock: private admissions t2 | 8.27 | 5.32 |
| share of seeds with an **entry** event | 0.915 | 0.960 |
| share of seeds with an **exit** event | 0.950 | 0.940 |
| mean providers **entered** at impact | 1.180 | 1.185 |
| mean providers **exited** at impact | 1.210 | 1.225 |
| **A = mean exit seats / mean entry seats** | **1.025** | **1.034** |
| recovery ratio (t4 seats / t1 seats) | 1.000 | 1.000 |

Demand behind those numbers: applications 85.66 → 100.00 (up, censored at the cohort ceiling) / 62.64 (down);
private customers 18.52 → 28.03 / 8.95.

**Threshold verdict.** **FAIL.** T1a (`A_high ≥ 1.25`) fails: `A_high = 1.034`. T1b
(`A_high − A_low ≥ 0.25`) fails: the difference is 0.008. The predeclared band `1.00 < A_high < 1.25` ("weak /
ambiguous") is where the result sits — but at 1.03 it is, for practical purposes, symmetric.

**Falsifier status.** **TRIGGERED.** "No asymmetry (symmetric response) → the fixed-cost story adds nothing."
The exit and entry responses are almost the same distribution, not merely the same mean: F_high exit events are
{0 providers: 12 seeds, 1: 132, 2: 55, 3: 1}; F_high entry events are {0: 8, 1: 147, 2: 45}. At this parameterisation
the fixed-cost threshold shifts the *level* and makes supply *discrete*, but it does not tilt exit against entry.

**Why it is symmetric (mechanism, not accident).** A −20% shock takes the private customer pool to ~8.95 households,
which is still enough to keep exactly one 8-seat provider at its 8-seat break-even; a +20% shock takes it to ~28.03,
enough to justify one more 8-seat provider. Both directions therefore move the market by about 1.2 provider units.
The threshold is a *step*, and a ±20% shock lands on the same step size in both directions. Producing "fast exit,
slow entry" from a fixed cost therefore needs a second, asymmetric friction — sunk-cost band, financing, or an entry
lag. Experiment #3 supplies the entry lag and does produce the asymmetry.

**Robustness (declared).** The discarded "build-to-demand" capacity rule gives the same near-symmetry
(`A_high = 1.034`) and `A_low = 0.914`; the null does not depend on the lumpiness assumption.

**Caveats.** (i) The market is shallow (≈1.9 providers at baseline; 4 maximum), so one provider is 52% of the
private sector and every event is a large discrete jump; means are mixture averages of 0/1/2-provider events.
(ii) The up-shock saturates the *application* pool at 100 households (censoring), though not the private customer
pool (28.03 of a possible ~35), so the up-shock is not a clean 20% demand increase in applications. (iii) With
contemporaneous decisions, timing asymmetry is zero *by construction*; only magnitudes could differ, and they do not.
(iv) `bk = cap` makes high-F survival depend on exactly filling one provider — a knife-edge by design, not by estimate.

---

## 2. Public expansion with private exit (net vs gross)

**Question.** How much of a public seat expansion survives private provider exit?

**Design.** Comparative statics with mature providers, premium fixed at 4.0, 200 paired cohorts. Primary:
2 providers × 15 seats. `F_low = $4.00` (break-even 4), `F_high = $15.00` (break-even 15 = one full provider);
`F = $12.00` (the base toy's own value) is reported as a **sensitivity** cell because break-even 12 sits on the mean
post-expansion customer pool (12.17 households) — a knife-edge, not a clean test. Expansions 30→50 and 38→39.
Secondary capacity replication: 1 provider × 30 seats.

**Key numbers (means over 200 seeds; applications fixed at 85.66 by construction — demand is not shocked).**

| arm | public pre→post | private admissions pre→post | total pre→post | gross | net | **R = net/gross** | exit share |
|---|---|---|---|---|---|---|---|
| cap15, F_high, 30→50 | 30→50 | 13.43→3.15 | 43.43→53.15 | +20.0 | **+9.73** | **0.486** | 0.685 |
| cap15, F_mid $12, 30→50 | 30→50 | 14.75→8.05 | 44.75→58.05 | +20.0 | +13.31 | 0.665 | 0.405 |
| cap15, F_low, 30→50 | 30→50 | 17.84→12.00 | 47.84→62.00 | +20.0 | +14.16 | 0.708 | 0.465 |
| cap15, F_high, 38→39 | 38→39 | 9.90→9.45 | 47.90→48.45 | +1.0 | +0.55 | 0.550 | 0.030 |
| cap15, F_low, 38→39 | 38→39 | 15.26→14.97 | 53.26→53.97 | +1.0 | +0.71 | 0.710 | 0.025 |
| cap30, F_high, 30→50 | 30→50 | 17.16→3.43 | 47.16→53.43 | +20.0 | +6.28 | 0.314 | 0.685 |
| cap30, F_low, 30→50 | 30→50 | 18.52→12.17 | 48.52→62.17 | +20.0 | +13.65 | 0.682 | 0.000 |

The mixture is stark: in the 137 of 200 seeds where the high-F provider exits, net gain is **exactly +5** (the 20 new
public seats minus the 15 lost private seats); in the other 63 seeds net gain is **exactly +20** (net = gross, no
exit). No seed has a negative net gain at 15-seat capacity; at 30-seat capacity, **42 of 200 seeds have net ≤ 0**
(private loss exceeds the gross public gain).

**Threshold verdict.** **PASS, on a thin margin.** T2a (`R(F_high, 30→50) < 0.50`): 0.486 — 1.4 pp below the bar.
T2b (`R(F_low, 30→50) ≥ 0.50`): 0.708 — pass. T2c (exit share ≥ 0.50): 0.685 — pass. The pass is arithmetically
`R = 1 − (exit share 0.685) × (15 lost / 20 gross)` = 0.486, i.e. the toy sits essentially on the 50% boundary; a
14-seed swing in the exit count would flip the verdict.

**Falsifier status.** **Not triggered.** The falsifier was `R ≥ 0.90` (net ≈ gross). The predeclared band
`0.50 ≤ R < 0.90` ("partial offset") is not entered either — 0.486 is in the "below" band.

**Sensitivity (disclosed, not primary).** With the base toy's `F = $12.00` the retention is **0.665**, i.e. T2a would
have **failed**; with 30-seat capacity and `F = $15.00` retention is 0.314 (stronger offset). The direction of the
result is robust across capacity and F; only the magnitude crosses the predeclared 50% line.

**Caveats.** (i) All-or-nothing provider exit makes the toy bimodal (retention 0% or 100% per seed), so "net vs
gross" is a mixture, not a smooth elasticity. (ii) The exit threshold and the post-expansion customer pool are close
by construction; the exit share is therefore a design-sensitive quantity. (iii) Nothing here says public expansion
"crowds out" private supply in any real system: real providers can shrink, cut quality, or hold price; this toy only
lets them exit whole. (iv) Applications are held fixed; if public expansion drew new applicants, gross and net would
both rise.

---

## 3. Provider entry lag and overshoot

**Question.** Does a lag between the entry decision and installed capacity produce enrolment deficits during a boom
and idle capacity (overshoot) after it?

**Design.** 30 public seats; 10 providers × 4 seats; `F = $4.00` (break-even 4 = one full provider); 12 periods.
Temporary boom: premium multiplier 1.20 in t = 2…5, back to 1.00 from t = 6. Permanent boom: 1.20 from t = 2.
Entry lag `L ∈ {0, 2, 4}` = periods between the order and the provider's first active period; **exit is immediate**
and a new provider is locked in for its first active period; entrants see capacity already under construction.
Six cells, 200 seeds, all cells on the same cohorts.

**Key numbers (means over 200 seeds; vacancy = installed seats − customers, i.e. idle capacity).**

| cell | peak vacancy | peak backlog | cumulative vacancy | cumulative backlog | admissions over 12 periods | time to steady state |
|---|---|---|---|---|---|---|
| L=0, temporary | 0.00 | 2.07 | 0.00 | 16.76 | 603.52 | 6.0 |
| L=2, temporary | 0.00 | 10.89 | 0.00 | 35.68 | 584.60 | 6.0 |
| **L=4, temporary** | **8.08** | 10.89 | **8.08** | 53.22 | 567.06 | 7.0 |
| L=0, permanent | 0.00 | 2.07 | 0.00 | 17.11 | 669.74 | 2.0 |
| L=2, permanent | 0.00 | 10.89 | 0.00 | 36.03 | 650.82 | 4.0 |
| L=4, permanent | 0.00 | 10.89 | 0.00 | 54.95 | 631.90 | 6.0 |

Paired against the same seed's L=0 path, L=4 under the temporary shock shows a peak admission shortfall of 9.46
seats during the boom and a small peak admission *excess* of 1.38 seats after it. Idle capacity appears in **100%**
of L=4 temporary seeds (max 16 seats) and in **0%** of every other cell. Steady-state is reached 1 period after the
boom ends (t = 7) for L=4 temporary, vs t = 6 for L=0/L=2; under the permanent shock it is t = 6 / 4 / 2 for
L = 4 / 2 / 0, with no censoring (0 of 200 seeds in every cell).

**Threshold verdict.** **PASS, on a thin margin.** T3a (`peak vacancy L=4 temporary ≥ 8.0`): 8.08 — margin 0.08
seats. T3b (`≥ L=0 temporary + 4.0`): 8.08 ≥ 4.0 — pass. T3c (`L=4 permanent < 4.0`): 0.00 — pass. The direction and
the temporary-vs-permanent contrast are unambiguous; only the level sits on the declared floor.

**Falsifier status.** **Not triggered** (`8.08 > 0 + 2`).

**Why the threshold appears at L=4 and not L=2 (mechanism, not accident).** The boom lasts 4 periods. An L=2 order
placed at t = 2 arrives at t = 4, *inside* the boom, where the extra 4-seat units are used. An L=4 order placed at
t = 2 arrives at t = 6, one period *after* the boom has ended, when demand has fallen back to ~18.5 — so the new
capacity is idle for a period before it can exit (installation lock). Overshoot therefore requires
**lag > remaining boom length**, not L=4 in particular: the same code with a 2-period boom would put L=2 in the
overshoot column. Under a permanent shock the late capacity is absorbed and vacancy stays at zero — the cost of the
lag then shows up only as a longer deficit.

**Monotone cost (descriptive).** Longer lags buy lower vacancy risk only by paying more deficit: admissions over the
12 periods fall monotonically with L under both shocks (603.5 → 584.6 → 567.1 temporary; 669.7 → 650.8 → 631.9
permanent). In this toy there is no lag that is "best"; the two error types trade off.

**Caveats.** (i) The overshoot magnitude is one capacity unit per late order times the number of orders the boom
sustains — it is bounded by the lump size and the boom length, both stipulated. (ii) Pipeline-aware entrants mean
over-entry cannot come from coordination failure; it comes purely from the lag outlasting the boom. (iii) The
installation lock (a new provider must serve one period before exit) is what converts late arrival into recorded
vacancy; without it the entrant would exit in the same period and the toy would show no overshoot at all.
(iv) Demand is exogenous and does not anticipate capacity; a forward-looking provider would not build into a known
temporary boom.

---

## 4. Failures, thin margins, and what would change the verdicts

* **#1 primary threshold failed and its falsifier fired.** The fixed-cost threshold alone did not generate
  exit-faster-than-entry asymmetry at ±20% with contemporaneous decisions. This is the toy's substantive negative
  result, and it is reported as such, not rerun with a different threshold.
* **#2 and #3 passed on thin margins** (0.486 vs 0.50; 8.08 vs 8.0). Both margins are smaller than the seed-to-seed
  spread of the underlying quantities, so the honest reading is "on the boundary", not "comfortably above".
  The predeclared numbers were not moved after the run; the margins are disclosed here instead.
* **Censored cells: none.** Every cell has 200 distinct seeds; no metric was undefined; no run crashed. The sentinel value is
  `-999` (for `retention` when gross gain is 0, `recovery_ratio` when baseline seats are 0, and
  `time_to_steady_state` when the path never settles); it occurs in **no** delivered cell, and no negative net gain is
  confusable with it.
* **Amendment disclosure.** Before the final run, `PRE_DECLARATIONS.md` was amended (Amendment 1) to replace a
  capacity rule that did not match the base toy and to standardise the high-F break-even at one full provider
  (`F = cap × contribution`), after a 6-seed mechanics smoke test. Thresholds and falsifiers were **not** changed.
  The pre-amendment #2 parameterisation (`F = $12.00`) is retained and reported as a sensitivity cell (R = 0.665),
  so the reader can see what the earlier vector would have produced.

---

## 5. What these toys can and cannot say

**Can.** Show that (a) fixed-cost entry thresholds make private supply discrete and create full-sector exit under a
public expansion — the net-vs-gross arithmetic is a mixture of "no exit, net = gross" and "exit, net = gross minus
the lost lump"; (b) a fixed-cost threshold by itself does **not** produce fast-exit/slow-entry; (c) an entry lag
does, but only when the lag outlasts the demand boom, and it trades deficit against vacancy.

**Cannot.** Test any historical claim; calibrate F, capacity, tuition or demand; reopen C1–C4; or speak to the
observed provider-entry supply-response question, which still requires the real-data cell in brief 014 §3.1. If
anything, #2 and #3 sharpen what that cell would have to measure: *net* (not gross) public-seat gains, private
provider exit as an outcome, and the lag between entry decisions and installed capacity.

---

## 6. Files

| file | contents |
|---|---|
| `PRE_DECLARATIONS.md` | predeclared rules, parameter vectors, thresholds, falsifiers; Amendment 1 |
| `code/toy_market.py` | household side + provider entry/exit engine (stdlib only) |
| `code/run_cluster_a.py` | the three experiments; writes `RESULTS.csv`, `RESULTS_SUMMARY.json` |
| `code/verdicts.py` | mechanical evaluation of the predeclared thresholds → `verdicts.json` |
| `code/build_manifest.py` | assembles `RUN_MANIFEST.json` (seeds, params, hashes) |
| `RESULTS.csv` | 234,400 rows, long format `experiment,arm,seed,metric,value`, aggregate rows with `seed=AGG` |
| `RESULTS_SUMMARY.json` | every aggregate quoted above, with the imposed parameter vectors |
| `verdicts.json` | threshold-by-threshold PASS/FAIL and falsifier status |
| `RUN_MANIFEST.json` | seeds, reps, Python version, parameter vectors, SHA-256 of every artefact |

Reproduce: `cd code && python3 run_cluster_a.py && python3 verdicts.py && python3 build_manifest.py`
(deterministic: identical `RESULTS.csv` on any Python 3.10+ with the same source).

*Label applies to every file in this directory, including `RESULTS.csv`: ILLUSTRATIVE TOY — stipulated parameters;
not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.*
