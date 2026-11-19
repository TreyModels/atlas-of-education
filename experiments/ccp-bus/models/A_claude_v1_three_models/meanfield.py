"""Mean-field (well-mixed) fixed points of the minimal bus model's choice core.
x = E_theta[ sigmoid((r - sigma*theta + h*x - F*D(x)) / tau) ],  theta ~ N(0,1)
D(x) = e * ((1-phi) + phi*(1-x)) * min(1, kappa/x)
Peer complementarity (h), reporting-by-honest-peers (phi; Andvig & Moene 1990) and
enforcement congestion (kappa; Lui 1986) are the three strategic complementarities."""
import numpy as np
GH_X,GH_W=np.polynomial.hermite_e.hermegauss(60); GH_W=GH_W/GH_W.sum()
def sig(z): return 1/(1+np.exp(-np.clip(z,-40,40)))
def detection(x,e,phi,kappa): return e*((1-phi)+phi*(1-x))*np.minimum(1,kappa/np.maximum(x,1e-9))
def rhs(x,p,e):
    D=detection(x,e,p['phi'],p['kappa'])
    z=(p['r']-p['sigma']*GH_X[None,:]+p['h']*x[:,None]-p['F']*D[:,None])/p['tau']
    return (sig(z)*GH_W).sum(axis=1)
def fixed_points(p,e,grid=np.linspace(1e-4,1-1e-4,4001)):
    g=rhs(grid,p,e)-grid; out=[]
    for i in np.flatnonzero(np.sign(g[:-1])!=np.sign(g[1:])):
        a,b=grid[i],grid[i+1]
        for _ in range(50):
            m=(a+b)/2
            if np.sign(rhs(np.array([m]),p,e)[0]-m)==np.sign(rhs(np.array([a]),p,e)[0]-a): a=m
            else: b=m
        x=(a+b)/2; eps=1e-5
        slope=(rhs(np.array([x+eps]),p,e)[0]-rhs(np.array([x-eps]),p,e)[0])/(2*eps)
        out.append((x,slope<1))
    return out
if __name__=='__main__':
    import itertools
    base=dict(r=0.6,sigma=1.0,tau=0.35,h=2.0,F=5.0,phi=0.6,kappa=0.10)
    for h,F,phi,kap in itertools.product([0,1.5,2.5],[4,6],[0,.6],[1,.08]):
        p=dict(base,h=h,F=F,phi=phi,kappa=kap)
        es=np.linspace(0,1,101); multi=[e for e in es if sum(s for _,s in fixed_points(p,e))>=2]
        print(f'h={h} F={F} phi={phi} kappa={kap}: bistable e-range',(round(min(multi),2),round(max(multi),2)) if multi else None)
