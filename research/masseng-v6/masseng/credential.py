"""MASSENG v5 with optional annual array admissions; defaults preserve v5."""
import json
from pathlib import Path
import numpy as np
from .engine import Model, Result, PUB, PRIV, N_GRADES, LEVEL_NAMES, _sigmoid
from .array_admissions import clear_two_sector_array

SCENARIO_ROOT = Path(__file__).resolve().parent.parent / 'countries'


def interpolate_knots(knots, years):
    points = sorted((int(k), float(v)) for k, v in knots.items() if not k.startswith('_'))
    if not points:
        raise ValueError('scenario path requires at least one point')
    return np.interp(years, [v[0] for v in points], [v[1] for v in points])


class CredentialModel(Model):
    def __init__(self, country, params=None, scenario=None, mechanism=None,
                 supply_rule=None, demand_form='income', switches=None,
                 burden_form='log', split_income=True, split_nu=False, annual_market=False):
        super().__init__(country, params=params, supply_rule=supply_rule,
                         demand_form=demand_form, switches=switches,
                         burden_form=burden_form, split_income=split_income, split_nu=split_nu)
        self.annual_market = bool(annual_market)
        self.market_scenario = None
        if self.annual_market:
            self.market_scenario = json.loads((SCENARIO_ROOT / country.iso3 / 'market_scenario.json').read_text())
        if scenario is None:
            scenario = json.loads((SCENARIO_ROOT / country.iso3 / 'credential_scenario.json').read_text())
        self.scenario = scenario
        self.mechanism = dict(scenario['mechanism'])
        if mechanism:
            self.mechanism.update(mechanism)
        for name in ('relational', 'positional', 'human_return', 'government', 'eta_formal', 'cost_insurance'):
            self.mechanism.setdefault(name, [0.0] * 4)
            value = self.mechanism[name]
            if np.isscalar(value):
                self.mechanism[name] = np.full(4, float(value))
            else:
                if len(value) != 4:
                    raise ValueError(f'{name} needs 4 coefficients, one per school level')
                self.mechanism[name] = np.asarray(value, dtype=float)
        self.max_deferral = int(self.mechanism.get('max_deferral', 0))
        self.defer_fraction = float(self.mechanism.get('defer_fraction', 0.0))
        self.defer_retention = float(self.mechanism.get('defer_retention', 0.0))
        if not 0 <= self.max_deferral <= 8:
            raise ValueError('max_deferral must be between 0 and 8 years')
        if not 0 <= self.defer_fraction <= 1 or not 0 <= self.defer_retention <= 1:
            raise ValueError('defer fractions must be probabilities')
        paths = scenario['declared_paths']
        self.formal_path = np.stack([interpolate_knots(paths['formal_threshold'][lev], self.years) for lev in LEVEL_NAMES], axis=1)
        self.return_path = np.stack([interpolate_knots(paths['relative_wage_return'][lev], self.years) for lev in LEVEL_NAMES], axis=1)
        if (self.formal_path < 0).any() or (self.formal_path > 1).any() or (self.return_path < 0).any():
            raise ValueError('invalid declared path')
        self.required_years = np.array([next(v for y, v in sorted([(int(yr), int(n)) for yr, n in paths['compulsory_years'].items()], reverse=True) if y <= year) if any(int(yr) <= year for yr in paths['compulsory_years']) else int(next(iter(paths['compulsory_years'].values()))) for year in self.years])
        self.opportunity_fraction = np.asarray(scenario['cost_decomposition']['opportunity_fraction_by_level'], float)
        self.shadow_share = np.asarray(scenario['cost_decomposition']['shadow_share_of_cash_by_level'], float)
        if self.opportunity_fraction.shape != (4,) or self.shadow_share.shape != (4,):
            raise ValueError('cost decomposition requires four shares')
        if np.any(self.opportunity_fraction < 0) or np.any(self.opportunity_fraction > 1) or np.any(self.shadow_share < 0) or np.any(self.shadow_share > 1):
            raise ValueError('cost shares must be probabilities')

    def _annual_seats(self, year, level, public_override=None):
        if level == 0: start_age = self.band[year]['primary'][0]
        elif level == 1: start_age = self.band[year]['primary'][0] + 6
        elif level == 2: start_age = self.band[year]['primary'][0] + 6 + self.n_lower
        else: start_age = self.band[year]['tertiary'][0]
        reference_population = self._pop_at_age(year, start_age)
        if level == 2 and year < self.shs_from: reference_population = 0.0
        public = self.market_scenario['seat_coverage_public'][level] * reference_population
        private = self.market_scenario['seat_coverage_private'][level] * reference_population
        if public_override is not None: public = public_override
        return np.maximum(np.array([public, private], dtype=float), 0.0)

    def _gov_signal(self, yi, level, out):
        if level == 3: return 0.0
        compulsory = self.required_years[yi]
        coverage = [1.0, float(compulsory >= 10), float(compulsory >= 13), 0.0][level]
        if level == 2 and self.years[yi] < self.shs_from: return 0.0
        proxy = {0: 'ner_primary', 1: 'ner_secondary', 2: 'ner_secondary'}.get(level)
        lag = float(out[proxy][yi - 1]) / 100 if yi and np.isfinite(out[proxy][yi-1]) else 0.0
        return coverage * (1.0 - np.clip(lag, 0.0, 1.0))

    def _positional_signal(self, yi, level, out):
        if yi == 0 or level == 0: return 0.0
        source = ('ger_primary' if level == 1 else 'ger_secondary')
        value = out[source][yi - 1]
        return float(np.clip(value / 100, 0, 1)) if np.isfinite(value) else 0.0

    def _demand_by_level(self, yi, out):
        base = self._demand_term(yi)
        ln_national = float(np.log(self.gdp[yi] / self.gdp_ref))
        signals = []
        for li in range(4):
            q = self.formal_path[yi, li]; w = self.return_path[yi, li]; m = self.mechanism
            extra = (m['relational'][li] * q + m['positional'][li] * self._positional_signal(yi, li, out) + m['human_return'][li] * np.log1p(w) + m['government'][li] * self._gov_signal(yi, li, out) + m['eta_formal'][li] * q * ln_national)
            signals.append(base + extra)
        return signals

    def _free_v(self, yi, li):
        p = self.p; ans = np.zeros((10, 2), dtype=float)
        mu = p['mu_ter'] if li == 3 else p['mu_basic']
        nu = p['nu_ter'] if (li == 3 and self.split_nu) else p['nu']
        ans[:, PRIV] = mu + nu * self.lninc[yi]
        return ans

    def _v(self, yi, li):
        p = self.p; k = p['kappa'] if self.sw['cost'] else 0.0
        k /= 1.0 + float(self.mechanism['cost_insurance'][li]) * self.formal_path[yi, li]
        burden = (self.cost[yi, li, :][None, :] - self.transfer[yi, :, li][:, None]).clip(0.0) / self.mult[yi][:, None]
        v = -k * (np.log1p(burden) if self.burden_form == 'log' else burden)
        mu = p['mu_ter'] if li == 3 else p['mu_basic']; nu = p['nu_ter'] if (li == 3 and self.split_nu) else p['nu']
        v[:, PRIV] += mu + nu * self.lninc[yi]
        return v

    def _record_spending(self, out, yi, E):
        persons = E * self.cohort[:, None, None, None]; by_decile = np.zeros((10, 3)); total_enrolled = 0.0
        for g in range(N_GRADES):
            li = self.level_of_grade[g]
            burden = (self.cost[yi, li, :][None, :] - self.transfer[yi, :, li][:, None]).clip(0.0)
            by_type = persons[:, :, g, :].sum(axis=0)
            full = (by_type * burden * self.gdp[yi]).sum(axis=1); cash = full * (1.0 - self.opportunity_fraction[li]); shadow = cash * self.shadow_share[li]
            by_decile[:, 0] += full; by_decile[:, 1] += cash; by_decile[:, 2] += shadow; total_enrolled += by_type.sum()
        out['hh_full_cost_total'][yi] = by_decile[:, 0].sum(); out['hh_cash_cost_total'][yi] = by_decile[:, 1].sum(); out['hh_shadow_cash_total'][yi] = by_decile[:, 2].sum(); out['hh_cash_per_student'][yi] = by_decile[:, 1].sum() / max(total_enrolled, 1)
        return by_decile

    def run(self, record_deciles=False):
        p = self.p; nb = self.b_hi - self.b_lo + 1
        E = np.zeros((nb, 10, N_GRADES, 2)); grads = np.zeros((nb, 10, 4)); drops = np.zeros((nb, 10)); aged = np.zeros((nb, 10)); entered = np.zeros((nb, 10)); notyet = np.full((nb, 10), 0.1)
        pending = np.zeros((self.max_deferral, nb, 10)); spending_deciles = []; stock_levels = np.zeros((len(self.years), 3, 10, 2), dtype=float)
        market_fields = ('eligible', 'latent_zero_cost', 'effective_at_cost', 'admitted', 'effective_public', 'effective_private', 'admitted_public', 'admitted_private', 'capacity_public', 'capacity_private', 'unmet_effective')
        markets = {k: np.zeros((len(self.years), 4, 10), dtype=float) for k in market_fields}; Y = self.years
        out = {k: np.full(len(Y), np.nan) for k in ['ger_primary', 'ner_primary', 'ger_secondary', 'ner_secondary', 'ger_tertiary', 'priv_primary', 'priv_secondary', 'priv_lower_secondary', 'priv_upper_secondary', 'priv_tertiary', 'ter_entrants', 'ter_rationed_share', 'k_ter', 'ter_first_year_headcount', 'ter_eligible_headcount', 'ter_pending_headcount', 'hh_cash_cost_total', 'hh_full_cost_total', 'hh_shadow_cash_total', 'hh_cash_per_student', 'gov_pressure_secondary', 'gov_pressure_upper_secondary', 'relational_threshold_tertiary', 'positional_pressure_tertiary']}
        dec_part = {}; k_ter = p['k_ter']; unmet_prev = 0.0; rc = self.cfg.get('repetition', {})
        rp, rs = rc.get('primary', p['rep_prim']), rc.get('secondary', p['rep_sec']); rep = np.array([rp, rs, rs, 0.0])
        a_within = np.array([p['a_prim'], p['a_sec'], p['a_sec'], p['a_ter']]); a_entry = np.array([p['a_prim'], p['a_sec_entry'], p['a_sec_entry'], p['a_ter_entry']]); bidx = np.arange(self.b_lo, self.b_hi + 1)
        for yi, y in enumerate(Y):
            age = y - 1 - bidx; alive = (age >= 5) & (age <= self.max_age); demands = self._demand_by_level(yi, out); mk = {k: np.zeros((4, 10), dtype=float) for k in market_fields}
            out['gov_pressure_secondary'][yi] = self._gov_signal(yi, 1, out); out['gov_pressure_upper_secondary'][yi] = self._gov_signal(yi, 2, out); out['relational_threshold_tertiary'][yi] = self.formal_path[yi, 3]; out['positional_pressure_tertiary'][yi] = self._positional_signal(yi, 3, out)
            V = [self._v(yi, li) for li in range(4)]; IV = [np.logaddexp(v[:, 0], v[:, 1]) for v in V]; share_priv = [np.exp(v[:, 1] - iv) for v, iv in zip(V, IV)]
            VF = [self._free_v(yi, li) for li in range(4)]; IVF = [np.logaddexp(v[:, 0], v[:, 1]) for v in VF]; free_pe = [_sigmoid(a_entry[li] + demands[li] + IVF[li]) for li in range(4)]
            newE = np.zeros_like(E); t1_pool = np.zeros((nb, 10))
            for g in range(N_GRADES):
                mass = E[:, :, g, :]
                if not mass.any(): continue
                li = self.level_of_grade[g]; stay = mass * rep[li]; passed = mass - stay; pc = _sigmoid(a_within[li] + demands[li][:, None] + V[li])
                newE[:, :, g, :] += stay * pc[None]; drops += (stay * (1 - pc[None])).sum(axis=2)
                if g == 5 or g == self.last_lower or g == 11 or g == 15:
                    tot = passed.sum(axis=2)
                    if g == 5: grads[:, :, 0] += 0; nxt_level = 1
                    elif g == self.last_lower: nxt_level = 2 if y >= self.shs_from else 3
                    elif g == 11: nxt_level = 3
                    else: grads[:, :, 3] += tot; continue
                    lvl_done = self.level_of_grade[g]
                    if nxt_level == 3: t1_pool += tot; continue
                    ng = self.first_grade[nxt_level]; pe = _sigmoid(a_entry[nxt_level] + demands[nxt_level] + IV[nxt_level]); cont = tot * pe[None]
                    sector_cont = cont[:, :, None] * np.stack([1-share_priv[nxt_level], share_priv[nxt_level]], axis=1)[None]
                    eligible = (tot * self.cohort[:, None]).sum(axis=0); accepted = (cont * self.cohort[:, None]).sum(axis=0)
                    mk['eligible'][nxt_level] += eligible; mk['latent_zero_cost'][nxt_level] += eligible * free_pe[nxt_level]; mk['effective_at_cost'][nxt_level] += accepted; mk['effective_public'][nxt_level] += accepted * (1 - share_priv[nxt_level]); mk['effective_private'][nxt_level] += accepted * share_priv[nxt_level]
                    if self.annual_market:
                        seats = self._annual_seats(y, nxt_level); admitted_persons, unmet = clear_two_sector_array(sector_cont * self.cohort[:, None, None], seats)
                        sector_cont = admitted_persons / self.cohort[:, None, None]; cont = sector_cont.sum(axis=2)
                        mk['admitted_public'][nxt_level] += admitted_persons[:, :, PUB].sum(axis=0); mk['admitted_private'][nxt_level] += admitted_persons[:, :, PRIV].sum(axis=0); mk['admitted'][nxt_level] += admitted_persons.sum(axis=(0, 2)); mk['capacity_public'][nxt_level] += seats[PUB] / 10; mk['capacity_private'][nxt_level] += seats[PRIV] / 10; mk['unmet_effective'][nxt_level] += unmet.sum(axis=0)
                    else:
                        mk['admitted'][nxt_level] += accepted; mk['admitted_public'][nxt_level] += accepted * (1 - share_priv[nxt_level]); mk['admitted_private'][nxt_level] += accepted * share_priv[nxt_level]
                    newE[:, :, ng, :] += sector_cont; grads[:, :, lvl_done] += tot - cont
                else:
                    newE[:, :, g + 1, :] += passed * pc[None]; drops += (passed * (1 - pc[None])).sum(axis=2)
            if t1_pool.any() and self.exam is not None:
                pr = self._pass_rate(y); failed = t1_pool * (1 - pr); grads[:, :, 1] += failed; t1_pool = t1_pool * pr
            fresh_pool = t1_pool.copy(); pending_old = pending.copy(); pending = np.zeros_like(pending)
            if self.max_deferral:
                active = (age <= self.max_age)
                if (~active).any(): grads[~active, :, 1] += pending_old[:, ~active, :].sum(axis=0); pending_old[:, ~active, :] = 0.0
                t1_pool += pending_old.sum(axis=0)
            eligible_ter = (t1_pool * self.cohort[:, None]).sum(axis=0); mk['eligible'][3] += eligible_ter; mk['latent_zero_cost'][3] += eligible_ter * free_pe[3]; out['ter_eligible_headcount'][yi] = eligible_ter.sum()
            if t1_pool.any():
                pe_both = _sigmoid(a_entry[3] + demands[3] + IV[3]); pe_priv = _sigmoid(a_entry[3] + demands[3] + V[3][:, PRIV]); sp = share_priv[3]
                mk['effective_at_cost'][3] += eligible_ter * pe_both; mk['effective_public'][3] += eligible_ter * pe_both * (1 - sp); mk['effective_private'][3] += eligible_ter * pe_both * sp
                pop_entry = self._pop_at_age(y, self.band[y]['tertiary'][0]); persons = t1_pool * self.cohort[:, None]; want_pub = (persons * (pe_both * (1 - sp))[None]).sum(); cap = self._capacity(y, k_ter, unmet_prev) * pop_entry; f = 1.0 if self.supply_rule == 'unconstrained' or want_pub <= cap else cap / want_pub
                if self.annual_market:
                    seats = self._annual_seats(y, 3, public_override=cap if np.isfinite(cap) else None); demand_sector = persons[:, :, None] * (pe_both[:, None] * np.stack([1-sp, sp], axis=1))[None]; admitted_persons, unmet = clear_two_sector_array(demand_sector, seats); admitted_share = admitted_persons / self.cohort[:, None, None]
                    to_pub = admitted_share[:, :, PUB]; to_priv = admitted_share[:, :, PRIV]; pub_accepted = admitted_persons[:, :, PUB].sum(axis=0); priv_accepted = admitted_persons[:, :, PRIV].sum(axis=0); mk['capacity_public'][3] += seats[PUB] / 10; mk['capacity_private'][3] += seats[PRIV] / 10; mk['unmet_effective'][3] += unmet.sum(axis=0)
                else:
                    to_pub = t1_pool * (f * pe_both * (1 - sp))[None]; to_priv = t1_pool * (f * pe_both * sp + (1 - f) * pe_priv)[None]; pub_accepted = (to_pub * self.cohort[:, None]).sum(axis=0); priv_accepted = (to_priv * self.cohort[:, None]).sum(axis=0)
                mk['admitted_public'][3] += pub_accepted; mk['admitted_private'][3] += priv_accepted; mk['admitted'][3] += pub_accepted + priv_accepted; newE[:, :, 12, PUB] += to_pub; newE[:, :, 12, PRIV] += to_priv
                admit_rate = np.divide(to_pub + to_priv, t1_pool, out=np.zeros_like(t1_pool), where=t1_pool != 0); fresh_left = fresh_pool * (1.0 - admit_rate); newly_deferred = fresh_left * self.defer_fraction if self.max_deferral else 0.0; grads[:, :, 1] += fresh_left - newly_deferred
                if self.max_deferral:
                    pending[0] += newly_deferred
                    for j in range(self.max_deferral):
                        left = pending_old[j] * (1.0 - admit_rate); kept = left * self.defer_retention if j + 1 < self.max_deferral else 0.0
                        if j + 1 < self.max_deferral: pending[j + 1] += kept
                        grads[:, :, 1] += left - kept
                out['ter_first_year_headcount'][yi] = ((to_pub + to_priv) * self.cohort[:, None]).sum(); out['ter_entrants'][yi] = out['ter_first_year_headcount'][yi] / max(pop_entry, 1); out['ter_rationed_share'][yi] = 1 - f; unmet_prev = max(0.0, want_pub - cap) / max(pop_entry, 1)
                if self.supply_rule == 'responsive': k_ter = self._capacity(y, k_ter, unmet_prev)
            out['k_ter'][yi] = self._capacity(y, k_ter, unmet_prev) if self.supply_rule != 'responsive' else k_ter; out['ter_pending_headcount'][yi] = (pending.sum(axis=0) * self.cohort[:, None]).sum()
            s6_now, s6_1, s6_2 = self.s6[yi], self.s6[max(yi - 1, 0)], self.s6[max(yi - 2, 0)]; lam = p['late']; share_at = {6: s6_now * (1 - lam), 7: (1 - s6_1) * (1 - lam) + s6_1 * lam, 8: (1 - s6_2) * lam}; pe0 = _sigmoid(a_entry[0] + demands[0] + IV[0]); primary_demand = np.zeros((nb, 10, 2))
            for a, sh in share_at.items():
                m = age == a
                if m.any():
                    ent = 0.1 * sh * pe0; sector_ent = np.zeros((nb, 10, 2)); sector_ent[m, :, PUB] = ent[None] * (1 - share_priv[0])[None]; sector_ent[m, :, PRIV] = ent[None] * share_priv[0][None]; cweighted = self.cohort[m].sum()
                    mk['eligible'][0] += 0.1 * sh * cweighted; mk['latent_zero_cost'][0] += 0.1 * sh * cweighted * free_pe[0]; mk['effective_at_cost'][0] += ent * cweighted; mk['effective_public'][0] += ent * cweighted * (1 - share_priv[0]); mk['effective_private'][0] += ent * cweighted * share_priv[0]
                    if self.annual_market: primary_demand += sector_ent
                    else:
                        mk['admitted'][0] += ent * cweighted; mk['admitted_public'][0] += ent * cweighted * (1 - share_priv[0]); mk['admitted_private'][0] += ent * cweighted * share_priv[0]; entered[m] += ent[None]; notyet[m] -= ent[None]; newE[m, :, 0, :] += sector_ent[m]
            hz = np.zeros(nb)
            if self.late_hazard > 0: hz[(age >= 9) & (age <= self.late_max_age)] = self.late_hazard
            if self.catch_up and self.catch_up['years'][0] <= y <= self.catch_up['years'][1]: hz[(age >= 7) & (age <= self.catch_up['max_age'])] = np.maximum(hz[(age >= 7) & (age <= self.catch_up['max_age'])], self.catch_up['rate'])
            if hz.any():
                considered = notyet * hz[:, None]; ent = considered * pe0[None]; pcandidates = (considered * self.cohort[:, None]).sum(axis=0); paccepted = (ent * self.cohort[:, None]).sum(axis=0)
                mk['eligible'][0] += pcandidates; mk['latent_zero_cost'][0] += pcandidates * free_pe[0]; mk['effective_at_cost'][0] += paccepted; mk['effective_public'][0] += paccepted * (1 - share_priv[0]); mk['effective_private'][0] += paccepted * share_priv[0]; sector_ent = ent[:, :, None] * np.stack([1-share_priv[0], share_priv[0]], axis=1)[None]
                if self.annual_market: primary_demand += sector_ent
                else:
                    mk['admitted'][0] += paccepted; mk['admitted_public'][0] += paccepted * (1 - share_priv[0]); mk['admitted_private'][0] += paccepted * share_priv[0]; entered += ent; notyet -= ent; newE[:, :, 0, :] += sector_ent
            if self.annual_market:
                seats = self._annual_seats(y, 0); admitted_persons, unmet = clear_two_sector_array(primary_demand * self.cohort[:, None, None], seats); admitted_share = admitted_persons / self.cohort[:, None, None]; ent = admitted_share.sum(axis=2)
                mk['admitted_public'][0] += admitted_persons[:, :, PUB].sum(axis=0); mk['admitted_private'][0] += admitted_persons[:, :, PRIV].sum(axis=0); mk['admitted'][0] += admitted_persons.sum(axis=(0, 2)); mk['capacity_public'][0] += seats[PUB] / 10; mk['capacity_private'][0] += seats[PRIV] / 10; mk['unmet_effective'][0] += unmet.sum(axis=0); entered += ent; notyet -= ent; newE[:, :, 0, :] += admitted_share
            aged[~alive] += newE[~alive].sum(axis=(2, 3)); newE[~alive] = 0.0; E = newE; self._record(out, yi, y, E, age, record_deciles, dec_part); persons = E * self.cohort[:, None, None, None]
            for lx, sl in enumerate((slice(0, 6), slice(6, 12), slice(12, 16))): stock_levels[yi, lx] = persons[:, :, sl, :].sum(axis=(0, 2))
            spending_deciles.append(self._record_spending(out, yi, E))
            for key in market_fields: markets[key][yi] = mk[key]
        return Result(Y, out, dict(deciles=dec_part, grads=grads, drops=drops, aged=aged, entered=entered, final_enrolled=E.sum(axis=(2, 3)), pending=pending.sum(axis=0), spending_deciles=np.array(spending_deciles), markets=markets, stock_levels=stock_levels, events=self.events_applied))
