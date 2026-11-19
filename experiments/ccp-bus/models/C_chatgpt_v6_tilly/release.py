"""Validate and package the completed execution; exclude the aborted first batch."""
from pathlib import Path
from collections import Counter
import hashlib,json,zipfile,py_compile
from run import provenance,reusable
P=Path(__file__).resolve().parent

def main():
    out=P/'results_completed';m=json.loads((out/'manifest.json').read_text());c=json.loads((out/'completion.json').read_text())
    assert c['completed']==c['expected']==len(m['jobs'])
    assert m['provenance']==provenance()
    annual=people=0;max_debt=max_budget=0.;families=Counter()
    for j in m['jobs']:
        f=out/'runs'/(j['id']+'.json');assert reusable(f,j,m['design_hash'])
        r=json.loads(f.read_text());families[j['family']]+=1;annual+=len(r['rows']);people+=len(r['cohort_records'])
        assert len(r['cohort_records'])==(0 if j['scenario']=='no_replacement' else j['params']['organizations'])
        for x in r['rows']:
            max_debt=max(max_debt,abs(x['obligation_residual']))
            max_budget=max(max_budget,abs(x['resource_allocated']-x['resource_diverted']-x['resource_delivered']))
            assert x['cohort_first_acts']<=x['cohort_first_act_risk']<=x['cohort_at_risk']
        for x in r['cohort_records']:
            if x['first_act'] is not None:assert x['first_act']>=x['appointed_tick']
            if x['first_true_sanction'] is not None:assert x['first_true_sanction']>=x['first_true_filing']+j['params']['case_lag']
    assert max_debt<1e-7 and max_budget<1e-6
    checks=json.loads((P/'results/checks.json').read_text());assert all(checks.values())
    analysis_checks=json.loads((out/'analysis_checks.json').read_text());assert all(analysis_checks.values())
    audit=dict(experiment_runs=len(m['jobs']),families=dict(families),annual_rows=annual,cohort_records=people,
        verification_groups=len(checks),additional_analysis_groups=len(analysis_checks),design_hash=m['design_hash'],
        elapsed_seconds=c['elapsed_seconds'],maximum_obligation_residual=max_debt,maximum_public_budget_residual=max_budget,
        code_and_data_match_manifest=True,all_jobs_reusable_under_same_design=True,executed_on=m['environment']['platform'],
        behavioral_source_hashes=m['provenance'],analysis_source_hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in P.glob('*.py')})
    (out/'execution_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    for f in P.glob('*.py'):py_compile.compile(str(f),doraise=True)
    files=[]
    for f in sorted(P.rglob('*')):
        if not f.is_file() or '__pycache__' in f.parts or '.venv' in f.parts or f.suffix=='.tmp' or f.name=='SHA256SUMS.txt':continue
        rel=f.relative_to(P)
        if rel.parts[0]=='results' and rel.as_posix()!='results/checks.json':continue
        files.append(f)
    sums=P/'SHA256SUMS.txt';sums.write_text('\n'.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P)) for f in files)+'\n')
    archive=P.parent/'bus_v6_tilly_executed_2026-11-18.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in files+[sums]:z.write(f,arcname=P.name+'/'+str(f.relative_to(P)))
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(json.dumps(dict(file=str(archive),bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),runs=len(m['jobs']),annual_rows=annual,cohort_records=people)))
if __name__=='__main__':main()
