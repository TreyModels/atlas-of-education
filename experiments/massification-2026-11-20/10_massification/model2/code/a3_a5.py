"""A3 (PHL demand-pull) + A5 (PHL rival comparison) — observed cells; A3b simulated-labelled; no direction claim."""
import csv, math, os
import numpy as np, pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__)); M2=os.path.abspath(os.path.join(HERE,'..')); ROOT=os.path.abspath(os.path.join(M2,'..','..')); OUT=os.path.join(M2,'runs'); D=os.path.join(ROOT,'10_massification')
def nw(y,X,lag=2):
    X=np.column_stack([np.ones(len(X)),X]); b,*_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b; n,k=X.shape
    XtXi=np.linalg.pinv(X.T@X); S=np.zeros((k,k))
    for t in range(n): S+=np.outer(X[t]*e[t],X[t]*e[t])
    for l in range(1,lag+1):
        w=1-l/(lag+1)
        for t in range(l,n): S+=w*(np.outer(X[t]*e[t],X[t-l]*e[t-l])+np.outer(X[t-l]*e[t-l],X[t]*e[t]))
    V=XtXi@S@XtXi; return b,np.sqrt(np.maximum(np.diag(V),0)),e
def load():
    u=pd.read_csv(os.path.join(D,'data','UNIVERSALIZATION_SERIES.csv'))
    j=pd.read_csv(os.path.join(D,'data','JOBS_AND_MARKETS_PANEL.csv'))
    p=u[u['iso3']=='PHL']; pj=j[j['iso3']=='PHL']
    def ser(ind):
        z=p[p['indicator']==ind][['year','value']].dropna().sort_values('year')
        return z.set_index('year')['value']
    out={k:ser(k) for k in ['ger_secondary','ger_tertiary','ger_primary','completion_upper_secondary']}
    def js(name):
        z=pj[pj['indicator_name'].str.contains(name,case=False,na=False)][['year','value']].dropna().sort_values('year')
        return z.groupby('year')['value'].mean()
    out['remit']=js('Personal remittances, received \\(% of GDP\\)')
    out['gdppc']=js('GDP per capita \\(PPP')
    out['spend']=js('expenditure on education as a percentage of GDP')
    out['teachers_s']=js('Secondary education, teachers')
    out['services']=js('Employment in services')
    out['agri']=js('Employment in agriculture')
    return out
def main():
    S=load(); rows=[]
    # A3a remittances (observed)
    for name in ['ger_tertiary','ger_secondary','ger_primary']:
        y=S[name]; idx=y.index.intersection(S['remit'].index).intersection(S['gdppc'].index)
        idx=sorted(idx)
        if len(idx)<12: rows.append(dict(cell='A3a',outcome=name,status='UNABLE',beta=np.nan,se=np.nan,n=len(idx))); continue
        ly=np.log(y.loc[idx].values); lr=np.log(S['remit'].loc[idx].values); lg=np.log(S['gdppc'].loc[idx].values)
        tr=np.arange(len(idx),dtype=float)
        b,se,e=nw(ly,np.column_stack([lr,lg,tr]))
        # lead placebo: future remittances (t+3) vs current y
        lr_lead=np.log(S['remit'].shift(-3).loc[idx].values)
        ok=np.isfinite(lr_lead)
        b2,se2,_=nw(ly[ok],np.column_stack([lr_lead[ok],lg[ok],tr[ok]]))
        rows.append(dict(cell='A3a',outcome=name,beta=b[1],se=se[1],n=len(idx),lead_beta=b2[1],lead_se=se2[1]))
    # A3b simulated design only (labelled)
    rng=np.random.default_rng(11)
    sim=[]
    for field in ['nursing','placebo_edu','placebo_business']:
        base=rng.uniform(1000,5000); eff={'nursing':0.20,'placebo_edu':0.0,'placebo_business':0.0}[field]
        pre=[base*math.exp(rng.normal(0,0.04)) for _ in range(6)]
        post=[base*(1+eff)*math.exp(rng.normal(0,0.04)) for _ in range(6)]
        sim.append(dict(cell='A3b_SIMULATED',field=field,pre_mean=np.mean(pre),post_mean=np.mean(post),pct_change=(np.mean(post)/np.mean(pre)-1)*100))
    # A5 rivals
    rivals={
     'HC':lambda df: np.column_stack([np.log(df['gdppc']),np.log(df['gdppc']).shift(1)]),
     'world_culture':lambda df: np.arange(len(df),dtype=float),
     'labour_queue':lambda df: np.column_stack([df['ger_secondary'].shift(1),df['ger_tertiary'].shift(1)]),
     'state_building':lambda df: np.column_stack([df['spend'],df['teachers_s']]),
     'sectoral_demand':lambda df: np.column_stack([df['services'],df['agri'],df['remit']]),
    }
    def frame():
        idx=sorted(set(S['ger_secondary'].index)|set(S['ger_tertiary'].index))
        df=pd.DataFrame(index=idx)
        for k,v in S.items(): df[k]=v
        df['trend']=np.arange(len(df),dtype=float)
        return df
    df=frame(); r5=[]
    for out_name in ['ger_secondary','ger_tertiary']:
        d=df[['ger_secondary','ger_tertiary','gdppc','spend','teachers_s','services','agri','remit']].copy()
        d=d.dropna(subset=[out_name])
        fit=d[d.index<=2012]; test=d[d.index>=2013]
        if len(fit)<10 or len(test)<4: r5.append(dict(rival='ALL',outcome=out_name,status='UNABLE')); continue
        for rname,fn in rivals.items():
            try:
                Xf=fn(fit)
                if Xf.ndim==1: Xf=Xf.reshape(-1,1)
                ok=np.isfinite(Xf).all(1)&np.isfinite(fit[out_name].values)
                if ok.sum()<10: r5.append(dict(rival=rname,outcome=out_name,status='UNABLE fit coverage')); continue
                b,*_=np.linalg.lstsq(np.column_stack([np.ones(ok.sum()),Xf[ok]]),fit[out_name].values[ok],rcond=None)
                Xt=fn(test)
                if Xt.ndim==1: Xt=Xt.reshape(-1,1)
                ok2=np.isfinite(Xt).all(1)&np.isfinite(test[out_name].values)
                if ok2.sum()<3: r5.append(dict(rival=rname,outcome=out_name,status='UNABLE test coverage')); continue
                pred=np.column_stack([np.ones(ok2.sum()),Xt[ok2]])@b
                mae=float(np.mean(np.abs(pred-test[out_name].values[ok2])))
                rmse=float(np.sqrt(np.mean((pred-test[out_name].values[ok2])**2)))
                # event break: observed vs predicted change 2012->2016/2018/2024
                yrs=[y for y in [2012,2016,2018,2024] if y in test.index]
                obs_ch=float(test[out_name].loc[yrs[-1]]-test[out_name].loc[yrs[0]]) if yrs else np.nan
                ii=[i for i,y in enumerate(test.index[ok2]) if y in yrs]
                pr_ch=float(pred[ii[-1]]-pred[ii[0]]) if len(ii)>=2 else np.nan
                r5.append(dict(rival=rname,outcome=out_name,status='ok',n_fit=int(ok.sum()),n_test=int(ok2.sum()),
                               oos_mae=mae,oos_rmse=rmse,obs_change=obs_ch,pred_change=pr_ch,event_err=pr_ch-obs_ch if np.isfinite(pr_ch) and np.isfinite(obs_ch) else np.nan))
            except Exception as ex:
                r5.append(dict(rival=rname,outcome=out_name,status='FIT-FAIL '+str(ex)[:50]))
    R=pd.DataFrame(r5); R.to_csv(os.path.join(OUT,'a5_rivals.csv'),index=False)
    A=pd.DataFrame(rows); A.to_csv(os.path.join(OUT,'a3_remittances.csv'),index=False)
    pd.DataFrame(sim).to_csv(os.path.join(OUT,'a3b_simulated.csv'),index=False)
    L=['A3/A5 — PHL ANCHOR DEMAND-PULL + RIVAL COMPARISON (observed; A3b SIMULATED-labelled; no direction claim).','',
       'A3a remittances -> schooling (log-log, NW lag2, controls log GDPpc + trend):']
    for _,r in A.iterrows():
        L.append(f'  {r["outcome"]:34s} beta {r["beta"] if pd.notna(r["beta"]) else float("nan"):+8.3f} (se {r["se"] if pd.notna(r["se"]) else float("nan"):.3f}) n={r["n"]} lead_placebo beta {r["lead_beta"] if pd.notna(r["lead_beta"]) else float("nan"):+.3f} (t {abs(r["lead_beta"]/r["lead_se"]) if pd.notna(r["lead_se"]) and r["lead_se"]>0 else float("nan"):.2f})')
    L += ['','A3b nurse-visa design expectation (SIMULATED ONLY; E3 DATA BLOCKED; no claim):']
    for s in sim: L.append(f'  {s["field"]:18s} pre {s["pre_mean"]:.0f} post {s["post_mean"]:.0f} -> {s["pct_change"]:+.1f}%')
    L += ['','A3c BPO regional growth: DATA BLOCKED (no regional/BPO series; PSA blocked) — not run, not claimed.','',
          'A5 rivals fitted on PHL pre-2013, predicting 2013-2024 (observed only; no direction claim):']
    for out_name in ['ger_secondary','ger_tertiary']:
        z=R[(R['outcome']==out_name)&(R['status']=='ok')].sort_values('oos_mae')
        if len(z)==0: L.append(f'  {out_name}: UNABLE'); continue
        L.append(f'  {out_name}: best {z.iloc[0]["rival"]} MAE {z.iloc[0]["oos_mae"]:.2f} | second {z.iloc[1]["rival"] if len(z)>1 else "-"} '
                 f'MAE {z.iloc[1]["oos_mae"]:.2f}' + (f' | gap {z.iloc[1]["oos_mae"]-z.iloc[0]["oos_mae"]:.2f}' if len(z)>1 else ''))
        for _,r in z.iterrows():
            L.append(f'    {r["rival"]:16s} MAE {r["oos_mae"]:5.2f} RMSE {r["oos_rmse"]:5.2f} event-change obs {r["obs_change"]:+.1f} pred {r["pred_change"]:+.1f} err {r["event_err"]:+.1f}')
    L += ['','EQUIVALENT (R3) if best/second OOS MAE gap <=0.5pp and event-break gap <=0.5pp. No anchor-vs-rival claim (A1 pending).',
          'No direction claim (R13/EQUIVALENT); observed vs simulated labelled; no imputation. No git writes.']
    open(os.path.join(OUT,'a3_a5_findings.txt'),'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
    import json; json.dump(dict(A3a='observed remittances',A3b='SIMULATED only; E3 DATA BLOCKED; no claim',A3c='DATA BLOCKED',
                               A5='rival-only comparison; anchor comparison deferred to A1'),open(os.path.join(OUT,'a3_a5_meta.json'),'w'),indent=1)
if __name__=='__main__': main()
