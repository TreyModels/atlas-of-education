#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build PRE_DECLARATIONS.md = a thin header + the TWO frozen files verbatim.

The frozen sources are never edited; this copy exists so the module carries its own spec.
sim_v1_3.py verifies (a) the frozen files hash to their recorded values and (b) this copy
contains both of them byte-for-byte.
"""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT13 = HERE.parent
SYNTH = ROOT13.parent
SHADOW = SYNTH / "shadow_module"
PREDECL = SHADOW / "PRE_DECLARATIONS.md"
S1 = SHADOW / "PRE_DECLARATIONS_S1_NOTE.md"
OUT = ROOT13 / "PRE_DECLARATIONS.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


pre = PREDECL.read_text()
s1 = S1.read_text()

head = f"""# PRE-DECLARATIONS — v1.3 shadow-education-at-the-gates module (VERBATIM COPY)

**LABEL: SYNTHETIC.** This file is a copy. It is not a new pre-declaration and it changes
nothing. The binding documents are the two frozen files in `shadow_module/`, reproduced below
byte-for-byte:

| frozen source | sha256 |
|---|---|
| `shadow_module/PRE_DECLARATIONS.md` | `{sha(PREDECL)}` |
| `shadow_module/PRE_DECLARATIONS_S1_NOTE.md` | `{sha(S1)}` |

`code/sim_v1_3.py` re-hashes both frozen files at start-up and refuses to run on mismatch, and
it also checks that this copy contains both of them verbatim (so the copy cannot drift).

Implementation gap resolutions (which v1.2 country carries which declared country type, the
gate-state contract, the feedback hook) are **not** here: they are declared separately in
`IMPLEMENTATION_NOTE.md` and `IMPLEMENTATION_NOTE_N1.md`, both written and hashed before the
first v1.3 run. Nothing in those notes changes a parameter or a threshold.

---

# PART 1 — `shadow_module/PRE_DECLARATIONS.md` (verbatim)

"""
mid = "\n\n---\n\n# PART 2 — `shadow_module/PRE_DECLARATIONS_S1_NOTE.md` (verbatim)\n\n"
OUT.write_text(head + pre + mid + s1)
print("wrote PRE_DECLARATIONS.md sha256 = %s" % sha(OUT))
print("contains frozen predecl verbatim: %s" % (pre in OUT.read_text()))
print("contains S1 note verbatim: %s" % (s1 in OUT.read_text()))
