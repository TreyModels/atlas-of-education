# Full-system multiverse integration — Codex wave synthesis (25 November 2026, task-45)

**Branch:** new additive branch `research/codex-wave-synthesis-edsystem-2026-11-25` from the synthesis head
`research/codex-wave-synthesis-2026-11-24` @ `f23f239`; no old head rewritten.

**Sources**

| source | branch @ commit | record file(s) |
|---|---|---|
| full-system multiverse, 1,440 runs (144 equation-choice combinations × 10 seeds; pre-registration `3679f2d`) | `research/masseng-edsystem-2026-11-25` @ `b7108da` | `research/records/2026-11-25-masseng-edsystem/RUN_REPORT.md`; `results_multiverse.json` |
| independent tests: cluster-robust OLS + seed FE + Holm + stratum sign checks | `research/edsystem-tests-2026-11-25` @ `aadbbb4` | `research/records/2026-11-25-edsystem-tests/MULTIVERSE_TESTS.md`; `full_system_tests.json` |

**Status:** toy, uncalibrated `eduengine` simulation — illustrative parameters, no country fit, no causal or
empirical claim. Not history.

**Numbers integrated in §2.5 / §4 / §6 R11:** gates dominate lower/upper completion and wealth completion gaps
(bar .720/.609 vs quota .550/.449; quota−bar −17.0/−16.0pp; bar screens q1 .174 vs q5 .966, gap .792 vs quota .646);
affordability dominates primary/tertiary completion and the poorest quintile's lower completion (cash-only .797/.296
vs credit up to .929/.428; q1 lower .091→.195); jobs regime dominates formal share (.293 queue vs .627 competitive;
+33.4pp [32.4,34.4]); rural structure dominates wealth parity (.245 vs .100; −14.6pp); supply/funding moves public
quality (.99 vs 1.12; +0.132 [0.115,0.149]) but is not identifiable from attainment (overlap 1.00); tutoring is
gate-driven (.273→.499; +22.6pp [21.3,23.9]) and second-order for attainment (η² ≈ 0 for completion; +3.5pp primary
in the learning arm, −0.09 skill premium).

**Engine boundaries (stated in §2.5):** toy/uncalibrated; no persistent learning state; no exam-score gate
(bar-vs-quota seat rules, not score cut-offs); stylised labour market and rural/urban blocks; no migration,
rural–urban sorting or remittances; push-out decomposition unusable (exit-reason bookkeeping); PHL level check
construct-limited (simulated lower completion .635 [.550,.833] vs observed 84.8% in 2024; no calibration). Data gaps:
household demand/affordability, learning grade profiles, exam/quota rules, migration flows, credential requirements.

**Disposition:** new §2.5; §4 bullet; §6 recompute row R11 (marked NOT RECOMPUTED, simulation); §8 file map.
No server compute; no branch rewrites.
