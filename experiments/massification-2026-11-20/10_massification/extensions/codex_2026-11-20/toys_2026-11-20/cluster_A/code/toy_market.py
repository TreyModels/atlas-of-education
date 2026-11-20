"""Shared stipulated market engine for Cluster A toys (#1-#3).

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence;
no historical test; phase closed; do not cite numbers as estimates.

Standard library only. Every rule here is imposed by ../PRE_DECLARATIONS.md,
not estimated. The household side is inherited from the base toy
`model.py`/`experiments.py`; the provider side is replaced by the fixed-cost
entry threshold the Council spec asks for.

Household side
  * 100 households; budgets half 1.5 and half 4.0, shuffled; opportunity cost
    U[0, 3.5); a public lottery order.
  * apply iff premium - cost >= public fee (1.0); public seats take the first
    `public_seats` applicants in lottery order.
  * private customers are waiting-list households with budget >= tuition (2.0)
    and premium - cost >= tuition.
Provider side
  * a provider is a fixed capacity unit of `cap` seats, exactly as the base
    toy's PRIVATE_CAPACITY = 30 is fixed; its utilisation varies with demand.
    (capacity_mode="divisible" is a declared robustness variant in which the
    provider instead installs min(cap, unmet customers at its decision date);
    the primary mode is "lump".)
  * entry: add an inactive provider iff unmet customers (net of capacity under
    construction and of active providers) >= bk, where
    bk = F / (tuition - varcost) in seats, i.e. qty * (tuition - varcost) >= F.
  * exit: an active provider whose allocated customers < bk is removed.
  * installation lock: a provider cannot exit in its first active period.
  * allocation: active providers fill in entry order, each up to cap.
"""

import random

NUM_HOUSEHOLDS = 100
PUBLIC_FEE = 1.0
TUITION = 2.0
VARIABLE_COST = 1.0
UNIT_CONTRIBUTION = TUITION - VARIABLE_COST
BASE_PREMIUM = 4.0
COST_MAX = 3.5
MODES = ("lump", "divisible")


# --------------------------------------------------------------------------- #
# Households
# --------------------------------------------------------------------------- #
def draw_cohort(seed):
    """Latent cohort used by every arm of a given seed (paired design)."""
    rng = random.Random(seed)
    budgets = [1.5, 4.0] * (NUM_HOUSEHOLDS // 2)
    rng.shuffle(budgets)
    costs = [COST_MAX * rng.random() for _ in range(NUM_HOUSEHOLDS)]
    lottery = list(range(NUM_HOUSEHOLDS))
    rng.shuffle(lottery)
    return budgets, costs, lottery


def pools(budgets, costs, lottery, premium, public_seats):
    """Return (applications, public_admissions, private_customers) counts."""
    applicants = [i for i in lottery if premium - costs[i] >= PUBLIC_FEE]
    public = applicants[:public_seats]
    waiting = applicants[public_seats:]
    customers = [i for i in waiting
                 if budgets[i] >= TUITION and premium - costs[i] >= TUITION]
    return len(applicants), len(public), len(customers)


# --------------------------------------------------------------------------- #
# Break-even arithmetic (integer by construction, no float ambiguity)
# --------------------------------------------------------------------------- #
def breakeven_seats(fixed_cost_cents):
    """bk = F / unit contribution; requires a whole number of seats."""
    step = int(round(UNIT_CONTRIBUTION * 100))
    if fixed_cost_cents % step != 0:
        raise ValueError("fixed cost must be a whole number of seats in cents")
    return fixed_cost_cents // step


def provider_size(residual, cap, mode):
    if mode == "lump":
        return cap
    if mode == "divisible":
        return min(cap, residual)
    raise ValueError(mode)


def equilibrium_install(customers, cap, breakeven, max_providers, mode="lump"):
    """Installed sizes of a mature competitive equilibrium, greedy in order."""
    installed = []
    residual = customers
    while len(installed) < max_providers and residual >= breakeven:
        size = provider_size(residual, cap, mode)
        installed.append(size)
        residual -= size
    return installed


def equilibrium_state(cohort, premium, public_seats, cap, breakeven,
                      max_providers, mode="lump"):
    """Static equilibrium with mature providers (used by experiment #2)."""
    budgets, costs, lottery = cohort
    apps, pub, cust = pools(budgets, costs, lottery, premium, public_seats)
    installed = equilibrium_install(cust, cap, breakeven, max_providers, mode)
    seats = sum(installed)
    served = min(cust, seats)
    return dict(applications=apps, public_admissions=pub, customers=cust,
                private_seats=seats, private_admissions=served,
                providers=len(installed), total_admissions=pub + served)


# --------------------------------------------------------------------------- #
# Dynamic private sector
# --------------------------------------------------------------------------- #
class PrivateSector(object):
    def __init__(self, cap, breakeven, max_providers, mode="lump"):
        if mode == "lump" and cap < breakeven:
            raise ValueError("lump capacity unit cannot cover the fixed cost")
        if mode not in MODES:
            raise ValueError(mode)
        self.cap = cap
        self.breakeven = breakeven
        self.max_providers = max_providers
        self.mode = mode
        self.installed = []
        self.age = []
        self.pending = {}
        self.total_exits = 0
        self.total_orders = 0
        self.total_arrivals = 0

    def start(self, customers):
        """Matched starting condition: period-1 equilibrium, mature providers."""
        self.installed = equilibrium_install(
            customers, self.cap, self.breakeven, self.max_providers, self.mode)
        self.age = [1000] * len(self.installed)
        return sum(self.installed)

    def allocations(self, customers):
        allocs = []
        left = customers
        for size in self.installed:
            take = min(size, left)
            allocs.append(take)
            left -= take
        return allocs

    def step(self, customers, period, entry_lag):
        new = self.pending.pop(period, [])
        self.installed.extend(new)
        self.age.extend([0] * len(new))
        arrivals = len(new)
        self.total_arrivals += arrivals

        # Exit: providers past their installation period whose allocation < bk.
        exited = 0
        while True:
            allocs = self.allocations(customers)
            victim = None
            for j in range(len(self.installed) - 1, -1, -1):
                if self.age[j] >= 1 and allocs[j] < self.breakeven:
                    victim = j
                    break
            if victim is None:
                break
            del self.installed[victim]
            del self.age[victim]
            exited += 1
        self.total_exits += exited

        # Entry: pipeline-aware, at most one cohort of orders per shortage.
        piped = sum(sum(v) for v in self.pending.values())
        outstanding = sum(len(v) for v in self.pending.values())
        residual = customers - sum(self.installed) - piped
        orders = 0
        while (residual >= self.breakeven
               and len(self.installed) + outstanding < self.max_providers):
            size = provider_size(residual, self.cap, self.mode)
            if entry_lag == 0:
                self.installed.append(size)
                self.age.append(0)
            else:
                self.pending.setdefault(period + entry_lag, []).append(size)
                outstanding += 1
            orders += 1
            residual -= size
        self.total_orders += orders

        seats = sum(self.installed)
        served = sum(self.allocations(customers))
        for j in range(len(self.age)):
            self.age[j] += 1
        return dict(private_seats=seats, private_admissions=served,
                    providers=len(self.installed), vacancy=seats - served,
                    backlog=max(0, customers - seats), arrivals=arrivals,
                    exits=exited, orders=orders, customers=customers)


def simulate(cohort, multipliers, public_seats, cap, breakeven, max_providers,
             entry_lag, mode="lump"):
    """Run one demand path; returns one record per period."""
    budgets, costs, lottery = cohort
    sector = PrivateSector(cap, breakeven, max_providers, mode)
    records = []
    for period, mult in enumerate(multipliers, start=1):
        premium = BASE_PREMIUM * mult
        apps, pub, cust = pools(budgets, costs, lottery, premium, public_seats)
        if period == 1:
            sector.start(cust)
        rec = sector.step(cust, period, entry_lag)
        rec.update(period=period, multiplier=mult, applications=apps,
                   public_admissions=pub,
                   total_admissions=pub + rec["private_admissions"])
        records.append(rec)
    return records
