# PRE-DECLARATIONS — Cluster B toy battery (experiments #4, #5, #6)

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.**

Written before the run, 2026-11-20 (Asia/Shanghai), by the agent executing the Cluster B
brief. Spec source: `extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md`,
Cluster B (experiments #4–#6); base model `model.py` + `experiments.py` from
`codex-massification-5eec11470690`. Phase status: **CLOSED** — nothing here reopens it.

This file fixes the model rules, the parameter vector, the arm list, the estimands, the
thresholds (with numeric margins), and the falsifiers. It is hashed into
`RUN_MANIFEST.json` at run time (`predeclarations.sha256_16`). Thresholds may not be
altered after seeing `RESULTS.csv`; any later change must be a dated amendment that
keeps the original text below.

## 0. Protocol (all three experiments)

- Python 3.10, **standard library only** (numpy is available but not used). No network, no
  writes outside `extensions_archive/toys_2026-11-20/cluster_B/`.
- Fixed seeds: `seed = 20261120 + rep`, `rep = 0 … 499` → **500 seeds per cell**
  (protocol floor: ≥100; ≥200 where cheap).
- **Paired counterfactuals:** inside a seed, every arm consumes the same latent draw
  (base skill, opportunity cost, lottery permutation; exp5/exp6 add the fixed group /
  credential permutation drawn independently of the arm). Matched starting conditions.
- **One-factor shocks:** only the named arm factor varies (mechanism × visibility;
  treatment × job regime; visibility × gate). Everything else is held at the same
  stipulated value in every arm.
- Metrics are cell means over seeds; paired per-seed differences and their sign-consistency
  are reported as **diagnostics, not thresholds**.
- **All cells are reported, including failures.** `RESULTS.csv` has the fixed schema
  `experiment,arm,seed,metric,value`; line 1 is the mandatory label as a `#` comment.
  Undefined values (e.g. mean skill of an empty rejected set) are written empty.
- Verdict rule: a threshold is **PASS** only if every leg holds; otherwise **NOT MET**.
  A falsifier is **FALSIFIER TRIGGERED** only if its stated condition holds; otherwise
  "falsifier not triggered". Cells are never dropped, and no cell is re-labelled after
  the run.

## 1. Experiment 4 — visibility × mechanism (HC vs signalling)

**Model (stipulated, extends `model.py`).** A one-cohort admissions market: 100 people
with budgets {1.5, 4.0}, base skill U[0,1), opportunity cost U[0,3.5), a common lottery;
30 public seats at fee 1.0; private overflow at tuition 2.0, capacity 30, seat cost 1.0,
fixed cost 12.0 with break-even `qty·(2.0−1.0) ≥ 12`; hiring fills 40 jobs.

- `human_capital`: each graduate gains **+1.0 true skill**; the gross degree premium is
  **4.0 at every v** (return to real skill).
- `signaling`: graduates gain **no skill**; the gross premium is **4.0·(1−v)** (the
  signal's value shrinks with visibility, to zero at v=1).
- Employer score: `v·true_skill + (1−v)·credential`; hires are the top 40 by score, ties by
  lottery order (same stable sort as `model.py`).
- Arms (6): mechanism ∈ {human_capital, signaling} × v ∈ {0, 0.5, 1}.

**Estimands per cell/seed:** applications; admissions; graduate hires; **output among
hires** on two declared metrics — `output_true_hires` = mean true skill of hires (real
productivity) and `output_valued_hires` = mean employer-assessed score of hires;
**skill of rejected applicants** (`rejected_skill`, mean true skill of applicants not
hired; empty if none) and `rejected_count`.

**Thresholds (pre-declared).**

- **T4.1 (primary, true output).** HC `output_true_hires` rises from v=0 to v=1 by
  **≥ +0.05** and is monotone non-decreasing within a **0.01** tolerance
  (v0.5 ≥ v0 − 0.01; v1 ≥ v0.5 − 0.01). Signalling `output_true_hires` **falls** from
  v=0 to v=1 by **≥ 0.05** and is monotone non-increasing within 0.01.
- **T4.2 (secondary, employer-valued output).** Same rise/fall pattern on
  `output_valued_hires`, same margins.
- **T4.3 (rejected-skill composition).** At each v ∈ {0.5, 1}: the two mechanisms' rejected
  sets differ by **≥ 10 applicants**, or their `rejected_skill` differs by **≥ 0.10**;
  and `graduate_hires` differs by **≥ 10**. At v=0 the two mechanisms must be identical
  in applications/admissions/rejected count (pairing diagnostic; at v=0 they are the same
  market by stipulation).
- **Falsifier F4.** The two mechanisms' signatures **coincide at all v**: at every
  v ∈ {0, 0.5, 1}, |Δoutput_true| < 0.02, |Δoutput_valued| < 0.02, rejected counts within
  0.5, and graduate hires within 0.5. If that holds, the toy provides no discriminator.

## 2. Experiment 5 — queue vs human capital under fixed jobs

**Model (stipulated).** Population 100. A **fixed older-diploma group** = indices 0–19
(never re-drawn). The policy upgrades the **fixed** young set T = indices 20–39 (identical
latent people in every arm); the other 60 young are indices 40–99. Job count is exogenous
to outcomes: fixed regime **J = J0 ~ Uniform{35,…,40}**, one draw per seed shared by both
fixed arms; responsive regime **J = 100** (maximum responsiveness: the job pool absorbs the
entire queue, every applicant hired).

- `skill_upgrade`: T gets **+1.0 true skill**, nothing else; hiring by true skill descending.
- `rank_upgrade`: T gets **queue priority only, no skill change**. Hiring order = T (lottery
  order), then the other 60 young by skill, then the 20 older-diploma holders by skill. This
  is the stipulated **credential-inflation queue**: the new credential outranks the old
  diploma, so the fixed older-diploma group is ranked last. *This ranking rule is a
  stipulation, not a finding; it is what allows "rank lowers older-group hires" to be
  possible at all.*
- `reference`: no treatment; hiring by true skill.
- Arms (4 + 2 reference cells): {skill_upgrade, rank_upgrade} × {fixed_jobs, responsive_jobs},
  plus reference/no-treatment in both job regimes (paired reference, not counted among the
  four mandated arms).

**Estimands per cell/seed:** hires of the fixed older-diploma group; output among hires
(mean true skill); total hires; treated-group hires; population mean skill (decomposition
diagnostic).

**Thresholds (pre-declared).**

- **T5.1.** Rank/fixed older-group hires ≤ reference/fixed − **1.0** *and*
  ≤ skill/fixed − **1.0**.
- **T5.2.** Rank/fixed output among hires ≤ reference/fixed − **0.05**.
- **T5.3.** Skill/fixed output among hires ≥ reference/fixed + **0.05**.
- **T5.4 (council wording, literal).** The fixed-jobs output separation **disappears** under
  responsive jobs: |output(rank,responsive) − output(skill,responsive)| ≤ **0.05**.
- **D5.5 (diagnostic).** Older-group hire separation disappears under responsive jobs:
  |older(rank,responsive) − older(skill,responsive)| ≤ **1.0**.
- **D5.6 (diagnostic).** The *allocation-induced* output gap under responsive jobs
  (= total responsive gap − population-mean skill gap, which is exactly the stipulated
  +1.0 on 20 people) is ≤ 0.05 in absolute value. This decomposition is declared now so
  that a literal T5.4 failure can be described without post-hoc metric shopping.
- Falsifier: **no separation** — if rank and skill arms differ by < 0.02 in output and by
  < 1 hire in older-group hires under fixed jobs, the queue-vs-skill distinction has no
  bite in the toy.

## 3. Experiment 6 — eligibility repeal vs blind ranking

**Model (stipulated; a staged screening toy, explicitly not an equilibrium vacancy test).**
100 applicants, **35 offers**. Credential status is stipulated and **independent of true
skill** (a pure signal with no productivity content — a stipulation, not a claim).
Main credential share **45 credentialed / 55 uncredentialed**; pre-declared sensitivity
**25 / 75** (credentialed supply below the offer count, so the gate can leave vacancies).

- **Stage 1 — gate.** Retained: only credentialed applicants are eligible (uncredentialed
  applications screened out before ranking). Repealed: all 100 enter the ranking.
- **Stage 2 — ranking.** Credential *visible*: credentialed ranked first, then by true
  skill. *Blind*: all eligible ranked by true skill only. Ties by a common lottery order.
- Arms (2×2 × 2 credential-share regimes = 8): {visible, blind} × {gate retained, repealed},
  in the main (c=45) and sensitivity (c=25) regimes.

**Estimands per cell/seed:** offer rate among uncredentialed applicants; uncredentialed and
credentialed offer counts; total offers; vacancies; mean true skill of offerees.

**Thresholds (pre-declared).** "Declared high level" = uncredentialed offer rate ≥ **0.25**;
"low level" = ≤ **0.05**.

- **T6.1.** Gate repeal **alone** (visible credential, gate repealed) raises the
  uncredentialed offer rate by **≥ 0.15** over the retained level *and* reaches the high
  level (≥ 0.25).
- **T6.2.** Blind ranking **alone** (gate retained) leaves the rate at the low level (≤ 0.05).
- **T6.3.** Both levers together (blind + repealed) reach the high level (≥ 0.25).
- **T6.4.** Repeal is a *sufficient* lever: rate(visible,repealed) ≥ **0.75 ×**
  rate(blind,repealed).
- **Falsifier F6.** No effect of either lever: all four main uncredentialed offer rates equal
  within **0.01** → no credential-signalling channel in the toy.

## 4. Imposed parameter vector (recorded, not estimated)

| Parameter | Value | Source |
|---|---|---|
| population / jobs / public seats | 100 / 40 / 30 | `model.py` |
| budgets | 1.5 and 4.0, alternating, unshuffled | `model.py` |
| public fee / private tuition | 1.0 / 2.0 | `model.py` |
| private capacity / seat cost / fixed cost | 30 / 1.0 / 12.0 | `model.py` |
| break-even rule | `qty·(tuition − seat cost) ≥ fixed cost` | `model.py` |
| base skill / opportunity cost | U[0,1) / U[0,3.5) | `model.py` |
| exp4 HC skill increment | +1.0 per graduate | stipulation (spec #4) |
| exp4 signalling premium | 4.0·(1−v); HC premium 4.0 | stipulation (spec #4) |
| exp4 employer score | `v·skill + (1−v)·credential` | `model.py` |
| exp5 older group / treated set | indices 0–19 / 20–39 | stipulation (spec #5) |
| exp5 fixed jobs J0 | Uniform{35,…,40} | stipulation (spec #5: "35–40") |
| exp5 responsive jobs | J = 100 (full absorption) | stipulation |
| exp6 offers | 35 | stipulation |
| exp6 credential shares | 45/55 main; 25/75 sensitivity | stipulation |
| seeds per cell | 500 (`20261120 + rep`) | protocol |

## 5. What this battery can and cannot show

It can show whether, **under these stipulated rules**, visibility separates HC from
signalling signatures, whether rank vs skill allocation separates under fixed jobs and
whether responsiveness removes the separation, and whether gate repeal or credential
blindness (or only both) moves uncredentialed offers. It cannot test any historical claim,
calibrate a parameter, or reopen the closed phase. A threshold that passes is a property of
the stipulated rules, not evidence about the world; a threshold that fails is a statement
about this toy's stipulations, not about the world either.
