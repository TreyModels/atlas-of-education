# Tullock Contest Gate Spec (`engine/eduengine/core.py` & `engine/eduengine/modules/tutoring.py`)

Apply against `research/binding-gate-2026-11-25` (HEAD `68da16e`):

1. **`CORE_DEFAULTS` in `engine/eduengine/core.py`**:
   ```python
   contest_r=1.5, contest_alpha=1.2, contest_price=0.12,
   contest_x0=2.0, contest_max_e=4.0, contest_decay=0.0,
   ```

2. **`Engine.__init__` & cohort spawn in `engine/eduengine/core.py`**:
   ```python
   self.crowd = [max(1.0, 1.0 / max(g.get('share', 1.0), 0.05)) if g['kind'] == 'contest' else 1.0
                 for g in p['gates']]
   self.contest_e = [0.0 for _ in p['gates']]
   # In cohort dict:
   contest_e=np.zeros(N),
   ```

3. **`Engine.values()` in `engine/eduengine/core.py`**:
   ```python
   if gate['kind'] == 'contest':
       if self.crowd[m] <= 1.0:
           P = np.ones(n)
       else:
           r_c = gate.get('contest_r', p['contest_r'])
           a_c = gate.get('contest_alpha', p['contest_alpha'])
           ce = np.where(lev_now == m, k['contest_e'][sl], 0.0)
           z_c = r_c * (Lend + a_c * np.log1p(ce) - self.cut[m]) / p['exam_sd']
           P = 1.0 / (1.0 + np.exp(-np.clip(z_c, -30, 30)))
   else:
       ref = gate['bar'] if gate['kind'] == 'bar' else self.cut[m]
       P = ndtr((Lend - ref) / p['exam_sd'])
   ```

4. **`Engine.contest_prep(self, t)` (called in `Engine.step()` right before `m.extras(self, t)`)**:
   ```python
   def contest_prep(self, t):
       p, k, y = self.p, self.kids, self.yr
       if not any(g['kind'] == 'contest' for g in p['gates']):
           return
       att = k['att']
       if not att.any():
           return
       n = len(att)
       e_buy, spend = np.zeros(n), np.zeros(n)
       for m_ in range(self.nlev):
           gate = p['gates'][m_]
           if gate['kind'] != 'contest' or self.closed[m_] or self.crowd[m_] <= 1.0:
               continue
           prev_contest = any(p['gates'][j]['kind'] == 'contest' and not self.closed[j] for j in range(m_))
           idx = np.flatnonzero(att & (k['cred'] == m_) if prev_contest else att & (k['cred'] <= m_))
           if not len(idx):
               continue
           pe = gate.get('contest_price', p['contest_price'])
           x0 = gate.get('contest_x0', p['contest_x0'])
           emax = gate.get('contest_max_e', p['contest_max_e'])
           yrs_left = np.maximum(self.ends[m_] - k['g'][idx], 1)
           prize_step = gate.get('elite_logw', max(float(self.B[m_ + 1] - self.B[m_]), 0.05))
           prize = (p['delta'] ** yrs_left) * p['kappa'] * prize_step
           A = (self.crowd[m_] - 1.0) * (x0 + self.contest_e[m_])
           yy = np.maximum(k['y'][idx], 0.05)
           e_star = np.sqrt(np.maximum(prize * A * yy / max(pe, 1e-6), 0.0)) - A - x0 - k['contest_e'][idx]
           cap = np.minimum(emax, np.maximum(self._cash[idx], 0.0) / max(pe, 1e-6))
           e_opt = np.where(e_star >= 0.25, np.clip(e_star, 0.0, cap), 0.0)
           e_opt = np.where(e_opt >= 0.25, e_opt, 0.0)
           e_buy[idx], spend[idx] = e_opt, pe * e_opt
           self._cash[idx] -= spend[idx]
       k['contest_e'] += e_buy
       y['contest_e'] = e_buy
       y['extra_spend'] += spend
   ```

5. **Gate resolution in `Engine.step()` (`elif gate['kind'] == 'contest':`)**:
   - Compute `seats = max(1, int(round(gate['share'] * p['N'])))`, `gi = np.flatnonzero(at_gate)`, `n_app = len(gi)`.
   - Update `self.crowd[m_]` and `self.contest_e[m_]` via `0.7 / 0.3` EMA.
   - Draw Plackett-Luce / Gumbel-max `c_score = r_c * (s_eff[gi] / p['exam_sd']) + (-np.log(-np.log(u_g)))`, admit top `seats`, update `self.cut[m_]`, reset `k['contest_e'][passed] = 0.0`.
   - For `fail='track'`, non-winners continue to regular tertiary track without exiting school.

6. **`TutoringMarket` in `engine/eduengine/modules/tutoring.py`**:
   - Define `ce = y.get('contest_e', np.zeros(n)) > 0` and `any_tut = (choice > 0) | ce`; compute `tut_rate`, `tut_by_grade`, `tut_by_q`, `firm_rev`, and `own_share` over `any_tut`.
