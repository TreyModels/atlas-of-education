"""Line-by-line transcription of the suite's CUDA `sim_step` kernel to NumPy and MLX.

The CUDA C source (KERNEL_SRC in exp1_unified_gpu_abm.py) is the specification. Everything below mirrors it:
Philox4x32-10 with counter (i, year, 0, 1) and key (seed0, seed1); uniforms (raw+0.5)/2^32; the four
utility comparisons with strict-greater tie-breaking; the 4-state child-labour continuum; tutoring; work
hours; learning; output arrays. The kernel RNG is computed once in NumPy and the identical uniform bits are
fed to both backends, so a NumPy-vs-MLX comparison isolates backend arithmetic, not RNG.

The transcription is NOT verified against a CUDA GPU (unavailable on Apple Silicon) — it is verified against
a scalar reference transcription and against itself across backends. See PRE_REGISTRATION.md §3-4.
"""
import numpy as np

M0 = np.uint32(0xD2511F53)
M1 = np.uint32(0xCD9E8D57)
W0 = np.uint32(0x9E3779B9)
W1 = np.uint32(0xBB67AE85)
TWO32 = np.float32(1.0 / 4294967296.0)
HALF = np.float32(0.5)


def _mulhilo32(a, b):
    """32x32 -> (hi, lo) 32-bit halves of the 64-bit product; matches CUDA mulhilo32."""
    a = np.asarray(a, dtype=np.uint32)
    b = np.asarray(b, dtype=np.uint32)
    p = a.astype(np.uint64) * b.astype(np.uint64)
    lo = (p & np.uint64(0xFFFFFFFF)).astype(np.uint32)
    hi = (p >> np.uint64(32)).astype(np.uint32)
    return hi, lo


def _philox_array(c0, c1, c2, c3, seed0, seed1):
    """Vectorised Philox4x32-10. c0..c3/seed* are uint32 arrays or scalars."""
    c0 = np.asarray(c0, dtype=np.uint32)
    c1 = np.asarray(c1, dtype=np.uint32)
    c2 = np.asarray(c2, dtype=np.uint32)
    c3 = np.asarray(c3, dtype=np.uint32)
    k0 = np.asarray(seed0, dtype=np.uint32)
    k1 = np.asarray(seed1, dtype=np.uint32)
    with np.errstate(over="ignore"):
        for i in range(10):
            hi0, lo0 = _mulhilo32(M0, c0)
            hi1, lo1 = _mulhilo32(M1, c2)
            n0 = hi1 ^ c1 ^ k0
            n2 = hi0 ^ c3 ^ k1
            c0, c1, c2, c3 = n0, lo1, n2, lo0
            if i < 9:
                k0 = k0 + W0
                k1 = k1 + W1
    return c0, c1, c2, c3


def _scalar_philox(c0i, c1i, c2i, c3i, seed0, seed1):
    """Scalar reference transcription used only by the test suite (independent of the vectorised path)."""
    mask = 0xFFFFFFFF
    c0, c1, c2, c3 = c0i & mask, c1i & mask, c2i & mask, c3i & mask
    k0, k1 = seed0 & mask, seed1 & mask
    for i in range(10):
        p0 = (0xD2511F53 * c0) & 0xFFFFFFFFFFFFFFFF
        p1 = (0xCD9E8D57 * c2) & 0xFFFFFFFFFFFFFFFF
        hi0, lo0 = (p0 >> 32) & mask, p0 & mask
        hi1, lo1 = (p1 >> 32) & mask, p1 & mask
        n0 = (hi1 ^ c1 ^ k0) & mask
        n2 = (hi0 ^ c3 ^ k1) & mask
        c0, c1, c2, c3 = n0, lo1, n2, lo0
        if i < 9:
            k0 = (k0 + 0x9E3779B9) & mask
            k1 = (k1 + 0xBB67AE85) & mask
    return c0, c1, c2, c3


def philox_uniforms(n, year, seed0, seed1):
    """Return (n,4) float32 uniforms exactly as the CUDA kernel's philox(...)+uni_from for each household."""
    idx = np.arange(int(n), dtype=np.uint32)
    year_u = np.full(int(n), np.uint32(year), dtype=np.uint32)
    zero = np.zeros(int(n), dtype=np.uint32)
    one = np.ones(int(n), dtype=np.uint32)
    r = _philox_array(idx, year_u, zero, one, np.uint32(seed0), np.uint32(seed1))
    u = np.empty((int(n), 4), dtype=np.float32)
    for j in range(4):
        u[:, j] = (r[j].astype(np.float32) + HALF) * TWO32
    return u


def _scalars(args):
    N = int(np.asarray(args[0]).item())
    year = int(np.asarray(args[1]).item())
    seed0 = int(np.asarray(args[2]).item()) & 0xFFFFFFFF
    seed1 = int(np.asarray(args[3]).item()) & 0xFFFFFFFF
    vals = [np.float32(np.asarray(a).item()) for a in args[4:16]]
    return N, year, seed0, seed1, vals


def _prepare(args):
    import gpu_compat as gc
    N, year, seed0, seed1, vals = _scalars(args)
    (f_pub, h_hidden, psi_hostility, ban_sw, q_pub, diversion_beta, w_child,
     y_sub, shadow_cost, w_pov, w_push, w_tutor) = vals
    base_y = gc.asnumpy(args[16]).astype(np.float32, copy=False).reshape(-1)
    ability = gc.asnumpy(args[17]).astype(np.float32, copy=False).reshape(-1)
    assert base_y.size == N and ability.size == N
    u = philox_uniforms(N, year, seed0, seed1)
    return dict(N=N, year=year, seed0=seed0, seed1=seed1, f_pub=f_pub, h_hidden=h_hidden,
                psi_hostility=psi_hostility, ban_sw=ban_sw, q_pub=q_pub, diversion_beta=diversion_beta,
                w_child=w_child, y_sub=y_sub, shadow_cost=shadow_cost, w_pov=w_pov, w_push=w_push,
                w_tutor=w_tutor, base_y=base_y, ability=ability, uniforms=u)


def _compute_numpy(P):
    u = P["uniforms"]
    ur = [u[:, j] for j in range(4)]
    u_shock = ur[0]
    eps = [np.float32((ur[j] - HALF) * np.float32(0.45)) for j in (1, 2, 3)]
    adult_shock = np.where(u_shock < np.float32(0.08), np.float32(0.55), np.float32(1.0)).astype(np.float32)
    y_hh = (P["base_y"] * adult_shock).astype(np.float32)
    surv_gap = np.maximum(np.float32(0.0), np.float32(P["y_sub"]) - y_hh).astype(np.float32)
    tot_cost = np.float32(P["f_pub"] + P["h_hidden"])
    ab = P["ability"]
    q_eff = np.maximum(np.float32(0.10),
                       np.float32(P["q_pub"] * (1.0 - P["diversion_beta"]))).astype(np.float32)
    w_tutor, w_push, w_pov, w_child = (np.float32(P["w_tutor"]), np.float32(P["w_push"]),
                                       np.float32(P["w_pov"]), np.float32(P["w_child"]))
    ban = np.float32(P["ban_sw"])
    u0 = (w_tutor * q_eff * ab - tot_cost - w_push * np.float32(P["psi_hostility"]) - w_pov * surv_gap
          + eps[0]).astype(np.float32)
    u1 = (w_tutor * np.float32(0.72) * q_eff * ab - tot_cost + np.float32(0.55) * w_child
          - np.float32(0.45) * w_push * np.float32(P["psi_hostility"]) - np.float32(0.30) * w_pov * surv_gap
          - ban + eps[1]).astype(np.float32)
    u2 = (w_child + np.float32(0.45) * w_pov * surv_gap - np.float32(0.30) * ban + eps[2]).astype(np.float32)
    u3 = (np.float32(0.85) * w_child + np.float32(0.70) * w_pov * surv_gap
          + np.where(ban > np.float32(0.0), np.float32(0.40), np.float32(-0.45))).astype(np.float32)
    best = np.zeros(P["N"], dtype=np.int32)
    best_u = u0
    for j, uu in ((1, u1), (2, u2), (3, u3)):
        mask = uu > best_u
        best = np.where(mask, np.int32(j), best).astype(np.int32)
        best_u = np.where(mask, uu, best_u).astype(np.float32)
    shadow_cost = np.float32(P["shadow_cost"])
    net_tutor = (w_tutor * (np.float32(1.0) - q_eff) * ab + np.float32(0.5) * np.float32(P["diversion_beta"])
                 - shadow_cost).astype(np.float32)
    tutor = (((best == 0) | (best == 1)) & ((y_hh - tot_cost) > shadow_cost)
             & (net_tutor > np.float32(0.05))).astype(np.int32)
    work = np.zeros(P["N"], dtype=np.float32)
    m1 = best == 1
    work[m1] = (np.float32(10.0) + np.float32(12.0) * np.minimum(
        np.float32(1.0), surv_gap[m1] + np.float32(0.2) * ur[1][m1])).astype(np.float32)
    m2 = best == 2
    work[m2] = (np.float32(28.0) + np.float32(10.0) * ur[2][m2]).astype(np.float32)
    m3 = best == 3
    work[m3] = (np.float32(36.0) + np.float32(12.0) * ur[3][m3]).astype(np.float32)
    learn = (np.where(best == 0, q_eff, np.where(best == 1, np.float32(0.70) * q_eff,
                                                 np.float32(0.05))) * ab
             + np.where(tutor == 1, np.float32(0.28), np.float32(0.0))).astype(np.float32)
    return dict(state=best, tutor=tutor, learn=learn, work=work, y_hh=y_hh)


def _compute_mlx(P):
    import mlx.core as mx
    u = mx.array(P["uniforms"])
    ur = [u[:, j] for j in range(4)]
    f32 = lambda v: mx.array(np.float32(v))
    u_shock = ur[0]
    eps = [(ur[j] - f32(0.5)) * f32(0.45) for j in (1, 2, 3)]
    adult_shock = mx.where(u_shock < f32(0.08), f32(0.55), f32(1.0))
    base_y = mx.array(P["base_y"]); ability = mx.array(P["ability"])
    y_hh = base_y * adult_shock
    surv_gap = mx.maximum(f32(0.0), f32(P["y_sub"]) - y_hh)
    tot_cost = f32(P["f_pub"] + P["h_hidden"])
    q_eff = mx.maximum(f32(0.10), f32(P["q_pub"] * (1.0 - P["diversion_beta"])))
    w_tutor, w_push, w_pov, w_child = f32(P["w_tutor"]), f32(P["w_push"]), f32(P["w_pov"]), f32(P["w_child"])
    ban = f32(P["ban_sw"])
    u0 = w_tutor * q_eff * ability - tot_cost - w_push * f32(P["psi_hostility"]) - w_pov * surv_gap + eps[0]
    u1 = (w_tutor * f32(0.72) * q_eff * ability - tot_cost + f32(0.55) * w_child
          - f32(0.45) * w_push * f32(P["psi_hostility"]) - f32(0.30) * w_pov * surv_gap - ban + eps[1])
    u2 = w_child + f32(0.45) * w_pov * surv_gap - f32(0.30) * ban + eps[2]
    u3 = f32(0.85) * w_child + f32(0.70) * w_pov * surv_gap + mx.where(ban > f32(0.0), f32(0.40), f32(-0.45))
    best = mx.zeros((P["N"],), dtype=mx.int32)
    best_u = u0
    for j, uu in ((1, u1), (2, u2), (3, u3)):
        mask = uu > best_u
        best = mx.where(mask, mx.full((P["N"],), j, dtype=mx.int32), best)
        best_u = mx.where(mask, uu, best_u)
    shadow_cost = f32(P["shadow_cost"])
    net_tutor = w_tutor * (f32(1.0) - q_eff) * ability + f32(0.5) * f32(P["diversion_beta"]) - shadow_cost
    tutor = (((best == 0) | (best == 1)) & ((y_hh - tot_cost) > shadow_cost) & (net_tutor > f32(0.05)))
    tutor = tutor.astype(mx.int32)
    work = mx.zeros((P["N"],), dtype=mx.float32)
    work = mx.where(best == 1, f32(10.0) + f32(12.0) * mx.minimum(f32(1.0), surv_gap + f32(0.2) * ur[1]), work)
    work = mx.where(best == 2, f32(28.0) + f32(10.0) * ur[2], work)
    work = mx.where(best == 3, f32(36.0) + f32(12.0) * ur[3], work)
    learn = (mx.where(best == 0, q_eff, mx.where(best == 1, f32(0.70) * q_eff, f32(0.05))) * ability
             + mx.where(tutor == 1, f32(0.28), f32(0.0)))
    mx.eval(best, tutor, learn, work, y_hh)
    return dict(state=best, tutor=tutor, learn=learn, work=work, y_hh=y_hh)


def run_sim_step_arrays(backend, args):
    """Run the transcribed kernel and return backend arrays (for tests)."""
    P = _prepare(args)
    if backend == "mlx":
        return _compute_mlx(P)
    return _compute_numpy(P)


def run_sim_step(backend, args):
    """RawModule.get_function('sim_step') entry point: fills the caller's output wrappers in place."""
    import gpu_compat as gc
    out = run_sim_step_arrays(backend, args)
    names = ("state", "tutor", "learn", "work", "y_hh")
    wraps = (args[18], args[19], args[20], args[21], args[22])
    for name, wrap in zip(names, wraps):
        wrap.data = out[name]
        wrap.backend = backend
    return None
