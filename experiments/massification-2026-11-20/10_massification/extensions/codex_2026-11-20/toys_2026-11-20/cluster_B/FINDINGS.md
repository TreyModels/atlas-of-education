# FINDINGS — Cluster B toy battery (experiments #4, #5, #6)

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.**
No historical test. Phase remains CLOSED. Nothing here may be cited as an estimate, a
calibrated parameter, or a validation of any rival theory. Every number below is a
property of the stipulated rules recorded in `PRE_DECLARATIONS.md` and
`RUN_MANIFEST.json`; a threshold that passes says the rules can generate the pattern, not
that the world does.

Spec: `extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md`, Cluster B (#4–#6).
Base model: `model.py` / `experiments.py` (`codex-massification-5eec11470690`), reproduced
exactly at seed 41, visibility 0 (`applications=89, public=30, private=15, admissions=45,
graduate_hires=40`; asserted in `code/test_toys.py`).

## 0. Run facts

- 500 seeds per cell (`seed = 20261120 + rep`), paired: identical latent draws in every arm
  of a seed; one-factor shocks only.
- Cells: 6 (exp4) + 6 in exp5 (4 mandated arms + 2 paired reference cells) + 8 (exp6:
  2×2 × two credential-share regimes) = 20 cells, **84,000 result rows**, no cell dropped.
- `RESULTS.csv` sha256-16 `e672272f008a25c9`; re-running the pipeline reproduces the file
  byte-for-byte. `code/test_toys.py`: 12 structural tests pass (accounting, pairing, seed
  fidelity, determinism, CSV schema).
- Standard library only (`numpy_used: false`). Fixed parameter vector in
  `RUN_MANIFEST.json` → `parameters`.
- Verdicts (from `code/summary.json`, predeclared in `PRE_DECLARATIONS.md`):
  T4.1 **NOT MET**, T4.2 **NOT MET**, T4.3 **PASS**, F4 not triggered;
  T5.1 **PASS**, T5.2 **PASS**, T5.3 **PASS**, T5.4 **NOT MET**, D5.5 **PASS**, D5.6 **PASS**;
  T6.1 **NOT MET**, T6.2 **PASS**, T6.3 **PASS**, T6.4 **NOT MET**, F6 not triggered.

## 1. Experiment 4 — visibility × mechanism (HC vs signalling)

Cell means over 500 paired seeds (40 jobs; 30 public seats; HC adds +1 skill per graduate;
signalling premium 4·(1−v); employer score `v·skill + (1−v)·credential`):

| arm | applications | admissions | graduate hires | output_true_hires | output_valued_hires | rejected n | rejected skill |
|---|---:|---:|---:|---:|---:|---:|---:|
| human_capital v=0 | 85.85 | 48.79 | 39.98 | 1.498 | 1.000 | 45.86 | 0.688 |
| human_capital v=0.5 | 85.85 | 48.79 | 39.98 | 1.585 | 1.292 | 45.85 | 0.613 |
| human_capital v=1 | 85.85 | 48.79 | 39.98 | 1.585 | 1.585 | 45.85 | 0.613 |
| signaling v=0 | 85.85 | 48.79 | 39.98 | 0.499 | 1.000 | 45.86 | 0.496 |
| signaling v=0.5 | 28.45 | 27.26 | 27.26 | 0.627 | 0.654 | 1.03 | 0.455 |
| signaling v=1 | 0.00 | 0.00 | 0.00 | 0.796 | 0.796 | 0.00 | — (no applicants) |

Paired per-seed changes (mean; share of 500 seeds with the stated sign):

| change | true output | valued output |
|---|---:|---:|
| HC v0→v0.5 | **+0.0866** (100% +) | +0.2927 (100% +) |
| HC v0.5→v1 | **0.0000** (100% zero) | +0.2927 (100% +) |
| SG v0→v0.5 | **+0.1281** (99.8% +) | **−0.3453** (100% −) |
| SG v0.5→v1 | **+0.1687** (100% +) | **+0.1413** (100% +) |
| SG applications v0→v1 | −85.85 (100% −) | — |

**T4.1 (primary, true output among hires) — NOT MET.** The HC leg holds: +0.0866 ≥ +0.05,
monotone non-decreasing (flat at v=0.5→1, because at both levels the top-40 by score are the
same highest-skill graduates). The signalling leg **fails**: true output among hires *rises* at
both steps (+0.128, +0.169), 100% sign consistency. The predeclared "signalling output falls
as v rises" is not generated.

**T4.2 (employer-valued output) — NOT MET, but for a different reason.** The endpoint
comparison matches the council pattern (HC +0.585, signalling −0.204), and the first step is
exactly as predicted (signalling valued output −0.345 as the credential premium decays), but
the v=0.5→1 step **reverses** (+0.141): at v=1 the signalling market has no applicants at all,
so the valuation term `(1−v)·credential` is zero and hires are scored on true skill. The
predeclared monotonicity leg fails; the pattern holds only between v=0 and v=0.5.

**T4.3 (rejected-skill composition) — PASS.** At v=0.5: rejected-set size gap 44.8 applicants
(45.85 vs 1.03), rejected-skill gap 0.157, graduate-hire gap 12.7. At v=1: rejected-size gap
45.85 (the signalling cell rejects nobody — it has no applicants), graduate-hire gap 39.98.
**F4 falsifier not triggered**: the signatures do not coincide (output_true gap 0.999 at v=0,
0.958 at v=0.5, 0.789 at v=1).

**Reading.** Under the base model's premium rule, visibility does not *degrade* a signalling
signature; it **shuts the signalling market down** (applications 86 → 28 → 0). Hiring then
falls back to visible skill, which raises the measured skill of hires for both mechanisms.
So the only stable discriminator in this toy is **composition** (who is rejected, how many
graduate hires), not the direction of the output response. A "falling signalling output"
signature has to be *stipulated into the output metric* (the valued metric's `(1−v)` weight),
and even then it is non-monotone. F4's v=0 leg can never fire (the HC definition adds +1
skill, so the two mechanisms differ in true skill from the start); it is informative only at
v≥0.5, where the gaps are large.

*Caveat that matters:* the v=1 signalling cell is degenerate (0 applicants, 0 admissions). The
failure of T4.1/T4.2 is partly a consequence of the stipulated premium reaching exactly zero
at v=1. No alternative premium rule was run, because none was predeclared.

## 2. Experiment 5 — queue vs human capital under fixed jobs

Cell means over 500 paired seeds. Fixed older-diploma group = 20 people (fixed membership);
treated = 20 fixed young people; fixed jobs J0 ∈ {35,…,40} per seed; responsive = 100.

| arm | older-group hires | treated hires | total hires | output among hires | population mean skill |
|---|---:|---:|---:|---:|---:|
| skill upgrade, fixed | 4.38 | 20.00 | 37.50 | **1.2126** | 0.6983 |
| rank upgrade, fixed | **0.00** | 20.00 | 37.50 | **0.6608** | 0.4983 |
| reference, fixed | 7.61 | 7.55 | 37.50 | 0.8080 | 0.4983 |
| skill upgrade, responsive | 20.00 | 20.00 | 100.00 | 0.6983 | 0.6983 |
| rank upgrade, responsive | 20.00 | 20.00 | 100.00 | 0.4983 | 0.4983 |
| reference, responsive | 20.00 | 20.00 | 100.00 | 0.4983 | 0.4983 |

Paired differences (mean, 500 seeds): rank−reference older hires **−7.61** (99.8% negative);
rank−skill older hires **−4.38** (99.4% negative); rank−reference output **−0.147** (100%
negative); skill−reference output **+0.405** (100% positive); rank−skill output **−0.552**;
rank−skill output under responsive jobs **−0.200** (100% negative, sd ≈ 0).

**T5.1 PASS.** Rank allocation drives older-group hires to 0.00 vs 7.61 (reference) and 4.38
(skill): the credential-inflation queue ranks all 80 young ahead of the 20 older-diploma
holders, and with ≤40 jobs no older worker is hired.
**T5.2 PASS.** Rank output 0.6608 ≤ reference 0.8080 − 0.05.
**T5.3 PASS.** Skill upgrade output 1.2126 ≥ reference + 0.05.
**T5.4 (literal council claim: separation disappears under responsive jobs) — NOT MET.**
Responsive gap is |0.4983 − 0.6983| = **0.200**, far above the declared 0.05.
**D5.5 PASS** (older-hire separation does disappear: 20 vs 20, gap 0.0).
**D5.6 PASS**: the residual responsive output gap equals the stipulated population skill gap
(−0.200 = −20 people × 1.0 skill / 100); the **allocation-induced component is ~5.6e-17**.
Attenuation of the fixed-jobs gap: 63.8%.

**Reading.** In this toy the rank-vs-skill separation is a **rationing phenomenon**: it exists
only while jobs < applicants. Under full absorption both arms hire exactly the same people,
so the allocation rule stops mattering (D5.5, D5.6) and the only remaining output gap is the
+1.0 skill the skill arm literally added. The council's "separation disappears" is therefore
true for the *allocation* component and the *older-group composition*, but false for the
raw output gap — which is exactly the confound a real test would face: an observed output
difference can be a rationing artifact or a real productivity difference, and this toy shows
the two are separable only by an assumption about how many jobs there are.

*Load-bearing stipulation:* the rank rule ("the new credential outranks the old diploma, all
young ahead of all older-diploma holders") is what produces T5.1/T5.2. A weaker queue (only
the 20 treated jump) would leave older-group hires unchanged between arms by symmetry. This
rule is a stipulated credential-inflation story, not a finding.

## 3. Experiment 6 — eligibility repeal vs blind ranking

Offer rate among uncredentialed applicants (35 offers; credential uncorrelated with true skill
by stipulation):

| credential share | ranking | gate | uncred offers | cred offers | total offers | uncred rate | vacancies |
|---|---|---:|---:|---:|---:|---:|---:|
| 45/55 (main) | visible | repealed | 0.00 | 35.00 | 35.00 | **0.000** | 0 |
| 45/55 (main) | visible | retained | 0.00 | 35.00 | 35.00 | **0.000** | 0 |
| 45/55 (main) | blind | repealed | 19.25 | 15.75 | 35.00 | **0.350** | 0 |
| 45/55 (main) | blind | retained | 0.00 | 35.00 | 35.00 | **0.000** | 0 |
| 25/75 (sensitivity) | visible | repealed | 10.00 | 25.00 | 35.00 | 0.133 | 0 |
| 25/75 (sensitivity) | visible | retained | 0.00 | 25.00 | 25.00 | 0.000 | 10 |
| 25/75 (sensitivity) | blind | repealed | 26.27 | 8.73 | 35.00 | 0.350 | 0 |
| 25/75 (sensitivity) | blind | retained | 0.00 | 25.00 | 25.00 | 0.000 | 10 |

Paired differences (main regime): blind/repealed − blind/retained = **+0.350** (100% positive);
visible/repealed − visible/retained = **0.000** (100% zero); both − visible/repealed = +0.350.

**T6.1 (gate repeal alone raises the uncredentialed rate ≥ 0.15 and to ≥ 0.25) — NOT MET.**
In the main regime repeal alone moves the rate by **exactly 0.000**: with 45 credentialed
applicants and only 35 offers, credential-first ranking fills every offer before any
uncredentialed applicant is reached, so the visible/repealed cell is numerically identical to
the gate-retained cell. In the sensitivity regime (25 credentialed < 35 offers) repeal alone
raises the rate by 0.133 — real, but below the declared 0.25 high level.
**T6.2 PASS.** Blind ranking alone (gate retained) leaves the rate at 0.000 ≤ 0.05.
**T6.3 PASS.** Both levers reach 0.350 ≥ 0.25 (19.25 of 55 uncredentialed applicants).
**T6.4 (repeal is sufficient: ≥ 0.75 × the both-levers rate) — NOT MET.** 0.000 < 0.263.
**F6 falsifier not triggered**: the four main rates are not equal (0, 0, 0, 0.350).

**Reading.** In this staged screening toy the gate and credential visibility are
**complements, not substitutes**: removing the gate while the credential remains visible at
ranking buys nothing when credentialed supply covers the offers, and only ~0.13 when it does
not. The council's prediction that "gate repeal raises the uncredentialed offer rate to the
high level" is not produced. The design implication for the C3-adjacent test: an eligibility
or licensing repeal studied *without* a change in credential visibility would be expected,
under this stipulation, to show a near-null — and a null there would not disconfirm the
queue/signalling reading. Conversely a blind-ranking mandate with the gate intact also shows
nothing (T6.2). Only a joint change is informative.

*Load-bearing stipulation:* credentials are independent of true skill. That is what makes
blind ranking raise uncredentialed offers; with a positive credential–skill correlation the
blind-ranking cell would still favour skilled applicants and the contrast would shrink.

## 4. What the three toys jointly say about a C3 rival discriminator

1. **Visibility alone is not a clean discriminator** (#4). It changes who is hired and who is
   rejected (large composition gaps), but it does not produce the council's output sign
   pattern: both mechanisms' hires become more skilled as skill becomes visible, because
   better information improves selection for everyone and, at v=1, the signalling market
   simply ceases to exist. A real test that leaned on "signalling output should fall" would
   be testing a metric convention, not a mechanism.
2. **The queue reading is a rationing reading** (#5). Rank-vs-skill separation is large under
   fixed jobs and vanishes — in composition and in the allocation component of output — the
   moment jobs absorb the queue. Any empirical claim that "queue allocation lowered output"
   is therefore conditional on job rationing, which is exactly the kind of auxiliary
   assumption the council's C3 test would need to defend.
3. **Single-lever credential policies are weak instruments** (#6). In the staged toy, only
   the joint removal of gate *and* visibility moves uncredentialed offers to the high level.
   A natural experiment based on one lever would be underpowered by construction.
4. **No falsifier fired.** In all three toys the mechanisms' signatures differ somewhere — the
   falsifiers ("signatures coincide", "no separation", "no effect of either lever") were not
   triggered. That is not support for any theory; it says these toys are built so that the
   stipulations bite. What failed were the council's *directional* predictions (T4.1, T4.2,
   T5.4, T6.1, T6.4), and those failures are informative about which auxiliary assumptions
   the predictions silently rely on.

## 5. Failures, degenerate cells and caveats (complete list)

- **T4.1 NOT MET**: signalling true output rises with v (+0.128, +0.169), not falls.
- **T4.2 NOT MET**: valued-output pattern holds from v=0 to v=0.5 (−0.345) but reverses at
  v=0.5→1 (+0.141); monotonicity leg fails.
- **Degenerate cell**: signalling at v=1 has 0 applicants, 0 admissions, 0 rejections — "skill
  of rejected applicants" is undefined there (recorded empty in `RESULTS.csv`).
- **F4's v=0 leg is structurally unfirable**: the HC rule adds +1 skill, so the mechanisms
  differ in true output at v=0 by construction (+0.999).
- **T5.4 NOT MET**: responsive gap 0.200; the "disappearance" holds only after netting out the
  stipulated skill increment (D5.6) and for older-group composition (D5.5).
- **T6.1 and T6.4 NOT MET**: repeal alone is a no-op in the main regime (0.000) and 0.133 in
  the sensitivity regime; it is not a sufficient lever.
- **exp5's rank rule is an extreme stipulation** (all young outrank all older-diploma
  holders). A weaker queue would null out T5.1/T5.2 by symmetry. The result is a property of
  the stipulation.
- **exp6 assumes zero credential–skill correlation**; this forces the blind-ranking result.
- **exp4 uses the base model's premium rule** (`4(1−v)`, zero at v=1), which makes the v=1
  signalling cell degenerate. Not varied, because not predeclared.
- No model in this battery has equilibrium wages, vacancy posting, firm heterogeneity, or
  any empirical input. All are one-shot allocation toys.

## 6. Reproduction and file hashes

Run from `extensions_archive/toys_2026-11-20/cluster_B/`:

```
python3 code/run_all.py --smoke      # structural invariants only
python3 code/run_all.py              # full 500-seed battery -> RESULTS.csv, RUN_MANIFEST.json
python3 code/test_toys.py -v     # 12 structural tests
```

| file | sha256-16 |
|---|---|
| `PRE_DECLARATIONS.md` | `8bf544761ac661a3` |
| `RESULTS.csv` | `e672272f008a25c9` |
| `RUN_MANIFEST.json` | `619dd97b83de6ad6` (includes hashes of all code and the spec) |
| `code/toy_common.py` | `f75658c6e3cb09a4` |
| `code/exp4_visibility.py` | `3d70318135a67b9d` |
| `code/exp5_queue.py` | `46dd9a16eabff334` |
| `code/exp6_eligibility.py` | `cd20493bf6683184` |
| `code/verdicts.py` | `0cdb31591e4071e4` |
| `code/run_all.py` | `f8ac20baed1b1dbc` |
| `code/test_toys.py` | `d45dff3ad0c4689b` |
| `code/summary.json` | generated artifact of the last run |

`RUN_MANIFEST.json` also records the spec and base-model hashes, the full imposed parameter
vector, the arm lists, the seed rule, the verdict summary and the failure list.

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.**
