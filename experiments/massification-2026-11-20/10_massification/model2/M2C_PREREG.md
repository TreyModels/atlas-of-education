# PRE-REGISTRATION — M2c: E1 two-shock estimator recovery test (SIMULATED; before E1 fielded)

**Written before running.** Simulated only; no observed data; no model fitting; direction claims remain barred
(R13/EQUIVALENT). Purpose: test whether E1's two-shock interaction estimator recovers a known supply×demand
interaction sign and size, or whether E1 is underpowered/not sufficient.

**Design.** Panel of 30 provinces × 10 years (simulated). Two shocks: `S` = K-12 2013 supply expansion (exposed
regions post-2013), `D` = health-worker visa demand expansion (exposed regions post-2014); outcome Y (e.g.,
nursing/schooling take-up). DGP: Y_it = α_i + λ_t + βs·S_it + βd·D_it + **γ·S_it·D_it** + ε_it, with βs=0.5,
βd=0.3, γ ∈ {−0.30, 0.00, +0.30} (substitution / null / complementarity), ε ~ N(0, σ²), σ ∈ {0.5, 1.0} (two power
regimes). 100 simulations per (γ, σ) cell, seeds 0–99.
**Estimator (E1 design):** two-way FE OLS of Y on S, D and the interaction S·D (unit + year FE), CR1 cluster SE by
unit; estimand = interaction coefficient γ̂ (complementarity vs substitution).
**Recovery metrics (per cell):** sign accuracy; median relative bias |γ̂−γ|/|γ| (nonzero γ); 90% CI coverage; for
γ=0 the false-positive rate = share with |t|>1.96.
**Predeclared sufficiency rule for E1:** E1 is SUFFICIENT iff, in the low-noise regime σ=0.5, (i) sign accuracy
≥ 0.67 for BOTH γ=+0.3 and γ=−0.3, (ii) median relative bias ≤ 0.50, (iii) 90% CI coverage ≥ 0.67, and
(iv) null false-positive rate ≤ 0.10. If E1 fails, report **E1 NOT SUFFICIENT** (underpowered) and do not field it
as the identification gate without a power fix; high-noise σ=1.0 row reported as power stress (expected worse).
**Failure rule:** a simulation error is logged and excluded with counts; no thresholds changed after results.
