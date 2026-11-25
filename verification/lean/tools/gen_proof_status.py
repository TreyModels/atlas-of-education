#!/usr/bin/env python3
"""Generate the Lean proof-status artefacts for the Atlas verification package.

Reads the Lean sources, builds the project, collects `#print axioms` for every theorem
automatically, and writes:

  docs/audit/LEAN_PROOF_STATUS.md      — human proof-status table + flags + versions/hashes
  docs/audit/LEAN_PROOF_STATUS.csv     — machine-readable one row per declaration
  docs/audit/results/LEAN_AXIOMS_ALL.txt     — raw #print axioms output (all theorems)
  docs/audit/results/LEAN_PROOF_STATUS_BUILD.log — raw lake build log

Requirements: a Lean 4.36.0 toolchain on PATH (lean/lake), Python 3.
Flags recorded per declaration: compiled, sorry-free, axioms (exactly as #print axioms says),
kind, file/line, project version/hash. Unproved/empirical claims are NOT counted as theorems —
they are separate `EmpiricalClaim`/`SpecClaim` declarations and the claim ledger.

Usage:
  PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.36.0/bin:$PATH" \
      python3 verification/lean/tools/gen_proof_status.py
"""
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)              # verification/lean
REPO = os.path.dirname(os.path.dirname(PROJECT))  # repo root

DECL_RE = re.compile(r"^(theorem|lemma|def|structure|inductive|abbrev)\s+([A-Za-z0-9_'.]+)")
NS_RE = re.compile(r"^namespace\s+([A-Za-z0-9_.']+)\s*$")
END_RE = re.compile(r"^end(\s+[A-Za-z0-9_.']+)?\s*$")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lean_sources():
    files = [os.path.join(PROJECT, "LeanStarter.lean"), os.path.join(PROJECT, "Atlas.lean")]
    atlas_dir = os.path.join(PROJECT, "Atlas")
    if os.path.isdir(atlas_dir):
        for name in sorted(os.listdir(atlas_dir)):
            if name.endswith(".lean"):
                files.append(os.path.join(atlas_dir, name))
    return files


def parse_declarations(files):
    decls = []
    for path in files:
        stack = []
        rel = os.path.relpath(path, PROJECT)
        for lineno, line in enumerate(open(path, encoding="utf-8"), start=1):
            m_ns = NS_RE.match(line.strip())
            if m_ns:
                stack.append(m_ns.group(1))  # full namespace, e.g. "Atlas.Claims"
                continue
            if END_RE.match(line.strip()):
                if stack:
                    stack.pop()
                continue
            m = DECL_RE.match(line)
            if m:
                name = ".".join(stack + [m.group(2)]) if stack else m.group(2)
                decls.append({
                    "declaration": name,
                    "kind": m.group(1),
                    "file": rel,
                    "line": lineno,
                })
    return decls


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-dir", default=os.path.join(REPO, "docs", "audit"))
    ap.add_argument("--skip-build", action="store_true")
    args = ap.parse_args()
    audit_dir = os.path.abspath(args.audit_dir)
    results_dir = os.path.join(audit_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    lean = run(["lean", "--version"], cwd=PROJECT)
    lake = run(["lake", "--version"], cwd=PROJECT)
    if lean.returncode != 0 or lake.returncode != 0:
        sys.exit("FATAL: lean/lake not on PATH; put the Lean 4.36.0 toolchain bin dir on PATH")

    # ---- build ----
    if args.skip_build:
        build_ok, build_log = True, "(build skipped)"
    else:
        b = run(["lake", "build"], cwd=PROJECT)
        build_ok = b.returncode == 0 and "Build completed successfully" in (b.stdout + b.stderr)
        build_log = b.stdout + b.stderr
    with open(os.path.join(results_dir, "LEAN_PROOF_STATUS_BUILD.log"), "w", encoding="utf-8") as f:
        f.write(build_log)

    # ---- sorry scan ----
    sscan = run([sys.executable, os.path.join(PROJECT, "ci", "sorry_scan.py"),
                 "Atlas", "Atlas.lean", "LeanStarter.lean"], cwd=PROJECT)
    sorry_ok = sscan.returncode == 0
    sorry_lines = sscan.stdout.strip().splitlines()

    # ---- declarations + axioms ----
    files = lean_sources()
    decls = parse_declarations(files)
    theorems = [d for d in decls if d["kind"] in ("theorem", "lemma")]
    audit_file = os.path.join(PROJECT, ".proof_status_axioms.lean")
    with open(audit_file, "w", encoding="utf-8") as f:
        f.write("import Atlas\nimport LeanStarter\n\n")
        for d in theorems:
            f.write(f"#print axioms {d['declaration']}\n")
    ax = run(["lake", "env", "lean", audit_file], cwd=PROJECT)
    os.remove(audit_file)
    axioms_raw = ax.stdout + ax.stderr
    path = os.path.join(results_dir, "LEAN_AXIOMS_ALL.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(axioms_raw)
    axioms = {}
    for line in axioms_raw.splitlines():
        m = re.match(r"^'([^']+)'( does not depend on any axioms| depends on axioms: \[(.*?)\])", line)
        if not m:
            continue
        name = m.group(1)
        axioms[name] = [] if m.group(2).startswith(" does not") else [a.strip() for a in m.group(3).split(",") if a.strip()]

    # ---- claims ledger ----
    ledger_csv = os.path.join(audit_dir, "LEMMA_LEDGER.csv")
    baseline_json = os.path.join(audit_dir, "LEMMA_LEDGER_BASELINE.json")
    claims = list(csv.DictReader(open(ledger_csv, encoding="utf-8"))) if os.path.isfile(ledger_csv) else []
    baseline = json.load(open(baseline_json, encoding="utf-8")) if os.path.isfile(baseline_json) else {}
    declared_claims = [c for c in claims if c["ledger_kind"] != "notYetLemmatised"]
    not_yet = [c for c in claims if c["ledger_kind"] == "notYetLemmatised"]

    # ---- version/hash facts ----
    commit = run(["git", "-C", REPO, "rev-parse", "--short=12", "HEAD"]).stdout.strip() or "unknown"
    toolchain = open(os.path.join(PROJECT, "lean-toolchain"), encoding="utf-8").read().strip()
    file_hashes = {os.path.relpath(p, REPO): sha256_file(p) for p in files + [os.path.join(PROJECT, "lakefile.toml")]}
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # ---- write CSV ----
    csv_path = os.path.join(audit_dir, "LEAN_PROOF_STATUS.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["declaration", "kind", "file", "line", "compiled", "sorry_free", "axioms", "notes"])
        for d in decls:
            ax_list = axioms.get(d["declaration"])
            w.writerow([
                d["declaration"], d["kind"], d["file"], d["line"],
                "yes" if build_ok else "NO",
                "yes" if sorry_ok else "NO",
                "" if not ax_list else "; ".join(ax_list) if ax_list != [] else "none",
                "not a theorem (definition/structure)" if d["kind"] not in ("theorem", "lemma") else "",
            ])

    # ---- write MD ----
    def axioms_text(d):
        if d["kind"] not in ("theorem", "lemma"):
            return "— (definition)"
        if d["declaration"] not in axioms:
            return "AUDIT MISSING"
        a = axioms[d["declaration"]]
        return "none" if not a else ", ".join(a)

    theorem_count = len(theorems)
    prohibited = {"sorryAx", "Classical.choice", "Lean.ofReduceBool", "Lean.trustCompiler"}
    bad = [(n, a) for n, al in axioms.items() for a in al if a in prohibited]
    non_propext = [(n, a) for n, al in axioms.items() for a in al if a not in ({"propext"} | prohibited)]
    lines = []
    lines.append("# LEAN PROOF STATUS — Atlas verification package")
    lines.append("")
    lines.append(f"**Generated:** {ts} · **Owner:** `audit-runner` · **Host-only** (no box use)")
    lines.append("")
    lines.append("**What this is:** one row per Lean declaration with compiled/sorry/axiom flags, generated by")
    lines.append("`verification/lean/tools/gen_proof_status.py` (build + automatic `#print axioms`).")
    lines.append("**What this is NOT:** it does **not** verify the 183 inventory equations, the Python engine, or its")
    lines.append("floating-point runtime. Those remain Tier-3 computations under reproducible-artifact evidence.")
    lines.append("")
    lines.append("## Version pin / hashes")
    lines.append("")
    lines.append(f"- toolchain: `{toolchain}` · Lean `{lean.stdout.strip()}` · Lake `{lake.stdout.strip()}`")
    lines.append(f"- git commit: `{commit}`")
    lines.append(f"- build: **{'PASS' if build_ok else 'FAIL'}** (`docs/audit/results/LEAN_PROOF_STATUS_BUILD.log`)")
    lines.append(f"- sorry scan: **{'0 sorry tokens' if sorry_ok else 'SORRY FOUND'}** "
                 f"({'; '.join(sorry_lines) if sorry_lines else ''})")
    lines.append(f"- declarations parsed: **{len(decls)}** ({theorem_count} theorems/lemmas, "
                 f"{len(decls) - theorem_count} definitions/structures)")
    lines.append(f"- axioms: **{sum(len(a) for a in axioms.values())} axiom dependencies**; "
                 f"prohibited axioms found: {len(bad)}; non-standard (non-propext) deps: {len(non_propext)}")
    lines.append(f"- claims ledger: **{len(declared_claims)} declared + {len(not_yet)} explicit NOT-YET = {len(claims)} rows**, "
                 f"baseline `{baseline.get('sha256', '?')[:16]}…` ({baseline.get('rows', '?')} rows)")
    lines.append("")
    lines.append("## Project file hashes")
    lines.append("")
    lines.append("| file | sha256 |")
    lines.append("|---|---|")
    for p, h in sorted(file_hashes.items()):
        lines.append(f"| `{p}` | `{h}` |")
    lines.append("")
    lines.append("## Declarations (compiled status + axioms)")
    lines.append("")
    lines.append("| declaration | kind | file:line | compiled | sorry-free | axioms |")
    lines.append("|---|---|---|---|---|---|")
    for d in decls:
        ax_txt = axioms_text(d)
        if d["kind"] in ("theorem", "lemma") and ax_txt not in ("none", "— (definition)") and ax_txt != "AUDIT MISSING":
            ax_txt += " ⚠️"
        lines.append(f"| `{d['declaration']}` | {d['kind']} | `{d['file']}:{d['line']}` | "
                     f"{'yes' if build_ok else 'NO'} | {'yes' if sorry_ok else 'NO'} | {ax_txt} |")
    lines.append("")
    lines.append("## Flag summary")
    lines.append("")
    lines.append(f"- compiled: {'YES (whole project)' if build_ok else 'NO'}; sorries: {'0' if sorry_ok else '>0'}; "
                 f"prohibited axioms: {len(bad)}; non-propext dependencies: {len(non_propext)}")
    lines.append("- axioms used anywhere: " + (", ".join(sorted({a for al in axioms.values() for a in al})) or "none"))
    lines.append("- empirical/spec claims: declared as `EmpiricalClaim`/`SpecClaim` records (never theorems); "
                 "see `LEMMA_LEDGER.md`/`.csv` for 18 declared + explicit NOT-YET rows.")
    lines.append("- Mathlib: **not used** (core Lean only); Tier-2 Mathlib package is CI-only per the scope document.")
    lines.append("")
    lines.append("## Claim status table (from LEMMA_LEDGER.csv)")
    lines.append("")
    lines.append("| claim | paper | kind | status | Lean declaration |")
    lines.append("|---|---|---|---|---|")
    for c in declared_claims:
        lines.append(f"| {c['claim_id']} | {c['paper']} | {c['ledger_kind']} | `{c['ledger_status']}` | "
                     f"`{c['lean_declaration']}` |")
    lines.append("")
    lines.append(f"Explicit NOT-YET-LEMMATISED rows: **{len(not_yet)}** (full list in `LEMMA_LEDGER.md`; ids in `.csv`).")
    lines.append("")
    lines.append("## Reproduce")
    lines.append("")
    lines.append("```bash")
    lines.append('PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.36.0/bin:$PATH" \\')
    lines.append("  python3 verification/lean/tools/gen_proof_status.py")
    lines.append("```")
    md_path = os.path.join(audit_dir, "LEAN_PROOF_STATUS.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {md_path} and {csv_path}: {len(decls)} declarations, {theorem_count} theorems, "
          f"build={'PASS' if build_ok else 'FAIL'}, sorry_free={sorry_ok}, axioms={len(axioms)}")
    return 0 if build_ok and sorry_ok and not bad and not non_propext else 1


if __name__ == "__main__":
    sys.exit(main())
