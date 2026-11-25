#!/usr/bin/env python3
"""summarise.py -- turn the run artifacts into non-disclosive markdown tables.

Reads runs/<run>/estimates.csv, status.csv, designs.csv, contrasts.csv and writes
SUMMARY.md + hashes.txt. Only design-based aggregates are emitted; no unit-level
record ever leaves the local machine.
"""
import hashlib, json, os, sys
import pandas as pd

run = sys.argv[1] if len(sys.argv) > 1 else "runs/2026-11-25_all"
norm = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/neon-boot/dhs8_local/normalized_all.csv")
E = pd.read_csv(os.path.join(run, "estimates.csv"))
S = pd.read_csv(os.path.join(run, "status.csv"))
C = pd.read_csv(os.path.join(run, "contrasts.csv"))
D = pd.read_csv(os.path.join(run, "designs.csv"))

L = []
w = L.append
w("# Run summary — eight DHS descriptive experiments\n")
w(f"Run directory: `{run}`  ")
w(f"Estimates: {len(E)} rows over {E.groupby(['experiment','country','wave']).ngroups} experiment-cells; "
  f"designs: {len(D)}.\n")

# ---------------- coverage / missingness ----------------
w("## 1. Coverage and missingness\n")
w("`complete` is the analysable domain count after dropping missing outcome or grouping; "
  "`eligible` is the age-and-sex eligible domain. A domain mean is only reported where "
  "complete >= 50.\n")
S2 = S.copy()
S2["loss_pct"] = (100 * (1 - S2["n_complete"] / S2["n_eligible"])).round(2)
piv = S2.pivot_table(index=["country", "wave"], columns="experiment",
                     values="n_complete", aggfunc="first")
w("### 1a. Analysable n by country-wave and experiment\n")
w(piv.fillna(0).astype(int).to_markdown())
w("\n### 1b. Cell status\n")
w(S2.groupby("status").size().rename("cells").to_frame().to_markdown())
w("")

# ---------------- status matrix ----------------
w("## 2. Which experiments are computable where\n")
m = S2.assign(ok=S2.status.str.startswith("ok")).pivot_table(
    index=["country", "wave"], columns="experiment", values="ok", aggfunc="first")
w(m.where(m.notna(), False).astype(bool).replace({True: "ok", False: "—"}).to_markdown())
w("")

# ---------------- per-experiment tables ----------------
NAMES = {
 "E1": "Attendance (persons 14–17) by wealth quintile",
 "E2": "Attendance (persons 14–17) by residence",
 "E3": "Attendance (persons 14–17) by sex",
 "E4": "Children ever born (women 40–49) by years of schooling",
 "E5": "Birth before age 20 (women 25–34) by years of schooling",
 "E6": "Current school participation (women 20–24) by residence",
 "E7": "Union before age 20 (women 25–34) by years of schooling",
 "E8": "Current household size (women 40–49) by years of schooling",
}
w("## 3. Estimates by experiment\n")
w("Estimates are weighted domain means with Taylor-linearised design-based SEs "
  "(PSU within stratum, no finite-population correction). `flag_*` marks unreliable cells.\n")
for k in [f"E{i}" for i in range(1, 9)]:
    sub = E[E.experiment == k]
    if sub.empty:
        w(f"### {k}. {NAMES[k]}\n\n*No estimates: no usable data (see §2).*\n")
        continue
    w(f"### {k}. {NAMES[k]}\n")
    t = sub[["country", "wave", "group", "estimate", "se", "lo95", "hi95", "n", "n_psu", "cv"]].copy()
    for c in ["estimate", "se", "lo95", "hi95"]:
        t[c] = (100 * t[c]).round(2) if k in ("E1", "E2", "E3", "E5", "E6", "E7") else t[c].round(3)
    t["cv"] = t["cv"].round(3)
    w(t.to_markdown(index=False))
    bad = sub[sub.flag_small_n | sub.flag_high_cv | sub.flag_few_psu]
    if len(bad):
        w(f"\n*Flagged unreliable cells: {len(bad)}* "
          f"(small n: {int(bad.flag_small_n.sum())}, CV>0.30: {int(bad.flag_high_cv.sum())}, "
          f"<10 PSUs: {int(bad.flag_few_psu.sum())}).\n")
    else:
        w("\n*No cell flagged unreliable.*\n")

# ---------------- contrasts ----------------
w("## 4. Design-based contrasts\n")
w("Differences of domain means with covariances from the same design (`svycontrast`). "
  "Sign convention: **positive = the first-listed (lower) group has the larger value.** "
  "E1 Q1−Q5; E2/E6 rural−urban; E3 male−female; E4/E5/E7/E8 <6 years − 12+ years.\n")
cc = C[~C.difference.isna()].copy()
cc["ci"] = cc.apply(lambda r: f"[{r.lo95:+.3f}, {r.hi95:+.3f}]", axis=1)
w(cc[["experiment", "country", "wave", "mean_ref", "mean_alt", "difference", "se", "ci", "z", "p", "p_holm"]]
  .to_markdown(index=False, floatfmt=".3f"))
w("\nHolm-adjusted p-values are within each experiment×country family of waves.\n")

# ---------------- negative / null results ----------------
w("## 5. Null and negative results\n")
ns = cc[cc.p_holm > 0.05] if not cc.empty else cc
if len(ns):
    w(cc[cc.p > 0.05][["experiment", "country", "wave", "difference", "se", "p"]].to_markdown(index=False, floatfmt=".4f"))
else:
    w("*All contrasts have p<0.05 before adjustment.*")
w("")

# ---------------- hashes ----------------
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

lines = []
for p in ["engine/experiments_v2.R", "engine/contrasts.R", "engine/run_tests.R",
          "engine/validate_benchmarks.R", "harmonize/harmonize.py"]:
    if os.path.exists(p):
        lines.append(f"{sha(p)}  {p}")
lines.append(f"{sha(norm)}  {os.path.basename(norm)}  (LOCAL-ONLY, not committed)")
for f in ["estimates.csv", "status.csv", "designs.csv", "contrasts.csv", "run_meta.txt"]:
    fp = os.path.join(run, f)
    if os.path.exists(fp):
        lines.append(f"{sha(fp)}  {run}/{f}")
open(os.path.join(run, "hashes.txt"), "w").write("\n".join(lines) + "\n")
w("## 6. Hashes\n\n```\n" + "\n".join(lines) + "\n```\n")

open(os.path.join(run, "SUMMARY.md"), "w").write("\n".join(L))
print(f"wrote {run}/SUMMARY.md ({len(L)} blocks) and hashes.txt")
