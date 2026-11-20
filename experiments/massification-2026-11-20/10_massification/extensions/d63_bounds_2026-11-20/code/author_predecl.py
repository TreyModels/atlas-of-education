#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-23 D63-BOUNDS -- authoring helper (NOT part of the experiment run).

Assembles PRE_DECLARATIONS.md. Its only job is to splice the Council's own text into the
predeclaration MECHANICALLY, so that the "verbatim" claim is a machine guarantee rather than a
transcription promise:

  * the SYNTHESIS_025.md section 6.3 EXP-23 block (heading + items 1-7) is extracted by line range
    and block-quoted between HTML markers;
  * the D153(xiii), D156 (EXP-23) and D158 (seven rules) clauses are extracted by character range
    from 08_council/DECISIONS.md and block-quoted the same way;
  * the banned-sentence list is extracted from SYNTHESIS_025.md section 8.

code/run_d63_bounds.py re-extracts all five from the frozen sources and refuses to run if they do
not match the on-disk predeclaration. Deterministic; no RNG; writes one file (PRE_DECLARATIONS.md)
inside this experiment directory.
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SYN = "08_council/brief_025/SYNTHESIS_025.md"
DEC = "08_council/DECISIONS.md"


def rd(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def block(lines):
    """Block-quote lines; blank lines become a bare '>'."""
    out = []
    for ln in lines:
        out.append(">" if ln == "" else "> " + ln)
    return "\n".join(out)


def slice_between(text, start, end, occurrence=0):
    i = -1
    for _ in range(occurrence + 1):
        i = text.find(start, i + 1)
        if i < 0:
            raise SystemExit(f"[FATAL] start anchor not found: {start!r}")
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f"[FATAL] end anchor not found: {end!r}")
    return text[i:j + len(end)]


def main():
    syn = rd(SYN).split("\n")
    s = next(i for i, l in enumerate(syn) if l.startswith("### 6.3 EXP-23"))
    e = next(i for i, l in enumerate(syn) if l.startswith("### 6.4"))
    while syn[e - 1].strip() == "":
        e -= 1
    v63 = block(syn[s:e])

    dec = rd(DEC)
    d153 = slice_between(dec, "(xiii) **D63's residual is split", "**barred**;")
    d156 = slice_between(dec, "**EXP-23 D63-BOUNDS** — the D63 residual split",
                         "D63 stays UNABLE) **#3**")
    d158 = slice_between(dec, "(1) **Hash enforcement at verdict time**",
                         "in the same sentence as the number.")

    syn_text = "\n".join(syn)
    banned = slice_between(syn_text, "- **Banned sentences (the list #5 carries into the write-up).**",
                           'without** the per-level split; "the repair made the model worse"; '
                           '"the upper-secondary ceiling is structural"; "the\n  proxy is consistent with the required coverage"; '
                           '"κ ≈ 0.95 is forward-usable"; "the representation capability holds at\n  both levels"; '
                           '"the model is behaviourally 13–17 pp wrong"; "demand falsified"; "v1.2 passes".')

    template = open(os.path.join(HERE, "code", "predecl_template.md"), encoding="utf-8").read()
    out = (template
           .replace("{{V63}}", v63)
           .replace("{{A153}}", block(d153.split("\n")))
           .replace("{{A156}}", block(d156.split("\n")))
           .replace("{{A158}}", block(d158.split("\n")))
           .replace("{{BANNED}}", block(banned.split("\n"))))

    dst = os.path.join(HERE, "PRE_DECLARATIONS.md")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"wrote {dst}  ({len(out)} chars, {out.count(chr(10)) + 1} lines)")
    print(f"  verbatim 6.3 : {len(syn[s:e])} source lines")
    print(f"  anchor D153  : {len(d153)} chars")
    print(f"  anchor D156  : {len(d156)} chars")
    print(f"  anchor D158  : {len(d158)} chars")
    print(f"  banned list  : {len(banned)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
