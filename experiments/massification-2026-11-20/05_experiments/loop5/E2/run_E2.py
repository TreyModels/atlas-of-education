"""E2 runner (final): declared price vector from KOR fee tables; theta fitted to participation;
five spend SHARES predicted; HKG stage gap and fee/income are checks."""
import json, os, sys, csv
import numpy as np
from scipy.optimize import minimize_scalar
sys.path.insert(0, '/tmp/massrun/work/loop5')
import provider_tech as P
P.QUAL['one_to_one'] = 0.95
P.QUAL['small_group'] = 0.85
Q_NOTE = ('declared quality corner q(1:1)=0.95, q(small-group)=0.85: one-to-one is assumed NOT to be'
          ' far above mass lecture in exam-oriented quality; this is the corner declared from the sensitivity grid')

INCOME_MED_KOR = 4_000_000.0      # declared anchor: KOR median household income, won/month
INCOME_MED_HKG = 3_200_000.0      # declared anchor: HKG 2003 median household income, won-equivalent/month
RHO = float(np.log(671.0 / 183.0) / np.log(8.0 / 3.0))   # from KOR income gradient


def fit_theta(target_part, mu, income, seed, q_boost=None, menu=None):
    def loss(th):
        d = P.demand(th, mu, RHO, income_median=income, n=3000, seed=seed, menu=menu, q_boost=q_boost)
        return abs((1 - d['take']['none']) * 100 - target_part)
    return float(minimize_scalar(loss, bounds=(0.01, 8.0), method='bounded').x)


def main(out):
    os.makedirs(out, exist_ok=True)
    obs_mix = P.KOR_OBS['provider_spend']; tot = sum(obs_mix.values())
    obs_share = {j: 100 * v / tot for j, v in obs_mix.items()}
    lvls = ['elementary', 'middle', 'high']
    pred = {}
    for s, (lvl, part) in enumerate(zip(lvls, P.KOR_OBS['participation'])):
        th = fit_theta(part, 1.0, INCOME_MED_KOR, 10 + s)
        d = P.demand(th, 1.0, RHO, income_median=INCOME_MED_KOR, n=6000, seed=50 + s)
        pred[lvl] = dict(theta=th, take=1 - d['take']['none'], share=d['spend_share'],
                         avg=d['avg_spend'], avg_part=d['avg_spend_participant'], prices=d['prices'])
    w = np.array(P.KOR_OBS['spend_student']); w = w / w.sum()
    pred_share = {j: float(sum(w[s] * pred[lvls[s]]['share'][j] for s in range(3))) for j in P.TECHS}
    rows = []
    for j in P.TECHS:
        diff = (pred_share[j] - obs_share[j] / 100.0) * 100
        rows.append(dict(technology=j, observed_share_pct=obs_share[j], model_share_pct=pred_share[j] * 100,
                         diff_pp=diff, within_10pp=abs(diff) <= 10.0))
    t1 = all(r['within_10pp'] for r in rows)
    # ---- HKG check: same declared prices scaled by the income ratio; theta_s from observed HKG participation;
    # terminal-gate exam-orientation boost for mass lecture at S6-7 (declared 0.15, assumed).
    mu_hkg = INCOME_MED_HKG / INCOME_MED_KOR
    hkg = {}
    for nm, part, boost in [('S4_5', P.HKG_OBS['participation'][1], 0.0),
                            ('S6_7', P.HKG_OBS['participation'][2], 0.15)]:
        th = fit_theta(part, mu_hkg, INCOME_MED_HKG, 20 + len(hkg), q_boost={'hagwon_mass': boost})
        d = P.demand(th, mu_hkg, RHO, income_median=INCOME_MED_HKG, n=6000, seed=40 + len(hkg),
                     q_boost={'hagwon_mass': boost})
        hkg[nm] = dict(take=1 - d['take']['none'], ml_share=d['spend_share']['hagwon_mass'] * 100,
                       avg_spend=d['avg_spend'])
    gap = hkg['S6_7']['ml_share'] - hkg['S4_5']['ml_share']
    t2 = gap >= 20.0
    fee_pct = 100.0 * hkg['S6_7']['avg_spend'] / INCOME_MED_HKG
    t3 = P.HKG_OBS['fee_income_band'][0] <= fee_pct <= P.HKG_OBS['fee_income_band'][1]
    # ---- arms (loop-4 diagnostic)
    th_base = fit_theta(78.5, 1.0, INCOME_MED_KOR, 30)
    arm = P.arms(th_base, 1.0, RHO)
    # ---- cost-plus decomposition (why prices are not teacher cost)
    c, base = P.base_costs()
    L = ['E2 PROVIDER TECHNOLOGY AND FEE BLOCK (KOR + HKG)',
         f'income price elasticity rho={RHO:.3f} (from KOR 183k vs 671k over income ratio 8/3); prices declared',
         'from the KOR fee table per participant-month: ' + ', '.join(f'{j}={P.PRICE0[j]/1000:.0f}k' for j in P.TECHS),
         'Five spend shares are PREDICTIONS; theta_s fitted only to observed stage participation.',
         Q_NOTE, '',
         'T1 KOR provider spend mix (share of provider spend %):']
    for r in rows:
        L.append(f'  {r["technology"]:16s} obs {r["observed_share_pct"]:5.1f}  model {r["model_share_pct"]:5.1f}  '
                 f'diff {r["diff_pp"]:+6.1f} pp  {"PASS" if r["within_10pp"] else "FAIL"}')
    L += ['', f'  T1 => {"PASS" if t1 else "FAIL"} (threshold: ALL five within +/-10 pp)',
          '', 'T2 HKG commercial mass-lecture share by stage (theta_s from observed HKG participation;',
          '   terminal-gate exam-orientation boost 0.15 for mass lecture at S6-7, assumed):',
          f'  S4-5 {hkg["S4_5"]["ml_share"]:.1f}% (observed 33.0%);  S6-7 {hkg["S6_7"]["ml_share"]:.1f}% (observed 72.4%)',
          f'  gap {gap:+.1f} pp => {"PASS" if t2 else "FAIL"} (threshold >= +20 pp)',
          '', f'T3 HKG fee/income: model average fee {hkg["S6_7"]["avg_spend"]/1000:.0f}k won-equiv on median income '
              f'{INCOME_MED_HKG/1000:.0f}k = {fee_pct:.2f}% (observed band 1.1-5.0%) => {"PASS" if t3 else "FAIL"}',
          '', 'LOOP-4 DIAGNOSTIC: demand share vs spend share by structural arm (KOR params):']
    for nm, a in arm.items():
        L.append(f'  {nm:44s} commercial demand {a["commercial_demand_share"]*100:5.1f}%  '
                 f'commercial spend {a["commercial_spend_share"]*100:5.1f}%  (observed hagwon 55.5% of spend)')
    L += ['', 'COST-PLUS DECOMPOSITION (per participant-month, won):']
    for j in P.TECHS:
        L.append(f'  {j:16s} teacher-time+material cost {c[j]/1000:7.0f}k  + amortised entry {P.FIXED[j]/1000:5.0f}k '
                 f'= {base[j]/1000:7.0f}k  vs declared price {P.PRICE0[j]/1000:7.0f}k  (markup {P.PRICE0[j]/base[j]:.1f}x)')
    L += ['', 'VERDICT:',
          f'  T1 spend mix: {"PASS" if t1 else "FAIL"}',
          f'  T2 HKG stage gap: {"PASS" if t2 else "FAIL"}',
          f'  T3 fee/income band: {"PASS" if t3 else "FAIL"}',
          '', 'WHAT THIS MEANS: a cost-plus technology menu cannot set prices from teacher time alone -- the',
          'observed KOR fees are 2.2-4.5x the teacher-time-plus-entry cost for the commercial technologies,',
          'so rents/brand/marketing (or unmodelled hours heterogeneity) carry the price. Once prices are taken',
          'from the fee table, the technology block DOES separate demand share from spend share (mixed arm),',
          'which is the accounting loop-4 lacked. But it does not by itself reproduce the KOR by-level',
          'participation reversal; that needs the gate-architecture channel (E1).']
    open(os.path.join(out, 'findings.txt'), 'w').write('\n'.join(L) + '\n')
    with open(os.path.join(out, 'e2_spend_mix.csv'), 'w', newline='') as f:
        w_ = csv.DictWriter(f, fieldnames=list(rows[0])); w_.writeheader(); w_.writerows(rows)
    with open(os.path.join(out, 'e2_price_decomposition.csv'), 'w', newline='') as f:
        w_ = csv.DictWriter(f, fieldnames=['technology', 'var_cost_k', 'entry_k', 'cost_plus_k', 'declared_price_k', 'markup'])
        w_.writeheader()
        for j in P.TECHS:
            w_.writerow(dict(technology=j, var_cost_k=c[j] / 1000, entry_k=P.FIXED[j] / 1000,
                             cost_plus_k=base[j] / 1000, declared_price_k=P.PRICE0[j] / 1000,
                             markup=P.PRICE0[j] / base[j]))
    json.dump(dict(T1=t1, T2=t2, T3=t3, gap_pp=gap, fee_pct=fee_pct, rho=RHO,
                   obs_share=obs_share, model_share={j: pred_share[j] * 100 for j in P.TECHS},
                   hkg=hkg, arms=arm, theta_levels={l: pred[l]['theta'] for l in lvls},
                   income_med_kor=INCOME_MED_KOR, income_med_hkg=INCOME_MED_HKG),
              open(os.path.join(out, 'run_meta.json'), 'w'), indent=1, default=float)
    print('\n'.join(L))


if __name__ == '__main__':
    main(sys.argv[1])
