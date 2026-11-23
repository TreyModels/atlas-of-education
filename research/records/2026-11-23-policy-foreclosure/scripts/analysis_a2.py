import json, sys, os
sys.path.insert(0,"/root/work/policy_foreclosure/scripts")
import numpy as np, pf_common as pc
df=pc.panel(); TFR={(r.iso,r.year):r.fertility for r in df.itertuples() if np.isfinite(r.fertility)}
EV=json.load(open("/root/work/policy_foreclosure/data/events.json")); EV=EV[0] if isinstance(EV,list) else EV
out=[]
for e in EV["events"]:
    i,y=e["iso"],e["year"]
    if TFR.get((i,y)) is None: continue
    if TFR[(i,y)]>=1.6: continue
    yrs=[yy for yy in range(y,2024) if (i,yy) in TFR]
    vals=[TFR[(i,yy)] for yy in yrs]
    run=mx=0; start=None; best=None
    for yy,v in zip(yrs,vals):
        if v>1.6:
            run+=1
            if run==1: start=yy
            if run>mx: mx=run; best=(start,yy)
        else: run=0
    out.append(dict(iso=i,intro=y,tfr_intro=TFR[(i,y)],tfr_2023=TFR.get((i,2023)),
                    max_post=float(np.nanmax(vals)),longest_run=mx,run_span=best,
                    any_above=bool(mx>0)))
long=[o for o in out if o["longest_run"]>=3]
print("events with a run >=3 consecutive years >1.6 at ANY time after introduction (not just 10y):",len(long),"of",len(out))
for o in sorted(long,key=lambda o:-o["longest_run"]):
    print("  %s intro %d TFR_intro %.2f -> max %.2f, longest run %d yrs %s, TFR2023 %s" % (
        o["iso"],o["intro"],o["tfr_intro"],o["max_post"],o["longest_run"],o["run_span"],o["tfr_2023"]))
json.dump(out, open("/root/work/policy_foreclosure/out/A2_longrun.json","w"), indent=1)
