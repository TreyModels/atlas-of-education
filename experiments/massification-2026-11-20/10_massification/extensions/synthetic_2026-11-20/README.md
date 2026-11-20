# synthetic_2026-11-20 — synthetic-data workbench

**Status: SYNTHETIC / DESCRIPTIVE-METHODOLOGICAL. Not evidence. No causal claims. No real country is modelled.**

A workbench that grows a labelled synthetic panel from **declared literature equations and declared facts**, so the
programme can test predeclared mechanisms (schooling flow, occupation mix, queues, takeoff) without pretending
synthetic output is observed data. It does not read any observed country series at runtime; the only observed numbers
encoded are the declared targets recorded in `generator_v1/RUN_MANIFEST.json` (`targets_encoded`).

## Map

| path | what it is |
|---|---|
| `MODEL_ARCHITECTURE.md` | user's specification restated as a layered design directive; includes dated amendments (A1: education → complexity) |
| `equations/EQUATION_REGISTER.csv` / `.md` | 43 literature relationships: form, parameters, status (`equation-in-literature` / `narrative-only` / `programme-invented` / `programme-estimated`), implementation site |
| `facts/STYLIZED_FACTS.csv` / `.md` | 53 provenance-labelled facts (35 VERIFIED-FROM-DISK; 6 SIMULATED, 5 DISPUTED, 4 MODEL-OUTPUT-NOT-FACT, 3 REPORT-ONLY-UNRELIABLE) a generator may reproduce; §12 records the completion/GER measurement note |
| `generator_v0/` | arithmetic skeleton (demand ceiling, capacity gate, law push, cohort flow, PHL-like): 32 countries × 55 years × 4 levels = 7,040 rows |
| `generator_v1/` | layered, tiered, occupation-aware generator (takeoff regime, sector mix, job ladder, rank/queue matching, composition growth): 30 countries × 56 years × 4 levels = 6,720 rows; **authoritative delivery** with `FINDINGS.md`, `TUNE_LOG.md`, `PARAMS.md`, `RUN_MANIFEST.json` |
| `FINDINGS.md` | the honest read-out: v0's two disclosed failures, v1's authoritative A–F table, the load-bearing seat-cap finding, and the completion/GER measurement insight |

## v1 predeclared checks (authoritative)

**A PASS but target-encoded · B FAIL · C PASS (half structural) · D PASS · E PASS · F PASS.** Check A's four
level-specific PHL supply paths are interpolated through the declared anchors, so "one parameterisation, no
per-level rescue" is **not** met; check B's headline literacy-vs-schooling pattern **survives the removal of its own
mechanism** (takeoff and job-ladder ablations) and is therefore **non-diagnostic**. Full table and diagnosis in
`FINDINGS.md` §3–§4. An earlier intermediate run of the same day (A–D FAIL) is withdrawn; see `generator_v1/TUNE_LOG.md`.

## Verification at packaging (controller, 2026-11-20)

- `generator_v1` file hashes match the worker's authoritative list (`sim_v1.py` `a03fa0cb…`,
  `synthetic_panel_v1.csv` `cf8dfbcb…`, `reproduction_checks_v1.csv` `0914e3c7…`,
  `reproduction_checks_detail_v1.csv` `fcbc7255…`, `RUN_MANIFEST.json` `f9e3640e…`).
- Two fresh runs of `sim_v1.py` into separate directories were **byte-identical to each other and to the delivered
  results CSVs**.
- accounting gate (check F) exact to 2e-16: cohort conservation, GER ≤ 105, sector and occupation shares sum to 1,
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

1. `FINDINGS.md` (what passed, what failed, what is load-bearing, why it matters)
2. `MODEL_ARCHITECTURE.md` (what the model is supposed to be; Amendment A1 = the user's education→complexity model)
3. `facts/STYLIZED_FACTS.md` then `equations/EQUATION_REGISTER.md` (what it is allowed to reproduce)
4. `generator_v1/PARAMS.md` + `generator_v1/TUNE_LOG.md` (the declared parameter block and the honest tuning trail)
