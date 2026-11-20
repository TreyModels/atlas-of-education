#!/usr/bin/env python3
"""T1: Korea private-education spend decomposition (participation x hours x price/hour).
Descriptive decomposition of MODS/KEDI 2023 official tables on disk. No causal claim.
Reproduce: python t1_korea.py  (from this directory; paths absolute below).
"""
import csv, json, math, os

ROOT = "/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20"
INC = os.path.join(ROOT, "04_data/shadow_round2/data/shadow_incidence_round2.csv")
FEE = os.path.join(ROOT, "04_data/shadow_round2/data/shadow_fees_round2.csv")
OUT = os.path.dirname(os.path.abspath(__file__))

# --- read participation and hours by level
part, hours = {}, {}
with open(INC, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("iso3") != "KOR":
            continue
        stage = (r.get("stage") or "").strip().lower()
        if stage not in ("elementary", "middle", "high"):
            continue
        measure = (r.get("measure") or "").lower()
        val = float(r["value"])
        if "participation hours" in measure:
            hours[stage] = val
        elif "participation" in measure:
            part[stage] = val / 100.0

# --- read spend per participating student by level
spend_part = {}
with open(FEE, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("iso3") != "KOR":
            continue
        stage = (r.get("stage") or "").strip().lower()
        if stage not in ("elementary", "middle", "high"):
            continue
        m = (r.get("fee_measure") or "").lower()
        if "expenditure per participating student" in m and r.get("provider_type") in ("any", "all", ""):
            v = r.get("value")
            if v not in (None, ""):
                spend_part[stage] = float(v)  # thousand won / month

WEEKS_PER_MONTH = 52.0 / 12.0
rows = []
for st in ("elementary", "middle", "high"):
    p = part[st]; h = hours[st]; s = spend_part[st]
    spend_month = p * s                      # thousand won / student / month (derived)
    hours_month = h * WEEKS_PER_MONTH
    price = (s * 1000.0) / hours_month        # won per hour (participant basis)
    rows.append(dict(stage=st, participation=p, hours_week=h, spend_participant_kw=s,
                     spend_student_kw=spend_month, hours_month=hours_month, price_won_h=price))

# --- decomposition elementary -> high (log terms)
e, h = rows[0], rows[2]
dln_spend = math.log(h["spend_student_kw"] / e["spend_student_kw"])
comp = {
    "dln_spend": dln_spend,
    "participation": math.log(h["participation"] / e["participation"]),
    "hours": math.log(h["hours_week"] / e["hours_week"]),
    "price": math.log(h["price_won_h"] / e["price_won_h"]),
}
comp["residual"] = dln_spend - (comp["participation"] + comp["hours"] + comp["price"])
price_ratio = h["price_won_h"] / e["price_won_h"]
part_fall = e["participation"] - h["participation"]
hours_fall = e["hours_week"] - h["hours_week"]

# --- predeclared decision rule
if price_ratio - 1.0 >= 0.20 and part_fall > 0 and hours_fall >= 0:
    verdict = "TWO/THREE-MARGIN (one-margin arms-race mechanism must be rewritten)"
elif abs(price_ratio - 1.0) < 0.10:
    verdict = "ONE-MARGIN SURVIVES (price/hour flat)"
else:
    verdict = "INDETERMINATE"

# consistency check vs brief-011 quoted spend/student 398/449/491
expected = {"elementary": 398.0, "middle": 449.0, "high": 491.0}
checks = {r["stage"]: abs(r["spend_student_kw"] - expected[r["stage"]]) / expected[r["stage"]] for r in rows}
consistent = all(v <= 0.01 for v in checks.values())

with open(os.path.join(OUT, "t1_inputs.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["stage","participation_pct","hours_week","spend_participant_kw_month","spend_student_kw_month_derived","hours_month","price_won_per_hour"])
    for r in rows:
        w.writerow([r["stage"], round(r["participation"]*100,1), r["hours_week"], r["spend_participant_kw"],
                    round(r["spend_student_kw"],1), round(r["hours_month"],2), round(r["price_won_h"])])
with open(os.path.join(OUT, "t1_decomposition.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["quantity","value"])
    for k, v in comp.items(): w.writerow([k, round(v, 4)])
    w.writerow(["price_ratio_high_over_elementary", round(price_ratio, 4)])
    w.writerow(["participation_fall_pp", round(part_fall*100, 1)])
    w.writerow(["hours_fall_h_per_week", round(hours_fall, 1)])
    w.writerow(["spend_student_change_pct", round((h["spend_student_kw"]/e["spend_student_kw"]-1)*100, 1)])

summary = dict(rows=rows, decomposition=comp, price_ratio=price_ratio,
               participation_fall_pp=part_fall*100, hours_fall=hours_fall,
               verdict=verdict, consistency_checks=checks, consistent=consistent)
with open(os.path.join(OUT, "t1_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1)
print(json.dumps(summary, indent=1))
