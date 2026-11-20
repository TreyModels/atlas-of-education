#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BUILD_FROM_BASE -- assemble code/sim_v1_5_bimodal.py from code/_template.py and the
frozen base copy, injecting the v1.3 year loop VERBATIM.

Why this exists: the A00 no-re-fit guard (e-i) requires that with bimodal=False and
kappa_link=False the v1.5 code reproduces generator_v1_3/results/synthetic_panel_v1_3.csv
byte for byte. Hand-retyping 350 lines of the year loop is exactly the kind of silent
change the guard exists to catch, so the loop is extracted mechanically from the frozen
file and only the declared insertion points (DESIGN.md sec.2.2, I2-I7) are added.

Injected ranges of base_v1_3_sim.py (== generator_v1_3/code/sim_v1_3.py, sha 70ae8f0e...):
  @@PREAMBLE@@   651-748  state up to the history buffers
  @@LOOP_HEAD@@  750-780  year loop head: X channel, takeoff, capacity, q/Q/class size
  @@BLOCK_A@@    784-823  household demand + rationing, by level  (re-indented +4)
  @@BLOCK_B@@    825-864  survival/completion + out-of-school composition (+4)
  @@LOOP_TAIL@@  866-988  pools, teachers, literacy, attainment, rungs/wages/growth,
                          shadow block, store

The only textual change inside the injected tail is the rung-4 candidate restriction of
I7 (Tier H credential holders only), which is inert when bimodal is False.

Run:  python code/build_from_base.py
"""
import hashlib
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
BASE = CODE / "base_v1_3_sim.py"
TPL = CODE / "_template.py"
OUT = CODE / "sim_v1_5_bimodal.py"

RANGES = {                      # 1-based inclusive line numbers in base_v1_3_sim.py
    "@@PREAMBLE@@": (651, 748, 0),
    "@@LOOP_HEAD@@": (750, 780, 0),
    "@@BLOCK_A@@": (784, 823, 4),
    "@@BLOCK_B@@": (825, 864, 4),
    "@@LOOP_TAIL@@": (866, 988, 0),
}

OLD_MATCH = """        grads_vec = out["grads"][:, t]
        cand = grads_vec * seek + queue_carry
        remaining = cand.copy()
"""
NEW_MATCH = """        grads_vec = out["grads"][:, t]
        cand = grads_vec * seek + queue_carry
        remaining = cand.copy()
        # ---- I7: the rung-4 rank order is drawn from Tier H credential holders only ----
        # (declared: a Tier O credential confers no rung-4 rank). Identity when OFF.
        if bimodal:
            _h3 = (float(out["grads_H"][3, t]) / float(grads_vec[3])
                   if float(grads_vec[3]) > 1e-12 else 1.0)
            cand_H3 = float(cand[3]) * _h3
        else:
            cand_H3 = float(cand[3])
"""

OLD_POOL = "            poolv = float(remaining[r:].sum())\n"
NEW_POOL = ("            poolv = (cand_H3 if (r == 3 and bimodal)\n"
            "                     else float(remaining[r:].sum()))\n")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    base_sha = sha(BASE)
    if base_sha != "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877":
        raise SystemExit("REFUSING: base_v1_3_sim.py sha256 mismatch: %s" % base_sha)
    lines = BASE.read_text().splitlines(keepends=True)
    tpl = TPL.read_text()

    for marker, (a, b, ind) in RANGES.items():
        if tpl.count("#" + marker) != 1:
            raise SystemExit("REFUSING: marker %s occurs %d times"
                             % (marker, tpl.count("#" + marker)))
        chunk = "".join(lines[a - 1:b])
        if ind:
            chunk = "".join((" " * ind) + ln if ln.strip() else ln
                            for ln in chunk.splitlines(keepends=True))
        if marker == "@@LOOP_TAIL@@":
            if chunk.count(OLD_MATCH) != 1:
                raise SystemExit("REFUSING: I7 anchor not found exactly once")
            chunk = chunk.replace(OLD_MATCH, NEW_MATCH)
            if chunk.count(OLD_POOL) != 1:
                raise SystemExit("REFUSING: rung pool line not found exactly once")
            chunk = chunk.replace(OLD_POOL, NEW_POOL)
        tpl = tpl.replace("#" + marker + "\n", chunk)
    if "@@" in tpl:
        raise SystemExit("REFUSING: an unsubstituted marker remains")
    OUT.write_text(tpl)
    print("wrote %s  (%d lines, sha256 %s)" % (OUT, len(tpl.splitlines()), sha(OUT)))


if __name__ == "__main__":
    main()
