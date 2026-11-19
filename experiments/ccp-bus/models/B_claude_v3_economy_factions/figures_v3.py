import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
import bus_v3 as W
S=['#2a78d6','#eb6834','#1baf7a','#eda100','#e87ba4','#008300','#6250d6','#e34948']
INK,INK2,GRID,SURF='#0b0b0b','#52514e','#e6e5e1','#fcfcfb'
plt.rcParams.update({'font.size':10,'axes.edgecolor':INK2,'axes.labelcolor':INK2,'xtick.color':INK2,'ytick.color':INK2,
  'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':GRID,'grid.linewidth':.6,
  'figure.facecolor':SURF,'axes.facecolor':SURF,'lines.linewidth':2,'legend.frameon':False,'axes.titlesize':11,'axes.titleweight':'bold','axes.titlecolor':INK})
pct=matplotlib.ticker.PercentFormatter(1,decimals=0); D=W.V.DATA

# Fig 5 economic engine
fig,ax=plt.subplots(1,3,figsize=(13,3.8))
sc={'Land flat (muddle through)':W.Scenario3(),'Land keeps falling':W.Scenario3(land_growth=-0.08,land_floor=1.5)}
for (n,s_),c,ls in zip(sc.items(),[S[0],S[1]],['-','--']):
    e=W.economy(s_); ax[0].plot(e.index[e.index>=2025],e.land_pct[e.index>=2025],ls,color=c,label=n,lw=1.6)
ax[0].plot(D.index,D.land_pct_gdp,color=INK,lw=2.2,label='Actual (MOF)'); ax[0].axvline(2025.5,color=INK2,lw=.7,ls=':')
ax[0].set(title='Land-sale revenue, % of GDP',xlabel='Year'); ax[0].legend(fontsize=8)
ax[1].plot(D.index,D.bis_credit_pct_gdp,color=INK,lw=2.2); ax[1].set(title='Total credit, % of GDP (BIS)',xlabel='Year')
ax[1].annotate('2009 stimulus',(2009,167),(2001,200),fontsize=8,color=INK2,arrowprops=dict(arrowstyle='-',color=INK2,lw=.7))
for (n,s_),c,ls in zip({'Defense +7%/yr':W.Scenario3(),'Defense +4%/yr':W.Scenario3(defense_growth=0.04),'+50% off-budget':W.Scenario3(off_budget=1.5)}.items(),[S[0],S[1],S[2]],['-','--',':']):
    e=W.economy(s_); ax[2].plot(e.index[e.index>=2025],e.equip_pct[e.index>=2025],ls,color=c,label=n,lw=1.6)
ax[2].plot(D.index,D.equip_pct_gdp,color=INK,lw=2.2,label='Actual (budget x equipment share)'); ax[2].axvline(2025.5,color=INK2,lw=.7,ls=':')
ax[2].set(title='PLA equipment procurement, % of GDP',xlabel='Year'); ax[2].legend(fontsize=7.5)
fig.tight_layout(); fig.savefig('figs/fig5_economy.png',dpi=170)

# Fig 6 hindcast
YRS=list(range(2013,2026)); obs=D.ccdi_cases_filed_10k; o=np.log(obs.loc[YRS]/obs.loc[2018:2021].mean())
allr=pd.read_csv('abc_v3_C_rounds.csv'); pas=allr[allr.x2012.between(.05,.6)&(allr.rr_core_tgt<.3)&(allr.contagion_hr>=1.5)&(allr.hidden2025>=.1)&allr.p5.astype(bool)&(allr.political_share<.5)]
v3a=pd.read_csv('abc_v3_all.csv'); bestA=v3a[(v3a.model=='A')&v3a.x2012.between(.05,.6)].sort_values('dist').iloc[0]
bestK=v3a[(v3a.model=='K')&v3a.x2012.between(.05,.6)].sort_values('dist').iloc[0]
sims=pas[[f'sim{y}' for y in YRS]].to_numpy()
fig,ax=plt.subplots(figsize=(7.6,4))
ax.fill_between(YRS,np.exp(np.quantile(sims,.1,0)),np.exp(np.quantile(sims,.9,0)),color=S[0],alpha=.18,lw=0,label='C: memory + factions, 10–90% of fits')
ax.plot(YRS,np.exp(np.median(sims,0)),color=S[0],label='C: median')
ax.plot(YRS,np.exp([bestA[f'sim{y}'] for y in YRS]),color=S[1],ls='--',lw=1.6,label='A: no memory, best fit')
ax.plot(YRS,np.exp([bestK[f'sim{y}'] for y in YRS]),color=S[2],ls=':',lw=1.8,label='K: capacity only, best fit')
ax.plot(YRS,np.exp(o),'o',color=INK,ms=5,label='Actual CCDI cases filed')
ax.set(title='Hindcast: discipline cases relative to 2018–21 average',xlabel='Year',ylabel='Cases ÷ 2018–21 mean'); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig('figs/fig6_hindcast.png',dpi=170)

# Fig 7 predictors of arrest
acc=pas
fig,ax=plt.subplots(1,2,figsize=(10,3.7))
names=['Faction status','Actually corrupt','Low in-faction degree']; cols=['auc_faction','auc_corrupt','auc_degree']
q=acc[cols].quantile([.1,.5,.9])
ax[0].bar(range(3),q.loc[.5],color=S[0],width=.55,yerr=[q.loc[.5]-q.loc[.1],q.loc[.9]-q.loc[.5]],ecolor=INK2,capsize=3)
ax[0].axhline(.5,color=INK2,lw=.8,ls='--'); ax[0].set_xticks(range(3),names,fontsize=9); ax[0].set_ylim(.4,.8)
ax[0].set(title='What predicts removal, 2013–2025 (AUC)',ylabel='AUC (0.5 = no better than chance)')
rr=acc[['rr_tgt_vs_rest','rr_corrupt']].quantile([.1,.5,.9])
ax[1].bar(range(2),rr.loc[.5],color=S[0],width=.5,yerr=[rr.loc[.5]-rr.loc[.1],rr.loc[.9]-rr.loc[.5]],ecolor=INK2,capsize=3)
ax[1].set_xticks(range(2),['In a targeted faction\nvs not','Corrupt\nvs clean'],fontsize=9); ax[1].set(title='Relative risk of removal',ylabel='× more likely')
fig.tight_layout(); fig.savefig('figs/fig7_predictors.png',dpi=170)

# Fig 8 faction life cycle (succession scenario)
sc=pd.read_csv('scenarios_v3.csv'); s8=sc[sc.scenario.str.startswith('Succession')]
g=s8.groupby('year')[['n_core','n_adjacent','n_targeted','n_unaffiliated','hidden_share']].median()
N=2500
fig,ax=plt.subplots(figsize=(8.6,4))
for c_,lab,col in [('n_core','Leader\'s core network',S[0]),('n_adjacent','Leader-adjacent cliques',S[1]),('n_targeted','Targeted factions',S[7]),('n_unaffiliated','Unaffiliated',INK2)]:
    ax.plot(g.index,g[c_]/N,color=col,label=lab)
ax.plot(g.index,g.hidden_share,color=S[2],ls='--',label='Share of ties hidden')
for yv,t in [(2013,'Xi takes over'),(2032,'Succession (scenario)')]:
    ax.axvline(yv,color=INK2,lw=.7,ls=':'); ax.text(yv+.3,.93,t,fontsize=8,color=INK2)
ax.yaxis.set_major_formatter(pct); ax.set_ylim(0,1); ax.set(title='Faction life cycle (median of fitted runs)',xlabel='Year',ylabel='Share of officials / ties')
ax.legend(fontsize=8,loc='center left',bbox_to_anchor=(1,.5)); fig.tight_layout(); fig.savefig('figs/fig8_faction_cycle.png',dpi=170)

# Fig 9 scenarios
order=list(dict.fromkeys(sc.scenario)); fig,ax=plt.subplots(1,2,figsize=(11,4))
for n,c in zip(order,S):
    gg=sc[(sc.scenario==n)&(sc.year>=2018)].groupby('year')[['x','pred_share']].median()
    ax[0].plot(gg.index,gg.x,color=c,label=n,lw=1.8); ax[1].plot(gg.index,gg.pred_share,color=c,lw=1.8)
for a in ax: a.axvline(2025.5,color=INK2,lw=.7,ls=':'); a.yaxis.set_major_formatter(pct)
ax[0].set(title='Corrupt share of civilian officials',xlabel='Year'); ax[1].set(title='Share of corruption that is predatory (fines, seizures)',xlabel='Year')
h,l=ax[0].get_legend_handles_labels(); fig.legend(h,l,loc='lower center',ncol=3,fontsize=8); fig.tight_layout(rect=(0,.12,1,1)); fig.savefig('figs/fig9_scenarios.png',dpi=170)
print('ok', len(pas),'pattern-passing fits')

# Fig 10 PLA under procurement scenarios
fig,ax=plt.subplots(figsize=(7.8,3.9))
for n,c,ls in [('Muddle through: land flat, credit rollover',S[0],'-'),('Defense growth slows to 4% a year',S[1],'--'),('Off-budget procurement adds 50%',S[2],':')]:
    gg=sc[sc.scenario==n].groupby('year').x_pla.median(); ax.plot(gg.index,gg.values,ls,color=c,label=n.replace(': land flat, credit rollover',' (defense +7%/yr)'),lw=1.9)
ax.axvspan(2023,2026,color=GRID,alpha=.6,lw=0); ax.text(2023.2,ax.get_ylim()[1]*0.92,'2023-26 purge',fontsize=8,color=INK2)
ax.yaxis.set_major_formatter(pct); ax.set(title='PLA corruption tracks procurement money (median of fits)',xlabel='Year',ylabel='Corrupt share, PLA officials'); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig('figs/fig10_pla.png',dpi=170)
