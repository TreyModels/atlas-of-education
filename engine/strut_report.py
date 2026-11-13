"""Strut-removal report for a country pack: vary each declared strut, see which patterns move. Run: python strut_report.py cambodia"""
import sys, importlib, os
from eduengine.struts import strut_test, STRUTS
from eduengine import measure as M
from countries._common import settled

PATTERNS = {
    'completion lower 2019': lambda E, o: M.completion_cohort(E, 1, 2019),
    'completion upper 2019': lambda E, o: M.completion_cohort(E, 2, 2019),
    'tutoring narrow G5-6 2015': lambda E, o: M.tutoring(E, 2015, [5, 6], 'narrow'),
    'tutoring broad primary 2015': lambda E, o: M.tutoring(E, 2015, [1, 2, 3, 4, 5, 6], 'broad'),
    'youth literacy (true) 2019': lambda E, o: M.literacy(E, 2019, 'true'),
    'graduates queuing 2023': lambda E, o: M.youth_unemployment(E, 2023),
    'street children /1000 (x0.01) 2019': lambda E, o: M.street_children(E, 10, 17, 2019) / 100,
}

def main(country):
    C = importlib.import_module(f'countries.{country}')
    best = settled(country)                                         # least implausible run in results/context_map.json
    rows = strut_test(lambda **o: C.make(**{**best, **o}), PATTERNS)
    L = [f'STRUT REPORT {country} (settled parameters from the history match; each strut varied low/high, seed 0). Load-bearing = moves a pattern by > 0.05', '']
    for r in rows:
        L.append(f"{r['id']} {r['name']}  [{r['param']}: {r['lo']} -> {r['hi']}]")
        L.append('    ' + '; '.join(f"{k} {r['low'][k]:.3f}->{r['high'][k]:.3f}" for k in PATTERNS))
        L.append(f"    LOAD-BEARING for: {', '.join(r['load_bearing']) if r['load_bearing'] else 'nothing (harmless scaffolding at this setting)'}")
    open(f'results/{country}_struts.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'cambodia')
