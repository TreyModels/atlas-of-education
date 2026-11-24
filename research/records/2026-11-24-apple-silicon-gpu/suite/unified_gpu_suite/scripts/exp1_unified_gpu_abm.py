"""EXP-1: Complete CuPy/CUDA GPU ABM unifying Nordtveit (child labor continuum + school push),
Bray/Jayachandran (shadow tutoring + teacher diversion + crowding), Pritchett (flat learning profile),
and Basu-Van/Baland-Robinson (subsistence + credit constraint).
Includes Philox4x32-10 RNG, pinned batch size, and Q1 zero-signal control (strength=0).
"""
import argparse, json, os, time
import numpy as np
import cupy as cp

KERNEL_SRC = r'''
extern "C" {
__device__ __forceinline__ void mulhilo32(unsigned a, unsigned b, unsigned &hi, unsigned &lo) {
    unsigned long long p = (unsigned long long)a * (unsigned long long)b;
    lo = (unsigned)p; hi = (unsigned)(p >> 32);
}

__device__ __forceinline__ void philox(unsigned c0i, unsigned c1i, unsigned c2i, unsigned c3i,
                                       unsigned seed0, unsigned seed1, unsigned o[4]) {
    const unsigned M0 = 0xD2511F53u, M1 = 0xCD9E8D57u;
    const unsigned W0 = 0x9E3779B9u, W1 = 0xBB67AE85u;
    unsigned c0 = c0i, c1 = c1i, c2 = c2i, c3 = c3i, k0 = seed0, k1 = seed1;
    #pragma unroll
    for (int i = 0; i < 10; i++) {
        unsigned hi0, lo0, hi1, lo1;
        mulhilo32(M0, c0, hi0, lo0);
        mulhilo32(M1, c2, hi1, lo1);
        unsigned n0 = hi1 ^ c1 ^ k0, n2 = hi0 ^ c3 ^ k1;
        c0 = n0; c1 = lo1; c2 = n2; c3 = lo0;
        if (i < 9) { k0 += W0; k1 += W1; }
    }
    o[0] = c0; o[1] = c1; o[2] = c2; o[3] = c3;
}

__device__ __forceinline__ float uni_from(unsigned x) {
    return ((float)x + 0.5f) * (1.0f / 4294967296.0f);
}

// States: 0=school_only, 1=study_and_work, 2=visible_work_only, 3=hidden_work
__global__ void sim_step(
    int N, int year, unsigned seed0, unsigned seed1,
    float f_pub, float h_hidden, float psi_hostility, float ban_sw,
    float q_pub, float diversion_beta, float w_child, float y_sub, float shadow_cost,
    float w_pov, float w_push, float w_tutor,
    const float* __restrict__ base_y,
    const float* __restrict__ ability,
    int* __restrict__ state_out,
    int* __restrict__ tutor_out,
    float* __restrict__ learn_out,
    float* __restrict__ work_hrs_out,
    float* __restrict__ y_hh_out
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= N) return;

    unsigned raw[4];
    philox((unsigned)i, (unsigned)year, 0u, 1u, seed0, seed1, raw);
    float u_shock = uni_from(raw[0]);
    float u_eps0  = (uni_from(raw[1]) - 0.5f) * 0.45f;
    float u_eps1  = (uni_from(raw[2]) - 0.5f) * 0.45f;
    float u_eps2  = (uni_from(raw[3]) - 0.5f) * 0.45f;

    // Adult health/income shock (Nordtveit HIV/poverty vulnerability)
    float adult_shock = (u_shock < 0.08f) ? 0.55f : 1.0f;
    float y_hh = base_y[i] * adult_shock;
    float surv_gap = fmaxf(0.0f, y_sub - y_hh);

    float tot_cost = f_pub + h_hidden;
    float ab = ability[i];
    // Effective public quality net of Jayachandran/Biswal teacher diversion
    float q_eff = fmaxf(0.10f, q_pub * (1.0f - diversion_beta));

    float u0 = w_tutor * q_eff * ab - tot_cost - w_push * psi_hostility - w_pov * surv_gap + u_eps0;
    float u1 = w_tutor * 0.72f * q_eff * ab - tot_cost + 0.55f * w_child - 0.45f * w_push * psi_hostility
               - 0.30f * w_pov * surv_gap - ban_sw + u_eps1;
    float u2 = w_child + 0.45f * w_pov * surv_gap - 0.30f * ban_sw + u_eps2;
    float u3 = 0.85f * w_child + 0.70f * w_pov * surv_gap + (ban_sw > 0.0f ? 0.40f : -0.45f);

    int best = 0;
    float best_u = u0;
    if (u1 > best_u) { best = 1; best_u = u1; }
    if (u2 > best_u) { best = 2; best_u = u2; }
    if (u3 > best_u) { best = 3; best_u = u3; }

    // Shadow tutoring (Bray crowding + Jayachandran withholding recovery)
    int takes_tutor = 0;
    if ((best == 0 || best == 1) && (y_hh - tot_cost > shadow_cost)) {
        float net_tutor = w_tutor * (1.0f - q_eff) * ab + 0.5f * diversion_beta - shadow_cost;
        if (net_tutor > 0.05f) takes_tutor = 1;
    }

    // Continuous work hours (for micro tie-breaker distribution)
    float work_hrs = 0.0f;
    if (best == 1) work_hrs = 10.0f + 12.0f * fminf(1.0f, surv_gap + 0.2f * uni_from(raw[1]));
    if (best == 2) work_hrs = 28.0f + 10.0f * uni_from(raw[2]);
    if (best == 3) work_hrs = 36.0f + 12.0f * uni_from(raw[3]);

    float learn = (best == 0 ? q_eff : (best == 1 ? 0.70f * q_eff : 0.05f)) * ab + (takes_tutor ? 0.28f : 0.0f);

    state_out[i] = best;
    tutor_out[i] = takes_tutor;
    learn_out[i] = learn;
    work_hrs_out[i] = work_hrs;
    y_hh_out[i] = y_hh;
}
}
'''

DGPS = {
    "DGP_ZERO_SIGNAL":    dict(w_pov=0.0, w_push=0.0, w_tutor=0.0, div=0.00),
    "DGP_POVERTY":        dict(w_pov=2.2, w_push=0.1, w_tutor=0.8, div=0.02),
    "DGP_SCHOOL_PUSH":    dict(w_pov=0.2, w_push=2.0, w_tutor=0.8, div=0.05),
    "DGP_CROWDING_TUTOR": dict(w_pov=0.3, w_push=0.3, w_tutor=2.2, div=0.22),
    "DGP_MIXED":          dict(w_pov=1.4, w_push=1.3, w_tutor=1.6, div=0.12),
}

ARMS = {
    "tuition_only":        dict(f_post=0.0, h_post=0.35, psi_post=0.45, ban_post=0.0, cap_scale=0.30),
    "protective_capacity": dict(f_post=0.0, h_post=0.00, psi_post=0.05, ban_post=0.0, cap_scale=1.00),
    "binary_ban":          dict(f_post=0.0, h_post=0.35, psi_post=0.45, ban_post=1.8, cap_scale=0.30),
}

def run_country_arm(kern, N, T, seed, dgp, arm):
    rng = cp.random.default_rng(seed)
    base_y = cp.exp(rng.normal(0.0, 0.55, size=N, dtype=cp.float32))
    ability = cp.clip(rng.normal(1.0, 0.20, size=N, dtype=cp.float32), 0.3, 1.8)

    state_out = cp.empty(N, dtype=cp.int32)
    tutor_out = cp.empty(N, dtype=cp.int32)
    learn_out = cp.empty(N, dtype=cp.float32)
    work_out  = cp.empty(N, dtype=cp.float32)
    y_hh_out  = cp.empty(N, dtype=cp.float32)

    p = DGPS[dgp]
    a = ARMS[arm]
    threads = 256
    blocks = (N + threads - 1) // threads

    q_pub = 0.65
    rows = []
    for t in range(T):
        post = t >= 10
        f_pub = a["f_post"] if post else 0.45
        h_hid = a["h_post"] if post else 0.35
        psi   = a["psi_post"] if post else 0.45
        ban   = a["ban_post"] if post else 0.0
        y_sub = 0.90 * (0.985 ** t)

        kern((blocks,), (threads,), (
            np.int32(N), np.int32(t), np.uint32(seed), np.uint32(t + 17),
            np.float32(f_pub), np.float32(h_hid), np.float32(psi), np.float32(ban),
            np.float32(q_pub), np.float32(p["div"]), np.float32(0.55), np.float32(y_sub), np.float32(0.32),
            np.float32(p["w_pov"]), np.float32(p["w_push"]), np.float32(p["w_tutor"]),
            base_y, ability, state_out, tutor_out, learn_out, work_out, y_hh_out
        ))
        cp.cuda.Stream.null.synchronize()

        s = cp.asnumpy(state_out)
        tut = cp.asnumpy(tutor_out)
        wrk = cp.asnumpy(work_out)
        lrn = cp.asnumpy(learn_out)
        yhh = cp.asnumpy(y_hh_out)

        enr_mask = s <= 1
        enr = float(np.mean(enr_mask))
        sw  = float(np.mean(s == 1))
        wo  = float(np.mean(s == 2))
        hw  = float(np.mean(s == 3))
        tut_rate = float(np.mean(tut))
        hrs_p90 = float(np.percentile(wrk[enr_mask], 90)) if np.any(enr_mask) else 0.0
        # Income gradient of tutoring among enrolled
        if np.any(enr_mask) and np.std(tut[enr_mask]) > 1e-6:
            tut_y_corr = float(np.corrcoef(np.log(yhh[enr_mask] + 1e-4), tut[enr_mask])[0, 1])
        else:
            tut_y_corr = 0.0

        q_pub = float(np.clip(0.65 - (1.0 - a["cap_scale"]) * max(0.0, enr - 0.55) * 0.45, 0.30, 0.80))
        rows.append({
            "dgp": dgp, "arm": arm, "seed": seed, "t": t, "batch_N": N,
            "ger": enr, "study_work": sw, "work_only": wo, "hidden_work": hw,
            "cl_total": sw + wo + hw, "tutoring": tut_rate,
            "enrolled_work_hrs_p90": hrs_p90,
            "hidden_to_sw_ratio": hw / max(sw, 1e-4),
            "tutor_income_corr": tut_y_corr,
            "mean_learn": float(np.mean(lrn)), "q_pub": q_pub,
        })
    return rows

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--out", default="results/exp1_abm.json")
    args = ap.parse_args()

    N = 10_000 if args.smoke else 250_000
    T = 15 if args.smoke else 25
    n_seeds = 2 if args.smoke else args.seeds

    mod = cp.RawModule(code=KERNEL_SRC)
    kern = mod.get_function("sim_step")

    t0 = time.time()
    all_rows = []
    for s_idx in range(n_seeds):
        seed = 20261125 + s_idx * 100
        for dgp in DGPS:
            for arm in ARMS:
                all_rows.extend(run_country_arm(kern, N, T, seed, dgp, arm))

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(all_rows, f)
    print(f"EXP-1 complete in {time.time() - t0:.2f}s | rows={len(all_rows)} | batch_N={N}")
