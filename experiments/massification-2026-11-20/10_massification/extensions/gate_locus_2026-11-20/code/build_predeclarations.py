#!/usr/bin/env python3
"""Build PRE_DECLARATIONS.md for EXP-8 GATE-LOCUS.

The EXP-8 block of Council brief 022 (SYNTHESIS_022.md, section 6) is spliced into
code/predecl_template.md VERBATIM, so that the frozen predeclaration quotes the Council
rather than this Worker's paraphrase of it.

Deterministic: no RNG, no clock. Reads two files, writes one.
"""

import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXP_DIR = HERE.parent
PROGRAMME_ROOT = EXP_DIR.parents[2]  # .../massification-2026-11-20

BRIEF = PROGRAMME_ROOT / "08_council" / "brief_022" / "SYNTHESIS_022.md"
TEMPLATE = HERE / "predecl_template.md"
OUT = EXP_DIR / "PRE_DECLARATIONS.md"

# 1-based inclusive line span of the EXP-8 block in SYNTHESIS_022.md.
FIRST_LINE = 370
LAST_LINE = 393
MARKER = "<<<VERBATIM_EXP8>>>"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    lines = BRIEF.read_text(encoding="utf-8").split("\n")
    block = "\n".join(lines[FIRST_LINE - 1:LAST_LINE]).strip("\n")
    if not block.startswith("### EXP-8"):
        sys.exit("FATAL: line span does not start with the EXP-8 heading")
    if "GATE-LOCUS" not in block:
        sys.exit("FATAL: line span does not contain GATE-LOCUS")

    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count(MARKER) != 1:
        sys.exit("FATAL: template must contain the marker exactly once")
    doc = template.replace(MARKER, block)
    OUT.write_text(doc, encoding="utf-8")

    print(f"wrote      {OUT}")
    print(f"brief      {sha256(BRIEF)}  {BRIEF.name}")
    print(f"lines      {FIRST_LINE}-{LAST_LINE} ({block.count(chr(10)) + 1} lines spliced)")
    print(f"predecl    {sha256(OUT)}  {OUT.name}")


if __name__ == "__main__":
    main()
