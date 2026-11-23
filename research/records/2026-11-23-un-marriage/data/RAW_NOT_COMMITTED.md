# Raw downloads (not committed — too large for the repo)

All files were downloaded on **23 Nov 2026** on the AutoDL server into
`/root/work/undata/raw/` and are kept there. The machine-readable extracts built
from them are in this directory (`*.json`, `*_provenance.csv`,
`availability.csv`, `source_composition.csv`).

Critical access note: `www.un.org` returns **HTTP 403** to the default `curl`
user agent but **HTTP 200** to a normal browser user agent. Every download
below was made with

```
curl -sS -L -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
     (KHTML, like Gecko) Chrome/124.0 Safari/537.36" -o <file> <url>
```

Reproduce with `scripts/download_raw.sh`.

| file | size | sha256 (start) | source |
|---|---|---|---|
| `undesa_pd_2019_wmd_marital_status.xlsx` | 26 MB | `aa85acb4fa66232d…` | UN World Marriage Data 2019 (POP/DB/Marr/Rev2019), www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2019_wmd_marital_status.xlsx |
| `undesa_pd_2026_living-arrangements-older-persons.xlsx` | 2.0 MB | `20d705e69f697f6f…` | UN Database on the Households and Living Arrangements of Older Persons 2026 |
| `undesa_pd_2026_hh-size-composition.xlsx` | 396 KB | `7687ad9c151f7c14…` | UN Database on Household Size and Composition 2026 (context only, not merged) |
| `un_locations.json` | 24 KB | `2de5cc72479fd597…` | UN Data Portal `/api/v1/locations` (M49 numeric code → ISO3) |
| `undesa_pd_2017_wmd_marital_status.xlsx` | 24 MB | — | UN World Marriage Data 2017, downloaded but not used |
| `owid_women-married-by-age-18.csv`, `owid_share-of-women-married-or-in-a-union.csv` | small | — | Our World in Data grapher exports, used only as cross-checks |

Full sha256 manifest on the server: `/root/work/undata/raw/SHA256SUMS.txt`.
The workbooks are UN material under CC BY 3.0 IGO; cite the UN Population
Division as in the README.
