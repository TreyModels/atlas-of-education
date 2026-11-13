"""Derive two inputs from sourced data (review items 1.1 and 1.3). Writes results/derived_inputs.json.

1.3  lam_g from graduate pay. Observed ratio r_y = 12 * MyCOS starting pay(y) / NBS urban non-private wage(y)
     (2015-2023; sources in inputs/other_sources.json items A1 and A3, data_china.STARTING_WAGE_BA / URBAN_WAGE).
     Assumption: the model's graduate wage closes a fraction lam of its gap to target each month, and the observed
     decline of r after 2015 is one such adjustment. Then the time for r to cover half of its 2015-23 decline is the
     half-life H (months), and lam = 1 - 2**(-1/H). The series alone does not identify a target, so this is an order
     of magnitude, not a regression estimate. Sensitivity: origin 2016 instead of 2015; and a one-year half-life.

1.1  Demand-shock size for the Aug-2021 step. dr = sum over sectors of (share of graduate-accessible jobs in the
     sector) x (fractional job loss in the sector). Job-loss fractions come from sources:
       - real-estate DEVELOPMENT employment fell 27.0% 2018->2023 (NBS 5th census; inputs item B1). Total real-estate
         employment ROSE 14.0% over the same years, so the -27% is a segment, not the sector.
       - tutoring: about 3m jobs lost within 4 months of July 2021 (Huang et al. 2025, item B2) against about 11m
         pre-policy employees (secondary, item B2_corroborating): 3/11 = 0.27.
     The graduate-accessible shares are NOT sourced. They are scenario assumptions (low/central/high below).
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results'); os.makedirs(RES, exist_ok=True)

# MyCOS bachelor's starting pay, six months after graduation, yuan a month, by graduating class.
START_PAY = {2015: 4042, 2016: 4376, 2017: 4774, 2018: 5135, 2019: 5440, 2020: round(5833 / 1.066), 2021: 5833,
             2022: 5990, 2023: 6050}
# NBS average annual wage, urban non-private units, yuan a year.
URBAN = {2015: 62029, 2016: 67569, 2017: 74318, 2018: 82461, 2019: 90501, 2020: 97379, 2021: 106837, 2022: 114029,
         2023: 120698}


def ratio(y):
    return 12 * START_PAY[y] / URBAN[y]


def half_life_years(origin, end=2023):
    r0, r1 = ratio(origin), ratio(end)
    target = r0 - 0.5 * (r0 - r1)
    for y in range(origin, end):
        a, b = ratio(y), ratio(y + 1)
        if a >= target >= b:
            return (y + (a - target) / (a - b)) - origin
    return None


def lam_from_half_life_months(h):
    return 1 - 2 ** (-1 / h)


def main():
    out = {'ratio': {y: round(ratio(y), 4) for y in START_PAY}}
    h15 = half_life_years(2015); h16 = half_life_years(2016)
    out['half_life_years_origin_2015'] = h15
    out['half_life_years_origin_2016'] = h16
    lam_c = lam_from_half_life_months(12 * h15)
    lam_alt = lam_from_half_life_months(12 * h16)
    lam_fast = lam_from_half_life_months(12.0)
    out['lam_g'] = dict(
        data_central=lam_c, data_origin2016=lam_alt, data_fast_12m_halflife=lam_fast, review_value=0.0025,
        implied_half_life_months_review=math.log(0.5) / math.log(1 - 0.0025),
        formula='lam = 1 - 2**(-1/H), H = months for the relative pay ratio to close half of its 2015-2023 decline',
    )
    # 1.1 step mapping
    re_loss, tut_loss = 0.27, 3 / 11
    scen = {'low': (0.05, 0.025), 'central': (0.10, 0.05), 'high': (0.15, 0.10)}
    out['dr_step'] = {k: dict(share_real_estate=a, share_tutoring=b,
                              dr=round(a * re_loss + b * tut_loss, 4)) for k, (a, b) in scen.items()}
    out['dr_step']['inputs'] = dict(real_estate_development_loss=re_loss, tutoring_loss_share=round(tut_loss, 4),
                                    note='graduate-accessible shares are assumptions, not sourced')
    path = os.path.join(RES, 'derived_inputs.json')
    json.dump(out, open(path, 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
