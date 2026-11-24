#!/usr/bin/env python3
"""Fetch the observed-core WDI/EdStats panel.

Public World Bank API only; no credentials, no imputation. Writes a tidy long CSV
(OBSERVED tier), a country/region list, and a manifest with retrieval timestamp,
exact API URLs and sha256 of every raw download and output file.

Run: python3 -u scripts/fetch_wdi.py [--date 1970:2023] [--out data] [--workers 8]
"""
import argparse, hashlib, json, os, sys, time, urllib.request, urllib.parse, datetime, csv
from concurrent.futures import ThreadPoolExecutor, as_completed

API = "https://api.worldbank.org/v2"
PER_PAGE = 20000

INDICATORS = {
    "SE.PRM.ENRR": "outcome",
    "SE.SEC.ENRR": "outcome",
    "SE.PRM.CMPT.ZS": "outcome",
    "SE.SEC.CMPT.LO.ZS": "outcome",
    "SE.PRM.ENRL.TC.ZS": "supply",
    "SE.SEC.ENRL.LO.TC.ZS": "supply",
    "SE.PRM.TCHR": "supply",
    "SE.XPD.TOTL.GD.ZS": "supply",
    "SE.XPD.PRIM.PC.ZS": "supply",
    "SE.XPD.SECO.PC.ZS": "supply",
    "SE.PRM.PRIV.ZS": "mix",
    "SE.SEC.PRIV.ZS": "mix",
    "SL.TLF.0714.ZS": "demand_structural",
    "SL.AGR.EMPL.ZS": "demand_structural",
    "SP.URB.TOTL.IN.ZS": "demand_structural",
    "NY.GDP.PCAP.KD": "macro",
    "SP.POP.TOTL": "macro",
}


def get(url, tries=4, timeout=180):
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "atlas-observed-core/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"  retry {k+1}/{tries} {url}: {e}", file=sys.stderr)
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"failed {url}: {last}")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def fetch_one(code, date):
    tmpl = (f"{API}/country/all/indicator/{urllib.parse.quote(code)}"
            f"?format=json&per_page={PER_PAGE}&page={{page}}&date={date}")
    page, pages, rows = 1, 1, []
    while page <= pages:
        raw = get(tmpl.format(page=page))
        doc = json.loads(raw)
        if not isinstance(doc, list) or len(doc) < 2 or doc[1] is None:
            break
        pages = int(doc[0].get("pages", 1))
        rows.extend(doc[1])
        page += 1
    return code, {"url": tmpl.format(page=1), "pages": pages, "rows": rows,
                  "sha256_raw": sha256(json.dumps(rows, sort_keys=True).encode())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="1970:2023")
    ap.add_argument("--out", default="data")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    manifest = {
        "retrieval_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "api": API, "date_range": a.date, "per_page": PER_PAGE,
        "tier": "OBSERVED (public World Bank API; no imputation, no interpolation)",
        "indicators": {}, "files": {},
    }

    raw = get(f"{API}/country?format=json&per_page=400")
    doc = json.loads(raw)
    countries = []
    for c in doc[1]:
        region = (c.get("region") or {}).get("value", "")
        iso3 = c.get("id")
        if not iso3 or region == "Aggregates":
            continue
        countries.append({"iso3": iso3, "country": (c.get("name") or "").strip(),
                          "region": region or "NA",
                          "income": ((c.get("incomeLevel") or {}).get("value") or "NA")})
    countries.sort(key=lambda r: r["iso3"])
    keep = {r["iso3"] for r in countries}
    cpath = os.path.join(a.out, "countries.csv")
    with open(cpath, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["iso3", "country", "region", "income"])
        w.writeheader(); w.writerows(countries)
    manifest["countries"] = {"n": len(countries), "sha256": sha256(open(cpath, "rb").read())}
    print(f"countries (aggregates excluded): {len(countries)}")

    results = {}
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(fetch_one, code, a.date): code for code in INDICATORS}
        for fut in as_completed(futs):
            code, info = fut.result()
            results[code] = info
            print(f"  fetched {code} rows={len(info['rows'])} pages={info['pages']}")

    out_rows = []
    for code, role in INDICATORS.items():
        info = results[code]
        n_raw, n_ok = len(info["rows"]), 0
        for r in info["rows"]:
            iso3 = r.get("countryiso3code"); v = r.get("value")
            if iso3 not in keep or v is None:
                continue
            out_rows.append([iso3, r["country"]["value"].strip(), r["date"], code, float(v)])
            n_ok += 1
        manifest["indicators"][code] = {
            "role": role,
            "name": info["rows"][0]["indicator"]["value"] if info["rows"] else "",
            "url": info["url"], "pages": info["pages"],
            "n_raw_rows": n_raw, "n_nonnull_country_rows": n_ok, "sha256_raw": info["sha256_raw"],
        }

    out_rows.sort(key=lambda r: (r[3], r[0], r[2]))
    lpath = os.path.join(a.out, "wdi_long.csv")
    with open(lpath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["iso3", "country", "year", "indicator", "value"])
        w.writerows(out_rows)
    manifest["panel"] = {
        "file": lpath, "rows": len(out_rows),
        "countries_with_any_data": len({r[0] for r in out_rows}),
        "years": [min(int(r[2]) for r in out_rows), max(int(r[2]) for r in out_rows)],
        "sha256": sha256(open(lpath, "rb").read()),
    }
    with open(os.path.join(a.out, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print(f"wrote {lpath} ({len(out_rows)} rows)")
    for code, m in manifest["indicators"].items():
        print(f"  {code:22s} {m['role']:18s} used={m['n_nonnull_country_rows']:6d}")


if __name__ == "__main__":
    main()
