#!/usr/bin/env python3
"""Mechanical consistency audit of the Lean claim ledger (host-only).

Baseline: results/audit/paper_claims.csv (re-hashed at every run; never trust a stale row count).
Authoritative ledger: docs/audit/LEMMA_LEDGER.csv (machine-readable, one row per claim).
Lean sources: verification/lean/**/*.lean.

Usage:
  python3 docs/audit/lemma_audit.py --claims results/audit/paper_claims.csv \
      --ledger docs/audit/LEMMA_LEDGER.csv --lean-dir verification/lean \
      --json-out docs/audit/results/lemma_audit.json

Rules:
 R1 claims inventory unique/non-empty (duplicates reported)
 R2 every claim id has exactly one ledger row and either >=1 existing Lean declaration
    (a declaration group) or an explicit not-yet-lemmatised entry (status/kind/note)
 R3 no silent `sorry`: code (not comments/docstrings) sorrys must be in the ledger with a reason
 R4 claim-id match: ledger ids == claims ids (orphans/missing listed); ids not silently dropped
 R5 no duplicate ledger rows and no duplicate Lean declaration names
 R6 in-Lean claimLedger (Claims.lean) agrees with LEMMA_LEDGER.csv on claim id -> lean declaration/status
"""
import argparse, csv, hashlib, json, os, re, sys

DECL_RE = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)*(theorem|lemma|def|abbrev|structure|instance)\s+([A-Za-z0-9_\.\']+)')
CLAIM_ID_RE = re.compile(r'^[A-Z]{1,3}-\d{1,3}$')
SORRY_RE = re.compile(r'\bsorry\b')
LEAN_BLOCK_SPLIT = re.compile(r'\{\s*claimId\s*:=')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def strip_comments(text):
    """Blank out Lean comments/docstrings while keeping line numbers."""
    out, i, n = [], 0, len(text)
    depth = 0
    while i < n:
        if text.startswith('/-', i):
            depth += 1; out.append('  '); i += 2; continue
        if depth and text.startswith('-/', i):
            depth -= 1; out.append('  '); i += 2; continue
        ch = text[i]
        if depth:
            out.append('\n' if ch == '\n' else ' '); i += 1; continue
        if text.startswith('--', i):
            while i < n and text[i] != '\n': out.append(' '); i += 1
            continue
        out.append(ch); i += 1
    return ''.join(out)

def lean_files(lean_dir):
    fs = []
    for root, _, files in os.walk(lean_dir):
        for f in files:
            if f.endswith('.lean'): fs.append(os.path.join(root, f))
    return sorted(fs)

def parse_lean(lean_dir):
    decls, sorries, texts = {}, [], {}
    for f in lean_files(lean_dir):
        raw = open(f, encoding='utf-8', errors='replace').read(); texts[f] = raw
        code = strip_comments(raw)
        cur = None
        for ln, line in enumerate(code.splitlines(), 1):
            m = DECL_RE.match(line)
            if m: cur = m.group(2); decls.setdefault(cur, []).append(dict(file=f, line=ln, kind=m.group(1)))
            if SORRY_RE.search(line): sorries.append(dict(file=f, line=ln, decl=cur, code=line.strip()))
    return decls, sorries, texts

def parse_ledger_csv(path):
    rows = list(csv.DictReader(open(path, encoding='utf-8')))
    ids = [r['claim_id'] for r in rows]
    return rows, ids

def is_notyet(row):
    blob = ' '.join(str(row.get(k, '')) for k in ('ledger_kind', 'ledger_status', 'note')).lower()
    return ('notyet' in blob.replace(' ', '')) or ('not-yet' in blob) or ('not yet' in blob)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--claims', required=True); ap.add_argument('--ledger', required=True)
    ap.add_argument('--lean-dir', default='verification/lean'); ap.add_argument('--json-out', default=None)
    a = ap.parse_args()
    out = dict(baseline=dict(path=a.claims, sha256=sha256(a.claims)), ledger=dict(path=a.ledger, sha256=sha256(a.ledger)),
               lean_dir=a.lean_dir, checks=[], missing=[], orphans=[], duplicates=[], silent_sorry=[], ledger_mismatch=[])
    def chk(rid, ok, detail): out['checks'].append(dict(id=rid, status='PASS' if ok else 'FAIL', detail=detail))
    claims = list(csv.DictReader(open(a.claims)))
    cids = [r['claim_id'].strip() for r in claims]
    out['baseline'].update(rows=len(cids), unique=len(set(cids)))
    dup_ids = sorted({i for i in cids if cids.count(i) > 1})
    chk('R1', bool(cids) and not dup_ids and all(cids), f'{len(cids)} claims, {len(set(cids))} unique; duplicate ids={dup_ids}')
    if not os.path.exists(a.ledger) or not os.path.exists(a.lean_dir):
        out['checks'].append(dict(id='R2', status='BLOCKED', detail=f'missing ledger or lean dir: {a.ledger} / {a.lean_dir}'))
        for r in ('R3', 'R4', 'R5', 'R6'): out['checks'].append(dict(id=r, status='BLOCKED', detail='missing ledger/Lean dir'))
        print(json.dumps(out, indent=1)); return 2
    lrows, lids = parse_ledger_csv(a.ledger); out['ledger'].update(rows=len(lrows), unique=len(set(lids)))
    dup_led = sorted({i for i in lids if lids.count(i) > 1})
    decls, sorries, texts = parse_lean(a.lean_dir)
    all_decl_names = set(decls)
    # R5 duplicates
    dup_decl = sorted({k for k, v in decls.items() if len(v) > 1})
    chk('R5', not dup_led and not dup_decl, f'ledger rows={len(lrows)} duplicate ledger ids={dup_led}; Lean declaration names={len(decls)} duplicated={dup_decl}')
    # R4 id match
    missing_led = [i for i in cids if i not in set(lids)]
    orphans = sorted(set(lids) - set(cids))
    chk('R4', not missing_led and not orphans, f'claims missing from ledger={missing_led[:10]}; ledger ids not in claims={orphans[:10]}')
    # R2 exactly one ledger row per claim + declaration group exists OR explicit not-yet
    missing_decl, multi_row = [], []
    for cid in cids:
        rows = [r for r in lrows if r['claim_id'] == cid]
        if len(rows) != 1: multi_row.append((cid, len(rows))); continue
        r = rows[0]; names = re.findall(r'[A-Za-z0-9_\.\']+', r.get('lean_declaration', ''))
        resolved = [n for n in names if n in all_decl_names]
        if resolved: continue           # declaration group exists (>=1 declaration)
        if is_notyet(r): continue       # explicit not-yet entry with status/kind/note
        missing_decl.append(cid)
    out['missing'] = missing_decl
    chk('R2', not missing_decl and not multi_row,
        f'declared={sum(1 for r in lrows if r.get("lean_declaration","").strip())} explicit-not-yet={sum(1 for r in lrows if is_notyet(r))} '
        f'missing declaration/not-yet={missing_decl[:15]} rows not exactly one={multi_row[:5]}')
    # R3 no silent sorry (code only)
    silent = []
    for s in sorries:
        key = f"{os.path.basename(s['file'])}:{s['line']}"
        if not s['decl']: silent.append(dict(sorry=key, reason='sorry outside a named declaration')); continue
        rows = [r for r in lrows if s['decl'] in r.get('lean_declaration', '')]
        if not rows: silent.append(dict(sorry=key, decl=s['decl'], reason='declaration not in ledger'))
        elif not any((r.get('ledger_status') or r.get('note') or '').strip() for r in rows):
            silent.append(dict(sorry=key, decl=s['decl'], reason='ledger row has no status/reason'))
    out['silent_sorry'] = silent; out['code_sorry_count'] = len(sorries)
    chk('R3', not silent, f'{len(sorries)} code `sorry` occurrence(s) after stripping comments/docstrings; silent/untracked={silent}')
    # R6 in-Lean claimLedger vs CSV (block-aware: records span multiple lines)
    claims_lean_path = os.path.join(a.lean_dir, 'Atlas', 'Claims.lean')
    ledger_text = texts.get(claims_lean_path, '')
    inlean = {}
    for block in LEAN_BLOCK_SPLIT.split(ledger_text)[1:]:
        mid = re.match(r'\s*"([^"]+)"', block)
        mk = re.search(r'kind\s*:=\s*\.(\w+)', block); ms = re.search(r'status\s*:=\s*\.(\w+)', block)
        md = re.search(r'leanDecl\s*:=\s*"([^"]*)"', block)
        if mid and mk and ms and md:
            inlean[mid.group(1)] = dict(kind=mk.group(1), status=ms.group(1), decl=md.group(1))
    mism = []
    declared_csv = [r['claim_id'] for r in lrows if r.get('lean_declaration', '').strip()]
    for cid in declared_csv:
        if cid not in inlean: mism.append(f'{cid}: declared in CSV/ledger but absent from in-Lean claimLedger')
    for cid, v in inlean.items():
        rows = [r for r in lrows if r['claim_id'] == cid]
        if not rows: mism.append(f'{cid}: in Lean claimLedger but not in CSV'); continue
        r = rows[0]
        if r.get('lean_declaration', '').strip() != v['decl'].strip(): mism.append(f'{cid}: decl CSV={r.get("lean_declaration")!r} vs Lean={v["decl"]!r}')
        if r.get('ledger_status', '').strip().lower() != v['status'].lower(): mism.append(f'{cid}: status CSV={r.get("ledger_status")} vs Lean={v["status"]}')
    out['ledger_mismatch'] = mism; out['inlean_rows'] = len(inlean)
    chk('R6', not mism, f'in-Lean claimLedger rows={len(inlean)} (CSV declared={len(declared_csv)}); mismatches={mism[:10]}')
    # R7 internal status consistency: a declared row must not be marked notYetLemmatised
    bad_status = [r['claim_id'] for r in lrows if r.get('lean_declaration','').strip() and str(r.get('ledger_status','')).lower() == 'notyetlemmatised']
    out['declared_but_notyet'] = bad_status
    chk('R7', not bad_status, f'declared rows with notYetLemmatised status={bad_status} (status/declaration inconsistency)')
    # QA note: declaration-with-notYet status is internally inconsistent (reported, not silently passed)
    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out), exist_ok=True); json.dump(out, open(a.json_out, 'w'), indent=1)
    print(json.dumps(out, indent=1))
    return 0 if all(c['status'] == 'PASS' for c in out['checks']) else 1

if __name__ == '__main__': sys.exit(main())
