# DOIs via Zenodo

**Whole Atlas (automatic):** Zenodo is linked to GitHub. Each GitHub *release* of `TreyModels/atlas-of-education` gets a version DOI, and there is one concept DOI that always points to the latest. Metadata comes from `.zenodo.json` and `CITATION.cff`.

One-time setup (Trey, about 2 minutes):
1. zenodo.org → log in with GitHub → profile menu → **GitHub** → **Sync now** → switch **TreyModels/atlas-of-education** ON.
2. On GitHub, create a release (e.g. tag `v2026.11.19`). Zenodo archives it and shows the DOI badge.
3. Paste the concept DOI into `CITATION.cff` (`doi:`) and into the site footer. Model pages then cite it.

**Per-model DOIs (optional, next step):** upload each model's download ZIP (code, data, results, README) to Zenodo as its own record. Use "Related identifiers: is part of → the Atlas concept DOI" and list the model's own paper (e.g. Klassen et al. 2022 for Angkor provisioning) under "References". This can be scripted with a Zenodo API token later. Never put the token in the repo or on the Bridge message log.
