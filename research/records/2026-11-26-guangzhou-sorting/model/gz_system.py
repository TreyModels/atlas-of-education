#!/usr/bin/env python3
"""Guangzhou sorting-system model. ILLUSTRATIVE: synthetic pupils, parameters are assumptions
(dossier numbers where marked [D]); nothing is calibrated to Guangzhou microdata.

Life course of one cohort:
  aptitude + family wealth + zone school + hukou status
  -> pre-gate years (tutoring legal or banned)          -> ZHONGKAO score
  -> gate: academic track (share ACAD) / vocational; elite boarding tier = top ELITE share
     non-hukou pupils capped at QUOTA of public academic seats [D 8-18%]; others go private (pay) or vocational
  -> high school: boarders get the school's hours, only the weekend window for tutoring;
     day pupils can buy evenings. Within-school banding: top classes get CLASS_EFF [D 0.44 SD]
  -> GAOKAO score -> top 10% of cohort = 'elite university'
Regimes compare the pre-2021 open market with the current system (ban before gate + boarding after).
"""
import numpy as np

BASE = dict(
    n=200_000, seed=0,
    APT_WEALTH=0.30,       # correlation of aptitude with log wealth (assumption)
    ZONE_G=0.15,           # zone (residence-assigned) junior school effect per SD of neighbourhood wealth, in score SD
    SEG=0.6,               # residential segregation by wealth
    NONHUKOU=0.10,         # share of cohort without local hukou (assumption)
    QUOTA=0.15,            # max share of public academic seats for non-hukou [D 8-15% core / 8-18% outer]
    ACAD=0.65,             # academic-track share at zhongkao (user: 60-70%)
    ELITE=0.10,            # top tier (elite boarding schools)
    CLASS_EFF=0.44,        # top-band class effect, SD [D]
    SCHOOL_EFF=0.10,       # school value-added per tier, SD [D 0-0.2]
    TUT_EFF=0.05,          # gaokao SD gain per sqrt(weekly hour) of tutoring (small; evidence mixed)
    EARLY_EFF=0.05,        # zhongkao SD gain per sqrt(weekly hour) pre-gate tutoring
    PRICE=400,             # yuan per hour [D 400-600]
    WEEKS=40,
    BAN_PRE=False,         # tutoring banned before the gate (2021 double reduction)
    ENFORCE=0.8,           # share of would-be pre-gate tutoring removed by the ban
    BOARDING=False,        # academic high schools board (Sun night - Fri)
    WEEKEND_HRS=4,         # hours a boarder can buy (one day a week)
    WEEKEND_TAKEUP=0.02,   # share of boarders who buy any weekend tutoring (teacher observation: none seen in a year)
    LEGAL_PRE_SHARE=1.0,   # share of pre-gate tutoring years when it was legal (cohort born ~2010: grades 1-4 of 9 = 0.45)
    MINBAN_PEN=0.20,       # zhongkao SD penalty for non-hukou pupils schooled in minban/purchased places (assumption)
    EVENING_HRS=12,        # hours a day pupil can buy
    PUBLIC_COST=13_000,    # public boarding high school, yuan/year all-in [D 1.2-1.4 wan]
    PRIVATE_COST=75_000,   # private ordinary class, yuan/year [D 6-12 wan]
    MED_INCOME=200_000,    # three-person household income [D approx]
)


def gini(x):
    x = np.sort(np.asarray(x, float)); n = x.size
    return float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum())) if x.sum() > 0 else 0.0


def conc_index(y, rank_var):
    """Concentration index of outcome y over the ranking of rank_var (Gini-type, -1..1; 0 = no wealth gradient)."""
    r = (np.argsort(np.argsort(rank_var)) + 0.5) / y.size
    return float(2 * np.cov(y, r, bias=True)[0, 1] / y.mean())


def run(**kw):
    p = {**BASE, **kw}; rng = np.random.default_rng(p['seed']); n = p['n']
    zone = rng.normal(size=n)
    logw = p['SEG'] * zone + np.sqrt(1 - p['SEG'] ** 2) * rng.normal(size=n)
    apt = p['APT_WEALTH'] * logw + np.sqrt(1 - p['APT_WEALTH'] ** 2) * rng.normal(size=n)
    income = p['MED_INCOME'] * np.exp(0.7 * logw)
    hukou = rng.random(n) >= p['NONHUKOU']
    wq = np.searchsorted(np.quantile(logw, [.2, .4, .6, .8]), logw)
    aq = np.searchsorted(np.quantile(apt, [.2, .4, .6, .8]), apt)

    # pre-gate tutoring: richer families buy more; ban removes ENFORCE of it
    want_pre = np.clip(2 + 3 * logw + rng.normal(0, 1, n), 0, 10)
    afford_pre = 0.10 * income / (p['PRICE'] * p['WEEKS'])
    pre = np.minimum(want_pre, afford_pre)
    if p['BAN_PRE']:
        pre = pre * (p['LEGAL_PRE_SHARE'] + (1 - p['LEGAL_PRE_SHARE']) * (1 - p['ENFORCE']))
    zk = apt - p['MINBAN_PEN'] * (~hukou) + p['ZONE_G'] * zone + p['EARLY_EFF'] * np.sqrt(pre) + 0.4 * rng.normal(size=n)

    # gate: rank by zhongkao; non-hukou capped in public academic seats
    seats = int(p['ACAD'] * n); order = np.argsort(-zk)
    public = np.zeros(n, bool); cap = int(p['QUOTA'] * seats); nh_taken = 0; filled = 0
    for i in order:
        if filled >= seats: break
        if not hukou[i]:
            if nh_taken >= cap: continue
            nh_taken += 1
        public[i] = True; filled += 1
    # non-hukou above the academic line but over quota: private if affordable (cost < 40% income), else vocational
    line = np.sort(zk)[::-1][seats - 1]
    shut_out = (~hukou) & (~public) & (zk >= line)
    private = shut_out & (p['PRIVATE_COST'] < 0.4 * income)
    academic = public | private
    # tiers among public academic: elite = top ELITE share of cohort by zhongkao among public
    pub_rank = np.full(n, np.nan); idx = np.flatnonzero(public)
    pub_rank[idx] = (np.argsort(np.argsort(-zk[idx])) + 0.5) / idx.size
    elite_school = public & (pub_rank <= p['ELITE'] / p['ACAD'])
    tier = np.where(elite_school, 2, np.where(public, 1, np.where(private, 1, 0)))
    # within-school banding: top 2 of ~16 classes per school -> top 1/8 within tier by zhongkao
    top_band = np.zeros(n, bool)
    for t in (1, 2):
        m = np.flatnonzero((tier == t) & public)
        if m.size: top_band[m[zk[m] >= np.quantile(zk[m], 7 / 8)]] = True
    experience = tier * p['SCHOOL_EFF'] + top_band * p['CLASS_EFF']
    top10_exp = academic & (experience >= np.quantile(experience[academic], 0.90))

    # post-gate tutoring
    window = np.where(p['BOARDING'] & academic, p['WEEKEND_HRS'], p['EVENING_HRS'])
    want_post = np.clip(3 + 3 * logw - 1.5 * apt + rng.normal(0, 1, n), 0, None)  # weaker pupils want more (compensatory)
    afford_post = 0.10 * income / (p['PRICE'] * p['WEEKS'])
    T = np.where(academic, np.minimum.reduce([want_post, window, afford_post]), 0.0)
    if p['BOARDING']:
        buys = rng.random(n) < p['WEEKEND_TAKEUP']
        T = np.where(academic & ~buys, 0.0, T)
    T[T < 1] = 0.0

    gk = apt + experience + p['TUT_EFF'] * np.sqrt(T) + 0.4 * rng.normal(size=n)
    gk[~academic] = -np.inf
    elite_uni = gk >= np.sort(gk)[::-1][int(0.10 * n) - 1]

    spend = np.where(public, p['PUBLIC_COST'], 0) + np.where(private, p['PRIVATE_COST'], 0) \
        + (T + 0 * pre) * p['PRICE'] * p['WEEKS']
    hi = aq == 4  # top-fifth aptitude
    bins = np.searchsorted(np.quantile(apt[hi_all := (aq == 4)], np.linspace(0, 1, 11)[1:-1]), apt)
    def eq_apt_ratio(out):
        r5 = []; r1 = []
        for b in range(10):
            m = hi_all & (bins == b) & hukou
            r5.append(out[m & (wq >= 3)].mean()); r1.append(out[m & (wq <= 1)].mean())
        return float(np.nanmean(r5) / max(np.nanmean(r1), 1e-9))
    def rate(mask, out): return float(out[mask].mean()) if mask.any() else np.nan
    gain_pts = p['TUT_EFF'] * np.sqrt(T[T > 0]) if (T > 0).any() else np.array([0])
    return dict(
        topExp_hiApt_Q1=rate(hi & (wq == 0) & hukou, top10_exp), topExp_hiApt_Q5=rate(hi & (wq == 4) & hukou, top10_exp),
        uni_hiApt_Q1=rate(hi & (wq == 0) & hukou, elite_uni), uni_hiApt_Q5=rate(hi & (wq == 4) & hukou, elite_uni),
        uni_hiApt_nonhukou=rate(hi & ~hukou, elite_uni),
        EO_ratio=rate(hi & (wq == 4) & hukou, elite_uni) / max(rate(hi & (wq == 0) & hukou, elite_uni), 1e-9),
        conc_elite_uni=conc_index(elite_uni.astype(float), logw),
        gini_spend=gini(spend[academic]),
        tutor_share=float((T > 0)[academic].mean()), tutor_share_Q5=float((T > 0)[academic & (wq == 4)].mean()),
        cost_share_Q1_public=float((p['PUBLIC_COST'] / income)[public & (wq == 0)].mean()),
        sd_gain_per_10k=float((gain_pts.mean() / (T[T > 0].mean() * p['PRICE'] * p['WEEKS'] / 1e4)) if (T > 0).any() else 0),
        EO_equal_apt=eq_apt_ratio(elite_uni), EO_equal_apt_track=eq_apt_ratio(academic),
        vocational_hiApt_Q1=rate(hi & (wq == 0) & hukou, ~academic), vocational_hiApt_nonhukou=rate(hi & ~hukou, ~academic),
        nonhukou_shut_out=float(shut_out.sum() / max((~hukou & (zk >= line)).sum(), 1)),
        nonhukou_to_private=float(private.sum() / max(shut_out.sum(), 1)),
    )


COHORTS = {
    'Cohort ~2015 (open market, day schools)': dict(BAN_PRE=False, BOARDING=False),
    'Cohort ~2026 (ban from grade 5, boarding)': dict(BAN_PRE=True, BOARDING=True, LEGAL_PRE_SHARE=0.45),
    'Fully banned cohort (~2030)': dict(BAN_PRE=True, BOARDING=True, LEGAL_PRE_SHARE=0.0),
}
REGIMES = {
    'Pre-2021 open market, day schools': dict(BAN_PRE=False, BOARDING=False),
    'Ban before gate only':              dict(BAN_PRE=True,  BOARDING=False),
    'Boarding only':                     dict(BAN_PRE=False, BOARDING=True),
    'Current: ban + boarding':           dict(BAN_PRE=True,  BOARDING=True),
}

if __name__ == '__main__':
    import json, sys
    seeds = range(5); res = {}
    for name, r in REGIMES.items():
        rs = [run(**r, seed=s) for s in seeds]
        res[name] = {k: float(np.mean([x[k] for x in rs])) for k in rs[0]}
    json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else 'gz_results.json', 'w'), indent=1)
    keys = ['topExp_hiApt_Q1', 'topExp_hiApt_Q5', 'uni_hiApt_Q1', 'uni_hiApt_Q5', 'uni_hiApt_nonhukou', 'EO_ratio',
            'conc_elite_uni', 'gini_spend', 'tutor_share', 'tutor_share_Q5', 'sd_gain_per_10k']
    for k in keys:
        print(f'{k:22s}' + ''.join(f'{res[n][k]:10.3f}' for n in REGIMES))
    print('non-hukou above the academic line but shut out of public:', round(res['Current: ban + boarding']['nonhukou_shut_out'], 3),
          '| of those, can afford private:', round(res['Current: ban + boarding']['nonhukou_to_private'], 3))
    print('public boarding cost / income, poorest fifth:', round(res['Current: ban + boarding']['cost_share_Q1_public'], 3))
