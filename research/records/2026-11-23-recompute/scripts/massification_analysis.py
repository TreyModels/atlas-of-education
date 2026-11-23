import os
#!/usr/bin/env python3
"""Massification: fertility + schooling + gender. Standalone, stdlib only."""
import json, os, random, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
random.seed(7)

NAME = {
    "fertility": "births per woman", "lsc": "finishing lower secondary",
    "sec": "secondary completion", "ter": "young people in higher ed",
    "gpi_ter": "women vs men in higher ed", "u5mr": "children dying before 5",
    "gdppc_log": "income per person", "flfp": "women in the labour force",
    "electricity": "homes with electricity", "wage_emp": "share of jobs that are paid",
    "urban": "share living in cities", "gpi_sec": "women vs men in secondary",
    "prm_cmp": "primary completion", "life_exp": "life expectancy",
}
KEYS = list(NAME)


def load(name):
    p = os.path.join(DATA, name + ".json")
    if not os.path.exists(p):
        import gzip
        with gzip.open(p + ".gz") as f:
            rows = json.load(f)
    else:
        with open(p) as f:
            rows = json.load(f)
    return {(r[0], int(r[1])): float(r[2]) for r in rows if r[2] is not None}


def demean(vals, groups):
    acc, n = {}, {}
    for v, g in zip(vals, groups):
        acc[g] = acc.get(g, 0.0) + v
        n[g] = n.get(g, 0) + 1
    mean = {g: acc[g] / n[g] for g in acc}
    return [v - mean[g] for v, g in zip(vals, groups)]


def r2_within(target, x, iso, year):
    if len(target) < 100:
        return 0.0
    xw = demean(demean(x, iso), year)
    yw = demean(demean(target, iso), year)
    mx = statistics.mean(xw); my = statistics.mean(yw)
    sx = sum((a - mx) ** 2 for a in xw) ** 0.5
    sy = sum((b - my) ** 2 for b in yw) ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    cov = sum((a - mx) * (b - my) for a, b in zip(xw, yw))
    return 100.0 * (cov / (sx * sy)) ** 2


def pair_rows(V, base="fertility"):
    F = V[base]
    out = {}
    for c in V:
        if c == base:
            continue
        rows = []
        for (i, t), v in F.items():
            if (i, t + 10) in F and (i, t) in V[c]:
                rows.append((i, t, F[(i, t + 10)] - v, V[c][(i, t)]))
        out[c] = rows
    return out


def main():
    meta = json.load(open(os.path.join(DATA, "meta.json")))
    ok = lambda iso: iso in meta and meta[iso]["region"].strip() != "Aggregates" and len(iso) == 3
    V = {}
    for k in KEYS:
        try:
            V[k] = {kk: vv for kk, vv in load(k).items() if ok(kk[0])}
        except FileNotFoundError:
            print("  (missing:", k, ")")
    rows = pair_rows(V)

    print("=" * 74)
    print("1. WHAT MOVES WITH THE FALL IN BIRTHS")
    print("   (share of the within-country fall each one explains)")
    print("=" * 74)
    scores = []
    for c, rs in rows.items():
        if len(rs) < 300:
            continue
        s = r2_within([r[2] for r in rs], [r[3] for r in rs], [r[0] for r in rs], [r[1] for r in rs])
        scores.append((c, s, len(rs)))
    for c, s, n in sorted(scores, key=lambda z: -z[1]):
        print("  %-40s %5.1f%%   (n=%d)" % (NAME[c], s, n))

    print()
    print("=" * 74)
    print("2. LUCK TEST  (shift each country's education in time, 500 runs)")
    print("=" * 74)
    base = "lsc"
    rs = rows[base]
    obs = r2_within([r[2] for r in rs], [r[3] for r in rs], [r[0] for r in rs], [r[1] for r in rs])
    by = {}
    for r in rs:
        by.setdefault(r[0], []).append(r)
    blocks = []
    for iso, b in by.items():
        b = sorted(b, key=lambda z: z[1])
        blocks.append(([r[1] for r in b], [r[2] for r in b], [r[3] for r in b]))
    nulls = []
    for _ in range(500):
        Y, X, I, T = [], [], [], []
        for k, (yrs, dv, xv) in enumerate(blocks):
            sh = random.randrange(len(xv))
            xv2 = xv[sh:] + xv[:sh]
            Y += dv; X += xv2; I += [k] * len(dv); T += yrs
        nulls.append(r2_within(Y, X, I, T))
    nulls.sort()
    beat = 100.0 * sum(1 for v in nulls if v >= obs) / len(nulls)
    print("  actual: %.1f%%" % obs)
    print("  no-link median: %.1f%%   95%% range: %.1f-%.1f%%" % (statistics.median(nulls), nulls[12], nulls[487]))
    print("  pure luck matched or beat it in %.1f%% of runs" % beat)

    print()
    print("=" * 74)
    print("3. NOISE TEST  (if part of the education figure is measurement error)")
    print("=" * 74)
    sd = statistics.pstdev([r[3] for r in rs])
    for frac in (0.2, 0.4, 0.6):
        sims = []
        for rep in range(120):
            g = random.Random(rep)
            Y = [r[2] for r in rs]
            X = [r[3] + g.gauss(0, frac * sd) for r in rs]
            sims.append(r2_within(Y, X, [r[0] for r in rs], [r[1] for r in rs]))
        print("  %2d%% noise -> %5.1f%% explained" % (int(frac * 100), statistics.mean(sims)))

    print()
    print("=" * 74)
    print("4. COUNTRY LUCK TEST  (redraw which countries are in the study, 200 runs)")
    print("=" * 74)
    isos = sorted({r[0] for r in rs})
    tally = {c: 0 for c in rows}
    top3 = {c: 0 for c in rows}
    g = random.Random(11)
    for _ in range(200):
        pick = set(g.choice(isos) for _ in isos)
        sc = {}
        for c, rr in rows.items():
            sub = [r for r in rr if r[0] in pick]
            sc[c] = r2_within([r[2] for r in sub], [r[3] for r in sub], [r[0] for r in sub], [r[1] for r in sub]) if len(sub) >= 100 else 0.0
        order = sorted(sc, key=lambda k: -sc[k])
        tally[order[0]] += 1
        for c in order[:3]:
            top3[c] += 1
    for c in sorted(tally, key=lambda k: -tally[k])[:8]:
        print("  %-40s first %3.0f%%   top three %3.0f%%" % (NAME[c], 100 * tally[c] / 200, 100 * top3[c] / 200))

    print()
    print("=" * 74)
    print("5. WHEN DID THE FALL BEGIN?  (measured 20 years before onset)")
    print("=" * 74)
    F = V["fertility"]
    onsets = {}
    for iso in {i for (i, y) in F}:
        for y in sorted(y for (i, y) in F if i == iso):
            if F[(iso, y)] < 5.0:
                if 1950 <= y <= 2020:
                    onsets[iso] = y
                break
    for c in ["lsc", "sec", "ter", "gpi_ter", "urban", "gdppc_log", "u5mr"]:
        if c not in V:
            continue
        xs, ys = [], []
        for iso, y0 in onsets.items():
            for back in range(0, 11):
                if (iso, y0 - 20 - back) in V[c]:
                    xs.append(V[c][(iso, y0 - 20 - back)]); ys.append(y0); break
        if len(xs) < 25:
            continue
        mx, my = statistics.mean(xs), statistics.mean(ys)
        sx = sum((a - mx) ** 2 for a in xs) ** 0.5
        sy = sum((b - my) ** 2 for b in ys) ** 0.5
        r = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / (sx * sy)
        print("  more %-36s -> fall begins %-7s (r=%+.2f, n=%d)" % (NAME[c], "EARLIER" if r < 0 else "later", r, len(xs)))
    print()
    print("done.")


if __name__ == "__main__":
    main()
