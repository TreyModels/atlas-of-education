"""Experiment 5 — Queue vs human capital under fixed jobs, Cluster B.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

Spec: extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md, Cluster B #5.

Stipulated rules:
  * Population of 100. A FIXED older-diploma group O = indices 0..19 (fixed
    membership at every seed, never re-drawn). Young applicants = indices
    20..99. The 20 people the policy "upgrades" are the fixed young set
    T = indices 20..39, identical latent people in every arm (paired).
  * The job count is one-factor-exogenous: fixed regime J = J0, with J0 drawn
    uniformly on {35,36,37,38,39,40} once per seed and used by BOTH fixed-job
    arms (jobs fixed at 35-40 per the spec). Responsive regime J = 100: the job
    pool absorbs the whole queue (maximum responsiveness; every applicant is
    hired). J is not a function of any arm outcome.
  * Allocation rules (the only thing that differs between skill and rank arms):
      - skill_upgrade: the 20 treated people get +1.0 TRUE skill and nothing
        else. Hiring is by true skill, descending (ties by lottery order).
      - rank_upgrade: the 20 treated people get queue priority (a new
        credential that outranks the older diploma), with NO skill change.
        Hiring order is: treated (lottery order), then the other 60 young by
        skill, then the 20 older-diploma holders by skill. This is a
        credential-inflation queue: the new credential outranks the old one, so
        the older-diploma group is ranked last.
      - reference (no treatment): hiring by true skill, descending.
  * These rules are stipulations chosen to make the queue-vs-skill contrast
    legible; the toy cannot test whether any real labour market looks like this.

Estimands per cell (per seed): hires of the fixed older-diploma group, output
among hires (mean TRUE skill of hires), total hires, treated-group hires, and
the population mean skill used for the decomposition diagnostic.
"""
from toy_common import POPULATION, cohort, arm_name

EXPERIMENT = "exp5_queue_vs_human_capital"

OLDER = tuple(range(0, 20))          # fixed older-diploma group
TREATED = tuple(range(20, 40))       # fixed 20 young people the policy upgrades
YOUNG = tuple(range(20, POPULATION))


def job_count(seed):
    """J0 on {35,...,40}; deterministic per seed, independent of any arm."""
    import random
    return random.Random(seed * 1000003 + 7).randint(35, 40)


def cell(treatment, jobs_regime, seed):
    c = cohort(seed)
    base_skill, lottery = c["skill"], c["lottery"]
    rank_pos = c["rank_pos"]
    j0 = job_count(seed)
    j = j0 if jobs_regime == "fixed_jobs" else POPULATION

    skill = list(base_skill)
    if treatment == "skill_upgrade":
        for i in TREATED:
            skill[i] += 1.0

    if treatment == "rank_upgrade":
        treated_order = sorted(TREATED, key=rank_pos.__getitem__)
        rest_young = sorted((i for i in YOUNG if i not in TREATED),
                            key=lambda i: (-skill[i], rank_pos[i]))
        older_order = sorted(OLDER, key=lambda i: (-skill[i], rank_pos[i]))
        order = treated_order + rest_young + older_order
    else:
        order = sorted(range(POPULATION), key=lambda i: (-skill[i], rank_pos[i]))

    hired = order[:j]
    hired_set = set(hired)
    older_hires = sum(i in OLDER for i in hired)
    treated_hires = sum(i in TREATED for i in hired)
    return {
        "older_group_hires": older_hires,
        "treated_group_hires": treated_hires,
        "total_hires": len(hired),
        "output_hires": sum(skill[i] for i in hired) / len(hired),
        "population_mean_skill": sum(skill) / POPULATION,
        "job_count": len(hired),
    }


def arms():
    out = []
    for treatment in ("skill_upgrade", "rank_upgrade"):
        for regime in ("fixed_jobs", "responsive_jobs"):
            out.append((treatment, regime, arm_name(treatment, regime)))
    for regime in ("fixed_jobs", "responsive_jobs"):
        out.append(("reference", regime, arm_name("reference_no_treatment", regime)))
    return out


def run(seeds):
    rows = []
    for seed in seeds:
        for treatment, regime, name in arms():
            out = cell(treatment, regime, seed)
            for metric, value in out.items():
                rows.append({"experiment": EXPERIMENT, "arm": name, "seed": seed,
                             "metric": metric, "value": value})
    return rows


METRICS = ["older_group_hires", "treated_group_hires", "total_hires",
           "output_hires", "population_mean_skill", "job_count"]
