"""EXP-4: Empirical TWFE check on ILO/UCW child-labor series (SL.TLF.0714.*)
across the 8 primary-verified SSA fee-abolition dates from E8.
"""
import argparse
import pandas as pd
import requests
import statsmodels.formula.api as smf

VERIFIED_DATES = {
    "MWI": 1994, "ETH": 1995, "UGA": 1997, "LSO": 2000,
    "TZA": 2001, "KEN": 2003, "MOZ": 2004, "GHA": 2005,
}
INDICATORS = {
    "cl_total": "SL.TLF.0714.ZS",
    "cl_work_only": "SL.TLF.0714.WK.ZS",
    "cl_study_work": "SL.TLF.0714.SW.ZS",
}

def main(out_csv):
    url_ssa = "https://api.worldbank.org/v2/country/region/SSF?format=json&per_page=100"
    ssa = [r["id"] for r in requests.get(url_ssa, timeout=30).json()[1]]

    frames = []
    for name, code in INDICATORS.items():
        url = f"https://api.worldbank.org/v2/country/{';'.join(ssa)}/indicator/{code}?format=json&per_page=5000&date=1990:2020"
        res = requests.get(url, timeout=30).json()
        if len(res) > 1 and res[1]:
            for r in res[1]:
                if r["value"] is not None:
                    frames.append({"iso3": r["countryiso3code"], "year": int(r["date"]), "ind": name, "val": float(r["value"])})

    df = pd.DataFrame(frames)
    out = []
    for name, g in df.groupby("ind"):
        g = g.copy()
        g["post"] = g.apply(lambda x: 1 if (x["iso3"] in VERIFIED_DATES and x["year"] >= VERIFIED_DATES[x["iso3"]]) else 0, axis=1)
        if g["post"].sum() < 3:
            out.append({"ind": name, "n": len(g), "treated_obs": int(g["post"].sum()), "att": None, "se": None, "note": "Too sparse"})
            continue
        m = smf.ols("val ~ post + C(iso3) + C(year)", data=g).fit(cov_type="cluster", cov_kwds={"groups": g["iso3"]})
        out.append({"ind": name, "n": len(g), "treated_obs": int(g["post"].sum()), "att": float(m.params["post"]), "se": float(m.bse["post"]), "p": float(m.pvalues["post"])})

    res = pd.DataFrame(out)
    res.to_csv(out_csv, index=False)
    print(res.to_string(index=False))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/exp4_fee_child_labor.csv")
    args = ap.parse_args()
    main(args.out)
