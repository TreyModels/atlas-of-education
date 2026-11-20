# E14 — Actor knockouts (triad necessity + lock-in)

Command: `PYTHONPATH=<work>/triad "$PY" exp/run_triad_E14_E15.py /tmp/massrun/runs/triad 3 2000 2`
reps=3 N=2000 (reduced from the model default 8/3000 for budget; seed dispersion reported).

## Necessity (end state, years 110-139)
```
NECESSITY: remove one or more actors' gain from the credential from year 0. End state, years 110-139.
  household gain removed = formal jobs pay no more than informal work
  employer gain removed  = firms cannot screen by credential (referrals or tests only)
  state gain removed     = the state captures no tax from formal output (rentier)

  WORLD: as built (schooling raises pay inside jobs)
  removed                             years  upper+ tertiary+ cred hiring  floor state funds to
  none (all three active)              11.6    0.58      0.38        0.83    3.9            4.3
  household                             8.2    0.26      0.00        0.78    2.6            3.0
  employer                             10.0    0.58      0.00        0.00    nan            3.0
  state                                10.5    0.52      0.22        0.85    3.4            0.0
  household+employer                    8.2    0.26      0.00        0.00    nan            3.0
  household+state                       7.3    0.18      0.00        0.70    2.4            0.0
  employer+state                        9.6    0.52      0.00        0.00    nan            0.0
  household+employer+state              7.3    0.18      0.00        0.00    nan            0.0
  years added by the full system over all-removed: +4.32; removing one alone costs: household +3.48, employer +1.66, state +1.18

  WORLD: weak skill return (schooling mostly signals)
  removed                             years  upper+ tertiary+ cred hiring  floor state funds to
  none (all three active)              10.0    0.57      0.03        0.89    3.1            3.6
  household                             6.9    0.16      0.00        0.37    2.6            2.9
  employer                              9.8    0.54      0.00        0.00    nan            3.0
  state                                 9.5    0.51      0.00        0.86    3.0            0.0
  household+employer                    7.0    0.16      0.00        0.00    nan            3.0
  household+state                       6.0    0.10      0.00        0.35    2.4            0.0
  employer+state                        9.3    0.47      0.00        0.00    nan            0.0
  household+employer+state              6.0    0.10      0.00        0.00    nan            0.0
  years added by the full system over all-removed: +3.99; removing one alone costs: household +3.07, employer +0.26, state +0.56

Read: "necessary" = removing it alone loses a large share of the deepening. If no single removal matters much,
the actors are substitutes, not a three-part motor. If each matters, it is a motor. Compare the two worlds:
the employer leg can only matter where credentials carry information that productivity alone does not.
```

## Lock-in (end state, years 120-139)
```
LOCK-IN: the same removals, made at year 0 vs. year 90 (after the system matures). End state, years 120-139.

  arm                                       years  upper+ tertiary+ cred hiring  floor state funds to
  full system                                11.5    0.58      0.38        0.83    3.8            4.1
  household removed EARLY (year 0)            8.2    0.26      0.00        0.80    2.6            3.0
  household removed LATE (year 90)            8.1    0.25      0.00        0.73    2.6            3.0
  employer removed EARLY (year 0)            10.0    0.58      0.00        0.00    nan            3.0
  employer removed LATE (year 90)            11.6    0.58      0.38        0.00    nan            4.2
  state removed EARLY (year 0)               10.4    0.52      0.21        0.87    3.4            0.0
  state removed LATE (year 90)               10.5    0.52      0.22        0.85    3.5            0.8
  kin networks restored (year 90)            11.7    0.58      0.37        0.05    4.4            4.6

Read: lock-in = a LATE removal leaves the pipeline much closer to the full system than an EARLY removal does.
If late and early removals end in the same place, there is no lock-in: the pipeline is only as strong as its weakest current support.
Restoring kin networks asks whether the pipeline survives the disappearance of the problem that started it.
```
