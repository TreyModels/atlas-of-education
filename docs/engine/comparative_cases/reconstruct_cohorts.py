"""Institutional timing benchmarks; synthetic equal cohorts, no fitted behaviour."""
from collections import Counter
from pathlib import Path
import json

def philippines(size=100):
    # Year denotes academic-year start. New SHS starts 2016; entry resumes 2018.
    # Cohorts indexed by counterfactual college-entry year under the old system.
    cohorts = [{'cohort': y, 'entry': y if y < 2016 else y + 2,
                'size': size, 'duration': 4} for y in range(2008, 2024)]
    return cohorts

def hong_kong(size=100):
    # Last old-system cohort enters in 2012. Following cohorts enter a year earlier.
    # Three-year old degrees coexist with four-year new degrees.
    return [{'cohort': y, 'entry': y if y <= 2012 else y - 1,
             'size': size, 'duration': 3 if y <= 2012 else 4,
             'track': 'old' if y <= 2012 else 'new'} for y in range(2005, 2024)]

def summarize(cohorts, years):
    entrants = Counter()
    for c in cohorts:
        entrants[c['entry']] += c['size']
    assert sum(entrants.values()) == sum(c['size'] for c in cohorts)
    return [{'year': y, 'entrants': entrants[y],
             'enrolled': sum(c['size'] for c in cohorts
                             if c['entry'] <= y < c['entry'] + c['duration'])}
            for y in years]

def admit_separate(applicants, capacities):
    return {track: min(n, capacities.get(track, 0)) for track, n in applicants.items()}

def main():
    ph = summarize(philippines(), range(2014, 2023))
    hk = summarize(hong_kong(), range(2010, 2017))
    p = {r['year']: r for r in ph}
    h = {r['year']: r for r in hk}
    assert [p[y]['entrants'] for y in (2015, 2016, 2017, 2018)] == [100, 0, 0, 100]
    assert [p[y]['enrolled'] for y in (2015, 2016, 2017, 2018, 2019, 2020, 2021)] == [400, 300, 200, 200, 200, 300, 400]
    assert h[2012]['entrants'] == 200
    assert h[2012]['enrolled'] == 400
    assert h[2013]['enrolled'] == 400
    assert admit_separate({'old': 20000, 'new': 10000}, {'old': 14500, 'new': 14500}) == {'old': 14500, 'new': 10000}
    observed = json.loads(Path(__file__).with_name('philippines_enrolment.json').read_text())
    for r in observed['observations']:
        assert r['public'] + r['private'] == r['total']
    result = {'status': 'all accounting checks passed',
              'assumptions': ['100 students in each synthetic cohort', 'all progress and enter university',
                              'no repeaters, dropouts, adult returners, early adopters or migration',
                              'fixed programme duration; unlimited capacity except separate-quota example'],
              'interpretation': 'Accounting checks only. No causal effect or historical fit estimated.',
              'philippines': ph, 'hong_kong': hk,
              'ched_total_change_2015_2017_pct': 100 * (observed['observations'][2]['total'] / observed['observations'][0]['total'] - 1),
              'ched_total_change_2017_2019_pct': 100 * (observed['observations'][4]['total'] / observed['observations'][2]['total'] - 1)}
    Path(__file__).with_name('cohort_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
