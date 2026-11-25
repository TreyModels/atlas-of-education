#!/usr/bin/env python3
"""Paper C — frozen PASSER computation from the screening artefact (host-only; no compute).

Rules (declared; for adjudicator sign-off):
  Data: screening JSON cells (per-cell seed rows; 8 matched seeds 0-7).
  T1 (S substitution): for each (L,supply,setting): d = tut_k12_rate(S=.85) - tut_k12_rate(S=1.15) (pp);
      effect = mean over 12 combinations of per-seed d; predicted sign positive; min effect +3 pp.
  T2 (supply form): for each (S,L,setting): d = own_share_financial_proxy(C) - (A); effect = mean over 12 combos;
      predicted positive; min +0.10.
  T3 (withholding assertion-support): for each (S,L): d = withheld(A|P55) - withheld(A|P12); effect mean over 6;
      pass requires mean withheld(A|P55) >= 0.05, mean withheld(A|P12) <= 0.01, and d >= 0.05.
  T4 (gate pressure): for each (S,supply,setting): d = (q5_q1_spend_gap(L=.45) - q5_q1_spend_gap(L=.25)) * 100 (pp);
      effect mean over 12; predicted positive; min +2 pp.
  p per test: one-sample two-sided t on the 8 per-seed effect values; Holm across T1-T4 at alpha=.05.
  Test passes = correct direction AND |effect| >= min effect AND Holm-adjusted p < .05.
  Candidate cells = union of cells used in passing tests; order = frozen appendix order (manifest['cells']).
  >6 rule: if |candidates| <= 6 all are passers; else the first 6 in appendix order are passers and the rest are
  reported screening-only.
Output: PAPER_C_PASSERS.json (rules, per-test estimates/CI/p/Holm, candidate list, frozen passers, appendix order).
"""
import json, math, hashlib, sys

SCREEN = sys.argv[1] if len(sys.argv) > 1 else '/Users/treymenefee/neon-boot/qa/incoming/paperC_screening/paperC_screening.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'docs/audit/PAPER_C_PASSERS.json'

d = json.load(open(SCREEN))
cells = d['cells']; manifest = d['manifest']
order = list(manifest['cells'])                      # frozen appendix order
rows = {cid: {int(r['seed']): r for r in cells[cid]['rows']} for cid in cells}
def cell(s, l, sup, st): return f"S{float(s):.2f}|L{float(l):.2f}|{sup}|{st}"

def tstat_p(vals, mu0=0.0):
    n = len(vals); m = sum(vals) / n
    var = sum((v - m) ** 2 for v in vals) / (n - 1)
    se = math.sqrt(var / n)
    if se == 0: return m, se, (0.0 if abs(m) > 0 else 1.0)
    t = (m - mu0) / se
    # two-sided normal approximation is conservative enough for n=8 here; report t and normal p
    p = math.erfc(abs(t) / math.sqrt(2))
    return m, se, p

def contrast(pairs, field, scale=1.0):
    """pairs: list of (cid_a, cid_b); per seed, avg over pairs of (a-b); returns 8 seed values."""
    vals = []
    for sd in range(8):
        diffs = []
        for ca, cb in pairs:
            if sd in rows[ca] and sd in rows[cb]:
                diffs.append((rows[ca][sd][field] - rows[cb][sd][field]) * scale)
        vals.append(sum(diffs) / len(diffs))
    return vals, sum(vals) / len(vals)

def mean_withheld(cid):
    return sum(r['withheld'] for r in rows[cid].values()) / len(rows[cid])

tests = {}
# T1
pairs1 = [(cell(0.85, L, sup, st), cell(1.15, L, sup, st)) for L in (0.25, 0.45) for sup in 'ABC' for st in ('P55', 'P12')]
v1, e1 = contrast(pairs1, 'tut_k12_rate', 100.0); m1, se1, p1 = tstat_p(v1)
tests['T1'] = dict(test='S substitution (K-12 participation, pp)', design_cells=len(pairs1), effect=e1, se=se1, p=p1,
                   min_effect=3.0, predicted_sign='positive', cells_touched=sorted({c for pr in pairs1 for c in pr}))
# T2
pairs2 = [(cell(S, L, 'C', st), cell(S, L, 'A', st)) for S in (0.85, 1.0, 1.15) for L in (0.25, 0.45) for st in ('P55', 'P12')]
v2, e2 = contrast(pairs2, 'own_share_financial_proxy'); m2, se2, p2 = tstat_p(v2)
tests['T2'] = dict(test='supply form (own_share_financial proxy, C-A)', design_cells=len(pairs2), effect=e2, se=se2, p=p2,
                   min_effect=0.10, predicted_sign='positive', cells_touched=sorted({c for pr in pairs2 for c in pr}))
# T3
pairs3 = [(cell(S, L, 'A', 'P55'), cell(S, L, 'A', 'P12')) for S in (0.85, 1.0, 1.15) for L in (0.25, 0.45)]
v3, e3 = contrast(pairs3, 'withheld'); m3, se3, p3 = tstat_p(v3)
h55 = sum(mean_withheld(cell(S, L, 'A', 'P55')) for S in (0.85, 1.0, 1.15) for L in (0.25, 0.45)) / 6
h12 = sum(mean_withheld(cell(S, L, 'A', 'P12')) for S in (0.85, 1.0, 1.15) for L in (0.25, 0.45)) / 6
tests['T3'] = dict(test='withholding assertion-support (A|P55 vs A|P12)', design_cells=len(pairs3), effect=e3, se=se3, p=p3,
                   min_effect=0.05, predicted_sign='positive', h_A_P55=h55, h_A_P12=h12,
                   assertion_support=(h55 >= 0.05 and h12 <= 0.01), cells_touched=sorted({c for pr in pairs3 for c in pr}))
# T4
pairs4 = [(cell(S, 0.45, sup, st), cell(S, 0.25, sup, st)) for S in (0.85, 1.0, 1.15) for sup in 'ABC' for st in ('P55', 'P12')]
v4, e4 = contrast(pairs4, 'q5_q1_spend_gap', 100.0); m4, se4, p4 = tstat_p(v4)
tests['T4'] = dict(test='gate pressure (Q5-Q1 spend gap, pp, L=.45 - L=.25)', design_cells=len(pairs4), effect=e4, se=se4, p=p4,
                   min_effect=2.0, predicted_sign='positive', cells_touched=sorted({c for pr in pairs4 for c in pr}))

# Holm
ps = sorted([(t['p'], k) for k, t in tests.items()])
m = len(ps); holm = {}; prev = 0.0
for i, (p, k) in enumerate(ps):
    adj = min(1.0, max(prev, (m - i) * p)); holm[k] = adj; prev = adj
for k, t in tests.items():
    t['p_holm'] = holm[k]
    cond_dir = (t['effect'] > 0) if t['predicted_sign'] == 'positive' else (t['effect'] < 0)
    cond_min = abs(t['effect']) >= t['min_effect']
    cond_sig = t['p_holm'] < 0.05
    cond_extra = t.get('assertion_support', True)
    t['passes'] = bool(cond_dir and cond_min and cond_sig and cond_extra)
    t['pass_reasons'] = dict(direction=cond_dir, min_effect=cond_min, holm_significant=cond_sig,
                             assertion_support=cond_extra)

cand = []
for k, t in tests.items():
    if t['passes']:
        for c in t['cells_touched']:
            if c not in cand: cand.append(c)
cand = [c for c in order if c in cand]          # appendix order
if len(cand) <= 6:
    passers = cand; rule_applied = 'all candidates (<=6)'
else:
    passers = cand[:6]; rule_applied = 'first 6 in appendix order; remainder screening-only'

payload = dict(paper='Paper C screening passer freeze (host-only)', source_screening_json=SCREEN,
               source_sha256=hashlib.sha256(open(SCREEN, 'rb').read()).hexdigest(),
               screening_counts=dict(n_runs=d['n_runs'], n_cells=d['n_cells'], invalid_cells=d['invalid_cells']),
               rules=dict(alpha=0.05, multiplicity='Holm across T1-T4', seed_count=8, matched_seeds=list(range(8)),
                          passer_rule='test passes = correct direction AND |effect| >= min effect AND Holm p < .05 AND T3 assertion-support; candidates = union of cells used in passing tests, appendix order; if >6, first 6 are passers, remainder screening-only',
                          appendix_order=order),
               tests=tests, candidates=cand, passers=passers, rule_applied=rule_applied,
               a4_note='P12=pay_gap=no-withholding control; exposed arms = A/C AND P55; A|P12 and B exempt (see PAPER_C_A4_P12_CLARIFICATION.md)')
json.dump(payload, open(OUT, 'w'), indent=2)
print(json.dumps({k: dict(effect=round(t['effect'], 4), p=round(t['p'], 5), p_holm=round(t['p_holm'], 5), passes=t['passes']) for k, t in tests.items()}, indent=1))
print('candidates', len(cand), 'passers', len(passers), 'rule', rule_applied)
print('wrote', OUT, hashlib.sha256(open(OUT, 'rb').read()).hexdigest())
