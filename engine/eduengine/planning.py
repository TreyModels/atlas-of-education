"""The planning core: the education-planning flow model (the IIEP / UNESCO simulation-model tradition, e.g. EPSSim),
as plain functions. No behaviour, only arithmetic: what planners compute.

    flows(E, t)                    -> promotion, repetition, dropout rates by grade, measured from the agents in year t
    project(E0, intake, rates, n)  -> enrolment by grade for n years (the reconstructed-cohort identity)
    requirements(E, ptr, pay, ...) -> teachers, salary bill, total cost, funding gap
    closure(E)                     -> each year, how far the agents' enrolment is from what the planning identity
                                      predicts from last year's rates: the planning model as a check on the agent model

Identity (grade g, year t):  Enr[g,t+1] = Intake[t+1] (g=1) or Promoted[g-1,t]  +  Repeaters[g,t]
The staffing/cost equations are canonical in planning/kernel.cjs (JavaScript); calculate() and audit() below call it
through Node (read-only). flows/project/closure/plan_vs_agents are Python-side diagnostics, not yet mirrored in JS.
"""
import json, subprocess
from pathlib import Path
import numpy as np


def flows(E, t):
    """Rates by grade measured from year t to t+1: p (promoted), r (repeated), d (left), from the agent records."""
    R = E.R
    if t + 1 >= len(R['att_by_grade']):
        return None
    e0 = np.array(R['att_by_grade'][t], float)
    new1 = np.array(R['new_by_grade'][t + 1], float)          # entrants to each grade next year (not repeaters)
    e1 = np.array(R['att_by_grade'][t + 1], float)
    G = len(e0)
    promoted = np.zeros(G); repeated = np.zeros(G)
    promoted[:-1] = new1[1:]                                   # new entrants to grade g+1 came from grade g
    repeated = np.clip(e1 - new1, 0, None)                     # enrolled next year minus new entrants = repeaters
    with np.errstate(invalid='ignore', divide='ignore'):
        p = np.where(e0 > 0, promoted / e0, np.nan)
        r = np.where(e0 > 0, repeated / e0, np.nan)
    p, r = np.clip(np.nan_to_num(p), 0, 1), np.clip(np.nan_to_num(r), 0, 1)
    d = np.clip(1 - p - r, 0, 1)
    return dict(p=p, r=r, d=d, intake=float(new1[0]))


def project(E0, intake, rates, n):
    """Enrolment by grade for n years from E0, with fixed rates and a list (or scalar) of intakes."""
    E0 = np.asarray(E0, float); out = [E0]
    p, r = np.asarray(rates['p'], float), np.asarray(rates['r'], float)
    for k in range(n):
        e = out[-1]; nxt = r * e
        nxt[1:] += p[:-1] * e[:-1]
        nxt[0] += intake[k] if np.ndim(intake) else intake
        out.append(nxt)
    return np.array(out)


def requirements(enrol, ptr, pay, salary_share=0.8, budget=None):
    """Teachers needed at a pupil-teacher ratio, their salary bill, total cost, and the gap against a budget."""
    pupils = float(np.sum(enrol)); teachers = pupils / ptr
    salaries = teachers * pay; total = salaries / salary_share
    return dict(pupils=pupils, teachers=teachers, salary_bill=salaries, total_cost=total,
                gap=None if budget is None else total - budget)


def closure(E, grades=None):
    """Per year: relative error of the one-year planning projection against the agents' actual enrolment."""
    R = E.R; out = []
    for t in range(len(R['att_by_grade']) - 2):
        f = flows(E, t)
        if f is None:
            break
        e0 = np.array(R['att_by_grade'][t], float)
        pred = project(e0, f['intake'], f, 1)[1]
        act = np.array(R['att_by_grade'][t + 1], float)
        gi = slice(None) if grades is None else [g - 1 for g in grades]
        out.append(float(abs(pred[gi].sum() - act[gi].sum()) / max(act[gi].sum(), 1)))
    return out


def plan_vs_agents(E, Y0, Y1, ptr=None):
    """Freeze the agents' flow rates in Y0, project to Y1 the way a planner would, and compare with what the agents did."""
    y0 = E.p['start_year']; t0, t1 = Y0 - y0, Y1 - y0
    f = flows(E, t0)
    e0 = np.array(E.R['att_by_grade'][t0], float)
    intakes = [float(E.R['new_by_grade'][t][0]) for t in range(t0 + 1, t1 + 1)]
    proj = project(e0, intakes, f, t1 - t0)
    act = np.array([E.R['att_by_grade'][t] for t in range(t0, t1 + 1)], float)
    ptr = ptr or E.p.get('ptr_target', 35.0)
    return dict(years=list(range(Y0, Y1 + 1)), planned=proj.sum(1).tolist(), agents=act.sum(1).tolist(),
                teachers_planned=(proj.sum(1) / ptr).tolist(), teachers_agents=[float(E.R['teachers'][t]) for t in range(t0, t1 + 1)])


# --- Read-only bridge to the canonical JS kernel (Node 18+ needed only when called) ---
KERNEL=Path(__file__).resolve().parents[2]/'planning'/'kernel.cjs'
def calculate(operation, inputs):
    p=subprocess.run(['node',str(KERNEL)],input=json.dumps({'operation':operation,'inputs':inputs},allow_nan=False),text=True,capture_output=True,check=True,timeout=30)
    return json.loads(p.stdout)
def audit(E):
    """Compare observed public enrolment to target staffing and existing budget.
    Original wage units; simulated population only; excludes tertiary/private costs.
    Returns accounting diagnostics, not an empirical validation score.
    """
    fields=['pub_enrol','teacher_pay','pub_budget','teachers','ptr','q_pub']
    if any(k not in E.R for k in fields):raise ValueError('PublicSchools run required')
    inputs=[]
    for i,n in enumerate(E.R['pub_enrol']):
        inputs.append(dict(pupils=float(n),targetPTR=float(E.p['ptr_target']),salary=float(E.R['teacher_pay'][i]),
            operatingPerPupil=float(E.p['ops_need']),budget=float(E.R['pub_budget'][i])))
    results=calculate('resources',inputs)
    rows=[]
    for i,r in enumerate(results):
        actual=float(E.R['teachers'][i])
        rows.append(dict(year=int(E.p['start_year']+i),**r,engineTeachers=actual,
            teacherGap=r['teachersRequired']-actual,enginePTR=float(E.R['ptr'][i]),
            salaryIdentityResidual=actual*inputs[i]['salary']-float(E.p['salary_share'])*inputs[i]['budget']))
    return dict(kernel='atlas-planning-0.1',mode='read-only',units='simulated pupil counts; informal adult annual wage units',
        rows=rows,maximumSalaryIdentityResidual=max(abs(r['salaryIdentityResidual']) for r in rows),
        yearsBelowTargetStaffing=sum(r['teacherGap']>1e-9 for r in rows),
        empiricalImprovement='not evaluated; accounting audit does not alter predictions')
