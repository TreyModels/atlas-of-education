"""Fertility-decline vs agricultural-release ordering with boundary dates treated as censored (review 2026-11-24).

Fertility dates are left-censored at 1965 (50 of 127 sit there) and release dates at 1991 (65 of 134), so
"fertility before release" is nearly guaranteed by the windows for any country whose fertility date is at the boundary.
Classes: fertility censored (F <= 1965 < 1991 <= R)      -> fertility first, identified (and uninformative about timing)
         both exact                                       -> compared directly
         release censored, fertility exact                -> release first/tie only if F >= 1991, else undetermined
Output: results/sequencing_fertility_release.json
"""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); REC = os.path.dirname(HERE)
rows = list(csv.DictReader(open(os.path.join(REC, "results", "event_dates.csv"))))
num = lambda x: float(x) if x not in ("", None) else None
a3 = [r for r in rows if all(num(r[k]) is not None for k in ("release", "schooling", "fertility"))]
c = dict(fertility_censored_fertility_first=0, both_exact_fertility_first=0, both_exact_release_first=0, both_exact_tie=0,
         release_censored_release_first_or_tie=0, undetermined=0)
for r in a3:
    F, R = num(r["fertility"]), num(r["release"])
    fc, rc = F == 1965.0, R == 1991.0
    if fc:
        c["fertility_censored_fertility_first"] += 1
    elif not rc:
        c["both_exact_fertility_first" if F < R else "both_exact_release_first" if F > R else "both_exact_tie"] += 1
    elif F >= 1991.0:
        c["release_censored_release_first_or_tie"] += 1
    else:
        c["undetermined"] += 1
out = dict(n=len(a3), **c,
           exact_comparison_only=dict(n=c["both_exact_fertility_first"] + c["both_exact_release_first"] + c["both_exact_tie"],
                                      fertility_first=c["both_exact_fertility_first"], release_first=c["both_exact_release_first"]),
           note="Fertility-censored pairs are fertility-first by the windows; only the both-exact block says anything about timing.")
json.dump(out, open(os.path.join(REC, "results", "sequencing_fertility_release.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
