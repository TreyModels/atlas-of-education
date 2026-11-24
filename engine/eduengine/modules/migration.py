"""Rural-to-urban migration/sorting (declared extension; illustrative, not calibrated).

The engine otherwise treats urban/rural as a fixed household attribute drawn at entry. This module
lets rural households move to urban areas at the start of a year, before continuation decisions, with
a declared probability that rises with the child's credential, ability, household income and home
capital and falls with migration friction. On moving, the household takes the engine's declared urban
income premium and urban school-quality premium, and rural distance/tutoring-access costs stop
applying. No remittances, no urban-to-rural moves, no spatial job access, no country calibration.

Switch: migration ∈ {'low','high'} installs the module; 'closed' does not (baseline bit-identical).
"""
import numpy as np
from ..core import Module


class Migration(Module):
    name = 'migration'
    defaults = dict(
        migration='closed',                # 'closed' (no module), 'low', 'high' friction
        migration_cred=0.35,               # credential weight in the move logit
        migration_ability=0.45,            # child ability weight
        migration_income=0.30,             # log household income weight
        migration_home=0.30,               # home-capital weight
        migration_max_age=18,              # oldest age at which a household moves
    )

    def setup(self, E):
        level = E.p.get('migration', 'closed')
        self.friction = 2.2 if level == 'low' else 4.0 if level == 'high' else None
        self.moved = 0
        self.considered = 0

    def supply(self, E, t):
        if self.friction is None:
            return
        p, k, r = E.p, E.kids, E.rng
        age = E.age(t)
        active = (k['reason'] < 0) & (~k['urban']) & (age >= p['entry_age']) & (age <= p['migration_max_age'])
        idx = np.flatnonzero(active)
        self.considered += int(len(idx))
        if len(idx) == 0:
            return
        logy = np.log(np.maximum(k['y'][idx], 1e-6) / max(p['y_median'], 1e-6))
        z = (-self.friction
             + p['migration_cred'] * k['cred'][idx]
             + p['migration_ability'] * k['a'][idx]
             + p['migration_income'] * logy
             + p['migration_home'] * (k['home'][idx] - 0.5))
        pr = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        move = idx[r.random(len(idx)) < pr]
        if len(move):
            k['urban'][move] = True
            k['y'][move] *= p['urban_income']
            k['q'][move] = np.clip(k['q'][move] + 0.05, 0.2, 1.0)
            self.moved += int(len(move))

    def summary(self, E):
        return dict(migration_rate_by_child=float(self.moved / max(self.considered, 1)) if self.friction is not None else 0.0,
                    migration_moves=int(self.moved))
