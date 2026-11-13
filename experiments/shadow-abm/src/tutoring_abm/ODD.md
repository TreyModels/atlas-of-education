# ODD protocol: teacher-supplied tutoring in a school system (Cambodia)

This describes the code in `model.py`, `calibrate.py`, `smc.py`, `analysis.py`, `shared_ablation.py`
and `fresh_check.py` as they stand. It follows the ODD structure of Grimm et al. (2020, *JASSS* 23(2):7),
with the seven elements in the order used there: 1 Purpose and patterns; 2 Entities, state variables and
scales; 3 Process overview and scheduling; 4 Design concepts; 5 Initialization; 6 Input data; 7 Submodels.

## 1. Purpose and patterns

**Purpose.** The model asks which mechanisms could make a teacher sell tutoring to the pupils the teacher
also teaches, and what policies would do under each mechanism. It is a model of one school system, not of
Cambodia. It does not predict outcomes for a specific school.

**Rival mechanisms** (each is one *variant*; the mechanism's parameter is free only in its variant):

| Variant | Free mechanism parameter | Mechanism |
| --- | --- | --- |
| `thin` | none (only `thin`, which is free in every variant) | the official timetable is too short for the curriculum |
| `diversion` | `diversion` (beta) | teachers withhold content that only they fully cover in paid classes |
| `favour` | `favour` (phi) | buying from your own teacher carries a benefit of its own |
| `full` | both | diversion and favour |

Note that `thin` is free in all four variants. The variants therefore differ only in the two parameters
`diversion` and `favour`; the code is identical.

**Patterns used for calibration** (`calibrate.py`, `TARGETS`; Bray et al. 2016, 2018). Each has a tolerance band:

| Pattern | Target | Tolerance |
| --- | --- | --- |
| participation, all pupils | 0.819 | ±0.03 |
| participation, Grade 9 | 0.747 | ±0.04 |
| participation, Grade 12 | 0.898 | ±0.04 |
| urban minus rural participation | 0.026 | ±0.04 |
| own-teacher share of tutoring purchases | 0.577 | ±0.07 |
| other-teacher share of tutoring purchases | 0.409 | ±0.07 |
| share of teachers who tutor | 0.54 | ±0.20 |
| commercial share of purchases | at most 0.05 (one-sided) | scale 0.05 |

**Fit.** For one world, the standardized deviation z is the largest of the eight z values (each pattern's
absolute deviation divided by its tolerance; the commercial term is one-sided). A world fits when z ≤ 1.
A *parameter set* fits when it fits in at least 7 of the 10 calibration worlds (the distance is the 7th
smallest of the 10 world z values, and it is ≤ 1 exactly in that case).

**Patterns not used for calibration** (reported as outputs): withholding, coverage by pupil resource quintile,
the buy and instruction gaps between tutoring and non-tutoring classes, and the ban and other policy effects.

## 2. Entities, state variables and scales

**Scale.** One school system per world: six schools, nine school-grade units, 18 classes, 1,260 pupils, 72
teachers. Time is not modelled explicitly; the outcome is one academic year at equilibrium. There is no
calendar.

**Schools** (`SCHOOLS`): three lower secondary schools (Grade 9 only) and three high schools (Grades 9 and 12).
Two of the six schools are urban (which two is an assumption; see `SCHOOLS`).

**Classes.** Each school-grade unit has two parallel classes of `CLASS_SIZE = 70` pupils. The parallel class of
class *c* is class *c ⊕ 1* (0↔1, 2↔3, …). A class has one teacher per subject.

**Subjects.** Four subjects (`K = 4`) with fixed offsets to pupil utility (`SUBJECT_OFFSETS = [0, -0.4, -0.8, -1.2]`).
They stand for mathematics, physics/chemistry, English and Khmer.

**Pupil state** (fixed within a world, from the world seed):
- grade (9 or 12), school, urban or rural (from the school);
- `resources` ~ N(0,1) + `urban_resources` · urban (a household-resource index);
- `m0`: the feasible regular instruction share of the class (share of curriculum delivered by regular teaching);
  `m0` of a school-grade unit = `m0_mean` + N(0, 0.08) + `extra_time`, clipped to [0.2, 1].

**Teacher state** (one per class and subject, 72 in total):
- `sell_own`: sells tutoring to its own class; `sell_other`: sells to the parallel class;
- `d`: withheld regular content, chosen from `D_GRID` = {0, 0.05, …, 0.4} and capped at the class's `m0`;
- fixed per world: `side_job` ~ U(0, `side_job_max`) (outside earnings, in utility units);
  `norm` = `norm_cost` · exp(N(0, 0.5)) (per-unit cost of withholding content);
  `teacher_fee` (1.0 Grade 9, 1.5 Grade 12, per subject).

**Pupil choice state.** Each pupil and subject has a probability of buying from the own teacher, from the parallel
teacher, from a commercial provider, or nothing. These are computed exactly, not sampled (see §7.1).

**Outputs** (`outcomes()`): participation (any purchase) overall, by grade, urban/rural, and by resource quintile;
provider shares of purchases; teacher shares; withholding; class instruction and coverage; signatures comparing
tutoring and non-tutoring classes; convergence flag and sweep count. With `dropout_channel` on, also spending and
dropout and child-work hazards by poverty status (§7.5).

## 3. Process overview and scheduling

Each world is solved once:

1. **Build the world.** Draw the school, pupil, teacher and class attributes (§5).
2. **Initial strategies.** Every teacher sells to its own class and to the parallel class, with `d = 0`.
   Under `ban_own`, `sell_own` starts `False` for every teacher.
3. **Best-response sweeps.** Repeat up to 30 sweeps. In each sweep, visit every teacher once in a random order
   (`rng.permutation`). Each teacher replaces its strategy with its best response given the current strategies of
   all other teachers and the pupils' choice probabilities (§7.2). Stop when a full sweep changes no teacher.
   If 30 sweeps pass without convergence, the solver stops and the world is flagged as not converged.
4. **Outcomes.** Compute pupil choice probabilities at the final strategies and aggregate (§7.4).

There is no within-world time. Updating is asynchronous and sequential. The policy experiments and the
fresh-world checks re-solve each world under the changed rule with the same world seed, so the paired
differences isolate the policy. The random order can still change the equilibrium that is reached.

## 4. Design concepts

- **Emergence.** Participation, the own-teacher share and the withholding level come out of teacher best responses
  and pupils' choices. None is set directly.
- **Adaptation.** Teachers adapt their own strategy (sell to own pupils, sell to the parallel class, take a side job,
  and withholding level) to maximize profit given others' strategies. Pupils adapt their purchase probabilities to
  the current teacher strategies within the same MNL choice.
- **Objectives.** A teacher maximizes expected profit: fee margin times expected pupils served, minus fixed,
  withholding and convexity costs, or the side-job return. A pupil maximizes utility, with a logit error.
- **Prediction.** A teacher predicts its expected pupils by summing the purchase probabilities of its class at each
  candidate withholding level, given the parallel teacher's current strategy. No learning across sweeps is modelled.
- **Sensing.** Teachers observe the parallel teacher's current `sell_other` and `d` and the pupils' purchase
  probabilities that depend on them. They have no information on other schools.
- **Interaction.** Indirect, through pupils' purchase probabilities (a teacher's withholding affects the demand for
  other teachers in the same school, through `recovery`) and through the parallel-class coupling.
- **Stochasticity.** World attributes are drawn from the world seed. The random order of sweeps uses the same seed.
  Pupil choice is not random (exact probabilities).
- **Observation.** Outcomes are computed on all pupils at equilibrium and averaged over worlds in calibration.

## 5. Initialization

- **World seed.** Each world is a seed. Calibration uses ten fixed calibration worlds `5,000,000 … 5,000,009`, the
  same for every parameter set (common random numbers). Prior-sample pilots use one seed per draw.
  Fresh-world checks use `9,800,000 …` (`fresh_check.py`), which is disjoint from calibration. Earlier checks used
  `9,700,000 …` and are not in the calibration worlds.
- **Parameters.** Each draw is uniform on `PRIORS`; mechanism parameters not free in the variant are 0.
  Non-free mechanism parameters are fixed at 0, and `ban_own`, `cond_pay`, `extra_time`, `com_entry` at their
  zero (no-policy) values.
- **Teachers.** Start with `sell_own = True` (`False` under ban), `sell_other = True`, `d = 0`.
- **Household channel.** Off unless `dropout_channel = True`.

## 6. Input data

There are no data files. The model is calibrated only to the published aggregate patterns in §1 (Bray et al. 2016,
2018), each with a stated tolerance. Two caveats follow from the sources. The provider shares (57.7% and 40.9%) are
read as main-provider answers and matched to shares of tutoring purchases; the question wording should be checked
against the original instrument. The commercial share is only bounded above (1.4% of answers). The school-level
assignment of urban and rural is an assumption. Individual-level data were not used, so the model does not reproduce
any observed distribution beyond those aggregates.

## 7. Submodels

### 7.1 Pupil purchase choice (`choice`, `choice_k`)

For pupil *i* and subject *k*, with `b = base_demand + offset_k + stakes12·1[grade 12] + thin·(1 − m0_i) − γ_i·fee_grade`
and `γ_i = fee_sens · exp(−resources_i)`:

- own teacher (if it sells to own pupils): `exp(b + diversion·d + favour)`;
- parallel-class teacher (if it sells to the parallel class): `exp(b + recovery·diversion·d − other_cost)`;
- commercial provider: `exp(b + recovery·diversion·d − com_cost_i)`, with
  `com_cost_i = max(0, com_cost_urban + com_cost_rural_extra·rural − com_entry)`;
- nothing: 1 (the base of the logit).

Purchase probabilities are the usual multinomial logit shares. Here `d` is the own teacher's withholding, and the
parallel-class option uses the parallel teacher's `d`. Pupils buy at most one provider per subject; the outcomes sum
subject-level probabilities.

### 7.2 Teacher decision (`best_response`)

For teacher *t* (class *c*, subject *k*), with `margin = teacher_fee − TEACHER_COST` (`TEACHER_COST = 0.2`) and
`q_par` the expected number of parallel-class pupils who buy from this teacher (divided by class size). Options:

1. **Side job:** `side_job_t + cond_pay`. Sells to neither.
2. **Parallel only:** `margin · q_par − fixed_cost + cond_pay`. Sells to the parallel class, not to own pupils.
3. **Own (and parallel), with withholding:** the teacher chooses `d` on the grid of feasible levels (≤ `m0`) to
   maximize `margin · (q_own(d) + q_par) − fixed_cost − norm_t · d − 0.5 · CONVEXITY · d²`. Not available under
   `ban_own`.

The teacher takes the highest-payoff option. Ties go to the first listed option in the order given.

### 7.3 Convergence

The teacher loop stops when a full sweep changes no teacher's strategy (`converged = True`), or after 30 sweeps.
Non-converged worlds are kept in the summaries, with `converged` as an output (a small share in some variants).

### 7.4 Outcome aggregation (`outcomes`)

Pupil-level probabilities at the final strategies are aggregated to the outputs in §2. Participation is one minus
the product of non-purchase probabilities over subjects. Coverage for a class is `min(1, m0 − d + added)`, with added
content `d + TUTOR_CONTENT` for own purchases and `recovery·d + TUTOR_CONTENT` for other purchases.

### 7.5 Household channel (off by default; task 3.4)

When `Params.dropout_channel` is True, pupils' expected tutoring spending is `spend_i = (Σ_k purchase probability_ik) · fee_grade`,
in units of a Grade 9 subject fee. For pupils in the lowest resource quintile (`q == 0`), the dropout hazard is
`clip(drop_base + drop_kappa · spend_i, 0, 1)` and the child-work hazard is `clip(work_base + work_kappa · spend_i, 0, 1)`.
The baselines (0.05) and the kappas are illustrative and not calibrated. Outputs are the mean spending and hazards in
the poorest quintile and in the rest. The flag is outside `PRIORS`, so it is never drawn in calibration. With the flag
off, outputs are identical to the earlier model (checked for 1,240 values across 40 world and parameter draws).
This channel is a sensitivity, not an estimate of effects on children.

### 7.6 Policies (`analysis.py`)

- `ban_own`: `sell_own` is forced to `False` for every teacher; the own-teacher option is removed.
- `cond_pay = 0.3`: a bonus for side-job and parallel-only options, so teachers who do not sell to own pupils earn more.
- `extra_time = 0.10`: added to `m0` in every unit (capped at 1).
- `com_entry = 1.5`: a reduction in commercial inconvenience.

Each is run in the same world and with the same parameters as its baseline. Effects are paired differences.

### 7.7 Calibration (`smc.py`)

For each variant, ABC-SMC over the free priors (uniform in `PRIORS`):

- Distance: the 7th smallest of the 10 calibration-world z values (§1).
- Each generation: propose from a mixture of the previous weighted particles, accept when distance ≤ ε, and set ε to
  the median of the previous distances (never below 1). Importance weights are prior / proposal density.
- After each generation, resample by importance weights and apply three random-walk Metropolis moves (`--mh-sweeps`, default 3) targeting
  prior × 1[distance ≤ ε]. This moves particles that are duplicates after resampling (see §7.8 for the ESS output).
- Evidence: importance sampling of `P(distance ≤ 1 | variant)` under the uniform prior, from a batch drawn from the
  final mixture; a bootstrap interval is reported.

### 7.8 Sensitivity and checks

- **Pilot** (`calibrate.py`): prior draws per variant, scored in the same ten worlds.
- **Fresh worlds** (`fresh_check.py`): each particle, in 20 fresh worlds, with the baseline and the ban. Reports
  the share of (particle, world) pairs that fit, and the share of particles that fit in at least 14 of 20 worlds.
- **Shared components** (`shared_ablation.py`): posterior particles re-simulated with one shared mechanism removed or
  changed (no re-calibration). Tests whether the policy ordering is preserved.
- **Robustness** (`analysis.py`): changing class size, tutor content, the Grade 12 fee, the urban school assignment,
  and subject offsets.
