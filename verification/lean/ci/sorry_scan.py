#!/usr/bin/env python3
"""Comment- and string-aware scan for the `sorry` token in Lean sources.

The Lean sources deliberately contain the *word* 'sorry' in prose (documenting the
no-sorry policy), so a naive grep is wrong. This scanner strips nested block comments
`/- ... -/`, line comments `-- ...` and string literals (preserving newlines so reported
line numbers stay correct), then searches for the identifier token `sorry`.

Exit 0 = no sorry token; exit 1 = sorry found (printed as file:line:col).
Usage: sorry_scan.py PATH [PATH ...]   (files or directories, *.lean)
"""
import os
import re
import sys


def strip_comments_and_strings(src: str) -> str:
    out = []
    i, n = 0, len(src)
    while i < n:
        if src.startswith("/-", i):
            depth = 1
            i += 2
            while i < n and depth > 0:
                if src.startswith("/-", i):
                    depth += 1
                    i += 2
                elif src.startswith("-/", i):
                    depth -= 1
                    i += 2
                else:
                    if src[i] == "\n":
                        out.append("\n")
                    i += 1
            continue
        if src.startswith("--", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if src[i] == '"':
            i += 1
            while i < n:
                if src[i] == "\\":
                    i += 2
                elif src[i] == '"':
                    i += 1
                    break
                else:
                    if src[i] == "\n":
                        out.append("\n")
                    i += 1
            continue
        out.append(src[i])
        i += 1
    return "".join(out)


TOKEN = re.compile(r"(?<![A-Za-z0-9_])sorry(?![A-Za-z0-9_])")


def lean_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for dirpath, _dirnames, filenames in os.walk(p):
                for name in sorted(filenames):
                    if name.endswith(".lean"):
                        yield os.path.join(dirpath, name)
        elif p.endswith(".lean") and os.path.isfile(p):
            yield p


def main(argv):
    paths = argv[1:] or ["Atlas", "Atlas.lean"]
    hits = 0
    scanned = 0
    for path in lean_files(paths):
        scanned += 1
        stripped = strip_comments_and_strings(open(path, encoding="utf-8").read())
        for lineno, line in enumerate(stripped.splitlines(), start=1):
            for m in TOKEN.finditer(line):
                hits += 1
                print(f"{path}:{lineno}:{m.start() + 1}: sorry token")
    print(f"sorry scan: {scanned} Lean files scanned, {hits} sorry token(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
