"""What the engine does and does not model, against the EFA / MDG / SDG 4 indicator frame.

Counts of observations come from the ledger (eduengine.ledger.OBS), so the table cannot drift from the code.
Out-of-sample figures are copied from results/TUNING_REPORT.md (3 evaluation seeds, anchors to 2015, tested after 2015).

status:
  scored      the engine produces it from its mechanism and it is scored against data
  fed         the engine is given the data as an input (anchoring), so a match is not a test until the anchor stops
  produced    the engine computes it but nothing is scored against data yet
  absent      not in the model
"""
from collections import Counter
from eduengine import ledger as LG

OOS = dict(  # TUNING_REPORT.md, original parameters
    anchored=dict(cambodia=(9.3, 15, 4.3), philippines=(6.7, 8, 5.0), china=(7.3, 12, 9.3)),     # passing, rows, completion MAE (pts)
    mechanism=dict(cambodia=(6.0, 15, 11.7), philippines=(3.0, 8, 10.5), china=(10.3, 12, 4.7)),
)


def _n(instr=None, ind_prefix=None):
    out = Counter()
    for o in LG.OBS:
        if (instr and o['instrument'] != instr) or (ind_prefix and not o['indicator'].startswith(ind_prefix)):
            continue
        out[o['country']] += 1
    return {c: out.get(c, 0) for c in ('cambodia', 'philippines', 'china')}


ROWS = [
    # (frame, indicator, status, what the engine does, caveat)
    dict(frame='MDG 2 · EFA 2 · SDG 4.1.2', name='Completion rate: primary, lower and upper secondary', status='fed', n=_n('completion_cohort'),
         how='Each simulated child decides grade by grade whether to continue (cost, income, belief about pay-off, exam gates). Quantity is steered to the UNESCO completion series up to the anchor year; after it, the mechanism decides.',
         caveat='Before the anchor stops, matching UNESCO is an input, not a test. After 2015, with anchors stopped, completion lands within about 4 to 9 points (Cambodia 4.3, Philippines 5.0, China 9.3). With no anchors at all: 5 to 12 points off.'),
    dict(frame='MDG 2 · EFA 2 · SDG 4.1.4', name='Out-of-school rate (primary and lower-secondary age)', status='scored', n=_n('oos_admin'),
         how='Counts children of each age not enrolled; reported twice, as a school census would (enrolled over population) and as a household survey would.',
         caveat='Observed only for Cambodia, from volatile UNESCO series. Not scored for the Philippines or China.'),
    dict(frame='EFA 2 · MDG 2.1', name='Net and gross enrolment ratios; gross intake ratio', status='produced', n=dict(cambodia=0, philippines=0, china=0),
         how='Enrolment by grade and year is recorded in full; a gross-intake measure exists and responds to population under-counts.',
         caveat='No enrolment-ratio observations are in the ledger yet, so none is scored. Adding UIS net and gross ratios is a data-entry job.'),
    dict(frame='EFA 2 · MDG 2.2 · SDG 4.1', name='Dropout, survival to last grade, repetition', status='produced', n=dict(cambodia=0, philippines=0, china=0),
         how='Every child has an exit year and an exit reason (cost, income need, exam failure, gate); repeated years are counted.',
         caveat='Recorded but not scored: no survival-rate or repetition observations in the ledger.'),
    dict(frame='SDG 4.1.1 · 4.6.1 · EFA 4', name='Learning and literacy', status='produced', n=dict(cambodia=0, philippines=0, china=0),
         how='Skill accumulates with years of effective schooling and teacher effort; youth literacy is read off a threshold, with the measuring-instrument error modelled separately.',
         caveat='Not scored against any assessment. Adult literacy (EFA 4) is not modelled: the engine follows youth cohorts.'),
    dict(frame='EFA 5 · MDG 3 · SDG 4.5.1', name='Gender parity', status='absent', n=dict(cambodia=0, philippines=0, china=0),
         how='Children have no sex in the model.', caveat='A real gap for EFA and MDG 3 reporting. Wealth parity (poorest over richest fifth) is produced but not scored.'),
    dict(frame='SDG 4.5.1', name='Wealth parity in completion', status='produced', n=dict(cambodia=0, philippines=0, china=0),
         how='Completion by household income fifth, poorest over richest.', caveat='No observed parity series entered yet (DHS/MICS/WIDE extracts needed).'),
    dict(frame='EFA 1 · SDG 4.2', name='Early childhood and pre-primary', status='absent', n=dict(cambodia=0, philippines=0, china=0),
         how='The model starts at primary entry.', caveat='China\'s 14th Plan reports preschool enrolment of 92%; the engine cannot speak to it.'),
    dict(frame='SDG 4.3', name='Tertiary participation', status='produced', n=dict(cambodia=0, philippines=0, china=0),
         how='China: gaokao quotas ration university places; other packs use fee and fiscal paths.', caveat='No tertiary enrolment ratios are scored yet.'),
    dict(frame='SDG 4.c', name='Teachers and pupil-teacher ratio', status='produced', n=dict(cambodia=0, philippines=0, china=0),
         how='Teachers = salary budget over pay (or hired to a planning norm if switched on); the pupil-teacher ratio follows.',
         caveat='Not scored against UNESCO teacher data. The planning kernel checks the arithmetic, not the behaviour.'),
    dict(frame='Financing', name='Public and household spending', status='produced', n=dict(cambodia=0, philippines=0, china=0),
         how='Public budget per child is a coded path; household spending (fees, tutoring, private school) is computed.',
         caveat='Budget paths are inputs. Spending shares are not scored.'),
    dict(frame='Private provision', name='Private-school share', status='scored', n=_n('private_share'),
         how='Private schools grow where public seats are rationed or families can pay for differentiation.',
         caveat='Philippines secondary share is the known miss (about 13% modelled vs 24% observed).'),
    dict(frame='Shadow education (Bray)', name='Share paying for private tutoring', status='scored', n={c: _n('tutoring_broad')[c] + _n('tutoring_narrow')[c] for c in ('cambodia', 'philippines', 'china')},
         how='Own-teacher tutoring from the teacher pay gap, commercial tutoring from exam stakes; price, channel and who pays all come from the mechanism.',
         caveat='Few survey observations per country (2 to 4); some are flagged unverified. China before 2016 is not pinned by data.'),
    dict(frame='Labour market', name='Graduate queuing / youth unemployment', status='scored', n=_n('youth_unemployment'),
         how='Formal jobs by tier; degree holders wait in a queue (Harris-Todaro logic); tutoring firms employ graduates; a ban shrinks those jobs.',
         caveat='China only, two stylised observations, excluded from parameter selection. The engine measures graduates waiting, not the official survey definition, and the level is not credible; read changes and rankings. Field-of-study mismatch is not modelled.'),
    dict(frame='Labour market', name='Employment type and wages by credential', status='produced', n=dict(cambodia=0, philippines=0, china=0),
         how='Formal rate, informal wage, premium by credential are computed each year.',
         caveat='The Cambodia Labour Force Survey 2019 (6.6% of employed hold a university degree; 88.3% informal) is sourced but not yet entered as an observation.'),
]


def build():
    rows = []
    for r in ROWS:
        r = dict(r); r['n_total'] = sum(r['n'].values()); rows.append(r)
    counts = Counter(r['status'] for r in rows)
    return dict(rows=rows, counts=dict(counts), total=len(rows), oos=OOS,
                observations=sum(1 for o in LG.OBS if o['country'] in ('cambodia', 'philippines', 'china')), other_observations=sum(1 for o in LG.OBS if o['country'] not in ('cambodia', 'philippines', 'china')),
                by_country={c: sum(1 for o in LG.OBS if o['country'] == c) for c in ('cambodia', 'philippines', 'china')},
                source='results/TUNING_REPORT.md; counts from eduengine.ledger.OBS')
