"""Python twin of web/camchild.js: Cambodia child labour, two linked regions (Phnom Penh, countryside).

A line-by-line port so the Cambodia world runs where the Python engine runs (AI sandboxes, atlas scripts, fitting).
The browser file is the source of truth for the interface; this file must reproduce it draw for draw. Same seed, same
random stream, same household choices: tests/camchild_parity.py checks every yearly aggregate and every choice
against node. Change both files together.

Money is in units of one adult informal annual wage (= 1). Every constant is an assumption unless noted (see the JS).
"""
import math

STATES = ['school', 'both', 'work', 'neither']
HAZ = .35   # share of full-time 15-17 workers in hazardous work or over 48 hours

REGIONS = {
    'pp': dict(label='Phnom Penh', share=.22, yMedian=1.55, ySigma=.6, shockP=.08, shockSize=.35, borrow=.22,
               debt=.07, distance=0, quality=.62, safety=.66, localPull=1.25, enterprise=.18, leftBehind=.05,
               formalJobs=.40, tutoring=.06, credFloor=.55, migrate=False, vPrim=3.391, vLow=2.162, vUp=.886),
    'rural': dict(label='Countryside', share=.78, yMedian=.9, ySigma=.6, shockP=.16, shockSize=.45, borrow=.12,
                  debt=.12, distance=.45, quality=.50, safety=.64, localPull=.80, enterprise=.55, leftBehind=.20,
                  formalJobs=.05, tutoring=.025, credFloor=.25, migrate=True, vPrim=3.506, vLow=5.657, vUp=2.199),
}

POLICY0 = dict(cashU=0, cash=0, feeding=0, protection=0, leftSupport=0, harvest=0, bridging=0, tutorFix=0, ban=0,
               debtRelief=0, garmentBoom=0, thaiOpen=1, floorRise=0)

QCUT = [-.8416, -.2533, .2533, .8416]


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


class _RNG:
    """The JS linear congruential generator: n = (n * 1664525 + 1013904223) >>> 0; return n / 2**32."""
    def __init__(self, seed):
        self.n = seed % 2 ** 32

    def __call__(self):
        self.n = (self.n * 1664525 + 1013904223) % 2 ** 32
        return self.n / 2 ** 32


def _normal(r):
    u = 0.0
    while u == 0:
        u = r()
    return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * r())


def _mk():
    return dict(n=0, school=0, both=0, work=0, neither=0, cl=0, migrant=0, lab=0.0,
                lvl=[[0, 0], [0, 0], [0, 0]], q=[dict(n=0, cl=0) for _ in range(5)], girls=[0, 0], boys=[0, 0],
                left=[0, 0])


def _cst(P, reg):
    return (P['feeding'] * .05 + P['protection'] * .03
            + (P['leftSupport'] * REGIONS['rural']['leftBehind'] * .08 + P['harvest'] * .005 if reg == 'rural'
               else P['leftSupport'] * .004)
            + P['bridging'] * .01 + P['tutorFix'] * .03 + P['ban'] * .004 + P['debtRelief'] * .02)


def simulate(years=12, N=6000, seed=7, policy=None, over=None):
    P = dict(POLICY0, **(policy or {}))
    over = over or {}
    R = {k: dict(REGIONS[k], **over.get(k, {})) for k in ('pp', 'rural')}
    r = _RNG(seed)
    H = []
    for _ in range(N):
        reg = 'pp' if r() < R['pp']['share'] else 'rural'
        C = R[reg]
        z = _normal(r)
        h = dict(reg=reg, z=z, y0=C['yMedian'] * math.exp(C['ySigma'] * z))
        h['age'] = 6 + math.floor(r() * 12)
        h['girl'] = r() < .5
        h['left'] = r() < C['leftBehind'] * (1.3 - .5 * (1 if z > 0 else 0))
        h['thai'] = r() < .65
        h['ability'] = _normal(r)
        h['enterprise'] = r() < C['enterprise']
        h['outYears'] = 0
        h['everOut'] = False
        h['taste'] = _normal(r)
        H.append(h)
    quint = lambda h: sum(1 for c in QCUT if h['z'] > c)
    wChild = {'pp': 1.0, 'rural': 1.0}
    L0 = None
    rows = []
    spent = dict(cash=0.0, other=0.0)

    def util(c, need):
        x, x0 = c - .6 * need, .05
        return math.log(x) if x > x0 else math.log(x0) + (x - x0) / x0

    for t in range(years):
        def decide():
            S = {'pp': _mk(), 'rural': _mk(), 'all': _mk()}
            choice, migr = [], []
            cash = 0.0
            for h in H:
                C = R[h['reg']]; q = quint(h); a = h['age']; rural = h['reg'] == 'rural'
                shocked = r() < C['shockP']
                y = h['y0'] * (1 - C['shockSize'] if shocked else 1)
                if shocked:
                    y += min(C['shockSize'] * h['y0'], (C['borrow'] + P['debtRelief'] * .1) * h['y0'])
                y -= C['debt'] * h['y0'] * (1 - P['debtRelief'] * .7)
                left = h['left']
                if h['left']:
                    if h['thai'] and P['thaiOpen'] < 1:
                        y += .6 * .63 * (1 - P['thaiOpen']); left = r() < P['thaiOpen']; y += .45 * P['thaiOpen']
                    else:
                        y += .45
                if q <= 1:
                    y += P['cashU']   # unconditional transfer: income effect only
                need = .85
                ageW = .25 if a < 10 else .45 if a < 12 else .7 if a < 15 else 1
                visible = P['ban'] * C['formalJobs']
                pull = C['localPull'] * (1 + P['garmentBoom'] if h['reg'] == 'pp' and a >= 14 else 1)
                famRet = .55 if h['enterprise'] else 0
                earn = .32 * ageW * max(wChild[h['reg']] * pull * (1 - visible), famRet)
                mig = False
                if C['migrate'] and a >= 15:
                    toPP = (.32 * R['pp']['localPull'] * (1 + P['garmentBoom']) * wChild['pp']
                            * (1 - P['ban'] * R['pp']['formalJobs']) - .10)
                    toTH = .32 * 1.9 * P['thaiOpen'] - .14
                    best = max(toPP, toTH) * .8
                    if best > earn:
                        earn = best; mig = True
                lvl = 0 if a <= 11 else 1 if a <= 14 else 2
                fee = [.03, .08, .13][lvl]
                tut = C['tutoring'] * [.6, 1, 1.4][lvl] * (1 - P['tutorFix'])
                dist = C['distance'] * [.03, .14, .22][lvl]
                cost = fee + tut + dist
                feed = P['feeding'] * (.07 if lvl == 0 else .05)
                cashAmt = P['cash'] if q <= 1 else 0
                quality = clamp(C['quality'] + .15 * P['protection'] + .05 * P['tutorFix']
                                + (.2 * P['bridging'] if h['outYears'] > 0 else 0), 0, 1.2)
                safety = clamp(C['safety'] + P['protection'] * (1 - C['safety']), 0, 1)
                leftPen = -.45 * (1 - P['leftSupport']) if left else 0
                reentry = (-1.3 * (1 - .7 * P['bridging']) * min(h['outYears'], 3) / 3) if h['outYears'] > 0 else 0
                floor = 1.1 * (clamp(C['credFloor'] + P['floorRise'] * (1 - C['credFloor']), 0, 1) - .4) if lvl == 2 else 0
                vLvl = [C['vPrim'], C['vLow'], C['vUp']][lvl]
                valueSchool = (vLvl + 1.1 * (quality - .55) + 1.2 * (safety - .65) + leftPen + reentry + floor
                               + .25 * h['ability'])
                harvestWork = .5 * P['harvest'] if rural and a >= 12 else 0
                U = dict(school=util(y - cost + feed + cashAmt, need) + valueSchool,
                         both=util(y - cost + feed + cashAmt + .5 * earn, need) + valueSchool * .72 + harvestWork - .25,
                         work=util(y + earn, need) - .2 * h['taste'],
                         neither=util(y, need) - .6 + (.25 if h['girl'] else 0))
                m = max(U['school'], U['both'], U['work'], U['neither'])
                ex = [math.exp((U[s] - m) / .3) for s in STATES]
                Z = 0.0
                for e in ex:
                    Z += e
                u = r() * Z; k = 0
                while u > ex[k] and k < 3:
                    u -= ex[k]; k += 1
                s = STATES[k]
                choice.append(s); migr.append(s == 'work' and mig)
                if s in ('school', 'both'):
                    cash += cashAmt
                if q <= 1:
                    cash += P['cashU']
                isCL = (s == 'work' and (a < 15 or r() < HAZ)) or (s == 'both' and a < 12)
                for G in (S[h['reg']], S['all']):
                    G['n'] += 1; G[s] += 1
                    if isCL:
                        G['cl'] += 1
                    if s == 'work' and mig:
                        G['migrant'] += 1
                    if s == 'work' and not mig:
                        G['lab'] += ageW
                    if s == 'both':
                        G['lab'] += .5 * ageW
                    G['lvl'][lvl][1] += 1
                    if s in ('work', 'neither'):
                        G['lvl'][lvl][0] += 1
                    G['q'][q]['n'] += 1
                    if isCL:
                        G['q'][q]['cl'] += 1
                    g = G['girls'] if h['girl'] else G['boys']
                    g[1] += 1
                    if isCL:
                        g[0] += 1
                    if left:
                        G['left'][1] += 1
                        if isCL:
                            G['left'][0] += 1
            return dict(S=S, choice=choice, migr=migr, cash=cash)

        Dd = decide()
        if L0 is None:
            L0 = {'pp': max(Dd['S']['pp']['lab'], 1), 'rural': max(Dd['S']['rural']['lab'], 1)}
        for _ in range(3):
            for k in ('pp', 'rural'):
                wChild[k] = clamp(math.pow(max(Dd['S'][k]['lab'], 1) / L0[k], -1 / 2.5), .4, 2.2)
            Dd = decide()
        spent['cash'] += Dd['cash']
        nPP, nR = Dd['S']['pp']['n'], Dd['S']['rural']['n']
        spent['other'] += nPP * _cst(P, 'pp') + nR * _cst(P, 'rural')

        def pack(G):
            n = G['n']
            return dict(n=n, school=G['school'] / n, both=G['both'] / n, work=G['work'] / n, neither=G['neither'] / n,
                        attend=(G['school'] + G['both']) / n, cl=G['cl'] / n, migrant=G['migrant'] / n,
                        oos=[x[0] / x[1] if x[1] else 0 for x in G['lvl']],
                        clPoor=G['q'][0]['cl'] / max(G['q'][0]['n'], 1), clRich=G['q'][4]['cl'] / max(G['q'][4]['n'], 1),
                        clGirls=G['girls'][0] / max(G['girls'][1], 1), clBoys=G['boys'][0] / max(G['boys'][1], 1),
                        clLeft=G['left'][0] / max(G['left'][1], 1),
                        balance=G['school'] + G['both'] + G['work'] + G['neither'] - n)
        rows.append(dict(t=t, year=2025 + t, pp=pack(Dd['S']['pp']), rural=pack(Dd['S']['rural']),
                         all=pack(Dd['S']['all']), wChild=dict(wChild), choice=list(Dd['choice']),
                         migr=list(Dd['migr']), age=[h['age'] for h in H], left=[h['left'] for h in H]))
        for i, h in enumerate(H):
            s = Dd['choice'][i]
            if s in ('work', 'neither'):
                h['outYears'] += 1; h['everOut'] = True
            else:
                h['outYears'] = 0
            h['age'] += 1
            if h['age'] > 17:
                h['age'] = 6; h['outYears'] = 0; h['everOut'] = False
                h['ability'] = _normal(r); h['girl'] = r() < .5
    return dict(rows=rows, spent=dict(cash=spent['cash'], other=spent['other'], total=spent['cash'] + spent['other']),
                N=N, H=H, P=P)


def compare(years=12, N=6000, seed=7, policy=None, over=None):
    policy = policy or {}
    base = simulate(years, N, seed, dict(thaiOpen=policy.get('thaiOpen', 1)), over)
    pol = simulate(years, N, seed, policy, over)
    yearsAvoided = sum(b['all']['cl'] - p['all']['cl'] for b, p in zip(base['rows'], pol['rows'])) * base['N']
    return dict(base=base, pol=pol, yearsAvoided=yearsAvoided,
                costPer=pol['spent']['total'] / yearsAvoided if yearsAvoided > 0 else None)
