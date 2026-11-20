#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MAKE_SUMS -- regenerate SHA256SUMS.txt over the delivered files (documentation step).

The scored run writes SHA256SUMS.txt before FINDINGS.md and TUNE_LOG.md exist; this script
re-derives the same sorted list plus those two documents. It touches no result file and no
frozen input: it only writes SHA256SUMS.txt.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

CELL = Path(__file__).resolve().parent.parent
RESULTS = CELL / "results"
EXTRAS = ("PRE_DECLARATIONS.md", "PARAMS.md", "FINDINGS.md", "TUNE_LOG.md",
          "FREEZE_RECORD.json")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    files = []
    for root, _dirs, names in os.walk(RESULTS):
        for n in sorted(names):
            p = Path(root) / n
            rel = os.path.relpath(p, CELL)
            if rel in ("RUN_MANIFEST.json", "SHA256SUMS.txt"):
                continue
            files.append(rel)
    files.sort()
    lines = ["%s  %s" % (sha(CELL / rel), rel) for rel in files + ["RUN_MANIFEST.json"]
             if (CELL / rel).exists()]
    lines += ["%s  %s" % (sha(CELL / e), e) for e in EXTRAS if (CELL / e).exists()]
    (CELL / "SHA256SUMS.txt").write_text("\n".join(sorted(lines)) + "\n")
    print("SHA256SUMS.txt: %d lines" % len(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
