# Smoke test — matrix

Run on region-42 with `/root/miniconda3/bin/python` (Python 3.10.8; NumPy 2.2.6), 2026-11-24:

```text
python -m unittest -v test_corrected
Ran 6 tests — OK
python run_corrected.py --smoke --workers 4 --output smoke_server.json
{"fits": 4200, "estimable": 4100, "comparisons": 4200, "elapsed_s": 3.38}
```

The 100 inestimable fits are S4 with income as both outcome and control and are explicitly marked. Smoke uses 300 households, 8 countries per block, 2 blocks, not the full experiment. It is solely a mechanics check; standard errors and TOST results from two-country subgroups/two blocks are not reliable research results.

SHA-256:

```text
60faefa71200d4b9d2742c659d8da119208d7ad05809751d08b7501e4b864eb2  run_corrected.py
b26b756146fb3694f5f2d367c3bab6e5c85abcee0df11bedc373f3efa47000a2  model.py
1357ea5a62d39317f43f6810288949b4eead5863dcea150b550ef26070651ff5  smoke_server.json
```

Server smoke output: `/root/work/codex-audit-smoke-20261124/smoke_server.json`. It includes elapsed wall time and is not intended to match byte-for-byte on another system. Old runs remain untouched.

# Smoke test — fertility layer

On the same region-42 Python/NumPy environment, `python -m unittest -v test_phaseb_corrected` passed all eight focused tests. The following bounded upstream smoke, with a copied calibration and 100 permutations for the smoke only, completed with 64 units in 0.873 s:

```text
python phaseb_corrected.py --smoke --calibration-path calibration.json --permutation-reps 100 --out phaseb_server_smoke.json
```

The smoke used 2/3/3 seeds per split, 256 upstream households and 200 women, far below the full experiment. Its output is not research evidence. Full code was not executed at full scale.

```text
c3bc506a1434add728ad4cee1cb0d197a4443138dbce28ccd325ced73d9089d9  phaseb_corrected.py
6cc3c5701f5ea34d226726f2eee8171b97440632e1675971e40054edf15a839e  calibration.json
17ac24fa3691ef7a5d85bf4878703f3f3e0a6d8f3a820d6741c4afc53b930fbd  phaseb_server_smoke.json
```

Server smoke output and log: `/root/work/codex-audit-smoke-20261124/phaseb_server_smoke.json` and `phaseb_server_smoke.log`.
