"""Survey measurement layer + tie-breaker extraction (prereg §3.3/§3.4).

Every tie-breaker is computed from *measured* variables only: reported state, recorded hours,
reported tutoring, and a noisy consumption proxy. Hidden work is never measured (reported as
school-only or study+work), by design (audit §7.3, claim 9).
"""
import numpy as np

# rows = true state, cols = reported state {0,1,2,3}; hidden work never reported as employment.
MISCLASS = np.array([
    [0.95, 0.05, 0.00, 0.00],
    [0.10, 0.70, 0.20, 0.00],
    [0.00, 0.20, 0.80, 0.00],
    [0.60, 0.40, 0.00, 0.00],
], dtype=np.float64)

NONRESP = {"state": 0.03, "hours": 0.05, "tutor": 0.04, "cons": 0.06}
SAMPLE_PER_YEAR = 1500
TUTOR_FN, TUTOR_FP = 0.20, 0.05
CONS_SIGMA = 0.35


def survey_unit(res_post, rng, cons_cuts=None, sample_per_year=SAMPLE_PER_YEAR):
    """Draw repeated cross-sections from post years and apply the measurement model."""
    st = res_post["state"]
    tut = res_post["tutor"]
    wrk = res_post["work"]
    yhh = res_post["y_hh"]
    tpost, n = st.shape

    idx = np.stack([rng.choice(n, size=sample_per_year, replace=False) for _ in range(tpost)])
    rows = np.arange(tpost)[:, None]
    true_state = st[rows, idx].reshape(-1).astype(np.int32)
    true_work = wrk[rows, idx].reshape(-1).astype(np.float64)
    true_tutor = tut[rows, idx].reshape(-1).astype(np.int32)
    yhh_s = yhh[rows, idx].reshape(-1).astype(np.float64)
    m = true_state.size

    # --- state reporting -----------------------------------------------------
    u = rng.random(m)
    cum = np.cumsum(MISCLASS, axis=1)
    rep_state = np.empty(m, dtype=np.int32)
    for k in range(4):
        mask = true_state == k
        if np.any(mask):
            rep_state[mask] = np.searchsorted(cum[k], u[mask], side="right")
    rep_state = np.clip(rep_state, 0, 3)

    # --- hours: recorded only for reported-employed children with positive true work
    employed = np.isin(rep_state, (1, 2))
    hours = np.where(true_state == 3, 0.5 * true_work, true_work)
    hours = hours + rng.normal(0.0, 2.0, size=m)
    hours = np.round(hours / 5.0) * 5.0
    hours = np.clip(hours, 1.0, 60.0)
    hours = np.where(employed & (true_work > 0), hours, np.nan)

    # --- tutoring reporting --------------------------------------------------
    rep_tutor = true_tutor.copy()
    rep_tutor[(true_tutor == 1) & (rng.random(m) < TUTOR_FN)] = 0
    rep_tutor[(true_tutor == 0) & (rng.random(m) < TUTOR_FP)] = 1

    # --- consumption proxy and quintiles ------------------------------------
    cons = yhh_s * np.exp(rng.normal(0.0, CONS_SIGMA, size=m))
    if cons_cuts is None:
        cons_cuts = np.quantile(cons, [0.2, 0.4, 0.6, 0.8])
    cons_q = np.searchsorted(cons_cuts, cons, side="right") + 1

    # --- item non-response ---------------------------------------------------
    rep_state_m = rep_state.astype(np.float64)
    rep_state_m[rng.random(m) < NONRESP["state"]] = np.nan
    hours[rng.random(m) < NONRESP["hours"]] = np.nan
    rep_tutor_m = rep_tutor.astype(np.float64)
    rep_tutor_m[rng.random(m) < NONRESP["tutor"]] = np.nan
    cons_q_m = cons_q.astype(np.float64)
    cons_q_m[rng.random(m) < NONRESP["cons"]] = np.nan

    return {"state": rep_state_m, "hours": hours, "tutor": rep_tutor_m,
            "cons_q": cons_q_m, "cons_cuts": cons_cuts, "sample_per_year": sample_per_year}


def _tv_distance(states, q, qa, qb):
    a = states[(q == qa) & ~np.isnan(states)]
    b = states[(q == qb) & ~np.isnan(states)]
    if a.size == 0 or b.size == 0:
        return np.nan
    pa = np.array([np.mean(a == k) for k in range(4)])
    pb = np.array([np.mean(b == k) for k in range(4)])
    return float(0.5 * np.sum(np.abs(pa - pb)))


def tiebreakers(meas):
    """Four pre-registered tie-breaker vectors from measured variables only."""
    st = meas["state"]
    hrs = meas["hours"]
    tut = meas["tutor"]
    q = meas["cons_q"]

    ok_state = ~np.isnan(st)
    ok_q = ~np.isnan(q)
    q12 = np.isin(q, (1, 2)) & ok_q
    q24 = np.isin(q, (2, 3, 4)) & ok_q
    q45 = np.isin(q, (4, 5)) & ok_q

    def share(value, qmask):
        den = int(np.sum(qmask & ok_state))
        if den == 0:
            return np.nan
        return float(np.sum((st == value) & qmask & ok_state) / den)

    # T1: state x consumption-quintile profile (4 dims)
    t1 = np.array([
        share(2, q12),                                  # visible work share, Q1-Q2
        share(1, q24),                                  # study+work share, Q2-Q4
        share(0, q45),                                  # school-only share, Q4-Q5
        _tv_distance(np.where(ok_state, st, np.nan), np.where(ok_q, q, np.nan), 1, 5),
    ], dtype=np.float64)

    # T2: hours-band shape among reported-employed with a recorded hour (5 dims)
    employed = np.isin(st, (1, 2)) & ok_state
    hm = employed & ~np.isnan(hrs) & (hrs >= 1)
    if np.sum(hm) >= 20:
        h = hrs[hm]
        t2 = np.array([
            np.mean((h >= 1) & (h <= 13)), np.mean((h >= 14) & (h <= 27)),
            np.mean((h >= 28) & (h <= 42)), np.mean(h >= 43),
            np.quantile(h, 0.75) - np.quantile(h, 0.25),
        ], dtype=np.float64)
    else:
        t2 = np.full(5, np.nan)

    # T3: tutoring gradient, Q4-Q5 minus Q1-Q2 (1 dim)
    ok_t = ~np.isnan(tut)
    t = np.where(ok_t, tut, np.nan)
    den_top = int(np.sum(q45 & ok_t))
    den_bot = int(np.sum(q12 & ok_t))
    top = np.sum((t == 1) & q45 & ok_t)
    bot = np.sum((t == 1) & q12 & ok_t)
    t3 = np.array([(top / den_top if den_top else np.nan)
                   - (bot / den_bot if den_bot else np.nan)], dtype=np.float64)

    # T4: hidden-work proxy = school-only share in Q1-Q2 (1 dim)
    t4 = np.array([share(0, q12)], dtype=np.float64)

    return {"T1": t1, "T2": t2, "T3": t3, "T4": t4}
