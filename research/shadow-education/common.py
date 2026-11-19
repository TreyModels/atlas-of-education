"""Shared helpers. The tutoring model itself is NOT copied here: it is imported unchanged from
experiments/shadow-abm/src/tutoring_abm/model.py, so these experiments test the model as it stands."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ABM = HERE.parents[1] / "experiments" / "shadow-abm" / "src" / "tutoring_abm"
sys.path.insert(0, str(ABM))
from model import Params, PRIORS, VARIANTS, World, run  # noqa: E402
from calibrate import TARGETS, COM_MAX  # noqa: E402

RESULTS = HERE / "results"
VARIANT_NAMES = ["thin", "diversion", "favour", "full"]
PARAM_NAMES = list(PRIORS)
# The seven published patterns plus the commercial share, as the calibration measures them.
MEASURED = ["participation", "participation_g9", "participation_g12", "urban_rural_gap",
            "own_purchase_share", "other_purchase_share", "teacher_tutor_share", "com_purchase_share"]
TOL = {**{k: tol for k, (_, tol) in TARGETS.items()}, "com_purchase_share": 0.05}


def load_particles(variant):
    """Fitted parameter sets stored by the repo's ABC-SMC run. Returns (list of Params, group ids).
    Resampling leaves duplicates, so identical parameter sets share a group id."""
    d = json.loads((ABM / "results" / f"posterior_{variant}.json").read_text())
    params, keys = [], []
    for row in d["particles"]:
        values = {k: row.get(k, 0.0) for k in PARAM_NAMES}
        params.append(Params(**values))
        keys.append(tuple(round(values[k], 12) for k in PARAM_NAMES))
    ids = {k: i for i, k in enumerate(dict.fromkeys(keys))}
    return params, [ids[k] for k in keys]


def with_gap(o):
    return dict(o, urban_rural_gap=o["participation_urban"] - o["participation_rural"])
