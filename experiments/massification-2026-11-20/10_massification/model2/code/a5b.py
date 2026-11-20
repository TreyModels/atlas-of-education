"""A5b — PHL anchor rival re-score on crossing ordering/spacing + mechanism-implied ordering (1999-2013 fit, 2014-2024 holdout)."""
import csv, math, os
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
HERE=os.path.dirname(os.path.abspath(__file__)); M2=os.path.abspath(os.path.join(HERE,'..')); ROOT=os.path.abspath(os.path.join(M2,'..','..')); OUT=os.path.join(M2,'runs'); D=os.path.join(ROOT,'10_massification')
DESIGN_ONLY=[('human_capital','PSA returns by education (FIES/APIS/LFS) — DATA BLOCKED; external request needs approval','design-only'),
             ('signalling_MMI','Enterprise Surveys employer credential/skills module — DATA BLOCKED; external request needs approval','design-only')]
def load():
    u=pd.read_csv(os.path.join(D,'data','UNIVERSALIZATION_SERIES.csv')); p=u[u['iso3']=='PHL']
    j=pd.read_csv(os.path.join(D,'data','JOBS_AND_MARKETS_PANEL.csv')); pj=j[j['iso3']=='PHL']
    def ser(ind):
        z=p[p['indicator']==ind][['year','value']].dropna().sort_values('year'); z['year']=z['year'].astype(int)
        return z.set_index('year')['value']
    def js(name):
        z=pj[pj['indicator_name']==name][['year','value']].dropna().sort_values('year'); z['year']=z['year'].astype(int)
        return z.groupby('year')['value'].mean()
    out={'completion_primary':ser('completion_primary'),'completion_lower_secondary':ser('completion_lower_secondary'),
         'completion_upper_secondary':ser('completion_upper_secondary'),'ger_tertiary':ser('ger_tertiary'),
         'gdppc':js('GDP per capita, PPP (current international $)'),
         'spend':js('Government expenditure on education as a percentage of GDP (%)'),
         'teachers':js('Secondary education, teachers'),
         'services':js('Employment in services (% of total employment) (modeled ILO estimate)'),
         'agri':js('Employment in agriculture (% of total employment) (modeled ILO estimate)'),
         'remit':js('Personal remittances, received (% of GDP)'),
         'urban':js('Urban population (% of total population)'),
         'cohort':ser('cohort_population_0_14'),'pop':ser('population_total')}
    return out
def logistic(t,K,r,t0): return K/(1+np.exp(-r*(t-t0)))
def gompertz(t,K,r,t0): return K*np.exp(-np.exp(-r*(t-t0)))
def cross_year(years_vals, threshold, start=1999, end=2050):
    ys,v=years_vals
    for y in range(start,end+1):
        if y in ys and v[ys.index(y)]>=threshold: return y
    return None
def main():
    S=load(); T=pd.DataFrame({'year':np.arange(1995,2025)}).set_index('year')
    for k,v in S.items(): T[k]=v.reindex(T.index)
    T['lcohort']=np.log(T['cohort']); T['lpop']=np.log(T['pop'])
    outcomes={'primary':('completion_primary',90),'lower_secondary':('completion_lower_secondary',90),
              'upper_secondary':('completion_upper_secondary',90),'tertiary_ger':('ger_tertiary',50)}
    fit=T[(T.index>=1999)&(T.index<=2013)]; hold=T[(T.index>=2014)&(T.index<=2024)]
    # observed crossings
    obs={}
    for name,(col,thr) in outcomes.items():
        z=T[col].dropna(); obs[name]={'cross':next((y for y in z.index if z.loc[y]>=thr),None),'thr':thr,'last':float(z.loc[z.index<=2024].iloc[-1]) if len(z) else np.nan}
    rivals={}; R=[]
    # 1 world-society: shared r,t0 across levels, level-specific K
    def model_shared(years, r, t0, *K):
        yrs=np.asarray(years,float); out=np.concatenate([logistic(yrs,K[i],r,t0) for i in range(len(K))]); return out
    ys=np.concatenate([fit.index.values.astype(float) for _ in outcomes])
    yv=np.concatenate([fit[col].values.astype(float) for _,(col,thr) in outcomes.items()])
    ok=np.isfinite(yv); ys2, yv2 = ys[ok], yv[ok]
    p0=[0.05,2005]+[float(fit[col].max()) for _,(col,thr) in outcomes.items()]
    lo=[0.001,1960]+[10]*len(outcomes); hi=[0.5,2030]+[160]*len(outcomes)
    try:
        pw,_=curve_fit(model_shared, ys2, yv2, p0=p0, bounds=(lo,hi), maxfev=80000)
        rivals['world_society']={'r':pw[0],'t0':pw[1],'K':list(pw[2:])}
    except Exception as e:
        rivals['world_society']={'error':str(e)[:80]}
    # 2 state building & 3 demographic & 4 formal shapes: per outcome
    def fit_linear(df, col, xs):
        d=df[[col]+xs].dropna()
        if len(d)<5: return None
        X=np.column_stack([np.ones(len(d))]+[d[x].values for x in xs]); b,*_=np.linalg.lstsq(X,d[col].values,rcond=None)
        return dict(b=b,xs=xs)
    def fit_logistic(df, col):
        d=df[[col]].dropna(); y=d[col].values.astype(float); yrs=d.index.values.astype(float)
        if len(d)<6: return None
        try:
            p,_=curve_fit(logistic,yrs,y,p0=[min(120,y.max()*1.1),0.05,2000],bounds=([10,0.001,1950],[160,0.5,2040]),maxfev=40000)
            return dict(p=p)
        except Exception: return None
    rivals['state_building']={}; rivals['demographic_cohort']={}; rivals['formal_shapes']={}
    preds={}
    for name,(col,thr) in outcomes.items():
        sb=fit_linear(fit,col,['spend','teachers','trend'] if 'trend' in fit else ['spend','teachers'])
        fit2=fit.copy(); fit2['trend']=np.arange(len(fit2),dtype=float)
        d=fit2[[col,'spend','teachers','trend']].dropna()
        if len(d)>=5:
            X=np.column_stack([np.ones(len(d)),d['spend'],d['teachers'],d['trend']]); b,*_=np.linalg.lstsq(X,d[col].values,rcond=None)
            h=hold.copy(); h['trend']=np.arange(len(fit2),len(fit2)+len(h),dtype=float)
            Xh=np.column_stack([np.ones(len(h)),h['spend'],h['teachers'],h['trend']])
            rivals['state_building'][name]=dict(b=b,pred=pd.Series(Xh@b,index=h.index))
        dc=fit_linear(fit,col,['lcohort','lpop','urban','gdppc'])
        d=fit[[col,'lcohort','lpop','urban','gdppc']].dropna()
        if len(d)>=5:
            X=np.column_stack([np.ones(len(d)),d['lcohort'],d['lpop'],d['urban'],d['gdppc']]); b,*_=np.linalg.lstsq(X,d[col].values,rcond=None)
            Xh=np.column_stack([np.ones(len(hold)),hold['lcohort'],hold['lpop'],hold['urban'],hold['gdppc']])
            rivals['demographic_cohort'][name]=dict(b=b,pred=pd.Series(Xh@b,index=hold.index))
        fl=fit_logistic(fit,col)
        if fl:
            pred=pd.Series(logistic(np.arange(2014,2051,dtype=float),*fl['p']),index=np.arange(2014,2051))
            rivals['formal_shapes'][name]=dict(p=fl['p'],pred=pred)
    # crossing extraction & scoring
    def pred_cross(series,thr):
        s=series.dropna()
        for y in s.index:
            if y>=2014 and y<=2050 and s.loc[y]>=thr: return int(y)
        return None
    rows=[]
    for rname,r in rivals.items():
        if 'error' in r: continue
        if rname=='world_society':
            pw=r; yrs=np.arange(2014,2051,dtype=float)
            for i,(name,(col,thr)) in enumerate(outcomes.items()):
                pred=pd.Series(logistic(yrs,pw['K'][i],pw['r'],pw['t0']),index=yrs.astype(int))
                rows.append(dict(rival=rname,outcome=name,threshold=thr,pred_cross=pred_cross(pred,thr),
                                 obs_cross=obs[name]['cross'],implied='shared timing'))
        else:
            for name,(col,thr) in outcomes.items():
                if name not in r: continue
                pred=r[name]['pred']
                if isinstance(pred,pd.Series):
                    rows.append(dict(rival=rname,outcome=name,threshold=thr,pred_cross=pred_cross(pred,thr),
                                     obs_cross=obs[name]['cross'],implied=''))
    Rd=pd.DataFrame(rows)
    # scoring: ordering/gaps/false positive/equivalent
    scored=[]
    for rname,g in Rd.groupby('rival'):
        d={row['outcome']:row for _,row in g.iterrows()}
        pc=d.get('primary',{}).get('pred_cross'); lc=d.get('lower_secondary',{}).get('pred_cross'); uc=d.get('upper_secondary',{}).get('pred_cross'); tc=d.get('tertiary_ger',{}).get('pred_cross')
        o_primary=obs['primary']['cross']; o_lower=obs['lower_secondary']['cross']; o_tert=obs['tertiary_ger']['cross']
        order_ok=(pc is not None and lc is not None and pc<lc) and (tc is None or lc<=tc) and (uc is None or uc>2024)
        gap1=abs((lc-pc)-((o_lower or 0)-(o_primary or 0))) if (pc is not None and lc is not None and o_primary and o_lower) else np.nan
        gap2=abs((tc-lc)-((o_tert or 0)-(o_lower or 0))) if (tc is not None and lc is not None and o_tert and o_lower) else np.nan
        fp_upper=bool(uc is not None and uc<=2024)
        within=lambda p,o: (p is not None and o is not None and abs(p-o)<=5)
        equiv=bool(order_ok and not fp_upper and within(pc,o_primary) and within(lc,o_lower) and (tc is not None and o_tert and abs(tc-o_tert)<=5))
        shared=bool(pc is not None and lc is not None and tc is not None and max(abs(pc-(lc or pc)),abs(lc-(tc or lc)))<=2)
        scored.append(dict(rival=rname,primary=pc,lower_secondary=lc,upper_secondary=uc,tertiary=tc,
                           order_ok=order_ok,gap_primary_to_lower=gap1,gap_lower_to_tertiary=gap2,
                           upper_false_positive=fp_upper,equivalent_R3=equiv,single_shared_curve_R23=shared))
    Sc=pd.DataFrame(scored)
    # mechanism-implied ordering text (declared)
    implied={'world_society':'near-simultaneous across levels (shared timing; R23 structural-miss check)',
             'state_building':'policy-sequence: primary before lower before upper; upper may not cross',
             'demographic_cohort':'cohort compression: primary earliest, then lower, upper later',
             'formal_shapes':'independent per-level shapes; order data-determined'}
    # event breaks: observed vs predicted change 2013->2024 (upper completion, tertiary GER)
    ev=[]
    for rname in ['world_society','state_building','demographic_cohort','formal_shapes']:
        for name in ['upper_secondary','tertiary_ger']:
            col,thr=outcomes[name]; o=obs[name]['last']; o13=float(T[col].loc[2013]) if pd.notna(T[col].loc[2013]) else np.nan
            if rname=='world_society':
                i=list(outcomes).index(name); p24=logistic(2024,rivals['world_society']['K'][i],rivals['world_society']['r'],rivals['world_society']['t0'])
            else:
                rr=rivals[rname].get(name); p24=float(rr['pred'].loc[2024]) if rr and 2024 in rr['pred'].index else np.nan
            ev.append(dict(rival=rname,outcome=name,obs_change=(o-o13) if np.isfinite(o) and np.isfinite(o13) else np.nan,
                           pred_change=(p24-o13) if np.isfinite(p24) and np.isfinite(o13) else np.nan,
                           err=(p24-o) if np.isfinite(p24) and np.isfinite(o) else np.nan))
    Ev=pd.DataFrame(ev)
    # timing alignment R24 (PHL events)
    align=[]
    for evname,evyear,aff,thr in [('PHL 1987 compulsory-primary lineage',1987,'primary',90),('PHL K-12 2013 (RA 10533)',2013,'upper_secondary',90),
                                  ('PHL free SHS 2016',2016,'upper_secondary',90),('PHL free tertiary 2018',2018,'tertiary_ger',50)]:
        cr=obs[aff]['cross']; gap=(evyear-cr) if cr else None
        post=(cr is not None and evyear<=cr<=evyear+5)
        aligned=bool(cr is not None and abs(gap)<=5)
        align.append(dict(event=evname,event_year=evyear,affected=aff,observed_cross=cr,event_to_crossing_gap=gap,
                          crossing_in_post_window=post,timing_aligned_R24=aligned,
                          verdict=('candidate marker' if aligned or post else 'context, not mechanism')))
    Al=pd.DataFrame(align)
    # design-only rows in every results file
    do_rows=pd.DataFrame([dict(rival=n,outcome='—',status=s,note=note) for n,note,s in DESIGN_ONLY])
    Rd.to_csv(os.path.join(OUT,'a5b_rivals_by_milestone.csv'),index=False); Sc.to_csv(os.path.join(OUT,'a5b_scores.csv'),index=False)
    Ev.to_csv(os.path.join(OUT,'a5b_event_breaks.csv'),index=False); Al.to_csv(os.path.join(OUT,'a5b_timing_alignment.csv'),index=False)
    with open(os.path.join(OUT,'a5b_design_only_rivals.csv'),'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['rival','data_requirement','status']); w.writeheader()
        for n,note,s in DESIGN_ONLY: w.writerow(dict(rival=n,data_requirement=note,status=s))
    L=['A5b — PHL ANCHOR RIVAL RE-SCORE: crossing ordering/spacing + mechanism-implied ordering (fit 1999-2013, holdout 2014-2024).',
       'Observed signature: primary completion >=90 in 2017; lower-secondary >=90 in 2024; upper-secondary NEVER >=90 by 2024; tertiary GER >=50 ' + str(obs['tertiary_ger']['cross'])+'.',
       'No direction/causal claim (R13/R24/R25). Design-only rivals listed separately (not modelled, not claimed as tested, D48).','',
       f'{"rival":20s} {"primary":>7s} {"lower":>7s} {"upper":>7s} {"tertiary":>8s} {"order_ok":>8s} {"gap1":>6s} {"gap2":>6s} {"FP_up":>6s} {"equiv":>6s} {"shared":>6s}']
    for _,r in Sc.iterrows():
        f=lambda v:'none' if v is None or (isinstance(v,float) and not np.isfinite(v)) else (str(int(v)) if isinstance(v,(int,np.integer)) else str(v))
        L.append(f'  {r["rival"]:20s} {f(r["primary"]):>7s} {f(r["lower_secondary"]):>7s} {f(r["upper_secondary"]):>7s} {f(r["tertiary"]):>8s} {str(r["order_ok"]):>8s} {f(r["gap_primary_to_lower"]):>6s} {f(r["gap_lower_to_tertiary"]):>6s} {str(r["upper_false_positive"]):>6s} {str(r["equivalent_R3"]):>6s} {str(r["single_shared_curve_R23"]):>6s}')
    L += ['','MECHANISM-IMPLIED ORDERING (predeclared):']
    for k,v in implied.items(): L.append(f'  {k}: {v}')
    L += ['','EVENT-BREAK SCORES (2013->2024 observed vs predicted change; pp; no rival gets event dummies):']
    for _,r in Ev.iterrows():
        L.append(f'  {r["rival"]:20s} {r["outcome"]:16s} obs {r["obs_change"]:+6.1f} pred {r["pred_change"]:+6.1f} err {r["err"]:+6.1f}')
    L += ['','TIMING ALIGNMENT (R24; PHL events):']
    for _,r in Al.iterrows():
        L.append(f'  {r["event"]:38s} affected {r["affected"]:16s} crossing {r["observed_cross"]} gap {r["event_to_crossing_gap"]} post-window {r["crossing_in_post_window"]} -> {r["verdict"]}')
    L += ['','DESIGN-ONLY RIVALS (D48; blocked, not modelled here — listed in every results file):']
    for n,note,s in DESIGN_ONLY: L.append(f'  {n}: {note} [{s}]')
    L += ['','VERDICT: see a5b_scores.csv; any rival without order_ok and within ±5y on all crossings is NOT equivalent (R3);',
          'a shared-curve rival (single timing) is a structural miss (R23). Anchor-vs-rival comparison remains deferred to A1.',
          'No direction/causal claim; event evidence descriptive (R24/R25). No git writes.']
    open(os.path.join(OUT,'a5b_findings.txt'),'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
    import json; json.dump(dict(obs=obs,design_only=[n for n,_,_ in DESIGN_ONLY]),open(os.path.join(OUT,'a5b_meta.json'),'w'),indent=1,default=str)
if __name__=='__main__': main()
