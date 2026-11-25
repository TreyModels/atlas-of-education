# ENGINE_CORE_AUDIT — Gate 1a Phase A (engine-core, 2026-11-25)

Scope: `engine/eduengine/core.py` (580 L), `planning.py`, `modules/labour.py`, `modules/tutoring.py` (read-only;
lane engine-tutoring), the 540 runner `papers/shadow-education-contest/code/run_hk_korea_comparative.py`, and the
country packs. Read-only audit against the pre-repair tree at commit `7356c97`; no engine file was edited in Phase A.

Reproduction commands (Mac host venv, from `/Users/treymenefee/neon-boot/wt4/auditv2`):

```
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine" \
  /Users/treymenefee/neon-boot/venv/bin/python docs/audit/ENGINE_core_probe.py       # population/gate inventory
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine" \
  /Users/treymenefee/neon-boot/venv/bin/python docs/audit/ENGINE_gate_trace.py      # expected-vs-realised, seat shares
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine" \
  /Users/treymenefee/neon-boot/venv/bin/python docs/audit/ENGINE_synthetic_gate_checks.py  # structural defects
```

The checks drive the real 540 configs through `build_arms()` and a line-event tracer on the unmodified `core.py`.
Post-repair regression checks live in `docs/audit/ENGINE_CHECKS.py` (added in Phase B).
Evidence taxonomy: every item below is **REPRODUCED SIMULATION** (measured on this tree), not empirical.

---

## A. KR Grade-9 contest has no persistent consequence (D1, critical)

**Code.** The only place a contest gate writes persistent child state is `core.py:428-429`:

```python
if gate.get('fail') == 'track' and m_ == self.nlev - 2:
    k['elite'][at_gate & ok] = True
```

i.e. elite status is set **only** for a gate whose level index is `nlev-2` (m_=2, end of upper secondary). The KR
G9 gate is gate index 1 (`run_hk_korea_comparative.py:115`:
`dict(kind='contest', share=0.35, fail='track', elite_logw=0.15, set_voc=False)`). For it:
- `core.py:428` is false (m_=1 ≠ 2) → no elite flag;
- `set_voc=False` → `core.py:443-444` does **not** mark losers vocational;
- `core.py:439-445` sets `tracked = at_gate & ~ok; ok = ok | tracked; passed = at_gate & ok` → winners and losers
  are both `passed` and receive credential 2 (`core.py:448-449`), same `comp_age`, same continuation.
- `core.py:427` resets `contest_e`, but no other state records the outcome.

Hence the contest consumes real resources and a real Gumbel-max draw and delivers **zero lasting consequence**.
Worse, the same gate is priced by the tutoring module as a prize: `modules/tutoring.py:97-101` reads
`elw = gate.get('elite_logw', p['elite_logw'])` (=0.15 at KR G9) and maximizes
`dV = delta**(yrs_left-1) * kappa * elw` times expected P (`tutoring.py:101-112`); the core's own value function does
the same at `core.py:181-188` (`elw = gate.get('elite_logw', ...)`, `Upass = U + kappa*elw`) — the "phantom prize".

**Measured (ENGINE_CHECKS, KR baseline 540 config, N=300, T=46, seed 0).**
- G9 gate (m=1) set **0** elite flags over the whole run; G12 gate (m=2) set 1260 elite flags.
- Realized G9 admission (winners/applicants) = 0.351, yet every child continues: 51.0 % of all contest-prep
  spending (21 099.6 of 41 350.4 wage units over the run) targets the phantom G9 gate.
- Contest preparation is 91.7 % of full-run household K-12 spending in KR (94.1 % in HK): the phantom prize is not a
  side-show — it is most of the private-spending mass in the 540 design.
- `k['elite']` is also hard-wired to the penultimate level (`core.py:428`): a contest at G9, at the last level, or in
  a differently shaped ladder can never set it.

**Contract fix:** D1 → explicit `track_consequence`/`track_prize` gates, persistent `k['track']` ∈ {-1,0,1}, KR-SINGLE
vs KR-TRACKED data specs (contract §1.2, §2, §3), `gate_prize_dv` from `values()` (contract §6).

## B. Expected vs realized probabilities are different objects (D2)

**Code.**
- Expected (household): `core.py:173-188`, specifically `core.py:177-178`:
  `x_eff = max(x0*max(Lend,0.1)/ends[m] + alpha*contest_e, 1e-6)`;
  `P = 1 - exp(-clip(lam_contest[m] * x_eff**r, 0, 50))`.
- Realized (gate): `core.py:397-415`: `w_log = r*log(x_eff)`, `gumbel = -log(-log(u))`,
  `pl_score = w_log + gumbel`, top-`seats` win — a Gumbel-max Plackett–Luce draw.
- `lam_contest[m]` is re-solved every year as a market-clearing scalar from aggregate seats,
  `core.py:416-426`: `target_s = min(seats/len(ci), 0.99)` and a 30-step bisection, then 0.7/0.3 EMA. It is not an
  individual win probability, and it is initialised to `0.5` for every contest gate (`core.py:101`) with no
  calibration. `values()` uses last year's λ for the current household decision; the same λ is then overwritten.
- The two paths also disagree on the input: `values()` projects `Lend = L + lam*(ends[m]-g)` from the *believed*
  learning rate (`core.py:171`) and cumulative `contest_e`; the gate uses realised `L` and `contest_e`.
- Tutoring prices effort with the same exponential form (`tutoring.py:112, 123, 130, 132`), so the whole private
  demand for contest prep is built on the wrong probability object.

**Measured (ENGINE_CHECKS, line-level tracer on the unmodified engine).** Warm years (t≥12, KR baseline):
- KR G12 (share 0.12): mean expected P = 0.292 vs realised admission 0.121 (2.4× overestimate); by x_eff quintile,
  expected/realised = 0.015/0.013, 0.284/0.071, 0.396/0.151, 0.374/0.174, 0.389/0.197 — the household's probability
  is nearly flat across the middle four quintiles while the realized PL gradient rises monotonically.
- HK G12 (share 0.23): warm mean expected P = 0.455 vs realised 0.232; quintiles 0.404/0.162, 0.606/0.235,
  0.662/0.304, 0.584/0.446.
- Transition: λ starts at 0.5, so early cohorts see expected P≈0.9 for a 12 % gate; the EMA needs ~15 years to settle.
  In the first cohort-years the gap is up to 0.97 vs 0.12.

**Contract fix:** D2 → `pl_win_probs`/`pl_realize` from `eduengine.contest_math` for *both* expected and realized
probabilities; λ re-solve deleted (contract §1.3, §6).

## C. Seat-share denominator is the entering cohort, not applicants (D3)

**Code.** `seats = max(int(round(gate['share'] * p['N'])), 1)` at `core.py:400` (contest) and
`seats = int(round(gate['share'] * p['N']))` at `core.py:433` (quota), where `p['N']` is the entering cohort and the
admitted set is the `at_gate`/`ci` applicant pool. The admission quota repeats it at `core.py:464`
(`adm['share'] * p['N']` on candidates `ci`). The comment at `core.py:430-431` records that the denominator was
deliberately moved off takers to avoid a ratcheting cutoff — but the consequence is that the *nominal* share is a
share of births, not of applicants, and applicants/seats/admission rates are nowhere reported (`E.R` has no
applicant/seat/admission series; `planning.py` has no gate-flow accounting).

**Measured.**
- 540 baseline happens to be near-universal progression to the gate (KR applicants/year 296.7 of N=300), so the wedge
  is small there (realised 0.121 vs nominal 0.12).
- With ordinary liquidity attrition (`subsist=1.2, borrow=0, y_median=1.2`) the same KR config has 139 applicants at
  G12 of N=300: seats stay 36 → realised admission **0.260** for a nominal share 0.12 (**2.2×**).
- `share_of='applicants'` does not exist in the legacy code; contract §1.2 adds it as the D3 repair and requires the
  per-gate diagnostics of §1.4.

**Additional seat bugs found (all confirmed):**
1. **Zero-seat quota admits everybody.** `core.py:432-436`: `seats = round(share*N)` can be 0; then
   `c = s[seats-1] if len(s) > seats else s[-1]` takes `s[-1]` (the *lowest* score) and `ok = score >= c` passes
   everyone. Synthetic check [2]: `share=1e-4, N=100` (seats=0) → admission 1.000 in 13/13 cohort-years. Should admit
   nobody (or raise).
2. **Contest is non-selective when applicants ≤ seats.** `core.py:411-415`: `if len(ci) > seats: ... else: ok[ci]=True`.
   Synthetic check [3]: 50 %-share contest with attrition → 102.7 applicants vs 100 seats → admission 1.000 in 11/22
   years. No contest is held and no prize is rationed.
3. **Seat floor of 1.** `max(..., 1)` at `core.py:400` awards a winner even when the seat share is 0.
4. **Double noise in admission ranking.** `core.py:466` adds `exam_sd*normal*0.5` on top of a score that already
   contains `exam_sd*normal` (`core.py:394`), so the admission ranking is noisier than the exam it claims to rank.
5. **In-sample cutoff.** `core.py:432-436` computes the quota cutoff from the same cohort's scores and applies it to
   the same cohort; the EMA value is then used as next year's *belief* (`core.py:190`) — a lagged order statistic of a
   different cohort, not a forward-looking admission probability.
6. **Admission blocks replace the prize.** `core.py:196-201`: when a gate carries `admit`, `Upass` is overwritten by
   `Pa*U + (1-Pa)*Vc[m+1]`, silently discarding any elite value on that gate.

## D. Other gate / credential / seat defects

| # | defect | anchor | evidence |
|---|---|---|---|
| D4.1 | Unknown `kind` silently behaves as `quota`; no ValueError | `core.py:173,190,397` (values), `core.py:395-436` (progression); `'bar'` is a bare string literal at 173/190/395/441 | synthetic check [1]: `kind='bogus_kind', share=0.5` runs as quota |
| D4.2 | `contest_e` is an undepreciated lifetime stock, reset only at a contest gate | `core.py:135,427`; `tutoring.py:136` (+= each year) | contract §5/D5; prep_stock replacement |
| D4.3 | `fail='track'` on a non-contest gate: value says "stop", progression says "continue" | `core.py:194` sets `Vfail = Vc[m+1]`; `core.py:439-445` makes failers continue (`ok = ok | tracked`) | affects `engine/countries/china.py:10` (`kind='quota', fail='track'`) → exam stakes overstated |
| D4.4 | Closed-level skipping leaves the value function without a continuation for children holding a closed level | `core.py:166-168` (`continue`), vs `core.py:453-459` (credential skipping) | `level_open` configs (china/cambodia); `cont_now` stays 0 for those children |
| D4.5 | Retake bookkeeping: retakes are impossible on `fail='track'` gates (everyone passes); retake years are not counted as repetition for gross intake; `gtimes` reset order | `core.py:475-480`, `core.py:372,381-383` | static; no retakes in the 540 configs |
| D4.6 | Elite premium applied only to the first-year income of new leavers, with the **global** `p['elite_logw']` while the value function uses the **gate-level** `elite_logw` | premium `core.py:498-499`; expected prize `core.py:181` | queuers' incomes (`labour.py:137,147`) miss the premium; beliefs/stock/tax base inconsistent; synthetic check [6] |
| D4.7 | Elite premium is a single post-labour multiplier with no direct-vs-selection decomposition | `core.py:498-499`; `labour.py:112` | contract D7/§8; raw elite gap = direct + composition |
| D4.8 | `pass_rate[m]` mixes non-selective gates (1.0 for `fail='track'` gates with `ok|tracked`) and feeds anchored enrolment | `core.py:447`, consumed at `core.py:249` | overstates pass-through for anchored packs |
| D4.9 | `contest` expected P is `P=0` for vocational candidates (`academic_only`, `core.py:179-180`) but the realized gate excludes them entirely; the two paths still agree, but the *prize* for non-candidates is not valued as "continue on track" consistently | `core.py:179-180` vs `core.py:398` | static |
| D4.10 | Scores are drawn for *all* children at every gate year even when no score-based gate needs them | `core.py:394` | consumes RNG (defect D6 impact below) |

## E. Randomness is a single sequential stream; persons have no id (D6)

**Code.** `core.py:93` creates one `np.random.default_rng(p['seed'])`; it is consumed in path order at:
`core.py:124,125,127,128` (cohort z/urban/home/ability), `core.py:251` (anchored logit), `core.py:331` (continue
draw), `core.py:332` (income shock), `core.py:365` (learning noise), `core.py:378` (promotion noise),
`core.py:394` (exam score, all children), `core.py:408` (PL uniforms), `core.py:466` (extra admission noise),
`core.py:492` (street). Modules draw from the same stream: `tutoring.py:50,51,53,54`; `schools.py:68,131`;
`labour.py:86,91,97,130`. There are no person ids (`add_cohort`, `core.py:128-135`); children are pooled and compacted
by mask (`core.py:507-511`), so an exogenous draw belongs to "the k-th survivor in array order", not to a person.

**Measured (ENGINE_CHECKS).** Two arms that differ only in `contest_price` (Baseline vs CF1a, same seed) match their
exogenous `z` draws in only **9/20** cohorts; the first divergence is cohort t=9 (when gate outcomes first change
survivor counts/array order), after which every cohort's characteristics differ (max |Δz| = 5). The runner's "30
matched seeds" (`run_hk_korea_comparative.py:2,199-208`) therefore match a stream seed, not draws: arm differences
include Monte-Carlo noise. Contract §7 replaces this with hash-keyed `EventRNG` + immutable `k['pid']`.

## F. Labour-market audit (D7)

`modules/labour.py`:
- Premium is applied *outside* the module (`core.py:498-499`) **after** tier assignment (`labour.py:90-115`) and after
  the queue decision (`labour.py:120-130`), so elite status never affects hiring/queueing; the model has no
  "selection into skilled jobs" channel for elite status — only a correlated-ability selection (`sig` uses `cred`,
  standardised `L` and noise, `labour.py:85-96`). The raw elite income gap in the engine is therefore
  direct premium + ability selection; the two are not separated (contract §8 asks for
  `elite_inc_gap_direct` / `elite_inc_gap_composition`).
- The signal is standardised *within the current applicant pool* (`labour.py:85`: `zL = (L-L.mean())/L.std()`), so a
  policy that changes leaver composition changes every leaver's signal — the "exogenous signal" is
  policy-dependent; an absolute-scale signal would be policy-invariant.
- The queue/stock accounting omits the premium for queuers hired later (`labour.py:137,147`), while the leaver's
  first-year income includes it (`core.py:498-499`) — the same person can be booked with and without the premium.
- Tier wage structure (`labour.py:112-113`): `wf = {w_skilled, w_routine} * exp(theta_L*(L-9))`, `winf` similarly.
  The elite multiplier multiplies whichever tier the person lands in, including informal work (a status premium paid
  on informal earnings). Wage-premium compression arms (runner §_with_dv_scale L44-52) therefore scale the elite
  premium **and** the expected prize; mechanically they leave `w_skilled/w_routine/theta_L` unchanged, but they do
  change public/observed channels (beliefs update `core.py:500,513-537`; stock bill `labour.py:147`; tax base when
  `FiscalState` is present) and, because elite is correlated with `L`, the **apparent return to learning** in a
  log-wage regression of income on L changes when the premium is compressed (omitted-variable term
  `elw * d Pr(elite)/dL`). This is the "silent corruption" the contract §8 test must pin down: with
  `elite_logw=0`/neutral track prizes the conditional income distribution by credential must be identical to a
  no-premium run.
- `engine/countries/*` and `engine/worlds.py` smoke coverage: gates are `'bar'`/`'quota'` (+ `admit`), so the `'bar'`
  alias is required for compatibility (contract §9.2).

## G. `planning.py` gap (D3 reporting)

`planning.py` computes promotion/repetition/dropout flows (`flows` L19-36), projection (`project` L39-48),
teacher/cost requirements (`requirements` L51-56) and closure (`closure` L59-71) from `att_by_grade`/`new_by_grade`
only. There is no gate-flow accounting: no applicants, seats, admitted, applicant:seat ratio, or admission rate per
gate per year, even though the engine's gate loop knows all four (`core.py:386-480`). Gate 1a adds them to core
(`E.R` series, contract §1.4) and exposes a `planning.gate_accounting(E)` reader so the planning report can carry
the denominators the review asked for.

## H. Contract mapping (Phase B)

| audit item | contract section | planned change (engine-core scope) |
|---|---|---|
| A (D1) | §1.2, §2, §3, §6 | `track_consequence`/`track_prize` validation; `k['pid','track','elite','elite_prize','prep_stock']`; `GATE_SPECS` KR-SINGLE/KR-TRACKED; `values(..., track_state=)`; `gate_prize_dv` |
| B (D2) | §1.3, §6 | `contest_math.pl_win_probs` in `values()` + `contest_expected_probs`; `pl_realize` at the gate from event stream; delete λ solve; no private PL code |
| C (D3) | §1.2, §1.4 | `share_of`, `contest_seats`, diagnostics series, `contest_summary()`, `planning.gate_accounting`; zero-seat/non-selective admission fixes |
| D4.1 | §1 | constructor + calendar normalisation; `ValueError` on unknown kind; `'bar'`→`fixed_bar` alias with DeprecationWarning |
| D4.2 | §5 (tutoring) | core allocates `prep_stock`, zeroes consumed column after the draw; reads it in values/gate |
| D4.3-D4.5 | §1 | `Vfail = continuation` for `fail='track'`; closed-level continuation fix; retake bookkeeping fix |
| D4.6-D4.7 | §2, §8 | `elite_prize` per child; labour applies prizes on every applicable income (leavers + queuers) and records the decomposition series |
| D6 | §7 | `rng.py EventRNG`; migrate core + labour draws; `k['pid']` |
| F | §8 | wage-compression invariance check + report |
| G | §1.4 | series + planning reader |

**Residual risks recorded now:** (i) expected P for `quota`/`fixed_bar` gates remains the legacy normal-CDF at a
lagged cutoff (contract only mandates PL for contest gates) — a known approximation, not a silent one;
(ii) `values()` prices `fixed_bar`/`quota` `fail='track'` continuation using the same continuation value as passing,
ignoring the realised `voc_quality` learning wedge (documented approximation, affects China pack only);
(iii) determinism of the engine now depends on `contest_math.pl_win_probs(method='auto')` being the deterministic
algorithm required by contract amendment A5 — the current untracked draft falls back to *unseeded* MC above n=12;
engine-core will enforce the seat-sum invariant and flag this dependency to the Commander if the module is not
deterministic when integration starts.
