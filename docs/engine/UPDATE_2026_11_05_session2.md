# Atlas update, 5 November 2026 (second session): running the to-do list

Worked the P1 items that could be done from the cloud sandbox, in this order. World Bank, UNESCO, PyPI and GitHub were unreachable, so nothing needing them was attempted.

## Done

1. **Child-labour mechanism tests** (`tests/test_camchild.cjs`, 13 → 26). Conservation of money, luxury axiom, income effect of transfers, conditional vs unconditional cash, ban reach. New lever `cashU` (unconditional transfer) in both twins; parity test extended to 10 scenarios.
2. **Monte Carlo manager** (`engine/mc.py`, `engine/test_mc.py`, 15 tests). Routed: `childworld_mc.py` (stored 20,000-world results reproduce exactly), camchild ridge seed check (identical), China stories, and the new strict run. New `childworld_sobol.py`.
3. **Tournament winner under the strict protocol** (`firms/stories_strict.py`). Result: 5.51 pts vs naive 0.89. A negative result, reported as such. See `firms/results/stories_strict.md`.
4. **Round 8 as permanent tests** (`tests/test_round8.py`, 14 tests) and a fix to massabm's CSV writer.
5. **Version control and CI**: repository initialised, no commit; `.github/workflows/ci.yml` written.
6. **Input verification, second pass**: property growth 2018–21 and graduate classes 2019 and 2022 now `v`, values unchanged, so no stored result moves.

## Not done, and what unblocks it

| Item | Blocker |
|---|---|
| Domain check, GitHub repository | needs Trey (no DNS or GitHub access from the sandbox) |
| Licence | Trey's choice; the to-do lists MIT or Apache-2.0 and CC BY 4.0 |
| Survey inputs (MICS, DHS, PLFS) | tables not attached; open internet needed |
| Sector labour demand for China | needs a sourced NBS sector series; none in `data_china.py` |
| Trey to approve survey targets; retune camchild's work side | approval first, then the retune |
| Sit down with Bjørn; template library; book chapter map | people |
| Score the blind forecast | NBS has not released October 2026 |
| WDI/UIS data and the credential-flood rerun | data access |
| Narrative engine, observation equations, fact-book generator, curves register, rival dropout explanations, massabm/triad merge, seasonal cash flows, hard cases | large builds, not started |

## Added later the same day

`docs/chengdu_case_and_classification.md`: the gate-reach classification, shadow education as one variable with a payee, the hours margin, the Chengdu reproduction table and the figures in the two Huizhi documents that need reconciling. New TODO items under §R (proposed next-phase focus, not yet adopted).
