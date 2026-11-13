"""Provenance-carrying country-year panels.

Every number in an Atlas panel carries where it came from:

    'v'  verified  read from a named source (or a checked release file) this session
    'm'  memory    entered from memory of an official release; not yet checked
    'd'  derived   produced by a transformation or an imputation, not observed
    ''   missing   there is no number for this cell

The invariant enforced here is: a cell has a finite value if and only if it has a non-empty
flag.  Derived values ('d') are kept, and can be displayed, but they are NOT observations:
by default the imputation methods fit on ('v', 'm') and never treat a 'd' cell as data.

This panel is the container the whole imputation ladder operates on.  It is deliberately a
thin numpy object (no pandas in the core): values shape (n_entities, n_years), flags the same
shape with dtype '<U1', entities a list of names, years a strictly increasing numeric array.
Year coordinates are real year numbers, not positions, so a 5-year Barro-Lee wave panel and an
annual PWT panel are handled by the same code: interpolation and gap lengths are in years.

Usage:

    p = ProvenancePanel(['A', 'B'], [2000, 2001, 2002], [[1, np.nan, 3], [5, 6, np.nan]])
    p.flags                      # [['v', '', 'v'], ['v', 'v', '']]
    imp = LinearInterpolator().fit(p)
    filled = p.with_fill(imp.predict())      # the two gaps are now 'd'

The constructor's default flag for finite values is 'v'; pass flags= explicitly for real
provenance, and use from_long(...) in engine.impute.data for the packaged public datasets.
"""
import numpy as np

# ---------------------------------------------------------------- flags
VERIFIED = 'v'
MEMORY = 'm'
DERIVED = 'd'
MISSING = ''

ALL_FLAGS = (VERIFIED, MEMORY, DERIVED, MISSING)
OBSERVED_FLAGS = (VERIFIED, MEMORY)      # flags that count as data when fitting by default
TRUSTED = OBSERVED_FLAGS                  # legacy-friendly alias

_FLAG_LABELS = {VERIFIED: 'verified', MEMORY: 'memory', DERIVED: 'derived', MISSING: 'missing'}


def label(flag):
    """Human label for a flag, for reports."""
    return _FLAG_LABELS.get(flag, flag)


class ProvenancePanel:
    """A country-year panel of floats whose every cell carries a provenance flag.

    Parameters
    ----------
    entities : sequence of str
        Country / unit names, length n.  Must be unique.
    years : sequence of numbers
        1-D, strictly increasing, length T.  Real year coordinates (e.g. 1950, 1955, ...).
    values : array (n, T)
        Numbers; NaN means "no number".  +/-inf is rejected.
    flags : array (n, T) of single characters, optional
        'v', 'm', 'd' or ''.  Default: 'v' for finite values, '' for NaN.
    name : str
        Label carried into reports.
    history : list of str, optional
        Records how derived cells were produced; with_fill() appends to it.
    """

    def __init__(self, entities, years, values, flags=None, name='', history=None):
        self.entities = [str(e) for e in entities]
        self.years = np.asarray(years, dtype=float).copy()
        self.values = np.asarray(values, dtype=float).copy()

        if self.values.ndim != 2:
            raise ValueError(f'values must be 2-D (n_entities, n_years); got shape {self.values.shape}')
        n, T = self.values.shape
        if n != len(self.entities):
            raise ValueError(f'{len(self.entities)} entities but values has {n} rows')
        if T != len(self.years):
            raise ValueError(f'{len(self.years)} years but values has {T} columns')
        if len(set(self.entities)) != n:
            raise ValueError('entity names must be unique')
        if not np.all(np.isfinite(self.years)):
            raise ValueError('years must be finite')
        if T > 1 and not np.all(np.diff(self.years) > 0):
            raise ValueError('years must be strictly increasing')
        if np.isinf(self.values).any():
            raise ValueError('values may be NaN but not +/-inf (use NaN for missing)')

        self.name = str(name)
        self.history = list(history) if history else []

        if flags is None:
            flags = np.where(np.isfinite(self.values), VERIFIED, MISSING)
        f = np.asarray(flags)
        if f.shape != self.values.shape:
            raise ValueError(f'flags shape {f.shape} != values shape {self.values.shape}')
        f = f.astype('<U1')
        bad = ~np.isin(f, ALL_FLAGS)
        if bad.any():
            i, j = np.argwhere(bad)[0]
            raise ValueError(f'invalid provenance flag {f[i, j]!r} at entity {self.entities[i]!r}, '
                             f'year {self.years[j]:g}; allowed: v, m, d or empty')
        finite = np.isfinite(self.values)
        has_flag = f != MISSING
        if np.any(finite != has_flag):
            i, j = np.argwhere(finite != has_flag)[0]
            detail = 'has a value but no flag' if finite[i, j] else 'has a flag but no value'
            raise ValueError(f'provenance invariant broken at entity {self.entities[i]!r}, '
                             f'year {self.years[j]:g}: cell {detail}')
        self.flags = f

    # ------------------------------------------------------------ basic properties
    @property
    def shape(self):
        return self.values.shape

    @property
    def n_entities(self):
        return self.values.shape[0]

    @property
    def n_years(self):
        return self.values.shape[1]

    @property
    def missing(self):
        """Boolean mask of cells with no number."""
        return self.flags == MISSING

    def observed(self, flags=OBSERVED_FLAGS):
        """Mask of cells usable as data: finite value and flag in `flags`.

        The default excludes derived ('d') cells, which is what makes an imputed panel safe
        to re-fit: derived numbers are never treated as observations unless asked for.
        """
        allowed = self._check_flags(flags)
        return np.isfinite(self.values) & np.isin(self.flags, allowed)

    def flag(self, flag):
        """Mask of cells with exactly this flag."""
        self._check_flags((flag,))
        return self.flags == flag

    def flag_counts(self):
        """{flag label: count} including 'missing'."""
        counts = {}
        for f in ALL_FLAGS:
            c = int(np.sum(self.flags == f))
            if c:
                counts[label(f)] = c
        return counts

    def observed_values(self, flags=OBSERVED_FLAGS):
        """The values array with non-usable cells set to NaN."""
        return np.where(self.observed(flags), self.values, np.nan)

    # ------------------------------------------------------------ building derived panels
    def copy(self):
        return ProvenancePanel(self.entities, self.years, self.values, self.flags,
                               name=self.name, history=self.history)

    def map(self, func, name=None):
        """Apply a deterministic transformation to the values, keeping the flags.

        Cells where the transform returns a non-finite number (e.g. log of 0) become missing,
        because there is then no number to attach the original provenance to.  Good for
        e.g. ``load_pwt().map(np.log)`` before a log-scale hold-out.
        """
        new = np.asarray(func(self.values), dtype=float)
        if new.shape != self.values.shape:
            raise ValueError('transform changed the value shape')
        finite = np.isfinite(new) & (self.flags != MISSING)
        values = np.where(finite, new, np.nan)
        flags = np.where(finite, self.flags, MISSING)
        return ProvenancePanel(self.entities, self.years, values, flags,
                               name=name or self.name, history=self.history)

    def subset(self, entity_mask=None, year_mask=None, name=None):
        """Restrict to a subset of entities and/or years (boolean masks)."""
        if entity_mask is None:
            entity_mask = np.ones(self.n_entities, bool)
        if year_mask is None:
            year_mask = np.ones(self.n_years, bool)
        entity_mask = np.asarray(entity_mask, bool)
        year_mask = np.asarray(year_mask, bool)
        if entity_mask.shape != (self.n_entities,) or year_mask.shape != (self.n_years,):
            raise ValueError('subset masks have the wrong shape')
        ents = [e for e, keep in zip(self.entities, entity_mask) if keep]
        return ProvenancePanel(ents, self.years[year_mask], self.values[entity_mask][:, year_mask],
                               self.flags[entity_mask][:, year_mask],
                               name=name or self.name, history=self.history)

    def with_fill(self, fill, where=None, note=None, overwrite=False):
        """Return a new panel with cells filled and flagged 'd' (derived).

        `fill` is either an ImputationResult (its .where / .values / .method are used) or a
        values array.  Cells keep their old value and flag unless `where` selects them and the
        fill is finite.  Filling a cell that holds a verified or memory observation ('v'/'m')
        raises unless overwrite=True: derived numbers must not silently replace real data.
        """
        from .base import ImputationResult
        if isinstance(fill, ImputationResult):
            values = fill.values
            where = fill.where if where is None else where
            method = fill.method
        else:
            values = np.asarray(fill, dtype=float)
            method = 'fill'
        if values.shape != self.values.shape:
            raise ValueError(f'fill shape {values.shape} != panel shape {self.values.shape}')
        if where is None:
            raise ValueError('with_fill requires where= (or an ImputationResult carrying it)')
        where = np.asarray(where, bool)
        if where.shape != self.values.shape:
            raise ValueError(f'where shape {where.shape} != panel shape {self.values.shape}')
        target = where & np.isfinite(values)
        protected = target & np.isin(self.flags, OBSERVED_FLAGS)
        if protected.any() and not overwrite:
            i, j = np.argwhere(protected)[0]
            raise ValueError(f'refusing to overwrite observed {self.flags[i, j]!r} value at '
                             f'entity {self.entities[i]!r}, year {self.years[j]:g} '
                             f'(pass overwrite=True only if you really mean it)')
        vals = np.where(target, values, self.values)
        flags = np.where(target, DERIVED, self.flags)
        entry = f'{note or method}: filled {int(target.sum())} cell(s)'
        return ProvenancePanel(self.entities, self.years, vals, flags,
                               name=self.name, history=self.history + [entry])

    # ------------------------------------------------------------ views
    def to_records(self):
        """Long-format list of {entity, year, value, flag} for every cell with a value or flag."""
        out = []
        for i, e in enumerate(self.entities):
            for j, y in enumerate(self.years):
                if self.flags[i, j] != MISSING:
                    out.append(dict(entity=e, year=float(y), value=float(self.values[i, j]),
                                    flag=str(self.flags[i, j])))
        return out

    def __repr__(self):
        observed = int(self.observed().sum())
        counts = ', '.join(f'{k} {v}' for k, v in sorted(self.flag_counts().items()))
        return (f'ProvenancePanel({self.n_entities} entities x {self.n_years} years, '
                f'{observed} observed; {counts or "empty"})')

    # ------------------------------------------------------------ helpers
    @staticmethod
    def _check_flags(flags):
        flags = (flags,) if isinstance(flags, str) else tuple(flags)
        bad = [f for f in flags if f not in ALL_FLAGS]
        if bad:
            raise ValueError(f'unknown provenance flag(s) {bad!r}; allowed: v, m, d, empty')
        return flags


def from_long(records, entities=None, years=None, default_flag=VERIFIED, name=''):
    """Build a ProvenancePanel from a long sequence of {entity, year, value, flag} dicts.

    `records` may also be an iterable of (entity, year, value, flag) tuples.  Missing cells get
    the empty flag.  Duplicate (entity, year) entries raise: provenance must be unambiguous.
    """
    rows = list(records)
    cells = {}
    ents, yrs = [], set()
    for r in rows:
        if isinstance(r, dict):
            e, y, v, f = r['entity'], r['year'], r['value'], r.get('flag', default_flag)
        else:
            e, y, v, f = r
        key = (str(e), float(y))
        if key in cells:
            raise ValueError(f'duplicate observation for {key[0]!r}, {key[1]:g}')
        f = default_flag if f in (None, '') else f
        if f not in ALL_FLAGS or f == MISSING:
            raise ValueError(f'invalid flag {f!r} for {key[0]!r}, {key[1]:g}')
        cells[key] = (float(v) if v is not None else np.nan, f)
        ents.append(key[0])
        yrs.add(key[1])
    ents = sorted(entities if entities is not None else set(ents))
    yrs = np.array(sorted(years if years is not None else yrs), dtype=float)
    if len(ents) == 0 or len(yrs) == 0:
        raise ValueError('cannot build an empty panel')
    idx_e = {e: i for i, e in enumerate(ents)}
    idx_y = {y: j for j, y in enumerate(yrs)}
    values = np.full((len(ents), len(yrs)), np.nan)
    flags = np.full((len(ents), len(yrs)), MISSING, dtype='<U1')
    for (e, y), (v, f) in cells.items():
        if e in idx_e and y in idx_y:
            values[idx_e[e], idx_y[y]] = v
            flags[idx_e[e], idx_y[y]] = f
    return ProvenancePanel(ents, yrs, values, flags, name=name)
