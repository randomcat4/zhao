"""Exact small-prime probe for complete zero-sum-free sequences in C_p^2.

This is only a finite diagnostic.  It enumerates nondecreasing multisets of
length 2p-3 over the nonzero elements of C_p^2, maintains their ordinary
subset-sum support exactly, and records sequences whose nonempty subset sums
cover every nonzero target.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def add_index(p: int, left: int, right: int) -> int:
    return (((left // p) + (right // p)) % p) * p + ((left + right) % p)


def neg_index(p: int, value: int) -> int:
    return ((-(value // p)) % p) * p + (-(value % p)) % p


def shift_mask(p: int, mask: int, value: int) -> int:
    shifted = 0
    cursor = mask
    while cursor:
        bit = cursor & -cursor
        index = bit.bit_length() - 1
        shifted |= 1 << add_index(p, index, value)
        cursor ^= bit
    return shifted


def vector(p: int, index: int) -> tuple[int, int]:
    return index // p, index % p


def search(p: int, stop_after: int) -> dict[str, object]:
    target_length = 2 * p - 3
    full_mask = (1 << (p * p)) - 1
    sequence: list[int] = []
    solutions: list[list[tuple[int, int]]] = []
    nodes = 0

    def dfs(start: int, reachable: int) -> None:
        nonlocal nodes
        nodes += 1
        if len(solutions) >= stop_after:
            return
        remaining = target_length - len(sequence)
        if reachable.bit_count() * (1 << remaining) < p * p:
            return
        if remaining == 0:
            if reachable == full_mask:
                solutions.append([vector(p, item) for item in sequence])
            return
        for value in range(start, p * p):
            if value == 0:
                continue
            if reachable & (1 << neg_index(p, value)):
                continue
            shifted = shift_mask(p, reachable, value)
            sequence.append(value)
            dfs(value, reachable | shifted)
            sequence.pop()
            if len(solutions) >= stop_after:
                return

    dfs(1, 1)
    return {
        "p": p,
        "length": target_length,
        "nodes": nodes,
        "complete_zero_sum_free_solutions": solutions,
        "stopped_after": stop_after,
        "status": "FINITE_PROBE_ONLY",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=5)
    parser.add_argument("--stop-after", type=int, default=10)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = search(args.p, args.stop_after)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.report is not None:
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
