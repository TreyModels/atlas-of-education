#!/usr/bin/env python3
"""NEW-GENERATION runner (frozen V540-FREEZE spec + explicit GATE_SPECS) — Paper B arm sweep.

Pre-registration: docs/audit/GATE2_PREREGISTRATION.md. Label: NEW GENERATION — REPRODUCED SIMULATION (repaired
engine, frozen spec). NOT a reproduction of the Gemini-era 420/540 docx tables.

Design: 18 arms x {HK,KR} x N matched seeds (default 100) for KR-TRACKED primary; plus KR-SINGLE sensitivity
(9 KR arms x N). Arm-level subprocesses with per-seed checkpointing (atomic JSONL, resumable), no ProcessPool
completion phase. Every output records spec/engine/runner hashes, seed list, wall, workers.

Usage:
  python run_new_generation.py driver [--seeds 0-99] [--workers 8] [--out-dir DIR]
  (arm mode is internal: `arm <jur> <arm_id> <gate_variant> <seeds_spec> <out_dir>`)
"""
import argparse, hashlib, json, os, subprocess, sys, time, warnings

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ENGINE = os.path.join(REPO, 'engine')
SPEC = os.path.join(REPO, 'docs', 'audit', 'canonical_spec.json')
LABEL = ("NEW GENERATION — REPRODUCED SIMULATION (repaired engine, frozen V540-FREEZE spec); "
         "NOT a reproduction of the Gemini-era 420/540 docx tables")

ARMS = ["Baseline", "CF1a", "CF1b", "CF2a", "CF2b", "CF3a", "CF3b", "CF4a", "CF4b"]
S_MOD = {"HK": 0.28, "KR": 0.16}
S_MAJ = {"HK": 0.50, "KR": 0.40}

def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

def _deepcopy(x):
    return json.loads(json.dumps(x))

def arm_params(spec, jur, arm_id, gate_variant):
    """Frozen spec params + pre-declared arm transformation. gate_variant: 'TRACKED'|'SINGLE' (KR only)."""
    jur_block = spec['params'][jur]
    if jur == 'KR' and gate_variant == 'SINGLE':
        base = _deepcopy(jur_block['sensitivity'])
    else:
        base = _deepcopy(jur_block['primary'])
    p = dict(base)
    if arm_id == 'Baseline':
        return p
    if arm_id == 'CF1a':
        p['contest_price'] = float(p['contest_price']) * 1.5
    elif arm_id == 'CF1b':
        p['contest_max_e'] = float(p['contest_max_e']) * 0.5
    elif arm_id in ('CF2a', 'CF2b'):
        p['gates'][2]['share'] = S_MOD[jur] if arm_id == 'CF2a' else S_MAJ[jur]
    elif arm_id in ('CF3a', 'CF3b', 'CF4a', 'CF4b'):
        mult = 0.70 if arm_id == 'CF3a' else 0.50
        p['elite_logw'] = float(p['elite_logw']) * mult
        for g in p['gates']:
            if 'elite_logw' in g:
                g['elite_logw'] = float(g['elite_logw']) * mult
            if 'track_prize' in g:
                g['track_prize']['earnings_logw'] = float(g['track_prize']['earnings_logw']) * mult
        if arm_id == 'CF4a':
            p['contest_max_e'] = float(p['contest_max_e']) * 0.5
        if arm_id == 'CF4b':
            p['gates'][2]['share'] = S_MAJ[jur]
    else:
        raise ValueError(arm_id)
    return p

def seed_row(jur, arm_id, seed, row):
    row.update(jurisdiction=jur, arm_id=arm_id, seed=seed)
    return row

def run_arm(jur, arm_id, gate_variant, seeds, out_dir):
    """Internal arm worker: sequential seeds, per-seed checkpoint JSONL, resume by skipping completed seeds."""
    warnings.filterwarnings('ignore')
    os.makedirs(out_dir, exist_ok=True)
    sys.path.insert(0, ENGINE)
    import numpy as np
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket
    spec = json.load(open(SPEC))
    params = arm_params(spec, jur, arm_id, gate_variant)
    tag = f"{jur}_{arm_id}_{gate_variant}"
    ckpt = os.path.join(out_dir, f"ckpt_{tag}.jsonl")
    done = set()
    if os.path.exists(ckpt):
        for line in open(ckpt):
            try: done.add(int(json.loads(line)['seed']))
            except Exception: pass
    def sim(seed):
        mods = [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]
        E = Engine(mods, **dict(params, seed=seed)); E.run()
        m = E.p['measure_from']; R = E.R
        rq = np.mean(np.array(R['tut_k12_rate_by_q'][m:], float), 0)
        sq = np.mean(np.array(R['tut_k12_spend_by_q'][m:], float), 0)
        X = E.ALL
        sel = (X['cohort'] >= m) & (X['cohort'] <= E.p['T'] - 14) & (X['g'] >= 12)
        el = X['elite'][sel]; qq = X['q'][sel]
        return dict(
            k12_spend=float(np.mean(R['tut_k12_spend'][m:])),
            k12_rate_pct=100.0 * float(np.mean(R['tut_k12_rate'][m:])),
            g12_pct=100.0 * float(np.mean(R['tut_g12_rate'][m:])),
            q5_q1_gap_pp=100.0 * float(rq[4] - rq[0]),
            q5_q1_spend_ratio=float(sq[4] / max(sq[0], 1e-9)),
            elite_q5_share_pct=(100.0 * float(np.mean(qq[el] == 4))) if el.any() else float('nan'),
            contest_e_mean=float(np.mean(R['contest_e_mean'][m:])),
            k12_rate_by_q=[float(100.0 * v) for v in rq],
            k12_spend_by_q=[float(v) for v in sq])
    for sd in seeds:
        if sd in done: continue
        row = seed_row(jur, arm_id, sd, sim(sd))
        with open(ckpt, 'a') as f:
            f.write(json.dumps(row) + "\n"); f.flush(); os.fsync(f.fileno())
    return tag

def _stats(vals):
    import numpy as np
    a = np.array(vals, float); n = len(a)
    mean = float(np.nanmean(a)); sd = float(np.nanstd(a, ddof=1)) if n > 1 else 0.0
    se = sd / np.sqrt(max(n, 1))
    return dict(mean=mean, sd=sd, ci95_lo=mean - 1.96 * se, ci95_hi=mean + 1.96 * se, n=n)

def driver(seeds, workers, out_dir):
    from concurrent.futures import ThreadPoolExecutor
    os.makedirs(out_dir, exist_ok=True)
    spec = json.load(open(SPEC))
    jobs = [('HK', a, 'PRIMARY') for a in ARMS] + [('KR', a, 'TRACKED') for a in ARMS]
    jobs += [('KR', a, 'SINGLE') for a in ARMS]
    t0 = time.time()
    def launch(job):
        jur, arm_id, gate_variant = job
        r = subprocess.run([sys.executable, os.path.abspath(__file__), 'arm', jur, arm_id, gate_variant,
                            seeds_spec(seeds), out_dir], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=ENGINE, OPENBLAS_NUM_THREADS='1',
                                    MKL_NUM_THREADS='1', OMP_NUM_THREADS='1'))
        if r.returncode != 0:
            raise RuntimeError(f"arm {jur}/{arm_id}/{gate_variant} failed (rc={r.returncode}): {r.stderr[-1200:]}")
        return job
    with ThreadPoolExecutor(max_workers=workers) as ex:
        done = list(ex.map(launch, jobs))
    wall = time.time() - t0
    # aggregate
    from collections import defaultdict
    rows = defaultdict(list)
    for jur, arm_id, gate_variant in jobs:
        tag = f"{jur}_{arm_id}_{gate_variant}"
        for line in open(os.path.join(out_dir, f"ckpt_{tag}.jsonl")):
            rows[(jur, arm_id, gate_variant)].append(json.loads(line))
    metrics = ['k12_spend', 'k12_rate_pct', 'g12_pct', 'q5_q1_gap_pp', 'q5_q1_spend_ratio',
               'elite_q5_share_pct', 'contest_e_mean']
    outs = {}
    for variant, outfile in (('TRACKED', 'paperB_new_generation_TRACKED.json'),
                             ('SINGLE', 'paperB_new_generation_SINGLE_KR.json')):
        summary = {"HK": {}, "KR": {}}
        for jur in summary:
            base_key = ('HK', 'Baseline', 'PRIMARY') if jur == 'HK' else ('KR', 'Baseline', variant)
            base = {r['seed']: r for r in rows.get(base_key, [])}
            if variant == 'SINGLE' and jur == 'HK':
                continue
            base_mean_spend = float(sum(r['k12_spend'] for r in base.values()) / max(len(base), 1))
            for arm_id in ARMS:
                key = (jur, arm_id, 'PRIMARY') if jur == 'HK' else (jur, arm_id, variant)
                rr = rows.get(key, [])
                if not rr: continue
                entry = {m: _stats([r[m] for r in rr]) for m in metrics}
                spend_idx = [100.0 * r['k12_spend'] / base[r['seed']]['k12_spend'] for r in rr if r['seed'] in base]
                entry['total_spend_index'] = round(100.0 * (sum(r['k12_spend'] for r in rr) / len(rr)) / base_mean_spend, 2)
                entry['total_spend_index_seed_stats'] = _stats(spend_idx)
                entry['delta_vs_baseline'] = {m: _stats([r[m] - base[r['seed']][m] for r in rr if r['seed'] in base])
                                              for m in metrics}
                summary[jur][arm_id] = entry
        payload = dict(
            label=LABEL,
            metadata=dict(
                generation='NEW GENERATION', spec='docs/audit/canonical_spec.json',
                spec_content_sha256=spec['frozen_files_sha256']['canonical_spec_content_sha256'],
                engine_commit='98baf6b (pre-re-pin; numerics unchanged vs 846c9e0 — engine-core 118-series identical)',
                engine_files=spec['engine_file_sha256'],
                runner_sha256=sha(os.path.abspath(__file__)),
                gate_variant=('KR-TRACKED primary' if variant == 'TRACKED' else 'KR-SINGLE sensitivity (KR only)'),
                seeds=list(seeds), n_seeds=len(seeds), total_runs=sum(len(v) for v in rows.values()) if variant == 'TRACKED' else len(rows[('KR', 'Baseline', 'SINGLE')]) * 9,
                workers=workers, elapsed_seconds=round(wall, 2),
                env='py3.10.8 numpy2.2.6 scipy1.15.3; OPENBLAS/MKL/OMP=1; nice -n 10',
                preregistration='docs/audit/GATE2_PREREGISTRATION.md',
                note='NEW GENERATION — not a reproduction of the Gemini 420/540 docx tables'),
            summary=summary)
        path = os.path.join(out_dir, outfile)
        json.dump(payload, open(path, 'w'), indent=2)
        outs[outfile] = dict(path=path, sha256=sha(path))
        print(f"wrote {path} sha256={outs[outfile]['sha256']}")
    # provenance bundle
    prov = dict(label=LABEL, wall_seconds=round(wall, 2), workers=workers, seeds=seeds,
                jobs=[list(j) for j in jobs], outputs=outs,
                engine_files=spec['engine_file_sha256'],
                spec_sha256=sha(SPEC), runner_sha256=sha(os.path.abspath(__file__)),
                preregistration_sha256=sha(os.path.join(REPO, 'docs', 'audit', 'GATE2_PREREGISTRATION.md')))
    json.dump(prov, open(os.path.join(out_dir, 'new_generation_provenance.json'), 'w'), indent=2)
    print(f"PROVENANCE {json.dumps(prov)[:400]}")
    return 0

def seeds_spec(seeds):
    return f"{seeds[0]}-{seeds[-1]}"

def parse_seeds(s):
    if '-' in s:
        a, b = s.split('-'); return list(range(int(a), int(b) + 1))
    return [int(x) for x in s.split(',')]

def main():
    if len(sys.argv) >= 2 and sys.argv[1] == 'arm':
        jur, arm_id, gate_variant, seeds_s, out_dir = sys.argv[2:7]
        run_arm(jur, arm_id, gate_variant, parse_seeds(seeds_s), out_dir)
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', default='0-99')
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--out-dir', default=os.path.join(REPO, 'results', 'new_generation'))
    a = ap.parse_args()
    return driver(parse_seeds(a.seeds), a.workers, a.out_dir)

if __name__ == '__main__':
    sys.exit(main())
