"""Writes TEXT_CHANGES.json. Every 'old' string is asserted to occur exactly once in its file (exact English text)."""
import json, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
C = []
def add(file, old, new, why, translate=False):
    C.append(dict(file=file, old=old, new=new, why=why, needs_translation=translate))

W = 'public/worlds.js'
add(W, 'Graduate-job value lost', 'Aug-2021 step (unexplained residual, fitted)',
    'Review 1.1: dr_drop is a fitted residual with no sourced counterpart. Relabel the slider.')
add(W, 'Assumed demand shock from August 2021.',
    'Unexplained residual (fitted), not a measured demand shock. No sourced series matches it.',
    'Review 1.1: the slider note called the step a demand shock. No data supports that reading.')
add(W, 'The Atlas documents that a model fitted to 2018–22 misses the later youth unemployment rise.',
    'The Atlas documents that a model fitted to 2018–22 misses the later youth unemployment rise. A naive benchmark (the same month of 2022, carried forward) does better on the 2023 H1 holdout and on the verified months from December 2023.',
    'Review 1.7: the naive benchmark beats the early fit on both out-of-sample windows. Say so next to the holdout.', True)
add(W, 'The reference was fitted to the record shown. Supply, demand and wage responses interact. The fitted hoarding share was set as an assumption.',
    'The reference was fitted to the record shown, so its fit statistics are in sample. Supply, demand and wage responses interact. The hoarding share, insider split and wage wedge were set as assumptions, not estimated. The waiting and emulation mechanisms are untested, and the 2021 step is an unexplained residual.',
    'Reviews 1.1, 1.5 and 1.7: the headline fit is in sample, and the Tilly mechanisms are not tested.', True)
add(W, 'Graduates waiting outside the labour force are outside the official unemployment rate.',
    'Graduates waiting outside the labour force are outside the official unemployment rate. The waiting mechanism is untested: no data on family support for waiting.',
    'Review 1.5 and 1.4: waiting is a built-in mechanism with no data behind its size.', True)
add(W, 'Share of secure openings filled through the network.',
    'Share of secure openings filled through the network. An assumption, not estimated.',
    'Review 1.5: the hoarding share is set, not estimated (tilly_fit.FIXED).', True)

R = 'public/reference/education/index.html'
add(R, 'Graduate-job value lost from Aug 2021', 'Aug-2021 step, unexplained residual (fitted)',
    'Review 1.1: relabel the dr_drop control on the reference page.')
add(R, 'Tutoring ban, platform crackdown, property slump: the data cannot separate them.',
    'Unexplained residual. Candidate causes (tutoring ban, platform crackdown, property slump) are not separately identified, and sourced job-loss figures point to a much smaller step.',
    'Review 1.1: the candidate causes are not identified, and the sourced magnitudes do not match the fitted size.')
add(R, 'Tilly’s four mechanisms act at those boundaries.',
    'Tilly’s four mechanisms are built in at those boundaries. None is tested against data: the Atlas has no hukou, party-membership or parental-sector series.',
    'Review 1.5: the mechanisms are presented as if they act, with no data to test them.')
add(R, 'and Tilly’s exploitation, hoarding, emulation and adaptation act at the boundaries.',
    'and Tilly’s exploitation, hoarding, emulation and adaptation are built in at the boundaries, with sizes set by assumption and untested.',
    'Review 1.5.')
add(R, 'Adaptation hides slack; it does not replace the demand fall.',
    'In the model, adaptation hides slack; it does not replace the demand fall.',
    'Review 1.4 and 1.5: a model result, not an empirical finding.')
add(R, "'Fitted, with Tilly mechanisms'", "'Fitted, with Tilly mechanisms (untested)'",
    'Review 1.5: the preset label should say the mechanisms are untested.')
add(R, 'Tilly’s hoarding share, wage wedge and insider split were set, not estimated; several fitted values sit on their bounds.',
    'Tilly’s hoarding share, wage wedge and insider split were set, not estimated; the waiting and emulation mechanisms are untested; several fitted values sit on their bounds.',
    'Review 1.2 and 1.5.')
add(R, 'The China graduate-queue world adds free entry, wage rigidity and Tilly’s categories.',
    'The China graduate-queue world adds free entry, wage rigidity and Tilly’s categories, whose mechanisms are untested.',
    'Review 1.5.')
add(R, 'insiders took ${Math.round(100 * tf.sec_ins_share)}% of secure posts.',
    'insiders took ${Math.round(100 * tf.sec_ins_share)}% of secure posts, as the hoarding assumption dictates.',
    'Review 1.5: the insider share of secure posts is set by the hoarding assumption, not estimated.')

D = 'docs/engine/facts_register.md'
add(D, '"no waiting" counterfactual: +22.8 pts, but only with `wait_max` fitted on post-2022 data.',
    '"no waiting" counterfactual: +12.2 pts on the current results/tilly_fit.json (the +22.8 of an earlier run is not reproduced). Holding the Tilly parameters fixed, the measured rise is +5.1 with waiting and +12.2 without; the broad measure with waiting is +9.5.',
    'Review 1.4: the +22.8 figure is stale; the current file gives +12.2.')
add('docs/engine/china_jobs_stories.md', 'more than 3 million job openings lost within four months',
    'about 3 million job losses within four months (estimate; Huang et al. 2025)',
    'Review 1.1: the source gives job losses (about 3m), not openings.')
add('docs/engine/china_fit.md', '- Graduate-job demand: real-estate contraction and the 2021 tutoring ban: +3.45 pp',
    '- Aug-2021 step (unexplained residual, fitted): +3.45 pp',
    'Review 1.1 and 1.6: the step is not real estate, and it is not a sourced shock.')
add('engine/firms/categorical.py', 'Four mechanisms do the work:',
    'Four mechanisms are built in (their sizes are assumptions, and none is tested against data):',
    'Review 1.5: the docstring presents the mechanisms as doing the work.')

M = 'src/data/model-catalogue.md'
add(M, '**Null model to add:**', '**Null model, now run:**', 'Review 1.8.')
add(M, 'The Tilly categories earn their place if they explain what the null model cannot: the July spike, waiting outside the labour force, and insider protection.',
    'The plain lake null has now been run (experiments/youth-review/lake_null.py, four constant-rate parameters). Out of sample it is no better than the categorical model on 2023 H1 (8.5 against 7.1 points of error) and better on the verified months from December 2023 (2.9 against 5.5). Both lose to a same-month naive benchmark (2.5 and about 1.6). The Tilly categories are therefore not shown to earn their place. The July spike, waiting and insider protection remain untested.',
    'Review 1.8: the claim was conditional on a null that has now been run. The result does not support it.', True)
add(M, '| 4 | Knight cohort-shock test and lake-model null | 2 days | NBS youth series (already in the Atlas) | China graduate queue | Not started |',
    '| 4 | Knight cohort-shock test and lake-model null | 2 days | NBS youth series (already in the Atlas) | China graduate queue | Lake null run (experiments/youth-review); Knight test not started |',
    'Review 1.8: status update.')

bad = []
for c in C:
    s = open(os.path.join(ROOT, c['file']), encoding='utf-8').read()
    if s.count(c['old']) != 1:
        bad.append((c['file'], s.count(c['old']), c['old'][:60]))
assert not bad, bad
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TEXT_CHANGES.json')
json.dump(C, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(C), 'proposals to', out)
