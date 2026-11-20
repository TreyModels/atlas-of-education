"""Experiment 6 — Eligibility repeal vs blind ranking, Cluster B.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

Spec: extensions_archive/codex_2026-11-20/COUNCIL_TOY_SPECS_015.md, Cluster B #6
("Luna item 5 toy: credential visible at ranking x gate repealed; blind ranking x
gate retained; both. Arms: 2x2"). Explicitly a staged screening toy, not an
equilibrium vacancy test.

Stipulated rules:
  * 100 applicants, J_OFFERS = 35 offers. Credential status is a stipulation,
    independent of true skill (a pure signal with no productivity content).
    Two credential-share regimes are run to test whether the verdict depends on
    the credentialed share: MAIN c = 45 credentialed / 55 uncredentialed, and
    SENSITIVITY c = 25 / 75 (credentialed supply below the offer count).
  * Stage 1 (the gate): if the gate is RETAINED, only credentialed applicants
    are eligible and uncredentialed applications are screened out before
    ranking. If the gate is REPEALED, all 100 enter the ranking.
  * Stage 2 (ranking): if the credential is VISIBLE, credentialed applicants are
    ranked ahead of uncredentialed ones, then by true skill; if ranking is
    BLIND, all eligible applicants are ranked by true skill only. Ties by a
    common lottery order.
  * Offers go to the top J_OFFERS eligible applicants; if fewer than J_OFFERS
    are eligible, the remainder are unfilled vacancies (recorded).

Estimands per cell (per seed): offer rate among uncredentialed applicants and
the counts of uncredentialed / credentialed / total offers, vacancies, and mean
true skill of offerees.
"""
from toy_common import POPULATION, cohort, arm_name

EXPERIMENT = "exp6_eligibility_vs_blind_ranking"
J_OFFERS = 35
CRED_SHARES = (45, 25)   # main, sensitivity


def draw(seed):
    """Latent draws shared by every arm and both credential-share regimes."""
    c = cohort(seed)          # skill + lottery order
    import random
    rng = random.Random(seed * 999983 + 11)
    perm = list(range(POPULATION))
    rng.shuffle(perm)
    return {"skill": c["skill"], "lottery": c["lottery"],
            "rank_pos": c["rank_pos"], "cred_perm": perm}


def cell(cred_share, visible, gate_repealed, seed):
    d = draw(seed)
    skill, rank_pos = d["skill"], d["rank_pos"]
    credentialed = set(d["cred_perm"][:cred_share])

    eligible = [i for i in range(POPULATION)
                if (gate_repealed or i in credentialed)]
    if visible:
        order = sorted(eligible, key=lambda i: (i not in credentialed, -skill[i], rank_pos[i]))
    else:
        order = sorted(eligible, key=lambda i: (-skill[i], rank_pos[i]))
    offers = order[:J_OFFERS]
    offer_set = set(offers)

    n_uncred = POPULATION - cred_share
    uncred = [i for i in range(POPULATION) if i not in credentialed]
    off_uncred = sum(i in offer_set for i in uncred)
    off_cred = len(offers) - off_uncred
    return {
        "uncred_offers": off_uncred,
        "cred_offers": off_cred,
        "total_offers": len(offers),
        "uncred_offer_rate": off_uncred / n_uncred,
        "offer_skill_mean": (sum(skill[i] for i in offers) / len(offers)) if offers else None,
        "vacancies": J_OFFERS - len(offers),
        "eligible_count": len(eligible),
        "credentialed_count": cred_share,
        "uncredentialed_count": n_uncred,
    }


def arms():
    out = []
    for cred_share in CRED_SHARES:
        for visible in (True, False):
            for gate_repealed in (True, False):
                name = arm_name(
                    f"c{cred_share}",
                    "visible_credential" if visible else "blind_ranking",
                    "gate_repealed" if gate_repealed else "gate_retained",
                )
                out.append((cred_share, visible, gate_repealed, name))
    return out


def run(seeds):
    rows = []
    for seed in seeds:
        for cred_share, visible, gate_repealed, name in arms():
            out = cell(cred_share, visible, gate_repealed, seed)
            for metric, value in out.items():
                rows.append({"experiment": EXPERIMENT, "arm": name, "seed": seed,
                             "metric": metric, "value": value})
    return rows


METRICS = ["uncred_offers", "cred_offers", "total_offers", "uncred_offer_rate",
           "offer_skill_mean", "vacancies", "eligible_count"]
