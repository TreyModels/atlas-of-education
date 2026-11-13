# Teacher-supplied tutoring: an agent-based model (Cambodia)

Work in progress, 9 November 2026. The model, calibration and analysis code are finished and tested. The paper is not written yet.

## What this is

72 teachers and 1,260 pupils in six Siem Reap–style schools (three lower secondary with Grade 9, three high schools with Grades 9 and 12, two parallel classes per grade, four subjects). Each teacher chooses whether to sell tutoring to its own pupils and the parallel class, how much regular content to withhold, or to take a side job. Each pupil chooses, subject by subject, to buy from the own teacher, the other teacher, a commercial provider, or no one.

Three rival explanations for why so much tutoring comes from pupils' own teachers:

| Variant | What drives own-teacher tutoring |
| --- | --- |
| `thin` | The timetable is too short for the curriculum (no withholding pays) |
| `diversion` | Teachers withhold content that only they fully cover in paid lessons |
| `favour` | Buying from your own teacher brings a benefit of its own (grades, relationship) |
| `full` | Diversion and favour both allowed |

Each variant is calibrated by ABC-SMC to seven published patterns from Bray et al. (2016, 2018): participation overall (81.9%), in Grade 9 (74.7%) and Grade 12 (89.8%); the small urban–rural gap (83.5% vs 80.9%); own-teacher (57.7%) and other-teacher (40.9%) shares of tutoring; about half of teachers tutoring (13 of 24 interviewed); and a small commercial share. A run "fits" when every pattern is within its tolerance band (`calibrate.py`).

Full model description: `paper/odd.md` (ODD protocol).

## Requirements

Python 3.10 or later with numpy, scipy, pandas and matplotlib:

```sh
pip install -r requirements.txt
```

## Run it

```sh
python3 smoke.py                 # one run plus 40 random runs, a few seconds
./run_all.sh                     # full pipeline, about 1 hour on 2 cores
./run_all.sh quick               # smaller calibration, about 15 minutes, for checking
```

`run_all.sh` runs, in order:

1. `calibrate.py --n 1000` — prior sample, used for prior-wide sensitivity (`results/pilot2.csv`)
2. `smc.py` — ABC-SMC for each variant (`results/posterior_<variant>.json`, log in `results/smc_log.txt`)
3. `analysis.py` — posterior summaries, policy experiments, signatures, sensitivity (PRCC), robustness to fixed assumptions (`results/summary.json`, `policy_runs.csv`, `robustness_runs.csv`)
4. `make_figures.py` — `paper/figures/`

Use more cores with `--procs` on `calibrate.py` and `smc.py`, and in the `Pool(2)` line of `analysis.py`.

## Policies tested

Ban on selling to own pupils; conditional pay (0.3 bonus for not selling to own pupils, as in New Generation Schools); ten more points of class time; commercial entry. Each is run on every calibrated parameter set with the same random seed as its baseline.

## Interim results included (`results/`)

- `thin`, `diversion`, `favour`: calibration finished (all reached tolerance 1.0). `full` was still running when this package was made.
- Evidence at tolerance 1 (prior probability of fitting all seven patterns, uniform priors): thin 3.1e-6 (90% bootstrap interval 0 to 9.4e-6); diversion 5.9e-6 (1.4e-6 to 1.1e-5); favour 0 in 4,000 proposals.
- **Open check before trusting the favour result:** its last generation had a low effective sample size (71), and none of the 4,000 evidence proposals fit, although 2.8% of that generation's proposals did. The likely reading is that favour fits only on favourable random worlds, not across seeds. Rerun with more particles, or re-simulate the favour posterior with new seeds, before drawing a conclusion. ABC model choice is fragile in any case (Robert et al. 2011), so treat these numbers as indicative.
- `summary.json` and the figures were produced from the three finished variants. Rerun `analysis.py` and `make_figures.py` once `posterior_full.json` exists.

## Files

| File | Role |
| --- | --- |
| `model.py` | The agent-based model |
| `calibrate.py` | Targets, tolerances, distance; prior sampling |
| `smc.py` | ABC-SMC calibration and evidence estimate |
| `analysis.py` | Policies, signatures, sensitivity, robustness |
| `make_figures.py` | Figures |
| `paper/odd.md` | ODD description (Appendix A of the paper) |

## Sources for the patterns

- Bray, M., Kobakhidze, M. N., Liu, J., & Zhang, W. (2016). The internal dynamics of privatised public education: Fee-charging supplementary tutoring provided by teachers in Cambodia. *International Journal of Educational Development*, 49, 291–299.
- Bray, M., Kobakhidze, M. N., Zhang, W., & Liu, J. (2018). The hidden curriculum in a hidden marketplace: Relationships and values in Cambodia's shadow education system. *Journal of Curriculum Studies*, 50(4), 435–455.

The provider shares (57.7% + 40.9% = 98.6%) are read as main-provider answers and matched to shares of tutoring purchases. Check the question wording in the original instrument.
