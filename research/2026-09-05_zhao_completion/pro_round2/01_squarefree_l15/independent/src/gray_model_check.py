#!/usr/bin/env python3
"""Third exact checker for the pinned false model, using Gray-code updates."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--reference", type=Path)
    args = parser.parse_args()
    data = json.loads(args.fixture.read_text())
    vectors = [tuple(v) for v in data["vectors"]]
    n = len(vectors)
    if n != 21 or len(set(vectors)) != 21 or (0, 0, 0, 0) in vectors:
        raise ValueError("fixture is not 21 distinct nonzero vectors")
    target = tuple(sum(v[j] for v in vectors) % 5 for j in range(4))
    zero_counts = [0] * (n + 1)
    zero_counts[0] = 1
    fibers = {k: [] for k in range(4, 8)}
    current_sum = (0, 0, 0, 0)
    current_weight = 0
    previous_gray = 0
    for index in range(1, 1 << n):
        gray = index ^ (index >> 1)
        changed = gray ^ previous_gray
        bit = (changed & -changed).bit_length() - 1
        if gray & changed:
            current_sum = tuple((current_sum[j] + vectors[bit][j]) % 5 for j in range(4))
            current_weight += 1
        else:
            current_sum = tuple((current_sum[j] - vectors[bit][j]) % 5 for j in range(4))
            current_weight -= 1
        if current_sum == (0, 0, 0, 0):
            zero_counts[current_weight] += 1
        if 4 <= current_weight <= 7 and current_sum == target:
            fibers[current_weight].append(gray)
        previous_gray = gray
    for masks in fibers.values():
        masks.sort()

    agreement = None
    if args.reference:
        reference = json.loads(args.reference.read_text())
        agreement = zero_counts == reference["zero_counts"] and all(
            fibers[k] == reference["full_fibers"][str(k)] for k in fibers
        )
        if not agreement:
            raise AssertionError("Gray-code result disagrees with reference")

    print(json.dumps({
        "method": "Gray-code single-bit modular update",
        "processed": 1 << n,
        "zero_counts_0_through_21": zero_counts,
        "short_zero_count_1_through_13": sum(zero_counts[1:14]),
        "full_fiber_counts_4_through_7": {str(k): len(v) for k, v in fibers.items()},
        "reference_agreement": agreement,
        "normal_exit": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
