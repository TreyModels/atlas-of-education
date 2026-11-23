#!/usr/bin/env python3
"""Pull the World Bank WDI series needed to rebuild Boppart et al.'s agricultural-input object.

Boppart's data are not in the NBER data appendix (only the appendix PDF is there), so the minimum
series are rebuilt from the World Bank (reachable from box2) and the Penn World Table.  Every
departure from the paper's data is listed in the record's README.

Output: /root/work/subsistence/data/wdi_long.csv  (iso3, country, year, indicator, value)
"""
import urllib.request, json, csv, time, os

BASE = "https://api.worldbank.org/v2/country/all/indicator/"
IND = {
    "ag_emp_share": "SL.AGR.EMPL.ZS",          # employment in agriculture, % of total employment
    "ag_va_cd": "NV.AGR.TOTL.CD",              # agriculture value added, current US$
    "ag_va_kd": "NV.AGR.TOTL.KD",              # agriculture value added, constant 2015 US$
    "ag_va_share": "NV.AGR.TOTL.ZS",           # agriculture value added, % of GDP
    "gdp_pc_kd": "NY.GDP.PCAP.KD",             # GDP per capita, constant 2015 US$
    "gdp_cd": "NY.GDP.MKTP.CD",
    "gcf_share": "NE.GDI.TOTL.ZS",             # gross capital formation, % of GDP
    "gcf_cd": "NE.GDI.TOTL.CD",
    "arable_ha": "AG.LND.ARBL.HA",             # arable land, hectares
    "tractors_per_land": "AG.LND.TRAC.ZS",     # tractors per 100 sq km of arable land
    "fert_kg_per_ha": "AG.CON.FERT.ZS",        # fertiliser consumption, kg per hectare of arable land
    "labour_force": "SL.TLF.TOTL.IN",
    "pop": "SP.POP.TOTL",
    "sec_completion": "SE.SEC.CMPT.ZS",        # lower secondary completion, % of relevant age group
    "prm_completion": "SE.PRM.CMPT.ZS",
    "tfr": "SP.DYN.TFRT.IN",                   # fertility, births per woman
    "urban_pct": "SP.URB.TOTL.IN.ZS",
    "cereal_yield": "AG.YLD.CREL.KG",
    "ind_va_share": "NV.IND.TOTL.ZS",
}
YEAR = "1960:2024"
OUT = "/root/work/subsistence/data"


def get(u, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (research)"})
            return json.load(urllib.request.urlopen(req, timeout=90))
        except Exception as e:
            print("retry", k, u[:100], e, flush=True)
            time.sleep(2 + 2 * k)
    raise RuntimeError("failed " + u)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, code in IND.items():
        page = 1
        while True:
            d = get(f"{BASE}{code}?format=json&per_page=20000&date={YEAR}&page={page}")
            if not isinstance(d, list) or len(d) < 2 or not isinstance(d[0], dict) or "pages" not in d[0]:
                print(f"  {name} ({code}) page {page}: no data / API message: {str(d)[:300]}", flush=True)
                break
            meta, data = d[0], d[1] or []
            for r in data:
                if r.get("value") is None:
                    continue
                rows.append([r.get("countryiso3code") or "", r.get("country", {}).get("value", ""),
                             int(r["date"]), name, r["value"]])
            if page >= int(meta.get("pages", 1)):
                break
            page += 1
        print(f"{name} ({code}): total rows so far {len(rows)}", flush=True)
    with open(f"{OUT}/wdi_long.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["iso3", "country", "year", "indicator", "value"]); w.writerows(rows)
    print("wrote", f"{OUT}/wdi_long.csv", len(rows), "rows")
