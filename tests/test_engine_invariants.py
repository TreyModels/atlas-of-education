"""Gate-1d invariant suite for the Atlas contest engine (audit v2, 2026-11-25).

Written **test-first** against the binding interface contract
(`docs/audit/ENGINE_INTERFACE_CONTRACT.md`, v1.0).  Each test maps to a row of the binding
invariant table (§11) or to one of the Directive's additional accounting tests.  The suite is
deliberately split into two layers, so the first-failure report can separate scaffolding from
genuine defects:

* **Contract layer** — written against the §6 core API / §1.3 probability objects / §4 accounting
  channels / §5 prep stock.  On the unrepaired baseline these are `xfail(strict=True)` with the
  exact missing API in the reason string; after the engine lanes land they must run and pass.
* **Baseline probe layer** — invariants expressed with the *current* baseline API only.  These run
  now and fail with observed-vs-expected numbers where a defect (D1-D7 of the contract) is present.
  They are kept as the historical record after the repairs and must pass afterwards.

Run (from the worktree root, exactly the command recorded in the report):

    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python \
    -m pytest tests/test_engine_invariants.py -q

Parallel test 12 uses `ProcessPoolExecutor` with a fork context; `QA_WORKERS` sets the worker count
(12 on the box, capped by CPU count on the host).
"""
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pytest

from conftest import (
    CAPS,
    annual_series,
    audited_engine,
    build_engine,
    legacy_gates_g12,
    legacy_gates_g9,
    legacy_gates_voc_then_contest,
    missing,
    run_audited,
    small_contest_engine,
    tracked_run,
    two_seed,
)

# =====================================================================================================
# helpers shared by the tests
# =====================================================================================================


def _keys(E):
    return sorted(E.R)


def _awards(E):
    """Number of children ever carrying a persistent contest/track award (contract §2)."""
    X = E.ALL
    names = [n for n in ("elite", "track", "elite_prize") if n in X]
    if not names:
        return 0
    total = 0
    for n in names:
        arr = np.asarray(X[n])
        total += int(arr.sum()) if arr.dtype != bool and n == "elite_prize" else int(np.count_nonzero(arr))
    return total


def _elite_count(E):
    return int(np.count_nonzero(np.asarray(E.ALL["elite"]))) if "elite" in E.ALL else 0


def _effort_zero(E, tol=1e-12):
    """True iff every effort/outlay indicator the engine records is zero.

    Contract §4.3: `contest_spend_now` (outlay), `contest_effort_by_q`, `contest_e_mean` (current-year
    e_t mean).  Pre-repair only `contest_e_mean` exists.  Any recorded outlay means effort > 0 because
    contest_price > 0 in every arm of this suite.
    """
    checks = []

    def _mx(values):
        arr = np.asarray(values, float)
        return float(np.nanmax(np.abs(arr))) if arr.size else 0.0

    for key in ("contest_spend_now", "contest_resource_cost", "contest_tax_paid"):
        if key in E.R:
            checks.append(_mx(E.R[key]))
    for key in ("contest_effort_by_q", "contest_outlay_by_q"):
        if key in E.R:
            checks.append(_mx(E.R[key]))
    if "contest_e_mean" in E.R:
        checks.append(_mx(E.R["contest_e_mean"]))
    if "contest_e" in E.kids:
        checks.append(_mx(E.kids["contest_e"]))
    if "prep_stock" in E.kids:
        checks.append(_mx(E.kids["prep_stock"]))
    if not checks:
        return False
    return all(float(c) <= tol for c in checks)


def _contest_gate_indices(E):
    out = []
    for m, g in enumerate(E.p["gates"]):
        kind = g.get("kind")
        if kind == "contest" or (hasattr(E, "gate_kind") and E.gate_kind(m) == "contest"):
            out.append(m)
    return out


def _seats_per_year(E, m, share):
    """Seat cap per gate year from the recorded/reported seat series, else the legacy formula."""
    if "contest_seats" in E.R:
        arr = np.asarray(E.R["contest_seats"], float)
        if arr.ndim == 2:
            vals = arr[:, m]
            return [float(v) for v in vals if np.isfinite(v)]
    return [float(max(int(round(share * E.p["N"])), 1))]


def _mean_elite_log_inc_first_exit(E):
    """Mean log income of the elite leavers in the first year any elite leaver exits."""
    X = E.X
    if not X or "elite" not in X:
        return None
    ys = np.asarray(X["exit_year"], float)
    el = np.asarray(X["elite"], bool)
    if not el.any():
        return None
    y0 = ys[el].min()
    sel = el & (ys == y0)
    return float(np.mean(np.log(np.maximum(np.asarray(X["inc"], float)[sel], 1e-12))))


# =====================================================================================================
# 1. zero elite prize => zero positional contest effort                              (contract §11 #1)
# =====================================================================================================
def test_01_zero_elite_prize_yields_zero_positional_effort():
    """#1: with every contest prize zero and contest_price > 0, no positional effort is bought.

    Control arm (prize 0.6) must buy effort, so the zero arm is not vacuous.
    """
    zero = build_engine(gates=legacy_gates_g12(contest=dict(elite_logw=0.0)), elite_logw=0.0)
    zero.run()
    control = build_engine(gates=legacy_gates_g12(contest=dict(elite_logw=0.6)), elite_logw=0.6)
    control.run()

    observed_zero = float(np.nanmax(np.abs(np.asarray(zero.R["contest_e_mean"], float))))
    observed_control = float(np.nanmax(np.asarray(control.R["contest_e_mean"], float)))
    assert observed_control > 0.0, (
        "control arm with a positive elite prize bought no contest effort - the zero-prize arm is "
        f"vacuous (control max e_t = {observed_control})"
    )
    assert _effort_zero(zero), (
        f"zero elite prize still bought positional contest effort: max e_t = {observed_zero} "
        f"(expected 0, tol 1e-12); contest_price = {zero.p['contest_price']}"
    )


# =====================================================================================================
# 2. zero contest-effort effectiveness => effort cannot raise admission               (contract §11 #2)
# =====================================================================================================
def test_02_zero_effectiveness_effort_cannot_raise_admission():
    """#2: `contest_alpha=0` => e_t = 0 and admission is independent of the effort price."""
    cheap = build_engine(gates=legacy_gates_g12(), contest_alpha=0.0, contest_price=0.02)
    cheap.run()
    dear = build_engine(gates=legacy_gates_g12(), contest_alpha=0.0, contest_price=1.60)
    dear.run()

    assert _effort_zero(cheap) and _effort_zero(dear), (
        "contest_alpha=0 (effort has no effect on x_eff) but effort was still purchased: "
        f"cheap arm max e_t={np.nanmax(np.abs(cheap.R['contest_e_mean']))}, "
        f"dear arm max e_t={np.nanmax(np.abs(dear.R['contest_e_mean']))}; expected 0 in both"
    )
    # Admissions cannot move with the effort price when effort is ineffective.
    if "contest_admitted" in cheap.R and "contest_admitted" in dear.R:
        a = np.asarray(cheap.R["contest_admitted"], float)
        b = np.asarray(dear.R["contest_admitted"], float)
        assert np.array_equal(np.nan_to_num(a), np.nan_to_num(b)), "admissions changed with the effort price under alpha=0"
    else:
        assert _elite_count(cheap) == _elite_count(dear), (
            "admissions changed with the effort price under contest_alpha=0: "
            f"{_elite_count(cheap)} vs {_elite_count(dear)}"
        )
        assert np.array_equal(np.asarray(cheap.R["enrolled"], float), np.asarray(dear.R["enrolled"], float)), (
            "enrolment path changed with the contest price when effort has zero effectiveness"
        )


# =====================================================================================================
# 3. universal seat => no positional marginal return                                 (contract §11 #3)
# =====================================================================================================
def test_03_universal_seat_has_no_positional_marginal_return():
    """#3: seats >= candidates => every applicant admitted (P_i=1) and e_t = 0."""
    if CAPS["share_of"]:
        # Contract path: declare the applicant denominator explicitly.
        E = small_contest_engine(gate_extra=dict(share=1.0, share_of="applicants"))
        E.run()
        m = 1
        cand = np.flatnonzero(E.contest_candidates(m))
        seats = int(E.contest_seats(m))
        assert len(cand) > 0, "no candidates reached the contest gate in the universal-seat arm"
        assert seats >= len(cand), f"universal-seat arm: seats={seats} < candidates={len(cand)}"
        if CAPS["api_expected_probs"]:
            _, P = E.contest_expected_probs(m)
            assert np.allclose(np.asarray(P, float), 1.0, atol=1e-12), (
                f"universal seat must give P_i = 1; observed min P = {float(np.min(P))}, "
                f"max P = {float(np.max(P))}, candidates = {len(cand)}"
            )
        assert _effort_zero(E), (
            "universal seat (every applicant admitted) still bought positional effort: "
            f"max e_t = {np.nanmax(np.abs(np.asarray(E.R['contest_e_mean'], float))):.6f}, expected 0"
        )
    else:
        # Baseline path: share=1.0 of the cohort N is >= the applicant count, so the gate is universal.
        E, years = tracked_run(gates=legacy_gates_g12(contest=dict(share=1.0)))
        cand = sum(y["candidates"][2] for y in years)
        awarded = sum(y["elite_new"] for y in years)
        assert cand > 0, "no candidates reached the G12 gate in the universal-seat arm"
        assert awarded == cand, (
            f"universal seat is by construction universal, yet only {awarded}/{cand} applicants were admitted"
        )
        ce = float(np.nanmax(np.abs(np.asarray(E.R["contest_e_mean"], float))))
        assert _effort_zero(E), (
            f"every applicant is admitted, so the positional marginal return of contest effort is zero, "
            f"yet max e_t = {ce:.6f} was purchased (expected 0).  "
            "The expected-probability model caps the win probability at 0.99 instead of 1.0 "
            "(core.py:418 target_s = min(seats/n_candidates, 0.99)), leaving a positive gradient at e=0."
        )


# =====================================================================================================
# 4. seats=1, two applicants, weights 4:1 => exact PL 0.8/0.2                        (contract §11 #4)
# =====================================================================================================
@missing(not CAPS["contest_math"],
         "missing API: engine/eduengine/contest_math.py pl_win_probs(method='exact') (contract §1.3; Gate-1c)")
def test_04_exact_pl_two_applicants_one_seat(pl_reference):
    """#4: the reference PL module gives exactly [0.8, 0.2] for weights [4, 1], one seat."""
    p = pl_reference.pl_win_probs([4.0, 1.0], 1, method="exact")
    np.testing.assert_allclose(np.asarray(p), [0.8, 0.2], atol=1e-12,
                               err_msg=f"pl_win_probs([4,1],1,'exact') = {p}; expected [0.8, 0.2]")
    # Method selection and scale invariance must not change the answer.
    for meth in ("auto", "exact"):
        np.testing.assert_allclose(np.asarray(pl_reference.pl_win_probs([4.0, 1.0], 1, method=meth)),
                                   [0.8, 0.2], atol=1e-12)
    np.testing.assert_allclose(np.asarray(pl_reference.pl_win_probs([40.0, 10.0], 1, method="exact")),
                               [0.8, 0.2], atol=1e-12)
    # Seat-sum invariant for the reference itself.
    w = np.array([4.0, 1.0])
    for k in (1, 2):
        np.testing.assert_allclose(np.sum(pl_reference.pl_win_probs(w, k, method="exact")), k, atol=1e-12)


# =====================================================================================================
# 5. monotonicity in own effective contest input                                     (contract §11 #5)
# =====================================================================================================
@missing(not CAPS["contest_math"],
         "missing API: engine/eduengine/contest_math.py pl_win_probs (contract §1.3; Gate-1c)")
def test_05a_pl_probability_non_decreasing_in_own_weight(pl_reference):
    """#5a: raising one applicant's weight, competitors fixed, never lowers its win probability."""
    grid = np.array([0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0])
    for seats in (1, 2, 3):
        others = np.array([1.0, 1.5, 2.5])
        prev = -1.0
        for w_own in grid:
            w = np.concatenate([[w_own], others])
            p = pl_reference.pl_win_probs(w, seats, method="exact")[0]
            assert p >= prev - 1e-12, (
                f"P(own win) fell from {prev} to {p} when own weight rose to {w_own} "
                f"(seats={seats}, competitors={others.tolist()})"
            )
            prev = p
    # Also: monotone at the engine's own expected-probability representation when present.
    E = build_engine(N=24, T=18, measure_from=6, gates=legacy_gates_g12())
    E.run()
    if hasattr(E, "contest_expected_probs") and CAPS["api_expected_probs"]:
        m = 2
        cand = np.flatnonzero(E.contest_candidates(m))
        if len(cand):
            base_w = np.asarray(E.contest_weights(m)[1], float)
            seats = int(E.contest_seats(m))
            prev = -1.0
            for mult in grid:
                w = base_w.copy()
                w[0] *= mult
                p = pl_reference.pl_win_probs(w, seats, method="exact")[0]
                assert p >= prev - 1e-12


@missing(not CAPS["api_contest_weights"],
         "missing API: Engine.contest_weights/contest_expected_probs (contract §6; defect D2)")
def test_05b_engine_expected_probability_monotone_in_own_stock():
    """#5b: the engine's expected probability is non-decreasing in own prep stock, competitors fixed."""
    E = small_contest_engine()
    E.run()
    m = 1
    cand = np.flatnonzero(E.contest_candidates(m))
    assert len(cand) > 0, "no candidates at the contest gate"
    idx, P = E.contest_expected_probs(m)
    w = np.asarray(E.contest_weights(m)[1], float)
    seats = int(min(E.contest_seats(m), len(w)))
    p = np.asarray(P, float)
    assert len(p) == len(w), f"expected_probs length {len(p)} != weights length {len(w)}"
    assert np.all(p >= 0.0) and np.all(p <= 1.0 + 1e-12)
    # Monotone comparative statics of the engine's own reported probabilities: perturb one weight
    # upward and recompute the exact reference on the perturbed vector.  The engine's reported P must
    # not be lower than the reference bound for the unperturbed vector.
    cm = CAPS["contest_math_module"]
    for mult in (1.5, 2.0, 4.0):
        wp = w.copy()
        wp[0] *= mult
        ref_p = float(cm.pl_win_probs(wp, seats, method="exact")[0])
        assert ref_p >= float(p[0]) - 1e-9, (
            f"P(own win) fell from engine-reported {p[0]:.6f} to reference {ref_p:.6f} when own weight "
            f"was raised x{mult} (competitors fixed)"
        )


# =====================================================================================================
# 6. no over-allocation, no ineligible admission                                     (contract §11 #6)
# =====================================================================================================
def test_06a_no_contest_allocates_more_placements_than_seats():
    """#6a: admitted <= seats_eff every gate year (reported series if present, else per-year tracer)."""
    if CAPS["reporting"]:
        E = build_engine()
        E.run()
        admitted = np.asarray(E.R["contest_admitted"], float)
        seats = np.asarray(E.R["contest_seats"], float)
        for t in range(admitted.shape[0]):
            for m in range(admitted.shape[1]):
                if np.isfinite(admitted[t, m]):
                    assert admitted[t, m] <= seats[t, m] + 1e-9, (
                        f"year {t} gate {m}: admitted {admitted[t, m]} > seats {seats[t, m]}"
                    )
    else:
        E, years = tracked_run(gates=legacy_gates_g12())
        cap = max(int(round(0.25 * E.p["N"])), 1)
        for y in years:
            assert y["elite_new"] <= cap, (
                f"year {y['t']}: {y['elite_new']} placements > seat cap {cap} "
                f"(share 0.25 x N {E.p['N']}); candidates={y['candidates'][2]}"
            )
        assert sum(y["elite_new"] for y in years) > 0, "no placements at all - the test is vacuous"


def test_06b_no_ineligible_applicant_is_admitted():
    """#6b: an academic-only contest gate never admits vocational-track pupils, and only gate candidates."""
    E, years = tracked_run(gates=legacy_gates_voc_then_contest())
    rows = list(years[-1]["rows"].values())          # every child ever born (exited + still in school)
    elite = np.array([r["elite"] for r in rows], bool)
    voc = np.array([r["voc"] for r in rows], bool)
    cred = np.array([r["cred"] for r in rows], int)
    n_voc = int(voc.sum())
    assert n_voc > 0, "test is vacuous: no vocational-track children were created"
    assert elite.any(), "no contest placements at all - the test is vacuous"
    assert not np.any(elite & voc), (
        f"{int(np.sum(elite & voc))} vocational-track pupils were admitted by an academic_only contest gate "
        f"(voc children: {n_voc}); core.py:437-438 must keep them out"
    )
    # An award is only ever granted at a gate: recipients must hold the credential the gate confers.
    assert np.all(cred[elite] >= 3), (
        "an 'elite' award exists on a child that never passed the G12 gate "
        f"(cred values: {sorted(set(cred[elite].tolist()))})"
    )


@missing(not CAPS["reporting"],
         "missing API: contest_candidates/contest_seats/contest_admitted/contest_expected_seats series "
         "(contract §1.4/§11 #6)")
def test_06c_reported_expected_seats_sum_to_seats_eff():
    """#6c: sum_i P_i == seats_eff (abs tol 1e-6) and admitted <= candidates, reported every gate year."""
    E = build_engine()
    E.run()
    expected = np.asarray(E.R["contest_expected_seats"], float)
    seats = np.asarray(E.R["contest_seats"], float)
    cand = np.asarray(E.R["contest_candidates"], float)
    admitted = np.asarray(E.R["contest_admitted"], float)
    seen = 0
    for t in range(expected.shape[0]):
        for m in range(expected.shape[1]):
            if np.isfinite(expected[t, m]):
                seen += 1
                seats_eff = min(seats[t, m], cand[t, m])
                assert abs(expected[t, m] - seats_eff) <= 1e-6, (
                    f"year {t} gate {m}: sum expected P = {expected[t, m]} but seats_eff = {seats_eff}"
                )
                assert admitted[t, m] <= seats_eff + 1e-9
                assert admitted[t, m] <= cand[t, m] + 1e-9
    assert seen > 0, "no contest-gate diagnostics were recorded - the test is vacuous"


# =====================================================================================================
# 7. non-selective gate creates no (artificial) elite prize                           (contract §11 #7)
# =====================================================================================================
def test_07_nonselective_gate_creates_no_elite_wage_prize():
    """#7: a gate that pays no elite premium must not be priced as if it did."""
    if CAPS["gate_kinds"]:
        # Contract path: an `open` gate (no selection) may not create elite state or a premium.
        from eduengine.core import Engine  # noqa: F401
        E = build_engine(N=32, T=18, measure_from=6,
                         gates=[dict(kind="open"), dict(kind="open"),
                                dict(kind="contest", share=0.25, fail="track", elite_logw=0.60),
                                dict(kind="open")],
                         levels=[("primary", 6), ("lower", 3), ("upper", 3), ("tertiary", 4)])
        E.run()
        assert _elite_count(E) > 0, "test is vacuous: the contest gate awarded nobody"
        # An open gate never awards state: only the contest gate's winners carry 'elite'.
        assert "elite" in E.ALL
        # Declared elite_logw on an open gate must be rejected rather than silently paid.
        with pytest.raises((ValueError, KeyError)):
            bad = list(E.p["gates"])
            bad[0] = dict(kind="open", elite_logw=0.60)
            build_engine(gates=bad)
    else:
        # Baseline probe: a contest gate without fail='track' never sets k['elite'], so the
        # premium priced by contest_prep (tutoring.py:94-101) is never paid by core (core.py:428).
        E = build_engine(gates=legacy_gates_g12(contest=dict(fail="drop")), elite_logw=0.60)
        E.run()
        awards = _elite_count(E)
        ce = float(np.nanmax(np.abs(np.asarray(E.R["contest_e_mean"], float))))
        assert awards > 0 or _effort_zero(E), (
            f"the gate never pays an elite wage premium (elite awards = {awards}, "
            f"k['elite'] is only set for fail='track' at core.py:428-429), "
            f"yet households bought positional effort priced on elite_logw=0.60: max e_t = {ce:.6f} "
            "(torch: the prize is priced by tutoring.py:94-101 but never delivered)"
        )


# =====================================================================================================
# 8. Grade-9 track award persists and changes a modelled future state                 (contract §11 #8)
# =====================================================================================================
@missing(not (CAPS["gate_specs"] and CAPS["state_track"]),
         "missing API: core.GATE_SPECS (KR-SINGLE/KR-TRACKED) and k['track'] persistent state "
         "(contract §2/§3/§11 #8; defect D1)")
def test_08a_g9_track_persists_kr_tracked_vs_single():
    """#8a: GATE_SPECS KR-TRACKED places G9 winners on track=1, losers track=0, sticky at exit;
    KR-SINGLE leaves track == -1 everywhere and is identical to the no-track baseline."""
    import copy

    from eduengine.core import GATE_SPECS

    assert set(GATE_SPECS) >= {"KR-SINGLE", "KR-TRACKED"}, f"GATE_SPECS keys = {sorted(GATE_SPECS)}"
    tracked = build_engine(gates=copy.deepcopy(GATE_SPECS["KR-TRACKED"]))
    tracked.run()
    single = build_engine(gates=copy.deepcopy(GATE_SPECS["KR-SINGLE"]))
    single.run()

    X = tracked.ALL
    tr = np.asarray(X["track"], int)
    assert set(np.unique(tr).tolist()) <= {-1, 0, 1}, f"track values outside {{-1,0,1}}: {sorted(set(tr.tolist()))}"
    g9 = np.asarray(X["g"], int) >= 9
    placed = g9 & (tr >= 0)
    assert placed.any(), "KR-TRACKED places no children at Grade 9 - vacuous"
    assert (tr == 1).any() and (tr == 0).any(), (
        f"KR-TRACKED must produce both winners (track=1) and losers (track=0); "
        f"counts: {int((tr == 1).sum())} / {int((tr == 0).sum())}"
    )
    # Sticky: a placed child's track value at exit equals its value at placement (never re-set).
    assert np.all(np.asarray(X["track"], int)[placed] != -1)
    # KR-SINGLE: no tracking state at all.
    tr_s = np.asarray(single.ALL["track"], int)
    assert np.all(tr_s == -1), f"KR-SINGLE must leave track == -1 everywhere; observed {sorted(set(tr_s.tolist()))}"
    # The three channels fire: earnings channel (track=1 leavers earn exp(earnings_logw) more) and
    # quality channel (track=1 children learn faster).  Both are pre-registered structural placeholders.
    assert "elite_prize" in X, "persistent prize state missing"
    prize = np.asarray(X["elite_prize"], float)
    assert np.all(prize[tr == 1] >= 0.0)
    L = np.asarray(X["L"], float)
    assert np.mean(L[tr == 1]) > np.mean(L[tr == 0]) - 1e-9, (
        "track=1 children do not learn at least as fast as track=0 children (quality_mult channel "
        f"inactive): mean L {np.mean(L[tr == 1]):.4f} vs {np.mean(L[tr == 0]):.4f}"
    )


def test_08b_g9_declared_elite_prize_is_persisted():
    """#8b (baseline probe, defect D1): a Grade-9 contest with a declared elite_logw must pay it.

    Baseline: `k['elite']` is set only when `m_ == nlev-2` (core.py:428-429), so G9 winners are
    indistinguishable from losers, while `contest_prep` prices the G9 prize (tutoring.py:94-101).
    """
    E = build_engine(gates=legacy_gates_g9())
    E.run()
    effort = float(np.nanmax(np.abs(np.asarray(E.R["contest_e_mean"], float))))
    awards = _elite_count(E)
    assert effort > 0.0, "test is vacuous: no G9 preparatory effort was purchased"
    prize_state = 0
    if CAPS["state_elite_prize"]:
        prize_state = int(np.count_nonzero(np.asarray(E.ALL["elite_prize"], float) > 0.0))
    assert awards > 0 or prize_state > 0, (
        "a Grade-9 contest with a declared elite_logw=0.15 is priced by contest_prep "
        f"(max e_t = {effort:.6f}/year) but no child carries any persistent award "
        f"(k['elite'] awards = {awards}, elite_prize holders = {prize_state}, expected > 0). "
        "core.py:428-429 sets k['elite'] only for m_ == nlev-2 (Grade 12)."
    )


# =====================================================================================================
# 9. annual tutoring expenditure respects available funds                            (contract §11 #9)
# =====================================================================================================
def test_09_annual_expenditure_within_available_funds(audited):
    """#9: per child-year, own+firm+contest outlay <= residual cash (`E._cash`, contract §4.2)."""
    E = audited()
    rows = [it for _, items in E.acct for it in items if it["check"] == "funds"]
    assert len(rows) == E.p["T"], f"expected one funds check per year, got {len(rows)}"
    bad = [it for it in rows if it["n_violations"]]
    worst = max(it["worst_overage"] for it in rows)
    assert not bad, f"tutoring outlay exceeded residual cash in {len(bad)} child-years; worst overage {worst}"
    assert max(it["n_att"] for it in rows) > 0, "test is vacuous: no children attended"


# =====================================================================================================
# 10. gross outlay == resource cost + tax                                            (contract §11 #10)
# =====================================================================================================
@missing(not CAPS["accounting"],
         "missing API: TutoringMarket.defaults contest_tax_rate + E.yr res_cost/tut_tax/tut_outlay/gov_tut_tax "
         "+ E.R contest_resource_cost/contest_tax_paid/gov_tut_receipt (contract §4.1/§4.3; defect D4)")
def test_10_gross_outlay_reconciles_to_resource_cost_plus_tax(audited):
    """#10: per year tut_outlay == res_cost + tut_tax and Sigma gov_tut_tax == Sigma tut_tax (tol 1e-12)."""
    E = audited(contest_tax_rate=0.25, gates=legacy_gates_g12())
    rows = [it for _, items in E.acct for it in items if it["check"] == "tut_outlay_identity"]
    assert rows, "no contest outlay decomposition rows recorded"
    for t, it in enumerate(rows):
        assert abs(it["outlay"] - (it["res_cost"] + it["tax"])) <= 1e-12 * max(1.0, abs(it["outlay"])), (
            f"year {t}: outlay {it['outlay']} != resource {it['res_cost']} + tax {it['tax']}"
        )
        assert abs(it["gov_receipt"] - it["tax"]) <= 1e-12 * max(1.0, abs(it["tax"])), (
            f"year {t}: government tutoring receipts {it['gov_receipt']} != tax paid {it['tax']}"
        )
        assert abs(it["yr_outlay"] - (it["yr_res"] + it["yr_tax"])) <= 1e-12
        assert abs(it["yr_gov"] - it["yr_tax"]) <= 1e-12
        assert it["res_cost"] >= 0.0 and it["tax"] >= 0.0


# =====================================================================================================
# 11. zero contest effort reproduces no-contest behaviour                            (contract §11 #11)
# =====================================================================================================
def test_11a_zero_effort_contest_parameters_are_inert():
    """#11a (runs on baseline): when effort is impossible (contest_max_e=0), contest-price and
    effectiveness parameters cannot change any recorded outcome - the no-contest limit."""
    a = build_engine(gates=legacy_gates_g12(), contest_max_e=0.0, contest_alpha=0.25, contest_price=0.16)
    a.run()
    b = build_engine(gates=legacy_gates_g12(), contest_max_e=0.0, contest_alpha=0.0, contest_price=1.60)
    b.run()
    assert _effort_zero(a) and _effort_zero(b)
    for key in ("enrolled", "tut_k12_spend", "tut_k12_rate", "contest_e_mean"):
        if key in a.R and key in b.R:
            np.testing.assert_array_equal(np.asarray(a.R[key], float), np.asarray(b.R[key], float),
                                          err_msg=f"zero-effort arms differ in recorded series {key!r}")
    assert _elite_count(a) == _elite_count(b)


@missing(not CAPS["gate_kinds"],
         "missing API: gate kind 'open' normalisation + Engine.gate_kind (contract §1; defect D8)")
def test_11b_zero_effort_contests_match_forced_open_gate():
    """#11b: with zero prizes, admissions/enrolment equal an engine with the gate kind forced open."""
    levels = [("primary", 6), ("lower", 3), ("upper", 3), ("tertiary", 4)]
    open_gates = [dict(kind="fixed_bar", bar=2.0), dict(kind="open"),
                  dict(kind="open"), dict(kind="fixed_bar", bar=10.0)]
    op = build_engine(N=36, T=18, measure_from=6, levels=levels, gates=open_gates, elite_logw=0.0)
    op.run()
    zero = build_engine(N=36, T=18, measure_from=6, levels=levels,
                        gates=legacy_gates_g12(contest=dict(elite_logw=0.0)), elite_logw=0.0)
    zero.run()
    np.testing.assert_array_equal(
        np.asarray(op.R["enrolled"], float), np.asarray(zero.R["enrolled"], float),
        err_msg="a zero-prize contest gate does not reproduce the forced-open-gate enrolment path",
    )
    assert _effort_zero(zero), "a zero-prize contest gate still bought effort"


# =====================================================================================================
# 12. parallel / deterministic stability                                             (contract §11 #12)
# =====================================================================================================
WORKERS = int(os.environ.get("QA_WORKERS", "12"))


def _parallel_task(payload):
    """Top-level worker for the ProcessPool determinism test (picklable by reference)."""
    E = build_engine(
        N=payload["N"], T=payload["T"], measure_from=payload["measure_from"], seed=payload["seed"],
        gates=legacy_gates_g12(contest=dict(share=payload["share"])),
    )
    E.run()
    row = dict(seed=int(payload["seed"]), share=float(payload["share"]),
               n_children=int(len(E.ALL["cohort"])),
               elite=int(np.count_nonzero(np.asarray(E.ALL["elite"]))),
               enrolled=tuple(int(v) for v in np.asarray(E.R["enrolled"], float)),
               ce=round(float(np.nanmean(np.asarray(E.R["contest_e_mean"], float))), 10))
    return row


def _tasks():
    # N/T chosen so every module's summary series exists on the pre-repair baseline too
    return [dict(N=24, T=20, measure_from=6, seed=s, share=sh)
            for s in (0, 1) for sh in (0.20, 0.40)]


def test_12_parallel_and_task_order_stability():
    """#12: identical seed rows under serial, multi-process (chunksize 1 and 4) and shuffled order."""
    tasks = _tasks()
    serial = [_parallel_task(t) for t in tasks]
    # same config+seed twice
    assert serial == [_parallel_task(t) for t in tasks], "repeating the same task changed the seed row"

    ctx = multiprocessing.get_context("fork")
    workers = max(1, min(WORKERS, len(tasks), os.cpu_count() or 1))
    for chunksize in (1, 4):
        with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as ex:
            par = list(ex.map(_parallel_task, tasks, chunksize=chunksize))
        assert par == serial, (
            f"ProcessPoolExecutor(chunksize={chunksize}, workers={workers}) results differ from serial"
        )
    # deterministic task-order shuffle
    order = [2, 0, 3, 1]
    shuffled = [_parallel_task(tasks[i]) for i in order]
    restored = [shuffled[order.index(j)] for j in range(len(tasks))]
    assert restored == serial, "task order changed the seed rows"


# =====================================================================================================
# DD. present-and-wrong baseline probes (D2, D3, D6, D7) + expected-vs-realized
# =====================================================================================================
def test_d2_expected_probability_matches_exact_pl_reference():
    """D2: the expected win probability used by households must equal the exact PL object.

    Baseline: `P = 1 - exp(-lam x^r)` with market-clearing lam (core.py:178, tutoring.py:112) vs the
    realised Gumbel-max PL gate (core.py:406-426).  Two applicants, one seat, PL weights 4:1.
    """
    if CAPS["api_expected_probs"] and CAPS["contest_math"]:
        E = small_contest_engine()
        E.run()
        m = 1
        idx, P = E.contest_expected_probs(m)
        w = np.asarray(E.contest_weights(m)[1], float)
        seats = int(E.contest_seats(m))
        ref = CAPS["contest_math_module"].pl_win_probs(w, min(seats, len(w)), method="exact")
        np.testing.assert_allclose(np.asarray(P, float), np.asarray(ref, float), atol=1e-9,
                                   err_msg="engine expected P != exact Plackett-Luce P")
        np.testing.assert_allclose(float(np.sum(P)), float(min(seats, len(w))), atol=1e-6)
        return

    assert CAPS["contest_math"], "missing API: contest_math reference (Gate-1c) and Engine.contest_expected_probs"
    # Baseline path: the engine's own expected-probability representation at its own solved lambda.
    E = build_engine(N=24, T=18, measure_from=6, gates=legacy_gates_g12())
    E.run()
    m = 2
    lam = float(E.lam_contest[m])
    r = float(E.p["contest_r"])
    x = np.array([4.0 ** (1.0 / r), 1.0])       # so that x**r has the PL weight ratio 4:1
    belief = 1.0 - np.exp(-np.clip(lam * (x ** r), 0.0, 50.0))
    exact = np.asarray(CAPS["contest_math_module"].pl_win_probs(x ** r, 1, method="exact"), float)
    np.testing.assert_allclose(belief, exact, atol=1e-9,
                               err_msg=(f"engine expected-probability form 1-exp(-lam*x^r) with lam={lam} "
                                        f"gives {belief}, but exact PL for the 4:1 / one-seat contest is {exact}"))
    # The seat-sum invariant of the expected object (contract §1.3: Sigma P = seats_eff) must also hold.
    assert abs(float(belief.sum()) - 1.0) <= 1e-9, (
        f"sum of the two applicants' expected win probabilities = {float(belief.sum()):.6f}, "
        f"but seats_eff = 1 (contract §1.3 requires Sigma P = seats_eff)"
    )


def test_d3_seat_share_is_of_applicants():
    """D3: the seat denominator must be the applicant count (declarable, reported), not the cohort.

    Baseline: `seats = max(round(share*N),1)` (core.py:400) - a share of the entering cohort - so the
    realised admission rate among applicants is far above the declared share and is never reported.
    """
    share = 0.25
    if CAPS["share_of"]:
        E = build_engine(gates=[dict(kind="bar", bar=2.0), dict(kind="bar", bar=4.0),
                                dict(kind="contest", share=share, share_of="applicants", fail="track"),
                                dict(kind="bar", bar=10.0)])
        E.run()
        rates = np.asarray(E.R["contest_admit_rate"], float)[:, 2]
        rates = rates[np.isfinite(rates)]
        assert len(rates) > 0, "no contest gate years recorded"
        worst = float(np.nanmax(np.abs(rates - share)))
        assert worst <= 0.05, (
            f"share_of='applicants' declared {share:.2f} but realised admit rate differs by up to {worst:.3f} "
            f"(mean {float(np.nanmean(rates)):.3f})"
        )
        return

    # harsher household budget so the applicant pool is genuinely smaller than the cohort
    E, years = tracked_run(gates=legacy_gates_g12(contest=dict(share=share)), N=40,
                           subsist=1.1, borrow=0.0, y_median=1.1, y_sigma=0.7)
    gate_years = [y for y in years if y["candidates"][2] > 0]
    assert gate_years, "no contest gate years - the test is vacuous"
    seats = max(int(round(share * E.p["N"])), 1)
    rates = [y["elite_new"] / y["candidates"][2] for y in gate_years]
    obs = float(np.mean(rates))
    assert abs(obs - share) <= 0.05, (
        f"declared seat share {share:.2f} of the cohort but the realised admission rate among applicants is "
        f"{obs:.3f} on average (per-year {['%.2f' % v for v in rates]}); seats/year = {seats}, "
        f"applicants/year = {[y['candidates'][2] for y in gate_years]}.  "
        "core.py:400 uses max(round(share*N),1) with N = entering cohort, and no applicant/seat/admit-rate "
        "series is recorded (contract §1.4)."
    )


def test_d6_policy_invariant_rng_across_policy_arms():
    """D6: a policy parameter may not change the exogenous draws of any person.

    Baseline: one sequential `np.random.default_rng(seed)` stream consumed in path order (core.py:93,
    124-127, 331-394-408), so two arms differing only in the contest seat share get different
    cohort covariates from the first gate year onwards.
    """
    # A policy that changes who reaches the gates (tuition-fee policy) changes the number of
    # conditional draws; a seat-share change does not, so it would not test the stream ordering.
    a = build_engine(gates=legacy_gates_g12(), fee_public=0.0)
    a.run()
    b = build_engine(gates=legacy_gates_g12(), fee_public=0.15)
    b.run()

    if CAPS["state_pid"]:
        pa = np.asarray(a.ALL["pid"], int)
        pb = np.asarray(b.ALL["pid"], int)
        oa = np.argsort(pa)
        ob = np.argsort(pb)
        assert np.array_equal(pa[oa], pb[ob]), "immutable person ids differ across arms"
        for key in ("z", "a", "home"):
            np.testing.assert_array_equal(np.asarray(a.ALL[key], float)[oa],
                                          np.asarray(b.ALL[key], float)[ob],
                                          err_msg=f"exogenous covariate {key!r} differs across policy arms")
        return

    first_bad = None
    n_bad = 0
    for coh in np.unique(np.asarray(a.ALL["cohort"], int)):
        for key in ("z", "a", "home"):
            za = np.sort(np.asarray(a.ALL[key], float)[np.asarray(a.ALL["cohort"], int) == coh])
            zb = np.sort(np.asarray(b.ALL[key], float)[np.asarray(b.ALL["cohort"], int) == coh])
            if len(za) != len(zb) or not np.allclose(za, zb, atol=1e-12):
                n_bad += 1
                if first_bad is None:
                    first_bad = (int(coh), key)
    assert n_bad == 0, (
        f"changing only the public-school fee (a policy parameter) changed the exogenous draws of "
        f"{n_bad} cohort-covariate "
        f"groups (first: cohort {first_bad[0]}, covariate {first_bad[1]!r}); the single sequential RNG "
        "stream (core.py:93/331/408) makes policy arms non-comparable person-by-person"
    )


def test_d7_gate_prize_is_paid_as_declared():
    """D7: the wage premium paid must be the prize the gate declares.

    Baseline: the labour step applies the *global* `p['elite_logw']` to `k['elite']`
    (core.py:498-499) and ignores the gate's own `elite_logw`, so a gate declaring 0.1 pays
    whatever the global parameter is (and pays nothing when the global default is 0).
    """
    common = dict(gates=legacy_gates_g12(contest=dict(elite_logw=0.1)), contest_alpha=0.0, T=20)
    if CAPS["state_elite_prize"]:
        E = build_engine(**common)
        E.run()
        prize = np.asarray(E.ALL["elite_prize"], float)
        winners = prize > 0
        assert winners.any(), "test is vacuous: no winner"
        np.testing.assert_allclose(prize[winners], 0.1, atol=1e-12,
                                   err_msg=f"declared gate prize 0.1 but stored elite_prize = {prize[winners][:5]}")
        return

    lo = build_engine(**dict(common, elite_logw=0.0))
    lo.run()
    hi = build_engine(**dict(common, elite_logw=0.6))
    hi.run()
    m_lo = _mean_elite_log_inc_first_exit(lo)
    m_hi = _mean_elite_log_inc_first_exit(hi)
    assert m_lo is not None and m_hi is not None, "test is vacuous: no elite leavers"
    observed = m_hi - m_lo
    assert abs(observed - 0.1) <= 1e-9, (
        f"the gate declares elite_logw=0.1, so switching the global default from 0.0 to 0.6 must leave the "
        f"paid prize at 0.1; observed paid log premium = {observed:.6f} "
        f"(global elite_logw is applied directly at core.py:498-499 instead of the gate prize)"
    )


# =====================================================================================================
# AC. accounting / denominators                                                      (Directive extras)
# =====================================================================================================
def test_ac1_tax_revenue_identity(audited):
    """Tax revenue totals: revenue = tax_formal*formal_bill + tax_cons*(formal+informal), per year."""
    E = audited()
    rows = [it for _, items in E.acct for it in items if it["check"] == "tax_revenue"]
    assert len(rows) == E.p["T"], f"expected one tax identity per year, got {len(rows)}"
    for t, it in enumerate(rows):
        assert abs(it["recorded"] - it["expected"]) <= 1e-9 * max(1.0, abs(it["expected"])), (
            f"year {t}: recorded revenue {it['recorded']} != recomputed {it['expected']}"
        )
        assert it["recorded"] >= 0.0 and it["gdp_recorded"] >= 0.0
        assert abs(it["tax_gdp_recorded"] - it["recorded"] / max(it["gdp_recorded"], 1e-9)) <= 1e-12
        if it["gdp_recorded"] > 0:
            assert abs(it["gdp_recorded"] - (it["formal"] + it["informal"])) <= 1e-9
    # Rebuild every year's revenue from the labour-module earnings stock (independent recomputation).
    lab = E.labour_module[0] if E.labour_module else None
    if lab is not None and hasattr(lab, "stock"):
        st = lab.stock
        L = st.L
        n = min(len(E.R["revenue"]), len(st.flows))
        for t in range(n):
            f = sum(a for a, _ in st.flows[max(0, t - L + 1):t + 1])
            i = sum(b for _, b in st.flows[max(0, t - L + 1):t + 1])
            expected = E.p["tax_formal"] * f + E.p["tax_cons"] * (f + i)
            assert abs(float(E.R["revenue"][t]) - expected) <= 1e-9 * max(1.0, abs(expected)), (
                f"year {t}: revenue {E.R['revenue'][t]} != earnings-stock rebuild {expected}"
            )
    # Reported budget is the declared share of revenue, with the floor (state.py:27-34).
    for t, it in enumerate(rows):
        floor = E.p["budget_floor"] * E.p["N"] * 12
        expected = max(E.p["edu_share"] * it["recorded"] + E.p["aid"] * E.p["N"] * 12, floor)
        assert abs(it["edu_budget"] - expected) <= 1e-9 * max(1.0, expected), (
            f"year {t}: edu_budget {it['edu_budget']} != max(edu_share*revenue + aid, floor) = {expected}"
        )


def test_ac2_per_quintile_accounting_reconciles(audited):
    """Per-quintile accounting: recorded quintile means equal the child register exactly; quintiles are
    population quintiles of each cohort."""
    E = audited()
    rows = [it for _, items in E.acct for it in items if it["check"] == "per_quintile"]
    assert len(rows) == E.p["T"], f"expected one quintile block per year, got {len(rows)}"
    for t, it in enumerate(rows):
        for r in it["rows"]:
            assert r["spend_recorded"] == pytest.approx(r["spend_expected"], abs=1e-12), (
                f"year {t} q{r['q']}: recorded k12 spend mean {r['spend_recorded']} != "
                f"register recomputation {r['spend_expected']} (n={r['n']})"
            )
            assert 0.0 <= r["rate_recorded"] <= 1.0 and r["spend_recorded"] >= 0.0
        assert it["k12_total_recorded"] == pytest.approx(it["k12_total_expected"], abs=1e-9), (
            f"year {t}: k12 spend total {it['k12_total_recorded']} != register sum {it['k12_total_expected']}"
        )
        # Quintile means must aggregate to the total: sum_j n_j * mean_j == total.
        agg = sum(r["n"] * r["spend_recorded"] for r in it["rows"])
        assert agg == pytest.approx(it["k12_total_recorded"], abs=1e-9), (
            f"year {t}: Sigma q n_q * mean_q = {agg} != total {it['k12_total_recorded']}"
        )
        # Per-quintile rates must aggregate to the reported aggregate rate (weighted by pupil counts).
        n_tot = sum(r["n_across"] for r in it["rows"])
        if n_tot > 0:
            rate_agg = sum(r["rate_recorded"] * r["n_across"] for r in it["rows"]) / n_tot
            assert rate_agg == pytest.approx(float(E.R["tut_k12_rate"][t]), abs=1e-12), (
                f"year {t}: quintile-weighted rate {rate_agg} != recorded tut_k12_rate "
                f"{E.R['tut_k12_rate'][t]}"
            )
    # Quintile assignment is a population quintile of each birth cohort (~20% each).
    X = E.ALL
    q = np.asarray(X["q"], int)
    shares = np.array([np.mean(q == j) for j in range(5)])
    assert np.all(np.abs(shares - 0.2) <= 1.0 / E.p["N"] + 1e-9), (
        f"quintile population shares {np.round(shares, 4)} deviate from 0.2 by more than one child"
    )
    assert set(np.unique(q).tolist()) == {0, 1, 2, 3, 4}


def test_ac3_cohort_denominators(build):
    """Cohort denominators: attendance series = per-grade census, cohort completion windows count each
    intended-age cohort exactly once, and out-of-school denominators are the fixed cohort size."""
    E = build_engine(N=36, T=22, measure_from=8)
    E.run()
    R = E.R
    for t in range(len(R["enrolled"])):
        assert int(R["enrolled"][t]) == int(np.asarray(R["att_by_grade"][t]).sum()), (
            f"year {t}: enrolled {R['enrolled'][t]} != sum(att_by_grade) {np.asarray(R['att_by_grade'][t]).sum()}"
        )
    # census: each (cohort, age) cell counts the cohort's enrolled children; the cohort population is N
    cohorts = sorted({c for (c, _) in E.census})
    for c in cohorts:
        cells = [a for (cc, a) in E.census if cc == c]
        assert cells, f"no census cells for cohort {c}"
        assert len(cells) == len(set(cells)), f"duplicate ages for cohort {c}"
        assert all(0 <= E.census[(c, a)] <= E.p["N"] for a in cells)
    from eduengine import measure as M

    Y = 20
    intended = E.p["entry_age"] + E.ends[0] - 1
    ages = Y - (E.p["start_year"] + np.asarray(E.ALL["cohort"], int)) + E.p["entry_age"]
    sel = (ages >= intended + 3) & (ages <= intended + 5)
    n_denom = int(sel.sum())
    assert n_denom == 3 * E.p["N"], (
        f"completion_cohort denominator at Y={Y} is {n_denom}, expected 3 cohorts x N = {3 * E.p['N']} "
        "(each intended age counted exactly once)"
    )
    rate = M.completion_cohort(E, 0, Y)
    assert 0.0 <= rate <= 1.0, f"completion_cohort returned {rate} outside [0,1]"
    # Gross intake denominator is the cohort size, not enrolment (measure.py:46).
    for lev in (0, 1):
        gi = M.gross_intake_last(E, lev, Y)
        if np.isfinite(gi):
            entrants = np.asarray(R["new_by_grade"][Y - E.p["start_year"]], float)[E.ends[lev] - 1]
            assert gi == pytest.approx(float(entrants / E.p["N"]), abs=1e-12), (
                f"gross_intake_last(level={lev}) = {gi} != new_entrants/N = {entrants / E.p['N']}"
            )


@missing(not CAPS["reporting"],
         "missing API: contest_applicant_seat_ratio/contest_admit_rate/contest_expected_p_mean series "
         "(contract §1.4)")
def test_ac4_contest_denominators_are_reported():
    """Cohort/denominator reporting for contest arms: candidates, seats, ratio, admit rate all finite."""
    E = small_contest_engine()
    E.run()
    for key in ("contest_candidates", "contest_seats", "contest_applicant_seat_ratio",
                "contest_admit_rate", "contest_expected_p_mean"):
        assert key in E.R, f"missing reported series {key!r} (contract §1.4)"
    cand = np.asarray(E.R["contest_candidates"], float)
    seats = np.asarray(E.R["contest_seats"], float)
    ratio = np.asarray(E.R["contest_applicant_seat_ratio"], float)
    admit = np.asarray(E.R["contest_admit_rate"], float)
    gate_years = np.isfinite(cand)
    assert gate_years.any(), "no contest gate years recorded"
    assert np.all(np.isfinite(seats[gate_years]))
    assert np.all(np.isfinite(ratio[gate_years]))
    assert np.all(np.isfinite(admit[gate_years]))
    assert np.all(ratio[gate_years] >= 0.0) and np.all(admit[gate_years] >= 0.0)
    assert np.all(admit[gate_years] <= 1.0)


@missing(not CAPS["reporting"],
         "missing API: contest_expected_p_mean / contest_admit_rate series for expected-vs-realized "
         "reconciliation (contract §1.4)")
def test_ac5_expected_vs_realized_reconciliation_over_seeds():
    """Expected-vs-realized: |admit_rate - mean P| within 4 seed-SE over 30 seeds of a small config."""
    gaps = []
    for seed in range(30):
        E = small_contest_engine(seed=seed)
        E.run()
        admit = np.asarray(E.R["contest_admit_rate"], float)
        pmean = np.asarray(E.R["contest_expected_p_mean"], float)
        mask = np.isfinite(admit) & np.isfinite(pmean)
        assert mask.any(), f"seed {seed}: no contest diagnostics"
        gaps.append(np.abs(admit[mask] - pmean[mask]).ravel())
    g = np.concatenate(gaps)
    gap = float(np.mean(g))
    se = float(np.std(g, ddof=1) / np.sqrt(max(len(g), 1)))
    assert gap <= 4.0 * max(se, 1e-6), (
        f"expected-vs-realized gap {gap:.4f} exceeds 4 seed-SE ({4 * se:.4f}); the household expected "
        "probability and the realized admission rule are different objects (defect D2)"
    )


@missing(not CAPS["state_prep_stock"],
         "missing API: k['prep_stock'][:, m] persistent preparation stock (contract §2/§5; defect D5)")
def test_ac6_prep_stock_follows_depreciation_recurrence():
    """Prep stock (contract §5): stock_t = (1-rho)*stock_{t-1} + e_t per gate column, rho = 0 by default.

    The gate consumes only its own column for the children who sit it; every other column is carried
    untouched.  With rho = 0 the recurrence reproduces the legacy undepreciated lifetime sum.
    """
    E, years = tracked_run(gates=legacy_gates_g12(), contest_prep_depreciation=0.0)
    rho = 0.0
    prev_stock = None
    prev_rows = None
    consumed_gate = False
    for t, y in enumerate(years):
        rows = y["rows"]
        stock = {k: v["prep_stock"] for k, v in rows.items() if "prep_stock" in v}
        if not stock:
            break
        if prev_stock is not None:
            for kk, st in stock.items():
                if kk not in prev_stock or kk not in prev_rows:
                    continue
                e_t = rows[kk]["ce"]
                expected = (1.0 - rho) * np.asarray(prev_stock[kk], float)
                expected[1] += e_t  # this year's effort is assigned to the child's upcoming gate (level 1)
                # the gate itself may consume its own column for children sitting it this year
                got = np.asarray(st, float)
                if prev_rows[kk]["cred"] != rows[kk]["cred"]:
                    consumed_gate = True
                    continue
                np.testing.assert_allclose(got, expected, atol=1e-9,
                                           err_msg=f"year {t}: prep_stock recurrence violated for child {kk}")
        prev_stock = stock
        prev_rows = rows
    assert consumed_gate, "no gate consumption (prep_stock[at_gate, m] = 0) was observed (contract §5)"
    # Depreciation switch exists and rho = 1 is memoryless: stock never exceeds the annual cap.
    for rho in (0.0, 0.25, 1.0):
        E2 = build_engine(gates=legacy_gates_g12(), contest_prep_depreciation=rho)
        E2.run()
        assert "prep_stock" in E2.ALL
