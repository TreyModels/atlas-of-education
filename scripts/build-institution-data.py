"""Compile exact Python trajectories for the browser stored-run explorer.
Usage: python3 scripts/build-institution-data.py HANDOFF_UNPACKED MAINTENANCE_DIR
Inputs are explicit paths; generated series never substitute JS random numbers.
"""
import sys,importlib.util,json,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1];source=pathlib.Path(sys.argv[1]).resolve();repair=pathlib.Path(sys.argv[2]).resolve();sys.path.insert(0,str(repair))
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
fixed=module('timing_fixed',repair/'timing_fixed.py');accounted=module('accounted',repair/'accounted.py');flight=module('flight',source/'angkor_scott_flight_v02/angkor_scott_flight_v02.py')
data={'columns':['year','state','refuge','total','canal','shortfall'],'models':{}}
def pack(h,fields):return [[round(float(r[k]),6) if k else None for k in fields] for r in h]
for name,m in [('maintenance',fixed),('accounts',accounted)]:
 groups={}
 for climate in ['normal','drought']:
  for regime in ['stable','maintenance_only','reshuffle']:
   histories=[]
   for seed in range(40):
    if name=='maintenance':h=m.run(m.Settings(drought=climate=='drought',disruption=regime=='reshuffle',maintenance_only=regime=='maintenance_only',seed=seed));fields=['year','angkor','refuge','total','canal','shortage_kg']
    else:h=m.run(m.Settings(regime=regime,drought=climate=='drought',seed=seed));fields=['year','state_population','refuge_population','total_population','canal_condition','shortfall_kg']
    histories.append(pack(h,fields))
   groups[regime+'_'+climate]=histories
 data['models'][name]=groups

groups={}
for climate in ['normal','drought']:
 for regime,overrides in flight.SCENARIOS.items():
  groups[regime+'_'+climate]=[pack(flight.run(flight.Params(drought=climate=='drought',seed=seed,**overrides)),['year','angkor_pop','refuge_pop','total_pop','canal','unmet_kg']) for seed in range(40)]
data['models']['flight']=groups
old=json.loads((source/'angkor_institutions_v01/angkor_institutions_v01/scenarios.json').read_text())
print('Institution scenarios',list(old['scenarios']))
data['models']['institutions']={k:[pack(v,['year','population',None,None,'avg_canal','unmet_food'])] for k,v in old['scenarios'].items()}
files=[repair/'timing_fixed.py',repair/'accounted.py',source/'angkor_scott_flight_v02/angkor_scott_flight_v02.py',source/'angkor_institutions_v01/angkor_institutions_v01/model.py']
data['sourceHashes']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
p=ROOT/'dist/engines/institution-data.js';p.write_text('globalThis.AngkorInstitutionData = '+json.dumps(data,separators=(',',':'))+';\n')
print('Stored histories',sum(len(v) for m in data['models'].values() for v in m.values()),'bytes',p.stat().st_size)
