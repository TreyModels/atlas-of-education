#!/usr/bin/env python3
"""Analyse NEW-GENERATION Paper B outputs: arms table, CF4 reversal, MC vs parameter uncertainty, quintiles.

Reads results/newgen/paperB_new_generation_TRACKED.json and _SINGLE_KR.json (written by run_new_generation.py)
and emits PAPER_B_NEWGEN.md + results/audit/newgen/paperB_newgen_tables.csv.

Labels: NEW GENERATION — REPRODUCED SIMULATION (repaired engine 98baf6b, frozen V540-FREEZE spec). The Gemini-era
420/540 docx numbers are AUTHOR-REPORTED baseline only; CF4 reversal is reported explicitly.
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RES = os.path.join(REPO, 'results', 'newgen')
OUT_MD = os.path.join(REPO, 'docs', 'audit', 'PAPER_B_NEWGEN.md')
OUT_CSV = os.path.join(REPO, 'results', 'audit', 'newgen', 'paperB_newgen_tables.csv')
ARMS = ['Baseline', 'CF1a', 'CF1b', 'CF2a', 'CF2b', 'CF3a', 'CF3b', 'CF4a', 'CF4b']
METRICS = [('k12_rate_pct', 'K-12 participation %'), ('g12_pct', 'Grade-12 participation %'),
           ('q5_q1_gap_pp', 'Q5-Q1 participation gap pp'), ('q5_q1_spend_ratio', 'Q5/Q1 spend ratio'),
           ('k12_spend', 'mean K-12 tutoring spend'), ('elite_q5_share_pct', 'elite-track Q5 share %'),
           ('contest_e_mean', 'contest-prep effort')]

def load(name):
    p = os.path.join(RES, name)
    if not os.path.exists(p):
        return None
    return json.load(open(p))

def rows_for(doc):
    out = []
    for jur, arms in doc['summary'].items():
        for a in ARMS:
            e = arms.get(a)
            if not e: continue
            vals = {}
            for m, _ in METRICS:
                vals[m] = e[m]['mean']; vals[m + '_sd'] = e[m]['sd']; vals[m + '_ci'] = [e[m]['ci95_lo'], e[m]['ci95_hi']]
            vals['total_spend_index'] = e['total_spend_index']
            vals['spend_index_seed_sd'] = e['total_spend_index_seed_stats']['sd']
            vals['delta'] = {m: e['delta_vs_baseline'][m]['mean'] for m, _ in METRICS}
            vals['jurisdiction'] = jur; vals['arm'] = a
            out.append(vals)
    return out

def main():
    tr = load('paperB_new_generation_TRACKED.json')
    si = load('paperB_new_generation_SINGLE_KR.json')
    if tr is None:
        print('TRACKED output not found yet:', os.path.join(RES, 'paperB_new_generation_TRACKED.json')); return 1
    rows = rows_for(tr)
    single = rows_for(si) if si else []
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['jurisdiction', 'arm', 'metric', 'mean', 'seed_sd', 'ci95_lo', 'ci95_hi', 'delta_vs_baseline'])
        for r in rows:
            for m, _ in METRICS:
                w.writerow([r['jurisdiction'], r['arm'], m, r[m], r[m + '_sd'], r[m + '_ci'][0], r[m + '_ci'][1], r['delta'][m]])
    md = ['# Paper B — NEW GENERATION (repaired engine, frozen V540-FREEZE, 100 matched seeds vs legacy 30)', '',
          '**Label: NEW GENERATION — REPRODUCED SIMULATION.** The Gemini-era 420/540 docx tables are the',
          'AUTHOR-REPORTED baseline; this run is not a reproduction of them. Uncertainty: seed/MC (100 matched seeds);',
          'calibrated-parameter uncertainty is **zero in this stage** (frozen parameters) and is stated as such.', '']
    for jur in ('HK', 'KR'):
        md.append(f'## {jur} — arms (mean [seed sd], delta vs Baseline)')
        md.append('')
        md.append('| arm | K-12 part. % | G12 % | Q5-Q1 gap pp | Q5/Q1 spend | spend idx | elite Q5 % | contest effort |')
        md.append('|---|---|---|---|---|---|---|---|')
        for r in [x for x in rows if x['jurisdiction'] == jur]:
            md.append('| {} | {:.2f} ({:.2f}) | {:.2f} ({:.2f}) | {:.2f} ({:.2f}) | {:.3f} ({:.3f}) | {:.1f} | {:.2f} ({:.2f}) | {:.4f} |'.format(
                r['arm'], r['k12_rate_pct'], r['k12_rate_pct_sd'], r['g12_pct'], r['g12_pct_sd'],
                r['q5_q1_gap_pp'], r['q5_q1_gap_pp_sd'], r['q5_q1_spend_ratio'], r['q5_q1_spend_ratio_sd'],
                r['total_spend_index'], r['elite_q5_share_pct'], r['elite_q5_share_pct_sd'], r['contest_e_mean']))
        md.append('')
    md.append('## CF4 reversal (vs the pre-repair 540 run) — explicit')
    md.append('')
    md.append('Pre-repair 540 result: CF4a failed the Win-Win criterion (spend index and/or elite Q5 did not fall in both')
    md.append('jurisdictions). The new-generation numbers are in the table above; the reversal direction is recorded with')
    md.append('the seed CIs, and the old failure is preserved in `GATE1_MIGRATION_TABLE.md` / `paper_claims.csv` — the new')
    md.append('run neither erases it nor claims it was wrong.')
    if single:
        md.append('')
        md.append('## KR-SINGLE sensitivity (gate design) — primary outcomes')
        md.append('')
        md.append('| arm | K-12 part. % | Q5-Q1 gap pp | Q5/Q1 spend | elite Q5 % |')
        md.append('|---|---|---|---|---|')
        for r in [x for x in single if x['jurisdiction'] == 'KR']:
            md.append('| {} | {:.2f} | {:.2f} | {:.3f} | {:.2f} |'.format(r['arm'], r['k12_rate_pct'], r['q5_q1_gap_pp'], r['q5_q1_spend_ratio'], r['elite_q5_share_pct']))
    md += ['', '## Caveats', '',
           '* Frozen spec parameters are not calibrated in this generation; no VALIDATED claim.',
           '* Seed/MC uncertainty only (100 matched seeds); parameter uncertainty is zero by construction here.',
           '* Labels: AUTHOR-REPORTED baseline (Gemini docx), REPRODUCED SIMULATION (540 legacy), NEW GENERATION (this).',
           '* Multiplicity: all 9 arms × 4 headline outcomes × 2 jurisdictions reported; CF4a is the pre-stated primary.']
    open(OUT_MD, 'w').write('\n'.join(md) + '\n')
    print('wrote', OUT_MD, 'and', OUT_CSV, 'rows', len(rows))
    return 0

if __name__ == '__main__':
    sys.exit(main())
