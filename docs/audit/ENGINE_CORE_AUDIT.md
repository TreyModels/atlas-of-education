# ENGINE_CORE_AUDIT — Gate 1a Phase A (engine-core, 2026-11-25)

Scope: `engine/eduengine/core.py` (580 L), `planning.py`, `modules/labour.py`, `modules/tutoring.py` (read-only;
lane engine-tutoring), the 540 runner `papers/shadow-education-contest/code/run_hk_korea_comparative.py`, and the
country packs. Read-only audit against the pre-repair tree at commit `7356c97`; no engine file was edited in Phase A.

Reproduction: the Phase-A numbers below were measured with a line-event tracer and synthetic small engines on the
unmodified `core.py` (the transient probe scripts are not retained: their line anchors are pre-repair). The
post-repair regression suite is `docs/audit/ENGINE_CHECKS.py`:

```
cd /Users/treymenefee/neon-boot/wt4/auditv2
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine:$PWD/papers/shadow-education-contest/code" \
  /Users/treymenefee/neon-boot/venv/bin/python docs/audit/ENGINE_CHECKS.py --runner
```

It drives the real 540 configs through `build_arms()`, small deterministic engines, and the unmodified 540 runner's
`_run_single`; it asserts the contract invariants this lane owns (13 checks, all green on 2026-11-25).
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


---

# PHASE B — implementation (engine-core), 2026-11-25

Implemented against `docs/audit/ENGINE_INTERFACE_CONTRACT.md` v1.0 @ `37e78fb` (plus amendments A1–A6).
Files: `engine/eduengine/core.py` (580 → 1204 L), `engine/eduengine/rng.py` (new, 232 L),
`engine/eduengine/modules/labour.py` (206 → 243 L), `engine/eduengine/planning.py` (113 → 175 L),
`docs/audit/ENGINE_CHECKS.py` (new regression suite). Nothing outside this lane's scope was edited.

## B1. Gate schema (§1; D8/D4.1)

* `normalise_gates()` (`core.py:117`) validates one gate per level; canonical kinds `open|fixed_bar|quota|contest`;
  `'bar'` → `fixed_bar` alias with one `DeprecationWarning` per Engine; **missing/unknown kind raises `ValueError`**
  (never falls through to quota); `share∈(0,1]`, `share_of∈{cohort,applicants}`, `fail∈{track,stop}` normalised,
  `admit={share,cut0,academic_only,kind∈{quota,open},share_of}`, `spec` may not carry numeric fields.
* `_install_gates()` (`core.py:298`) runs at construction **and** after every calendar `events` gate replacement
  (`apply_calendar`, `core.py:807`), carrying `cut`/`cut_adm`/`lam_contest` over for unchanged indices.
* Tracking-gate validation: requires `contest`, `fail='track'`, `track_prize` keys exactly
  `{quality_mult,earnings_logw,g12_track_bonus}` (numeric, at least one non-neutral), forbids `elite_logw`/`set_voc`,
  at most one tracking gate. `GATE_SPECS = {'KR-SINGLE':…, 'KR-TRACKED':…}` (`core.py:93`) exactly per contract §3
  (G9 open vs selective tracking gate; G12 `track_bonus=1.25`); the three magnitudes are the pre-registered
  structural placeholders of contract §3, not estimates.

## B2. Persistent state (§2; D1)

`add_cohort` (`core.py:538`) allocates `k['pid'] = t*N + arange(N)` (immutable), `k['track']` int8 −1/0/1,
`k['elite']` bool, `k['elite_prize']` float64 (max won effective log prize), `k['prep_stock']` (N,nlev) float64.
Compaction on exit is automatic (`core.py:1057-1064`). `contest_e` survives only as the current-year effort flow
(reset in `step`, `core.py:882`) and feeds no probability path.

## B3. Track consequence (§3; D1)

`values(t, L=None, idx=None, track_state=None)` (`core.py:568`) / `_value_recursion` (`core.py:577`) implement the
dual-state recursion: for levels above the tracking gate the value tables are computed for track=1 and track=0
(`quality_mult` on projected learning, track-conditional credential values `kappa*(B+earnings_logw)`, `track_bonus`
on own contest weight at later gates); at the tracking gate pass → track=1 continuation, fail → track=0 continuation.
`gate_prize_dv(m, idx)` (`core.py:708`) returns `delta**yrs_left * (U_track1 − U_track0)` from that same recursion
for tracking gates (only prize tutoring may price) and `kappa*effective_elite_logw` for elite gates. Realised
channels: learning line multiplies quality by `quality_mult` for `track==1` (`core.py:899-901`), later contest weight
multiplies by `track_bonus` (`_contest_w`, `core.py:394-412`), labour applies `exp(earnings_logw)` to track=1 leavers
(`labour.py:139-148`).

## B4. Plackett–Luce probabilities (§1.3; D2)

The `1−exp(−λx^r)` household probability and the λ re-solve are deleted (`self.lam_contest` remains only as an
initialised, unused compatibility attribute). `pl_win_probs`/`pl_realize` are imported from
`eduengine.contest_math` (`core.py:22`): expected P in `_gate_expected_P` (`core.py:486`) and in the
`contest_expected_probs` API (`core.py:464`); realised admission uses `pl_realize` with event-keyed uniforms
`(year, f'contest_pl_{m}', pid)` (`core.py:944-949`). `_pl_probs` (`core.py:437`) enforces
`|ΣP − seats_eff| ≤ 1e-3` and renormalises, raising otherwise (contract §1.3). No private Gumbel/argsort PL code
remains in `core.py`/`labour.py` (checked by `ENGINE_CHECKS.py`).
**Performance engineering:** the sitting-cohort pool (`_contest_pool_mask`, `core.py:344`) plus a cached monotone
probability map (`_gate_expected_P`, `core.py:486`) reduce a 540-config run from 76 s to 4.4 s (KR) / 2.4 s (HK) on
the host, while every expected probability still comes from `pl_win_probs` on the official candidate pool.

## B5. Seat accounting and diagnostics (§1.2/§1.4; D3)

Seats are `max(round(share·denominator),1)` with `share_of='cohort'` (legacy `N`) or `'applicants'` (candidate count);
quota cutoffs are now set by *rank* (exact seat count, no zero-seat all-pass, no double exam noise in admission);
the realised admission quota ranks on the exam score without an extra noise draw. Every year records
`contest_candidates/seats/expected_seats/admitted/applicant_seat_ratio/admit_rate/expected_p_mean/expected_p_by_q/
realized_by_q/prep_stock_mean_by_q` per gate (`core.py:1069-1104`); `contest_summary()` (`core.py:1105`) is merged
additively into `Engine.run()` output. `planning.gate_accounting(E)` (`planning.py:122`) reads the series into the
per-gate applicant/seat/admission table the review asked for.

## B6. Event-keyed randomness (§7; D6)

New `engine/eduengine/rng.py`: `EventRNG` = splitmix64 hash of `(seed, replicate, year, shock_type, pid, tap)`,
vectorised over pid, subset/order independent; `SHOCK_TYPES` registry append-only; gate-indexed families
(`gate_exam_{m}`, `contest_pl_{m}`, `admit_{m}`) stable. `E.rng` remains an `EventRNG`; unmigrated modules keep a
private legacy generator exposed as `random/standard_normal/legacy_logistic/permutation/choice` (residual
path-dependence documented). All core.py + labour.py exogenous draws listed in contract §7.2 are event-keyed.
Measured: identical pids and identical cohort covariates across arms; Baseline vs CF1a same-seed exogenous z now
matches in **all** cohorts (phase A: 9/20).

## B7. Labour (§8; D7)

Prizes are applied inside `QueueLabour.labour` **after** tier assignment/queueing and **last**, multiplicatively:
`inc *= exp(elite_prize) * (exp(track_earnings_logw) if track==1 else 1)` (`labour.py:139-148`); the same multiplier
covers queuers (their prize/track are carried in the queue dict), so beliefs, the earnings stock and the tax base are
consistent. `elite/prize/track` no longer touch wage parameters or hiring signals. Audit series
`elite_share, elite_prize_mean, track_share, track_prize_mean, elite_inc_gap_raw/direct/composition` are recorded
per year (`labour.py:183`). Measured decomposition (KR-TRACKED, N=40/T=22): raw elite log-income gap 2.32,
direct multiplier component 0.29, composition/selection 2.04 — i.e. the raw gap is mostly selection, as contract §8
warns. Wage-compression invariance is asserted exactly: `inc_after == inc_base * multiplier` to 1e-12, the
multiplier equals `exp(elite_prize)·[exp(0.15) if track=1]`, and non-track incomes are untouched by the track premium.

## B8. Compatibility (§9)

`Engine(modules, **params)` unchanged; unknown params still `KeyError`; `'bar'` alias covers every existing world /
country pack. Smoke-run: all four `engine/worlds.py` worlds and the China/Cambodia/Philippines packs construct and
run (`EGINE_CHECKS.py` `compat` check); the unmodified 540 runner's `_run_single` runs (KR seed 0, N=120/T=26).
Series keys are additive-only; the one documented meaning change is the intended D7 correction (the elite premium is
now the *won* per-child prize, not the global parameter).

## B9. Documented deviations / clarifications (for Commander + qa)

1. **`contest_candidates(m)` uses the sitting cohort** (`cred==m` and `g==ends[m]-1`, i.e. the children who sit the
   gate this year) rather than the literal contract wording `cred<=m`. With `cred<=m` the pool would span several
   year groups and *expected* P would no longer be the same object as the realised top-seat draw — the exact defect
   D2 is fixing. Flagged to the Commander as a wording clarification; no lane's call sites are affected.
2. **Expected P for children valued at a future gate** uses the official pool probabilities' monotone map by own
   weight (exact for the sitting cohort). This is a documented approximation: the future cohort's weight
   distribution is represented by this year's sitting cohort. No probability is produced by any formula other than
   `pl_win_probs` on the official pool.
3. **`fail='track'` on fixed_bar/quota gates** is now valued as the continuation it actually is (`Vfail = Vcont`),
   fixing D4.3; the vocational learning-quality wedge is realised in learning but not separately valued (documented
   approximation; affects the China pack's zhongkao only).
4. **Zero/absent seats** now floor at 1 (contract §1.3), so a tiny quota share no longer admits everybody; quota
   admission is rank-based and no longer adds a second exam-noise draw.
5. **Legacy 540 config**: because `k['elite']` may now be set at any level (§2), the old KR G9 gate's
   `elite_logw=0.15` is *delivered* as a direct premium instead of remaining a phantom. The canonical repair is
   `GATE_SPECS['KR-TRACKED']`; the unmodified 540 run is kept runnable and its numerics change is quantified below.

## B10. Migration table — unmodified 540 Baseline, old record vs repaired engine (3 matched seeds, mean)

| metric | KR old | KR new | Δ | HK old | HK new | Δ |
|---|---|---|---|---|---|---|
| `k12_spend` (household) | 1067.9 | 134.6 | −933.2 | 1336.1 | 156.4 | −1179.7 |
| `k12_rate_pct` | 57.48 | 58.13 | +0.65 | 59.08 | 61.82 | +2.74 |
| `g12_pct` (tutoring at G12) | 73.22 | 36.17 | −37.05 | 72.47 | 49.45 | −23.01 |
| `q5_q1_gap_pp` | 68.38 | 30.13 | −38.25 | 70.37 | 35.23 | −35.15 |
| `q5_q1_spend_ratio` | 18.12 | 2.14 | −15.98 | 39.92 | 2.52 | −37.40 |
| `elite_q5_share_pct` | 36.73 | 21.99 | −14.74 | 46.09 | 24.70 | −21.39 |
| `contest_e_mean` | 1.710 | 0.016 | −1.694 | 2.177 | 0.043 | −2.134 |

Causes, in order of magnitude: (i) D2 — honest Plackett–Luce expected probabilities replace the old exponential
form, whose mean expected probability was 2.4× the realised admission (audit §B), so contest preparation collapses
(old contest prep was ~92 % of K-12 household spend per audit §A); (ii) D6 — arms no longer drift on the RNG stream;
(iii) the legacy G9 premium is delivered rather than phantom. The KR Q5−Q1 participation gap moves from 68.4 pp to
30.1 pp (review target 32.1 pp) and the Q5/Q1 spend ratio from 18.1× to 2.14× (target 3.4×) *without any
calibration* — i.e. most of the review's "540 calibration lost" finding was the contest-architecture defect, not a
parameter problem. This is a migration record, not a calibration: the canonical spec stays unfrozen (Dashboard
decision 1) and no wave-1 numbers should be read as empirical.

## B11. Checks run (all green, 2026-11-25)

`docs/audit/ENGINE_CHECKS.py --runner` → **13/13** checks pass (~60 s on host; no box job used):
gate schema/alias/length/tracking validation; calendar re-normalisation; PL seat-sum & no-private-PL grep;
D1 track persistence + all three channels + `gate_prize_dv == V(track=1)−V(track=0)`; KR-SINGLE no-track;
D3 seat denominators/diagnostics/`planning.gate_accounting`/share_of; D6 bit-determinism + matched exogenous draws;
D7 multiplicative-last identity + decomposition; zero-prize ⇒ zero effort; worlds/countries smoke;
unmodified 540-runner `_run_single`. qa-verifier's `tests/test_engine_invariants.py` currently shows 23 pass /
4 fail, all four failures being test-side (`method='exact'` used with n>EXACT_MAX_N=20, and a strict
`xfail` that now XPASSes because the API exists) — reported to qa-verifier, not engine defects.

## B12. Residual risks

1. `contest_math` quadrature cost (~14–50 ms per gate-year, contract target ≤50 ms) sets a floor on run time; the
   repaired 540 config runs at 4.4 s (KR) / 2.4 s (HK) with the pool-map cache, so the full 540 rerun is ~20–30 min
   on 8 host workers (legacy: ~3 min). A cached/vectorised probability service is a wave-2 optimisation.
2. Future-gate expected probabilities use the current sitting cohort's weight distribution (documented
   approximation, §B9.2); the sitting-cohort P itself is exact from `pl_win_probs`.
3. Unmigrated modules (`schools.py`, `tutoring.py`, `anchor.py`) still consume the private legacy stream: their own
   draws are deterministic for a run but not matched across policy arms (contract §7 rule 2, recorded residual).
4. `quota`/`fixed_bar` expected probabilities remain the legacy normal CDF at a lagged cutoff (contract mandates PL
   only for contest gates); the cutoff is still an in-sample order statistic, now recorded per gate for audibility.
5. The legacy 540 KR G9 gate delivers its old `elite_logw` at G9; `elite_q5_share` in the old runner therefore now
   counts G9 winners. The canonical KR specs avoid the ambiguity; the old metric should not be compared across the
   repair without noting this.
