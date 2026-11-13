"""floorworld v2: what does education do for industrialisation? China, Vietnam, the Philippines, Cambodia.

Aggregate cohort model, 1980-2035, built to make rival theories of education precise and test them jointly against
four countries (docs/education_and_formalization.md). Each year an 18-year-old cohort (size 1) leaves school with:
  B  below lower secondary            L  lower secondary (the 'floor')
  U  general upper secondary          V  vocational upper secondary          T  tertiary
and joins a 40-year workforce. Jobs:
  I  informal (anyone; untaxed)                                   wage 1
  R  formal routine: factories, garments, BPO (needs L or more;   wage 2   (a share b_ok of R jobs still takes B)
     hired by rank, so surplus graduates bump others down)
  G  public / state-enterprise graduate posts                     wage 2.5
  K  formal complex: teams of graduates with distinct know-how    wage 4
     (Hidalgo's personbytes) using capabilities built by doing

Theories (structures):
  S1 human-capital-led  formal and complex jobs grow with productive human capital (supply creates demand; schooling
                        makes activity legible and taxable)
  S2 demand-led         formal and complex jobs are set by investment and industrial policy; education only fills them
  S3 complexity         routine jobs from investment; complex jobs need capabilities (built by doing, closer to complex
                        products = faster) AND enough productive graduates to staff teams
  S5 floor + demand     the hybrid argued in the notes: the floor attracts factory investment (as S4), but complex
                        jobs follow industrial policy and demand (as S2), not the graduate stock
  S4 adoption           as S3, but factory investment locates where the productive floor is (Nelson & Phelps 1966:
                        education matters for absorbing technology); the floor attracts investment, investment raises
                        returns to schooling
Caplan is a parameter, not a structure: each level's credential has a signalling share sigma (zero-sum ranking) and a
productive share 1 - sigma. Only the productive part raises output, attracts investment or staffs complex teams.
Vocational upper secondary has four roles with weights drawn by the Monte Carlo: skills, pipeline (tied to employers'
vacancies), protection (keeps 12-15s in school to finish the floor; Nordtveit) and parking (none of the above).
Learning quality q scales what a year of school teaches (Hanushek & Woessmann; Pritchett).
"""
import math
import numpy as np

YEARS = np.arange(1980, 2036)
LEV = ('B', 'L', 'U', 'V', 'T')


def ramp(y, pts):
    xs, vs = zip(*pts)
    return float(np.interp(y, xs, vs))


# ---- stylised schedules: inputs, not fitted. Sources and caveats in docs/education_and_formalization.md
COUNTRIES = {
    'China': dict(floor_lower=[(1980, .3), (1990, .5), (2000, .85), (2010, .95)],      # 9-yr compulsory law 1986
                  floor_upper=[(1980, .1), (2005, .5), (2020, .9)], vshare=[(1980, .2), (1995, .45), (2020, .45)],
                  he_cap=[(1980, .02), (1998, .07), (1999, .1), (2010, .3), (2020, .55)],   # 1999 expansion
                  invest=[(1980, .02), (1990, .15), (2001, .35), (2012, .5), (2035, .5)],    # SEZs, WTO 2001
                  invest_K=[(1980, 0), (2000, .01), (2020, .08)], prox=.8, q=.9,
                  public=[(1980, .06), (1998, .06), (2010, .04)], wait=.6, emig=[(1980, 0), (2035, .02)], tax_eff=.6),
    'Vietnam': dict(floor_lower=[(1980, .2), (1990, .3), (2000, .6), (2010, .8), (2020, .85)],
                    floor_upper=[(1980, .1), (2000, .3), (2020, .5)], vshare=[(1980, .1), (2020, .2)],
                    he_cap=[(1980, .02), (1995, .03), (2005, .1), (2019, .29)],
                    invest=[(1980, 0), (1990, .02), (2000, .1), (2010, .3), (2020, .45)],     # Doi Moi, FDI electronics
                    invest_K=[(1980, 0), (2010, .005), (2020, .02)], prox=.6, q=1.0,           # PISA 2012 ~ Germany
                    public=[(1980, .04), (2000, .04), (2020, .03)], wait=.2, emig=[(1980, .02), (2035, .05)], tax_eff=.5),
    'Philippines': dict(floor_lower=[(1980, .6), (2000, .75), (2022, .84)],
                        floor_upper=[(1980, 0), (2015, 0), (2016, .3), (2018, .6), (2022, .7)],   # K-12 from 2016
                        vshare=[(1980, 0), (2015, 0), (2016, .3)],                                  # TVL track
                        he_cap=[(1980, .2), (2000, .3), (2020, .35)],
                        invest=[(1980, .08), (2005, .12), (2020, .2)], invest_K=[(1980, 0), (2035, .005)],
                        prox=.4, q=.6, public=[(1980, .04), (2035, .04)], wait=.2,
                        emig=[(1980, .1), (2000, .25), (2020, .3)], tax_eff=.4),               # OFWs
    'Cambodia': dict(floor_lower=[(1980, .05), (1990, .1), (2000, .2), (2010, .4), (2021, .56)],  # UIS completion
                     floor_upper=[(1980, 0), (2035, .1)], vshare=[(1980, 0), (2035, .05)],
                     he_cap=[(1980, .005), (2000, .03), (2019, .15)],
                     invest=[(1980, 0), (1995, .03), (2005, .1), (2015, .15), (2020, .2)],      # garments, SEZs
                     invest_K=[(1980, 0), (2035, 0)], prox=.1, q=.5,
                     public=[(1980, .02), (2035, .02)], wait=.1, emig=[(1980, 0), (2035, .03)], tax_eff=.3),
}

PRIORS = {
    'sig_L': (0.0, 0.3), 'sig_U': (0.0, 0.7), 'sig_T': (0.0, 0.9),   # Caplan: signalling share by level
    'legib': (0.0, 0.6), 'k_sup': (0.2, 1.0),                        # S1
    'k_cap': (0.5, 3.0), 'team': (0.02, 0.15), 'learn': (0.05, 0.4), 'decay': (0.01, 0.1),   # S3/S4
    'eta': (0.5, 3.0), 'adj': (0.05, 0.3),                          # S4: attraction to the floor, adjustment speed
    'b_ok': (0.1, 0.6),
    'inv_scale': (0.3, 2.0),                                        # every theory: how many routine jobs a unit of investment makes                                             # share of routine jobs open to below-floor workers
    'resp': (1.0, 6.0), 'budget': (0.5, 3.0), 'emig_resp': (0.5, 2.0),
    'v_skill': (0.0, 1.0), 'v_pipe': (0.0, 1.0), 'v_protect': (0.0, 1.0),
}
OUTS = ('informal', 'formal', 'complex', 'overeduc', 'undereduc', 'surplus', 'emig', 'tax', 'output', 'floor', 'tertiary')


def simulate(country, S, th, override=None):
    c = dict(COUNTRIES[country]); c.update(override or {})
    sig = dict(B=0.0, L=th['sig_L'], U=th['sig_U'], V=th['sig_U'], T=th['sig_T'])
    base = dict(B=0.0, L=1.0, U=1.3, V=1.3, T=2.0)
    q = c['q']

    def prod(e):   # productive skill of one worker with credential e
        extra = (base[e] - (1.0 if e != 'B' else 0.0))
        if e == 'V':
            extra *= th['v_skill']
        return q * ((1.0 if e != 'B' else 0.0) * (1 - sig['L']) + extra * (1 - sig[e]))

    # initial stock: steady state of 1980 schooling
    y0 = YEARS[0]; Lst = {}
    l0 = ramp(y0, c['floor_lower']); u0 = l0 * ramp(y0, c['floor_upper']); h0 = min(u0, ramp(y0, c['he_cap']))
    v0 = (u0 - h0) * ramp(y0, c['vshare'])
    Lst = dict(B=1 - l0, L=l0 - u0, U=u0 - h0 - v0, V=v0, T=h0)
    JR = ramp(y0, c['invest']); cap = 0.01; tax = 0.0; prem = dict(L=.3, U=.3, T=.6)
    out = {k: np.zeros(len(YEARS)) for k in OUTS}
    for i, y in enumerate(YEARS):
        # ---- this year's cohort (economy -> education)
        prot = th['v_protect'] * ramp(y, c['vshare']) * 0.3
        floorL = min(1.0, ramp(y, c['floor_lower']) + min(0.15, th['budget'] * tax * 0.3) + prot)
        l = floorL + (1 - floorL) * 0.5 / (1 + math.exp(-(th['resp'] * prem['L'] - 1)))
        u = l * max(ramp(y, c['floor_upper']), 0.8 / (1 + math.exp(-(th['resp'] * prem['U'] - 1.2))))
        h = min(u, ramp(y, c['he_cap']), u * 1 / (1 + math.exp(-(th['resp'] * prem['T'] - 1.5))) + .5 * ramp(y, c['he_cap']))
        v = (u - h) * ramp(y, c['vshare'])
        coh = dict(B=1 - l, L=l - u, U=u - h - v, V=v, T=h)
        for e in LEV:
            Lst[e] = Lst[e] * (1 - 1 / 40) + coh[e] / 40
        W = sum(Lst.values())
        effT = Lst['T'] * q * (1 - sig['T'])                                     # productive graduates
        floorP = sum(Lst[e] for e in ('L', 'U', 'V', 'T')) / W * q * (1 - sig['L'])   # productive floor
        Hprod = sum(Lst[e] * prod(e) for e in LEV)
        inv = th['inv_scale'] * ramp(y, c['invest']) * (1 + 0.3 * th['v_pipe'] * ramp(y, c['vshare']))
        # ---- jobs by theory
        if S == 'S1':
            JR = 0.5 * inv + th['legib'] * Hprod
            JK = th['k_sup'] * effT
        elif S == 'S2':
            JR = inv; JK = ramp(y, c['invest_K'])
        elif S == 'S5':                       # hybrid: the floor attracts factory investment; complex jobs follow demand
            JR = JR + th['adj'] * (inv * min(1.5, (floorP / .6) ** th['eta']) - JR)
            JK = ramp(y, c['invest_K'])
        else:
            if S == 'S4':
                JR = JR + th['adj'] * (inv * min(1.5, (floorP / .6) ** th['eta']) - JR)
            else:
                JR = inv
            JK = th['k_cap'] * cap * (1 - math.exp(-(effT / W) / th['team'])) * W
        JG = ramp(y, c['public']) * W
        # ---- allocation by rank
        EK = min(JK, Lst['T']); restT = Lst['T'] - EK
        EG = min(JG, restT); restT -= EG
        emig = restT * min(1.0, ramp(y, c['emig']) * th['emig_resp']); restT -= emig
        wait = restT * c['wait']; restT -= wait
        avail = dict(T=restT, U=Lst['U'], V=Lst['V'], L=Lst['L'], B=Lst['B'])
        order = ['T', 'V', 'U', 'L'] if th['v_pipe'] > .5 else ['T', 'U', 'V', 'L']
        # a share b_ok of routine jobs hires whoever is available (garment lines, no credential screen);
        # the rest screen by credential rank (Thurow job competition; Caplan's signal does its work here)
        open_jobs = JR * th['b_ok']; pool = sum(avail.values())
        ER = {e: min(avail[e], open_jobs * avail[e] / max(pool, 1e-9)) for e in avail}
        left = JR - sum(ER.values())
        for e in order:
            take = min(avail[e] - ER[e], left); ER[e] += take; left -= take
        EI = {e: avail[e] - ER[e] for e in avail}
        nR = sum(ER.values()); nI = sum(EI.values()); emp = EK + EG + nR + nI
        # ---- output, taxes, capabilities (economy loops)
        skillR = sum(ER[e] * prod(e) for e in ER) / max(nR, 1e-9)
        Y = 4 * EK * (1 + .2 * q * (1 - sig['T'])) + 2.5 * EG + nR * 2 * (1 + .3 * (skillR - 1)) + nI
        formal_bill = Y - nI
        tax = c['tax_eff'] * formal_bill / max(Y, 1e-9) * 0.25
        if S in ('S3', 'S4'):
            cap += th['learn'] * (EK / W + c['prox'] * .5 * nR / W) + ramp(y, c['invest_K']) - th['decay'] * cap
        # ---- expected returns for the next cohort (job access by credential)
        def ew(e, Eformal, wage):
            n = Lst[e] if e != 'T' else max(Lst['T'] - emig, 1e-9)
            return (Eformal * wage + (n - Eformal)) / max(n, 1e-9)
        wB = ew('B', ER['B'], 2); wL = ew('L', ER['L'], 2); wU = ew('U', ER['U'] + ER['V'] * (Lst['U'] > 0), 2)
        wT = (4 * EK + 2.5 * EG + 2 * ER['T'] + EI['T'] + 0 * wait) / max(Lst['T'] - emig, 1e-9)
        prem = {k: .7 * prem[k] + .3 * val for k, val in (('L', wL / max(wB, 1e-9) - 1), ('U', wU / max(wL, 1e-9) - 1),
                                                          ('T', wT / max(wU, 1e-9) - 1))}
        o = dict(informal=nI / emp, formal=1 - nI / emp, complex=EK / emp,
                 overeduc=(ER['T'] + EI['T'] + EI['U'] + EI['V']) / emp,
                 undereduc=ER['B'] / max(nR, 1e-9), surplus=(Lst['T'] - EK - EG) / max(Lst['T'], 1e-9),
                 emig=emig / W, tax=tax, output=Y / W, floor=l, tertiary=h)
        for k in OUTS:
            out[k][i] = o[k]
    return out


def at(o, k, y):
    return float(o[k][int(y - YEARS[0])])
