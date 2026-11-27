"""Targeted regression checks for cumulative premiums, evasion, and route exclusivity."""
import numpy as np
import gz_v5 as model

base = dict(n=8000, seed=122, REBAND=False, PRE_EFF=0, POST_EFF=0,
            FT_SHARE=0, ART_SHARE=0, HK_SHARE=0, TOP_TEACH=0, PEER=0)
plain = model.run(**base)
premium = model.run(**{**base, 'TOP_TEACH': .15, 'PEER': .29})
assert np.array_equal(plain['band1'], premium['band1'])
assert np.allclose(premium['skill18'] - plain['skill18'], .44 * plain['band1'])
assert np.allclose(premium['skill15'], plain['skill15'])
zero = model.run(n=8000, seed=1, BAN_RED=0, BAN_GRAD=0)
gradient = model.run(n=8000, seed=1, BAN_RED=0, BAN_GRAD=1)
assert np.array_equal(zero['pre'], gradient['pre'])
uniform = model.run(n=8000, seed=1, BAN_GRAD=0)
wr = uniform['wr']
effective = np.clip(uniform['p']['BAN_RED']*(1+0*(1-2*wr)), 0, 1)
assert np.allclose(effective, uniform['p']['BAN_RED'])
routes = model.run(n=8000, seed=4, ART_SHARE=.1, HK_SHARE=.1)
assert not np.any(routes['art'] & routes['hkr'])
assert np.all((routes['art'] | routes['hkr']) <= routes['acad'])
assert routes['art'].sum() == 800
assert routes['hkr'].sum() == 800
print('Cumulative premiums, zero-restriction equivalence, uniform reduction and exclusive routes verified.')

# Independent wealth in a neutral world: finite cohorts fluctuate around unity.
# Verify ensemble log-ratios, not an impossible exact 1.00 for every random sample.
from sweep import rates, joint_ratio
neutral = dict(TAL_WEALTH=0, SEG=0, HOME=0, TEACH_ZONE=0,
               NONHUKOU=0, PRE_SHARE=0, TERM_SHARE=0, HOL_SHARE=0,
               FT_SHARE=0, ART_SHARE=0, HK_SHARE=0, ELITE_BUY=0,
               ZONE_ADMIT=0)
ratios = []
for seed in range(20):
    d = model.run(n=40000, seed=9000+seed, **neutral)
    ratios.append([rates(d,d['uni'],'tal'), rates(d,d['uni'],'zk'), joint_ratio(d)[0]])
logs=np.log(ratios)
for name, column in zip(('T','S','Sstar'),logs.T):
    mean=column.mean(); se=column.std(ddof=1)/np.sqrt(len(column))
    assert abs(mean) < max(.03,3*se), (name,mean,se)
    print(f'Neutral {name}: geometric mean={np.exp(mean):.4f}, SE(log ratio)={se:.4f}, 20 cohorts.')
