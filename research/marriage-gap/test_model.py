"""Plain-assert tests. Run: python3 test_model.py"""
import numpy as np
import model as M


def test_no_gap_when_nothing_differs():
    for p in (0.3, 0.7, 0.95):
        for m in (0.1, 0.5, 1.0):
            res = M.run(1.0, p, p, m)          # r = 1, p_m = p_w, main model (g = 0)
            for lo, hi in [(18, 34)] + list(M.BANDS.values()) + [(a, a) for a in range(18, 35)]:
                assert abs(M.gap(res, lo, hi)) < 1e-12


def test_shares_within_zero_and_one():
    for r in (1.0, 1.1, 1.3):
        for pm, pw in ((0.9, 0.5), (0.5, 0.9), (1.0, 1.0), (0.05, 0.05)):
            for m in (0.05, 0.5, 1.0):
                for g in (0, 2):
                    res = M.run(r, pm, pw, m, g)
                    for lo, hi in [(18, 34)] + list(M.BANDS.values()):
                        for st in (True, False):
                            s = M.shares(res, lo, hi, st)
                            assert np.isnan(s["w"]) or 0.0 <= s["w"] <= 1.0
                            assert np.isnan(s["m"]) or 0.0 <= s["m"] <= 1.0
                    assert (res["w_wants"] >= -1e-12).all() and (res["m_wants"] >= -1e-12).all()


def test_non_wanters_never_marry():
    # nobody wants marriage -> no marriages at all
    res = M.run(1.2, 0.0, 0.0, 0.8)
    assert res["marriages_w"].sum() == 0 and res["marriages_m"].sum() == 0
    # only women want it -> still no marriages (no man wants), and no man is ever married
    res = M.run(1.2, 0.0, 0.9, 0.8)
    assert res["marriages_m"].sum() == 0 and res["marriages_w"].sum() == 0
    # marriages never exceed the number of wanters
    res = M.run(1.1, 0.6, 0.8, 0.7)
    assert np.cumsum(res["marriages_w"])[-1] <= 0.8 + 1e-12
    assert np.cumsum(res["marriages_m"])[-1] <= 1.1 * 0.6 + 1e-12
    # the not-wanting boxes never change
    assert np.allclose(res["w_nowant"], 1 - 0.8) and np.allclose(res["m_nowant"], 1.1 * (1 - 0.6))


def test_totals_conserved():
    for g in (0, 2):
        res = M.run(1.15, 0.8, 0.9, 0.4, g)
        women, men = M.totals(res)
        assert np.allclose(women, 1.0)
        assert np.allclose(men, 1.15)
    # marriages are one man and one woman each
    res = M.run(1.15, 0.8, 0.9, 0.4, 2)
    assert abs(res["marriages_w"].sum() - res["marriages_m"].sum()) < 1e-12


def test_more_men_raises_the_men_share_only():
    # with equal preferences women are always the short side, so a surplus of men
    # leaves the women's path unchanged and keeps more wanting men in the pool
    lo = M.shares(M.run(1.00, 0.9, 0.9, 0.3))
    hi = M.shares(M.run(1.20, 0.9, 0.9, 0.3))
    assert abs(hi["w"] - lo["w"]) < 1e-12 and hi["m"] > lo["m"]


def test_age_gap_alone_makes_a_gap():
    # documented limit: with g = 2, men stay unmarried longer, so a gap exists even at r = 1
    assert M.gap(M.run(1.0, 0.8, 0.8, 0.4, g=2)) > 0.01


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
