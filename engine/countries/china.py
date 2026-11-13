"""China pack v0.2. Enrolment anchored to UIS completion up to 2015 (UIS series start in 2010; earlier years extrapolate flat,
a known weakness). The zhongkao is a tracking exam (failers go vocational), the gaokao a quota exam for academic-track
pupils. Tutoring, private schooling and graduate queuing come from the mechanism. Coded from the record or assumed."""
import eduengine as ee
from countries._common import targets, modules


def _gates(zk, gk):
    return [dict(kind='bar', bar=1.5),
            dict(kind='quota', share=zk, cut0=7.0, fail='track'),                       # zhongkao: academic places, rest vocational
            dict(kind='bar', bar=6.0, admit=dict(share=gk, cut0=11.0, academic_only=True)),  # graduation; gaokao rations tertiary places
            dict(kind='bar', bar=11.0)]


PARAMS = dict(
    start_year=1980, T=50, N=1000, measure_from=15,
    gates=_gates(0.35, 0.04),
    y_sigma=0.7, urban_share=0.2, subsist=0.35, borrow=0.25, q0=1.0,
    paths=dict(
        y_median=[(1980, .5), (2000, 1.0), (2010, 1.9), (2020, 3.0), (2029, 3.6)],    # assumed: rapid income growth
        urban_share=[(1980, .19), (2000, .36), (2010, .50), (2020, .64), (2029, .70)],  # approx. NBS urbanisation
        budget_per_child=[(1980, .03), (2000, .06), (2012, .12), (2029, .15)],          # coded: 4% of GDP target met 2012
        vac0=[(1980, .10), (2000, .18), (2015, .30), (2029, .32)],
        queue_on=[(1980, 0), (2008, 0), (2009, 1)],                                     # graduates queue once degrees are common
    ),
    pay_ratio=1.0, monitoring=0.6, h_max=0.4, fee_public=0.02, fee_tertiary=0.30,
    events=[
        dict(year=1999, set=dict(gates=_gates(0.45, 0.10)), label='Higher-education expansion begins (kuozhao)'),
        dict(year=2006, set=dict(fee_public=0.0, gates=_gates(0.50, 0.22)), label='Free compulsory education (rural 2006, urban 2008)'),
        dict(year=2012, set=dict(gates=_gates(0.55, 0.35)), label='Expansion continues'),
        dict(year=2015, set=dict(own_ban=0.5), label='Ban on teachers tutoring their own pupils (weakly enforced)'),
        dict(year=2019, set=dict(gates=_gates(0.55, 0.45)), label='Higher-vocational enrolment expansion'),
        dict(year=2021, set=dict(firm_ban=0.88, own_ban=0.9), label='Double Reduction: for-profit tutoring in core subjects banned'),
    ],
    fiscal_budget=False, cct=0.0, promote_bar=0.0, rank_routine=False, queue_support=1.5, kin_support=0.8,
    skilled_share=0.35, vac_growth=0.0,                 # vacancies follow the coded path (no extra compounding)
)


def make(anchored=True, anchor_until=2015, **over):
    prm = dict(PARAMS)
    if anchored:
        prm['enrol_targets'] = targets('china', anchor_until)
    prm.update(over)
    return ee.build(modules(), **prm)
