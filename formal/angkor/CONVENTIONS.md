# Conventions for the Angkor formalizations

Project: `formal/angkor`, Lean 4.36.0, core only. No Mathlib and no network or package installs (disk is nearly full).

## Fidelity
- Formalize the code as written, not a nicer model. Same constants (exact: `.035` is `35/1000`), same order of updates, same branches. Where the source reassigns a variable, use successive `let`s or intermediate definitions.
- Read the whole source first. Each definition gets a doc comment with the source file and line range.
- State is a structure over `Rat`; parameters are a structure over `Rat`; enum options are inductive types.
- Randomness is an input. Draws and other nonrational values (`log`, `exp`, `sin`, `sqrt`, powers) enter as explicit arguments or function parameters with hypotheses; say so in the module doc. Never replace them silently.
- Rationals stand in for floating point: theorems are about the ideal arithmetic, not IEEE rounding. State this in the module doc.
- Division by zero: Lean gives 0, JavaScript gives NaN or Infinity, Python raises. Flag each division and prove the denominator nonzero or carry that as a hypothesis.

## Proofs
- Forbidden: `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `implemented_by`, `set_option warn.sorry false`, and weakening a definition to make a theorem pass.
- Theorems must not be vacuous: no hypothesis that contradicts another, and no hypothesis that assumes the conclusion. Prove hypotheses satisfiable with a concrete example where they are not obvious.
- Prove, for whatever applies: each claimed ledger is exactly balanced; mass conservation; bounds and nonnegativity of state preserved by a step; then the same for any number of steps by induction; knockouts and monotonicity.
- If a property the model claims is false, prove the counterexample (`theorem foo_false : ∃ ..., ¬ ...`). That is a valuable result, not a failure.
- If you cannot prove something, leave it out of the Lean file and report it. Do not weaken it quietly.
- Useful tools: `grind` (linear and ring reasoning over Rat), `omega` (integers), `simp only`, `unfold`, `split`, `Rat.mul_nonneg`, `decide`, induction. Multiplication of two unknowns is nonlinear: first prove the product facts with `Rat.mul_nonneg` and pass them to `grind`. Split large steps into small definitions with one lemma each.

## Checking
Build only your own file, from `formal/angkor`:

    export PATH=/private/tmp/claude-501/lean436/bin:$PATH; lake build Angkor.<Name>

Finish with `#print axioms` on each main theorem (in a scratch file outside the project): only `propext`, `Classical.choice`, `Quot.sound` are allowed.
