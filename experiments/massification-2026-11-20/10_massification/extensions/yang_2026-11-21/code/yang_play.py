#!/usr/bin/env python3
"""EXPLORATORY — play with Yang et al. (2026) city-size/occupational-variety log law.

Source: Yang, Holehouse, Kempes, Youn, Arroyo, Redner & West, "Scaling laws for function
diversity and specialization across socioeconomic and biological complex systems", PNAS 2026
(doi:10.1073/pnas.2509729123; arXiv:2208.06487). City (MSA) relation: D = b*ln(N) + c,
fitted b = 128 occupations per ln(working population), R^2 = 0.94 (their Table 1).
Their worked example: urban population growth delta = 0.71%/yr in 2019 -> dD/dt = delta*b ~ 0.9
occupations/year.

This script is EXPLORATORY / DERIVED / SIMULATED. It does not estimate the law; it adopts the
published b and explores three implications relevant to the massification programme:
  (1) the level/elasticity schedule and the residual-speed identity dD/dt = delta*b;
  (2) aggregation over a city-size (Zipf) system as urbanisation rises;
  (3) a benchmark for credential growth: how fast can *occupation-driven* variety grow, versus the
      observed credential-count growth from the Domus E4 package (which the review flagged).
No observed city data are read; c is a declared anchor with sensitivity.
"""
import json
from pathlib import Path
import math

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(parents=True, exist_ok=True)

# ---- adopted from Yang et al. (2026) ----
B = 128.0            # occupations per ln(working population), MSA fit, R^2=0.94
DELTA = 0.0071       # US urban population growth, 0.71%/yr (their 2019 figure)
# declared anchor for c: D(N_ref) = D_ref. Sensitivity D_ref in {300, 500, 700} at N_ref=1e6.
N_REF = 1_000_000.0
D_REFS = [300.0, 500.0, 700.0]
C = {d: d - B * math.log(N_REF) for d in D_REFS}


def D(N, dref=500.0):
    return max(0.0, B * math.log(N) + C[dref])


def main():
    rows = []
    # (1) level/elasticity schedule
    for dref in D_REFS:
        for N in [1e4, 1e5, 1e6, 1e7, 1e8]:
            d = D(N, dref)
            # elasticity of diversity w.r.t. population: d ln D / d ln N = B / D
            elast = B / d if d > 0 else float("nan")
            rows.append(dict(exercise="E1_schedule", anchor_Dref=dref, N=N, D=round(d, 2),
                             rungs_per_1000=round(1000 * d / N, 4),
                             elasticity=round(elast, 5), label="DERIVED"))

    # (2) Zipf city system: urbanisation rises by moving people into cities
    # 200 cities, ranks 1..200, size = S / rank^alpha; rural baseline variety 20 occupations.
    alpha = 1.0
    n_cities = 200
    rural_D = 20.0
    total_people = 50_000_000.0
    weights = [1.0 / (r ** alpha) for r in range(1, n_cities + 1)]
    wsum = sum(weights)
    for urb in [0.2, 0.4, 0.6, 0.8, 1.0]:
        urban_people = urb * total_people
        rural_people = total_people - urban_people
        total_D = rural_D + sum(D(urban_people * w / wsum, 500.0) for w in weights)
        rows.append(dict(exercise="E2_zipf", anchor_Dref=500.0, urbanisation=urb,
                         urban_people=round(urban_people, 0),
                         total_D=round(total_D, 2),
                         D_per_million=round(total_D / (total_people / 1e6), 4),
                         urban_D_per_million=round(
                             (total_D - rural_D) / (urban_people / 1e6) if urban_people else float("nan"), 4),
                         label="SIMULATED"))

    # (3) credential-growth benchmark (Domus E4 numbers, adopted as given by the package)
    cred_2019, cred_2025 = 738_000.0, 1_850_000.0
    occ_1977, occ_2018 = 662.0, 867.0
    dlnN_6y = 6 * DELTA
    dD_6y = B * dlnN_6y
    rows.append(dict(exercise="E3_benchmark", anchor_Dref=500.0,
                     occupation_variety_growth_6y=round(dD_6y, 2),
                     occupation_growth_pct_of_2018=round(100 * dD_6y / occ_2018, 3),
                     credential_growth_6y=round(cred_2025 / cred_2019, 3),
                     credential_growth_pct=round(100 * (cred_2025 / cred_2019 - 1), 1),
                     ratio_credential_to_occupation_growth=round(
                         (cred_2025 / cred_2019 - 1) / (dD_6y / occ_2018), 1),
                     label="DERIVED"))

    # (4) gate-pressure implication: one credential rung per occupation type;
    # graduates per rung if graduate share of population is fixed at 10%.
    for N in [1e5, 1e6, 1e7]:
        d = D(N, 500.0)
        grads = 0.10 * N
        rows.append(dict(exercise="E4_gate_pressure", anchor_Dref=500.0, N=N, D=round(d, 2),
                         rungs_per_1000=round(1000 * d / N, 3),
                         grads_per_rung=round(grads / d, 1) if d else float("nan"),
                         label="SIMULATED"))

    # write
    import csv
    keys = sorted({k for r in rows for k in r})
    with open(OUT / "yang_play.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    summary = dict(
        source="Yang et al. 2026 PNAS doi:10.1073/pnas.2509729123 (arXiv:2208.06487)",
        adopted=dict(b=B, delta=DELTA, N_ref=N_REF, D_refs=D_REFS,
                     note="b and delta adopted verbatim from the paper; c is a DECLARED anchor "
                          "(D(N_ref)=D_ref) with sensitivity; no city data read."),
        residual_speed=dict(formula="dD/dt = delta*b", value=round(DELTA * B, 4),
                            unit="occupations/year"),
        six_year_variety_growth=round(B * 6 * DELTA, 3),
        six_year_variety_growth_pct_of_867=round(100 * B * 6 * DELTA / occ_2018, 4),
        credential_growth_over_same_window=round(cred_2025 / cred_2019, 4),
        interpretation="At the paper's own urban growth rate, occupation-driven variety grows by "
                       "single digits of occupations in six years; the observed credential-count "
                       "increase is two orders of magnitude larger, so credentials are not "
                       "occupational categories (consistent with the Domus E4 two-law correction, "
                       "pending the reviewer's retraction of 1.88/5.04/181%).",
        limits=["EXPLORATORY: adopts b from the paper, does not re-estimate it.",
                "c is a declared anchor with sensitivity over D_ref in {300,500,700}.",
                "Zipf and rural-variety parameters are DECLARED for illustration only.",
                "No observed city-size or occupational data are read; no claim about any country.",
                "The credential-growth comparison uses the Domus package's numbers as given; "
                "the reviewer has flagged those numbers as partly invalid."])
    (OUT / "yang_play_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("\nfirst rows:")
    for r in rows[:6]:
        print(r)


if __name__ == "__main__":
    main()
