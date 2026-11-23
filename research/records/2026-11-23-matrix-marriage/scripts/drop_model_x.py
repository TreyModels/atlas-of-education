#!/usr/bin/env python3
"""Drop the UN model-based estimate rows for the marriage links that survived
the circular-shift permutation but are NOT marriage-as-outcome links (those are
covered in falsify_matrix.py).  Same test, opposite direction of the link.

Writes out/drop_model_x.json.
"""
import json
from edge_marriage import S, build_rows, fit
from falsify_matrix import census_survey_series, MARRIAGE

# Note: importing falsify_matrix above already applies the session rule's income
# log to the shared series dict, so it must not be applied twice here.

LINKS = [("smam_f", "fertility"),
         ("smam_gap", "prm_cmp"),
         ("smam_gap", "u5mr"),
         ("smam_gap", "electricity"),
         ("nevermar_f_4549", "emp_agri"),
         ("nevermar_f_4549", "tax")]

if __name__ == "__main__":
    M = json.load(open("out/matrix20.json"))
    filt = census_survey_series()
    old = {k: S[k] for k in MARRIAGE}
    out = {}
    try:
        for k in MARRIAGE:
            S[k] = dict(filt[k])
        for x, y in LINKS:
            key = f"{x}->{y}"
            out[key] = {}
            for setting, trend in (("fe", False), ("trend", True)):
                r = fit(build_rows(x, y, "grid10"), trend, x, y)
                full = M[key][setting]
                out[key][setting] = dict(
                    full_b=full["b"] if full else None,
                    full_se=full["se"] if full else None,
                    filt_b=r["b"] if r else None,
                    filt_se=r["se"] if r else None,
                    filt_n=r["n"] if r else None,
                    filt_nc=r["nc"] if r else None,
                    same_sign=(None if (full is None or r is None)
                               else bool((full["b"] > 0) == (r["b"] > 0))),
                    still_sig=(None if (full is None or r is None) else
                               bool(abs(r["b"] / r["se"]) > 1.96)))
                print(f"{key:32s} {setting:5s} full={full['b'] if full else None} "
                      f"filt={out[key][setting]['filt_b']} "
                      f"n={out[key][setting]['filt_n']} "
                      f"same_sign={out[key][setting]['same_sign']} "
                      f"still_sig={out[key][setting]['still_sig']}")
    finally:
        for k, v in old.items():
            S[k] = v
    json.dump(out, open("out/drop_model_x.json", "w"), indent=1)
    print("wrote out/drop_model_x.json")
