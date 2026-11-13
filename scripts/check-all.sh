#!/bin/bash
# Full local check: JS world tests, translations, repair hashes, Python engine tests, build.
# Needs Node >= 20 (uses Homebrew node if present) and a Python with numpy+scipy (PY=...).
cd "$(dirname "$0")/.."
export PATH=/opt/homebrew/bin:$PATH
PY=${PY:-python3}
fail=0
node test-worlds.cjs >/tmp/atlas-tw.log 2>&1 && echo "worlds: ok ($(grep -c '^✔' /tmp/atlas-tw.log) pass)" || { echo "worlds: FAIL"; grep '^✖' /tmp/atlas-tw.log | sort -u; fail=1; }
node check-translations.cjs >/tmp/atlas-tr.log 2>&1 && echo "translations: ok" || { echo "translations: FAIL"; tail -5 /tmp/atlas-tr.log; fail=1; }
node scripts/check-repairs.cjs >/tmp/atlas-rp.log 2>&1 && echo "repairs: ok" || { echo "repairs: FAIL"; tail -5 /tmp/atlas-rp.log; fail=1; }
(cd engine && $PY -m unittest firms.test_firms firms.test_tilly >/tmp/atlas-py.log 2>&1) && echo "python: ok" || { echo "python: FAIL"; tail -3 /tmp/atlas-py.log; fail=1; }
npm run build >/tmp/atlas-build.log 2>&1 && echo "build: ok" || { echo "build: FAIL"; grep -i error /tmp/atlas-build.log | head -5; fail=1; }
exit $fail
