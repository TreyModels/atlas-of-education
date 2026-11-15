# Find the built-in result: twelve exercises

Each exercise rests on one finding from the external review of 14 November 2026. The model's headline result looked like a discovery. Students find out that it was put there by an assumption, a default, a definition or a weak test.

Every number below was copied from the file named in the exercise. Where a number was reproduced by running the engine, the exercise says so.

## How to use these exercises

- Open the app locally (see `teach/README.md`). Model pages open at an address ending in `#` plus the model id, for example `#china`. The ids used here are `china`, `cambodia`, `petri`, `relocation` and `credentials`.
- The static pages under `public/research/` (Out of Africa, shadow education, fertility, relocation methods) are copied into `dist/` by `npm run build`. `vite.config.ts` sets `publicDir: false`, so the dev server may not serve them. Use `npm run build` then `npm run preview` for those pages. (To confirm on your machine.)
- "Instructor demonstration" means the app has no control for the change. The exercise then gives a command or a file edit. Run it in front of the class, or hand students the printed result.
- Paths are from the repository root, `atlas-of-education/`, unless the exercise says `ooa-coast-vs-herds/`. The Out of Africa model lives in a separate repository. The copy of its code inside `public/research/out-of-africa/coast-or-herds-model.zip` is the version from before the review and has no `c_mix` option.
- "pp" means percentage points. "MAE" means mean absolute error: the average size of the miss, ignoring direction.

## Order and time

| # | Title | Model | Needs code? | Minutes |
|---|---|---|---|---|
| 1 | Does the model beat "same as last year"? | China graduate jobs | No | 20 |
| 2 | Who is the cost index charging? | Cambodia child labour | No (one sum) | 25 |
| 3 | Is the policy effect bigger than the noise? | Cambodia child labour | No | 35 |
| 4 | The coordination multiplier | Angkor, Petri lab and relocation | Demo | 30 |
| 5 | Can the mixed strategy lose? | Out of Africa | Reading | 30 |
| 6 | Rank by total, or by area? | Out of Africa | Spreadsheet | 30 |
| 7 | The unexplained step in August 2021 | China graduate jobs | No | 30 |
| 8 | Two lines going down | Fertility | Demo | 35 |
| 9 | The floor under the water | Angkor relocation | Demo | 35 |
| 10 | Three explanations, one code base | Shadow education | Reading | 35 |
| 11 | Parameters on the wall | China graduate jobs (fit) | Reading | 35 |
| 12 | The cliff in the credential floor (and the seed that changes) | Credential floor | Reading + demo | 40 |

---

## Exercise 1. Does the model beat "same as last year"?

**Model:** China graduate jobs (youth unemployment, fitted labour-market model).

**Where to open it**
- Student: app route `#china` ("China · Graduate jobs"). Read the metric tiles under the chart.
- Instructor: `public/engines/youth.js`, function `benchmarks` (lines 285 to 300). The stored numbers are in `public/engines/atlas_data.js` (`profiles['early|sigma_A=5.0']` and `naive`). Evidence: `experiments/youth-review/README.md`, sections 1.7 and 1.8. The newer benchmark folder is `research/china-forecast-ledger/README.md`.

**The claim as the model originally presented it.** The model was shown as a fitted account of China's graduate unemployment, with named mechanisms. Its fit to 2018 to 2022 was the evidence. No simple benchmark was shown beside it. (The review added the benchmark rows.)

**Student task**
1. Open `#china`. Leave every control alone.
2. Find the two tiles that begin "Holdout, 2023 H1" and "Forecast, Dec 2023 to Sep 2026". Write down the two numbers on each tile. One is labelled "model", one "naive".
3. Read the small print on the tile: "Fitted to 2018-22 only. Mean absolute error, points." Lower is better.
4. Move the slider "Aug-2021 step (unexplained residual, fitted)" and watch the two tiles. Do they move? Why might they not?
5. Write one sentence: which forecast would you rather give a ministry, and why?

**Hint 1.** The "naive" rule has no parameters at all. Its description is in `experiments/youth-review/README.md`, section 1.7 (table headed "Naive (same month of 2022)").

**Hint 2.** The naive rule says: next month will look like the same month a year ago. The model was fitted on 2018 to 2022 and then asked to predict later months. Compare the two numbers on each tile and ask which is smaller.

**What the review found (the answer).** The naive rule is closer on both windows. In the app: holdout 2023 H1, model 7.1 against naive 2.5; forecast December 2023 to September 2026, model 5.5 against naive 1.6. In the README: 7.14 against 2.50, and 5.54 against 1.61 (engine, n = 32). The model's fit to 2018 to 2022 was good (MAE 1.19), so a good fit in the past did not carry forward. The tiles do not move with the sliders because they come from a separate stored fit on 2018 to 2022 only. The plain "lake" model (4 parameters, one pool of job-seekers) also loses to the naive rule: 8.45 on 2023 H1 and 2.88 on the verified months (`experiments/youth-review/README.md`, 1.8). The full-window fit has an error of 1.27 on the new-method months, but that fit has seen those months, so it is not a test. Evidence: `experiments/youth-review/README.md` section 1.7; `research/china-forecast-ledger/README.md` reports that no small model beat the same-month rule across the board (3 of 15 model-horizon comparisons).

**The lesson.** A model that fits history can still lose to last year's number.

**Discussion question.** Ministries and donors publish enrolment and graduate-supply projections with detailed causal stories. What would it take for a planning unit to adopt a rule that any new projection method must first beat "same as last year"? Who would lose from that rule?

**Time.** 20 minutes.

---

## Exercise 2. Who is the cost index charging?

**Model:** Cambodia child labour (household simulation, "CamChild").

**Where to open it**
- Student: app route `#cambodia` ("Cambodia · Child labour"). Look at the last tile, "Illustrative cost index per child-year avoided (invented unit costs)".
- Instructor: `public/engines/camchild.js`, line 150 (the charge) and lines 167 to 185 (the comment block and the function `cst`). Evidence: `REVIEW_STATUS.md`, "Problems found beyond the review", item 6; `experiments/camchild-seeds/README.md`, "Caveats".

**The claim as the model originally presented it.** Each policy lever came with a cost per child-year of labour avoided, which reads like a programme cost-effectiveness figure.

**Student task**
1. Open `#cambodia`. Set "Simulated histories per setting" to "1 · fastest". Set "Random seed" to 1.
2. Set "School meal coverage" to 100%. All other controls stay at their defaults.
3. Read three tiles: "Child-years avoided" (2,805), "Child labour, richest fifth" (1.5%), and the cost index (1.28).
4. The tile says "Over 12 years per 6,000 children". The engine charges 0.05 adult annual wages per child per year for full school meals. Work out: 0.05 x 6,000 children x 12 years = ? Divide by 2,805. Do you get the tile's number?
5. Now ask: do the 6,000 children include children who would never have worked? Who pays for their meals in this sum?

**Hint 1.** Your sum has no term for "children who were helped". It has only the number of children.

**Hint 2.** Open `public/engines/camchild.js` at the comment starting "ILLUSTRATIVE COST INDEX". It says the unit cost is "charged to every child in the region (not only to beneficiaries)".

**What the review found (the answer).** The sum gives 3,600 divided by 2,805, which is 1.28. This matches the tile (checked by running the app's engine for seed 1). The index is total unit cost for every child in the region, divided by child-years avoided. So it is not a programme cost even on its own assumptions. The unit costs themselves are also invented: every constant in `cst()` is marked UNSOURCED in the engine comment (for meals 0.05, safety and care 0.03, migrant-support 0.08 times 0.20 in the countryside, and so on). The ratio is also unstable when little is avoided. For migrant-child support the denominator is about 113 child-years, and the per-seed ratio averages 8.4 over the 43 seeds with positive avoidance, against a pooled 4.2 (`experiments/camchild-seeds/README.md`). In the app, migrant-child support at 50% with seed 6 shows "—" for the index, because that run avoids a negative number of child-years.

**The lesson.** A cost figure divided by the wrong population measures the denominator, not the programme.

**Discussion question.** Cost-effectiveness tables (cost per extra year of schooling) are widely used to rank education programmes for aid. What must be known about who actually receives a programme before two entries in such a table can be compared?

**Time.** 25 minutes.

---

## Exercise 3. Is the policy effect bigger than the noise?

**Model:** Cambodia child labour.

**Where to open it**
- Student: app route `#cambodia`.
- Instructor: `experiments/camchild-seeds/run.cjs` and its output `experiments/camchild-seeds/results.json` (per-seed values under `perSeed`). Full tables: `experiments/camchild-seeds/README.md`. The app's 13 levers are defined in `public/worlds.js`, lines 34 to 50 (`cash`, `cashU`, `tutorFix`, `debtRelief`, `protection`, `feeding`, `leftSupport`, `harvest`, `bridging`, `ban`, `floorRise`, `garmentBoom`, `thaiOpen`).

**The claim as the model originally presented it.** Each of the 13 levers moves the child labour rate, and the app lets you rank them by their effect in 2036.

**Student task**
1. Open `#cambodia`. Set "Simulated histories per setting" to "1 · fastest". Leave all levers at zero.
2. Read the first tile, "Working in 2036". Change "Random seed" from 1 to 6, one at a time, and write down the six values. (They should be about 14.3, 13.7, 13.8, 14.0, 14.6 and 13.5 percent.) That spread is run-to-run noise: same world, same policy (none), different luck.
3. Set "Support for children of migrant parents" to 50%. For seeds 5 and 6, read "Change vs no programmes". (Seed 5: -1.1 pp. Seed 6: +0.6 pp.) The same programme appears to help in one run and hurt in the next.
4. Now set "Cash for school attendance" to 7.5% instead. Read the same tile for a few seeds. (Seed 1 gives about -5 pp.)
5. Which lever would you trust from one run? Which would you not?

**Hint 1.** Compare the size of the change with the size of the seed-to-seed spread you wrote down in step 2.

**Hint 2.** The review ran 50 seeds. The spread of the no-programme rate is a standard deviation of 0.46 pp. A lever whose average effect is smaller than that cannot be seen in one run.

**What the review found (the answer).** At half the slider maximum, five single levers move the 2036 national child labour rate by less than the seed spread (0.46 pp): migrant-child support -0.26 pp, bridging classes -0.44, minimum-age enforcement -0.32, Phnom Penh teen wages (`garmentBoom`) +0.02, and closing the Thai route (`thaiOpen` = 0) 0.00. Cash for attendance (-4.82 pp), unconditional cash (-2.07), meals (-2.30), safety and care (-2.20), ending teacher-sold tutoring (-1.34) and debt relief (-1.28) are all well above the spread. Harvest timetable (-0.50) is just above. Two of the five small ones are context levers, not programmes. The review also says the three small programmes are reliably below zero when the same 50 seeds are paired (migrant-child support t = -3.5, bridging t = -6.6, enforcement t = -4.4). So they are real in the model, but invisible in a single history. Closing the Thai route leaves the national rate unchanged and cuts teens working away from home by 10.0 pp: the work moves rather than disappears. Evidence: `experiments/camchild-seeds/README.md`.

**The lesson.** Policy effects smaller than run-to-run noise are not findings; you need many runs, or a paired design, before you can claim them.

**Discussion question.** Conditional and unconditional cash transfers are both defended on the evidence of school attendance studies. If a real trial has the same amount of noise as this model, how large would the sample need to be for a 0.3 pp effect to be detected, and would a ministry fund a trial that large?

**Time.** 35 minutes.

---

## Exercise 4. The coordination multiplier

**Model:** Angkor, Provisioning Petri lab and Elite relocation.

**Where to open it**
- Student: app routes `#petri` ("Angkor · Provisioning Petri lab") and `#relocation` ("Angkor · Elite relocation").
- Instructor: `public/engines/petri.js`, lines 3 to 6 (comment and defaults), line 9 (the knockout rule) and line 16 (harvest). `public/engines/relocation.js`, lines 3 to 5, line 11 (harvest) and lines 45 to 46. Evidence: `experiments/angkor-review/README.md`, sections 5.1 and 5.4; `experiments/angkor-review/results/sweep-engines.md`; `public/research/relocation.html`.
- Names: `coordination` and `waterFloor` are engine options. They are not controls in the app.

**The claim as the model originally presented it.** Harvest was multiplied by 5^0.227, about 1.44, taken from a published size relation. With that, the population rose and the court left in the relocation model. A "Remove coordination gain" knockout was offered as a causal test.

**Student task**
1. Open `#petri`. Leave all controls at their defaults and write down the three tiles: Peak population index, Final population retained, Accumulated food shortfall.
2. Set "Remove a mechanism" to "Remove coordination gain (no effect at the default multiplier 1)". Write the three tiles again. What changed?
3. Set "Remove a mechanism" to "Remove hydraulic dependence". Write the tiles again. This knockout changes the result. Why is the first one different?
4. Open `#relocation` with the defaults. Read "Elite households remaining". Then move "Opportunity at the second centre" to 1.6 and read it again.
5. Instructor demonstration (the app has no control for the multiplier). From the repository root run the snippet below. It runs 32 weather seeds with the default multiplier of 1 and with the old multiplier.

```
node -e "
const fs=require('fs'),vm=require('vm');
const load=f=>{const c=vm.createContext({});vm.runInContext(fs.readFileSync('public/engines/'+f,'utf8'),c);return c};
const R=load('relocation.js').AngkorRelocation;
for(const coordination of [1,5**0.227]){let exits=0;for(let seed=1;seed<=32;seed++){const r=R.run({climate:'drought',outside:1.2,seed,coordination});if(r.exitYear!==null)exits++;}console.log(coordination.toFixed(3),exits+'/32');}
"
```

**Hint 1.** In step 2 the numbers should be the same as in step 1. A test that cannot change the result tests nothing. Read the label of the control carefully.

**Hint 2.** Look at `petri.js` line 9: `coord=p.knockout==='coordination'?1:p.coordination`. If the default `coordination` is already 1, switching it "off" sets it to 1 again.

**What the review found (the answer).** At the default multiplier of 1, the coordination knockout gives the same result as "All mechanisms" (66.5% retained, shortfall 4.404, peak 527.3 on the app's seed 42). Under the old multiplier (5^0.227 = 1.441) the results were very different. Reproduced from the engines: in the relocation model at outside opportunity 1.2 with drought, the court left in 0 of 32 seeds at multiplier 1 and in 32 of 32 at 1.441. Old-centre core retained was 0.925 at 1 and 0.478 at 1.441. In the Petri lab (256 seeds, drought), retention was 0.665 at multiplier 1 with no water floor and 1.000 at 1.441 with the old 0.1 floor (peak 0.922 against 1.135; food gap 4.402 against 2.132). The exponent 1.227 in the source paper (Klassen, Ortman, Lobo and Evans 2022, Table 5) is a size association. Larger communities were given more land and water per person, so the exponent exceeds 1 for that reason, not because size causes productivity. The "5" in 5^0.227 is the ratio 500 to 100 people. At outside opportunity 1.6 the court still leaves without the multiplier (251 of 384 drought settings in the relocation grid). Evidence: `experiments/angkor-review/README.md` (tables under 5.1 and 5.4) and `experiments/angkor-review/results/sweep-engines.md`.

**The lesson.** A result that holds only at a default value is an assumption.

**Discussion question.** Arguments for large consolidated schools, or for big infrastructure, often cite the observation that bigger units produce more per person. What would you need to know before treating that as a reason to build bigger units?

**Time.** 30 minutes.

---

## Exercise 5. Can the mixed strategy lose?

**Model:** Out of Africa ("Coast or herds?"), separate repository.

**Where to open it**
- Student: the app's navigation link "Coast or herds? Out of Africa" (file `public/research/out-of-africa.html`). Find the sentence "The mixed strategy is the most likely in both chronologies."
- Instructor: `ooa-coast-vs-herds/code/model.py`, lines 191 to 193 (the mixed speed). `ooa-coast-vs-herds/code/mc.py`, lines 34, 70 to 75 (`--c-mix`). Evidence: `ooa-coast-vs-herds/REVIEW_RESPONSE.md` sections 1 and 3; `ooa-coast-vs-herds/results/review_summary.json`.
- Names: the option is `c_mix` (command line `--c-mix`). There is no control for it in the web page. Re-running the Monte Carlo takes about 6 minutes on 2 cores (`README.md` of that repository), so show the stored results.

**The claim as the model originally presented it.** Three strategies race from the Horn of Africa to Sahul: coastal, big-game hunting ("terrestrial") and mixed. The Atlas copy of the page says the mixed strategy is the most likely in both chronologies.

**Student task**
1. Read the page sentence above. Then open `REVIEW_RESPONSE.md` and find the table in section 1.
2. Read the model rule in `model.py` lines 191 to 193 (instructor can project it). In plain words: on coastal cells the mixed forager takes whichever of the two pure speeds is higher; elsewhere it uses the terrestrial speed. Ask: can the mixed forager be slower than either pure strategy on any cell?
3. In the table, read "P(mixed reaches Sahul first)" at c_mix = 0 and at c_mix = 0.2. What is c_mix?
4. Read the three posterior numbers (coastal / terrestrial / mixed) in each row. How far apart are they?
5. Write two sentences: what the original claim should say, and what extra thing the model would need to know about foragers who switch strategies.

**Hint 1.** The mixed strategy is not a rival way of living. It is defined as the better of the other two, cell by cell.

**Hint 2.** `c_mix` is a cost: the mixed speed is multiplied by (1 - c_mix). Compare the row with c_mix 0 against the row with c_mix 0.2.

**What the review found (the answer).** At c_mix = 0, mixed reaches Sahul first in 79% of runs (0.789 in `review_summary.json`), by construction. A 20% efficiency cost cuts that to 40% (0.399). Waiting at the coast for lower sea level changes nothing material (0.789 to 0.790). The posterior weights barely separate the strategies at any cost: coastal 0.23 to 0.25, terrestrial 0.33 to 0.36, mixed 0.39 to 0.44. Extension: the fitting step (ABC, which keeps simulated runs that match the evidence) keeps only runs in which people reach the Nefud palaeolakes in northern Arabia at 70 ka or earlier. That constraint is not independent of the assumed 70 to 73 ka humid window, and it is what pushes coastal below terrestrial. Dropping it moves the posterior from 0.23 / 0.33 / 0.44 to 0.31 / 0.30 / 0.39 (coastal / terrestrial / mixed), so the two pure strategies tie. This figure is in `REVIEW_RESPONSE.md` section 3 and in the page text. The output file for it is not stored in the repository (to confirm). The review also notes that the repository does not record whether the 70 to 73 ka range was chosen after seeing the Nefud date. The standalone page `ooa-coast-vs-herds/coast-or-herds.html` has been corrected. The Atlas copy `public/research/out-of-africa.html` still carries the old sentence.

**The lesson.** A strategy defined as the best of two others cannot lose to them.

**Discussion question.** "Blended", "hybrid" and "mixed-method" approaches often win comparisons in education policy papers. In what sense might they win because of how they were defined, and what cost of combining should the comparison include?

**Time.** 30 minutes.

---

## Exercise 6. Rank by total, or by area?

**Model:** Out of Africa, drowned-site hotspots.

**Where to open it**
- Student: `public/research/out-of-africa.html`, section "Experiment: where to look underwater" (the table lists each region's share of the hotspot score and median depth). Spreadsheet software.
- Instructor: `ooa-coast-vs-herds/code/exp.py`, lines 47 to 64 (shelf area and the normalised ranking). Evidence: `ooa-coast-vs-herds/REVIEW_RESPONSE.md` section 4; `ooa-coast-vs-herds/results/review_summary.json` (`hotspots`).

**The claim as the model originally presented it.** The model flags where drowned sites are most likely to be found. The Bay of Bengal and Myanmar came first, then the Sunda shelf and the western India shelf.

**Student task**
1. Copy this table into a spreadsheet. Columns: region, hotspot score, shelf area in km² above -120 m.

| Region | Score | Shelf km² |
|---|---|---|
| Bay of Bengal & Myanmar | 40.024 | 335,941 |
| Sunda shelf (Malaya, Sumatra, Java) | 20.574 | 1,602,868 |
| W India shelf (Gujarat–Kerala) | 16.449 | 245,022 |
| Makran & Indus delta | 13.285 | 64,208 |
| Oman & Persian Gulf | 5.223 | 290,639 |
| Sri Lanka & Palk Strait | 2.506 | 47,587 |
| Gulf of Aden & S Arabia | 0.749 | 30,948 |
| Red Sea & Bab-el-Mandeb | 0.645 | 183,811 |
| Sahul shelf | 0.169 | 939,527 |

2. Rank the regions by score. Compare with the share column on the page.
3. Add a column: score divided by (shelf km² / 1,000). Rank again.
4. Which regions move up, and which move down? Explain in one sentence why the Sunda shelf drops.
5. If you could dive in only two places, which would you choose, and what else would you want to know?

**Hint 1.** The score adds up route use over every drowned cell in a region. A region with more cells has more to add up.

**Hint 2.** The Sunda shelf has about 1.6 million km² of shelf. Makran and the Indus delta have about 64,000.

**What the review found (the answer).** Per 1,000 km² of shelf, the order is Makran & Indus delta (0.207), Bay of Bengal & Myanmar (0.119), W India shelf (0.067), Sri Lanka & Palk Strait (0.053), Gulf of Aden & S Arabia (0.024), Oman & Persian Gulf (0.018), Sunda shelf (0.013), Red Sea (0.004), Sahul shelf (0.000). In the raw ranking the shares were 0.399 (Bay of Bengal), 0.205 (Sunda), 0.164 (W India), 0.132 (Makran). The Bay of Bengal's first place is partly area, and the Sunda shelf falls to seventh once its very large area is counted. Evidence: `REVIEW_RESPONSE.md` section 4.

**The lesson.** A ranking by totals mostly measures size; ask whether the quantity should be per unit of area, per person or per pupil.

**Discussion question.** League tables of countries by total enrolment, total aid received or total number of research studies reward size. Pick one comparative education ranking and say whether a per-pupil or per-capita version would reorder it.

**Time.** 30 minutes.

---

## Exercise 7. The unexplained step in August 2021

**Model:** China graduate jobs.

**Where to open it**
- Student: app route `#china`. The slider is "Aug-2021 step (unexplained residual, fitted)".
- Instructor: `public/engines/youth.js`, lines 114 to 115 (`dr_drop`, applied from month 202108). `engine/firms/calibrate_china.py`, lines 23 to 27 (`FREE`, the fitted parameters and bounds) and line 127 (`LABEL`). Evidence: `experiments/youth-review/README.md`, sections 1.1 and 1.6; `engine/firms/results/china_fit.md`.

**The claim as the model originally presented it.** The rise in graduate unemployment was split into causes (the split uses Shapley values, a way of dividing a total among its causes). The largest, +3.84 pp of +5.18 pp, was labelled "Graduate-job demand: real-estate contraction and the 2021 tutoring ban" (the label is still in `engine/firms/results/china_fit.md`).

**Student task**
1. Open `#china`. Note the tile "Model rate · 2024–26" at the default (16.1%).
2. Move the "Aug-2021 step" slider to 0. Note the tile again (10.9%). What is the change, and which tile reports it?
3. Set the slider to 0.04 (the size the sourced data suggest; see the answer). Note the tile (about 11%).
4. Read the control's note: "No sourced series matches it." Read the chart: where does the model line jump?
5. Write down: what do you know about why jobs fell in that month? What would you need to measure to show the step is real estate, or tutoring, or neither?

**Hint 1.** The step is one number applied to every month from August 2021 on. Ask where in the data that number could have come from.

**Hint 2.** The review tried to derive the step from real-estate and tutoring job losses. It got 0.020, 0.041 and 0.068. The fitted step is much larger.

**What the review found (the answer).** The fitted step is 0.30 on the full window (0.32 after widening bounds) and 0.079 on the early window only, so it is unstable. Sourced data give a data-sized step of 0.020 (low), 0.041 (central) and 0.068 (high). Those sizes rest on assumed shares of real-estate and tutoring jobs open to graduates (those shares are not sourced). With a data-sized step the other parameters can be refitted and the rise stays about 5 pp (+5.00, +5.11, +5.13 pp), so the rise is not identified as step-driven. But the fit is worse in sample (cost 277.41, 255.71 and 244.24, against 227.25). No variant reproduces the observed fall in graduate vacancies (about -22% year on year in H1 2025): the model gives +8.3% for the widened fit and +15.1% to +27.4% for the data-sized steps. Real-estate development employment fell 27.0% from 2018 to 2023, but total real-estate employment rose 14.0%. The tutoring figure is about 3 million job losses against about 11 million employees, not lost openings. The label is now "Aug-2021 step (unexplained)". Caution: moving the slider without refitting, as in steps 2 and 3, is a rougher test than the review's refits, which re-estimated every other parameter. Evidence: `experiments/youth-review/README.md` section 1.1.

**The lesson.** A fitted term with no measured counterpart is a name for what the model cannot explain.

**Discussion question.** China's 2021 "double reduction" policy restricted private tutoring and is often discussed together with graduate unemployment. How would a comparative education researcher separate the effect of that policy from the effect of the property downturn, using data from outside the model?

**Time.** 30 minutes.

---

## Exercise 8. Two lines going down

**Model:** Fertility in East Asia (levels, first differences, cointegration).

**Where to open it**
- Student: `public/research/fertility.html` ("Fertility collapse lab", catalogue id `fertility-collapse`). Read the four-act summary and the "claims held vs ruled out" section.
- Instructor: `experiments/fertility-trend-check/check.py` and `README.md`. Data: `public/research/fertility/fertility-series.json` and `life_asia.json` inside `public/research/fertility/fertility-research-full.zip`. The script needs numpy, scipy and pandas; statsmodels is optional (`python3 check.py --no-statsmodels` writes `results_fallback.json` next to the script, so copy the folder first if you must not change the repository).

**The claim as the model originally presented it.** Development, measured by life expectancy and income, explains the fall in fertility in six places, and fertility settles at a floor of about 1.3 to 1.5.

**Student task**
1. Read the page's statement about the trend check. Then open `experiments/fertility-trend-check/README.md` and find the first table.
2. For Korea (KOR) with life expectancy, read the "Levels slope", "Levels R²", "Diff slope" and "Diff HAC p" columns. R² is the share of the movement that the line explains (1.00 is perfect, 0.00 is nothing). A small p (below 0.05) means the slope is unlikely to be luck. "Diff" means year-to-year change.
3. Look at the Levels R² for all twelve rows. Then look at the Diff slope and Diff HAC p. Count the rows where the change-on-change slope is clearly different from zero. Then read the "Reading" paragraph under the tables for the R² of the differenced fits.
4. Draw by hand, for two invented countries, a fertility line and a life expectancy line that both fall for 60 years, but whose year-to-year wiggles do not match. Would they correlate in levels? In changes?
5. Instructor demonstration: run the Korea check in a few lines.

```
python3 - <<'EOF'
import json,zipfile,numpy as np
from scipy import stats
R='public/research/fertility/'
z=zipfile.ZipFile(R+'fertility-research-full.zip')
L=json.loads(z.read('fertility_handoff/life_asia.json'))
s=json.load(open(R+'fertility-series.json'))
tfr=np.array(s['places']['KOR']['obs'],float)
le=np.array([L['KOR']['values'][str(y)] for y in s['years']])
a=stats.linregress(le,tfr); b=stats.linregress(np.diff(le),np.diff(tfr))
print('levels slope',round(a.slope,3),'R2',round(a.rvalue**2,2))
print('changes slope',round(b.slope,3),'R2',round(b.rvalue**2,2))
EOF
```

**Hint 1.** Two series that both trend will line up in levels whatever drives them.

**Hint 2.** Compare the year-to-year changes, not the levels. A real link should show up there too.

**What the review found (the answer).** The levels relation is strong in every place (R² 0.65 to 0.94). For Korea and life expectancy: levels slope -0.155, R² 0.87; first differences slope -0.015, R² 0.01 (checked by running the snippet). Only four of twelve differenced slopes are significant at 5%, and their signs disagree: PHL life expectancy +0.019 (the wrong sign), THA GDP -0.48, KOR life expectancy -0.015, CHN life expectancy +0.205 (driven by the swing in 1961 to 1963). Pooled over six places, differences give +0.109 for life expectancy (p 0.096, R² 0.16) and -0.507 for log GDP per capita (p 0.22, R² 0.01). No place is cointegrated at 5% over 1961 to 2024 (lowest p 0.079, PHL). Chinese life expectancy changes sign when 1961 to 1963 are dropped (+0.205 to -0.334). Held-out error averages 0.40 children (1985 to 2024), from 0.24 to 0.81, and 2024 predictions range from 1.06 (JPN) to 2.22 (PHL), so the "floor of about 1.3 to 1.5" is a fitted curve, not a finding. Evidence: `experiments/fertility-trend-check/README.md`.

**The lesson.** Two trending series will correlate whether or not one causes the other.

**Discussion question.** "Development" and "women's education" both rise steadily and both are linked to lower fertility in cross-country charts. What kind of evidence from outside the national trend lines (policy changes, sibling comparisons, school-leaving age reforms) could separate them?

**Time.** 35 minutes.

---

## Exercise 9. The floor under the water

**Model:** Angkor, Elite relocation and Petri lab.

**Where to open it**
- Student: `public/research/relocation.html` (the paragraph beginning "Time is elapsed model years"), and app route `#relocation`.
- Instructor: `public/engines/relocation.js`, line 29 (`clamp(..., waterFloor, 1)`) and line 5 (default `waterFloor:0`). `public/engines/petri.js`, line 37 and line 6. Evidence: `REVIEW_STATUS.md`, "Problems found beyond the review", item 10; `experiments/angkor-review/README.md` section 5.4 and table "Petri, coordination and water floor"; `public/research/relocation.html`.
- Names: `waterFloor` is an engine option, not a control.

**The claim as the model originally presented it.** Water condition in each centre was held at a minimum of 0.1. Before November 2026, results showed elite departure raising water condition. The floor made the model look stable where nothing was keeping it stable.

**Student task**
1. Read the relocation page paragraph about the 0.1 floor. Write down what it says happens to water condition with no local repair and no floor.
2. Open `#relocation`. Set "Maintenance covered by local cooperation" to 0%. Read "Old farming population retained" and "Old residential core retained". The defaults give 94.7% and 92.6%; with local repair at 0% they give 71.1% and 68.4%. This shows local repair matters. It does not show the floor, which has no control in the app.
3. Instructor demonstration: run the snippet below. It runs the 1,152 settings with no local repair (outside opportunity, moving hurdle, portability, climate and 32 seeds) with and without the floor, and prints the median final water condition at the old centre.

```
node -e "
const fs=require('fs'),vm=require('vm');
const c=vm.createContext({});vm.runInContext(fs.readFileSync('public/engines/relocation.js','utf8'),c);const R=c.AngkorRelocation;
const med=a=>{a=[...a].sort((x,y)=>x-y);return a[Math.floor(a.length/2)]};
for(const waterFloor of [0,0.1]){const w=[];for(const outside of [.8,1.2,1.6])for(const movingCost of [.05,.25,.5])for(const portability of [.25,.75])for(const climate of ['stable','drought'])for(let seed=1;seed<=32;seed++)w.push(R.run({outside,movingCost,portability,localRepair:0,climate,seed,waterFloor}).oldWater);console.log('floor',waterFloor,'median water',med(w).toFixed(3));}
"
```

4. Ask: if you saw only the version with the floor, what would you conclude about water without local repair?

**Hint 1.** A floor is a number below which the model refuses to go. What does a row of results look like when most of them sit exactly on that number?

**Hint 2.** The median with the floor should be exactly the floor value.

**What the review found (the answer).** Without the floor, water at a centre with no local repair falls to about zero (median 0.002, reproduced from the engine). With the floor the median is 0.100, which is the floor itself. The review states that the floor "had pinned it at 0.1 in at least half of the earlier runs". With local repair the median is about 0.76 (`REVIEW_STATUS.md`); on the repair-0.75 half of the grid used here the engine gives 0.77 (to confirm which grid the review used). In the Petri lab, the floor alone moves drought retention from 0.665 to 0.714 and the food gap from 4.402 to 4.153. Under stable climate it moves retention from 0.946 to 0.991. The relocation page now states this. Evidence: `experiments/angkor-review/README.md` (5.1 and 5.4 tables) and `public/research/relocation.html`.

**The lesson.** A safety net written into the model hides the collapse the model was built to look for.

**Discussion question.** School finance systems use guaranteed minimum funding, automatic promotion and minimum pass marks. What failures might those floors hide from a ministry looking at its own statistics?

**Time.** 35 minutes.

---

## Exercise 10. Three explanations, one code base

**Model:** Shadow education (private tutoring in Cambodia), agent-based model.

**Where to open it**
- Student: `public/research/shadow-education.html` (catalogue id `shadow-education`, "Shadow education lab"). Read "Three rival explanations" and the policy explorer.
- Instructor: `experiments/shadow-abm/src/tutoring_abm/model.py`, lines 69 to 79 (`PRIORS` and `VARIANTS`). `experiments/shadow-abm/src/tutoring_abm/shared_ablation.py`; result file `experiments/shadow-abm/src/tutoring_abm/results/shared_ablation.json`. Evidence: `experiments/shadow-abm/README.md` item 3.3.

**The claim as the model originally presented it.** Three rival explanations of why pupils pay their own teachers were tested against seven published patterns, and all of them pointed to the same policy levers.

**Student task**
1. On the page, find the sentence about policy agreement. Write down what it says.
2. Open `model.py` and find `VARIANTS` (four short lines). In your own words, what is different between "thin", "diversion", "favour" and "full"?
3. Read the line above it, `PRIORS`: how many parameters are listed? How many of them are switched on or off by the variant?
4. Open `results/shared_ablation.json`. Find `overlap`. How many lines of the model differ?
5. Look at the summary for the perturbation `no_alternative_providers` (policy `ban_own`). What happens to the effect of the ban, and to the share of simulated worlds that still fit?
6. If two explanations share nearly all their code, how much extra confidence does it give you that they agree?

**Hint 1.** Count how many of the 15 priors differ between variants.

**Hint 2.** Compare "agree on policy" with "agree because they run the same model". Ask what a model with a really different skeleton would be.

**What the review found (the answer).** The variants share one `model.py`. Only 6 of about 215 non-blank lines differ (`mechanism_lines_in_model_py: 6`, `nonblank_code_lines_in_model_py: 215`), and 2 of the 15 priors (`diversion` and `favour`) differ. Removing the alternative providers shifts every variant's policy effect together: the effect of banning teachers from selling to their own pupils on participation goes from -0.35 to -0.51 for the thin variant (-0.50 to -0.53 across the four), and the share of worlds that still fit falls to 0.0. Removing the thin-timetable channel drops the fit share from about 0.46 to 0.04 for the thin variant. Changing the withholding cost or convexity changes nothing (-0.35 stays -0.35). The review's conclusion: "The policy agreement comes from shared code and is not independent evidence." Also, on the evidence ratios at tolerance 1, thin fits most often, but "every estimate rests on a handful of fitting proposals". Fresh-world fit is 37 to 44%, but only 1 to 7% of settings fit most worlds. The code has four variants (thin, diversion, favour, full); the page shows three. Evidence: `experiments/shadow-abm/README.md`; `shared_ablation.json`.

**The lesson.** Three explanations that share one code base are not independent evidence.

**Discussion question.** International agencies often converge on the same recommendation on tutoring (regulate, don't ban; pay teachers properly). If they all draw on the same few studies and the same framework, how should a ministry weigh their agreement?

**Time.** 35 minutes.

---

## Exercise 11. Parameters on the wall

**Model:** China graduate jobs (the fit behind the model).

**Where to open it**
- Student: `engine/firms/results/china_fit.md`, the table "Headline model: full|sigma_A=5.0" (columns Estimate and s.e.). And `experiments/youth-review/README.md`, section 1.2.
- Instructor: `engine/firms/calibrate_china.py`, lines 23 to 27 (`FREE`: name, lower bound, upper bound, start). These are the widened bounds after the review. Stored fit: `engine/firms/results/china_fit.json` (`profiles['full|sigma_A=5.0'].params`).

**The claim as the model originally presented it.** The fitted parameter values were presented as the model's best estimates of how the market works.

**Student task**
1. Open `china_fit.md` and look at the Estimate column of the headline model.
2. Circle every estimate that looks "too round": a value that is exactly 0.0300, 0.4200, 1.0000 and so on.
3. Now open `experiments/youth-review/README.md` section 1.2. It lists seven parameters that sat on a bound: `m_g` (0.03, lower), `m_n` (0.42, upper), `f_n_ref` (0.38, upper), `lam_g` (1.0, upper), `m_a` (0.02, lower), `e_prop` (0, lower), `dr_drop` (0.30, upper). Check that your circles match.
4. Look at the "s.e." column (standard error: how uncertain the estimate is; small is good) for the first two. What do you notice?
5. Read what happened when the bounds were widened: which parameters moved, and did the headline rise change?

**Hint 1.** A fitting routine searches inside a box. If the best point is on the edge of the box, the data may want to go further, or may not care.

**Hint 2.** Look at the standard errors. A huge one means the data barely pin that parameter down.

**What the review found (the answer).** Seven of eleven parameters sat on a bound in the stored full fit. The standard errors for `m_g` (54.2485) and `m_n` (23.8530) are enormous. Two bounds are structural limits: `m_n` must stay below 0.45 (the non-graduate wage must stay above the flow value 0.55), so the old upper bound 0.42 was just under that ceiling; `f_n_ref` must stay below the application rate 0.40. After widening, the headline rise went from +5.18 to +5.06 pp and the fit cost improved from 244.9 to 227.3, but the parameters moved a lot: `m_g` 0.030 to 0.361, `lam_g` 1.00 to 0.004, `m_n` 0.42 to 0.332. Three still sit on bounds (`f_n_ref`, `m_a`, `e_prop`). The cost surface is flat: several different parameter sets fit within a few cost units, and a multistart with the new bounds did not reach the stored optimum. The graduate wage speed `lam_g` is weakly identified: the free fit moves between 0.004 and 1.0 and the early fit gives 0.15. Evidence: `experiments/youth-review/README.md` sections 1.2 and 1.3.

**The lesson.** A parameter that lands on its bound reflects the box the modeller drew, not what the data say.

**Discussion question.** Composite indices and weights in education statistics (for example, how to weight enrolment, completion and learning) are often chosen by experts and then treated as findings. How do you check whether a weight is chosen by the data or by the limits of the range offered?

**Time.** 35 minutes.

---

## Exercise 12. The cliff in the credential floor (and the seed that changes)

**Model:** Credential floor (Cambodia, Vietnam, China).

**Where to open it**
- Student: app route `#credentials` ("Education · Credential floor"), and `public/reference/credential-floor.md`.
- Instructor: `engine/relfloor_countries.py`: line 109 (`SMOOTH_LIQ`, the `--smooth-liq` flag), lines 112 to 113 (parameter `s_liq`), lines 141 to 146 (the hard threshold, then the graded alternative), lines 157 to 160 (deterministic seeds) and docstring lines 8 to 10. Stored results: `public/reference/relfloor_countries_v2.json` (hard threshold), `public/reference/relfloor_countries_v2_smoothliq.json` (graded), `public/reference/relfloor_countries.json` (v1, which the app page still reads). Evidence: `public/reference/credential-floor.md`; `REVIEW_STATUS.md` problems 1 to 3.
- Hard against graded: a household below `y_sub + kappa x cost` cannot pay, except with probability `p_fin` (hard). In the graded option the chance of financing rises smoothly in log income around the threshold.

**The claim as the model originally presented it.** The relational floor (eligibility for secure jobs depends on holding the credential) was rejected in Cambodia and Vietnam because it fitted worse than human capital alone.

**Student task**
1. Open `#credentials`. Set Country to Cambodia and "Highlight a mechanism bundle" to "+ Relational". Read "Exits from poorest 40%" (98.1% in the stored v1 data).
2. In `credential-floor.md`, find "Observed Cambodia value". What share of lower-secondary non-completers were in the poorest 40% in 2021? (55 to 64%.)
3. Instructor: open the two v2 JSON files and compare the Cambodia relational bundle: accepted draws, and the 2021 median share from the poorest 40%.
4. Read the sentence "that makes a cliff in completion by wealth" in the "Robustness" section. Sketch the completion rate by wealth quintile for a cliff and for a smooth rise. Which looks like the observed Cambodian profile (17, 25, 37, 53 and 65% in 2014)?
5. Seed demonstration (instructor): run `python3 -c "print(hash('M_REL'))"` twice and compare the two numbers. Version 1 of the model seeded its runs with `hash(S)`. What does that do to a result you try to rerun?

**Hint 1.** If the model has a cliff, a smooth observed profile cannot be matched by any setting. The review counted how many draws fit the full quintile profile.

**Hint 2.** Look at the "accepted, full quintile profile" column of the graded table, and at the first table's line for the hard threshold ("no draw fits any quintile profile").

**What the review found (the answer).** With the hard threshold, the relational bundle predicts 85% [69, 97] of Cambodian non-completers from the poorest 40% in 2021, against 55 to 64% observed, with 463 accepted draws (of 24,000). That looks like a rejection. But no draw fits the full quintile profile in Cambodia (0 accepted) and at most 10 in Vietnam, so it is a ranking inside a misspecified model. With the graded constraint, all three structures fit the full profile in Cambodia (64 / 91 / 44 draws for human capital, positional, relational) and in Vietnam (MICS profile: 996 / 1,370 / 1,626). The relational bundle gives 67% [57, 80] (58% [54, 61] when fitted to the profile), inside the observed range. The relational weight's posterior equals its prior in all three countries (Cambodia 0.38 [0.04, 0.75] against a prior of 0.40 [0.04, 0.76], KS p = 0.60). So: "The data do not discriminate the relational floor." The 2035 completion response also changes sign with the constraint: relational about 0 (hard) against +10 points (graded); human capital -12 against -6. Other problems in version 1: the share of non-completers from the poorest 40% was read in 2035 and then compared with 2021 data; and the seed was Python's per-process `hash()`, so runs could not be reproduced (the two `hash('M_REL')` calls print different numbers; one test gave -7071009229866375123 and 3307619203293976997). Version 2 uses deterministic seeds. The app page `#credentials` still shows the v1 stored output (version line "5 November 2026"), including 98.1% for the relational bundle in Cambodia and the statement that Vietnam's acceptance falls from 6.1% to about 0.8%; those are the numbers the review overturned. Evidence: `public/reference/credential-floor.md`.

**The lesson.** When a verdict flips with the form of one assumption (and a result cannot be rerun), the verdict belongs to the assumption.

**Discussion question.** Human capital theory, credentialism and relational accounts of schooling (in the line of Boudon, Collins and Dore) are old rivals in comparative education. If household data on wealth gradients cannot tell them apart, what other evidence would?

**Time.** 40 minutes.
