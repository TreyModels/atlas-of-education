#!/usr/bin/env python3
"""Component tests: RNG transcription, shim identity, RawModule limits, backend reporting."""
import json, os, subprocess, sys
import numpy as np
RECORD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RECORD)
sys.path.insert(0, os.path.join(RECORD, "shim"))
PY = os.environ.get("APPLE_PY", sys.executable)
ENV = dict(os.environ)
ENV["PYTHONPATH"] = os.pathsep.join([RECORD, os.path.join(RECORD, "shim"),
                                     os.path.join(RECORD, "suite", "unified_gpu_suite", "scripts")])
out = {}

# 1. Philox vectorised transcription == scalar transcription
from kernels_np_mlx import philox_uniforms, _scalar_philox
n, year, s0, s1 = 16, 7, 20261125, 41
u = philox_uniforms(n, year, s0, s1)
ok = True
for i in range(n):
    r = _scalar_philox(i, year, 0, 1, s0, s1)
    for j in range(4):
        us = (np.float32(r[j]) + np.float32(0.5)) * np.float32(1 / 4294967296.0)
        ok &= bool(us == u[i, j])
out["philox_vector_equals_scalar"] = bool(ok)
out["philox_first_uniforms"] = [float(x) for x in u[0]]

# 2. shim: `import cupy` resolves to our shim and reports the backend
code = ("import cupy as cp, json; "
        "print(json.dumps({'file': cp.__file__, 'backend': cp.backend(), "
        "'has_attrs': all(hasattr(cp, a) for a in ['float32','int32','empty','asnumpy','exp','clip',"
        "'RawModule','random','cuda'])}))")
p = subprocess.run([PY, "-c", code], env=ENV, capture_output=True, text=True)
out["shim_import"] = json.loads(p.stdout) if p.returncode == 0 else {"error": p.stderr[-300:]}

# 3. RawModule refuses arbitrary CUDA C
code2 = ("import cupy as cp, json\n"
         "src = 'extern \"C\" __global__ void other(int* x){x[0]=1;}'\n"
         "try:\n"
         "    m = cp.RawModule(code=src)\n"
         "    m.get_function('other')\n"
         "    print(json.dumps({'refused': False}))\n"
         "except cp.PortabilityError as e:\n"
         "    print(json.dumps({'refused': True, 'msg': str(e)[:120]}))\n")
p2 = subprocess.run([PY, "-c", code2], env=ENV, capture_output=True, text=True)
out["rawmodule_arbitrary_cuda_refused"] = json.loads(p2.stdout) if p2.returncode == 0 else {"error": p2.stderr[-300:]}

# 4. the suite's own kernel source is accepted (fingerprint recognised)
suite = os.path.join(RECORD, "suite", "unified_gpu_suite", "scripts")
sys.path.insert(0, suite)
import exp1_unified_gpu_abm as ex1  # noqa: E402  (imports `cupy` = our shim)
mod = __import__("cupy").RawModule(code=ex1.KERNEL_SRC)
fn = mod.get_function("sim_step")
out["suite_kernel_accepted"] = dict(fingerprint=mod.fingerprint, name=fn.name)

json.dump(out, open(os.path.join(RECORD, "results", "component_tests.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
