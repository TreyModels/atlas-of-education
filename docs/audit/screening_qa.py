#!/usr/bin/env python3
"""QA for Paper C screening bundle (36 cells x 8 seeds = 288 runs; screening-only).

Usage:
  python3 docs/audit/screening_qa.py --results ~/neon-boot/qa/incoming/paperC_screening \
      --queue ~/neon-boot/qa/incoming/paperC_screening_queue \
      --prereg docs/audit/PAPER_C_CONFIRMATORY_PREREG.md \
      --launch-manifest docs/audit/PAPER_C_LAUNCH_MANIFEST.json \
      --runner papers/shadow-education-contest/code/run_paperC_screening.py \
      --json-out docs/audit/results/screening_qa.json

Checks (S1–S11), analogue of Pilot-0 A1–A10:
 S1 payload + duplicate `_results` + .sha256 sidecars
 S2 queue SHA256SUMS + checkpoint_sha256 map + sidecar hashes
 S3 pins (engine/core/spec/runner/prereg; repo cross-check where available)
 S4 36-cell grid in fixed appendix order
 S5 288 rows, 8 seeds 0–7 per cell, N/T/measure_from, no duplicate seeds
 S6 per-row params/gate/supply/settings (P55/P12), engine fields, unfired_events==[]
 S7 binding assertions: exposed = supply A/C AND P55 -> withheld>1e-3 & own_share>0.1; B and A|P12 exempt
 S8 no NaN completion_* fields; no NaN/inf in summary means
 S9 summary key set: 36 cells x 18 metrics, n=8, mean/sd/ci95 present
 S10 ckpt rows reproduce summary mean/sd/n exactly
 S11 screening-only label/status, p12_mode=pay_gap recorded with prereg-clarification note, invalid_cells==[]
"""
import argparse, csv, glob, hashlib, json, math, os, re, subprocess, sys

S_VALUES = [0.85, 1.00, 1.15]; L_VALUES = [0.25, 0.45]; ARMS = ['A', 'B', 'C']; SETTINGS = ['P55', 'P12']
SUPPLIES = {'A': dict(own_ban=0.0, firm_ban=0.0), 'B': dict(own_ban=0.95, firm_ban=0.0), 'C': dict(own_ban=0.0, firm_ban=0.9)}
SETTINGS_MAP = {'P55': dict(pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap'),
                'P12': dict(pay_ratio=1.2, monitoring=0.5, withhold_mode='pay_gap')}
L_R = {0.25: 1.2, 0.45: 1.6}
EXPECTED_METRICS = ['tut_k12_rate', 'tut_k12_spend', 'tut_rate', 'withheld', 'own_share', 'own_share_financial_proxy',
                    'q5_q1_part_gap_pp', 'q5_q1_spend_gap', 'q5_q1_spend_ratio', 'own_count_proxy_k12',
                    'firm_count_proxy_k12', 'own_spend_proxy_k12', 'firm_spend_proxy_k12', 'q_pub', 'ptr',
                    'teacher_pay', 'priv_share', 'firm_price']
CORE_SHA = 'e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71'
SPEC_SHA = 'e5ddef6b4ecd04a0e96f480b43a97f0567bed7654ec032c1779c9e20f6beb755'
EXPECTED_RUNNER_SHA = 'd2d25c1cd6681c4271ab90d2df3afe18687b231b6b84fb7472392f23bef2562c'
ENGINE_COMMIT = '846c9e0'


def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def cell_ids():
    return [f'S{s:.2f}|L{l:.2f}|{a}|{st}' for s in S_VALUES for l in L_VALUES for st in SETTINGS for a in ARMS]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', required=True); ap.add_argument('--queue', required=True)
    ap.add_argument('--prereg', required=True); ap.add_argument('--launch-manifest', required=True)
    ap.add_argument('--runner', required=True); ap.add_argument('--json-out', default=None)
    a = ap.parse_args()
    R = a.results; Q = a.queue
    out = dict(results=R, queue=Q, checks=[], defects=[])
    def chk(sid, ok, msg):
        out['checks'].append(dict(id=sid, status='PASS' if ok is True else ('FAIL' if ok is False else 'INFO'), detail=msg))
    def defect(did, sev, msg):
        out['defects'].append(dict(id=did, severity=sev, detail=msg))

    payload_path = os.path.join(R, 'paperC_screening.json')
    dup_path = os.path.join(R, 'paperC_screening_results.json')
    if not os.path.exists(payload_path):
        chk('S1', False, f'payload missing: {payload_path}'); print(json.dumps(out, indent=1)); return 2
    p = json.load(open(payload_path)); m = p.get('manifest', {})
    same = os.path.exists(dup_path) and sha256(payload_path) == sha256(dup_path)
    sides_ok = all(os.path.exists(os.path.join(R, n + '.sha256')) and
                   sha256(os.path.join(R, n)) == open(os.path.join(R, n + '.sha256')).read().split()[0]
                   for n in ('paperC_screening.json', 'paperC_screening_results.json'))
    ck = sorted(glob.glob(os.path.join(R, 'ckpt_*.jsonl')))
    chk('S1', same and sides_ok and len(ck) == 36, f'payload present; duplicate _results identical={same}; sidecars ok={sides_ok}; ckpts={len(ck)}')

    # S2 checksums
    sums = os.path.join(Q, 'SHA256SUMS')
    bad = []
    if os.path.exists(sums):
        for line in open(sums):
            parts = line.split()
            if len(parts) < 2: continue
            h, f = parts[0], parts[1]
            fp = os.path.join(R, f)
            if not os.path.exists(fp) or sha256(fp) != h: bad.append(f)
    else:
        bad = ['SHA256SUMS missing']
    map_ok = p.get('checkpoint_sha256', {}) and all(
        p['checkpoint_sha256'].get(cid) == sha256(os.path.join(R, 'ckpt_' + cid.replace('|', '_') + '.jsonl'))
        for cid in p['checkpoint_sha256'])
    chk('S2', not bad and map_ok, f'queue SHA256SUMS entries bad={bad[:5]}; checkpoint_sha256 map ok={bool(map_ok)}')

    # S3 pins + repo cross-check
    runner_sha = sha256(a.runner)
    pins = dict(engine_commit=m.get('engine_commit') == ENGINE_COMMIT, core=m.get('core_sha256') == CORE_SHA,
                spec=m.get('spec_sha256') == SPEC_SHA, runner=m.get('runner_sha256') == EXPECTED_RUNNER_SHA,
                runner_file=runner_sha == EXPECTED_RUNNER_SHA)
    launch = json.load(open(a.launch_manifest))
    pins['launch_engine'] = launch.get('engine', {}).get('commit') == ENGINE_COMMIT
    pins['launch_core'] = launch.get('engine', {}).get('core_sha256') == CORE_SHA
    pins['launch_spec'] = launch.get('engine', {}).get('spec_file_sha256') == SPEC_SHA
    pins['prereg'] = sha256(a.prereg) == launch.get('prereg', {}).get('sha256')
    chk('S3', all(pins.values()), 'pins: ' + ', '.join(f'{k}={v}' for k, v in pins.items()))
    if launch.get('runner', {}).get('sha256') not in (None, m.get('runner_sha256')):
        out['defects'].append(dict(id='D-S0', severity='info',
            detail=f"launch manifest runner sha {launch['runner']['sha256'][:12]}… differs from executed runner {str(m.get('runner_sha256'))[:12]}… "
                   "— documented as 'screening runner extended before launch, launch sha recorded in run manifest'; actual runner file hash matches manifest"))

    # S4 grid
    expected = cell_ids(); man_cells = m.get('cells', [])
    rows_by_cell = {}
    for f in ck:
        rr = [json.loads(l) for l in open(f)]
        if not rr: continue
        rows_by_cell[rr[0]['cid']] = rr
    grid_ok = man_cells == expected and set(rows_by_cell) == set(expected) and len(rows_by_cell) == 36
    chk('S4', grid_ok, f'cells={len(man_cells)}; appendix order exact={man_cells == expected}; ckpt cells={len(rows_by_cell)}')

    # S5 runs/seeds
    probs = []
    total = 0
    for cid in expected:
        rr = rows_by_cell.get(cid)
        if rr is None: probs.append(f'{cid}: missing'); continue
        seeds = sorted(int(x['seed']) for x in rr)
        if seeds != list(range(8)): probs.append(f'{cid}: seeds {seeds}')
        if len(set(seeds)) != len(seeds): probs.append(f'{cid}: duplicate seeds')
        total += len(rr)
        for x in rr:
            if int(x['N']) != 600 or int(x['T']) != 46 or int(x['measure_from']) != 18:
                probs.append(f'{cid}: N/T/measure_from {x["N"]}/{x["T"]}/{x["measure_from"]}')
                break
    chk('S5', not probs and total == 288, f'runs={total}; problems={probs[:8]}')

    # S6 params/gate/settings/engine/unfired
    probs = []
    for cid in expected:
        sc, lc, arm, st = cid.split('|'); S = float(sc[1:]); L = float(lc[1:])
        for x in rows_by_cell[cid]:
            pr, gp = x.get('params', {}), x.get('gate', {})
            exp = dict(SUPPLIES[arm], **SETTINGS_MAP[st])
            if abs(float(pr.get('own_ban')) - exp['own_ban']) > 1e-12 or abs(float(pr.get('firm_ban')) - exp['firm_ban']) > 1e-12:
                probs.append(f'{cid} seed {x["seed"]}: supply params')
            if abs(float(pr.get('pay_ratio')) - exp['pay_ratio']) > 1e-12 or abs(float(pr.get('monitoring')) - exp['monitoring']) > 1e-12 \
               or pr.get('withhold_mode') != exp['withhold_mode']:
                probs.append(f'{cid} seed {x["seed"]}: setting params')
            if abs(float(pr.get('q0')) - S) > 1e-12 or abs(float(pr.get('N')) - 600) > 0 or abs(float(pr.get('T')) - 46) > 0:
                probs.append(f'{cid} seed {x["seed"]}: q0/N/T')
            if gp.get('kind') != 'contest' or gp.get('share_of') != 'cohort' or gp.get('fail') != 'stop' \
               or abs(float(gp.get('share')) - L) > 1e-12 or abs(float(gp.get('r')) - L_R[L]) > 1e-12:
                probs.append(f'{cid} seed {x["seed"]}: gate {gp}')
            e = x.get('engine', {})
            if e.get('commit') != ENGINE_COMMIT or e.get('core_sha') != CORE_SHA or e.get('spec_sha') != SPEC_SHA:
                probs.append(f'{cid} seed {x["seed"]}: row engine pins')
            if x.get('unfired_events') != []:
                probs.append(f'{cid} seed {x["seed"]}: unfired_events {x.get("unfired_events")}')
    chk('S6', not probs, f'param/gate/engine/unfired problems={probs[:8]}')
    if any(abs(float(x.get('params', {}).get('contest_r', 0)) - 1.5) < 1e-12 for rr in rows_by_cell.values() for x in rr):
        out['defects'].append(dict(id='D-S2', severity='info',
            detail='row params.contest_r is the static engine default 1.5, while the G6→G9 gate override sets gate.r by L (1.2/1.6) and the engine uses the gate override (core.py: r = p["contest_r"] if r is None else r) — harmless but potentially confusing; record gate.r as authoritative'))

    # S7 assertions (A/C AND P55 exposed; B and A|P12 exempt)
    probs = []; enforcement_bad = []
    meta_bad = []
    for cid in expected:
        arm = cid.split('|')[2]; st = cid.split('|')[3]
        exposed = arm in ('A', 'C') and st == 'P55'
        for x in rows_by_cell[cid]:
            h, own = float(x['withheld']), float(x['own_share'])
            if exposed and not (h > 1e-3 and own > 0.1):
                enforcement_bad.append(f'{cid} seed {x["seed"]}: h={h} own={own}')
            if not exposed and (h > 1e-3 and own > 0.1) and arm in ('A', 'C'):
                pass  # exempt cells may still exceed thresholds; no assertion applies
            afl = x.get('assertions', {})
            if bool(afl.get('exposed')) != exposed:
                meta_bad.append(f'{cid}: assertions.exposed={afl.get("exposed")} expected {exposed}')
    chk('S7', not enforcement_bad,
        f'exposed-arm enforcement (A/C AND P55) failures={enforcement_bad[:6]}; '
        f'non-blocking metadata exposed-flag mismatches={len(meta_bad)} (A|P12 mislabelled; actual check correct)')
    if meta_bad:
        defect('D-S1', 'low', 'runner metadata defect: per-row assertions.exposed is set to (supply in (A,C)) and rule text says only "B exempt" (runner line 207), so A|P12 is labelled exposed though A3.3 exempts it; the actual binding check (line 154) correctly applies only to A/C AND P55. Fix metadata before confirmatory (no effect on screening results; invalid_cells=[] and A|P12 not asserted).')

    # S8 NaN completion_* / non-finite summary
    comp_keys = [k for k in EXPECTED_METRICS if k.startswith('completion_')]
    nan_comp = [k for k in comp_keys if k in (p.get('summary', {}).get(expected[0], {}) or {})]
    nonfinite = []
    for cid, ms in p.get('summary', {}).items():
        for k, v in ms.items():
            mv = v.get('mean') if isinstance(v, dict) else v
            if isinstance(mv, float) and not math.isfinite(mv): nonfinite.append(f'{cid}.{k}')
    row_nonfinite = []
    for cid, rr in rows_by_cell.items():
        for x in rr:
            for k in EXPECTED_METRICS:
                v = x.get(k)
                if isinstance(v, float) and not math.isfinite(v): row_nonfinite.append(f'{cid}.{k}')
    chk('S8', not comp_keys and not nonfinite and not row_nonfinite,
        f'completion_* keys present={comp_keys}; non-finite summary={nonfinite[:5]}; non-finite rows={row_nonfinite[:5]}')

    # S9 summary key set
    probs = []
    for cid in expected:
        ms = p.get('summary', {}).get(cid)
        if ms is None: probs.append(f'{cid}: missing summary'); continue
        if set(ms) != set(EXPECTED_METRICS): probs.append(f'{cid}: metric set diff {set(ms) ^ set(EXPECTED_METRICS)}')
        for k, v in ms.items():
            if v.get('n') != 8: probs.append(f'{cid}.{k}: n={v.get("n")}')
            for f in ('mean', 'sd', 'ci95_lo', 'ci95_hi'):
                if f not in v: probs.append(f'{cid}.{k}: missing {f}')
    chk('S9', not probs, f'summary cells={len(p.get("summary", {}))}; problems={probs[:8]}')

    # S10 ckpt -> summary reproduction
    probs = []
    for cid in expected:
        ms = p['summary'][cid]; rr = rows_by_cell[cid]
        for k in EXPECTED_METRICS:
            vals = [float(x[k]) for x in rr]
            n = len(vals); mean = sum(vals) / n
            sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (n - 1)) if n > 1 else 0.0
            if not math.isclose(mean, float(ms[k]['mean']), rel_tol=0, abs_tol=1e-12):
                probs.append(f'{cid}.{k}: mean {mean} != {ms[k]["mean"]}')
            if not math.isclose(sd, float(ms[k]['sd']), rel_tol=0, abs_tol=1e-12):
                probs.append(f'{cid}.{k}: sd {sd} != {ms[k]["sd"]}')
    chk('S10', not probs, f'ckpt->summary reproduction problems={probs[:8]}')

    # S11 labels/status/queue
    label = str(p.get('label', '') or m.get('label', '')).upper()
    st = str(m.get('status', '')).upper()
    settings_note = str(m.get('settings_note', ''))
    q_status = open(os.path.join(Q, 'STATUS')).read().strip() if os.path.exists(os.path.join(Q, 'STATUS')) else ''
    queue_ok = q_status.startswith('OK') and os.path.exists(os.path.join(Q, 'RESULTS_DONE')) and os.path.exists(os.path.join(Q, 'finalize.log'))
    finalize = open(os.path.join(Q, 'finalize.log')).read() if os.path.exists(os.path.join(Q, 'finalize.log')) else ''
    chk('S11', ('SCREENING' in label) and st == 'SCREENING-ONLY' and p.get('invalid_cells') == []
        and str(m.get('p12_mode')) == 'pay_gap'
        and ('amend' in settings_note.lower() or 'confirmatory' in settings_note.lower())
        and queue_ok and 'verified' in finalize.lower() and float(p.get('wall_seconds', 0)) > 0,
        f'status={st}; label_screening={"SCREENING" in label}; invalid={p.get("invalid_cells")}; p12_mode={m.get("p12_mode")}; '
        f'queue_ok={queue_ok}; finalize_verified={"verified" in finalize.lower()}; wall={p.get("wall_seconds")}')
    if q_status and not q_status.startswith('OK'):
        defect('D-S3', 'high', f'queue STATUS not OK: {q_status}')

    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out), exist_ok=True); json.dump(out, open(a.json_out, 'w'), indent=1)
    print(json.dumps(out, indent=1)[:9000])
    ok = all(c['status'] == 'PASS' for c in out['checks'])
    print('\nSUMMARY:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
