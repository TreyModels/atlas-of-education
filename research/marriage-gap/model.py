"""Smallest model that can express both rival explanations of the marriage-aspiration gap.

In plain words
--------------
* Every birth cohort is the same size. Per 1 woman there are r men.   (parameter r)
* A share p_w of women and a share p_m of men want to marry. This is fixed for
  each person and never changes.                                       (p_w, p_m)
* A man of age a can only marry a woman of age a - g, with g = 0 in the main model
  (g = 2 is run as a robustness check). Marriage is possible from woman age 20 (fixed).
* Each year, the unmarried people who want marriage in a pair of matched cohorts
  meet. The number of marriages is m times the SMALLER of the two groups. (m)
* People who do not want marriage never marry. Nobody dies, migrates or divorces.
* Output: among unmarried 18-34 year olds, the share who want to marry, by sex,
  overall and by age band.

Parameters fitted or swept: r, p_m, p_w, m (four). Age gap and age limits are fixed.
"""
import numpy as np

AGE_GAP = 0           # men marry women this many years younger; 0 = same age (fixed, not fitted)
MIN_WOMAN_AGE = 20    # first age at which a woman (and so her partner cohort) can marry (fixed)
AGE_MIN, AGE_MAX = 18, 34
BANDS = {"18-22": (18, 22), "23-26": (23, 26), "27-30": (27, 30), "31-34": (31, 34)}


def run(r, p_m, p_w, m, g=AGE_GAP):
    """Step one man cohort and one woman cohort through life, pairing by age.

    All cohorts are identical, so the man of age a and the woman of age a-g who meet
    in a given year have each already lived through the same earlier years as every
    other cohort. Walking up through man age a, woman age b=a-g, is therefore enough.
    Everything is per 1 woman at entry (men: r).
    """
    ages_m = np.arange(AGE_MIN, AGE_MAX + g + 1)     # men are followed g years longer
    n_w = AGE_MAX - AGE_MIN + 1
    x = r * p_m               # unmarried men who want marriage (this cohort)
    w = p_w                   # unmarried women who want marriage
    x_end = np.zeros(len(ages_m))
    w_end = np.zeros(n_w)
    mar_m = np.zeros(len(ages_m))
    mar_w = np.zeros(n_w)
    for a in ages_m:
        b = a - g
        k = 0.0
        if MIN_WOMAN_AGE <= b <= AGE_MAX:
            k = m * min(x, w)             # marriages this year: m times the short side
            w -= k
            mar_w[b - AGE_MIN] = k
        elif AGE_MIN <= b < MIN_WOMAN_AGE:
            pass
        x -= k
        mar_m[a - AGE_MIN] = k
        x_end[a - AGE_MIN] = x
        if AGE_MIN <= b <= AGE_MAX:
            w_end[b - AGE_MIN] = w
    return dict(r=r, p_m=p_m, p_w=p_w, m=m, ages=np.arange(AGE_MIN, AGE_MAX + 1),
                w_wants=w_end, w_nowant=np.full(n_w, 1 - p_w),
                m_wants=x_end[:n_w], m_nowant=np.full(n_w, r * (1 - p_m)),
                m_wants_all=x_end, marriages_w=mar_w, marriages_m=mar_m)


def _band_mask(ages, lo, hi):
    return (ages >= lo) & (ages <= hi)


def shares(res, lo=AGE_MIN, hi=AGE_MAX, standardise=True):
    """Share wanting marriage among unmarried people aged lo..hi, by sex.

    standardise=True (default): work out the share at each single age, then give every
    age the same weight (a simple age standardisation, as the survey chart is
    age-standardised). standardise=False: pool all unmarried people in the age range.
    """
    k = _band_mask(res["ages"], lo, hi)
    out = {}
    for s, wants, nowant in (("w", res["w_wants"], res["w_nowant"]),
                             ("m", res["m_wants"], res["m_nowant"])):
        den = wants[k] + nowant[k]          # unmarried people of this sex at each age
        if den.sum() < 1e-12:
            out[s] = float("nan")           # nobody unmarried: share undefined
        elif standardise:
            ok = den > 1e-12                # ages with nobody unmarried are skipped
            out[s] = float(np.mean(wants[k][ok] / den[ok]))
        else:
            out[s] = float(wants[k].sum() / den.sum())
    return out


def gap(res, lo=AGE_MIN, hi=AGE_MAX, standardise=True):
    """Men minus women, as a share (positive = women want marriage less)."""
    s = shares(res, lo, hi, standardise)
    return s["m"] - s["w"]


def profile(res):
    """Shares and gap overall and by age band."""
    d = {"all": dict(shares(res), gap=gap(res))}
    for name, (lo, hi) in BANDS.items():
        d[name] = dict(shares(res, lo, hi), gap=gap(res, lo, hi))
    return d


def ever_married(res, lo=30, hi=34):
    """Share of each sex (and both pooled) who have ever married, average over ages lo..hi."""
    k = _band_mask(res["ages"], lo, hi)
    cw = np.cumsum(res["marriages_w"])[: len(res["ages"])]
    cm = np.cumsum(res["marriages_m"])[: len(res["ages"])]
    r = res["r"]
    w = float((cw[k] / 1.0).mean())
    mm = float((cm[k] / r).mean())
    pooled = float(((cw[k] + cm[k]) / (1.0 + r)).mean())
    return dict(w=w, m=mm, pooled=pooled)


def totals(res):
    """Bookkeeping used by the tests: everyone in the cohort is in exactly one box."""
    n_w = len(res["ages"])
    cw = np.cumsum(res["marriages_w"])
    cm = np.cumsum(res["marriages_m"])[:n_w]
    women = res["w_wants"] + res["w_nowant"] + cw
    men = res["m_wants"] + res["m_nowant"] + cm
    return women, men
