"""Cluster D toy engine: level-structured takeoff toy, stdlib only.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

This is an extension of `takeoff.py` from the archived toy workspace
(/tmp/codex_unpack/.../workspace/takeoff.py): three sequential credentials, one gate
per cohort, seat construction rationed by unmet-application backlog, parents observing
last cohort's jobs and screening practice. Additions, all stipulated:

  * a cohort-size hook (for the #11 demographic shock), with a capacity-scaling switch;
  * a seat-injection hook (for the #10 PV-equal level schedules and the #12 lease);
  * a placement-signal / information-regime switch (for the #12 expectation arm);
  * a frozen-posts employer regime (JOBS = 40, as in model.py) next to the responsive one.

Nothing here is estimated. Numbers are properties of these rules.
"""
import random

LABEL = "ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates."

N = 120
HORIZON = 30
MAXN = 144
LEVELS = ("primary", "lower_secondary", "upper_secondary")

# Imposed parameter vector (recorded verbatim in RUN_MANIFEST.json).
DEFAULT_PARAMS = {
    "cohort_nominal": N,
    "horizon_cohorts": HORIZON,
    "max_cohort": MAXN,
    "fee": (0.20, 0.36, 0.55),
    "work_mult": (0.85, 1.35, 1.80),
    "payoff": (0.65, 0.51, 0.42),
    "access": (0.14, 0.90, 0.30),
    "rank": (0.05, 0.20, 0.65),
    "skill_gain": (0.25, 0.40, 0.60),
    "seat0": (18, 0, 0),
    "build_limit": 12,
    "work": 1.0,
    "capital": 1.0,
    "fixed_posts": 40,
    "discount_pv": 0.97,
    "placement_prior": 0.50,
    "group_cycle": 3,
    "investment_fixed": None,   # None -> takeoff backlog rule; int -> fixed seats/cohort
    "init_readers": 0.05,
    "init_formal_share": 0.10,
    "init_skill_stock": 0.0,
    "warm_stage": False,        # cohort 1 arrives with a pre-existing stage composition
    "belief_memory": 0.70,
    "placement_reference": 12.0,
    "belief_cap": 2.0,
    "belief_floor": 0.50,
}

# Affluence groups, as in takeoff.py: cash and home-work cost depend on group.
GROUP_CASH = (0.24, 0.62, 1.05)
GROUP_HOME = (0.65, 0.42, 0.25)


# --------------------------------------------------------------------------- draws
def cohort_draws(seed, t, size):
    """Latent cohort draws, a pure function of (seed, t, slot).

    Slots consume exactly three uniforms each, in a fixed order, so a cohort of size n
    is an exact prefix of a cohort of size n' > n under the same (seed, t). That is what
    makes the #11 size arms paired person-for-person, and every arm inside one seed is
    draw-identical by construction. The shuffle uses a separate stream so it cannot
    depend on the size either.
    """
    rng_slot = random.Random((seed * 1000 + t) & 0x7FFFFFFF)
    cash, home, apt = [], [], []
    for i in range(size):
        g = i % 3
        cash.append(GROUP_CASH[g] + rng_slot.uniform(0.0, 0.50))
        home.append(GROUP_HOME[g] * rng_slot.uniform(0.45, 1.55))
        apt.append(rng_slot.random())
    rng_order = random.Random((seed * 1000 + t + 7919) & 0x7FFFFFFF)
    order = list(range(MAXN))
    rng_order.shuffle(order)
    # Lottery priority is a nested subsequence: the size-n order is the size-n' order
    # (n' > n) filtered to slots < n, so slot priority is draw-identical across sizes.
    lottery = [x for x in order if x < size]
    return cash, home, apt, lottery


# --------------------------------------------------------------------------- engine
def simulate(seed, seats_plan=None, sizes=None, per_child=False, employer="responsive",
             info=False, fee_plan=None, horizon=HORIZON, params=None):
    """Run one arm of one seed. Returns a list of per-cohort dicts.

    `fee_plan[t]` may be a dict {level: fee} applied to cohort t (t zero-indexed);
    `seats_plan[t]` is a 3-tuple of seats added to installed capacity at cohort t
    (negative values remove leased seats).
    """
    p = dict(DEFAULT_PARAMS)
    if params:
        p.update(params)
    sizes = sizes or [N] * horizon
    base_fee = list(p["fee"])
    seat_f = [float(x) for x in p["seat0"]]
    readers = float(p["init_readers"])
    skill_stock = float(p["init_skill_stock"])
    formal_share = float(p["init_formal_share"])
    placement = p["placement_prior"]
    belief = 1.0

    out = []
    for t in range(horizon):
        n = sizes[t]
        scale = n / float(N)
        cash, home, apt, lottery = cohort_draws(seed, t, n)

        if seats_plan is not None:
            inj = seats_plan[t]
            for k in range(3):
                seat_f[k] = max(0.0, seat_f[k] + float(inj[k]))
        # "per_child" capacity: the nominal stock is seats per 120 children, so actual
        # capacity is seat_f * n/120 (seats per child held constant). Otherwise the stock
        # is delivered as absolute seats, identical whatever the cohort size.
        cap = [min(n, max(0, int(seat_f[k] * (scale if per_child else 1.0)))) for k in range(3)]

        admitted_by_level = [[], [], []]
        if p["warm_stage"] and t == 0:
            # Mid-transition starting composition (identical in every arm): cohort 1
            # arrives with 12 already at upper-secondary entry, 88 at primary completion,
            # and 20 with no credential.
            stage = [2 if i % 10 == 0 else (1 if i % 10 != 1 else 0) for i in range(n)]
        else:
            stage = [0] * n
        skill = [0.0] * n
        comple = [0, 0, 0]
        appl = [0, 0, 0]
        backlog = [0, 0, 0]

        for k in range(3):
            f = base_fee[k]
            fp = fee_plan.get(t) if fee_plan else None
            if fp and k in fp:
                f = fp[k]
            elig = [i for i in lottery if stage[i] == k]
            applicants = []
            for i in elig:
                cost = home[i] * p["work_mult"][k] * p["work"]
                payoff = p["payoff"][k] * (0.7 + apt[i])
                if k == 0:
                    access = p["access"][0]
                else:
                    access = p["access"][k] * readers * formal_share * 5.0
                rank = p["rank"][k] * readers * formal_share * 4.0
                if k == 2 and info:
                    # Information regime (stipulated): families act on an adaptive belief
                    # about upper-secondary opportunity, in units of the reference flow of
                    # 12 credentialed places; the belief updates with a 0.70 memory.
                    mult = min(p["belief_cap"], max(p["belief_floor"], belief))
                    access *= mult
                    rank *= mult
                if cash[i] >= f and payoff + access + rank >= f + cost:
                    applicants.append(i)
            admitted = applicants[:max(0, cap[k])]
            admitted_by_level[k] = admitted
            for i in admitted:
                stage[i] += 1
                skill[i] += p["skill_gain"][k]
            appl[k] = len(applicants)
            comple[k] = len(admitted)
            backlog[k] = len(applicants) - len(admitted)

        # ---- labour market, kept from takeoff.py
        skill_stock = 0.80 * skill_stock + 0.20 * sum(skill) / n
        if employer == "responsive":
            posts = min(n, round(n * (0.10 + 0.52 * p["capital"] * skill_stock)))
        elif employer == "frozen":
            posts = min(n, int(p["fixed_posts"]))
        else:
            raise ValueError("employer must be 'responsive' or 'frozen'")
        readers_new = 0.05 + 0.85 * sum(1 for s in stage if s >= 2) / n
        gated = min(posts, round(posts * readers_new))
        ranked = sorted(lottery, key=lambda i: stage[i], reverse=True)
        cred = [i for i in ranked if stage[i] >= 2][:gated]
        cred_set = set(cred)
        open_pool = sorted((i for i in range(n) if i not in cred_set),
                           key=lambda i: apt[i], reverse=True)
        hires = cred_set | set(open_pool[:max(0, posts - gated)])
        formal_share = len(hires) / n
        readers = readers_new

        upper = [i for i in range(n) if stage[i] >= 3]
        placement = (sum(1 for i in upper if i in hires) / len(upper)) if upper else placement * 0.5
        grad = [i for i in cred if stage[i] >= 3]
        # Adaptive belief about upper-secondary opportunity, in units of the reference
        # flow of `placement_reference` credentialed places per cohort. Persistence 0.70.
        observed = len(grad) / p["placement_reference"]
        belief = p["belief_memory"] * belief + (1.0 - p["belief_memory"]) * observed

        output = sum(1.0 + 0.18 * s + (i in hires) * p["capital"] * (0.45 + 0.85 * s)
                     for i, s in enumerate(skill))
        poor_upper = sum(1 for i in admitted_by_level[2] if i % 3 == 0)
        poor_primary = sum(1 for i in admitted_by_level[0] if i % 3 == 0)
        out.append(dict(
            t=t + 1, n=n, seats=tuple(cap),
            completions=tuple(comple), applications=tuple(appl),
            poor_upper=poor_upper, poor_primary=poor_primary,
            belief=belief,
            posts=posts, hires=len(hires), cred_hires=len(cred),
            grad_hires=len(grad), formal_share=formal_share,
            placement=placement, output=output, backlog=tuple(backlog),
        ))

        if p["investment_fixed"] is not None:
            budget = int(p["investment_fixed"])
        else:
            budget = min(int(p["build_limit"]), 3 + int(len(hires) * 0.16))
        for _ in range(budget):
            k = max(range(3), key=backlog.__getitem__)
            if backlog[k] <= 0:
                break
            seat_f[k] += 1.0
            backlog[k] -= 1

    return out


# ----------------------------------------------------------------- crossing metrics
# (level index, completion share threshold) — fixed in PRE_DECLARATIONS.md.
MILESTONES = (
    ("M0", 0, 0.50),
    ("M1", 0, 0.90),
    ("M2", 1, 0.50),
    ("M3", 2, 0.50),
    ("U90", 2, 0.90),
)


def crossings(series, horizon=HORIZON):
    """First cohort t with completions_k(t)/n(t) >= theta; 31 and censored if never."""
    res = {}
    for name, level, theta in MILESTONES:
        year, cens = horizon + 1, 1
        for row in series:
            if row["completions"][level] / row["n"] >= theta:
                year, cens = row["t"], 0
                break
        res["X_" + name] = year
        res["cens_" + name] = cens
    return res


def shares_at_horizon(series, tail=5):
    rows = series[-tail:]
    prim = sum(r["completions"][0] / r["n"] for r in rows) / len(rows)
    lower = sum(r["completions"][1] / r["n"] for r in rows) / len(rows)
    upper = sum(r["completions"][2] / r["n"] for r in rows) / len(rows)
    return prim, lower, upper


def metrics(series):
    """Per-seed scalar metrics shared by the three experiments."""
    m = crossings(series)
    m["U90"] = m.pop("X_U90")
    prim, lower, upper = shares_at_horizon(series)
    m["primary_share_h"] = prim
    m["lower_share_h"] = lower
    m["upper_share_h"] = upper
    m["floor_ceiling_gap"] = upper - prim
    m["S_M3_M0"] = m["X_M3"] - m["X_M0"]
    m["S_M3_M2"] = m["X_M3"] - m["X_M2"]
    m["S_M1_M0"] = m["X_M1"] - m["X_M0"]
    m["upper_total"] = sum(r["completions"][2] for r in series)
    m["primary_total"] = sum(r["completions"][0] for r in series)
    m["applications_total"] = sum(sum(r["applications"]) for r in series)
    m["hires_total"] = sum(r["hires"] for r in series)
    tail = series[-5:]
    m["poor_share_upper_h"] = mean([(r["poor_upper"] / r["completions"][2]) if r["completions"][2] else 0.0
                                    for r in tail])
    m["primary_seats_h"] = mean([r["seats"][0] for r in series[-5:]])
    m["primary_apps_h"] = mean([r["applications"][0] for r in series[-5:]])
    return m


# ------------------------------------------------------------------ stats helpers
def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return float("nan")
    mid = n // 2
    return xs[mid] if n % 2 else 0.5 * (xs[mid - 1] + xs[mid])


def quantile(xs, q):
    xs = sorted(xs)
    if not xs:
        return float("nan")
    pos = q * (len(xs) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")
