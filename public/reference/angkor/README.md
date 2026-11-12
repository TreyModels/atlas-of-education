# Angkor Atlas, standalone browser research sandbox (v1.0)

## Launch

1. Unzip the folder.
2. Double-click **index.html** in Chrome, Firefox, Edge or Safari. It works completely offline and needs no server, Python, npm or internet.
3. Choose a scenario, change parameters, click **Run single history**.
4. Use **Monte Carlo** to compare the current setup against another preset using paired random seeds.
5. Use **Regression lab** for independent parameter sweeps and OLS coefficient estimates; export CSV datasets.
6. Click **中文** in the top right for the Chinese explanatory UI.

Files: `index.html` UI, `app.js` controls and Canvas plots, `model.js` simulation/Monte Carlo/OLS engine, `MODEL_CARD.md` caveats and research specification, `test_model.js` basic reproducibility/unit tests.

## AI handoff prompt

> Open this ZIP as an offline browser app. Read README.md, MODEL_CARD.md, model.js, app.js and index.html. Preserve existing features, the seeded simulation and CSV exports. Extend the model by adding named competing kingdoms with independent resource stocks and allegiance networks, crop seasonality, explicit food logistics and multiple true household agents. Add paired-seed tests and record which parameter values are historical estimates versus hypothesized. Keep interface bilingual English/Chinese. Run `node test_model.js` after modifications.

## What it does and does not do

- It is a reproducible **spatial cohort-based ABM-inspired mechanism sandbox**, not a calibrated archaeological reproduction or true household-level agent simulation.
- The historical preset contains illustrative assumptions, alongside a few historical scale anchors. It is explicitly not an empirical posterior.
- Regressions are ordinary least squares on synthetic Monte Carlo data, useful for model sensitivity; their coefficients do not establish real-world historical causation.
- The rival-power process is an endogenous stylized competitor, **not yet multiple independent named kingdom agents**. It can produce raids, defeats, sacks, labor capture and loyalty responses.
- Inputs such as `corveeDays`, `bonded`, `maintenanceIntensity` and `conquestDamage` should be treated as experimental uncertainties.
- A 140-cell schematic map is **not** a historically georeferenced GIS base.

If Chrome restricts local scripts, launch with `python -m http.server 8000` inside the unzipped folder and open `http://localhost:8000`. Standard browsers usually open it directly by double-clicking.

## Research edition: accompanying paper and reproducible results

This archive also includes a `research/` directory. Start with **`research/RESEARCH_PAPER.md`** for the research question, history, methods, findings and limitations. Read **`research/BUILD_HISTORY.md`** for the collaborative design process and how the ideas evolved. **`research/METHODS_AND_ASSUMPTIONS.md`** audits the exact equations and important defects. **`research/SOURCES_AND_PROVENANCE.md`** identifies the historical and comparative sources that inspired the hypotheses, with evidence grades. **`research/RESULTS_README.md`** explains the CSV and JSON outputs.

To reproduce the reported results, run `node scripts/reproduce_results.js` (Node.js optional for the web app). The package includes pre-generated results so readers can inspect them without installing anything. The app itself remains usable offline by opening `index.html`.

**Research integrity:** The results are simulated and exploratory. This is not a calibrated archaeological reconstruction, and the software currently has known food-accounting and military-budget limitations documented in the paper.
