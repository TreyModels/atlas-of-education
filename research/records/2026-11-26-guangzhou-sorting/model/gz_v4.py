#!/usr/bin/env python3
"""Guangzhou sorting model v4 (v3.1 + informant corrections, 2026-11-26). v3 docstring follows.
v4 adds: pre-gate tutoring that survives the ban (家教), partial performance re-banding, term-weekend and holiday
tutoring at both tails, a full-time institution route (keep school place), boarding switch for the pre-2021 regime.
Guangzhou sorting model v3: explicit teachers, classes, schools. ILLUSTRATIVE (synthetic pupils).
Teacher/school parameters taken from the dossier '学校与教师质量_Model2参数证据.md' [D]:
  school brand value-added 0-0.2 SD (RD studies)            -> SCHOOL_VA = 0.10
  top/magnet class effect 0.435 SD (double RD, one county)  -> split: TOP_TEACH + PEER
  teacher: median -> top 16% = +0.3-0.5 SD; teacher SD ~0.2  -> TEACH_SD = 0.20 per teacher
  within-school teacher variance net 8-11%, between-school large (sorting) -> junior teacher quality tracks zone (TEACH_ZONE)
  zhibiao dao xiao: ~50% of seats allocated to each junior school's own top pupils  -> ZHIBIAO
Life course: talent, zone wealth -> junior school (zone) with teachers -> skill15 -> zhongkao
 -> elite / regular high school (with ZHIBIAO quota) or vocational -> classes banded by score, best teachers to top band
 -> senior 1 growth -> re-band at senior 2 -> gaokao.  Truth is stored so estimators can be checked against it.
"""
import numpy as np

P = dict(n=60_000, seed=0, TAL_WEALTH=0.10, SEG=0.6, HOME=0.15,
         N_JUNIOR=300, JR_CLASSES=6, TEACH_SD=0.20, TEACH_ZONE=0.10,
         ACAD=0.65, ELITE=0.10, ZHIBIAO=0.5, N_HS=60, HS_CLASS=50,
         SCHOOL_VA=0.10, TOP_BAND=1 / 8, TOP_TEACH=0.30, PEER=0.14, HS_TEACH_SD=0.20,
         GROW=0.5, DECAY=0.5, REBAND=True, NOISE=0.35,
         # hukou layer [D = Guangzhou cost/subsidy dossiers]
         NONHUKOU=0.20,     # share of cohort without local hukou (assumption; teacher saw 10-20% non-locals in an elite school)
         NH_WEALTH=-0.3,    # mean log-wealth shift of non-hukou families (assumption)
         MINBAN_PEN=0.15,   # junior teacher-quality penalty in minban / purchased places (assumption; dossier: private VA ~0)
         QUOTA=0.15,        # max share of PUBLIC academic seats for non-hukou [D 8-15% core, 8-18% outer; 8-20% from 2027]
         PRIVATE_COST=75_000, AFFORD=0.40, MED_INCOME=200_000,
         N_PRIV=12, ZB_FLOOR=0.30,
         # v4 [informant A, 2026-11-26]
         PRE_SHARE=0.4,    # share of families buying pre-gate tutoring with no ban (wealth-weighted)
         BAN_RED=0.4,      # share of that removed by the 2021 ban (informant: much continues as private 家教)
         PRE_EFF=0.15,     # skill gain (SD) for a pre-gate tutoring taker
         REBAND_PERF=0.3,  # share of pupils re-banded by performance at senior 2 (rest by subject combination)
         BOARD=True,       # boarding: term tutoring only at weekends; False = day schools, evenings open
         TERM_SHARE=0.10,  # share of academic pupils tutoring in term when boarding (both tails); x3 when not boarding
         HOL_SHARE=0.40,   # share of academic pupils tutoring in holidays (both tails, wealth-weighted)
         POST_EFF=0.10,    # gaokao gain (SD) for a term or holiday tutoring taker (each)
         FT_SHARE=0.03,    # share of cohort in full-time institution study (keeps school place) [informant ~5%]
         FT_COST=140_000,  # yuan/yr, small class [informant 60-80k/semester]; one-to-one ~1.2m/yr
         FT_EFF=0.0)       # gaokao effect of full-time study relative to staying in school classes (SD; unknown sign)


def run(**kw):
    p = {**P, **kw}; rng = np.random.default_rng(p['seed']); n = p['n']
    J = p['N_JUNIOR']
    zone_j = rng.normal(size=J)                                   # neighbourhood wealth of each junior school zone
    jr = rng.integers(0, J, n)
    hukou = rng.random(n) >= p['NONHUKOU']
    logw = p['SEG'] * zone_j[jr] + np.sqrt(1 - p['SEG'] ** 2) * rng.normal(size=n) + p['NH_WEALTH'] * (~hukou)
    income = p['MED_INCOME'] * np.exp(0.7 * logw)
    tal = p['TAL_WEALTH'] * logw + np.sqrt(1 - p['TAL_WEALTH'] ** 2) * rng.normal(size=n)
    # junior teachers: each junior school has JR_CLASSES teachers; quality = zone gradient + noise
    tq_j = p['TEACH_ZONE'] * zone_j[:, None] + p['TEACH_SD'] * rng.normal(size=(J, p['JR_CLASSES']))
    jcls = rng.integers(0, p['JR_CLASSES'], n)                    # random assignment within junior school (balanced classes rule)
    jteach = np.where(hukou, tq_j[jr, jcls], -p['MINBAN_PEN'] + p['TEACH_SD'] * rng.normal(size=n))
    wr = (np.argsort(np.argsort(logw)) + .5) / n                  # wealth rank
    pre_p = np.clip(p['PRE_SHARE'] * 2 * wr, 0, 1) * (1 - p['BAN_RED'])
    pre = rng.random(n) < pre_p
    head = jteach + p['HOME'] * logw + p['PRE_EFF'] * pre
    skill15 = tal + head
    zk = skill15 + p['NOISE'] * rng.normal(size=n)

    # --- gate: academic seats; elite seats half by open ranking, half by each junior school's quota (zhibiao)
    seats = int(p['ACAD'] * n); order = np.argsort(-zk); nh = ~hukou[order]
    allowed = ~nh | (np.cumsum(nh) <= int(p['QUOTA'] * seats))
    public = np.zeros(n, bool); public[order[allowed][:seats]] = True
    line = zk[public].min()
    shut = (~hukou) & (~public) & (zk >= line)
    private = shut & (p['PRIVATE_COST'] < p['AFFORD'] * income)
    exitp = shut & ~private
    acad = public
    # v3.1 (2026 rules, per review): zhibiao only for Guangzhou-hukou pupils; seats per junior school in proportion to
    # its ELIGIBLE pupils; a minimum score (top ZB_FLOOR of the cohort); unused seats revert to open admission.
    # Open elite admission caps non-hukou at QUOTA of elite seats (school-specific cap applied to the elite tier).
    n_el = int(p['ELITE'] * n); elite = np.zeros(n, bool)
    q_seats = int(p['ZHIBIAO'] * n_el)
    floor = np.quantile(zk, 1 - p['ZB_FLOOR'])
    elig = acad & hukou
    if q_seats and elig.any():
        cnt = np.bincount(jr[elig], minlength=J); tot = cnt.sum()
        for j in np.flatnonzero(cnt):
            k = int(round(q_seats * cnt[j] / tot))
            idx = np.flatnonzero(elig & (jr == j) & (zk >= floor))
            if k and idx.size: elite[idx[np.argsort(-zk[idx])[:k]]] = True
    zhib = elite.copy()
    rest = np.flatnonzero(acad & ~elite); rest = rest[np.argsort(-zk[rest])]
    nh_cap = int(p['QUOTA'] * n_el) - int((elite & ~hukou).sum())
    nhr = ~hukou[rest]; ok = ~nhr | (np.cumsum(nhr) <= nh_cap)
    elite[rest[ok][:max(n_el - elite.sum(), 0)]] = True
    # high schools: elite pupils spread over elite schools (first 10% of N_HS), regular over the rest, by score order
    H = p['N_HS']; n_elite_hs = max(1, int(round(H * p['ELITE'] / p['ACAD'])))
    hs = np.full(n, -1)
    def assign(mask, lo, hi):
        idx = np.flatnonzero(mask); idx = idx[np.argsort(-zk[idx])]
        for c, part in enumerate(np.array_split(idx, hi - lo)): hs[part] = lo + c
    assign(elite, 0, n_elite_hs); assign(acad & ~elite, n_elite_hs, H)
    if private.any(): assign(private, H, H + p['N_PRIV'])
    acad = public | private
    school_va = np.where((hs >= 0) & (hs < H), np.where(hs < n_elite_hs, 2, 1) * p['SCHOOL_VA'], 0.0)

    def band_and_class(score):
        band = np.zeros(n, bool); cls = np.full(n, -1)
        for s in range(H + p['N_PRIV']):
            idx = np.flatnonzero(hs == s)
            if not idx.size: continue
            idx = idx[np.argsort(-score[idx])]
            ntop = max(1, int(round(p['TOP_BAND'] * idx.size)))
            band[idx[:ntop]] = True
            for c, part in enumerate(np.array_split(idx, max(1, idx.size // p['HS_CLASS']))): cls[part] = s * 1000 + c
        return band, cls
    band1, cls1 = band_and_class(zk)
    # high-school teachers: top band gets +TOP_TEACH, every class a random teacher draw
    uniq = np.unique(cls1[cls1 >= 0]); tdraw = dict(zip(uniq, p['HS_TEACH_SD'] * rng.normal(size=uniq.size)))
    hteach1 = np.array([tdraw.get(c, 0.0) for c in cls1]) + band1 * p['TOP_TEACH']
    peer1 = band1 * p['PEER']
    skill16 = tal + (1 - p['DECAY']) * head + p['GROW'] * tal + school_va + hteach1 + peer1
    obs16 = skill16 + p['NOISE'] * rng.normal(size=n)
    if p['REBAND']:
        # v5.1 fix: composite rank keeps the top-band size fixed (previous version let it grow)
        r16 = (np.argsort(np.argsort(obs16)) + .5) / n; r15 = (np.argsort(np.argsort(zk)) + .5) / n
        band2, cls2 = band_and_class(p['REBAND_PERF'] * r16 + (1 - p['REBAND_PERF']) * r15)
        uniq2 = np.unique(cls2[cls2 >= 0]); tdraw2 = dict(zip(uniq2, p['HS_TEACH_SD'] * rng.normal(size=uniq2.size)))
        hteach2 = np.array([tdraw2.get(c, 0.0) for c in cls2]) + band2 * p['TOP_TEACH']
    else:
        band2, cls2, hteach2 = band1, cls1, hteach1
    peer2 = band2 * p['PEER']
    # post-gate tutoring: both tails of the academic skill distribution, wealth-weighted
    a_idx = acad
    sr = np.full(n, .5); sr[a_idx] = (np.argsort(np.argsort(skill16[a_idx])) + .5) / a_idx.sum()
    tail = np.where((sr < .2) | (sr > .8), 2.0, 0.5)
    tw = tail * (0.5 + wr)                                          # mean about 1
    term_share = p['TERM_SHARE'] * (1 if p['BOARD'] else 3)
    term = a_idx & (rng.random(n) < np.clip(term_share * tw / tw[a_idx].mean(), 0, 1))
    hol = a_idx & (rng.random(n) < np.clip(p['HOL_SHARE'] * tw / tw[a_idx].mean(), 0, 1))
    # full-time institution route: affordable (cost < 50% income), weaker half, chosen to reach FT_SHARE of cohort
    cand = a_idx & (p['FT_COST'] < 0.5 * income) & (sr < .5)
    ft = np.zeros(n, bool)
    if p['FT_SHARE'] > 0 and cand.any():
        k = min(int(p['FT_SHARE'] * n), cand.sum()); ft[rng.choice(np.flatnonzero(cand), k, replace=False)] = True
    in_school = np.where(ft, 0.0, hteach2 + peer2)
    skill18 = skill16 + in_school + p['POST_EFF'] * (term.astype(float) + hol) + ft * p['FT_EFF']
    gk = skill18 + p['NOISE'] * rng.normal(size=n)
    gk_acad = np.where(acad, gk, -np.inf)
    uni = gk_acad >= np.sort(gk_acad)[::-1][int(.10 * n) - 1]
    sub = (np.where(hukou, 19_600, 5_000) * 6 + np.where(hukou, 32_100, 6_000) * 3
           + np.where(public, 41_500, np.where(private | exitp, 0, 38_400)) * 3.0)
    return dict(pre=pre, term=term, hol=hol, ft=ft, ft_cand=cand, hukou=hukou, public=public, private=private, exitp=exitp, income=income, subsidy=sub, zhib=zhib, p=p, tal=tal, logw=logw, zone=zone_j[jr], jr=jr, jteach=jteach, head=head, skill15=skill15, zk=zk,
                acad=acad, elite=elite, hs=hs, school_va=school_va, band1=band1, cls1=cls1, band2=band2, cls2=cls2,
                hteach2=hteach2, peer2=peer2, skill18=skill18, gk=gk, uni=uni, n_elite_hs=n_elite_hs)
