#!/usr/bin/env python3
"""Talent vs skill version. ILLUSTRATIVE; all parameters assumed and swept.
talent (what the child brings) -> skill at 15 = talent + zone teacher quality + home inputs (+ legal tutoring)
zhongkao measures skill -> academic track (ACAD) / vocational; school tier by score; class band by score
senior 1: skill grows with talent and class; zone advantage fades by DECAY
senior 2: RE-BANDING on current skill (if REBAND) -> senior 2-3 class effect -> gaokao measures skill at 18
Fairness is judged at equal TALENT, by family wealth."""
import numpy as np

P = dict(n=200_000, seed=0, TAL_WEALTH=0.10, SEG=0.6,
         ZONE_TEACH=0.25,   # SD of skill at 15 per SD of zone-school quality (teacher quality); zone quality tracks neighbourhood wealth
         HOME=0.15,         # SD of skill at 15 per SD of log wealth (home inputs)
         PRE_TUT=0.0,       # SD per SD of wealth from legal pre-gate tutoring (2015 cohort > 0; 2026 cohort ~0)
         ACAD=0.65, CLASS_EFF=0.44, SCHOOL_EFF=0.10, TOP_BAND=1 / 8,
         GROW=0.5,          # senior-high learning that scales with talent
         DECAY=0.5,         # share of pre-gate zone/home advantage that fades by senior 2
         REBAND=True, POST_TUT=0.0, NOISE=0.35)


def run(**kw):
    p = {**P, **kw}; rng = np.random.default_rng(p['seed']); n = p['n']
    zone = rng.normal(size=n)
    logw = p['SEG'] * zone + np.sqrt(1 - p['SEG'] ** 2) * rng.normal(size=n)
    tal = p['TAL_WEALTH'] * logw + np.sqrt(1 - p['TAL_WEALTH'] ** 2) * rng.normal(size=n)
    head = p['ZONE_TEACH'] * zone + p['HOME'] * logw + p['PRE_TUT'] * logw      # what wealth/zone buys before 15
    skill15 = tal + head
    zk = skill15 + p['NOISE'] * rng.normal(size=n)
    acad = zk >= np.quantile(zk, 1 - p['ACAD'])
    # tier: top 10% of cohort elite school, rest of academic regular
    elite = zk >= np.quantile(zk, 0.90)
    def bands(score, mask):
        b = np.zeros(n, bool)
        for t in (True, False):
            m = mask & (elite == t)
            if m.any(): b[m] = score[m] >= np.quantile(score[m], 1 - p['TOP_BAND'])
        return b
    band1 = bands(zk, acad)
    school = np.where(elite, 2, 1) * p['SCHOOL_EFF']
    skill16 = tal + (1 - p['DECAY']) * head + p['GROW'] * tal + school + band1 * p['CLASS_EFF'] + p['POST_TUT'] * logw
    obs16 = skill16 + p['NOISE'] * rng.normal(size=n)
    band2 = bands(obs16, acad) if p['REBAND'] else band1
    skill18 = skill16 + band2 * p['CLASS_EFF']
    gk = np.where(acad, skill18 + p['NOISE'] * rng.normal(size=n), -np.inf)
    uni = gk >= np.sort(gk)[::-1][int(.10 * n) - 1]

    # fairness at equal talent: top-fifth talent split into 10 bins; richer two-fifths vs poorer two-fifths
    wq = np.searchsorted(np.quantile(logw, [.2, .4, .6, .8]), logw)
    hi = tal >= np.quantile(tal, .8)
    bins = np.searchsorted(np.quantile(tal[hi], np.linspace(0, 1, 11)[1:-1]), tal)
    def eq(out):
        r = [(out[hi & (bins == b) & (wq >= 3)].mean(), out[hi & (bins == b) & (wq <= 1)].mean()) for b in range(10)]
        return float(np.mean([a for a, _ in r]) / max(np.mean([c for _, c in r]), 1e-9))
    weakzone = zone <= np.quantile(zone, .2)
    def climb(mask):  # among high-talent pupils from weak zones on the academic track, share in a top band
        return float(mask[hi & weakzone & acad].mean())
    r = (np.argsort(np.argsort(logw)) + .5) / n
    conc = float(2 * np.cov(uni.astype(float), r, bias=True)[0, 1] / uni.mean())
    return dict(EO_track=eq(acad), EO_topband_entry=eq(band1), EO_topband_s2=eq(band2), EO_uni=eq(uni), conc_uni=conc,
                weakzone_hiTal_topband_entry=climb(band1), weakzone_hiTal_topband_s2=climb(band2),
                hiTal_vocational_weakzone=float((~acad)[hi & weakzone].mean()))


def avg(**kw):
    rs = [run(seed=s, n=120_000, **kw) for s in range(5)]
    return {k: float(np.mean([x[k] for x in rs])) for k in rs[0]}


if __name__ == '__main__':
    import json
    keys = ['EO_track', 'EO_topband_entry', 'EO_topband_s2', 'EO_uni', 'conc_uni',
            'weakzone_hiTal_topband_entry', 'weakzone_hiTal_topband_s2', 'hiTal_vocational_weakzone']
    out = {}
    cases = {
        'cohort 2015 (pre-gate tutoring legal, no reband)': dict(PRE_TUT=0.15, POST_TUT=0.05, REBAND=False),
        'cohort 2026 (no tutoring, reband at S2)': dict(PRE_TUT=0.0, POST_TUT=0.0, REBAND=True),
        'cohort 2026 but NO reband': dict(PRE_TUT=0.0, POST_TUT=0.0, REBAND=False),
        'cohort 2026, zone teachers = 0 (equal schools)': dict(ZONE_TEACH=0.0),
    }
    print('ratios = richer/poorer at EQUAL TALENT (1.00 = level). ILLUSTRATIVE.')
    print(f"{'case':50s}" + ''.join(f'{k[:13]:>14s}' for k in keys))
    for name, kw in cases.items():
        m = avg(**kw); out[name] = m
        print(f'{name:50s}' + ''.join(f'{m[k]:14.2f}' for k in keys))
    print('\nsensitivity, cohort 2026 with reband: talent-wealth link x zone-teacher effect x fade')
    for tw in (0.0, 0.1, 0.2):
        for zt in (0.15, 0.25, 0.40):
            for dc in (0.25, 0.5, 0.75):
                m = avg(TAL_WEALTH=tw, ZONE_TEACH=zt, DECAY=dc); out[f'sens {tw} {zt} {dc}'] = m
                print(f'tal-wealth {tw:.1f} zone {zt:.2f} fade {dc:.2f}:  EO_uni {m["EO_uni"]:.2f}  '
                      f'weak-zone climbers entry {m["weakzone_hiTal_topband_entry"]:.2f} -> S2 {m["weakzone_hiTal_topband_s2"]:.2f}')
    json.dump(out, open('/home/claude/sig/gz_talent_results.json', 'w'), indent=1)
