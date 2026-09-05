#!/usr/bin/env python3
"""Fresh exact count of labeled-point, unordered, simple regular hypergraphs.

This implementation does not read the candidate certificate or import its code.
It uses the signed cycle-index form of injection inclusion-exclusion and a
separate histogram recursion that chooses the *smallest* remaining cycle weight,
with no candidate-package pruning rules.
"""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb, factorial
import json


def partitions(n: int, max_part: int | None = None):
    if n == 0:
        yield ()
        return
    max_part = n if max_part is None else min(max_part, n)
    for first in range(max_part, 0, -1):
        for tail in partitions(n - first, first):
            yield (first,) + tail


def exact_count(v: int, edge_size: int, edges: int, degree: int):
    if edge_size * edges != v * degree:
        return 0, None, 0

    @lru_cache(maxsize=None)
    def assignments(hist: tuple[int, ...], groups: tuple[int, ...]) -> int:
        if not groups:
            return int(hist[0] == v)
        w = groups[0]  # deliberately opposite order from the candidate generator
        rest = groups[1:]
        residual_classes = tuple(range(w, degree + 1))
        picked = [0] * len(residual_classes)
        total = 0

        def choose(i: int, left: int) -> None:
            nonlocal total
            if i == len(residual_classes):
                if left != 0:
                    return
                nxt = list(hist)
                factor = 1
                for r, k in zip(residual_classes, picked):
                    if k > nxt[r]:
                        return
                    factor *= comb(nxt[r], k)
                    nxt[r] -= k
                    nxt[r - w] += k
                total += factor * assignments(tuple(nxt), rest)
                return
            r = residual_classes[i]
            for k in range(min(hist[r], left) + 1):
                picked[i] = k
                choose(i + 1, left - k)

        choose(0, edge_size)
        return total

    ordered_injective = 0
    cycle_types = 0
    for cycle_type in partitions(edges):
        if cycle_type[0] > degree:
            continue
        groups = tuple(sorted(cycle_type))
        value = assignments((0,) * degree + (v,), groups)
        mult = Counter(cycle_type)
        number_of_permutations = factorial(edges)
        for w, m in mult.items():
            number_of_permutations //= (w ** m) * factorial(m)
        sign = -1 if (edges - len(cycle_type)) % 2 else 1
        ordered_injective += sign * number_of_permutations * value
        cycle_types += 1

    quotient, remainder = divmod(ordered_injective, factorial(edges))
    if remainder:
        raise ArithmeticError("nonintegral unordered count")
    return quotient, assignments.cache_info(), cycle_types


def brute_force(v: int, edge_size: int, edges: int, degree: int) -> int:
    blocks = list(combinations(range(v), edge_size))
    answer = 0
    for family in combinations(blocks, edges):
        degrees = [0] * v
        for block in family:
            for point in block:
                degrees[point] += 1
        answer += degrees == [degree] * v
    return answer


def main() -> None:
    toy_parameters = [
        (4, 2, 2, 1),
        (4, 2, 4, 2),
        (5, 2, 5, 2),
        (6, 3, 2, 1),
        (6, 2, 3, 1),
    ]
    toys = []
    for parameters in toy_parameters:
        formula, _, _ = exact_count(*parameters)
        direct = brute_force(*parameters)
        if formula != direct:
            raise AssertionError((parameters, formula, direct))
        toys.append({"parameters": parameters, "formula": formula, "brute_force": direct})

    full, cache, cycle_types = exact_count(21, 7, 15, 5)
    expected = 860662922414727068051994283870582495183777624400448
    if full != expected:
        raise AssertionError((full, expected))
    print(json.dumps({
        "method": "fresh signed-cycle-index inclusion-exclusion plus independent no-prune histogram recursion",
        "toy_direct_enumeration_tests": toys,
        "full_parameters": [21, 7, 15, 5],
        "cycle_types_processed": cycle_types,
        "cache": {
            "hits": cache.hits,
            "misses": cache.misses,
            "size": cache.currsize,
        },
        "association_total": str(full),
        "matches_candidate": True,
        "normal_exit": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
