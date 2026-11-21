# FINDINGS — v0.1-YANG: **NOT WIREABLE AS SPECIFIED** (design mismatch, reported, not forced)

**Label: `SIMULATED` / `ILLUSTRATIVE`.** New extension; **coevolve v0 and its frozen predeclaration are untouched**
(`PRE_DECLARATIONS.md` sha256 `7d25e176…` unchanged; `git status` clean for that file). No MC was run because the
feasibility test declared in advance fired.

## 1. What was requested

Wire the Yang gate margin into coevolution v0: g(N) sets the **share of the upper-secondary and tertiary gate places
that carry a credential requirement**, with the model's existing gates/controllers otherwise unchanged; then run a
150-draw parameter MC (2,700 runs) against the ≥0.5 pp-at-≥3-sizes bar.

## 2. The feasibility test (declared before the run, `PRE_DECLARATIONS.md` §2)

> The primary wiring is implementable within the model's existing gate objects iff there exist gate applicants who do
> **not already hold** the credential that the gated place would require. If that count is exactly zero, the share
> `g` cannot change any admission decision: `INERT-BY-CONSTRUCTION` → **STOP**.

Audit: `code/credential_gate_audit.py` (read-only import of the frozen model; baseline arm; seeds
20261121/20261122). Results: `results/CREDENTIAL_GATE_AUDIT.json`.

| gate / allocation | candidates or applicants | lacking the prerequisite credential |
|---|---:|---:|
| selective gate (upper-secondary, requires `cred ≥ 2`) | 12,516 | **0** |
| university/post-secondary gate (requires `cred ≥ 3`) | 12,455 | **0** |
| allocation, all six levels (197,096 primary · 43,784 lower · 12,516 upper · 142 selective · 12,455 post-sec · 1,005 tertiary) | 447,098 | **0 in every level** |

**Verdict: `INERT-BY-CONSTRUCTION`.**

## 3. Why it is inert — the code (file:line evidence)

- `coevolve_v0.py:713` — `advancing = (self.pending_level == nxt) & (nxt >= 0)` with `nxt` built from
  `NEXT_AFTER_CRED` (`coevolve_v0.py:60`): a child can only be *advancing* if `cred == c`, i.e. **only children who
  already hold the completed credential can seek the next level**. `_allocate` (`coevolve_v0.py:824`) and the gates
  (`_selective_gate` at `:905`, `_university_gate` at `:936`) act on exactly those candidates.
- The selective gate takes `is_new & (want == L_UPPER)` — all hold `cred = 2` (completed lower secondary).
- The university/post-secondary gate takes `is_new & (want == L_POSTSEC)` — all hold `cred = 3` (completed upper
  secondary).
- The model's gates are **residence** (allocation), **exam + rank** (selective), and **exam + fee + rank**
  (university) — there is **no gate-place object carrying a credential requirement** beyond the prerequisite
  completion that advancement already enforces. A share `g` of places "requiring the credential" therefore changes
  nothing: every applicant already has it.

## 4. What would be needed to wire it (not built here — needs a new predeclaration)

A faithful primary wiring requires **one new declared object**, e.g. one of:
1. **Gate-place credential threshold**: a per-gate `cred_req` (employer-style level) applied to a share `g(N)` of
   upper-secondary/tertiary places, so gated places exclude applicants below the threshold; or
2. **Allocation-controller mix**: a share `g(N)` of ordinary upper-secondary and tertiary places allocated by the
   **selective (exam + credential) controller** instead of residence, with the rest unchanged; or
3. **Return-side alternative** (the Lead's declared alternative): `g(N)` multiplies the credential value `C_value`
   (`coevolve_v0.py:120` `C_value_by_level`; `:1101` `weight_credential * C * c_market * p_gate`), which IS
   implementable with existing objects but is a **different object** from the requested gate-incidence wiring and is
   declared **future work**.

Each option changes the model's gate objects or the credential object and therefore requires a **new predeclaration**
and the Lead/user's approval; it is not a defect fix and not licensed by this extension.

## 5. Consequences for the requested MC

No `mc_results.json`, `mc_per_draw.csv` or MC `FINDINGS` are produced: running the primary MC after the feasibility
test fired would report zero by construction, not by result, and would violate the declared stop rule. The only
results are the audit (above). Runtime of the audit: seconds; two sizes/designs are irrelevant to a check that is
non-binding by construction. The YANG-toy boundary-check contingency (inert/active × Yang-toy inert/active) is also
**not run** for the same reason.

## 6. Recommendation to the Lead

- **Do not force the specified wiring.** The clean outcome is: *coevolve v0 has no gate-place credential-requirement
  object; the requested primary wiring is inert by construction.*
- If the user wants the Yang margin in coevolution, choose one of the two declarations in §4 and predeclare it
  **before any run**:
  (a) a new `cred_req`-at-gate object with share `g(N)` (the closest faithful reading of "credential requirement");
  (b) the declared alternative `g(N) × C_value` (return-side), which is runnable now and is what the Yang-toy's own
     wage-premium/decomposition logic suggests is the load-bearing channel.
- The Yang-toy result (D178: robust-ACTIVE 68.3%, top driver factory-wage premium +0.784, Yang slope/anchor nearly
  inert) supports (b): the margin is a **return/credential-premium object**, not a gate-incidence object alone.

## 7. Labels and limits

`SIMULATED`/`DERIVED`/`ILLUSTRATIVE`; no observed data; no country claims; no causal or direction claims; no tuning;
the closed records and coevolve v0 are untouched; the requested MC is not run.
