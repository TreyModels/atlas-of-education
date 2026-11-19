# Tilly-inspired CCP political-economy experiments, V6

Start with `results_completed/RESULTS.md`, then `ODD.md`. The package implements resource access, favor obligations, organizational routines and an immutable appointment cohort on the V5 simulation kernel. Behavioral parameters are experimental.

The default population is 50,000, with 64 organizations and five official ranks. Fifteen regimes test campaigns, access reform, obligations, protection, emulation, adaptation, resource allocation, oversight, assistance demand, relationship resets and promotion support. Separate controls omit outsider replacement or set resource attraction to zero.

Each appointment intervention installs 64 new, initially clean, high-integrity people. Records follow those people until retirement/removal or the fixed horizon. A person can remain clean, incur obligations lawfully, commit misconduct or face a false case. These synthetic people are not identified historical appointees of Xi Jinping.

## Execution and review

The complete design has 828 jobs. Each saves 45 annual rows after burn-in and the appointment cohort's event histories. The delivered execution is in `results_completed/`. Fourteen verification groups cover accounting, identities, cohort risk sets, mechanism controls, observation boundaries, export and resume validity. The requested gpt-6.1-terra agent's critique and fixes are in `PEER_REVIEW.md`.

`IMPLEMENTATION_LOG.md` records a serialization failure in the aborted first batch and its correction. The release excludes that incomplete batch's run files. The completed experiment uses the corrected source hash. Parameter variation and random-seed variation have separate summaries.

## Run on a Mac

Use Python 3.12 or later. From Terminal in this folder:

```bash
chmod +x run_mac.command
./run_mac.command
```

The launcher creates a virtual environment, checks the implementation and runs a fresh experiment in `results_mac/`, with four workers by default. Set `BUS_WORKERS=6` for six workers. The delivered run used the available Linux workspace; native Mac execution has not been tested here.

Manual commands:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python checks.py
.venv/bin/python empirical_adapter.py --check
.venv/bin/python run.py --workers 4 --output results_mac
.venv/bin/python analyze.py --output results_mac
```

Rerun the same `run.py` command to resume. Completed job files are reusable only when source, data, parameter design and the numerical environment match. A changed environment needs a fresh output directory. The exact delivered versions are in `requirements-executed.txt` and the manifest.

For a larger exploration, change `--draws`, `--seeds` or `--trajectories`, using a fresh output directory. Reference experiments always use eight seeds; integrity anchors, scale and initialization checks have their own fixed replication. The full manifest supplies the actual counts. One simulation step represents an annual decision cycle, rather than a one-for-one reconstruction of actual Chinese events.

## Empirical data and the site supplied during development

`CCPORG_ASSESSMENT.md` assesses [ccporg.org](https://ccporg.org/) and its methods. It can provide source-linked events and career overlaps, subject to selected coverage, source quality and chronology. It has not been ingested as a complete database or fitted to the model.

`empirical_adapter.py` accepts a CSV with columns `person_a, person_b, relation_type, service_start, service_end, source_published, source_url, end_imputed, verified`. The primary graph retains explicit, verified co-service intervals backed by sources available at the requested cutoff. It preserves rejection reasons and does not treat an unrecorded tie as absent. It is an export adapter, rather than a scraper.

```bash
.venv/bin/python empirical_adapter.py --input career_edges.csv --as-of 2020-12-31 --output empirical/edges_audited.csv
```

The retained official panel and selected procurement notices enter the model only through declared normalized economic drivers and evidence profiling. A case file is an enforcement event. Empirical evaluation still requires a common position-at-risk population and separate evidence about underlying conduct. The earlier `LITERATURE_REVIEW.md` assesses V4 and supplies the substantive bibliography; use the present ODD and results for V6 behavior.
