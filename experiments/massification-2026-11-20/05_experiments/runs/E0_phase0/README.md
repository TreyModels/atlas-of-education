# E0 — Phase 0 gate: environment, smoke runs, invariants

Full record: `logs/PHASE0_env.txt` (environment + source hashes) and `logs/phase0_results.txt` (runs and exit codes).
```
PHASE0 ENVIRONMENT RECORD
sampled_utc: 2026-11-20T04:16:50Z
os: macOS 26.6.2 25.6.0
arch: arm64
cpu_cores: 8
mem_gb: 8
--- python ---
python 3.11.17
numpy 2.4.6
scipy 1.17.1
pandas 3.1.1
matplotlib 3.11.2
python_exe: /Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python
PYTHONDONTWRITEBYTECODE=1
--- source hashes (sha256) ---
2b6484e7a98866f8362a216b118cf8abbfefc7236b9278d2ec0ac47d6eafeb40  /Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/01_sources/massification_project/code/massabm/massabm/model.py
6a4d133a3369b8a34ceb905dfa4fd66e0a0369b44aa710ab17dc3ec0deffe2d9  /Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/01_sources/massification_project/code/massabm/massabm/params.py
7b22d93cab66f8c4af08f3131800f8dc5489f5f9041cd66dc5b327053314ccea  /Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/01_sources/massification_project/code/triad/triad/model.py
f2e23a62bd78919c229bf24530a25a34b8562aa9d161cc5d240663e396565ddd  /Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/01_sources/massification_project/code/massabm/run.py
--- atlas engine files present ---
atlas_coverage.py
atlas_sobol.py
camchild.py
camchild_record.cjs
camchild_ridge.py
camchild_sobol.py
checks.py
childworld.py
childworld_agealigned.py
childworld_mc.py
childworld_sobol.py
china_page.py
countries
data
eduengine
evaluate_tuning.py
experiments.py
firms
fit_country.py
floorworld.py

--- gates ---
== 1. massabm run.py smoke ==
  basic completion, entry 1990-95 (HS ~2001-05)              0.743   target ~0.55-0.62
  basic completion, entry 2008-12 (SHS ~2020-24)             0.649   target ~0.70-0.73
  basic completion Q1, entry 1985-90                         0.411   target ~0.35-0.40
  basic completion Q5, entry 1985-90                         0.816   target ~0.90+
  degree share, entry 1990-95                                0.196   target ~0.14-0.20
  basic->college transition, entry 2008-12                   0.296   target ~0.70 (SHS grads)
  prof-track entry share, entry 1990-98 (nursing boom)       0.095   target ~0.04-0.06
  OFW professional share of deployments, 2015-23             0.106   target <~0.25 (41% elementary)
  informal share of entrants, 2010                           0.466   target ~0.5-0.6
  tutoring rate at board exam, 2010                          0.921   target high (review centres)
  tutoring rate at basic gate, 2010                          0.069   target thin
  tertiary GPI (college entry F/M), entry 1995-2005          0.835   target ~1.2-1.3
[exit: 0]
== 2. triad emergence --quick ==
  Median year (of 2 runs) each thing first happens:
    state funds upper secondary (>=50%)              30
    half of each cohort completes upper secondary    34
    households' median target reaches tertiary      38
    most firms screen by credential                  66  (urban share then 0.53)
  End state (years 110-139): mean_years 11.69, upper 0.58, tertiary 0.38, cred 0.80, floor 3.93, frontier 4.50, formal 0.49
  Convergence after year 90: mean |employer floor - state funding frontier| = 0.51 levels
[exit: 0]
== 3. known-answer cohort arithmetic (E2 core, independent new implementation) ==
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
== 4. massabm invariant checks ==
  default (N=3000): PASS
```
