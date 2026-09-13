#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT}/internaltooling${PYTHONPATH:+:${PYTHONPATH}}"
cd "${ROOT}"
python -m pytest internaltooling/tests
