#!/usr/bin/env python3
"""Plan, execute, resume and summarize purpose-specific Atlas experiments.

Planning uses only the standard library. Every trial runs in an isolated process;
scientific batches require an explicit run command. No results are shipped here.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import itertools
import json
import math
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = ('credential', 'shadow', 'camchild', 'angkor', 'schools', 'youth', 'fertility', 'ooa')
# Rigor families (research/rigor/README.md): mechanism recovery, placebo, rolling-origin and external checks.
RIGOR_FAMILIES = ('credential_recovery', 'shadow_recovery', 'youth_placebo', 'youth_rolling', 'fertility_placebo',
                  'camchild_validation')
ALL_FAMILIES = FAMILIES + RIGOR_FAMILIES


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False, encoding='utf-8') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
        temp = f.name
    os.replace(temp, path)


def source_state(ooa_root=None, output_root=None):
    """Hash actual code, protocols and input bytes, including uncommitted edits."""
    files = set()
    for part in ('engine', 'experiments', 'inputs', 'research'):
        for p in (ROOT / part).rglob('*'):
            if p.is_file() and not any(x in p.parts for x in ('__pycache__', '.venv', 'runs')) and p.suffix in ('.py', '.js', '.cjs', '.json', '.md'):
                if 'results' not in p.parts and 'results_v1' not in p.parts:
                    files.add(p)
    files.update((ROOT / 'public/engines').glob('*.js'))
    files.update(p for p in (ROOT / 'public/reference/east-asia-schools/source').rglob('*') if p.is_file())
    files.update((ROOT / 'public/research/fertility').glob('*'))
    excluded=Path(output_root).resolve() if output_root else None
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(files) if p.is_file() and not (excluded and p.is_relative_to(excluded))}
    if ooa_root:
        ooa_root = Path(ooa_root).resolve()
        required = ooa_root / 'code/model.py'
        if not required.exists():
            raise ValueError(f'OOA checkout missing: {required}')
        for folder in ('code', 'data'):
            for p in sorted((ooa_root / folder).glob('*')):
                if p.is_file():
                    hashes['ooa/' + str(p.relative_to(ooa_root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return {'digest': digest(hashes), 'files': hashes}


def environment():
    versions = {}
    for name in ('numpy', 'scipy', 'pandas', 'statsmodels', 'numba'):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    def git(*args):
        return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    node = subprocess.run(['node', '--version'], capture_output=True, text=True).stdout.strip() if __import__('shutil').which('node') else None
    return dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
                packages=versions, node=node, git_head=git('rev-parse', 'HEAD'),
                git_status=git('status', '--porcelain'), recorded_utc=datetime.now(timezone.utc).isoformat())


sys.path.insert(0, str(Path(__file__).resolve().parent))


def make_tasks(families, profile, draws=None, replicates=None, master_seed=20261116):
    smoke = profile == 'smoke'
    nd = draws if draws is not None else (2 if smoke else 32)
    nr = replicates if replicates is not None else (1 if smoke else 8)
    if min(nd, nr) < 1:
        raise ValueError('draws and replicates must be positive')
    tasks = []
    def add(family, cell, draw, rep, **settings):
        # Seeds omit structural cell labels so contrasts share exogenous draws.
        seed = int(digest([master_seed, family, draw, rep])[:8], 16)
        param_seed = int(digest([master_seed, family, draw, 'parameters'])[:8], 16)
        t = dict(family=family, cell=cell, draw=draw, replicate=rep, seed=seed,
                 parameter_seed=param_seed, settings=settings)
        t['id'] = digest(t)[:20]
        tasks.append(t)
    for family in families:
        if family == 'credential':
            for country, structure, liquidity in itertools.product(('Cambodia', 'Vietnam', 'China'), ('M_HC','M_POS','M_REL'), ('hard','graded')):
                for d, r in itertools.product(range(nd), range(nr)):
                    add(family, f'{country}/{structure}/{liquidity}', d, r, country=country,
                        structure=structure, liquidity=liquidity, n=200 if smoke else 4000)
        elif family == 'shadow':
            subsets = [None] if smoke else [None, [1,2,4], [1,2,5], [1,4,5], [2,4,5]]
            for variant, initial, subjects, subset in itertools.product(('thin','diversion','favour','full'),
                    ('all_sell','none_sell') if smoke else ('all_sell','none_sell','random'), (4,) if smoke else (4,6), subsets):
                for d, r in itertools.product(range(nd), range(nr)):
                    add(family, f'{variant}/{initial}/{subjects}/{subset}', d, r,
                        variant=variant, initial=initial, subjects=subjects, provider_schools=subset,
                        max_sweeps=100, policies=not smoke)
        elif family == 'camchild':
            for wealth in ('within_region_rank', 'national_income'):
                for d, r in itertools.product(range(nd), range(nr)):
                    add(family, wealth, d, r, wealth=wealth, n=200 if smoke else 6000,
                        years=2 if smoke else 12, uncertainty=not smoke)
        elif family == 'angkor':
            for coordination, floor, climate in itertools.product((1,1.2,5**.227), (0,.1), ('stable','drought')):
                for d, r in itertools.product(range(nd), range(nr)):
                    add(family, f'{coordination:.6g}/{floor}/{climate}', d, r,
                        coordination=coordination, waterFloor=floor, climate=climate)
            for floor,elite_use,drought in itertools.product((0,.3),('relief','service'),(False,True)):
                for d,r in itertools.product(range(nd),range(nr)):
                    add(family,f'institutions/{floor}/{elite_use}/{drought}',d,r,
                        engine='institutions',canal_floor=floor,elite_use=elite_use,drought=drought,
                        communities=2 if smoke else 24)
        elif family == 'schools':
            # Deterministic backtests and declared scenarios need no seed replication.
            add(family, 'retrospective-and-scenarios', 0, 0)
        elif family == 'youth':
            for cutoff in (2022,2024):
                for lam in ((None,) if smoke else (None,.005,.0124,.03,.15,1.0)):
                    for step in ((None,) if smoke else (None,0,.041,.068)):
                        for d in range(1 if smoke else nd):
                            add(family, f'cutoff{cutoff}/lambda{lam}/step{step}', d, 0,
                                cutoff=cutoff, lam=lam, step=step, max_nfev=3 if smoke else 300)
        elif family == 'fertility':
            for start, hac in itertools.product((1961,1964), (1,2,4)):
                add(family, f'start{start}/hac{hac}', 0, 0, start=start, hac=hac)
        elif family in RIGOR_FAMILIES:
            from rigor.design import rigor_tasks
            for cell, d, r, settings in rigor_tasks(family, smoke, nd, nr):
                add(family, cell, d, r, **settings)
        elif family == 'ooa':
            for chronology, speed_band, mix_cost, wait in itertools.product(('L','S'),
                    ('original',) if smoke else ('original','narrow_sensitivity'),
                    (0,.2) if smoke else (0,.05,.1,.2,.3), (0,) if smoke else (0,5)):
                for d in range(nd):
                    add(family, f'{chronology}/{speed_band}/{mix_cost}/{wait}', d, 0,
                        chronology=chronology, speed_band=speed_band, mix_cost=mix_cost, wait=wait)
    return tasks


def plan(args):
    families = list(dict.fromkeys(args.families))
    if 'ooa' in families and not args.ooa_root:
        raise ValueError('OOA trials require --ooa-root pointing to the companion checkout')
    out = Path(args.out).resolve()
    if (out / 'plan.json').exists():
        raise ValueError('plan already exists; choose a new directory or resume with run')
    state = source_state(args.ooa_root,out)
    tasks = make_tasks(families,args.profile,args.draws,args.replicates,args.seed)
    config = dict(schema=1, purpose='theoretical exploration and retrospective diagnostics',
                  profile=args.profile, source_digest=state['digest'],
                  master_seed=args.seed, families=families, tasks=tasks,
                  ooa_root=str(Path(args.ooa_root).resolve()) if args.ooa_root else None,
                  prospective_preregistration=False)
    config['plan_digest'] = digest(config)
    write_json(out / 'sources.json',state)
    write_json(out / 'environment-plan.json',environment())
    write_json(out / 'plan.json',config)
    counts={f:sum(t['family']==f for t in tasks) for f in families}
    print(json.dumps(dict(out=str(out),trials=len(tasks),by_family=counts,profile=args.profile),indent=2))


def clean(value, bad, path=''):
    if hasattr(value, 'tolist'):
        value=value.tolist()
    if isinstance(value,dict):
        return {str(k):clean(v,bad,f'{path}/{k}') for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [clean(v,bad,f'{path}/{i}') for i,v in enumerate(value)]
    if isinstance(value,float) and not math.isfinite(value):
        bad.append(path)
        return None
    return value


def worker():
    from adapters import trial
    spec=json.load(sys.stdin)
    result=trial(spec['task'],Path(spec['ooa_root']) if spec.get('ooa_root') else None)
    bad=[]
    result=clean(result,bad)
    result['nonfinite_fields']=bad
    print(canonical(result))


def execute_one(task, out, config, timeout):
    target=out/'trials'/f"{task['id']}.json"
    if target.exists():
        old=json.loads(target.read_text())
        if old['status']=='ok':
            return 'cached'
    started=time.monotonic()
    try:
        proc=subprocess.run([sys.executable,str(Path(__file__).resolve()),'_worker'],
            input=canonical({'task':task,'ooa_root':config['ooa_root']}),text=True,
            cwd=ROOT,capture_output=True,timeout=timeout,
            env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
        if proc.returncode:
            raise RuntimeError(proc.stderr[-12000:] or proc.stdout[-12000:])
        result=json.loads(proc.stdout)
        record=dict(task=task,status='ok',result=result,stderr=proc.stderr[-12000:])
    except Exception as exc:
        record=dict(task=task,status='failed',error=f'{type(exc).__name__}: {exc}')
    record.update(plan_digest=config['plan_digest'],environment_digest=config['environment_digest'],
                  seconds=time.monotonic()-started)
    write_json(target,record)
    return record['status']


def run(args):
    out=Path(args.out).resolve()
    config=json.loads((out/'plan.json').read_text())
    expected=config['plan_digest']
    body={k:v for k,v in config.items() if k!='plan_digest'}
    if digest(body)!=expected:
        raise ValueError('plan was edited; create a new plan so the amendment has its own identity')
    if source_state(config['ooa_root'],out)['digest']!=config['source_digest']:
        raise ValueError('source or input bytes changed; create a new plan directory')
    current_env=environment()
    planned_env=json.loads((out/'environment-plan.json').read_text())
    env_keys=('python','packages','node')
    if any(current_env[k]!=planned_env[k] for k in env_keys):
        raise ValueError('Python/package/Node versions changed since planning; create a new plan directory')
    config['environment_digest']=digest({k:current_env[k] for k in env_keys})
    (out/'trials').mkdir(exist_ok=True)
    # A run directory has a single writer. A failed process leaves a visible lock.
    lock=out/'RUNNING.lock'
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    os.write(fd,str(os.getpid()).encode());os.close(fd)
    try:
        write_json(out/f'environment-run-{time.time_ns()}.json',current_env)
        tasks=config['tasks'][:args.limit] if args.limit else config['tasks']
        failed=0
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            pending=[pool.submit(execute_one,t,out,config,args.timeout) for t in tasks]
            for i,f in enumerate(as_completed(pending),1):
                status=f.result();failed+=status=='failed'
                print(f'{i}/{len(tasks)} {status}',flush=True)
        ending=source_state(config['ooa_root'],out)['digest']
        write_json(out/'integrity.json',{'source_digest_end':ending,
                                        'source_matches_plan':ending==config['source_digest']})
        report(out)
        if ending!=config['source_digest']:
            raise ValueError('source/input drift during execution: this batch is invalid; create a new plan')
        if failed:
            raise SystemExit(1)
    finally:
        lock.unlink()


def describe(values):
    values=list(values)
    n=len(values)
    if not n:
        return {'n':0}
    sd=statistics.stdev(values) if n>1 else None
    return dict(n=n,mean=statistics.mean(values),sd=sd,
                mcse=sd/math.sqrt(n) if sd is not None else None,min=min(values),max=max(values))


def nested_summary(rows):
    by_draw={}
    for draw,value in rows:
        by_draw.setdefault(draw,[]).append(value)
    means=[statistics.mean(v) for v in by_draw.values()]
    between=describe(means)
    within=[statistics.variance(v) for v in by_draw.values() if len(v)>1]
    return dict(draw_means=between,replicates_per_draw=sorted(len(v) for v in by_draw.values()),
                mean_within_draw_variance=statistics.mean(within) if within else None,
                interpretation='MCSE of sampled draw means, conditional on declared design and ranges; no real-world confidence interval')


def report(out):
    out=Path(out)
    config=json.loads((out/'plan.json').read_text())
    records=[]
    for t in config['tasks']:
        p=out/'trials'/f"{t['id']}.json"
        if p.exists():
            r=json.loads(p.read_text())
            if r['plan_digest']!=config['plan_digest']:
                raise ValueError(f'wrong plan identity in {p}')
            records.append(r)
    groups={}
    for r in records:
        if r['status']!='ok':continue
        t=r['task']
        for name,val in r['result'].get('metrics',{}).items():
            if isinstance(val,(int,float)) and not isinstance(val,bool):
                groups.setdefault((t['family'],t['cell'],name),[]).append((t['draw'],val))
    expected_cells={}
    for t in config['tasks']:
        key=(t['family'],t['cell']);expected_cells[key]=expected_cells.get(key,0)+1
    summary=[dict(family=f,cell=c,metric=m,valid_trials=len(v),planned_trials=expected_cells[(f,c)],
                  **nested_summary(v)) for (f,c,m),v in sorted(groups.items())]
    status=dict(expected=len(config['tasks']),successful=sum(r['status']=='ok' for r in records),
                failed=sum(r['status']=='failed' for r in records),pending=len(config['tasks'])-len(records))
    if (out/'integrity.json').exists():
        status['source_matches_plan']=json.loads((out/'integrity.json').read_text())['source_matches_plan']
    write_json(out/'summary.json',dict(status=status,summaries=summary))
    lines=['# Experiment run', '',canonical(status),'',
           'Smoke runs check execution only. This report never certifies a social theory or promotes an exploratory result to a forecast.', '',
           '| Family | Cell | Metric | Valid/planned trials | Draws | Mean | MCSE of draw means |', '|---|---|---|---:|---:|---:|---:|']
    for s in summary:
        x=s['draw_means'];mc=x['mcse']
        lines.append(f"| {s['family']} | {s['cell']} | {s['metric']} | {s['valid_trials']}/{s['planned_trials']} | {x['n']} | {x['mean']:.6g} | {'' if mc is None else format(mc,'.3g')} |")
    lines+=['','Raw trials include parameter settings, solver diagnostics, paired effects, missing/nonfinite fields and failures. ',
            'Repeat observations from one parameter draw are averaged before MCSE calculation. Parameter-range uncertainty and synthetic seed variability are reported separately.']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print(canonical(status))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('plan')
    q.add_argument('--out',required=True)
    q.add_argument('--families',nargs='+',choices=ALL_FAMILIES,default=list(FAMILIES[:-1]))
    q.add_argument('--profile',choices=('smoke','main'),default='smoke')
    q.add_argument('--draws',type=int);q.add_argument('--replicates',type=int)
    q.add_argument('--seed',type=int,default=20261116);q.add_argument('--ooa-root')
    q=sub.add_parser('run');q.add_argument('--out',required=True)
    q.add_argument('--jobs',type=int,default=1);q.add_argument('--timeout',type=float,default=3600)
    q.add_argument('--limit',type=int)
    q=sub.add_parser('report');q.add_argument('--out',required=True)
    sub.add_parser('_worker')
    a=p.parse_args()
    if a.command=='plan':plan(a)
    elif a.command=='run':
        if a.jobs<1 or a.timeout<=0 or (a.limit is not None and a.limit<1):p.error('execution limits must be positive')
        run(a)
    elif a.command=='report':report(Path(a.out))
    else:worker()


if __name__=='__main__':main()
