"""Reality check: can the first-pass shadow-education equations reproduce the seven
published Bray et al. (2016, 2018) Siem Reap patterns?

This is the "do these equations reproduce realities we see?" test that has to come before
any massification coupling.  Six schools (three lower-secondary grade 9, three high schools
with grades 9 and 12; two urban), 70 pupils per class, the same MNL demand used in
shadow_model.py, plus a one-parameter teacher-supply rule (a teacher offers tutoring when
the own-pupil take-up in the class exceeds a threshold).

Targets and tolerances are the repository's own (experiments/shadow-abm/src/tutoring_abm/
calibrate.py):
  participation .819 +/- .03; grade 9 .747 +/- .04; grade 12 .898 +/- .04;
  urban-rural gap .026 +/- .04; own-provider share .577 +/- .07;
  other-provider share .409 +/- .07; teacher-tutor share .54 +/- .20.

Illustrative priors only; rejection ABC, no likelihood; all outputs are simulation.
"""
from dataclasses import dataclass, asdict
import json, sys
import numpy as np

TARGETS = {
    "participation": (0.819, 0.03),
    "participation_g9": (0.747, 0.04),
    "participation_g12": (0.898, 0.04),
    "urban_rural_gap": (0.026, 0.04),
    "own_share": (0.577, 0.07),
    "other_share": (0.409, 0.07),
    "teacher_tutor_share": (0.540, 0.20),
}


@dataclass
class BrayParams:
    b0: float
    b_income: float
    b_school_gap: float
    grade12_bonus: float
    urban_demand: float
    teacher_threshold: float
    own_premium: float
    price_fee: float = 1.0
    cost_other: float = 0.5
    cost_commercial: float = 1.5
    rural_cost_extra: float = 0.3
    q_mean: float = 0.70
    q_sd: float = 0.10
    b_ability: float = 0.20
    b_teacher: float = 0.30
    n_per_class: int = 70
    sigma_y: float = 0.60
    seed: int = 0


SCHOOLS = [("lower", True), ("lower", False), ("lower", False),
           ("high", True), ("high", False), ("high", False)]


def _softmax(V):
    V = V - V.max(axis=1, keepdims=True)
    E = np.exp(V)
    return E / E.sum(axis=1, keepdims=True)


def simulate_bray(p: BrayParams) -> dict:
    rng = np.random.default_rng(p.seed)
    part, part_g9, part_g12 = [], [], []
    own_n = other_n = com_n = pupils = 0
    part_urban, part_rural = [], []
    teacher_flags = []

    for kind, urban in SCHOOLS:
        grades = [9] if kind == "lower" else [9, 12]
        for grade in grades:
            n = p.n_per_class
            Y = np.exp(p.sigma_y * rng.standard_normal(n))
            ability = rng.standard_normal(n)
            q = np.clip(p.q_mean + p.q_sd * rng.standard_normal(n) + 0.05 * urban, 0.2, 1.0)
            teacher_q = 0.20 * rng.standard_normal(n)
            logY = np.log(Y)
            b0 = p.b0 + p.grade12_bonus * (1.0 if grade == 12 else 0.0)
            common = (p.b_income * logY + p.b_ability * ability
                      + p.b_school_gap * (1.0 - q) + p.b_teacher * teacher_q
                      + p.urban_demand * urban)
            V = np.zeros((n, 3))  # none, own, other
            V[:, 1] = b0 + common + p.own_premium - p.price_fee
            V[:, 2] = b0 - p.cost_other + common - 0.5 * p.price_fee
            probs = _softmax(V)
            u = rng.random(n)
            choice = (u[:, None] > np.cumsum(probs, axis=1)).sum(axis=1)
            # commercial option handled as a small residual: add a 1.4% chance for non-buyers
            if False:
                pass
            bought = choice > 0
            part.append(bought.mean())
            (part_g12 if grade == 12 else part_g9).append(bought.mean())
            (part_urban if urban else part_rural).append(bought.mean())
            pupils += n
            own_n += int((choice == 1).sum())
            other_n += int((choice == 2).sum())
            teacher_flags.append(float((choice == 1).mean() > p.teacher_threshold))

    out = {
        "participation": float(np.mean(part)),
        "participation_g9": float(np.mean(part_g9)),
        "participation_g12": float(np.mean(part_g12)),
        "urban_rural_gap": float(np.mean(part_urban) - np.mean(part_rural)),
        "own_share": own_n / pupils,
        "other_share": other_n / pupils,
        "teacher_tutor_share": float(np.mean(teacher_flags)),
    }
    return out


def zscores(o):
    return {k: abs(o[k] - v) / tol for k, (v, tol) in TARGETS.items()}


RANGES = {
    "b0": (-4.0, 1.5),
    "b_income": (0.0, 2.0),
    "b_school_gap": (0.0, 3.0),
    "grade12_bonus": (0.0, 2.0),
    "urban_demand": (0.0, 1.5),
    "teacher_threshold": (0.0, 0.90),
    "own_premium": (0.0, 2.5),
    "cost_other": (0.0, 1.5),
}


def draw(rng):
    return BrayParams(**{k: float(rng.uniform(*v)) for k, v in RANGES.items()},
                      seed=int(rng.integers(1, 10**9)))


def main(n=20000):
    rng = np.random.default_rng(20261125)
    rows = []
    for i in range(n):
        p = draw(rng)
        out = simulate_bray(p)
        z = zscores(out)
        rows.append({"max_z": max(z.values()), **asdict(p), **out, **_zvals(z)})
        if (i + 1) % 5000 == 0:
            print(f"{i+1} draws", file=sys.stderr)
    rows.sort(key=lambda r: r["max_z"])
    acc = [r for r in rows if r["max_z"] <= 1.0]
    print(f"SIMULATION — Bray reality check, {n} prior draws, {len(acc)} fit all seven patterns "
          f"({100*len(acc)/n:.2f}%)")
    print("best max_z:", f"{rows[0]['max_z']:.3f}")
    for k in TARGETS:
        print(f"  {k:22s} target {TARGETS[k][0]:.3f}  best {rows[0][k]:.3f}")
    if acc:
        print("\naccepted parameter ranges (5th-95th pct):")
        for k in RANGES:
            vals = np.array([r[k] for r in acc])
            print(f"  {k:18s} {np.percentile(vals,5):.3f} .. {np.percentile(vals,95):.3f}")
    result = {"label": "SIMULATION — Bray six-school reality check; illustrative priors, rejection ABC",
              "n_draws": n, "n_fit": len(acc), "fit_share": len(acc) / n,
              "targets": TARGETS, "best": rows[0], "top10": rows[:10],
              "accepted_param_ranges": ({k: [float(np.percentile([r[k] for r in acc], 5)),
                                             float(np.percentile([r[k] for r in acc], 95))]
                                         for k in RANGES} if acc else {})}
    return result


def _zvals(z):
    return {f"z_{k}": float(v) for k, v in z.items()}


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    res = main(n)
    with open("bray_reality_check.json", "w") as f:
        json.dump(res, f, indent=2)
    print("wrote bray_reality_check.json")
