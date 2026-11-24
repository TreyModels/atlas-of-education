# PRESERVATION — 24 Nov 2026 (task-22)

Region-42 preservation manifest, captured before any shutdown. **Old outputs were not modified or deleted.**

| item | value |
|---|---|
| tar path | `/root/work/PRESERVE_20261124/artifacts.tar.gz` |
| tar sha256 | **`8c1d49c652c0e39bfd202760ed32c673d79677de4f4724f52fd53dac355b1ec2`** |
| tar size | **4.2 MB** |
| tar contains | all server logs (`phaseb_fixed_1795521194.log`, `phaseb.log`, `v2.log`, `v2b.log`, `matrix_repro.log`), `synthloop-b/rec/results/`, matrix `results/`, `cells_v2b/`, and `synthloop-b/rec/synth_loop/` |

**Server code hashes (live copies, uncommitted vs pushed):**
- `run_phaseb.py` = `c3a0e3ec844f8fe0cdcb4f16bb49ccfbc71a478e9264e915d024c706b55726c6` (post-audit fix, pushed later as `e05763f`)
- `fertility.py` = `b367324c91fc093cc72b9faacc4ae4cea671f35e3daa0ad4e577183bd4505ebe` — **still `WOMEN=400` (prereg: 4,000)**
- `run_matrix_v2b.py` = `6c0195fd658f0842bc6f0d2b93938b18cbf4fd040b2942c051a95cd4dda518d1`
- `model.py` = `b26b756146fb3694f5f2d367c3bab6e5c85abcee0df11bedc373f3efa47000a2`
- `phaseb_results.json` = `f1f32ef6cbfdd685799bbb9aa4d46cb1aac655017830460d84958d058f954e6b`

**Pushed-revision mismatch:** Codex audited `research/synthetic-phaseb-2026-11-24` @ `81112ab` (where `countries` is undefined); the live server copy is `c3a0e3ec…` (fix `e05763f`). The audit therefore describes the pushed revision, not a verified live checkout — both are recorded here.

**Job status:** no `run_phaseb` / `run_matrix_v2b` PIDs at preservation time. Nothing is running on region-42.

**Shutdown:** Trey may shut region-42 down **after** this manifest and the code hashes are committed (done by this commit). The tar itself lives only on the box; it must be downloaded or accepted as lost if the instance is released — it is **not released**, only a candidate for 关机.
