#!/usr/bin/env python3
"""Analyse controls_results.json: mediator rule, verdict changes per added control, power,
collinearity, leave-one-control-out, negative-control demonstration.
Writes results/ (CSV + summary.txt)."""
import json, os, csv
import numpy as np

OUT = "/root/work/controls/out"
RES = "/root/work/controls/results"
os.makedirs(RES, exist_ok=True)
D = json.load(open(f"{OUT}/controls_results.json"))
VARS = D["vars"]; C = D["cells"]; MED = D["mediator"]
PAIRS = [(x, y) for x in VARS for y in VARS if x != y]
ADD = {"base": "base", "u5mr": "u5mr", "flfp": "flfp", "both": "u5mr+flfp"}


def verdict(b, se):
    if se is None or se <= 0:
        return "n/a"
    t = b / se
    return "sig+" if t > 1.96 else ("sig-" if t < -1.96 else "null")


def get(x, y, t, ad):
    return C.get(f"{x}|{y}|{t}|{ad}")


def allowed(x, y, c):
    return c not in (x, y) and not MED[f"{x}|{y}"][c]


L = []
A = L.append

# ---------- 1. baseline check ----------
A("=== baseline (no added controls; income logged, urbanisation controlled) ===")
for t, lab in ((0, "country effects"), (1, "country trends")):
    n = sum(1 for x, y in PAIRS if get(x, y, t, "base") and verdict(get(x, y, t, "base")["b"], get(x, y, t, "base")["se"]) != "null")
    A(f"{lab}: {n} of 272 links significant (absolute t) -> recompute reference is 127 / 42")
both = 0
for x, y in PAIRS:
    a, b = get(x, y, 0, "base"), get(x, y, 1, "base")
    if a and b and verdict(a["b"], a["se"]) != "null" and verdict(b["b"], b["se"]) != "null" \
       and (a["b"] > 0) == (b["b"] > 0):
        both += 1
A(f"significant in both specs with same sign: {both} (recompute reference 24)")

# ---------- 2. mediator rule ----------
A("")
A("=== mediator rule: which added controls may be used ===")
n_med = {"u5mr": 0, "flfp": 0}
n_na = {"u5mr": 0, "flfp": 0}
for x, y in PAIRS:
    for c in ("u5mr", "flfp"):
        if c in (x, y):
            n_na[c] += 1
        elif MED[f"{x}|{y}"][c]:
            n_med[c] += 1
A(f"child mortality is a mediator (x -> child mortality -> y) for {n_med['u5mr']} links; "
  f"it is x or y for {n_na['u5mr']} links; usable for {272 - n_med['u5mr'] - n_na['u5mr']}")
A(f"women's work is a mediator for {n_med['flfp']} links; it is x or y for {n_na['flfp']} links; "
  f"usable for {272 - n_med['flfp'] - n_na['flfp']}")
A(f"both controls usable together for {sum(1 for x, y in PAIRS if allowed(x, y, 'u5mr') and allowed(x, y, 'flfp'))} links")
ex_flfp = [f"{x}->{y}" for x, y in PAIRS if MED[f"{x}|{y}"]["flfp"]]
ex_u5 = [f"{x}->{y}" for x, y in PAIRS if MED[f"{x}|{y}"]["u5mr"]]
A("women's-work mediators (first 40): " + ", ".join(ex_flfp[:40]))
A("child-mortality mediators: " + ", ".join(ex_u5))
with open(f"{RES}/mediator_table.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["x", "y", "u5mr_mediator", "flfp_mediator", "u5mr_usable", "flfp_usable"])
    for x, y in PAIRS:
        w.writerow([x, y, int(MED[f"{x}|{y}"]["u5mr"]), int(MED[f"{x}|{y}"]["flfp"]),
                    int(allowed(x, y, "u5mr")), int(allowed(x, y, "flfp"))])

# ---------- 3. verdict changes per variant ----------
A("")
A("=== verdict changes vs baseline (only rule-allowed control uses) ===")
rows = []
changed = []
for x, y in PAIRS:
    for t in (0, 1):
        base = get(x, y, t, "base")
        if not base:
            continue
        vb = verdict(base["b"], base["se"])
        for ad, cs in (("u5mr", ["u5mr"]), ("flfp", ["flfp"]), ("both", ["u5mr", "flfp"])):
            r = get(x, y, t, ADD[ad])
            if not r:
                continue
            ok = all(allowed(x, y, c) for c in cs)
            addinfo = r.get("add", {})
            has = cs[0] in addinfo
            v = verdict(r["b"], r["se"])
            kind = "none"
            if ok and vb != v:
                if vb == "null" and v != "null":
                    kind = "gained"
                elif vb != "null" and v == "null":
                    kind = "lost"
                elif vb != "null" and v != "null" and (base["b"] > 0) != (r["b"] > 0):
                    kind = "sign flip"
            rec = dict(x=x, y=y, spec="country effects" if t == 0 else "country trends", variant=ad,
                       usable=int(ok), base_b=base["b"], base_se=base["se"], base_n=base["n"], base_nc=base["nc"],
                       b=r["b"], se=r["se"], n=r["n"], nc=r["nc"], base_verdict=vb, verdict=v,
                       change=kind, delta=base["b"] - r["b"],
                       mdc=(2.8 * addinfo[cs[0]]["se_delta"] if len(cs) == 1 and has else ""),
                       se_delta=(addinfo[cs[0]]["se_delta"] if len(cs) == 1 and has else ""),
                       vif=(addinfo[cs[0]]["vif"] if len(cs) == 1 and has else ""),
                       partial_r2=(addinfo[cs[0]]["partial_r2"] if len(cs) == 1 and has else ""),
                       add_coef=(addinfo[cs[0]]["coef"] if len(cs) == 1 and has else ""),
                       add_se=(addinfo[cs[0]]["se"] if len(cs) == 1 and has else ""))
            rows.append(rec)
            if kind != "none":
                changed.append(rec)
for t, lab in ((0, "country effects"), (1, "country trends")):
    for ad in ("u5mr", "flfp", "both"):
        cc = [r for r in changed if r["spec"] == lab and r["variant"] == ad]
        A(f"{lab}, +{ad}: {len(cc)} verdict changes of " +
          f"{sum(1 for r in rows if r['spec'] == lab and r['variant'] == ad and r['usable'])} usable tests "
          f"({sum(1 for r in cc if r['change'] == 'gained')} gained, {sum(1 for r in cc if r['change'] == 'lost')} lost, "
          f"{sum(1 for r in cc if r['change'] == 'sign flip')} sign flips)")
with open(f"{RES}/variant_table.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
if changed:
    with open(f"{RES}/changed_verdicts.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(changed[0].keys())); w.writeheader(); w.writerows(changed)

A("")
A("=== every changed verdict ===")
for r in changed:
    A(f" {r['change']:9s} +{r['variant']:4s} {r['spec']:15s} {r['x']:11s}->{r['y']:11s} base {r['base_verdict']:4s} "
      f"{r['base_b']:+.3f}({r['base_se']:.3f}) n={r['base_n']} -> {r['verdict']:4s} {r['b']:+.3f}({r['se']:.3f}) n={r['n']}")

# ---------- 3b. control effect vs sample composition ----------
CS = {}
csp = f"{OUT}/common_sample.json"
if os.path.exists(csp):
    CS = json.load(open(csp))
A("")
A("=== did a changed verdict come from the CONTROL or from the smaller sample? ===")
A("baseline re-estimated on exactly the rows each control variant used (common-sample baseline).")
A("sample = baseline verdict already changes on the restricted rows (the control's coverage changed the sample);")
A("control = the added control changes the verdict relative to that same-row baseline.")
cnt = {}
for r in changed:
    j = r["variant"]; t = 0 if r["spec"] == "country effects" else 1
    cs = {"u5mr": ("u5mr",), "flfp": ("flfp",), "both": ("u5mr", "flfp")}[j]
    key = f"{r['x']}|{r['y']}|{t}|{'+'.join(cs)}"
    same = CS.get(key)
    if not same:
        cnt["unclassified"] = cnt.get("unclassified", 0) + 1
        continue
    vs = verdict(same[0], same[1])
    sample_change = vs != r["base_verdict"]
    control_change = r["verdict"] != vs
    if sample_change and not control_change:
        cls = "sample composition only"
    elif control_change and not sample_change:
        cls = "control effect only"
    elif control_change and sample_change:
        cls = "both"
    else:
        cls = "neither (numerical)"
    r["same_b"], r["same_se"], r["same_verdict"], r["origin"] = same[0], same[1], vs, cls
    cnt[cls] = cnt.get(cls, 0) + 1
A("changed verdicts by origin: " + ", ".join(f"{k}={v}" for k, v in sorted(cnt.items())))
for cls in ("control effect only", "sample composition only", "both"):
    sub = [r for r in changed if r.get("origin") == cls]
    A(f"{cls}: {len(sub)}")
    for r in sub[:12]:
        A(f"   {r['spec']:15s} +{r['variant']:4s} {r['x']}->{r['y']}: full-rows base {r['base_verdict']} "
          f"{r['base_b']:+.3f} -> same-rows base {r['same_verdict']} {r['same_b']:+.3f} -> variant {r['verdict']} {r['b']:+.3f}")
with open(f"{RES}/changed_origin.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["x", "y", "spec", "variant", "base_verdict", "same_verdict", "variant_verdict", "origin"])
    for r in changed:
        w.writerow([r["x"], r["y"], r["spec"], r["variant"], r["base_verdict"], r.get("same_verdict", ""), r["verdict"], r.get("origin", "")])

# ---------- 4. power check ----------
A("")
A("=== power check: could a meaningful change have been seen where the verdict did not move? ===")
for ad, c in (("u5mr", "u5mr"), ("flfp", "flfp")):
    for t, lab in ((0, "country effects"), (1, "country trends")):
        sub = [r for r in rows if r["variant"] == ad and r["spec"] == lab and r["usable"]]
        mdc = [r["mdc"] for r in sub]
        det = [r for r in sub if abs(r["delta"]) >= r["mdc"]]
        rel = [r["mdc"] / abs(r["base_b"]) for r in sub if abs(r["base_b"]) > 0]
        A(f"+{ad}, {lab}: {len(sub)} usable; a change of >= the printed MDC (2.8 x its SE) would be detected; "
          f"median MDC {np.median(mdc):.4g}, as share of |baseline estimate| median {100*np.median(rel):.0f}%; "
          f"{len(det)} of {len(sub)} links show a change that large")
# unchanged links where change could hide a 20% attenuation
for ad in ("u5mr", "flfp"):
    for t, lab in ((0, "country effects"), (1, "country trends")):
        sub = [r for r in rows if r["variant"] == ad and r["spec"] == lab and r["usable"] and r["change"] == "none"]
        hide20 = sum(1 for r in sub if r["mdc"] > 0.2 * abs(r["base_b"]))
        A(f"+{ad}, {lab}: of {len(sub)} unchanged links, {hide20} could hide a 20%-of-baseline change at 80% power")

# ---------- 5. collinearity ----------
A("")
A("=== collinearity of the added controls ===")
for ad, c in (("u5mr", "u5mr"), ("flfp", "flfp")):
    for t, lab in ((0, "country effects"), (1, "country trends")):
        sub = [r for r in rows if r["variant"] == ad and r["spec"] == lab and r["usable"]]
        vif = [r["vif"] for r in sub]; pr2 = [r["partial_r2"] for r in sub]
        A(f"+{ad}, {lab}: VIF median {np.median(vif):.2f}, max {max(vif):.1f}; partial R2 median {np.median(pr2):.2f}, "
          f"max {max(pr2):.2f}")
# both together
bothv = [r for r in rows if r["variant"] == "both" and r["usable"]]
A(f"both controls: {len(bothv)} usable tests; median n {int(np.median([r['n'] for r in bothv]))} vs baseline "
  f"{int(np.median([r['base_n'] for r in bothv]))} (rows lost to control availability)")

# ---------- 6. leave-one-control-out ----------
A("")
A("=== leave-one-control-out: does the conclusion depend on which control is added? ===")
for t, lab in ((0, "country effects"), (1, "country trends")):
    agree = tot = 0
    flips = []
    for x, y in PAIRS:
        if not (allowed(x, y, "u5mr") and allowed(x, y, "flfp")):
            continue
        u, f, b = get(x, y, t, "u5mr"), get(x, y, t, ADD["flfp"]), get(x, y, t, ADD["both"])
        if not (u and f and b):
            continue
        tot += 1
        vu, vf, vb = verdict(u["b"], u["se"]), verdict(f["b"], f["se"]), verdict(b["b"], b["se"])
        if vu == vf == vb:
            agree += 1
        elif not (vu == vf):
            flips.append((x, y, vu, vf, vb))
    A(f"{lab}: {agree} of {tot} links give the same verdict with child mortality only, women's work only and both; "
      f"{len(flips)} differ between the two single-control versions")
    for x, y, vu, vf, vb in flips[:10]:
        A(f"   {x}->{y}: +u5mr {vu}, +flfp {vf}, both {vb}")

# ---------- 7. negative control: deliberately controlling a mediator ----------
A("")
A("=== negative control: deliberately control a MEDIATOR (rule violation) and let the estimate collapse ===")
shown = 0
for x, y in PAIRS:
    for c in ("u5mr", "flfp"):
        if not MED[f"{x}|{y}"][c] or c in (x, y):
            continue
        for t, lab in ((0, "country effects"), (1, "country trends")):
            b, r = get(x, y, t, "base"), get(x, y, t, c)
            if not (b and r) or r["add"].get(c) is None:
                continue
            vb = verdict(b["b"], b["se"])
            if vb == "null" or len(str(r["n"])) < 3:
                continue
            v = verdict(r["b"], r["se"])
            drop = 1 - abs(r["b"]) / abs(b["b"]) if b["b"] else 0
            A(f"   {lab}, {x}->{y} controlling its mediator {c}: {vb} {b['b']:+.3f}({b['se']:.3f}) n={b['n']} -> "
              f"{v} {r['b']:+.3f}({r['se']:.3f}) n={r['n']}  (estimate shrinks {100*drop:.0f}%)")
            shown += 1
            if shown >= 10:
                break
        if shown >= 10:
            break
    if shown >= 10:
        break

open(f"{RES}/summary.txt", "w").write("\n".join(L) + "\n")
print("\n".join(L))
