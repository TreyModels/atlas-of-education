/* PROPOSED, NOT APPLIED. public/worlds.js is outside this review's edit list, so the wiring below is for whoever owns
   that file. It uses only functions added to public/engines/youth.js in this review:
     AtlasYouth.benchmarks(ATLAS_DATA)      holdout and naive rows (model vs naive, MAE in points)
     AtlasYouth.shapleyLabels(ATLAS_DATA)   Shapley labels, with 'sector' shown as the unexplained Aug-2021 step
     run(...).broad_u                       broad unemployment (unemployed + graduates waiting), per month
   Strings introduced here need zh-Hans and vi entries in public/languages.js before check-translations.cjs covers them.
   Those for the labels already exist (see the review README); the rest are listed in TEXT_CHANGES.json as proposals.
*/

// 1. China world, view(): add the benchmark rows next to the fit (inside the metrics array)
const benchmarkMetrics = AtlasYouth.benchmarks(ATLAS_DATA).filter(b => b.id !== 'fit_2018_22').map(b =>
  metric(b.label, number(b.model, 1) + ' pts model · ' + (b.naive == null ? '–' : number(b.naive, 1)) + ' pts naive', b.detail));
// ...then: metrics: [ ...existing three, ...benchmarkMetrics ]

// 2. China world, controls: relabel the dr_drop slider (currently 'Graduate-job value lost' / 'Assumed demand shock from August 2021.')
//    range('dr_drop', 'Aug-2021 step (unexplained residual, fitted)', 0, .6, 'any', pct,
//      'Unexplained residual (fitted), not a measured demand shock. No sourced series matches it.')
//    Upper bound .6 matches the widened fit bound in engine/firms/calibrate_china.py; .3 was the old cap the fit sat on.

// 3. China world, view(): broad unemployment as a line, next to the official rate
//    line('Broad unemployment (unemployed + waiting)', data(current.run, 'broad_u'), 'reference')
//    (data() would need a key argument; it currently hard-codes rate_old / rate_new.)

// 4. Chart legend and Shapley bar labels: use AtlasYouth.shapleyLabels(ATLAS_DATA) instead of ATLAS_DATA.shapley.label.
