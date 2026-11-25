import Atlas.Definitions
import Atlas.Identities
import Atlas.PlackettLuce

/-!
# Claims.lean — the LEMMA LEDGER in Lean

One declaration per claim in `results/audit/paper_claims.csv` for the Lead-scoped starting
rows: **A-34…A-39, B-41…B-44, C-01…C-04, D-01…D-04** (18 claims). All remaining rows of the
baseline (row count read from `results/audit/paper_claims.csv` at ledger-generation time; currently 130) are
recorded as explicit `NOT-YET-LEMMATISED` entries in `docs/audit/LEMMA_LEDGER.md` (they have no
Lean declaration yet, by design — see the ledger's extension plan).

Four statement kinds:
1. `definition` — model objects (see `Atlas/Definitions.lean`; every def states units/domain);
2. `theoremProved` — identities and finite Plackett–Luce math (see `Atlas/Identities.lean`,
   `Atlas/PlackettLuce.lean`);
3. `computational` — exact re-encodings of numeric claims, checked by `decide` in exact
   integer/rational units. These prove **arithmetic consistency**, never the empirical claim;
4. `omission` — independence lemmas: the inventory/classical equation is *definitionally
   invariant* to each of Paper D's five omitted channels.

**Hard rule:** there are **no `sorry`s in this repository's Lean sources**. Claims whose
empirical/float content cannot be a theorem are declared as `EmpiricalClaim`/`SpecClaim`
records with artifact hashes and a status — unproved is not false, and empirical is not a
theorem. `#print axioms` is audited in CI (see `docs/audit/LEMMA_LEDGER.md`).
-/


namespace Atlas.Claims

/-! ## Ledger vocabulary -/

/-- The four statement kinds (plus empirical/spec records for non-theorems). -/
inductive ClaimKind where
  | definition
  | theoremProved
  | computational
  | omission
  | empirical
  | spec
deriving Repr, DecidableEq

/-- Status of a claim entry. `hypothesis` = an empirical/data statement (never a theorem);
`specified` = a mathematical/numeric specification with a differential-test contract;
`notYetLemmatised` = no Lean declaration yet (documented in the markdown ledger). -/
inductive ClaimStatus where
  | defined
  | proved
  | computationallyChecked
  | specified
  | hypothesis
  | notYetLemmatised
deriving Repr, DecidableEq

structure ClaimEntry where
  claimId : String
  paper : String
  kind : ClaimKind
  status : ClaimStatus
  leanDecl : String
  note : String
deriving Repr

/-- An empirical statement about the world. It is **marked as a hypothesis**, carries its
    data provenance (artifact hashes), and is never asserted as a theorem. -/
structure EmpiricalClaim where
  claimId : String
  statement : String
  artifactHashes : List String
  status : ClaimStatus
deriving Repr

/-- A mathematical/numeric specification whose exact re-encoding is stated here but whose
    proof requires data/code outside this prototype. The `differentialContract` names the
    fixture-level test that bridges Lean ↔ Python (see LEAN_VERIFICATION_SCOPE.md §4). -/
structure SpecClaim where
  claimId : String
  exactEncoding : String
  differentialContract : String
  artifactHashes : List String
  status : ClaimStatus
deriving Repr

/-! ## Kind-3 computational lemmas (exact re-encodings; `decide` in exact units) -/

/-- Absolute difference in exact milli-pp units (1 unit = 0.001 pp). -/
def withinPp (reported other tolerance : Int) : Prop := (reported - other).natAbs ≤ tolerance

/-- **A-34 arithmetic check** (not the empirical claim): the fresh-WDI simple-DiD estimate
    `+12.322 pp` and the author baseline `+12.44 pp` are within the claim's stated tolerance
    when re-encoded exactly in milli-pp: `|12322 − 12440| = 118 ≤ 120`. -/
theorem A34_arithmetic : withinPp 12322 12440 120 := by unfold withinPp; decide

/-- **B-41/B-42 Win-Win accounting criterion** in exact milli-units: spend < 80 index points
    and elite Q5 share below the same-jurisdiction baseline. This formalizes the *accounting*
    criterion only — it is not a welfare statement (B-44). -/
def winWinCell (spendMilli eliteMilli baselineMilli : Int) : Prop :=
  spendMilli < 8000 ∧ eliteMilli < baselineMilli

/-- B-41: HK cell meets the pre-stated accounting criterion (70.59 spend / 23.21 elite vs
    24.82 baseline, milli-units). -/
theorem B41_HK_meets_criterion : winWinCell 7059 2321 2482 := by unfold winWinCell; decide

/-- B-41: KR-TRACKED meets the accounting criterion (73.13 / 22.16 vs 23.90). -/
theorem B41_KR_TRACKED_meets_criterion : winWinCell 7313 2216 2390 := by unfold winWinCell; decide

/-- B-41: KR-SINGLE meets the accounting criterion (75.43 / 22.04 vs 24.08). -/
theorem B41_KR_SINGLE_meets_criterion : winWinCell 7543 2204 2408 := by unfold winWinCell; decide

/-- B-42: CF4b fails the spend leg in HK (89.99 ≥ 80), irrespective of its elite share. -/
theorem B42_CF4b_fails_spend_HK : ¬ winWinCell 8999 2343 2482 := by unfold winWinCell; decide

/-- B-42: CF1b fails the spend leg in HK (97.25 ≥ 80). -/
theorem B42_CF1b_fails_spend_HK : ¬ winWinCell 9725 2343 2482 := by unfold winWinCell; decide

/-- B-42: CF3b passes both legs (70.88 / 23.43 vs 24.82 baseline) — the single-lever pass
    that falsifies the paper's "only pairing compression with caps/seats works" reading. -/
theorem B42_CF3b_passes_both : winWinCell 7088 2343 2482 := by unfold winWinCell; decide

/-- **A-38 arithmetic check**: the author's 74.88 % pre-abolition calibration anchor lies above
    the maximum reachable 71.0 % at fee 0, which itself is above the achieved 59.44 % at
    fee 0.15 — in exact hundredths. This is the infeasibility arithmetic, not the empirical
    provenance question. -/
theorem A38_anchor_infeasible : (5944 : Int) ≤ 7100 ∧ (7100 : Int) < 7488 := by decide

/-! ## Kind-4 omission / independence lemmas (proved by definitional invariance) -/

/-- **M1 — school-supplied preparation.** The inventory/classical demand equation, as
    encoded, does not depend on school supply `S`. -/
theorem classical_demand_ignores_school_supply (q : EqState) (s : Int) :
    classicalDemand { q with schoolSupply := s } = classicalDemand q := rfl

/-- **M2 — positional/fixed elite seats.** Invariant to the positional-seat channel. -/
theorem classical_demand_ignores_positional_seats (q : EqState) (s : Int) :
    classicalDemand { q with positionalSeats := s } = classicalDemand q := rfl

/-- **M3 — teacher withholding / rent.** Invariant to the withholding channel. -/
theorem classical_demand_ignores_withholding (q : EqState) (w : Int) :
    classicalDemand { q with withholding := w } = classicalDemand q := rfl

/-- **M4 — student/teacher time budgets.** Invariant to the time-budget channel. -/
theorem classical_demand_ignores_time_budget (q : EqState) (t : Int) :
    classicalDemand { q with timeBudget := t } = classicalDemand q := rfl

/-- **M5 — supply form (private/hybrid/public).** Invariant to the supply-form channel. -/
theorem classical_demand_ignores_supply_form (q : EqState) (f : Int) :
    classicalDemand { q with supplyForm := f } = classicalDemand q := rfl

/-! ## Kind-4 contradiction illustration (D-02) -/

/-- Toy encoding of "raising elite seats raises aggregate spend" in one cell. -/
def paradoxHolds (baseSpend highSpend : Int) : Prop := highSpend > baseSpend

/-- **D-02 counterexample (toy encoding):** the seat-expansion paradox is not a universal
    statement — a concrete cell violates it (`5 > 10` is false). The real model-level
    contradiction is recorded in `SCIENTIFIC_CLAIM_LEDGER.md`; this lemma demonstrates the
    `¬ claim` formalization pattern for recorded contradictions. -/
theorem D02_paradox_not_universal : ¬ (∀ baseSpend highSpend : Int,
    paradoxHolds baseSpend highSpend) := by
  intro hall
  have h : ¬ paradoxHolds 10 5 := by unfold paradoxHolds; decide
  exact absurd (hall 10 5) h

/-! ## Empirical statements — hypotheses with data provenance (never theorems) -/

def A34_empirical : EmpiricalClaim where
  claimId := "A-34"
  statement :=
    "Fresh-WDI simple-DiD abolition impact +12.322 pp vs author +12.44; Fisher p 0.0056 dates / 0.0044 countries"
  artifactHashes :=
    [ "docs/audit/E8_BULGE_NEWGEN.md sha256 97734cdc98b9fdc4221110d61233233cc9b53587f6341ae0de98708aa28b4ca5",
      "results/audit/newgen/e8_bulge_fresh_wdi_2026-11-25.json sha256 5c243943957e5d865fbf1608e9a2e6a8569624ef7d7eb454306471c06ab69ef3",
      "WDI manifest sha256 d7296e1fed3eb6806ba5111de2538e7fcd206323832307a1fabeeaefc6c55ee4" ]
  status := .hypothesis

def A35_empirical : EmpiricalClaim where
  claimId := "A-35"
  statement :=
    "CS-style group-time ATT post mean +25.083 pp vs author +25.26; event path 12.32,23.66,25.79,21.88,24.94,28.45,25.78; pre-trend -3 +0.138"
  artifactHashes :=
    [ "docs/audit/CS_ESTIMATOR_NEWGEN.md sha256 04faf9dc065db6fad113027c1ef7d991dcebcac73657304065580df2aad8b196",
      "results/audit/newgen/cs_estimator_fresh_wdi_2026-11-25.json sha256 4ac9551d0c4b5b2c9180131859a6f4c3876d527ae158f70a7e039fe34c1d1905" ]
  status := .hypothesis

def A36_empirical : EmpiricalClaim where
  claimId := "A-36"
  statement :=
    "Delayed secondary-bulge t* jump: ATT at t* -0.956 pp, post +0.30, Fisher p 0.251/0.384 -> no detectable jump (no-effect evidence)"
  artifactHashes := [ "same newgen artifacts as A-34/A-35 (t* = abolition + SE.PRM.DURS; outcome SE.SEC.ENRR)" ]
  status := .hypothesis

def C01_empirical : EmpiricalClaim where
  claimId := "C-01"
  statement :=
    "Paper C provisional anchor: Paper B canonical spec is a private-market regime - withheld h=0.00000; own-teacher share 2.47% HK / 2.82% KR (own_ban=0.95, mode=positional)"
  artifactHashes :=
    [ "docs/audit/PAPER_C_MODEL_GAP.md sha256 d994df74d10ac2888e2646dad7f59469c8305cd308c644f3660a4b9192643ffc" ]
  status := .hypothesis

def C02_empirical : EmpiricalClaim where
  claimId := "C-02"
  statement :=
    "Paper C provisional anchor: q0 0.8->1.2 lowers K-12 tutoring participation 0.605->0.491 and spend 161.7->135.9"
  artifactHashes := [ "docs/audit/PAPER_C_MODEL_GAP.md sha256 d994df74d10ac2888e2646dad7f59469c8305cd308c644f3660a4b9192643ffc" ]
  status := .hypothesis

def C03_empirical : EmpiricalClaim where
  claimId := "C-03"
  statement :=
    "Paper C provisional anchor: withholding regime (pay_ratio=.55, monitoring=.2, own_ban=0) -> h=0.144, own share 0.528; +firm_ban=.9 -> own share 0.978, spend 118.1, firm price 2.0957"
  artifactHashes := [ "docs/audit/PAPER_C_MODEL_GAP.md sha256 d994df74d10ac2888e2646dad7f59469c8305cd308c644f3660a4b9192643ffc" ]
  status := .hypothesis

/-- D-04 is an attribution-risk/citation statement, not a mathematical proposition. -/
def D04_attribution : EmpiricalClaim where
  claimId := "D-04"
  statement :=
    "Paper D inventory is an AI-generated candidate map with placeholder citations; no equation/citation may be used without primary-source verification"
  artifactHashes :=
    [ "docs/audit/refs/education-equation-inventory-20261124.txt sha256 0fd30f770a75ee55cdf26d3ce332df795f78d29d070bed01af38810bfa4752df" ]
  status := .hypothesis

/-! ## Specifications with differential-test contracts (kind 3, non-theorem) -/

def A37_spec : SpecClaim where
  claimId := "A-37"
  exactEncoding :=
    "Forecast path (pp, hundredths): abolition - persistence = 1719,2097,2337,2503,2614,2618,2535 for e=0..6; full-7 RMSE 2.764/MAE 2.432 vs persistence 23.759/23.260; held-out e=+5,+6 RMSE 1.637/MAE 1.350"
  differentialContract :=
    "Lean defines the scoring function (RMSE/MAE over a finite horizon, exact rational); Python emits its forecast rows as fixtures; the test asserts Lean-evaluated RMSE equals the reported artifact within 1 unit in the last decimal. Float32 engine internals are not formalized."
  artifactHashes :=
    [ "docs/audit/FORECAST_NEWGEN.md sha256 d4c0a239d421ed09d4ff5ee247525aa376385a63f7647256943d707b4382d8f1",
      "results/audit/newgen/forecast_holdout_fixed_846c9e0.json sha256 f0eee995aafb982f316ae7cfd74accc40a6749110dad524b2d2bf4e368184c04" ]
  status := .specified

def A39_spec : SpecClaim where
  claimId := "A-39"
  exactEncoding :=
    "4 theta x 4 moments Jacobian: rank 4/4, null dim 0 at 3/3 starts; SVs (51.030,32.596,1.907,0.341),(46.916,17.058,6.801,0.128),(46.852,23.579,1.993,0.046); s4 drift 0.3409->0.1278->0.0457; stop_gate LOCAL_FULL_RANK_CONDITIONING_UNRESOLVED"
  differentialContract :=
    "Lean can state rank = dim (rows) and nullity = 0 over an exact rational matrix; the proof that a specific finite matrix has rank 4 is a `decide`-style computation on the exact encoding of the Jacobian. The Jacobian itself comes from Python central differences, so the bridge is a fixture: Lean consumes the exact rational matrix, checks rank/nullity/SVs bounds symbolically for the rank part, and the float SV/conditioning numbers remain artifact evidence (not theorem)."
  artifactHashes :=
    [ "docs/audit/G2A_IDENTIFIABILITY_MULTISEED.md sha256 9c40aeedf7cedc815e51a103ea5fd580b71ec791a5d3ae9c009e9ff311053b07",
      "results/audit/newgen/identifiability_multiseed_846c9e0_pin.json sha256 66535941272286c03b549edb20d16e728c9b6afcc9f3a7c214d943aff1c34be3" ]
  status := .specified

def B43_spec : SpecClaim where
  claimId := "B-43"
  exactEncoding :=
    "Provenance correction: early new-gen JSONs (14fc2a31/697e7ca9/cba8ee0f) had empty HK summary due to TRACKED-vs-PRIMARY aggregation lookup; corrected hashes cf801af8/2b69fa08/8f08164d; no simulation rerun; engine label 98baf6b"
  differentialContract :=
    "Not a mathematical proposition: provenance bookkeeping. Lean-side encoding is a ledger record (hash chain); the check is a Python fixture that recomputes the corrected aggregation from intact checkpoints and compares hashes."
  artifactHashes :=
    [ "commit a4b0808", "results/newgen/paperB_new_generation_TRACKED.json sha256 cf801af8e07f9ebf615d075c42ec742f00d5a98a19a0e938005a3632e28836d3",
      "results/newgen/paperB_new_generation_SINGLE_KR.json sha256 2b69fa08ea521c664bda59da4d6fce0d9b48d494d5cee793b69987795bef0330",
      "new_generation_provenance.json sha256 8f08164d08006d5c0225cd2115352270560806fe4055294ff16f453dd62e3301" ]
  status := .specified

def B44_spec : SpecClaim where
  claimId := "B-44"
  exactEncoding :=
    "Under CF4a: K-12 participation -13.33 pp HK / -12.98 pp KR; G12 -10.23 / -5.69; CF3b similar. The criterion's Win-Win is an accounting statement about spend and elite-Q5, NOT a welfare statement; the ~13 pp participation fall is an unmeasured welfare change."
  differentialContract :=
    "Welfare interpretation is not formalizable from the current data (requires learning/access/teacher-workload/student-time data). Lean records only the accounting criterion (winWinCell) and the delta arithmetic (decide over exact pp encodings); the welfare caveat is prose, not a theorem."
  artifactHashes :=
    [ "results/newgen/paperB_new_generation_TRACKED.json sha256 cf801af8e07f9ebf615d075c42ec742f00d5a98a19a0e938005a3632e28836d3",
      "results/newgen/paperB_new_generation_SINGLE_KR.json sha256 2b69fa08ea521c664bda59da4d6fce0d9b48d494d5cee793b69987795bef0330" ]
  status := .specified

def C04_spec : SpecClaim where
  claimId := "C-04"
  exactEncoding :=
    "Paper C confirmatory grid: 3 S x 3 L x 4 supply = 36 cells + 4 regime anchors; N=600/T=46 screening ~320 runs ~2.2 CPU-h; N=1500 confirmatory subset; REQUIRES A PRE-REGISTRATION"
  differentialContract := "No Lean theorem: no run yet (UNRESOLVED). The declaration records the design cells and the prereg requirement only."
  artifactHashes :=
    [ "docs/audit/PAPER_C_MODEL_GAP.md section 4 sha256 d994df74d10ac2888e2646dad7f59469c8305cd308c644f3660a4b9192643ffc",
      "docs/audit/PAPER_D_EQUATION_AUDIT.md section 5 sha256 b6bafd1490b0a98df021f8b6ad1caff52b6ddf1a18b5606d4982ef8e1050a49d" ]
  status := .specified

def D03_spec : SpecClaim where
  claimId := "D-03"
  exactEncoding :=
    "Paper D divergence tests D1-D9: standard-equation prediction X vs mechanism-rich prediction Y; cell/outcome/compute ~300-420 runs at N=600/T=30 (~2-3 CPU-h); D3/D7 need wave-2 extensions"
  differentialContract := "Pre-registerable tests, not results. Lean records the design schema; no theorem until the divergence tests are pre-registered and run."
  artifactHashes := [ "docs/audit/PAPER_D_EQUATION_AUDIT.md section 4 sha256 b6bafd1490b0a98df021f8b6ad1caff52b6ddf1a18b5606d4982ef8e1050a49d" ]
  status := .specified

/-! ## The ledger table (18 Lead-scoped rows) -/

def claimLedger : List ClaimEntry :=
  [ { claimId := "A-34", paper := "A", kind := .computational, status := .computationallyChecked,
      leanDecl := "A34_arithmetic (+ A34_empirical hypothesis)",
      note := "exact milli-pp tolerance check proved; the empirical estimate itself is a data hypothesis (REPRODUCED EMPIRICAL ANALYSIS in paper_claims.csv)" },
    { claimId := "A-35", paper := "A", kind := .empirical, status := .hypothesis, leanDecl := "A35_empirical",
      note := "CS-style ATT numbers are data, not theorem; artifacts hashed" },
    { claimId := "A-36", paper := "A", kind := .empirical, status := .hypothesis, leanDecl := "A36_empirical",
      note := "no-effect evidence (UNRESOLVED); cannot be a theorem" },
    { claimId := "A-37", paper := "A", kind := .spec, status := .specified, leanDecl := "A37_spec",
      note := "simulation forecast: specification + differential-test contract; float32 engine not formalized" },
    { claimId := "A-38", paper := "A", kind := .computational, status := .computationallyChecked,
      leanDecl := "A38_anchor_infeasible",
      note := "infeasibility arithmetic (59.44 <= 71.0 < 74.88) proved in exact units; provenance question is empirical" },
    { claimId := "A-39", paper := "A", kind := .spec, status := .specified, leanDecl := "A39_spec",
      note := "rank/nullity is exact-matrix computable; SV/conditioning floats are artifact evidence; stop gate recorded" },
    { claimId := "B-41", paper := "B", kind := .computational, status := .computationallyChecked,
      leanDecl := "B41_HK_meets_criterion, B41_KR_TRACKED_meets_criterion, B41_KR_SINGLE_meets_criterion",
      note := "Win-Win *accounting* criterion proved for the three cited cells; welfare interpretation is NOT proved (B-44)" },
    { claimId := "B-42", paper := "B", kind := .computational, status := .computationallyChecked,
      leanDecl := "B42_CF4b_fails_spend_HK, B42_CF1b_fails_spend_HK, B42_CF3b_passes_both",
      note := "the 'only pairing works' reading is falsified by the exact accounting values" },
    { claimId := "B-43", paper := "B", kind := .spec, status := .specified, leanDecl := "B43_spec",
      note := "provenance/hash-chain correction; not a mathematical proposition" },
    { claimId := "B-44", paper := "B", kind := .spec, status := .specified, leanDecl := "B44_spec",
      note := "participation deltas are accounting facts; the welfare caveat is not formalizable from current data" },
    { claimId := "C-01", paper := "C", kind := .empirical, status := .hypothesis, leanDecl := "C01_empirical",
      note := "provisional anchor, design-only; not a Paper C result" },
    { claimId := "C-02", paper := "C", kind := .empirical, status := .hypothesis, leanDecl := "C02_empirical",
      note := "provisional anchor, design-only" },
    { claimId := "C-03", paper := "C", kind := .empirical, status := .hypothesis, leanDecl := "C03_empirical",
      note := "provisional anchor, design-only" },
    { claimId := "C-04", paper := "C", kind := .spec, status := .specified, leanDecl := "C04_spec",
      note := "design cells + prereg requirement; no run yet" },
    { claimId := "D-01", paper := "D", kind := .omission, status := .proved,
      leanDecl := "classical_demand_ignores_school_supply, ..._positional_seats, ..._withholding, ..._time_budget, ..._supply_form",
      note := "five omission/independence lemmas proved by definitional invariance in the exact encoding; candidates, not errors (no real-world claim)" },
    { claimId := "D-02", paper := "D", kind := .theoremProved, status := .proved, leanDecl := "D02_paradox_not_universal",
      note := "contradiction-pattern illustration in a toy encoding; the recorded model-level contradictions are empirical/artifact evidence" },
    { claimId := "D-03", paper := "D", kind := .spec, status := .specified, leanDecl := "D03_spec",
      note := "pre-registerable divergence tests, not results" },
    { claimId := "D-04", paper := "D", kind := .empirical, status := .hypothesis, leanDecl := "D04_attribution",
      note := "citation/attribution risk is not a mathematical proposition; recorded as an explicit non-theorem" } ]

end Atlas.Claims
