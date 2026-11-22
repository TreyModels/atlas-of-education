#!/usr/bin/env python3
"""Generate the PHL v5 loss-first report from final JSON outputs only."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'PHL' / 'v5'


def f(value, digits=3):
    if value is None or not math.isfinite(value):
        return '—'
    return f'{value:.{digits}f}'


def markdown_block(scores, recovery=None):
    rivals = scores['rivals']
    winner = scores['winner_by_preregistered_rule']
    r0 = rivals['R0']['three_ger_rmse']['model']
    persistence = rivals[winner]['three_ger_rmse']['persistence']
    trend = rivals[winner]['three_ger_rmse']['trend']
    L = [
        '## PHL v5 — retrospective rival test', '',
        '**Losses first. Status: not calibrated. This was a retrospective, inspected test, not a blind validation.**', '',
        f"The pre-registered winner is **{winner}**, with three-GER held-out RMSE **{f(rivals[winner]['three_ger_rmse']['model'])}**. "
        f"R0 is **{f(r0)}**, persistence **{f(persistence)}**, and linear trend **{f(trend)}**. "
        'Lower is better; selection uses the three GERs only, not training cost.', '',
        '| rival | three-GER RMSE | minus R0 | persistence | trend | training cost | evaluations | at bounds |',
        '|---|---:|---:|---:|---:|---:|---:|---|',
    ]
    for spec, v in rivals.items():
        g = v['three_ger_rmse']
        evaluations = v.get('total_nfev', v['nfev'])
        stage_limit = 500 if v.get('total_nfev', v['nfev']) > v['nfev'] else 250
        cap = ' (last stage cap)' if v['nfev'] >= stage_limit else ''
        L.append(f"| {spec} | {f(g['model'])} | {f(g['model_minus_R0'])} | {f(g['persistence'])} | {f(g['trend'])} | "
                 f"{f(v['train_cost'])} | {evaluations}{cap} | {', '.join(v['at_bounds']) or 'none'} |")
    model_loss = rivals[winner]['three_ger_rmse']['model']
    if model_loss >= min(persistence, trend):
        L += ['', f"**Benchmark failure:** {winner} does not beat the best naive rule on the three GERs. Its selection among rivals is not forecasting validation."]
    else:
        L += ['', f"**Benchmark result:** {winner} beats both naive rules on the three GERs. This remains a retrospective inspected result, not blind validation."]
    if winner == 'R2':
        L += [f"**Mechanism warning:** R2's fitted `b_h` is {f(rivals['R2']['parameters']['b_h'])} and hits a bound. "
              'It therefore does not estimate a positive human-capital effect; its lower RMSE must not be presented as support for the earnings-return account.']
    if rivals[winner]['at_bounds']:
        L += ['Bound-hitting estimates are reported as computational/red-flag results, not clean structural measurements.']
    L += ['', '### Held-out losses for the selected rival', '',
          '| series | n | model | R0 | persistence | trend |', '|---|---:|---:|---:|---:|---:|']
    for series, v in rivals[winner]['series_losses'].items():
        comp = rivals[winner]['rmse_comparison_with_R0'][series]
        L.append(f"| {series} | {v['n']} | {f(v['model'])} | {f(comp['R0'])} | {f(v['persistence'])} | {f(v['trend'])} |")
    L += ['', '### Separating observations', '',
          'The protocol pairs tertiary GER in 2013 and 2024 with a college-premium fall from 0.88 to 0.59 log points. '
          'The table reports model predictions against the held-out GER observations; it does not infer causation from the timing.', '',
          '| rival | tertiary GER 2013 | tertiary GER 2024 | Grade 10→11, 2018 |',
          '|---|---:|---:|---:|']
    ger_table = rivals[winner]['series_losses']['ger_tertiary']
    obs_2013 = ger_table['obs'][ger_table['years'].index(2013)]
    obs_2024 = ger_table['obs'][ger_table['years'].index(2024)]
    transition_obs = rivals[winner]['series_losses']['trans_lsec_usec']['obs'][0]
    for spec, v in rivals.items():
        s = v['separating_observations']
        L.append(f"| {spec} | {f(s['tertiary_ger_2013'])} | {f(s['tertiary_ger_2024'])} | {f(s['grade10_to_grade11_2018'])} |")
    L.append(f"| **observed** | **{f(obs_2013)}** | **{f(obs_2024)}** | **{f(transition_obs)}** |")
    L += ['', 'Recession secondary GER predictions (observations, where available, remain in `scores.json`):', '',
          '| rival | 1984 | 1985 | 1986 | 1998 |', '|---|---:|---:|---:|---:|']
    for spec, v in rivals.items():
        s = v['separating_observations']['recession_secondary_ger']
        L.append(f"| {spec} | {f(s['1984'])} | {f(s['1985'])} | {f(s['1986'])} | {f(s['1998'])} |")
    if scores.get('separating_test_outcomes'):
        L += ['', '### Separating-test decisions', '',
              '| test | observed years | lowest-error rival | RMSE |', '|---|---|---|---:|']
        for name, outcome in scores['separating_test_outcomes'].items():
            best = outcome['supported_rival']
            loss = outcome['rmse'].get(best) if best else None
            L.append(f"| {name} | {', '.join(map(str, outcome['years'])) or 'none'} | {best or 'not scored'} | {f(loss)} |")
    for series, title in (
        ('enrol_tertiary', 'K-12 recovery: CHED tertiary headcount index (2016 = 1)'),
        ('edu_share_hh', 'FIES household education spending share'),
        ('hh_share_total_spending', 'PIDS NTA household share of total education spending'),
    ):
        L += ['', f'### {title}', '', '| year | observed | ' + ' | '.join(rivals) + ' |',
              '|---|---:|' + ''.join('---:|' for _ in rivals)]
        base = rivals[winner]['series_losses'][series]
        for i, year in enumerate(base['years']):
            cells = []
            for spec in rivals:
                table = rivals[spec]['series_losses'][series]
                j = table['years'].index(year)
                cells.append(f(table['pred'][j]))
            L.append(f"| {year} | {f(base['obs'][i])} | " + ' | '.join(cells) + ' |')
    L += ['', '### Protocol and interpretation limits', '',
          '- Protocol amendments: none.',
          '- Post-1995 enrolment was not fitted. The explicitly registered FIES and APIS training exceptions were retained.',
          '- Unverified FIES 2023 was excluded. The DepEd transition is reference year 2018 (SY2017–18), not 2017.',
          '- PHL premiums mix methods and interpolate 1995–2013. The relational driver is wage/salary employment (`formal_share`), not a spliced occupation series.',
          '- The occupational-threshold driver is exogenous here; aggregate timing cannot identify whether requirements drove enrolment or enrolment drove requirements.',
          '- These are model comparisons, not proof of the relational account or causal estimates of policy effects.', '']
    if recovery:
        L += ['### Synthetic recovery on the selected rival', '',
              f"Declared Gaussian noise; {recovery['replicates']} replicates. A parameter passes only if at least 80% of recoveries fall within ±25% of a nonzero truth.", '',
              f"Optimiser-cap replicates: {recovery.get('optimizer_cap_replicates', 'not recorded')}.", '',
              '| parameter | truth | median | 5th–95th percentile | share within ±25% | bound-hit replicates | status |',
              '|---|---:|---:|---:|---:|---:|---|']
        for name, v in recovery['parameters'].items():
            if v['status'] == 'not in rival':
                L.append(f"| {name} | — | — | — | — | — | not in rival |")
            else:
                L.append(f"| {name} | {f(recovery['truth'][name])} | {f(v['median'])} | {f(v['q05'])} to {f(v['q95'])} | "
                         f"{f(v['within_25pct_share'], 2)} | {v.get('bound_hit_replicates', '—')} | **{v['status']}** |")
        L.append('')
    return L


def main():
    scores = json.loads((OUT / 'scores.json').read_text())
    recovery_path = OUT / f"recovery_{scores['winner_by_preregistered_rule']}.json"
    recovery = json.loads(recovery_path.read_text()) if recovery_path.exists() else None
    lines = ['# MASSENG Philippine v5 rival results', ''] + markdown_block(scores, recovery)
    (OUT / 'report.md').write_text('\n'.join(lines) + '\n')
    print(f'report written from final outputs: {OUT / "report.md"}')


if __name__ == '__main__':
    main()
