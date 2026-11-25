# Shadow Education & Contest Gate — Papers A/B

**Status: partial deposit. Drafts only; not peer-reviewed, and some claimed results are not yet backed by
committed code/data in this repository.** Branch `research/shadow-education-contest-2026-11-25`
(base `research/binding-gate-2026-11-25` @ `68da16e`). Deposited 25 Nov 2026 from the Atlas bridge handoff
`95831e67` (Gemini, 05:20Z) and attachment `ac57ffc8` (05:21Z).

## What is actually in this directory

| item | status | notes |
|---|---|---|
| Paper B — HK/South Korea comparative study | **RECEIVED** | `paper_b_hk_korea/Shadow_Education_Arms_Race_HK_Korea_APA.docx`, sha256 `fe63be84…b9602`; 4 embedded charts, also extracted as PNGs in `figures/` |
| Paper A — general mechanism (SSA) | **NOT RECEIVED** | only a Google Doc ID was supplied (see `paper_a_general_mechanism/README.md`); no file was attached |
| Tullock `contest` gate engine patches (`engine/eduengine/core.py`, `modules/tutoring.py`) | **NOT RECEIVED** | described in the handoff but no patch/code attached |
| `run_hk_korea_comparative.py` | **NOT RECEIVED** | — |
| Results JSONs (Exp 1, Exp 3, Exp 4, Exp 5, HK/Korea) | **NOT RECEIVED** | five named JSON files in the handoff; none attached |
| Paper A APA `.docx` | **NOT RECEIVED** | — |

The handoff asked to commit all of the above. Only Paper B's `.docx` was actually supplied; the rest is
recorded in `code/MISSING_ARTIFACTS.md` rather than fabricated.

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
├── paper_a_general_mechanism/
│   └── README.md                   ← status: NOT RECEIVED (Google Doc ID only)
├── paper_b_hk_korea/
│   ├── Shadow_Education_Arms_Race_HK_Korea_APA.docx
│   ├── README.md                   ← calibration + 14-arm counterfactual summary (author-reported)
│   └── figures/fig1..fig4.png      ← extracted from the docx
└── code/
    └── MISSING_ARTIFACTS.md        ← exact files needed to verify the claimed results
```

## Provenance

- Bridge handoff: `95831e67-3219-4dbb-b789-6c74bc333e7d` (2026-11-25T05:20:26Z, gemini → all).
- Bridge attachment: `ac57ffc8-b541-44b0-bb5d-56d4a08a7e9c` (2026-11-25T05:21:07Z), file
  `Shadow_Education_Arms_Race_HK_Korea_APA.docx`, bytes 642,328, sha256
  `fe63be84fe873ef57f1dde5ae0d588077d957b75d127b7a656a7fc884d8b9602` (verified on receipt).
- This deposit: additive only; no engine files changed; no `main`; no force.
