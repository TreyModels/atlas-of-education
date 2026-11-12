from pathlib import Path
import importlib.util,sys,csv,json,statistics,hashlib
from dataclasses import replace
from accounted import Settings,run
ROOT=Path(__file__).parent

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
original=load('original_model',ROOT/'original/run.py');fixed=load('timing_fixed',ROOT/'timing_fixed.py')
rows=[];summaries=[]
for engine in ('original','timing_fixed','accounted'):
 for drought in (False,True):
  for regime in ('stable','maintenance_only','reshuffle'):
   group=[]
   for seed in range(40):
    if engine=='accounted':
     h=run(Settings(regime=regime,drought=drought,seed=seed));last=h[-1]
     row={k:last[k] for k in ('state_population','refuge_population','total_population','canal_condition')}
     row.update(cumulative_shortfall_kg=sum(x['shortfall_kg'] for x in h),cumulative_flight=sum(x['flight'] for x in h),unpaid_service_kg=sum(x['unpaid_service_kg'] for x in h))
    else:
     m=original if engine=='original' else fixed
     h=m.run(m.Settings(disruption=regime=='reshuffle',maintenance_only=regime=='maintenance_only',drought=drought,seed=seed));last=h[-1]
     row=dict(state_population=last['angkor'],refuge_population=last['refuge'],total_population=last['total'],canal_condition=last['canal'],cumulative_shortfall_kg=sum(x['shortage_kg'] for x in h),cumulative_flight=sum(x['flight'] for x in h),unpaid_service_kg='')
    row=dict(engine=engine,drought=drought,regime=regime,seed=seed,**row);rows.append(row);group.append(row)
   summary=dict(engine=engine,drought=drought,regime=regime,**{k:statistics.median(x[k] for x in group) for k in ('state_population','refuge_population','total_population','canal_condition','cumulative_shortfall_kg')});summaries.append(summary);print(summary)
with (ROOT/'runs.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'summary.json').write_text(json.dumps(summaries,indent=2))
# Timing intervention must match stable bit-for-bit before year55, both climates.
for drought in (False,True):
 a=fixed.run(fixed.Settings(drought=drought));b=fixed.run(fixed.Settings(drought=drought,maintenance_only=True));assert a[:55]==b[:55]
assert run(Settings())==run(Settings())
for s in (Settings(communities=0),Settings(military_share=0,monument_share=0,religion_share=0),Settings(drought=True),Settings(maintenance_factor=0,regime='maintenance_only')):run(s)
# No bookkeeping assertion is a historical calibration test.
print('Timing, reproducibility, zero-population, zero-sector and zero-maintenance checks passed.')
# Store an example annual ledger so every flow is inspectable.
h=run(Settings(regime='maintenance_only',drought=True))
with (ROOT/'annual_ledger.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(h[0]));w.writeheader();w.writerows(h)
print('Max annual accounting errors', {k:max(abs(x[k]) for x in h) for k in ('grain_error','population_error','labour_error')})
