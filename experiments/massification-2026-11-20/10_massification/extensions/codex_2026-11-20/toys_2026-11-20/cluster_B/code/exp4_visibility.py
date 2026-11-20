"""Experiment 4 — Visibility x mechanism (HC vs signalling), Cluster B.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

Spec: extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md, Cluster B #4.

Stipulated rules (one-factor shock = visibility v; mechanism is the second arm):
  * A private/public admissions market exactly as model.py: common lottery for
    PUBLIC_SEATS=30 public seats, fee-paying private overflow up to
    PRIVATE_CAPACITY=30 with a fixed cost / break-even rule, TUITION=2.
  * Subjective value of a degree before fees = GROSS_PREMIUM(4) - opportunity
    cost, under both mechanisms at v=0 (this is why the arms start identical).
  * human_capital: every graduate gains +1.0 true skill unit; the degree
    premium is 4.0 at every v (the premium is the return to real skill).
  * signaling: graduates gain no skill; the degree premium is 4.0*(1-v), so
    the market for degrees shrinks to nothing at v=1.
  * Employer score = v*true_skill + (1-v)*credential. At v=0 the employer sees
    only the credential; at v=1 only measured skill. Hires are the top JOBS=40
    by score, ties broken by the lottery order (same stable-sort as model.py).

Estimands per cell (per seed):
  applications            applicant count
  admissions              public + private admissions
  graduate_hires          hires holding the degree
  output_true_hires       mean TRUE skill of hires (real productivity)
  output_valued_hires     mean EMPLOYER-ASSESSED score of hires
                          (v*skill + (1-v)*credential: a stipulated valuation)
  rejected_skill          mean true skill of applicants who were not hired
                          (empty when every applicant was hired)
  rejected_count          number of applicants not hired
"""
from toy_common import (
    POPULATION, JOBS, PUBLIC_SEATS, PUBLIC_FEE, PRIVATE_CAPACITY,
    PRIVATE_FIXED_COST, PRIVATE_SEAT_COST, TUITION, GROSS_PREMIUM,
    cohort, arm_name,
)

EXPERIMENT = "exp4_visibility_mechanism"
MECHANISMS = ("human_capital", "signaling")
VISIBILITIES = (0.0, 0.5, 1.0)


def cell(mechanism, visibility, seed):
    """One arm x one seed. Pure function of the latent draw."""
    if mechanism not in MECHANISMS:
        raise ValueError(mechanism)
    if visibility not in VISIBILITIES:
        raise ValueError(visibility)
    c = cohort(seed)
    budgets, base_skill, costs, lottery = c["budgets"], c["skill"], c["costs"], c["lottery"]
    signal_weight = 1.0 - visibility
    premium = GROSS_PREMIUM if mechanism == "human_capital" else GROSS_PREMIUM * signal_weight

    applicants = [i for i in lottery if premium - costs[i] >= PUBLIC_FEE]
    public = applicants[:PUBLIC_SEATS]
    waiting = applicants[PUBLIC_SEATS:]
    customers = [i for i in waiting
                 if TUITION <= budgets[i] and premium - costs[i] >= TUITION]
    qty = min(PRIVATE_CAPACITY, len(customers))
    enters = qty * (TUITION - PRIVATE_SEAT_COST) >= PRIVATE_FIXED_COST
    private = customers[:qty] if enters else []
    graduates = set(public) | set(private)

    skill = [s + (1.0 if (i in graduates and mechanism == "human_capital") else 0.0)
             for i, s in enumerate(base_skill)]
    score = [visibility * skill[i] + signal_weight * (1.0 if i in graduates else 0.0)
             for i in range(POPULATION)]
    hired = sorted(lottery, key=score.__getitem__, reverse=True)[:JOBS]
    hired_set = set(hired)
    rejected = [i for i in applicants if i not in hired_set]

    return {
        "applications": len(applicants),
        "admissions": len(graduates),
        "public_admissions": len(public),
        "private_admissions": len(private),
        "graduate_hires": sum(i in graduates for i in hired),
        "applicant_hires": sum(i in hired_set for i in applicants),
        "output_true_hires": sum(skill[i] for i in hired) / len(hired),
        "output_valued_hires": sum(score[i] for i in hired) / len(hired),
        "rejected_count": len(rejected),
        "rejected_skill": (sum(skill[i] for i in rejected) / len(rejected)) if rejected else None,
    }


def arms():
    return [(m, v, arm_name(m, f"v{v:.1f}")) for m in MECHANISMS for v in VISIBILITIES]


def run(seeds):
    rows = []
    for seed in seeds:
        for mechanism, visibility, name in arms():
            out = cell(mechanism, visibility, seed)
            for metric, value in out.items():
                rows.append({"experiment": EXPERIMENT, "arm": name, "seed": seed,
                             "metric": metric, "value": value})
    return rows


METRICS = ["applications", "admissions", "public_admissions", "private_admissions",
           "graduate_hires", "applicant_hires", "output_true_hires", "output_valued_hires",
           "rejected_count", "rejected_skill"]
