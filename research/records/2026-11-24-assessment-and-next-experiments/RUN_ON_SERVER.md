# Running the experiments on a rented server (AutoDL or similar)

These experiments are CPU-bound (many small regressions). **A GPU is not needed**; pick a CPU-only instance if available. 8 cores,
16-56 GB memory and 30 GB disk are enough. E1 (1,200 draws) takes about 3 h on 16 cores, about 6 h on 8.

## One-time setup (Ubuntu 22.04, Python 3.10, Miniconda image)
```bash
# On AutoDL, GitHub may be slow or blocked; enable the academic accelerator first:
source /etc/network_turbo        # (skip on other providers)
git clone --filter=blob:none https://github.com/TreyModels/atlas-of-education.git atlas && cd atlas
git fetch origin 'refs/heads/*:refs/remotes/origin/*'
git checkout -b research/<topic>-$(date +%F) origin/research/assessment-and-next-experiments-2026-11-24
python3 -m venv .venv && source .venv/bin/activate
pip install numpy pandas scipy statsmodels matplotlib
pip freeze > research/records/2026-11-24-assessment-and-next-experiments/requirements.txt
```
To read a script that lives on another branch without checking it out:
`git show origin/research/grouping-multiverse-400-2026-11-23:research/records/2026-11-23-grouping-multiverse-400/scripts/gm_core.py`

## Reproduce this record's results (about 6 minutes in total on one core)
```bash
cd research/records/2026-11-24-assessment-and-next-experiments/results
python3 -I ../scripts/placebo_orthogonal.py ../data            # ~10 s
python3 -I ../scripts/n4_gdp_mortality.py ../data               # ~5 s
python3 -I ../scripts/demand_series_start_check.py ../data      # ~2 s
python3 -I ../scripts/known_truth_sim.py 100 400                # ~5 min; overwrites known_truth_sim.json
python3 -I ../scripts/summarise_sim.py > known_truth_sim_summary.md
```
Compare with the committed files; they must match exactly (seeds are fixed). Report any difference.

## Long runs: keep them alive and resumable
```bash
nohup python3 -I run_multiverse400.py > run.log 2>&1 &     # use tmux/screen if available
tail -f run.log
```
AutoDL stops billing only when the instance is shut down; shut it down when the run finishes. Do not leave it running overnight by accident.

## Saving results back
```bash
git add research/records/<your-record-dir>
git commit -m "Results: <experiment ids>"            # no force pushes, no edits to existing branches
git push -u origin HEAD
```
If `git push` is refused (no credentials on the server), copy the `results/` folder to your computer (AutoDL file manager or `scp`) and
commit from there. **Never paste passwords, tokens or SSH keys into a chat or a file in the repo.**
