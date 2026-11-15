"""Run: python -m unittest test_ledger -v   (from this folder)"""
import csv, os, shutil, tempfile, unittest
import models as M
import score as S


class T(unittest.TestCase):
    def setUp(self):
        self.series, self.grads = M.load_observed(), M.load_graduates()

    def test_no_leak(self):
        """Changing anything after the origin (rates, later class sizes) must not change the forecast."""
        for o in (M.idx(2025, 6), M.idx(2025, 12), M.idx(2026, 5), M.idx(2026, 9)):
            for h in (1, 3, 6, 12):
                for name in M.NAMES:
                    base = M.forecast(name, self.series, self.grads, o, o + h)
                    s2 = {i: (v + 7.0 if i > o else v) for i, v in self.series.items()}
                    s2[o + 40] = 99.0
                    g2 = {c: (g * 3 if M.idx(c - 1, 12) > o else g) for c, g in self.grads.items()}
                    self.assertEqual(base, M.forecast(name, s2, g2, o, o + h), (name, M.label(o), h))

    def test_ledger_complete(self):
        rows = list(csv.DictReader(open(os.path.join(M.HERE, 'ledger.csv'))))
        targets = {M.label(M.idx(2026, 10) + k) for k in range(6)}
        for name in M.NAMES:
            got = {r['target_month'] for r in rows if r['model'] == name}
            self.assertEqual(got, targets, name)
        for name in ('blind_seasonal_2024_spread11', 'blind_naive_2024'):
            self.assertEqual({r['target_month'] for r in rows if r['model'] == name}, {'2026-10', '2026-11', '2026-12'})
            self.assertTrue(all(r['date_frozen'] == '2026-11-05' for r in rows if r['model'] == name))
        self.assertTrue(all(r['date_frozen'] == '2026-11-14' for r in rows if r['model'] in M.NAMES))
        self.assertTrue(all(M.MODELS[n]['n_params'] <= 4 for n in M.NAMES))

    def test_score_nothing_yet(self):
        d = tempfile.mkdtemp()
        try:
            p = os.path.join(d, 'o.csv')   # real data only up to the ledger cutoff
            with open(M.OBSERVED) as f, open(p, 'w') as g:
                g.write(f.readline())
                for line in f:
                    y, m = line.split(',')[:2]
                    if M.idx(int(y), int(m)) <= M.idx(2026, 9):
                        g.write(line)
            out = S.score(observed_path=p)
            self.assertEqual(out, [])
            self.assertIn('nothing to score yet', S.write(out, d))
            with open(p, 'a') as g:
                g.write('2026,10,17.0,test\n')
            out = S.score(observed_path=p)
            self.assertTrue(out and all(r['n_months'] == 1 for r in out))
        finally:
            shutil.rmtree(d)


if __name__ == '__main__':
    unittest.main()
