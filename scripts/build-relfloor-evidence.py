"""Put the v2 graded-liquidity credential-floor summaries into public/evidence.js (key 'relfloor').

Main test per country: Cambodia = full UIS quintile profile, Vietnam = MICS 2014 profile, China = aggregate
(no profile exists). Source: public/reference/relfloor_countries_v2_smoothliq.json. Re-pins its hash.
Then run scripts/sync-react-models.py.
"""
import hashlib, json
from pathlib import Path
root = Path(__file__).resolve().parents[1]; pub = root / 'public'
SRC = 'relfloor_countries_v2_smoothliq.json'
TESTS = {'Cambodia': 'profile', 'Vietnam': 'mics', 'China': 'agg'}


def compact(src):
    out = {}
    for c, t in TESTS.items():
        out[c] = {}
        for s, r in src[c][t].items():
            out[c][s] = {'accepted': r['accepted'], 'rate': r['rate'],
                         'exit_low': r['exit_low_2021'] if c == 'Cambodia' else None,
                         'b_rel': r['post_b_rel'] if s == 'M_REL' else None}
    return out


if __name__ == '__main__':
    f = pub / 'reference' / SRC
    p = pub / 'evidence.js'; s = p.read_text(); a = s.index('{'); D, end = json.JSONDecoder().raw_decode(s[a:])
    D['relfloor'] = compact(json.loads(f.read_text()))
    D['sha256'].pop('relfloor_countries.json', None)
    D['sha256'][SRC] = hashlib.sha256(f.read_bytes()).hexdigest()
    p.write_text(s[:a] + json.dumps(D, separators=(',', ':')) + s[a + end:])
    print(json.dumps(D['relfloor'], indent=1))
