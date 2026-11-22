"""Run deterministic Phase 1 mechanism tests; all quantities are synthetic."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from masseng_v6.education.admissions import Applicant, clear_admissions
from masseng_v6.education.institutions import Market

ROOT = Path(__file__).resolve().parents[1]


def scenario(name, applicants, markets):
    result = clear_admissions(applicants, markets)
    return {
        "scenario": name,
        "status": "illustrative synthetic known-answer test",
        "Q": result.funnel.qualified,
        "L": result.funnel.latent_zero_cost,
        "E": result.funnel.effective,
        "R": result.funnel.realized,
        "unique_applicants": result.unique_applicants,
        "unmet_effective_demand": result.unmet_effective_demand,
        "physical_empty_seats": sum(m.empty_seats for m in result.markets),
        "accessible_empty_seats": sum(m.accessible_empty_seats for m in result.markets),
        "assignments": dict(sorted(result.assignments.items())),
    }


def main():
    markets = [
        Market("public", "urban", "tertiary", "public", 2),
        Market("private", "urban", "tertiary", "private", 2),
    ]
    people = [Applicant(f"a{i}", ("public", "private")) for i in range(5)]
    runs = [
        scenario("joint_choice_binding_public", people, markets),
        scenario("zero_capacity", people, [Market("public", "urban", "tertiary", "public", 0), Market("private", "urban", "tertiary", "private", 0)]),
        scenario("continuing_reservation", people, [Market("public", "urban", "tertiary", "public", 5, 4), Market("private", "urban", "tertiary", "private", 0)]),
        scenario(
            "cost_exclusion_despite_vacancy",
            [Applicant("poor", ("public",), effective=False), Applicant("rich", ("public",))],
            [Market("public", "urban", "tertiary", "public", 2)],
        ),
        scenario(
            "geographic_mismatch",
            [Applicant("rural", ("urban_public",))],
            [
                Market("urban_public", "urban", "tertiary", "public", 1),
                Market("rural_private", "rural", "tertiary", "private", 3),
            ],
        ),
    ]
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "phase1_results.json").write_text(json.dumps(runs, indent=2) + "\n")
    with (out / "market_panel.csv").open("w", newline="") as handle:
        fields = ["scenario", "Q", "L", "E", "R", "unique_applicants", "unmet_effective_demand", "physical_empty_seats", "accessible_empty_seats", "status"]
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(runs)
    hashes = {}
    for path in sorted((ROOT / "masseng_v6").rglob("*.py")):
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (out / "code_hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    print(json.dumps(runs, indent=2))


if __name__ == "__main__":
    main()
