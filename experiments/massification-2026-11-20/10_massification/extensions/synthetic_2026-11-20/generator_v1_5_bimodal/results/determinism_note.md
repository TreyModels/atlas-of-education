# determinism note -- v1.5 BIMODAL-GATE

Two complete runs into `results/` and `results/determinism_run2/`.
Every result file present in the second run was compared with `cmp` semantics
(byte equality) and by sha256.

- files compared: **14**
- byte-identical: **14**
- status: **DETERMINISM-PASS**

`guard_report.json` and this note are written AFTER the comparison and are
identical in both directories by construction.

Seed 20261120, one numpy PCG64 stream, the frozen v1.2 draw order; the tier block
draws no random numbers. Floats are written at `%.10g`. No timestamp, hostname,
PID or wall-clock enters any output.
