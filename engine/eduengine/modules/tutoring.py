"""Shadow education: a market with three motives and two suppliers.

Motives (Dang & Rogers 2008; Bray 1999, 2009):
  buy-back   restore lessons the own teacher withheld (Biswal 1999; Jayachandran 2014) - only the own teacher fully can
  gate prep  raise the chance of passing the next gate x what passing is worth (Kim & Lee 2010; Dang 2007), priced
             through the core's marginal value of learning, so it rises with exam stakes and labour-market scarcity
  remedial   help a home cannot give (parental education), independent of exams
Suppliers: the pupil's own teacher (fixed price, available unless banned and enforced) and firms (upward-sloping
short-run supply, flat long-run supply through entry; bans cut availability and push prices up).

CONTEST TUTORING LEDGER (Gate 1b, ENGINE_INTERFACE_CONTRACT v1.0 §4-§5). One price is split into four
explicit quantities per child-year, all in wage units:

    res_cost[i]   = contest_price * e_t[i]                       resource cost (teacher time, materials)
    tut_tax[i]    = contest_tax_rate * res_cost[i]               tax paid by the household
    tut_outlay[i] = res_cost[i] + tut_tax[i]                     HOUSEHOLD OUTLAY = what the cash budget must cover
    gov_tax[i]    = tut_tax[i]                                   government receipt (attributed to the payer)

with the exact identities `tut_outlay == res_cost + tut_tax` and `sum(gov_tax) == sum(tut_tax)`.
`contest_price` (CORE_DEFAULTS) is the PRE-TAX resource price; the household's unit outlay is
`contest_price * (1 + contest_tax_rate)`. Defaults are legacy-neutral: tax 0, prep depreciation 0, pure
positional coaching, no rebate.

Preparation is a PER-GATE STOCK owned by core: `k['prep_stock'] (N, nlev)`, allocated in `add_cohort`, compacted
on exit and consumed (column zeroed) at the gate. This module performs the annual update

    prep_stock[i, :] *= (1 - contest_prep_depreciation)          every attending child, every gate
    prep_stock[i, m] += contest_prep_positional_share * e_t[i]   m = child's nearest upcoming contest gate

so `contest_prep_depreciation = 0` is the legacy undepreciated lifetime sum and `1` is memoryless
(Directive rho = depreciation rate, contract §5 / amendment A1). `k['contest_e']` is now only this year's effort
flow `e_t` (assigned, never accumulated) for `contest_e_mean` reporting; it never feeds a probability.

The effort `e_t` maximises `E.gate_prize_dv(m, .) * P(x_eff(e)) - unit_net * e / y` on an explicit proportional
grid plus a documented analytic local search (a parabola through the three grid nodes around each child's best
node), where `P` is the contract §1.3 expected probability (`pl_win_probs` over the weights owned by core,
`E.contest_weights`), NOT the legacy `1 - exp(-lam x^r)` formula. The prize is read only through
`E.gate_prize_dv` (no direct `elite_logw` / `track_prize` reads). Cost: 9 probability evaluations per
contest gate-year (plus none when no child in the pool has a positive prize or positive cash), and the residual
grid/refinement error is reported as `contest_grid_bound`.
"""
import numpy as np
from ..core import Module

# contest effort choice: 9-point proportional grid over each child's [0, e_hi] (fraction of cap/cash bound),
# then an analytic quadratic local search through the three nodes around each child's best node. 9 probability
# evaluations per contest gate-year; the residual bound is reported as `contest_grid_bound` (contract §5).
_PREP_GRID = np.linspace(0.0, 1.0, 9)

_VALID_MODES = ('positional', 'learning', 'both')
_VALID_REBATE_POLICIES = ('none', 'uniform')


class TutoringMarket(Module):
    name = 'tutoring'
    defaults = dict(
        tut_effect=0.35, tut_effect_own=0.25,       # grade-equivalents of learning per year of tutoring
        p_own=0.04, p_firm=0.06,                    # own-teacher price; firms' long-run price (wage units per year)
        firm_elast=1.0, firm_entry=0.3,
        own_ban=0.0, firm_ban=0.0,                  # enforcement share of a ban on own-pupil / commercial tutoring
        rural_firm_access=0.4, buyback_firm=0.3, r0=0.0, tut_taste=0.03,
        # ---- contest tutoring fiscal ledger + preparation stock (Gate 1b; contract §4-§5) ----
        contest_tax_rate=0.0,              # tax on the contest-tutoring resource cost (0 = legacy)
        contest_prep_depreciation=0.0,     # rho: prep_stock <- (1-rho)*prep_stock + e ; 0 = legacy, 1 = memoryless
        contest_prep_mode='positional',    # 'positional' (legacy) | 'learning' | 'both'
        contest_prep_learning_gain=0.0,    # grade-equivalents of learning per unit e_t (active in learning/both)
        contest_prep_positional_share=1.0, # positional weight of e_t in the gate (1 legacy; 0 in 'learning')
        contest_rebate_policy='none',      # 'none' | 'uniform' (rebate credited to paying households)
        contest_rebate_rate=0.0,           # share of tut_tax credited back to the household under 'uniform'
    )

    def setup(self, E):
        E.tut_sell = 1.0 - E.p['own_ban']           # read by PublicSchools: withholding only pays if it can be sold
        self.K = 0.0; self.D = 0.0
        p = E.p
        mode = p['contest_prep_mode']
        if mode not in _VALID_MODES:
            raise ValueError(f"contest_prep_mode must be one of {_VALID_MODES}; got {mode!r}")
        if p['contest_rebate_policy'] not in _VALID_REBATE_POLICIES:
            raise ValueError(f"contest_rebate_policy must be one of {_VALID_REBATE_POLICIES}; "
                             f"got {p['contest_rebate_policy']!r}")
        if not (0.0 <= float(p['contest_prep_depreciation']) <= 1.0):
            raise ValueError("contest_prep_depreciation must be in [0, 1]")
        if not (0.0 <= float(p['contest_tax_rate']) < 1.0):
            raise ValueError("contest_tax_rate must be in [0, 1)")
        if not (0.0 <= float(p['contest_rebate_rate']) <= 1.0):
            raise ValueError("contest_rebate_rate must be in [0, 1]")
        if not (0.0 <= float(p['contest_prep_positional_share']) <= 1.0):
            raise ValueError("contest_prep_positional_share must be in [0, 1]")
        if float(p['contest_prep_learning_gain']) < 0.0:
            raise ValueError("contest_prep_learning_gain must be >= 0")
        if mode != 'positional' and float(p['contest_prep_learning_gain']) <= 0.0:
            raise ValueError(f"contest_prep_mode={mode!r} requires contest_prep_learning_gain > 0 "
                             "(otherwise the learning channel is empty and no contest effort is worthwhile)")

    def firm_price(self, E):
        p = E.p
        base = p['p_firm'] * (1 + p['firm_ban'])     # a ban pushes surviving supply underground and dearer
        if self.K <= 0:
            return base * 1.5
        return base * max(1.0, self.D / self.K) ** (1 / p['firm_elast'])

    # ------------------------------------------------------------------ helpers (contract §6 API)
    @staticmethod
    def _require(E, name):
        fn = getattr(E, name, None)
        if fn is None:
            raise RuntimeError(
                f"tutoring.py: Engine has no {name}(); ENGINE_INTERFACE_CONTRACT §6 (engine-core) not landed yet. "
                "Contest configurations cannot run until core.py implements the §6 API; tutoring will not fall "
                "back to the removed 1-exp(-lam x^r) expected-probability formula."
            )
        return fn

    @staticmethod
    def _contest_gates(E):
        """[(m, gate)] for contest gates, sorted by level (contract §6 E.contest_gates, else read p['gates'])."""
        cg = getattr(E, 'contest_gates', None)
        if cg is not None:
            return sorted([(int(m), g) for m, g in cg], key=lambda x: x[0])
        gates = getattr(E, 'gates', E.p['gates'])
        out = [(m, g) for m, g in enumerate(gates) if g.get('kind') == 'contest']
        return out

    @staticmethod
    def _as_mask(x, n):
        a = np.asarray(x)
        if a.dtype == bool:
            if a.shape != (n,):
                raise RuntimeError(f"candidate mask has shape {a.shape}, expected ({n},)")
            return a
        mask = np.zeros(n, dtype=bool)
        if a.size:
            mask[a.astype(np.int64)] = True
        return mask

    @staticmethod
    def _unpack_pids_weights(out, idx):
        """Normalise E.contest_weights / E.contest_expected_probs returns to (pids, values)."""
        if isinstance(out, tuple) and len(out) == 2:
            pids, vals = out
            return np.asarray(pids), np.asarray(vals, dtype=float)
        # contract says (pids, values); accept a bare array only if it lines up with idx length
        vals = np.asarray(out, dtype=float)
        return None, vals

    def _weights_with_override(self, E, m, base_pids, base_w, sub_global, stock_override):
        """Weights over the FULL candidate set with `sub_global` children's prep stock replaced.

        The weight definition belongs to core (§1.3/§6): we ask core for the overridden children's weights and
        splice them into the cached full-candidate vector. We never re-derive x_eff here.
        """
        fn = self._require(E, 'contest_weights')
        try:
            out = fn(m, idx=sub_global, stock_override=stock_override)
        except TypeError as exc:      # stock_override not implemented yet
            raise RuntimeError(
                "tutoring.py: E.contest_weights(m, idx, stock_override=...) is required by contract §6 for the "
                f"prep-effort grid search; got TypeError ({exc}). engine-core API incomplete."
            ) from exc
        pids_sub, w_sub = self._unpack_pids_weights(out, sub_global)
        if w_sub.shape != np.shape(sub_global):
            raise RuntimeError(f"E.contest_weights override returned {w_sub.shape} weights for "
                               f"{np.shape(sub_global)} children")
        w = base_w.astype(float, copy=True)
        if pids_sub is None:
            # no pids: assume the returned order matches sub_global, locate via base pids if available
            if base_pids is None:
                raise RuntimeError("E.contest_weights(..., idx=...) must return (pids, w) per contract §6")
            pids_sub = np.asarray(base_pids)[np.asarray(sub_global)]
        if base_pids is None:
            raise RuntimeError("E.contest_weights(m) must return (pids, w) per contract §6")
        base_pids = np.asarray(base_pids)
        order = np.argsort(base_pids)
        sorted_pids = base_pids[order]
        pos = np.searchsorted(sorted_pids, pids_sub)
        if np.any(pos >= sorted_pids.size) or np.any(sorted_pids[np.minimum(pos, sorted_pids.size - 1)] != pids_sub):
            raise RuntimeError("E.contest_weights override returned pids outside the candidate set")
        w[order[pos]] = w_sub
        return w

    def _prize_dv(self, E, m, sub_global):
        """Utility value of passing gate m for `sub_global` children (the ONLY prize source, contract §6)."""
        out = self._require(E, 'gate_prize_dv')(m, sub_global)
        if isinstance(out, tuple) and len(out) == 2:
            _pids, dv = out
        else:
            dv = out
        dv = np.asarray(dv, dtype=float)
        if dv.shape != np.shape(sub_global):
            raise RuntimeError(f"E.gate_prize_dv returned {dv.shape} values for {np.shape(sub_global)} children")
        return dv

    def _positional_share(self, p):
        """Share of e_t that enters the gate as positional prep stock (contract §5 switch).

        'positional': 1.0; 'both': contest_prep_positional_share (default 1.0); 'learning': 0.0 unless the user
        set an explicit non-default share (the declared default 1.0 with mode='learning' means no positional input).
        """
        mode = p['contest_prep_mode']
        share = float(p['contest_prep_positional_share'])
        if mode == 'positional':
            return 1.0
        if mode == 'both':
            return share
        # 'learning'
        return 0.0 if share >= 1.0 else share

    def _learning_gain(self, p):
        if p['contest_prep_mode'] == 'positional':
            return 0.0
        return float(p['contest_prep_learning_gain'])

    def _rebate_rate(self, p):
        if p['contest_rebate_policy'] == 'none':
            return 0.0
        return float(p['contest_rebate_rate'])

    # ------------------------------------------------------------------ annual behaviour
    def extras(self, E, t):
        p, k, r, y = E.p, E.kids, E.rng, E.yr
        att = k['att']
        idx = np.flatnonzero(att)
        n = len(att)
        choice = np.zeros(n, int)          # 0 none, 1 own teacher, 2 firm
        pf = self.firm_price(E)
        if len(idx):
            mvl = E.mvl_all(t)[idx]
            h = y['withheld'][idx]; q = y['quality'][idx]
            rem = p['r0'] * (1 - k['home'][idx])
            yy = np.maximum(k['y'][idx], 0.05)
            u_own = mvl * (p['tut_effect_own'] + h * q) + rem * p['tut_effect_own'] - p['p_own'] / yy
            u_firm = mvl * (p['tut_effect'] + p['buyback_firm'] * h * q) + rem * p['tut_effect'] - pf / yy
            own_ok = (k['sector'][idx] == 0) & (k['g'][idx] < 12) & (r.random(len(idx)) >= p['own_ban'])
            firm_ok = (r.random(len(idx)) < (1 - p['firm_ban']) * np.where(k['urban'][idx], 1.0, p['rural_firm_access']))
            cash = E._cash[idx]
            u_own = np.where(own_ok & (cash >= p['p_own']), u_own + p['tut_taste'] * r.standard_normal(len(idx)), -np.inf)
            u_firm = np.where(firm_ok & (cash >= pf), u_firm + p['tut_taste'] * r.standard_normal(len(idx)), -np.inf)
            U = np.stack([np.zeros(len(idx)), u_own, u_firm], 1)
            ch = U.argmax(1)
            choice[idx] = ch
        # firm capacity rations demand (highest income first), then entry moves capacity toward demand
        dem = np.flatnonzero(choice == 2)
        self.D = len(dem)
        if self.K <= 0:
            choice[dem] = 0
        elif len(dem) > self.K:
            drop = dem[np.argsort(k['y'][dem])][:len(dem) - int(self.K)]
            choice[drop] = 0
        self.K = max(0.0, self.K + p['firm_entry'] * (self.D - self.K) + (min(self.D, 0.01 * p['N']) if self.K < 1 else 0))
        own, firm = choice == 1, choice == 2
        y['tut_gain'] += np.where(own, p['tut_effect_own'], 0.0) + np.where(firm, p['tut_effect'], 0.0)
        y['buyback'] |= own
        y['withheld'] = np.where(firm, y['withheld'] * (1 - p['buyback_firm']), y['withheld'])
        y['extra_spend'] += np.where(own, p['p_own'], 0.0) + np.where(firm, pf, 0.0)
        pre_contest_spend = y['extra_spend'].copy()      # budget-tutoring outlays already booked (contract §4.2)

        # ---- Tullock contest tutoring (only active when at least one gate has kind='contest') ----
        nlev = E.nlev
        contest_e_now = np.zeros(n)          # this year's physical prep effort e_t (flow; reporting only)
        res_cost = np.zeros(n)               # contest resource cost
        tut_tax = np.zeros(n)                # tax paid by the household
        tut_outlay = np.zeros(n)             # household outlay = res_cost + tut_tax (cash-budget quantity)
        gov_tax = np.zeros(n)                # government receipts, attributed to the paying household
        rebate = np.zeros(n)                 # rebate credited to households (only if policy != 'none')
        prep_stock_mean = np.full(nlev, np.nan)
        contest_assigned_gate = np.full(n, -1, int)
        prep_pre = np.zeros((n, nlev))
        learn_gain = 0.0
        pos_share = 1.0
        prob_evals = 0
        grid_bound = 0.0
        assigned_any = np.zeros(n, bool)
        contest_gates = self._contest_gates(E)
        if contest_gates and len(idx):
            prep = k.get('prep_stock')
            if prep is None or np.shape(prep) != (n, nlev):
                raise RuntimeError(
                    "tutoring.py: k['prep_stock'] (N, nlev) is required by contract §2/§5 but is missing or "
                    f"mis-shaped (got {None if prep is None else np.shape(prep)}). engine-core core.py not landed."
                )
            rho = float(p['contest_prep_depreciation'])
            prep_pre = np.array(k['prep_stock'], dtype=float, copy=True)   # audit snapshot (before decay)
            if rho > 0.0:
                # contract §5: depreciation applies every year, for every attending child, every gate
                k['prep_stock'][att] *= (1.0 - rho)
            price = float(p['contest_price'])
            tax_rate = float(p['contest_tax_rate'])
            unit_outlay = price * (1.0 + tax_rate)          # household unit outlay (budget)
            unit_net = unit_outlay - self._rebate_rate(p) * tax_rate * price   # net-of-rebate unit cost (choice)
            unit_net = max(unit_net, 0.0)
            pos_share = self._positional_share(p)
            learn_gain = self._learning_gain(p)
            e_cap = float(p['contest_max_e'])
            g_i, voc_i = k['g'][idx], k['voc'][idx]
            # each contest gate's candidate pool is authoritative (contract §6: cred==m, academic/track filtered);
            # a child prepares only while studying the level whose gate it will sit (depreciation makes early
            # effort decay, and the expected probability is priced over the same-year pool the gate uses).
            assigned = np.full(n, -1, int)
            gate_masks = {}
            for m_, gt in contest_gates:
                cand_mask = self._as_mask(self._require(E, 'contest_candidates')(m_), n)
                gate_masks[m_] = cand_mask
                elig_m = att & cand_mask & (assigned < 0)
                if gt.get('academic_only'):
                    elig_m &= ~voc_i
                assigned[elig_m] = m_
            method = p.get('contest_prob_method', 'auto')
            for m_, gt in contest_gates:
                sub = np.flatnonzero(assigned == m_)
                if len(sub) == 0:
                    continue
                cand_mask = gate_masks[m_]
                assigned_any[sub] = True
                dV = self._prize_dv(E, m_, sub)
                seats = int(self._require(E, 'contest_seats')(m_))
                pids_full, w_full = self._unpack_pids_weights(self._require(E, 'contest_weights')(m_), None)
                if pids_full is None:
                    cand_idx = np.flatnonzero(cand_mask)
                    pids_full = np.asarray(k['pid'][cand_idx], dtype=np.int64) if 'pid' in k else cand_idx
                n_cand = w_full.size
                seats_eff = min(max(seats, 0), n_cand)
                yy = np.maximum(k['y'][sub], 0.05)
                cash_rem = np.maximum(E._cash[sub] - pre_contest_spend[sub], 0.0)
                if unit_outlay > 0.0:
                    e_hi = np.minimum(e_cap, cash_rem / unit_outlay)
                else:
                    e_hi = np.full(len(sub), e_cap, dtype=float)
                e_hi = np.maximum(e_hi, 0.0)
                mvl_sub = np.asarray(E.mvl_all(t))[sub]              # value of one grade-equivalent of learning
                learn_value = mvl_sub * learn_gain                   # value units per unit of prep effort (learning)
                active = (e_hi > 0.0) & ((dV > 0.0) | (learn_value > 0.0))
                e_opt = np.zeros(len(sub))
                n_steps = _PREP_GRID.size - 1
                if active.any() and seats_eff < n_cand:
                    prep_col = np.asarray(k['prep_stock'][sub, m_], dtype=float)
                    cost_norm = unit_net / yy                         # value units: money / household income
                    # --- explicit proportional grid over each child's own [0, e_hi] (one batched call/point)
                    U_grid = np.full((_PREP_GRID.size, len(sub)), -np.inf)
                    act = np.flatnonzero(active)
                    # One batched probability call for the whole grid. Each point is an
                    # independent evaluation of the same deterministic function, so this is
                    # exactly equivalent to the per-point loop; on the GPU backend (amendment
                    # A-GPU-1) it becomes a single batched kernel instead of 9 sequential calls.
                    _Ws = []
                    for gi, frac in enumerate(_PREP_GRID):
                        e_try = frac * e_hi
                        over = np.where(active, prep_col + pos_share * e_try, prep_col)
                        _Ws.append(self._weights_with_override(E, m_, pids_full, w_full, sub, over))
                    _Palls = _pl_win_probs_batch(_Ws, seats_eff, method=method)
                    prob_evals += len(_Ws)
                    for gi, frac in enumerate(_PREP_GRID):
                        e_try = frac * e_hi
                        # candidate order in w_full corresponds to the candidate mask; select sub positions
                        Psub = self._p_sub(_Palls[gi], sub, cand_mask)
                        U_grid[gi, act] = (dV[act] * Psub[act] + learn_value[act] * e_try[act]
                                           - cost_norm[act] * e_try[act])
                    best_j = np.argmax(U_grid, axis=0)
                    u_best = U_grid[best_j, np.arange(len(sub))]
                    f_best = _PREP_GRID[best_j].copy()
                    # --- analytic local search: parabola through (best-1, best, best+1); interior nodes only
                    interior = (best_j > 0) & (best_j < n_steps)
                    j = best_j
                    ar = np.arange(len(sub))
                    u_lo = U_grid[np.maximum(j - 1, 0), ar]
                    u_hi = U_grid[np.minimum(j + 1, n_steps), ar]
                    denom = u_lo - 2.0 * u_best + u_hi            # < 0 when the best node is interior
                    h = 1.0 / n_steps
                    with np.errstate(divide='ignore', invalid='ignore'):
                        offset = np.where(interior & (np.abs(denom) > 1e-300),
                                          0.5 * (u_lo - u_hi) / denom * h, 0.0)
                    offset = np.clip(np.nan_to_num(offset, nan=0.0, posinf=0.0, neginf=0.0), -0.5 * h, 0.5 * h)
                    f_best = np.clip(f_best + offset, 0.0, 1.0)
                    # conservative bounding error: a vertex at half a grid step can add at most |denom|/8
                    with np.errstate(divide='ignore', invalid='ignore'):
                        rel = np.where(np.abs(u_best) > 1e-12, np.abs(denom) / 8.0 / np.abs(u_best),
                                       np.abs(denom) / 8.0)
                    grid_bound = max(grid_bound, float(np.max(rel[active])) if active.any() else 0.0)
                    e_opt = np.clip(f_best, 0.0, 1.0) * e_hi
                    # the e=0 corner is grid node 0: keep effort only if it beats the zero-effort utility
                    e_opt = np.where(u_best > U_grid[0, :] + 1e-12, e_opt, 0.0)
                elif active.any():
                    # a universal seat has P==1 for every candidate: no positional return (learning channel may
                    # still make effort worthwhile when learn_gain > 0, handled by the learning term below)
                    cost_norm = unit_net / yy
                    worth = learn_value - cost_norm
                    e_opt = np.where(worth > 0.0, e_hi, 0.0)
                # ---- fiscal ledger + prep stock (contract §4.1-§4.3, §5)
                e_opt = np.minimum(e_opt, e_hi)
                res_cost[sub] = price * e_opt
                tut_tax[sub] = tax_rate * res_cost[sub]
                tut_outlay[sub] = res_cost[sub] + tut_tax[sub]          # exact identity
                gov_tax[sub] = tut_tax[sub]
                if p['contest_rebate_policy'] != 'none':
                    rebate[sub] = self._rebate_rate(p) * tut_tax[sub]
                k['prep_stock'][sub, m_] += pos_share * e_opt
                contest_e_now[sub] = e_opt
                k['contest_e'][sub] = e_opt
                if learn_gain > 0.0:
                    y['tut_gain'][sub] += learn_gain * e_opt
                if np.any(cand_mask):
                    prep_stock_mean[m_] = float(np.mean(k['prep_stock'][cand_mask, m_]))
                contest_assigned_gate[sub] = m_
                # ---- binding assertions (contract §4.2: not assumed, asserted)
                assert np.all(e_opt <= e_hi + 1e-12), "contest effort exceeded the cap/cash bound e_hi"
                assert np.all(contest_e_now[sub] <= e_cap + 1e-12), "annual effort cap violated"
                assert np.all(tut_outlay[sub] <= cash_rem + 1e-9), "contest outlay exceeded residual cash"
            # `k['contest_e']` is THIS-YEAR flow only (assigned, never accumulated; contract §5)
            k['contest_e'][~assigned_any] = 0.0
            y['extra_spend'] += tut_outlay
            # per-child yearly tutoring outlay cannot exceed core's residual liquidity (contract §4.2)
            assert np.all(y['extra_spend'][att] <= E._cash[att] + 1e-9), "tutoring outlay exceeded E._cash"
            # exact financial identities (contract §4.1)
            assert np.array_equal(tut_outlay, res_cost + tut_tax), "tut_outlay != res_cost + tut_tax"
            assert abs(float(gov_tax.sum()) - float(tut_tax.sum())) <= 1e-12 * max(1.0, float(tut_tax.sum())), \
                "government receipts != sum of taxes"
            # derived per-year arrays: the fiscal ledger the accounting tests read (contract §4.1)
            E.yr['res_cost'] = res_cost
            E.yr['tut_tax'] = tut_tax
            E.yr['tut_outlay'] = tut_outlay
            E.yr['gov_tut_tax'] = gov_tax
            # derived audit state (recurrence/identity checks; not read by any probability path)
            E.yr['prep_stock_pre'] = prep_pre
            E.yr['contest_effort'] = contest_e_now
            E.yr['contest_assigned_gate'] = contest_assigned_gate
            E.yr['contest_prob_evals'] = int(prob_evals)
            E.yr['contest_grid_bound'] = float(grid_bound)
            if p['contest_rebate_policy'] != 'none':
                E.yr['rebate'] = rebate
        y['tut_kind'] = choice

        # ---- reporting (existing keys keep their names and meaning; new keys are additive, contract §4.3)
        g = k['g']
        k12 = att & (g < 12)
        k['tut_k12'] += np.where(k12, y['extra_spend'], 0.0)
        tut_any = (choice > 0) | (contest_e_now > 1e-4)
        G = E.ends[-1]
        by_grade = [float((tut_any & att & (g == j)).sum() / max((att & (g == j)).sum(), 1)) for j in range(G)]
        own_g = [float((own & att & (g == j)).sum() / max((att & (g == j)).sum(), 1)) for j in range(G)]
        firm_g = [float(((firm | (contest_e_now > 1e-4)) & att & (g == j)).sum() / max((att & (g == j)).sum(), 1))
                  for j in range(G)]
        by_q = [float((tut_any & att & (k['q'] == j)).sum() / max((att & (k['q'] == j)).sum(), 1)) for j in range(5)]
        k12_rate_q = [float((tut_any & k12 & (k['q'] == j)).sum() / max((k12 & (k['q'] == j)).sum(), 1))
                      for j in range(5)]
        k12_spend_q = [float(y['extra_spend'][k12 & (k['q'] == j)].mean()) if (k12 & (k['q'] == j)).any() else 0.0
                       for j in range(5)]
        g12_mask = att & (g == 11)

        def _bq(arr, mask):
            return [float(arr[mask & (k['q'] == j)].mean()) if (mask & (k['q'] == j)).any() else 0.0
                    for j in range(5)]

        assigned_mask = assigned_any & att
        k12_count_q = [int((k12 & (k['q'] == j)).sum()) for j in range(5)]
        assigned_count_q = [int((assigned_mask & (k['q'] == j)).sum()) for j in range(5)]
        contest_effort_q = _bq(contest_e_now, assigned_mask)
        contest_outlay_q = _bq(tut_outlay, k12)
        contest_res_q = _bq(res_cost, k12)
        contest_tax_q = _bq(tut_tax, k12)
        rebate_total = float(rebate.sum())
        rebate_recipients = int((rebate > 0.0).sum())

        E.note(tut_rate=float(tut_any[att].mean()) if att.any() else 0.0, tut_by_grade=by_grade,
               tut_own_by_grade=own_g, tut_firm_by_grade=firm_g, tut_by_q=by_q, firm_price=pf,
               tut_spend=float(y['extra_spend'][att].sum()),
               firm_rev=float(pf * (firm & att).sum() + res_cost.sum()),  # commercial revenue = RESOURCE cost only
               own_share=float(own.sum() / max(tut_any.sum(), 1)),
               tut_k12_rate=float(tut_any[k12].mean()) if k12.any() else 0.0,
               tut_k12_spend=float(y['extra_spend'][k12].sum()),
               tut_k12_rate_by_q=k12_rate_q,
               tut_k12_spend_by_q=k12_spend_q,
               tut_g12_rate=float(tut_any[g12_mask].mean()) if g12_mask.any() else 0.0,
               contest_e_mean=float(contest_e_now[k12].mean()) if k12.any() else 0.0,
               # ---- new additive contest-ledger series (contract §4.3)
               contest_spend_now=float(tut_outlay.sum()),          # household OUTLAY (backward-compatible name)
               contest_resource_cost=float(res_cost.sum()),
               contest_tax_paid=float(tut_tax.sum()),
               gov_tut_receipt=float(gov_tax.sum()),
               contest_outlay_by_q=contest_outlay_q,
               contest_res_cost_by_q=contest_res_q,
               contest_tax_by_q=contest_tax_q,
               contest_effort_by_q=contest_effort_q,
               contest_prep_stock_mean=prep_stock_mean,
               contest_rebate_total=rebate_total,
               contest_rebate_recipients=rebate_recipients,
               contest_learning_added=float(learn_gain * float(contest_e_now[att].sum())) if learn_gain > 0 else 0.0,
               contest_k12_count_by_q=k12_count_q,
               contest_assigned_count_by_q=assigned_count_q,
               contest_prob_evals=int(prob_evals),
               contest_grid_bound=float(grid_bound))

    # candidate-order helper: `cand_mask` indexes the full kid array; `sub` are kid indices.
    @staticmethod
    def _p_sub(P_all, sub, cand_mask):
        """Select P for kid indices `sub` out of a candidate-ordered probability vector."""
        pos = np.searchsorted(np.flatnonzero(cand_mask), sub)
        return P_all[np.minimum(pos, P_all.size - 1)]

    # ------------------------------------------------------------------ summary
    @staticmethod
    def _finite_col_means(R, key, m):
        """Column means over the measured window ignoring NaNs (non-contest gate columns are NaN by design)."""
        arr = np.array(R[key][m:], float)
        if arr.ndim == 1:
            arr = arr[:, None]
        out = []
        for j in range(arr.shape[1]):
            col = arr[:, j]
            fin = np.isfinite(col)
            out.append(float(col[fin].mean()) if fin.any() else float('nan'))
        return out

    def summary(self, E):
        R, m = E.R, E.p['measure_from']

        def A(key, nan=False):
            fn = np.nanmean if nan else np.mean
            return fn(np.array(R[key][m:], float), 0)

        out = dict(tut_rate=float(A('tut_rate')), tut_by_grade=list(A('tut_by_grade')),
                   tut_own_by_grade=list(A('tut_own_by_grade')), tut_firm_by_grade=list(A('tut_firm_by_grade')),
                   tut_by_q=list(A('tut_by_q')), firm_price=float(A('firm_price')), own_share=float(A('own_share')),
                   tut_k12_rate=float(A('tut_k12_rate')), tut_k12_spend=float(A('tut_k12_spend')),
                   tut_k12_rate_by_q=list(A('tut_k12_rate_by_q')), tut_k12_spend_by_q=list(A('tut_k12_spend_by_q')),
                   tut_g12_rate=float(A('tut_g12_rate')), contest_e_mean=float(A('contest_e_mean')))
        # additive contest-ledger summary keys, same names as the E.R series (contract §4.3)
        for key in ('contest_spend_now', 'contest_resource_cost', 'contest_tax_paid', 'gov_tut_receipt',
                    'contest_rebate_total', 'contest_rebate_recipients', 'contest_prob_evals',
                    'contest_grid_bound'):
            out[key] = float(A(key)) if key in R else 0.0
        for key in ('contest_outlay_by_q', 'contest_res_cost_by_q', 'contest_tax_by_q', 'contest_effort_by_q',
                    'contest_prep_stock_mean'):
            out[key] = self._finite_col_means(R, key, m) if key in R else []
        out['contest_rebate_recipient'] = ('households'
                                           if E.p['contest_rebate_policy'] != 'none' else 'none')
        return out


def _pl_win_probs(weights, seats, method='auto'):
    """Contract §1.3 expected probability: the one canonical Plackett-Luce module (no private PL here).

    Applies the same documented seat-sum renormalisation as core's `Engine._pl_probs`, so tutoring prices
    effort with exactly the probability vector `values()` sees.
    """
    try:
        from ..contest_math import pl_win_probs
    except ImportError as exc:  # pragma: no cover - contest_math.py is a Gate-1c deliverable
        raise RuntimeError(
            "tutoring.py: eduengine.contest_math.pl_win_probs is required for the contest expected "
            f"probability (contract §1.3/§6); import failed ({exc}). No fallback to 1-exp(-lam x^r)."
        ) from exc
    P = np.asarray(pl_win_probs(weights, seats, method=method), dtype=float)
    seats = int(min(max(int(seats), 0), P.size))
    if seats > 0 and P.size:
        total = float(P.sum())
        if total > 0.0:
            P = P * (seats / total)
    return P


def _pl_win_probs_batch(weight_rows, seats, method='auto'):
    """Batched form of :func:`_pl_win_probs` for the 9-point prep grid.

    Delegates to ``contest_math.pl_win_probs_batch``, which is bit-identical to the per-point
    loop on the default CPU backend and uses one GPU batch under amendment A-GPU-1. The same
    documented seat-sum renormalisation is applied per row.
    """
    try:
        from ..contest_math import pl_win_probs_batch
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "tutoring.py: eduengine.contest_math.pl_win_probs_batch is required for the batched "
            f"contest expected probability (contract §1.3/§6); import failed ({exc})."
        ) from exc
    W = np.asarray(weight_rows, dtype=float)
    if W.ndim != 2 or W.shape[0] == 0:
        raise ValueError("_pl_win_probs_batch expects a non-empty (B, n) weight array")
    P = np.asarray(pl_win_probs_batch(W, seats, method=method), dtype=float)
    seats = int(min(max(int(seats), 0), P.shape[1]))
    if seats > 0 and P.shape[1]:
        totals = P.sum(axis=1)
        scale = np.where(totals > 0.0, seats / np.where(totals > 0.0, totals, 1.0), 1.0)
        P = P * scale[:, None]
    return P
