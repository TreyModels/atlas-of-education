#!/usr/bin/env python3
"""Step 3: final multiple imputation (M=20) of the six education series, then write the panel.
Needs validation_*.json (spread factor and trustworthy horizon per series)."""
import sys, json, shutil
import numpy as np
from common import *
from implib import *

M = 20
TARGETS = ["lsc", "sec", "ter", "prm_cmp", "gpi_sec", "gpi_ter"]
MACROS = ["fertility", "life_exp", "u5mr", "urban", "gdppc_log"]
OTHER = ["electricity", "wage_emp", "tax", "agri_va", "emp_agri", "flfp"]
aux = dict(np.load(f"{OUT}/aux.npz"))
X, ng, names = build_cells(aux)
rng = np.random.default_rng(777)
imp, flag, summ = {}, {}, {}
for T in TARGETS:
    v = json.load(open(f"{OUT}/validation_{T}.json"))
    y = to_panel(load(T)); lo, hi = v["lo"], v["hi"]
    y = np.clip(y, lo, hi)
    mod = Model(T, y, X, ng, lo, hi)
    d = mod.draw(M, v["kappa"], rng)
    h = horizon(y)
    ok = np.isfinite(y) | (h <= v["max_horizon_years"])
    d = np.where(ok[None], d, np.nan)
    d[:, np.isfinite(y)] = np.broadcast_to(y, d.shape)[:, np.isfinite(y)]
    imp[T] = d.astype(np.float32)
    flag[T] = np.where(np.isfinite(y), 0, np.where(np.isfinite(d[0]), 2, -1)).astype(np.int8)
    summ[T] = dict(observed=float(np.isfinite(y).mean()), after=float(np.isfinite(d[0]).mean()), horizon=v["max_horizon_years"],
                   kappa=v["kappa"], countries_modelled=int(mod.use.sum()), countries_total=NC)
    print(T, summ[T], flush=True)
for k in MACROS:
    lr = aux[f"lr_{k}"]
    imp[k] = np.broadcast_to(lr, (M,) + lr.shape).astype(np.float32)
    flag[k] = np.where(np.isfinite(aux[f"obs_{k}"]), 0, np.where(np.isfinite(lr), 1, -1)).astype(np.int8)
    summ[k] = dict(observed=float(np.isfinite(aux[f"obs_{k}"]).mean()), after=float(np.isfinite(lr).mean()))
    print(k, summ[k], flush=True)
np.savez_compressed(f"{OUT}/imputed_panel.npz", **{f"imp_{k}": v for k, v in imp.items()}, **{f"flag_{k}": v for k, v in flag.items()})
json.dump(summ, open(f"{OUT}/coverage_summary.json", "w"), indent=1)
# ---- write JSON series in the same layout as /root/work/data (rows [iso3, year, value]) ----
D = sys.argv[1] if len(sys.argv) > 1 else "/root/work/data_imputed"
os.makedirs(D, exist_ok=True)
dirs = ["mean"] + [f"m{m + 1:02d}" for m in range(M)]
for dd in dirs:
    os.makedirs(f"{D}/{dd}", exist_ok=True)
    for k in OTHER + ["meta"]:
        shutil.copy(f"{DATA}/{k}.json", f"{D}/{dd}/{k}.json")
os.makedirs(f"{D}/flags", exist_ok=True)
for k, arr in imp.items():
    for m in range(M):
        json.dump(panel_to_rows(arr[m]), open(f"{D}/m{m + 1:02d}/{k}.json", "w"))
    json.dump(panel_to_rows(np.nanmean(arr, 0)), open(f"{D}/mean/{k}.json", "w"))
    fl = flag[k]
    json.dump([[REG[i], int(YEARS[j]), int(fl[i, j])] for i in range(NC) for j in range(NY) if fl[i, j] >= 0], open(f"{D}/flags/{k}.json", "w"))
open(f"{D}/README.txt", "w").write("Imputed panel, 1950-2023. mean/ = average over 20 imputations; m01..m20 = individual imputations; "
    "flags/ rows are [iso3, year, 0 observed | 1 long-run source | 2 modelled]. Same layout as /root/work/data. gdppc_log is in LEVELS (as in the original file). "
    "Series without a long-run source (electricity, wage_emp, tax, agri_va, emp_agri, flfp) are copied unchanged. See research/records/2026-11-23-imputed-panel/README.md\n")
print("written", D)
