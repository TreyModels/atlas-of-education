#!/usr/bin/env python3
"""Mechanical QA for Paper C Pilot-0 artefacts (host-only; no box jobs).

Usage:
  python3 docs/audit/pilot0_qa.py --results /path/to/paperC/results \
      [--engine-repo /path/to/atlas-worktree]

Checks (each returns PASS/FAIL/BLOCKED):
 1 artefact presence + payload schema (paperC_pilot0_results.json)
 2 engine pin 846c9e0 recorded AND core.py sha e111397b… verified against the pinned git commit
 3 design: 16 cells x 8 seeds = 128 runs; 4 regimes; q0 {1.0,1.2}; p_firm {0.03,0.08}
 4 recorded parameters match the declared design (own_ban, pay_ratio, monitoring, firm_ban)
 5 seed completeness in every ckpt_*.jsonl (8 unique seeds, no duplicates, row params match cell)
 6 summary keys exist for all 16 cells and all expected metrics, n=8 per metric
 7 no-op guard: every non-market regime cell has mean(withheld) > 1e-3 and mean(own_share) > 0.1
 8 EXPLORATORY label present (no confirmatory/causal claim in the payload)
"""
import argparse, hashlib, json, os, re, subprocess, sys

import numpy as np

REGIMES = {
    'market_only':            dict(own_ban=0.95, pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap'),
    'own_open_gap':           dict(own_ban=0.0,  pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap'),
    'own_open_incentive':     dict(own_ban=0.0,  pay_ratio=1.2,  monitoring=0.2, withhold_mode='incentive'),
    'own_open_gap_firm_ban':  dict(own_ban=0.0,  pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap', firm_ban=0.9),
}
Q0S = [1.0, 1.2]; PFIRMS = [0.03, 0.08]; NSEEDS = 8; EXPECTED_CELLS = 16; EXPECTED_RUNS = 128
METRICS = ['tut_k12_rate','tut_k12_spend','tut_g12_rate','own_share','firm_price','q_pub','withheld','ptr',
           'teacher_pay','pub_spend','priv_share','elite_share','track_share','completion_primary',
           'completion_upper','contest_e_mean','tut_rate','elite_q5_share_pct','tut_own_by_grade_last',
           'tut_firm_by_grade_last','L_mean','L6_mean','L9_mean']
PIN = '846c9e0'; CORE_SHA = 'e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71'
# Provenance (lead-confirmed): engine at 846c9e0 + canonical_spec.json FILE from the re-pin commit 46c080d
# (file sha e5ddef6b…b755; spec content sha 280b5d95…). The git tree at 846c9e0 predates the re-pin, so an
# in-tree spec hash of 35576f… is expected old content, not a defect.
SPEC_SHA = 'e5ddef6b4ecd04a0e96f480b43a97f0567bed7654ec032c1779c9e20f6beb755'
results = []
def rec(sid, ok, msg): results.append((sid, 'PASS' if ok is True else ('FAIL' if ok is False else 'BLOCKED'), msg))

def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest() if p and os.path.exists(p) else None

def cellkey(r, q0, pf):
    return f'{r}|q0={q0}|p_firm={pf}'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--results', required=True); ap.add_argument('--engine-repo', default=None)
    ap.add_argument('--log', default=None, help='optional pilot driver log; checks absence of unfired_events/RuntimeError')
    a = ap.parse_args(); root = a.results
    payload_path = os.path.join(root, 'paperC_pilot0_results.json') if os.path.isdir(root) else root
    if not os.path.exists(payload_path):
        rec('A1', None, f'paperC_pilot0_results.json not found at {payload_path} (artefact UNAVAILABLE)')
        for sid in ['A2','A3','A4','A5','A6','A7','A8']: rec(sid, None, 'blocked on A1')
        print(json.dumps(dict(results=results), indent=1)); return 2
    p = json.load(open(payload_path)); rec('A1', True, f'payload present: {payload_path}')
    man = p.get('manifest', {}); summ = p.get('summary', {})
    # A2 engine pin
    ok2 = (man.get('engine_commit') == PIN and man.get('engine_core_sha256') == CORE_SHA
           and man.get('spec_sha256') == SPEC_SHA)
    msg2 = f"engine_commit={man.get('engine_commit')} core_sha={str(man.get('engine_core_sha256'))[:12]} spec_sha={str(man.get('spec_sha256'))[:12]}"
    msg2 += ' (provenance: engine 846c9e0 + spec file from re-pin 46c080d e5ddef6b…; in-tree 846c9e0 spec 35576f… is expected old content)' if man.get('spec_sha256') == SPEC_SHA else ' — EXPECTED spec_sha e5ddef6b…'
    if a.engine_repo and ok2:
        try:
            commit = subprocess.check_output(['git','-C',a.engine_repo,'rev-parse',PIN], text=True).strip()
            core = subprocess.check_output(['git','-C',a.engine_repo,'show',f'{PIN}:engine/eduengine/core.py'], text=True).encode()
            ok2 = hashlib.sha256(core).hexdigest() == CORE_SHA
            msg2 += f'; git pin resolves {commit[:10]} + core sha verified'
        except Exception as e:
            ok2 = False; msg2 += f'; git verification failed: {e}'
    rec('A2', ok2, msg2)
    # A3 design
    seeds = man.get('seeds'); nseeds = man.get('n_seeds'); cells = man.get('cells'); runs = man.get('runs')
    ok3 = (man.get('regimes') is not None and set(man['regimes']) == set(REGIMES) and
           man.get('q0_proxy') == Q0S and man.get('p_firm') == PFIRMS and
           nseeds == NSEEDS and cells == EXPECTED_CELLS and runs == EXPECTED_RUNS and
           isinstance(seeds, list) and len(seeds) == NSEEDS)
    rec('A3', ok3, f'regimes={list(man.get("regimes", {}))} q0={man.get("q0_proxy")} p_firm={man.get("p_firm")} seeds={seeds} n_seeds={nseeds} cells={cells} runs={runs}')
    # A4 recorded params
    bad = []
    for rname, exp in REGIMES.items():
        got = man.get('regimes', {}).get(rname, {})
        for k, v in exp.items():
            gv = got.get(k)
            if isinstance(v, (int, float)):
                if gv is None or abs(float(gv) - float(v)) > 1e-12:
                    bad.append(f'{rname}.{k}={gv} != {v}')
            else:
                if str(gv) != str(v):
                    bad.append(f'{rname}.{k}={gv} != {v}')
    rec('A4', not bad, 'parameter mismatches: ' + ('; '.join(bad) if bad else 'none (own_ban/pay_ratio/monitoring/withhold_mode/firm_ban match declared design)'))
    # A5 seed completeness
    if os.path.isdir(root):
        ck = [f for f in os.listdir(root) if re.match(r'ckpt_.*\.jsonl$', f)]
        cell_exp = [(r, q0, pf) for r in REGIMES for q0 in Q0S for pf in PFIRMS]
        problems = []
        for r, q0, pf in cell_exp:
            tag = f'{r}_q{q0:.2f}_pf{pf:.3f}'; f = os.path.join(root, f'ckpt_{tag}.jsonl')
            if not os.path.exists(f): problems.append(f'missing ckpt {tag}'); continue
            rows = [json.loads(l) for l in open(f) if l.strip()]
            sds = [int(x.get('seed')) for x in rows]
            if sorted(sds) != list(range(NSEEDS)): problems.append(f'{tag}: seeds {sorted(sds)}')
            if len(set(sds)) != len(sds): problems.append(f'{tag}: duplicate seed rows')
            for x in rows:
                if x.get('regime') != r or abs(float(x.get('q0'))-q0) > 1e-12 or abs(float(x.get('p_firm'))-pf) > 1e-12:
                    problems.append(f'{tag}: row params mismatch'); break
        rec('A5', not problems, f'{len(ck)} ckpt files; ' + ('; '.join(problems[:8]) if problems else 'all 16 cells x 8 unique seeds, params match'))
    else:
        rec('A5', None, 'results dir not available for ckpt inspection')
    # A6 summary keys
    expect_keys = {cellkey(r, q0, pf) for r in REGIMES for q0 in Q0S for pf in PFIRMS}
    miss = expect_keys - set(summ); extra = set(summ) - expect_keys
    metric_problems = []
    for k, ms in summ.items():
        for m in METRICS:
            if m not in ms: metric_problems.append(f'{k}: missing {m}')
            elif ms[m].get('n') != NSEEDS: metric_problems.append(f'{k}.{m}: n={ms[m].get("n")}')
    rec('A6', not (miss or extra or metric_problems), f'cells={len(summ)} missing={sorted(miss)} extra={sorted(extra)} metric_problems={metric_problems[:6]}')
    # A7 no-op guard
    guard = []
    for k, ms in summ.items():
        r = k.split('|')[0]
        if r == 'market_only': continue
        h = ms.get('withheld', {}).get('mean'); os_ = ms.get('own_share', {}).get('mean')
        if h is None or os_ is None or not (h > 1e-3) or not (os_ > 0.1): guard.append(f'{k}: withheld={h} own_share={os_}')
    rec('A7', not guard, 'non-market cells passing withheld>1e-3 && own_share>0.1: ' + (f'{EXPECTED_CELLS-4-len(guard)}/12' if not guard else '; '.join(guard[:6])))
    # A8 exploratory label
    lab = str(p.get('label','')) + ' ' + json.dumps(man)
    ok8 = ('EXPLORATORY' in lab.upper()) and not re.search(r'\bCAUSAL\b|\bCONFIRMATORY RESULT\b', lab.upper().replace('NOT CONFIRMATORY',''))
    rec('A8', ok8, f'label starts: {str(p.get("label",""))[:100]}')
    # A9 unfired events / loud-failure evidence (runner raises on non-empty unfired_events)
    log = a.log if a.log else None
    if log and os.path.exists(log):
        txt = open(log, encoding='utf-8', errors='replace').read()
        bad = ('unfired events' in txt) or ('RuntimeError' in txt) or ('Traceback' in txt)
        rec('A9', not bad, f'log={log}: unfired/RuntimeError/Traceback found={bad}')
    else:
        rec('A9', None, 'no driver log supplied (--log): unfired_events==[] is enforced per run by the runner (raises), but attach pilot_v3_8w.log for evidence')
    # A10: ckpt rows must reproduce the published summary (mean/sd/n) exactly, and the no-op guard
    # must hold on the raw per-seed rows (not only on the summary means).
    if os.path.isdir(root):
        problems = []
        for k, ms in summ.items():
            rname = k.split('|')[0]
            tag = f"{rname}_q{float(k.split('q0=')[1].split('|')[0]):.2f}_pf{float(k.split('p_firm=')[1]):.3f}"
            f = os.path.join(root, f'ckpt_{tag}.jsonl')
            if not os.path.exists(f): problems.append(f'{tag}: missing ckpt'); continue
            rows = [json.loads(l) for l in open(f) if l.strip()]
            for metric, sv in ms.items():
                vals = np.array([r[metric] for r in rows if metric in r], float)
                if len(vals) != sv.get('n'): problems.append(f'{tag}.{metric}: n {len(vals)} != {sv.get("n")}'); continue
                m_raw = float(np.nanmean(vals)); m_sum = float(sv['mean'])
                if not ((np.isnan(m_raw) and np.isnan(m_sum)) or
                        np.isclose(m_raw, m_sum, rtol=0, atol=1e-12)):
                    problems.append(f'{tag}.{metric}: mean {m_raw} != summary {m_sum}')
            if rname != 'market_only':
                h = np.nanmean([r['withheld'] for r in rows]); os_ = np.nanmean([r['own_share'] for r in rows])
                if not (h > 1e-3 and os_ > 0.1): problems.append(f'{tag}: raw-row guard withheld={h} own_share={os_}')
        rec('A10', not problems, 'ckpt rows reproduce summary mean/n and raw-row no-op guard; ' + ('; '.join(problems[:8]) if problems else 'all 16 cells OK'))
    print(json.dumps(dict(results=results), indent=1))
    print('\nSUMMARY:', 'PASS' if all(s=='PASS' for _,s,_ in results) else 'FAIL/BLOCKED')
    return 0 if all(s=='PASS' for _,s,_ in results) else 1

if __name__ == '__main__': sys.exit(main())
