// GPU port of the individual-level schooling-dose fertility model (research/records/2026-11-23-dose-gpu).
// Same statistical model as research/records/2026-11-23-dose-model/scripts/model.py. Two structural changes,
// both required by the GPU:
//   * the unit of parallelism is a woman; many parameter sets x countries x country-effects are batched
//     into one launch along a "run" axis (r = run index);
//   * the marriage market, serial in the original (a random permutation of the 60 women of a
//     cohort x urban cell, visited one at a time), becomes a deterministic priority claim: each woman
//     draws a 32-bit priority, claims one man, and the highest-priority claimant wins (atomicMax; ties
//     broken by the woman's index in the cell, so it is reproducible).  test_port.py checks
//     distributionally against the original CPU model that this changes nothing that matters.
// RNG is counter-based (Philox4x32-10): stream = (woman index, run*512 + purpose), purpose 0 = init,
// purpose 1+(t-1900) = calendar year t.  Execution order therefore cannot change any draw, which is what
// makes the numpy reference (ref_numpy.py) able to consume exactly the same numbers.

#define NG 126          // gdp array length, 1925..2050
#define NPR 25          // scalars per run in the parameter block
#define PWLEV 7         // women: 6 cut points + trailing 1.0
#define PMLEV 7         // men: 7 cumulative values

// ---------------------------------------------------------------- bit-exact exp/log (mirrors dosecore.py)
__device__ __forceinline__ double sy_exp(double x) {
    const double LN2HI = 6.93147180369123816490e-01;
    const double LN2LO = 1.90821492927058770002e-10;
    const double INVLN2 = 1.44269504088896338700e+00;
    double k = floor(x * INVLN2 + 0.5);
    double r = (x - k * LN2HI) - k * LN2LO;
    double p = 1.0 / 6227020800.0;
    p = p * r + 1.0 / 479001600.0;
    p = p * r + 1.0 / 39916800.0;
    p = p * r + 1.0 / 3628800.0;
    p = p * r + 1.0 / 362880.0;
    p = p * r + 1.0 / 40320.0;
    p = p * r + 1.0 / 5040.0;
    p = p * r + 1.0 / 720.0;
    p = p * r + 1.0 / 120.0;
    p = p * r + 1.0 / 24.0;
    p = p * r + 1.0 / 6.0;
    p = p * r + 0.5;
    p = p * r + 1.0;
    p = p * r + 1.0;
    return ldexp(p, (int)k);
}
__device__ __forceinline__ double sy_log(double x) {
    const double LN2HI = 6.93147180369123816490e-01;
    const double LN2LO = 1.90821492927058770002e-10;
    int e; double m = frexp(x, &e);
    if (m < 0.7071067811865476) { m = m * 2.0; e -= 1; }
    double t = (m - 1.0) / (m + 1.0);
    double t2 = t * t;
    double p = 1.0 / 13.0;
    p = p * t2 + 1.0 / 11.0;
    p = p * t2 + 1.0 / 9.0;
    p = p * t2 + 1.0 / 7.0;
    p = p * t2 + 1.0 / 5.0;
    p = p * t2 + 1.0 / 3.0;
    double logm = 2.0 * t * (1.0 + t2 * p);
    return ((double)e * LN2HI + (double)e * LN2LO) + logm;
}
__device__ __forceinline__ double logit_noise(double u) { return 0.5 * sy_log(u / (1.0 - u)); }

// ---------------------------------------------------------------- Philox4x32-10
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
__device__ __forceinline__ double uni_from(unsigned x) { return ((double)x + 0.5) * (1.0 / 4294967296.0); }

// uniform slot table -- MUST match ref_numpy.py.  Laid out to mirror the ORIGINAL model's draw order:
//  0 birth | 1 separation | 2 arranged trigger | 3..10 the 8 arranged-marriage man draws
//  11 priority | 12..12+3Kc-1 the market's up-to-3Kc man draws
//  12+3Kc .. 12+4Kc-1 woman logit noises for the Kc available-and-eligible men
//  12+4Kc man acceptance noise
// The original draws the arranged man up to 8 times until one is eligible, and samples up to 3*Kc men
// to get Kc eligible ones; both loops are reproduced here, which is what removes the marriage-age bias.
__device__ __forceinline__ void draw_uniforms(unsigned long long wid, unsigned aux,
                                             unsigned seed0, unsigned seed1, int nb,
                                             double *u, unsigned *raw) {
    unsigned w0 = (unsigned)wid, w1 = (unsigned)(wid >> 32);
    for (int b = 0; b < nb; b++) {
        unsigned o[4];
        philox(w0, w1, aux, (unsigned)b, seed0, seed1, o);
        for (int j = 0; j < 4; j++) { raw[4 * b + j] = o[j]; u[4 * b + j] = uni_from(o[j]); }
    }
}

// ---------------------------------------------------------------- indexing
#define PW_(r, cell, q, l) (PWc[(unsigned long long)(r) * (28 * 5 * PWLEV) + (unsigned long long)(cell) * (5 * PWLEV) + (unsigned long long)(q) * PWLEV + (l)])
#define PM_(r, cell, l)    (PMc[(unsigned long long)(r) * (28 * PMLEV) + (unsigned long long)(cell) * PMLEV + (l)])
#define WC_(r, cell, q)    (wcell[(unsigned long long)(r) * (28 * 5) + (unsigned long long)(cell) * 5 + (q)])
#define PD_(r, i)          (Pd[(unsigned long long)(r) * NPR + (i)])
#define DOS_(r, l)         (dosen[(unsigned long long)(r) * 7 + (l)])
#define ZC_(r, c)          (Zc[(unsigned long long)(r) * 14 + (c)])
#define GDP_(r, y)         (gdp[(unsigned long long)(r) * NG + (y)])
#define BB_(r, ti, ai)     (births[(unsigned long long)(r) * (101 * 35) + (unsigned long long)(ti) * 35 + (ai)])
#define EX_(r, ti, ai)     (expo[(unsigned long long)(r) * (101 * 35) + (unsigned long long)(ti) * 35 + (ai)])
#define SG_(r, ti, ai)     (sing[(unsigned long long)(r) * (101 * 35) + (unsigned long long)(ti) * 35 + (ai)])
#define AFBS_(r, ti)       (afb_s[(unsigned long long)(r) * 101 + (ti)])
#define AFBN_(r, ti)       (afb_n[(unsigned long long)(r) * 101 + (ti)])
#define M18N_(r, i)        (m18n[(unsigned long long)(r) * 80 + (i)])
#define M18D_(r, i)        (m18d[(unsigned long long)(r) * 80 + (i)])
#define COH_(r, c, l, s)   (coh[(unsigned long long)(r) * (14 * 7 * 8) + (unsigned long long)(c) * 56 + (unsigned long long)(l) * 8 + (s)])
#define MB_(r, cell, j)    (m_born[(unsigned long long)(r) * MPT + (unsigned long long)(cell) * nmax + (j)])
#define MED_(r, cell, j)   (m_edm[(unsigned long long)(r) * MPT + (unsigned long long)(cell) * nmax + (j)])
#define MEX_(r, cell, j)   (m_exm[(unsigned long long)(r) * MPT + (unsigned long long)(cell) * nmax + (j)])
#define MAV_(r, cell, j)   (m_av[(unsigned long long)(r) * MPT + (unsigned long long)(cell) * nmax + (j)])
#define MKEY_(r, cell, j)  (m_key[(unsigned long long)(r) * MPT + (unsigned long long)(cell) * nmax + (j)])
#define MGID(r, cell, j)   ((unsigned long long)(r) * MPT + (unsigned long long)(cell) * nmax + (unsigned long long)(j))

// parameter block indices -- MUST match dosecore.par_block()
#define P_THK 0
#define P_THF 1
#define P_GAM 2
#define P_LAMS 3
#define P_DLO 4
#define P_DHI 5
#define P_SDD 6
#define P_C0 7
#define P_PHI0 8
#define P_K0 9
#define P_EPS 10
#define P_A0 11
#define P_ALD 12
#define P_ALU 13
#define P_R0 14
#define P_RHOA 15
#define P_ALM 16
#define P_RM 17
#define P_SEXR 18
#define P_DSEP 19
#define P_FC 20
#define P_EFC 21
#define P_GAP 22
#define P_BCM 23         // calibrated births per point of child mortality (per 100)
#define P_CMREF 24       // child mortality at the calibration reference year

// how far a woman's calendar year reaches: 5-year cohorts, 15..49
#define YEAR_AUX(t) ((unsigned)(1 + ((t) - 1900)))

__device__ __forceinline__ double ind_of(int scen, int r, int t, int q, int U,
                                         const double *gdp, const double *Pd, double ind0, int gy0) {
    if (scen == 0) return ind0;
    double x = (GDP_(r, t - gy0) - 6.5) / 2.2;
    if (x < 0.) x = 0.; if (x > 1.4) x = 1.4;
    return x + .12 * (double)(q - 2) + .10 * (double)U;
}

// ---------------------------------------------------------------- init
extern "C" __global__ void k_init(
    int nW, int scen, int coh0, int gy0, const unsigned long long *seedv,
    const double *PWc, const double *PMc, const double *wcell, const double *dosen,
    const double *Zc, const double *gdp, const double *Pd,
    const double *yrs, int WPC, int WPT, int MPT, int nmax,
    int *w_born, int *w_ed, int *w_ex, int *w_mk, int *w_st, int *w_par, int *w_afm, int *w_afbw,
    int *w_b30, int *w_b35, int *w_q, int *w_U, int *w_claim, double *w_wt, double *w_ind0,
    int *m_born, int *m_edm, int *m_exm, int *m_av, unsigned long long *m_key,
    int nWtot, int nMtot)
{
    int idx = (int)(blockIdx.x * blockDim.x + threadIdx.x);
    if (idx >= nWtot + nMtot) return;
    if (idx < nWtot) {
        int r = idx / WPT; int local = idx - r * WPT;
        int cell = local / WPC; int within = local - cell * WPC;
        int c = cell >> 1, U = cell & 1, q = within / nW;
        int y0 = coh0 + 5 * c;
        unsigned seed0 = (unsigned)seedv[r], seed1 = (unsigned)(seedv[r] >> 32);
        double u[8]; unsigned raw[8];
        draw_uniforms((unsigned long long)local, (unsigned)(r * 1024), seed0, seed1, 2, u, raw);
        int b = y0 + (int)(u[0] * 5.0);
        int ed = 0; double rr = u[1];
        while (ed < 6 && rr > PW_(r, cell, q, ed)) ed++;
        int e = 6 + (int)yrs[ed];
        if (ed >= 4) e += (int)(u[2] * 3.0) - 1;
        double ind0 = DOS_(r, ed) * ZC_(r, c);
        double ie;
        if (scen == 0) ie = ind0;
        else {   // original uses gdp at school exit, b+e, clamped to the array
            int gi = b + e - gy0; if (gi < 0) gi = 0; if (gi > NG - 1) gi = NG - 1;
            double x = (GDP_(r, gi) - 6.5) / 2.2; if (x < 0.) x = 0.; if (x > 1.4) x = 1.4;
            ie = x + .12 * (double)(q - 2) + .10 * (double)U;
        }
        w_born[idx] = b; w_ed[idx] = ed; w_ex[idx] = e;
        w_mk[idx] = e + (int)floor(PD_(r, P_GAM) * (ie > 0. ? ie : 0.) + 0.5);
        w_st[idx] = 0; w_par[idx] = 0; w_afm[idx] = -1; w_afbw[idx] = -1;
        w_b30[idx] = 0; w_b35[idx] = 0; w_q[idx] = q; w_U[idx] = U; w_claim[idx] = -1;
        w_wt[idx] = WC_(r, cell, q) / (double)nW;
        w_ind0[idx] = ind0;
    } else {
        int midx = idx - nWtot;
        int r = midx / MPT; int local = midx - r * MPT;
        int cell = local / nmax; int j = local - cell * nmax;
        int c = cell >> 1;
        int y0 = coh0 + 5 * c;
        int nm = (int)(5.0 * (double)nW * PD_(r, P_SEXR) + 0.5);
        unsigned seed0 = (unsigned)seedv[r], seed1 = (unsigned)(seedv[r] >> 32);
        if (j >= nm) { m_av[midx] = 0; m_key[midx] = 0ULL; m_born[midx] = 0; m_edm[midx] = 0; m_exm[midx] = 0; return; }
        double u[4]; unsigned raw[4];
        draw_uniforms((unsigned long long)(nWtot + local), (unsigned)(r * 1024), seed0, seed1, 1, u, raw);
        m_born[midx] = y0 - (int)(PD_(r, P_GAP) + 0.5) + (int)(u[0] * 5.0);
        int e = 0; double rr2 = u[1];
        while (e < 6 && rr2 > PM_(r, cell, e)) e++;
        m_edm[midx] = e;
        m_exm[midx] = 6 + (int)yrs[e] + 1;
        m_av[midx] = 1; m_key[midx] = 0ULL;
    }
}

// separation needs the parameter block; kept in k_claim together with the marriage market so that a
// woman's year is decided in one place.
extern "C" __global__ void k_claim(
    int t, int rnd, int nW, int scen, int gy0, const unsigned long long *seedv,
    const double *PWc, const double *PMc, const double *wcell, const double *dosen,
    const double *Zc, const double *gdp, const double *Pd, const int *Kci, const double *yrs,
    int WPC, int WPT, int MPT, int nmax,
    const int *w_born, const int *w_ed, const int *w_ex, const int *w_mk, int *w_st,
    int *w_q, int *w_U, int *w_claim, const double *w_ind0, const double *w_wt,
    double *expo, double *sing,
    const int *m_born, const int *m_edm, const int *m_exm, const int *m_av,
    unsigned long long *m_key, unsigned long long *w_key, int nWtot)
{
    int idx = (int)((long long)blockIdx.x * blockDim.x + threadIdx.x);
    if (idx >= nWtot) return;
    int r = idx / WPT; int local = idx - r * WPT;
    int cell = local / WPC; int within = local - cell * WPC;
    int U = cell & 1, q = within / nW;
    unsigned seed0 = (unsigned)seedv[r], seed1 = (unsigned)(seedv[r] >> 32);
    w_claim[idx] = -1; w_key[idx] = 0ULL;             // never read stale claim state
    int a = t - w_born[idx];
    if (rnd > 0) {                                    // later rounds: only women still single re-enter
        if (a < 15 || a > 49) return;
        if (a < w_ex[idx]) return;
        if (w_st[idx] != 0) return;
        if (a < w_mk[idx] || a > 45) return;
    }
    if (rnd == 0 && (a < 15 || a > 49)) return;
    if (rnd == 0) {   // exposure and single-share accumulation (before school exit and before this year's marriage)
        int ti = t - 1950; if (ti < 0) ti += 101;
        int ai = a - 15;
        atomicAdd(&EX_(r, ti, ai), w_wt[idx]);
        if (w_st[idx] == 0) atomicAdd(&SG_(r, ti, ai), w_wt[idx]);
    }
    if (a < w_ex[idx]) return;
    if (w_st[idx] == 1) {
        double us[4]; unsigned rws[4];
        draw_uniforms((unsigned long long)local, YEAR_AUX(t), seed0, seed1, 1, us, rws);
        if (us[1] < PD_(r, P_DSEP)) w_st[idx] = 2;
        return;
    }
    if (w_st[idx] != 0) return;
    double u[56]; unsigned raw[56];
    int Kcb = Kci[r];
    int nb = (12 + 4 * Kcb + 1 + 3) / 4;
    draw_uniforms((unsigned long long)local, YEAR_AUX(t) + (rnd > 0 ? 400u : 0u), seed0, seed1, nb, u, raw);
    double Ind = ind_of(scen, r, t, q, U, gdp, Pd, w_ind0[idx], gy0);
    double K0 = 1.0 / (1.0 + sy_exp(-(PD_(r, P_K0) + PD_(r, P_FC))));
    double K = K0 * sy_exp(-PD_(r, P_THK) * Ind);
    int nm = (int)(5.0 * (double)nW * PD_(r, P_SEXR) + 0.5);
    int claimed = -1, is_arranged = 0;
    double sh = (a <= 28) ? 1.0 : sy_exp(-.15 * (double)(a - 28));
    double parr = 1.0 - sy_exp(-PD_(r, P_A0) * PD_(r, P_EFC) * K * sh);
    if (rnd == 0 && u[2] < parr) {           // the family arranges at most one attempt per year
        for (int k = 0; k < 8; k++) {              // the original retries up to 8 times
            int jm = (int)(u[3 + k] * (double)nm);
            if (!MAV_(r, cell, jm)) continue;
            int age_m = t - MB_(r, cell, jm);
            int lo = MEX_(r, cell, jm) > 20 ? MEX_(r, cell, jm) : 20;
            if (age_m >= lo && age_m <= 55) { claimed = jm; is_arranged = 1; break; }
        }
    }
    if (claimed < 0 && a >= w_mk[idx] && a <= 45) {
        int Kc = Kci[r];
        double s_ = 1.0 + PD_(r, P_LAMS) * Ind;
        double Rw = PD_(r, P_R0) + PD_(r, P_RHOA) * (double)(a - w_mk[idx]);
        double bu = -1e9; int jb = -1, nv = 0;
        for (int k = 0; k < 3 * Kc; k++) {
            int jm = (int)(u[12 + k] * (double)nm);
            if (!MAV_(r, cell, jm)) continue;
            int age_m = t - MB_(r, cell, jm);
            int lo = MEX_(r, cell, jm) > 20 ? MEX_(r, cell, jm) : 20;
            if (!(age_m >= lo && age_m <= 55)) continue;
            double g = (yrs[MED_(r, cell, jm)] - yrs[w_ed[idx]]) / 12.0;
            double uu = -PD_(r, P_ALD) * s_ * (-g > 0. ? -g : 0.) - PD_(r, P_ALU) * (g > 0. ? g : 0.)
                        + logit_noise(u[12 + 3 * Kc + nv]);
            nv++;
            if (uu > bu) { bu = uu; jb = jm; }
            if (nv >= Kc) break;
        }
        if (jb >= 0 && bu + Rw > 0.0) {
            double g = (yrs[w_ed[idx]] - yrs[MED_(r, cell, jb)]) / 12.0;
            double um = -PD_(r, P_ALM) * (g > 0. ? g : 0.) + PD_(r, P_RM) + logit_noise(u[12 + 4 * Kc]);
            if (um > 0.0) { claimed = jb; is_arranged = 0; }
        }
    }
    if (claimed >= 0) {
        unsigned long long key = ((unsigned long long)(t - 1900) << 39)
                               | ((unsigned long long)is_arranged << 38)
                               | ((unsigned long long)raw[11] << 6)
                               | (unsigned long long)within;
        key += 1ULL;                                  // 0 means "unclaimed"
        w_claim[idx] = (int)MGID(r, cell, claimed);
        w_key[idx] = key;
        atomicMax(&MKEY_(r, cell, claimed), key);
    } else {
        w_key[idx] = 0ULL;
    }
}

// ---------------------------------------------------------------- resolve
extern "C" __global__ void k_resolve(
    int t, int WPT, const int *w_born, const int *w_ex, int *w_st, int *w_afm,
    const int *w_claim, const unsigned long long *w_key, const unsigned long long *m_key,
    int *m_av, int nWtot)
{
    int idx = (int)((long long)blockIdx.x * blockDim.x + threadIdx.x);
    if (idx >= nWtot) return;
    int claim = w_claim[idx];
    if (claim < 0) return;
    if (w_key[idx] == 0ULL) return;
    int a = t - w_born[idx];
    if (a < 15 || a > 49) return;
    if (a < w_ex[idx]) return;
    if (m_key[claim] != w_key[idx]) return;
    w_st[idx] = 1; w_afm[idx] = a; m_av[claim] = 0;
}

// ---------------------------------------------------------------- births
extern "C" __global__ void k_birth(
    int t, int nW, int scen, int gy0, const unsigned long long *seedv,
    const double *PWc, const double *PMc, const double *wcell, const double *dosen,
    const double *Zc, const double *gdp, const double *Pd, const double *hut, const double *Carr,
    int WPC, int WPT,
    const int *w_born, const int *w_ed, const int *w_ex, int *w_st, int *w_par, int *w_afbw,
    int *w_b30, int *w_b35, const int *w_q, const int *w_U, const double *w_wt, const double *w_ind0,
    double *births, double *afb_s, double *afb_n, int nWtot)
{
    int idx = (int)((long long)blockIdx.x * blockDim.x + threadIdx.x);
    if (idx >= nWtot) return;
    int r = idx / WPT; int local = idx - r * WPT;
    int cell = local / WPC; int within = local - cell * WPC;
    int U = cell & 1, q = within / nW;
    unsigned seed0 = (unsigned)seedv[r], seed1 = (unsigned)(seedv[r] >> 32);
    int a = t - w_born[idx];
    if (a < 15 || a > 49) return;
    if (a < w_ex[idx]) return;
    double Ind = ind_of(scen, r, t, q, U, gdp, Pd, w_ind0[idx], gy0);
    double K0 = 1.0 / (1.0 + sy_exp(-(PD_(r, P_K0) + PD_(r, P_FC))));
    double K = K0 * sy_exp(-PD_(r, P_THK) * Ind);
    int st = w_st[idx], par = w_par[idx];
    double hz = 0.0;
    if (st > 0 || a <= 40) {
        double phi = 2.0 * sy_exp(-PD_(r, P_THF) * Ind) - 1.0;
        double Di = PD_(r, P_DLO) + (PD_(r, P_DHI) - PD_(r, P_DLO)) * 0.5 * (1.0 + phi);
        {   // Child-mortality channel (a MODEL EXTENSION, not in the published model): desired births
            // respond to the prevailing child mortality with the coefficient estimated from our own
            // country-level data, beta births per woman per point of child mortality per 100, measured
            // against the child mortality of the calibration era.  With beta = 0 the addition is exactly
            // zero and the engine is the published model bit for bit (the porting test checks this).
            int si = t - gy0; if (si < 0) si = 0; if (si > NG - 1) si = NG - 1;
            double cm = Carr[(unsigned long long)r * NG + si];
            Di = Di + PD_(r, P_BCM) * (cm - PD_(r, P_CMREF));
        }
        double cost = PD_(r, P_C0) * (1.0 - .9 * K) * (1.0 + .1 * (double)par);
        double S = 1.0 / (1.0 + sy_exp(-(Di - (double)par - 0.5) / PD_(r, P_SDD)));
        double base_h = PD_(r, P_PHI0) * hut[a] * S * sy_exp(-cost);
        if (st == 1) hz = base_h;
        else if (st == 2) hz = base_h * K;
        else hz = PD_(r, P_EPS) * hut[a] * sy_exp(-cost);
    }
    if (hz > 0.0) {
        double u[4]; unsigned raw[4];
        draw_uniforms((unsigned long long)local, YEAR_AUX(t), seed0, seed1, 1, u, raw);
        if (u[0] < 1.0 - sy_exp(-hz)) {
            int ti = t - 1950; if (ti < 0) ti += 101;
            int ai = a - 15;
            atomicAdd(&BB_(r, ti, ai), w_wt[idx]);
            if (par == 0) {
                atomicAdd(&AFBS_(r, ti), w_wt[idx] * (double)a);
                atomicAdd(&AFBN_(r, ti), w_wt[idx]);
                w_afbw[idx] = a;
            }
            w_par[idx] = par + 1;
            if (a < 30) w_b30[idx] = w_b30[idx] + 1;
            if (a < 35) w_b35[idx] = w_b35[idx] + 1;
        }
    }
}

// ---------------------------------------------------------------- end-of-run cohort aggregates
extern "C" __global__ void k_final(
    int tmax, int coh0, int my0, int WPC, int WPT,
    const int *w_born, const int *w_ed, const int *w_afm, const int *w_par, const int *w_afbw,
    const int *w_b30, const int *w_b35, const double *w_wt,
    double *m18n, double *m18d, double *coh, int nWtot)
{
    int idx = (int)((long long)blockIdx.x * blockDim.x + threadIdx.x);
    if (idx >= nWtot) return;
    int r = idx / WPT; int local = idx - r * WPT;
    int cell = local / WPC;
    int c = cell >> 1;
    int y0 = coh0 + 5 * c;
    int b = w_born[idx];
    if (b + 18 <= tmax) {
        atomicAdd(&M18D_(r, b - my0), w_wt[idx]);
        if (w_afm[idx] >= 0 && w_afm[idx] < 18) atomicAdd(&M18N_(r, b - my0), w_wt[idx]);
    }
    if (y0 + 4 + 49 <= tmax) {
        int ed = w_ed[idx]; double w = w_wt[idx]; int par = w_par[idx];
        atomicAdd(&COH_(r, c, ed, 0), w);
        atomicAdd(&COH_(r, c, ed, 1), w * (double)w_b30[idx]);
        atomicAdd(&COH_(r, c, ed, 2), w * (double)w_b35[idx]);
        atomicAdd(&COH_(r, c, ed, 3), w * (double)par);
        if (par == 0) atomicAdd(&COH_(r, c, ed, 4), w);
        else { atomicAdd(&COH_(r, c, ed, 6), w * (double)w_afbw[idx]); atomicAdd(&COH_(r, c, ed, 7), w); }
        if (w_afm[idx] >= 0) atomicAdd(&COH_(r, c, ed, 5), w);
    }
}
