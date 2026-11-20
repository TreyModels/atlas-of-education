"""Timing / reconstruction probe (scratch, not a result). Reads ONLY frozen synthetic panels."""
import csv, sys, time
from pathlib import Path
import numpy as np

CODE = Path(__file__).resolve().parent
FROZEN = CODE / "frozen"
sys.path.insert(0, str(FROZEN))
import sim_v1_6_repair as S

SYNTH_DIR = (CODE / "frozen").resolve().parents[2] / "synthetic_2026-11-20"
S.ROOT = SYNTH_DIR / "generator_v1_6_repair"
S.SYNTH = SYNTH_DIR
S.MASS = SYNTH_DIR.parents[1]
S.DATA = S.MASS / "data"
V13 = SYNTH_DIR / "generator_v1_3" / "results" / "synthetic_panel_v1_3.csv"

def load_band_pop(path, country="SYN00_PHL_LIKE"):
    coh = {}
    pop = {}
    band = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["country"] != country:
                continue
            y = int(float(r["year"]))
            pop[y] = float(r["population"])
            if r["level"] == "primary":
                band[y] = float(r["band_population"])
    return coh, pop, band

t0 = time.time()
_coh, pop, band = load_band_pop(V13)
S_path = np.array([band[y] / S.P["band_share"][0] for y in S.YEARS])
Ppop = np.array([pop[y] for y in S.YEARS])
print("recon rows", len(S_path), "took", time.time() - t0)
print("S[0]", S_path[0], "Pop[0]", Ppop[0], "S[-1]", S_path[-1])

S.load_observed_phl_paths = lambda: (S_path, Ppop, {}, {}, {})

rng = np.random.default_rng(S.SEED)
cps = S.apply_declared(S.draw_countries(rng))
cp = cps[0]
print("cp0", cp["name"], "shadow type?")
t0 = time.time()
res = S.simulate_country(cp, np.zeros(S.T), np.zeros(S.T), S_path, Ppop,
                         sh_in=None, beh=S.SHADOW_BEHAV, bimodal=True)
print("one PHL sim (no shadow host) took %.2fs" % (time.time() - t0))
print("demand_share upper 2024", res["demand_share"][2, 2010 - 1970], res["demand_share"][2, 2024 - 1970])
print("p_school upper", res["p_school"][2, 2024 - 1970], "p_both", res["p_both"][2, 2024 - 1970])
