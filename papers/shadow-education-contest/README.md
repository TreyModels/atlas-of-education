# Shadow Education & Contest Gate — Papers A/B

**Status: partial deposit, updated 2026-11-25 14:05 CST. The exact patched engine and the tested runner were
received, applied and run — the 540-run HK/Korea CF4 job reproduces the supplied reference output to the last
floating-point bit (SIMULATION). The canonical all-in-one bundle has been integrated: Paper A draft docx,
GPU scripts, and the reference output are now in this directory.** Branch
`research/shadow-education-contest-2026-11-25` (base `research/binding-gate-2026-11-25` @ `68da16e`).
Deposited 25 Nov 2026 from the Atlas bridge handoff `95831e67` (Gemini, 05:20Z) and attachment `ac57ffc8`
(05:21Z); exact code and all-in-one bundles received later the same day.

## What is actually in this directory

| item | status | notes |
|---|---|---|
| Paper B — HK/South Korea comparative study | **RECEIVED** | `paper_b_hk_korea/Shadow_Education_Arms_Race_HK_Korea_APA.docx`, sha256 `fe63be84…b9602`; 4 embedded charts, also extracted as PNGs in `figures/`. Draft; author-reported. |
| Paper A — general mechanism (SSA) | **RECEIVED (draft)** | `paper_a_general_mechanism/When_Fee_Abolition_Meets_Rationed_Gates_APA.docx`, 369,246 bytes, sha256 `39092abb…0c91`; manuscript deposited as received. Its simulation/identifiability numbers are **not** reproduced here (author-reported) — see `paper_a_general_mechanism/README.md` |
| Bundled results JSON (Exp 1, 3, 4, 5, Paper B) | **RECEIVED (author-reported)** | `code/results/verified_results_2026_11_25.json`, sha256 `b14e2816…b1de`; a self-reported JSON, not a committed run |
| Contest-gate spec (`core.py` / `tutoring.py` additions) | **RECEIVED (superseded by the exact patch)** | `code/contest_gate_spec.md`, sha256 `4c470ba3…d2d2`; a description, kept for history. The exact patched files below are authoritative. |
| **Exact patched `engine/eduengine/core.py`, `modules/tutoring.py`** | **RECEIVED & APPLIED** | byte-identical to the bundle (`core.py` sha256 `618bd6dd…fb4f`, `tutoring.py` `b2d213b6…4308`); applied with `code/contest_gate.patch` (`35b1480a…1f9f`), which equals `git diff` of the two files |
| HK/Korea runner (`run_hk_korea_comparative.py`) | **RECEIVED, TESTED, RAN** | sha256 `dd0b1d8d…bcec`; replaces the earlier incompatible `da07107c…`; unmodified run — see `code/RUNNER_STATUS.md` |
| Reproduced run output (18 arms × 30 seeds = 540) | **RECEIVED FROM RUN** | `code/results/hk_korea_comparative_with_cf4.json`, sha256 `c1fa0926…2e99`; 540/540, exit 0, 178.65 s; SIMULATION |
| Bundle reference output (comparison target) | **RECEIVED, committed for audit** | `code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json`, sha256 `851bb1df…e41b`; supplied with the bundles, unmodified |
| CF4a/CF4b reproduction + evaluation record | **WRITTEN** | `code/REPRODUCTION_CF4_2026-11-25.md`; comparison + per-arm numbers + verdict, SIMULATION |
| RTX 3080 Ti GPU job scripts | **RECEIVED (deposited)** | `code/rtx3080ti_gpu_scripts/` — `README_RTX3080TI.md`, `gpu_bray_abc_and_contest_surface.py`, `gpu_e1_q3_wild_cluster_ri.py`; deposited here from the canonical bundle; **not run on this branch** (the GPU lane runs them separately) |
| Five individual result JSON files | **NOT RECEIVED as files** | their contents appear bundled inside `verified_results_2026_11_25.json` |

## Headline reproduction result (SIMULATION)

- 540/540 runs (18 arms × 30 matched seeds), `exit 0`, 178.65 s on the Mac venv (Python 3.10.2, NumPy 2.2.6).
- **Numerically identical to the supplied reference output**: all `total_spend_index` (2 d.p.) values and all
  non-numeric fields equal; 9,174/9,180 seed-level values and 842/846 summary values exactly equal; the
  remaining differences are last-bit floating-point (max abs 4.4e-16 summary, 3.6e-15 seed rows) plus
  `elapsed_seconds` (165.47 → 178.65). Not a byte-identical file; no substantive discrepancy.
- **CF4a/CF4b fail the stated Win-Win criterion** (spend index < 80 **and** elite Q5 share below baseline, in
  **both** HK and KR). CF4a: HK fails on elite capture (+2.28 pp vs baseline), KR passes. CF4b: spend 90.88
  (HK) / 88.04 (KR) ≥ 80, though elite share falls in both. The only arm meeting the criterion is the single
  effort-cap arm **CF1b**. The pre-stated Exp-7 falsifier is **not met**. Full numbers:
  `code/REPRODUCTION_CF4_2026-11-25.md`.

## Read this before citing

- **Paper B** is a simulation study. Its four charts were checked for internal consistency against the
  handoff numbers (they match). The code that produced the *bundle reference* run (18 arms, 540 runs,
  `N=300`, `T=46`) is now committed and was reproduced here, but the **draft manuscript describes a
  different design** (author-reported 14 arms, 420 runs, `N=400`, `T=70`). The draft's calibration and
  counterfactual table is therefore **not** reproduced by this run — only the 18-arm reference output is.
  Treat the manuscript's numbers as author-reported; cite the reproduced 18-arm run only as SIMULATION.
- The reproduced run's own result **contradicts** the draft's reading that wage compression paired with
  caps/seats reaches the Win-Win Zone: in this specification every ΔV-compression arm raises elite Q5 share
  relative to baseline, and the composites CF4a/CF4b miss the criterion. Report the negative result.
- **Paper A's** headline claims (Tullock contest H2, the `t*` duration analysis, the identifiability theorem,
  the 74.88% calibration) still have **no committed code or data** in this repository and were **not** run
  here, even though the **draft manuscript is now received** (`When_Fee_Abolition_Meets_Rationed_Gates_APA.docx`).
  Its empirical E8 figures spot-check consistent with the committed E8 record; its simulation/identifiability
  claims remain author-reported. See `RECONCILIATION.md` and `paper_a_general_mechanism/README.md`. Do not
  cite them as verified.
- The committed Atlas records remain the authority for the empirical E8/RI/gender numbers and for the
  phase/equifinality simulation. Those are listed in `RECONCILIATION.md` with their branch SHAs.

## Files

```
papers/shadow-education-contest/
├── README.md                       ← this file
├── RECONCILIATION.md               ← claimed vs committed numbers; what must not be cited yet
├── NEXT_EXPERIMENTS.md             ← Gemini's proposed Exp 2/6/7/8; Exp 7 now run (falsifier not met)
├── RESEARCH_AGENDA_AND_EXPERIMENTS.md
├── paper_a_general_mechanism/
│   ├── When_Fee_Abolition_Meets_Rationed_Gates_APA.docx  ← RECEIVED (draft)
│   └── README.md                   ← status: RECEIVED as draft; claims still unverified
├── paper_b_hk_korea/
│   ├── Shadow_Education_Arms_Race_HK_Korea_APA.docx
│   ├── README.md                   ← calibration + 14-arm counterfactual summary (author-reported)
│   └── figures/fig1..fig4.png      ← extracted from the docx
└── code/
    ├── MISSING_ARTIFACTS.md             ← what is still missing / what has since arrived
    ├── RUNNER_STATUS.md                 ← runner reproduced; bundle verified
    ├── RUN_ATTEMPT_2026-11-25.md        ← first attempt failed; second attempt succeeded (update appended)
    ├── REPRODUCTION_CF4_2026-11-25.md   ← comparison + CF4a/CF4b evaluation (SIMULATION)
    ├── contest_gate.patch               ← exact bundle patch (= git diff of the two engine files)
    ├── contest_gate_spec.md             ← received spec (superseded; kept for history)
    ├── run_hk_korea_comparative.py      ← tested bundle runner (unmodified run)
    ├── compare_cf4_reference.py         ← comparison + CF4 evaluation tool (re-runnable)
    ├── rtx3080ti_gpu_scripts/           ← 3 GPU job files from the canonical bundle (not run here)
    └── results/
        ├── hk_korea_comparative_with_cf4.json           ← reproduced 540-run output (our run)
        ├── reference/hk_korea_comparative_with_cf4_bundle_reference.json  ← supplied reference (audit)
        └── verified_results_2026_11_25.json             ← received self-reported results
```

## Provenance

- Bridge handoff: `95831e67-3219-4dbb-b789-6c74bc333e7d` (2026-11-25T05:20:26Z, gemini → all).
- Bridge attachment: `ac57ffc8-b541-44b0-bb5d-56d4a08a7e9c` (2026-11-25T05:21:07Z), file
  `Shadow_Education_Arms_Race_HK_Korea_APA.docx`, bytes 642,328, sha256
  `fe63be84fe873ef57f1dde5ae0d588077d957b75d127b7a656a7fc884d8b9602` (verified on receipt).
- Exact code bundle received 2026-11-25 (operator): `hk_korea_exact_bundle.zip` sha256
  `e9cc02c2da17906c7bdc706285b723cb1e2058dd803312cb08a41197c425be4e`;
  `hk_korea_contest_code_bundle.zip` sha256
  `da5cd1ee4ae6d00598bf02543545491c60ee1ffc120f98eaae3acce01c74e47f`.
- **Canonical all-in-one bundle** received 2026-11-25: `/tmp/ALL_ATLAS_WORK_2026_11_25.zip`, sha256
  `f602ede3cb6ef147c9211b56f82b4806d065f5bd15c6d30c7de6ff2dc7814f74` (also archived on branch
  `research/atlas-all-work-2026-11-25`). It supersedes the two earlier HK zips: its engine/runner/patch files
  are byte-identical to the ones verified above, and it adds the Paper A draft docx, the three GPU scripts and
  the reference output (`851bb1df…e41b`). Its `verified_results_2026_11_25.json` and Paper B docx are
  byte-identical to the files already deposited here.
- Engine provenance: `68da16e` (base) + `contest_gate.patch` = the bundle engine files = the files in this
  branch; verified in `code/REPRODUCTION_CF4_2026-11-25.md` §1.
- This deposit: additive only; no `main`; no force-push.
