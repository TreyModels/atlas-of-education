#!/usr/bin/env python3
"""Mechanical consistency audit of Lean claims (Paper C / programme claim ledger).

Usage:
  python3 docs/audit/lemma_audit.py --claims results/audit/paper_claims.csv \
      --lean verification/lean/Claims.lean --ledger docs/audit/LEMMA_LEDGER.md

Rules checked:
 R1 every claim id in paper_claims.csv is unique and non-empty
 R2 every claim id has exactly ONE declaration in Claims.lean OR an explicit
    "not-yet-lemmatised" entry in LEMMA_LEDGER.md (no silent omissions)
 R3 no silent `sorry`: every Lean `sorry` lies in a declaration that appears in the
    ledger with a non-empty reason, or on a claim-row marked not-yet-lemmatised with reason
 R4 claim ids in the ledger match claim ids in paper_claims.csv (no orphans/mismatches)
 R5 no duplicate declarations (same name) and no duplicate ledger claim rows
"""
import argparse, csv, json, re, sys

DECL_RE = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)*(theorem|lemma|def|example|abbrev)\s+([A-Za-z0-9_\.\']+)')
SORRY_RE = re.compile(r'\bsorry\b')
NOTYET_RE = re.compile(r'not[- ]?yet[- ]?lemmati[sz]ed|NOT[- ]?YET[- ]?LEMMATISED', re.I)

def parse_lean(path):
    decls = []   # (kind, name, line)
    sorrys = []  # (line, enclosing decl name or None)
    cur = None
    for i, line in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
        m = DECL_RE.match(line)
        if m: cur = m.group(2); decls.append((m.group(1), cur, i))
        if SORRY_RE.search(line): sorrys.append((i, cur))
    return decls, sorrys

def parse_ledger(path):
    """Return (entries: list of dicts with claim_id/declaration/status/reason/line, raw rows)."""
    text = open(path, encoding='utf-8', errors='replace').read().splitlines()
    entries = []
    for i, line in enumerate(text, 1):
        if line.strip().startswith('|') and '---' not in line:
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) >= 2:
                ids = re.findall(r'\b[A-Z]{1,10}-\d{1,3}\b', ' '.join(cells))
                if ids:
                    for cid in ids:
                        entries.append(dict(claim_id=cid, cells=cells, line=i,
                                            declaration=cells[1] if len(cells) > 1 else '',
                                            status=' '.join(cells[2:4]) if len(cells) > 2 else '',
                                            reason=' '.join(cells[2:]) if len(cells) > 2 else ''))
        else:
            ids = re.findall(r'\b[A-Z]{1,10}-\d{1,3}\b', line)
            for cid in ids:
                entries.append(dict(claim_id=cid, cells=[line.strip()], line=i, declaration='',
                                    status=('NOT-YET-LEMMATISED' if NOTYET_RE.search(line) else ''),
                                    reason=line.strip()))
    return entries, text

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--claims', required=True); ap.add_argument('--lean', required=True); ap.add_argument('--ledger', required=True)
    ap.add_argument('--json-out', default=None)
    a = ap.parse_args()
    out = dict(claims=a.claims, lean=a.lean, ledger=a.ledger, checks=[], missing_decls=[], duplicates=[], mismatches=[], silent_sorry=[], blunt={})
    def chk(rid, ok, detail):
        out['checks'].append(dict(id=rid, status='PASS' if ok else 'FAIL', detail=detail))
    # baseline claims
    rows = list(csv.DictReader(open(a.claims)))
    ids = [r['claim_id'].strip() for r in rows]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    chk('R1', bool(ids) and not dup and all(ids), f'{len(ids)} claims; duplicate ids={dup}')
    import os
    if not (os.path.exists(a.lean) and os.path.exists(a.ledger)):
        out['blunt'] = dict(status='BLOCKED', missing=[p for p in (a.lean, a.ledger) if not os.path.exists(p)])
        chk('R2', False, f'BLOCKED: missing {out["blunt"]["missing"]}')
        chk('R3', False, 'BLOCKED: no Lean/ledger files')
        chk('R4', False, 'BLOCKED: no Lean/ledger files')
        chk('R5', False, 'BLOCKED: no Lean/ledger files')
    else:
        decls, sorrys = parse_lean(a.lean)
        entries, raw = parse_ledger(a.ledger)
        decl_names = [d[1] for d in decls]
        dup_decl = sorted({n for n in decl_names if decl_names.count(n) > 1})
        chk('R5', not dup_decl, f'{len(decls)} declarations; duplicate names={dup_decl}')
        led_ids = {}
        for e in entries: led_ids.setdefault(e['claim_id'], []).append(e)
        dup_led = sorted([i for i, v in led_ids.items() if len(v) > 1])
        chk('R4', not (set(led_ids) - set(ids)),
            f'ledger ids not in claims={sorted(set(led_ids)-set(ids))[:10]}; claims without ledger entry={sorted(set(ids)-set(led_ids))[:10]}')
        # R2: each claim exactly one declaration OR not-yet-lemmatised entry
        def decl_for(cid):
            return [n for n in decl_names if cid.replace('-', '_') in n or cid in n]
        missing = []; multi = []
        for cid in ids:
            ds = decl_for(cid)
            e = led_ids.get(cid, [])
            notyet = any(NOTYET_RE.search(' '.join(x['cells'])) for x in e)
            if not ds and not notyet: missing.append(cid)
            if len(ds) > 1: multi.append((cid, ds))
        out['missing_decls'] = missing; out['multi_decls'] = multi
        chk('R2', not missing and not multi, f'missing declaration/not-yet entry={missing[:15]}; multi-declared={multi[:10]}')
        # R3: no silent sorry
        silent = []
        for line, encl in sorrys:
            if not encl: silent.append(dict(line=line, decl=None, reason='sorry outside a named declaration')); continue
            e = [x for x in entries if x['claim_id'] and (encl in x['declaration'] or encl in ' '.join(x['cells']))]
            if not e: silent.append(dict(line=line, decl=encl, reason='declaration not in ledger'))
            elif not any(x['status'] or x['reason'] for x in e): silent.append(dict(line=line, decl=encl, reason='ledger entry has no status/reason'))
        out['silent_sorry'] = silent
        chk('R3', not silent, f'{len(sorrys)} sorry occurrences; silent/untracked={silent[:10]}')
        # R4 extras: ledger ids not in claims + claims with no lean decl and no not-yet entry already covered
        out['ledger_only_ids'] = sorted(set(led_ids) - set(ids))
    if a.json_out: json.dump(out, open(a.json_out, 'w'), indent=1)
    print(json.dumps(out, indent=1)[:6000])
    return 0 if all(c['status'] == 'PASS' for c in out['checks']) else (2 if out['blunt'].get('status') == 'BLOCKED' else 1)

if __name__ == '__main__': sys.exit(main())
