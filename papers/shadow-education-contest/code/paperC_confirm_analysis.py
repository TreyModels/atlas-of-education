#!/usr/bin/env python3
"""Paper C CONFIRMATORY A5 analysis: T2/T3 paired-seed contrasts, Holm m=2, achieved CI/MDE (host-only)."""
import json, math, sys, hashlib
J = sys.argv[1] if len(sys.argv) > 1 else '/Users/treymenefee/neon-boot/qa/incoming/paperC_confirmatory/paperC_confirmatory.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'docs/audit/PAPER_C_CONFIRMATORY_RESULTS.json'
d = json.load(open(J)); cells = d['cells']; SEEDS = list(range(100, 116))
rows = {cid: {int(r['seed']): r for r in c['rows'] if int(r['seed']) in SEEDS} for cid, c in cells.items()}
def cid(s, l, sup, st): return f'S{float(s):.2f}|L{float(l):.2f}|{sup}|{st}'
def tstat(vals):
    n = len(vals); m = sum(vals) / n
    var = sum((v - m) ** 2 for v in vals) / (n - 1); se = math.sqrt(var / n)
    if se == 0: return m, se, (0.0 if m != 0 else 1.0), (m, m)
    t = m / se; p = math.erfc(abs(t) / math.sqrt(2))
    return m, se, p, (m - 1.96 * se, m + 1.96 * se)
def contrast(pairs, field, scale=1.0):
    out = []
    for sd in SEEDS:
        ds = [(rows[a][sd][field] - rows[b][sd][field]) * scale for a, b in pairs if sd in rows[a] and sd in rows[b]]
        out.append(sum(ds) / len(ds))
    return out
# T2: C-A own_share_financial_proxy, across S,L,settings
v2 = contrast([(cid(S, L, 'C', st), cid(S, L, 'A', st)) for S in (0.85, 1.0, 1.15) for L in (0.25, 0.45) for st in ('P55', 'P12')], 'own_share_financial_proxy')
m2, se2, p2, ci2 = tstat(v2)
# T3: A|P55 - A|P12 withheld, across S,L
v3 = contrast([(cid(S, L, 'A', 'P55'), cid(S, L, 'A', 'P12')) for S in (0.85, 1.0, 1.15) for L in (0.25, 0.45)], 'withheld')
m3, se3, p3, ci3 = tstat(v3)
h55 = sum(rows[cid(S, L, 'A', 'P55')][sd]['withheld'] for S in (0.85, 1.0, 1.15) for L in (0.25, 0.45) for sd in SEEDS) / (6 * len(SEEDS))
h12 = sum(rows[cid(S, L, 'A', 'P12')][sd]['withheld'] for S in (0.85, 1.0, 1.15) for L in (0.25, 0.45) for sd in SEEDS) / (6 * len(SEEDS))
# Holm m=2
ps = sorted([(p2, 'T2'), (p3, 'T3')]); holm = {}; prev = 0.0
for i, (p, k) in enumerate(ps):
    adj = min(1.0, max(prev, 2 * p)); holm[k] = adj; prev = adj
def verdict(e, min_e, p_holm, ci, direction='positive'):
    dir_ok = e > 0 if direction == 'positive' else e < 0
    return dict(effect=e, min_effect=min_e, direction_ok=dir_ok, min_effect_met=abs(e) >= min_e,
                holm_significant=(p_holm < 0.05), ci95=list(ci), mde_half_width=(ci[1] - ci[0]) / 2,
                passes=bool(dir_ok and abs(e) >= min_e and p_holm < 0.05))
res = dict(
    paper='Paper C CONFIRMATORY — A5 16-seed interim analysis',
    source=J, source_sha256=hashlib.sha256(open(J, 'rb').read()).hexdigest(),
    design=dict(cells=len(cells), seeds=SEEDS, n_seeds=16, n_runs=d['n_runs'], n_cells=d['n_cells'], invalid_cells=d['invalid_cells'],
                n=1500, t=46, holm_family=['T2', 'T3'], holm_m=2, alpha=0.05,
                engine_commit='846c9e0', core_sha256='e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71',
                a5='docs/audit/PAPER_C_A5_SEED_TRUNCATION.md sha 36515596...', precision='A5 interim: SE=sqrt(2) x 32-seed plan; no full-precision claim'),
    T2=dict(estimand='own_share_financial_proxy (C - A), paired by seed; proxy caveat (contest-prep mixing; only L=.25 P55/P12 and L=.45 P55 for T2 cells)',
            **verdict(m2, 0.10, holm['T2'], ci2), se=se2, p=p2, p_holm=holm['T2']),
    T3=dict(estimand='withheld (A|P55 - A|P12), paired by seed', **verdict(m3, 0.05, holm['T3'], ci3), se=se3, p=p3, p_holm=holm['T3'],
            h_A_P55=h55, h_A_P12=h12, assertion_support=bool(h55 >= 0.05 and h12 <= 0.01)),
    T1_T4='SCREENING FAILURES (T1 +0.655pp vs >=3.0; T4 +1.767pp vs >=2.0) — NOT confirmatorily tested; no threshold change',
    no_s_generalisation='all six passers are S=0.85; no S-generalisation claim',
)
json.dump(res, open(OUT, 'w'), indent=2)
print(json.dumps({k: res[k] for k in ('T2', 'T3')}, indent=1)[:1800]); print('wrote', OUT, hashlib.sha256(open(OUT, 'rb').read()).hexdigest())
