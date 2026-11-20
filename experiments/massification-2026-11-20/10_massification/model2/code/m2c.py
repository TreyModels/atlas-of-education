"""M2c — E1 two-shock interaction estimator recovery test (SIMULATED; pre-registered in M2C_PREREG.md)."""
import csv, json, math, os
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); M2=os.path.abspath(os.path.join(HERE,'..')); OUT=os.path.join(M2,'runs')

def ols_cluster(X,y,g):
    X=np.column_stack([np.ones(len(X)),X]); b,*_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b
    XtXi=np.linalg.pinv(X.T@X); meat=np.zeros((X.shape[1],X.shape[1]))
    for u in np.unique(g):
        m=g==u; s=X[m].T@e[m]; meat+=np.outer(s,s)
    G=len(np.unique(g)); V=XtXi@meat@XtXi*(G/(G-1))
    return b, np.sqrt(np.maximum(np.diag(V),0))

def main():
    rows=[]
    for gamma in [-0.30, 0.0, 0.30]:
        for sigma in [0.5, 1.0]:
            for sim in range(100):
                rng=np.random.default_rng(7000+sim)
                N,T=30,10
                unit=np.repeat(np.arange(N),T); year=np.tile(np.arange(T),N)
                S=np.zeros(N*T); D=np.zeros(N*T)
                expo_s=rng.random(N)<0.5; expo_d=rng.random(N)<0.5
                for i in range(N):
                    for t in range(T):
                        k=i*T+t
                        S[k]=1.0 if (expo_s[i] and t>=4) else 0.0
                        D[k]=1.0 if (expo_d[i] and t>=5) else 0.0
                alpha=np.repeat(rng.normal(0,0.5,N),T); lam=np.tile(rng.normal(0,0.3,T),N)
                eps=rng.normal(0,sigma,N*T)
                Y=alpha+lam+0.5*S+0.3*D+gamma*S*D+eps
                X=np.column_stack([S,D,S*D])
                # absorb unit+year FE via within transform (two-way demeaning is approximate; use dummies for exactness)
                Ud=np.kron(np.eye(N),np.ones((T,1))); Td=np.kron(np.ones((N,1)),np.eye(T))
                Xf=np.column_stack([S,D,S*D,Ud[:,1:],Td[:,1:]])
                b,se=ols_cluster(Xf,Y,unit)
                gh,seh=b[1],se[1]; tstat=gh/max(seh,1e-9)
                cover=(gh-1.645*seh)<=gamma<=(gh+1.645*seh)
                rows.append(dict(gamma=gamma,sigma=sigma,sim=sim,ghat=gh,se=seh,t=tstat,cover=bool(cover)))
    import pandas as pd
    R=pd.DataFrame(rows); R.to_csv(os.path.join(OUT,'m2c_recovery.csv'),index=False)
    def summ(g,s):
        z=R[(R['gamma']==g)&(R['sigma']==s)]
        if g==0: return dict(false_pos=float((z['t'].abs()>1.96).mean()), cover=float(z['cover'].mean()), bias=np.nan)
        return dict(false_pos=np.nan, cover=float(z['cover'].mean()),
                    bias=float(np.median(np.abs(z['ghat']-g)/abs(g))),
                    sign=float((np.sign(z['ghat'])==np.sign(g)).mean()))
    lines=['M2c — E1 TWO-SHOCK INTERACTION ESTIMATOR RECOVERY (SIMULATED; pre-registered before running)',
           'DGP: 30 provinces x 10y; Y=a_i+l_t+0.5S+0.3D+gamma*S*D+eps; gamma in {-0.30,0,+0.30}; sigma in {0.5,1.0}; 100 sims/cell.',
           'Estimator: two-way FE OLS with unit+year dummies, CR1 cluster by unit; estimand gamma.','',
           f'  {"gamma":>6s} {"sigma":>6s} {"sign acc":>9s} {"median|bias|":>12s} {"90% cover":>10s} {"null FP":>8s}']
    low=[]; 
    for g in [-0.30,0.0,0.30]:
        for s in [0.5,1.0]:
            d=summ(g,s)
            lines.append(f'  {g:+6.2f} {s:6.1f} {d.get("sign",float("nan")):9.2f} {d.get("bias",float("nan")):12.2f} {d["cover"]:10.2f} {d.get("false_pos",float("nan")):8.2f}')
            if s==0.5: low.append((g,d))
    lo=np.array([d for g,d in low])
    sign_ok = all(d.get('sign',0)>=0.67 for g,d in low if g!=0)
    bias_ok = all(d.get('bias',9)<=0.50 for g,d in low if g!=0)
    cover_ok = all(d['cover']>=0.67 for g,d in low)
    fp_ok = all(d.get('false_pos',9)<=0.10 for g,d in low if g==0)
    suff = sign_ok and bias_ok and cover_ok and fp_ok
    lines += ['', 'Predeclared sufficiency rule (low-noise sigma=0.5): sign accuracy >=0.67 for both signs, median |bias| <=0.50,',
              '90% CI coverage >=0.67, null false-positive rate <=0.10.',
              f'  sign_ok={sign_ok} bias_ok={bias_ok} cover_ok={cover_ok} nullFP_ok={fp_ok}',
              f'  -> E1 {"SUFFICIENT (recovery passes)" if suff else "NOT SUFFICIENT — E1 cannot be fielded as the identification gate without a power fix"}',
              '  High-noise sigma=1.0 row is the power stress (PATRINOS underpowered warning); see table.']
    open(os.path.join(OUT,'m2c_findings.txt'),'w').write('\n'.join(lines)+'\n'); print('\n'.join(lines))
    json.dump(dict(sufficient=bool(suff), sign_ok=sign_ok, bias_ok=bias_ok, cover_ok=cover_ok, null_fp_ok=fp_ok,
                   cells=[{'gamma':g,'sigma':s, **{k:(float(v) if isinstance(v,(int,float,np.floating)) and v==v else None) for k,v in summ(g,s).items()}} for g in [-0.3,0,0.3] for s in [0.5,1.0]]),
              open(os.path.join(OUT,'m2c_meta.json'),'w'), indent=1)

if __name__=='__main__': main()
