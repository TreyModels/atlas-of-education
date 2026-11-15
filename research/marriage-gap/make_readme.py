"""Writes README.md from results/*.json and FACT_CHECK.md. No model number is typed by hand.
Run after experiments.py:  python3 make_readme.py"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
L = lambda n: json.load(open(os.path.join(HERE, "results", n)))
inp, A, B, C, D, E, F = (L("inputs_used.json"), L("a_selection_ceiling.json"), L("b_fits.json"),
                         L("c_age_profile.json"), L("d_cross_country.json"),
                         L("e_robustness_age_gap.json"), L("f_sampling_noise.json"))
fact = open(os.path.join(HERE, "FACT_CHECK.md")).read()

pc = lambda x, d=0: f"{100 * x:.{d}f}"          # share -> percent string
pt = lambda x: f"{100 * x:.0f}"                  # share -> points
obs_gap = pt(A["observed_gap"])
BANDS = ["18-22", "23-26", "27-30", "31-34"]

def para_after(marker, stop="\n\n"):
    i = fact.index(marker) + len(marker)
    j = fact.index(stop, i)
    return fact[i:j].strip()

squash = lambda t: " ".join(t.split())
doubt = squash(para_after("**Main doubt about the headline number.**"))
reading = squash(para_after("Reading across them:"))
reading = reading[0].upper() + reading[1:]

bg, sel, div, mix = A["best_guess"], B["selection"], B["divergence"], B["mixed"]
rc = inp["R_CHINA"]
gap_bg = 100 * bg["gap"]
# smallest m (grid) at which, within the realistic window and r <= China's mean, the grid reaches the observed gap
reach = [x for x in A["max_in_window_r_at_or_below_china_by_m"] if x["best"] and x["best"]["gap"] >= A["observed_gap"]]
m_reach = reach[0] if reach else None
dec = C["mixed"]["decomposition"]
sel_g, div_g = C["selection"]["by_band"], C["divergence"]["by_band"]
z = F["difference"] / ((F["se_gap_selection_fit"] ** 2 + F["se_gap_divergence_fit"] ** 2) ** 0.5)

def band_table(rows):
    out = "| Model (fitted to the China pair) | " + " | ".join(BANDS) + " |\n|---|" + "---|" * len(BANDS) + "\n"
    for name, d in rows:
        out += f"| {name} | " + " | ".join(pt(d[b]) for b in BANDS) + " |\n"
    return out

o = []
w = o.append
w("# Why do unmarried Chinese women say they want marriage less than men do? A small-model test\n")
w("*A worked example of building a small model with the six-rule gate. Every model number below is written into this file by `make_readme.py` from `results/*.json`; nothing is typed by hand. Re-run `python3 experiments.py && python3 make_readme.py` to regenerate. Tests: `python3 test_model.py`.*\n")

w("## Puzzle\n")
w("The Institute for Family Studies chart \"Big marriage aspiration gap in China\" (IFS-Wheatley Survey of Family Culture 2026) shows the percent of unmarried adults aged 18-34 who would like to get married someday, women / men: "
  + ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in inp["chart"].items())
  + f". In mainland China 48% of women and 77% of men say yes, a gap of {obs_gap} points. Japan, with similarly low numbers, shows no gap. The gap is the puzzle: do Chinese women want marriage less, or is something about who is left unmarried making it look that way?\n")

w("## Fact check\n")
w(f"**Main doubt first.** {doubt}\n")
w("Short version of the rest (full table with a URL for every figure and a read-in-source / not-found label for each: `FACT_CHECK.md`):\n")
w(f"- Survey: online opt-in panel (Lucid/Cint), 1,047 mainland Chinese respondents in all, fielded August 2026, weighted to UN margins. The question wording and the size of the unmarried 18-34 cells were not found.")
w(f"- Independent surveys: {reading}")
w(f"- Sex ratio at birth, UN WPP 2024, average over the 1992-2008 birth cohorts (those aged 18-34 in 2026): China {100*inp['R']['China']:.1f}, South Korea {100*inp['R']['Korea']:.1f}, Japan {100*inp['R']['Japan']:.1f} boys per 100 girls. Only the UN series was read for China and Japan; Korea was partly cross-checked.")
w(f"- Share of 30-34 year olds who had ever married in China, 2022, about {pc(inp['ever_married_target'],1)}% (a news report of a yearbook figure; used only to set the speed of marriage).\n")

w("## Two rival explanations\n")
w("- **DIVERGENCE.** Women in China really want marriage less than men do, for reasons such as family duties after marriage and risk. The sex ratio plays no part.")
w("- **SELECTION.** Men and women want marriage equally. But the unmarried are not a random sample: where men outnumber women, women who want to marry are matched and leave the unmarried pool, while men who want to marry stay in it. Among the unmarried, the share of women who want marriage falls and the share of men stays high, with no difference in underlying preference.\n")

w("## The observation that separates them\n")
w("Decided before the model was built, and written down in `experiments.py`: **the age profile of the gap.** " 
  "Selection acts only after people start to leave the pool, so it predicts a gap near zero among the youngest unmarried (18-22) that widens with age. Divergence predicts a gap that is already present at 18-22. "
  "Anything that shows the share wanting marriage by sex and single year of age separates them; a single country-wide pair of numbers, like the chart, cannot.\n")

w("## The model in plain words\n")
w("Everyone in one birth cohort is the same age and cohorts are the same size. Each year, unmarried people who want marriage meet; marriages happen at a fixed rate; people who do not want marriage never marry. Nobody dies, moves or divorces. Four parameters:\n")
w("- **r**: the number of men per woman in each cohort (selection takes it from the sex ratio at birth; divergence sets it to 1).")
w("- **p_m**: the share of men who want to marry, fixed for each person for life.")
w("- **p_w**: the share of women who want to marry, fixed for life. SELECTION sets p_w = p_m.")
w("- **m**: each year, the number of marriages is m times the smaller of the two groups (men or women who want marriage and are still unmarried) in a matched pair of cohorts. A larger m means marriage happens faster.")
w("- Fixed, not fitted: men and women of the same age are matched (the main model); marriage is possible from age 20; ages 18-34 are reported. A robustness run has men marrying women two years younger.")
w("- Output: among unmarried 18-34 year olds, the share who want to marry, by sex, overall and by age band. The overall figure is age-standardised in a simple way (each single age gets equal weight), because the chart is age-standardised; the unweighted pooled version is also stored in the JSON files and is smaller.")
w("- m is pinned by one real figure: the share ever married by age 30-34 (pooled over both sexes) should be the census-style figure above. The window treated as realistic is "
  f"{pc(inp['window'][0])}% to {pc(inp['window'][1])}%.\n")

w("## Results\n")
if gap_bg < 100 * A["observed_gap"]:
    first = (f"**Selection alone does not reach the observed gap at realistic values.** With the sex ratio from the data (r = {rc:.3f}), a common wish to marry of {pc(bg['p'])}% and marriage speed m = {bg['m']:.2f} (set so that {pc(bg['ever_married']['pooled'],1)}% have ever married by 30-34), it produces a {gap_bg:.0f}-point gap ({pc(bg['share_w'])}% women vs {pc(bg['share_m'])}% men) against {obs_gap} observed. "
             f"It gets to {obs_gap} points only with a larger sex ratio (fitted r = {sel['r']:.2f} against {rc:.2f} from the data) or with faster marriage and a very high common wish to marry.")
else:
    first = f"**Selection alone reaches the observed gap at the best-guess values**: {gap_bg:.0f} points against {obs_gap} observed."
w(first + "\n")

w("### (a) How big a gap can selection alone make?\n")
mx, mw, mr = A["max_gap_any"], A["max_gap_in_realistic_window"], A["max_gap_in_realistic_window_r_at_or_below_china"]
w(f"Sweep of {A['n_runs']} runs: r from 1.00 to 1.20, a common p from 0.60 to 0.95, m from {A['m_grid'][0]} to {A['m_grid'][-1]}. The largest gap anywhere in the sweep is {pt(mx['gap'])} points (r = {mx['r']:.2f}, p = {mx['p']:.2f}, m = {mx['m']:.2f}); it needs everyone who wants marriage to marry almost at once, which no data I have checked supports. Within the ever-married window and r no higher than China's mean ({round(rc,2):.2f}), the largest is {pt(mr['gap'])} points at m = {mr['m']:.2f}. {A['share_of_grid_reaching_observed_gap']*100:.0f}% of all sweep cells reach the observed {obs_gap} points; among cells inside the ever-married window, {100*A['share_of_window_reaching_observed_gap']:.0f}% do. "
  + (f"So the sweep alone cannot rule selection out: with r at or below China's, the sweep first reaches {obs_gap} points at m = {m_reach['m']:.1f}, p = {m_reach['best']['p']:.2f} ({pt(m_reach['best']['gap'])} points), where {pc(m_reach['best']['ever_married_pooled'],1)}% have ever married by 30-34, the top of the realistic window. " if m_reach else f"Within the window and r at or below China's, no cell in the sweep reaches {obs_gap} points. ")
  + "The answer depends on the speed of marriage and on p, neither of which this chart can identify.\n")
w(f"At the best-guess values (r = {rc:.3f}, p = {bg['p']:.2f}, m = {bg['m']:.2f}): gap {gap_bg:.0f} points overall. By age band (men minus women, points): " + ", ".join(f"{b} {pt(bg['by_band'][b]['gap'])}" for b in BANDS) + f". Measured as a plain pooled share of all unmarried 18-34 year olds instead of age-standardised, the same run gives {pt(bg['gap_pooled'])} points. The result is sensitive to this choice, so how the survey standardised its ages matters and was not found.\n")
g2 = E["selection_fit_g2"]; g2r1 = E["gap_at_r1_equal_preferences_g2"]
w(f"Robustness, men marrying women two years younger: the best-guess gap becomes {pt(A['best_guess_age_gap_2']['gap'])} points, but part of that comes from men simply staying unmarried longer: with r = 1 and equal preferences the same setting gives {pt(g2r1['gap'])} points. The fitted selection r under this setting is {g2['r']:.2f}.\n")
w("Gap at the best-guess p and m for several sex ratios (m re-set each time so that ever-married stays at the same figure):\n")
w("| r | m | gap (points) |\n|---|---|---|")
for x in A["gap_by_r_at_p_best_calibrated"]:
    w(f"| {x['r']:.3f} | {x['m']:.2f} | {pt(x['gap'])} |")
w("")

w("### (b) Fit each rival to the China pair\n")
w(f"Each rival has three free parameters and three targets (women {pc(B['targets']['w'])}%, men {pc(B['targets']['m'])}%, ever married by 30-34 {pc(B['targets']['ever_married_pooled'],1)}%). A close fit is therefore guaranteed and is not a test; the question is whether the implied parameters are believable.\n")
w("| | r | p_m | p_w | m | ever married 30-34, women / men |\n|---|---|---|---|---|---|")
w(f"| SELECTION (p_m = p_w) | {sel['r']:.2f} | {sel['p']:.2f} | {sel['p']:.2f} | {sel['m']:.2f} | {pc(sel['ever_married']['w'])}% / {pc(sel['ever_married']['m'])}% |")
w(f"| DIVERGENCE (r = 1) | 1.00 | {div['p_m']:.2f} | {div['p_w']:.2f} | {div['m']:.2f} | {pc(div['ever_married']['w'])}% / {pc(div['ever_married']['m'])}% |")
w(f"| MIXED (r from data) | {mix['r']:.2f} | {mix['p_m']:.2f} | {mix['p_w']:.2f} | {mix['m']:.2f} | {pc(mix['ever_married']['w'])}% / {pc(mix['ever_married']['m'])}% |\n")
w(f"- SELECTION needs a sex ratio of {sel['r']:.2f} men per woman at entry. The data give {rc:.2f} (UN WPP, births 1992-2008), so the required ratio is {100*(sel['r']/rc-1):.0f}% above the birth ratio. Birth ratios are not marriage-market ratios (migration, deaths, the age gap), so this is close enough that selection cannot be dismissed, but it does not fit without stretching the sex ratio. The fitted p of {pc(sel['p'])}% is the same for both sexes.")
w(f"- DIVERGENCE needs only a {100*(div['p_m']-div['p_w']):.0f}-point difference in who wants marriage at all (p_m {pc(div['p_m'])}% vs p_w {pc(div['p_w'])}%), not a halving. In this model even a modest preference difference is magnified in the unmarried pool, because the group that wants marriage less is depleted faster. That is a result about the model: because about {pc(inp['ever_married_target'])}% of people marry by 30-34 and preferences are fixed here, no more than about {pc(1-inp['ever_married_target'])}% of people can be permanent non-wanters. The strong version of divergence, in which nearly half of Chinese women never want marriage, is not compatible with the census-style figure under fixed preferences. It is compatible only if wishes change over time or if the online sample is unrepresentative.")
w(f"- If m is not tied to the ever-married figure, selection can fit with very different r and p: with m = {B['selection_two_target_by_m'][2]['m']:.1f} it needs r = {B['selection_two_target_by_m'][2]['r']:.2f}; with m = {B['selection_two_target_by_m'][3]['m']:.1f} only r = {B['selection_two_target_by_m'][3]['r']:.2f}, but then {pc(B['selection_two_target_by_m'][3]['ever_married_pooled'])}% would have married by 30-34, too many, and with m = {B['selection_two_target_by_m'][1]['m']:.1f} it needs r = {B['selection_two_target_by_m'][1]['r']:.1f} and only {pc(B['selection_two_target_by_m'][1]['ever_married_pooled'])}% marry. The ever-married figure is what makes the test informative.\n")

w("### (c) The age profile of the gap (the observation fixed before building)\n")
w("Gap, men minus women, in points, among unmarried people in each age band, at each rival's fitted parameters:\n")
w(band_table([("SELECTION", sel_g), ("DIVERGENCE", div_g), ("MIXED (r from data)", C["mixed"]["by_band"])]))
w(f"Both rivals predict a gap that grows with age, because people leave the pool as they marry. They differ at the youngest ages: {pt(sel_g['18-22'])} points for selection against {pt(div_g['18-22'])} for divergence in the 18-22 band (mixed: {pt(C['mixed']['by_band']['18-22'])}). That is a difference of {pt(F['difference'])} points. If a survey had about {F['assumed_n_per_sex_18_22']} unmarried respondents per sex in that band (an assumption, not a known number), the sampling error of the gap would be about {pt(F['se_gap_selection_fit'])} points, so the difference would be about {z:.1f} standard errors: suggestive, not decisive. By single year of age the profiles are in `results/c_age_profile.json`.\n")
w("How much of the gap does each mechanism carry? Mixed model, r from data, p_m and p_w both fitted (points):\n")
w("| Total | Selection only (equal preferences, r from data) | Preferences only (fitted p_m, p_w, r = 1) | Interaction |\n|---|---|---|---|")
w(f"| {pt(dec['total'])} | {pt(dec['selection_only'])} | {pt(dec['preferences_only'])} | {pt(dec['interaction'])} |\n")
w(f"The mixed fit has a preference difference of {100*(mix['p_m']-mix['p_w']):.0f} points (p_m {pc(mix['p_m'])}%, p_w {pc(mix['p_w'])}%). The two mechanisms do not add up: each alone gives a smaller or similar gap, and together they overlap. The split is a property of this particular model and should not be read as a measurement.\n")

w("### (d) Cross-country consistency check (weak: three points)\n")
w("With each country's sex ratio and a common p, and the China-calibrated m, selection predicts these gaps (points); chart in the last column. The chart's Korea gap is not significant, and the Japan gap has no significance label in the data we were given.\n")
w("| common p | " + " | ".join(f"{c} (r = {inp['R'][c]:.3f})" for c in ("China", "Korea", "Japan")) + " |\n|---|---|---|---|")
for p in (0.6, 0.75, 0.9):
    vals = {r_["country"]: r_["predicted_gap_points"] for r_ in D["rows"] if r_["common_p"] == p}
    w(f"| {p} | " + " | ".join(f"{vals[c]:.0f}" for c in ("China", "Korea", "Japan")) + " |")
w("| chart | " + " | ".join(f"{D['chart_gap_points'][c]}" for c in ("China", "Korea", "Japan")) + " |\n")
ov = D["own_average_variant"]
w(f"Ordering predicted at p = 0.9: {' > '.join(D['order_predicted_p0.9'])}; chart: {' > '.join(D['order_chart'])}. "
  + ("The ordering matches. " if D['order_predicted_p0.9'] == D['order_chart'] else "The ordering does not match. ")
  + f"But the size is off: Japan is over-predicted at high p ({D['rows'][8]['predicted_gap_points']:.0f} against {D['chart_gap_points']['Japan']}), and Japan's own numbers imply a low common p, which is not common. A variant that sets p to each country's own chart average (which uses the outcome, so favours selection) gives " + ", ".join(f"{x['country']} {x['predicted_gap_points']:.0f}" for x in ov) + f", where the ordering is {' > '.join(sorted([x['country'] for x in ov], key=lambda c: -[y['predicted_gap_points'] for y in ov if y['country']==c][0]))}. With three points and free p this is a consistency check, not a test. Divergence makes no cross-country prediction without a story about why preferences differ. Countries where women exceed men on the chart (Ireland, the United States) are not explained by either mechanism here; their sex ratios were not checked.\n")

w("## Verdict so far\n")
w(f"The chart cannot tell the two explanations apart, because a single gap among the unmarried is produced by both. At the sex ratio the data give, selection by itself makes about {gap_bg:.0f} of the {obs_gap} points and needs a sex ratio about {100*(sel['r']/rc-1):.0f}% higher than the birth data to make all of it, so a mixture, or selection plus a modestly higher effective sex ratio, is as consistent with the numbers as either pure story. "
  f"The size of the preference difference that divergence needs ({100*(div['p_m']-div['p_w']):.0f} points) is much smaller than the headline suggests, so the chart does not show that Chinese women want marriage much less than men; it shows that the unmarried women are less keen, which is partly arithmetic. "
  f"The headline number itself comes from a non-random online sample of 1,047 Chinese respondents, with other surveys giving different values for women. The next step is data on marriage intention by sex and single year of age, not more modelling of this chart.\n")

w("## What data would settle it\n")
w("A survey, or a survey wave, with: marriage intention by sex in single years of age (or at least 18-20, 21-23, and so on) and enough respondents in each cell, say several hundred per sex in the youngest band; ideally the same people followed for several years, so we can see who with a given stated wish marries (which would test the fixed-wish assumption), and the local sex ratio of each respondent. I have not verified that any specific survey has these. Candidates to check: the China Family Panel Studies, the Chinese General Social Survey, the Renmin University surveys of unmarried people, and the micro data of the IFS-Wheatley survey itself (to see the unmarried 18-34 cell sizes, the question wording and the age weighting). Marriage registration counts by sex and age are a separate check on how fast marriage happens (m).\n")

w("## Limits\n")
for t in [
    "Preferences are fixed for life. If people's wish to marry changes with age or experience, the ever-married figure no longer limits how many women can be non-wanters at a given moment, and the fixed-wish divergence fit is too restrictive.",
    "No deaths, migration, divorce or remarriage. The survey's 'not currently married' includes divorced people; the model's unmarried are never-married only.",
    "Marriages are one-to-one between the same age (main model) and the speed m is one number for everyone and every age. Real search is more complicated, including class and region matching, which can make local sex ratios much more extreme than the national one.",
    f"The sex ratio at birth is used as the sex ratio of the pool. UN WPP values are smoothed and national series can differ (Korea: two sources differed by about 2 per 100 in some years).",
    "The ever-married anchor is one figure from a news report of a yearbook table, for both sexes, for 2022, and the window of 'realistic' values is my choice.",
    "The survey is an online opt-in sample; its weighting, question wording and cell sizes were not found. Significance in the chart covers sampling noise only.",
    "The age-standardisation here (equal weights across single years) is an assumption; a different standardisation changes the overall gap noticeably (see (a)).",
    "Both rivals fit the China pair exactly with three free parameters and three targets, so the fits cannot favour either. Only the age profile and independent data can.",
    "This is a model of a mechanism, not an estimate of how much of the real gap each mechanism explains.",
]:
    w(f"- {t}")
w("")
w("## Files\n")
w("`model.py` (the model), `experiments.py` (all experiments), `data_inputs.py` (sourced inputs), `FACT_CHECK.md` (sources), `results/*.json`, `make_readme.py` (this file's generator), `test_model.py`.")
open(os.path.join(HERE, "README.md"), "w").write("\n".join(o) + "\n")
print("README written")
