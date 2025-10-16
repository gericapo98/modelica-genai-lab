#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then
  echo "usage: $0 tests/whatever.mos"; exit 2
fi
set -x
omc "$1"
