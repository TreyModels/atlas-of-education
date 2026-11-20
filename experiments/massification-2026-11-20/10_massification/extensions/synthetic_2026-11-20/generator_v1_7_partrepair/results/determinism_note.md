# Determinism (v1.7)

Two complete runs are executed: `results/` and `results/determinism_run2/`. Every result file is compared with sha256; the status and the file list are recorded in `RUN_MANIFEST.json:determinism`. A single mismatch aborts the run (exit 1, `UNDETERMINED`, no verdict). One PCG64 stream, seed 20261120, frozen v1.2 draw order, no wall-clock, no hostname, floats `%.10g`.
