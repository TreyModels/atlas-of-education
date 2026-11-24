# Letter for DeepSeek - pick up here

From: Claude (Sonnet 5.5), working with Trey Menefee. Written 24 Nov 2026.
To: DeepSeek, running on the server Trey is setting up when he gets home.

Trey will connect you to a server and a GitHub checkout of `TreyModels/atlas-of-education`. This letter says where things stand, what to do in what order,
and what not to trust. Read it before touching anything. Everything below is checkable in the repo.

## 1. The situation in six lines
- The programme (education, fertility, farm labour, 1960-2024, ~200 countries) has **measurement, sequencing and falsification results and no identified causal mechanism**. Treat any sentence that says "X causes Y" as a bug.
- Seven paper drafts were fixed and pushed on 24 Nov (`fix/*-2026-11-24` branches). The plan is **four papers**: sequencing ("schools before factories"), a merged fertility audit, a short shape note, a methods note. See `research/records/2026-11-24-assessment-and-next-experiments/PAPER_PLAN.md`.
- Two findings from today change those drafts: the **"7%" labour-demand figure is a data-start artefact** (the series start in 1991), and **"robust everywhere" does not certify a homogeneous effect** (known-truth simulation). Both are in `CLAIMS_LEDGER.md` and `TEXT_FIXES.md` of that record.
- Today's new analyses (this folder, scripts + outputs, all reproducible in seconds) found: the "91% schooling first" depends on the schooling threshold (65-97%); a cleaner placebo is inconclusive; backcasts work for some series and not for GDP.
- Gemini wrote a runbook (`gemini/Next_Tests_Runbook.md`). I reviewed it in `gemini/REVIEW.md`. Do not run its scripts as written; use mine or fix them first.
- You are the one with the server. Most of what remains needs more compute or network than my sandbox had.

## 2. Rules (non-negotiable)
1. **Never push to, force-push, rewrite or delete an existing branch.** New branch per job: `research/<topic>-2026-11-NN`. Do not open pull requests unless Trey asks.
2. **Write `PRE_REGISTRATION.md` first** (question, data, specification, decision rule) and commit it before you run anything. Do not change the decision rule after seeing results; if you must, say so in the report.
3. **Report everything**, including nulls, failures and runs you discard. Save raw logs. Record the git commit, input hashes, seeds and wall time.
4. **Recompute before you quote.** Every number from a paper, from Gemini or from me must be reproduced by a script you ran, or labelled UNVERIFIED.
5. **No secrets in the repo or in chat**: no passwords, tokens, SSH keys, API keys. If git push fails for lack of credentials, leave the results in a folder and tell Trey.
6. **Associations are associations.** Say "predicts", "is associated with". Reserve causal wording for an event study with checked pre-trends, and then say "consistent with".
7. **Imputed or synthetic data must be labelled** (tier: observed / reconstructed from retrospective data / model-imputed) and carry an interval. Never test a relationship using cells imputed from one of the variables in that relationship.
8. Shut the rented instance down when a job finishes; it bills by the hour. Long runs go in `nohup`/`tmux` and must be resumable or restartable.

## 3. Setup (about 10 minutes)
```bash
# AutoDL: enable the accelerator first if GitHub is slow:  source /etc/network_turbo
git clone --filter=blob:none https://github.com/TreyModels/atlas-of-education.git atlas && cd atlas
git fetch origin 'refs/heads/*:refs/remotes/origin/*'
git checkout -b research/<your-topic>-$(date +%F) origin/research/assessment-and-next-experiments-2026-11-24
python3 -m venv .venv && . .venv/bin/activate && pip install numpy pandas scipy statsmodels matplotlib requests
# reproduce this session's results (must match the committed files exactly):
cd research/records/2026-11-24-next-tests/results
for s in q1_threshold_sweep q2_adult_stock_placebo q3_form_race q5_backcast_validation; do python3 -I ../scripts/$s.py ../data > $s.rerun.txt; done
```
See also `research/records/2026-11-24-assessment-and-next-experiments/RUN_ON_SERVER.md`. To read a file on another branch: `git show origin/<branch>:<path>`.
GPU is not needed; the work is CPU-bound.

## 4. What to do, in order
Detailed specs, decision rules and runtimes are in `research/records/2026-11-24-assessment-and-next-experiments/NEXT_EXPERIMENTS.md` (E1-E17, N1-N8) and `q4_methods_params.json` here.

**Step 0 - verify (30 min).** Re-run the four scripts above and the simulation (`../2026-11-24-assessment-and-next-experiments/scripts/known_truth_sim.py 100 400`, ~6 min). Confirm byte-identical outputs. Read `gemini/REVIEW.md`. Check whether `/root/work/data` and `/root/work/groups/out/final400.pkl` exist on the box (Gemini says yes; I could not verify). That decides E0.

**Step 1 - methods paper (the only job that truly needs the big machine).**
- E1: `GM_R=1200` run of `run_multiverse400.py` (first 400 draws must reproduce `final400.pkl`); then BH and BY verdicts for all 272 links at R = 74/400/800/1200 and split-halves at 1200. About 3 hours on 16 cores.
- E2: known-truth simulation with the real estimator, regimes A, W, B, C, D, S (see `q4_methods_params.json`), 200 replicates, R in {74, 400, 1200}.
- E3: add the heterogeneity condition to the verdict rules and re-label the 5 links that "travel".
- Deliver: `results/verdict_by_R.csv`, a one-page `REPORT.md`, and a yes/no on each of: (a) does the BY-certified tier change; (b) how many "robust" links are concentrated in a minority of countries.

**Step 2 - sequencing paper.**
- E6: rebuild the demand-timing test with series that exist before 1990 (GGDC 10-Sector, Penn World Table, WDI urbanisation and sector value added). The old 7% figure must not be re-derived; it is an artefact.
- E8: fee-abolition event study. Verify the 12 dates against primary sources (conflicts: Cameroon 1999/2000, Ghana 1997/2005, Ethiopia 1994/1995, Tanzania 2001/2003, Malawi 1994/1995, Mozambique 2004/2005), then use a staggered-adoption-robust estimator (Callaway-Sant'Anna or Sun-Abraham; keep TWFE for comparison). Outcomes: primary GER, then lower-secondary GER at t+5..t+10.
- Extend `q1_threshold_sweep.py`: add smoothing windows 3/5/7, and a left-truncated survival version of the take-off dating (N3 in the experiment list).
- Deliver a table of the forward share across all definitions and a recommendation for how Paper 1's abstract should state it.

**Step 3 - fertility audit.**
- E11: the change-on-change placebo ladder on the 23 Nov battery panel (`corr-battery-2026-11-23`; raw files via `corr-rebuild/scripts/download_raw.sh`).
- Resolve the Q2 discrepancy: `effective_fertility` and `tfr_observed_1950plus` give opposite lead/lag patterns in `results/q2_adult_stock_placebo.txt`. They should be the same series after 1950. Find out why (definition, smoothing, sample) before using either.
- E12: DHS stratified pull (`api.dhsprogram.com`). Check indicator IDs via `/rest/dhs/indicators` first.

**Step 4 - shape paper.**
- E14/E15: extend `q3_form_race.py` to the US, Japan, Germany, UK, Canada, Australia (download long-run TFR from Human Fertility Database after a free registration, or OWID; pass the CSV as the optional second argument, columns `iso3,year,tfr`). Keep the double-logistic in the race.
- E16: add region fixed effects and 1960 TFR to `../2026-11-24-assessment-and-next-experiments/scripts/n4_gdp_mortality.py`; is starting child mortality a proxy for initial development?

**Step 5 - backcast protocol (optional, high value).** Extend `q5_backcast_validation.py`: widen intervals until 80% coverage holds in the rich-to-poor scenario; add the retrospective-data route (DHS birth histories for fertility and child mortality; cohort-age attainment from censuses for schooling) as a separate, non-model tier; test a hierarchical Bayesian version. Do not impute any series from the others in a relationship under test.

## 5. Known weaknesses in what I am handing you
- `known_truth_sim.py`: simplified estimator, 8 groupings, three of four verdict tiers; I changed the data-generating process and one rule after seeing early results (documented in the earlier record's README). It is a design check only.
- `q2`: lead/lag with two trending series cannot separate common trend, anticipation (quantity-quality) and a schooling effect; the two fertility outcomes disagree.
- `q3`: 9 countries; pre-1950 series is a modelled reconstruction; the transition-end rule is mine.
- `q5`: "truth" for 1950-1989 is itself modelled; intervals are too narrow in the rich-to-poor case; GDP is not recoverable.
- `q1`: reproduces the paper's definitions exactly, but those definitions (schooling +1.0 year in 10, release -3 points in 10, release series from 1991) are themselves choices.
- Unverified anywhere: Gemini's +0.05 +/- 0.19 provenance, 60%/75% sign-flip shares, CR.3 67.5% -> 75.0%, the model-race percentages (49/29/7%), the pronatalist +0.035 over 38 policies, the 5-of-272 "travel everywhere" count.

## 6. Questions for Trey (leave them in your REPORT.md; do not block on them)
1. Where is the multiverse panel (`GM_DATA`)? If `/root/work/data` on the box is it, say so in the report.
2. Do you want the "7%" text fixes (`TEXT_FIXES.md`) applied to the three drafts on new branches, or left until the experiments are in?
3. Is the Philippine demand-rivals negative-result note wanted as a fifth paper? (Not before the CHED headcount table is checked against its PDF.)
4. Human Fertility Database needs a free registration; who registers?

## 7. How to report back
Each job: a new branch, a folder `research/records/<date>-<topic>/` with `PRE_REGISTRATION.md`, `scripts/`, `results/`, `REPORT.md` (status, numbers, deviations from the plan, what changed in the paper plan), and a one-line update appended to `research/records/2026-11-24-assessment-and-next-experiments/CLAIMS_LEDGER.md` **on your own branch** (do not edit mine in place on the pushed branch).
If something is wrong in my files, say so plainly in your report; I would rather be corrected than cited.
