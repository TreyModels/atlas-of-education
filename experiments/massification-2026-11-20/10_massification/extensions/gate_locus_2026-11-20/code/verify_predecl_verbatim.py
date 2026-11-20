#!/usr/bin/env python3
"""Verify that the frozen PRE_DECLARATIONS.md quotes the Council brief byte for byte.

Checks, in order:
  1. the quoted markdown fence in PRE_DECLARATIONS.md equals SYNTHESIS_022.md lines 370-393;
  2. PRE_DECLARATIONS.md still hashes to the value recorded in PRE_DECLARATIONS.sha256.

Deterministic, read-only. Exits non-zero on any failure.
"""

import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXP_DIR = HERE.parent
PROGRAMME_ROOT = EXP_DIR.parents[2]

BRIEF = PROGRAMME_ROOT / "08_council" / "brief_022" / "SYNTHESIS_022.md"
PREDECL = EXP_DIR / "PRE_DECLARATIONS.md"
SIDECAR = EXP_DIR / "PRE_DECLARATIONS.sha256"
FIRST_LINE, LAST_LINE = 370, 393
OPEN_FENCE = "```markdown"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    src = BRIEF.read_text(encoding="utf-8").split("\n")
    expected = "\n".join(src[FIRST_LINE - 1:LAST_LINE]).strip("\n")

    doc = PREDECL.read_text(encoding="utf-8")
    parts = doc.split(OPEN_FENCE)
    if len(parts) != 2:
        sys.exit(f"FATAL: expected exactly one {OPEN_FENCE} fence, found {len(parts) - 1}")
    rest = parts[1]
    if rest.count("```") != 1:
        sys.exit("FATAL: the quoted fence is not closed exactly once")
    quoted = rest.split("```")[0].strip("\n")

    if quoted != expected:
        for i, (a, b) in enumerate(zip(quoted.split("\n"), expected.split("\n")), 1):
            if a != b:
                sys.exit(f"FATAL: verbatim quote diverges at quoted line {i}\n  quote: {a!r}\n  brief: {b!r}")
        sys.exit("FATAL: quote differs in line count from the brief's span")

    recorded = SIDECAR.read_text(encoding="utf-8").split()[0]
    actual = sha256(PREDECL)
    if recorded != actual:
        sys.exit(f"FATAL: predeclaration changed after freeze\n  recorded: {recorded}\n  actual:   {actual}")

    print("VERBATIM-QUOTE-OK  lines %d-%d, %d lines, sha256 %s" % (
        FIRST_LINE, LAST_LINE, expected.count("\n") + 1,
        hashlib.sha256(expected.encode("utf-8")).hexdigest()))
    print(f"PREDECL-FROZEN-OK   sha256 {actual}")


if __name__ == "__main__":
    main()
