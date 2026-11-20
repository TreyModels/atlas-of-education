"""Cluster C toy models (#7, #8, #9) for the Council brief 015 specification.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.
No historical test. Phase closed. Do not cite numbers as estimates.

Standard library only (no numpy, no pandas, no scipy). Every number produced
here is a property of the stipulated rules below, nothing else.

Design rules enforced by construction:
  * Pairing: latent draws are produced by draw_*_case(seed[, t]) with a
    random.Random constructed only from (seed, t). Arm parameters are never
    passed into a draw function, so every arm of a given seed sees identical
    draws. See selftest.py for the executable check.
  * Matched starting conditions: every arm of an experiment starts from the
    same initial state (same seats; same 30 rooms / 2 posts; same no-law
    baseline) and the same seed list.
  * One-factor shocks: arms differ in exactly one declared parameter.
"""

import random

LABEL = ("ILLUSTRATIVE TOY \u2014 stipulated parameters; not calibrated; "
         "not evidence; no historical test; phase closed; do not cite "
         "numbers as estimates")

N = 120


# --------------------------------------------------------------------------
# Experiment 7 — capacity by level (floor / ceiling split)
# --------------------------------------------------------------------------
COHORTS = 30
FEE = (0.20, 0.36, 0.55)
BASE_SEATS = (55, 20, 7)
GATE = (0.30, 0.45, 0.35)
APT_W = 0.15          # aptitude weight in the progression gate
STOCK_W = 0.15        # community-readiness weight in the progression gate
CASH_GROUP = (0.24, 0.62, 1.05)
CASH_DRAW = 0.50
SEAT_RAMP = 4         # cohorts over which a capacity shock is installed
STOCK_KEEP = 0.80
STOCK_FEED = 0.20
LEVELS = ("primary", "secondary", "tertiary")
CROSS_BARS = (0.25, 0.50, 0.90)
CENSORED_YEAR = float(COHORTS + 1)   # reported as ">COHORTS", never as a number

# Exactly one factor moves per arm: the per-level capacity multiplier.
ARMS_7 = {
    "control":        (1.0, 1.0, 1.0),
    "primary_only":   (2.0, 1.0, 1.0),
    "secondary_only": (1.0, 2.0, 1.0),
    "tertiary_only":  (1.0, 1.0, 2.0),
    "all_levels":     (2.0, 2.0, 2.0),
}


def draw_level_case(seed, t):
    """Latent draws for one (seed, cohort). Independent of arm by construction."""
    rng = random.Random(seed * 1000 + t)
    group = [i % 3 for i in range(N)]
    cash = [CASH_GROUP[g] + rng.uniform(0.0, CASH_DRAW) for g in group]
    aptitude = [rng.random() for _ in group]
    ready = [[rng.random() for _ in group] for _ in range(3)]
    lottery = list(range(N))
    rng.shuffle(lottery)
    return {"cash": cash, "aptitude": aptitude, "ready": ready, "lottery": lottery}


def seats_at(level, t, mult):
    """Installed places at cohort index t (0-based); four-cohort ramp, permanent."""
    phase = min(1.0, t / SEAT_RAMP)
    return int(round(BASE_SEATS[level] * (1.0 + (mult - 1.0) * phase)))


def run_level_capacity(seed, arm):
    """Run 30 cohorts for one arm. Returns per-cohort rows (one dict per cohort)."""
    if arm not in ARMS_7:
        raise ValueError(arm)
    mult = ARMS_7[arm]
    stock = [0.0, 0.0, 0.0]
    history = []
    for t in range(COHORTS):
        draws = draw_level_case(seed, t)
        cash, aptitude, ready, lottery = (draws["cash"], draws["aptitude"],
                                          draws["ready"], draws["lottery"])
        seats = [seats_at(k, t, mult[k]) for k in range(3)]
        stage = [0] * N
        row = {"cohort": t + 1}
        for k in range(3):
            gate = GATE[k]
            eligible = [i for i in lottery if stage[i] == k]
            applicants = [i for i in eligible
                          if cash[i] >= FEE[k]
                          and ready[k][i] + APT_W * aptitude[i] + STOCK_W * stock[k] >= gate]
            admitted = applicants[:seats[k]]
            for i in admitted:
                stage[i] = k + 1
            row[k] = {"eligible": len(eligible), "applications": len(applicants),
                      "seats": seats[k], "completions": len(admitted)}
            assert len(admitted) <= min(seats[k], len(applicants)) <= len(eligible)
        for k in range(3):
            stock[k] = STOCK_KEEP * stock[k] + STOCK_FEED * (row[k]["completions"] / N)
        history.append(row)
    return history


def crossing_year(history, level, bar):
    """First 1-based cohort with completion share >= bar, else CENSORED_YEAR."""
    for row in history:
        if row[level]["completions"] / N >= bar:
            return float(row["cohort"])
    return CENSORED_YEAR


def level_seed_metrics(history):
    """Per-seed scalar metrics for experiment 7 (final cohort + crossings)."""
    last = history[-1]
    out = {}
    for k in range(3):
        name = LEVELS[k]
        out[f"seats_{name}"] = float(last[k]["seats"])
        out[f"applications_{name}"] = float(last[k]["applications"])
        out[f"completions_{name}"] = float(last[k]["completions"])
        seats = last[k]["seats"]
        out[f"utilization_{name}"] = (last[k]["completions"] / seats) if seats else 0.0
        out[f"share_{name}_pp"] = 100.0 * last[k]["completions"] / N
    floor = out["share_primary_pp"]
    ceiling = out["share_tertiary_pp"]
    out["floor_pp"] = floor
    out["middle_pp"] = out["share_secondary_pp"]
    out["ceiling_pp"] = ceiling
    out["floor_minus_ceiling_pp"] = floor - ceiling
    out["ceiling_over_floor"] = (ceiling / floor) if floor > 0 else 0.0
    for k in range(3):
        name = LEVELS[k]
        for bar in CROSS_BARS:
            out[f"cross_{name}_{int(bar * 100)}"] = crossing_year(history, k, bar)
    for t in (4, 9, 29):                     # cohort 5, 10, 30 trajectory points
        for k in range(3):
            out[f"comp_{LEVELS[k]}_t{t + 1}"] = float(history[t][k]["completions"])
    return out


# --------------------------------------------------------------------------
# Experiment 8 — enforcement x compulsory law
# --------------------------------------------------------------------------
ATT_THRESHOLD = 0.55
COMP_THRESHOLD = 0.60
COMP_BASE = 0.02
DELTA_NORM = 0.010      # stipulated norm/announcement effect of the statute itself
ENF_COEF = 0.35         # sanction/verification strength per unit of enforcement
REG_THRESHOLD = 0.70
REG_NORM = 0.10         # register-only effect of a paper law
REG_ENF = 0.30
WORK_RETAIN = 0.60      # share of household work retained while attending

# (law, enforcement) cells; enforcement is declared, not measured.
LAW_CELLS = {
    "no_law":        (0, 0.0),
    "law_e0":        (1, 0.0),
    "law_e05":       (1, 0.5),
    "law_e1":        (1, 1.0),
    "no_law_e05":    (0, 0.5),
    "no_law_e1":     (0, 1.0),
}


def draw_law_case(seed):
    """Latent household draws for experiment 8. Independent of law/enforcement."""
    rng = random.Random(seed * 7919 + 13)
    return {"a": [rng.random() for _ in range(N)],   # base attendance propensity
            "s": [rng.random() for _ in range(N)],   # exposure to inspection/sanction
            "r": [rng.random() for _ in range(N)],   # learning readiness
            "w": [rng.random() for _ in range(N)],   # household work intensity
            "reg0": [rng.random() for _ in range(N)]}  # baseline registration propensity


def run_law(seed, cell):
    """One cohort, one (law, enforcement) cell."""
    if cell not in LAW_CELLS:
        raise ValueError(cell)
    law, enf = LAW_CELLS[cell]
    d = draw_law_case(seed)
    registered = attended = completed = 0
    work_total = 0.0
    sanction_exposure = 0.0
    for i in range(N):
        s = d["s"][i]
        if d["reg0"][i] + law * (REG_NORM + enf * REG_ENF * s) >= REG_THRESHOLD:
            registered += 1
        attends = d["a"][i] + law * (DELTA_NORM + enf * ENF_COEF * s) >= ATT_THRESHOLD
        if attends:
            attended += 1
            # Verified instruction: only enforcement plus law adds learning quality.
            if d["r"][i] + COMP_BASE + law * enf * ENF_COEF * s >= COMP_THRESHOLD:
                completed += 1
        work_total += d["w"][i] * (1.0 - WORK_RETAIN * attends)
        sanction_exposure += law * enf * s
    # Completion is a subset of attendance; registration is a separate gate.
    assert completed <= attended
    assert completed <= N and attended <= N and registered <= N
    return {
        "registration_n": float(registered),
        "attendance_n": float(attended),
        "completion_n": float(completed),
        "registration_pp": 100.0 * registered / N,
        "attendance_pp": 100.0 * attended / N,
        "completion_pp": 100.0 * completed / N,
        "mean_household_work": work_total / N,
        "sanction_exposure": sanction_exposure / N,
    }


# --------------------------------------------------------------------------
# Experiment 9 — buildings vs teachers at equal budget
# --------------------------------------------------------------------------
BUDGET = 480
ROOM_COST = 12          # budget units per physical place
TEACHER_COST = 60       # budget units per teacher post
TEACHER_CAPACITY = 12   # places per effective teacher at full quality
BASE_ROOMS = 30
BASE_POSTS = 2
Q_BASE = 0.92           # completion pass rate at load <= TEACHER_CAPACITY
Q_FLOOR = 0.55
Q_SLOPE = 0.04
RETENTION = {"low": 0.60, "high": 0.90}
ALLOC = {"baseline": (0, 0), "rooms_only": (40, 0),
         "teachers_only": (0, 8), "split": (20, 4)}


def draw_budget_case(seed):
    """Latent completion propensities and lottery order; independent of arm."""
    rng = random.Random(seed * 104729 + 7)
    lottery = list(range(N))
    rng.shuffle(lottery)
    return {"pass": [rng.random() for _ in range(N)], "lottery": lottery}


def run_budget(seed, arm, retention):
    """One cohort, one allocation arm at one retention level."""
    if arm not in ALLOC:
        raise ValueError(arm)
    if retention not in RETENTION:
        raise ValueError(retention)
    rooms_add, posts_add = ALLOC[arm]
    pi = RETENTION[retention]
    physical = BASE_ROOMS + rooms_add
    posts = BASE_POSTS + posts_add
    eff_teachers = posts * pi
    teacher_capacity = int(eff_teachers * TEACHER_CAPACITY + 1e-9)
    admissions = min(physical, teacher_capacity, N)
    load = admissions / eff_teachers
    q = Q_BASE if load <= TEACHER_CAPACITY else max(Q_FLOOR, Q_BASE - Q_SLOPE * (load - TEACHER_CAPACITY))
    d = draw_budget_case(seed)
    completions = sum(1 for i in d["lottery"][:admissions] if d["pass"][i] <= q)
    spent = rooms_add * ROOM_COST + posts_add * TEACHER_COST
    # Equal-budget invariant: every purchase arm spends exactly B; baseline spends 0.
    assert spent == BUDGET if arm != "baseline" else spent == 0, (arm, spent)
    assert admissions <= min(physical, N)
    assert completions <= admissions
    return {
        "physical_places": float(physical),
        "admissions_staffed": float(admissions),
        "completions_n": float(completions),
        "completion_pp": 100.0 * completions / N,
        "ptr_declared": admissions / posts,
        "ptr_effective": admissions / eff_teachers,
        "teacher_load": load,
        "budget_spent": float(spent),
        "rooms_added": float(rooms_add),
        "posts_added": float(posts_add),
    }
