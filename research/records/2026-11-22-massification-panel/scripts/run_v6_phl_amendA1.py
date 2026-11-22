"""Amendment A1 runs for PROTOCOL_v6_phl.md (dated 2026-11-22, written after P0-P2 fits were inspected).

Registers two extra specs WITHOUT editing engine_v6_phl.py:
  P0h_con: P0 dials + b_h, b_h >= 0   (eta, eta_x, kappa, b_h)
  P0h_unc: same, b_h in [-6, 12]
These are the properly nested 'add returns to the income+cost benchmark' comparison.
Also supports multistart refits of any registered spec (--multistart SPEC SEED).
"""
import sys, json
from pathlib import Path
import numpy as np
import masseng.engine_v6_phl as E

E.V6_SPECS["P0h_con"] = dict(dials=["eta", "eta_x", "kappa", "b_h"], constrained=True, z=None)
E.V6_SPECS["P0h_unc"] = dict(dials=["eta", "eta_x", "kappa", "b_h"], constrained=False, z=None)


sys.path.insert(0, str(Path(__file__).parent))
import run_v6_phl as R
from masseng.data import Country
from masseng import calibrate5 as C5

OUT = Path("outputs/PHL/v6_phl")
MS = OUT / "multistart"; MS.mkdir(parents=True, exist_ok=True)


def multistart(spec, seed):
    c = Country("PHL")
    rows = C5.build_rows(c)
    train = [r for r in rows if r["role"] == "train"]
    rng = np.random.default_rng(1000 + seed)
    b = E.spec_bounds(spec)
    start = {n: float(rng.uniform(*b[n])) if n in b else None for n in E.fitted_names_v6(spec)}
    start = {k: v for k, v in start.items() if v is not None}
    f = E.fit_v6_phl(c, train, spec=spec, start=start, max_nfev=250, ftol=1e-7)
    f["start"] = start; f["seed"] = seed
    (MS / f"{spec}_seed{seed:02d}.json").write_text(json.dumps(f, indent=2) + "\n")
    print(f"MS {spec} seed{seed}: cost={f['cost']:.3f} nfev={f['nfev']} dials_at_bounds={f['dials_at_bounds']}", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "--fit":
        R.cmd_fit(sys.argv[2])
    elif sys.argv[1] == "--multistart":
        multistart(sys.argv[2], int(sys.argv[3]))
