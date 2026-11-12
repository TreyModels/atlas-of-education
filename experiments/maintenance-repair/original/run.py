"""Minimal Angkor institutional maintenance stress-test, NOT calibrated history.
Derivative of angkor_scott_flight_v02.py. Fixed seeds, paired scenarios.
"""
from dataclasses import dataclass
from pathlib import Path
import sys,csv,random,statistics
sys.path.insert(0,str(Path(__file__).parent))
from angkor_scott_flight_v02 import Params,P

@dataclass
class Settings:
    disruption:bool=False
    maintenance_only:bool=False
    drought:bool=False
    seed:int=1
    years:int=110
    villages:int=24

def run(s):
    r=random.Random(s.seed)
    villages=[P() for _ in range(s.villages)]
    temple=[15000.0]*s.villages
    refugees=0.0
    cumulative_births=cumulative_deaths=0.
    history=[]
    for year in range(s.years):
        # Event years are exploratory scenario choices, not historical dates.
        shock=s.disruption and year>=55
        wet=.36 if s.drought and 65<=year<74 else 1.0
        weather=r.uniform(.92,1.08)*wet
        flight=0.0; hunger=0.0; births=0.0; deaths=0.0; produced=0.0
        for i,c in enumerate(villages):
            # Maintenance workers diverted from cultivation; more degraded canals need more labor.
            required_maintenance=.025+.055*(1-c.canal)
            effective_maintenance=required_maintenance*(.35 if (shock or s.maintenance_only) else 1.0)
            farming_labor=max(0.,1-.015-effective_maintenance)
            harvest=max(0.,110*2150*weather*(.4+.6*c.canal)*farming_labor-110*65)
            tax=.16+(.09 if shock else 0.0)
            temple_levy=.16
            elite_levy=.07
            household=harvest*(1-tax-temple_levy-elite_levy)
            prev=temple[i]*.94+harvest*temple_levy
            need=c.n*280
            stock=c.store*.94+household
            eaten=min(need,stock)
            stock-=eaten
            short=need-eaten
            relief=min(short,(.30 if shock else .95)*prev)
            short-=relief;prev-=relief
            c.store=stock;temple[i]=prev
            produced+=harvest;hunger+=short
            deficit=short/max(1,need)
            died=c.n*(.013+.19*deficit)
            born=c.n*.021*(1-deficit)
            grievance=max(0.,tax+temple_levy+elite_levy-.29)
            escape_fraction=min(.23,(.13*deficit+.032*grievance+.015*(1-c.trust))*.92)
            escaping=max(0.,(c.n-died+born)*escape_fraction)
            c.n=c.n-died+born-escaping
            refugees+=escaping;flight+=escaping
            births+=born;deaths+=died
            c.trust=max(0.,min(1.,c.trust+(.012 if deficit<.02 else -.09*deficit)-.009*grievance-(.015 if shock else 0)))
            repair=effective_maintenance/.025*.018*min(1.,c.n/400)
            c.canal=max(.3,min(1.,c.canal-.018+repair-(.06 if s.drought and year in (68,72) else 0)))
        # Refuge region is an independent demographic stock, not deaths/disappearance.
        excess=max(0.,refugees-13000)/13000
        ref_deaths=refugees*(.015+.06*min(2.,excess))
        ref_births=refugees*.02*(1-min(.8,excess*.45))
        refugees+=ref_births-ref_deaths
        births+=ref_births;deaths+=ref_deaths
        cumulative_births+=births;cumulative_deaths+=deaths
        state=sum(c.n for c in villages)
        total=state+refugees
        assert abs(total-(9600+cumulative_births-cumulative_deaths))<1e-5
        assert min(*(v.store for v in villages),*temple)>=-1e-6
        history.append(dict(year=year,angkor=state,refuge=refugees,total=total,
                            canal=statistics.mean(v.canal for v in villages),
                            shortage_kg=hunger,flight=flight,harvest=produced))
    return history

def main():
    out=Path(__file__).parent
    rows=[]
    for regime in ("stable","maintenance_only","reshuffle"):
        shock=(regime=="reshuffle")
        for drought in (False,True):
            for seed in range(40):
                series=run(Settings(disruption=shock,maintenance_only=(regime=="maintenance_only"),drought=drought,seed=seed))
                last=series[-1]
                rows.append(dict(scenario=f"{regime}_{'drought' if drought else 'normal'}",
                                 seed=seed,state_population=round(last['angkor'],2),refuge_population=round(last['refuge'],2),
                                 total_population=round(last['total'],2),canal_condition=round(last['canal'],3),
                                 cumulative_shortfall_kg=round(sum(p['shortage_kg'] for p in series)),
                                 cumulative_flight=round(sum(p['flight'] for p in series))))
    with (out/'runs.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    for scenario in dict.fromkeys(row['scenario'] for row in rows):
        sub=[x for x in rows if x['scenario']==scenario]
        print(scenario, {k:round(statistics.median(x[k] for x in sub),1) for k in ('state_population','refuge_population','total_population','canal_condition','cumulative_shortfall_kg')})
if __name__=='__main__': main()
