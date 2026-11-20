# FINDINGS — v1.4 demand-signal core (EXP-2 / A3-D)

**LABEL: SYNTHETIC / DECLARED. Not evidence. Not an estimate. Not a forecast. No causal and no
direction claim.** Every number below comes from a declared-assumption generator; no real country is
modelled or measured. The demand block is a **declared behavioural assumption**, not an estimated
demand system.

## The one-paragraph answer

**No — the demand block does not replace the declared upper-secondary work-incentive/taste parameter
as the generator of the ceiling.** Under the parameter-free conversion declared before the run, the
demand-derived value is about **2.5× the declared taste value**, so substituting it drives the
upper-secondary demand share to the bound (0.993 in 2024) and upper UIS completion to **95.05%**, far
outside the `[73,77]` band (+18.05 pp above it). d1 and d2 pass in two of three country types but fail
in the `SYN_PHL_LIKE` type (the ceiling country) because its demand is already at the bound; d3 fails
with the wrong sign. The block is **not decorative** — switching it on moves 2024 by **+18.41 pp**,
clearing the 3.0 pp D81 bar — but it matters by *removing the ceiling*, not by reproducing it. The
experiment is **FALSIFIED** on the block's own falsifier. The ceiling in v1.2/v1.3 remains a
**declared-taste** phenomenon.

## 1. The d1/d2/d3/d6 table

| check | threshold | `SYN_HKG_LIKE` | `SYN_PHL_LIKE` | `SYN_KHM_LIKE` | verdict |
|---|---|---|---|---|---|
| **d1** +10% gross `E[R]` → upper demand share at 2020 | ≥ +1.0 pp in all three | **+1.516 pp** ✓ | **+0.151 pp** ✗ | **+4.768 pp** ✓ | **FAIL** |
| d1 sign, every scored cell | ≥ 0 | min **+0.000 pp**; 103 scored, 62 saturated | | | PASS component |
| **d2** `R→2R` at g2, 2020, gate-level demand | ≥ +0.5 pp in all three | **+2.470 pp** ✓ | **+0.233 pp** ✗ | **+10.329 pp** ✓ | **FAIL** |
| d2 shadow demand rises more than non-gate | ordering | shadow **+32.64 pp** | shadow **+31.13 pp** | shadow **+32.03 pp** | structural PASS |
| **d3** office − mfg upper demand, equal graduate flow | ≥ +2.0 pp | — | — | — | **FAIL (−0.584 pp)** |
| **d6** identities | zero violations | 0 / 6,720 rows; shares ∈ [0.000112, 0.998791]; max \|Σshares−1\| = 3.3e−16 | | | **PASS** |

- **d1**: the sign is right everywhere it can be measured, and the response is large in the two
  country types whose demand is not at the bound. It fails the magnitude bar in `SYN_PHL_LIKE` because
  the replacement has already driven that demand share to 0.99; a +10% return cannot add 1 pp to a
  share already at the ceiling. The saturation is reported, **not** used to exclude the cell
  (`PRE_DECLARATIONS.md` §5 d1).
- **d2**: same pattern. The gate-pressure channel is real (+2.5 to +10.3 pp where not saturated) and
  the shadow block responds more strongly (+31 to +33 pp), but the PHL cell is at the bound
  (+0.23 pp). The ordering clause is structural: only g2's pressure is doubled, so non-gate demand is
  unchanged by construction.
- **d3**: the office-biased twin's upper demand is **lower** than the mfg-biased twin's, by 0.58 pp
  flow-matched (raw twins −0.52 pp; their graduate flows are equal by construction). The reason is
  visible in `DETAIL.csv`: the generator's wage ladder pays the production rung (3.2–4.6× informal)
  more than the clerical rung, so when the office twin's composition shifts toward clerical rungs its
  composition-weighted destination wage falls faster than its placement probability rises. The
  access-only variant is −0.55 pp, so it is not the wage term alone. **This is a real falsifier, not a
  coding failure** — but it is a property of this generator's declared rung ladder and destination
  mapping, not a statement about any economy.

## 2. The replacement test (reported, never re-tuned)

| arm | upper UIS 2024 | band | distance | verdict |
|---|---|---|---|---|
| baseline (demand block OFF = v1.3) | **76.6391** | [73, 77] | 0 | INFO |
| replacement (`v_2` → `E[R]×P(advance)`) | **95.0455** | [73, 77] | **+18.05 pp above** | **NOT DEMAND-ROBUST** |

The ceiling is **not demand-robust**. The value is outside the band by 18.05 pp, i.e. far beyond the
2.0 pp falsifier tolerance. **No parameter, coefficient, destination set, migration value, `H`, scale
factor or band was changed after this value was seen.** No re-tune was attempted.

What drives it (PHL 2024, upper secondary): the model's own destination-composition-weighted formal
wage is **59.44** against an informal wage of **8.80**; with `P(advance) = 0.999` (the upper gate is
not rationed in this generator) and `access = 0.722`, the annual net return is **5.32 household
incomes**, giving `E[R]×P(advance) = 5.59` and `v_D = 1.939` against the declared taste
`v_2 = 0.786`. The demand share goes from 0.800 to **0.993**. A demand-driven household in this
synthetic world would fill upper secondary; the ceiling exists only because the declared taste (plus
the work option) holds it back.

The replacement also breaks v1.2 check (a)'s "upper never ≥90 by 2024" property (95.05 > 90). That is
reported as a consequence of the substitution, not scored here.

## 3. The ablation (D81)

| state | upper UIS 2024 | Δ vs OFF | bar | verdict |
|---|---|---|---|---|
| demand block OFF (v1.3) | 76.6391 | — | — | — |
| replacement arm ON | 95.0455 | **+18.41 pp** | ≥ 3.0 pp | **NON-DECORATIVE** |

The block is **not decorative**: it moves the 2024 outcome by 18.41 pp, six times the D81 bar. But
D81-2's logic cuts both ways here: the block matters, and what it does is *destroy* the ceiling. A
synthetic PASS would have been non-diagnostic; a synthetic FAIL of this size is informative about the
generator, not about the world.

## 4. The no-re-fit guard and code integrity

| check | result |
|---|---|
| demand block OFF → panel vs frozen v1.3 panel | sha256 `47d4b082…` **=** `47d4b082…` — **byte-identical (PASS)** |
| placebo: block ON, substitution OFF, liquidity OFF | 76.63908112 and panel sha `47d4b082…` — **byte-identical (PASS)** |
| two clean runs, separate output dirs | **0 cmp failures** on 10 result files + `RUN_MANIFEST.json` (see `results/determinism_note.md`) |

The guard is the analogue of v1.3's c6: with the demand block off, the v1.4 panel contains exactly the
v1.3 bytes (89 columns, same rows, same `%.10g` formatting). The placebo independently confirms that
the block does not leak into the base arithmetic when its substitution is switched off.

## 5. The migration / remittance channel — role and status

**DECLARED / NOT-VERIFIED. No literature coefficient was inserted.** `PUSH_PULL.md` records the
remittance→schooling coefficient as **NOT VERIFIED** (Clemens/Yang not retrievable); a measured
coefficient remains **HELD** and nothing here imputes, proxies or fabricates one. The channel is a
declared behavioural assumption (D02–D05), not an estimate.

Its role in this run is **small**:

| variant | upper UIS 2024 | change vs central |
|---|---|---|
| central | 95.0455 | — |
| migration OFF (`mig_L = 0`, no remittance lift) | 94.9588 | **−0.087 pp** |
| remittance OFF (`remit_prop = 0` only) | 95.0326 | **−0.013 pp** |
| liquidity-only (no substitution, lift ON) | 76.9249 | **+0.286 pp** vs baseline 76.6391 |
| destination differential 2.50 / 4.50 | 95.0087 / 95.0799 | −0.037 / +0.034 pp |

So the declared migration premium shifts the ceiling by less than 0.1 pp and the declared liquidity
lift by ~0.29 pp. Neither is anywhere near the 3.0 pp bar on its own. That is a statement about *this
declared channel's magnitude*, not evidence that remittances do or do not affect schooling anywhere.
d4 (A3's "channel present and labelled") is reported as **INFO / NOT-SCORED**, as A3 requires.

## 6. Sensitivity (pre-declared, cannot replace the central run)

The replacement value stays between **90.90 and 95.34** across the declared grid except for two rows
that change the *kind* of substitution: `ER_scale = 0.75/1.25` gives 94.37/95.34, the destination set
excluding the professional rung gives 90.90, and the NOT-SCORED `arm_R2` numeric work-weight swap
gives **70.12** (−6.52 pp vs baseline). The last row is the alternative reading of "work-incentive
weight": putting `E[R]×P(advance)` in the child-earnings slot makes work *more* attractive (the
demand value is 2–5, the declared work weight ~0.9), collapsing demand and the ceiling from the other
side. **Both readings fail**: one saturates demand, the other collapses it. That is the sharpest
single result of the experiment — the demand object has no dimensionally neutral slot in this
household block, and choosing a scaling factor to create one would be exactly the fitted "demand
parameter" that R4/R27 forbids.

## 7. What this cannot claim

- **No causal claim and no direction claim.** Nothing here says returns do or do not drive schooling
  in the Philippines, Hong Kong, Cambodia, or anywhere else. The generator is synthetic.
- **A synthetic PASS would have been non-diagnostic unless the ablation failed (D81-2).** Here there
  is no PASS; the ablation is non-decorative, which makes the *failure* informative about the
  generator's structure (the ceiling is taste-carried), not about any real education system.
- **The demand block is a declared behavioural assumption, not an estimated demand system.** Every
  value is declared (PARAMS D01–D08); none is estimated, and none was chosen by looking at the 2024
  outcome.
- **The migration/remittance channel is declared, not estimated.** No literature coefficient was
  inserted; HELD data stays HELD.
- **The ceiling claim (D63) is unchanged.** The experiment cannot explain, reclassify or move it; at
  most it shows that in *this* generator the ceiling is not what a parameter-free demand signal
  produces.
- **Two generator-specific limitations bound the reading:** (i) `P(advance)` read from the model's own
  `pi0` is ~0.999 at the upper gate because advances include over-age admissions — the upper gate is
  unrationed, so the gate-probability channel is nearly inert except where the pipeline is small;
  (ii) the model's formal/informal wage ladder is steep (rung multipliers 2.2–6.4), so a
  parameter-free return object is large relative to the household block's normalised income. Both are
  properties of the frozen generator, disclosed rather than adjusted.
- **d3's sign is a property of the declared credential→rung destination mapping** (production pays
  more than clerical in this ladder). A different declared mapping could flip it; that is why it is
  reported with the access-only variant and the raw twin difference.

## 8. What would change the answer (not run here)

1. A **declared, pre-registered scale** mapping `E[R]×P(advance)` into the household block's utility
   units — which is a new declared parameter and must be justified a priori, not fitted to `[73,77]`.
   (The `ER_scale` sensitivity rows deliberately are *not* that: they are reported, not adopted.)
2. A **rationing-based `P(advance)`** (admitted/qualified demand, queue length, rank) instead of the
   model's `pi0`, which is ~1 at the unrationed upper gate.
3. A revised **credential→rung destination mapping** for d3, declared before the run.

None of these is done here: each would change the experiment after its outcome is known.

## 9. Bottom line for the Council

The EXP-2/A3-D block is implemented, deterministic, guarded and scored. It **does not replace the last
declared taste parameter**. The block is ablation-live (18.41 pp) but the ceiling is **not
demand-robust** (95.05 vs `[73,77]`); d3 fails outright; d1/d2 fail in the ceiling country at the
bound. Per the block's own negative branch: **the ceiling stays a declared taste parameter; the A3
core is PARKED and no layer is added to the ceiling claim.** No re-tuning was performed.
