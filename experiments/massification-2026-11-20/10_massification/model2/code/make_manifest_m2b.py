import csv, hashlib, json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); M2=os.path.abspath(os.path.join(HERE,'..'))
def sha(p):
    h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()[:16]
rows=[]
for fn,group in [('m2b_scaling.csv','M2b_scaling'),('m2b_logistic_compare.csv','M2b_logistic'),
                 ('m2c_recovery.csv','M2c_recovery')]:
    p=os.path.join(M2,'runs',fn)
    if os.path.exists(p):
        d=list(csv.DictReader(open(p)))
        rows.append(dict(group=group,file=fn,rows=len(d),sha=sha(p)))
man=dict(phase='massification',owner='experiment-runner-2',scope='10_massification/model2 only',
         gate_ack='GATE_ACK_BRIEF013.md sha256-16 '+sha(os.path.join(M2,'GATE_ACK_BRIEF013.md')),
         m2b=dict(amendment='AMENDMENT_M2b.md',discrepancy='estimator range +0.84..+2.3; scout relay +1.174; exact scout script not executable'),
         m2c=dict(prereg='M2C_PREREG.md',verdict='E1 NOT SUFFICIENT (sign recoverable, size bias 0.55>0.50)'),
         task34_data_adoption='DEFERRED by instruction; original M2/M2b estimates stand',
         code_sha={p:sha(os.path.join(M2,p)) for p in ['code/m2b.py','code/m2c.py','code/make_manifest_m2b.py']},
         outputs=rows)
json.dump(man,open(os.path.join(M2,'RUN_MANIFEST_M2B_M2C.json'),'w'),indent=1)
print('manifest ok', len(rows))
