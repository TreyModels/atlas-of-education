# LEAN VERIFICATION SCOPE — "can we run everything against Lean?"

**Question (operator):** can we machine-check the mathematics and claims of the Atlas programme in the Lean 4
theorem prover?
**Answer:** **No, not "everything" — and claiming so would be false.** A useful, honest architecture is:
**Lean proves the reference mathematics and the accounting/inventory identities; the Python engine is
differential-tested against Lean-computed witnesses on fixtures; numerical results stay reproducible-artifact
evidence under hashes and tests. That is not "the engine is verified".**

**Owner:** `audit-runner` (formal QA + harness lane) · **Date:** 2026-11-25 · **Host-only** (no box use; Paper A/B
own the box) · **Status:** prototype built and compiled; tier table below.

---

## 1. Host/toolchain record (measured on this Mac)

| item | value |
|---|---|
| host | `MacBookAir10,1`, macOS 26.6.2, Apple M1, **8 GiB RAM**, `/System/Volumes/Data` **≈11 GiB free** (228 GiB volume, 95 % full) |
| toolchain manager | `elan 4.4.0` installed at `/Users/treymenefee/.elan/bin` |
| Lean | **`leanprover/lean4:v4.36.0`** (pinned in `verification/lean/lean-toolchain`), installed from distribution `lean-4.36.0-darwin_aarch64.tar.zst` = **637,952,376 B (608.4 MiB)**; `lean --version` = 4.36.0 (commit `611c117b…`), `lake` 5.0.0-src |
| download | default CDN `releases.lean-lang.org` measured **70 B/s** (unusable); GitHub release mirror used instead: resumable 80-piece parallel `curl -r` download, measured **0.5–2.9 MB/s** aggregate, total install window **20:48 → 21:11 CST (~23 min)** incl. extraction; the integrity check is exact file size 637,952,376 B |
| unpacked footprint | **3.0 GiB** measured (`du -sh ~/.elan/toolchains/leanprover--lean4---v4.36.0`); free disk fell **12 GiB → 8.9 GiB**; `verification/lean` build artifacts are MB-scale (no Mathlib dependency) |
| build time | **`lake build`: 16 jobs, ~2 s cold, <1 s warm** (measured; log `docs/audit/results/LEAN_BUILD_COLD.log`, refreshed `LEAN_PROOF_STATUS_BUILD.log`) |
| Mathlib | **not installed on this host.** Full Mathlib is **not viable here**: cache/oleans are multi-GB (≥2–4 GB compressed, ~6–8 GiB unpacked) against **11 GiB free** on an 8 GiB-RAM Mac, and the measured link would take **1–2 h** to pull the cache. Mathlib-dependent Tier-2 proofs therefore belong in **CI with a cached Mathlib**, not on this laptop. |

Everything in `verification/lean/` **compiles with Lean core only** — no Mathlib, no `sorry`.

---

## 2. Tier table (honest feasibility)

| tier | content | Lean feasibility | effort | RAM/disk | decision |
|---|---|---|---|---|---|
| **1 — weeks→days** | accounting identities: budget/teacher-salary ledger, seat-share denominators, prep-stock recursion `prep_t = (1−ρ)prep_{t−1}+e_t`, tax/resource ledger, gate accounting ranks, definitional lemmas over `Nat`/`Rat`/`Fin n` | **high** — core Lean suffices; exact integer/rational encodings; `decide`/induction proofs are short | **prototype done in ~1 day**; full Tier-1 (all identities + `Rat`/`ℝ` versions + fixtures) **≈1–2 weeks** of focused work | <0.1 GiB build; seconds–minutes to compile | **recommended: build Tier 1 fully** (see §6) |
| **1b — days** | inventory/omission lemmas: each Paper D omitted channel (M1–M5) as a **definitional invariance** theorem of the classical equation; recorded contradictions as `¬ claim` counterexamples | **high** — `rfl`-level proofs; the formal content is the *encoding* choice (what the equation depends on) | days; done in prototype for M1–M5 | negligible | **recommended: include in Tier 1** |
| **2 — weeks** | finite Plackett–Luce top-K: `Σ_seats P_i = min(seats, |candidates|)`, monotonicity/symmetry, exact subset-DP ↔ closed form (small n computational), prefix-suffix cumsum construction | **medium** — needs `Finset`/combinatorics; Mathlib makes it tractable (finite, combinatorial). Core-only proofs for general n would be long; small-n computational proofs are easy | **weeks (≈2–4)** for the general-n PL package incl. Mathlib setup + CI cache; prototype has n=2 symbolic + `decide` checks | Mathlib cache/build: multi-GB, needs ≥8–12 GiB RAM realistically; CI runner recommended | **conditional**: start only with a CI Mathlib cache; n=2/n=3 core proof is a cheap seed (done) |
| **3 — not Lean-provable as theorems** | numpy float32 numerics (`max|ΔP|`, RMSE), DID/bootstrap *inference*, the 5,632-run outputs, empirical claims about the world | **infeasible / category error** — these are computations/data claims, not theorems; float32 internals are implementation artifacts | — | — | **keep as reproducible-artifact evidence**: hashed outputs + tests; only exact re-encodings (e.g. tolerance arithmetic) and verified interval arithmetic belong in Lean |

**Rule of thumb:** if the statement is "for all x, the equation/identity holds", Lean is the right tool. If it is
"this program run on this data produced this number", Lean can only formalize the *specification* and a
*differential-test contract* — the number itself stays artifact evidence.

---

## 2b. Codex staged plan (recorded) + Luna starter integration

**Pinned model definitions and domains** (all in `verification/lean/Atlas/Model.lean`, exact integer encoding):
`Learning {achieved, required}`, `Requirement = fixed cutoff | rank seats`, `gap achieved required = required − achieved`
(= `max(0, R−A)` on `Nat`, units: score points), `accepted applicants capacity = min applicants capacity` (pupils),
`Sources {school, privateTutoring, home}` with `totalInput = school+private+home` (input units), `timeUsed = prep+work+review`
(time units), and a deterministic rank with an **explicit tie rule** (`outranks = higher score ∨ (equal score ∧ stable tie-break)`).
Time ordering is the list order of the prep-stock recursion; all domains are `Nat` unless stated, with explicit
hypotheses where a bound is required.

**Conditional invariants proved** (each is conditional on the stated assumptions, not unconditional):

| invariant | Lean theorem | status |
|---|---|---|
| `gap ≥ 0`; gap = 0 iff met; gap > 0 iff shortfall | `gap_nonneg`, `gap_eq_zero_iff_met`, `gap_pos_iff_shortfall` | proved (propext only) |
| accounting balances: accepted ≤ valid seat capacity | `accepted_le_capacity` | proved |
| zero additional input ⇒ unchanged learning increment | `zero_extra_input_no_increment` | proved (no axioms) |
| source accounting identity; **distinct source terms sum only under additivity** | `total_input_eq_sum`, `additive_combine_eq_sum`, `max_not_additive` (counterexample) | proved |
| time budget respected if enforced (and no double-booking identity) | `budget_implies_component`, `time_accounting_identity` | proved |
| **rank invariance to common score shifts** for deterministic rank + explicit tie rule | `rank_invariant_under_common_shift` (+ `outranksBool_eq_true_iff`) | proved |
| monotonicity of acceptance **under fixed capacity** | `accepted_monotone_fixed_capacity` | proved (assumption-restricted) |
| fixed-seat relative-rank, complementarity, feedback-capacity **counterexamples** (monotonicity is *not* implied in general) | `fixed_seat_relative_rank_counterexample`, `complementarity_counterexample`, `feedback_capacity_counterexample` | proved counterexamples |

**Restricted ranges / ties / stochastic-numerical semantics (recorded):** score domain is `Nat` (negative common
shifts are outside the pinned domain); ties are resolved explicitly by a stable id, never silently; stochastic
draws and floating-point semantics are **out of Lean** (Tier 3) — the rank theorem is deterministic-only.

**Luna starter integration** (`verification/lean/LeanStarter.lean`; source sha256
`a7145fdc43f01a02ae3f2a80562b623b0a6755e6749dec2d5142d94f0d4932f7`): compiled into the Lake package as an
additional lib root (`roots = ["Atlas", "LeanStarter"]`). Exact fixes needed:
1. the leading `/-- … -/` doc comment cannot attach to a `namespace` declaration → converted to a `/-! … -/` module doc;
2. the block-comment prose must not contain `/-`-opening sequences (`/--`, `/-!`) — Lean block comments nest, so the
   original wording produced an "unterminated comment" error; reworded without comment delimiters;
3. `work_within_elapsed`/`review_within_elapsed` had **unsolved `simp` goals** (`work ≤ preparation + (work + review)`),
   and `preparation_within_elapsed` carried an unused-simp-arg warning; all three were proved via explicit
   `Nat.le_add_left/right` transitivity (not `omega`, to keep the axiom audit to `propext` only);
4. `gap_eq_zero_of_met`'s `simp` proof introduced `Quot.sound`; replaced with `Nat.sub_eq_zero_of_le` so the theorem
   depends on `propext` only. Statements/definitions of the starter are unchanged.

**Explicit warning (Codex):** these are selected, exact-encoded mechanisms. They do **not** verify the 183 inventory
equations, the Python engine, or its floating-point runtime, and toy lemmas must not be cited as such.

## 3. What the prototype actually contains (`verification/lean/`)

| file | contents | status |
|---|---|---|
| `lean-toolchain`, `lakefile.toml` | pinned Lean 4.36.0, Lake package `atlasVerification`, library `Atlas` | compiles |
| `Atlas/Definitions.lean` | model objects with units/domains: `Cohort`, `Gate`/`GateKind`, `seatCount` (`max 1 (round share·N)`), `Budget`, `TaxLedger`, `PrepStock`, `PLWeights`, `EqState` (Paper D M1–M5 channels), `classicalDemand` | compiles |
| `Atlas/Identities.lean` | **proved**: `budget_ledger_identity`, `tax_revenue_le_base`, **`prep_recursion_closed_form`** | compiles |
| `Atlas/PlackettLuce.lean` | **proved**: `pl_top1_sum_eq_denom` (`ΣP = min 1 2`), `pl_top1_sum_eq_min`, `pl_topK_selected_sum` (`K ≥ 2 → ΣP = min K 2`), plus concrete `decide` checks | compiles |
| `Atlas/Claims.lean` | `ClaimKind`/`ClaimStatus`/`ClaimEntry`; `claimLedger` (18 Lead-scoped claims, one declaration each); empirical `EmpiricalClaim`s with artifact hashes; `SpecClaim`s with differential-test contracts; **kind-3 `decide` lemmas** (A-34 tolerance, A-38 infeasibility, B-41/B-42 Win-Win accounting); **kind-4 omission lemmas** M1–M5; D-02 `¬` counterexample | compiles (0 `sorry`) |
| `LeanStarter.lean` | Luna starter (Nat gap/capacity/time lemmas), compiled into the package with 4 fixes (§2b) | compiles; 13 lemmas |
| `Atlas/Model.lean` | Codex staged-plan model: A/R, fixed vs rank, gap, capacity, sources/time accounting, explicit tie-rule rank, conditional invariants + counterexamples (§2b) | compiles; 25 declarations |
| `ci/lean_verify.sh` + `ci/sorry_scan.py` + `ci/axiom_audit.py` | CI hook: `lake build`, **comment-aware** `sorry` scan, `#print axioms` allow-list audit (only `propext`/none), 18/18 claim-id check | **PASS** — `LEAN VERIFY: PASS`, 16 jobs, 7 files, 0 sorry, 33 axiom lines audited, log `docs/audit/results/LEAN_VERIFY_host.log` |
| `bridge/lean_witness.lean` + `bridge/fixtures.json` + `bridge/differential_test.py` | executable Lean witness → exact fixture comparison | **PASS 22/22 exact fixtures** (`docs/audit/results/LEAN_DIFFERENTIAL_BRIDGE.json`) |

**Theorems are about the model objects, not about the world.** Empirical claims (A-34/A-35/A-36, C-01…C-03, D-04)
are `EmpiricalClaim` records marked `hypothesis`/`notYetLemmatised` with artifact hashes — they are never asserted
as theorems. Unproved ≠ false; empirical ≠ theorem.

---

## 4. Differential-test bridge design (Lean reference ↔ Python engine)

The bridge is the only honest way to connect "proved identity" to "engine computes that identity":

```
Lean reference                             Python engine
─────────────────                          ─────────────
Definitions.lean / Identities.lean   ──►   fixture generator emits EXACT inputs (integers / rationals as
(exact encodings)                           numerator-denominator pairs), never reinterpreted floats
Lean evaluates witness (`lake exe` /        Python runs the engine/aggregation function on those fixtures
`lake env lean bridge/lean_witness.lean`)   and emits its outputs
        │                                          │
        └──────────► bridge/differential_test.py ◄┘
                     asserts equality within a declared tolerance (0 for exact integer
                     identities; exact rational equality for Rat encodings; explicit
                     ulp/tolerance for float32 legs), and writes a signed result JSON
                     with: fixture hash, Lean build hash, witness hash, Python command,
                     output hash, pass/fail per fixture.
```

Contracts (binding):
1. **Exact legs** (ledger identities, seat rounding, prep recursion, PL selection counts): equality must be
   **exact** on the exact encoding; no tolerances.
2. **Float legs** (engine float32/float64 numerics): Lean specifies the recurrence/aggregation in exact arithmetic
   and the fixture test compares with a declared tolerance; the tolerance itself is part of the claim ledger.
3. **No silent re-encoding:** each fixture carries the Python source hash and the Lean witness hash; changing
   either invalidates the fixture hash.
4. The bridge tests **specific fixtures**, so passing it never upgrades the engine to "verified"; it upgrades a
   set of named differential contracts.

Initial fixture set (prototype plan): budget/ledger accounting on 3 fixture worlds; seat-count rounding
(`max 1 (round share·N)`) on the audit's seat-share cases; prep-stock recursion over 5 periods vs engine stock
series; PL top-K admission counts for n=2/3 candidates at 4 seat shares; the two-candidate probability sums.
The `verification/lean/bridge/` directory is implemented and **passing**: the Lean witness emits exact integer
values (budget ledger, prep-stock recursion vs closed form, seat rounding, PL numerator sums) and the Python test
compares them to `bridge/fixtures.json` — 22/22 exact matches, `passed: true`
(`docs/audit/results/LEAN_DIFFERENTIAL_BRIDGE.json`).

---

## 5. CI hook plan

- **Local / pre-commit** (`verification/lean/ci/lean_verify.sh`, no network):
  `lake build` → fail on `sorry` (grep) → `#print axioms` for every proved theorem (allowed axiom set: none; any
  `sorryAx`/`Classical.choice`/`Lean.ofReduceBool` shows up in the log and fails) → dump theorem list + hashes.
- **GitHub Actions** (`.github/workflows/lean.yml` proposal): `leanprover/lean-action` with toolchain from
  `lean-toolchain`, `lake build`, `lake exe cache get` **only for the Tier-2 Mathlib job**; artifact: build log +
  `#print axioms` output + axiom/sorry report. Pin the Mathlib commit/toolchain pair in `lake-manifest.json`.
- **Repo gate:** the audit branch's `verification/lean` build + `docs/audit/LEMMA_LEDGER.md` status consistency is
  part of the release checklist; a claim row without a declaration *or* an explicit `notYetLemmatised` entry fails.

---

## 6. Recommendation

1. **Build Tier 1 fully — yes.** It is cheap (core Lean, seconds to compile, no Mathlib, <1 day prototype already
   compiling), it covers the identities the Python engine's correctness actually rests on, and it yields the
   **omission lemmas** that formalize Paper D's M1–M5 without overclaiming.
2. **Tier 2 — conditionally.** Start the general-n Plackett–Luce package **only in CI with a Mathlib cache**
   (weeks of work; not on this 8 GiB/11 GiB-free laptop). The n=2 core seed is already in the repo.
3. **Tier 3 — do not attempt as theorems.** Keep numerical/DID/bootstrap results as hashed reproducible artifacts;
   formalize only exact re-encodings and tolerances where they are genuinely arithmetic.
4. **Never say "the engine is verified".** The correct sentence: *Lean proves the reference mathematics and the
   accounting/inventory identities; named differential contracts bind the engine to those Lean statements on
   fixtures; numerical outputs remain reproducible-artifact evidence.*
