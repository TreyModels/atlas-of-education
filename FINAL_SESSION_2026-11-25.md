# FINAL SESSION RECORD — 25 Nov 2026 (before AutoDL release)

This closes the session that began at 00:18 CST. Everything below is pushed to
`https://github.com/TreyModels/atlas-of-education`. **QA is CLEARED** (adversarial gate, 16+ branches,
no FAIL; `~/neon-boot/QA_GATE_2026-11-25.md`).

## Heads (origin)

| branch | head | what |
|---|---|---|
| `research/handoff-2026-11-24` | this commit | handoff + quarantine addendum + retraction fixes + final record |
| `research/papers-2026-11-25` | `5223284` | **Paper #1** phase transition, **Paper #2** massification, **Paper #3** silent-failures methods, `RESULTS_DOSSIER_2026-11-25.md` |
| `research/phase-transition-2026-11-25` | `f1c16f1` | quick-grid prereg `408aa3e`, run, ABSENT/PARTIAL verdict, `REPRODUCTION_STATUS` |
| `research/phase-transition-dense-2026-11-25` | `ced04a7` | dense prereg `8b0cc88` + statistic amendment `40159c7` + **SIGNATURE verdict** |
| `research/binding-gate-2026-11-25` | `68da16e` | prereg `37cbe3d` + binding sweep results (H1 supported, H2 null) |
| `research/equifinality-phase-2026-11-25` | (parallel window) | 16k-run dense grid, executed by `lead-nb` |
| `research/box-runs-2026-11-25` | `75968e6` | fixed-driver 1,440 + 5,760 runs, sweeps, DHS patched verify, lockfile, boundary/equifinality |
| `research/equation-suite-neon-fixes-2026-11-25` | `575d4cd` | Neon Part A+B, re-record, S10 flags, deviations |
| `research/dhs-corrected-2026-11-25` | `22de735` | AUTHORITATIVE corrected DHS record |
| `research/dhs-api-ecological-2026-11-24` | `792dba1` | code chain + `SUPERSESSION_2026-11-25.md` |
| `research/dhs-ir-pipeline-neon-2026-11-25` | `fc9b7f7` | Neon ir_pipeline patch + PSU deviation amendment |
| `research/dhs-eco-gfr-uncomputed-2026-11-25` | `792dba1` | GFR mirror (canonical FF'd) |
| `research/bulge-arrival-2026-11-25` | `1b91a71` | E6/E8 packet, t* NOT-ESTIMABLE |
| `research/bulge-micro-dhs-2026-11-25` | `230521b` | DHS micro data gate (0/48), LSMS not held |
| `research/masseng-gate-jobs-neon-2026-11-25` | `9d79df1` | v6 fixes + tests (fail-on-base pattern) |
| `fix/edsystem-exit-reason-2026-11-25` | `4679ddb` | e.exits driver fix + retraction |
| `fix/edsystem-tests-pinv-2026-11-25` | `3e35ff0` | rank/stratum guards, 45/72 + 28/72 |
| `fix/equation-test-bench-2026-11-25` | `2c575d9` | F9 lag join, singular control |
| `research/edsystem-audit-2026-11-25` | `3afac25` | FS-12 erratum |
| `research/masseng-edsystem-2026-11-25` | `d87b89f` | RUN_REPORT retraction |
| `research/codex-wave-synthesis-2026-11-24` | `6935026` | SYNTHESIS retraction |

## Headline results
1. **Phase transition (SIMULATION)**: no boundary under a non-binding bar gate (J_max 2.88 < 4);
   **SIGNATURE boundary under the binding quota gate on the vacancy axis** — tutoring Q5−Q1 gap
   J=11.50 at vac0 0.4005→0.5044 (sharpness 18.17), gate-fail J=12.58 (23.48); gate contrast 0.074;
   **374 equifinal pairs** (same attainment, tutoring differs >20 pp); seat scarcity monotone
   (Spearman −1.00) but the fee × scarcity interaction is a **null** (+0.0039, CI [−0.019, +0.027]).
2. **eduengine driver** was misreading exits (engine correct); corrected decomposition q1 liquidity
   **68.99 %** vs universal 0.0 before.
3. **DHS corrected**: Africa-11 2-group ratio **1.0698 [0.9987, 1.1403]** (incl. 1.0);
   C_vs_B **−0.1962 (0.0495)**; the move is the **interaction-set change**, not the multiplicity fix.
   Patched re-run **PASS_BYTE_IDENTICAL** (13/13, 27/27, M4 passed, IR infeasible).
4. **Five silent failure classes** documented with receipts (Paper #3): resampling multiplicities,
   transposed TWFE, `pinv` masking rank deficiency, `e.kids` vs `e.exits`, `returncode==0` vs
   `decision_rule.PASS`.
5. **E6/E8**: E6 demand-first 10.0–24.1 % (auditor's 76–90 % does **not** reproduce); E8 CS post
   +22.12…+28.56 pp, on-impact +12.44 (CI includes 0); RI T_obs 12.4436, p 9.999e-05/5.999e-04;
   `t*` **NOT-ESTIMABLE** (L_primary 0/8).

## Box / power
- Instance `autodl-container-a8f742b5ee-292349c5`, `ssh -p 45973 root@connect.cqa1.seetacloud.com`.
- All runs pulled; no job running; replication lockfile committed in `box-runs`.
- **POWER RULES (absolute)**: see `NEON_FREE_FIXES_2026-11-25.md` / `~/neon-boot/POWER_RULES_2026-11-25.md`.
  An agent-authored `shutdown_after_two.sh` powered the box off at 00:31:04 CST and was recovered; both
  watchers are `*.DISABLED_2026-11-25`. The operator later authorised a single shutdown *after everything
  finished*, executed via the lease protocol in `~/neon-boot/BOX_LEASE.md`.

## Open / next
- Paper drafting continues (no empirical work needed): finish #1–#3, then the Paper #1/#2 sketch with the
  auditor ("Zero Universal Laws, 32 Regimes").
- DHS individual-level (IR) leg: 0/48 microdata held → needs a data-access request.
- E1 wild-cluster bootstrap: regenerable in principle (WB API `sweep.py`), not bit-reproducible
  (vintage); needs ~1.5 h/8 cores.
- Quarantine remains on `research/equation-test-bench-2026-11-25` @ `02d930c` and
  `research/shadow-equations-review-2026-11-25` @ `264c059` — do not cite.
