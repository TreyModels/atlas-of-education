# REPRODUCTION MATRIX — Massification and Its Mechanisms

Audited 2026-11-20 by `repo-auditor`. **Nothing here is a reproduction that did not execute.**
`reported` = the October 2026 manuscript (`paper/Massification_and_Its_Mechanisms.md`) and/or the
stored `results/` file it matches. `fresh` = a run executed by this audit, with its command in
`RUN_LOG.md` and its output in `runs/`.

**Verdict vocabulary**
- **Reproduced** — fresh level agrees with reported to the reported precision at the audit's reps.
- **Reproduced at small reps** — direction and size agree, but an edge cell or slope is seed/reps-sensitive.
- **Not run** — no execution; listed with its cost.
- **Failed / partial** — something ran but did not complete or did not produce a comparable number.

**What differs globally:** reported tables use `--reps 4` (floor test, gates), `6` paired (grad. supply),
and `30` (actors, N=3000). Fresh runs used `--reps 2`, N=6000 for massabm, `--reps 2` N=3000 for triad.
Seeds are those hard-coded in the experiment modules; identical code path, same seeds, fewer reps.
Environment differs (Python 3.11.17 / numpy 2.4.6 / scipy 1.17.1 here vs 3.10.2 / 2.2.6 / 1.15.3 in
the stored round-2 notes). Machine: 8-core macOS under shared load (other agents running).

---

## Scoreboard

| # | Result | Manuscript location | Fresh run executed | Verdict |
|---|---|---|---|---|
| 1 | Six-arm floor/race table (30 level cells + 6 slopes) | §"Floor and race, separated", table after ¶128; Appendix "Floor vs race" | `run.py floor_test --reps 2 --N 6000 --workers 2` (204 s) | **Reproduced** (all 30 level cells ≤0.014; 1 of 6 slopes off by 0.07) |
| 2 | Graduate-supply shock, surplus vs competitive | §"A graduate-supply shock", table ¶155–164 | `run.py grad_supply --reps 2 --N 6000 --workers 2` (54 s) | **Reproduced** (all 20 shock changes ≤0.0063) |
| 3 | Actors' contributions / knockouts | §"Three actors", ¶168; Appendix "Actors' contributions" | `run_triad.py necessity --reps 2 --N 3000 --workers 2` (32 s) | **Reproduced at small reps** (years/tertiary match; "4% without screening" does not) |
| 4 | Gate tutoring shares + bar sweep | §"Gates", ¶176; Appendix "Gate clustering" | `run.py gates --reps 2 --N 6000 --workers 2` (143 s) | **Reproduced** (every reported share within 0.01) |
| 5 | Floorworld baseline trajectories + 8-test screen | Repository audit lead, not a manuscript number | baseline script (0.5 s) + `floorworld_mc.py --draws 400` (~80 s) | **Reproduced** (engine runs; pass rates match stored 6,000-draw report) |
| 6 | K-12 reform distribution (Trillanes) | §"Who carries the floor", ¶216; note 14 | `run.py reform_distribution --reps 2 --N 6000` (57 s) | **Reproduced** for the as-built variant (Δaggregate 0.001); the paper's quoted −6.5/−22/−2 numbers are the un-run `dropout_per_stage` variant |
| 7 | H2 investment slope (−0.09) | §"Investment under compression", ¶147; note 6 | not run as a standalone ablation; read off the floor-test baseline arm | **Partially reproduced** (−0.068 vs −0.09) |

---

## 1. Six-arm floor/race table

**Reported** (stored `round8_mechanisms_and_ledger_fix/floor_test/findings.txt`, reproduced verbatim in
the paper table; 4 reps/cell, N=6000, SD≤0.013):

| Arm | diploma | diploma Q1 | formal\|\<dip | formal\|dip | college Q3-5 | slope |
|---|---|---|---|---|---|---|
| ranked, no floor | 0.772 | 0.573 | 0.121 | 0.354 | 0.488 | −0.044 |
| ranked, adaptive floor | 0.770 | 0.569 | 0.119 | 0.225 | 0.542 | −0.064 |
| ranked, fixed floor | 0.772 | 0.572 | 0.117 | 0.354 | 0.492 | −0.048 |
| unranked, no floor (lottery) | 0.731 | 0.538 | 0.436 | 0.450 | 0.180 | +0.151 |
| unranked, adaptive floor | 0.771 | 0.570 | 0.118 | 0.207 | 0.614 | +0.036 |
| unranked, fixed floor | 0.771 | 0.571 | 0.118 | 0.495 | 0.478 | +0.630 |

**Fresh** (`runs/massabm/floor_test/`, 2 reps/cell, N=6000):

| Arm | diploma | diploma Q1 | formal\|\<dip | formal\|dip | college Q3-5 | slope |
|---|---|---|---|---|---|---|
| ranked, no floor | 0.771 | 0.570 | 0.121 | 0.351 | 0.494 | −0.034 |
| ranked, adaptive floor | 0.770 | 0.568 | 0.120 | 0.212 | 0.550 | −0.068 |
| ranked, fixed floor | 0.771 | 0.570 | 0.118 | 0.354 | 0.492 | −0.037 |
| unranked, no floor (lottery) | 0.733 | 0.539 | 0.433 | 0.447 | 0.189 | +0.221 |
| unranked, adaptive floor | 0.771 | 0.569 | 0.116 | 0.214 | 0.614 | +0.027 |
| unranked, fixed floor | 0.771 | 0.570 | 0.117 | 0.495 | 0.473 | +0.650 |

**Delta (fresh − reported), largest absolute per column**
- diploma: ≤0.0022; diploma Q1: ≤0.0032; formal\<dip: ≤0.0028; formal\|dip: ≤0.0136; college Q3-5: ≤0.0093.
- slopes: 5 of 6 within 0.020. The **unranked-lottery slope** is the exception: +0.151 reported vs
  +0.221 fresh (Δ 0.070). A slope needs 6 points (2 reps × 3 demand scales); at 2 reps it is the
  noisiest cell in the table.
**Verdict: reproduced.** The qualitative claims survive exactly: a floor without ranking produces
persistence/exclusion but positive slopes; ranking produces negative slopes; and inside a ranked queue
the adaptive (moving) floor raises better-off college entry (0.488→0.550 fresh; 0.488→0.542 reported)
and cuts diploma holders' formal rate (0.351→0.212 fresh; 0.354→0.225 reported), while a fixed floor
does not.

## 2. Graduate-supply shock

**Reported** (stored round 8; paper table ¶155–164; 6 paired reps):

| World | Shock | Δ degree share | Δ diploma income | Δ degree income | Δ ratio | Δ formal\|dip |
|---|---|---|---|---|---|---|
| Surplus | half price | +0.138 | −0.061 (0.014) | −0.359 | +0.051 | −0.156 (0.018) |
| Surplus | 80% off | +0.216 | −0.042 (0.012) | −0.447 | +0.079 | −0.169 (0.016) |
| Competitive | half price | +0.128 | +0.290 (0.007) | −0.429 | +0.166 | n/a |
| Competitive | 80% off | +0.219 | +0.544 (0.006) | −0.652 | +0.319 | n/a |

**Fresh** (2 paired reps): surplus half +0.141 / −0.059 / −0.364 / +0.053 / −0.151;
surplus 80% +0.216 / −0.040 / −0.453 / +0.081 / −0.165;
competitive half +0.127 / +0.285 / −0.429 / +0.163 / n/a;
competitive 80% +0.221 / +0.545 / −0.657 / +0.318 / n/a.
Baseline levels: surplus diploma income 1.570 (reported 1.573), degree income 2.939 (2.936);
competitive 1.072 (1.074) and 3.091 (3.074).

**Verdict: reproduced.** Every reported change agrees to ≤0.0063; the discriminating opposite signs on
diploma holders' **absolute income** (−0.04/−0.06 surplus vs +0.29/+0.54 competitive) reproduce, as does
the point that the relative ratio rises in both worlds.

## 3. Actors' contributions (three-actor model)

**Reported** (paper ¶168 and appendix: **median of 30 replications**; matches
`round2b_three_actor_model/30_replications/necessity/findings.txt`):

| World | Years | Upper+ | Tertiary+ | Cred. hiring | Contributions (years) |
|---|---|---|---|---|---|
| all three | 11.6 | 0.58 | 0.38 | 0.84 | total +4.29 over all-removed |
| − household | 8.2 | 0.25 | 0.00 | 0.74 | +3.45 |
| − employer | 10.1 | 0.58 | 0.04 | 0.00 | +1.49 |
| − state | 10.4 | 0.52 | 0.21 | 0.85 | +1.19 |

**Fresh** (2 reps, N=3000): 11.50 / 8.16 / 9.96 / 10.43 years; tertiary 0.375 / 0.003 / 0.0004 / 0.216;
contributions **+3.34 / +1.53 / +1.06**; total **+4.16**.
The 8-rep stored run (`round2b_three_actor_model/necessity`, N=3000) independently gives 11.6 / 8.1 /
10.0 / 10.3 and +3.50 / +1.67 / +1.30.

**Deltas vs the 30-rep figures:** years −0.10/−0.04/−0.14/+0.03; contributions −0.11/+0.04/−0.13;
total −0.13. **The one substantive mismatch is employer tertiary completion: 0.04 reported vs 0.0004
fresh** (the 8-rep stored run shows 0.00 as well). The manuscript's "4 percent without credential
screening" is carried by a handful of runs; the fresh 2-rep set has essentially zero.
**Verdict: reproduced at small reps.** Ordering and approximate size reproduce (households largest,
employers follow, state smallest); the 0.04 tertiary cell is fragile and should be reported with its
replication set. Also reproduced in the quick pass: state funds at year 30, households aim at tertiary
at 38, most firms switch at 66 (reported 29/38/65), and lock-in remains absent (late employer removal
leaves the pipeline intact: 11.9 fresh vs 11.8 full).

## 4. Gate tutoring shares

**Reported** (stored `round1_philippine_model/gates/findings.txt`; paper ¶176; 4 reps, 2000–12):
board **0.93**, college **0.35**, elite/apex **0.30**, basic **0.05**; tutoring spend shares
0.15/0.40/0.26/0.20; basic-bar sweep −2.0→+0.5: 0.03, 0.12, 0.32, 0.58, **0.76**, 0.77.

**Fresh** (2 reps): board 0.93, college 0.35, apex 0.30, basic 0.06; spend 0.15/0.40/0.25/0.20;
sweep 0.03, 0.12, 0.31, 0.58, **0.76**, 0.77.
**Verdict: reproduced.** The headline "3 → 76 percent when the basic-diploma bar is raised from −2.0 to
0.0" is exact. The tutoring-ban rerouting numbers also reproduce (total spend 3,322 reported vs 3,316
fresh; apex ban cuts apex spend 1,329→976 reported vs 1,330→980 fresh).

## 5. Floorworld (Atlas engine — repository lead, not a manuscript number)

**Reported** (`01_sources/atlas-main-55732f4/engine/results/floorworld_mc.md`, stored 6,000-draw run):
share of draws passing all eight country tests — S1 10.25%, S2 14.72%, S3 0.03%, S4 0.00%, S5 0.72%.
**Fresh** (400 draws, same seed and priors, worker-capped copy): S1 **10.25%** (41), S2 **14.50%** (58),
S3 **0.00%** (0), S4 **0.00%** (0), S5 **0.50%** (2). Per-test rates track the stored report within
sampling (e.g. S5 T1 100%/100%, T5 100%/100%, T6 55%/54%).
Deterministic baseline path (`runs/floorworld/baseline_paths.csv`, first `rng(23)` draw): all 4 countries
× 5 structures × years 1990/2000/2010/2018/2035; that draw passes 8/8 tests under S1 and S2, 6/8 under
S5, 3/8 S3, 2/8 S4 — consistent with the structure ranking in the MC.
**Verdict: reproduced** (engine executes; stored pattern-screen rates recur). Note: the paper makes no
numeric claim from this engine, so this is a code-health check, not a manuscript reproduction.

## 6. K-12 reform distribution (Trillanes critique)

Reported, **as-built** variant (stored `round1_philippine_model/reform_distribution`, 10 paired reps;
paper ¶216): aggregate basic-diploma completion 0.783 → 0.652 (**−0.132**); quintile effects
Q1 −0.258, Q2 −0.107, Q3 −0.104, Q4 −0.094, Q5 −0.094; rich-poor gap 0.201 → 0.365.
**The paper's quoted sentence** — "about 22 points in the poorest quintile and about 2 in the richest …
from 0.20 to 0.41, aggregate near 6.5 points" — is the **`dropout_per_stage` judgment-call variant**
from the `audit` experiment (stored `round2_robustness/audit`, row `dropout_per_stage`: cycle −0.068,
Q1 −0.231, Q5 −0.026, gap 0.20→0.41), i.e. a *different* run from `reform_distribution`'s default.

**Fresh** (`run.py reform_distribution --reps 2 --N 6000 --workers 2`, 57 s):
reform+cct vs no reform: aggregate 0.783 → 0.652 (**−0.131**);
Q1 −0.254, Q2 −0.107, Q3 −0.108, Q4 −0.096, Q5 −0.089; gap 0.196 → 0.361.
Second variant (no CCT): aggregate 0.763 → 0.631 (−0.132); Q1 −0.245, Q5 −0.098; gap 0.298 → 0.446.
Overseas-professional outcome quartet identical to stored (1.00/0.00/0.00/0.00 vs 0.00/0.00/0.60/0.40).
**Verdict: reproduced** for the as-built variant (aggregate Δ 0.001; Q1 Δ 0.004; gap 0.201→0.196).
The paper's exact −6.5/−22/−2/0.41 numbers come from the `dropout_per_stage` variant, which was **not
run** in this audit (it is one row of the 9-variant `audit` experiment). Direction is the same in both.

## 7. H2 investment slope (partial)

Reported: slope of better-off college entry on degree-holder absolute income = **−0.09** (full model);
−0.05 no employer floor; +0.03 no ranking; +0.23 pure signal; +0.55 competitive market (paper ¶147,
note 6; stored `round1_philippine_model/ablation`, 4 reps/scenario).
Fresh read-off: the floor-test baseline (ranked, adaptive floor) across formal-demand scales 0/1/2 gives
**−0.068**; no-floor arm −0.034; ranked fixed floor −0.037; unranked arms +0.027/+0.221/+0.650.
**Verdict: partially reproduced.** Sign and cross-arm ordering match (surplus/full more negative than
no-floor; unranked positive); the point estimate is 0.02–0.03 short of −0.09 at 2 reps. The standalone
`ablation` experiment (which is where the −0.09 comes from) was **not run** — 25 cells × reps, ~3–5 min
on an idle machine.

---

## Provenance of `public/research/massification/actor-runs.csv` (and `data.json`)

**Finding: same model and knockout design, but NOT the same run as the paper's numbers, and not the file
the paper's table was computed from.**

- `actor-runs.csv` has 8 rows, one per removal combination, with `n=8`; `data.json`'s `triad` block is
  byte-for-byte the same numbers; the web page labels it "mean over 8 runs".
- The paper (¶168, appendix) states **median of 30 replications**, and those values match
  `results/round2b_three_actor_model/30_replications/necessity/findings.txt` (11.6 / 8.2 / 10.1 / 10.4;
  contributions +3.45/+1.49/+1.19), not the public CSV.
- Public-CSV implied contributions (its own `none` row minus each removal): **+3.40 / +1.43 / +1.09**,
  vs +3.45/+1.49/+1.19 in the 30-rep stored run and +3.50/+1.67/+1.30 in the 8-rep stored run.
  So the public file is an **8-seed mean on an unknown seed set**, not the 30-rep median.
- **Status: partially unresolved.** The design (actor knockouts, end-state means) is the same family, and
  the numbers are close, so this is not a contradiction. But no script, seed list or manifest for the
  public file exists in either the local copy or the public checkout, so **exact provenance cannot be
  reconstructed**. Do not cite the public CSV as "the paper's 30-replication result", and do not call the
  two contradictory.

**Related public files:** `parent-runs.csv` (160 rows, peer-pressure grid) and the page's parent tab
**have no generating code anywhere in the delivered material** (not in the public checkout and not in
`01_sources/massification_project/code`). `inequality-runs.csv` / the page's "tilly" block use the
`engine/firms` Tilly arms (`access_exclusion`, `wage_withholding`, `credential_initiation`, …), whose
source (`engine/firms/tilly_experiments.py`) **does** exist in the public checkout but was not executed
here. The public checkout's own `research/ISSUES.md` says the stored massification experiments cannot
be fully inspected from source; this audit confirms that for parents and partially for actors.

## What was NOT attempted (and what it would cost)

| Result | Reason | Cost on idle 8-core box |
|---|---|---|
| K-12 `audit` variants incl. `dropout_per_stage` (paper's quoted −6.5/−22/−2/0.41) | machine load; default variant already reproduced | audit = 9 variants × 5 scales ≈ 10–20 min |
| H2 ablation (all 5 worlds × 5 scales × 4 reps) | machine load | ~5–10 min |
| Actors 30-rep median / lock-in 30 reps | machine load; 2 reps already executed | necessity 30 reps ≈ 4–6 min; with lock-in ≈ 10 min |
| triage: timing, scope, gender, sensitivity, calibrate, macro, policy_payoff, nurse_check, returnees | not headline tables / heavy | policy_payoff+macro ≈ 10–20 min; calibrate 300×4000 is hours |
| atlas `childworld_mc` full 6,000 worlds | only 100-run smoke executed | hours-scale; documented default 6000 worlds |
| atlas `relfloor_countries` documented 24,000 draws | 120-draw smoke executed (thin acceptance) | many hours |
| atlas `firms` China fit / Tilly experiments | ~20–60 min per documented command | not attempted |
| atlas `shadow-abm` SMC recalibration | expensive, and old posteriors are invalid after the observation fix | hours |

## Honest limits of this audit

1. **Small reps.** Two replications per cell are enough for level cells (their SD ≤0.013) but not for
   derived slopes and rare cells (employer tertiary completion). The verdicts above say where.
2. **One environment.** Fresh runs use newer numpy/scipy than the stored runs; exact bit-reproduction
   was not attempted and is not claimed.
3. **Compute contention.** Other agents ran on the same 8-core machine; wall times are inflated and one
   planned run did not finish.
4. **No independent reimplementation.** Every fresh number comes from the same code the stored number came
   from. This audits *executability and reproducibility*, not the models' scientific claims. The paper's
   two models were built by the same hands — this audit cannot fix that.
5. **The manuscript's Philippine empirical claims are not tested here** (nurse response, GER path,
   completion gradient); they are reported as model failures or data claims in the paper and would need
   the data-ledger work, not more model runs.
