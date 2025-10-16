#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

rc=0
for f in tests/*.mos; do
  echo "==> $f"
  if ! ./omc.sh "$f"; then
    echo "FAILED: $f"
    rc=1
  fi
done

if [[ $rc -eq 0 ]]; then
  echo "ALL PASS"
else
  echo "SOME TESTS FAILED"
fi
exit $rc
