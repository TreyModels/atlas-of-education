"""Experiment 13 - Migration and remittance route (Cluster E). Stdlib only.

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence.

Question (COUNCIL_TOY_SPECS_015 #13): can an external credentialed job route pull
origin schooling while local jobs stay flat, and do remittances add a smaller
effect?  Model base: model.py / takeoff.py demand-and-fee logic.

Rules (all stipulated, all imposed):
  * N=200 origin households re-exposed for T=20 school cycles (the repeated-latent-
    cohort design of experiments.py: the same households are re-exposed, so arms
    are paired and changes are within-household, not fresh sampling).
  * Latents (cash b, opportunity cost c, aptitude a, route access r, kin remittance
    link) are drawn ONCE per seed and shared by every arm.
  * Secondary application requires BOTH
      (i) net credential value v_i - c_i >= FEE, and
      (ii) household cash plus remittances b_i + R_i >= FEE + INDIRECT (attendance
           cash cost).
  * v_i = V0 + APT_VALUE*a_i + route_open*PREMIUM_MULT*ROUTE_PREMIUM*r_i.
    The route therefore acts on DEMAND / willingness to pay, not on local jobs.
  * Origin seats are deliberately set ABOVE peak demand (170 of 200) so that the
    estimand isolates the demand channel. STATED STIPULATION: with binding origin
    seats the schooling response would be capped by capacity, as the Cluster C
    toys show; this toy says nothing about which regime obtains.
  * Remittances: R_i = remit_on * REMIT_AMOUNT * kin_i * min(1, M_prev/40), where
    M_prev is the migrant count in the previous cycle. A diaspora of 20 migrants
    exists at t=0 so that the closed-route/remittance-on cell is not empty.
  * Migration: completers with route access migrate with p = 0.55 + 0.25*a_i, only
    when the route is open. Migrant count is reported as UNIQUE PERSONS ever
    migrating ("counted once") plus the per-cycle flow.
  * Local formal jobs: a FIXED 45 posts in every arm and every cycle, allocated
    among non-migrants to completers first then by aptitude. Local labour demand
    is flat by construction, so no schooling response can be a local-jobs response.
    Local OUTPUT can still move through who is hired (migrant selection); that is
    reported and has a predeclared expected sign (down) but no pass/fail threshold.

Arms: route {closed, open} x remittances {off, on} = 4 cells, paired within seed.
Sensitivity (auxiliary, no threshold test): route premium halved (PREMIUM_MULT=.5),
route open vs closed, remittances off.
"""
import random

from common import LABEL, row, verdict

EXPERIMENT = "E13_migration_remittance"

N = 200
T = 20
SEATS_ORIGIN = 170          # stipulated non-binding (max applications ~150)
FEE = 1.0                   # secondary fee (model.py public fee)
INDIRECT = 0.8              # uniforms/transport, paid in cash
V0 = 2.6                    # base demand for the credential
APT_VALUE = 0.6
ROUTE_PREMIUM = 2.4         # external credentialed-route premium in value units
ROUTE_ACCESS_P = 0.45
REMIT_AMOUNT = 0.8
KIN_P = 0.35
M_REF = 40.0
DIASPORA = 20
LOCAL_JOBS = 45
P_COMPLETE_BASE = 0.82
P_COMPLETE_APT = 0.12
P_MIGRATE_BASE = 0.55
P_MIGRATE_APT = 0.25

ARMS = [("closed", 0), ("closed", 1), ("open", 0), ("open", 1)]
ARM_LABEL = {("closed", 0): "route=closed|remit=off",
             ("closed", 1): "route=closed|remit=on",
             ("open", 0): "route=open|remit=off",
             ("open", 1): "route=open|remit=on"}


def draw(seed):
    """All latent draws for one paired cohort. Shared verbatim across arms."""
    rng = random.Random(seed * 7919 + 13)
    b = [1.5 + 2.0 * rng.random() for _ in range(N)]          # household cash
    c = [3.5 * rng.random() for _ in range(N)]                # opportunity cost
    a = [rng.random() for _ in range(N)]                      # aptitude
    r = [1 if rng.random() < ROUTE_ACCESS_P else 0 for _ in range(N)]
    kin = [1 if rng.random() < KIN_P else 0 for _ in range(N)]
    comp_u = [[rng.random() for _ in range(N)] for _ in range(T)]
    mig_u = [[rng.random() for _ in range(N)] for _ in range(T)]
    order = []
    for _ in range(T):
        o = list(range(N))
        rng.shuffle(o)
        order.append(o)
    return dict(b=b, c=c, a=a, r=r, kin=kin, comp_u=comp_u, mig_u=mig_u,
                order=order)


def diaspora_ids(lat):
    """20 pre-existing migrants, all with route access; arm-independent."""
    return [i for i in range(N) if lat["r"][i]][:DIASPORA]


def simulate(lat, route_open, remit_on, premium_mult=1.0):
    """Run T cycles and return per-seed metrics (means over cycles unless noted)."""
    b, c, a, r, kin = lat["b"], lat["c"], lat["a"], lat["r"], lat["kin"]
    premium = ROUTE_PREMIUM * premium_mult if route_open else 0.0
    value = [V0 + APT_VALUE * a[i] + premium * r[i] for i in range(N)]
    value_ok = [value[i] - c[i] >= FEE for i in range(N)]

    migrants = set(diaspora_ids(lat))
    ever = set(migrants)
    sum_apps = sum_adm = sum_comp = sum_migflow = 0
    sum_remit = sum_resources = 0.0
    sum_output = 0.0
    final_comp = 0

    for t in range(T):
        m_prev = len(migrants)
        scale = min(1.0, m_prev / M_REF)
        remit = [(remit_on * REMIT_AMOUNT * kin[i] * scale) for i in range(N)]
        order = lat["order"][t]
        applicants = [i for i in order if value_ok[i] and b[i] + remit[i] >= FEE + INDIRECT]
        admitted = applicants[:SEATS_ORIGIN]
        adm_set = set(admitted)
        cu = lat["comp_u"][t]
        completers = [i for i in admitted
                      if cu[i] < P_COMPLETE_BASE + P_COMPLETE_APT * a[i]]
        comp_set = set(completers)

        migrated_now = []
        if route_open:
            mu = lat["mig_u"][t]
            for i in completers:
                if r[i] and mu[i] < P_MIGRATE_BASE + P_MIGRATE_APT * a[i]:
                    migrated_now.append(i)
            migrants.update(migrated_now)
            ever.update(migrated_now)

        # Local formal jobs: fixed 45 posts, completers first, then aptitude.
        non_migrants = [i for i in order if i not in migrants]
        non_migrants.sort(key=lambda i: (i in comp_set, a[i]), reverse=True)
        hires = non_migrants[:LOCAL_JOBS]
        output = sum(1.0 + 0.18 * (1 if i in comp_set else 0)
                     + 0.45 * (1 if i in comp_set else 0) for i in hires)

        sum_apps += len(applicants)
        sum_adm += len(admitted)
        sum_comp += len(completers)
        sum_migflow += len(migrated_now)
        sum_remit += sum(remit)
        sum_resources += sum(b[i] + remit[i] for i in range(N))
        sum_output += output
        final_comp = len(completers)

    return dict(
        apps_per_cycle=sum_apps / T,
        app_rate_pp=100.0 * sum_apps / T / N,
        adm_per_cycle=sum_adm / T,
        comp_per_cycle=sum_comp / T,
        completion_rate_pp=100.0 * sum_comp / T / N,
        completion_rate_final_pp=100.0 * final_comp / N,
        unique_migrants=float(len(ever)),
        migrant_flow_per_cycle=sum_migflow / T,
        remit_income_per_hh=sum_remit / T / N,
        household_resources=sum_resources / T / N,
        local_jobs_filled=float(LOCAL_JOBS),
        local_output_per_cycle=sum_output / T,
    )


METRICS = [
    ("apps_per_cycle", "persons", "Applications per school cycle; origin secondary applicants (value and cash conditions met)."),
    ("app_rate_pp", "pp of cohort", "Applications as a percentage of the 200-household cohort."),
    ("adm_per_cycle", "persons", "Admissions per cycle; capped by the stipulated 170 origin seats."),
    ("comp_per_cycle", "persons", "Secondary completions per cycle (admitted x completion draw)."),
    ("completion_rate_pp", "pp of cohort", "Secondary completions as a percentage of the cohort, averaged over cycles."),
    ("completion_rate_final_pp", "pp of cohort", "Secondary completion rate in the final cycle."),
    ("unique_migrants", "persons", "Migrants counted ONCE: unique persons who ever migrated over the horizon."),
    ("migrant_flow_per_cycle", "persons/cycle", "New migrants per cycle (flow, not deduplicated)."),
    ("remit_income_per_hh", "cash units", "Remittance income received per household per cycle."),
    ("household_resources", "cash units", "Mean household cash plus remittances per cycle."),
    ("local_jobs_filled", "posts", "Local formal posts filled; stipulated constant 45 in every arm."),
    ("local_output_per_cycle", "output units", "Local output from the 45 fixed posts (completer premium); migrant selection can lower it."),
]


def run(seeds):
    results = {arm: {m: [] for m, _, _ in METRICS} for arm in ARMS}
    sens = {m: [] for m, _, _ in METRICS}

    for seed in seeds:
        lat = draw(seed)
        for arm in ARMS:
            out = simulate(lat, route_open=(arm[0] == "open"), remit_on=bool(arm[1]))
            for m, _, _ in METRICS:
                results[arm][m].append(out[m])
        out = simulate(lat, route_open=True, remit_on=False, premium_mult=0.5)
        for m, _, _ in METRICS:
            sens[m].append(out[m])

    rows = []
    for arm in ARMS:
        for m, unit, definition in METRICS:
            rows.append(row(EXPERIMENT, ARM_LABEL[arm], "", m, "all", results[arm][m],
                            unit, definition))

    def contrast(name, left, right, metrics, definition_of):
        for m in metrics:
            xs = [results[left][m][k] - results[right][m][k] for k in range(len(seeds))]
            unit = dict((mm, u) for mm, u, _ in METRICS)[m]
            rows.append(row(EXPERIMENT, ARM_LABEL[left], f"minus {ARM_LABEL[right]}",
                            m, "all", xs, unit, definition_of(left, right, m)))

    route_m = ["apps_per_cycle", "app_rate_pp", "comp_per_cycle", "completion_rate_pp",
               "unique_migrants", "local_jobs_filled", "local_output_per_cycle"]
    contrast("route_effect", ("open", 0), ("closed", 0), route_m,
             lambda l, r, m: f"Paired within-seed difference ({ARM_LABEL[l]} minus {ARM_LABEL[r]}) for {m}.")
    contrast("remit_effect_open", ("open", 1), ("open", 0),
             ["apps_per_cycle", "app_rate_pp", "comp_per_cycle", "completion_rate_pp",
              "remit_income_per_hh", "household_resources"],
             lambda l, r, m: f"Paired within-seed difference ({ARM_LABEL[l]} minus {ARM_LABEL[r]}) for {m}.")
    contrast("remit_effect_closed", ("closed", 1), ("closed", 0),
             ["apps_per_cycle", "app_rate_pp", "comp_per_cycle", "completion_rate_pp",
              "remit_income_per_hh", "household_resources"],
             lambda l, r, m: f"Paired within-seed difference ({ARM_LABEL[l]} minus {ARM_LABEL[r]}) for {m}.")
    contrast("joint_vs_control", ("open", 1), ("closed", 0),
             ["apps_per_cycle", "comp_per_cycle", "completion_rate_pp", "unique_migrants",
              "household_resources"],
             lambda l, r, m: f"Paired within-seed difference ({ARM_LABEL[l]} minus {ARM_LABEL[r]}) for {m}.")

    # Auxiliary sensitivity: no threshold test, sign of the route effect only.
    for m in ["apps_per_cycle", "completion_rate_pp", "unique_migrants"]:
        xs = [sens[m][k] - results[("closed", 0)][m][k] for k in range(len(seeds))]
        rows.append(row(EXPERIMENT, "route=open|premium=half|remit=off",
                        "minus route=closed|remit=off", m, "sensitivity", xs,
                        dict((mm, u) for mm, u, _ in METRICS)[m],
                        f"Auxiliary sensitivity (NOT a threshold test): route premium halved to {0.5*ROUTE_PREMIUM}; paired difference vs closed/off for {m}."))

    rows.extend(threshold_rows(results, seeds))
    return rows


def threshold_rows(results, seeds):
    """Predeclared thresholds (frozen in PRE_DECLARATIONS.md before the run)."""
    n = len(seeds)
    out = []

    def diffs(left, right, m):
        return [results[left][m][k] - results[right][m][k] for k in range(n)]

    d_remit_apps = diffs(("open", 1), ("open", 0), "apps_per_cycle")
    d_remit_comp = diffs(("open", 1), ("open", 0), "completion_rate_pp")
    d_route_apps = diffs(("open", 0), ("closed", 0), "apps_per_cycle")
    d_route_comp = diffs(("open", 0), ("closed", 0), "completion_rate_pp")
    d_route_mig = diffs(("open", 0), ("closed", 0), "unique_migrants")
    d_jobs_open = diffs(("open", 0), ("closed", 0), "local_jobs_filled")
    d_jobs_remit = diffs(("open", 1), ("open", 0), "local_jobs_filled")

    m1 = sum(d_remit_apps) / n >= 4.0
    m2 = sum(d_remit_comp) / n >= 1.0
    out.append(row(EXPERIMENT, ARM_LABEL[("open", 1)], "minus " + ARM_LABEL[("open", 0)],
                   "threshold_remit_apps", "threshold", d_remit_apps, "persons/cycle",
                   "T13-P1a: remittances (route open) raise applications by >= 4.0 persons per cycle (= +2.0 pp of cohort), declared sign positive.",
                   "T13-P1a", ">= 4.000000", verdict([m1])))
    out.append(row(EXPERIMENT, ARM_LABEL[("open", 1)], "minus " + ARM_LABEL[("open", 0)],
                   "threshold_remit_completion", "threshold", d_remit_comp, "pp of cohort",
                   "T13-P1b: remittances (route open) raise secondary completion by >= 1.0 pp, declared sign positive.",
                   "T13-P1b", ">= 1.000000", verdict([m2])))

    m3 = sum(d_route_comp) / n >= 8.0
    out.append(row(EXPERIMENT, ARM_LABEL[("open", 0)], "minus " + ARM_LABEL[("closed", 0)],
                   "threshold_route_completion", "threshold", d_route_comp, "pp of cohort",
                   "T13-P2: opening the route (remittances off) raises secondary completion by >= 8.0 pp, declared sign positive.",
                   "T13-P2", ">= 8.000000", verdict([m3])))

    m4 = max(abs(x) for x in d_jobs_open + d_jobs_remit) == 0.0
    out.append(row(EXPERIMENT, "all 4 cells", "flat-local-jobs design check", "threshold_local_jobs_flat",
                   "threshold", d_jobs_open, "posts",
                   "T13-P3: local formal posts filled are identical (45) in every arm and every seed: local labour demand is flat by construction, so the schooling response cannot be a local-jobs response.",
                   "T13-P3", "max |difference| = 0", verdict([m4])))

    out.append(row(EXPERIMENT, ARM_LABEL[("open", 0)], "minus " + ARM_LABEL[("closed", 0)],
                   "aux_route_unique_migrants", "auxiliary", d_route_mig, "persons",
                   "Auxiliary (no threshold): migrants counted once rise under the open route (expected positive, mechanism by construction).",
                   "", "", ""))
    out.append(row(EXPERIMENT, ARM_LABEL[("open", 0)], "minus " + ARM_LABEL[("closed", 0)],
                   "aux_route_apps", "auxiliary", d_route_apps, "persons/cycle",
                   "Auxiliary (no threshold): applications rise under the open route.",
                   "", "", ""))

    f1 = not (m3 and sum(d_route_apps) / n >= 2.0 and sum(d_remit_apps) / n > 0)
    out.append(row(EXPERIMENT, "falsifier check", "", "falsifier_13_triggered", "falsifier",
                   [1.0 if f1 else 0.0], "0/1",
                   "F13 falsifier 'no or perverse effect': triggered if the route effect on completion is < 2.0 pp, or the route effect is <= 0, or the remittance application effect is <= 0. 0 = route and remittance channels both operate with the declared positive sign.",
                   "F13", "0 = not triggered", verdict([not f1])))
    return out
