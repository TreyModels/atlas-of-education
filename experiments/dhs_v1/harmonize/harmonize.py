#!/usr/bin/env python3
"""DHS -> README normalized schema harmonizer for the eight-experiment starter.

Writes unit-level normalized CSVs to a LOCAL-ONLY directory (default
~/neon-boot/dhs8_local/normalized). Raw microdata and these outputs are DHS
restricted data: they must never be committed to the repo or sent to the box.

Every non-obvious recode is asserted at runtime; if an assertion fails for a
file, that file's adapter is recorded as INVALID and no CSV is written.

Usage: harmonize.py --out DIR [--only TAG ...]
"""
import argparse, hashlib, json, os, sys, warnings
import numpy as np
import pandas as pd
import pyreadstat

warnings.filterwarnings("ignore")

RAW = os.path.expanduser("~/neon-boot/pulled/dhs")
DEFAULT_OUT = os.path.expanduser("~/neon-boot/dhs8_local/normalized")
MANIFEST = os.path.expanduser("~/neon-boot/dhs8_local/manifest.json")

# ---------------------------------------------------------------------------
# Adapters. `att_code` is the HV121 value that means "currently attending in
# the current school year"; it is wave-specific and is *empirically* verified
# below (see check_attendance_code) before use.
# ---------------------------------------------------------------------------
PERSON = {
    "KH-2000":    dict(rel="cambodia/2000/KHPR42SD/KHPR42FL.SAS7BDAT",      att_code=1, wealth=True),
    "KH-2005":    dict(rel="cambodia/2005/KHPR51SD/KHPR51FL.SAS7BDAT",      att_code=2, wealth=True),
    "KH-2010":    dict(rel="cambodia/2010/KHPR61SD/KHPR61FL.SAS7BDAT",      att_code=2, wealth=True),
    "KH-2014":    dict(rel="cambodia/2014/KHPR73SD/KHPR73FL.SAS7BDAT",      att_code=2, wealth=True),
    "KH-2021-22": dict(rel="cambodia/2021-22/KHPR82SD/KHPR82FL.SAS7BDAT",   att_code=2, wealth=True),
    "ID-2017":    dict(rel="indonesia/2017/IDPR71DT/IDPR71FL.DTA",          att_code=2, wealth=True),
    "PH-2017":    dict(rel="philippines/2017/PHPR71SD/PHPR71FL.SAS7BDAT",   att_code=2, wealth=True),
    "PH-2022":    dict(rel="philippines/2022/PHPR82DT/PHPR82FL.DTA",        att_code=2, wealth=True),
}
# PH-2003 is deliberately absent: HV022 (variance stratum) is entirely missing in
# that file, so no design-based SE can be computed. Documented as BLOCKED.

WOMAN = {
    "KH-2000":    dict(rel="cambodia/2000/KHIR42SD/KHIR42FL.SAS7BDAT"),
    "KH-2005":    dict(rel="cambodia/2005/KHIR51SD/KHIR51FL.SAS7BDAT"),
    "KH-2010":    dict(rel="cambodia/2010/KHIR61SD/KHIR61FL.SAS7BDAT"),
    "KH-2014":    dict(rel="cambodia/2014/KHIR73SD/KHIR73FL.SAS7BDAT"),
    "KH-2021-22": dict(rel="cambodia/2021-22/KHIR82SD/KHIR82FL.SAS7BDAT"),
    "PH-2022":    dict(rel="philippines/2022/PHIR82DT/PHIR82FL.DTA"),
}

SCHEMA = ["country", "wave", "weight", "stratum", "psu", "record_type", "age",
          "sex", "urban", "wealth", "attendance", "school_years",
          "children_ever_born", "age_first_birth", "currently_in_school",
          "age_first_union", "household_size"]

DK_CODES = [95, 96, 97, 98, 99]          # DHS "don't know / inconsistent" block


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def loader(path):
    return pyreadstat.read_dta if path.lower().endswith(".dta") else pyreadstat.read_sas7bdat


def read_cols(path, wanted):
    """Read `wanted` (lowercase canonical names) mapping to the file's real names."""
    f = loader(path)
    _, meta = f(path, metadataonly=True)
    lookup = {n.lower(): n for n in meta.column_names}
    present = {w: lookup[w] for w in wanted if w in lookup}
    missing = [w for w in wanted if w not in lookup]
    df, _ = f(path, usecols=list(present.values()))
    df = df.rename(columns={v: k for k, v in present.items()})
    for m in missing:
        df[m] = np.nan
    return df, missing


def check_attendance_code(df, declared):
    """Prove that `declared` is 'currently attending': ~0 share at ages 25-49,
    and a large share at ages 9-14. Returns (ok, evidence dict)."""
    a = df["hv105"]
    base = df[df["hv121"].notna()]
    share_older = float((base.loc[base["hv105"].between(25, 49), "hv121"] == declared).mean())
    peak = float((base.loc[base["hv105"].between(9, 14), "hv121"] == declared).mean())
    ok = (share_older < 0.02) and (peak > 0.50)
    return ok, dict(declared_code=declared, share_ages_25_49=round(share_older, 5),
                    share_ages_9_14=round(peak, 4), rule="ok if <2% at 25-49 and >50% at 9-14")


def check_never_semantics(ir):
    """Prove blank V212 == verified never-birth and blank V511 == verified never-union.
    Returns (ok212, ok511, evidence)."""
    blank212 = ir["v212"].isna()
    parous = ir["v201"] > 0
    viol212 = int((blank212 & parous).sum() + (~blank212 & ~parous).sum())
    blank511 = ir["v511"].isna()
    never_union = ir["v501"] == 0
    viol511 = int((blank511 & ~never_union).sum() + (~blank511 & never_union).sum())
    return viol212 == 0, viol511 == 0, dict(
        v212_blank_equals_ceb0_violations=viol212,
        v511_blank_equals_never_union_violations=viol511,
        rule="blank encodes a verified never-state only if violations==0")


def z(x):
    return pd.to_numeric(x, errors="coerce")


def clean_school_years(s):
    s = z(s)
    return s.where(~s.isin(DK_CODES))


def build_person(tag, spec):
    path = os.path.join(RAW, spec["rel"])
    cols = ["hv005", "hv021", "hv022", "hv024", "hv025", "hv104", "hv105",
            "hv108", "hv121", "hv270", "hv009", "hv001", "hv002", "hvidx"]
    df, missing = read_cols(path, cols)
    ev = {"adapter": "person", "raw": os.path.relpath(path, RAW), "missing_cols": missing}

    ok, attev = check_attendance_code(df, spec["att_code"])
    ev["attendance_check"] = attev
    if not ok:
        return None, dict(tag=tag, status="INVALID", reason="attendance code check failed", evidence=ev)
    if df["hv022"].isna().all() or df["hv021"].isna().all():
        return None, dict(tag=tag, status="INVALID", reason="stratum or psu entirely missing", evidence=ev)

    n = len(df)
    out = pd.DataFrame(index=df.index)
    out["country"] = tag.split("-")[0]
    out["wave"] = tag.split("-", 1)[1]
    out["weight"] = z(df["hv005"])
    out["stratum"] = z(df["hv022"]).astype("Int64").astype(str)
    out["psu"] = z(df["hv021"]).astype("Int64").astype(str)
    out["record_type"] = "person"
    out["age"] = z(df["hv105"])
    out["sex"] = z(df["hv104"])
    u = z(df["hv025"])
    out["urban"] = np.where(u == 1, 1, np.where(u == 2, 0, np.nan))
    out["wealth"] = z(df["hv270"]) if spec["wealth"] else np.nan
    att = z(df["hv121"])
    out["attendance"] = np.where(att.isna(), np.nan, (att == spec["att_code"]).astype(float))
    out["school_years"] = clean_school_years(df["hv108"])
    out["children_ever_born"] = np.nan          # not carried by PR recodes
    out["age_first_birth"] = np.nan             # not carried by PR recodes
    out["currently_in_school"] = out["attendance"]
    out["age_first_union"] = np.nan             # not carried by PR recodes
    out["household_size"] = z(df["hv009"])

    uid = (out["stratum"] + "-" + out["psu"] + "-" +
           z(df["hv001"]).astype("Int64").astype(str) + "-" +
           z(df["hv002"]).astype("Int64").astype(str) + "-" +
           z(df["hvidx"]).astype("Int64").astype(str))
    dups = int(uid.duplicated().sum())
    g = df.groupby("hv022")["hv021"].nunique()
    ev.update(dict(n_rows=n, weights_sum=float(out["weight"].sum()), weight_min=float(out["weight"].min()),
                   weight_nonpositive=int((out["weight"] <= 0).sum()),
                   n_strata=int(out["stratum"].nunique()), n_psu=int(out["psu"].nunique()),
                   singleton_strata=int((g == 1).sum()), dup_ids_within_stratum=dups,
                   psu_label_shared_across_strata=int(df.groupby("hv021")["hv022"].nunique().gt(1).sum()),
                   hv121_missing=int(att.isna().sum()),
                   school_years_missing=int(out["school_years"].isna().sum()),
                   wealth_missing=int(pd.isna(out["wealth"]).sum())))
    if dups:
        return None, dict(tag=tag, status="INVALID", reason=f"{dups} duplicate ids within strata", evidence=ev)
    return out[SCHEMA], dict(tag=tag, status="ok", evidence=ev, sha256=sha256(path),
                             bytes=os.path.getsize(path))


def build_woman(tag, spec):
    path = os.path.join(RAW, spec["rel"])
    cols = ["v005", "v021", "v022", "v024", "v025", "v012", "v133", "v136",
            "v201", "v212", "v501", "v511", "v001", "v002", "v003"]
    df, missing = read_cols(path, cols)
    ev = {"adapter": "woman", "raw": os.path.relpath(path, RAW), "missing_cols": missing}

    ok212, ok511, never_ev = check_never_semantics(df)
    ev["never_semantics"] = never_ev
    if not (ok212 and ok511):
        return None, dict(tag=tag, status="INVALID",
                          reason="blank-never semantics not proven; refusing to guess",
                          evidence=ev)
    if df["v022"].isna().all() or df["v021"].isna().all():
        return None, dict(tag=tag, status="INVALID", reason="stratum or psu entirely missing", evidence=ev)

    n = len(df)
    out = pd.DataFrame(index=df.index)
    out["country"] = tag.split("-")[0]
    out["wave"] = tag.split("-", 1)[1]
    out["weight"] = z(df["v005"])
    out["stratum"] = z(df["v022"]).astype("Int64").astype(str)
    out["psu"] = z(df["v021"]).astype("Int64").astype(str)
    out["record_type"] = "woman"
    out["age"] = z(df["v012"])
    out["sex"] = 2
    u = z(df["v025"])
    out["urban"] = np.where(u == 1, 1, np.where(u == 2, 0, np.nan))
    out["wealth"] = np.nan                        # v190 not needed by E4-E8
    out["attendance"] = np.nan                    # IR carries no attendance item
    out["school_years"] = clean_school_years(df["v133"])
    out["children_ever_born"] = z(df["v201"])
    # blank == verified never (proven above), so encode as 99 as the README requires
    out["age_first_birth"] = z(df["v212"]).fillna(99)
    out["currently_in_school"] = np.nan
    out["age_first_union"] = z(df["v511"]).fillna(99)
    out["household_size"] = z(df["v136"])

    uid = (out["stratum"] + "-" + out["psu"] + "-" +
           z(df["v001"]).astype("Int64").astype(str) + "-" +
           z(df["v002"]).astype("Int64").astype(str) + "-" +
           z(df["v003"]).astype("Int64").astype(str))
    dups = int(uid.duplicated().sum())
    g = df.groupby("v022")["v021"].nunique()
    ev.update(dict(n_rows=n, weights_sum=float(out["weight"].sum()), weight_min=float(out["weight"].min()),
                   weight_nonpositive=int((out["weight"] <= 0).sum()),
                   n_strata=int(out["stratum"].nunique()), n_psu=int(out["psu"].nunique()),
                   singleton_strata=int((g == 1).sum()), dup_ids_within_stratum=dups,
                   psu_label_shared_across_strata=int(df.groupby("v021")["v022"].nunique().gt(1).sum()),
                   school_years_missing=int(out["school_years"].isna().sum()),
                   age_first_birth_never=int((out["age_first_birth"] == 99).sum()),
                   age_first_union_never=int((out["age_first_union"] == 99).sum())))
    if dups:
        return None, dict(tag=tag, status="INVALID", reason=f"{dups} duplicate ids within strata", evidence=ev)
    return out[SCHEMA], dict(tag=tag, status="ok", evidence=ev, sha256=sha256(path),
                             bytes=os.path.getsize(path))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    manifest = {}
    for kind, table, builder in (("person", PERSON, build_person), ("woman", WOMAN, build_woman)):
        for tag, spec in table.items():
            if args.only and tag not in args.only:
                continue
            key = f"{tag}:{kind}"
            try:
                df, meta = builder(tag, spec)
            except Exception as e:
                manifest[key] = dict(tag=tag, kind=kind, status="ERROR",
                                     reason=f"{type(e).__name__}: {str(e)[:200]}")
                print(f"ERROR {key}: {type(e).__name__}: {e}")
                continue
            if df is None:
                manifest[key] = dict(kind=kind, **meta)
                print(f"SKIP  {key}: {meta['reason']}")
                continue
            fname = f"{tag}_{kind}.csv"
            dest = os.path.join(args.out, fname)
            df.to_csv(dest, index=False)
            meta.update(dest=fname, out_sha256=sha256(dest),
                        cells={c: int(df[c].notna().sum()) for c in SCHEMA})
            manifest[key] = dict(kind=kind, **meta)
            print(f"OK    {key}: n={len(df)} -> {fname}")

    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    print(f"\nmanifest: {MANIFEST}")
    bad = [k for k, v in manifest.items() if v.get("status") != "ok"]
    print(f"ok={len(manifest)-len(bad)} not-ok={len(bad)} {bad if bad else ''}")


if __name__ == "__main__":
    main()
