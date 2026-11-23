#!/usr/bin/env python3
"""Enumerate the DHS individual-level dataset files that exist in the public metadata API.

The metadata API lists every released file (file name, survey, format, size) but does NOT expose a
public download link: the flat files themselves are behind a registered-account login.  This script
records the inventory so the report can say exactly what a manual download would need.
Output: /root/work/dhs/data/dhs_individual_files.csv and a printed summary.
"""
import urllib.request, json, csv, collections


def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=60))


rows = []
page = 1
total = 1
while page <= total:
    d = get(f"https://api.dhsprogram.com/rest/dhs/datasets?returnFormat=json&f=json&perpage=1000&page={page}")
    total = int(d.get("TotalPages", 1))
    rows += d["Data"]
    page += 1
print("dataset file records:", len(rows))
ft = collections.Counter(r.get("FileType", "") for r in rows)
for k, v in ft.most_common(12):
    print(f"  {k}: {v}")
ind = [r for r in rows if "individual" in str(r.get("FileType", "")).lower()]
lr = [r for r in rows if str(r.get("FileType", "")).lower() == "individual recode"]
print("individual-level file records:", len(ind))
print("Individual Recode records:", len(lr))
print("countries with individual recode records:", len(set(r["CountryName"] for r in lr)))
print("example:", [(r["CountryName"], r["SurveyYear"], r["FileName"]) for r in lr[:6]])
with open("/root/work/dhs/data/dhs_individual_files.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["FileName", "CountryName", "SurveyYear", "SurveyId", "DatasetType", "FileType", "FileFormat", "FileSize"])
    for r in ind:
        w.writerow([r.get("FileName"), r.get("CountryName"), r.get("SurveyYear"), r.get("SurveyId"),
                    r.get("DatasetType"), r.get("FileType"), r.get("FileFormat"), r.get("FileSize")])
print("wrote /root/work/dhs/data/dhs_individual_files.csv")
