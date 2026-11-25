#!/usr/bin/env python3
"""Fail unless the `#print axioms` output only uses the allowed axioms.

Allowed: (none) and `propext` (the standard Lean kernel axiom used by definitional
extensionality in a few core lemmas). Anything else — `sorryAx`, `Classical.choice`,
`Lean.ofReduceBool`, `Lean.trustCompiler` — fails the audit.
Usage: axiom_audit.py AXIOUT_FILE
"""
import re
import sys

ALLOWED = {"propext"}


def main(path):
    bad = []
    lines = 0
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("'"):
            continue
        lines += 1
        m = re.search(r"depends on axioms: \[(.*?)\]", line)
        if not m:
            continue  # "does not depend on any axioms"
        axioms = [a.strip() for a in m.group(1).split(",") if a.strip()]
        bad.extend((line, a) for a in axioms if a not in ALLOWED)
    print(f"axiom audit: {lines} theorem lines parsed; allowed={sorted(ALLOWED)}")
    if bad:
        for line, a in bad:
            print(f"DISALLOWED AXIOM {a!r} in: {line}")
        return 4
    print("axiom audit OK (only allowed axioms: none/propext)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
