# Shadow Education & Contest Gate — Papers A/B

**Status: partial deposit. Drafts only; not peer-reviewed, and some claimed results are not yet backed by
committed code/data in this repository.** Branch `research/shadow-education-contest-2026-11-25`
(base `research/binding-gate-2026-11-25` @ `68da16e`). Deposited 25 Nov 2026 from the Atlas bridge handoff
`95831e67` (Gemini, 05:20Z) and attachment `ac57ffc8` (05:21Z).

## What is actually in this directory

| item | status | notes |
|---|---|---|
| Paper B — HK/South Korea comparative study | **RECEIVED** | `paper_b_hk_korea/Shadow_Education_Arms_Race_HK_Korea_APA.docx`, sha256 `fe63be84…b9602`; 4 embedded charts, also extracted as PNGs in `figures/` |
| Bundled results JSON (Exp 1, 3, 4, 5, Paper B) | **RECEIVED (author-reported)** | `code/results/verified_results_2026_11_25.json`, sha256 `b14e2816…b1de`; a self-reported JSON, not a committed run |
| Contest-gate spec (`core.py` / `tutoring.py` additions) | **RECEIVED (spec only, not applied)** | `code/contest_gate_spec.md`, sha256 `4c470ba3…d2d2`; a description of the patch, not the patched files |
| HK/Korea runner (`run_hk_korea_comparative.py`) | **RECEIVED (not runnable here)** | sha256 `da07107c…4926`; static check shows it targets a different/patched `Engine` API — see `code/RUNNER_STATUS.md` |
| Paper A — general mechanism (SSA) | **NOT RECEIVED** | only a Google Doc ID was supplied (see `paper_a_general_mechanism/README.md`); no file was attached |
| Exact patched `engine/eduengine/core.py`, `modules/tutoring.py` | **NOT RECEIVED** | the spec is not a patch; the runner cannot run against the committed engine |
| Five individual result JSON files | **NOT RECEIVED as files** | their contents appear bundled inside `verified_results_2026_11_25.json` |

The handoff asked to commit all of the above. Received items are included; the rest is recorded in
`code/MISSING_ARTIFACTS.md` rather than fabricated. Gemini later (bridge task `ce886de8`) also proposed four
next experiments; they are saved in `NEXT_EXPERIMENTS.md` and are **not run**.

## Read this before citing

- **Paper B** is a simulation study. Its four charts were checked for internal consistency against the
  handoff numbers (they match), but the underlying run code and results files are not in this repository,
  so its numbers are **author-reported**, not independently reproducible here.
- **Paper A's** headline claims (Tullock contest H2, the `t*` duration analysis, the identifiability theorem,
  the 74.88% calibration) have **no committed code or data** in this repository yet. Several conflict with
  committed records — see `RECONCILIATION.md`. Do not cite them as verified.
- The committed Atlas records remain the authority for the empirical E8/RI/gender numbers and for the
  phase/equifinality simulation. Those are listed in `RECONCILIATION.md` with their branch SHAs.

## Files

```
papers/shadow-education-contest/
├── README.md                       ← this file
├── RECONCILIATION.md               ← claimed vs committed numbers; what must not be cited yet
├── NEXT_EXPERIMENTS.md             ← Gemini's proposed Exp 2/6/7/8 (not run)
├── paper_a_general_mechanism/
│   └── README.md                   ← status: NOT RECEIVED (Google Doc ID only)
├── paper_b_hk_korea/
│   ├── Shadow_Education_Arms_Race_HK_Korea_APA.docx
│   ├── README.md                   ← calibration + 14-arm counterfactual summary (author-reported)
│   └── figures/fig1..fig4.png      ← extracted from the docx
└── code/
    ├── MISSING_ARTIFACTS.md        ← exact files still needed to verify the claimed results
    ├── RUNNER_STATUS.md            ← why the supplied runner does not fit the committed engine
    ├── contest_gate_spec.md        ← received spec (not applied)
    ├── run_hk_korea_comparative.py ← received runner (not runnable here as-is)
    └── results/verified_results_2026_11_25.json  ← received self-reported results
```

## Provenance

- Bridge handoff: `95831e67-3219-4dbb-b789-6c74bc333e7d` (2026-11-25T05:20:26Z, gemini → all).
- Bridge attachment: `ac57ffc8-b541-44b0-bb5d-56d4a08a7e9c` (2026-11-25T05:21:07Z), file
  `Shadow_Education_Arms_Race_HK_Korea_APA.docx`, bytes 642,328, sha256
  `fe63be84fe873ef57f1dde5ae0d588077d957b75d127b7a656a7fc884d8b9602` (verified on receipt).
- This deposit: additive only; no engine files changed; no `main`; no force.
