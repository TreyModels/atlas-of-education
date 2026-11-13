"""Philippines pack v0.2. Enrolment anchored to UIS completion up to 2015; tutoring, private schooling, learning and
labour outcomes come from the mechanism. Values coded from the record (comments) or assumed."""
import eduengine as ee
from countries._common import targets, modules

PARAMS = dict(
    start_year=1980, T=50, N=1000, measure_from=15,
    levels=[('primary', 6), ('lower', 4), ('upper', 2), ('tertiary', 4)],          # 6-4 basic cycle; Senior High (Grades 11-12) from 2016
    level_open=[None, None, [(1980, 0), (2015, 0), (2016, 1)], None],              # coded: RA 10533 (2013), first SHS intake 2016
    gates=[dict(kind='bar', bar=2.0), dict(kind='bar', bar=4.5), dict(kind='bar', bar=6.5), dict(kind='bar', bar=10.0)],
    y_sigma=0.85, urban_share=0.45, subsist=0.40, borrow=0.20, q0=0.85,
    paths=dict(
        y_median=[(1980, 1.0), (2000, 1.05), (2015, 1.45), (2029, 1.8)],          # assumed: richer than Cambodia, slower growth
        urban_share=[(1980, .37), (2010, .45), (2029, .50)],
        budget_per_child=[(1980, .03), (2000, .035), (2015, .05), (2029, .06)],   # assumed
        vac0=[(1980, .12), (2010, .16), (2029, .20)],
    ),
    pay_ratio=1.0, monitoring=0.5, h_max=0.4, fee_public=0.0, fee_tertiary=0.35,
    voucher=0.25,                                                                  # coded: ESC/voucher subsidies for private high school
    r0=0.03,                                                                       # coded: remedial demand (OFW parents absent, English-medium)
    events=[
        dict(year=2008, set=dict(cct=0.04), label='Pantawid Pamilya (4Ps) conditional cash transfers'),
        dict(year=2018, set=dict(fee_tertiary=0.15), label='Free tuition in state universities (RA 10931)'),
    ],
    fiscal_budget=False, cct=0.0, promote_bar=0.45, gate_retakes=0, rank_routine=False, kin_support=0.7, vac_growth=0.0,
)


def make(anchored=True, anchor_until=2015, **over):
    prm = dict(PARAMS)
    if anchored:
        prm['enrol_targets'] = targets('philippines', anchor_until)
    prm.update(over)
    return ee.build(modules(), **prm)
