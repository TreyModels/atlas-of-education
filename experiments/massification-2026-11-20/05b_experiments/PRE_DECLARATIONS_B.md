# PRE-DECLARATIONS — Batch B (independent adversarial replication, `experiment-runner-2`)

Written BEFORE any Batch-B run. Batch B runs in parallel with runner 1's `05_experiments/` suite.
Nothing here writes into `05_experiments/` or `01_sources/`.

## Standing rules for every B cell

- Python: `/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python`
  (numpy 2.4.6, scipy 1.17.1, pandas 3.1.1, python 3.11.17). `PYTHONDONTWRITEBYTECODE=1`.
- `nice -n 10`; workers = 2; per-run SIGALRM timeout = 300 s (declared in `code/bcommon.py`).
- Seeds are **matched across arms** (same seed in each arm of a comparison); where the model pair
  is broken the break is reported. Seed dispersion = standard deviation **across replications**
  (not a standard error, not parameter uncertainty). Parameter uncertainty is NOT sampled here:
  parameter values are the source defaults, so every interval below is simulation/seed dispersion.
- Every run's OK/failure is logged. Failed or non-converged runs are kept in the log and in the
  manifest; a cell with a failed rep reports the reduced n.
- Any module written in `code/` is a **NEW implementation**. Nothing in Batch B is a reproduction
  of the paper's own experiment scripts unless explicitly stated. The one exception is B1/B2/B3,
  which re-drive existing massabm code: B1 uses runner 1's declared extension `mode='hc_fair_slots'`
  (a NEW mechanism added to a copy of massabm; see `05_experiments/code/new/README_EXTENSION.md`);
  B2/B3 use the unmodified `mode` variants of the stock model. My drivers (`run_B*.py`) are new.
- A cell is claimed only if it was run. No cell is inferred from a table.

## Provenance / prior state

- Runner 1's first E13b pass was `reps=1, N=2000` and therefore **provisional**; by the time I
  predeclared, runner 1 had already upgraded the stored E13b cell to `reps=6, N=5000`
  (`05_experiments/runs/E13b`, wall 282 s, 72/72 ok). I have SEEN that output. B1 below is an
  **independent rerun at a different N (3000)** plus a predeclared precision/plausibility test that
  the stored E13b did not apply. It is a replication, not a blind test; that is stated in the
  results. The comparator cell is the stored E13b, not the original reps=1 pilot.
- Runner 1's E8 (6-arm floor/race) is stored at `reps=4, N=6000`, wall 332 s, 72/72 ok. B2 is an
  independent rerun of the same design (same seeds) and B3 is a predeclared subset analysis of the
  same run set. I have seen the stored E8 slope signs; B2/B3 test precision and identification,
  not the sign's direction in isolation.

---

## B1 — Does the matched-elasticity rival really contradict C3? (precision + plausibility test)

**Question.** Does a competitive CES skill-price world that has a formal/informal margin reproduce
a fall in diploma holders' *absolute* income after a college-cost shock, at any substitution
elasticity sigma in {0.5, 1.0, 2.0}? (If yes, the paper's discriminating claim C3 — "only the
surplus/slot account can make diploma holders lose" — is contradicted.)

**Hypothesis (rival).** Under imperfect substitution, cheaper degrees raise the degree share and
*lower* the degree price; diploma holders become scarcer, so their absolute income rises. Under the
surplus account, graduates take formal slots that diploma holders used to fill, so diploma holders'
absolute income AND formal-employment probability fall.
Predeclared expectation for C3's discriminating margin: **the formal-employment probability is the
clean discriminator; absolute income of diploma holders is not.**

**Estimand (unit = model world, paired seed).** Paired change vs `no shock`, same seed:
(a) diploma holders' absolute basic income (Δdip_income);
(b) diploma holders' formal-employment probability (Δformal|dip);
(c) diploma/degree income ratio (Δratio).

**Arms.** Surplus world `mode='full'` (slots + credential floors + ranked hiring) at one sigma-free
cell; matched rival `mode='hc_fair_slots'` with `fair_sigma ∈ {0.5, 1.0, 2.0}` — CES skill prices
on the SAME formal vacancy path, hiring by expected productivity, no credential floor, no rank.
Shocks: (i) none, (ii) college half-price from 1995, (iii) college 80% off from 1995.

**Controls.** Identical households (`seed=20000+r`), same tuition paths, same formal vacancy path
(`macro_elasticity=0`, so vacancies are exogenous and identical across worlds), no K-12 reform
(`reform_rule='never'`, `t1=2035`), outcome window 2010–2030, cohorts entering 1995–2012, N=3000,
reps r=0..5 (6 paired reps). Batch B adds 2 reps and +1000 N over the original pilot; it uses
N=3000 rather than runner 1's 5000 to fit the shared 8-core/8 GB laptop (declared trade-off).

**Predeclared decision rule (primary).** The contradiction SURVIVES if, at some sigma and for at
least one shock, all three hold:
1. both shocks' Δdip_income < 0 at that sigma (sign-stable across the two shock sizes);
2. |Δdip_income| > 2 × (sd across the 6 paired reps) at that sigma — i.e. the loss is
   distinguishable from zero seed noise, not a point estimate;
3. the rival world at that sigma is not numerically degenerate, declared a priori as **baseline
   diploma/degree income ratio ≥ 0.20** (surplus baseline is ~0.54; a rival whose unskilled income
   is <20% of the skilled wage has no plausible "scarcity of diploma holders" structure and is
   flagged as an implausible CES limit, not counted as a fair rival test).

Otherwise the contradiction does **NOT survive** and is reported as a point-estimate artefact.
Secondary check, stated in advance: C3's surplus-specific mechanism is supported on the
formal-employment margin if Δformal|dip < −2·sd in the surplus world and Δformal|dip > −2·sd at
every rival sigma. `not identified` if surplus Δformal|dip is itself within 2·sd.

**Runs.** 2 world-type cells × (1 or 3 sigma) × 3 shocks × 6 reps = 72 model runs.

---

## B2 — Close the reps gap on the 6-arm floor/race table (4 reps, N=6000)

**Question.** Do the stored October/manuscript 6-arm floor/race cells reproduce at the manuscript's
4 reps, and what is the **unranked-lottery** intensification slope at 4 reps (stored +0.151) versus
the 2-rep pilot (+0.221)?

**Estimand.** Per arm: baseline-scale (formal_growth_scale=1) mean of basic-diploma completion (all,
Q1), formal-employment rate below the diploma vs diploma holders, Q3–Q5 college entry (mean, sd
across reps); and `slope = d(Q3−Q5 college entry)/d(degree holders' absolute income)` across
formal-demand scales {0, 1, 2}. B2 reports the slope two ways: (i) the stored pooled-across-reps
slope (for comparison to the stored number), and (ii) the **per-rep slope** averaged over reps with
its sd (new; separates simulation noise from the pooled number).

**Arms (2×3, exactly the stored design).** ranking {on, off} × eligibility rule {none, adaptive
employer floor, fixed rule-set floor (elite=4, mid=4, routine=3)}.
- ranked, no floor = `mode='no_floor'`; ranked, adaptive floor = `mode='full'`;
  ranked, fixed floor = `mode='full', floor_fixed=FIXED_FLOOR`;
  unranked, no floor (lottery) = `mode='lottery'`; unranked, adaptive floor = `mode='no_rank'`;
  unranked, fixed floor = `mode='no_rank', floor_fixed=FIXED_FLOOR`.

**Controls.** Same as the stored design: identical cohorts/schedules/seeds, no K-12 reform, seeds
19000+r matched across arms and scales; window cohorts entering 1995–2012, labour market 2010–30.
N=6000, reps=4, formal-demand scales {0, 1, 2}, workers=2.

**Predeclared decision rule.** `rank-dependence confirmed` iff, at 4 reps, (i) every ranked arm has
slope < 0, (ii) the unranked-lottery arm has slope > 0, and (iii) the lottery slope exceeds 2× its
per-rep sd in absolute value. `not identified` if per-rep slopes have |mean| < 2·sd in either
group. Report the lottery slope against the two stored numbers explicitly; do not tune the design
to land on +0.151.

**Runs.** 6 arms × 3 scales × 4 reps = 72 model runs.

---

## B3 — Allocation-rule knockout: rank vs employer cutoff vs random-among-eligible

**Question.** Is "intensification" (investing more as degrees pay less) a property of *ranking*, or
does it also appear under a non-rank allocation — i.e. is C3/the race mechanism allocation-specific?

**Estimand.** Same as B2's slope, but the knockout compares four **allocation rules** holding the
household utility/cost specification, cohorts, seeds and labour-demand scales fixed:
1. `rank + employer cutoff` = `mode='full'` (floor then rank by credential signal);
2. `rank only` = `mode='no_floor'` (no cutoff, rank among all);
3. `cutoff + random among eligible` = `mode='no_rank'` (employer floor retained, random draw
   among those above it);
4. `random among all` = `mode='lottery'` (no floor, no rank).
The cutoff arms (1, 3) share the same eligibility rule; the rank arms (1, 2) share the same ranking.
This 2×2 separates the two mechanisms.
**B3 shares one run set with B2** (declared: the same 72 runs, subset analysis). This is not a
second independent replication; it is a predeclared knock-out computed from B2's run set.

**Predeclared decision rule.** "Intensification requires ranking" is **allocation-specific** if
slope > 0 (and > 2·per-rep sd) in ≥2 of the non-rank arms {2, 3, 4}. It is **mechanism-general** if
slope < 0 in ≥2 non-rank arms. `not identified` if, within an arm, the range of degree income
across demand scales is < 0.1 index units (no identifying variation) or per-rep sd ≥ |mean|.
Also reported: mean degree income per demand scale per arm, to show the slope is not being driven
by a degenerate degree-price range.

**Runs.** Shared with B2 (72 runs); no additional runs.

---

## B4 — E12 long-run massification trajectories (10/20/30/40 years), NEW implementation

**Question.** Starting from a plausible stylized world, do 10/20/30/40-year cohort/workforce
trajectories of entry, progression, completion, wages and employment mix **require a supplied
(exogenous) education trend**, or can an endogenous household decision path generate the rise?

**This is a NEW implementation** (`code/e12_traj.py`), not massabm, not triad, not floorworld, not
a reproduction of the paper's E12. It is a 40-year annual cohort-flow model with declared
accounting: annual birth cohort N=1000; states not-enrolled / secondary / college / exited; fixed
secondary-completion and college-progression probabilities; a labour market with exogenous formal
vacancy growth and informal work as outside option; wages by education level with a declared
elasticity of the degree premium to degree share (congestion). Births and workforce turnover are
declared scenario inputs. Every number is labelled input-driven or generated.

**Arms.** (A) **EXO**: college-entry rate follows a supplied upward schedule (input-driven by
construction; the "supplied trend" arm). (B) **ENDO**: college entry is a logit decision on the
expected private return (completion probability × expected degree-vs-diploma wage gap × working
years − household cost) with the same logit noise scale as the model's `tau`; the entry rate is
**generated**, not supplied. Both arms share births, schedules, vacancies, wage rule, seeds.
Variants: workforce turnover 1/40 vs 1/20 per year; births flat vs 1%/yr growth. Seeds 0..4
(matched across arms/variants), stochastic logit draws and turnover draws.

**Outcomes at years 10, 20, 30, 40** (year-by-year series also written): cohort secondary
completion; college entry rate; college completion rate; degree share of the workforce; formal
employment share; formal-employment probability of degree holders; degree/diploma wage ratio; mean
wage index.

**Predeclared decision rule.** `generated` (no supplied trend needed) if ENDO's college-entry rate
rises by at least 50% of EXO's rise over 40 years with no trend in ENDO's inputs, and its
degree-share trajectory has the same sign at every decadal checkpoint. `requires supplied trend`
if ENDO entry is flat or falls while EXO rises, or if the ENDO degree share is below its 10-year
value at year 40. Non-convergence is not applicable (deterministic accounting + explicit
stochastic draws); failed draws are reported. All EXO outcomes are flagged `input-driven` in the
table; all ENDO outcomes `generated`.

**Runs.** 2 arms × 2 turnover × 2 birth settings × 5 seeds = 40 trajectories (each 40 years).

---

## B5 — E16 credential information/recognition

Not predeclared in Batch B. It is the last priority and is run only if B1–B4 finish with time.
If it is not run it is recorded as `not run` and is not claimed.

## Out of scope for Batch B

- No new parameter-uncertainty sampling (no Sobol/LHS): seed dispersion only, per the standards'
  distinction between simulation noise and parameter uncertainty.
- No country-level or causal claim from any simulated cell.
- No floorworld/childworld/atlas cell is claimed (not run here).
- The paper's October `floor_test` stored numbers have unknown provenance; B2 reproduces the
  *design*, and reports direction/precision, not a provenance claim.

---

## Amendments (recorded after the relevant runs; post-hoc, never used to upgrade a verdict)

**Amendment 1 — B4 post-hoc robustness arm (recorded after the primary B4 run).** The primary ENDO arm
showed cobweb instability (entry collapsing toward the 0.02 floor; seed sd up to 0.38 at year 20). A
post-hoc arm `ENDO_SMOOTH` (partial adjustment of take-up, 0.5 per year) was added to test whether the
predeclared "requires supplied trend" verdict survives smoothing. It is labelled POST-HOC in the
findings, CSV and `EXPERIMENTS_B.md`. The primary verdict is still taken from the predeclared EXO-vs-ENDO
rule; the post-hoc arm can only confirm or qualify, not upgrade.

**Amendment 2 — B1 post-replication plausibility diagnostic (recorded after the primary B1 run).** The
predeclared condition (3) was written on the arm mean of the rival's baseline diploma/degree ratio. It
passed the numerically unstable sigma=0.5 cell on the mean (0.234) while 5/6 seeded worlds in that cell
had per-seed baselines 0.022–0.055. A post-hoc diagnostic re-applies condition (3) per replication and
reports the rival's across-seed range (`code/b1_robust.py`, `runs/B1/b1_robustness.csv`). It can only
downgrade the literal verdict. The literal program output is retained in `runs/B1/findings.txt` for
audit; the reported B1 verdict is the robust one (contradiction does not survive as a fair-rival result).

**Amendment 3 — spec drift on the E13b baseline (recorded before running B1).** The stored E13b cell was
already at reps=6/N=5000 when this batch started, not the reps=1/N=2000 pilot named in the brief. B1
uses the stored reps=6/N=5000 as comparator and an independent N=3000 replication; see `ERROR_LOG_B.md`.

**Amendment 4 — B5 (superseded).** Initially recorded as not reached within the batch budget; the
batch finished B1–B4 faster than expected and B5/E16 was then predeclared as Amendment 5 below and run.
This amendment is retained for audit, marked superseded.

---

## B5 — E16 credential information / recognition (predeclared BEFORE running; AMENDMENT 5)

**Question.** How do different credential readers trade off hiring errors, exclusion, wages and
certification demand: domestic detailed reader vs coarse reader vs a skill test vs a formal eligibility
rule, and how do signal accuracy, screening cost, network access and cross-border recognition move
those trade-offs independently?

**This is a NEW implementation** (`code/e16_readers.py`), not massabm, not triad, not floorworld, not
the paper's E16 (which was not run). It is a one-period static screening/hiring model with declared
accounting: N=2000 applicants, M=300 formal vacancies; latent ability a~N(0,1), SES s~N(0,1), credential
tier c∈{0,1,2,3} (tier assigned from a declared distribution mildly correlated with SES, 2 years per
tier); true productivity p = a + omega·(2c), omega=0.25 (schooling has a real productivity component, so
a credential reader is not reading a pure signal and a skill test is not optimal by construction).
Applicants who are not hired work informally at 1.0; hired formal wage 2.2. Declared reader rules
(signal used to fill the M slots by rank, with ties broken by SES-linked referral share):
1. domestic detailed: signal = a + 0.2·(2c) + noise(σ_acc);
2. coarse domestic: signal = (2c) + noise(σ_acc) (no within-tier ability);
3. skill test: signal = a + noise(σ_acc) (no credential/schooling information);
4. formal eligibility rule: eligible iff c ≥ 2, then random among eligible (no ability information);
5. foreign reader: reads the origin credential at recognised fraction ρ of its years plus noise, and
   no domestic reference detail: signal = ρ·(2c) + a·0.5 + noise(σ_acc).
Factors varied independently: accuracy noise σ_acc ∈ {0.3 (high), 0.8 (low)}; screening cost paid by
the applicant ∈ {0.0, 0.5} with application allowed iff cost ≤ SES budget exp(0.5s) (so cost can exclude
poor applicants); network/referral share of vacancies ∈ {0, 0.3} allocated to high-SES applicants
before the merit ranking; cross-border recognition ρ ∈ {1.0, 0.3} (affects the foreign reader).
Seeds 0..9 (matched across all arms/factors; noise and referral draws).

**Outcomes.** (a) hiring error: mean |p_hired − p_optimal| / sd(p) and share of the true top-M
productivity applicants not hired; (b) exclusion: top-tertile-productivity applicants not hired, and
the SES gradient of hired productivity / of exclusion; (c) wages (mean formal, mean all); (d)
certification demand: share of applicants for whom the expected gain from acquiring tier c+1
(re-ranked with c+1, gain in hire probability × discounted formal-informal wage difference over 20
years) exceeds a declared certification cost of 6 index units. Baseline configuration declared as
accuracy=high, screening cost=0, network share=0, recognition=full; one-factor variants and the full
factorial are written to the CSV.

**Predeclared decision rule.** A reader improves hiring error over another iff the mean paired
difference across the 10 matched seeds exceeds 2 seed-sd and has the same sign in ≥8/10 seeds;
otherwise `not identified at this N`. `Calling-card claim tested`: "the detailed domestic reader has
lower hiring error than the coarse reader but induces higher certification demand" — reported as
`supports` / `contradicted` / `not identified` by that rule. Cross-border recognition is reported as
the foreign-reader error/exclusion change between ρ=1.0 and ρ=0.3 under the same rule. All cells are
stylized model outcomes, not empirical hiring estimates; no country claim.

**Runs.** 5 arms × 16 factor combinations × 10 seeds = 800 static hiring evaluations (cheap).
