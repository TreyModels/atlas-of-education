#!/usr/bin/env python3
"""Pull the historical series for the US (and other early industrialisers) sequencing test.

Network-bound job: started before any analysis so it can run while the battery job owns the CPU.
Sources (all public, fetched with a browser user-agent; OWID grapher CSV endpoints are reachable from box2):
  - OWID long-run share of employment in agriculture (Herrendorf-Rogerson / OWID)
  - OWID long-run fertility (children per woman)
  - OWID long-run mean years of schooling
  - OWID secondary/primary attainment and school-enrolment long-run series where available
Raw files are saved under /root/work/subsistence_v2/data/raw/; the extract used for the test is written to
/root/work/subsistence_v2/data/us_history.csv with provenance in us_history_sources.txt.
"""
import csv, io, json, os, time, urllib.request

OUT = "/root/work/subsistence_v2/data"
RAW = f"{OUT}/raw"
os.makedirs(RAW, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
SERIES = {
    "ag_employment_share": "https://ourworldindata.org/grapher/share-of-employment-in-agriculture.csv?v=1&csvType=full&useColumnShortNames=true",
    "fertility": "https://ourworldindata.org/grapher/fertility-rate-complete-gapminder.csv?v=1&csvType=full&useColumnShortNames=true",
    "schooling_years": "https://ourworldindata.org/grapher/mean-years-of-schooling-long-run.csv?v=1&csvType=full&useColumnShortNames=true",
    "ag_output_per_worker": "https://ourworldindata.org/grapher/agricultural-output-per-worker.csv?v=1&csvType=full&useColumnShortNames=true",
    "primary_attainment": "https://ourworldindata.org/grapher/share-of-population-with-completed-primary-education.csv?v=1&csvType=full&useColumnShortNames=true",
}


def fetch(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            print("retry", k, url[:80], e, flush=True)
            time.sleep(3 + 3 * k)
    return None


if __name__ == "__main__":
    log = []
    frames = {}
    for name, url in SERIES.items():
        body = fetch(url)
        if not body:
            log.append(f"FAILED {name} {url}")
            print("FAILED", name, flush=True)
            continue
        open(f"{RAW}/{name}.csv", "w").write(body)
        rows = list(csv.reader(io.StringIO(body)))
        log.append(f"OK {name}: {len(rows) - 1} rows, columns {rows[0][:4]}")
        print("OK", name, len(rows) - 1, rows[0][:4], flush=True)
        frames[name] = rows
    open(f"{OUT}/us_history_sources.txt", "w").write("\n".join(log) + "\n")
    print("done", flush=True)
