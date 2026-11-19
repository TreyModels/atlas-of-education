"""Model adapters. Each call is isolated by lab.py; imports cannot leak between models."""
from __future__ import annotations

from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research'))
from rigor.adapters_rigor import TRIALS as RIGOR_TRIALS  # noqa: E402


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod


def credential(t):
    import numpy as np
    sys.path.insert(0,str(ROOT/'engine'))
    import relfloor_countries as m
    s=t['settings'];cfg=m.CFG[s['country']]
    # All structures and both financing rules receive the same nuisance draw.
    p=m.draw(np.random.default_rng(t['parameter_seed']),'M_REL',cfg,smooth_liq=True)
    if s['structure']=='M_HC':p['b_pos']=p['b_rel']=0.
    elif s['structure']=='M_POS':p['b_rel']=0.
    if s['liquidity']=='hard':p['s_liq']=0.
    b=m.sim(p,cfg,'base',s['n'],t['seed'])
    f=m.sim(p,cfg,'fall',s['n'],t['seed'])
    metrics=m.premium_contrasts(b,f)
    metrics.update(completion_2024=float(b['c'][m.yi(2024)]),completion_2035=float(b['c'][-1]),
                   b_rel=p['b_rel'],b_pos=p['b_pos'],prem0=p['prem0'])
    metrics.update({'screen_'+k:float(test(b)) for k,test in cfg['tests'].items()})
    if s['country']=='Cambodia':
        for year in (2014,2021):
            metrics[f'profile_max_error_{year}']=float(np.max(np.abs(b['q'][m.yi(year)]-m.KHM_Q[year])))
            metrics[f'bottom40_noncompleters_{year}']=float(b['exit_low'][m.yi(year)])
    return dict(metrics=metrics,parameters=p,profiles={str(y):b['q'][m.yi(y)].tolist() for y in (2014,2021,2024,2035)},
                evidence_role='retrospective screens; all targets previously inspected',
                limitation='relational term is an additive utility value; institutional eligibility is not identified')


def shadow(t):
    import numpy as np
    path=ROOT/'experiments/shadow-abm/src/tutoring_abm'
    sys.path.insert(0,str(path))
    import model as m
    import calibrate as c
    s=t['settings']
    p=m.draw_params(np.random.default_rng(t['parameter_seed']),'full')
    values={k:0. for k in ('diversion','favour') if k not in m.VARIANTS[s['variant']]}
    offsets=(0.,-.4,-.8,-1.2) if s['subjects']==4 else (0.,-.4,-.8,-1.2,-1.6,-2.)
    p=replace(p,**values,subject_offsets=offsets,provider_school_ids=s['provider_schools'],initial_state=s['initial'])
    b=m.World(p,t['seed']).solve(s['max_sweeps']).outcomes()
    distances=c.distances(b)
    metrics=dict(converged=b['converged'],sweeps=b['sweeps'],screen_fit=float(max(distances.values())<=1))
    if b['converged']:
        for k in ('participation','withholding_mean','coverage','coverage_q1','coverage_q5',
                  'source_own_provider_share','source_other_provider_share','own_purchase_share'):
            metrics[k]=b[k]
    policy_diagnostics={}
    if s['policies'] and b['converged']:
        for name,change in {'ban_own':{'ban_own':True},'conditional_pay':{'cond_pay':.3},
                            'extra_instruction':{'extra_time':.1},'provider_entry':{'com_entry':1.5}}.items():
            o=m.World(replace(p,**change),t['seed']).solve(s['max_sweeps']).outcomes()
            policy_diagnostics[name]={'converged':o['converged'],'sweeps':o['sweeps']}
            metrics[name+'_converged']=o['converged']
            if o['converged']:
                for key in ('participation','withholding_mean','coverage_q1','coverage_q5'):
                    metrics[name+'_effect_'+key]=o[key]-b[key]
    return dict(metrics=metrics,parameters={**p.__dict__},distances=distances,policies=policy_diagnostics,
                evidence_role='prior exploration of synthetic school systems; no new observed-school validation',
                limitation='six-subject offsets and possible source-school subsets are declared structural assumptions')


def node_trial(t):
    p=subprocess.run(['node',str(ROOT/'research/node_adapter.cjs')],input=json.dumps(t),
                     capture_output=True,text=True,cwd=ROOT,check=True)
    return json.loads(p.stdout)


def institutions(t):
    import itertools
    import random
    m=module(ROOT/'experiments/angkor-review/model/accounted_v2.py','review_accounts')
    s={k:v for k,v in t['settings'].items() if k!='engine'}
    rng=random.Random(t['parameter_seed'])
    p=m.Settings(**s,seed=t['seed'],maintenance_factor=rng.uniform(.1,.8),
                 elite_spend=rng.uniform(0,.25),refuge_yield=rng.uniform(1500,2500))
    b=m.run(replace(p,regime='stable'))
    maintained=m.run(replace(p,regime='maintenance_only'))
    def final(x):return x['history'][-1] if isinstance(x,dict) else x[-1]
    baseline=final(b);ref=final(maintained)
    metrics={}
    for key in ('total_population','state_population','refuge_population','canal_condition','grain_stock_kg'):
        metrics['maintenance_effect_'+key]=ref[key]-baseline[key]
    for flags in itertools.product((False,True),repeat=4):
        parts=','.join(k for k,on in zip(m.PARTS,flags) if on) or 'none'
        result=m.run(replace(p,regime='reshuffle',reshuffle_parts=parts))
        last=final(result)
        for key in ('total_population','state_population','refuge_population','canal_condition','grain_stock_kg'):
            metrics[parts+'_effect_'+key]=last[key]-ref[key]
    return dict(metrics=metrics,parameters=p.__dict__,evidence_role='factorial reshuffle channels with annual grain, labour and population assertions',
                limitation='illustrative institutions; rates are uncalibrated, and the historical pathway remains unvalidated')


def youth(t):
    import numpy as np
    from scipy.optimize import least_squares
    sys.path.insert(0,str(ROOT/'engine'))
    from firms import calibrate_china as c, forecast_strict as f, forecast_2024 as f4
    s=t['settings'];fixed={'sigma_A':5.}
    if s['lam'] is not None:fixed['lam_g']=s['lam']
    if s['step'] is not None:fixed['dr_drop']=s['step']
    free=[row for row in c.FREE if row[0] not in fixed]
    lo=np.array([row[1] for row in free]);hi=np.array([row[2] for row in free])
    start=np.array([row[3] for row in free]) if t['draw']==0 else np.random.default_rng(t['parameter_seed']).uniform(lo,hi)
    def expand(x):
        ps={**dict(zip([row[0] for row in free],x)),**fixed}
        return np.array([ps[row[0]] for row in c.FREE])
    run=lambda x:f.run(expand(x),'strict',fixed) if s['cutoff']==2022 else f4.run(expand(x),fixed)
    def train(R):
        if s['cutoff']==2022:return c.obs_pairs(R,2018,2022,'old')
        a,b=f4.fit_pairs(R);return a+b
    nobs=len(train(run(start)))
    def resid(x):
        try:
            err=np.array([mod-obs for _,_,obs,mod,_ in train(run(x))])
            return err if np.all(np.isfinite(err)) else np.full(nobs,50.)
        except ValueError:return np.full(nobs,50.)
    fit=least_squares(resid,start,bounds=(lo,hi),diff_step=1e-3,max_nfev=s['max_nfev'])
    R=run(fit.x)
    metrics={'train_cost':float(fit.cost),'train_mae':c.stats(train(R))['mae'],
             'optimizer_success':float(fit.success),'nfev':fit.nfev,
             'bound_count':sum(min(v-a,b-v)<.01*(b-a) for v,a,b in zip(fit.x,lo,hi))}
    if s['cutoff']==2022:
        scores=f.score(R);naive=f.score(f=f.naive('same_month_2022'))
        for name in scores:
            metrics[name+'_mae']=scores[name]['mae']
            metrics[name+'_naive_mae']=naive[name]['mae']
        comparability='2023H1 uses same old definition; post-2023 comparison crosses a measurement break'
    else:
        metrics['test_mae']=c.stats(f4.test_pairs(R))['mae']
        metrics['naive_mae']=f4.score_fn(f4.naive('same_month_2024'))['mae']
        comparability='2025-26 benchmark and model use the new definition'
    singular=np.linalg.svd(fit.jac,compute_uv=False)
    return dict(metrics=metrics,parameters={row[0]:float(v) for row,v in zip(c.FREE,expand(fit.x))},
                jacobian_singular_values=singular.tolist(),optimizer_message=fit.message,
                evidence_role='retrospective information-set reconstruction; evaluation periods already inspected',
                uncertainty_role='draw index is optimizer restart, not a posterior draw',comparability=comparability,
                limitation='Jacobian rank is a local numerical diagnostic; unexplained step remains a fitted residual')


def fertility(t):
    import numpy as np
    from scipy import stats
    s=t['settings']
    page=json.loads((ROOT/'public/research/fertility/fertility-series.json').read_text())
    with zipfile.ZipFile(ROOT/'public/research/fertility/fertility-research-full.zip') as z:
        life=json.loads(z.read('fertility_handoff/life_asia.json'))
        panel=json.loads(z.read('fertility_handoff/asia_panel_data.json'))
    years=np.asarray(page['years'])
    mask=years>=s['start'];years=years[mask]
    records={};metrics={}
    try:
        from statsmodels.tsa.stattools import coint
    except ImportError:coint=None
    for place in ('PHL','THA','KOR','JPN','HKG','CHN'):
        y=np.asarray(page['places'][place]['obs'])[mask]
        for name,x in [('life_expectancy',np.array([life[place]['values'][str(v)] for v in years],float)),
                       ('log_gdp',np.log([panel['gdp_'+place]['values'][str(v)] for v in years]))]:
            key=place+'/'+name
            data={}
            for form in ('levels','differences','linear_detrended'):
                yy=np.diff(y) if form=='differences' else y
                xx=np.diff(x) if form=='differences' else x
                X=np.column_stack([np.ones(len(xx)),xx])
                if form=='linear_detrended':X=np.column_stack([X,np.arange(len(xx))])
                beta=np.linalg.lstsq(X,yy,rcond=None)[0];e=yy-X@beta
                # HAC is computed within place, never over concatenated country blocks.
                bread=np.linalg.pinv(X.T@X);xe=X*e[:,None];meat=xe.T@xe
                for lag in range(1,s['hac']+1):
                    g=xe[lag:].T@xe[:-lag];meat+=(1-lag/(s['hac']+1))*(g+g.T)
                se=float(np.sqrt(max(0,(bread@meat@bread)[1,1])))
                data[form]={'slope':float(beta[1]),'hac_se':se,
                            'p_asymptotic':float(2*stats.norm.sf(abs(beta[1]/se))) if se else None,
                            'condition_number':float(np.linalg.cond(X))}
                metrics[key+'/'+form+'_slope']=float(beta[1])
            conditional=[];frozen=[];persistence=[]
            for i,year in enumerate(years):
                if year<1990 or i<20:continue
                coef=np.linalg.lstsq(np.column_stack([np.ones(i),x[:i]]),y[:i],rcond=None)[0]
                conditional.append(abs(y[i]-(coef[0]+coef[1]*x[i])))
                frozen.append(abs(y[i]-(coef[0]+coef[1]*x[i-1])))
                persistence.append(abs(y[i]-y[i-1]))
            data['rolling']={'conditional_realised_covariate_mae':float(np.mean(conditional)),
                             'frozen_covariate_mae':float(np.mean(frozen)),
                             'persistence_mae':float(np.mean(persistence)), 'n':len(persistence)}
            for k,v in data['rolling'].items():metrics[key+'/'+k]=v
            if coint:
                data['engle_granger_p']=float(coint(y,x,trend='c',autolag='AIC')[1])
            records[key]=data
    return dict(metrics=metrics,details=records,evidence_role='exploratory time-series diagnostics, all series previously inspected',
                limitation='period TFR; six places; integration and break assumptions need scrutiny; multiple exploratory comparisons; no pooled p-values',
                cointegration_backend='statsmodels' if coint else 'not installed: cointegration omitted')


def ooa(t,root):
    if root is None:raise ValueError('missing OOA checkout')
    import numpy as np
    sys.path.insert(0,str(root/'code'))
    import model as m
    s=t['settings'];rng=np.random.default_rng(t['parameter_seed'])
    p=m.sample_params(rng)
    if s['speed_band']=='narrow_sensitivity':p['v_max']=float(np.exp(rng.uniform(np.log(1),np.log(2))))
    p.update(c_mix=s['mix_cost'],wait_kyr=s['wait'])
    # Draw noise from a separate stream; changing a prior never changes the noise.
    noise=m.noise_field(np.random.default_rng(t['seed']))
    start_rng=np.random.default_rng([t['parameter_seed'],500])
    if s['chronology']=='L':
        t0=start_rng.uniform(72000,85000);box=(36,43.5,8,15.5);alt=2000
    else:
        t0=start_rng.uniform(47000,51000);box=(34.5,48,29.5,34);alt=1500
    seeds=np.flatnonzero((m._box(*box)&~m.water_mask(-40)&(m.ZMED<alt)).ravel())
    # The preparation product is cached outside the checkout and identified by
    # its grid/model hashes. lab.py hashes both before each resumed invocation.
    import os
    cache=Path(os.environ.get('ATLAS_OOA_CACHE',str(root.parent/'ooa-crossings-cache')))
    identity=__import__('hashlib').sha256((root/'code/model.py').read_bytes()+(root/'data/grid.npz').read_bytes()).hexdigest()
    target=cache/(identity+'.npz');cache.mkdir(parents=True,exist_ok=True)
    if target.exists():
        with np.load(target) as c:X=(c['ptr'],c['idx'],c['w'])
    else:
        X=m.build_crossings()
        import tempfile
        with tempfile.NamedTemporaryFile(dir=cache,suffix='.npz',delete=False) as f:tmp=f.name
        np.savez_compressed(tmp,ptr=X[0],idx=X[1],w=X[2]);os.replace(tmp,target)
    sahul=(((m.LON2>=131.5)&(m.LAT2<=0))|((m.LAT2<=-11.2)&(m.LON2>=121))).ravel()
    def region(lat,lon,r=2):
        i=int(np.argmin(abs(m.LAT-lat)));j=int(np.argmin(abs(m.LON-lon)))
        mask=np.zeros((m.NY,m.NX),bool);mask[max(0,i-r):i+r+1,max(0,j-r):j+r+1]=True
        return np.flatnonzero(mask.ravel())
    sites={'nefud':region(28,40.5,3),'lida':region(-.25,100.3),
           'sulawesi':np.r_[region(-5,119.7),region(-4.9,122.6)]}
    metrics={};arrivals={}
    for strategy in ('coastal','terrestrial','mixed'):
        arr,_,_=m.run(p,strategy,seeds,t0,noise,X)
        a={name:float(np.max(np.where(np.isfinite(arr[idx]),arr[idx],-np.inf))) for name,idx in sites.items()}
        a['sahul']=float(np.max(np.where(sahul&np.isfinite(arr),arr,-np.inf)))
        arrivals[strategy]=a
        metrics[strategy+'_reaches_sahul']=float(np.isfinite(a['sahul']))
        metrics[strategy+'_arrival_bp']=a['sahul'] if np.isfinite(a['sahul']) else None
        for omit in (None,'nefud','lida','sulawesi'):
            gates={'nefud':70000,'lida':63000,'sulawesi':67800}
            metrics[strategy+'_screen_omit_'+str(omit)]=float(all(a[k]>=v for k,v in gates.items() if k!=omit))
    reached=[k for k,v in arrivals.items() if np.isfinite(v['sahul'])]
    if reached:
        first=max(arrivals[k]['sahul'] for k in reached)
        winners=[k for k in reached if abs(arrivals[k]['sahul']-first)<1e-6]
        for k in arrivals:metrics[k+'_first_fractional_ties']=1/len(winners) if k in winners else 0.
    return dict(metrics=metrics,parameters=p,start_bp=float(t0),arrivals=arrivals,
                evidence_role='feasibility screens and prior/structural sensitivity; dates previously used in model design',
                limitation='1-2 km/year is a narrow sensitivity bracket, not an empirically estimated prior; no settlement/preservation/detection likelihood')


def trial(t,ooa_root=None):
    if t['family'] in RIGOR_TRIALS:return RIGOR_TRIALS[t['family']](t)
    if t['family']=='angkor' and t['settings'].get('engine')=='institutions':return institutions(t)
    if t['family'] in ('camchild','angkor','schools'):return node_trial(t)
    if t['family']=='ooa':return ooa(t,ooa_root)
    return {'credential':credential,'shadow':shadow,'youth':youth,'fertility':fertility}[t['family']](t)
