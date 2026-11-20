# TUNE_LOG — EXP-14 V16-REPAIR

**Purpose: an unflattering, chronological record of everything that was decided, seen, changed and frozen.**
Two rules governed the run and are stated first:

- **No parameter, threshold, band, year set, arm-scoring rule or verdict word changed after the scored run.**
  The scored run is `python code/run_v16.py` writing `results/` (and `results/determinism_run2/`), with the
  predeclaration sha256 `6a554dc0…` embedded in `code/sim_v1_6_repair.py` at build time.
- **Nothing was tuned to the observed path.** No parameter was chosen, rescaled or selected from a grid by
  reference to any level, any observed cell, the 17/33 bar or the `[55,85]` band. The declared grids are reported
  in `results/sensitivity_arms.csv`; the scored value is the pre-declared value in every case.

Clock times are local, from the file mtimes, not from any in-output timestamp (no wall-clock enters any result).

---

## C1. Pre-run probe of A10 — **disclosed: I saw the level before the final freeze** (00:47–00:50)

**What I did.** After `build_v16.py` produced a byte-identical A00 panel (`47d4b082…`), I ran three machinery
probes: (i) the A00 identity, (ii) an A11V15-vs-v1.5 equality check, (iii) a **smoke run of A10** and the 33-cell
count on it.

**What I saw.** A10's levels (primary 81.25, lower 74.67, upper 57.41 at 2024) and the count **0/33**, before the
final predeclaration hash was taken.

**What I changed as a result.** The only pre-freeze amendment: **added the diagnostic decomposition arm
`D1_survonly`** to `PRE_DECLARATIONS.md` §4, so that "which obligation changed what" would be a declared comparison
rather than a post-hoc one. Its values are v1.5's own (`v_O = 0.45 v_H`, survival multipliers set to 1.0), not chosen
by any level. The predeclaration was then re-hashed (`70412050…` → `6a554dc0…`) and the code rebuilt so that the new
hash is embedded. **No parameter, threshold, band, arm-scoring rule or verdict word changed.** This is recorded
because a probe that reveals the headline before the freeze is exactly the kind of thing a predeclaration exists to
make visible.

## C2. The injection register — rate → count (00:49)

The counterfactual identity first failed with **373 differing of 598 080 cells** even though the two panels were
byte-identical as CSV. Cause: I injected the upper admission **rate** and multiplied by `C`, and `(a/C)·C ≠ a` in
floating point — a last-bit residue that `%.10g` hides. **Fix: inject the admission COUNT vector** (A01D's
`admitted_official` column) directly, which is also what "feed A01's upper admission vector into A00's accounting"
literally says. Identity then **0/598 080**. Fixed **before** the scored run; no parameter involved.

## C3. `demand_official` double count (00:46)

v1.5 reported `D_off = A_H + A_O_cand`, where `A_H` already contains the refused Tier-H applicants and `A_O_cand`
contains them **again** among those who accept Tier O. That inflates the reported applicant object (primary demand/C
1.57). **Fix (V16 D-2):** `D_off = A_H + A_O_first` (unduplicated applicants), declared in the code comment and in
PARAMS. It changes no admission decision, only the reported demand/rationed objects — which are exactly the objects
R5c tests, so leaving it would have contaminated the child-wage pre-cap leg. The reconstruction arm keeps the v1.5
form (`dup_demand=True`) so the reconciliation is like-for-like.

## C4. Tertiary tier composition — the one within-year feedback **removed** (design, 00:44)

v1.5 disclosed that the tertiary tier *composition* inherited the **same-year** upper-secondary choice shares
(D131 post-run disclosure (iii)). That is a same-year cross-level dependency, which R2's one-way requirement forbids
unless declared. **Fix: the tertiary composition now reads the ENTRY cohort (`t − DVEC[2] = t−3`)** — the cohort that
actually graduates at `t`. This is the only behavioural design change made under R2, it is declared in
`PRE_DECLARATIONS.md` §3.2 (W2) and in FINDINGS §8, and it is inert for A00 (identity verified).

## C5. **My own predeclaration error: R5c named an arm that cannot produce its objects** (found 00:56, recorded, NOT fixed)

`PRE_DECLARATIONS.md` R5c names **A01D** (the capped arm) and then asks for `demand_official`, **`A_H`** and the
**Tier-H queue**. A01D is `bimodal OFF` — it has no tier block, so `A_H` and the Tier-H queue do not exist in it.
This is exactly the error class D134(4) called out for the a-iv leg: **a leg named by one switch when two are
orthogonal.** I did **not** change the leg, the arm, or the verdict: C2 is scored as written and reported **`MIXED`**
(one of three objects scorable, and it holds at −0.4776 pp), with the two missing objects reported from a post-hoc,
non-verdict-bearing arm `A11K` (`bimodal ON + kappa ON`) where they are also exactly zero. Recorded in
`FINDINGS.md` §6 and in `v1_6_checks.csv` row C2.

## C6. Per-country injection bug (found 00:52, fixed pre-run)

The first working injection built the vector from the **anchor country only** and applied it to **all 30 countries**,
so the "identity" was computed against a panel where 29 countries had been given the Philippines' upper admission
counts. Caught by the identity guard itself (175 353 differing cells). **Fix:** `inject_upper` is a dict keyed by
country name. No parameter involved.

## C7. `phys_cap` global-state leak (found 00:54, fixed pre-run)

`run_arm(..., phys_cap=x)` set `P["phys_cap"]` and never restored it, so after the 6-point phys_cap grid the module
global was left at **1.30** and the *second* (determinism) pipeline would have run at 1.30 while the first ran at
1.15 — a determinism failure manufactured by my own driver. **Fix:** reset `P["phys_cap"] = 1.15` after the grid.
Caught before the scored run; the delivered determinism check (17/17) is on the fixed driver.

## C8. The (a-iii) definition — **a check implementation changed after seeing a preliminary result** (found 00:57, disclosed)

My first implementation of (a-iii) required **every** scored cell in a year to hold both conditions; under that
stricter reading A10 scored `2/15` and S3 read `REPRESENTATION-FAILS`. The predeclaration says the (a) family is
**carried verbatim from v1.5**, and v1.5's own code defines a year as holding if **any** cell in that year has both
(`code/sim_v1_5_bimodal.py:1355-1362`). **I corrected the implementation to v1.5's carried definition**, which gives
`15/15`. This is a change to a *check implementation* after seeing a preliminary verdict, and it is disclosed here in
full rather than buried:

- the correction restores the definition the predeclaration says is used (the stricter reading was my invention, not
  the carried check);
- **no threshold moved** (0.10, 1.10, 15/30, 8/15, 0.50 all as carried);
- **the headline verdict is unchanged either way**: the overall verdict formula does not use the representation axis,
  so S1 (0/33) + S2 (1/3) give `PATH-FAILED` under both readings; only the reported representation axis would differ.

I also implemented v1.5's `same_level` definition (spare seats > 0 **and** rationed applicants > 0 at upper
secondary) rather than my earlier ad-hoc count, for the same "carried verbatim" reason: A00 = 0, A10 = 15.

## C9. `lower_channel_report` used the wrong year for the admission rate (found 01:01, fixed pre-run)

The report labelled `entry_year = 2018` but read `admitted_official / cohort` from the **2021** row, so the printed
chain product (67.40) did not match the model's 2021 completion (58.615) and the report implied a chain-identity
failure that did not exist. **Fix:** read the admission rate from the **2018** (entry) row. The chain identity is now
**exact** (error 0.0), which is the check D140 asks for. No parameter, threshold or verdict changed.

## C10. Freeze points

| what | when | sha256 |
|---|---|---|
| `PRE_DECLARATIONS.md` v1 (before the D1 amendment) | 00:44 | `70412050…` |
| `PRE_DECLARATIONS.md` v2 (**frozen, used by the scored run**) | 00:50 | `6a554dc033828835431f65be2e5e218833fcdb56220baad8fbe53c3324e78991` |
| `code/base_v1_3_sim.py` (verbatim frozen v1.3 copy) | 00:42 | `70ae8f0e…` |
| `code/build_v16.py` (frozen with the run) | 00:55 | `38dd9413…` |
| `code/sim_v1_6_repair.py` (built, embeds the predecl hash) | 00:55 | `9c0e7998…` |
| `PARAMS.md` | 00:50 | `5e15dfba…` |
| scored run `code/run_v16.py` (both pipelines, determinism on) | 01:02–01:04 | — |

**After the scored run, nothing was edited except `FINDINGS.md`, `TUNE_LOG.md` and `SHA256SUMS.txt`.** The result
CSVs, panels, `guard_report.json`, `RUN_MANIFEST.json`, code, `PARAMS.md` and `PRE_DECLARATIONS.md` are the ones the
run wrote or read.

## C11. `SHA256SUMS.txt` regenerated (01:05)

The run writes `SHA256SUMS.txt` at the end of the pipeline, which is before `FINDINGS.md` and `TUNE_LOG.md` exist.
It was regenerated once, with the same format and the same exclusions (`SHA256SUMS.txt` itself, `__pycache__`), so
the index covers the narrative files too. **No result file changed**: the earlier index's results hashes are
identical to the final one.

## C12. Things that were seen and **not** acted on

- **`q_O = 1.00` scores 3/33** (vs 0/33 at the declared 0.55). Not adopted; reported as a declared sensitivity. It
  strengthens the negative: even *removing* the open-tier discount does not reach the bar.
- **`S_survpen_0.95` lowers primary to 77.85 and upper to 54.24.** Not adopted; the declared value is 1.000 with its
  own justification and sensitivity (R4c).
- **`S_hshare_plus` raises upper 2024 to 59.80.** Not adopted; `h_share` is a declared A5 value and no on-disk series
  constrains it.
- **`phys_cap` has no bite at the anchor** at any declared value. Not "corrected" by choosing a smaller `phys_cap` to
  make the floor bind — that would be a fit. Reported as the D139 finding.
- **C1's zero.** Not rescued by declaring a bigger shock. The +10 % value is the declared one; the ×1.25/×1.50 rows
  are labelled post-hoc and non-verdict-bearing.

## C13. Process notes

- Scratch probes wrote three CSVs to `/tmp` (`/tmp/a00check.csv`, `/tmp/a00_v16.csv`, `/tmp/a00b.csv`). **No file
  outside `generator_v1_6_repair/` was written or modified in the programme tree**; `git`-equivalent verification is
  the frozen-file hash table in `results/guard_report.json` (17 files, unchanged before/after).
- The driver imports the frozen base as a module (`code/base_v1_3_sim.py`) for the A00 cross-check helpers only; the
  simulated code is the mechanically assembled `code/sim_v1_6_repair.py`.
- No server was touched, no network call was made, no data file was fabricated or imputed.

---

**Freeze statement.** The scored run used `PRE_DECLARATIONS.md` sha256 `6a554dc0…`, `PARAMS.md` sha256 `5e15dfba…`,
`code/sim_v1_6_repair.py` sha256 `9c0e7998…`, seed 20261120. **No parameter, threshold, band, year, arm or verdict
word was changed after it.** The verdict is `PATH-FAILED`; it is reported as delivered.
