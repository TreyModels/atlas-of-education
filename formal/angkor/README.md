# Angkor models in Lean 4

Lean 4.36.0, core only (no Mathlib). Exact rational arithmetic stands in for floating point; random draws, logs, exponentials, sines and square roots are inputs. Each file names its JavaScript source and the line ranges it mirrors.

Build: `lake build` (all eight modules build together, exit 0).

| Module | Source | Theorems |
|---|---|---|
| Angkor/Maintenance.lean | experiments/angkor-review/model/accounted_v2.py | 57 |
| Angkor/Obligations.lean | public/engines/obligations.js | 46 |
| Angkor/Mandala.lean | src/models/angkor-model.js | 44 |
| Angkor/Monsoon.lean | public/engines/monsoon.js | 43 |
| Angkor/Relocation.lean | src/models/relocation.js | 43 |
| Angkor/Signalling.lean | src/models/signalling.js | 36 |
| Angkor/Petri.lean | public/engines/petri.js | 31 |
| Angkor/Provisioning.lean | public/engines/provisioning.js | 27 |

327 theorems. Audit (2026-11-26): no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe` or `implemented_by`; `#print axioms` on every theorem shows only `propext`, `Classical.choice`, `Quot.sound` (some use fewer). Definitions were compared with the JavaScript by hand.

Limits: these are exact-arithmetic properties of the code's formulas (ledgers, bounds, conservation, counters, monotonicity, counterexamples), not floating-point behaviour, calibration or historical validity. Run summaries and scoring are mostly not formalized. Each module's header lists what is left out, and witnesses state whether they are reachable from the engine's initial state. See CONVENTIONS.md for the rules the formalizations follow.
