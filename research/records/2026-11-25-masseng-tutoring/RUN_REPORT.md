# RUN REPORT — MASSENG v5 R1 tutoring coupling

**SIMULATION / first-pass coupling prototype. No causal claims. No secrets or credentials were written; SSH key
authentication only. The AutoDL instance was NOT shut down (per instruction); only short jobs were started and all
have finished. A pre-existing `/root/work/shadow` directory belonging to another task was left untouched.**

## 1. Branch and base

- New branch: `research/masseng-tutoring-2026-11-25` (worktree `~/atlas-work-2026-11-23/masstutor`).
- Base: `research/codex-masseng-staging-2026-11-24` @ `bac3a7c` (additive; base branch never rewritten).
- Engine file **not modified**: `git diff bac3a7c -- research/masseng-v6/model/masseng/engine5.py
  research/masseng-v6/model/masseng/data.py research/masseng-v6/model/countries/PHL
  research/masseng-v6/model/outputs/PHL/v5` is empty. The coupling is a new file
  `research/masseng-v6/model/masseng/tutoring.py` (subclass of `Model5`).
- Ported standalone copies (not imports): `research/records/2026-11-25-masseng-tutoring/ported/` from
  `research/shadow-equations-2026-11-25` @ `fdc8da0` (`shadow_model.py`, `bray_reality_check.py`,
  plus the committed 8k-draw result for reference).

## 2. Server deployment

- Server: `ssh -p 45973 root@connect.cqa1.seetacloud.com` (key auth; **no password used or stored**), host
  `autodl-container-a8f742b5ee-292349c5`, 192 cores, 1007 GB RAM, RTX 4090 D 24.5 GB, `/root` 30 GB with 30 GB free.
- Deploy target: `/root/work/masseng-tutoring/` (`model/` = copy of `research/masseng-v6/model`, `record/scripts`,
  `record/ported`, `record/results`, `record/logs`).
- Python `/root/miniconda3/bin/python` 3.10.8, numpy 1.24.1. **scipy 1.9.3 was installed this session**
  (`/root/miniconda3/bin/pip install scipy==1.9.3`, from the configured aliyun mirror) because
  `masseng/data.py::decile_income_multipliers` imports `scipy.stats.norm` and the base conda env did not have scipy.
  This is the only environment change; it was installed into the existing base env, no new env or credentials.
- Pristine baseline check on the server before any coupling run: the committed PHL v5 R1 fit reproduces its
  committed held-out three-GER RMSE **16.925** exactly (`logs/diag_env.log`), and the engine has no score-gate,
  no quota and no configured capacity rule for PHL (`model.exam=None`, `us_cap=None`,
  `annual_capacity=None`, `tertiary_entry_exam=None`) — this is the source of the §2 boundary table.

Commands (all from `/root/work/masseng-tutoring/model`, `PYTHONPATH=/root/work/masseng-tutoring/model`):

```bash
# 0. environment / baseline / boundary check
/root/miniconda3/bin/python /root/work/masseng-tutoring/record/scripts/diag_env.py

# 1. demand-mix anchor + check (50,000 prior draws, 48 workers)
/root/miniconda3/bin/python /root/work/masseng-tutoring/record/scripts/run_bray_check.py --draws 50000 --workers 48

# 2. switch-off identity (full 1940-2024 and short 2000-2024)
/root/miniconda3/bin/python /root/work/masseng-tutoring/record/scripts/verify_switch_off.py

# 3. channel decomposition (6 arms: learn/financing 2x2 + ban + baseline)
/root/miniconda3/bin/python /root/work/masseng-tutoring/record/scripts/channel_decomposition.py

# 4. coupled grid: 53 deterministic runs, 60 workers
/root/miniconda3/bin/python /root/work/masseng-tutoring/record/scripts/run_coupling.py --workers 60
```

Analysis (CPU-only, no model import; reads the committed results):

```bash
python3 research/records/2026-11-25-masseng-tutoring/scripts/analyse_results.py
```

## 3. Wall times and outputs

| step | wall time | output |
|---|---:|---|
| `diag_env.py` | 2.7 s | `logs/diag_env.log` |
| `run_bray_check.py --draws 50000 --workers 48` | **6.7 s** | `results/bray_check.json` |
| `verify_switch_off.py` (full + short, two full runs each) | full 2.061 s + 1.406 s; short 0.309 s + 0.307 s | `results/switch_off_identity.json` |
| `channel_decomposition.py` (6 coupled runs) | < 15 s | `results/channel_decomposition.json`, `results/channel.log` |
| `run_coupling.py --workers 60` (53 configs) | grid **10.403 s**, total 13.7 s | `results/coupling_raw.json.gz` (2.1 MB gz), `results/summary.json`, `results/tables.md` |
| `analyse_results.py` | < 3 s | same summary/tables |

Total server compute for the study is well under one minute of grid wall time; the instance was left running.

## 4. Acceptance A1 — switch-off identity (PASS)

`TutoringModel5(switches={'tutoring': False})` vs untouched `Model5`, same fit, same data:

- full run: 85 years, **318 numerical comparisons, all byte-identical**;
- short run: 25 years, **138 numerical comparisons, all byte-identical**;
- the only `Result.extra` difference is the always-attached diagnostics key `tutoring`.

`results/summary.json:switch_off_arm_equals_pristine = true`; the grid's OFF arm agrees with the pristine
baseline at every recorded year. See `MASSENG_TUTORING_COUPLING.md` §6.1.

## 5. Hashes (sha256)

Deployed code and inputs (also in `logs/server_environment.log`):

| file | sha256 |
|---|---|
| `masseng/tutoring.py` (new module) | `2fa27b1295e08677bdd8c964731bb362fd3a78b92a45ca142110b4de5244d15b` |
| `masseng/engine5.py` (unmodified) | `e01bd54383a7215503c3caff50212c5fcf16312aca9531e10ad810c7a3a5c17c` |
| `masseng/data.py` (unmodified) | `34f47a17401430d69493f38bb531dec9622f6a73c7d9a25a6c837d921d22cf01` |
| `outputs/PHL/v5/fit_R1.json` | `e0690737d0570e719c20a946b50036d3290a6d1d70689f019ea89ab2d33ef796` |
| `scripts/run_coupling.py` | `f5d928c9e8df2de084aa9b3eaf3cdc62b7e47b3ab7a1b71d5077e59d825c9721` |
| `scripts/verify_switch_off.py` | `de948dcabe488fb62fbca691eab686d98394a4610df4ae5d94747d204f31b9ac` |
| `scripts/run_bray_check.py` | `393f3fab3f2684627eca90eb56b743d41c50ab2fab1140fd4a517475e4f808d9` |
| `scripts/analyse_results.py` | `92adf5d25fb808ba7b64e20f94f349454eb29816cd44ca9b58a902a524f0ab1d` |
| `scripts/channel_decomposition.py` | `018cfe0308bb03f90ae937ce1808bf8988644ff0b5eb623cba96fa97ada1ba33` |
| `scripts/smoke_coupling.py` | `7dc32eabbb4ad787dc357982e764f0d79a5425ed415f3dc4ba0a73b0f7eac897` |
| `scripts/diag_env.py` | `6749e5a0de2dfc775b969eec6d0c0a7b3f9982c70e274efd27cb7aaac0fb3859` |
| `ported/bray_reality_check.py` | `85e9b809daabdc20abbc6c182543f6c8edcd1d8b4e0a39162eb2a6c3109bc17a` |
| `ported/shadow_model.py` | `dc14fadfa63c01f30677948d6aedc878e883a14bb31186e78700e4fc976783ba` |

A full manifest of every committed code/result file is in `results/MANIFEST.sha256`.

## 6. Files

- `MASSENG_TUTORING_COUPLING.md` — main deliverable (system frame, engine-boundary table, coupling design, results,
  reality check, missing mechanisms).
- `PRE_REGISTRATION_COUPLING.md` — declared design, grid, decision/acceptance rules.
- `scripts/` — `diag_env.py`, `run_bray_check.py`, `verify_switch_off.py`, `channel_decomposition.py`,
  `smoke_coupling.py`, `run_coupling.py`, `analyse_results.py`.
- `ported/` — verbatim standalone copies + provenance README.
- `results/` — `coupling_raw.json.gz` (all 53 runs, full indicator series + decile flows), `summary.json`,
  `tables.md`, `bray_check.json`, `channel_decomposition.json`, `switch_off_identity.json`, `channel.log`,
  `MANIFEST.sha256`.
- `logs/` — `server_environment.log` (env + hashes), `diag_env.log`.
- New engine-side code: `research/masseng-v6/model/masseng/tutoring.py`.

## 7. What was not run, and why

- **Quota vs score-bar admissions**: MASSENG v5 R1 has no score, no quota and no contest-success admission margin.
  Not run; cannot be coupled without a new admissions subsystem (declared in the report).
- **Jobs/pay, rural/urban, migration, borrowing**: no such state in the engine. Not run; listed as missing.
- **Tutoring supply / market clearing / teacher withholding**: no supplier module. Fee fixed exogenous.
- No Bayesian/ABC posterior was computed for the coupled model: the engine is deterministic and the tutoring
  parameters are not estimated, so this would have implied a likelihood that does not exist. Seed draws are
  parameter-uncertainty draws, stated as such.
- The instance was **not** shut down and no other user's process was touched.
