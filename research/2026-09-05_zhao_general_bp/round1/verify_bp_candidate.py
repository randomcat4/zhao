#!/usr/bin/env python3
"""Exact positional verifier for a proposed counterexample to B_p.

Input JSON: {"p": 7, "sequence": [[0,1,2,3], ...]}
A counterexample must have exactly 5*p-5 positions, p prime >= 7, and
no nonempty zero-sum positional subset of size <= 3*p-1.

This program does not contain or claim to have found a counterexample.
It uses only Python's standard library. Its dynamic programming works
with integer counts, not floating point or a solver's feasibility flag.
"""
from __future__ import annotations
import argparse
import json
import math
import random
import sys
from pathlib import Path
from typing import Sequence

Vec = tuple[int, int, int, int]
ZERO: Vec = (0, 0, 0, 0)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))


def add(a: Vec, b: Vec, p: int) -> Vec:
    return ((a[0]+b[0]) % p, (a[1]+b[1]) % p,
            (a[2]+b[2]) % p, (a[3]+b[3]) % p)


def zero_counts(sequence: Sequence[Vec], p: int) -> list[int]:
    """Count all zero-sum position subsets, separately for each length.

    Descending length updates ensure each position can be used only once.
    Repeated values are deliberately processed as separate positions.
    """
    n = len(sequence)
    layers: list[dict[Vec, int]] = [{ZERO: 1}] + [{} for _ in range(n)]
    for index, g in enumerate(sequence):
        for length in range(index + 1, 0, -1):
            src, dst = layers[length-1], layers[length]
            for h, count in src.items():
                target = add(h, g, p)
                dst[target] = dst.get(target, 0) + count
    # Verify the mass of every layer, not just its zero coefficient.
    for length, layer in enumerate(layers):
        if sum(layer.values()) != math.comb(n, length):
            raise AssertionError(f"DP mass failure at length {length}")
    return [layer.get(ZERO, 0) for layer in layers]


def brute_counts(sequence: Sequence[Vec], p: int) -> list[int]:
    """Separate exhaustive implementation, used only for small self-tests."""
    n = len(sequence)
    out = [0] * (n + 1)
    for mask in range(1 << n):
        total = [0, 0, 0, 0]
        length = 0
        for i, g in enumerate(sequence):
            if mask & (1 << i):
                length += 1
                for j in range(4):
                    total[j] += g[j]
        if all(t % p == 0 for t in total):
            out[length] += 1
    return out


def parse_candidate(path: Path) -> tuple[int, list[Vec]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    p = raw.get("p")
    if type(p) is not int or p < 7 or not is_prime(p):
        raise ValueError("p must be a prime >= 7")
    rows = raw.get("sequence")
    if not isinstance(rows, list) or len(rows) != 5*p-5:
        raise ValueError(f"sequence must contain exactly {5*p-5} positions")
    sequence: list[Vec] = []
    for i, row in enumerate(rows):
        if (not isinstance(row, list) or len(row) != 4
                or any(type(x) is not int or not 0 <= x < p for x in row)):
            raise ValueError(f"position {i}: expected four integers in [0,p)")
        sequence.append((row[0], row[1], row[2], row[3]))
    return p, sequence


def self_test() -> dict:
    rng = random.Random(20260905)
    cases = 0
    for p in (5, 7, 11):
        for n in range(11):
            sequence = [tuple(rng.randrange(p) for _ in range(4))
                        for _ in range(n)]
            if n >= 3:
                sequence[1] = sequence[0]  # Test repeated positions.
            assert zero_counts(sequence, p) == brute_counts(sequence, p)
            cases += 1
    for p in (5, 7, 11):
        for rank in (1, 2, 3):
            for n in (8, 10):
                sequence = [tuple([rng.randrange(p) for _ in range(rank)]
                                  + [0] * (4-rank)) for _ in range(n)]
                assert zero_counts(sequence, p) == brute_counts(sequence, p)
                cases += 1
        sequence = [ZERO] * 10
        assert zero_counts(sequence, p) == [math.comb(10, k) for k in range(11)]
        cases += 1
    for p in (5, 7):
        sequence = [(1, 0, 0, 0)] * (p + 2)
        counts = zero_counts(sequence, p)
        assert counts[p] == math.comb(p + 2, p)
        assert sum(counts[1:]) == counts[p]
        cases += 1
    return {"status": "PASS", "cases": cases,
            "scope": "implementation self-test, not a proof of B_p"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2))
        return 0
    if args.candidate is None:
        parser.error("supply a candidate JSON file or --self-test")
    try:
        p, sequence = parse_candidate(args.candidate)
        counts = zero_counts(sequence, p)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(exc)}))
        return 2
    short_count = sum(counts[1:3*p])
    result = {
        "status": "VERIFIED_COUNTEREXAMPLE" if short_count == 0 else "REJECTED",
        "p": p,
        "positions": len(sequence),
        "forbidden_max_length": 3*p-1,
        "short_zero_position_count": short_count,
        "nonempty_zero_counts_by_length": {
            str(k): counts[k] for k in range(1, len(counts)) if counts[k]
        },
        "arithmetic": "exact integers; all positions counted separately",
    }
    print(json.dumps(result, indent=2))
    return 0 if short_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
