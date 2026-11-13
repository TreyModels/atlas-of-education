"""Stylized Angkor/Scott state-evasion mechanism experiment, v0.2.
This is NOT historical calibration. Persons are tracked across polities/refuge,
with food storage and demographic accounting at annual time steps.
"""
from dataclasses import dataclass
import random, csv, argparse, statistics, json

@dataclass
class P:
    n: float = 400.0
    store: float = 12000.0
    trust: float = .75
    canal: float = .85

@dataclass
class Params:
    years:int=110
    communities:int=24
    initial_refuge:float=0
    tax:float=.16
    temple_levy:float=.16
    elite_levy:float=.07
    relief_share:float=.75
    drought:bool=True
    exit_cost:float=.22 # fraction of potential flight stopped by physical costs
    defense_work:float=.035 # annual fraction farming lost to fortification/guards
    recapture_rate:float=.018 # fraction of refugees subject to recapture yearly
    relief_on:bool=True
    seed:int=1

def run(s):
    r=random.Random(s.seed)
    communities=[P() for _ in range(s.communities)]
    refuge=float(s.initial_refuge)
    temple_stores=[15000.0 for _ in communities]
    court_store=0.0
    stats=[]; cumulative_deaths=0.; cumulative_births=0.; cumulative_flight=0.; cumulative_recaptures=0.
    for y in range(s.years):
        drought=.36 if s.drought and 65<=y<74 else 1.
        weather=r.uniform(.92,1.08)*drought
        deaths=0.; births=0.; flight=0.; unmet=0.; captured=0.; food_produced=0.; service_labor=0.
        next_refuge=refuge
        for idx,c in enumerate(communities):
            # Each village is locally bounded; temple has a distinct stored reserve.
            labor_fraction=max(.0,1.-s.defense_work)
            yield_kg=110*2150*weather*(.4+.6*c.canal)*labor_fraction
            seed=110*65
            harvest=max(0.,yield_kg-seed)
            court=s.tax*harvest
            temple=s.temple_levy*harvest
            elite=s.elite_levy*harvest
            household=harvest-court-temple-elite
            # Court extraction is modeled as consumed by state services & defense,
            # never as fictitious food available to villagers.
            court_store+=court
            prev_temple=temple_stores[idx]*.94
            support_budget=prev_temple+temple
            # Only a discretionary share of the actual available temple grain is usable.
            need=c.n*280
            household_stock=c.store*.94+household
            household_eaten=min(need,household_stock)
            household_stock-=household_eaten
            short=max(0.,need-household_eaten)
            support=min(short,s.relief_share*support_budget) if s.relief_on else 0.
            support_budget-=support
            short-=support
            c.store=household_stock
            temple_stores[idx]=support_budget
            unmet+=short
            food_produced+=harvest
            d=short/max(1.,need)
            # Deaths, births and outmigration are separate and cannot create people.
            death_rate=.013+.19*d
            b_rate=.021*(1-d)
            died=c.n*death_rate
            born=c.n*b_rate
            # Bounded exit: even food-secure households can flee predatory claims.
            grievance=max(0.,s.tax+s.temple_levy+s.elite_levy-.29)
            flight_prop=min(.23,(.13*d+.032*grievance+.015*(1-c.trust))*(1-s.exit_cost))
            escaping=max(0.,(c.n-died+born)*flight_prop)
            c.n=max(0.,c.n-died+born-escaping)
            next_refuge+=escaping
            flight+=escaping
            deaths+=died
            births+=born
            c.trust=max(0.,min(1.,c.trust+(.012 if d<.02 else -.09*d)-.009*grievance))
            # Channel decline and maintenance. Scarcity of labor after flight affects repairs.
            repairs=.02*min(1.,c.n/400)
            c.canal=max(.3,min(1.,c.canal-.018+repairs-(.06 if s.drought and y in (68,72) else 0)))
        # Refuge is not empty wilderness; subsistence capacity is bounded.
        # Density increases deaths; local birth rates remain positive at low population.
        refuge_carry=13000.
        excess=max(0.,next_refuge-refuge_carry)/refuge_carry
        ref_deaths=next_refuge*(.015+.06*min(2.,excess))
        ref_births=next_refuge*.020*(1-min(.8,excess*.45))
        next_refuge=max(0.,next_refuge-ref_deaths+ref_births)
        deaths+=ref_deaths; births+=ref_births
        # Recapture is probabilistic return to bonded labor, not creation or disappearance.
        taken=min(next_refuge,next_refuge*s.recapture_rate*r.uniform(.7,1.3))
        next_refuge-=taken
        for c in communities:
            c.n+=taken/len(communities)
        refuge=next_refuge
        cumulative_deaths+=deaths; cumulative_births+=births
        cumulative_flight+=flight; cumulative_recaptures+=taken
        stats.append(dict(year=y,angkor_pop=sum(c.n for c in communities),refuge_pop=refuge,
                          total_pop=sum(c.n for c in communities)+refuge,
                          unmet_kg=unmet,flight=flight,recaptured=taken,
                          canal=sum(c.canal for c in communities)/len(communities),
                          temple_stock=sum(temple_stores),court_grain=court_store,
                          harvest=food_produced,births=births,deaths=deaths,
                          cumulative_births=cumulative_births,cumulative_deaths=cumulative_deaths,
                          cumulative_flight=cumulative_flight,cumulative_recaptured=cumulative_recaptures))
        expected=400*s.communities+s.initial_refuge+cumulative_births-cumulative_deaths
        assert abs(stats[-1]['total_pop']-expected)<1e-5,(stats[-1]['total_pop'],expected)
        assert min(*(c.store for c in communities),*temple_stores,court_store)>=-1e-5
    return stats

SCENARIOS={
    'redistribution_open':dict(relief_share=.95,exit_cost=.08,defense_work=.015,recapture_rate=.005),
    'extraction_open':dict(relief_share=.25,exit_cost=.08,defense_work=.015,recapture_rate=.005),
    'extraction_fortified':dict(relief_share=.25,exit_cost=.70,defense_work=.11,recapture_rate=.06),
    'redistribution_fortified':dict(relief_share=.95,exit_cost=.70,defense_work=.11,recapture_rate=.06),
}

def experiment(n=30):
    rows=[]
    for scenario,overrides in SCENARIOS.items():
        for seed in range(n):
            series=run(Params(seed=seed,**overrides))
            last=series[-1]
            rows.append(dict(scenario=scenario,seed=seed,angkor_pop=round(last['angkor_pop'],1),
                             refuge_pop=round(last['refuge_pop'],1),total_pop=round(last['total_pop'],1),
                             famine_kg=round(sum(x['unmet_kg'] for x in series)),
                             cumulative_flight=round(last['cumulative_flight']),
                             cumulative_recaptured=round(last['cumulative_recaptured']),
                             canal=round(last['canal'],3),year_74_angkor=round(series[74]['angkor_pop'],1)))
    return rows

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',type=int,default=30);ap.add_argument('--output',default='angkor_scott_results.csv')
    a=ap.parse_args();rows=experiment(a.seeds)
    with open(a.output,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    for name in SCENARIOS:
        subset=[row for row in rows if row['scenario']==name]
        print(name, {field:round(statistics.median(row[field] for row in subset),1) for field in ('angkor_pop','refuge_pop','total_pop','cumulative_flight','cumulative_recaptured','famine_kg')})
