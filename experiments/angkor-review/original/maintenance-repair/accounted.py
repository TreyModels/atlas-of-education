"""Separate exploratory extension. kg grain, people, person-days, annual steps.
No historical calibration. Service rations replace household rations, never add mouths.
The refuge has its own harvest, seed, storage, consumption and demographic account.
"""
from dataclasses import dataclass
import random, math

@dataclass
class Settings:
    regime: str = 'stable'
    drought: bool = False
    seed: int = 0
    years: int = 110
    communities: int = 24
    maintenance_factor: float = .35
    military_share: float = .08
    monument_share: float = .04
    religion_share: float = .04
    refuge_yield: float = 2150.


def run(s):
    assert s.regime in ('stable','maintenance_only','reshuffle')
    assert s.communities >= 0 and s.years >= 0
    assert all(0<=v<=1 for v in (s.maintenance_factor,s.military_share,s.monument_share,s.religion_share))
    rng=random.Random(s.seed)
    villages=[dict(n=400.,store=12000.,temple=15000.,court=0.,elite=0.,canal=.85,trust=.75) for _ in range(s.communities)]
    refuge=ref_store=0.
    history=[]
    for year in range(s.years):
        active=year>=55 and s.regime!='stable'
        reshuffle=active and s.regime=='reshuffle'
        weather=rng.uniform(.92,1.08)*(.36 if s.drought and 65<=year<74 else 1.)
        opening_n=sum(c['n'] for c in villages)+refuge
        opening_grain=sum(c[k] for c in villages for k in ('store','temple','court','elite'))+ref_store
        births=deaths=harvest=seed_grain=consumption=spoilage=shortfall=flight=unpaid=0.
        work={k:0. for k in ('available','agriculture','military','irrigation','monuments','religion','administration','idle')}
        max_local_error=0.
        for c in villages:
            n=c['n']; available=n*.45*180
            maintenance=(.025+.055*(1-c['canal']))*(s.maintenance_factor if active else 1.)
            shares=dict(military=s.military_share,irrigation=maintenance,monuments=s.monument_share,religion=s.religion_share,administration=.015)
            assert sum(shares.values())<=1
            requested={k:available*v for k,v in shares.items()}
            farm_days=available*(1-sum(shares.values()))
            coverage=min(1.,farm_days/(110*162))
            gross=110*2150*weather*(.4+.6*c['canal'])*coverage
            # Seed retained from harvest is an explicit loss from edible stores.
            seed=min(gross,110*65); net=gross-seed
            harvest+=gross;seed_grain+=seed
            for k in ('store','temple','court','elite'):
                loss=.06*c[k];c[k]-=loss;spoilage+=loss
            tax=.25 if reshuffle else .16
            c['court']+=net*tax;c['temple']+=net*.16;c['elite']+=net*.07
            c['store']+=net*(1-tax-.16-.07)
            # Annual duty-days converted to ration-years. Paid service is a
            # transfer to resident workers, then consumed in their household account.
            bill=sum(requested.values())/365*280
            paid=min(c['court'],bill);funded=paid/bill if bill else 1.
            c['court']-=paid;c['store']+=paid;unpaid+=bill-paid
            actual={k:v*funded for k,v in requested.items()}
            idle=sum(requested.values())-sum(actual.values())
            error=available-farm_days-sum(actual.values())-idle
            max_local_error=max(max_local_error,abs(error));assert abs(error)<1e-7
            work['available']+=available;work['agriculture']+=farm_days;work['idle']+=idle
            for k,v in actual.items():work[k]+=v
            need=n*280;eaten=min(need,c['store']);c['store']-=eaten
            relief=min(need-eaten,c['temple']*(.30 if reshuffle else .95))
            c['temple']-=relief;eaten+=relief;consumption+=eaten
            gap=need-eaten;shortfall+=gap;deficit=gap/max(1,need)
            died=n*(.013+.19*deficit);born=n*.021*(1-deficit)
            grievance=max(0,tax+.16+.07-.29)
            fraction=min(.23,(.13*deficit+.032*grievance+.015*(1-c['trust']))*.92)
            moving=max(0,(n-died+born)*fraction)
            c['n']=n+born-died-moving;refuge+=moving;flight+=moving
            births+=born;deaths+=died
            c['trust']=max(0,min(1,c['trust']+(.012 if deficit<.02 else -.09*deficit)-.009*grievance-(.015 if reshuffle else 0)))
            effective=actual['irrigation']/available if available else 0
            repair=effective/.025*.018*min(1,c['n']/400)
            c['canal']=max(.3,min(1,c['canal']-.018+repair-(.06 if s.drought and year in (68,72) else 0)))
        # Refuge includes arrivals this year. Land caps at 3,575 ha, equivalent
        # to 13,000 people at the starting village land/person ratio. Capacity,
        # yield and shared weather exposure are declared experimental assumptions.
        land=min(3575.,refuge*110/400)
        ref_available=refuge*.45*180
        ref_farm=min(ref_available,land*162)
        ref_coverage=min(1,ref_farm/(land*162)) if land else 0
        ref_gross=land*s.refuge_yield*weather*.91*ref_coverage
        ref_seed=min(ref_gross,land*65)
        loss=ref_store*.06;spoilage+=loss
        ref_store=ref_store-loss+ref_gross-ref_seed
        ref_need=refuge*280;ref_eaten=min(ref_need,ref_store);ref_store-=ref_eaten
        harvest+=ref_gross;seed_grain+=ref_seed;consumption+=ref_eaten
        ref_gap=ref_need-ref_eaten;shortfall+=ref_gap
        deficit=ref_gap/max(1,ref_need)
        ref_died=refuge*(.013+.19*deficit);ref_born=refuge*.021*(1-deficit)
        refuge+=ref_born-ref_died;births+=ref_born;deaths+=ref_died
        work['available']+=ref_available;work['agriculture']+=ref_farm;work['idle']+=ref_available-ref_farm
        total=sum(c['n'] for c in villages)+refuge
        closing_grain=sum(c[k] for c in villages for k in ('store','temple','court','elite'))+ref_store
        grain_error=closing_grain-(opening_grain+harvest-seed_grain-consumption-spoilage)
        population_error=total-(opening_n+births-deaths)
        labour_error=work['available']-sum(v for k,v in work.items() if k!='available')
        assert abs(grain_error)<1e-6 and abs(population_error)<1e-6 and abs(labour_error)<1e-6
        assert all(c[k]>=-1e-7 for c in villages for k in ('n','store','temple','court','elite')) and min(refuge,ref_store)>=-1e-7
        row=dict(year=year,state_population=sum(c['n'] for c in villages),refuge_population=refuge,total_population=total,
                 canal_condition=sum(c['canal'] for c in villages)/len(villages) if villages else 0.,shortfall_kg=shortfall,
                 flight=flight,unpaid_service_kg=unpaid,births=births,deaths=deaths,harvest_kg=harvest,seed_kg=seed_grain,
                 consumed_kg=consumption,spoilage_kg=spoilage,grain_stock_kg=closing_grain,
                 grain_error=grain_error,population_error=population_error,labour_error=labour_error)
        row.update({k+'_days':v for k,v in work.items()});history.append(row)
    return history
