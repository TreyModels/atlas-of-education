"""Shared loaders/constants for the COEVOLUTION v0 harness.

Reads ONLY the delivered files under results/ and the frozen PRE_DECLARATIONS.md /
PARAMETERS.csv. Never writes outside harness/. Every derived number is labelled
SIMULATED (model) or DERIVED (arithmetic on SIMULATED).
"""
import csv
import hashlib
import json
import os

EXT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(EXT, "results")
OUT = os.path.join(EXT, "harness", "out")
PARAM_PATH = os.path.join(EXT, "PARAMETERS.csv")
PREDECL_PATH = os.path.join(EXT, "PRE_DECLARATIONS.md")

ARMS = ["baseline", "travel_cut", "ordinary_expansion", "selective_expansion",
        "mandate_before_funding", "fees_abolished", "degrees_outrun_jobs", "spillback"]
SEEDS = [20261121, 20261122, 20261123]
COUNTERFACTUAL_ARMS = ["travel_cut", "ordinary_expansion", "selective_expansion"]
REPORT_B_ARMS = ["mandate_before_funding", "fees_abolished", "degrees_outrun_jobs"]

# declared level taxonomy of the simulator (code/coevolve_v0.py lines 50-57)
LEVELS = ["primary", "lower_secondary", "upper_secondary", "upper_selective",
          "post_secondary_non_tertiary", "tertiary"]
BAND = {"primary": (6, 11), "lower_secondary": (12, 15), "upper_secondary": (16, 17),
        "upper_selective": (16, 17), "post_secondary_non_tertiary": (18, 19),
        "tertiary": (18, 22)}
# §7: five-year age group immediately after the official secondary leaving age (17)
SECONDARY_LEAVING_AGE = 17
TERTIARY_BAND = (18, 22)
LEVEL_ORD = {"primary": 0, "lower_secondary": 1, "upper_secondary": 2,
             "upper_selective": 2, "post_secondary_non_tertiary": 3, "tertiary": 4}

# declared population frame (§1, PARAMETERS.csv)
TOWN_COHORT = 320
VILLAGE_SIZES = [176, 150, 132, 114, 97, 79, 70, 62]
COHORT_SIZE = 1200
N_BURNIN = 11
N_COHORTS = 24
T0, T1 = -N_BURNIN, N_COHORTS - 1
SAMPLE_MOD = 32

FAMILY_TYPES = [("town", 0), ("town", 1), ("village", 0), ("village", 1)]

TOL_IDENTITY = 1e-9     # %.10g round-trip tolerance for ratios / means
TOL_EXACT = 5e-9        # recomputation of a delivered table from pupil records
TOL_CORR = 1e-8


# ---------------------------------------------------------------------------
def read_csv(name):
    with open(os.path.join(RES, name), newline="") as fh:
        return list(csv.DictReader(fh))


def read_json(name):
    with open(os.path.join(RES, name)) as fh:
        return json.load(fh)


def load_params():
    out = {}
    with open(PARAM_PATH, newline="") as fh:
        for row in csv.DictReader(fh):
            out[row["name"]] = row["value"]
    return out


def params():
    return load_params()


def pfloat(P, key):
    return float(P[key])


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# pupil_id -> declared population frame.  pupil ids are assigned per entry year
# in blocks of cohort_size, town first, then villages by declared size; the age of
# a child in year t is 6 + (t - entry_year).  This lets the harness recover the
# age band and location of *every* sampled pupil-year row (including burn-in
# cohorts that are not in panel_*.csv), and it is validated against the panel.
# ---------------------------------------------------------------------------
_CUM = [TOWN_COHORT]
for _s in VILLAGE_SIZES:
    _CUM.append(_CUM[-1] + _s)


def loc_of_ids(ids):
    """0 = town, 1..8 = village (declared id layout)."""
    out = []
    for i in ids:
        pos = int(i) % COHORT_SIZE
        loc = 0
        for k in range(1, len(_CUM)):
            if pos >= _CUM[k - 1]:
                loc = k
        out.append(loc)
    return out


def entry_of_ids(ids):
    return [T0 + int(i) // COHORT_SIZE for i in ids]


class Panel:
    """panel_<arm>.csv with the id-derived frame columns added."""

    def __init__(self, arm):
        self.arm = arm
        self.rows = read_csv("panel_%s.csv" % arm)
        self.n = len(self.rows)
        self._derive()

    def _derive(self):
        for r in self.rows:
            pid = int(r["pupil_id"])
            r["_entry"] = entry_of_ids([pid])[0]
            r["_loc"] = loc_of_ids([pid])[0]
            r["_rural"] = 1 if r["_loc"] > 0 else 0
            r["_poor"] = int(r["poor"])
            r["_yc"] = int(r["years_completed"])
            for k in ("completed_primary_year", "completed_lower_year",
                      "completed_upper_year", "completed_postsec_year",
                      "completed_tertiary_year", "exit_year", "years_attended",
                      "repeat_count", "attended_secondary", "selective_admitted",
                      "selective_attended", "final_credential", "cohort_entry_year"):
                if k in r:
                    r["_" + k] = int(r[k])
            for k in ("catchup_hours", "gate_hours", "mastery_final"):
                r["_" + k] = float(r[k])

    def by(self, key):
        d = {}
        for r in self.rows:
            d.setdefault(r[key], []).append(r)
        return d

    def seed_rows(self, seed):
        return [r for r in self.rows if int(r["seed"]) == seed]


def arms_panels(arms=None):
    return {a: Panel(a) for a in (arms or ARMS)}


def agg_rows(arm):
    return read_csv("aggregates_%s.csv" % arm)


def cohort_rows(arm):
    return read_csv("cohorts_%s.csv" % arm)


def coex_rows(arm):
    return read_csv("coexistence_%s.csv" % arm)


def family_rows(arm):
    return read_csv("families_%s.csv" % arm)


def write_csv(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return path


def write_json(name, obj):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return path
