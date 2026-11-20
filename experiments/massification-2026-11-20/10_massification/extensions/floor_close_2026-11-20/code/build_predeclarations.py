#!/usr/bin/env python3
"""Build PRE_DECLARATIONS.md for EXP-12 FLOOR-CLOSE.

The EXP-12 block is spliced *verbatim* from the Council brief (lines 436-472 of
SYNTHESIS_023.md) and the D133 scope sentence is spliced verbatim from DECISIONS.md,
so no definition can drift through transcription.  The build asserts byte identity
against the source files and refuses to write if either source hash moved.

Run once, before code/run_floor_close.py is first executed.  The resulting file is
hashed to PRE_DECLARATIONS.sha256 and that hash is pinned in run_floor_close.py.
"""

import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXP_DIR = HERE.parent
PROGRAMME_ROOT = EXP_DIR.parents[2]

SYNTHESIS = PROGRAMME_ROOT / "08_council" / "brief_023" / "SYNTHESIS_023.md"
DECISIONS = PROGRAMME_ROOT / "08_council" / "DECISIONS.md"
OUT = EXP_DIR / "PRE_DECLARATIONS.md"

SYNTHESIS_SHA256 = "39e666cffbe3950d43460ba177a36501d53fd0ec8083cd5c9abcbd1c7aeed44c"
DECISIONS_SHA256 = "15c564cffb1d9994386873b7daf9793407745da5477d437ef3adcb9efba8771c"

BLOCK_FIRST = 436          # 1-based, "### 6.2 EXP-12 ..."
BLOCK_LAST = 472           # 1-based, "7. **Cost / rank.** ..."


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if sha256(SYNTHESIS) != SYNTHESIS_SHA256:
        sys.exit("FATAL: SYNTHESIS_023.md hash moved; refusing to splice a different block")
    if sha256(DECISIONS) != DECISIONS_SHA256:
        sys.exit("FATAL: DECISIONS.md hash moved; refusing to splice a different D133")

    lines = SYNTHESIS.read_text(encoding="utf-8").splitlines()
    block = "\n".join(lines[BLOCK_FIRST - 1:BLOCK_LAST])
    if not block.startswith("### 6.2 EXP-12"):
        sys.exit("FATAL: block does not start at the EXP-12 heading")
    if not block.rstrip().endswith("on disk right now."):
        sys.exit("FATAL: block does not end at the EXP-12 cost/rank line")
    if "FLOOR-CLOSE" not in block or "phys_cap" not in block:
        sys.exit("FATAL: spliced block is not the EXP-12 block")

    dec = DECISIONS.read_text(encoding="utf-8")
    m = re.search(
        r'(A10/D62 "capacity buys the floor" scoped:.*?until FLOOR-CLOSE returns\.)',
        dec, re.DOTALL)
    if not m:
        sys.exit("FATAL: D133 A10/D62 scope sentence not found verbatim")
    d133 = m.group(1)
    # The regex may cross a table row boundary if the sentence moved; guard it.
    if "|" in d133 or len(d133) > 800:
        sys.exit("FATAL: D133 scope splice is not a single clean sentence")

    template = (EXP_DIR / "code" / "predecl_template.md").read_text(encoding="utf-8")
    template = template.replace("<<<VERBATIM_EXP12_BLOCK>>>", block)
    template = template.replace("<<<VERBATIM_D133_SCOPE>>>", d133)

    OUT.write_text(template, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(PROGRAMME_ROOT)}")
    print(f"sha256 {sha256(OUT)}")
    print(f"block lines {BLOCK_FIRST}-{BLOCK_LAST} ({len(block.splitlines())} lines) spliced verbatim")


if __name__ == "__main__":
    main()
