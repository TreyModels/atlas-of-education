#!/usr/bin/env python3
"""Acquire the WDI/UIS sex-disaggregated primary GER panels for the gender-split E8 record.

Series (World Bank WDI bulk-CSV distribution of the UNESCO UIS series; label OBSERVED (WDI/UIS)):
  SE.PRM.ENRR.FE  primary GER, female (%)
  SE.PRM.ENRR.MA  primary GER, male   (%)
  SE.PRM.ENRR     primary GER, total  (%)  -- reproduction-gate series only

No imputation, interpolation or gap filling: a missing year stays missing in the committed panel.
Raw zips are NOT committed (downloads); their sha256s are recorded in data/input_hashes.csv together with the
URLs and the WDI vintage ("Last Updated Date") read out of each zip.

Usage:
  python3 scripts/acquire_wdi_sex_ger.py                # download, verify, extract, write panels
  python3 scripts/acquire_wdi_sex_ger.py --raw-dir DIR  # keep the raw zips in DIR (default: temp dir, deleted)

Outputs (under the record directory):
  data/wdi_sex_ger_panels.csv        iso3, year, indicator, value  (long; both sexes)
  data/wdi_pooled_ger_panel.csv      iso3, year, indicator, value  (pooled gate series)
  data/wdi_metadata_country.csv      iso3, country, region
  data/input_hashes.csv              sha256 + URL + vintage for each zip and each derived panel
"""
import argparse
import csv
import hashlib
import os
import tempfile
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(REC, "data")
os.makedirs(DATA, exist_ok=True)

BASE = "https://api.worldbank.org/v2/en/indicator/{code}?downloadformat=csv"

# sha256 of the exact zips acquired for this record (2026-11-25, WDI vintage 2026-11-11), see input_hashes.csv
INDICATORS = [
    ("SE.PRM.ENRR", "ca495dfed92b90ea6e99b5d253fb3e5ea702012a206d6fb834588f95ab941d13"),
    ("SE.PRM.ENRR.FE", "c2e6773b06c5dfeb521c975ce3c667ad976281d3d5112a7c6641106d0ad5f879"),
    ("SE.PRM.ENRR.MA", "56f744083e7fab2d5cc95b64d72f143e96c52fbfe333ba9593e2c88b35aef39b"),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(code, dest, expected_sha):
    url = BASE.format(code=code)
    tmp = dest + ".part"
    with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
        f.write(r.read())
    got = sha256_file(tmp)
    os.replace(tmp, dest)
    if expected_sha and got != expected_sha:
        raise SystemExit(f"sha256 mismatch for {code}: got {got}, expected {expected_sha}")
    return url, got


def read_api_csv(path, code):
    """WDI bulk API CSV: 4 leading metadata lines, then a header row of years; long format."""
    import pandas as pd

    raw = pd.read_csv(path, skiprows=4)
    year_cols = [c for c in raw.columns if str(c).strip().isdigit()]
    long = raw.melt(id_vars=["Country Code", "Country Name"], value_vars=year_cols,
                    var_name="year", value_name="value")
    long = long.dropna(subset=["value"]).copy()
    long["year"] = long["year"].astype(int)
    long["value"] = long["value"].astype(float)
    long = long.rename(columns={"Country Code": "iso3", "Country Name": "country"})
    long["indicator"] = code
    return long[["iso3", "indicator", "year", "value"]]


def read_metadata_country(path):
    import pandas as pd

    m = pd.read_csv(path)
    m = m.rename(columns={"Country Code": "iso3", "TableName": "country", "Region": "region"})
    return m[["iso3", "country", "region"]]


def vintage(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        api_name = [n for n in z.namelist() if os.path.basename(n).startswith("API_")][0]
        head = z.read(api_name).decode("utf-8-sig").splitlines()
    for line in head[:5]:
        if line.startswith('"Last Updated Date"'):
            return line.split(",", 1)[1].rstrip(",").strip().strip('"')
    return "UNKNOWN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", default=None)
    args = ap.parse_args()
    tmpdir = args.raw_dir or tempfile.mkdtemp(prefix="wdi_gender_split_")
    os.makedirs(tmpdir, exist_ok=True)

    rows = []
    frames = []
    meta = None
    for code, expected in INDICATORS:
        zip_path = os.path.join(tmpdir, code + ".zip")
        url, sha = download(code, zip_path, expected)
        vint = vintage(zip_path)
        with zipfile.ZipFile(zip_path) as z:
            api_name = [n for n in z.namelist() if os.path.basename(n).startswith("API_")][0]
            mname = [n for n in z.namelist() if os.path.basename(n).startswith("Metadata_Country")][0]
            api_path = os.path.join(tmpdir, os.path.basename(api_name))
            mpath = os.path.join(tmpdir, os.path.basename(mname))
            with open(api_path, "wb") as f:
                f.write(z.read(api_name))
            with open(mpath, "wb") as f:
                f.write(z.read(mname))
        rows.append({"item": code + ".zip", "sha256": sha, "url": url, "path_or_output": os.path.basename(api_name),
                     "note": "WDI bulk CSV zip; vintage (Last Updated Date) = " + vint})
        frames.append(read_api_csv(api_path, code))
        if code == "SE.PRM.ENRR":
            meta = read_metadata_country(mpath)

    import pandas as pd

    alllong = pd.concat(frames, ignore_index=True).sort_values(["indicator", "iso3", "year"])
    sex = alllong[alllong.indicator.isin(["SE.PRM.ENRR.FE", "SE.PRM.ENRR.MA"])].copy()
    pooled = alllong[alllong.indicator == "SE.PRM.ENRR"].copy()

    sex_path = os.path.join(DATA, "wdi_sex_ger_panels.csv")
    pooled_path = os.path.join(DATA, "wdi_pooled_ger_panel.csv")
    meta_path = os.path.join(DATA, "wdi_metadata_country.csv")
    sex.to_csv(sex_path, index=False)
    pooled.to_csv(pooled_path, index=False)
    meta.sort_values("iso3").to_csv(meta_path, index=False)
    for p, n in ((sex_path, len(sex)), (pooled_path, len(pooled)), (meta_path, len(meta))):
        rows.append({"item": os.path.basename(p), "sha256": sha256_file(p), "url": "",
                     "path_or_output": os.path.basename(p), "note": f"{n} rows"})
    with open(os.path.join(DATA, "input_hashes.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "sha256", "url", "path_or_output", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"sex panel rows={len(sex)} pooled rows={len(pooled)} countries_meta={len(meta)}")
    print(open(os.path.join(DATA, "input_hashes.csv")).read())


if __name__ == "__main__":
    main()
