"""Teacher-supplied tutoring in a small school system: an agent-based model.

Agents
  Teachers   one per class and subject. Each chooses to sell tutoring to its own pupils and to
             pupils of the parallel class (with a level of withheld regular content d), to sell
             only to the parallel class, or to take a side job.
  Pupils     one per seat. For each subject a pupil chooses to buy from the own teacher, from the
             parallel-class teacher, from a commercial provider, or to buy nothing.

Three rival mechanisms make own-teacher tutoring attractive:
  thin       xi > 0: feasible regular instruction m0 is short of the curriculum for everyone
  diversion  beta > 0: content the own teacher withholds raises demand; only the own teacher
             fully covers it (others recover a fraction rho)
  favour     phi > 0: buying from the own teacher carries a benefit of its own (assessment,
             relationship, favouritism) whatever is taught

All choice probabilities are computed exactly (multinomial logit) for each simulated pupil, so a run
is deterministic given its seed. Teachers play sequential best responses until no teacher changes.
"""
from dataclasses import dataclass, field, asdict
import numpy as np

SUBJECT_OFFSETS = np.array([0.0, -0.4, -0.8, -1.2])  # e.g. mathematics, physics/chemistry, English, Khmer
K = len(SUBJECT_OFFSETS)
FEE = {9: 1.0, 12: 1.5}          # posted fee per subject, normalized to Grade 9
TEACHER_COST = 0.2               # cost per pupil taught in a tutoring class (same units as fees)
CONVEXITY = 0.5                  # curvature of the cost of withholding content
TUTOR_CONTENT = 0.25             # content a tutoring class adds beyond what the school should cover
D_GRID = np.linspace(0, 0.4, 9)  # feasible withholding levels (capped by m0)
CLASS_SIZE = 70
# Six schools as in the Siem Reap study: three lower secondary (Grade 9) and three high schools
# (Grades 9 and 12). Which two are urban is an assumption.
SCHOOLS = [("lower", True), ("lower", False), ("lower", False),
           ("high", True), ("high", False), ("high", False)]


@dataclass
class Params:
    base_demand: float = -1.0       # A
    stakes12: float = 0.8           # extra value of tutoring in Grade 12 (national exam)
    thin: float = 1.0               # xi
    m0_mean: float = 0.75           # mean feasible regular instruction (share of curriculum)
    diversion: float = 0.0          # beta
    favour: float = 0.0             # phi
    recovery: float = 0.5           # rho
    other_cost: float = 0.6         # inconvenience of the parallel-class teacher
    com_cost_urban: float = 1.5     # inconvenience of a commercial provider in town
    com_cost_rural_extra: float = 2.0
    fee_sens: float = 1.2           # gamma0
    urban_resources: float = 0.4    # urban shift in household resources (sd units)
    side_job_max: float = 0.6       # side-job returns ~ U(0, max)
    norm_cost: float = 0.4          # median per-unit cost of withholding content (lognormal)
    fixed_cost: float = 0.1         # cost of opening a tutoring class
    # policy levers (zero in the observed world)
    ban_own: bool = False           # teachers may not sell to their own pupils
    cond_pay: float = 0.0           # bonus for teachers who do not sell to own pupils
    extra_time: float = 0.0         # added feasible regular instruction
    com_entry: float = 0.0          # reduction in commercial inconvenience
    # household channel (task 3.4): OFF in calibration; not in PRIORS, so it is never drawn or fitted.
    # When on, expected tutoring spending of pupils in the poorest resource quintile raises their dropout and
    # child-work hazards. Units: spending in Grade-9 subject fees; the hazards are illustrative, not data.
    dropout_channel: bool = False
    drop_base: float = 0.05         # baseline dropout hazard (illustrative)
    work_base: float = 0.05         # baseline child-work hazard (illustrative)
    drop_kappa: float = 0.0         # extra dropout hazard per unit of tutoring spending, poorest quintile
    work_kappa: float = 0.0         # extra child-work hazard per unit of tutoring spending, poorest quintile


PRIORS = {  # uniform ranges used for calibration
    "base_demand": (-3.0, 1.0), "stakes12": (0.0, 2.0), "thin": (0.0, 3.0), "m0_mean": (0.5, 0.9),
    "diversion": (0.0, 4.0), "favour": (0.0, 2.0), "recovery": (0.0, 1.0), "other_cost": (0.0, 1.5),
    "com_cost_urban": (0.5, 3.0), "com_cost_rural_extra": (1.0, 4.0), "fee_sens": (0.5, 3.0),
    "urban_resources": (0.0, 0.8), "side_job_max": (0.1, 1.2), "norm_cost": (0.05, 2.0),
    "fixed_cost": (0.0, 0.3),
}
VARIANTS = {  # which mechanism parameters are free; the others are fixed at zero
    "thin": (), "diversion": ("diversion",), "favour": ("favour",), "full": ("diversion", "favour"),
}


def draw_params(rng, variant):
    values = {k: rng.uniform(*v) for k, v in PRIORS.items()}
    for mech in ("diversion", "favour"):
        if mech not in VARIANTS[variant]:
            values[mech] = 0.0
    return Params(**values)


class World:
    def __init__(self, p: Params, seed: int):
        rng = np.random.default_rng(seed)
        self.p = p
        units = []  # (school, grade)
        for s, (kind, _) in enumerate(SCHOOLS):
            units += [(s, 9)] + ([(s, 12)] if kind == "high" else [])
        m0_unit = np.clip(p.m0_mean + rng.normal(0, 0.08, len(units)) + p.extra_time, 0.2, 1.0)
        cls_unit = np.repeat(np.arange(len(units)), 2)            # two parallel classes per unit
        self.n_cls = len(cls_unit)
        self.partner = np.arange(self.n_cls) ^ 1                   # 0<->1, 2<->3, ...
        pc = np.repeat(np.arange(self.n_cls), CLASS_SIZE)          # pupil -> class
        self.pupil_class = pc
        self.class_pupils = [np.flatnonzero(pc == c) for c in range(self.n_cls)]
        self.school = np.array([units[u][0] for u in cls_unit])[pc]
        self.grade = np.array([units[u][1] for u in cls_unit])[pc]
        self.urban = np.array([SCHOOLS[s][1] for s in self.school])
        self.m0 = m0_unit[cls_unit][pc]
        self.resources = rng.normal(0, 1, pc.size) + p.urban_resources * self.urban
        n_t = self.n_cls * K                                       # teacher = class * K + subject
        self.side_job = rng.uniform(0, p.side_job_max, n_t)
        self.norm = p.norm_cost * np.exp(rng.normal(0, 0.5, n_t))
        self.teacher_m0 = np.repeat(m0_unit[cls_unit], K)
        self.teacher_fee = np.repeat(np.array([FEE[units[u][1]] for u in cls_unit]), K)
        # pupil x subject utility pieces that do not depend on teachers
        fee = np.vectorize(FEE.get)(self.grade)
        gamma = p.fee_sens * np.exp(-self.resources)
        self.base = (p.base_demand + SUBJECT_OFFSETS[None, :] + p.stakes12 * (self.grade == 12)[:, None]
                     + p.thin * (1 - self.m0)[:, None] - (gamma * fee)[:, None])
        com_cost = p.com_cost_urban + p.com_cost_rural_extra * (~self.urban) - p.com_entry
        self.com_cost = np.maximum(com_cost, 0)[:, None]
        # teacher state
        self.sell_own = np.ones(n_t, bool) & (not p.ban_own)
        self.sell_other = np.ones(n_t, bool)
        self.d = np.zeros(n_t)
        self.converged = False
        self.sweeps = 0
        self.rng = rng

    # --- pupils -----------------------------------------------------------------------------
    def own_teacher(self, pupils):
        return self.pupil_class[pupils][:, None] * K + np.arange(K)[None, :]

    def choice(self, pupils, d_own=None, sell_own=None, other_open=None):
        """Probabilities (own, other, commercial) for the given pupils, shape (n, K, 3)."""
        p = self.p
        t = self.own_teacher(pupils)
        partner_t = self.partner[self.pupil_class[pupils]][:, None] * K + np.arange(K)[None, :]
        d = self.d[t] if d_own is None else d_own
        own_ok = self.sell_own[t] if sell_own is None else sell_own
        oth_ok = self.sell_other[partner_t] if other_open is None else other_open
        b = self.base[pupils]
        v_own = np.where(own_ok, np.exp(b + p.diversion * d + p.favour), 0.0)
        v_oth = np.where(oth_ok, np.exp(b + p.recovery * p.diversion * d - p.other_cost), 0.0)
        v_com = np.exp(b + p.recovery * p.diversion * d - self.com_cost[pupils])
        denom = 1 + v_own + v_oth + v_com
        return np.stack([v_own, v_oth, v_com], axis=-1) / denom[..., None]

    # --- teachers ---------------------------------------------------------------------------
    def choice_k(self, pupils, k, d, own_ok, oth_ok):
        """Probabilities (own, other, commercial) in subject k; d may be (n,) or (n, G)."""
        p = self.p
        b = self.base[pupils, k]
        com = self.com_cost[pupils, 0]
        if d.ndim == 2:
            b, com = b[:, None], com[:, None]
        v_own = np.exp(b + p.diversion * d + p.favour) * own_ok
        v_oth = np.exp(b + p.recovery * p.diversion * d - p.other_cost) * oth_ok
        v_com = np.exp(b + p.recovery * p.diversion * d - com)
        denom = 1 + v_own + v_oth + v_com
        return v_own / denom, v_oth / denom, v_com / denom

    def best_response(self, t):
        p = self.p
        cls, k = divmod(t, K)
        own = self.class_pupils[cls]
        par_cls = self.partner[cls]
        par = self.class_pupils[par_cls]
        margin = self.teacher_fee[t] - TEACHER_COST
        par_t = par_cls * K + k
        _, prob_par, _ = self.choice_k(par, k, np.full(par.size, self.d[par_t]),
                                       float(self.sell_own[par_t]), 1.0)
        q_par = prob_par.sum() / CLASS_SIZE
        options = [(self.side_job[t] + p.cond_pay, False, False, 0.0),
                   (margin * q_par - p.fixed_cost + p.cond_pay, False, True, 0.0)]
        if not p.ban_own:
            grid = D_GRID[D_GRID <= self.teacher_m0[t] + 1e-12]
            d = np.broadcast_to(grid[None, :], (own.size, grid.size))
            p_own, _, _ = self.choice_k(own, k, d, 1.0, float(self.sell_other[par_t]))
            q_own = p_own.sum(0) / CLASS_SIZE
            profit = margin * (q_own + q_par) - p.fixed_cost - self.norm[t] * grid - .5 * CONVEXITY * grid ** 2
            g = int(np.argmax(profit))
            options.append((profit[g], True, True, grid[g]))
        best = max(options, key=lambda o: o[0])
        return best[1], best[2], best[3]

    def solve(self, max_sweeps=30):
        n_t = self.sell_own.size
        for sweep in range(max_sweeps):
            changed = False
            for t in self.rng.permutation(n_t):
                own, other, d = self.best_response(t)
                if own != self.sell_own[t] or other != self.sell_other[t] or abs(d - self.d[t]) > 1e-12:
                    self.sell_own[t], self.sell_other[t], self.d[t] = own, other, d
                    changed = True
            self.sweeps = sweep + 1
            if not changed:
                self.converged = True
                break
        return self

    # --- outputs ----------------------------------------------------------------------------
    def outcomes(self):
        p = self.p
        everyone = np.arange(self.pupil_class.size)
        pr = self.choice(everyone)                       # (n, K, 3)
        buy = pr.sum(-1)
        any_buy = 1 - np.prod(1 - buy, axis=1)
        any_own = 1 - np.prod(1 - pr[..., 0], axis=1)
        any_oth = 1 - np.prod(1 - pr[..., 1], axis=1)
        any_com = 1 - np.prod(1 - pr[..., 2], axis=1)
        t = self.own_teacher(everyone)
        d = self.d[t]
        cls_cov = self.m0[:, None] - d                   # regular instruction actually delivered
        add = pr[..., 0] * (d + TUTOR_CONTENT) + (pr[..., 1] + pr[..., 2]) * (p.recovery * d + TUTOR_CONTENT)
        coverage = np.minimum(1, cls_cov + add)
        q = np.digitize(self.resources, np.quantile(self.resources, [.2, .4, .6, .8]))
        tutors = self.sell_own | self.sell_other
        tutoring_class = self.sell_own[t]                # pupil's own teacher sells to own pupils
        part_subj = buy
        g9, g12 = self.grade == 9, self.grade == 12
        u, r = self.urban, ~self.urban
        tot = any_buy.sum()
        out = {
            "participation": any_buy.mean(),
            "participation_g9": any_buy[g9].mean(), "participation_g12": any_buy[g12].mean(),
            "participation_urban": any_buy[u].mean(), "participation_rural": any_buy[r].mean(),
            # provider shares of all tutoring purchases (pupil-subjects): the main-provider reading
            "own_purchase_share": pr[..., 0].sum() / buy.sum(),
            "other_purchase_share": pr[..., 1].sum() / buy.sum(),
            "com_purchase_share": pr[..., 2].sum() / buy.sum(),
            "subjects_bought": buy.sum(1).mean(),
            "own_share": any_own.sum() / tot, "other_share": any_oth.sum() / tot, "com_share": any_com.sum() / tot,
            "teacher_tutor_share": tutors.mean(), "teacher_own_share": self.sell_own.mean(),
            "withholding_mean": self.d.mean(),
            "withholding_among_sellers": self.d[self.sell_own].mean() if self.sell_own.any() else 0.0,
            "class_instruction": cls_cov.mean(),
            "coverage": coverage.mean(),
            "coverage_q1": coverage[q == 0].mean(), "coverage_q5": coverage[q == 4].mean(),
            "participation_q1": any_buy[q == 0].mean(), "participation_q5": any_buy[q == 4].mean(),
            # coverage among pupil-subjects with no purchase, weighted by the probability of not buying
            "nonbuyer_class_instruction": ((1 - buy) * cls_cov).sum() / (1 - buy).sum(),
            # signatures: subject-level purchase and delivered instruction in classes whose teacher
            # does / does not sell to own pupils
            "buy_tutoring_teacher": part_subj[tutoring_class].mean() if tutoring_class.any() else np.nan,
            "buy_nontutoring_teacher": part_subj[~tutoring_class].mean() if (~tutoring_class).any() else np.nan,
            "instr_tutoring_teacher": cls_cov[tutoring_class].mean() if tutoring_class.any() else np.nan,
            "instr_nontutoring_teacher": cls_cov[~tutoring_class].mean() if (~tutoring_class).any() else np.nan,
            "other_given_tutoring_teacher": pr[..., 1][tutoring_class].mean() if tutoring_class.any() else np.nan,
            "other_given_nontutoring_teacher": pr[..., 1][~tutoring_class].mean() if (~tutoring_class).any() else np.nan,
            "converged": float(self.converged), "sweeps": self.sweeps,
        }
        if p.dropout_channel:
            fee = np.array([FEE[g] for g in self.grade])
            spend = buy.sum(1) * fee                       # expected tutoring spending per pupil
            poor = q == 0                                  # lowest resource quintile
            h_drop = np.clip(p.drop_base + p.drop_kappa * spend * poor, 0, 1)
            h_work = np.clip(p.work_base + p.work_kappa * spend * poor, 0, 1)
            out.update({"spend_poor": spend[poor].mean(), "spend_nonpoor": spend[~poor].mean(),
                        "dropout_poor": h_drop[poor].mean(), "dropout_nonpoor": h_drop[~poor].mean(),
                        "child_work_poor": h_work[poor].mean(), "child_work_nonpoor": h_work[~poor].mean()})
        return {k: float(v) for k, v in out.items()}


def run(params: Params, seed: int):
    return World(params, seed).solve().outcomes()
