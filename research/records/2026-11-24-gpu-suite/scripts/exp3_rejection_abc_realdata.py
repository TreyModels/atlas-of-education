"""EXP-3: Equal-weight Rejection-ABC fit against public World Bank WDI / ILO-UCW series
for the 8 verified E8 SSA countries + 6 comparison countries, with strict 0.80 prior-width gate.
"""
import argparse, json, os
import numpy as np
import pandas as pd
import requests
import cupy as cp
from exp1_unified_gpu_abm import KERNEL_SRC

COUNTRIES = ["MWI", "ETH", "UGA", "LSO", "TZA", "KEN", "MOZ", "GHA", "KHM", "PHL", "VNM", "BEN", "NAM", "SWZ"]
INDICATORS = {
    "prm_enr": "SE.PRM.ENRR",
    "cl_total": "SL.TLF.0714.ZS",
    "cl_work_only": "SL.TLF.0714.WK.ZS",
    "cl_study_work": "SL.TLF.0714.SW.ZS",
}

def pull_wb_targets():
    rows = []
    for name, code in INDICATORS.items():
        url = f"https://api.worldbank.org/v2/country/{';'.join(COUNTRIES)}/indicator/{code}?format=json&per_page=5000&date=1990:2023"
        r = requests.get(url, timeout=30).json()
        if len(r) < 2 or not r[1]:
            continue
        for item in r[1]:
            if item["value"] is not None:
                rows.append({"iso3": item["countryiso3code"], "year": int(item["date"]), "ind": name, "val": float(item["value"])})
    df = pd.DataFrame(rows)
    return df.groupby(["iso3", "ind"])["val"].mean().unstack()

def main(draws=5000, batch_n=50000, out_json="results/exp3_abc_posterior.json"):
    targets = pull_wb_targets().dropna(subset=["prm_enr", "cl_total"])
    print(f"Pulled public WDI/ILO-UCW targets for {len(targets)} countries.")

    mod = cp.RawModule(code=KERNEL_SRC)
    kern = mod.get_function("sim_step")

    rng_np = np.random.default_rng(20261125)
    priors = {
        "w_pov": (0.0, 3.0),
        "w_push": (0.0, 3.0),
        "w_tutor": (0.0, 3.0),
        "div_beta": (0.0, 0.35),
    }

    rng_cp = cp.random.default_rng(12345)
    base_y = cp.exp(rng_cp.normal(0.0, 0.55, size=batch_n, dtype=cp.float32))
    ability = cp.clip(rng_cp.normal(1.0, 0.20, size=batch_n, dtype=cp.float32), 0.3, 1.8)
    state_out = cp.empty(batch_n, dtype=cp.int32)
    tutor_out = cp.empty(batch_n, dtype=cp.int32)
    learn_out = cp.empty(batch_n, dtype=cp.float32)
    work_out  = cp.empty(batch_n, dtype=cp.float32)
    y_hh_out  = cp.empty(batch_n, dtype=cp.float32)

    threads = 256
    blocks = (batch_n + threads - 1) // threads

    tgt_enr = (targets["prm_enr"].mean() / 100.0)
    tgt_cl  = (targets["cl_total"].mean() / 100.0)

    candidates = []
    for d in range(draws):
        w_pov  = float(rng_np.uniform(*priors["w_pov"]))
        w_push = float(rng_np.uniform(*priors["w_push"]))
        w_tut  = float(rng_np.uniform(*priors["w_tutor"]))
        div_b  = float(rng_np.uniform(*priors["div_beta"]))

        kern((blocks,), (threads,), (
            np.int32(batch_n), np.int32(d), np.uint32(777), np.uint32(d + 1),
            np.float32(0.20), np.float32(0.30), np.float32(0.40), np.float32(0.0),
            np.float32(0.60), np.float32(div_b), np.float32(0.55), np.float32(0.85), np.float32(0.32),
            np.float32(w_pov), np.float32(w_push), np.float32(w_tut),
            base_y, ability, state_out, tutor_out, learn_out, work_out, y_hh_out
        ))
        cp.cuda.Stream.null.synchronize()
        s = cp.asnumpy(state_out)
        enr = float(np.mean(s <= 1))
        cl  = float(np.mean(s >= 1))
        dist = float(np.sqrt((enr - tgt_enr) ** 2 + (cl - tgt_cl) ** 2))
        candidates.append({"w_pov": w_pov, "w_push": w_push, "w_tutor": w_tut, "div_beta": div_b, "dist": dist})

    cdf = pd.DataFrame(candidates).sort_values("dist")
    acc = cdf.head(max(10, int(0.10 * draws)))

    ident = {}
    for k, (lo, hi) in priors.items():
        q05, q50, q95 = np.percentile(acc[k], [5, 50, 95])
        ratio = (q95 - q05) / (hi - lo)
        ident[k] = {"q05": float(q05), "median": float(q50), "q95": float(q95), "width_ratio": float(ratio), "identified": bool(ratio <= 0.80)}

    os.makedirs(os.path.dirname(out_json) or ".", exist_ok=True)
    with open(out_json, "w") as f:
        json.dump({"draws": draws, "accepted": len(acc), "batch_n": batch_n, "identifiability": ident}, f, indent=2)
    print(json.dumps(ident, indent=2))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=5000)
    ap.add_argument("--batch-n", type=int, default=50000)
    ap.add_argument("--out", default="results/exp3_abc_posterior.json")
    args = ap.parse_args()
    main(args.draws, args.batch_n, args.out)
