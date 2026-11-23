#!/usr/bin/env python3
"""Summarise matrix_results.json: counts, and which links change between observed-only and imputed 1950+."""
import json, sys
from common import OUT
R = json.load(open(f"{OUT}/matrix_results.json"))
EDU = {"lsc", "sec", "ter", "prm_cmp", "gpi_sec", "gpi_ter"}


def sig(r): return r is not None and r[1] > 0 and abs(r[0] / r[1]) > 1.96
def get(s, x, y, t): return R[s].get(f"{x}|{y}|{int(t)}")


pairs = sorted({tuple(k.split("|")[:2]) for k in R["obs"]} | {tuple(k.split("|")[:2]) for k in R["imp"]})
st = {}
for s in ("obs", "imp"):
    fe = {p for p in pairs if sig(get(s, *p, False))}
    tr = {p for p in pairs if sig(get(s, *p, True))}
    sv = {p for p in fe & tr if (get(s, *p, False)[0] > 0) == (get(s, *p, True)[0] > 0)}
    st[s] = dict(fe=fe, tr=tr, sv=sv, n=sum(1 for p in pairs if get(s, *p, False) and get(s, *p, True)))
    print(f"{s}: estimable {st[s]['n']}, FE-significant {len(fe)}, trend-significant {len(tr)}, both same sign {len(sv)} "
          f"({100 * len(sv) / max(len(fe), 1):.1f}% of FE)")


def fmt(p):
    a, b = get("obs", *p, False), get("obs", *p, True)
    c, d = get("imp", *p, False), get("imp", *p, True)
    f = lambda r: "   n/a      " if r is None else f"{r[0]:+8.3f}({r[1]:.3f})"
    return f"  {p[0]:11s}->{p[1]:11s} obs FE {f(a)} tr {f(b)} | imp FE {f(c)} tr {f(d)}"


def group(p):
    if "fertility" in p: return "fertility"
    if set(p) & EDU: return "massification"
    return "other"


for kind, label in (("sv", "SURVIVE both country effects and country trends"), ("fe", "significant with country effects only"), ("tr", "significant with country trends")):
    gained = st["imp"][kind] - st["obs"][kind]; lost = st["obs"][kind] - st["imp"][kind]
    print(f"\n=== {label}: gained under imputation {len(gained)}, lost {len(lost)}, kept {len(st['obs'][kind] & st['imp'][kind])}")
    for g in ("fertility", "massification", "other"):
        for tag, s in (("GAINED", gained), ("LOST", lost)):
            for p in sorted(x for x in s if group(x) == g):
                print(f"{g:13s} {tag:6s}{fmt(p)}")
print("\n=== all fertility and education links, survivors in either run")
for p in sorted(st["obs"]["sv"] | st["imp"]["sv"]):
    if group(p) != "other":
        print(f"{group(p):13s} {'both' if p in st['obs']['sv'] & st['imp']['sv'] else ('obs only' if p in st['obs']['sv'] else 'imp only'):8s}{fmt(p)}")
