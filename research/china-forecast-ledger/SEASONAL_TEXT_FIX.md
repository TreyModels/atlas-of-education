# Seasonal text fix (engine/firms/seasonal_2024.py)

Problem: the prose under "What this establishes" in `engine/firms/results/seasonal_2024.md` was typed into the script and
contradicted the table. It called the variant chosen on training fit (spread8, test MAE 0.99) "the first China specification
in this project to beat the naive benchmark" although naive is 0.89, and it quoted "0.62-0.70" and "base 1.36 / duration 1.04"
for test performance, which do not match the table (those look like fit numbers; the test MAEs are 1.71 and 1.19 for base and duration).

Change: `report()` is split into `add_vs_naive()` (needs model runs, as before), `report()` (both) and a new `render(res)` that
writes the markdown from a results dict alone. All prose in "What this establishes" is now computed in `render()`: the variant
selected on training fit, whether its test MAE is below naive, which variants are below naive on test MAE (and the range),
which spread variants beat or miss naive, the number of test months, its paired t, wins and mean difference, its July error and the
variant count. Wording switches with the numbers (beats / does not beat; "distinguishable" only if |t| >= 2). The spread-entry
reading is now stated as a hypothesis, shown only if every spread variant has lower test MAE than base. A `--render-only` flag
re-renders from the stored json without refitting.

Run: `cd engine && python3 -m firms.seasonal_2024 --render-only` (done). `results/seasonal_2024.json` is byte-identical before
and after (checked with cmp); tables in the .md are unchanged; only the header line and the four numbered paragraphs changed.

New conclusion in the regenerated text: spread8 (selected on training fit) has test MAE 0.99 against naive 0.89, wins 7/19 months,
paired t +0.66, so it does not beat naive. Only spread11 (0.77) and duration+spread11 (0.71) are below naive on test MAE, with paired t
-0.77 and -1.14, not distinguishable from naive. Note these two were not the variants selected on training fit.
