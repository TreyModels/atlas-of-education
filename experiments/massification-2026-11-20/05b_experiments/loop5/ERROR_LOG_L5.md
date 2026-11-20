# ERROR LOG — Loop 5 (`05b_experiments/loop5/`)

## Run-level
- E1 (3 arms × 2 country configs), E1b, E4 executed; **0 failed cells** (numpy-only, single process).

## Interpretation issues / caveats
1. **E1 FAIL is a level failure, not a shape failure.** Under frozen structural parameters and NO
   take-up fitting, the gate-stakes arms produce the right gradient shapes (KOR falling under
   gate-each-transition 27.3→24.4; HKG rising under terminal-only 14.4→46.7) but levels 20–59 pp below
   the observed rates. The predeclared ±5 pp threshold is on levels, so E1 FAILS and the gate-position
   story is dropped; the shape-only observation is reported as a diagnostic, not a claim.
2. **Policy-dated assignment is declared, not verified.** KOR CSAT 1994 date is ASSUMED; HKG HKDSE 2012
   is in the card but the card itself says dates were not independently verified. The KOR
   gate-each-transition and HKG terminal-only assignments are declared mappings, not measured
   architectures.
3. **E1b direction checks are mixed.** Hours direction passes (falling participation + rising spend),
   provider direction fails (commercial share 41.4% < the 50% pass bar; observed hagwon is 55.5% of
   spend). Per the predeclaration the mixed result and the 43–58 pp level misses mean E1b FAILS and the
   stop-rule stands permanently.
4. **E4 first pass was a mechanical identity** (spend scaled by the declared income multiplier, ratio
   4.00 by construction). Fixed before reporting: demand is recomputed per income band at the single
   market price, giving a demand-consistent ratio **2.14** (monotone, inside the predeclared band). The
   mechanical 8.55 is reported only as a diagnostic.
5. **Hours level 7.3 h/wk is UNABLE** (no hours object) in both E1 and E1b; not used as a pass condition
   (per predeclaration), but it also cannot rescue any claim.
6. **Relation slots PENDING:** `09_relations/` slot tables were not consulted; no relation-slot claim.
7. KHM/PH transfer not run (out-of-sample, expected to fail per predeclaration).
