#!/usr/bin/env python3
"""Exact, finite interface checks for the accompanying A_p research note.

This is NOT an exhaustive search for A_p counterexamples and NOT a proof of A_p.
The all-prime arguments are in research_note.md.  This script uses only the
Python standard library; all arithmetic below is exact (integers or F_p).
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


def require(test: bool, message: str) -> None:
    if not test:
        raise AssertionError(message)


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def primes_up_to(limit: int) -> list[int]:
    return [n for n in range(5, limit + 1)
            if all(n % d for d in range(2, math.isqrt(n) + 1))]


def rank_mod(matrix: list[list[int]], p: int) -> int:
    a = [[x % p for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [(x * inv) % p for x in a[r]]
        for i in range(r + 1, len(a)):
            if a[i][c]:
                scale = a[i][c]
                a[i] = [(x - scale * y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def check_deletion() -> dict:
    layers = 0
    homogeneous_basis_vectors = 0
    tested = primes_up_to(43)
    for p in tested:
        D, N = 4 * p - 3, 5 * p - 4
        lengths = list(range(3 * p - 1, D + 1))
        for m in range(D, N + 1):
            A = [[((-1) ** k) * choose(m - k, d) % p for k in lengths]
                 for d in range(m - D + 1)]
            rhs = [-choose(m, d) % p for d in range(m - D + 1)]
            z = [int(k == 3 * p) for k in lengths]
            require(all(sum(x * y for x, y in zip(row, z)) % p == b
                        for row, b in zip(A, rhs)), 'deletion particular solution')
            free = max(5 * p - 5 - m, 0)
            require(rank_mod(A, p) == (p - 1 - free), 'deletion rank')
            exponent = m - D + 1
            for j in range(free):
                # Delta P(t) = (t-1)^exponent t^j.
                coeff = {j + i: choose(exponent, i) * (-1) ** (exponent - i)
                         for i in range(exponent + 1)}
                dz = [((-1) ** k) * coeff.get(D - k, 0) % p for k in lengths]
                require(all(sum(x * y for x, y in zip(row, dz)) % p == 0
                            for row in A), 'deletion homogeneous basis')
                homogeneous_basis_vectors += 1
            layers += 1
    return {'primes': tested, 'layers': layers,
            'homogeneous_basis_vectors': homogeneous_basis_vectors,
            'claim': 'Finite checks of the proven symbolic parametrization, not an all-prime enumeration.'}


def add_vector(x: tuple[int, ...], y: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + b) % p for a, b in zip(x, y))


def signed_distribution(sequence: list[tuple[int, ...]], p: int,
                        marked: set[int]) -> dict[tuple[int, ...], int]:
    """Coefficients of the signed subset-sum polynomial, forcing marked positions."""
    zero = (0,) * len(sequence[0])
    dp = {zero: 1}
    for i, v in enumerate(sequence):
        out: dict[tuple[int, ...], int] = defaultdict(int)
        for s, count in dp.items():
            if i not in marked:
                out[s] = (out[s] + count) % p
            t = add_vector(s, v, p)
            out[t] = (out[t] - count) % p
        dp = {s: count for s, count in out.items() if count}
    return dp


def check_marked_moments() -> dict:
    rng = random.Random(20260905)
    cases = []
    for p in (5, 7):
        for d in (1, 2, 3):
            for degree in (0, 1, 2):
                for mark_count in (0, 1):
                    n = d * (p - 1) + degree + mark_count + 1
                    sequence = [tuple(rng.randrange(p) for _ in range(d + 1))
                                for _ in range(n)]
                    # Make repeated values explicit rather than testing only sets.
                    if n >= 3:
                        sequence[1] = sequence[0]
                    dist = signed_distribution(sequence, p, set(range(mark_count)))
                    value = sum(count * pow(s[-1], degree, p)
                                for s, count in dist.items() if all(x == 0 for x in s[:-1])) % p
                    require(value == 0, 'marked quotient moment')
                    cases.append({'p': p, 'projection_rank': d, 'degree': degree,
                                  'marked_positions': mark_count, 'n': n})
    return {'number_of_tests': len(cases), 'cases': cases,
            'claim': 'Exact DP tests of the Boolean-polynomial identity; no counterexample search.'}


def projective_reps(p: int) -> list[tuple[int, int, int, int]]:
    result = []
    for first in range(4):
        for tail in itertools.product(range(p), repeat=3 - first):
            result.append(tuple([0] * first + [1] + list(tail)))
    return result


def dot(x: tuple[int, ...], y: tuple[int, ...], p: int) -> int:
    return sum(a * b for a, b in zip(x, y)) % p


def count_projected_zeros(values: list[int], p: int) -> list[int]:
    n = len(values)
    dp = [[0] * p for _ in range(n + 1)]
    dp[0][0] = 1
    for i, value in enumerate(values):
        for k in range(i + 1, 0, -1):
            for t in range(p):
                dp[k][(t + value) % p] += dp[k - 1][t]
    return [row[0] for row in dp]


def zero_counts(sequence: list[tuple[int, ...]], p: int) -> list[int]:
    n = len(sequence)
    result = [0] * (n + 1)
    for mask in range(1 << n):
        total = (0,) * len(sequence[0])
        for i, v in enumerate(sequence):
            if mask >> i & 1:
                total = add_vector(total, v, p)
