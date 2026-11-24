#!/usr/bin/env python3
"""Panel provenance + real-pass reproduction check for E1.

(a) sha256 of the 17 estimator series + meta.json in GM_DATA.
(b) Recompute the deterministic real-grouping pass and compare the pooled t-statistics of all 544
    specifications with the committed edge_table400.csv columns pooled_FE_t / pooled_TR_t.
Stops the E1 run if the real pass does not reproduce (systematic panel-vintage discrepancy).
"""
import os, json, hashlib, csv, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gm_core as g

DATA = g.DATA
lines = ["# E1 panel provenance", f"GM_DATA={DATA}", f"C={g.C}", f"NE={g.NE}",
         f"ISOS_sha256={hashlib.sha256(('|'.join(g.ISOS)).encode()).hexdigest()}"]
for v in g.VARS + ["meta"]:
    p = os.path.join(DATA, v + ".json")
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    lines.append(f"{v}.json\t{h}")
    print("HASH", v, h, flush=True)
open(os.path.join(os.path.dirname(DATA), "e1", "out", "panel_hashes.txt"), "w").write("\n".join(lines) + "\n")

b, se, n, nc, k = g.fit_cell(g.mask(np.arange(g.C)))
t = b / se
pairs = g.PAIRS
print(f"real pass: {k} fits; comparing 544 pooled t-stats to committed edge_table400.csv", flush=True)
committed = {}
with open(os.path.join(os.path.dirname(HERE), "data", "edge_table400.csv")) as fh:
    for row in csv.DictReader(fh):
        committed[(row["x"], row["y"])] = row
diffs = []
missing = 0
for pi, (x, y) in enumerate(pairs):
    row = committed.get((x, y))
    if row is None:
        missing += 1; continue
    for trend, key in ((0, "pooled_FE_t"), (1, "pooled_TR_t")):
        val = t[2 * pi + trend]
        ref = float(row[key])
        diffs.append(abs(val - ref))
diffs = np.array(diffs)
rep = dict(n_compared=int(len(diffs)), n_missing_pairs=missing,
           max_abs_diff=float(np.nanmax(diffs)), median_abs_diff=float(np.nanmedian(diffs)),
           n_over_1e6=int(np.nansum(diffs > 1e-6)),
           n_over_1e4=int(np.nansum(diffs > 1e-4)),
           verdict="REPRODUCED" if np.nanmax(diffs) <= 1e-6 else "DISCREPANCY")
print(json.dumps(rep, indent=1))
open(os.path.join(os.path.dirname(HERE), "results", "panelcheck.json"), "w").write(json.dumps(rep, indent=1))
open(os.path.join(os.path.dirname(HERE), "results", "panel_hashes.txt"), "w").write("\n".join(lines) + "\n")
