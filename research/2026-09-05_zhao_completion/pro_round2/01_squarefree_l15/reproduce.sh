#!/usr/bin/env bash
set -euo pipefail
python3 independent/src/proof_arithmetic_check.py > /tmp/l15-proof-arithmetic.json
python3 independent/src/independent_count.py > /tmp/l15-independent-count.json
python3 independent/src/gray_model_check.py proof/sources/known_false_model.json > /tmp/l15-gray-model.json
sha256sum -c SHA256SUMS.txt
printf '%s\n' L15_INDEPENDENT_REPLAY_OK
