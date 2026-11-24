"""Is 'labour-market demand precedes schooling in 7% of 58 countries' an artefact of series start dates?
Uses the supply-demand event table (research/records/2026-11-23-supply-demand) and the 22 Nov series.
Usage: python3 -I demand_series_start_check.py ../data"""
import sys, json, pandas as pd
base = sys.argv[1].rstrip('/') + '/'
ev = pd.read_csv(base + 'supply_demand_event_ordering.csv')
def first(n):
    d = pd.DataFrame([(i, y) for i, y, v in json.load(open(base + n + '.json')) if v is not None], columns=['i', 'y'])
    return d.groupby('i').y.min()
out = {}
for n in ('wage_emp', 'emp_agri', 'agri_va'):
    f = first(n); out[n] = {'min': int(f.min()), 'median': float(f.median()), 'max': int(f.max())}
    print(n, 'first observed year: min/median/max', out[n])
we = first('wage_emp').rename('we_first'); d = ev.merge(we, left_on='iso3', right_index=True, how='left')
out['n_countries'] = int(len(d)); out['schooling_takeoff_by_1990_share'] = round(float((ev.schooling <= 1990).mean()), 3)
out['schooling_after_first_paid_emp_year_plus5'] = int((d.schooling > d.we_first + 5).sum())
print('schooling take-offs dated <=1990:', out['schooling_takeoff_by_1990_share'], 'of', out['n_countries'])
print('countries where schooling take-off is later than first paid-employment year + 5:', out['schooling_after_first_paid_emp_year_plus5'])
print('=> narrow labour-market demand can precede schooling in at most that many countries; the "7%" is mechanically capped.')
json.dump(out, open('demand_series_start_check.json', 'w'), indent=1)
