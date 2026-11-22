#!/usr/bin/env python3
"""Record exact dependency, source and final-output hashes for PHL v5."""
import hashlib
import json
import platform
from pathlib import Path

import matplotlib
import numpy
import pytest
import scipy

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'outputs' / 'qa'
QA.mkdir(parents=True, exist_ok=True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


sources = {}
for folder in ('masseng', 'scripts', 'tests', 'countries', 'docs'):
    for path in sorted((ROOT / folder).rglob('*')):
        if path.is_file() and path.suffix in ('.py', '.json', '.md') and '__pycache__' not in path.parts:
            sources[str(path.relative_to(ROOT))] = digest(path)
for name in ('PROTOCOL.md', 'PROTOCOL_v5.md', 'HANDOFF_v5.md', 'README.md', 'requirements-v5.txt'):
    sources[name] = digest(ROOT / name)
requirements = {
    'python': platform.python_version(), 'numpy': numpy.__version__, 'scipy': scipy.__version__,
    'matplotlib': matplotlib.__version__, 'pytest': pytest.__version__,
    'blas_threads': 'OPENBLAS_NUM_THREADS=1; OMP_NUM_THREADS=1',
}
(QA / 'reproducibility_inputs.json').write_text(json.dumps({'requirements': requirements, 'files': sources}, indent=2) + '\n')
outputs = {}
for path in sorted((ROOT / 'outputs' / 'PHL' / 'v5').rglob('*')):
    if path.is_file():
        outputs[str(path.relative_to(ROOT))] = digest(path)
(QA / 'final_output_hashes.json').write_text(json.dumps(outputs, indent=2, sort_keys=True) + '\n')
print(f'{len(sources)} source files and {len(outputs)} final outputs hashed')
