#!/usr/bin/env python3
"""Analyse matrix_ext.json: observed vs imputed matrix, changed verdicts, per-imputation spread,
future-treatment placebo, coverage.  Writes CSV/text into /root/work/impute/results/."""
import json, os, csv
import numpy as np
from common import NC, NY, REG, OUT, load, to_panel

RES = os.environ.get("RES_DIR", "/root/work/impute/results")
os.makedirs(RES, exist_ok=True)
R = json.load(open(f"{OUT}/matrix_ext.json"))
M = R["meta"]["M"]
VARS = R["meta"]["vars"]
EDU = ["lsc", "sec", "ter", "prm_cmp", "gpi_sec", "gpi_ter"]
PAIRS = [(x, y) for x in VARS for y in VARS if x != y]
SPEC = {0: "country effects", 1: "country trends"}


def f3(v):
    return f"{v:+.3f}" if isinstance(v, (int, float)) else "n/a"


def f2(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "n/a"


def verdict(b, se):
    if se is None or se <= 0:
        return "n/a"
    t = b / se
    return "sig+" if t > 1.96 else ("sig-" if t < -1.96 else "null")


def group(x, y):
    if "fertility" in (x, y):
        return "fertility"
    if set((x, y)) & set(EDU):
        return "massification"
    return "other"


def main(spec):            # dict pair -> cell for one spec
    d = {}
    for x, y in PAIRS:
        c = R["main"].get(f"{x}|{y}|{spec}")
        if c:
            d[(x, y)] = c
    return d


M0, M1 = main(0), main(1)
DP = f"{OUT}/matrix_decomp.json"
DEC = json.load(open(DP)) if os.path.exists(DP) else None

# ---------- 1. all links / changed verdicts ----------
rows, changed = [], []
for x, y in PAIRS:
    for t in (0, 1):
        k = f"{x}|{y}|{t}"
        cell = R["main"].get(k, {})
        o, i, me, ob = cell.get("obs"), cell.get("imp"), cell.get("mean"), cell.get("obsonly")
        vo = verdict(*o[:2]) if o else "n/a"
        vi = verdict(*i[:2]) if i else "n/a"
        vob = verdict(*ob[:2]) if ob else "n/a"
        ch = "none"
        if o and i:
            if vo == "null" and vi != "null":
                ch = "gained"
            elif vo != "null" and vi == "null":
                ch = "lost"
            elif vo != "null" and vi != "null" and (o[0] > 0) != (i[0] > 0):
                ch = "sign flip"
        elif not o and i:
            ch = "new estimable"
        elif o and not i:
            ch = "dropped"
        rec = dict(x=x, y=y, group=group(x, y), spec=SPEC[t],
                   obs_b=o[0] if o else "", obs_se=o[1] if o else "", obs_n=o[2] if o else "",
                   obs_nc=o[3] if o else "", obs_verdict=vo,
                   imp_b=i[0] if i else "", imp_se=i[1] if i else "", imp_n=i[2] if i else "",
                   imp_nc=i[3] if i else "", imp_lambda=i[4] if i else "", imp_verdict=vi,
                   mean_b=me[0] if me else "", mean_verdict=verdict(*me[:2]) if me else "n/a",
                   obsonly_b=ob[0] if ob else "", obsonly_se=ob[1] if ob else "", obsonly_verdict=vob,
                   eduonly_b=(DEC["eduonly"][k]["imp"][0] if DEC and k in DEC["eduonly"] else ""),
                   eduonly_verdict=(verdict(*DEC["eduonly"][k]["imp"][:2]) if DEC and k in DEC["eduonly"] else "n/a"),
                   macroonly_b=(DEC["macroonly"][k][0] if DEC and k in DEC["macroonly"] else ""),
                   macroonly_verdict=(verdict(*DEC["macroonly"][k][:2]) if DEC and k in DEC["macroonly"] else "n/a"),
                   changed=ch)
        rows.append(rec)
        if ch in ("gained", "lost", "sign flip", "new estimable", "dropped"):
            per = cell.get("per")
            extra = dict(per_b_min="", per_b_max="", per_sd="", per_median_se="",
                         n_match_imp_verdict="", n_imp_sig_any="", n_imp_sig_same_sign="",
                         leave_one_out_verdict_flips="")
            if per:
                b = np.array([p[0] for p in per]); se = np.array([p[1] for p in per])
                vp = [verdict(b[j], se[j]) for j in range(M)]
                # leave-one-imputation-out Rubin: does any single imputation drive the verdict?
                flips = 0
                for j in range(M):
                    bb = np.delete(b, j); ss = np.delete(se, j); n1 = M - 1
                    W = (ss ** 2).mean(); B = bb.var(ddof=1); T = W + (1 + 1 / n1) * B
                    if verdict(bb.mean(), np.sqrt(T)) != vi:
                        flips += 1
                extra = dict(per_b_min=round(float(b.min()), 4), per_b_max=round(float(b.max()), 4),
                             per_sd=round(float(b.std(ddof=1)), 4), per_median_se=round(float(np.median(se)), 4),
                             n_match_imp_verdict=sum(1 for vv in vp if vv == vi),
                             n_imp_sig_any=sum(1 for vv in vp if vv != "null"),
                             n_imp_sig_same_sign=sum(1 for vv in vp if vv == vi and vv != "null"),
                             leave_one_out_verdict_flips=flips)
            rec2 = dict(rec); rec2.update(extra)
            changed.append(rec2)

with open(f"{RES}/all_links.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# ---- three labels + precision-vs-shift rule ----
WPP_PAIRS = {("fertility", "u5mr"), ("life_exp", "u5mr"), ("fertility", "life_exp")}
LADDER_PAIRS = {("lsc", "sec"), ("sec", "ter"), ("lsc", "ter")}
for r in changed:
    lam = r["imp_lambda"]
    if lam >= 0.8:
        r["label"] = "stochastic-imputation (unreliable)"
    elif r.get("macroonly_verdict") == r["imp_verdict"]:
        r["label"] = "added long-run rows"
    else:
        r["label"] = "estimate moved"
    pr = tuple(sorted((r["x"], r["y"])))
    u = (r["x"] in ("fertility", "life_exp", "u5mr") and r["y"] in ("fertility", "life_exp", "u5mr")
         and r["x"] != r["y"])
    if u and set(pr) in [set(p) for p in WPP_PAIRS]:
        r["mechanical"] = "same UN WPP life-table source"
    elif set(pr) in [set(p) for p in LADDER_PAIRS]:
        r["mechanical"] = "cumulative schooling ladder"
    else:
        r["mechanical"] = ""
    ob, bb = r["obs_b"], r["imp_b"]
    r["change_type"] = "precision only" if abs(bb - ob) <= 0.5 * r["obs_se"] else "estimate moved"
    if r["label"] == "stochastic-imputation (unreliable)":
        r["group4"] = "unreliable imputation"
    elif r["change_type"] == "precision only":
        r["group4"] = "precision only"
    elif r["label"] == "added long-run rows":
        r["group4"] = "coverage-driven (zero imputation spread)"
    else:
        r["group4"] = "genuine estimate movement"

if changed:
    with open(f"{RES}/changed_verdicts.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(changed[0].keys())); w.writeheader(); w.writerows(changed)

# ---------- 2. summary ----------
L = []
A = L.append
A("=== counts of significant links (272 ordered pairs; nominal |t|>1.96) ===")
for spec, name in SPEC.items():
    mm = main(spec)
    n = {}
    for s in ("obs", "imp", "mean", "obsonly"):
        n[s] = sum(1 for c in mm.values() if c.get(s) and verdict(*c[s][:2]) != "null")
    A(f"{name}: obs {n['obs']}, imputed {n['imp']}, mean-imputation {n['mean']}, observed-cells-only {n['obsonly']}")
surv = {}
for s in ("obs", "imp"):
    v = 0
    for p in PAIRS:
        a, b = M0.get(p), M1.get(p)
        if a and b and a.get(s) and b.get(s):
            va, vb = verdict(*a[s][:2]), verdict(*b[s][:2])
            if va != "null" and vb != "null" and (a[s][0] > 0) == (b[s][0] > 0):
                v += 1
    surv[s] = v
A(f"significant in BOTH country effects and country trends, same sign: obs {surv['obs']}, imputed {surv['imp']}")

A("")
A("=== survivors (both country effects and country trends, same sign) ===")
for s in ("obs", "imp"):
    A(f"-- {s}")
    for p in PAIRS:
        a, b = M0.get(p), M1.get(p)
        if a and b and a.get(s) and b.get(s):
            va, vb = verdict(*a[s][:2]), verdict(*b[s][:2])
            if va != "null" and vb != "null" and (a[s][0] > 0) == (b[s][0] > 0):
                A(f"   {p[0]:11s}->{p[1]:11s} FE {a[s][0]:+.3f} ({a[s][1]:.3f}) n={a[s][2]} nc={a[s][3]} | "
                  f"tr {b[s][0]:+.3f} ({b[s][1]:.3f}) n={b[s][2]} nc={b[s][3]}")

from collections import Counter
A("")
A("=== changed verdicts sorted by the three labels ===")
for spec, name in SPEC.items():
    cc = [r for r in changed if r["spec"] == name]
    A(f"{name}: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(r["label"] for r in cc).items())))
A("precision-vs-shift rule: |imputed estimate - observed estimate| <= 0.5 * observed standard error = 'precision only' (the estimate did not really move, only its certainty); otherwise 'estimate moved'.")
for spec, name in SPEC.items():
    cc = [r for r in changed if r["spec"] == name]
    A(f"{name}: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(r["change_type"] for r in cc).items())))
A("dashboard groups: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(r["group4"] for r in changed).items())))
A("mechanical/definitional pairs flagged: " +
  ", ".join(f"{r['x']}->{r['y']}({r['spec']}, {r['mechanical']})" for r in changed if r["mechanical"]))
A("")
A("=== changed verdicts, by spec and group ===")
for spec, name in SPEC.items():
    c = Counter(r["changed"] for r in changed if r["spec"] == name)
    A(f"{name}: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
cg = Counter((r["spec"], r["group"], r["changed"]) for r in changed)
for k, v in sorted(cg.items()):
    A(f"   {k[0]} / {k[1]} / {k[2]}: {v}")

A("")
A("=== per-imputation spread ===")
lam = [c["imp"][4] for c in R["main"].values() if c.get("imp")]
A(f"lambda (share of total variance from between-imputation spread): median {np.median(lam):.3f}, "
  f"90th {np.percentile(lam, 90):.3f}, max {max(lam):.3f}; cells lambda>0.5: {sum(1 for v in lam if v > 0.5)} of {len(lam)}")
nm = [r["n_match_imp_verdict"] for r in changed if r["n_match_imp_verdict"] != ""]
if nm:
    A(f"changed-verdict cells: median number of the 20 single-imputation runs giving the same verdict: {np.median(nm):.1f} of 20")
    A(f"changed-verdict cells where all 20 imputations individually significant same sign: "
      f"{sum(1 for r in changed if r['n_imp_sig_same_sign'] == M)} of {len(changed)}")
    A(f"changed-verdict cells where NO single imputation is significant: "
      f"{sum(1 for r in changed if r['n_imp_sig_any'] == 0)} of {len(changed)}")
# are the major changes concentrated in education links?
for spec, name in SPEC.items():
    cc = [r for r in changed if r["spec"] == name]
    A(f"{name}: changed cells with education involved {sum(1 for r in cc if r['group'] == 'massification')}, "
      f"fertility links {sum(1 for r in cc if r['group'] == 'fertility')}, other {sum(1 for r in cc if r['group'] == 'other')}")

# ---------- lambda caveat list ----------
A("")
A("=== education links whose verdict rests on imputation spread (lambda >= 0.8) ===")
lamrows = []
for k, c in R["main"].items():
    if not c.get("imp"):
        continue
    x, y, t = k.split("|")
    if not (set((x, y)) & set(EDU)):
        continue
    if c["imp"][4] >= 0.8:
        o = c.get("obs")
        lamrows.append((c["imp"][4], x, y, int(t), c["imp"], c.get("eduonly", {}).get("imp") if "eduonly" in c else None))
for lam, x, y, t, i, _ in sorted(lamrows, reverse=True):
    o = R["main"][f"{x}|{y}|{t}"].get("obs")
    ov = verdict(*o[:2]) if o else "n/a"
    A(f"  lambda={lam:.2f} {SPEC[t]:15s} {x:11s}->{y:11s} obs {ov:4s} {o[0]:+.3f}({o[1]:.3f}) -> imp {verdict(*i[:2]):4s} {i[0]:+.3f}({i[1]:.3f})")
A(f"  {len(lamrows)} of 544 cells")

# ---------- 2b. where changes come from ----------
A("")
A("=== where a changed verdict comes from: education gap-fill vs macro long-run splice ===")
if DEC:
    cc = [r for r in changed if r["changed"] in ("gained", "lost", "sign flip")]
    edu_c = [r for r in cc if set((r["x"], r["y"])) & set(EDU)]
    oth_c = [r for r in cc if not set((r["x"], r["y"])) & set(EDU)]
    for lab, sub in (("links involving education", edu_c), ("links with no education series", oth_c)):
        em = sum(1 for r in sub if r["eduonly_verdict"] == r["imp_verdict"])
        mm = sum(1 for r in sub if r["macroonly_verdict"] == r["imp_verdict"])
        A(f"{lab}: {len(sub)} changed cells; verdict reproduced by education-only panel {em}, by macro-only panel {mm}")
    A("if a changed education link is NOT reproduced by the education-only panel, its change is from the macro splice, not the schooling imputation")
    A("")
    A("=== every changed verdict (obs -> imputed) ===")
    for spec, name in SPEC.items():
        for r in changed:
            if r["spec"] != name:
                continue
            A(f" {r['changed']:10s} {name:15s} {r['x']:11s}->{r['y']:11s} obs {r['obs_verdict']:4s} {f3(r['obs_b'])}({f2(r['obs_se'])}) n={r['obs_n']}"
              f" -> imp {r['imp_verdict']:4s} {f3(r['imp_b'])}({f2(r['imp_se'])}) n={r['imp_n']} lam={f2(r['imp_lambda'])}"
              f" | eduonly {f3(r['eduonly_b'])}? macroonly {f3(r['macroonly_b'])}? | {r['label']} | {r['change_type']}"
              + (" | MECHANICAL" if r["mechanical"] else ""))
    # unique-link summary
    A("")
    A("=== unique links whose verdict changed in at least one spec ===")
    seen = {}
    for r in changed:
        seen.setdefault((r["x"], r["y"]), {})[r["spec"]] = r
    for (x, y), d in seen.items():
        parts = []
        for spec in ("country effects", "country trends"):
            r = d.get(spec)
            parts.append(f"{spec.split()[-1]}={r['changed']}" if r else "")
        A(f"  {group(x, y):13s} {x:11s}->{y:11s} " + " ".join(p for p in parts if p))

# ---------- why did significant links lose significance? ----------
A("")
A("=== for every lost-significance cell: did n fall (power) or did the estimate shrink? ===")
for spec, name in SPEC.items():
    lost = [r for r in changed if r["spec"] == name and r["changed"] == "lost"]
    dn = [r["imp_n"] - r["obs_n"] for r in lost]
    shrink = sum(1 for r in lost if abs(r["imp_b"]) < abs(r["obs_b"]))
    power = sum(1 for r in lost if r["imp_n"] < r["obs_n"])
    A(f"{name}: {len(lost)} lost; n fell in {power}; |estimate| shrank in {shrink}; "
      f"n change median {int(np.median(dn)) if dn else 0} (range {min(dn) if dn else 0}..{max(dn) if dn else 0})")
    for r in lost:
        A(f"   {r['x']:11s}->{r['y']:11s} obs {r['obs_b']:+.3f}({r['obs_se']:.3f}) n={r['obs_n']} -> "
          f"imp {r['imp_b']:+.3f}({r['imp_se']:.3f}) n={r['imp_n']}  dn={r['imp_n']-r['obs_n']:+d}")

# ---------- 3. placebo ----------
A("")
A("=== future-treatment placebo (supposed cause measured 20 years AFTER the outcome window) ===")
pl = R["placebo"]
for s in ("obs", "imp"):
    tot = sig = 0; by = Counter()
    for k, c in pl.items():
        if c.get(s):
            tot += 1
            if verdict(*c[s][:2]) != "null":
                sig += 1; by[group(*k.split("|")[:2])] += 1
    A(f"placebo {s}: estimable {tot}, significant {sig} ({100*sig/max(tot,1):.1f}%), by group {dict(by)}")
for s in ("obs", "imp"):
    tot = sum(1 for c in R["main"].values() if c.get(s))
    sig = sum(1 for c in R["main"].values() if c.get(s) and verdict(*c[s][:2]) != "null")
    A(f"main matrix {s}: estimable {tot}, significant {sig} ({100*sig/max(tot,1):.1f}%)")
A("prior-project placebo link electricity->tax:")
for t in (0, 1):
    k = f"electricity|tax|{t}"
    for s in ("obs", "imp"):
        c = R["main"].get(k, {})
        if c.get(s):
            A(f"   main {SPEC[t]}, {s}: {c[s][0]:+.4f} ({c[s][1]:.4f}) {verdict(*c[s][:2])}")
    c = pl.get(k, {})
    for s in ("obs", "imp"):
        if c.get(s):
            A(f"   PLACEBO {SPEC[t]}, {s}: {c[s][0]:+.4f} ({c[s][1]:.4f}) {verdict(*c[s][:2])}")
with open(f"{RES}/placebo.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["x", "y", "spec", "group", "obs_b", "obs_se", "obs_verdict",
                                   "imp_b", "imp_se", "imp_verdict"])
    for k, c in pl.items():
        x, y, t = k.split("|")
        w.writerow([x, y, SPEC[int(t)], group(x, y)] +
                   ([c["obs"][0], c["obs"][1], verdict(*c["obs"][:2])] if c.get("obs") else ["", "", "n/a"]) +
                   ([c["imp"][0], c["imp"][1], verdict(*c["imp"][:2])] if c.get("imp") else ["", "", "n/a"]))

# ---------- 4. coverage ----------
A("")
A("=== coverage (country x year cells, 1950-2023 grid) ===")
IMP = "/root/work/data_imputed"
tot_cells = NC * NY
cov = []
for v in VARS:
    p = f"{IMP}/flags/{v}.json"
    if os.path.exists(p):
        fl = np.array([int(r[2]) for r in json.load(open(p))])
        ob, lr, mo = int((fl == 0).sum()), int((fl == 1).sum()), int((fl == 2).sum())
        miss = tot_cells - len(fl)
    else:
        ob = int(np.isfinite(to_panel(load(v))).sum()); lr = mo = 0; miss = tot_cells - ob
    cov.append((v, ob, lr, mo, miss))
    A(f"{v:11s} observed {ob:6d} ({100*ob/tot_cells:5.1f}%)  long-run {lr:5d} ({100*lr/tot_cells:4.1f}%)  "
      f"modelled {mo:6d} ({100*mo/tot_cells:5.1f}%)  missing {miss:6d} ({100*miss/tot_cells:5.1f}%)")
with open(f"{RES}/coverage.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["series", "grid_cells", "observed", "long_run_source", "modelled", "missing"])
    for v, ob, lr, mo, miss in cov:
        w.writerow([v, tot_cells, ob, lr, mo, miss])

# ---------- 5. rows used per matrix cell ----------
A("")
A("=== rows used per matrix cell ===")
for spec, name in SPEC.items():
    for cond, lab in ((lambda x, y: bool(set((x, y)) & set(EDU)), "links involving education"),
                      (lambda x, y: not set((x, y)) & set(EDU) and "fertility" not in (x, y), "links involving neither education nor fertility")):
        dn, dp, do = [], [], []
        for x, y in PAIRS:
            c = R["main"].get(f"{x}|{y}|{spec}")
            if c and cond(x, y) and c.get("obs") and c.get("imp"):
                dn.append(c["imp"][2] - c["obs"][2]); dp.append(c["imp"][2]); do.append(c["obs"][2])
        if dp:
            A(f"{name}, {lab}: rows obs median {int(np.median(do))} -> imputed median {int(np.median(dp))} "
              f"(added median {int(np.median(dn))}, range {min(dn)}..{max(dn)})")

# ---------- 6. verification against the pre-existing run ----------
A("")
A("=== verification against out/matrix_results.json (pre-existing 16:07 run) ===")
old = json.load(open(f"{OUT}/matrix_results.json"))
maxd_o = maxd_i = 0.0; cnt_o = cnt_i = 0
for k, c in R["main"].items():
    if c.get("obs") and k in old["obs"]:
        maxd_o = max(maxd_o, abs(c["obs"][0] - old["obs"][k][0]), abs(c["obs"][1] - old["obs"][k][1])); cnt_o += 1
    if c.get("imp") and k in old["imp"]:
        maxd_i = max(maxd_i, abs(c["imp"][0] - old["imp"][k][0]), abs(c["imp"][1] - old["imp"][k][1])); cnt_i += 1
A(f"cells compared obs {cnt_o}, imp {cnt_i}; max |difference| in estimate/SE vs old run: obs {maxd_o:.2e}, imp {maxd_i:.2e}")
mo = 0.0; cnt = 0; vd = 0
for k, c in R["main"].items():
    if c.get("obs") and c.get("obsonly"):
        mo = max(mo, abs(c["obs"][0] - c["obsonly"][0]), abs(c["obs"][1] - c["obsonly"][1])); cnt += 1
        vd += int(verdict(*c["obs"][:2]) != verdict(*c["obsonly"][:2]))
A(f"observed-cells-only vs observed-data matrix: max |difference| {mo:.3f} over {cnt} cells; verdict differs in {vd} cells")
A("(the reference observed matrix includes a few 2024 endpoints in 6 series; the 1950-2023 gap-filled grid cannot use them, so ~130 rows of the parity links drop. That, not masking, is the source of this residual.)")

open(f"{RES}/summary.txt", "w").write("\n".join(L) + "\n")
print("\n".join(L))
