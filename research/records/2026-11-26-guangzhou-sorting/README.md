# Guangzhou sorting system: shadow education and equity (2026-11-26)

**Status: EXPLORATORY / SIMULATION.** Synthetic pupils; parameters are dossier figures or stated assumptions. Nothing here
is an estimate from Guangzhou microdata. One small real-data test (boarding vs admission cutoff) is exploratory.
Working-paper draft: Claude Docs artifact https://claude.ai/artifact/G2AxLfRyeZNvzWguusBRZ6 (two papers: shadow
education under controlled time; equity after the gate). Assumption checklist reviewed by an informant:
https://claude.ai/artifact/FMkZ1CQKrk8Gw3HRC1K29D

## Files
| Folder | What |
| --- | --- |
| `fieldnotes/INFORMANT_A_2026-11-26.md` | **Primary data.** Verbatim (voice-transcribed) statements of a Guangzhou tutoring-institution teacher, with translations. Privacy handled by the author. |
| `model/` | `gz_system.py` (first version), `gz_talent.py` (talent vs skill), `gz_v3_0.py` (v3 as run for `v3_results`), `gz_v3.py` (v3.1, admissions rules corrected), `eq_tests.py` (inventory equations vs model truth), sweep and analysis scripts, `fade_sweep.py` |
| `prereg/` | `PREREG_GZ_SORTING.md` (talent model), `PREREG_V3.md` (v3, with Amendment 1 for v3.1) |
| `results/` | Raw sweep outputs (jsonl), manifests with sha256, analysis printouts |
| `lean/` | Lean 4.36 project `GZSorting` (26 theorems on the formulas of `gz_system.py`/`gz_talent.py`; built on the author's Mac; axioms propext, Classical.choice, Quot.sound only). Does not yet cover v3. |
| `dossier/` | Guangzhou dossiers supplied by the author (compiled by an AI agent, secondary, unverified): Tianhe inventory, double-reduction policy, boarding census (216 campuses), teacher/school quality evidence, private schools, boarding history, costs, subsidies; external review of the draft. The 209-page 2026 admissions guide PDF is not included. |
| `inventory/Atlas_Inventory.xlsx` | Inventory of all 188 repo branches plus bridge to-dos (408 rows), same day |

Note: `run_v3.py` imports `gz_v3`; the v3 results in `results/v3_results.jsonl` were produced before Amendment 1, i.e. by
the code now saved as `model/gz_v3_0.py`. `run_v31.py` with the current `gz_v3.py` produced `v31_results.jsonl`.
Pre-registration hashes are local, not publicly timestamped before the runs; this commit is the first public record.

## Results in brief (medians over sweeps; ranges are 5th-95th percentile of sampled configurations, not confidence intervals)
- Talent model (2,000 draws): 4 of 5 pre-registered claims supported; "zone teachers carry most of the remaining gap" not supported.
- v3 (800 draws): 3 of 8 supported. v3.1 with corrected zhibiao/hukou rules (400 draws): same 3 of 8.
- Equal-talent wealth ratio for locals (elite university): v3.1 1.18 (1.03-1.60). At equal zhongkao score the ratio is 0.85 (0.62-1.03): poorer pupils do better than richer pupils with the same gate score. Unconditional: 2.04 (1.22-3.27).
- Head-start fade is the dominant driver (rank correlation about -0.5 to -0.8). Fade sweep: equal-talent ratio 1.44 at no fade to 1.01 at 90% fade (school VA 0.1).
- Non-hukou cohort (v3.1, shares of all non-hukou pupils): public academic 37%, private 12%, leave/return home 18%, vocational 33%. The hukou gap among those who stay is small (1.16) while exclusion at entry is large; the cohort share of non-hukou pupils (unknown) drives exit.
- Zhibiao effect on the local wealth gap: median +0.002 (helps in 59% of draws). Re-banding: +0.04 (helps in 78%).
- Equation tests: school fixed effects report 2.2-2.4 SD elite-school gaps where the causal label effect is 0-0.5 SD; between-school variance share about 60% vs about 0.1% true value-added share; linear-in-means peer coefficient flips sign without re-banding; RD at the elite cutoff is too noisy at this sample size.

## Known problems (from external review and the informant, not yet fixed in the model)
1. Pre-gate tutoring did not stop after 2021 (private 家教; primary and junior). The "current cohort near-level" result is too optimistic.
2. Holiday tutoring (summer pre-learning; winter except ~3 days) is absent from the model; time control holds in term only.
3. Senior-2 re-banding is often by subject combination, not performance.
4. Term-time tutoring concentrates at both tails (very weak, very ambitious), not near cutoffs.
5. Full-time institutional study while keeping school registration (one-to-one ~100,000+ yuan/month; small classes 60,000-80,000/semester; informant estimate ~5% of gaokao takers, denominator unconfirmed) is not modelled.
6. Academic-track share may be ~50% (informant), not 60-70%.
7. Interprovincial admission quotas are outside the model.
8. Fairness results are conditional on the "equal latent talent" definition; see v3.1 equal-zhongkao and unconditional measures.
9. Three citywide seat totals disagree (101,724 / about 93,000 / 104,584); 30 of 153 schools lack district matches.

## Next
Rerun as v4 with items 1-6, fade as the organizing variable, and tutoring effects swept; extend Lean to v3 rules.

## v4 (informant corrections), 400 draws, seed 20261129 — added 2026-11-26 23:25 CST
Pre-registration `prereg/PREREG_V4.md`; model `model/gz_v4.py`; results `results/v4_results.jsonl`, `results/V4_ANALYSIS.txt`.
- V1 current system fairer than the pre-2021 regime at equal talent: 66% of draws (needed 90%) — NOT SUPPORTED. Median improvement 0.02.
- V2 post-gate tutoring (term, holiday, full-time) still leaks wealth: 83% (needed 80%) — supported; median 0.04.
- V3 pre-gate tutoring still leaks wealth: 76.5% (needed 80%) — NOT SUPPORTED; median 0.03.
- Equal-talent wealth ratio (locals): median 1.31 (1.09-1.82); by head-start fade from 1.57 (no fade) to 1.15 (75-90% fade). At equal zhongkao score: 0.87. Unconditional: 2.28.
- Largest drivers: head-start fade (-0.64), home inputs (+0.56), zone teachers (+0.30); tutoring parameters are secondary (post-gate effect +0.18).
- Reading: with tutoring persisting as the informant describes, the model's earlier "near-level" result disappears, and the tutoring and boarding policies explain little of the remaining gap; home inputs and zone schools before 15, and how fast their advantage fades, explain most of it.

## v5 equation tests (insurance demand, art and Hong Kong routes), 300 draws, seed 20261130 — 2026-11-27 00:00 CST
Pre-registration `prereg/PREREG_V5_EQUATIONS.md`; results `results/V5_EQ_ANALYSIS.txt`.
- E74 tutoring-achievement with prior-score and SES controls MISLEADS: it understates the true effect by a median 0.14 SD because both-tail selection (weak pupils tutor more) survives the controls. This can produce the null or negative estimates in the CEPS literature even when tutoring helps.
- E76 SES x tutoring interaction: spurious (|t| > 2) in 63% of draws although the true interaction is zero.
- E58 participation logit on income: misses the both-tail (U-shaped) demand; pseudo-R2 0.06 vs 0.35 with score and score squared.
- E79 peer effect in tutoring demand: about 0.9 in every draw whatever the true peer effect (rank correlation 0.2): an artefact of class sorting.
- E35 school FE and E159 variance shares measure intake, not value added; E36 peer, E152 RD, E32 VA and E34 teacher effects are biased or noisy in this system.
- Art and Hong Kong routes take a median 10% of elite seats (3.5-19%, depends on assumed size and bonus) and add 0.07 to the equal-talent wealth ratio.
- Proposed new equations: class as the unit of provision; school-vs-class margin trade-off; positional-insurance demand (both tails, fear of falling, peer escalation, time windows by term and holiday); gate switching (admission on the best of several routes, with access by wealth or status).

## Erratum (2026-11-27 00:20 CST)
Partial re-banding in gz_v4/gz_v5 (v4 and v5 runs above) let the top-band size grow. Fixed (composite rank). v6 supersedes
the v4 scenarios. The v5 equation tests were rerun with the fix (results/V5_EQ_ANALYSIS_fixed.txt); every verdict is unchanged.

## v6: the author's four claims, 400 draws, seed 20261201 (PREREG_V6.md)
- M1 fair by its own idea of merit ("same score, same chance"): SUPPORTED, 93.5% of draws <= 1.10. Median ratio 0.90: at the same zhongkao score, poorer local pupils do slightly better later.
- M2 fairer than a stylised Hong Kong: NOT SUPPORTED at the 90% bar. Equal talent: lower in 76.5% of draws (median -0.05); unconditional: 63.7%. The stylised Hong Kong is built from Guangzhou's population; buying elite-school seats does little when school value added is small.
- M3 rich routes under 5 admission points per 100,000 yuan: NOT SUPPORTED at the 80% bar (72%). Median 2.9 points per 100,000 yuan.
- M4 double reduction on its own terms (partly by construction): pre-gate take-up 40% to 27%, mean household tutoring spend 40,500 to 29,800 yuan (-26%), equal-talent gap 1.43 to 1.35 (current lower in 84% of draws).
- Equal-talent gap (CURRENT) median 1.35 (1.12-1.88); by head-start fade from 1.55 to 1.16.

## v7: second-review analyses, 150 draws, seed 20261202 (PREREG_V7.md)
- S* (score and talent both held fixed): 1.18 (1.07-1.40), above 1 in 99% of draws, while S = 0.91. The same-score result is largely composition (collider); after admission richer pupils gain more.
- Realistic counterfactual (boarding, holidays and routes kept; no ban, no re-banding) to now: T 1.41 to 1.35 (lower in 79%); spend 34,600 to 29,000 yuan per pupil over junior 1-3 and senior 1-2 (lower in 99%).
- Shapley shares (all off to all on), T: ban -0.01, boarding -0.01, re-banding -0.04, substitution into holidays/institutions/routes +0.10. Spend: ban -4,600, boarding -5,600, substitution +13,600.
- Interventions on the current system, T: no home advantage 1.19, equal zone teachers 1.25, no pre-gate tutoring effect 1.32, all three 1.09, no art/joint-exam routes 1.27.
- Paper: Claude Docs "Same Score, Same Chance: Procedural Equity and Positional Competition in Guangzhou's Education System" (https://claude.ai/artifact/7z9mQBi5KTjdggJBtnMrWC).

## v8: third-review analyses, 150 draws, seed 20261203 (PREREG_V8.md). Model frozen at v5.1 for circulation.
- S* robust to grid: 1.19 (5x5), 1.20 (10x10), 1.16 (20x20); common support 99%, 92%, 47%.
- Post-gate ablation (same pupils, all wealth-dependent post-gate mechanisms off): S* 1.19 to 1.09 (still > 1 in 94%); median 49% of the excess removed. The rest is persisting pre-gate advantage.
- Ordinary exam only: T 1.25, S 0.85, S* 1.11, U 2.20 (all routes: 1.35, 0.91, 1.19, 2.34).
- Historically anchored (boarding, holidays, routes held on): T paired change -0.06 (lower in 84%); spend paired -4,800 yuan (lower in 99%). Shapley: ban T -0.02, spend -5,000; re-banding T -0.04, spend ~0.
- Interventions (paired): no home advantage -0.15 (44% of excess), equal zone teachers -0.07 (22%), no pre-gate tutoring effect -0.03 (8%), all three -0.24 (74%); learning change among academic pupils 0.00 to -0.02 SD.
