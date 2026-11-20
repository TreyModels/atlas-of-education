# E2 — Cohort arithmetic and conservation stress (known-answer)

Command: `"$PY" exp/kat_cohort.py --csv <out>/kat_cohort.csv`  (exit 0 on all checks)

This is an **independently named new implementation, not a reproduction** of massabm/triad.
Full output: `logs/phase0_results.txt` block 3. Raw per-year ledger: `kat_cohort.csv`.

== 3. known-answer cohort arithmetic (E2 core, independent new implementation) ==
KNOWN-ANSWER COHORT ARITHMETIC TEST (independent new implementation)
  world: N=200/cohort, 10 grades, seats=60, vacancies=150, T=40
  C1 people conservation per cohort: PASS
  C2 fixed seats never overfilled: PASS
  C3 enrolment stock identity: PASS
  C4 money conservation + endowment never overdrawn: PASS
  C5 jobs: formal<=vacancies, formal+informal==labour force: PASS
  C6 nonnegativity / finiteness: PASS
  C7 probabilities in [0,1]: PASS
  C8 limit cases (seats=0, seats>=N): PASS
  C9 enrolment-cap stress: PASS
  KNOWN ANSWER admission share (all pass, zero dropout), constant across matured cohorts: 0.3000  (must equal min(SEATS,N)/N = 0.3000)
  KNOWN ANSWER final money_cum (must be ~0): 0.00e+00
  KNOWN ANSWER startup endowment drawn: 0 of 4000 (remaining 2530); fiscal warm-up is an explicit stock, not a hidden subsidy
  failures: 0

