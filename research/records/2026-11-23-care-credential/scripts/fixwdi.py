import json, glob, os
RAW = "/root/work/care_cred/raw"
keys = {"tfr": "tfr", "flfp": "flfp", "edu_upsec_f": "edu_upsec_f", "edu_ter_f": "edu_ter_f",
        "gdp_pc": "gdp_pc", "urban": "urban"}
out = {}
for k in keys:
    f = f"{RAW}/wb_{k}.json"
    d = json.load(open(f))
    rows = d[1] if len(d) > 1 and d[1] else []
    out[k] = [(r["countryiso3code"], r["date"], r["value"]) for r in rows
              if r.get("countryiso3code") and r.get("value") is not None]
    print(k, len(out[k]))
json.dump(out, open(f"{RAW}/wdi.json", "w"))
print("wrote wdi.json")
