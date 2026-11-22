#!/usr/bin/env python3
"""Big Monte Carlo: 20,000 no-link worlds and 2,000 country redraws, parallel."""
import json, os, random, statistics
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

NAME = {"fertility": "births per woman", "lsc": "finishing lower secondary",
        "sec": "secondary completion", "ter": "young people in higher ed",
        "gpi_ter": "women vs men in higher ed", "u5mr": "children dying before 5",
        "gdppc_log": "income per person", "flfp": "women in the labour force",
        "electricity": "homes with electricity", "wage_emp": "share of jobs that are paid",
        "urban": "share living in cities", "gpi_sec": "women vs men in secondary",
        "prm_cmp": "primary completion", "life_exp": "life expectancy"}


def load(name):
    with open(os.path.join(DATA, name + ".json")) as f:
        rows = json.load(f)
    return {(r[0], int(r[1])): float(r[2]) for r in rows if r[2] is not None}


def demean(vals, groups):
    acc, n = {}, {}
    for v, g in zip(vals, groups):
        acc[g] = acc.get(g, 0.0) + v; n[g] = n.get(g, 0) + 1
    mean = {g: acc[g] / n[g] for g in acc}
    return [v - mean[g] for v, g in zip(vals, groups)]


def r2_within(y, x, iso, year):
    if len(y) < 100:
        return 0.0
    xw = demean(demean(x, iso), year); yw = demean(demean(y, iso), year)
    mx = statistics.mean(xw); my = statistics.mean(yw)
    sx = sum((a - mx) ** 2 for a in xw) ** 0.5; sy = sum((b - my) ** 2 for b in yw) ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    cov = sum((a - mx) * (b - my) for a, b in zip(xw, yw))
    return 100.0 * (cov / (sx * sy)) ** 2


meta = json.load(open(os.path.join(DATA, "meta.json")))
ok = lambda iso: iso in meta and meta[iso]["region"].strip() != "Aggregates" and len(iso) == 3
V = {k: {kk: vv for kk, vv in load(k).items() if ok(kk[0])} for k in NAME}
F = V["fertility"]


def rows_for(c):
    return [(i, t, F[(i, t + 10)] - v, V[c][(i, t)])
            for (i, t), v in F.items() if (i, t + 10) in F and (i, t) in V[c]]


ROWS = {c: rows_for(c) for c in NAME if c != "fertility"}
BASE = "lsc"
rs = ROWS[BASE]
OBS = r2_within([r[2] for r in rs], [r[3] for r in rs], [r[0] for r in rs], [r[1] for r in rs])
by = {}
for r in rs:
    by.setdefault(r[0], []).append(r)
BLOCKS = []
for iso, b in by.items():
    b = sorted(b, key=lambda z: z[1])
    BLOCKS.append(([r[1] for r in b], [r[2] for r in b], [r[3] for r in b]))
ISOS = sorted({r[0] for r in rs})


def null_run(seed):
    g = random.Random(seed)
    Y, X, I, T = [], [], [], []
    for k, (yrs, dv, xv) in enumerate(BLOCKS):
        sh = g.randrange(len(xv))
        xv2 = xv[sh:] + xv[:sh]
        Y += dv; X += xv2; I += [k] * len(dv); T += yrs
    return r2_within(Y, X, I, T)


def boot_run(seed):
    g = random.Random(seed)
    pick = set(g.choice(ISOS) for _ in ISOS)
    out = {}
    for c, rr in ROWS.items():
        sub = [r for r in rr if r[0] in pick]
        out[c] = r2_within([r[2] for r in sub], [r[3] for r in sub],
                           [r[0] for r in sub], [r[1] for r in sub]) if len(sub) >= 100 else 0.0
    return out


if __name__ == "__main__":
    with Pool(32) as p:
        nulls = p.map(null_run, range(20000), chunksize=100)
        boots = p.map(boot_run, range(2000), chunksize=20)
    nulls.sort()
    print("=" * 72)
    print("LUCK TEST — 20,000 simulated worlds where education has NO effect")
    print("=" * 72)
    print("  actual share explained: %.2f%%" % OBS)
    print("  no-effect worlds: median %.3f%%, 99th percentile %.3f%%, maximum %.3f%%"
          % (statistics.median(nulls), nulls[int(0.99 * len(nulls))], nulls[-1]))
    print("  worlds that reached the real value: %d of 20,000" % sum(1 for v in nulls if v >= OBS))

    print()
    print("=" * 72)
    print("COUNTRY RESAMPLE — 2,000 different sets of countries")
    print("=" * 72)
    tally = {c: 0 for c in ROWS}; top3 = {c: 0 for c in ROWS}
    for b in boots:
        order = sorted(b, key=lambda k: -b[k])
        tally[order[0]] += 1
        for c in order[:3]:
            top3[c] += 1
    for c in sorted(tally, key=lambda k: -tally[k])[:8]:
        print("  %-40s first %3.1f%%   top three %3.1f%%"
              % (NAME[c], 100.0 * tally[c] / len(boots), 100.0 * top3[c] / len(boots)))
