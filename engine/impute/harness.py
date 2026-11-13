"""The hold-out harness: delete known points, impute them, score error by method and gap length.

Protocol (the one described in the A10/B11 to-do items, made operational):

  1. Pick blocks of consecutive years that are fully observed in the real panel.  Delete every
     cell of the block (value -> NaN, flag -> ''), keeping at least one observed anchor on each
     side, and record the block length as the cell's gap length.  Blocks of length 1, 2, 3, 5 and
     10 are laid down in one replicate without overlapping and without sharing anchors.
  2. Refit every method on the damaged panel (truth is not visible to the imputer).
  3. Predict the deleted cells and score error (MAE, RMSE, bias) by method x gap length.
     For methods that provide intervals, also score interval coverage against the nominal level.
  4. Average over replicates.  Only cells whose ORIGINAL flag is in `score_flags` (default 'v',
     verified) are scored, so a result is never graded against a value we ourselves supplied.

Gap length is measured in years of missing run: for an annual panel a block of L consecutive
years is a gap of L years.  The harness is written for panels on a consecutive-year grid (the
annual PWT and Lee-Lee panels used in engine/test_impute.py); for a 5-year wave panel each slot
is a wave and the report notes the year span separately.

Everything is seeded; repeated calls with the same arguments give identical deletions, fits and
scores.
"""
import math
import time

import numpy as np

from .base import make_imputer, method_names
from .panel import MISSING, OBSERVED_FLAGS, ProvenancePanel

DEFAULT_GAP_LENGTHS = (1, 2, 3, 5, 10)
DEFAULT_REPLICATES = 3


# ---------------------------------------------------------------- deletions
def make_deletions(panel, gap_lengths=DEFAULT_GAP_LENGTHS, n_replicates=DEFAULT_REPLICATES,
                   seed=0, score_flags=OBSERVED_FLAGS, points_per_gap=40):
    """Plan the held-out cells: one dict per replicate.

    Each replicate contains
        mask   : (n_entities, n_years) bool - cells to delete (set missing before fitting)
        group  : (n_entities, n_years) int  - gap length of each deleted cell, -1 elsewhere
        score  : (n_entities, n_years) bool - deleted cells with a trusted original value
    The different gap lengths are packed from longest to shortest, each block fully observed in
    the original panel and separated from its neighbours by at least one observed anchor cell;
    blocks may share an anchor observation but never overlap.
    """
    gap_lengths = tuple(int(g) for g in gap_lengths)
    if not gap_lengths or min(gap_lengths) < 1:
        raise ValueError('gap_lengths must be positive integers')
    if max(gap_lengths) >= panel.n_years - 2:
        raise ValueError(f'gap length {max(gap_lengths)} too long for a {panel.n_years}-year panel')
    trusted = panel.observed(score_flags)
    out = []
    for r in range(int(n_replicates)):
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(r)]))
        occupied = np.zeros(panel.shape, bool)
        group = np.full(panel.shape, -1, dtype=int)
        # pack the longest blocks first so they find room; the score aggregation is order-free
        for L in sorted(gap_lengths, reverse=True):
            need = max(1, int(math.ceil(points_per_gap / L)))
            got = 0
            # candidate starts: all cells of the block and both anchors are trusted observations
            order = rng.permutation(panel.n_entities)
            for i in order:
                if got >= need:
                    break
                starts = np.flatnonzero(trusted[i])
                starts = starts[(starts >= 1) & (starts + L <= panel.n_years - 1)]
                if starts.size == 0:
                    continue
                starts = rng.permutation(starts)
                for start in starts:
                    if got >= need:
                        break
                    block = np.arange(start, start + L)
                    windows = np.concatenate(([start - 1], block, [start + L]))
                    if not trusted[i, windows].all():
                        continue
                    if occupied[i, windows].any():
                        continue
                    occupied[i, block] = True
                    group[i, block] = L
                    got += 1
            if got == 0:
                raise ValueError(f'no room left to delete a {L}-year block; shrink gap_lengths '
                                 f'or points_per_gap')
        out.append(dict(mask=occupied, group=group, score=occupied & trusted))
    return out


def damage(panel, mask, name=None):
    """A copy of the panel with `mask` cells deleted (NaN, empty flag); truth is not kept."""
    values = np.where(mask, np.nan, panel.values)
    flags = np.where(mask, MISSING, panel.flags)
    return ProvenancePanel(panel.entities, panel.years, values, flags,
                           name=name or panel.name, history=panel.history)


# ---------------------------------------------------------------- scoring
class HoldoutReport:
    """Scores from a hold-out run: {method: {gap: stats}} plus run metadata.

    stats keys: n, mae, rmse, bias, coverage, width, nominal, cover_n
    (coverage/width are NaN for methods without intervals).
    """

    def __init__(self, scores, meta):
        self.scores = scores
        self.meta = meta

    # -- views -----------------------------------------------------------------
    @property
    def methods(self):
        return list(self.scores)

    @property
    def gaps(self):
        gaps = set()
        for m in self.scores.values():
            gaps.update(m)
        return sorted(gaps)

    def table(self, metric='mae', digits=3, suffix='y'):
        """Markdown table: rows = methods, columns = gap lengths, cells = metric."""
        gaps = self.gaps
        head = '| method | ' + ' | '.join(f'gap {g}{suffix}' for g in gaps) + ' |'
        sep = '|---|' + '---:|' * len(gaps)
        rows = [head, sep]
        for m in self.methods:
            cells = []
            for g in gaps:
                v = self.scores[m].get(g, {}).get(metric)
                cells.append('--' if v is None or not np.isfinite(v) else f'{v:.{digits}f}')
            rows.append(f'| {m} | ' + ' | '.join(cells) + ' |')
        return '\n'.join(rows)

    def coverage_table(self, digits=3, suffix='y'):
        """Markdown table of interval coverage by method x gap (only methods with intervals)."""
        gaps = self.gaps
        methods = [m for m in self.methods if self.scores[m].get(gaps[0] if gaps else 0, {}).get('nominal')]
        if not methods:
            return '(no interval methods in this run)'
        rows = ['| method | nominal | ' + ' | '.join(f'gap {g}{suffix}' for g in gaps) + ' |',
                '|---|---:|' + '---:|' * len(gaps)]
        for m in methods:
            nominal = next((self.scores[m][g]['nominal'] for g in gaps
                            if 'nominal' in self.scores[m].get(g, {})), None)
            cells = []
            for g in gaps:
                st = self.scores[m].get(g, {})
                c = st.get('coverage')
                cells.append('--' if c is None or not np.isfinite(c) else f'{c:.{digits}f}')
            rows.append(f'| {m} | {nominal:.2f} | ' + ' | '.join(cells) + ' |')
        return '\n'.join(rows)

    def counts_table(self, suffix='y'):
        """Markdown table of the number of scored points behind each cell."""
        gaps = self.gaps
        rows = ['| method | ' + ' | '.join(f'gap {g}{suffix}' for g in gaps) + ' |',
                '|---|' + '---:|' * len(gaps)]
        for m in self.methods:
            cells = [str(self.scores[m].get(g, {}).get('n', 0)) for g in gaps]
            rows.append(f'| {m} | ' + ' | '.join(cells) + ' |')
        return '\n'.join(rows)

    def best(self, gap, metric='mae'):
        """(method, value) with the lowest metric at one gap length."""
        candidates = [(m, self.scores[m][gap][metric]) for m in self.methods
                      if gap in self.scores[m] and np.isfinite(self.scores[m][gap].get(metric, np.nan))]
        if not candidates:
            return None, float('nan')
        return min(candidates, key=lambda t: t[1])

    def to_dict(self):
        return dict(meta=self.meta, scores=self.scores)

    def __repr__(self):
        return (f'HoldoutReport(panel={self.meta.get("panel", "?")!r}, '
                f'{len(self.methods)} methods, gaps={self.gaps}, '
                f'replicates={self.meta.get("n_replicates")})')


# ---------------------------------------------------------------- the run
def _normalise_methods(methods):
    if methods is None:
        methods = method_names()
    if isinstance(methods, dict):
        out = {}
        for name, m in methods.items():
            if not hasattr(m, 'fit') or not hasattr(m, 'predict'):
                raise TypeError(f'method {name!r} is not an Imputer')
            out[str(name)] = m
        return out
    out = {}
    for item in methods:
        if isinstance(item, str):
            out[item] = make_imputer(item)
        elif hasattr(item, 'fit') and hasattr(item, 'predict'):
            out[item.name] = item
        else:
            raise TypeError(f'cannot interpret method {item!r}')
    return out


def holdout(panel, methods=None, gap_lengths=DEFAULT_GAP_LENGTHS,
            n_replicates=DEFAULT_REPLICATES, seed=0, score_flags=OBSERVED_FLAGS,
            points_per_gap=40, score_transform=None, verbose=False):
    """Delete observed cells, impute them with every method, score error by method x gap length.

    Parameters
    ----------
    panel : ProvenancePanel
        Real (or synthetic) data panel on a consecutive-year grid.  An annual panel makes a gap
        length of L mean L missing years.
    methods : dict name -> Imputer, list of names/Imputers, or None (the full six-rung ladder).
    gap_lengths : consecutive missing-run lengths to test, default (1, 2, 3, 5, 10).
    n_replicates : independent deletion patterns, default 3.
    seed : master seed for the deletion patterns.
    score_flags : provenance flags the original held-out values must have; default ('v',)
        (verified).  Pass ('v', 'm') to score memory-flagged points as well.
    points_per_gap : target number of scored cells per gap length per replicate.
    score_transform : callable applied to predictions and truth before scoring error (e.g. np.log
        to score a levels panel in log error).  Interval coverage is always checked in the panel's
        own units.  None (default) scores in panel units.

    Returns a HoldoutReport.  Deterministic for fixed arguments.
    """
    if not isinstance(panel, ProvenancePanel):
        raise TypeError('holdout expects a ProvenancePanel')
    methods = _normalise_methods(methods)
    t0 = time.time()
    plans = make_deletions(panel, gap_lengths, n_replicates, seed,
                           score_flags=score_flags, points_per_gap=points_per_gap)
    # accumulate per method x gap
    acc = {name: {int(g): dict(err=[], sq=[], cover=[], width=[]) for g in gap_lengths}
           for name in methods}
    truth_all = panel.values
    for rep, plan in enumerate(plans):
        train = damage(panel, plan['mask'])
        score = plan['score']
        group = plan['group']
        if not score.any():
            raise ValueError('the deletion plan scored no cells; check score_flags')
        for name, imputer in methods.items():
            imp = imputer.clone()
            imp.fit(train)
            res = imp.predict(score)
            pred = res.values
            for g in gap_lengths:
                sel = score & (group == g) & np.isfinite(pred)
                if not sel.any():
                    continue
                a = acc[name][int(g)]
                p = pred[sel]
                t = truth_all[sel]
                if score_transform is not None:
                    p, t = score_transform(p), score_transform(t)
                    keep = np.isfinite(p) & np.isfinite(t)
                    p, t = p[keep], t[keep]
                if p.size:
                    err = p - t
                    a['err'].append(err)
                    a['sq'].append(err ** 2)
                if res.lower is not None:
                    lo, hi = res.lower[sel], res.upper[sel]
                    raw_t = truth_all[sel]
                    a['cover'].append((lo <= raw_t) & (raw_t <= hi))
                    a['width'].append(hi - lo)
        if verbose:
            print(f'  replicate {rep + 1}/{len(plans)}: scored {int(score.sum())} cells')

    scores = {}
    for name, by_gap in acc.items():
        scores[name] = {}
        for g, a in by_gap.items():
            if not a['err']:
                scores[name][int(g)] = dict(n=0, mae=float('nan'), rmse=float('nan'),
                                            bias=float('nan'), coverage=float('nan'),
                                            width=float('nan'), nominal=None)
                continue
            e = np.concatenate(a['err'])
            st = dict(n=int(e.size), mae=float(np.mean(np.abs(e))),
                      rmse=float(np.sqrt(np.mean(np.concatenate(a['sq'])))),
                      bias=float(np.mean(e)))
            if a['cover']:
                c = np.concatenate(a['cover'])
                st['coverage'] = float(c.mean())
                st['width'] = float(np.concatenate(a['width']).mean())
                st['nominal'] = float(getattr(methods[name], 'coverage', 0.9))
                st['cover_n'] = int(c.size)
            else:
                st['coverage'] = float('nan')
                st['width'] = float('nan')
            scores[name][int(g)] = st
    meta = dict(panel=panel.name, n_entities=panel.n_entities, n_years=panel.n_years,
                gap_lengths=[int(g) for g in gap_lengths], n_replicates=int(n_replicates),
                seed=int(seed), score_flags=tuple(score_flags),
                points_per_gap=int(points_per_gap),
                score_transform=getattr(score_transform, '__name__', None),
                seconds=round(time.time() - t0, 3))
    return HoldoutReport(scores, meta)
