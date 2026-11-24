#!/usr/bin/env python3
"""Build the REPORT tables from calibration.json and bhby.json."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
RES = os.path.join(REC, "results")


def pct(x):
    return f"{100*x:.1f}%"


def ci(d, key):
    c = d.get(key + "_ci")
    if not c:
        return ""
    return f" [{100*c[0]:.1f}, {100*c[1]:.1f}]"


def main():
    cal = json.load(open(os.path.join(RES, "calibration.json")))
    bh = json.load(open(os.path.join(RES, "bhby.json")))
    L = []
    L.append("### Table 1. Known-truth calibration, main regimes (400 independent replicates each, R = 400 draws)\n")
    L.append("| regime | ROBUST+H | ROBUST-HET | ROBUST-but-GROUP | GROUP | BEATS | NONE | key error rate |")
    L.append("|---|---|---|---|---|---|---|---|")
    labelmap = {"C": "R0 null", "U": "R1 uniform strong (b=0.15)", "B": "R3 minority-only (b=0.40, top third)",
                "D": "R4 shared country trends (no effect)", "S": "R5 sign-split (+/-0.25)"}
    for reg in ("C", "U", "B", "D", "S"):
        d = cal["main"][reg]
        def cell(k):
            return pct(d.get(k + "_rate", 0)) + ci(d, k)
        if reg in ("C", "D"):
            key = f"false-positive **{pct(d['false_positive_rate'])}**" + ci(d, "false_positive")
        elif reg == "U":
            key = f"false-negative **{pct(d['false_negative_rate'])}**" + ci(d, "false_negative")
        elif reg == "B":
            key = (f"planted tag flagged **{pct(d['planted_tag_flagged_rate'])}**" +
                   ci(d, "planted_tag_flagged") + f"; false-ROBUST {pct(d['false_robust_everywhere_rate'])}" +
                   ci(d, "false_robust_everywhere"))
        else:
            key = "descriptive (truth is sign-ambiguous)"
        L.append(f"| {labelmap[reg]} | {cell('ROBUST+H')} | {cell('ROBUST-HET')} | {cell('ROBUST-but-GROUP')} "
                 f"| {cell('GROUP')} | {cell('BEATS')} | {cell('NONE')} | {key} |")
    L.append("")
    L.append("### Table 2. Uniform-effect strength ladder (400 replicates per strength)\n")
    L.append("| b (per country) | ROBUST+H (strict) [95% CI] | any-robust (ROBUST+H + ROBUST-but-GROUP) [95% CI] | NONE (false negative) [95% CI] |")
    L.append("|---|---|---|---|")
    for b in ("0.02", "0.04", "0.06", "0.1", "0.15", "0.25"):
        d = cal["strength_ladder"].get(b) or cal["strength_ladder"].get(str(float(b)))
        if not d:
            continue
        L.append(f"| {b} | {pct(d['ROBUST+H_rate'])} [{100*d['ROBUST+H_ci'][0]:.1f}, "
                 f"{100*d['ROBUST+H_ci'][1]:.1f}] | {pct(d['correct_robust_rate'])} "
                 f"[{100*d['correct_robust_ci'][0]:.1f}, {100*d['correct_robust_ci'][1]:.1f}] | "
                 f"{pct(d['false_negative_rate'])} "
                 f"[{100*d['false_negative_ci'][0]:.1f}, {100*d['false_negative_ci'][1]:.1f}] |")
    L.append("")
    L.append("Canonical source: `results/calibration.json` -> `strength_ladder[b].ROBUST+H_rate` (strict), "
             "`strength_ladder[b].correct_robust_rate` (any-robust), `strength_ladder[b].false_negative_rate`.\n")
    L.append("### Table 3. Design-size grid (200 replicates per cell): Monte Carlo intervals are in Table 1; here the spread is across sample/mechanism cells\n")
    L.append("| regime | N | T | R | key rate [95% CI] |")
    L.append("|---|---|---|---|---|")
    order = [("C", "N80_T50"), ("C", "N150_T30"), ("C", "N150_T50"), ("C", "N150_T60"), ("C", "N220_T50"),
             ("U", "N80_T50"), ("U", "N150_T30"), ("U", "N150_T50"), ("U", "N150_T60"), ("U", "N220_T50"),
             ("B", "N80_T50"), ("B", "N150_T30"), ("B", "N150_T50"), ("B", "N150_T60"), ("B", "N220_T50")]
    for reg, suffix in order:
        d = cal["design_grid"].get(f"{reg}_{suffix}")
        if not d:
            continue
        if reg == "C":
            key = f"FP {pct(d['false_positive_rate'])}" + ci(d, "false_positive")
        elif reg == "U":
            key = (f"any-robust {pct(d['correct_robust_rate'])}" + ci(d, "correct_robust") +
                   f" (strict ROBUST+H {pct(d['ROBUST+H_rate'])})")
        else:
            key = (f"tag hit {pct(d['planted_tag_flagged_rate'])}" + ci(d, "planted_tag_flagged") +
                   f"; false-ROBUST combined {pct(d['false_robust_everywhere_rate'])} "
                   f"(strict ROBUST+H {pct(d['ROBUST+H_rate'])})")
        L.append(f"| {reg} | {d['N']} | {d['T']} | {d['R']} | {key} |")
    L.append("")
    L.append("Canonical source: `results/calibration.json` -> `design_grid[cell].ROBUST+H_rate`, "
             "`.correct_robust_rate`, `.false_robust_everywhere_rate`, `.planted_tag_flagged_rate`.\n")
    L.append("### Table 4. Draw-count axis (200 replicates per cell)\n")
    L.append("| regime | R | key rate [95% CI] |")
    L.append("|---|---|---|")
    for reg in ("C", "U"):
        for R in (100, 400):
            d = cal["R_axis"].get(f"{reg}_R{R}")
            if not d:
                continue
            if reg == "C":
                key = f"FP {pct(d['false_positive_rate'])}" + ci(d, "false_positive")
            else:
                key = (f"any-robust {pct(d['correct_robust_rate'])}" + ci(d, "correct_robust") +
                   f" (strict ROBUST+H {pct(d['ROBUST+H_rate'])})")
            L.append(f"| {reg} | {R} | {key} |")
    L.append("")
    L.append("### Table 5. Full-vector BH and BY on the four real strict-tier families (272 links each)\n")
    L.append("| family | BH (m=272) | BY (m=272) | BH at m_eff=157 (approximation) | min p | links at floor |")
    L.append("|---|---|---|---|---|---|")
    for fam in ("up", "down", "sign_flip", "heterogeneity"):
        f = bh["families"][fam]
        L.append(f"| {fam} | {f['bh']} | {f['by']} | {f['bh_at_m_eff_157']} | {f['min_p']:.5f} | {f['n_at_floor']} |")
    L.append("")
    L.append("### Adequacy benchmarks (pre-registered)\n")
    null_fp = cal["main"]["C"]["false_positive_rate"]
    null_ci = cal["main"]["C"]["false_positive_ci"]
    uni_fn = cal["main"]["U"]["false_negative_rate"]
    uni_ci = cal["main"]["U"]["false_negative_ci"]
    min_hit = cal["main"]["B"]["planted_tag_flagged_rate"]
    min_hit_ci = cal["main"]["B"]["planted_tag_flagged_ci"]
    min_frob = cal["main"]["B"]["false_robust_everywhere_rate"]
    min_frob_ci = cal["main"]["B"]["false_robust_everywhere_ci"]
    trend_fp = cal["main"]["D"]["false_positive_rate"]
    trend_ci = cal["main"]["D"]["false_positive_ci"]
    rows = [
        ("null FP <= 5% with upper CI <= 10%", f"{pct(null_fp)} [{100*null_ci[0]:.1f}, {100*null_ci[1]:.1f}]",
         null_fp <= 0.05 and null_ci[1] <= 0.10),
        ("uniform-strong FN (NONE) <= 5%", f"{pct(uni_fn)} [{100*uni_ci[0]:.1f}, {100*uni_ci[1]:.1f}]", uni_fn <= 0.05),
        ("minority planted-tag hit >= 80%", f"{pct(min_hit)} [{100*min_hit_ci[0]:.1f}, {100*min_hit_ci[1]:.1f}]", min_hit >= 0.80),
        ("minority false-ROBUST <= 10%", f"{pct(min_frob)} [{100*min_frob_ci[0]:.1f}, {100*min_frob_ci[1]:.1f}]", min_frob <= 0.10),
        ("shared-trend FP <= 5%", f"{pct(trend_fp)} [{100*trend_ci[0]:.1f}, {100*trend_ci[1]:.1f}]", trend_fp <= 0.05),
    ]
    L.append("| benchmark | observed | passed |")
    L.append("|---|---|---|")
    for name, obs, ok in rows:
        L.append(f"| {name} | {obs} | {'PASS' if ok else 'FAIL'} |")
    txt = "\n".join(L)
    open(os.path.join(RES, "tables.md"), "w").write(txt + "\n")
    print(txt)
    # machine-readable summary of benchmark results
    json.dump({"benchmarks": [{"name": n, "observed": o, "passed": bool(p)} for n, o, p in rows]},
              open(os.path.join(RES, "benchmarks.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
