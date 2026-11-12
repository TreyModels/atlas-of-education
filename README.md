# Atlas of Education · Model Lab

A unified catalogue of 46 entries across Education & work, Population & school systems,
the IIEP/UIS planning collection, Historical systems: Angkor, Fertility, and Shadow education.
Entries include live workbenches, classic tools, research downloads, and four curated stored
massification experiments; they are not 46 distinct simulation engines. Three standalone
laboratory implementations are listed separately. English, Simplified Chinese and Vietnamese
are supported in the shared interface; classic workbenches retain their original language.

A single responsive navigation system provides a desktop rail, mobile drawer and
bottom shortcuts. Global search, collection filters and the model switcher all use
the same 46-entry inventory in `src/data/model-catalogue.ts`. Classic entries open
specific tools or worlds through `reference/education/index.html#tool=...` and
`#world=...`, rather than dropping users at an archive homepage.

All simulations run locally; live simulations execute in Web Workers. Stored
experiments are labelled separately. The language query `?lang=vi` opens directly
in Vietnamese and the selection persists locally. A web manifest and service worker
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

Credit and cite **Dr. Trey Menefee** when using, reproducing, sharing, or adapting his material. Noncommercial use is permitted under the conditions in [LICENSE](LICENSE); commercial use requires prior permission. Third-party materials retain their own terms.
