# DOIs via Zenodo

**Whole Atlas (automatic):** Zenodo is linked to GitHub. Each GitHub *release* of `TreyModels/atlas-of-education` gets a version DOI, and there is one concept DOI that always points to the latest. Metadata comes from `.zenodo.json` and `CITATION.cff`.

## Current DOIs (19 Nov 2026)

| Purpose | DOI | Record |
| --- | --- | --- |
| **Concept DOI** — cite this; always resolves to the latest version | [10.5281/zenodo.24369167](https://doi.org/10.5281/zenodo.24369167) | [zenodo.org/records/24369167](https://zenodo.org/records/24369167) |
| **Version DOI** — v2026.11.19 | [10.5281/zenodo.24369168](https://doi.org/10.5281/zenodo.24369168) | [zenodo.org/records/24369168](https://zenodo.org/records/24369168) |
| **Version DOI** — v2026.11.20 | [10.5281/zenodo.24369385](https://doi.org/10.5281/zenodo.24369385) | [zenodo.org/records/24369385](https://zenodo.org/records/24369385) |
| **Version DOI** — v2026.11.21 | [10.5281/zenodo.24369841](https://doi.org/10.5281/zenodo.24369841) | [zenodo.org/records/24369841](https://zenodo.org/records/24369841) |
| **Version DOI** — v2026.11.22 | [10.5281/zenodo.24370343](https://doi.org/10.5281/zenodo.24370343) | [zenodo.org/records/24370343](https://zenodo.org/records/24370343) |
| **Version DOI** — v2026.11.23 | [10.5281/zenodo.24371193](https://doi.org/10.5281/zenodo.24371193) | [zenodo.org/records/24371193](https://zenodo.org/records/24371193) |
| **Version DOI** — v2026.11.24 | [10.5281/zenodo.24372120](https://doi.org/10.5281/zenodo.24372120) | [zenodo.org/records/24372120](https://zenodo.org/records/24372120) |

`CITATION.cff` carries the **concept** DOI (10.5281/zenodo.24369167), so a citation keeps resolving to the newest release. Each future GitHub release mints a new version DOI under the same concept DOI; add it to this table when it is issued.

One-time setup — **DONE 19 Nov 2026** (kept as reference):
1. zenodo.org → log in with GitHub → profile menu → **GitHub** → **Sync now** → switch **TreyModels/atlas-of-education** ON.
2. On GitHub, create a release (e.g. tag `v2026.11.19`). Zenodo archives it and shows the DOI badge.
3. Paste the concept DOI into `CITATION.cff` (`doi:`) and into the site footer. Model pages then cite it.

**Per-model DOIs (optional, next step):** upload each model's download ZIP (code, data, results, README) to Zenodo as its own record. Use "Related identifiers: is part of → the Atlas concept DOI" and list the model's own paper (e.g. Klassen et al. 2022 for Angkor provisioning) under "References". This can be scripted with a Zenodo API token later. Never put the token in the repo or on the Bridge message log.
