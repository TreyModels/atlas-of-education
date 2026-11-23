#!/usr/bin/env python3
"""Pull DHS public API indicator extracts for the schooling -> children-ever-born test.

Indicators used (provenance: api.dhsprogram.com, public DHS Program indicator API, 23 Nov 2026):
  FE_FRTY_W_MNC  completed fertility of women age 40-49 (mean children ever born) - main outcome
                 breakdown: Education, Education (2 groups), Wealth quintile, Residence, Region
  FE_AAFB_W_M25  median age at first birth, women 25-29 - tempo measure, breakdown by Education
  ED_EDUC_W_SEH / ED_EDUC_W_SSC / ED_EDUC_W_NED / ED_EDUC_W_TOT  women's education distribution
                 (pipeline density: share of women with secondary or higher)
  FE_CEBA_W_MNC  mean children ever born by age group - data sanity / life-cycle check
Output: /root/work/dhs/data/dhs_extract.csv (long format), /root/work/dhs/data/pull_log.txt
"""
import urllib.request, json, csv, time, os

BASE = "https://api.dhsprogram.com/rest/dhs"
IND = ["FE_FRTY_W_MNC", "FE_AAFB_W_M25", "ED_EDUC_W_SEH", "ED_EDUC_W_SSC", "ED_EDUC_W_NED",
       "ED_EDUC_W_TOT", "ED_EDUC_W_MYR", "FE_CEBA_W_MNC"]
OUT = "/root/work/dhs/data"


def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research; atlas-of-education)"})
            return json.load(urllib.request.urlopen(req, timeout=45))
        except Exception as e:
            print("retry", k, url[:90], e, flush=True)
            time.sleep(2 + 2 * k)
    raise RuntimeError("failed " + url)


def fetch_indicator(ind):
    rows = []
    page = 1
    total = 1
    while page <= total:
        u = (f"{BASE}/data?indicatorIds={ind}&breakdown=background&returnFormat=json&f=json"
             f"&perpage=1000&page={page}")
        d = get(u)
        data = d.get("Data", [])
        total = int(d.get("TotalPages", 1))
        rows += data
        print(f"  {ind} page {page}/{total} rows_so_far {len(rows)}", flush=True)
        page += 1
        if page > 200:
            break
    print(ind, "rows", len(rows), flush=True)
    return rows


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    log = []
    allrows = []
    for ind in IND:
        rows = fetch_indicator(ind)
        log.append(f"{ind}: {len(rows)} rows")
        allrows += rows
    cols = ["IndicatorId", "Indicator", "CountryName", "DHS_CountryCode", "SurveyId", "SurveyYear",
            "SurveyType", "CharacteristicId", "CharacteristicCategory", "CharacteristicLabel", "Value",
            "DenominatorWeighted", "DenominatorUnweighted", "CILow", "CIHigh", "IsPreferred", "IsTotal"]
    with open(f"{OUT}/dhs_extract.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in allrows:
            w.writerow(r)
    open(f"{OUT}/pull_log.txt", "w").write("\n".join(log) + f"\nTOTAL {len(allrows)} rows\n")
    print("wrote", f"{OUT}/dhs_extract.csv", len(allrows), "rows")
