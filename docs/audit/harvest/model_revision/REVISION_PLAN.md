# Model revision plan — HK/Korea shadow-education contest model

**Status:** ACTIVE. **Labels:** all numbers produced under this plan are **SIMULATION** (stochastic model output,
not empirical estimates; no causal language). **Date:** 2026-11-25. **Worker:** `model-fix`.
**Branch:** `research/model-revision-2026-11-25` (base `1c3417c`). **Worktree:** `/Users/treymenefee/neon-boot/wt3/model`.

This plan responds to the confirmed external review (`papers/shadow-education-contest/REVIEW_RESPONSE_2026-11-25.md`,
committed on branch `research/shadow-education-contest-2026-11-25` @ `7356c97`). It is committed **before** the final
calibration and policy-arm rerun; every design decision that the rerun depends on is declared here.

---

## 0. Defects this plan fixes (mapped to the review)

| # | review item | fix in this plan | where |
|---|---|---|---|
| 1 | two result generations disagree (420 vs 540) | freeze **canonical = restored 420 parameterisation, ported onto the current patched engine**; 540 kept as documented alternative | §1 |
| 2 | CF4 win-win claim fails its own test | rerun all arms and report CF4a/CF4b **as failures**, no tuning | §6 |
| 3A | KR Grade-9 contest is a phantom prize (no lasting consequence) | `elite9` placement flag with two persistent realized channels + two sensitivity variants | §2 |
| 3B | expected probability (`1−exp(−λx^r)`) inconsistent with Gumbel-max Plackett–Luce gate | logistic top-K expected probability fitted to the **same** gate mechanism by vectorized Gumbel Monte Carlo | §3 |
| 3C | seat-share denominator unreported | applicants / seats / applicant:seat ratio / realized admission per arm and gate | §4 |
| 4 | 540 design loses Korean calibration | recalibrate with declared procedure + held-out moments | §5 |
| 6 | 540 reproduction is authoritative for its own design | preserve; not deleted, labelled alternative | §1 |
| 7 | reproducibility | manifest, commands, env, hashes, seeds, single-command rerun | §7, §8 |

Not in scope here (separate lanes): GPU ABC/estimator repairs (§5 of the review) and Paper A's replication
package. Paper B's tables are rewritten only after these results land.

---

## 1. Canonical specification decision

### Decision

**Canonical model = the 420-generation parameterisation, ported onto the current patched
`Engine(modules, **params)` / `E.R` engine (HEAD `1c3417c`), with the G9 and expected-probability fixes of §2–§3.**
It is *not* a reproduction of the author-reported 420 table (the 420 runner targets an older engine API and its
code/results are not in the repository); it is a new, fully reproducible simulation under the frozen params below.

### Why this and not the 540 design

- The 420 design is the **only generation that met the Korean calibration targets** it was built to hit
  (author-reported: K–12 participation 76.5 ± 0.1 %, Q5−Q1 gap 34.1 ± 0.3 pp, Q5/Q1 spend 3.19 ± 0.02×;
  Paper B README). The 540 design, reproduced bit-for-bit, misses them badly (Q5−Q1 gap 68.36 pp vs 32.1;
  Q5/Q1 spend 18.01× vs 3.4×; elite Q5 46.36 % HK / 36.12 % KR vs 30.0 % / 24.6 % in the paper table).
- The paper's tables (Paper B docx, four charts) match the **420** generation, so restoring it keeps the paper's
  design and the canonical run aligned — the alternative is to regenerate every table from the 540 design, which
  would require recalibrating a design that is further from the benchmarks.
- The 540 run is retained unchanged as an audited artifact (`papers/shadow-education-contest/code/results/`) and as
  the documented alternative specification (below). Nothing about the 540 reproduction is deleted or edited.

### Canonical parameters (frozen; `N=400`, `T=70`, `measure_from=35`)

| parameter | HK | KR | notes |
|---|---|---|---|
| `N`, `T` | 400, 70 | 400, 70 | 420 design; score cohorts `measure_from=35` |
| `y_median`, `y_sigma` | 3.0, 0.65 | 3.0, 0.60 | |
| `urban_share` | 1.0 | 0.85 | |
| `subsist`, `borrow` | 0.15, 0.5 | 0.15, 0.5 | |
| `p_own`, `p_firm` | 99, 99 | 99, 99 | commercial **contest-only** baseline of the 420 design |
| `contest_r` | 1.5 | 1.6 | |
| `contest_alpha` | 1.2 | 1.25 | |
| `contest_price` | 0.12 | 0.11 | unit price of contest effort |
| `contest_x0` | 2.0 | 2.0 | |
| `contest_max_e` | 4.0 | 4.5 | regulatory cap on contest effort |
| `elite_logw` (global) | 0.85 | 1.15 | Grade-12 elite wage premium |
| G6 gate | bar 0.0 | bar 0.0 | |
| G9 gate | bar 0.0 | **contest, share 0.35, fail=track, elite_logw 0.15** | KR only; §2 |
| G12 gate | contest, share 0.23, fail=track | contest, share 0.12, fail=track | vertical-tier elite gate |
| G16 gate | bar 0.0 | bar 0.0 | |
| everything else | engine / module defaults | engine / module defaults | including `fee_public=0`, `budget_per_child` etc. |

Arms (same 18 as the 540 runner, so policies are comparable across designs): Baseline, CF1a (+50 % tax),
CF1b (−50 % effort cap), CF2a/CF2b (Grade-12 seat share), CF3a/CF3b (elite wage premium ΔV −30 %/−50 %),
CF4a (ΔV −50 % + cap −50 %), CF4b (ΔV −50 % + large seats), per jurisdiction.
Seat-share arm targets: HK S=0.28 / 0.50; KR S₁₂=0.16 / 0.40.

### Documented alternative (not canonical)

**540 design** (`N=300`, `T=46`, `y_median` 2.2/2.0, `subsist` 0.35, `borrow` 0.25, `contest_alpha` 0.25,
`contest_price` 0.16, `contest_max_e` 6.0, `elite_logw` 0.50/0.60, bar gates 2/4/10, general tutoring prices
default) — reproducible bit-for-bit at `1c3417c`/`68da16e`+`contest_gate.patch`; **fails the Korean calibration
targets**, so it is retained as a documented alternative only (a robustness/portability check, not a paper table).

---

## 2. Grade-9 phantom prize: design and variants

### Defect

`core.py` sets `k['elite']` only at `m_ == self.nlev − 2` (the Grade-12 gate). The KR Grade-9 contest
(`kind='contest'`, `share=0.35`, `fail='track'`, `elite_logw=0.15`, `set_voc=False`) awards nothing: winners and
losers follow the identical path, and contest spending on it is priced from a premium that is never paid.

### Fix: explicit, persistent G9 placement (`elite9`)

- A new per-child boolean `elite9` is set for winners of **any non-terminal `fail='track'` contest gate**
  (`m_ < nlev − 2`; in this model that is the KR Grade-9 gate only — the HK Grade-12 gate is terminal and keeps
  `elite`). The flag is persistent for the rest of the child's life.
- Two **realized** consequences, both scaled by a single parameter `g9_consequence ∈ [0,1]`:
  1. **School quality**: G9 placements add `g9_learn_boost` grade-equivalents of learning per upper-secondary year
     (`9 ≤ g < 12`) — placement into a better upper-secondary school raises learning productivity.
  2. **Grade-12 contest standing**: G9 placements multiply the child's effective Grade-12 contest input by
     `(1 + g9_contest_boost)` — the selective-high-school advantage in the CSAT race.
  3. Optional direct log-wage channel `g9_elite_logw` (default **0** in the canonical spec; available for
     sensitivity). We deliberately do *not* double-count a wage premium in the canonical spec; the placement
     premium is realized through schooling and the Grade-12 gate.
- The household's **anticipated** value of a G9 win stays the gate's existing reduced-form `elite_logw` (0.15)
  in `values()`. This is a belief, not the realized object; §2.3 validates the realized return so the gap between
  anticipated and realized premium is measured and reported rather than assumed away.
- Parameter values in the canonical spec (documented assumptions, not calibrated to a moment):
  `g9_consequence = 1.0`, `g9_learn_boost = 0.20` grade-equivalents/year (~0.6 total, a moderate
  effective-school/peer-effect size), `g9_contest_boost = 0.35` (35 % effective-input advantage, material but not
  dominant relative to the Grade-12 prize), `g9_elite_logw = 0.0`.
- Sensitivity to these values is reported through the variants below; no calibration to the G9 channels is done
  (they are structural assumptions, and tuning them to Korean moments would confound them with §5).

### Variants run (KR only, all 9 policy arms, same 30 seeds)

| variant | definition | purpose |
|---|---|---|
| **V1 canonical** | G9 contest + placement consequences on | headline results |
| **V2 G9 removed** | Grade-9 gate replaced by a pass-through bar gate (`bar=0.0`, `fail='track'`); no G9 contest at all | bounds the role of the G9 tournament |
| **V3 consequence off (legacy)** | G9 contest present, `g9_consequence=0` (i.e. the reviewed bug, reproduced on purpose) | quantifies the phantom prize: prep spend with zero realized return |

HK has no G9 gate, so HK arms are identical across variants; we run HK once.

### Validation to report

1. Realized return of a G9 placement (all SIMULATION, descriptive): Grade-12 elite admission rate by
   `elite9`; mean grade-equivalents of learning at exit by `elite9`; mean log income at exit by `elite9`
   (no causal claim — selection is endogenous by construction).
2. G9 contest spending and participation under V1 vs V3 (does the phantom prize inflate spending in V3?).
3. All V1/V2/V3 policy-arm results, including the CF4 criterion.

---

## 3. Expected vs realized admission probabilities

### Defect

`contest_prep` (household effort choice) prices the contest with `P = 1 − exp(−λ x^r)` where λ is
calibrated to match aggregate seats; the gate admits by Gumbel-max Plackett–Luce ranking of
`r·log(x_eff) + Gumbel`. Individual incentive gradients (∂P/∂x) therefore do not match the mechanism, and the
headline "expected admission" is not the expected value of the realized gate.

### Fix: expected top-K admission probability from the same mechanism

- The gate's own mechanism is the Gumbel-max Plackett–Luce ranking with weights `w_i = x_eff,i^r`. The exact
  probability that candidate `i` is in the top `K` (seats) has no simple closed form, so it is estimated by a
  **vectorized Monte Carlo of that same mechanism**: 256 independent Gumbel draws of the candidate field per gate
  year, giving `p_mc,i = P(admit)` for every candidate (cost is `O(M·n log n)` per gate year, negligible).
- The estimated curve is summarised by a logistic in log effective input,
  `P(x) = σ(β · (log x − c_K))`, fitted by weighted least squares of the empirical logit on `log x_eff`
  (`M = 256` draws, weights `p(1−p)`), and **re-centred by market clearing** each year so that
  `mean_i P(x_eff,i) = min(seats / n_candidates, 0.99)`. `β` and `c_K` are stored per gate and used by both
  `values()` (household continuation values) and `contest_prep` (effort choice). This replaces
  `1 − exp(−λ x^r)` everywhere: **one functional form, estimated from the realized mechanism, used for
  expectations and incentives.**
- A dedicated RNG stream (`seed + 1 000 003`) drives the fitting draws so that seeds stay matched across arms and
  the main simulation stream is not perturbed; the fitting is deterministic given the seed.
- Fallbacks (documented, not silent): if the weighted fit is degenerate (slope outside `[0.1, 5.0]`), `β=1` is used
  and the year is flagged in the calibration diagnostics.

### Validation to report (pooled over arms/seeds, per jurisdiction and gate)

- Calibration table: **realized admission rate vs mean expected probability** in each decile of expected
  probability (10 bins) and in each quintile of contest effort (5 bins), with counts.
- Brier score of expected probability vs a seat-share benchmark `p = seats/applicants` (flat), to show whether the
  aligned probability beats the aggregate-only approximation.
- Admission-vs-effort gradient: realized admission by effort quintile; expected gradient from the same bins.
- These diagnostics are recorded in `core.py` during every gate resolution (before the realized draw), so they are
  produced by the exact runs that generate the results — not by a separate illustrative simulation.

---

## 4. Seat denominator reporting

For every arm and contest gate, record and report:

- **applicants** = candidates at the gate (children sitting it that year, after `academic_only`/track filters;
  summed over gate years in the scored window);
- **seats** = `round(share · N)` (the model's fixed cohort-share rule; stated explicitly, not applicants);
- **applicant:seat ratio** = applicants / seats;
- **realized admission rate** = admitted / applicants.

Reported per arm in the results JSON and RUN_REPORT, alongside the share-of-cohort rule so the denominator is never
ambiguous.

---

## 5. Recalibration to the Korean benchmarks

### Targets

| moment | target | role |
|---|---|---|
| KR K–12 tutoring participation | 76.5 % (published band 75.7–78.5 %) | **training** moment 1 |
| KR Q5−Q1 tutoring participation gap | 32.1 pp | **training** moment 2 |
| KR Q5/Q1 tutoring spend ratio | 3.4× | **held-out** moment |
| HK Grade-9 tutoring participation | 53.8 % | **held-out** moment |
| HK Grade-12 tutoring participation | 71.8 % | **held-out** moment |

### Declared procedure (executed after this plan is committed)

1. **Untuned port first.** Run the frozen canonical parameters (§1) with the G9 and probability fixes, on
   **calibration seeds 0–9** for the KR baseline. If both training moments are inside tolerance
   (participation in the published band; gap within ±3.0 pp of 32.1 pp), **keep the untuned port** — parsimony
   and fidelity to the 420 generation take precedence over chasing moments. This is the expected outcome given
   the 420 generation's reported calibration.
2. **If out of tolerance**, search the **pre-declared** grid (and nothing else):
   `contest_price` multiplier ∈ {0.85, 1.00, 1.15} × `contest_alpha` multiplier ∈ {0.90, 1.00, 1.10}
   (9 configurations, KR baseline only, 10 calibration seeds), scored by
   `S = ((part−76.5)/2.8)² + ((gap−32.1)/3.0)²`; choose the minimum-S configuration, ties broken toward the
   untuned port. The 420 values (multipliers 1.00) are the preferred default.
3. **Held-out evaluation.** The chosen configuration is then run on **held-out seeds 10–29** for all arms.
   Held-out moments (KR spend ratio, HK grade-9/12 participation) are computed from those held-out runs only and
   are **not** used for selection or tuning. Held-out tolerance: spend ratio within 3.4 ± 0.5×; HK participation
   within ±5 pp of 53.8 % / 71.8 % (declared as descriptive bands, since the HK series are not the paper's primary
   calibration claim).
4. **Record the outcome either way**, including a failure to hit a moment (commit the null, do not tune it away).

Calibration runs use the same seeds 0–9 that later appear in the full 30-seed run (seed matching across arms is
preserved); the held-out *moment* discipline is about which moments are used to choose parameters, and is stated
explicitly rather than pretending the seeds are independent.

---

## 6. Rerun arm list and uncertainty

- **V1 canonical:** 18 arms (HK 9 + KR 9) × 30 matched seeds = **540 runs**.
- **V2 (G9 removed, KR only):** 9 arms × 30 = **270 runs**.
- **V3 (consequence off / legacy, KR only):** 9 arms × 30 = **270 runs**.
- Total **1 080 runs**, one `Engine` per (arm, seed), identical seed list 0–29 for every arm and variant
  (matched seeds).
- **Uncertainty:** report per-arm mean, seed-level SD, 95 % CI (`mean ± 1.96·SD/√n` over 30 seeds), and
  **paired** arm−baseline deltas computed seed-by-seed (same seed ⇒ same cohorts), with CI from the paired SD.
- **CF4 criterion (fixed in advance, unchanged from the 540 reproduction):** an arm is Win-Win iff
  `total_spend_index < 80` **and** elite Q5 share < baseline elite Q5 share, in **both** HK and KR. Report CF4a and
  CF4b against it in both variants; **preserve the failure** — no parameter or criterion changes to rescue it.
  Also report the Q5−Q1 participation-gap dimension separately so the equity metric in use is unambiguous.
- Outcomes per arm: total spend index (baseline = 100), K–12 tutoring participation, Grade-12 elite share,
  elite Q5 share, Q5−Q1 participation gap, Q5/Q1 spend ratio, contest effort mean, and the §4 seat accounting.
- All arms labelled SIMULATION; no causal interpretation.

---

## 7. Compute protocol (box)

- Host: `connect.nmb2.seetacloud.com:36934` (80 cores, RTX 3080 Ti), work dir **`/root/work/modelrev`** (separate
  from the GPU lane's `/root/work/gpu`; not touched).
- **CPU cap:** `nice -n 10`, `max_workers = min(56, N_WORKERS)` (≤ 70 % of 80 cores), leaving ≥ 30 % free for the
  paper-fix lanes. No watchers, no reboot/power actions (operator-only).
- Package = worktree subset (`engine/`, the new runner, this plan) as a `tar.gz`, `scp` to the box, hash-checked.
  `scipy` installed into `/root/miniconda3` (numpy 1.24.1 present; `scipy` missing initially).
- Results JSONs pulled back to
  `research/records/2026-11-25-model-revision/results/` and committed.

---

## 8. Deliverables and status discipline

| artifact | state at commit |
|---|---|
| `REVISION_PLAN.md` | this file, committed **before** final calibration/rerun |
| `engine/eduengine/core.py`, `engine/eduengine/modules/tutoring.py` | G9 placement, aligned expected probability, seat/calibration instrumentation |
| `code/run_hk_korea_canonical.py` (under the records dir) | canonical runner: 18 arms × V1/V2/V3, 30 seeds, seat accounting, expected/realized diagnostics, `N_WORKERS` cap |
| `results/*.json` | calibration sweep, held-out, V1/V2/V3 arm results, seed-level rows |
| `RUN_REPORT.md` | canonical spec, every review item with achieved numbers, CF4 failure retained, box/CPU facts |
| `MANIFEST.sha256` | hashes of code, inputs, results |

Rule: if a fix cannot be validated in time, commit it as **partial/failed with a clear status** — never fabricate.
Additive commits only; branch pushed to `origin research/model-revision-2026-11-25`; `main` untouched.

---

## Amendment 1 — calibration grid widened (committed BEFORE the formal sweep)

**Why.** A single-seed (seed 0) port check of the frozen canonical parameters on the current patched engine (with
the §2–§3 fixes) put the untuned port outside tolerance on **both training moments**:

| port check (seed 0, KR baseline) | participation | Q5−Q1 gap | Q5/Q1 spend |
|---|---|---|---|
| exact 420 port (contest-only, `p_own=p_firm=99`) | 66.24 % | 80.87 pp | 5.35× |
| target | 76.5 % | 32.1 pp | 3.4× (held out) |

So the "keep the untuned port" branch of §5.1 does not apply and a search is required. The pilot also showed that
the declared 3×3 price/alpha grid of §5.2 is too narrow in the relevant direction (participation is almost
insensitive to `contest_alpha`; it responds mainly to the price and through the contest stakes), so the grid is
widened now, **before** the formal sweep, and the whole grid is reported.

**Declared formal grid (executed after this amendment):**

- `contest_price` multiplier ∈ {0.25, 0.5, 0.75, 1.0, 1.5, 2.0}
- `contest_alpha` multiplier ∈ {0.85, 1.0, 1.15}
- 18 configurations, KR baseline under V1, calibration seeds **0–9**, workers ≤ 56.
- Score: `S = ((part−76.5)/2.8)² + ((gap−32.1)/3.0)²`; choose the minimum. The untuned port (×1.0, ×1.0) is kept
  only if it is inside both tolerances (participation 75.7–78.5 %, gap 32.1 ± 3.0 pp).
- The best configuration's multipliers are applied to **both** jurisdictions' `contest_price`/`contest_alpha`
  (the design treats them as the same contest technology; jurisdiction differences are otherwise already in the
  frozen spec).
- Held-out discipline unchanged: selection uses only the two training moments on seeds 0–9; the KR spend ratio and
  the HK grade-9/12 participation moments are computed on seeds 10–29 of the final run and never used for selection.
- If the minimum-S configuration still misses a training moment, that miss is **reported as achieved, not tuned
  away** (the frontier of the model's achievable (participation, gap) combinations is reported from the grid).

**Documented alternative considered, not canonical:** enabling general commercial tutoring (engine-default
`p_own=0.04`, `p_firm=0.06`) alongside the 420 contest parameters gives, on seed 0, participation 80.3 %,
gap 53.9 pp, ratio 4.81×. It is reported in the RUN_REPORT as a sensitivity for the 420 generation's
contest-only assumption, but the canonical model keeps the 420 generation's explicit `p_own=p_firm=99`
(contest-only) because that is the generation whose calibration record the paper cites.

**Also frozen with this amendment:** the Korean Grade-9 gate of the canonical spec keeps the 420 config
(`contest, share 0.35, fail='track', elite_logw 0.35`, `set_voc` default = True, i.e. losers are tracked to the
vocational track). V1 adds the winners' persistent `elite9` placement consequences on top; V3 turns the winners'
consequences off **and** sets `set_voc=False`, so V3 has no lasting consequence for winner or loser — the
reviewed phantom-prize configuration — while keeping the same anticipated premium (0.35) that prices G9 prep.

---

## Amendment 2 — calibration outcome recorded, canonical arms decision, box CPU finding

Committed **after** the formal calibration sweep (results: `results/calibration_sweep.json`, 18 configs ×
10 calibration seeds = 180 runs) and **before** the policy-arm rerun.

### Calibration outcome: FAILED on the training moments (reported as achieved, not tuned away)

| realisation | participation | Q5−Q1 gap | Q5/Q1 spend | S |
|---|---|---|---|---|
| untuned 420 port (`price ×1.00, alpha ×1.00`) | 66.27 ± 0.24 % | 80.77 ± 0.21 pp | 5.32 ± 0.06× | 276.58 |
| minimum-S grid point (`price ×0.25, alpha ×1.15`) | 91.63 ± 0.27 % | 37.11 ± 1.17 pp | 1.59 ± 0.03× | 31.98 |
| **target** | **76.5 %** (75.7–78.5) | **32.1 pp** (±3.0) | 3.4× (held out) | — |

No grid point reaches both training moments: the model's achievable (participation, gap) frontier jumps from
about (91.6 %, 37.1 pp) to (80.5 %, 65.0 pp) between `price ×0.25` and `price ×0.50`, and higher prices only widen
the gap. The held-out spend ratio at the best-fit point (1.59×) is also far from 3.4×. **The 420-generation
calibration record is therefore not reproducible on the current patched engine with the declared knobs**; the
full grid is in the results JSON and the frontier is reported in RUN_REPORT. The general-tutoring-on sensitivity
(amendment 1) is also outside both tolerances (participation 80.3 %, gap 53.9 pp on the untuned port).

### Decision for the policy-arm rerun (frozen now)

- **Canonical policy arms are run on the frozen 420 parameter values (`price ×1.0, alpha ×1.0`)** — i.e. the
  canonical specification of §1 and the task's recommended port — **not** on the minimum-S grid point. Rationale:
  the minimum-S point is still far outside both training tolerances and would silently replace the 420
  parameterisation the paper's design rests on; using it would be tuning to a miss. The calibration result is
  reported as a failure, and the minimum-S realisation is reported as an alternative calibration outcome (its
  baseline moments are in the calibration JSON; it is not used for the 18 policy arms).
- Policy arms therefore document the *behaviour of the canonical 420-generation model under the G9/probability
  fixes*, with the honest caveat that its Korean calibration on this engine does not match the published
  benchmarks.

### Box CPU finding and worker cap (deviation from the 56-worker instruction, with evidence)

`nproc` reports 80, but the container cgroup quota is **10 CPUs** (`/sys/fs/cgroup/cpu.max = 1000000 100000`,
period 100000 µs). Empirically: the 180-run calibration at 56 workers took **102 s**; a 16-task benchmark took
**6.7 s at 8 workers vs 6.1 s at 16 workers** (no gain beyond ~10). We therefore run the policy rerun with
**8 workers, `nice -n 10`** (≤ 70 % of the effective 10-core quota, and still ≤ the instructed 56 cap), so the
other lanes keep CPU. This is slower than the instructed configuration but faster *and* less disruptive than 56
workers on a 10-CPU quota; recorded here rather than silently exceeding the effective quota.
