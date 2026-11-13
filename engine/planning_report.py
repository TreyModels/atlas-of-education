"""Run: python engine/planning_report.py; writes a reproducible accounting report."""
import json,time,hashlib
from pathlib import Path
from countries import cambodia,philippines,china
from eduengine import planning_audit
from eduengine.planning import KERNEL
out={'kernel_sha256':hashlib.sha256(KERNEL.read_bytes()).hexdigest(),'seed':7,'N':400,'T':50,'countries':{}}
for c in (cambodia,philippines,china):
    start=time.perf_counter();E=c.make(seed=7,N=400,T=50);E.run();run=time.perf_counter()-start
    start=time.perf_counter();r=planning_audit(E);r['auditSeconds']=time.perf_counter()-start;r['engineSeconds']=run
    out['countries'][c.__name__.split('.')[-1]]=r
p=Path(__file__).resolve().parents[1]/'results'/'planning_audit.json';p.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
for c,r in out['countries'].items():
    print(c, 'salary residual',r['maximumSalaryIdentityResidual'],'staffing gap years',r['yearsBelowTargetStaffing'],'audit seconds',round(r['auditSeconds'],4))
print(p)
