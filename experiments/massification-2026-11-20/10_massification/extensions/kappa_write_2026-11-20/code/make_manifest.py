#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_manifest.py -- EXP-24 KAPPA-WRITE (worker KW)

Writes RUN_MANIFEST.json and SHA256SUMS.txt for the cell, and verifies:
  * the predeclaration hash against the constant the runner enforces;
  * that the 17 declared input files are unchanged (no write escaped this cell);
  * that the two runs are byte-identical (determinism);
  * that FINDINGS.md carries the KOR counter-example and the four fixed sentences,
    and that no banned phrasing is asserted outside the quoted BANNED block.

Usage:
  "/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" code/make_manifest.py
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CELL = os.path.dirname(HERE)
EXT = os.path.dirname(CELL)
ROOT = os.path.dirname(os.path.dirname(EXT))

PRE_DECL_SHA256 = "db20d123835164f0274e7d486d87c9eadd4ef7fa7dbcb74ad6cdb437583776f1"

INPUT_SHA = {
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv":
        "da5a78e2113a618da9f4b315bbecbbd8be6227c33e1cb572493d669244ac67a4",
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_DETAIL.csv":
        "a52c322726c8a20b2867e5468e052ba20ff302f8b1f8a3d9f970d12948cce004",
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_SECONDARY.csv":
        "d0ef0a56f515d8126f97480ec75bf77e32823ff1cfb7f7612bd2eb8ffb9fa774",
    "10_massification/extensions/kappa_fwd_2026-11-20/FINDINGS.md":
        "024d049b763eda29635ab68c954c0850e8ecd22df5daf42421e480ccf443603c",
    "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_RESULTS.csv":
        "7c4faa427f48485393e58a234d1f1cbd2302bbfc11e81d55454cc56b5e5eff6c",
    "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv":
        "692ca7c01b8b3a7105e84339a87f97029b6a50e277681bdcdbe0f02bf027600f",
    "10_massification/extensions/pipe_loo_2026-11-20/FINDINGS.md":
        "2e37159103874214edd95f1cc91533f3ece374f6e8c39d9196470ae8f741d12b",
    "10_massification/extensions/repro_path_2026-11-20/results/KAPPA_LINK.csv":
        "671962dc585bcc833215ecc22823fb46d26f65b8a181dd9a6d8aa96dfb6b1e38",
    "10_massification/extensions/repro_path_2026-11-20/results/REPRO_PATH_RESULTS.csv":
        "8666492c396afb6beda094b50e3a414542dd50f5fd49702015b873e6284df227",
    "10_massification/extensions/repro_path_2026-11-20/FINDINGS.md":
        "eb868567669e434282be68eaeec4138a7961a4485e767511f558a613cc45ab52",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/results/KAPPA_BIND_CELLS.csv":
        "ce3b1c1277e9618985a7fad7cd3c764dabd1de92146e1a3420495f07ad880162",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/results/kappa_cap_audit.csv":
        "e7cebc4e46b72f7d267fe9439802f42cfe519d8405bca1ca8c0350a824306e9b",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/kappa_object_audit.csv":
        "e9ac569233fe14cc87b49c2bcc65b9cdc1914c8cdf1e2ff628c308d17574791d",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/panel_A01D_kappa.csv":
        "a6ea635f1aea7a35572d1b61bc3b1265a0c57025a5148ab1678f83b9d5b6afcc",
    "08_council/DECISIONS.md":
        "b0a314b06f73b1cc933539d77f2e8bc3d4f6237e63ba8541e2b16629708c3e57",
    "08_council/brief_025/SYNTHESIS_025.md":
        "e279e8200bb8504cafb6b5a4f6f70f3f436410d6839b315896877973c50a8beb",
    "10_massification/STATUS.md":
        "8fe0a3ec62e1b59cf1e827951662e644471508f7675e892281d82787e47958c4",
}

RESULT_FILES = ["KAPPA_WRITE_REGISTER.csv", "KAPPA_WRITE_USES.csv", "KAPPA_WRITE_SUMMARY.csv", "console.txt"]

KOR_SENTENCE = ("KOR is the counter-example that bars \"κ-STABLE is forward-usable\": slope +0.002875/yr "
                "and half-shift 0.6354 pp both clear their bars, yet 0/3 hold-out cells (excess +0.6824, "
                "+0.6506, +0.5917 pp).")

FIXED_SENTENCES = {
    "PHL": "within-window; slope flat but half-shift 2.1348 pp > 2.0, so not stationary in level",
    "KOR": "slope flat and shift 0.6354 pp, yet 0/3 hold-out cells — κ-STABLE is never written forward-usable",
    "KHM": "trending, shift 7.4361 pp",
    "CHN": "reported only; non-stationary; not a forward constraint",
}

BANNED_ASSERTIONS = [
    "κ ≈ 0.95 for the Philippines",
    "κ is stable across systems",
    "κ-STABLE is forward-usable",
    "κ predicts upper completion",
    "the κ-link validates the model path",
    "κ is a parameter",
    "CHN is a forward constraint",
    "the register is clean",
]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p):
    return os.path.relpath(p, CELL)


def main():
    manifest = {
        "cell": "EXP-24 KAPPA-WRITE",
        "worker": "KW",
        "brief": "Council brief 025, SYNTHESIS_025.md section 6.4, rank #4; D156",
        "type": "static register, not a run",
        "predeclaration": {
            "file": "PRE_DECLARATIONS.md",
            "sha256": sha256_of(os.path.join(CELL, "PRE_DECLARATIONS.md")),
            "enforced_at_verdict_time": True,
            "embedded_constant": PRE_DECL_SHA256,
            "verdict": "PRE_DECL-FROZEN",
        },
        "determinism": {},
        "findings_checks": {},
        "inputs_unchanged": {},
        "files": [],
        "claims": {
            "model_run": "NONE", "refit": "NONE", "adoption": "NONE",
            "causal_or_direction_claim": "NONE", "external_request": "NONE",
            "writes_outside_cell": "NONE",
            "labels": ["OBSERVED", "DERIVED"],
        },
    }

    # predecl hash enforcement consistency
    pd = manifest["predeclaration"]["sha256"]
    if pd != PRE_DECL_SHA256:
        sys.exit("PRE_DECLARATIONS.md hash %s != embedded constant %s" % (pd, PRE_DECL_SHA256))

    # determinism: compare the two runs
    ok_all = True
    for f in RESULT_FILES:
        a = os.path.join(CELL, "results", f)
        b = os.path.join(CELL, "results", "determinism_run2", f)
        same = os.path.exists(a) and os.path.exists(b) and sha256_of(a) == sha256_of(b)
        ok_all = ok_all and same
        manifest["determinism"][f] = {
            "run1_sha256": sha256_of(a) if os.path.exists(a) else None,
            "run2_sha256": sha256_of(b) if os.path.exists(b) else None,
            "byte_identical": same,
        }
    manifest["determinism"]["all_four_byte_identical"] = ok_all

    # findings checks
    with open(os.path.join(CELL, "FINDINGS.md"), "r", encoding="utf-8") as fh:
        find = fh.read()
    body = re.sub(r"<!-- BANNED-EXAMPLES.*?<!-- /BANNED-EXAMPLES -->", "", find, flags=re.S)

    def norm(t):
        t = re.sub(r"(?m)^\s*>\s?", "", t)
        return re.sub(r"\s+", " ", t)

    body_flat = norm(body)
    body_scan = body_flat.replace(norm(KOR_SENTENCE), "")

    manifest["findings_checks"]["kor_counter_example_carried"] = norm(KOR_SENTENCE) in body_flat
    manifest["findings_checks"]["fixed_sentences_present"] = {
        k: v in body for k, v in FIXED_SENTENCES.items()
    }
    manifest["findings_checks"]["banned_assertions_outside_prohibition_clauses"] = {
        b: (norm(b) in body_scan) for b in BANNED_ASSERTIONS
    }
    manifest["findings_checks"]["verdict_word_present"] = "REGISTER-NARROWED" in body

    # inputs unchanged (no write escaped the cell)
    for relp, expected in INPUT_SHA.items():
        got = sha256_of(os.path.join(ROOT, relp))
        manifest["inputs_unchanged"][relp] = {
            "sha256": got, "declared": expected, "unchanged": got == expected,
        }
    manifest["inputs_unchanged"]["_all_unchanged"] = all(
        v["unchanged"] for k, v in manifest["inputs_unchanged"].items() if not k.startswith("_"))

    # file inventory (cell-local only)
    for dirpath, dirnames, filenames in os.walk(CELL):
        dirnames.sort()
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            manifest["files"].append({
                "path": rel(p), "bytes": os.path.getsize(p), "sha256": sha256_of(p),
            })

    with open(os.path.join(CELL, "RUN_MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")

    # SHA256SUMS.txt (cell-local, deterministic order, excludes itself and the manifest)
    lines = []
    for rec in sorted(manifest["files"], key=lambda r: r["path"]):
        if rec["path"] in ("SHA256SUMS.txt", "RUN_MANIFEST.json"):
            continue
        lines.append("%s  %s" % (rec["sha256"], rec["path"]))
    lines.append("%s  RUN_MANIFEST.json" % sha256_of(os.path.join(CELL, "RUN_MANIFEST.json")))
    with open(os.path.join(CELL, "SHA256SUMS.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("predecl sha256        : %s (enforced)" % pd)
    print("determinism           : %s" % ("PASS (4/4 byte-identical)" if ok_all else "FAIL"))
    print("KOR counter-example   : %s" % manifest["findings_checks"]["kor_counter_example_carried"])
    print("fixed sentences       : %s" % all(manifest["findings_checks"]["fixed_sentences_present"].values()))
    print("banned assertions     : %s" % ("none asserted"
                                          if not any(manifest["findings_checks"]["banned_assertions_outside_prohibition_clauses"].values())
                                          else "FOUND: %s" % [k for k, v in
                                                              manifest["findings_checks"]["banned_assertions_outside_prohibition_clauses"].items() if v]))
    print("inputs unchanged      : %s" % ("17/17" if manifest["inputs_unchanged"]["_all_unchanged"] else "MISMATCH"))
    print("files hashed          : %d" % len(manifest["files"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
