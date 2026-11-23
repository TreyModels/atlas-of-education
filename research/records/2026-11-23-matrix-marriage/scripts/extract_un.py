#!/usr/bin/env python3
"""Extract the UN marriage and living-arrangement series we need from the raw
UN Population Division workbooks (streaming xlsx reader, fast).

Inputs (downloaded from www.un.org with a browser user-agent; see README):
  raw/undesa_pd_2019_wmd_marital_status.xlsx        UN World Marriage Data 2019
  raw/undesa_pd_2026_living-arrangements-older-persons.xlsx
  raw/un_locations.json                             UN portal M49-code -> ISO3 map
Outputs, one JSON list per series (rows = [ISO3, year, value]):
  smam_f, smam_m, smam_gap                   singulate mean age at marriage
  nevermar_f_4549, nevermar_m_4549           share never married at 45-49
  nevermar_f_4549_direct (cross-check)       same, from the "Never married" tabulation
  coresid_60plus, coresid_60plus_f           share of 60+ living with children aged 20+
  multigen_60plus                            share of 60+ in a multi-generation household
  alone_60plus                               share of 60+ living alone
plus *_provenance.csv, availability.csv and source_composition.csv.

Year convention: survey/census year = round((YearStart+YearEnd)/2); raw
YearStart/YearEnd are kept in the provenance files.  No interpolation anywhere.
The UN "DataProcess" field (Census / Survey / Estimate / ...) is preserved so the
share of model-based observations can be reported.
"""
import csv, json, os, re, zipfile
import xml.etree.ElementTree as ET

RAW = "/root/work/undata/raw"
OUT = "/root/work/undata/out"
WMD = os.path.join(RAW, "undesa_pd_2019_wmd_marital_status.xlsx")
HHLA = os.path.join(RAW, "undesa_pd_2026_living-arrangements-older-persons.xlsx")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}

meta = json.load(open("/root/work/data/meta.json"))
PANEL = {i for i, m in meta.items()
         if len(i) == 3 and m.get("region", "").strip() != "Aggregates"}
NUM2ISO = {int(r["id"]): r["iso3"] for r in
           json.load(open(os.path.join(RAW, "un_locations.json")))
           if r.get("iso3") and len(r["iso3"]) == 3}


def colnum(ref):
    s = re.match(r"([A-Z]+)", ref).group(1)
    n = 0
    for ch in s:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


_CACHE = {}


def _shared(zf, path):
    """Shared-string table, loaded once per workbook (loading it is expensive)."""
    key = (path, "shared")
    if key not in _CACHE:
        shared = []
        if "xl/sharedStrings.xml" in zf.namelist():
            with zf.open("xl/sharedStrings.xml") as f:
                for _, el in ET.iterparse(f):
                    if el.tag == "{%s}si" % NS["m"]:
                        texts = [t.text or "" for t in el.iter("{%s}t" % NS["m"])]
                        shared.append("".join(texts))
                        el.clear()
        _CACHE[key] = shared
    return _CACHE[key]


def _sheet_target(path, sheetname):
    key = (path, "sheets")
    if key not in _CACHE:
        zf = zipfile.ZipFile(path)
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rid2t = {r.get("Id"): r.get("Target") for r in rels}
        m = {}
        for s in wb.find("m:sheets", NS):
            t = rid2t[s.get("{%s}id" % NS["r"])]
            m[s.get("name")] = t.lstrip("/") if t.startswith("/") else "xl/" + t
        _CACHE[key] = m
    return _CACHE[key].get(sheetname)


def sheet_iter(path, sheetname):
    """Yield (row_number, values) from one xlsx sheet, streaming."""
    zf = zipfile.ZipFile(path)
    shared = _shared(zf, path)
    target = _sheet_target(path, sheetname)
    if target is None:
        raise KeyError(sheetname)
    with zf.open(target) as f:
        for _, el in ET.iterparse(f):
            if el.tag != "{%s}row" % NS["m"]:
                continue
            rownum = int(el.get("r")) if el.get("r") else None
            row = []
            for c in el.findall("m:c", NS):
                idx = colnum(c.get("r"))
                while len(row) <= idx:
                    row.append(None)
                t = c.get("t")
                v = c.find("m:v", NS)
                if t == "s":
                    val = shared[int(v.text)] if v is not None else None
                elif t == "inlineStr":
                    isel = c.find("m:is", NS)
                    val = ("".join(x.text or "" for x in isel.iter("{%s}t" % NS["m"]))
                           if isel is not None else None)
                else:
                    val = v.text if v is not None else None
                row[idx] = val
            yield rownum, row
            el.clear()


def midyear(ys, ye):
    try:
        ys, ye = int(float(ys)), int(float(ye))
    except (TypeError, ValueError):
        return None
    return ys if ys == ye else int(round((ys + ye) / 2.0))


def num(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def write_series(name, rows, provenance=None):
    keep, dropped = {}, 0
    for iso, yr, val in rows:
        if val is None or yr is None:
            continue
        try:
            val = float(val)
        except (TypeError, ValueError):
            continue
        if iso not in PANEL:
            dropped += 1
            continue
        keep.setdefault((iso, int(yr)), val)
    out = [[k[0], k[1], v] for k, v in sorted(keep.items())]
    json.dump(out, open(os.path.join(OUT, name + ".json"), "w"))
    print(f"{name:26s} rows={len(out):6d} countries={len({r[0] for r in out}):4d} "
          f"years={min((r[1] for r in out), default='-')}-{max((r[1] for r in out), default='-')} "
          f"non_panel_dropped={dropped}")
    if provenance:
        with open(os.path.join(OUT, name + "_provenance.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["country", "year", "value", "year_start", "year_end",
                        "data_process", "data_catalog", "detail"])
            w.writerows(provenance)
    return out


def rows_from(sheet, hdr_row):
    hdr, idx = None, None
    for n, row in sheet_iter(*sheet):
        if n is None or n < hdr_row:
            continue
        if n == hdr_row:
            hdr = [str(h).strip() if h is not None else "" for h in row]
            idx = {h: j for j, h in enumerate(hdr)}
            continue
        yield idx, row


def main():
    os.makedirs(OUT, exist_ok=True)

    # ---------- SMAM, with same-survey matching for the female-male gap ----------
    smam = {"Women": [], "Men": []}
    prov = {"Women": [], "Men": []}
    bygroup = {}
    for idx, r in rows_from((WMD, "SMAM"), 3):
        if not r or not r[idx["Country or area"]]:
            continue
        code = r[idx["ISO code"]]
        iso = NUM2ISO.get(int(float(code))) if code not in (None, "") else None
        country = str(r[idx["Country or area"]]).strip()
        sex = str(r[idx["Sex"]]).strip()
        val = num(r[idx["DataValue"]])
        ys, ye = r[idx["YearStart"]], r[idx["YearEnd"]]
        yr = midyear(ys, ye)
        proc = r[idx["DataProcess"]]
        cat = r[idx["DataCatalog ShortName"]]
        pv = [country, yr, val, ys, ye, proc, cat,
              str(r[idx["DataCatalog LongName"]])[:80]]
        bygroup.setdefault((country, ys, ye, cat), {})[sex] = (val, pv, iso)
        if sex in ("Women", "Female"):
            smam["Women"].append((iso, yr, val)); prov["Women"].append(pv)
        elif sex in ("Men", "Male"):
            smam["Men"].append((iso, yr, val)); prov["Men"].append(pv)
    write_series("smam_f", smam["Women"], prov["Women"])
    write_series("smam_m", smam["Men"], prov["Men"])
    gap, prov_g = [], []
    for (country, ys, ye, cat), d in bygroup.items():
        fem, male = d.get("Women"), d.get("Men")
        if not fem or not male or fem[0] is None or male[0] is None or fem[2] is None:
            continue
        yr = midyear(ys, ye)
        g = fem[0] - male[0]
        gap.append((fem[2], yr, g))
        prov_g.append([country, yr, g, ys, ye, fem[1][5], cat,
                       f"female SMAM {fem[0]} minus male SMAM {male[0]}"])
    write_series("smam_gap", gap, prov_g)

    # ---------- never married at 45-49: 100 - ever married (full coverage) ----------
    nm = {"Women": [], "Men": []}
    pv_nm = {"Women": [], "Men": []}
    for idx, r in rows_from((WMD, "EVER_MARRIED"), 3):
        if not r or not r[idx["Country or area"]]:
            continue
        if str(r[idx["AgeGroup"]]).strip() != "[45-49]":
            continue
        sex = str(r[idx["Sex"]]).strip()
        if sex not in nm:
            continue
        code = r[idx["ISO code"]]
        iso = NUM2ISO.get(int(float(code))) if code not in (None, "") else None
        ever = num(r[idx["DataValue"]])
        if ever is None or iso is None:
            continue
        never = 100.0 - ever
        if not (-0.01 <= never <= 100.01):
            continue
        ys, ye = r[idx["YearStart"]], r[idx["YearEnd"]]
        yr = midyear(ys, ye)
        nm[sex].append((iso, yr, never))
        pv_nm[sex].append([str(r[idx["Country or area"]]).strip(), yr, never, ys, ye,
                           r[idx["DataProcess"]], str(r[idx["DataCatalog ShortName"]]),
                           f"100 minus ever-married share at 45-49 ({ever})"])
    write_series("nevermar_f_4549", nm["Women"], pv_nm["Women"])
    write_series("nevermar_m_4549", nm["Men"], pv_nm["Men"])

    # ---------- cross-check: direct "Never married" tabulation ----------
    dn = {"Women": [], "Men": []}
    pv_dn = {"Women": [], "Men": []}
    for idx, r in rows_from((WMD, "MARITAL_STATUS_BY_AGE"), 3):
        if not r or not r[idx["Country or area"]]:
            continue
        if str(r[idx["AgeGroup"]]).strip() != "[45-49]":
            continue
        if str(r[idx["MaritalStatus"]]).strip().lower() != "never married":
            continue
        sex = str(r[idx["Sex"]]).strip()
        if sex not in dn:
            continue
        code = r[idx["ISO code"]]
        iso = NUM2ISO.get(int(float(code))) if code not in (None, "") else None
        val = num(r[idx["DataValue"]])
        if iso is None or val is None:
            continue
        ys, ye = r[idx["YearStart"]], r[idx["YearEnd"]]
        yr = midyear(ys, ye)
        dn[sex].append((iso, yr, val))
        pv_dn[sex].append([str(r[idx["Country or area"]]).strip(), yr, val, ys, ye,
                           r[idx["DataProcess"]], str(r[idx["DataCatalog ShortName"]]),
                           "direct share never married at 45-49"])
    write_series("nevermar_f_4549_direct", dn["Women"], pv_dn["Women"])
    write_series("nevermar_m_4549_direct", dn["Men"], pv_dn["Men"])

    # ---------- living arrangements of people aged 60+ ----------
    hh = "HHLA of Older Persons 2026"
    want = {"coresid_60plus": "With children aged 20 years or over",
            "multigen_60plus": "Multi-generation",
            "alone_60plus": "One person"}
    got, pv_hh = {}, {}
    for idx, r in rows_from((HHLA, hh), 5):
        if not r or not r[idx["Country and area"]]:
            continue
        iso = str(r[idx["ISO3 Code"]]).strip()
        sex = str(r[idx["Sex"]]).strip()
        if str(r[idx["Age range"]]).strip() not in ("60 or over", "60+"):
            continue
        yr = midyear(r[idx["Reference year"]], r[idx["Reference year"]])
        if yr is None:
            continue
        for name, col in want.items():
            if sex not in ("Both sexes", "Females"):
                continue
            v = num(r[idx[col]])
            if v is None:
                continue
            key = name if sex == "Both sexes" else name + "_f"
            got.setdefault(key, []).append((iso, yr, v))
            pv_hh.setdefault(key, []).append(
                [str(r[idx["Country and area"]]).strip(), yr, v, yr, yr,
                 str(r[idx["Data source category"]]),
                 str(r[idx["Data source catalog ID"]]),
                 str(r[idx["Data source detailed name"]])[:80]])
    for name in got:
        write_series(name, got[name], pv_hh[name])

    # ---------- availability + source composition ----------
    names = sorted(f[:-5] for f in os.listdir(OUT) if f.endswith(".json"))
    rows = []
    for name in names:
        d = json.load(open(os.path.join(OUT, name + ".json")))
        dec = {}
        for _, y, _ in d:
            dec[(y // 10) * 10] = dec.get((y // 10) * 10, 0) + 1
        rows.append([name, len(d), len({r[0] for r in d}),
                     min((r[1] for r in d), default=""),
                     max((r[1] for r in d), default=""),
                     " ".join(f"{k}:{v}" for k, v in sorted(dec.items()))])
    with open(os.path.join(OUT, "availability.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series", "observations", "countries", "first_year",
                    "last_year", "observations_by_decade"])
        w.writerows(rows)
    comp = []
    for name in names:
        p = os.path.join(OUT, name + "_provenance.csv")
        if not os.path.exists(p):
            continue
        cnt, n = {}, 0
        with open(p) as f:
            for row in csv.DictReader(f):
                n += 1
                k = (row.get("data_process") or "blank").strip()
                cnt[k] = cnt.get(k, 0) + 1
        comp.append([name, n] + [f"{k}:{v}" for k, v in
                                 sorted(cnt.items(), key=lambda kv: -kv[1])])
    with open(os.path.join(OUT, "source_composition.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series", "observations", "data_process_counts"])
        w.writerows(comp)

    # ---------- cross-check ever-married complement vs direct tabulation ----------
    xs = {(r[0], r[1]): r[2] for r in
          json.load(open(os.path.join(OUT, "nevermar_f_4549.json")))}
    dd = json.load(open(os.path.join(OUT, "nevermar_f_4549_direct.json")))
    diffs = sorted(abs(xs[(r[0], r[1])] - r[2]) for r in dd if (r[0], r[1]) in xs)
    with open(os.path.join(OUT, "crosscheck_nevermar_f.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["iso3", "year", "derived_100_minus_ever", "direct_never"])
        for r in dd:
            if (r[0], r[1]) in xs:
                w.writerow([r[0], r[1], xs[(r[0], r[1])], r[2]])
    print(f"cross-check never-married female: {len(diffs)} matched country-years, "
          f"median abs diff={diffs[len(diffs)//2] if diffs else float('nan'):.2f} pp, "
          f"max={diffs[-1] if diffs else float('nan'):.2f}")
    for r in rows:
        print("AVAIL", r)


if __name__ == "__main__":
    main()
