/* Education Atlas — youth labour market with a categorical (Tilly) core, browser port of engine/firms/categorical.py.
   Same equations, same order of operations; tests/js_parity.mjs checks it against the Python runs stored in ATLAS_DATA.
   Workers: cells of (degree / none) x (insider / outsider). Positions: secure posts (rationed, hoarded), private graduate
   jobs (free entry), open jobs (free entry, a share c requiring a degree by emulation). Monthly; masses in millions. */
(function (root) {
'use strict';
const exp = Math.exp, log = Math.log;

function urnXFromF(f, a) {
  if (f >= a) throw new Error('f must be below a');
  let lo = 1e-12, hi = 200.0;
  for (let i = 0; i < 200; i++) { const mid = 0.5 * (lo + hi); if (a * (1 - exp(-mid)) / mid > f) lo = mid; else hi = mid; }
  return 0.5 * (lo + hi);
}
function cesRelative(S, Sref, sigma) { return Number.isFinite(sigma) ? Math.pow(S / Sref, -1 / sigma) : 1.0; }

function tiers(types) {
  const idx = types.map((t, i) => i).filter(i => types[i][0] > 0).sort((i, j) => types[j][1] - types[i][1]);
  const out = [];
  for (const i of idx) {
    const last = out[out.length - 1];
    if (last && Math.abs(types[last[0]][1] - types[i][1]) <= 1e-12 * Math.max(1, Math.abs(types[i][1]))) last.push(i);
    else out.push([i]);
  }
  return out;
}
function groupsFor(types, rank) { return rank === 'value' ? tiers(types) : [types.map((t, i) => i).filter(i => types[i][0] > 0)]; }
function rankValue(types, rank) {
  if (!types.some(t => t[0] > 0)) return 0;
  let v = 0, surv = 1;
  for (const t of groupsFor(types, rank)) {
    const X = t.reduce((s, i) => s + types[i][0], 0);
    v += surv * (1 - exp(-X)) * t.reduce((s, i) => s + types[i][0] * types[i][1], 0) / X;
    surv *= exp(-X);
  }
  return v;
}
function rankHires(V, types, rank) {
  const out = types.map(() => 0);
  if (V <= 0 || !types.some(t => t[0] > 0)) return out;
  let surv = 1;
  for (const t of groupsFor(types, rank)) {
    const X = t.reduce((s, i) => s + types[i][0], 0);
    const h = V * surv * (1 - exp(-X));
    for (const i of t) out[i] = h * types[i][0] / X;
    surv *= exp(-X);
  }
  return out;
}
const mean = a => a.reduce((s, x) => s + x, 0) / a.length;

const GROUPS = [['G_in', true, true], ['G_out', true, false], ['N_in', false, true], ['N_out', false, false]];

/* opts: params overriding defaults (any model.py or Tilly name), plus
     gradSupply: 'observed' | 'hold2018' | number (multiplier on graduates from 2019)
     demand: 'observed' | 'flat' | 'hold2018'      grad_demand: 'observed' | 'flat' */
function run(DATA, opts) {
  const o = Object.assign({}, opts || {});
  const p = Object.assign({}, DATA.defaults, DATA.tilly_defaults, o);
  const T = p; const I = DATA.inputs;
  const sigmaA = (p.sigma_A === null || p.sigma_A === 'inf' || p.sigma_A === Infinity) ? Infinity : p.sigma_A;
  const y0 = I.years[0];
  const Gobs = y => I.graduates[Math.min(Math.max(y - y0, 0), I.graduates.length - 1)];
  const NL0 = y => I.nongrad[Math.min(Math.max(y - y0, 0), I.nongrad.length - 1)];
  const gs = o.gradSupply || 'observed';
  const G = gs === 'hold2018' ? (y => Gobs(Math.min(y, 2018))) : typeof gs === 'number' ? (y => y >= 2019 ? gs * Gobs(y) : Gobs(y)) : Gobs;
  const NL = o.nongradSupply === 'hold2018' ? (y => NL0(Math.min(y, 2018))) : NL0;
  const a = p.a, r = p.r;
  const s_g = p.s_g * p.sep_scale, s_n = p.s_n * p.sep_scale, s_gn = p.s_gn * p.sep_scale;
  const dg = r + s_g + p.age_g, dn = r + s_n + p.age_n, dgn = r + s_gn + p.age_g, dsec = r + T.s_sec + p.age_g;
  const w_g0 = p.p_g0 * (1 - p.m_g), w_n0 = p.p_n0 * (1 - p.m_n);
  const om_g = (w_g0 - p.z_g) / (p.p_g0 - p.z_g), om_n = (w_n0 - p.z_n) / (p.p_n0 - p.z_n);
  const kap_g = (1 - exp(-urnXFromF(p.f_g_ref, a))) * (p.p_g0 - w_g0) / dg;
  const kap_n = (1 - exp(-urnXFromF(p.f_n_ref, a))) * (p.p_n0 - w_n0) / dn;
  const [SG_ref, SN_ref] = p.S_ref;
  const w_sec = T.sec_prem * w_g0;
  const secPerMonth = T.sec_open * p.psi_g * 0.5 * (G(2018) + G(2019)) / 12;
  const names = GROUPS.map(g => g[0]), deg = {}, ins = {};
  GROUPS.forEach(([k, d, i]) => { deg[k] = d; ins[k] = i; });
  const dgroups = names.filter(k => deg[k]), ngroups = names.filter(k => !deg[k]);
  const U = {}, W = {}, Eg = {}, Es = {}, Eo = {}, qsec = {};
  names.forEach(k => { U[k] = 0; Eo[k] = 0; });
  dgroups.forEach(k => { W[k] = 0; Eg[k] = 0; Es[k] = 0; qsec[k] = 0.05; });
  let S_un = 0, S_sig = 0, pending = 0, w_g = w_g0, w_n = w_n0, c = 0;
  const histG = [], histN = [];
  const shareG = {G_in: T.ins_g, G_out: 1 - T.ins_g}, shareN = {N_in: T.ins_n, N_out: 1 - T.ins_n};
  const out = {year: [], month: [], rate_old: [], rate_new: [], slack: [], u_G: [], u_N: [], waiting: [], c_req: [],
    u_G_in: [], u_G_out: [], u_N_in: [], u_N_out: [], w_N_in: [], w_N_out: [], f_g: [], V_n: [], V_g: [], p_g: [], w_g: [],
    under: [], sec_ins_share: [], rent_exploit: [], rent_hoard: [], output: [], balance: [], A: [], LF_G: [], LF_N: []};
  const t_ref = p.ref_years[0] + 0.5 * (p.ref_years[1] - p.ref_years[0]) + 0.5;
  const idxOf = {}; I.months.forEach(([y, m], i) => { idxOf[y * 100 + m] = i; });
  const warmUntil = p.warm_until[0] * 100 + p.warm_until[1];
  // demand index from adult unemployment at this run's adult margin m_a (model.demand_index)
  const qA = u => 1 - exp(-urnXFromF(0.012 * (1 - u) / u, a));
  const qRef = qA(I.adult_ref);
  const Aobs = I.adult.map(u => (u === null || u === undefined) ? 1.0 : 1 - p.m_a + p.m_a * qRef / qA(u));
  for (const [y, m] of I.months) {
    const tt = y + (m - 0.5) / 12 - t_ref;
    const i = idxOf[y * 100 + m];
    let A = Aobs[i];
    if (o.demand === 'flat') A = 1.0;
    if (o.demand === 'hold2018' && y >= 2019) A = 1.0;
    const lfg = dgroups.reduce((s, k) => s + U[k] + Eg[k] + Eo[k] + Es[k], 0);
    const lfn = ngroups.reduce((s, k) => s + U[k] + Eo[k], 0);
    histG.push(lfg); histN.push(lfn);
    const LF_G = mean(histG.slice(-12)), LF_N = mean(histN.slice(-12));
    const warm = (y * 100 + m) < warmUntil;
    const sig = warm ? Infinity : sigmaA;
    let Dg = 1.0;
    if ((o.grad_demand || p.grad_demand || 'observed') === 'observed' && !warm)
      Dg = Math.pow(I.property[i], p.e_prop) * (1 - p.dr_drop * ((y * 100 + m) >= 202108 ? 1 : 0));
    const p_g = Dg * A * p.p_g0 * cesRelative(Math.max(LF_G, 1e-9), SG_ref * exp(p.g_H * tt), sig);
    const p_n = A * p.p_n0 * cesRelative(Math.max(LF_N, 1e-9), SN_ref * exp(p.g_N * tt), sig);
    const lg = warm ? 1 : p.lam_g, ln = warm ? 1 : p.lam_n;
    w_g += lg * (p.z_g + om_g * (p_g - p.z_g) - w_g);
    w_n += ln * (p.z_n + om_n * (p_n - p.z_n) - w_n);
    const wo = {}, z = {}, Jo = {};
    for (const k of names) {
      wo[k] = ins[k] ? w_n : (1 - T.ex) * w_n;
      z[k] = (deg[k] ? p.z_g : p.z_n) * (ins[k] ? 1 : 1 - T.ex) + (ins[k] ? T.z_ins : 0);
      Jo[k] = deg[k] ? (p_n * (1 + p.eps) - wo[k]) / dgn : (p_n - wo[k]) / dn;
    }
    const J_g = (p_g - w_g) / dg;
    if (m === 9) { S_un = p.psi_g * G(y + 1); S_sig = 0; }
    const searching = m >= 9 || m <= 6;
    const stud = searching ? p.zeta * S_un : 0;
    // 1. secure posts
    const hS = {}, hS_W = {};
    dgroups.forEach(k => { hS[k] = 0; hS_W[k] = 0; });
    if (secPerMonth > 0) {
      const app = {}; dgroups.forEach(k => { app[k] = W[k] + T.chi_s * U[k]; });
      const O = secPerMonth, O_h = T.hoard * O;
      const insApp = dgroups.filter(k => ins[k]).reduce((s, k) => s + app[k], 0);
      const hIns = (O_h > 0 && insApp > 0) ? O_h * (1 - exp(-insApp / O_h)) : 0;
      for (const k of dgroups) if (ins[k] && insApp > 0) hS[k] += hIns * app[k] / insApp;
      const O_o = O - hIns;
      const rest = {}; dgroups.forEach(k => { rest[k] = app[k] - hS[k]; });
      const tot = dgroups.reduce((s, k) => s + rest[k], 0);
      const hOpen = (O_o > 0 && tot > 0) ? O_o * (1 - exp(-tot / O_o)) : 0;
      for (const k of dgroups) if (tot > 0) hS[k] += hOpen * rest[k] / tot;
      for (const k of dgroups) {
        if (app[k] > 0) hS_W[k] = hS[k] * W[k] / app[k];
        qsec[k] = 0.7 * qsec[k] + 0.3 * (app[k] > 0 ? hS[k] / app[k] : 0);
      }
    }
    const hS_U = {}; dgroups.forEach(k => { hS_U[k] = hS[k] - hS_W[k]; });
    // 2. private graduate jobs
    const UGav = {}; dgroups.forEach(k => { UGav[k] = U[k] - hS_U[k]; });
    const Ueff = dgroups.reduce((s, k) => s + UGav[k], 0) + p.chi * dgroups.reduce((s, k) => s + Eo[k], 0) + stud;
    const kg = kap_g * A;
    let f_g = 0, V_g = 0;
    if (J_g > kg && Ueff > 0) { const x = -log(1 - kg / J_g); f_g = a * (1 - exp(-x)) / x; V_g = a * Ueff / x; }
    const hG_U = {}, hG_O = {};
    dgroups.forEach(k => { hG_U[k] = f_g * UGav[k]; hG_O[k] = f_g * p.chi * Eo[k]; });
    const hG_S = f_g * stud;
    // 3. downgrading and waiting
    const phi = {}, wflow = {};
    for (const k of dgroups) {
      wflow[k] = 0;
      const dz = (dg * z[k] + f_g * w_g) / (dg + f_g);
      phi[k] = 1 / (1 + exp(-((wo[k] - p.d) - dz) / (p.nu * p.p_n0)));
      if (T.wait_max > 0 && secPerMonth > 0) {
        const gain = qsec[k] * (w_sec - dz) / dsec - f_g * (w_g - dz) / dg;
        const supp = ins[k] ? T.supp_in : T.supp_out;
        wflow[k] = T.wait_max * supp / (1 + exp(-gain / T.wait_scale));
      }
    }
    // 4. open jobs
    const Gapp = {}; dgroups.forEach(k => { Gapp[k] = phi[k] * (UGav[k] - hG_U[k]) * (1 - wflow[k]); });
    const UNt = ngroups.reduce((s, k) => s + U[k], 0), Gt = dgroups.reduce((s, k) => s + Gapp[k], 0);
    const kn = kap_n * A;
    const hO = {}; names.forEach(k => { hO[k] = 0; });
    let V_n = 0;
    if (UNt + Gt > 0) {
      const base = UNt > 0 ? UNt : Gt, openfrac = 1 - c;
      const types = xb => { const xs = {};
        for (const k of dgroups) xs[k] = xb * Gapp[k] / base;
        for (const k of ngroups) xs[k] = openfrac > 1e-12 ? xb * U[k] / base / openfrac : 0;
        return xs; };
      const value = xb => { const xs = types(xb);
        const vOpen = rankValue(names.map(k => [xs[k], Jo[k]]), p.rank);
        if (c <= 0) return vOpen;
        return openfrac * vOpen + c * rankValue(dgroups.map(k => [xs[k], Jo[k]]), p.rank); };
      if (value(200.0) > kn) {
        let lo = 1e-12, hi = 200.0;
        for (let it = 0; it < 100; it++) { const mid = Math.sqrt(lo * hi); if (value(mid) > kn) hi = mid; else lo = mid; }
        const xb = Math.sqrt(lo * hi);
        V_n = a * base / xb;
        const xs = types(xb);
        rankHires(V_n * openfrac, names.map(k => [xs[k], Jo[k]]), p.rank).forEach((h, j) => { hO[names[j]] += h; });
        if (c > 0) rankHires(V_n * c, dgroups.map(k => [xs[k], Jo[k]]), p.rank).forEach((h, j) => { hO[dgroups[j]] += h; });
      }
    }
    if (T.em_rate > 0 && !warm) {
      const sG = (lfg + lfn) > 0 ? lfg / (lfg + lfn) : 0;
      c = Math.min(Math.max(c + T.em_rate * (c + T.c0) * (1 - c) * (sG - T.em_threshold), 0), 0.99);
    }
    // 5. entry
    const infl = {}, signed = {};
    names.forEach(k => { infl[k] = 0; }); dgroups.forEach(k => { signed[k] = 0; });
    if (m === 7) {
      const cls = p.psi_g * G(y);
      for (const k of dgroups) signed[k] = S_sig * shareG[k];
      pending = cls - S_sig; S_un = 0; S_sig = 0;
    }
    if (m >= 7 && pending > 0) {
      const totIn = pending * (m === 7 ? p.july_g : (1 - p.july_g) / 5);
      for (const k of dgroups) infl[k] = totIn * shareG[k];
    }
    const nin = p.psi_n * NL(y) * (m === 7 ? p.july_n : (1 - p.july_n) / 11);
    for (const k of ngroups) infl[k] = nin * shareN[k];
    // 6. stocks
    const stock = () => names.reduce((s, k) => s + U[k] + Eo[k], 0) + dgroups.reduce((s, k) => s + W[k] + Eg[k] + Es[k], 0);
    const before = stock();
    const ageOut = dgroups.reduce((s, k) => s + p.age_g * (U[k] + W[k] + Eg[k] + Es[k] + Eo[k]), 0) +
      ngroups.reduce((s, k) => s + p.age_n * (U[k] + Eo[k]), 0);
    for (const k of dgroups) {
      const u = U[k], wt = W[k], eg = Eg[k], es = Es[k], eo = Eo[k];
      const toWait = wflow[k] * (UGav[k] - hG_U[k]);
      U[k] = u + infl[k] - hS_U[k] - hG_U[k] - hO[k] - toWait + T.wait_quit * wt + s_g * eg + s_gn * eo + T.s_sec * es - p.age_g * u;
      W[k] = wt + toWait - hS_W[k] - T.wait_quit * wt - p.age_g * wt;
      Eg[k] = eg + hG_U[k] + hG_O[k] + signed[k] - s_g * eg - p.age_g * eg;
      Es[k] = es + hS[k] - T.s_sec * es - p.age_g * es;
      Eo[k] = eo + hO[k] - hG_O[k] - s_gn * eo - p.age_g * eo;
    }
    for (const k of ngroups) {
      const u = U[k], eo = Eo[k];
      U[k] = u + infl[k] - hO[k] + s_n * eo - p.age_n * u;
      Eo[k] = eo + hO[k] - s_n * eo - p.age_n * eo;
    }
    if (searching) { S_un -= hG_S; S_sig += hG_S; }
    const balance = stock() - (before + names.reduce((s, k) => s + infl[k], 0) - ageOut) - dgroups.reduce((s, k) => s + signed[k], 0);
    // 7. observation
    const Ut = names.reduce((s, k) => s + U[k], 0), Wt = dgroups.reduce((s, k) => s + W[k], 0);
    const LF = Ut + dgroups.reduce((s, k) => s + Eg[k] + Es[k], 0) + names.reduce((s, k) => s + Eo[k], 0);
    const su = searching ? p.zeta * S_un : 0;
    const LG = dgroups.reduce((s, k) => s + U[k] + Eg[k] + Es[k] + Eo[k], 0), LN = ngroups.reduce((s, k) => s + U[k] + Eo[k], 0);
    const Eempg = dgroups.reduce((s, k) => s + Eg[k] + Es[k] + Eo[k], 0);
    const hSt = dgroups.reduce((s, k) => s + hS[k], 0);
    const lfk = k => U[k] + Eo[k] + (deg[k] ? Eg[k] + Es[k] : 0);
    const push = (k, v) => out[k].push(v);
    push('year', y); push('month', m);
    push('rate_new', LF > 0 ? 100 * Ut / LF : NaN); push('rate_old', LF > 0 ? 100 * (Ut + su) / (LF + su) : NaN);
    push('slack', LF > 0 ? 100 * (Ut + Wt) / (LF + Wt) : NaN);
    push('u_G', LG > 0 ? 100 * dgroups.reduce((s, k) => s + U[k], 0) / LG : 0);
    push('u_N', LN > 0 ? 100 * UNt_after() / LN : 0);
    function UNt_after() { return ngroups.reduce((s, k) => s + U[k], 0); }
    for (const k of names) push('u_' + k, lfk(k) > 0 ? 100 * U[k] / lfk(k) : 0);
    push('w_N_in', w_n); push('w_N_out', wo.N_out);
    push('waiting', Wt); push('c_req', c); push('f_g', f_g); push('V_n', V_n); push('V_g', V_g); push('p_g', p_g); push('w_g', w_g);
    push('under', Eempg > 0 ? 100 * dgroups.reduce((s, k) => s + Eo[k], 0) / Eempg : 0);
    push('sec_ins_share', hSt > 0 ? hS.G_in / hSt : NaN);
    push('rent_exploit', names.reduce((s, k) => s + (w_n - wo[k]) * Eo[k], 0));
    push('rent_hoard', dgroups.reduce((s, k) => s + (w_sec - w_g) * Es[k], 0));
    push('output', p_g * dgroups.reduce((s, k) => s + Eg[k] + Es[k], 0) + p_n * (1 + p.eps) * dgroups.reduce((s, k) => s + Eo[k], 0)
      + p_n * ngroups.reduce((s, k) => s + Eo[k], 0));
    push('balance', balance); push('A', A); push('LF_G', LG); push('LF_N', LN);
  }
  out.final = {U: Object.assign({}, U), W: Object.assign({}, W), Eg: Object.assign({}, Eg), Es: Object.assign({}, Es), Eo: Object.assign({}, Eo)};
  return out;
}

function windowMean(R, key, a, b) {
  const v = [];
  for (let i = 0; i < R.year.length; i++) {
    const ym = R.year[i] * 100 + R.month[i];
    if (ym >= a[0] * 100 + a[1] && ym <= b[0] * 100 + b[1] && Number.isFinite(R[key][i])) v.push(R[key][i]);
  }
  return v.length ? mean(v) : NaN;
}

const api = {run, windowMean, urnXFromF, cesRelative, rankValue, rankHires};
if (typeof module !== 'undefined') module.exports = api;
root.AtlasYouth = api;
})(typeof window !== 'undefined' ? window : globalThis);
