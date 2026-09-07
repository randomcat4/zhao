#!/usr/bin/env python3
"""Exact interface checks for A_p round 4 (standard library only).

The proofs are in research_note.md. This is not a sequence enumeration,
not a proof-assistant certificate, and not a proof of h <= p-5 or A_p.
All reported counts are obtained from loops actually executed here.
"""
from __future__ import annotations

import hashlib
import itertools as it
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def primes_up_to(n: int) -> list[int]:
    return [p for p in range(2, n + 1)
            if all(p % d for d in range(2, math.isqrt(p) + 1))]


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def rank_mod(rows: list[list[int]], p: int) -> int:
    a = [[x % p for x in row] for row in rows]
    r = 0
    for j in range(len(a[0])):
        i = next((i for i in range(r, len(a)) if a[i][j]), None)
        if i is None:
            continue
        a[r], a[i] = a[i], a[r]
        u = pow(a[r][j], -1, p)
        a[r] = [x * u % p for x in a[r]]
        for i in range(len(a)):
            if i != r:
                u = a[i][j]
                a[i] = [(x - u * y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def check_marked_lifts() -> dict:
    cases = coefficient_checks = marginal_checks = 0
    single_basis = [[1, 3, 3, 1, 0], [0, 1, 3, 3, 1]]
    pair_basis = [[1, 2, 1, 0, 0], [0, 1, 2, 1, 0], [0, 0, 1, 2, 1]]
    for p in primes_up_to(199):
        if p < 7:
            continue
        for qmax, basis in [(2, single_basis), (1, pair_basis)]:
            mat = [[(-1) ** j * choose(p-j, q) for j in range(5)]
                   for q in range(qmax + 1)]
            assert rank_mod(mat, p) == qmax + 1
            for v in basis:
                for row in mat:
                    assert sum(x*y for x, y in zip(row, v)) % p == 0
                    coefficient_checks += 1
            cases += 1
        for beta in range(p):
            single = [0, beta, 3*beta, 3*beta, beta]
            for j in range(1, 5):
                assert ((3*p+j-1) * single[j] - (j-1)*single[j]) % p == 0
                marginal_checks += 1
        assert (3*p+4)*(p-1) - (3*p+1)*(p-4) == 12*p
        assert (3*p+3)*(p-4) - (3*p+2)*(p-6) == 7*p
        assert sum([p-4, p-6, p-4, p-1]) + 2*p == 6*p-15
    damaged = [0, 1, 2, 3, 1]
    p = 7
    mat = [[(-1)**j * choose(p-j, q) for j in range(5)] for q in range(3)]
    assert any(sum(x*y for x, y in zip(row, damaged)) % p for row in mat)
    return {"marked_matrix_cases": cases,
            "kernel_equations_checked": coefficient_checks,
            "marginal_length_reductions_checked": marginal_checks,
            "single_basis": single_basis, "pair_basis": pair_basis,
            "damaged_single_basis_rejected": True}


def check_p7_positive_certificate() -> dict:
    rows = []
    w = [Fraction(1, 6), Fraction(1, 5), Fraction(1, 4), Fraction(1, 3)]
    for t in range(7):
        residues = [(r-a*t) % 7 for r, a in zip([3, 1, 3, 6], [1, 3, 3, 1])]
        score = sum((a*b for a, b in zip(w, residues)), Fraction(0))
        assert score >= Fraction(5, 3)
        rows.append({"beta": t, "residues": residues, "score": str(score)})
    assert min(Fraction(row["score"]) for row in rows) == Fraction(5, 3)
    threshold = 28 * Fraction(5, 3)
    minimum_total = next(13 + 7*u for u in range(100) if 13+7*u >= threshold)
    assert minimum_total == 48
    assert Fraction(140, 3) == threshold
    return {"rows": rows, "positive_weights": [str(x) for x in w],
            "summed_rational_bound": str(threshold),
            "integer_count_bound": minimum_total}


def partitions(n: int, largest: int | None = None):
    if n == 0:
        yield ()
        return
    if largest is None:
        largest = n
    for b in range(min(n, largest), 0, -1):
        for rest in partitions(n-b, b):
            yield (b,) + rest


def check_simultaneous_replacement_bound() -> dict:
    checked = rejected_multiple_replacement = 0
    summaries = []
    for k in range(3, 7):
        maximum = 0
        local = 0
        for b in partitions(k-1):
            for q in [-1, *range(len(b))]:
                for external in it.product(range(k), repeat=len(b)):
                    if q >= 0 and external[q] == 0:
                        continue
                    e = [external[j]-int(j == q) for j in range(len(b))]
                    capacities = sum(min(bj, ej) for bj, ej in zip(b, e))
                    ways = math.prod(math.comb(bj+ej, bj) for bj, ej in zip(b, e))
                    h = max([1, *[bj+tj for bj, tj in zip(b, external)]])
                    if capacities >= 2:
                        rejected_multiple_replacement += 1
                        continue
                    assert ways <= min(k, h)
                    positive = [(bj, ej) for bj, ej in zip(b, e) if ej]
                    if positive:
                        assert len(positive) == 1
                        bj, ej = positive[0]
                        assert min(bj, ej) == 1
                        assert ways == bj+ej
                    else:
                        assert ways == 1
                    maximum = max(maximum, ways)
                    checked += 1
                    local += 1
        summaries.append({"k": k, "admissible_capacity_cases": local,
                          "maximum_degree_seen": maximum})
    positional = 0
    for b in partitions(3):
        for external in it.product(range(4), repeat=len(b)):
            labels = []
            B = []
            for j, bj in enumerate(b):
                B.extend(range(len(labels), len(labels)+bj))
                labels.extend([j]*bj)
            B = set(B)
            for j, extra in enumerate(external):
                labels.extend([j]*extra)
            all_choices = [set(c) for c in it.combinations(range(len(labels)), 3)
                           if tuple(sum(labels[i] == j for i in c) for j in range(len(b))) == b]
            double_hit = all(len(C & B) >= 2 for C in all_choices)
            capacity_condition = sum(min(bj, ej) for bj, ej in zip(b, external)) <= 1
            assert double_hit == capacity_condition
            if double_hit:
                assert len(all_choices) <= min(4, max(bj+ej for bj, ej in zip(b, external)))
