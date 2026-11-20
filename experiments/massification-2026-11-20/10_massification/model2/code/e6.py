"""E6 — independent timing comparison for universalization milestones (observed only; no direction claim)."""
import csv, json, math, os
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
HERE=os.path.dirname(os.path.abspath(__file__)); M2=os.path.abspath(os.path.join(HERE,'..')); ROOT=os.path.abspath(os.path.join(M2,'..','..')); OUT=os.path.join(M2,'runs')
D=os.path.join(ROOT,'10_massification')
def logistic(t,K,r,t0): return K/(1+np.exp(-r*(t-t0)))
def gompertz(t,K,r,t0): return K*np.exp(-np.exp(-r*(t-t0)))
def linear(t,a,b): return a+b*t
def exponential(t,a,r): return a*np.exp(r*t)
FORMS={'logistic':(logistic,[50,0.05,1990],[1,0.001,1850],[200,0.5,2100]),
       'gompertz':(gompertz,[50,0.05,1990],[1,0.001,1850],[200,0.5,2100]),
       'linear':(linear,[0,1],[0,-100],[200,100]),
       'exponential':(exponential,[1,0.01],[1e-6,-1],[300,1])}
def get_series(u,iso3,series):
    z=u[(u['iso3']==iso3)&(u['indicator']==series)][['year','value']].dropna().sort_values('year')
    if len(z): return z['year'].values.astype(float), z['value'].values.astype(float)
    if series.startswith('in_school_'):
        ind='oos_'+series.replace('in_school_','',1)
        z=u[(u['iso3']==iso3)&(u['indicator']==ind)][['year','value']].dropna().sort_values('year')
        if len(z): return z['year'].values.astype(float), 100.0-z['value'].values.astype(float)
    return None,None
def main():
    t=pd.read_csv(os.path.join(D,'relations','data','UNIVERSALIZATION_TIMING.csv'))
    u=pd.read_csv(os.path.join(D,'data','UNIVERSALIZATION_SERIES.csv'))
    rows=[]; scored=[]
    for (iso3,level),g in t.groupby(['iso3','level']):
        g=g.sort_values('priority')
        g2=g[(g['reconstructed']!=True)]
        if not len(g2): g2=g
        cand=g2[g2['status'].isin(['crossed','censored_above_at_first_obs','not_crossed_by_last_obs'])]
        if not len(cand): continue
        r=cand.iloc[0]
        yrs,vals=get_series(u,iso3,str(r['series']))
        status=r['status']; thr=float(r['threshold_pct'])
        if yrs is None or len(yrs)<5:
            for f in FORMS: rows.append(dict(iso3=iso3,level=level,form=f,status=status,verdict='UNABLE',
                                             observed_mid=r['crossing_mid'],pred=np.nan,err=np.nan,tol=np.nan,note='series missing'))
            continue
        if status=='crossed' and pd.notna(r['crossing_lo']):
            fitmask=yrs < float(r['crossing_lo'])
        elif status=='crossed':
            fitmask=np.ones(len(yrs),bool)
        else:
            fitmask=np.ones(len(yrs),bool)  # censored/not-crossed: use full observed window (no crossing to hold out)
        fy,fv=yrs[fitmask],vals[fitmask]
        tol=3.0 if (pd.notna(r['interval_width_years']) and float(r['interval_width_years'])<=2) else 5.0
        for f,(fn,p0,lo,hi) in FORMS.items():
            rec=dict(iso3=iso3,level=level,form=f,status=status,observed_mid=r['crossing_mid'],tol=tol,
                     n_fit=int(len(fy)),note='')
            if len(fy)<8:
                rec.update(verdict='UNABLE',pred=np.nan,err=np.nan,note='<8 pre-crossing obs'); rows.append(rec); continue
            try:
                p,_=curve_fit(fn,fy,fv,p0=p0,maxfev=40000,bounds=(lo,hi))
            except Exception as e:
                rec.update(verdict='FIT-FAIL',pred=np.nan,err=np.nan,note=str(e)[:60]); rows.append(rec); continue
            # predicted crossing year: first integer year >= max(fy) (or 1850) with curve >= thr
            pred=None
            for y in range(int(max(fy)), int(max(fy))+301):
                try:
                    v=float(fn(y,*p))
                except Exception:
                    v=np.nan
                if np.isfinite(v) and v>=thr:
                    pred=y; break
            if status=='not_crossed_by_last_obs':
                last=max(yrs)
                fp=(pred is not None and pred<=last)
                rec.update(pred=pred,err=np.nan,verdict='FALSE-CROSSING' if fp else 'NO-CROSSING-OK')
                rows.append(rec)
            elif status=='censored_above_at_first_obs':
                first=min(yrs)
                rec.update(pred=pred,err=np.nan,verdict='LEFT-CENSORED',
                           note=('fit crosses at/before first obs' if (pred is not None and pred<=first) else 'fit crosses after first obs (descriptive only)'))
                rows.append(rec)
            else:
                mid=float(r['crossing_mid']); err=(pred-mid) if pred is not None else np.nan
                rec.update(pred=pred,err=err)
                if pred is None: rec['verdict']='NO-PRED-CROSSING'
                elif abs(err)<=tol: rec['verdict']='PASS'
                elif abs(err)<=2*tol: rec['verdict']='PARTIAL'
                else: rec['verdict']='FAIL'
                rows.append(rec); scored.append(rec)
    R=pd.DataFrame(rows); R.to_csv(os.path.join(OUT,'e6_timing_independent.csv'),index=False)
    # aggregate conforming decision rule
    S=R[R['verdict'].isin(['PASS','PARTIAL','FAIL','NO-PRED-CROSSING'])]
    lines=['E6 — INDEPENDENT TIMING COMPARISON (observed only; crossing = holdout; no direction claim).',
           'Data: UNIVERSALIZATION_TIMING.csv (bands) + UNIVERSALIZATION_SERIES.csv (observed); reconstructed excluded from primary.','']
    agg={}
    for f in ['logistic','gompertz','linear','exponential']:
        z=S[S['form']==f]
        npc=z[z['verdict']=='PASS']
        nocross=R[(R['form']==f)&(R['status']=='not_crossed_by_last_obs')]
        false_cross=int((nocross['verdict']=='FALSE-CROSSING').sum())
        agg[f]=dict(scored=len(z),pass_=len(npc),median_abs_err=float(np.nanmedian(np.abs(z['err']))) if z['err'].notna().any() else np.nan,
                    false_cross=false_cross)
        lines.append(f'  {f:12s} scored {len(z):2d} | PASS {len(npc):2d} | median |err| '
                     f'{agg[f]["median_abs_err"] if np.isfinite(agg[f]["median_abs_err"]) else float("nan"):5.1f}y | false crossings {false_cross}')
    bounded=[f for f in ['logistic','gompertz'] if agg[f]['scored']>0 and agg[f]['pass_']/max(agg[f]['scored'],1)>=2/3 and agg[f]['false_cross']==0]
    passed=bool(bounded)
    lines += ['',f'PREDECLARED RULE: timing reproduced iff >=2/3 scored PASS for a bounded form AND 0 false crossings.',
              f'  -> E6 timing {"REPRODUCED by "+"/".join(bounded) if passed else "FAIL = STRUCTURAL TIMING MISS (R19); cycle closes PARTIAL+EQUIVALENT with explicit timing miss (D36)"}','',
              'Per-milestone table (primary rows):']
    for _,r in R[R['form'].isin(['logistic','gompertz'])].iterrows():
        lines.append(f'  {r["iso3"]:4s} {r["level"]:26s} {r["form"]:9s} obs {r["observed_mid"]} pred {r["pred"]} '
                     f'err {r["err"]} tol +/-{r["tol"]} -> {r["verdict"]}')
    # comparison with scout
    sc=os.path.join(D,'relations','data','e6_timing_comparison.csv')
    if os.path.exists(sc):
        S2=pd.read_csv(sc)
        lines += ['', 'SCOUT COMPARISON (cell-level, same iso3/level/form where both define a predicted crossing):']
        n=0; agree=0
        for _,x in S2.iterrows():
            m=R[(R['iso3']==x['iso3'])&(R['level']==x['level'])&(R['form']==x['form'])]
            if len(m) and pd.notna(x['timing_error_years']) and m.iloc[0]['form'] in FORMS and pd.notna(m.iloc[0]['err']):
                n+=1; agree += 1 if abs(float(x['timing_error_years'])-float(m.iloc[0]['err']))<=1.0 else 0
        lines.append(f'  comparable cells: {n}; agree within 1y: {agree} ({agree/max(n,1):.0%})')
    open(os.path.join(OUT,'e6_findings.txt'),'w').write('\n'.join(lines)+'\n'); print('\n'.join(lines))
    json.dump(dict(decision=('reproduced' if passed else 'structural timing miss (R19)'), bounded_forms=bounded,
                   aggregate=agg, scored_milestones=int(len(S))), open(os.path.join(OUT,'e6_meta.json'),'w'), indent=1)
if __name__=='__main__': main()
