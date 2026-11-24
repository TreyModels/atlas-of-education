# RUN REPORT — corrected small experiment (matrix + Phase B), region-42, 2026-11-24

**STATUS: EXPLORATORY SIMULATION — NOT CONFIRMATORY, NOT EMPIRICAL EVIDENCE, NO CAUSAL
LANGUAGE.** These results may not be compared directly with E1's 1.8 % and do not establish
that any macro "wall" holds in real countries. The pre-registered raw-unit ±0.05 TOST margin
is **provisional and not substantively established per outcome**; effect sizes and CIs are
reported as exploratory. **Rm (misspecified world) is NOT IMPLEMENTED in this run** and must
not be described as assessed. Fertility-stratum macro FE, the matched-nuisance follow-up, and
a formal null-control validation are **NOT IMPLEMENTED**. Amendment_01 was **declined by
Codex as a confirmatory design** (Bridge 2026-11-24T12:23:07Z) and is retained only as a
proposed exploratory follow-up; it is not an active pre-registration and no run used it.

This run executed the **Codex audited exploratory implementation** of the committed
corrected pre-registration (`77d6f23`) under Codex's explicit exploratory clearance
(Bridge 2026-11-24T12:23:07Z, "exploratory run cleared with bounded pilot"). Code was not
edited. All artefacts and hashes are recorded below; old exploratory outputs are untouched.
The `synth_loop/` directory in this record is an **earlier, unrun draft** (commit `90e6a1b`);
it was superseded by Codex's implementation and was **not used for any result** — everything
reported here comes from the `a12d357` files at this record's root.

---

## 1. Provenance and protocol

| item | value |
|---|---|
| code branch / commit | `research/synthetic-corrected-codex-2026-11-24` @ **a12d357278d703c76da66fd2bc840666957bbbde** (parent `77d6f23`) |
| deployment dir (server) | `/root/work/corrected-codex/` (fresh; sha256 local==remote verified before run) |
| pre-registration base | `research/records/2026-11-24-synthetic-matrix-v2/PRE_REGISTRATION_corrected.md` @ `77d6f23`, sha256 `eab63120…` |
| mapping / limitations | `PRE_REGISTRATION_MAPPING.md` (Codex, in this record) |
| Amendment_01 | commit `395a397` on branch `research/synthetic-corrected-2026-11-24` — **declined as confirmatory design; proposed exploratory follow-up only** |
| server | region-42 `root@region-42.seetacloud.com:54585`, host `autodl-container-bbbc11ba52-44a6772d`, 96 cores, 375 GB RAM, 30 GB free, Python 3.10.8, NumPy 2.2.6, `REDESIGN_BACKEND=numpy` |
| code sha256 | `run_corrected.py 60faefa71200d4b9d2742c659d8da119208d7ad05809751d08b7501e4b864eb2`; `phaseb_corrected.py c3bc506a1434add728ad4cee1cb0d197a4443138dbce28ccd325ced73d9089d9`; `model.py b26b756146fb3694f5f2d367c3bab6e5c85abcee0df11bedc373f3efa47000a2`; `port_backend/kernels_np_mlx.py c44ca6cd…`; `port_backend/gpu_compat.py 4db8407…`; `calibration.json 6cc3c570…`; `test_corrected.py 17d36e81…`; `test_phaseb_corrected.py eadff66b…` |
| exact commands | see `results/COMMANDS.txt` and `results/run_meta.txt` (timestamps, stdout, hashes appended) |

Order of work (all compute on region-42; none on the Mac):

1. **Deploy + hash verify.** `a12d357` tree copied to a fresh dir; every code hash matched the
   branch and `SMOKE_TEST.md` before anything ran.
2. **Bounded pilot** (12:24:36–12:24:43Z): unit tests, CLI smoke, full-size component timings.
3. **Pilot projection:** matrix ≈ 85 s, Phase B ≈ 142 s — far below the 45-min stop rule.
4. **Full matrix** launched 12:24:51Z, completed 12:27:11Z.
5. **Full Phase B** launched 12:27:11Z, completed 12:29:31Z.
6. Results pulled to the Mac, sha256 re-verified against the server, committed here.

### Pilot evidence (mechanics only — not results)

- `python -m unittest -v test_corrected test_phaseb_corrected` → **15/15 tests OK** in 0.47 s
  (7 matrix + 8 fertility; independent run by the runner).
- `python run_corrected.py --smoke --workers 4 --output pilot_smoke.json` →
  **4,200 fits, 4,100 estimable, 4,200 comparisons, 3.38 s**; the 100 unestimable are
  S4 × income (control is the outcome) and are explicitly marked.
- Full-size component timings: one N=10k kernel run 56.9 ms; Pool(96) throughput 105 tasks/s →
  3,200 runs ≈ 30.5 s; full-size fit cost S3 16.3 ms (64-country group) / 2.5 ms (16-country
  archetype), other specs 3–4 ms / ~1.1–1.25 ms.
- Projected full matrix 85 s (generation 30.5 s + 21,000 serial fits 49.5 s), output ≈ 8 MB,
  memory < 1 GB. Projected full Phase B 142 s. Actuals below.

### Actual wall times

| stage | script elapsed | wall incl. launch | notes |
|---|---|---|---|
| full matrix | **87.56 s** | 12:24:51 → 12:27:11Z (140 s incl. process start/JSON write) | 21,000 fits; 10.6 MB output |
| full Phase B | **132.12 s** | 12:27:11 → 12:29:31Z (140 s) | 1,120 units; 714 KB output |

No runtime errors; no rank-deficiency fabrication; no output overwritten; result files are
unique new names. After completion: **no PIDs of ours running**, box idle (load from unrelated
co-site work only).

### Artefacts (sha256)

- `results/matrix_full_EXPLORATORY.json` — 10,635,055 bytes, `ff6dd729924e3e05762a431fa3cc6564a50e14a0df98e6a94a05ed0309d1509c`
- `results/phaseb_full_EXPLORATORY.json` — 713,813 bytes, `97ce46b1256cdbe6cf104e971d5d01339b685ea34f71035a20c547b8226810ca`
- `results/pilot_smoke.json` (3.5 MB), `results/pilot_projection.json`, `results/pilot.log`,
  `results/matrix_full.log`, `results/phaseb_full.log`, `results/run_meta.txt`,
  `results/matrix_summary_EXPLORATORY.json`, `results/phaseb_summary_EXPLORATORY.json`.

---

## 2. Matrix results (EXPLORATORY)

Grid actually executed: 5 worlds (P, S, C, R, **null = the s=0 common baseline**; Rm **NOT
IMPLEMENTED**), N=10,000 households, 64 countries, 25 years, **10 independent country blocks**
(fresh country draws per block; country characteristics paired across worlds within a block),
6 specifications S1–S6 (S2/S5 use **true 5-year windows**; S1/S4 10-year; S3 levels with
country+year FE; S6 annual first differences), 2 measurement-error doses (0×, 1× σ=0.05),
7 outcomes, 5 groups (full sample + 4 declared archetypes).

- **Fits:** 21,000; **estimable 20,500**; **unestimable 500** — all and only `S4 × income`
  (income is simultaneously outcome and the declared control; explicitly retained as an error,
  never coerced to zero).
- **Pairwise comparisons:** 4,200; **usable 4,100**; 100 undefined (`S4 × income`).
- **Uncertainty:** CR1 country-cluster sandwich standard errors within each block; paired
  differences across the 10 independent blocks summarised with Student t (df = 9; conservative
  t table). **No binomial-over-cells uncertainty** is used anywhere. The raw-unit ±0.05 TOST
  flag is Codex's **provisional** criterion and is reported as such.

**Headline (exploratory):** **1,809 / 4,100 pairwise world contrasts (44.1 %) are TOST-
equivalent under the provisional raw ±0.05 margin**; delete-one-block jackknife 95 % CI
**42.6 %–45.7 %**. 60.4 % of contrasts have a 90 % CI excluding zero. Effect sizes:
|Δslope| median **0.0313**, IQR **0.0019–0.0801**, p90 **0.136**, max **0.506**; 39.1 % of
|Δ| exceed 0.05.

| breakdown | share TOST-equivalent (provisional) | median |Δ| |
|---|---|---|
| dose 0× | **60.1 %** | 0.016 |
| dose 1× (σ=0.05) | **28.1 %** | 0.042 |
| S1 / S2 / S3 / S4 / S5 / S6 | 45.0 / 43.4 / 44.7 / 40.8 / 41.9 / 48.4 % | 0.027–0.040 |
| outcome `hw` (hidden work) | **100 %** | 0.000 |
| outcome `inc` | 61.2 % | 0.003 |
| outcome `wo` | 55.7 % | 0.007 |
| outcome `sw` | 36.7 % | 0.045 |
| outcome `cl` | 30.2 % | 0.045 |
| outcome `learn` | 18.7 % | 0.071 |
| outcome `tut` | 9.3 % | 0.095 |
| group full sample | 54.0 % | 0.030 |
| groups type0–type3 | 38.5–44.5 % | 0.024–0.038 |
| closest world pair C–null | 64.9 % | — |
| most separated world pair P–R | 34.4 % | 0.057 |

**Cell-level analogue of the wall statistic:** of the 410 cells with all ten pairwise
comparisons estimable, **117 (28.5 %)** have all ten differences TOST-equivalent under the
provisional raw margin; 293 do not.

Interpretation limits (binding): five synthetic worlds with declared literatures; the `null`
world is the **common baseline** parameterisation (θ0), not a world with no mechanisms; the
±0.05 margin is in each link's own raw slope units and is not comparable across links or
justified per outcome; no multiplicity control; the block/cluster structure gives no
real-country inference; and the mapping's own limitations apply. Nothing here is confirmatory.

---

## 3. Phase B results (EXPLORATORY)

Grid: **WOMEN = 4,000 per unit** (prereg), 25 annual ages 15–40, 20 calibration / 60 held-out /
60 replication seeds per world × 4 worlds, upstream model at N=10,000; 2,000 blocked-permutation
reps; **1,120 units** (560 main + 560 s=0). Wall 132.1 s.

**B1 (within-mother birth-spacing, explicit denominators):** median **7,825** post-death
intervals, **12,844** other intervals, **3,717 mothers with both** per unit (min 5,021 / 11,283
/ 3,102); estimable in **100 %** of units; missing/unsupported values are `None`, never 0.
B2 denominators median 3,096 (low education) / 904 (high); B3 same.

**Feature-specific admissibility gates** (one R² per feature on upstream school-utility weights
+ GER_post + child-labour_post; threshold 0.90):

| feature | R² | gate |
|---|---|---|
| B1 | **0.952** | **REJECTED** (effectively a transform of the declared fertility parameters) |
| B2 | 0.106 | admissible |
| B3 | 0.116 | admissible |

**4-class nearest-centroid classifiers** (chance 0.25; accuracies are descriptive; p-values are
blocked seed-permutation diagnostics, not preregistered significance tests; Holm across the
three held-out features):

| feature | held-out acc (n=240) | perm p | Holm | replication acc (n=240) | exploratory pattern |
|---|---|---|---|---|---|
| B1 | 0.950 | 0.0005 | 0.0015 | 0.946 | **none** (gate-rejected; cannot support separation) |
| B2 | **0.425** | 0.0005 | 0.0015 | **0.417** | **admissible separation pattern** (exploratory) |
| B3 | 0.292 | 0.066 | 0.066 | 0.363 | none (held-out fails) |

**s=0 control (descriptive only, NOT a formal chance test):** B1 0.304, B2 0.254, B3 0.233
(chance 0.25). The s=0 null shares one upstream input per seed group across labels while its
fertility histories are independently drawn per label (recorded deviation); therefore the null
classifier accuracies are descriptive and do not establish a validated control.

**Caveats (binding):** each world uses its own calibration-chosen nuisance vector, so classifier
separation is conditional on and potentially confounded by nuisance differences and cannot be
attributed uniquely to a mechanism label; a matched-nuisance analysis is **NOT IMPLEMENTED**.
The gate here uses school-utility weights (matching the pre-registration; note the handed-off
mapping text describing a fertility-parameter gate is inconsistent with the code). The
classifier/permutation/Holm machinery is an explicit exploratory deviation from the
pre-registration's binomial analysis. The fertility layer is a minimal approximation, not a
DHS-transportable fertility model. **Fertility-stratum macro FE and a formal full-control
validation are NOT IMPLEMENTED.**

---

## 4. Audit-item evidence (what this run does and does not settle)

| audit item | status in this run | evidence |
|---|---|---|
| M1 all six specs executed | **PASS** | 6 specs × 5 worlds × 2 doses × 7 outcomes × 5 groups × 10 blocks = 21,000 fits |
| M2 s=0 included in matrix | **PASS** | `null` world present in every fit/comparison |
| M3 true 5-year windows | **PASS** | S2/S5 lag = 5 (20 obs/country) vs S1/S4 lag = 10 (15 obs); unit test asserts this |
| M4 10 independent country blocks | **PASS** | fresh draws per block; namespaced seed collision test passes for all 3,200 block×country×world seeds |
| M5 cluster-robust over countries, not binomial | **PASS** | CR1 country-cluster SE inside every fit; paired block t (df 9) for contrasts; no binomial CIs |
| M6 seeds/rank/departures recorded | **PASS** | seeds, hashes, failures, departures in this report + `PRE_REGISTRATION_MAPPING.md` |
| B2 Phase B WOMEN 400 → 4,000 | **PASS** | design records 4,000 women/unit |
| B3 B1 within-mother + denominators | **PASS** | within-mother paired intervals with explicit, large denominators; `None` not 0 |
| B4 feature-specific gates | **PASS** | one R² gate per feature (B1 rejected, B2/B3 admissible) |
| B5 independent s=0 draws, no relabelled clones | **PARTIAL** | fertility histories independent per label; upstream aggregate input shared per seed group (recorded deviation, descriptive only) |
| Rm secondary diagnostic | **NOT IMPLEMENTED** | explicitly out of this run; not assessed |
| predictive discrimination (matrix) | **NOT IMPLEMENTED** | TOST-only path per mapping |
| Amendment_01 design | **NOT IMPLEMENTED / DECLINED** | declined as confirmatory design by Codex; retained as proposed follow-up; no run used it |

What would be needed before any confirmatory claim: a committed amended design with
per-outcome justified standardised margins and multiplicity control; predictive discrimination;
matched-nuisance and formal null-control validation; Rm; and Codex's recorded review of the
smoke and design. None of that is claimed here.

---

## 5. Shutdown readiness

- No jobs of ours are running on region-42 (verified after completion); the box is otherwise
  idle for this programme.
- All results were pulled to the Mac and **sha256-verified local==server**, then committed to
  git together with this report, logs, pilot evidence and exact commands/hashes.
- Old exploratory outputs and Codex's server smoke directory (`/root/work/codex-audit-smoke-20261124/`)
  and the preservation tar (`/root/work/PRESERVE_20261124/`) were **not modified**.
- **Trey can stop (关机, not release) region-42 after this report is committed**: the disk
  persists through shutdown, and no server-only artefact is the sole copy of any result. Final
  shutdown should be coordinated with Trey; re-running would require the box to be up again.
