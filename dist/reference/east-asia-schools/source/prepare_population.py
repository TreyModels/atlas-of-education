"""Extract the 2015–2050 school-age slice of the official WPP 2024 bulk files."""
import csv
import gzip
import json
import sys
from pathlib import Path

countries = {392: "Japan", 410: "South Korea", 158: "Taiwan", 764: "Thailand"}
result = {name: {} for name in countries.values()}
base, out = map(Path, sys.argv[1:3])
for period in ("1950-2023", "2024-2100"):
    path = base / f"WPP2024_PopulationBySingleAgeSex_Medium_{period}.csv.gz"
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        for r in csv.DictReader(stream):
            loc = int(r["LocID"])
            if loc not in countries:
                continue
            year = int(r["Time"])
            age = int(r["AgeGrpStart"])
            if 2015 <= year <= 2050 and age <= 17:
                ages = result[countries[loc]].setdefault(year, [None]*18)
                assert ages[age] is None
                ages[age] = round(float(r["PopTotal"])*1000)
for name, series in result.items():
    assert set(series) == set(range(2015, 2051)), name
    assert all(v > 0 for ages in series.values() for v in ages), name
out.write_text(json.dumps(result,separators=(",",":"))+"\n",encoding="utf-8")
