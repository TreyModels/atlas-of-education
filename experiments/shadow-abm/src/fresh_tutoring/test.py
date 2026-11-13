import csv
r=list(csv.DictReader(open('results/draws.csv')))
assert len(r)==800
for v in ('thin','diversion','favour','full'):
 z=[x for x in r if x['variant']==v]; assert len(z)==200 and len({int(x['seed']) for x in z})==5
 assert all(0<=float(x['participation'])<=1 and int(x['fit'])==(float(x['max_distance'])<=1) for x in z)
print('Run size, seed allocation, rate bounds and fit flags passed.')
