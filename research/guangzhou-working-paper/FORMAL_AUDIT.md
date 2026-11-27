# Formal audit: `Admission.lean`

## Verification

Ran `lean Admission.lean` from this directory with the pinned Lean 4.36.0 toolchain; it succeeds. The output matches `proof-check.txt`. The two finite witnesses (`strict_displacement_witness`, `cutoff_tie`) report no additional axioms. `displacement`, `rival_bonus`, and `band_size` report `propext` and `Quot.sound`; `conditioning_witness` additionally reports `Classical.choice`.

## Exact proof scope

- `seat_balance` proves a counting identity for a finite list of Boolean before/after pairs. `displacement` derives equal numbers of admissions gained and lost if the two Boolean admission totals are equal. It does not establish how the Python route-selection algorithm chooses entrants or verify that algorithm.
- `rival_bonus` proves, for integer scores and a nonnegative bonus, that raising one listed rival's score cannot increase the count of rivals strictly above the focal score. Its qualification criterion is “fewer than `k` strictly above,” which is tie-inclusive. `strict_displacement_witness` is only the concrete one-seat example `(8, 7)` with a bonus of 2.
- `band_size` proves the length and no-duplicate property of a `take k` prefix of a permutation of a distinct-ID roster: its length is `min k roster.length`. It does not prove Python's `band_and_class` behavior, its rounding/minimum-one rule, or the simulation's tie ordering.
- `cutoff_tie` is a concrete inclusive-cutoff counterexample: at cutoff 8, both scores in `[8,8]` qualify despite `k = 1`. It is not a general theorem about the model's complete admission process.
- `conditioning_witness` uses exact rational arithmetic on two stipulated Boolean lists. It shows standardized rates have ratio 1 while overall win rates have ratio 3 for that constructed example; it does not derive the lists from the simulation or establish a general conditioning result.

## Alignment and corrections

The formal-check descriptions in `manuscript.md` (formal-check bullets and replication summary) are appropriately qualified as generic lemmas and witnesses, and explicitly say the Python model is not verified. They accurately distinguish the inclusive-cutoff tie counterexample from the fixed-prefix rule, and state that proof does not validate NumPy tie behavior. `illustrate.py`'s prose likewise describes the abstractions and includes a scope limitation. No Lean correction is indicated.

One phrase in `illustrate.py` could be made more exact: “For any finite before-and-after roster ... whenever the total admitted stays fixed” is supported only when each list row is represented as a pair of Boolean admission indicators and the two totals are equal. Consider “For any finite list of before/after Boolean admission indicators, gains equal losses when the two admission totals are equal.” The existing manuscript wording is already precise enough.
