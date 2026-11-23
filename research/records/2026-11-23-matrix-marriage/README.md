# Adding marriage age to the lead-lag matrix: 20 measures, 380 links (income logged)

Worker `un-data`, branch `research/matrix-marriage-2026-11-23`, 23 Nov 2026. Same estimator as
`research/records/2026-11-23-handoff-run/scripts/full_matrix_trends.py`; **income is logged** at load in every
script (`np.log` of the level file), per the session rule. **Server: box2 only** (`ssh autodl2`), directory
`/root/work/matrix_marriage` (6 workers; the matrix runs in ~1 minute). The box1 copy of that directory is retired
with box1 and is not needed: every number in this record was produced on box2, and the committed
`data/`/`results/` files are the durable record. Series used by the falsifiers are on box2 at
`/root/work/undata/{out,raw}`; the panel is at `/root/work/data` (migrated copy under `/root/autodl-tmp/migrated/`).
Full matrix in `data/matrix20.csv` / `.json`.

**Short answer.** The three UN marriage measures entered the matrix as variables (never as controls), giving
380 ordered links. With income logged, the 272 old links are **bit-identical** to the corrected logged
baseline (127 significant with country effects, 42 with country trends, 24 surviving both — panel-matrix's
observed arm), and the old baseline is unchanged by the marriage variables. None of the new marriage links
survives the full test set: the best marriage → fertility link is the same levels-vs-change artefact as before,
and the best "schooling → later marriage" link dies under the correct permutation and under dropping the UN's
model-based rows. One marriage-as-outcome association is stable but misses multiple-testing correction: more
agrarian economies saw a slower rise in the never-married share. Marriage age is on the causal path from
schooling to fertility and is **never a control** in any link; the control set is identical (logged income,
urbanisation) for all 380 links.

**Income footnote.** The handoff README's 126/45/25 counts came from income entered in levels (the file
`gdppc_log.json` holds GDP per head in levels despite its name). The corrected logged recompute gives
127/42/24, and our 20-measure matrix reproduces the corrected logged baseline exactly. This correction commit
reruns every matrix and falsifier number with logged income; the earlier levels run is discarded.

## What was run, and the proof that the old matrix is untouched

20 measures: the 17 handoff measures plus women's mean age at marriage, the share never married at 45-49 and
the female-minus-male marriage-age gap. 20 × 19 = **380 ordered links**, each estimated twice (country effects;
country effects plus a straight-line country trend). Estimable: **380 with country effects, 379 with trends**
(the pair lower-secondary → age gap has too few overlapping survey years). For the sparse UN series the start
years are real census/survey years, never interpolated: when the marriage measure is the outcome, the window is
an actual pair of surveys 8-13 years apart.

**The baseline is unchanged — proved, not asserted.** We recomputed the handoff estimator (with logged income)
for all 272 17-measure links and compared 544 estimates (2 settings) with the 20-measure matrix: maximum
absolute difference in the coefficient **0.0**, in the standard error **0.0**, in the sample size **0**, in the
country count **0**; 544 of 544 exact. The logged baseline counts are **127 significant with country effects /
42 with country trends / 24 surviving both**, matching panel-matrix's corrected observed-arm numbers. (The
handoff run's 126/45/25 came from income in levels.) Marriage is an enlarged variable set, not a new control.

**Multiple testing.** Benjamini-Hochberg across the 380 links: with country effects **116** of 380 survive at
q<0.05; with country trends **16** of 379. With 380 tests about 19 would be expected by chance at 5% if nothing
were real, so the trend-surviving set is roughly chance-sized and must be read link by link. BH assumes
independent tests; links share measures, so these q-values are optimistic.

## (1) Fertility

**No marriage → fertility link survives the falsifiers.** The whole marriage-to-fertility block, country trends:

| link (plain words) | estimate | standard error | rows / countries | BH q | killed by |
|---|---|---|---|---|---|
| later female marriage age → smaller fall in births | +0.0198 births per woman per year | 0.0056 | 1,698 / 170 | 0.020 | change-on-change reverses it to −0.027 (0.010) |
| narrower age gap → larger fall in births | −0.0347 births per woman per year of gap | 0.0159 | 1,453 / 156 | 0.22 | not BH-significant; sign flips without the starting-level control |
| more never-married women → fall in births | −0.0040 births per woman per point | 0.0026 | 1,684 / 170 | 0.45 | nothing to kill: it is a null |
| higher fertility now → faster rise in never-married share | +1.68 points per birth per woman | 0.43 | 1,100 / 112 | 0.006 | permutation p=0.067; falls to about +0.2 (ns) without UN model rows |

The first row is the same artefact as before, now inside the matrix: it passes the circular-shift permutation
(p<0.005) and dropping the UN's model-based rows (+0.014, still significant), but putting changes on both
sides flips the sign to **−0.027 (standard error 0.010, 1,360 rows, 196 countries)** — within a country,
faster rises in marriage age go with faster fertility falls. In the matrix framing the trap is exactly as
predicted, so it is reported as an artefact, not a finding. The gap row is the only marriage → fertility link
that survives the strict permutation (circular-shift p=0.017), but it is not BH-significant and its sign flips
to +0.018 when the starting-level control is removed, so: provisional. The never-married row is a null. The
fourth row is in the fertility → marriage direction (an outcome, not the causal-path direction) and does not
survive the strict permutation or the model-row check.

**What the marriage measures do to the fertility block: nothing that survives.** They add 108 new links; of
the 16 that are significant with country trends, none passes all four tests. The existing schooling →
fertility edge is untouched (one of the 24 unchanged baseline links).

## (2) Massification

**The schooling → marriage link does not survive either.** Tertiary schooling → later marriage looked like the
one massification result: +0.071 years per point of enrolment (standard error 0.021; 398 rows, 57 countries;
BH q=0.020). Test designed to kill it: the circular-shift permutation gives **p=0.50** (shuffled alignment
produces estimates this large half the time; null 95th percentile 0.156), and dropping the UN's model-based
estimates flips the sign (not significant). Killed twice. Secondary schooling → marriage age remains
null/negative (−0.037 ± 0.023, 63 countries), lower-secondary −0.050 ± 0.027, primary +0.020 ± 0.010. There is
no consistent "massification delays marriage" link in this matrix.

**The one stable marriage association is an outcome, not a driver.** More agricultural value added predicts a
**slower rise in the never-married share**: −0.126 points per point of agriculture (standard error 0.045; 827
rows, 92 countries; BH q=0.091, just above 0.05; circular-shift p=0.017; sign unchanged when the UN
model-based rows are dropped, n=460). Read plainly: agrarian economies were slower to reach the modern pattern
of late and sometimes forgone marriage. It is a marker of development, not a cause.

**Other marriage links, weak after testing.** Never-married share → agricultural employment +0.056 per point
(0.025; 989 rows, 132 countries; q=0.21; circular-shift p<0.005; loses significance without model rows);
never-married → tax −0.099 (0.047; 842 rows, 73 countries; q=0.23; loses significance without model rows). The
age gap → primary completion +2.78 points per year of gap (0.83; 384 rows, 56 countries; q=0.026;
circular-shift p<0.005) **dies when the UN model-based rows are removed** (−0.14, not significant), as do gap
→ child mortality (−1.09 ± 0.44; sign flips without model rows) and gap → electricity (−0.43 ± 0.13). So the
marriage measures behave like markers of where a country is, not like variables that predict schooling or
fertility changes.

## Falsifiers — what ran and what each killed

1. **Circular-shift permutation within country** (60 draws; the only permutation used — the year-shuffle is
   anti-conservative and appears nowhere). 15 marriage links tested (all marriage links significant with
   trends plus the three marriage → fertility links). Killed: tertiary schooling → marriage age (p=0.50),
   teacher-pupil ratio → never-married (p=0.58), fertility → marriage age (p=0.25), never-married → marriage
   age (p=0.27), gap → electricity (p=0.10), gap → primary completion survives (p<0.005), agriculture →
   never-married p=0.017, gap → child mortality p=0.033, never-married → agricultural employment p<0.005,
   gap → fertility p=0.017.
2. **Dropping the UN's model-based "Estimate" rows.** 12 of 57 marriage-as-outcome links flip sign; of the
   permutation survivors, gap → primary completion, gap → child mortality and gap → electricity die; never-
   married → agricultural employment and never-married → tax lose significance; only agriculture →
   never-married keeps its sign and significance; female age → fertility keeps its positive sign (+0.014)
   but is then killed by test 3.
3. **Change-on-change** for every marriage → fertility link: female age → fertility flips to −0.027 (0.010,
   n=1,360, 196 countries); gap → fertility is −0.097 (0.026, n=1,194, 190 countries) but is not robust to
   removing the starting-level control; never-married → fertility is +0.001 (0.005) — nothing.
4. **Benjamini-Hochberg across 380 links**, reported above and per link in the CSV.

## Power, limits, and what is not claimed

The matrix has decent power for large links, but the marriage cells are thinner (298-1,698 rows, 42-170
countries) and the survey-anchored windows mean each link uses a different sample — stated per link in the
CSV. No causal claim is made anywhere: marriage age sits on the causal path from schooling to fertility and is
never a control; all marriage links are associations or outcomes. Honest summary: adding marriage to the
matrix does **not** change any of the 272 old links and does **not** produce a marriage link that survives the
falsifiers as a driver of fertility or schooling; it produces one stable outcome association (agriculture →
slower rise in never-married) that just misses BH, and one provisional gap → fertility association.

## Files

`data/matrix20.csv` — full deliverable, 760 rows (380 links × 2 settings): estimate, standard error, sample,
countries, decades, years, t, p, BH q. `data/matrix20.json` — same with verdict flags. `data/baseline_compare.json`
— the 544-comparison logged-baseline proof (127/42/24). `data/falsify_matrix.json` — permutation, model-row and
change-on-change results. `data/drop_model_x.json` — model-row test for marriage-as-predictor links.
`results/logs/` — run logs. Scripts: `matrix20.py`, `validate_baseline.py`, `falsify_matrix.py`,
`drop_model_x.py`, plus the shared `edge_marriage.py` / `extract_un.py` estimator and extractor.
