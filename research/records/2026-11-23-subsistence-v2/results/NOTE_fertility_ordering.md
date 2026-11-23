# Note: the 68.75% schooling-before-fertility field counts ties

**Correction note (30 Nov 2026).** The field `pct_schooling_before_fertility` = 68.75 in
`results/sequencing.json` (and the line "schooling before fertility: 69%" in `results/sequencing.txt`) **counts
simultaneous take-offs as schooling-first**: 20 of the 64 three-event countries have the schooling and fertility
take-offs in the same year, and the field is 24 strict forward + 20 ties = 44/64. A direct recomputation from
`results/event_dates.csv` gives the **strict** ordering: **24/64 = 37.5% (bootstrap 95% interval 26.6-50.0%)**,
with 31.3% simultaneous and 31.3% fertility-first; across all 81 countries with both dates it is **29/81 = 35.8%
(95% interval 25.9-45.7%)**. The 68.75% figure should **not** be cited as the schooling-before-fertility ordering.
Recomputation (script, committed input copy, output): `research/paper-massification-2026-11-25` @ `95dc135`,
`research/records/2026-11-25-paper-massification/scripts/recompute_fertility_ordering.py` and
`research/records/2026-11-25-paper-massification/data/recompute_fertility_ordering.json`. Paper M (95dc135) reports
the strict 37.5% figure and marks this JSON field as not used. Nothing else in this record changes.

