#!/usr/bin/env python3
"""Create the requested session-state note and complete research ZIP."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT.parent
WORKSPACE = RESEARCH.parents[1]
PR_RESEARCH = WORKSPACE / 'atlas-pr33' / 'research' / 'masseng-v6'
OUT = ROOT / 'outputs' / 'PHL' / 'v5'
DELIVERY = WORKSPACE / 'deliverables'
BUNDLE = DELIVERY / 'MASSENG_complete_results_2026-11-22'
ZIP = DELIVERY / 'MASSENG_complete_results_2026-11-22.zip'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    scores = json.loads((OUT / 'scores.json').read_text())
    winner = scores['winner_by_preregistered_rule']
    w = scores['rivals'][winner]
    recovery = json.loads((OUT / f'recovery_{winner}.json').read_text())
    repro_path = ROOT / 'outputs' / 'qa' / 'fresh_copy_comparison.json'
    repro = json.loads(repro_path.read_text()) if repro_path.exists() else {'all_byte_identical': False}
    rmse = w['three_ger_rmse']['model']
    persistence = w['three_ger_rmse']['persistence']
    trend = w['three_ger_rmse']['trend']
    failed = [name for name, v in recovery['parameters'].items()
              if v['status'] != 'not in rival' and not str(v['status']).startswith('identified')]
    lines = [
        '# MASSENG session state — final Philippine v5 package', '',
        '## Bottom line', '',
        f'- Pre-registered winner: **{winner}**, three-GER held-out RMSE **{rmse:.12f}**.',
        f'- Persistence RMSE: **{persistence:.12f}**; linear-trend RMSE: **{trend:.12f}**.',
        f'- Naive benchmark beaten: **{rmse < min(persistence, trend)}**.',
        '- Status: **not calibrated**. The test was retrospective and inspected, not blind.',
        '- Protocol amendments: **none**.',
        f'- Recovery failures / not identified: **{", ".join(failed) if failed else "none"}**.',
        f'- Fresh-copy files all byte-identical: **{repro["all_byte_identical"]}**.',
        '- Atlas Worlds: **NOT READY**. No delivery or release is claimed.',
        '- Hong Kong: not started.',
        '- PR #33 remains a draft and is not merged: https://github.com/TreyModels/atlas-of-education/pull/33', '',
        '## Important interpretation', '',
        'The best member of a rival set is not automatically a good forecasting model or evidence for its named '
        'mechanism. Read bound hits, naive benchmarks, separating observations, and recovery together. The China '
        'credential-floor comparison has the wrong sign for all three models and is not support for the relational '
        'account.', '',
        '## Package map', '',
        '- `research/masseng-v6/model/PROTOCOL_v5.md`: authoritative pre-registered design.',
        '- `research/masseng-v6/model/outputs/PHL/v5/scores.json`: authoritative rival scores.',
        f'- `research/masseng-v6/model/outputs/PHL/v5/recovery_{winner}.json`: recovery results.',
        '- `research/masseng-v6/model/outputs/qa/`: source, reproducibility, and QA records.',
        '- `research/masseng-v6/manuscripts/Philippine_demand_rivals.md`: new results-led paper with LaTeX and charts.',
        '- `research/masseng-v6/manuscripts/original/`: unchanged original papers.',
        '- `research/masseng-v6/ATLAS_WORLDS_QA.md`: open and closed QA gates.', '',
        '## Remaining blocker', '',
        'The CHED original PDF has not been independently retrieved. DepEd, World Bank spot checks, Bray source '
        'checks, and the Siem Reap publisher text have been checked as recorded in the QA files.', '',
        '## Reproduce', '',
        'From `research/masseng-v6/model`, install the exact requirements in `requirements-v5.txt`, then use the '
        'commands in `README.md`. Set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`. The fresh-copy comparison '
        'covers fits, scores, recovery, report, and both figures.', '',
    ]
    DELIVERY.mkdir(exist_ok=True)
    state = DELIVERY / 'SESSION_STATE.md'
    state.write_text('\n'.join(lines) + '\n')
    if BUNDLE.exists():
        shutil.rmtree(BUNDLE)
    BUNDLE.mkdir()
    shutil.copy2(state, BUNDLE / 'SESSION_STATE.md')
    shutil.copytree(PR_RESEARCH, BUNDLE / 'research' / 'masseng-v6',
                    ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache', '*.pyc', '.DS_Store'))
    files = {}
    for path in sorted(BUNDLE.rglob('*')):
        if path.is_file():
            files[str(path.relative_to(BUNDLE))] = digest(path)
    (BUNDLE / 'PACKAGE_MANIFEST.json').write_text(json.dumps(files, indent=2, sort_keys=True) + '\n')
    with zipfile.ZipFile(ZIP, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(BUNDLE.rglob('*')):
            if path.is_file():
                z.write(path, path.relative_to(BUNDLE.parent))
    with zipfile.ZipFile(ZIP) as z:
        bad = z.testzip()
        if bad:
            raise SystemExit(f'ZIP CRC failure: {bad}')
    print(json.dumps({'zip': str(ZIP), 'bytes': ZIP.stat().st_size,
                      'sha256': digest(ZIP), 'files': len(files) + 1,
                      'fresh_copy_all_byte_identical': repro['all_byte_identical']}, indent=2))


if __name__ == '__main__':
    main()
