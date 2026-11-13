"""Settling: find completion wedge paths so the engine reproduces observed completion, by iterating whole runs.

For an observation of level-m completion in year Yobs (UIS: cohort 3-5 years past the intended last grade), the decisions
that produced it were made about 4 + len(m)/2 years earlier; the wedge knot sits there. Each iteration moves every knot
by gain x (observed - model). Levels are settled together; damping keeps the coupling (a later level's wedge also
raises the value of earlier levels) from oscillating.
"""
import numpy as np
from . import measure as M


def settle(make, targets, iters=10, gain=3.0, clip=8.0, seeds=(0, 1), verbose=False):
    """make(**over) -> engine (with an Anchor module). targets: {level: {year: completion}}. Returns (paths, history)."""
    probe = make(seed=seeds[0])
    lv = {m: probe.p['levels'][m][1] for m in targets}
    knots = {m: {Y - 4 - lv[m] // 2: 0.0 for Y in targets[m]} for m in targets}
    hist = []
    for it in range(iters):
        paths = {m: sorted(knots[m].items()) for m in targets}
        Es = []
        for s in seeds:                        # settle against the average of several seeds, not one draw
            E = make(seed=s, wedge_paths=paths); E.run(); Es.append(E)
        err = []
        for m, obs in targets.items():
            for Y, v in obs.items():
                mv = float(np.nanmean([M.completion_cohort(E, m, Y) for E in Es]))
                if np.isfinite(mv):
                    k = Y - 4 - lv[m] // 2
                    knots[m][k] = float(np.clip(knots[m][k] + gain * (v - mv) * (0.7 ** it + 0.3), -clip, clip))
                    err.append(abs(v - mv))
        hist.append(float(np.mean(err)) if err else np.nan)
        if verbose:
            print(f'  settle iter {it}: mean |gap| {hist[-1]:.3f}')
    return {m: sorted(knots[m].items()) for m in targets}, hist
