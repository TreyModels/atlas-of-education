# CORRECTIONS PENDING — audit response (task-22; no new runs until Trey decides)

Trigger: Codex bridge steer `d4b70c8e` (2026-11-24T11:53Z). v2/v2b and Phase B are labelled **EXPLORATORY PENDING REVIEW**; the headline percentages are not directly comparable to E1's 1.8 %.

| # | audit item | status | fix required |
|---|---|---|---|
| B1 | `run_phaseb.py` `countries`/`panels`/`w` scope (pushed `81112ab`) | **FAIL in pushed rev**; server fix `c3a0e3ec…` (`e05763f`) | commit the fixed file; verify hash before run |
| B2 | `fertility.py` `WOMEN=400` vs prereg 4,000 | **FAIL** | set 4,000 (or declare deviation) and rerun at declared power |
| B3 | B1 within-mother birth-spacing + missing denominators | **open** | define within-mother contrast with denominators; smoke test |
| B4 | common admissibility gate across features | **FAIL** | feature-specific R² gates |
| B5 | zero-signal control duplicates observations across labels | **FAIL** | independent s=0 draws per label; no pseudoreplication |
| M1 | 3 of 6 preregistered specs executed | **FAIL** | implement all 6 |
| M2 | s=0 zero-signal world omitted from matrix | **FAIL** | include null world in the matrix as declared |
| M3 | "5y" spec uses 10y differencing | **FAIL** | implement true 5-year windows |
| M4 | blocks reuse the same simulated countries | **FAIL** | independent country draws per block |
| M5 | binomial uncertainty over cells, not clustered | **FAIL** | cluster-robust CIs over countries/blocks |
| M6 | seed/rank audit, departures from prereg | **open** | document every departure |

**Smallest corrected experiment (proposed, NOT run):** 4 worlds + s=0, N=10k, 64 countries, all 6 declared specs, 10 independent country blocks, cluster-robust CIs; Phase B at WOMEN=4,000 with clean independent s=0 and feature-specific gates; 2-seed smoke first; decision by effect size/TOST or predictive discrimination — not "non-significant = equivalent".

**No new scaling runs** until Trey decides.
