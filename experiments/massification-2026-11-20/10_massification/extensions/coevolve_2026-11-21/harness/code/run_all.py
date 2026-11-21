"""Run the whole COEVOLUTION v0 harness and emit one machine-readable result file.

Usage:  python harness/code/run_all.py
Writes: harness/out/verification_results.json, harness/SHA256SUMS.txt
Reads only delivered results + frozen contract; never re-runs the simulator.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C

SCRIPTS = [
    ("A", "verify_a_report_card.py"),
    ("B", "verify_b_coexistence.py"),
    ("C", "verify_c_counterfactuals.py"),
    ("D", "verify_d_spillback.py"),
    ("E", "verify_e_degrees.py"),
    ("F", "verify_f_integrity.py"),
]
SUMMARY = {"A": "A_summary.json", "B": "B_summary.json", "C": "C_summary.json",
           "D": "D_summary.json", "E": "E_summary.json", "F": "F_summary.json"}


def main():
    logs = {}
    for tag, script in SCRIPTS:
        print("=" * 78)
        print("running %s" % script)
        out = subprocess.run([sys.executable, os.path.join(HERE, script)],
                             capture_output=True, text=True)
        logs[tag] = out.stdout
        if out.returncode != 0:
            print(out.stdout[-2000:])
            print(out.stderr[-4000:], file=sys.stderr)
            return out.returncode
        print(out.stdout.strip()[-1200:])

    results = {"label": "SIMULATED",
               "harness": "COEVOLUTION v0 independent verification harness",
               "reads": "delivered results/ + PRE_DECLARATIONS.md + PARAMETERS.csv only",
               "re_ran_model": False,
               "predeclaration_sha256": C.sha256_file(C.PREDECL_PATH),
               "checks": {}, "verdicts": {"pass": 0, "fail": 0, "descriptive": 0}}
    for tag, _ in SCRIPTS:
        with open(os.path.join(C.OUT, SUMMARY[tag])) as fh:
            doc = json.load(fh)
        results["checks"][tag] = doc["checks"]
        for c in doc["checks"]:
            v = str(c.get("verdict", ""))
            if v.startswith("PASS") or v in ("DEFECT-CONFIRMED", "ACCEPTED-EVIDENCE",
                                             "DESCRIPTIVE", "NOT-CHECKED"):
                key = ("pass" if v.startswith("PASS") else
                       "descriptive")
            elif v.startswith("FAIL"):
                key = "fail"
            else:
                key = "descriptive"
            results["verdicts"][key] += 1

    with open(os.path.join(C.OUT, "verification_results.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
        fh.write("\n")

    # harness hashes: code + outputs + the two report files it supports
    lines = ["%s  ../FINDINGS.md" % C.sha256_file(os.path.join(C.EXT, "FINDINGS.md")),
             "%s  ../HARNESS_VERIFICATION.md" % C.sha256_file(os.path.join(C.EXT, "HARNESS_VERIFICATION.md"))]
    for base in (os.path.join(C.EXT, "harness", "code"), os.path.join(C.EXT, "harness", "out")):
        for name in sorted(os.listdir(base)):
            if name.startswith(".") or name == "SHA256SUMS.txt":
                continue
            path = os.path.join(base, name)
            if os.path.isfile(path):
                lines.append("%s  %s" % (C.sha256_file(path),
                                         os.path.relpath(path, os.path.join(C.EXT, "harness"))))
    with open(os.path.join(C.EXT, "harness", "SHA256SUMS.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    print("=" * 78)
    print("checks: pass=%d fail=%d descriptive=%d"
          % (results["verdicts"]["pass"], results["verdicts"]["fail"],
             results["verdicts"]["descriptive"]))
    print("wrote harness/out/verification_results.json and harness/SHA256SUMS.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
