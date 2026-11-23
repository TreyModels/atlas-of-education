"""Tables for the transition record: cohort fertility by arm, the mortality counterfactual, sensitivity."""
import json, sys
import numpy as np
r = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "trans_results.json"))
rows = r["rows"]; CO = r["cohorts"]; ISOS = []
for m in r["meta"]:
    if m["iso"] not in ISOS: ISOS.append(m["iso"])
def get(iso, arm, band):
    return [x for x in rows if x["iso"] == iso and x["arm"] == arm and x["band"] == band][0]
print("SCALE: %.2fM women, %.0fM woman-years, wall %.2fs, %.1fM women/s, %d runs of %d women"
      % (r["women"] / 1e6, r["woman_years"] / 1e6, r["wall_sec"], r["throughput_women_per_sec"] / 1e6,
         r["runs"], r["women"] // r["runs"]))
C0, CM_, C1 = CO[0], CO[len(CO) // 2], CO[-1]
print("\n1. COHORT FERTILITY (births by age 49), central coefficient")
print("| country | arm | %d | %d | %d | change |" % (C0, CM_, C1))
print("|---|---|---|---|---|---|")
for iso in ISOS:
    for arm in ("history", "frozen"):
        cf = np.array(get(iso, arm, "mid")["cohort_fertility"])
        print("| %s | %s | %.2f | %.2f | %.2f | %+.2f |" % (iso, arm, cf[0], cf[6], cf[-1], cf[-1] - cf[0]))
print("\n2. THE COUNTERFACTUAL: change from the %d cohort to the %d cohort" % (C0, C1))
print("| country | history | frozen mortality | share of the change removed by freezing mortality |")
print("|---|---|---|---|")
shares = []
for iso in ISOS:
    h = np.array(get(iso, "history", "mid")["cohort_fertility"])
    f = np.array(get(iso, "frozen", "mid")["cohort_fertility"])
    fh, ff = h[-1] - h[0], f[-1] - f[0]
    sh = (ff - fh) / fh if abs(fh) > 1e-9 else np.nan
    shares.append(sh)
    print("| %s | %+.2f | %+.2f | %+.1f%% |" % (iso, fh, ff, 100 * sh))
print("mean across countries: history %+.2f, frozen %+.2f, share of the change removed %+.1f%%"
      % (np.mean([np.subtract(*np.array(get(i, 'history', 'mid')['cohort_fertility'])[[-1, 0]]) for i in ISOS]),
         np.mean([np.subtract(*np.array(get(i, 'frozen', 'mid')['cohort_fertility'])[[-1, 0]]) for i in ISOS]),
         100 * np.nanmean(shares)))
print("\n3. SENSITIVITY to the mortality coefficient (+/-50%%)")
print("| coefficient (births per point of child mortality) | mean fall, history | mean fall, frozen | share removed |")
print("|---|---|---|---|")
for band, lab in (("lo", "0.00335 (-50%)"), ("mid", "0.00670 (central)"), ("hi", "0.01005 (+50%)")):
    fh = np.mean([np.subtract(*np.array(get(iso, "history", band)["cohort_fertility"])[[-1, 0]]) for iso in ISOS])
    ff = np.mean([np.subtract(*np.array(get(iso, "frozen", band)["cohort_fertility"])[[-1, 0]]) for iso in ISOS])
    print("| %s | %+.2f | %+.2f | %.0f%% |" % (lab, fh, ff, 100 * (ff - fh) / fh))
print("\n4. IS THE PRE-ANTIBIOTIC CORNER REACHABLE?")
mx = max(np.array(get(i, "frozen", "hi")["cohort_fertility"]).max() for i in ISOS)
print("maximum cohort fertility anywhere in the runs: %.2f births per woman (%d cohort, frozen mortality, high coefficient)" % (mx, C0))
print("historical pre-antibiotic effective fertility in the data: 2.54 surviving children per woman;")
print("implied total fertility about 3.6-4.0 (derived) and about 5 in national historical series.")
print("\n5. CHILDLESSNESS at the ends of the arc (central coefficient)")
for iso in ISOS[:3]:
    h = np.array(get(iso, "history", "mid")["cohort_childless"])
    f = np.array(get(iso, "frozen", "mid")["cohort_childless"])
    print("  %s: never-childless share 1890 %.2f -> 1955 %.2f (history); frozen %.2f -> %.2f" % (iso, h[0], h[-1], f[0], f[-1]))
