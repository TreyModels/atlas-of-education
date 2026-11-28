# Atlas Worlds · Model Lab


Formerly **Atlas of Education**. Renamed **Atlas Worlds** on 19 November 2026: the project now covers education, history, political economy and human evolution, and every model builds a small world you can run.
Research experiments, literature and contribution guidance are in [research/README.md](research/README.md). The research revision supplies code and unrun production protocols, distinguishing toy mechanism exploration from descriptive, forecasting and policy claims. Historical numerical outputs retain their version labels.

DOI: [10.5281/zenodo.24369167](https://doi.org/10.5281/zenodo.24369167) (concept DOI; always resolves to the latest release).

## Current public release

The default branch, [`main`](https://github.com/TreyModels/atlas-of-education/tree/main), is the source for the public GitHub Pages build. Branches and open pull requests contain work in progress or historical experiments.

| Project | Live | Source on main |
| --- | --- | --- |
| Atlas Worlds | [Open Atlas Worlds](https://treymodels.github.io/atlas-of-education/) | [Application source](src/) |
| Guangzhou Education Explorer | [Open the explorer](https://treymodels.github.io/atlas-of-education/guangzhou-explorer/) | [Explorer source and saved results](public/guangzhou-explorer/) |

The Guangzhou explorer reads saved simulation results. Its main experiment covers 40.96 million simulated pupil-runs. The data and provenance manifest sit alongside the page source. [How we ran the study](https://treymodels.github.io/atlas-of-education/guangzhou-explorer/methods.html).

A unified catalogue of 65 entries across the nine research families: Education & work (8),
Population & school systems (9), the IIEP/UIS planning collection (12), Historical systems:
Angkor (13), Fertility (11), Shadow education (2), Political economy (4), Deep history (2) and
Farmer field schools (4). Entries include 24 interactive Atlas workbenches, 17 classic lab
tools, 19 downloadable code-and-data bundles, 3 research write-ups and 2 narrated journeys;
they are not 65 distinct simulation engines. Three standalone laboratory implementations are
listed separately. English and Simplified Chinese are supported in the shared interface;
classic workbenches retain their original language.

A single responsive navigation system provides a desktop rail, mobile drawer and
bottom shortcuts. Global search, collection filters and the model switcher all use
the same 65-entry inventory in `src/data/model-catalogue.ts`. Classic entries open
specific tools or worlds through `reference/education/index.html#tool=...` and
`#world=...`, rather than dropping users at an archive homepage.

All simulations run locally; live simulations execute in Web Workers. Stored
experiments are labelled separately. The language query `?lang=zh-Hans` opens directly
in Simplified Chinese and the selection persists locally. A web manifest and service worker
support installation and static font/icon caching; navigation remains network-only.

    npm ci
    npm run dev
    npm run build

Model definitions and research downloads are retained in public/. React adapters
in src/models reproduce those engines (run `python3 scripts/sync-react-models.py`
after editing public/worlds.js). The institutional data is serialized as a JSON
string in its adapter to avoid processing millions of numeric AST nodes in the
build; its actual adapter SHA-256 is recorded. No engine equations changed.

Checks:

    node test-worlds.cjs
    node check-translations.cjs
    node scripts/check-react.cjs
    npm run build
    node scripts/check-worker.cjs

The worker test executes the built worker in a browser-like context in a Node
worker thread, verifies all 22 default outputs and changed inputs, and exercises
view/CSV generation. It is not a browser rendering or iOS installation test.

One React entry point serves all 22 modules. Historical controller fixtures are used only by tests. Sources and
results from the Python institution models remain downloadable, including the
maintenance repair and separate accounting extension. See REACT_INTERFACE_CREDITS.md
and CHANGES.md.

## Attribution and reuse

Credit and cite **Dr. Trey Menefee** when using, reproducing, sharing, or adapting his material. Licensed under [CC BY-NC 4.0](LICENSE): reuse and adaptation with attribution for noncommercial purposes; commercial use requires prior permission. Cite via [CITATION.cff](CITATION.cff) (DOI: [10.5281/zenodo.24369167](https://doi.org/10.5281/zenodo.24369167); details: [docs/DOI.md](docs/DOI.md)). Third-party materials retain their own terms.
