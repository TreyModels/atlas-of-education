#!/usr/bin/env python3
"""Acquire the WDI primary GER outcome panel used by the E8 Fisher RI record.

Source (public): World Bank WDI bulk CSV for SE.PRM.ENRR
  https://api.worldbank.org/v2/en/indicator/SE.PRM.ENRR?downloadformat=csv
The downloaded zip contains API_SE.PRM.ENRR_DS2_en_csv_v2_*.csv and
Metadata_Country_API_SE.PRM.ENRR_DS2_en_csv_v2_*.csv.

The script (1) downloads the bulk zip, (2) records its sha256 and the WDI "Last Updated Date",
(3) extracts API_*/Metadata_* into data/wdi_SE.PRM.ENRR/ (the layout the E8 record script expects),
(4) writes the exact analysis panel data/e8_primary_ger_panel.csv (iso3,year,value; years 1990-2015,
    every country present in the raw series) and the SSA region map data/wdi_region_map.csv,
(5) writes data/SHA256SUMS. If data/_raw_sha256.txt exists, the fresh download is verified against it
    and the script exits non-zero on a vintage mismatch (so a revision cannot silently change the panel).

The exact parsing of step (4) is exposed as build_long_panel() and is the *same function* the
reproduction gate uses, so the committed panel and the gate compare like with like.

Run:  /Users/treymenefee/neon-boot/venv/bin/python data/acquire_wdi.py [--force]
"""
import argparse
import hashlib
import os
import re
import sys
import zipfile
import urllib.request

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)                      # record root
URL = "https://api.worldbank.org/v2/en/indicator/SE.PRM.ENRR?downloadformat=csv"
IND = "SE.PRM.ENRR"
RAW_DIR = os.path.join(HERE, f"wdi_{IND}")
ZIP_CACHE = os.path.join(HERE, f"wdi_{IND}.zip")
PANEL = os.path.join(HERE, "e8_primary_ger_panel.csv")
REGION = os.path.join(HERE, "wdi_region_map.csv")
SUMS = os.path.join(HERE, "SHA256SUMS")
PIN = os.path.join(HERE, "_raw_sha256.txt")
YEAR_LO, YEAR_HI = 1990, 2015

UA = {"User-Agent": "Mozilla/5.0 (atlas-of-education E8 RI acquisition; contact repo owner)"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def download():
    req = urllib.request.Request(URL, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r:
        payload = r.read()
    if not payload.startswith(b"PK"):
        raise RuntimeError(f"download did not return a zip (first bytes {payload[:40]!r})")
    return payload


def _api_and_meta():
    api = [f for f in os.listdir(RAW_DIR) if f.startswith("API_")]
    meta = [f for f in os.listdir(RAW_DIR) if f.startswith("Metadata_Country")]
    if len(api) != 1 or len(meta) != 1:
        raise RuntimeError(f"expected one API_*.csv and one Metadata_Country_*.csv in {RAW_DIR}; "
                           f"found api={api} meta={meta}")
    return os.path.join(RAW_DIR, api[0]), os.path.join(RAW_DIR, meta[0])


def build_long_panel():
    """Exact long panel (iso3,year,value) from the extracted raw WDI API csv, years 1990-2015.

    This is the same arithmetic as load_wdi_outcome()+build_panel() in
    e8_fee_event_study.py @ bd782be: skiprows=4, melt the year columns, drop missing values.
    """
    api_path, _ = _api_and_meta()
    raw = pd.read_csv(api_path, skiprows=4)
    year_cols = [c for c in raw.columns if str(c).strip().isdigit()]
    long = raw.melt(id_vars=["Country Code"], value_vars=year_cols, var_name="year", value_name="value")
    long = long.dropna(subset=["value"]).copy()
    long["year"] = long["year"].astype(int)
    long = long.rename(columns={"Country Code": "iso3"})[["iso3", "year", "value"]]
    panel = long[(long.year >= YEAR_LO) & (long.year <= YEAR_HI)]
    return panel.sort_values(["iso3", "year"]).reset_index(drop=True)[["iso3", "year", "value"]]


def build_region_map():
    _, meta_path = _api_and_meta()
    md = pd.read_csv(meta_path)
    return (md[["Country Code", "Region"]]
            .rename(columns={"Country Code": "iso3"})
            .sort_values("iso3").reset_index(drop=True))


def wdi_last_updated():
    api_path, _ = _api_and_meta()
    with open(api_path, encoding="utf-8-sig") as f:
        head = "".join(f.readline() for _ in range(6))
    m = re.search(r"Last Updated Date[^\n]*?(\d{4}-\d{2}-\d{2})", head)
    return m.group(1) if m else "UNKNOWN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download even if the zip cache exists")
    args = ap.parse_args()
    os.makedirs(RAW_DIR, exist_ok=True)
    if args.force or not os.path.exists(ZIP_CACHE):
        payload = download()
        with open(ZIP_CACHE, "wb") as f:
            f.write(payload)
        print(f"downloaded {URL} -> {ZIP_CACHE} ({len(payload)} bytes)")
    zip_sha = sha256_file(ZIP_CACHE)
    print(f"raw zip sha256 = {zip_sha}")
    if os.path.exists(PIN) and not args.force:
        with open(PIN) as f:
            pin = f.read().split()[0]
        if pin != zip_sha:
            sys.exit(f"VINTAGE MISMATCH: fresh download sha256 {zip_sha} != pinned {pin}.\n"
                     f"This is a reportable data-vintage failure, not something to paper over. "
                     f"Use --force only if the record is deliberately being re-based.")
    with open(PIN, "w") as f:
        f.write(zip_sha + "\n")
    with zipfile.ZipFile(ZIP_CACHE) as z:
        print("extracted:", z.namelist())
        z.extractall(RAW_DIR)
    api_path, meta_path = _api_and_meta()
    last_updated = wdi_last_updated()
    print(f"WDI Last Updated Date = {last_updated}")
    print(f"API csv sha256 = {sha256_file(api_path)}")

    panel = build_long_panel()
    panel.to_csv(PANEL, index=False)
    print(f"wrote {PANEL}: {len(panel)} rows, {panel.iso3.nunique()} countries, {YEAR_LO}-{YEAR_HI}")

    reg = build_region_map()
    reg.to_csv(REGION, index=False)
    n_ssa = int(reg.Region.fillna("").str.contains("Sub-Saharan").sum())
    print(f"wrote {REGION}: {len(reg)} rows; {n_ssa} Sub-Saharan Africa countries")

    rows = [
        (f"wdi_{IND}.zip (downloaded {URL})", zip_sha, os.path.getsize(ZIP_CACHE)),
        (os.path.basename(api_path), sha256_file(api_path), os.path.getsize(api_path)),
        (os.path.basename(meta_path), sha256_file(meta_path), os.path.getsize(meta_path)),
        ("e8_primary_ger_panel.csv", sha256_file(PANEL), os.path.getsize(PANEL)),
        ("wdi_region_map.csv", sha256_file(REGION), os.path.getsize(REGION)),
    ]
    with open(SUMS, "w") as f:
        f.write("wdi_last_updated_date=" + last_updated + "\n")
        for name, digest, size in rows:
            f.write(f"{digest}  {name}  ({size} bytes)\n")
    print(f"wrote {SUMS}")


if __name__ == "__main__":
    main()
