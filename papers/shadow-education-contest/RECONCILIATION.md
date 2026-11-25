# Reconciliation — claimed Paper A/B numbers vs committed Atlas records

**Purpose.** The bridge handoff asks to commit "verified" numbers. Several of those claims have no committed
code/data in this repository, and some conflict with committed records. This file separates the three tiers:
**COMMITTED** (citable), **AUTHOR-REPORTED** (not yet verifiable here), **CONFLICT** (must not be cited as is).

## Committed reference values (citable)

| result | value | evidence |
|---|---|---|
| E8 CS ATT at abolition | 12.44362392207772; 95% CI [−2.3558, 27.2431]; SE 7.5507 | `research/e6e8-sequencing-2026-11-25` @ `bd782be`, `results/e8_event_SE.PRM.ENRR_verified8.csv` |
| E8 post ATTs (+1…+6) | 23.8244, 25.9429, 22.1208, 25.1932, 28.5608, 25.9224; mean 25.2607 | same |
| E8 Fisher RI | p_date 9.999e−05; p_country 5.999e−04 (T0), 2.9997e−04 (Tpost); B = 10,000 × 2 | `research/e8-fisher-ri-2026-11-25` @ `fb8b67e` |
| Gender split | D = −3.94395, paired 95% CI [−8.7178, +0.2946] | `research/gender-split-e6e8-2026-11-25` @ `b4eb680` |
| E6 ordering | demand-first 10.0–24.1%; schooling-first 21.5–46.3% (strict 58.3–71.4%) | `research/e6e8-sequencing-2026-11-25` @ `bd782be`; dossier line 115: auditor "76–90%" does **not** reproduce |
| Equifinality (SIMULATION) | within-gate 176 observed vs null 190.52 (p = 0.838); total pairs 319,600 = 159,600 within + 160,000 cross | `research/equifinality-phase-2026-11-25` @ `ab415f2` |
| Contest gate in committed engine | **NOT-IMPLEMENTED**: only `bar`/`quota`; unknown kind silently becomes quota | `…equifinality-phase/PRE_REGISTRATION.md` @ `078cc13`; `engine/eduengine/core.py`:164, 369–371 |
| `t*` bulge | **NOT-ESTIMABLE**: `L_primary` sourced 0/8 in-repo; no proxy | `research/bulge-arrival-2026-11-25` @ `1b91a71` |

## Paper A claims — status

| claim | tier | issue |
|---|---|---|
| Exp 5 on-impact predicted +11.60/+13.48 vs empirical +12.44 | AUTHOR-REPORTED | the empirical +12.44 **matches** the committed E8 value; the simulated predictions have no committed run |
| Exp 1 `t*` live-WDI, 7,290 obs, 2,500 permutations | AUTHOR-REPORTED | data/code not committed. Committed bulge record says `t*` NOT-ESTIMABLE in-repo (0/8). A live WDI `SE.PRM.DURS` pull could legitimately make it estimable, but the series, hashes, sample, and runner must be committed before the null result can be cited |
| Exp 3 Tullock `contest`, 1,640 runs, H2 +0.1086 (p = 1.9e−11) | **CONFLICT** | committed engine has no `contest` kind; committed phase prereg/report records NOT-IMPLEMENTED. The patch, runner, seeds, and results JSON are not in this deposit |
| Exp 4 identifiability (rank 5/7, cond 1.09e13 → 7/7, 43.81) | **CONFLICT / QUARANTINED** | no committed code/results; the shadow-equations review branch is quarantined (`264c059`) and must not be cited |
| E6 "76–90% schooling-first" (appears in an earlier Paper A draft) | **CONFLICT** | the committed record shows this auditor figure does not reproduce; E6 is 10.0–24.1% demand-first, 21.5–46.3% schooling-first |
| Earlier Paper A draft Table 1 event column (+1 22.12, +2 24.18, +3 25.60, +6 28.56; on-impact CI [+7.12, +17.76]) | **CONFLICT — but NOT the manuscript now received** | does not match the committed verified-8 table above (e.g. committed +1 = 23.8244; on-impact CI [−2.3558, 27.2431]). The received `When_Fee_Abolition_Meets_Rationed_Gates_APA.docx` (2026-11-25) instead quotes +12.44 on impact, +25.26 mean over +1…+6, range +22.12 to +28.56 — **consistent** with the committed table. Any earlier draft must still be corrected |

## Paper B claims — status

| item | status |
|---|---|
| 14 arms, 420 runs, 30 matched seeds, HK/Korea calibration | **AUTHOR-REPORTED**; `run_hk_korea_comparative.py` and `hk_korea_comparative.json` not received. The committed tested runner is an **18-arm / 540-run, `N=300`, `T=46`** design, which is not the draft's 14-arm / 420-run / `N=400` / `T=70` design |
| Four embedded charts | extracted and checked against the handoff numbers: **all four match** (calibration, counterfactual spend, seat expansion, trade-off frontier) |
| Headline counterfactuals (tax +50% raises spend; seat expansion raises participation/spend; wage compression is the win-win route) | **AUTHOR-REPORTED**; simulation, uncalibrated beyond the stated benchmarks. The committed 18-arm run (below) is the only committed simulation evidence, and it **contradicts** the "wage compression + caps/seats reaches the Win-Win Zone" reading on the pre-stated criterion |
| Exact patched engine + tested runner (bundle) | **COMMITTED & VERIFIED**: files byte-identical to the bundle; patch = `git diff`; provenance `68da16e` + patch = bundle |
| 18-arm / 540-run bundle reference output | **COMMITTED & REPRODUCED (SIMULATION)**: our run matches the reference to last-bit floating point (all 2-d.p. figures identical); `code/REPRODUCTION_CF4_2026-11-25.md` |
| **CF4a/CF4b** combined win-win arms (Exp 7) | **COMMITTED RUN — FALSIFIER NOT MET (SIMULATION)**: on the stated criterion (spend index < 80 AND elite Q5 share below baseline, both jurisdictions), CF4a fails in HK (+2.28 pp elite share), CF4b fails in both (spend 90.88/88.04); only the single-lever CF1b passes |

## Verdict rule for future citation

- Empirics: cite only the COMMITTED values above.
- Phase/equifinality: cite `ab415f2`; it is descriptive and **not** evidence beyond chance.
- Contest gate: the patch is now committed and applied on this branch (`code/contest_gate.patch`, engine files
  byte-identical to the bundle); the 540-run HK/Korea job is committed and reproduced against the supplied
  reference. It is **SIMULATION** evidence only — no empirical claim may rest on it.
- Paper B's 18-arm CF4 run: citable as SIMULATION with its actual numbers (including the CF4a/CF4b negative
  result). The draft manuscript's 14-arm calibration/counterfactual table remains AUTHOR-REPORTED and is not
  reproduced by this run.
- Live-WDI `t*`, identifiability, calibration, and the rest of Paper A: **cannot be cited as verified** until
  the missing artifacts are committed with code, data, seeds, and hashes.
- Paper A must correct the empirical table if the earlier draft is the deposited version.

## Update 2026-11-25 14:00 CST — exact bundle applied, 540-run CF4 job reproduced

The exact patched `engine/eduengine/core.py` + `engine/eduengine/modules/tutoring.py`, the tested runner and
`contest_gate.patch` were received in the operator bundle (sha256 `e9cc02c2…` / `da5cd1ee…`), verified
byte-identical, and applied additively on this branch. The 540-run job (`18 arms × 30 seeds`) completed
`540/540` in 178.65 s (exit 0) and matches the supplied reference output to last-bit floating point: all
2-d.p. `total_spend_index` values and all non-numeric fields equal; 9,174/9,180 seed-level and 842/846
summary numeric values exactly equal; remaining differences ≤ 3.6e-15 (seed) / 4.4e-16 (summary) plus
`elapsed_seconds`. **SIMULATION.**

CF4a/CF4b evaluation (criterion: spend index < 80 AND elite Q5 share below baseline, in **both** HK and KR):

| arm | HK | KR | both |
|---|---|---|---|
| CF4a (ΔV −50 % + cap −50 %) | FAIL — spend 43.78 ✓, elite Q5 48.64 % vs 46.36 % baseline (+2.28 pp) ✗ | PASS — 46.50 ✓, 34.10 % (−2.02 pp) ✓ | **FAIL** |
| CF4b (ΔV −50 % + seats) | FAIL — spend 90.88 ✗ (elite 35.98 %, −10.38 pp) | FAIL — spend 88.04 ✗ (elite 26.51 %, −9.62 pp) | **FAIL** |
| CF1b (cap −50 %, single lever) | PASS — 67.39 ✓, 41.96 % (−4.40 pp) ✓ | PASS — 76.42 ✓, 26.39 % (−9.73 pp) ✓ | **PASS (only arm)** |

So the pre-stated Exp-7 falsifier ("CF4a/CF4b land in the Win-Win Zone in both jurisdictions") is **not met**;
the only arm satisfying the criterion is the single effort cap. The draft's wage-compression reading should
not be cited as reproduced. Full record: `code/REPRODUCTION_CF4_2026-11-25.md`.

## Update 2026-11-25 13:29 CST — later artifacts received

Gemini subsequently attached `verified_results_2026_11_25.json` (sha256 `b14e2816…b1de`),
`run_hk_korea_comparative.py` (`da07107c…4926`) and `contest_gate_spec.md` (`4c470ba3…d2d2`). Status:

- The JSON is **self-reported**, not a committed run. It records the same Exp 1/3/4/5 and Paper B numbers as
  author-reported and does not by itself resolve the conflicts above.
- The spec is a **description** of the contest-gate patch, not the patched `core.py`/`tutoring.py`; without
  those files the committed engine still has no `contest` kind.
- The runner does **not** fit the committed API (`Engine(modules, **params)`, no `.history`, `contest` absent),
  so it cannot reproduce Paper B against this tree. See `code/RUNNER_STATUS.md`.

Paper B remains a draft / author-reported simulation. The citable committed results are unchanged.

## Update 2026-11-25 14:05 CST — canonical all-in-one bundle integrated

The operator-supplied canonical bundle `/tmp/ALL_ATLAS_WORK_2026_11_25.zip` (sha256
`f602ede3cb6ef147c9211b56f82b4806d065f5bd15c6d30c7de6ff2dc7814f74`; also archived on branch
`research/atlas-all-work-2026-11-25`) has been integrated into this branch. It supersedes the two earlier HK
zips — its engine/runner/patch files are byte-identical to the ones already verified and applied here, and its
`verified_results_2026_11_25.json` (`b14e2816…b1de`) and Paper B docx (`fe63be84…b9602`) are byte-identical to
the files already deposited. It adds:

- **Paper A manuscript** `paper_a_general_mechanism/When_Fee_Abolition_Meets_Rationed_Gates_APA.docx`
  (369,246 bytes, sha256 `39092abb…0c91`). Paper A is therefore **RECEIVED as a draft** — but its Exp 1/3/4/5
  simulations and identifiability theorem are **not** reproduced here (no runner/results were supplied and
  nothing was run). Its empirical E8 figures (+12.44 on impact, +25.26 mean, range +22.12…+28.56) are
  consistent with the committed E8 record; the rest remains author-reported. The earlier conflicting draft's
  table is not this manuscript (see the Paper A claims table above).
- **Three RTX 3080 Ti GPU scripts** under `code/rtx3080ti_gpu_scripts/` (deposited only; not run on this
  branch).
- The **reference output** `hk_korea_comparative_with_cf4.json` (sha256 `851bb1df…e41b`), committed at
  `code/results/reference/` as the comparison target for our reproduced run (sha256 `c1fa0926…2e99`, at
  `code/results/hk_korea_comparative_with_cf4.json`).

The engine patch, the reproduced 540-run CF4 result, and the CF4a/CF4b verdict above are unchanged by this
integration. SIMULATION labels stand.
