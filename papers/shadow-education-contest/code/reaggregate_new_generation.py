#!/usr/bin/env python3
"""Re-aggregate the NEW-GENERATION Paper B JSONs from existing per-seed checkpoints (no re-run).

Fixes: (i) HK primary jobs are keyed ('HK', arm, 'PRIMARY') — the original aggregator looked up 'TRACKED' for HK and
produced empty HK summaries; (ii) total_runs for TRACKED = HK 900 + KR-TRACKED 900 = 1,800 (SINGLE = 900);
(iii) engine label stays 98baf6b (pre-re-pin; numerics unchanged vs 846c9e0). Emits the same two JSON schemas + provenance.
"""
import hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_new_generation as R

RES = sys.argv[1] if len(sys.argv) > 1 else '/root/work/newgen/results'
SPEC = R.SPEC
spec = json.load(open(SPEC))
jobs = [('HK', a, 'PRIMARY') for a in R.ARMS] + [('KR', a, 'TRACKED') for a in R.ARMS] + [('KR', a, 'SINGLE') for a in R.ARMS]
rows = {}
for (jur, arm, var) in jobs:
    tag = f'{jur}_{arm}_{var}'; p = os.path.join(RES, f'ckpt_{tag}.jsonl')
    if not os.path.exists(p): continue
    rows[(jur, arm, var)] = [json.loads(l) for l in open(p)]
print('checkpoint rows:', {f'{j}/{a}/{v}': len(r) for (j, a, v), r in rows.items()})

def stat(v):
    import numpy as np
    a = np.array(v, float); n = len(a); m = float(np.nanmean(a)); sd = float(np.nanstd(a, ddof=1)) if n > 1 else 0.0
    se = sd / np.sqrt(max(n, 1))
    return dict(mean=m, sd=sd, ci95_lo=m - 1.96 * se, ci95_hi=m + 1.96 * se, n=n)

metrics = ['k12_spend', 'k12_rate_pct', 'g12_pct', 'q5_q1_gap_pp', 'q5_q1_spend_ratio', 'elite_q5_share_pct', 'contest_e_mean']
outs = {}
for variant, outfile in (('TRACKED', 'paperB_new_generation_TRACKED.json'), ('SINGLE', 'paperB_new_generation_SINGLE_KR.json')):
    summary = {'HK': {}, 'KR': {}}
    for jur in summary:
        if variant == 'SINGLE' and jur == 'HK': continue
        base_key = ('HK', 'Baseline', 'PRIMARY') if jur == 'HK' else ('KR', 'Baseline', variant)
        base = {r['seed']: r for r in rows.get(base_key, [])}
        if not base: continue
        base_mean_spend = float(sum(r['k12_spend'] for r in base.values()) / len(base))
        for arm in R.ARMS:
            key = (jur, arm, 'PRIMARY') if jur == 'HK' else (jur, arm, variant)
            rr = rows.get(key, [])
            if not rr: continue
            e = {m: stat([r[m] for r in rr]) for m in metrics}
            si = [100.0 * r['k12_spend'] / base[r['seed']]['k12_spend'] for r in rr if r['seed'] in base]
            e['total_spend_index'] = round(100.0 * (sum(r['k12_spend'] for r in rr) / len(rr)) / base_mean_spend, 2)
            e['total_spend_index_seed_stats'] = stat(si)
            e['delta_vs_baseline'] = {m: stat([r[m] - base[r['seed']][m] for r in rr if r['seed'] in base]) for m in metrics}
            summary[jur][arm] = e
    payload = dict(label=R.LABEL,
                   metadata=dict(generation='NEW GENERATION', spec='docs/audit/canonical_spec.json',
                                 spec_content_sha256=spec['frozen_files_sha256']['canonical_spec_content_sha256'],
                                 engine_commit='98baf6b (pre-re-pin; numerics unchanged vs 846c9e0 — engine-core 118-series identical)',
                                 engine_files=spec['engine_file_sha256'], runner_sha256=R.sha(os.path.abspath(__file__)),
                                 gate_variant=('KR-TRACKED primary' if variant == 'TRACKED' else 'KR-SINGLE sensitivity (KR only)'),
                                 seeds=list(range(100)), n_seeds=100,
                                 total_runs=(sum(len(rows.get((j, a, 'PRIMARY' if j == 'HK' else 'TRACKED'), [])) for j in ('HK', 'KR') for a in R.ARMS)
                                             if variant == 'TRACKED' else sum(len(rows.get(('KR', a, 'SINGLE'), [])) for a in R.ARMS)),
                                 workers=8, elapsed_seconds=11234.49,
                                 env='py3.10.8 numpy2.2.6 scipy1.15.3; OPENBLAS/MKL/OMP=1; nice -n 10',
                                 preregistration='docs/audit/GATE2_PREREGISTRATION.md',
                                 note='NEW GENERATION — not a reproduction of the Gemini 420/540 docx tables; re-aggregated from intact per-seed checkpoints (HK key fix), no re-run'),
                   summary=summary)
    path = os.path.join(RES, outfile); json.dump(payload, open(path, 'w'), indent=2)
    outs[outfile] = dict(path=path, sha256=R.sha(path)); print('wrote', path, outs[outfile]['sha256'])
prov = dict(label=R.LABEL, wall_seconds=11234.49, workers=8, seeds=list(range(100)), jobs=[list(j) for j in jobs],
            outputs=outs, engine_files=spec['engine_file_sha256'], spec_sha256=R.sha(SPEC),
            runner_sha256=R.sha(os.path.abspath(__file__)), reaggregated=True,
            note='HK aggregation key fix; no model re-run; engine pin 98baf6b (pre-re-pin)')
json.dump(prov, open(os.path.join(RES, 'new_generation_provenance.json'), 'w'), indent=2)
print('provenance', R.sha(os.path.join(RES, 'new_generation_provenance.json')))
