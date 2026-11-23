import csv, numpy as np
OUT="/root/work/care_cred"
def num(x):
    try:
        v=float(x); return v if np.isfinite(v) else np.nan
    except Exception: return np.nan
cs=list(csv.DictReader(open(f"{OUT}/panel_cross_section.csv")))
att=np.array([num(r.get("edu_ter_f","")) for r in cs]); isco=np.array([num(r.get("isco12_f","")) for r in cs])
tfr=np.array([num(r.get("tfr","")) for r in cs]); gap=att-isco
m=np.isfinite(att)&np.isfinite(isco)&np.isfinite(tfr)
print("n =", int(m.sum()))
print("corr(tfr, attainment) = %+.3f" % np.corrcoef(tfr[m],att[m])[0,1])
print("corr(tfr, isco12)     = %+.3f" % np.corrcoef(tfr[m],isco[m])[0,1])
print("corr(tfr, gap)        = %+.3f" % np.corrcoef(tfr[m],gap[m])[0,1])
print("corr(att, isco12)     = %+.3f" % np.corrcoef(att[m],isco[m])[0,1])
print("means: att %.1f isco %.1f gap %.1f tfr %.2f" % (att[m].mean(), isco[m].mean(), gap[m].mean(), tfr[m].mean()))
# simple bivariate slopes (standardised) for the three, to check signs
for lab,x in (("attainment",att),("isco12",isco),("gap",gap)):
    b=np.polyfit((x[m]-x[m].mean())/x[m].std(),(tfr[m]-tfr[m].mean())/tfr[m].std(),1)[0]
    print("  standardised slope tfr on %-10s = %+.3f" % (lab,b))
