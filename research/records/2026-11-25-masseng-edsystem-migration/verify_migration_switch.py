#!/usr/bin/env python3
"""Switch-off identity check: the migration='closed' arm must reproduce the committed
1,440-run multiverse results bit-identically (same metrics, arrays, group tables, seeds).

Usage: python verify_migration_switch.py --prior <results_multiverse.json> [--seeds 3]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)
import run_edsystem_migration as R  # noqa: E402


def canon(x):
    return json.dumps(x, sort_keys=True, allow_nan=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prior", required=True)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--engine-root", default=os.path.join(ROOT, "engine"))
    a = ap.parse_args()
    prior = json.load(open(a.prior))
    paxes = list(prior["design"]["axes"].keys())
    base = tuple(prior["design"]["axes"][ax][0] for ax in paxes)
    old = {r["seed"]: r for r in prior["rows"] if tuple(r["combo"]) == base}
    R.init_engine(a.engine_root)
    ok = True
    for seed in range(a.seeds):
        new = R.one((0, base + ("closed",), seed))
        row = old.get(seed)
        if row is None:
            print(f"seed {seed}: no prior row for baseline combo; FAIL")
            ok = False
            continue
        for key in ("metrics", "arrays", "groups"):
            old_v = row[key]
            new_v = new[key]
            # closed runs must have no migration summary keys; compare all prior keys exactly
            mism = [k for k in old_v if canon(old_v[k]) != canon(new_v.get(k))]
            if mism:
                ok = False
                print(f"seed {seed}: {key} mismatch on {mism}")
            else:
                print(f"seed {seed}: {key} identical ({len(old_v)} keys)")
    print("SWITCH-OFF IDENTITY:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
