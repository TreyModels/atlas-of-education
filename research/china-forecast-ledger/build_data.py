"""One-off: write data/observed.csv and data/graduates.csv from engine/firms/data_china.py, exactly as stored.

After this, the CSV files are the master copy. Append new NBS months to data/observed.csv by hand; this script refuses to
overwrite an existing file.
"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'engine'))
from firms import data_china as D  # noqa: E402

SRC = 'engine/firms/data_china.py'


def main():
    obs, gr = os.path.join(HERE, 'data', 'observed.csv'), os.path.join(HERE, 'data', 'graduates.csv')
    if os.path.exists(obs) or os.path.exists(gr):
        print('data files already exist; not overwriting'); return
    rows = []
    for y in range(2023, 2027):
        for m in range(1, 13):
            v = D.youth(y, m)
            if v and v[1] == 'new':
                rows.append((y, m, v[0], f'NBS urban surveyed 16-24 excluding students (new method); {SRC} flag {v[2]}'))
    with open(obs, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['year', 'month', 'rate', 'source_note']); w.writerows(rows)
    with open(gr, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['year', 'millions', 'source_note'])
        for y in sorted(D.GRADUATES):
            w.writerow([y, D.GRADUATES[y], f'MoE expected graduating class for employment planning; {SRC} flag {D.GRAD_FLAG[y]}'])
    print(len(rows), 'observed rows written')


if __name__ == '__main__':
    main()
