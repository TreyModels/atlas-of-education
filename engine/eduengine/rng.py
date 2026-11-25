"""Event-keyed random streams: policy-invariant exogenous draws for the education engine.

Contract: ``docs/audit/ENGINE_INTERFACE_CONTRACT.md`` §7 (D6).

The engine used to draw from one sequential ``np.random.default_rng(seed)`` stream, so two policy arms
with the same seed consumed the stream at different offsets and their "matched" exogenous shocks were
not matched at all (audit §E: 9/20 cohorts matched, first divergence at the cohort where gate outcomes
first differ).  This module replaces the stream for exogenous shocks with a *pure function of the key*

    (seed, replicate, year, shock_type, pid, tap)

using a splitmix64 mix.  Consequences:

* a person's draw depends only on their immutable ``k['pid']``, never on how many other people were
  drawn this year, nor on the order in which pids are requested;
* two arms that differ only in policy parameters see identical covariates and identical gate/learning
  noise for every pid (the acceptance test in §7.4);
* the same config + seed is bit-deterministic;
* all methods are vectorised over pid arrays.

``Engine.rng`` is an :class:`EventRNG`.  Modules that have not yet migrated (``schools.py``,
``tutoring.py``, ``anchor.py``) keep working through the legacy methods (``random``,
``standard_normal``, ``legacy_logistic``, ``permutation``, ``choice``), which are backed by a private
sequential ``numpy.random.Generator``.  That legacy stream is a *separate* generator: it shares no
state with the event streams, and its residual path dependence is recorded in the Gate-1 report.
"""
from __future__ import annotations

import numpy as np

__all__ = ["EventRNG", "SHOCK_TYPES"]

#: Stable shock-type registry.  Values may be appended for new shock families, *never* renumbered:
#: renumbering would change every draw in existing runs.  Gate-indexed families ("gate_exam_{m}",
#: "contest_pl_{m}", "admit_{m}") take ``base * 100 + m`` so they are stable without enumeration.
SHOCK_TYPES = {
    "cohort_z": 1,
    "cohort_urban": 2,
    "cohort_home": 3,
    "cohort_ability": 4,
    "continuation": 5,
    "income_shock": 6,
    "learning": 7,
    "promote": 8,
    "gate_exam": 9,
    "contest_pl": 10,
    "admit": 11,
    "anchor": 12,
    "street": 13,
    "queue_accept": 14,
    "labour_signal": 15,
    "labour_lottery": 16,
    "labour_floor": 17,
    "tut_own_ok": 18,
    "tut_firm_ok": 19,
    "tut_taste": 20,
}

_INDEXED = ("gate_exam", "contest_pl", "admit")

# splitmix64 constants (public domain; fixed forever -- they define the draws)
_GOLD = np.uint64(0x9E3779B97F4A7C15)
_M1 = np.uint64(0xBF58476D1CE4E5B9)
_M2 = np.uint64(0x94D049BB133111EB)
_K_SEED = np.uint64(0xD1B54A32D192ED03)
_K_REP = np.uint64(0xABC98388FB8FAC03)
_K_YEAR = np.uint64(0x8CB92BA72F3D8DD7)
_K_TYPE = np.uint64(0x9E3779B97F4A7C15)
_K_PID = np.uint64(0xC2B2AE3D27D4EB4F)
_K_TAP = np.uint64(0x165667B19E3779F9)
_U53 = 1.0 / 9007199254740992.0       # 2**-53


def _mix(h):
    """splitmix64 finaliser, vectorised over a uint64 array (wraps modulo 2**64)."""
    with np.errstate(over="ignore"):
        z = h + _GOLD
        z = (z ^ (z >> np.uint64(30))) * _M1
        z = (z ^ (z >> np.uint64(27))) * _M2
        return z ^ (z >> np.uint64(31))


def _as_u64(x):
    """Reinterpret integer(s) as uint64 by their two's-complement bit pattern (stable for negative sentinels)."""
    a = np.asarray(x)
    if a.dtype.kind in "iu":
        return a.astype(np.int64, copy=False).view(np.uint64)
    return a.astype(np.uint64)


class _SplitMix:
    """A tiny scalar splitmix64 counter (used only for the unseeded MC validation path)."""

    def __init__(self, seed):
        self.s = np.uint64(int(seed) & 0xFFFFFFFFFFFFFFFF)

    def u64(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.s = self.s + _GOLD
            z = self.s
            z = (z ^ (z >> np.uint64(30))) * _M1
            z = (z ^ (z >> np.uint64(27))) * _M2
            return z ^ (z >> np.uint64(31))


class EventRNG:
    """Hash-keyed random streams over immutable person ids.

    Parameters
    ----------
    seed : int
        Global seed of the run.
    replicate : int
        Replicate identifier.  Contract §7 rule 3: ``replicate = p['seed']``; distinct runs therefore
        get distinct keys even if the caller reuses a seed by mistake.

    Event API (positional, vectorised; the only methods engine-core should call for shocks)::

        uniform(year, shock_type, pid)          -> U(0,1)  shape == np.shape(pid)
        normal(year, shock_type, pid)           -> N(0,1)  (Box-Muller from two keyed uniforms)
        logistic(year, shock_type, pid)         -> standard logistic
        gumbel(year, shock_type, pid)           -> standard Gumbel
        permutation_like(year, shock_type, pid) -> per-pid U(0,1); caller argsorts()

    ``pid`` may be an integer array (usual) or a scalar (sentinel draws such as ``labour_floor``).
    The value for a key never depends on which other pids are passed or on their order.
    """

    def __init__(self, seed, replicate=0):
        self.seed = int(seed)
        self.replicate = int(replicate)
        with np.errstate(over="ignore"):
            self._seed_u = _as_u64(self.seed & 0xFFFFFFFFFFFFFFFF) ^ _mix(_as_u64(self.replicate) * _K_REP)
        # Legacy stream for modules that have not migrated (contract §7 rule 2).
        self._legacy = np.random.default_rng(np.random.SeedSequence([self.seed, self.replicate, 0x1E6AC1]))
        # Deterministic generator for method='mc' validation calls (never the engine decision path).
        self._mc = np.random.default_rng(np.random.SeedSequence([self.seed, self.replicate, 0x3C6EF372]))

    # ---------------------------------------------------------------- key machinery
    @staticmethod
    def _type_id(shock_type):
        if shock_type in _INDEXED:
            raise KeyError(f"indexed shock family {shock_type!r} needs an index, e.g. '{shock_type}_3'")
        if shock_type in SHOCK_TYPES:
            return SHOCK_TYPES[shock_type]
        for base in _INDEXED:
            prefix = base + "_"
            if shock_type.startswith(prefix):
                try:
                    m = int(shock_type[len(prefix):])
                except ValueError:
                    break
                if m < 0:
                    break
                return SHOCK_TYPES[base] * 100 + m
        raise KeyError(
            f"unknown shock_type {shock_type!r}; add it to rng.SHOCK_TYPES (append only, never renumber)")

    def _hash(self, year, shock_type, pid, tap):
        """uint64 key array for (year, shock_type, pid, tap)."""
        tid = self._type_id(shock_type)
        with np.errstate(over="ignore"):
            h = self._seed_u ^ (_mix(_as_u64(year) * _K_YEAR))
            h = h ^ _mix(_as_u64(tid) * _K_TYPE)
            h = h ^ _mix(_as_u64(pid) * _K_PID)
            h = _mix(h) ^ _mix(_as_u64(tap) * _K_TAP)
        return h

    def _uniform_key(self, year, shock_type, pid, tap=0):
        h = self._hash(year, shock_type, pid, tap)
        u = (h >> np.uint64(11)).astype(np.float64) * _U53
        return u

    # ---------------------------------------------------------------- event API
    def uniform(self, year, shock_type, pid):
        return self._uniform_key(year, shock_type, pid, 0)

    def normal(self, year, shock_type, pid):
        u1 = np.clip(self._uniform_key(year, shock_type, pid, 0), 1e-12, 1.0 - 1e-12)
        u2 = self._uniform_key(year, shock_type, pid, 1)
        return np.sqrt(-2.0 * np.log(u1)) * np.cos(2.0 * np.pi * u2)

    def logistic(self, year, shock_type, pid):
        u = np.clip(self._uniform_key(year, shock_type, pid, 0), 1e-12, 1.0 - 1e-12)
        return np.log(u) - np.log1p(-u)

    def gumbel(self, year, shock_type, pid):
        u = np.clip(self._uniform_key(year, shock_type, pid, 0), 1e-12, 1.0 - 1e-12)
        return -np.log(-np.log(u))

    def permutation_like(self, year, shock_type, pid):
        """Per-pid U(0,1); the caller argsorts to obtain a policy-invariant permutation."""
        return self._uniform_key(year, shock_type, pid, 0)

    # ---------------------------------------------------------------- legacy API (unmigrated modules)
    def random(self, size=None):
        """Legacy sequential U(0,1) stream (path-dependent; for unmigrated modules only)."""
        return self._legacy.random(size)

    def standard_normal(self, size=None):
        """Legacy sequential N(0,1) stream (path-dependent; for unmigrated modules only)."""
        return self._legacy.standard_normal(size)

    def legacy_logistic(self, size=None):
        """Legacy sequential standard-logistic stream (path-dependent)."""
        return self._legacy.logistic(size)

    def permutation(self, n):
        """Legacy sequential permutation (path-dependent; engine-core uses ``permutation_like``)."""
        return self._legacy.permutation(n)

    def choice(self, a, size=None, replace=True, p=None):
        """Legacy sequential choice (path-dependent; for unmigrated modules only)."""
        return self._legacy.choice(a, size=size, replace=replace, p=p)

    # ---------------------------------------------------------------- validation helper
    def mc_rng(self, offset=0):
        """Deterministic generator for ``method='mc'`` validation calls (never the decision path)."""
        state = self._mc.bit_generator.state
        gen = np.random.default_rng(np.random.SeedSequence([self.seed, self.replicate, 0x3C6EF372, int(offset)]))
        self._mc.bit_generator.state = state
        return gen


def stable_int(text):
    """A stable (process-independent) 64-bit integer for a string, e.g. shock names in external code."""
    h = 0
    for ch in text.encode("utf-8"):
        h = (h * 1099511628211 + ch) & 0xFFFFFFFFFFFFFFFF
    return h
