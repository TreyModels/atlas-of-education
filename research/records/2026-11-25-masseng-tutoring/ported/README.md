# Ported first-pass shadow-education code (verbatim copies)

| file | source | branch / commit | sha256 |
|---|---|---|---|
| `shadow_model.py` | `research/records/2026-11-25-shadow-equations/shadow_model.py` | `research/shadow-equations-2026-11-25` @ `fdc8da0` | `dc14fadf…` |
| `bray_reality_check.py` | `research/records/2026-11-25-shadow-equations/bray_reality_check.py` | `research/shadow-equations-2026-11-25` @ `fdc8da0` | `85e9b809…` |
| `bray_reality_check_standalone_8k.json` | committed 8k-draw result | same | (result file) |

These files are **copies**, not imports across branches (the task forbids cross-branch imports).  They are not
modified; the MASSENG port lives in `research/masseng-v6/model/masseng/tutoring.py` and is a re-implementation
of the household-demand block, not a wrapper around these files.

The copies are used for exactly one purpose in this record: the **demand-mix check** (six Siem Reap schools,
seven Bray et al. 2016/2018 patterns).  They are NOT used for PHL validation.

Note: the shadow-equations branch is still being worked on downstream; these copies are pinned to `fdc8da0`,
the head at which this task started.
