#!/usr/bin/env python3
"""Turn rigor-family trial records into tables and verdicts against criteria declared in protocols_rigor.json.

    python research/rigor/analyze.py --run research/runs/rigor-main [--run research/runs/mechanism-pilot ...]

Writes ANALYSIS_RIGOR.md and analysis_rigor.json into the first --run directory. Reads only trial records whose
plan_digest matches their run's plan. Works on partial runs (reports n). Also analyses the `schools` family of the
original runner when a run containing it is passed (benchmark comparison with Diebold-Mariano tests).

Verdict words are fixed in advance (protocols_rigor.json, "criteria"); this script applies them mechanically.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(ROOT / 'engine'))
from rigor.stats import abc_recovery, diebold_mariano, paired_summary  # noqa: E402

CRIT = json.loads((HERE / 'protocols_rigor.json').read_text())['criteria']


def load(run):
    run = Path(run)
    plan = json.loads((run / 'plan.json').read_text())
    recs = []
    for t in plan['tasks']:
        p = run / 'trials' / f"{t['id']}.json"
        if p.exists():
            r = json.loads(p.read_text())
            if r['plan_digest'] == plan['plan_digest'] and r['status'] == 'ok':
                recs.append(r)
    return recs


def fmt(x, d=3):
    return '—' if x is None or (isinstance(x, float) and not np.isfinite(x)) else (f'{x:.{d}f}' if isinstance(x, float) else str(x))


def confusion_md(res):
    labs = res['labels']
    L = ['| true \\ predicted | ' + ' | '.join(labs) + ' | recall |', '|---' * (len(labs) + 2) + '|']
    for i, a in enumerate(labs):
        row = res['confusion'][i]
        L.append(f'| {a} | ' + ' | '.join(str(v) for v in row) + f" | {fmt(res['per_true_recall'][a], 2)} |")
    return L


def recovery_verdict(res):
    c = CRIT['recovery']
    if res['accuracy'] is None or res['n_pseudo_observed'] < c['min_pseudo_observed']:
        return 'too few pseudo-observations'
    rec = [v for v in res['per_true_recall'].values() if v is not None]
    if res['accuracy'] >= c['discriminates_accuracy'] and min(rec) >= c['discriminates_min_recall']:
        return 'DISCRIMINATES'
    if res['accuracy'] < c['fails_accuracy']:
        return 'DOES NOT DISCRIMINATE'
    return 'PARTIAL'


# ------------------------------------------------------------------ credential recovery
def credential(recs, out):
    import relfloor_gate as G
    rows, labels, liq, perr = [], [], [], []
    for r in recs:
        if r['task']['family'] != 'credential_recovery':
            continue
        tb = r['result']['table']; s = r['task']['settings']
        rows += tb['rows']; perr += tb['profile_error']
        labels += [s['structure']] * len(tb['rows']); liq += [s['liquidity']] * len(tb['rows'])
    if not rows:
        return []
    X = np.array(rows, float); labels = np.array(labels); liq = np.array(liq); perr = np.array(perr)
    names = list(G.SUMMARY_NAMES)
    L = ['## Credential floor: can any study design tell the structures apart?', '',
         'Reference table: prior-predictive simulations of HC, POS, REL and GATE (eligibility gate). Each simulation in '
         'turn plays the observed data, with the declared survey and quasi-experiment errors added '
         '(`engine/relfloor_gate.py: NOISE`); its nearest neighbours vote. "Near data" restricts the pseudo-observed '
         'rows to simulations whose 2014 and 2021 quintile profiles are within the stated distance of UIS CR.2.', '']
    counts = {f'{s}/{l}': int(((labels == s) & (liq == l)).sum()) for s in G.STRUCTS for l in ('graded', 'hard')}
    near = {f'{s}/{l}': int(((labels == s) & (liq == l) & (perr <= .15)).sum()) for s in G.STRUCTS for l in ('graded', 'hard')}
    L += [f'Simulations by structure/financing: {counts}', f'Within 15 points of both profiles: {near}', '']
    out['credential'] = {'counts': counts, 'near15': near, 'designs': {}}
    for lq in ('graded', 'hard'):
        sel = liq == lq
        for dname, cols in G.DESIGNS.items():
            ci = [names.index(c) for c in cols]
            noise = [G.NOISE[c] for c in cols]
            for tag, mask in (('all prior draws', np.ones(sel.sum(), bool)), ('near data (<=15 pts)', perr[sel] <= .15)):
                res = abc_recovery(X[sel][:, ci], labels[sel], noise, mask_obs=mask, rng=np.random.default_rng(1))
                v = recovery_verdict(res)
                out['credential']['designs'][f'{lq}|{dname}|{tag}'] = dict(res, verdict=v)
                L += [f'### {lq} financing · {dname} · {tag}: accuracy {fmt(res["accuracy"], 2)} '
                      f'(chance {res["chance"]:.2f}, n={res["n_pseudo_observed"]}) → **{v}**', '']
                L += confusion_md(res) + ['']
    return L


# ------------------------------------------------------------------ shadow recovery
SHADOW_NOISE = {  # declared observation-error SDs (ASSUMED; see protocols_rigor.json)
    'participation': .015, 'participation_g9': .02, 'participation_g12': .02, 'urban_rural_gap': .02,
    'source_own_provider_share': .03, 'source_other_provider_share': .03, 'teacher_tutor_share': .10,
    'instr_gap_tutoring_teacher': .03, 'buy_gap_tutoring_teacher': .03, 'other_gap_tutoring_teacher': .03,
    'coverage_gap_q5_q1': .03, 'ban_effect_participation': .03, 'ban_effect_class_instruction': .02,
    'extra_time_effect_participation': .03}
PUBLISHED = list(SHADOW_NOISE)[:7]
SHADOW_DESIGNS = {
    'S0_published_patterns': PUBLISHED,
    'S1_plus_classroom_instruction': PUBLISHED + ['instr_gap_tutoring_teacher'],
    'S2_plus_purchase_by_teacher_status': PUBLISHED + ['buy_gap_tutoring_teacher', 'other_gap_tutoring_teacher'],
    'S3_plus_coverage_by_wealth': PUBLISHED + ['coverage_gap_q5_q1'],
    'S4_plus_policy_response': PUBLISHED + ['ban_effect_participation', 'ban_effect_class_instruction',
                                            'extra_time_effect_participation'],
    'S5_all_field_observations': list(SHADOW_NOISE),
}


def shadow(recs, out):
    rows, labels, z = [], [], []
    names = None
    for r in recs:
        if r['task']['family'] != 'shadow_recovery':
            continue
        tb = r['result']['table']; names = tb['names']
        rows += [[np.nan if v is None else v for v in row] for row in tb['rows']]
        z += [np.inf if v is None else v for v in tb['max_z']]
        labels += [r['task']['settings']['variant']] * len(tb['rows'])
    if not rows:
        return []
    X = np.array(rows, float); labels = np.array(labels); z = np.array(z)
    L = ['## Shadow education: which field observation would separate the explanations?', '',
         'Reference table: prior draws of each variant (thin, diversion, favour; full shown separately). Published '
         'patterns use the corrected pupil-level observation equation. Candidate observations: instruction delivered '
         'by tutoring vs non-tutoring teachers, purchase rates by teacher status, coverage by wealth, and responses to '
         'a ban and to added class time. Error SDs are declared in this script and the protocol.', '',
         f'Draws by variant: { {str(v): int((labels == v).sum()) for v in sorted(set(labels))} }; '
         f'within max-z 3 of the published patterns: { {str(v): int(((labels == v) & (z <= 3)).sum()) for v in sorted(set(labels))} }', '']
    out['shadow'] = {}
    for scope, keep in (('three rivals', labels != 'full'), ('four variants', np.ones(len(labels), bool))):
        for dname, cols in SHADOW_DESIGNS.items():
            ci = [names.index(c) for c in cols]
            for tag, mask in (('all prior draws', None), ('near data (max z <= 3)', z[keep] <= 3)):
                res = abc_recovery(X[keep][:, ci], labels[keep], [SHADOW_NOISE[c] for c in cols], mask_obs=mask,
                                   rng=np.random.default_rng(2))
                v = recovery_verdict(res)
                out['shadow'][f'{scope}|{dname}|{tag}'] = dict(res, verdict=v)
                L += [f'### {scope} · {dname} · {tag}: accuracy {fmt(res["accuracy"], 2)} '
                      f'(chance {res["chance"]:.2f}, n={res["n_pseudo_observed"]}) → **{v}**', '']
                L += confusion_md(res) + ['']
    return L


# ------------------------------------------------------------------ youth placebo
def youth_placebo(recs, out):
    best = {}
    for r in recs:
        if r['task']['family'] != 'youth_placebo':
            continue
        d = r['result']['date']; key = 'none' if d is None else f'{d[0]}-{d[1]:02d}'
        m = r['result']['metrics']
        if key not in best or m['cost'] < best[key]['cost']:
            best[key] = dict(m, n_pairs=None)
    if not best:
        return []
    c_star = min(v['cost'] for k, v in best.items() if k != 'none')
    aug = best.get('2021-08')
    n = 98   # observation pairs in the full window (calibrate_china.pairs_for)
    sigma2 = 2 * c_star / n
    lr = {k: 2 * (v['cost'] - c_star) / sigma2 for k, v in best.items()}
    dates = sorted(k for k in best if k != 'none')
    rank = sorted(dates, key=lambda k: best[k]['cost']).index('2021-08') + 1 if aug else None
    indist = [k for k in dates if lr[k] < CRIT['placebo']['lr_threshold'] and k != '2021-08']
    share = len(indist) / max(len(dates) - 1, 1)
    verdict = ('AUG-2021 NOT SINGLED OUT' if share >= CRIT['placebo']['not_identified_share']
               else 'AUG-2021 SINGLED OUT' if rank == 1 else 'MIXED')
    out['youth_placebo'] = dict(best=best, lr=lr, rank_aug2021=rank, n_dates=len(dates), indistinguishable=indist,
                                share_indistinguishable=share, verdict=verdict)
    L = ['## China youth: is the August-2021 step special? (placebo in time)', '',
         f'Best cost over restarts for each step month; LR ≈ 2Δcost/σ̂² with σ̂² from the best placebo fit '
         f'(iid Gaussian approximation; residual autocorrelation makes it optimistic). August 2021 ranks '
         f'**{rank} of {len(dates)}**; {len(indist)} other months ({share:.0%}) fit within LR < '
         f"{CRIT['placebo']['lr_threshold']}. No-step cost {fmt(best.get('none', {}).get('cost'), 1)}. → **{verdict}**", '',
         '| Step month | Cost | LR vs best | Fitted step | Rise (pp) |', '|---|---:|---:|---:|---:|']
    for k in ['none'] + sorted(dates, key=lambda k: best[k]['cost']):
        v = best[k]
        L.append(f"| {k} | {v['cost']:.1f} | {lr[k]:.1f} | {fmt(v.get('dr_drop'))} | {fmt(v.get('rise_pp'), 2)} |")
    return L + ['']


# ------------------------------------------------------------------ youth rolling
def youth_rolling(recs, out):
    best = {}
    for r in recs:
        if r['task']['family'] != 'youth_rolling':
            continue
        o = tuple(r['result']['origin']); m = r['result']['metrics']
        if o not in best or m['train_mae'] < best[o]['result']['metrics']['train_mae']:
            best[o] = r
    if not best:
        return []
    errs = [e for r in best.values() for e in r['result']['errors']]
    hmax = max(e['h'] for e in errs)
    L = ['## China youth: rolling-origin forecasts within the old NBS definition', '',
         f"Origins: {sorted(best)}; forecasts to June 2023; restart with the lowest training error kept per origin. "
         'Diebold–Mariano with the Harvey–Leybourne–Newbold correction; long-run variance with h_max−1 lags because '
         'forecasts from different origins overlap. Negative DM = model more accurate.', '',
         '| Benchmark | MAE model | MAE benchmark | DM stat | p | n | verdict |', '|---|---:|---:|---:|---:|---:|---|']
    out['youth_rolling'] = {}
    model = np.array([e['model'] for e in errs])
    for b in ('random_walk', 'seasonal_naive', 'lake'):
        bench = np.array([e[b] for e in errs])
        dm = diebold_mariano(model, bench, h=hmax)
        ok = np.isfinite(model) & np.isfinite(bench)
        a, c = float(np.mean(np.abs(model[ok]))), float(np.mean(np.abs(bench[ok])))
        p = dm['p_two_sided']
        verdict = ('model better' if p is not None and p < .05 and dm['stat'] < 0 else
                   'model worse' if p is not None and p < .05 and dm['stat'] > 0 else 'no detectable difference')
        out['youth_rolling'][b] = dict(dm, mae_model=a, mae_bench=c, verdict=verdict)
        L.append(f"| {b} | {a:.2f} | {c:.2f} | {fmt(dm['stat'], 2)} | {fmt(p, 3)} | {dm['n']} | {verdict} |")
    L += ['', '| Horizon (months) | n | MAE model | MAE random walk | MAE seasonal naive | MAE lake |', '|---|---:|---:|---:|---:|---:|']
    for lo, hi in ((1, 3), (4, 6), (7, 12), (13, 36)):
        sub = [e for e in errs if lo <= e['h'] <= hi]
        if sub:
            g = lambda k: np.nanmean(np.abs([e[k] for e in sub]))
            L.append(f'| {lo}–{hi} | {len(sub)} | {g("model"):.2f} | {g("random_walk"):.2f} | {g("seasonal_naive"):.2f} | {g("lake"):.2f} |')
    return L + ['']


# ------------------------------------------------------------------ fertility
def fertility(recs, out):
    rs = [r for r in recs if r['task']['family'] == 'fertility_placebo']
    if not rs:
        return []
    L = ['## Fertility: are the levels fits stronger than trending alone?', '',
         'Random-walk null: independent Gaussian random walks with each covariate\'s own drift and volatility '
         '(Granger & Newbold 1974). Swap: the same regression on each of the other five places\' covariate.', '']
    out['fertility'] = {}
    for r in rs:
        m = r['result']['metrics']; start = r['task']['settings']['start']
        L += [f'### Sample from {start}', '', '| Place / covariate | R² | Share of random walks with R² ≥ observed | '
              'RW null 95th pct | Max R² with another place\'s covariate | verdict |', '|---|---:|---:|---:|---:|---|']
        keys = sorted({k.rsplit('/', 1)[0] for k in m})
        for k in keys:
            share = m[k + '/rw_null_share_r2_ge_obs']; swap = m[k + '/swap_max_r2']; r2 = m[k + '/r2']
            v = ('NOT DISTINGUISHABLE FROM TRENDING' if share >= CRIT['fertility']['null_share'] or swap >= r2
                 else 'stronger than trending benchmarks')
            out['fertility'][f'{start}|{k}'] = dict(r2=r2, rw_share=share, swap_max=swap, verdict=v)
            L.append(f"| {k} | {r2:.2f} | {share:.2f} | {m[k + '/rw_null_r2_p95']:.2f} | {swap:.2f} | {v} |")
        L.append('')
    return L


# ------------------------------------------------------------------ Cambodia external check
def camchild(recs, out):
    rs = [r for r in recs if r['task']['family'] == 'camchild_validation']
    if not rs:
        return []
    c = CRIT['camchild_filmer_schady']
    L = ['## Cambodia: does the cash lever reproduce the CESSP scholarship result?', '',
         f"Target (Filmer & Schady 2011; **verify against the paper's tables**): effect on attendance in "
         f"[{c['effect_lo']:.2f}, {c['effect_hi']:.2f}]; US$60 minus US$45 no larger than {c['dose_diff_max']:.2f}. "
         'Eligible group: bottom two quintiles aged 12–13, first simulated year, paired seeds. W (adult informal annual '
         'wage, US$) drawn from the declared range.', '',
         '| Baseline setting | n trials | baseline attendance | effect $45 [95% CI] | effect $60 | $60 − $45 [95% CI] | verdict |',
         '|---|---:|---:|---|---:|---|---|']
    out['camchild'] = {}
    for cell in sorted({r['task']['cell'] for r in rs}):
        sub = [r['result']['metrics'] for r in rs if r['task']['cell'] == cell]
        e45 = paired_summary([m['effect_attend_45'] for m in sub])
        e60 = paired_summary([m['effect_attend_60'] for m in sub])
        dd = paired_summary([m['effect_diff_60_minus_45'] for m in sub])
        base = float(np.mean([m['baseline_attend_eligible'] for m in sub]))
        ok_level = e45.get('ci95') and c['effect_lo'] <= e45['mean'] <= c['effect_hi']
        ok_dose = dd.get('mean') is not None and dd['mean'] <= c['dose_diff_max']
        v = 'CONSISTENT' if ok_level and ok_dose else ('LEVEL TOO LARGE' if e45.get('mean', 0) > c['effect_hi']
             else 'LEVEL TOO SMALL' if e45.get('mean', 1) < c['effect_lo'] else 'DOSE RESPONSE TOO STEEP')
        out['camchild'][cell] = dict(baseline=base, effect45=e45, effect60=e60, diff=dd, verdict=v)
        ci = lambda s: f"{fmt(s.get('mean'))} [{fmt(s['ci95'][0])}, {fmt(s['ci95'][1])}]" if s.get('ci95') else fmt(s.get('mean'))
        L.append(f"| {cell} | {len(sub)} | {base:.2f} | {ci(e45)} | {fmt(e60.get('mean'))} | {ci(dd)} | {v} |")
    return L + ['', 'CIs are Monte Carlo intervals over nuisance draws and seeds, not real-world sampling intervals.', '']


# ------------------------------------------------------------------ schools (original runner's family)
def schools(recs, out):
    rs = [r for r in recs if r['task']['family'] == 'schools']
    if not rs:
        return []
    bt = rs[0]['result']['backtests']
    L = ['## School futures: model against the flat (persistence) benchmark', '',
         f"Rows with fewer than {CRIT['schools']['min_n']} forecasts are anecdotal and get no verdict. "
         'DM uses h = 1 lag structure within each series (rows are not all one-step; treat p as indicative).', '',
         '| Series / metric | n | MAE model | MAE flat | ratio | DM stat | p | verdict |', '|---|---:|---:|---:|---:|---:|---:|---|']
    out['schools'] = {}
    for series, rows in sorted(bt.items()):
        groups = {}
        for x in rows:
            groups.setdefault(x['metric'], []).append(x)
        for metric, g in sorted(groups.items()):
            e1 = np.array([x['model'] - x['actual'] for x in g], float)
            e2 = np.array([x['naive'] - x['actual'] for x in g], float)
            n = len(g)
            a, b = float(np.mean(np.abs(e1))), float(np.mean(np.abs(e2)))
            hmax = max([x['year'] - x['origin'] for x in g if 'origin' in x] or [1])
            dm = diebold_mariano(e1, e2, h=hmax) if n >= 3 else dict(stat=None, p_two_sided=None)
            if n < CRIT['schools']['min_n']:
                v = 'anecdotal (n too small)'
            elif dm['p_two_sided'] is not None and dm['p_two_sided'] < .05:
                v = 'beats benchmark' if dm['stat'] < 0 else 'loses to benchmark'
            else:
                v = 'no detectable difference'
            out['schools'][f'{series}|{metric}'] = dict(n=n, mae=a, bench=b, dm=dm, verdict=v)
            L.append(f"| {series} / {metric} | {n} | {a:.4g} | {b:.4g} | {a / b if b else float('nan'):.2f} | "
                     f"{fmt(dm.get('stat'), 2)} | {fmt(dm.get('p_two_sided'), 3)} | {v} |")
    L += ['', 'Check before citing: whether any `model` forecast uses information dated after its `origin` '
          '(some rows carry a separate `conditional` field). A forecast that conditions on realised entry is a '
          'reconstruction, not a forecast.', '']
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', action='append', required=True)
    a = ap.parse_args()
    recs = [r for run in a.run for r in load(run)]
    out = {'runs': a.run, 'n_records': len(recs)}
    L = ['# Rigor analysis', '', f'Runs: {a.run}. Successful trial records read: {len(recs)}.', '',
         'Verdict words and thresholds are fixed in `research/rigor/protocols_rigor.json` before any run. All empirical '
         'targets were previously inspected; none of this is a prospective test.', '']
    for f in (credential, shadow, youth_placebo, youth_rolling, fertility, camchild, schools):
        L += f(recs, out)
    first = Path(a.run[0])
    (first / 'ANALYSIS_RIGOR.md').write_text('\n'.join(L) + '\n')
    (first / 'analysis_rigor.json').write_text(json.dumps(out, indent=1, default=float))
    print('\n'.join(L))


if __name__ == '__main__':
    main()
