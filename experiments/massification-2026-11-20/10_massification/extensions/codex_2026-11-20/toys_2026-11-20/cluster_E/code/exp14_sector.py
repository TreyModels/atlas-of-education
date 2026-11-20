"""Experiment 14 - Sector-demand shock x field access (Cluster E). Stdlib only.

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence.

Question (COUNCIL_TOY_SPECS_015 #14): does a sector-specific demand shock
reallocate cohorts into the targeted field, or just raise overall enrolment -
and does the reallocation require access to that field?

Rules (all stipulated, all imposed):
  * N=200 school leavers per seed. Two fields: A (targeted credential) and B
    (placebo credential). Latents (aptitude in each field, gate score, cash,
    opportunity cost, lottery order) are drawn ONCE per seed and shared by all
    arms, so every arm is paired with its no-shock baseline.
  * Value of field f to person i: v_if = 1.2 + 1.0*a_if + return_f, where
    return_f = 2.0 plus the 2.5 shock if f is the shocked field. The shock is a
    one-factor change to one field's return only.
  * Each person makes ONE application: to the affordable, value-eligible field
    with the highest net value v_if - c_i.
  * Field ACCESS: open = both fields open to everyone; closed = field A is gated
    to the top 30% of the gate-score distribution (tracking / credential gate),
    field B open. 'Access' is the only factor that changes between access arms.
  * Seats: 150 per field, deliberately ABOVE peak demand (raise of A applications
    under open access is ~150), so that the toy isolates access and demand from
    seat capacity. STATED STIPULATION: with binding field seats the completions
    response would be capped by seats; the seat-filling estimand is reported.
  * Seats filled = admissions = applications per field (seats non-binding).
  * Licensed completers = admissions with p = 0.80 + 0.12*a_if.
  * Vacancy proxy: sector posts = 30 normally, +25 in the shocked sector;
    vacancies = max(0, posts - licensed completers). Illustrative units.

Arms: shock {none, targeted A, placebo B} x access {open, closed} = 6 conditions.
Reported cells are the 4 shock arms; each is paired against its access-matched
no-shock baseline (same seed, identical latent draws).
Sensitivity (auxiliary, no threshold test): gate at 15% instead of 30%.
"""
import random

from common import row, verdict

EXPERIMENT = "E14_sector_shock_field_access"

N = 200
FEE = 1.0
V_BASE = 1.2
APT_VALUE = 1.0
RETURN_BASE = 2.0
SHOCK = 2.5
SEATS = 150
GATE_SHARE = 0.30
POSTS_BASE = 30
POSTS_SHOCK = 25
P_LICENSE_BASE = 0.80
P_LICENSE_APT = 0.12

FIELD_A, FIELD_B = "A", "B"
CONDITIONS = [(shock, access) for access in ("open", "closed")
              for shock in (None, FIELD_A, FIELD_B)]
COND_LABEL = {(None, "open"): "shock=none|access=open",
              (FIELD_A, "open"): "shock=targeted_A|access=open",
              (FIELD_B, "open"): "shock=placebo_B|access=open",
              (None, "closed"): "shock=none|access=closed",
              (FIELD_A, "closed"): "shock=targeted_A|access=closed",
              (FIELD_B, "closed"): "shock=placebo_B|access=closed"}

METRICS = [
    ("apps_A", "persons", "Applications to the targeted field A."),
    ("apps_B", "persons", "Applications to the placebo field B."),
    ("apps_total", "persons", "Total applications across both fields; each person applies once."),
    ("seats_filled_A", "persons", "Field A seats filled (admissions); seats are non-binding at 150."),
    ("seats_filled_B", "persons", "Field B seats filled (admissions)."),
    ("completers_A", "persons", "Field A licensed completers (admissions x licence draw)."),
    ("completers_B", "persons", "Field B licensed completers."),
    ("completers_total", "persons", "Total licensed completers across both fields."),
    ("vacancies_A", "posts", "Vacancy proxy in sector A: max(0, posts_A - completers_A)."),
    ("vacancies_B", "posts", "Vacancy proxy in sector B."),
]


def draw(seed):
    rng = random.Random(seed * 6247 + 14)
    aA = [rng.random() for _ in range(N)]
    aB = [rng.random() for _ in range(N)]
    gate = [rng.random() for _ in range(N)]
    cash = [0.8 + 2.0 * rng.random() for _ in range(N)]
    cost = [3.5 * rng.random() for _ in range(N)]
    licence = [rng.random() for _ in range(N)]
    order = list(range(N))
    rng.shuffle(order)
    return dict(aA=aA, aB=aB, gate=gate, cash=cash, cost=cost, licence=licence,
                order=order)


def gated_set(lat, share):
    ranked = sorted(range(N), key=lambda i: lat["gate"][i], reverse=True)
    return set(ranked[: int(round(share * N))])


def simulate(lat, shock_field, access, gate_share=GATE_SHARE):
    ret = {FIELD_A: RETURN_BASE + (SHOCK if shock_field == FIELD_A else 0.0),
           FIELD_B: RETURN_BASE + (SHOCK if shock_field == FIELD_B else 0.0)}
    admitted = {FIELD_A: 0, FIELD_B: 0}
    completers = {FIELD_A: 0, FIELD_B: 0}
    apps = {FIELD_A: 0, FIELD_B: 0}
    gate = gated_set(lat, gate_share)

    for i in lat["order"]:
        best, best_net = None, None
        for f, apt in ((FIELD_A, lat["aA"]), (FIELD_B, lat["aB"])):
            allowed = access == "open" or f == FIELD_B or i in gate
            if not allowed:
                continue
            if lat["cash"][i] < FEE:
                continue
            value = V_BASE + APT_VALUE * apt[i] + ret[f]
            net = value - lat["cost"][i]
            if net < FEE:
                continue
            if best_net is None or net > best_net + 1e-12:
                best, best_net = f, net
        if best is not None:
            apps[best] += 1
            # Seats are non-binding at 150; admissions = applications.
            admitted[best] += 1
            if lat["licence"][i] < P_LICENSE_BASE + P_LICENSE_APT * (
                    lat["aA"][i] if best == FIELD_A else lat["aB"][i]):
                completers[best] += 1

    posts = {FIELD_A: POSTS_BASE + (POSTS_SHOCK if shock_field == FIELD_A else 0),
             FIELD_B: POSTS_BASE + (POSTS_SHOCK if shock_field == FIELD_B else 0)}
    return dict(
        apps_A=float(apps[FIELD_A]), apps_B=float(apps[FIELD_B]),
        apps_total=float(apps[FIELD_A] + apps[FIELD_B]),
        seats_filled_A=float(admitted[FIELD_A]), seats_filled_B=float(admitted[FIELD_B]),
        completers_A=float(completers[FIELD_A]), completers_B=float(completers[FIELD_B]),
        completers_total=float(completers[FIELD_A] + completers[FIELD_B]),
        vacancies_A=float(max(0, posts[FIELD_A] - completers[FIELD_A])),
        vacancies_B=float(max(0, posts[FIELD_B] - completers[FIELD_B])),
    )


def run(seeds):
    results = {c: {m: [] for m, _, _ in METRICS} for c in CONDITIONS}
    sens = {(FIELD_A, "closed"): {m: [] for m, _, _ in METRICS},
            (None, "closed"): {m: [] for m, _, _ in METRICS}}

    for seed in seeds:
        lat = draw(seed)
        for c in CONDITIONS:
            out = simulate(lat, c[0], c[1])
            for m, _, _ in METRICS:
                results[c][m].append(out[m])
        for c in sens:
            out = simulate(lat, c[0], c[1], gate_share=0.15)
            for m, _, _ in METRICS:
                sens[c][m].append(out[m])

    rows = []
    for c in CONDITIONS:
        for m, unit, definition in METRICS:
            rows.append(row(EXPERIMENT, COND_LABEL[c], "", m, "all", results[c][m],
                            unit, definition))

    contrasts = [
        ("targeted_open", (FIELD_A, "open"), (None, "open")),
        ("targeted_closed", (FIELD_A, "closed"), (None, "closed")),
        ("placebo_open", (FIELD_B, "open"), (None, "open")),
        ("placebo_closed", (FIELD_B, "closed"), (None, "closed")),
    ]
    contrast_metrics = ["apps_A", "apps_B", "apps_total", "completers_A",
                        "completers_B", "completers_total", "vacancies_A", "vacancies_B"]
    for name, left, right in contrasts:
        for m in contrast_metrics:
            xs = [results[left][m][k] - results[right][m][k] for k in range(len(seeds))]
            unit = dict((mm, u) for mm, u, _ in METRICS)[m]
            rows.append(row(EXPERIMENT, COND_LABEL[left], f"minus {COND_LABEL[right]}",
                            m, name, xs, unit,
                            f"Paired within-seed shock effect ({name}) for {m}: shocked arm minus its access-matched no-shock baseline."))

    # Auxiliary sensitivity: tighter gate (15%); no threshold test.
    for m in ["apps_A", "completers_A"]:
        xs = [sens[(FIELD_A, "closed")][m][k] - sens[(None, "closed")][m][k]
              for k in range(len(seeds))]
        rows.append(row(EXPERIMENT, "shock=targeted_A|access=closed|gate=15%",
                        "minus shock=none|access=closed|gate=15%", m, "sensitivity", xs,
                        dict((mm, u) for mm, u, _ in METRICS)[m],
                        f"Auxiliary sensitivity (NOT a threshold test): tighter 15% gate; paired targeted-shock effect on {m}."))

    rows.extend(threshold_rows(results, seeds))
    return rows


def threshold_rows(results, seeds):
    n = len(seeds)
    out = []

    pairs = {"targeted_open": ((FIELD_A, "open"), (None, "open")),
             "targeted_closed": ((FIELD_A, "closed"), (None, "closed")),
             "placebo_open": ((FIELD_B, "open"), (None, "open"))}

    def d(name, m):
        left, right = pairs[name]
        return [results[left][m][k] - results[right][m][k] for k in range(n)]

    ta_open_apps = d("targeted_open", "apps_A")
    ta_open_comp = d("targeted_open", "completers_A")
    ta_open_total = d("targeted_open", "completers_total")
    ta_closed_apps = d("targeted_closed", "apps_A")
    ta_closed_comp = d("targeted_closed", "completers_A")
    pb_open_B = d("placebo_open", "apps_B")
    pb_open_A = d("placebo_open", "apps_A")
    vac_open = [results[(FIELD_A, "open")]["vacancies_A"][k] for k in range(n)]
    vac_closed = [results[(FIELD_A, "closed")]["vacancies_A"][k] for k in range(n)]

    m_open_apps = sum(ta_open_apps) / n
    m_open_comp = sum(ta_open_comp) / n
    m_open_total = sum(ta_open_total) / n
    m_closed_apps = sum(ta_closed_apps) / n
    m_closed_comp = sum(ta_closed_comp) / n

    c1 = m_open_apps >= 30.0
    c2 = m_open_comp >= 25.0
    c3 = abs(m_open_total) <= 10.0
    out.append(row(EXPERIMENT, COND_LABEL[(FIELD_A, "open")],
                   "minus " + COND_LABEL[(None, "open")], "threshold_field_specificity",
                   "threshold", ta_open_apps, "persons",
                   "T14-P1a: with OPEN field access, the targeted shock raises field-A applications by >= 30 persons.",
                   "T14-P1a", ">= 30.000000", verdict([c1])))
    out.append(row(EXPERIMENT, COND_LABEL[(FIELD_A, "open")],
                   "minus " + COND_LABEL[(None, "open")], "threshold_field_specificity_completers",
                   "threshold", ta_open_comp, "persons",
                   "T14-P1b: with OPEN field access, the targeted shock raises field-A licensed completers by >= 25 persons.",
                   "T14-P1b", ">= 25.000000", verdict([c2])))
    out.append(row(EXPERIMENT, COND_LABEL[(FIELD_A, "open")],
                   "minus " + COND_LABEL[(None, "open")], "threshold_reallocation_not_general",
                   "threshold", ta_open_total, "persons",
                   "T14-P1c: the targeted shock REALLOCATES rather than raises overall enrolment: |change in total licensed completers| <= 10 persons.",
                   "T14-P1c", "|x| <= 10.000000", verdict([c3])))

    ratio_apps = m_closed_apps / m_open_apps if m_open_apps else float("nan")
    ratio_comp = m_closed_comp / m_open_comp if m_open_comp else float("nan")
    c4 = ratio_apps <= 0.50
    c5 = ratio_comp <= 0.50
    out.append(row(EXPERIMENT, COND_LABEL[(FIELD_A, "closed")],
                   "minus " + COND_LABEL[(None, "closed")], "threshold_gate_attenuation_apps",
                   "threshold", ta_closed_apps,
                   "persons",
                   f"T14-P2a: with CLOSED field access the field-A application response to the same shock is <= 50% of the open-access response. Row value = closed-access paired delta; observed ratio closed/open = {ratio_apps:.4f}.",
                   "T14-P2a", "ratio <= 0.500000", verdict([c4])))
    out.append(row(EXPERIMENT, COND_LABEL[(FIELD_A, "closed")],
                   "minus " + COND_LABEL[(None, "closed")], "threshold_gate_attenuation_completers",
                   "threshold", ta_closed_comp, "persons",
                   f"T14-P2b: closed-access field-A completer response <= 50% of the open-access completer response. Row value = closed-access paired delta; observed ratio closed/open = {ratio_comp:.4f}.",
                   "T14-P2b", "ratio <= 0.500000", verdict([c5])))

    m_pb_B = sum(pb_open_B) / n
    m_pb_A = sum(pb_open_A) / n
    c6 = m_pb_B >= 30.0 and m_pb_A <= -20.0
    out.append(row(EXPERIMENT, COND_LABEL[(FIELD_B, "open")],
                   "minus " + COND_LABEL[(None, "open")], "threshold_placebo_symmetry",
                   "threshold", pb_open_B, "persons",
                   "T14-P3: an open-access shock to the PLACEBO field moves field-B applications by >= +30 and field-A applications by <= -20, confirming the shock is field-targeted rather than a general demand shift.",
                   "T14-P3", "B >= +30 and A <= -20", verdict([c6])))

    c7 = sum(vac_closed) / n >= 10.0 and sum(vac_open) / n <= 3.0
    out.append(row(EXPERIMENT, COND_LABEL[(FIELD_A, "closed")], "vs open, both shocked",
                   "threshold_vacancies_under_gate", "threshold", vac_closed, "posts",
                   f"T14-P4: after the targeted shock, sector-A unfilled posts are >= 10 under closed access and <= 3 under open access: demand without access shows up as vacancies. Row value = closed-access level; observed open-access level = {sum(vac_open)/n:.4f}.",
                   "T14-P4", "closed >= 10 and open <= 3", verdict([c7])))

    # Falsifier: 'demand works without access'.
    falsified = (ratio_apps >= 1.0) or (ratio_comp >= 1.0) or (m_closed_comp >= m_open_comp)
    out.append(row(EXPERIMENT, "falsifier check", "", "falsifier_14_triggered", "falsifier",
                   [1.0 if falsified else 0.0], "0/1",
                   "F14 falsifier 'demand works without access': triggered if the closed-access field-A response (applications or completers) is at least the open-access response. 0 = the gate attenuates the response.",
                   "F14", "0 = not triggered", verdict([not falsified])))
    return out
