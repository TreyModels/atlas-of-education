"""Design-phase diagnostic (not a deliverable). Prints the PHL-like series and regime counts."""
import numpy as np, sys
sys.path.insert(0, ".")
import sim_v1 as S

res = S.run_all()
r = res[0]
Y = S.YEARS
def show(name, arr, yrs):
    print(name)
    for y in yrs:
        i = int(np.where(Y == y)[0][0])
        print(f"   {y}: " + "  ".join(f"{v:.2f}" for v in np.atleast_1d(arr[..., i])))
print("=== PHL completion")
for L, nm in enumerate(S.LEVELS):
    print(nm, " ".join(f"{y}:{r['comp'][L][Y==y][0]:.1f}" for y in (1970,1985,1999,2010,2013,2017,2021,2024,2025)))
print("=== PHL GER")
for L, nm in enumerate(S.LEVELS):
    print(nm, " ".join(f"{y}:{r['ger'][L][Y==y][0]:.1f}" for y in (1971,1990,1999,2010,2016,2018,2021,2024,2025)))
print("=== PHL surv")
for L, nm in enumerate(S.LEVELS):
    print(nm, " ".join(f"{y}:{r['surv'][L][Y==y][0]:.2f}" for y in (1970,1990,1999,2010,2017,2021,2024)))
print("=== PHL states")
for y in (1970,1990,2000,2010,2017,2024,2025):
    i = int(np.where(Y == y)[0][0])
    print(f"  {y}: X={r['X'][i]:.3f} Y={r['Y'][i]:.0f} lit={r['lit'][i]:.3f} T={r['Tstate'][i]} "
          f"sec={np.round(r['sec'][:,i],3)} g={r['g'][i]*100:.2f} yos={r['yos'][i]:.2f} "
          f"form={r['E'][:,i].sum()/(0.52*r['Pop'][i]):.3f}")
print("=== PHL queues (millions) and wages")
for y in (1970,1990,2010,2024):
    i = int(np.where(Y == y)[0][0])
    print(f"  {y}: q={np.round(r['queue_r'][:,i]/1e6,4)} tot={r['queue_tot'][i]/1e6:.4f} "
          f"J={np.round(r['J'][:,i]/1e6,4)} E={np.round(r['E'][:,i]/1e6,4)} "
          f"w_inf={r['w_inf'][i]:.2f} w_for={np.round(r['w_for'][:,i],2)}")
print("=== regime counts by decade")
for d in range(1970, 2030, 10):
    m = (Y >= d) & (Y <= min(d+9, 2025))
    if m.sum() < 3: continue
    cnt = np.zeros(3, int)
    for rr in res:
        cnt[int(np.bincount(rr["Tstate"][m], minlength=3).argmax())] += 1
    print(f"  {d}s: pre={cnt[0]} ind={cnt[1]} div={cnt[2]}")
g = np.array([rr["g"].mean()*100 for rr in res])
print(f"growth across countries: mean {g.mean():.2f} sd {g.std():.2f} min {g.min():.2f} max {g.max():.2f}")
