"""Fixture module for the Gate-1d invariant suite (engine contract v1.0, §12).

Binding references
------------------
* `docs/audit/ENGINE_INTERFACE_CONTRACT.md` §1 gate kinds, §2 persistent state, §4 accounting,
  §5 prep stock, §6 core API methods, §7 RNG, §11 the twelve invariant definitions, §12 this
  fixture contract.
* This lane owns ``tests/**`` except ``tests/test_contest_math.py`` (Gate-1c) and is read-only on
  ``engine/``. Nothing here edits engine code.

What the fixtures provide (§12)
-------------------------------
``build_engine(**overrides)``       -> Engine over modules
                                       [PublicSchools, PrivateSchools, TutoringMarket, QueueLabour, SDG4],
                                       N<=120, T<=24, measure_from<=10.
``small_contest_engine(gate_extra=None, **params)``
                                    -> 3-level ladder: one primary ``fixed_bar`` gate (level 0), ONE
                                       ``contest`` gate at level 1 (the last paid gate at ``nlev-2``),
                                       ``open`` elsewhere; isolates prize/gate logic from G12 special cases.
``annual_series(E, key)``           -> ``np.asarray`` of a yearly series.
``two_seed(builder=None, seeds=(0,1), **overrides)`` -> ``{seed: Engine}`` helper.

Extra helpers used by the accounting tests (same contract, additive only)
-------------------------------------------------------------------------
``audited_engine(**overrides)``     -> Engine with FiscalState, checking accounting identities at the
                                       end of every simulated year (``record`` hook, before compaction).
``tracked_run(**overrides)``        -> per-year tracer: gate candidates, new elite awards, largest prep
                                       stock, exits, keyed by the immutable ``pid`` when the engine has one
                                       (contract §2) and by ``(cohort, z)`` on the pre-repair baseline.
``legacy_gates_*``                  -> pre-repair compatible 4-level gate lists for the "present-and-wrong"
                                       baseline probes (D1/D2/D3/D6/D7 evidence rows in the report).
"""
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
ENGINE_DIR = ROOT / "engine"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

import eduengine.core as core_mod  # noqa: E402
from eduengine.core import Engine  # noqa: E402
from eduengine.modules.labour import QueueLabour  # noqa: E402
from eduengine.modules.schools import PrivateSchools, PublicSchools  # noqa: E402
from eduengine.modules.sdg4 import SDG4  # noqa: E402
from eduengine.modules.state import FiscalState  # noqa: E402
from eduengine.modules.tutoring import TutoringMarket  # noqa: E402

# --------------------------------------------------------------------------------------------- base config
# 4-level ladder ends = [6, 9, 12, 16] (the canonical 540-config ladder).  A contest on gate index 1 is
# the Grade-9 gate (checkable against the legacy baseline), index 2 is the Grade-12 gate.
BASE_4 = dict(
    N=40, T=22, measure_from=8, seed=0,
    y_median=2.2, y_sigma=0.6, urban_share=1.0, subsist=0.35, borrow=0.25,
    pay_ratio=1.2, monitoring=0.9, budget_per_child=0.14, vac0=0.30, vac_growth=0.005,
    own_ban=0.95, r0=0.04,
    elite_logw=0.60, contest_r=1.5, contest_alpha=0.25, contest_price=0.16,
    contest_x0=1.0, contest_max_e=6.0,
)
LEVELS_4 = [("primary", 6), ("lower", 3), ("upper", 3), ("tertiary", 4)]
LEVELS_3 = [("primary", 6), ("lower", 3), ("upper", 3)]      # nlev = 3 -> nlev-2 = 1 (G9)


def _modules():
    """§12 module stack: no FiscalState by default (kept for the fiscal identity tests)."""
    return [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]


def build_engine(modules=None, **overrides):
    """§12 fixture: Engine(modules, **params) with the standard stack, N<=120, T<=24."""
    p = dict(BASE_4)
    p.setdefault("gates", legacy_gates_g12())
    p.update(overrides)
    mods = modules if modules is not None else _modules()
    return Engine(mods, **p)


def small_contest_engine(gate_extra=None, **params):
    """§12 fixture: fixed_bar at level 0, one contest gate at level 1 (=nlev-2), open elsewhere."""
    extra = dict(share=0.12, fail="track", elite_logw=0.60)
    extra.update(gate_extra or {})
    gates = [dict(kind="fixed_bar", bar=2.0), dict(kind="contest", **extra), dict(kind="open")]
    p = dict(BASE_4, levels=LEVELS_3, gates=gates)
    p.update(params)
    return Engine(_modules(), **p)


def two_seed(builder=None, seeds=(0, 1), **overrides):
    """§12 helper: ``{seed: Engine}`` for the same configuration under two seeds."""
    mk = builder if builder is not None else (lambda **kw: build_engine(**kw))
    return {s: mk(seed=s, **overrides) for s in seeds}


def annual_series(E, key):
    """§12 helper: a yearly series as ``np.ndarray(float)``; raises KeyError with the keys present."""
    if key not in E.R:
        raise KeyError(f"{key!r} not recorded; series present: {sorted(E.R)}")
    return np.asarray(E.R[key], dtype=float)


# --------------------------------------------------------------------------------------------- legacy gate lists
BAR = lambda bar, **kw: dict(kind="bar", bar=bar, **kw)  # noqa: E731  (deprecated alias per §1)


def legacy_gates_g12(contest=None, **kw):
    g = dict(kind="contest", share=0.25, fail="track")
    g.update(contest or {})
    g.update(kw)
    return [BAR(2.0), BAR(4.0), g, BAR(10.0)]


def legacy_gates_g9(contest=None, **kw):
    g = dict(kind="contest", share=0.35, fail="track", elite_logw=0.15, set_voc=False)
    g.update(contest or {})
    g.update(kw)
    return [BAR(2.0), g, BAR(6.0), BAR(10.0)]


def legacy_gates_voc_then_contest():
    """Vocational track created by a fail='track' bar gate at level 1, then an academic-only contest."""
    return [BAR(2.0), BAR(4.0, fail="track"),
            dict(kind="contest", share=0.25, fail="track", academic_only=True), BAR(10.0)]


# --------------------------------------------------------------------------------------------- accounting
class AuditedEngine(Engine):
    """Engine that checks the §4/§11 accounting identities at the end of every simulated year.

    ``record()`` runs after all module phases and before exited children are compacted out of
    ``Engine.kids`` (core.py:506-511), so the child vectors, this year's arrays in ``Engine.yr`` and
    the recorded series all have the same length there.  Diagnostics are stored in ``self.acct``.
    """

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.acct = []

    def record(self, t, ex, inc):  # noqa: D401 - engine hook
        super().record(t, ex, inc)
        k, y, R = self.kids, self.yr, self.R
        att = k["att"]
        n = len(y["extra_spend"])
        items = []

        # §11.9: schooling need + own/firm spend + contest outlay <= residual cash, per child-year
        cash = self._cash[:n] if hasattr(self, "_cash") else np.zeros(n)
        over = np.flatnonzero(att & (y["extra_spend"] > cash + 1e-9))
        items.append(dict(check="funds", n_violations=int(len(over)),
                          worst_overage=float((y["extra_spend"][over] - cash[over]).max())
                          if len(over) else 0.0,
                          n_att=int(att.sum())))

        # cohort denominators: attendance series must be the per-grade census of the same year
        items.append(dict(check="enrolled_eq_att_by_grade",
                          lhs=int(R["enrolled"][t]),
                          rhs=int(np.asarray(R["att_by_grade"][t]).sum())))

        # §11 per-quintile accounting reconciliation of the legacy tutoring series.
        # The recorded series use the PRE-promotion grade ("index j = pupils studying grade j+1
        # this year", core.py:374-376) while `record()` runs after promotion increments k['g'].
        # With automatic promotion (promote_bar == 0) the pre-promotion grade is k['g'] - 1 for
        # every attending child; tests do not set promote_bar, so the reconstruction is exact.
        assert self.p["promote_bar"] == 0.0, "audited per-quintile check assumes automatic promotion"
        pre_g = k["g"] - 1
        k12 = att & (pre_g < 12)
        rows = []
        for j in range(5):
            sel = k12 & (k["q"] == j)
            n_j = int(sel.sum())
            rows.append(dict(q=j, n=n_j,
                             spend_recorded=float(R["tut_k12_spend_by_q"][t][j]),
                             spend_expected=float(y["extra_spend"][sel].mean()) if n_j else 0.0,
                             rate_recorded=float(R["tut_k12_rate_by_q"][t][j]),
                             rate_expected=float(sel.sum() / max((k12 & (k["q"] == j)).sum(), 1)),
                             n_across=float((k12 & (k["q"] == j)).sum())))
        items.append(dict(check="per_quintile", rows=rows,
                          k12_total_recorded=float(R["tut_k12_spend"][t]),
                          k12_total_expected=float(y["extra_spend"][k12].sum())))

        # §4.1/§11.10: contest outlay decomposition (only when the engine records the channels)
        if "contest_resource_cost" in R and "contest_tax_paid" in R and "contest_spend_now" in R:
            items.append(dict(check="tut_outlay_identity",
                              outlay=float(R["contest_spend_now"][t]),
                              res_cost=float(R["contest_resource_cost"][t]),
                              tax=float(R["contest_tax_paid"][t]),
                              gov_receipt=float(R["gov_tut_receipt"][t]),
                              yr_outlay=float(y.get("tut_outlay", np.zeros(n)).sum()),
                              yr_res=float(y.get("res_cost", np.zeros(n)).sum()),
                              yr_tax=float(y.get("tut_tax", np.zeros(n)).sum()),
                              yr_gov=float(y.get("gov_tut_tax", np.zeros(n)).sum())))

        # §11 tax revenue identity (FiscalState): revenue = tax_formal*formal + tax_cons*(formal+informal)
        if "revenue" in R:
            f, i = getattr(self, "bill", (0.0, 0.0))
            items.append(dict(check="tax_revenue",
                              recorded=float(R["revenue"][t]),
                              expected=float(self.p["tax_formal"] * f + self.p["tax_cons"] * (f + i)),
                              gdp_recorded=float(R["gdp"][t]), gdp_expected=float(f + i),
                              tax_gdp_recorded=float(R["tax_gdp"][t]),
                              edu_budget=float(R["edu_budget"][t]),
                              formal=float(f), informal=float(i)))
        self.acct.append((t, items))


def audited_engine(**overrides):
    """Engine with FiscalState + per-year accounting diagnostics (tax identity needs the state module)."""
    p = dict(BASE_4)
    p.setdefault("gates", legacy_gates_g12())
    p.update(overrides)
    mods = [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), FiscalState()]
    return AuditedEngine(mods, **p)


def run_audited(**overrides):
    E = audited_engine(**overrides)
    E.run()
    return E


# --------------------------------------------------------------------------------------------- per-year tracer
def _row(k, i):
    out = dict(cred=int(k["cred"][i]), elite=bool(k["elite"][i]),
               ce=float(k["contest_e"][i]) if "contest_e" in k else 0.0,
               g=int(k["g"][i]), reason=int(k["reason"][i]),
               voc=bool(k["voc"][i]) if "voc" in k else False)
    if "track" in k:
        out["track"] = int(k["track"][i])
    if "elite_prize" in k:
        out["elite_prize"] = float(k["elite_prize"][i])
    if "prep_stock" in k:
        out["prep_stock"] = np.asarray(k["prep_stock"][i], dtype=float).copy()
    return out


def tracked_run(builder=None, **overrides):
    """Run year by year; return ``(E, years)``.

    ``years[t]`` carries what the recorded series do not expose: children advancing each level (gate
    candidates), new elite awards, the largest prep stock held at year end, exits.  Children are keyed
    by the immutable ``pid`` (§2) when present, else by ``(cohort, z)`` (pre-repair baseline).
    """
    E = (builder or build_engine)(**overrides)
    prev = {}
    years = []
    use_pid = None
    for t in range(E.p["T"]):
        n_before = len(E.exits)
        E.step(t)
        k = E.kids
        if use_pid is None:
            use_pid = "pid" in k

        def key(kk, i):
            if use_pid:
                return int(kk["pid"][i])
            return (int(kk["cohort"][i]), float(kk["z"][i]))

        alive = {key(k, i): _row(k, i) for i in range(len(k["y"]))}
        after = dict(alive)
        for e in E.exits[n_before:]:
            for i in range(len(e["cohort"])):
                after[key(e, i)] = _row(e, i)
        cand = {m: 0 for m in range(E.nlev)}
        elite_new = 0
        ce_max = 0.0
        for kk, a in after.items():
            b = prev.get(kk)
            if b is None:
                continue
            if a["cred"] == b["cred"] + 1:
                cand[a["cred"] - 1] += 1
            if a["elite"] and not b["elite"]:
                elite_new += 1
            ce_max = max(ce_max, a["ce"])
        years.append(dict(t=t, active=len(alive), exits=len(after) - len(alive),
                          max_ce=ce_max, elite_new=elite_new, candidates=cand, rows=after))
        prev = after
    return E, years


# --------------------------------------------------------------------------------------------- capability probe
def _import_contest_math():
    try:
        import eduengine.contest_math as cm
        return cm if hasattr(cm, "pl_win_probs") else None
    except Exception:  # pragma: no cover - feature probe, absence is expected pre-repair
        return None


def _capabilities():
    cm = _import_contest_math()
    caps = dict(
        contest_math=cm is not None,
        contest_math_module=cm,
        gate_kinds=False,
        gate_specs=hasattr(core_mod, "GATE_SPECS"),
        api_contest_weights=hasattr(Engine, "contest_weights"),
        api_expected_probs=hasattr(Engine, "contest_expected_probs"),
        api_prize_dv=hasattr(Engine, "gate_prize_dv"),
        api_contest_summary=hasattr(Engine, "contest_summary"),
        event_rng=False,
        state_track=False,
        state_elite_prize=False,
        state_prep_stock=False,
        state_pid=False,
        reporting=False,
        accounting=False,
        share_of=False,
        prep_depreciation=False,
        contract_error="",
    )
    try:
        caps["accounting"] = "contest_tax_rate" in TutoringMarket.defaults
        caps["prep_depreciation"] = "contest_prep_depreciation" in TutoringMarket.defaults
        E = build_engine(N=24, T=18, measure_from=6, gates=legacy_gates_g12())
        caps["event_rng"] = type(E.rng).__name__ == "EventRNG"
        try:
            E.run()
            for key, flag in (("track", "state_track"), ("elite_prize", "state_elite_prize"),
                              ("prep_stock", "state_prep_stock"), ("pid", "state_pid")):
                caps[flag] = key in E.ALL
            caps["reporting"] = "contest_candidates" in E.R
            caps["gate_kinds"] = hasattr(E, "gate_kind")
            caps["share_of"] = hasattr(E, "contest_seats")
        except Exception as exc:  # pragma: no cover
            caps["contract_error"] += f" legacy run failed: {exc!r}"
        try:
            E2 = small_contest_engine(N=24, T=8, measure_from=3)
            E2.run()
        except Exception:
            caps["gate_kinds"] = False
    except Exception as exc:  # pragma: no cover
        caps["contract_error"] += f" probe failed: {exc!r}"
    return caps


CAPS = _capabilities()


def missing(condition, reason):
    """Strict xfail marker for a contract API that the unrepaired baseline does not have.

    ``condition`` is True while the API is absent; the marker then fails loudly (XPASS(strict)) if
    the test unexpectedly passes, which is what we want: a "missing API" marker must be removed as
    soon as the lane lands the feature.
    """
    return pytest.mark.xfail(condition, strict=True, reason=reason)


# --------------------------------------------------------------------------------------------- fixtures
@pytest.fixture(scope="session")
def caps():
    return CAPS


@pytest.fixture(scope="session")
def pl_reference():
    """Exact Plackett-Luce top-K reference from Gate-1c (``eduengine.contest_math``)."""
    if not CAPS["contest_math"]:
        pytest.xfail("missing API: engine/eduengine/contest_math.py (contract §6; Gate-1c lane)")
    return CAPS["contest_math_module"]


@pytest.fixture(scope="session")
def series():
    return annual_series


@pytest.fixture(scope="session")
def build():
    return build_engine


@pytest.fixture(scope="session")
def small_contest():
    return small_contest_engine


@pytest.fixture(scope="session")
def tracked():
    return tracked_run


@pytest.fixture(scope="session")
def audited():
    return run_audited


@pytest.fixture(scope="session")
def engines_two_seeds():
    return two_seed
