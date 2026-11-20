# TUNE_LOG — v1.4 demand-signal core (EXP-2 / A3-D)

**LABEL: SYNTHETIC.** This is a design-phase history, not a result. It records what was seen, what
was changed, and where the freeze point is, including the changes that make the module look worse.
All numbers below are design-preview numbers from the synthetic generator; none is evidence.

## 0. What the base v1.3 already is

`generator_v1_3/code/sim_v1_3.py` (sha256 `70ae8f0e…`) already carries the shadow-education block and
its own frozen c1–c6. Its baseline upper-secondary UIS completion in 2024 is **76.6391**, inside the
declared `[73,77]` band, and its own PARAMS/FINDINGS attribute the ceiling to the four-state
household block's work incentive at ages 15–17 (`v0, decay, w_child, compat, cost, neither`),
"upper demand ≈ 0.80". v1.4 adds one block and does not touch any of that arithmetic when the block
is off.

## 1. Design order (what was seen first)

1. **Read first, no numbers.** Read the EXP-2 block (SYNTHESIS_021 §4 lines 316–341) and Amendment
   A3's Layer-2c specification. Copied `sim_v1_3.py` to `code/base_v1_3_sim.py` byte-for-byte
   (sha256 equality checked) and started `code/sim_v1_4_demand.py` from that same text.
2. **State magnitudes for unit checking (no demand output seen yet).** Pulled `w_for`, `w_inf`, `J`
   and gate states for `SYN00_PHL_LIKE` and the two twins at 1970 and 2024 from the frozen v1.3 panel
   and gate CSV. Findings that shaped the design:
   - `w_for(2)/w_inf ≈ 3.8`; the destination-composition-weighted formal wage is several times the
     informal wage. The generator's wage ladder is steep.
   - `pi0` at the upper gate is **0.999** in the v1.3 gate state (advances/candidates, where advances
     include over-age admissions, so the ratio can exceed 1 and is clipped). The upper gate is, in
     this generator, **not rationed** — the ceiling is demand-side, not supply-side. This is a
     limitation of using the model's own `pi0` as `P(advance)`; it is reported in `FINDINGS.md` and
     was **not** "fixed" by substituting a different admission object after seeing outcomes.
3. **Units correction before any run.** The first draft of `ER_hh` used the *capitalised* return
   (× `H`), which made the demand value two orders of magnitude larger than `v_2 = v0·decay² ≈ 0.786`.
   Hand-checking showed this was a horizon mismatch: the four-state block is a one-year decision, so
   the capitalised return must be converted to its annual equivalent by dividing by `H`. Corrected to
   `ER_ann = ER/H` **before** any simulation was run. No declared value was involved.
4. **Smoke preview #1** (before the d1 perturbation fix; the numbers are recorded here verbatim —
   the `_scratch/preview` directory now holds the later smoke):
   - upper UIS 2024 with the replacement: **95.0455** (baseline 76.6391; move +18.4 pp);
   - d1 sign cells contained negative deltas for `SYN_KHM_LIKE` at 1972/1974/… (−2.27, −1.86, … pp);
   - d1/d2 failed at `SYN_PHL_LIKE` (+0.15 pp / +0.23 pp) because its upper demand share was already
     at the bound (~0.99);
   - d3 failed: flow-matched office − mfg = −0.58 pp.
   The d1 negative deltas were traced to a **definition flaw**, not a model result: the perturbation
   multiplied `ER_net` by 1.10, which *worsens* a negative net return. That is not what "+10% E[R]"
   means. Fix (pre-freeze, `PRE_DECLARATIONS.md` Revision 1): perturb the **gross** return by +10%,
   holding cost, foregone and migration fixed. This changes only how d1 is *tested*; the scored
   replacement arm is untouched.
5. **Smoke preview #2** (after Revision 1, same declared values):
   - upper UIS 2024: still **95.0455** (unchanged — the perturbation is a check, not the scored arm);
   - d1: HKG +1.52 pp (pass), PHL +0.15 pp (fail), KHM +4.77 pp (pass); sign is non-negative in every
     scored cell (min +0 pp);
   - d2: HKG +2.47, PHL +0.23 (fail), KHM +10.33; shadow offsets +31.1 to +32.6 pp;
   - d3: −0.584 pp (fail); access-only variant −0.551 pp;
   - d6: 0 violations.
6. **Dry scored run** (23:24, into `results/`), then inspected. Two issues, both outside the scored
   arm:
   - `REPLACEMENT_TEST.csv`'s `distance_from_band_pp` carried a **negative** sign for an above-band
     value (−18.05); fixed to a positive distance plus a `direction` column.
   - The sensitivity "placebo" cell left the declared **remittance liquidity lift ON**, so it could
     not be a clean code-integrity check: it returned 76.9249 (panel sha `af8a08…`), not the v1.3
     panel. Root cause was the placebo's definition, not a leak: the liquidity lift is part of the
     demand block. Fixed by turning the substitution **and** the lift off for the integrity placebo
     (which then returns 76.6391 and the exact v1.3 panel sha `47d4b082…`), and adding a separate
     `liquidity only` row to report the lift's own effect (+0.286 pp).
   No declared value, threshold, band, ablation bar or scored-arm definition changed; the dry and
   final runs gave identical scored numbers (95.04548615 / 76.63908112 / +18.40640503 pp).
7. **Freeze.** `PRE_DECLARATIONS.md` sha256 `9ed0cae3…` (Revision 2), `PARAMS.md` sha256 `c22edec7…`.
   Every D01–D08 value, every threshold, the `[73,77]` band, the 3.0 pp ablation bar and the
   replacement object were frozen here. The final scored run is the run after this point; its code
   sha256 is `6e4a6761…`.

## 2. What was NOT changed after the previews

Explicitly, because it would be re-tuning:

- **D01–D08 were not moved.** `mig`, `dest_mult`, `export`, `remit_prop`, `B_Z_D`, `ER_floor`, the lag
  and the destination rung sets are exactly the values written before the first preview.
- **The `[73,77]` band and the 3.0 pp bar were not moved**, and no "outside by >2.0 pp" tolerance was
  invented to accommodate 95.05.
- **The saturation rule was not used to rescue d1/d2.** `SYN_PHL_LIKE`'s 2020 demand share is at the
  bound, so its +0.15 / +0.23 pp responses are mechanically small; excluding those cells would make a
  saturating replacement pass. `PRE_DECLARATIONS.md` §5 d1 states that the 2020 magnitude bar is
  scored on the raw Δ and the saturation is reported beside the verdict. The cells are **not**
  excluded.
- **`P(advance)` was not redefined** to a rationing ratio after seeing that `pi0 ≈ 0.999`, even though
  a smaller `P(advance)` would lower `E[R]`. That would be a post-hoc structural change aimed at the
  band. The limitation is reported instead.
- **The conversion `y_med / w_inf` was not rescaled**, nor was a free scale factor added to map
  `E[R]` into the `v_2` range. A scale factor would be exactly the fitted "demand parameter" that
  R4/R27 forbids.
- **The destination rung sets were not reordered** to make the office twin win d3.

## 3. Interpretation of the preview (recorded here, before the scored run)

The replacement arm drives upper-secondary demand to the bound and upper UIS 2024 to ~95. The cause
is visible in `DETAIL.csv`-class magnitudes: the generator's own formal/informal wage gap and
destination composition imply an annual net return several times household income, so the
demand-derived value `v_D ≈ 1.9` is roughly 2.5× the declared taste `v_2 = 0.786`. The ceiling in
v1.2/v1.3 is therefore a **declared-taste** phenomenon, not a demand phenomenon, under this
parameter-free conversion. The experiment is expected to return `NOT DEMAND-ROBUST` / `FALSIFIED`;
it is reported as such, and no layer is wired into the ceiling claim.

## 4. Freeze point

- Predeclaration frozen at `9ed0cae353c9a3dfba00582ff47d19ca8b761d8dd7b7ce5f9a8a8e4c5c5f49b3`
  (Revision 1 and Revision 2 recorded in its §14).
- `PARAMS.md` frozen at `c22edec770aff3f09a7b8157928f73d4e8385bbf5a40aeac23570157b14e4bad`.
- `code/sim_v1_4_demand.py` frozen at `6e4a6761fa32325c61f138037a1e5c8d5e578e19f8a2ee2519e73e8f2332b2d1`.
- Post-freeze change (documented): `write_checks_v14` was rewritten so `DEMAND_CHECKS.csv` carries each
  component with its own threshold and component verdict (the deliverable asked for
  components/thresholds/verdicts). This is **output formatting only** — no scored value, declared
  value or verdict changed; both scored runs before and after the change produced identical
  numbers (95.04548615 / 76.63908112 / +18.40640503 pp).
- `code/sim_v1_4_demand.py` is frozen at the scored run; its sha256 is in `RUN_MANIFEST.json` and
  `SHA256SUMS.txt`. Any later change voids the run and must be recorded here with before/after hashes.
- Two clean runs into separate output directories must be byte-identical; the OFF panel must equal the
  v1.3 panel byte-for-byte. Both checks are in `results/determinism_note.md`.
