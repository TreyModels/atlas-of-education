"""Download Barro-Lee (via World Bank EdStats mirror) and demographic targets. Run on a machine with internet."""
import json, urllib.request, sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
os.makedirs(OUT, exist_ok=True)
FIT = "PHL THA CHN IDN VNM IND BGD EGY".split()
HOLD = "KOR MYS KEN BRA TUR MEX".split()
CS = ";".join(FIT + HOLD)
AGES = ["1519","2024","2529","3034","3539","4044","4549","5054","5559","6064","6569","7074","7599"]
def get(ind, src=None):
    url = f"https://api.worldbank.org/v2/country/{CS}/indicator/{ind}?format=json&per_page=20000&date=1950:2024"
    for _ in range(3):
        try:
            d = json.load(urllib.request.urlopen(url, timeout=60))
            if len(d) > 1 and d[1]: return [[r["countryiso3code"], int(r["date"]), r["value"]] for r in d[1] if r["value"] is not None]
            return []
        except Exception as e: err = e
    print("fail", ind, err); return []
res = {}
for sx in ["FE", "MA"]:
    for a in AGES:
        for k in ["NOED.%s.ZS", "PRM.ICMP.%s.ZS", "PRM.CMPT.%s.ZS", "SEC.ICMP.%s.ZS", "SEC.CMPT.%s.ZS", "TER.ICMP.%s.ZS", "TER.CMPT.%s.ZS", "POP.%s", "SCHL.%s"]:
            kk = k % a
            if kk.endswith(".ZS"): ind = f"BAR.{kk[:-3]}.{sx}.ZS"
            else: ind = f"BAR.{kk}.{sx}"
            res[ind] = get(ind)
for ind in ["SP.DYN.SMAM.FE", "SP.DYN.SMAM.MA", "SP.ADO.TFRT", "SP.DYN.TFRT.IN", "SP.POP.TOTL", "SP.URB.TOTL.IN.ZS", "NY.GDP.PCAP.KD", "SL.TLF.CACT.FE.ZS", "SP.POP.1519.FE","SP.POP.1519.MA","SP.POP.2024.FE","SP.POP.2024.MA","SP.POP.2529.FE","SP.POP.2529.MA","SP.POP.3034.FE","SP.POP.3034.MA","SP.POP.3539.FE","SP.POP.3539.MA","SP.POP.4044.FE","SP.POP.4044.MA","SP.POP.4549.FE","SP.POP.4549.MA"]:
    res[ind] = get(ind)
json.dump({"FIT": FIT, "HOLD": HOLD, "data": res}, open(f"{OUT}/wb_fetch.json", "w"))
print({k: len(v) for k, v in list(res.items())[:5]}, sum(1 for v in res.values() if not v), "empty of", len(res))
