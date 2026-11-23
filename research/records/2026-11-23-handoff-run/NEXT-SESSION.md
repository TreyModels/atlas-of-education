# NEXT SESSION — read this first (written 23 Nov 2026, end of session 2)

User: Dr. Trey Menefee. Explain results in plain words, never with variable names.
$20 plan: be token-cheap. Opus judges and interprets. Use ONE long-lived Sonnet worker and queue new tasks to it.
Do NOT spawn a new agent per task. Agents must push to GitHub after every milestone and send reports of 10 lines or fewer.

## Server
- AutoDL, rented hourly; the address and port change each time.
- Log in by SSH key only: `ssh -i ~/.ssh/autodl_claude -p <port> root@<host>`.
- For a fresh server, the user runs `ssh-copy-id -i ~/.ssh/autodl_claude.pub -p <port> root@<host>` once.
- Python: /root/miniconda3/bin/python. Work dir: /root/work. Set `OMP_NUM_THREADS=1`.
- Don't oversubscribe the 32 cores. The GPU is idle: port the dose model to CuPy/PyTorch, then batch the regressions.

## Branches (all on origin)
| branch | what |
|---|---|
| research/handoff-run-2026-11-23 | jobs 1-6 of the old queue, PUBLISHABLE.md, PLAN_jobs_4_and_7.md, this file |
| research/recompute-2026-11-23 | income-was-not-logged bug fix reruns, +16.05 traced, Boppart w31101 comparison, 380-pair rerun |
| research/grouping-multiverse-2026-11-23 | 7.2M regressions over 179 country groups + random-grouping null |
| research/imputed-panel-2026-11-23 | gap-filling/backcast scripts. The panel itself is on the server at /root/work/data_imputed/. The matrix rerun on it (/root/work/impute/matrix.log, then report_matrix.py) was unfinished |
| research/dose-model-2026-11-23 | individual-level schooling-as-dose model (scenario A individuation vs B development-only). Was still running at handoff; check the branch for status |

Older: research/massification-session-2026-11-22, research/massification-panel-2026-11-22.

## The story so far
**Massification**
- Electricity and wage jobs line up with schooling only when each country is compared with itself.
- Once each country's own trend is controlled, both vanish. A power test shows the test could have seen a real effect, so read this as "can't be separated from development", not "zero".
- Electricity's +16.05 is per standard deviation, about +0.5 point per point.
- Wage jobs: null in every grouping. Cheaper farm inputs: null on paid jobs and births once income is logged.
- Our elasticity of 0.43 is within-country, so it doesn't test Boppart's figure. On a cross-section setup we get 1.4-1.6, close to theirs.

**Fertility**
- Country-level births track child survival and life expectancy, which hold in about 80-95% of groups.
- Once income is logged correctly, schooling loses to income in model averaging (inclusion 0.45 vs 0.97).
- Schooling doesn't beat random groupings.
- The "not luck" result holds but is weaker: 6 of 20,000 under a harder null.
- The individual-level dose model is the real test of the user's hypothesis (kin support, wealth flows up, assortative matching, tempo/quantum, cohort deepening).

## Next jobs (in order)
1. Finish and read the dose model. Answer: does A beat B out of sample? How strong are the kin and cohort-deepening effects? What is the tempo vs quantum split?
2. Finish the imputed-panel matrix rerun. Commit the results and a README.
3. GPU rewrite of the dose model, then rerun with more draws and more random groupings (74 was the actual count; planned 400).
4. Control-set check: add child mortality and women's work as controls. Do not control for things on the causal path, e.g. marriage age when testing schooling to fertility.
5. Get the UN World Marriage Data (the un.org download returned 403). Then do job 7 in PLAN_jobs_4_and_7.md.
6. Papers, ranked in PUBLISHABLE.md:
   - (1) wage jobs to university: a fragile association
   - (2) most development links are country trends in disguise, plus a power-tested method
   - (3) schooling-as-dose model, once job 1 is done
   - Do not submit paper 02 (electricity floor/apex) as written.
