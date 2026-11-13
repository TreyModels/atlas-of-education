"""Anchor: completion wedges (strut S0). The engine runs with a wedge per level (a utility term added to the value of
continuing that level) that follows a time path. settle.py finds the paths by iterating whole runs until completion
tracks the observed series ("the model settles into its history"). The wedge's size and sign say how much of history the
engine's causal variables do NOT explain (wedge accounting: Chari, Kehoe & McGrattan 2007; model discrepancy: Kennedy &
O'Hagan 2001). No paths = no wedge.
"""
import numpy as np
from ..core import Module, interp_path


class Anchor(Module):
    name = 'anchor'
    defaults = dict(wedge_paths={})            # {level: [(year, wedge), ...]}

    def supply(self, E, t):
        Y = E.year(t)
        for m, path in E.p['wedge_paths'].items():
            E.wedge[int(m)] = interp_path(path, Y)

    def after(self, E, t):
        E.note(wedge=E.wedge.copy())

    def summary(self, E):
        W = np.array(E.R['wedge'])
        return dict(wedge_mean=list(W[E.p['measure_from']:].mean(0)), wedge_absmax=list(np.abs(W).max(0)))
