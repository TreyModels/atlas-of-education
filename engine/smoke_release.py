"""End-to-end release checks: actual local HTTP handlers and policy invariants."""
from pathlib import Path
import json, sys, threading, urllib.request
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'app'))
import server as app
import policy


def main():
    http=app.http.server.ThreadingHTTPServer(('127.0.0.1',0),app.H)
    thread=threading.Thread(target=http.serve_forever,daemon=True); thread.start()
    base='http://127.0.0.1:'+str(http.server_port)
    try:
        def get(path):
            with urllib.request.urlopen(base+path,timeout=180) as response: return json.load(response)
        meta=get('/api/meta'); assert meta['version']=='0.3.2'
        cmap=get('/api/context_map'); assert cmap['samples']==21
        assert all(c['training_until']==2015 for c in cmap['countries'].values())
        run=get('/api/run?country=cambodia&anchor_until=2015&seed=7')
        assert run['validation']['completion_targets_until']<=2015
        assert run['validation']['newly_blind'] is False
        assert run['calibration'] is None
        replay=get('/api/run?country=cambodia&anchor_until=2030&seed=7')
        assert replay['validation']['mode']=='historical replay'
        assert replay['calibration'] is not None
        print('PASS: HTTP metadata, context map, temporal test and replay semantics')
    finally:
        http.shutdown(); http.server_close(); thread.join()
    noop=policy.lab('cambodia',{},year=2025,until=2029,seeds=(7,))
    assert all(r['delta'] in (None,0) for r in noop['rows'])
    assert noop['cost']['extra_public_spending_median_incomes']==0
    print('PASS: no-op policy has exactly zero effect and extra cost')
    changed=policy.lab('cambodia',{'cct':.08},year=2025,until=2029,seeds=(7,))
    s=changed['series']; pre=[i for i,y in enumerate(s['baseline']['years']) if y<2025]
    for indicator in ('tutoring','youth_unemployment','private_lower'):
        assert all(s['baseline'][indicator][i]==s['scenario'][indicator][i] for i in pre)
    for level in s['baseline']['completion']:
        assert all(s['baseline']['completion'][level][i]==s['scenario']['completion'][level][i] for i in pre)
    assert changed['cost']['extra_public_spending_median_incomes']>0
    print('PASS: policy arms match before intervention; increased CCT incurs extra cost')

if __name__=='__main__': main()
