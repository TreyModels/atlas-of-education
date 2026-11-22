#!/usr/bin/env python3
"""Build the separate results-led Philippine paper from final v5 outputs only."""
import json
from pathlib import Path

from make_report5 import f, markdown_block

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'PHL' / 'v5'
PAPER_DIR = ROOT.parent / 'manuscripts'


def main():
    scores = json.loads((OUT / 'scores.json').read_text())
    winner = scores['winner_by_preregistered_rule']
    recovery_path = OUT / f'recovery_{winner}.json'
    if not recovery_path.exists():
        raise SystemExit('Refusing to write final paper before winner recovery exists')
    recovery = json.loads(recovery_path.read_text())
    rivals = scores['rivals']
    w = rivals[winner]
    persistence = w['three_ger_rmse']['persistence']
    trend = w['three_ger_rmse']['trend']
    rmse = w['three_ger_rmse']['model']
    benchmark_text = (
        f"Its RMSE of {rmse:.3f} percentage points is worse than persistence ({persistence:.3f})"
        if rmse >= persistence else
        f"Its RMSE of {rmse:.3f} percentage points beats persistence ({persistence:.3f})"
    )
    if rmse >= min(persistence, trend):
        benchmark_text += f"; the best naive benchmark is therefore not beaten (trend: {trend:.3f})."
    else:
        benchmark_text += f" and linear trend ({trend:.3f})."
    mechanism = ''
    if winner == 'R2':
        mechanism = (
            f" Moreover, the selected specification's human-capital coefficient is {w['parameters']['b_h']:.3f}, "
            "at its lower bound. The statistical selection therefore cannot be read as evidence for a positive "
            "earnings-return mechanism."
        )
    L = [
        '# The Limits of Demand-Side Explanations of Educational Expansion', '',
        '## Rival Models, Historical Accounting, and the Philippine K-12 Transition', '',
        '**Trey Menefee**  ',
        '*Independent researcher*  ',
        '*November 2026 · Results-led working paper*', '',
        '## Abstract', '',
        'Why does educational participation continue to expand when the wage premium to the next credential falls? '
        'This paper turns that familiar theoretical question into an explicit comparison of six demand-side models '
        'for the Philippines. The models share cohort accounting and observed policy inputs but differ in whether '
        'participation responds to income, earnings returns, positional feedback, formal-economy thresholds, or '
        'saturation-dependent costs. Parameters are fitted to registered pre-1996 enrolment observations and '
        'declared household-spending targets, then scored on later observations. The test is retrospective and '
        'inspected, not blind. Under the registered three-GER selection rule, '
        f"**{winner}** has the lowest rival RMSE. {benchmark_text}{mechanism} The full positional-relational "
        'specification does not win, and the separating observations do not provide a consistent mechanism ranking. '
        'The paper therefore makes a deliberately limited contribution: it shows which theoretical ambitions the '
        'present evidence cannot sustain, while supplying a reproducible accounting and model-comparison framework '
        'for stronger tests. Status: **not calibrated**.', '',
        '**Keywords:** educational demand; massification; Philippines; K-12; model comparison; human capital; '
        'positional competition; credential thresholds; reproducibility', '',
        '## 1. A different question', '',
        'This is not a general theory of massification. It asks a narrower empirical question: when several '
        'demand-side explanations are required to reproduce the same historical observations, which survives '
        'comparison with its rivals and with naive benchmarks? The distinction matters. A model can reproduce a '
        'trend for the wrong reason, a theoretically preferred mechanism can lose to a simpler alternative, and '
        'the best member of a model set can still lose to carrying the last observation forward.', '',
        'The Philippine case is useful because it combines long enrolment series, uneven economic returns, household '
        'financing observations, and a dated structural break. The 2013 K-12 reform added senior secondary years; '
        'the first two cohorts did not feed directly into tertiary education, producing a sharp but temporary '
        'tertiary headcount contraction. The college premium used here falls from 0.88 to 0.59 log points between '
        '2013 and 2024, while tertiary gross enrolment rises from 31.870% to 47.413%. These observations discipline '
        'the models but do not, by themselves, identify causation.', '',
        'The analysis is organised around losses rather than theoretical preference. The preferred rival is selected '
        'only by the registered mean RMSE over primary, secondary, and tertiary GER in held-out years. Naive '
        'persistence and linear-trend rules are reported alongside every structural model. The result is a test of '
        'the implementations and data used here, not a once-and-for-all test of every human-capital, positional, or '
        'relational theory.', '',
        '## 2. A common accounting core with rival demand signals', '',
        'All six rivals use the same cohort engine. Children progress by age, grade, income decile, and sector; '
        'repetition, completion, deferred tertiary entry, policy costs, and cycle changes are explicit. This common '
        'structure prevents differences in bookkeeping from masquerading as differences in behaviour. The demand '
        'signal for level $L$, decile $d$, and year $y$ is', '',
        '$$', r'\begin{aligned}', 'U_{Ldy} ={}& \\alpha_L + b_h p_{Ly} + b_p S_{L,y-1} + b_r R_{Ly}',
        r' + \eta_x \log(I_{dy}/\bar I_y)', r' - \kappa A_{Ldy} \log(1+C_{Lsdy}/I_{dy}),', r'\end{aligned}', '$$', '',
        'where $p$ is the wage premium, $S$ is the previous credential stock, $R$ is the credential-threshold proxy, '
        '$I$ is decile income, and $C$ is direct plus forgone cost. Saturation-dependent affordability is '
        '$A_{Ldy}=\\exp(-\\lambda S_{L,y-1})$; R5 replaces $S$ with the threshold driver $R$. The rivals impose '
        'different restrictions on this common expression.', '',
        '| Rival | Demand account |', '|---|---|',
        '| R0 | Earlier income-sensitive benchmark: national income, decile income, and cost |',
        '| R1 | Full human-capital, positional, relational-threshold, and saturation-dependent-cost engine |',
        '| R2 | Human capital only; positional, threshold, and saturation feedback removed |',
        '| R3 | Full demand terms with constant rather than saturation-dependent cost sensitivity |',
        '| R4 | Full engine without positional feedback |',
        '| R5 | Cost sensitivity varies with the credential threshold rather than saturation |', '',
        'The threshold driver is exogenous in these runs. Aggregate timing cannot distinguish requirements causing '
        'enrolment from enrolment causing requirements. A stronger design would need occupational requirements '
        'measured before the enrolment changes.', '',
        '## 3. Registered design and evidence limits', '',
        'Training uses the registered 1971–1995 enrolment series plus declared APIS and early FIES targets. Test '
        'observations include post-1995 enrolment, CHED tertiary headcounts for 2016–2020, FIES 2012, and National '
        'Transfer Account household-financing shares. The unverified FIES 2023 row is excluded. The DepEd transition '
        'observation is 1,587,416 Grade 10 completers in SY2016–17 and 1,481,103 Grade 11 entrants in SY2017–18, '
        'or 93.3%; its reference year is 2018.', '',
        'For a series with $n$ scored observations, loss is', '',
        '$$', r'\operatorname{RMSE}=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i)^2}.', '$$', '',
        'GER errors are in percentage points. Lower is better. The protocol was written before the v5 fits and has '
        'no amendments. Computational continuation of an optimiser is not a change to targets, weights, or model '
        'rules. Nevertheless, the later observations had been inspected in earlier work: this is **not blind '
        'validation**.', '',
        '## 4. Results: the best rival still has serious losses', '',
        f"The registered winner is **{winner}**, with three-GER held-out RMSE **{rmse:.3f}**. {benchmark_text}",
        mechanism, '',
        '| Rival | Three-GER RMSE | RMSE minus R0 | Training cost | Evaluations | Bounds |',
        '|---|---:|---:|---:|---:|---|',
    ]
    for spec, v in rivals.items():
        evaluations = v.get('total_nfev', v['nfev'])
        stage_limit = 500 if v.get('total_nfev', v['nfev']) > v['nfev'] else 250
        cap = ' (last stage cap)' if v['nfev'] >= stage_limit else ''
        L.append(f"| {spec} | {v['three_ger_rmse']['model']:.3f} | {v['three_ger_rmse']['model_minus_R0']:.3f} | "
                 f"{v['train_cost']:.3f} | {evaluations}{cap} | {', '.join(v['at_bounds']) or 'none'} |")
    L += ['',
          f"For reference, persistence scores {persistence:.3f} and linear trend {trend:.3f} on the same GER rows. "
          'Training cost is not the selection criterion. A lower training cost can coexist with a worse held-out '
          'prediction, which is precisely why the two are separated.', '',
          '![Observed and predicted enrolment with held-out tests](figures/fit_and_test.png)', '',
          '### 4.1 The premium–participation contrast', '',
    ]
    sep = scores['separating_test_outcomes']
    tertiary = sep['tertiary_2013_2024']
    best_t = tertiary['supported_rival']
    L += [
        f"The lowest-error rival on the paired 2013 and 2024 tertiary observations is **{best_t}**, with RMSE "
        f"{tertiary['rmse'][best_t]:.3f} points. This is a descriptive separating test, not a causal estimate of "
        'the wage premium. The result is particularly important for interpretation: matching the direction of '
        'tertiary expansion is not sufficient to validate the mechanism that generated it.', '',
        '### 4.2 Recessions and the first senior-high transition', '',
    ]
    rec = sep['recession_secondary']
    trans = sep['grade10_to_grade11_2018']
    L += [
        f"The lowest-error recession prediction is **{rec['supported_rival']}** "
        f"(RMSE {rec['rmse'][rec['supported_rival']]:.3f}), using the observed years available in the registered "
        f"test set. The closest Grade 10→11 prediction is **{trans['supported_rival']}**, with transition-rate "
        f"RMSE {trans['rmse'][trans['supported_rival']]:.3f} points. No single mechanism sweeps these tests. "
        'Support for saturation-dependent cost sensitivity would require R1 to beat R3 both on recession behaviour '
        'and overall GER RMSE; that joint requirement is not established merely because one fit looks plausible.', '',
        '![Demand rival comparison](figures/demand_rivals.png)', '',
        '### 4.3 K-12 tertiary contraction and incomplete recovery', '',
        'All models reproduce a tertiary contraction around the first senior-high cohorts, but most understate the '
        'subsequent headcount recovery. The observed CHED index, with 2016 = 1, reaches 0.830 in 2020. This gap is '
        'substantive, not cosmetic: deferred entry and cohort accounting are not enough to recover the observed '
        'series under the fitted demand rules. The CHED transcription has not yet been independently rechecked '
        'against its original PDF because the source server is inaccessible; the table remains a declared QA '
        'limitation rather than a silently passed check.', '',
        '### 4.4 Household financing', '',
        'The models broadly reproduce the level and upward movement of the household share of total education '
        'spending, but aggregate fit again conceals errors. Financing shares are not per-student costs, and '
        'aggregate spending is not spending per pupil. These data constrain the cost scale; they do not identify '
        'why households value credentials.', '',
        '## 5. Synthetic recovery and identification', '',
        f"The recovery exercise uses 20 synthetic replicates around the selected fit with the declared Gaussian "
        f"noise design. Optimiser-cap replicates: **{recovery.get('optimizer_cap_replicates', 'not recorded')}**. "
        'The registered pass rule requires each relevant parameter to return within ±25% of a nonzero truth in at '
        'least 80% of replicates. Failure means **not identified** under this design, not zero effect.', '',
        '| Parameter | Truth | Recovered median | 5th–95th percentile | Within ±25% | Bound hits | Status |',
        '|---|---:|---:|---:|---:|---:|---|',
    ]
    for name, v in recovery['parameters'].items():
        if v['status'] == 'not in rival':
            L.append(f'| {name} | — | — | — | — | — | not in rival |')
        else:
            L.append(f"| {name} | {recovery['truth'][name]:.3f} | {v['median']:.3f} | {v['q05']:.3f} to {v['q95']:.3f} | "
                     f"{v['within_25pct_share']:.2f} | {v['bound_hit_replicates']} | **{v['status']}** |")
    failed = [name for name, v in recovery['parameters'].items()
              if v['status'] != 'not in rival' and not str(v['status']).startswith('identified')]
    boundary_note = ''
    if winner == 'R2':
        hits = recovery['parameters']['b_h']['bound_hit_replicates']
        boundary_note = (f" Although `b_h` meets the numerical recovery rule, it hits a bound in {hits}/20 "
                         "replicates. That is boundary recovery, not clean interior identification or evidence "
                         "for a positive effect.")
    L += ['',
          ('Failing parameters: **' + ', '.join(failed) + '**. ' if failed else 'No relevant parameter fails the registered recovery rule. ') +
          'Recovery from data generated by the same model is a minimum diagnostic. It does not establish '
          'identification from the real historical series, where model error and measurement error coexist.' +
          boundary_note, '',
          '## 6. What follows—and what does not', '',
          'Three conclusions are licensed. First, a common cohort-and-policy accounting structure can host sharply '
          'different demand explanations, making their comparative losses visible. Second, the present Philippine '
          'results do not justify elevating the full positional-relational engine above its rivals. Third, model '
          'selection among structural rivals is not enough: naive benchmarks, bound diagnostics, separating tests, '
          'and recovery all change the interpretation.', '',
          'Three stronger claims are not licensed. The exercise does not prove that earnings returns cause '
          'participation, that positional competition drives massification, or that occupational thresholds form '
          'an exogenous relational floor. Nor does it validate the model for forecasting or policy simulation. '
          'Its status remains **not calibrated**.', '',
          'The most useful next step is therefore not another narrative defence of a preferred mechanism. It is '
          'better measurement: consistent wage-premium series, original administrative headcounts, dated '
          'occupational requirements, and supply-capacity measures capable of distinguishing inaccessible seats '
          'from unwanted ones. The v6 fractional admissions work addresses the accounting side of that programme; '
          'it does not repair the demand-side identification failures reported here.', '',
          '## 7. Relation to the wider research programme', '',
          'The original massification manuscripts remain separate theoretical works. This paper does not recycle '
          'their argument with a new empirical appendix; it begins with comparative losses and accepts a negative '
          'result. A related credential-floor check points in the same cautious direction. In the China comparison, '
          'the observed raw change is −0.0387 and the cohort-adjusted change is −0.0531, whereas the human-capital, '
          'positional, and relational models predict positive median changes of 0.056, 0.068, and 0.078 '
          'respectively; no 10–90% interval crosses zero. Those credential-floor results must not be cited as '
          'support for the relational account.', '',
          'The paper also preserves distinctions developed in Mark Bray\'s work: household contributions reveal '
          'the full cost of schooling rather than proving independent household demand; remedial, enrichment, and '
          'examination-preparation tutoring are not interchangeable; and sample-specific tutoring rates are not '
          'national administrative accounts. These distinctions constrain interpretation rather than supplying a '
          'decorative literature review.', '',
          '## 8. Reproducibility and release status', '',
          'The bundle contains the registered protocol, exact dependencies, source and output hashes, fit and '
          'scoring scripts, recovery code, tests, figures, and fresh-copy comparison. Reproduction claims should '
          'be read from `outputs/qa/fresh_copy_comparison.json` and `outputs/qa/reproducibility_inputs.json`, not '
          'from the prose alone. Atlas Worlds release remains **NOT READY** while a source or computational QA '
          'gate is open. No Hong Kong extension is part of this paper.', '',
          '## Data and code availability', '',
          'The accompanying archive and draft pull request contain the complete MASSENG model and final Philippine '
          'v5 outputs. `PROTOCOL_v5.md` is authoritative for the design. `outputs/PHL/v5/scores.json` is '
          'authoritative for comparative results, and the recovery JSON is authoritative for recovery diagnostics.', '',
          '## References', '',
          'Bray, M. (1996). *Counting the Full Cost: Parental and Community Financing of Education in East Asia*. '
          'World Bank.', '',
          'Bray, M. (1999). *The Private Costs of Public Schooling: Household and Community Financing of Primary '
          'Education in Cambodia*. UNESCO-IIEP.', '',
          'Bray, M., & Kwok, P. (2003). Demand for private supplementary tutoring: Conceptual considerations and '
          'socio-economic patterns in Hong Kong. *Economics of Education Review, 22*(6), 611–620.', '',
          'Bray, M., Kobakhidze, M. N., Liu, J., & Zhang, W. (2016). The internal dynamics of privatised public '
          'education: Fee-charging supplementary tutoring provided by teachers in Cambodia. *International '
          'Journal of Educational Development, 49*, 291–299.', '',
          'Zhan, S., Bray, M., Wang, D., Lykins, C., & Kwo, O. (2013). The effectiveness of private tutoring: '
          'Students’ perceptions in comparison with mainstream schooling in Hong Kong. *Asia Pacific Education '
          'Review, 14*, 495–509.', '',
          '---', '',
          '# Appendix: complete generated result tables', '',
    ]
    L += markdown_block(scores, recovery)
    PAPER_DIR.mkdir(parents=True, exist_ok=True)
    path = PAPER_DIR / 'Philippine_demand_rivals.md'
    path.write_text('\n'.join(L) + '\n')
    print(path)


if __name__ == '__main__':
    main()
