#!/usr/bin/env bash
# Local CI hook for the Atlas Lean verification prototype (host-only; no network needed).
# Checks: (1) build, (2) no `sorry`, (3) axiom audit of every proved theorem.
# Exit non-zero on any failure.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$HERE"

# Tolerate an elan-managed toolchain that is not the global default.
if ! command -v lake >/dev/null 2>&1; then
  if [ -x "$HOME/.elan/toolchains/leanprover--lean4---v4.36.0/bin/lake" ]; then
    export PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.36.0/bin:$PATH"
  elif [ -x "$HOME/.elan/bin/lake" ]; then
    export PATH="$HOME/.elan/bin:$PATH"
  fi
fi
command -v lake >/dev/null 2>&1 || { echo "FATAL: lake not found (install Lean v4.36.0)"; exit 2; }

echo "== toolchain =="
lake --version
lean --version

echo "== build =="
time lake build

echo "== comment-aware sorry scan (must be empty) =="
python3 ci/sorry_scan.py Atlas Atlas.lean LeanStarter.lean || { echo "FATAL: 'sorry' token found in Lean sources"; exit 3; }

echo "== axiom audit =="
AUDIT=".axiom_audit.lean"
cat > "$AUDIT" <<'LEAN'
import Atlas
#print axioms Atlas.budget_ledger_identity
#print axioms Atlas.tax_revenue_le_base
#print axioms Atlas.prep_recursion_closed_form
#print axioms Atlas.pl_top1_sum_eq_denom
#print axioms Atlas.pl_top1_sum_eq_min
#print axioms Atlas.pl_topK_selected_sum
#print axioms Atlas.Claims.A34_arithmetic
#print axioms Atlas.Claims.A38_anchor_infeasible
#print axioms Atlas.Claims.B41_HK_meets_criterion
#print axioms Atlas.Claims.B42_CF4b_fails_spend_HK
#print axioms Atlas.Claims.D02_paradox_not_universal
#print axioms Atlas.Claims.classical_demand_ignores_school_supply
#print axioms LeanStarter.gap_eq_truncated_sub
#print axioms LeanStarter.gap_pos_of_shortfall
#print axioms LeanStarter.used_plus_remaining_eq_capacity
#print axioms LeanStarter.preparation_within_elapsed
#print axioms LeanStarter.work_within_elapsed
#print axioms LeanStarter.review_within_elapsed
#print axioms Atlas.Model.gap_nonneg
#print axioms Atlas.Model.gap_eq_zero_iff_met
#print axioms Atlas.Model.gap_pos_iff_shortfall
#print axioms Atlas.Model.accepted_le_capacity
#print axioms Atlas.Model.zero_extra_input_no_increment
#print axioms Atlas.Model.total_input_eq_sum
#print axioms Atlas.Model.additive_combine_eq_sum
#print axioms Atlas.Model.max_not_additive
#print axioms Atlas.Model.budget_implies_component
#print axioms Atlas.Model.time_accounting_identity
#print axioms Atlas.Model.rank_invariant_under_common_shift
#print axioms Atlas.Model.fixed_seat_relative_rank_counterexample
#print axioms Atlas.Model.accepted_monotone_fixed_capacity
#print axioms Atlas.Model.complementarity_counterexample
#print axioms Atlas.Model.feedback_capacity_counterexample
LEAN
lake env lean "$AUDIT" | tee /tmp/atlas_lean_axioms.txt
rm -f "$AUDIT"
python3 ci/axiom_audit.py /tmp/atlas_lean_axioms.txt || { echo "FATAL: disallowed axiom in a proved theorem"; exit 4; }

echo "== claim declarations present =="
for id in A-34 A-35 A-36 A-37 A-38 A-39 B-41 B-42 B-43 B-44 C-01 C-02 C-03 C-04 D-01 D-02 D-03 D-04; do
  grep -q "claimId := \"$id\"" Atlas/Claims.lean || { echo "FATAL: claim $id missing from Claims.lean"; exit 5; }
done
echo "18/18 Lead-scoped claim ids present"
echo "LEAN VERIFY: PASS"
