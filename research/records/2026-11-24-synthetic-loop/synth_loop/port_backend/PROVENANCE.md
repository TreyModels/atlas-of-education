# Provenance — vendored port backend

Copied **unmodified** from `research/apple-silicon-gpu-2026-11-24` @ `52d74ec`
(`research/records/2026-11-24-apple-silicon-gpu/{kernels_np_mlx.py,gpu_compat.py}`), which is the verified
CUDA→Apple-Silicon port: kernel transcription bit-identical across NumPy/MLX and verified against 10 real
CUDA launches (0 integer mismatches, max abs 3.815e-06; `results/cuda_vs_transcription.json` on that branch).

Only `kernels_np_mlx.run_sim_step_arrays(backend, args)` is used by the redesign. The upstream suite copy in
`suite/unified_gpu_suite/` (on the handoff branch) is not edited.
