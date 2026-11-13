"""Cambodia pack v0.2. Enrolment anchored to UIS completion up to 2015 (anchored=True); everything else is mechanism.
Originally: Cambodia pack v0.1: UNCALIBRATED. Values are coded from the historical record (sources in comments) or assumed.
Purpose: show the ledger and struts on a real country, not to claim a fit. Calibration (fit 2000-15, test 2016+) is next."""
import eduengine as ee

def modules():
    return [ee.PublicSchools(), ee.PrivateSchools(), ee.TutoringMarket(), ee.FiscalState(), ee.QueueLabour()]

PARAMS = dict(
    start_year=1980, T=50, N=1000, measure_from=15,
    y_median=0.55, y_sigma=0.8, urban_share=0.2, subsist=0.40, borrow=0.15, q0=0.85,
    paths=dict(
        y_median=[(1980, .55), (1995, .65), (2005, .85), (2019, 1.4), (2029, 1.7)],     # assumed: rising household income (GDP pc ~7%/yr 1998-2019)
        urban_share=[(1980, .15), (2000, .19), (2020, .25), (2029, .28)],              # approx. World Bank urban share
        budget_per_child=[(1980, .006), (1995, .010), (2005, .018), (2015, .025), (2024, .035)],   # assumed; education ~2% of GDP (UIS 2023)
        pay_ratio=[(1980, .40), (2013, .45), (2018, .80), (2029, .85)],               # coded: large salary rises 2014-2018
        vac0=[(1980, .04), (2000, .06), (2020, .12), (2029, .14)],                    # assumed: small formal sector (~77% informal)
    ),
    events=[
        dict(year=2001, set=dict(fee_public=0.0), label='Formal primary/secondary fees abolished (Priority Action Programme)'),
        dict(year=2007, set=dict(cct=0.04), label='Scholarships for poor lower-secondary pupils (CESSP)'),
        dict(year=2014, set=dict(gates=[dict(kind='bar', bar=2.0), dict(kind='bar', bar=4.0), dict(kind='bar', bar=8.5),
                                       dict(kind='bar', bar=10.0)]), label='Bac II anti-cheating reform: pass rate collapses'),
        dict(year=2016, set=dict(gates=[dict(kind='bar', bar=2.0), dict(kind='bar', bar=4.0), dict(kind='bar', bar=7.0),
                                       dict(kind='bar', bar=10.0)]), label='Bac II pass rates recover'),
    ],
    fee_public=0.03, monitoring=0.2, h_max=0.4, fee_tertiary=0.30,
    gates=[dict(kind='bar', bar=2.0), dict(kind='bar', bar=4.0), dict(kind='bar', bar=5.5), dict(kind='bar', bar=10.0)],
    fiscal_budget=False, cct=0.0,
    promote_bar=0.5, gate_retakes=1,          # coded: high repetition in the 1990s-2000s; Bac II can be resat
    need_mode='luxury', poverty_line=1.0, need_max=1.0,
    vac_growth=0.0, rank_routine=False, kin_support=0.75,
)

def make(anchored=True, anchor_until=2015, **over):
    from countries._common import targets
    prm = dict(PARAMS)
    if anchored:
        prm['enrol_targets'] = targets('cambodia', anchor_until)
    prm.update(over)
    return ee.build(modules(), **prm)
