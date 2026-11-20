# synthetic_2026-11-20 — synthetic-data workbench

**Status: SYNTHETIC / DESCRIPTIVE-METHODOLOGICAL. Not evidence. No causal claims. No real country is modelled.**

A workbench that grows a labelled synthetic panel from **declared literature equations and declared facts**, so the
programme can test predeclared mechanisms (schooling flow, occupation mix, queues, takeoff) without pretending
synthetic output is observed data. It does not read any observed country series at runtime; the only observed numbers
encoded are the declared targets recorded in `generator_v1/results/RUN_MANIFEST.json`.

## Map

| path | what it is |
|---|---|
| `MODEL_ARCHITECTURE.md` | user's specification restated as a layered design directive; includes dated amendments (education → complexity) |
| `equations/EQUATION_REGISTER.csv` / `.md` | 43 literature relationships: form, parameters, status (`equation-in-literature` / `narrative-only` / `programme-invented` / `programme-estimated`), implementation site |
| `facts/STYLIZED_FACTS.csv` / `.md` | 53 provenance-labelled facts (35 VERIFIED-FROM-DISK; 6 SIMULATED, 5 DISPUTED, 4 MODEL-OUTPUT-NOT-FACT, 3 REPORT-ONLY-UNRELIABLE) a generator may reproduce |
| `generator_v0/` | arithmetic skeleton (demand ceiling, capacity gate, law push, cohort flow, PHL-like): 32 countries × 55 years × 4 levels = 7,040 rows |
| `generator_v1/` | layered, tiered, occupation-aware generator (takeoff regime, sector mix, job ladder, rank/queue matching, composition growth): 30 countries × 56 years × 4 levels = 6,720 rows; **2 of 6 predeclared checks pass** |
| `FINDINGS.md` | the honest read-out, including v0's two disclosed failures and v1's A–F check table |

## Verification at packaging

- `generator_v1/results/*.csv` reproduced **byte-identically** by two clean re-runs (and identical to the delivered
  copies): `synthetic_panel_v1.csv` sha256 `d27957be…3103a2b`.
- accounting gate (check F) exact to 1e-16: cohort conservation, GER ≤ 105, sector and occupation shares sum to 1,
  no negative stocks.
- `RUN_MANIFEST.json` + `SHA256SUMS.txt` built by `../build_package.py`; verify with
  `shasum -a 256 -c SHA256SUMS.txt` from this directory.

## Reproduce

```bash
VENV="/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"
cd generator_v1/code && "$VENV" sim_v1.py
cd ../../generator_v0/code && "$VENV" sim.py
```

## Read order

1. `FINDINGS.md` (what passed, what failed, why it matters)
2. `MODEL_ARCHITECTURE.md` (what the model is supposed to be)
3. `facts/STYLIZED_FACTS.md` then `equations/EQUATION_REGISTER.md` (what it is allowed to reproduce)
4. `generator_v1/PARAMS.md` (the declared parameter block, mirrored from the run manifest)
