#!/usr/bin/env python3
"""
EXP-22 PART-MARGIN-DESC -- standalone verbatim check.

Asserts that every passage quoted in PRE_DECLARATIONS.md (the frozen block §6.2, the D156 EXP-22
clause, D153(xii), D158's seven rules, brief §8's banned-sentences bullet and the V35a-V35c rows)
occurs verbatim in its source file. The runner performs the same check as step 3; this script
exists so the claim can be re-verified without running the cell.

Exit 0 = PASS, 2 = FAIL. No clock, no writes.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run_part_margin_desc as R  # noqa: E402


def main():
    with open(R.PREDECL, encoding="utf-8") as fh:
        text = fh.read()
    checks = R.verbatim_checks(text)
    print(json.dumps(checks, indent=2, sort_keys=True))
    ok = checks.get("all_verbatim") is True
    print("VERBATIM:", "PASS" if ok else "FAIL")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
