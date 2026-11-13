"""Toy worlds: abstractions, not countries. Each is a module list plus parameters. Edit freely; nothing is calibrated."""
import eduengine as ee

BASE = dict(subsist=0.40, borrow=0.20, fee_tertiary=0.35, vac0=0.20, vac_growth=0.010)


def modules(labour='queue', private=True, tutoring=True, fiscal=False):
    m = [ee.PublicSchools()]
    if private: m.append(ee.PrivateSchools())
    if tutoring: m.append(ee.TutoringMarket())
    if fiscal: m.append(ee.FiscalState())
    m.append(ee.QueueLabour() if labour == 'queue' else ee.CompetitiveLabour())
    return m


WORLDS = {
    # T1: underpaid, unmonitored teachers in a poor state with few formal jobs (Cambodia-like abstraction)
    'low_pay': dict(mods=dict(), params=dict(BASE, pay_ratio=0.55, monitoring=0.2, budget_per_child=0.025, h_max=0.4,
                                              vac0=0.10, vac_growth=0.006, urban_share=0.25, y_sigma=0.8, priv_quality=1.0)),
    # T2: a capable state with selection exams after Grades 9 and 12 and scarce graduate jobs (East-Asia-like)
    'exam_race': dict(mods=dict(), params=dict(BASE, pay_ratio=1.2, monitoring=0.9, budget_per_child=0.12,
                                                urban_share=0.7, y_median=1.6, vac0=0.25, vac_growth=0.008,
                                                gates=[dict(kind='bar', bar=3.0), dict(kind='quota', share=0.55, cut0=7.0),
                                                       dict(kind='quota', share=0.45, cut0=10.0), dict(kind='bar', bar=11.5)])),
    # T3: a budget below demand; low-cost private schools enter (Kenya-like abstraction)
    'excess_demand': dict(mods=dict(), params=dict(BASE, budget_per_child=0.045, ptr_max=55.0, pay_ratio=0.9,
                                                    priv_wage=0.8, priv_quality=1.05, urban_share=0.35)),
    # T4: the push-pull loop; the budget is a share of taxes on a small formal sector
    'formal_loop': dict(mods=dict(fiscal=True), params=dict(BASE, vac0=0.08, vac_growth=0.0, tax_formal=0.15,
                                                             edu_share=0.18, urban_share=0.3)),
}


def make(world, mods=None, **over):
    w = WORLDS[world]
    m = dict(w['mods']); m.update(mods or {})
    prm = dict(w['params']); prm.update(over)
    return ee.build(modules(**m), **prm)


def run(world, mods=None, seeds=(0, 1), **over):
    """Average the summary over seeds (lists element-wise)."""
    import numpy as np
    outs = [make(world, mods, seed=s, **over).run() for s in seeds]
    res = {}
    for k in outs[0]:
        v = [o[k] for o in outs]
        if isinstance(v[0], dict):
            res[k] = {kk: float(np.mean([x[kk] for x in v])) for kk in v[0]}
        elif isinstance(v[0], (list, tuple)):
            res[k] = list(np.nanmean(np.array(v, float), 0))
        else:
            res[k] = float(np.nanmean(v))
    return res
