#!/usr/bin/env python3
"""Documented attempts to reach DHS individual-level microdata from box2 (23 Nov 2026).
Every attempt and its HTTP outcome is saved to /root/work/dhs/data/microdata_probe.txt."""
import urllib.request, datetime
out = []
def rec(s):
    out.append(s); print(s)
rec("DHS individual-level microdata probing, box2, " + datetime.datetime.utcnow().isoformat() + "Z")
urls = [
 ("DHS API indicators (aggregates only)", "https://api.dhsprogram.com/rest/dhs/indicators?returnFormat=json&f=json"),
 ("DHS API datasets metadata (file names and sizes; no download link)", "https://api.dhsprogram.com/rest/dhs/datasets?returnFormat=json&f=json&perpage=5"),
 ("DHS dataset by flat-file name (returns the metadata list, not the file)", "https://api.dhsprogram.com/rest/dhs/datasets/AFIR66FL.ZIP?returnFormat=json&f=json"),
 ("DHS direct flat-file URL /data/dataset/AFIR66FL.ZIP", "https://dhsprogram.com/data/dataset/AFIR66FL.ZIP"),
 ("DHS direct flat-file URL /data/AFIR66FL.ZIP", "https://dhsprogram.com/data/AFIR66FL.ZIP"),
 ("DHS dataset landing page (account login required for download)", "https://dhsprogram.com/data/dataset/Bangladesh_Standard-DHS_2017.cfm"),
 ("IPUMS-DHS landing", "https://www.idhsdata.org/idhs/"),
 ("IPUMS API extract endpoint (requires key)", "https://api.ipums.org/extracts/?collection=dhs"),
 ("Zenodo search API for DHS recode", "https://zenodo.org/api/records?q=DHS%20individual%20recode&size=5"),
 ("Harvard Dataverse search for DHS individual recode", "https://dataverse.harvard.edu/api/search?q=DHS%20individual%20recode&per_page=5"),
]
for name, u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        r = urllib.request.urlopen(req, timeout=30)
        ctype = r.headers.get("Content-Type")
        body = r.read(300)
        rec("ATTEMPT " + name + ": HTTP " + str(r.status) + ", type " + str(ctype) + ", first bytes " + repr(body[:120]))
    except Exception as e:
        rec("ATTEMPT " + name + ": ERROR " + str(e))
open("/root/work/dhs/data/microdata_probe.txt", "w").write("\n".join(out) + "\n")
