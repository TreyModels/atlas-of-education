"""Re-pin engine SHA-256 hashes in public/evidence.js after an intended engine change.

Usage: python3 scripts/repin-hashes.py petri.js relocation.js
Only the named files are re-pinned, so an unreviewed change still fails the test.
Then run scripts/sync-react-models.py to refresh src/models.
"""
import hashlib, json, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]; pub = root / 'public'
p = pub / 'evidence.js'; s = p.read_text()
a = s.index('{'); D, end = json.JSONDecoder().raw_decode(s[a:])
for name in sys.argv[1:]:
    f = next((x for x in [pub / 'engines' / name, pub / 'reference' / name, pub / name] if x.exists()), None)
    if f is None or name not in D['sha256']: sys.exit(f'unknown file {name}')
    D['sha256'][name] = hashlib.sha256(f.read_bytes()).hexdigest(); print('pinned', name)
p.write_text(s[:a] + json.dumps(D, separators=(',', ':')) + s[a + end:])
