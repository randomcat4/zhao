"""Independently count all position zero sums in one recorded 18-term leaf.

The verifier uses four integer coordinates and Gray-code enumeration, and does
not import or reuse the subsequence-distance implementation being checked.
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
data = json.loads((BASE / "evidence/atom_four_independent_A.json").read_text(encoding="utf-8"))
record = next(r for r in data["runs"] if r["max_reached_length"] == 18)
encoded = [g for g in (1, 5, 25, 125) for _ in range(3)] + record["one_longest_extension"]
coords = [tuple((g // 5**i) % 5 for i in range(4)) for g in encoded]
counts = [0] * (len(coords) + 1)
current = [0, 0, 0, 0]
weight = 0
previous = 0
for k in range(1, 1 << len(coords)):
    gray = k ^ (k >> 1)
    flip = gray ^ previous
    i = flip.bit_length() - 1
    sign = 1 if gray & flip else -1
    weight += sign
    for j in range(4):
        current[j] = (current[j] + sign * coords[i][j]) % 5
    if current == [0, 0, 0, 0]:
        counts[weight] += 1
    previous = gray

out = {
    "n": len(coords),
    "sequence_coordinates": coords,
    "zero_sum_counts_by_length": {str(k): v for k, v in enumerate(counts) if v},
    "subsets_checked": (1 << len(coords)) - 1,
    "minimum_zero_sum_length": next(k for k, v in enumerate(counts) if v),
}
assert out["minimum_zero_sum_length"] > 13
(BASE / "evidence/atom_four_longest18_graycheck.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out))
