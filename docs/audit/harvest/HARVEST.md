# HARVEST — legacy `model-revision` and `gpu-rtx3080ti` work (PRE-REPAIR, AUTHOR-REPORTED)

**Status: prior/alternative-spec evidence only. NOT Gate-1 evidence, NOT a repair, NOT audited for reuse.**
Two lanes from the previous window (outside our roster) kept running after the handover; the Lead instructed
harvest-and-stop. Their processes were never killed or written to. Contents are labelled
**AUTHOR-REPORTED / PRE-REPAIR** unless a row says the Commander re-executed it.

**Sources**
* branch `research/model-revision-2026-11-25`, tip **`d20ba6e`** — commits `aa2a32f` (pre-registered plan),
  `5c65364` (plan amendment 1), `9939ad7` (engine fixes 3A–3C + canonical 420 runner), `d20ba6e` (plan amendment 2 +
  calibration sweep). Files: `model_revision/`.
* branch `research/gpu-rtx3080ti-2026-11-25`, tip **`9f7dfa9`** (pushed) — RTX 3080 Ti run record. Files:
  `gpu_rtx3080ti/` (see its own README for mandatory labels).
* box `/root/work/modelrev/results/` and `/root/work/gpu/results_rtx3080ti/` — pulled read-only with
  `/tmp/box_pull.sh`; the result JSONs are byte-identical to the branch record (sha256 in
  `HARVEST_MANIFEST.csv`).

---

## 1. What the legacy `model-revision` engine fixes do (commit `9939ad7`, +173 L core, +46 L tutoring)

Line numbers below are in **that branch's** `engine/eduengine/core.py` (post-fix), not in our audit branch.

| review item | legacy mechanism | anchors |
|---|---|---|
| §3.A KR G9 phantom prize | adds persistent boolean `k['elite9']` + switches `g9_consequence`, `g9_learn_boost` (upper-secondary learning boost), `g9_contest_boost` (multiplicative boost to later-gate `x_eff`), `g9_elite_logw` (optional direct wage channel, 0 in their canonical spec); switch off = legacy | `core.py:63-66, 158, 241-247, 501-503, 544` |
| §3.B expected vs realized | expected top-K admission `contest_prob(m,x) = sigmoid(beta·(log x − c_K))`; `beta, c_K` re-fitted **every gate year** by 256-draw vectorised Gumbel-max MC of the gate's own ranking, re-centred so mean P = min(seats/applicants, 0.99); same function used in `values()` and in tutoring's effort choice; separate RNG stream `rng_fit = default_rng(seed + 1_000_003)` | `core.py:118, 249-311`; `modules/tutoring.py:107, 111-118` |
| §3.C seat denominator | per-gate diagnostics accumulators `contest_calib` (applicants, seats, admitted, ratio, Brier, flat-Brier, decile bins, effort-quintile bins, beta/cut) recorded in the scored window for expected-vs-realized reporting | `core.py:118-124, 312+` |
| generation | canonical 420-generation port + `run_hk_korea_canonical.py` (579 L) with V1/V2/V3 variants, 30 matched seeds; lumpy contest purchase margin 0.25 | `run_hk_korea_canonical.py` |

## 2. Diff against our binding contract — what could ever be reused, and what cannot

| contract requirement (`ENGINE_INTERFACE_CONTRACT.md`) | legacy implementation | verdict |
|---|---|---|
| **§3 rule 4: G9 expected prize = actual transition continuation value** (no reduced-form prize) | their own code comment: *"the household's anticipated value is still the gate's `elite_logw` (reduced-form belief, used in `values()`); the realised consequences are the two channels below"* — i.e. expected prize stays `kappa·elite_logw` while realisation is `elite9` channels | **NON-COMPLIANT** — the expectation/realisation mismatch in the *prize* is preserved (only the probability side is addressed) |
| **§1.2/§2: single track state `k['track'] ∈ {−1,0,1}`**, sticky, consumed by values and labour | `k['elite9']` boolean; no −1 state; not shared with our state or labour channels | **NOT INTEROPERABLE** — would duplicate state; no reuse |
| **§1.3/A5: expected P = deterministic exact-ish `pl_win_probs`**, exact for n≤12, sum-to-seats exact | logistic curve fitted by **MC** (256 draws/gate-year) on a separate seed-shifted stream; mean-calibrated to `min(seats/n, 0.99)`, not sum-to-seats; MC noise per seed; tiny contests are not exact (a 4:1 one-seat contest cannot produce 0.8/0.2) | **NON-COMPLIANT with A5's exactness/determinism targets**; our `contest_math` (`1a6f3d5`) supersedes it and meets the targets |
| **§1.4 diagnostics series + `share_of='applicants'`** | aggregate accumulator dict in `contest_calib`, scored-window only; no per-year `E.R` series, no `share_of` option; denominator unchanged (share of cohort) | **PARTIAL — superseded**; our contract already has the fuller design |
| **§8 labour premium decomposition / `elite_prize`** | not addressed | **NOT ADDRESSED** |
| **§7 policy-invariant event-keyed RNG** | only the *fit* RNG is separate (seed+1 000 003); main cohort/path stream still sequential and path-dependent | **NOT ADDRESSED** |
| lumpy contest purchase margin 0.25 | 420-generation spec detail, not in our contract | **WAVE-2 SPEC QUESTION ONLY** (canonical spec not frozen) |

## 3. Commander re-execution: our invariant suite against the legacy engine — REJECT

I extracted the legacy branch engine to `/tmp/legacy-modelrev` (`git archive research/model-revision-2026-11-25
engine`), copied **our** committed invariant suite (`tests/test_engine_invariants.py` + `conftest.py` from audit
branch) and ran it. Log: `LEGACY_INVARIANT_RUN.log`.

```
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=$PWD/engine \
  /Users/treymenefee/neon-boot/venv/bin/python -m pytest tests/test_engine_invariants.py -q --tb=no
→ 7 failed, 10 passed, 10 xfailed (85 warnings) in 5.19 s
```

**The same seven present-and-wrong failures as the unrepaired baseline (F1–F7):**
universal-seat positional effort; non-selective gate priced; G9 award not persisted in the contract's state;
expected P ≠ exact PL; seat denominator not of applicants; policy-variant RNG; gate prize paid as global not declared.
So the legacy fixes close **none** of our seven contract-level failures (they change the mechanism, not the
contract-conformance), and its G9 state (`elite9`) is not the contract's `k['track']`/`k['elite_prize']`.
**Conclusion: no code or state design from `research/model-revision-2026-11-25` is adopted into Gate 1.** Its engine
diff stays `AUTHOR-REPORTED / PRE-REPAIR`; only the items below are preserved.

## 4. Preserved negative result: Korean calibration FAILURE (AUTHOR-REPORTED, PRE-REPAIR)

Source: `model_revision/calibration_sweep_branch.json` (sha256 `9b3d5c8f…`, also byte-identical to the box copy),
metadata `SIMULATION — stochastic model output, not empirical estimates`; 180 runs (6×3 grid × 10 calibration seeds),
`nice -n 10`, 56 workers (**oversubscribed the 10-CPU cgroup — their own note later corrected to ≤8; the sweep took
100.99 s**).

| point | participation % | Q5−Q1 gap (pp) | Q5/Q1 spend ratio | elite Q5 % | vs targets (76.5 / 32.1 / 3.4) |
|---|---|---|---|---|---|
| untuned 420 port (price×1.0, α×1.0) | **66.27** | **80.77** | **5.32×** | 22.77 | outside every target |
| grid best (price×0.25, α×1.15) | **91.63** | **37.11** | **1.59×** | 20.21 | participation far too high, gap still too wide |
| price×0.50, α×1.00 | 79.84 | 66.07 | 2.95× | 21.43 | gap still ~2× too wide |

**Interpretation (preserve, do not hide):** the canonical 420-generation port, as pre-registered and swept by the
legacy lane, **does not recover the Korean participation/gap/spend-ratio moments**; no grid point reaches all three,
and the selection rule had to pick a minimum-score point that is still outside tolerance. This is a **negative result
for the 420-port-to-patched-engine route** and is directly relevant to the Lead's open canonical-spec decision
(DASHBOARD open decision 1). It is **AUTHOR-REPORTED / PRE-REPAIR**; it does **not** substitute for Gate 2 calibration
and no Gate-1 conclusion depends on it.

## 5. Operational fact corroborated

The legacy lane independently recorded that the box is a **10-CPU cgroup** (`cpu.max = 1000000 100000`), that `nproc`
reports the 80-CPU host, and that a 56-worker run oversubscribed it (slower than the 8-worker run). This corroborates
the Lead correction; our lanes were told: total ≤8 workers, ≤4 per lane, `nice -n 10`, BLAS/OpenMP threads = 1.

## 6. Harvest rules applied

* Read-only: no process was killed, no legacy box directory was written, no legacy branch was modified or merged.
* Everything here is labelled **AUTHOR-REPORTED / PRE-REPAIR** (plus one Commander re-execution log,
  `LEGACY_INVARIANT_RUN.log`, which is a conformance test, not a reproduction of their result).
* Nothing from this directory may be cited in the Gate-0/Gate-1 reports as repaired behaviour, calibration, or
  E1/Q3 reconstruction. Reuse requires the item to be re-expressed under `ENGINE_INTERFACE_CONTRACT.md` and to pass
  our invariant suite — none of it currently does.
