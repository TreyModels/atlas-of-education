#!/usr/bin/env python3
"""Verify the port's transcribed sim_step against the REAL CUDA kernel.

The T4 reference capture (``cuda_reference/cuda_kernel_dump.npz`` + manifest) holds
10 launches of the unmodified CUDA ``sim_step``: 5 DGPs x (t=0, t=12), fixed seed
20261125, N=10,000, threads=256, blocks=40, with the *inputs* (base_y, ability)
saved exactly as the CUDA run received them. Feeding those saved inputs to the
NumPy and MLX transcriptions isolates the kernel: the data-generation stream is
identical by construction, so any difference is transcription error.

Declared tolerances (PRE_REGISTRATION.md §4):
  * integer arrays (state, tutor): exact, 0 differing households;
  * float arrays (learn, work, y_hh): max abs <= 1e-5 and max rel <= 1e-4
    (rel evaluated where |ref| > 1e-6).
If integers differ, that is reported as a real state change -- not waved through.

Writes ``results/cuda_vs_transcription.json``.
"""
import json
import os
import sys

import numpy as np

RECORD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RECORD)

from kernels_np_mlx import run_sim_step_arrays  # noqa: E402

REF_DIR = os.path.join(RECORD, "cuda_reference")
RESULTS = os.path.join(RECORD, "results")
ABS_TOL = 1e-5
REL_TOL = 1e-4
REL_FLOOR = 1e-6
INT_ARRAYS = ("state", "tutor")
FLOAT_ARRAYS = ("learn", "work", "y_hh")


def _version(module):
    try:
        return getattr(__import__(module), "__version__", None)
    except Exception:
        return None


def int_metrics(ref, cand):
    ref = np.asarray(ref)
    cand = np.asarray(cand)
    return int(np.sum(ref != cand))


def float_metrics(ref, cand):
    ref = np.asarray(ref, dtype=np.float64)
    cand = np.asarray(cand, dtype=np.float64)
    adiff = np.abs(ref - cand)
    max_abs = float(adiff.max()) if adiff.size else 0.0
    mask = np.abs(ref) > REL_FLOOR
    max_rel = float((adiff[mask] / np.abs(ref[mask])).max()) if np.any(mask) else 0.0
    return max_abs, max_rel


def main():
    npz_path = os.path.join(REF_DIR, "cuda_kernel_dump.npz")
    man_path = os.path.join(REF_DIR, "cuda_kernel_dump_manifest.json")
    if not (os.path.exists(npz_path) and os.path.exists(man_path)):
        print(f"MISSING CUDA DUMP: {npz_path}")
        raise SystemExit(2)
    npz = np.load(npz_path)
    manifest = json.load(open(man_path))
    n_launches = len(manifest["launches"])

    have_mlx = True
    try:
        import mlx.core  # noqa: F401
    except Exception as exc:  # pragma: no cover
        have_mlx = False
        print(f"[verify_cuda_kernel] MLX unavailable ({exc}); NumPy transcription only")
    backends = ["numpy"] + (["mlx"] if have_mlx else [])

    report = {
        "cuda_dump": "cuda_reference/cuda_kernel_dump.npz",
        "cuda_dump_sha256": manifest.get("npz_sha256"),
        "cuda_capture": {
            "gpu": "Tesla T4 (16 GB), driver 565.57.01, CUDA 12.7",
            "n": manifest.get("n"), "seed": manifest.get("seed"),
            "threads": manifest.get("threads"), "blocks": manifest.get("blocks"),
            "n_launches": len(manifest["launches"]),
            "cupy": manifest.get("cupy"), "numpy": manifest.get("numpy"),
            "data_stream": manifest.get("data_stream"),
        },
        "port_environment": {
            "interpreter": sys.executable,
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "mlx": _version("mlx.core"),
        },
        "tolerance": {"int_mismatches": 0, "float_max_abs": ABS_TOL,
                      "float_max_rel": REL_TOL, "rel_floor": REL_FLOOR},
        "results": [],
        "summary": {},
    }

    n_pass = n_fail = 0
    int_total = 0
    max_abs_overall = 0.0
    max_rel_overall = 0.0
    print(f"CUDA KERNEL vs TRANSCRIPTION ({n_launches} launches, "
          f"N={manifest['n']}, seed={manifest['seed']}, backends={backends})")
    print(f"{'launch':28s} {'backend':7s} {'int_diff':>8s} {'max_abs':>12s} {'max_rel':>12s}  pass")
    for launch in manifest["launches"]:
        key = launch["key"]
        base_y = npz["base_y"]
        ability = npz["ability"]
        args = (manifest["n"], launch["year"], launch["seed0"], launch["seed1"],
                launch["f_pub"], launch["h_hidden"], launch["psi"], launch["ban"],
                launch["q_pub"], launch["diversion_beta"], launch["w_child"],
                launch["y_sub"], launch["shadow_cost"], launch["w_pov"],
                launch["w_push"], launch["w_tutor"], base_y, ability)
        for backend in backends:
            out = run_sim_step_arrays(backend, args)
            entry = {"launch": key, "backend": backend,
                     "dgp": launch["dgp"], "year": launch["year"], "int": {}, "float": {}}
            ok = True
            for name in INT_ARRAYS:
                ref = npz[f"{name}_{key}"]
                n_diff = int_metrics(ref, out[name])
                entry["int"][name] = n_diff
                int_total += n_diff
                ok = ok and n_diff == 0
            for name in FLOAT_ARRAYS:
                ref = npz[f"{name}_{key}"]
                max_abs, max_rel = float_metrics(ref, out[name])
                entry["float"][name] = {"max_abs": max_abs, "max_rel": max_rel}
                max_abs_overall = max(max_abs_overall, max_abs)
                max_rel_overall = max(max_rel_overall, max_rel)
                ok = ok and (max_abs <= ABS_TOL) and (max_rel <= REL_TOL)
            entry["pass"] = bool(ok)
            n_pass += int(ok)
            n_fail += int(not ok)
            report["results"].append(entry)
            ints = entry["int"]
            print(f"{key:28s} {backend:7s} {sum(ints.values()):8d} "
                  f"{max(v['max_abs'] for v in entry['float'].values()):12.3e} "
                  f"{max(v['max_rel'] for v in entry['float'].values()):12.3e}  {ok}")

    report["summary"] = {
        "n_launches": len(manifest["launches"]) * len(backends),
        "n_pass": n_pass, "n_fail": n_fail,
        "int_mismatches_total": int_total,
        "max_abs_overall": max_abs_overall,
        "max_rel_overall": max_rel_overall,
        "verdict": "PASS" if n_fail == 0 else "FAIL",
        "note": ("Inputs are the CUDA run's own saved base_y/ability, so this isolates the "
                 "transcription; the port's data-generation stream is not involved. "
                 "PORT-PROVENANCE test, not a research result."),
    }
    os.makedirs(RESULTS, exist_ok=True)
    out_path = os.path.join(RESULTS, "cuda_vs_transcription.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nCUDA vs TRANSCRIPTION: {report['summary']['verdict']} "
          f"({n_pass}/{n_pass + n_fail} launches; int mismatches={int_total}; "
          f"max_abs={max_abs_overall:.3e}; max_rel={max_rel_overall:.3e})")
    print(f"report: {out_path}")
    if n_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
