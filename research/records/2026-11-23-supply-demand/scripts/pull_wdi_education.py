#!/usr/bin/env python3
"""Pull the supply-side indicators for the massification test from the World Bank API.

Indicators: public education spending (%GDP), pupil-teacher ratio (primary), primary gross enrolment
(capacity), primary/secondary teachers, secondary enrolment.  The demand-side and outcome series are
already in /root/work/subsistence/data/wdi_long.csv (task-22) and /root/work/transition.
Output: /root/work/supply_demand/data/wdi_education_long.csv
"""
import urllib.request, json, csv, time, os

BASE = "https://api.worldbank.org/v2/country/all/indicator/"
IND = {
    "edu_spend_gdp": "SE.XPD.TOTL.GD.ZS",
    "edu_spend_gov": "SE.XPD.TOTL.GB.ZS",
    "pupil_teacher_primary": "SE.PRM.ENRL.TC.ZS",
    "ger_primary": "SE.PRM.ENRR",
    "ger_secondary": "SE.SEC.ENRR",
    "teachers_primary": "SE.PRM.TCHR",
    "teachers_secondary": "SE.SEC.TCHR",
    "pupil_teacher_secondary": "SE.SEC.ENRL.TC.ZS",
}
OUT = "/root/work/supply_demand/data"


def get(u, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (research)"})
            return json.load(urllib.request.urlopen(req, timeout=90))
        except Exception as e:
            print("retry", k, u[:90], e, flush=True)
            time.sleep(2 + 2 * k)
    return None


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, code in IND.items():
        d = get(f"{BASE}{code}?format=json&per_page=20000&date=1960:2024&page=1")
        if not isinstance(d, list) or len(d) < 2:
            print("NO DATA", name, code, str(d)[:150], flush=True)
            continue
        n = 0
        for r in d[1] or []:
            if r.get("value") is None:
                continue
            rows.append([r.get("countryiso3code") or "", int(r["date"]), name, r["value"]])
            n += 1
        print(name, code, "rows", n, flush=True)
    with open(f"{OUT}/wdi_education_long.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["iso3", "year", "indicator", "value"]); w.writerows(rows)
    print("wrote", len(rows), "rows")
