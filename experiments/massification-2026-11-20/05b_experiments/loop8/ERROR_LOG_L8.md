# ERROR LOG — Loop 8 (`05b_experiments/loop8/`)

## Run-level
- 256 LHS draws × 5 matched seeds × 4 country configs + wired cohort flows; plus the explicit eps_ec arm
  (4 values × 2 countries × 5 seeds) and the KOR two-margin tabulation. **0 failed cells.**

## Interpretation issues / caveats
1. **Everything is SYNTHETIC/POSSIBILITY — not a fit, not evidence, not validation; programme CLOSED;
   brief-008 identification limits stand.** No closed claim is reopened.
2. **Wiring is by declared distributions**, not point estimates: R01/R04/R07/R13/R21/R22/R23/R24/R29 were
   wired to twoway/shadow-model parameters with literature-grounded ranges (table in EXPERIMENTS_L8.md);
   ECI R41–R49 marked PENDING (no data on disk; no imputation).
3. **The demand-level intercept is fixed (A0 = −1.5)** — no relation supplies a demand level. This is the
   known blocker from loops 4–7, declared before running; low generated levels are therefore expected and
   not tuned away. The predeclared shrink test therefore asks only whether any previously-empty target
   gains support.
4. **Shrink result:** HKG stage gradient 0→1/256 (YES, predeclared shrink), but **KOR stage gradient stays
   0/256** — empty support persists for the Korean gradient. This must be reported plainly, not spun.
5. **Some targets moved against us** (PHL completion 36→0; KOR income-gradient 117→87) and some improved
   (KHM completion 73→142; HKG fee 134→137). All deltas are synthetic possibility fractions under the same
   bands; none is a fit or validation.
6. **eps_ec arm** is run against the negative R13 panel estimate (range includes −1.035; explicit arm
   {−1.035, 0, 0.3, 0.6}); the module still contains the mild positive education→growth channel, effect
   small (~2–3% complex jobs across the whole arm); no synthetic target needed eps_ec>0.
7. **KOR two-margin**: joint 0/256, participation-only 0, intensity-only 229 — both margins present, joint
   Korean pattern still empty support (stronger form of the predeclared one-margin clause).
8. Relation-slot claims PENDING; no git push (Lead handles git).
