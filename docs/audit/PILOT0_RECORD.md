# Paper C Pilot-0 — code-authoritative design record (corrects earlier 96-run/12-cell mention)

**Live pilot:** PID 40056 (8 workers, restarted by Lead from the 2-worker v2 run; per-seed checkpoints preserved),
`/root/work/paperC`, box engine pin `846c9e0` (`core.py` e111397b…), spec `e5ddef6b…`.

**Design (CODE-AUTHORITATIVE): 4 regimes × 2 S proxies × 2 private-supply levels × 8 seeds = 16 cells × 8 = 128 runs.**
* regimes: `market_only` (own_ban .95, pay_ratio .55, monitoring .2, pay_gap), `own_open_gap` (own_ban 0, pay_ratio .55,
  monitoring .2, pay_gap), `own_open_incentive` (own_ban 0, pay_ratio 1.2, monitoring .2, incentive),
  `own_open_gap_firm_ban` (as own_open_gap + firm_ban .9).
* S proxy `q0 ∈ {1.0, 1.2}` (declared PROXY; q0 scales public AND private quality); private supply `p_firm ∈ {.03,.08}`;
  N=1500; base = canonical HK primary gates (fixed); measure/T from spec.
* Binding assertions (active in v3 runner): non-market regimes require `withheld > 1e-3` and `own_share > 0.1`;
  a no-op cell raises. Contamination: `own_share`/`tut_firm_by_grade` mix contest prep with firm tutoring.
* **Status: EXPLORATORY / hypothesis-generating; NOT confirmatory; 128 runs/16 cells is the QA-validated target.**
* The earlier **96-run / 3-regime / pay_ratio .8** text was a superseded draft (v2); it must not stand. Docstring,
  QA validator and payload must use **128/16** and the v3 parameters above.
* Runner sha256 recorded in the pilot manifest at completion; source commits: v3 code `fbc1991`, docstring alignment
  `69e38b2`, latest runner `edc6a59` (diagnostic extraction only).
