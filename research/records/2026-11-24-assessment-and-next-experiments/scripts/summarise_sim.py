"""Render known_truth_sim.json (v2, 100 reps) and the run-1 JSON (paper-rule-only, 200 reps) as markdown. python3 -I summarise_sim.py"""
import json
r2 = json.load(open('known_truth_sim.json')); r1 = json.load(open('known_truth_sim_run1_paper_rule_only.json'))
truth = {'A': 'uniform b=0.15 (robust)', 'W': 'weak uniform b=0.06 (robust, low power)', 'B': 'b=0.40 only in top tercile of family 0 (group-specific)',
         'C': 'null, independent series', 'D': 'null, shared country trends (spurious levels link)', 'S': 'sign split: +0.25 / -0.25 by family-1 median (group-specific)'}
L = ['| regime | truth | R | ' + ' | '.join(['paper-rule ROBUST', 'ROBUST+H', 'ROBUST-HET', 'ROBUST-but-GROUP', 'GROUP', 'NONE', 'planted tag flagged']) + ' |', '|---|---|---|' + '---|'*7]
for k in 'AWBCDS':
    for R, c in r2['results'][k].items():
        rob = c.get('ROBUST+H', 0) + c.get('ROBUST-HET', 0) + c.get('ROBUST-but-GROUP', 0)
        L.append(f"| {k} | {truth[k]} | {R} | {rob} | {c.get('ROBUST+H',0)} | {c.get('ROBUST-HET',0)} | {c.get('ROBUST-but-GROUP',0)} | {c.get('GROUP',0)} | {c.get('NONE',0)} | {c.get('planted_tag_flagged','')} |")
print('Counts out of', r2['reps'], 'replicates per regime (v2 rules).\n'); print('\n'.join(L))
print('\nRun 1 (paper rule only, no heterogeneity condition, 200 replicates):')
for k in 'AWBCDS': print(k, r1['results'][k]['400'])
