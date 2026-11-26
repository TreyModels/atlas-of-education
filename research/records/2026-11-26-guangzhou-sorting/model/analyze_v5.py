import json,numpy as np
from scipy.stats import spearmanr
R=[json.loads(l) for l in open('/home/claude/sig/v5_eq_results.jsonl')]
g=lambda k: np.array([r[k] for r in R],float); P=lambda k: np.array([r['params'][k] for r in R])
q=lambda x:[round(float(v),3) for v in np.nanpercentile(x,[5,25,50,75,95])]
def verdict(name, within, signok=None):
    w=np.nanmean(within); lab='HOLDS' if w>=.8 else ('BIASED' if (signok is None or np.nanmean(signok)>=.8) else 'MISLEADS')
    print(f'{name:48s} within tolerance {w:5.2f}  -> {lab}')
tr=g('truth_any_tut')
verdict('E74 tutoring-achievement, naive', np.abs(g('E74_naive')-tr)<=.05, np.sign(g('E74_naive'))==np.sign(tr+1e-9))
verdict('E74/E72 with prior score + SES', np.abs(g('E74_controls')-tr)<=.05, np.sign(g('E74_controls'))==np.sign(tr+1e-9))
print('   naive minus truth',q(g('E74_naive')-tr),' controls minus truth',q(g('E74_controls')-tr))
sp=np.abs(g('E76_t'))>2; print(f"{'E76 SES x tutoring (truth 0)':48s} spurious |t|>2 in {sp.mean():.2f} ->",'MISLEADS' if sp.mean()>.2 else 'HOLDS')
gain=g('E58_R2_with_U')-g('E58_R2_income_only'); print(f"{'E58 participation logit, income only':48s} U-shape adds <0.01 R2 in {np.mean(gain<.01):.2f} ->",'HOLDS' if np.mean(gain<.01)>=.8 else 'MISSES U-SHAPE','  R2 income',q(g('E58_R2_income_only')),'with U',q(g('E58_R2_with_U')))
rho=P('RHO_DEMAND'); e79=g('E79_coef'); low=rho<.1
print(f"{'E79 peer effect in demand':48s} spurious >0.1 when true <0.1: {np.mean(e79[low]>.1):.2f} (n={low.sum()}) ->",'MISLEADS' if np.mean(e79[low]>.1)>.2 else 'HOLDS',' rank corr with truth',round(spearmanr(e79,rho)[0],2),' est',q(e79))
va=P('SCHOOL_VA')
verdict('E35 school fixed effects vs true VA gap', np.abs(g('E35')-va)<=.1, None)
verdict('E159 variance share vs VA share (within 2x)', (g('E159')<=2*g('VA_share'))&(g('E159')>=.5*g('VA_share')))
pt=P('PEER')/(P('PEER')+P('TOP_TEACH')); verdict('E36 linear-in-means peer vs true peer share', np.abs(g('E36')-pt)<=.1)
verdict('E152 fuzzy RD vs true school VA', np.abs(g('E152')-va)<=.1)
verdict('E32 value added with prior score', np.abs(g('E32')-va)<=.05)
verdict('E34 teacher effects (corr >= 0.7)', g('E34_corr')>=.7)
print('\nroutes: EO with art/HK',q(g('EO_with_routes')),' without',q(g('EO_no_routes')),' diff',q(g('EO_with_routes')-g('EO_no_routes')))
print('share of elite seats via art/HK',q(g('route_share_of_seats')),' tutoring take-up',q(g('tut_takeup')))
print('rank-rank E133',q(g('E133')),' concentration E131',q(g('E131')))
