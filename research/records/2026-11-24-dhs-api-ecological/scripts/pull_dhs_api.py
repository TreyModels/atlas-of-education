#!/usr/bin/env python3
"""Pull and cache DHS public-API indicator data for the ecological schooling->fertility sprint.

Pre-registered indicator set (see ../PRE_REGISTRATION.md; committed at 88073d0 before any value was pulled):

  cell level (education breakdown available -- audited):
    A FE_FRTY_W_MNC   completed fertility of women 40-49        (cumulative births)
    B FE_FRTR_W_TFR   total fertility rate 15-49                (period births)
    C PR_WTFR_W_WFR   total wanted fertility rate               (period desired births)
    D PR_DESL_W_WNM   women who want no more children           (stated preference)
    E FE_AAFB_W_M25   median age at first birth, women 25-29    (tempo)
    F FE_FRTR_W_GFR   general fertility rate                    (period births, robustness)
  survey level (NO education breakdown -- the point):
    G FE_CEBA_W_MNC   mean number of children ever born         (by age group)
    H FE_CEBA_W_MND   mean number of children died              (by age group)
  modifier:
    ED_EDUC_W_SEH     women with secondary+ (by age group, for pipeline density)

No key, no login. Only public endpoints. Cached JSON is a documented subset of the response: the analysis
categories (Education, Education (2 groups), the age groups used, and Total where present) are kept so the
cache stays reviewable; the exact query below reproduces the full response.

Usage:  python3 pull_dhs_api.py            # uses the cache if present
        python3 pull_dhs_api.py --force    # re-pulls everything
"""
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://api.dhsprogram.com/rest/dhs"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
RAW = os.path.join(DATA, "raw")
UA = "Mozilla/5.0 (research; atlas-of-education; dhs-api-ecological)"
SLEEP = 0.4

FIELDS = ("IndicatorId,Indicator,CountryName,DHS_CountryCode,SurveyId,SurveyYear,SurveyType,"
          "SurveyYearLabel,CharacteristicId,CharacteristicCategory,CharacteristicLabel,Value,"
          "DenominatorUnweighted,DenominatorWeighted,CILow,CIHigh,IsPreferred,IsTotal,"
          "ByVariableId,ByVariableLabel")

# indicator -> categories kept in the cache
KEEP = {
    "FE_FRTY_W_MNC":   {"Education", "Education (2 groups)"},
    "FE_FRTR_W_TFR":   {"Education", "Education (2 groups)"},
    "PR_WTFR_W_WFR":   {"Education", "Education (2 groups)"},
    "PR_DESL_W_WNM":   {"Education", "Education (2 groups)"},
    "FE_AAFB_W_M25":   {"Education", "Education (2 groups)"},
    "FE_FRTR_W_GFR":   {"Education", "Education (2 groups)"},
    "FE_CEBA_W_MNC":   {"Age (5-year groups)", "Total"},
    "FE_CEBA_W_MND":   {"Age (5-year groups)", "Total"},
    "ED_EDUC_W_SEH":   {"Age (5-year groups)", "Total", "Total 15-49", "Age (10-year groups)"},
}
INDICATORS = list(KEEP)

SURVEY_FIELDS = ("SurveyId,CountryName,DHS_CountryCode,SurveyYear,SurveyType,SurveyStatus,"
                 "NumberOfWomen,RegionName,SubregionName,FieldworkStart,FieldworkEnd")


def fetch(url, tries=4):
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001 - want the retry for any transport error
            last = e
            time.sleep(1.5 * (k + 1))
    raise RuntimeError(f"failed {url}: {last}")


def pull_pages(path, extra):
    out, page, total = [], 1, 1
    while page <= total:
        url = f"{BASE}/{path}?{extra}&f=json&perpage=1000&page={page}"
        d = fetch(url)
        out += d.get("Data", [])
        total = int(d.get("TotalPages", 1))
        page += 1
        time.sleep(SLEEP)
    return out


def pull_indicator(ind, force=False):
    fp = os.path.join(RAW, f"{ind}.json")
    if os.path.exists(fp) and not force:
        return json.load(open(fp)), "cached"
    records = pull_pages("data", "indicatorIds=" + urllib.parse.quote(ind) + "&breakdown=background"
                         + "&returnFields=" + urllib.parse.quote(FIELDS, safe=","))
    keep = KEEP[ind]
    trimmed = [r for r in records if r.get("CharacteristicCategory") in keep]
    if ind == "PR_DESL_W_WNM":
        # this indicator is also crossed with number of living children (a second dimension exposed via
        # ByVariableId); ByVariableId == 1000 ("Total" by-variable) is the education main effect.
        trimmed = [r for r in trimmed if str(r.get("ByVariableId")) == "1000"]
    # national totals separately (no breakdown); keeps a "Total" row for every survey
    tot = pull_pages("data", "indicatorIds=" + urllib.parse.quote(ind)
                     + "&returnFields=" + urllib.parse.quote(FIELDS, safe=","))
    tot = [r for r in tot if str(r.get("ByVariableId", "1000")) == "1000"]
    trimmed += [dict(r, CharacteristicCategory="Total") for r in tot]
    json.dump({"indicator": ind, "query_categories_kept": sorted(keep),
               "n_background_records": len(records), "n_kept": len(trimmed),
               "filter": "PR_DESL: ByVariableId==1000 (education main effect)" if ind == "PR_DESL_W_WNM" else "all",
               "records": trimmed}, open(fp, "w"))
    return {"records": trimmed}, "pulled"


def pull_meta(name, path, fields):
    fp = os.path.join(DATA, f"{name}.json")
    if os.path.exists(fp):
        return "cached"
    rows = pull_pages(path, "returnFields=" + urllib.parse.quote(fields, safe=","))
    json.dump(rows, open(fp, "w"))
    return f"pulled {len(rows)}"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    force = "--force" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")
    os.makedirs(RAW, exist_ok=True)
    print(pull_meta("raw_surveys", "surveys", SURVEY_FIELDS))
    print(pull_meta("raw_countries", "countries",
                    "DHS_CountryCode,CountryName,ISO3_CountryCode,RegionName,SubregionName"))
    for ind in INDICATORS:
        if only and ind not in only:
            continue
        d, how = pull_indicator(ind, force or (only is not None))
        cats = sorted({r["CharacteristicCategory"] for r in d["records"]})
        print(f"{ind:16s} {how:7s} kept={len(d['records']):6d} cats={cats}")
    files = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(DATA) for f in fs
                   if f.endswith((".json", ".csv")))
    with open(os.path.join(DATA, "MANIFEST.sha256"), "w") as fh:
        for f in files:
            fh.write(f"{sha256(f)}  {os.path.relpath(f, HERE)}\n")
    print("manifest:", len(files), "files")


if __name__ == "__main__":
    main()
