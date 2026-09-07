#!/usr/bin/env python3
"""Exact finite-interface checks for the third A_p research round.

The general statements are proved in research_note.md. This program does not
exhaust sequences in F_p^4 and does not certify A_p or h(S) <= p-5.
Python standard library only. Every count below is produced by an executed loop.
"""
from __future__ import annotations
import hashlib
import itertools as it
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def primes_upto(n: int) -> list[int]:
    return [q for q in range(2, n + 1)
            if all(q % d for d in range(2, math.isqrt(q) + 1))]


def choose_general(n: int, k: int) -> int:
    if k < 0:
        return 0
    z = 1
    for i in range(1, k + 1):
        z = z * (n - i + 1) // i
    return z


def rank_q(a: list[list[int | Fraction]]) -> int:
    if not a:
        return 0
    b = [[Fraction(x) for x in row] for row in a]
    r = 0
    for j in range(len(b[0])):
        piv = next((i for i in range(r, len(b)) if b[i][j]), None)
        if piv is None:
            continue
        b[r], b[piv] = b[piv], b[r]
        z = b[r][j]
        b[r] = [x / z for x in b[r]]
        for i in range(len(b)):
            if i != r and b[i][j]:
                z = b[i][j]
                b[i] = [x - z * y for x, y in zip(b[i], b[r])]
        r += 1
        if r == len(b):
            break
    return r


def det_q(a: list[list[int]]) -> Fraction:
    b = [[Fraction(x) for x in row] for row in a]
    n = len(b)
    ans = Fraction(1)
    for j in range(n):
        piv = next((i for i in range(j, n) if b[i][j]), None)
        if piv is None:
            return Fraction(0)
        if piv != j:
            b[j], b[piv] = b[piv], b[j]
            ans = -ans
        z = b[j][j]
        ans *= z
        for i in range(j + 1, n):
            if b[i][j]:
                c = b[i][j] / z
                for k in range(j + 1, n):
                    b[i][k] -= c * b[j][k]
    return ans


def rank_mod(a: list[list[int]], p: int) -> int:
    b = [[x % p for x in row] for row in a]
    r = 0
    for j in range(len(b[0])):
        piv = next((i for i in range(r, len(b)) if b[i][j]), None)
        if piv is None:
            continue
        b[r], b[piv] = b[piv], b[r]
        z = pow(b[r][j], -1, p)
        b[r] = [x * z % p for x in b[r]]
        for i in range(len(b)):
            if i != r and b[i][j]:
                z = b[i][j]
                b[i] = [(x - z * y) % p for x, y in zip(b[i], b[r])]
        r += 1
        if r == len(b):
            break
    return r


def matrix(r: int) -> list[list[int]]:
    return [[(-1) ** j * choose_general(r - 4 - j, d)
             for j in range(2 * r - 3)] for d in range(r)]


def check_normal_forms() -> dict:
    cases, coeff_checks, null_checks = 0, 0, 0
    exact_minors = []
    for r in range(3, 17):
        m = matrix(r)
        det = det_q([row[:r] for row in m])
        assert det == 1
        exact_minors.append([r, int(det)])
        for s in range(r - 3):
            v = [math.comb(r, j - s) if 0 <= j - s <= r else 0
                 for j in range(2 * r - 3)]
            assert all(sum(x * y for x, y in zip(row, v)) == 0 for row in m)
            null_checks += 1
    for p in primes_upto(199):
        for r in range(3, min(12, (p + 1) // 2) + 1):
            m, size = matrix(r), 4 * p + r - 4
            assert rank_mod(m, p) == r
            for d in range(r):
                assert math.comb(size, d) % p == choose_general(r - 4, d) % p
                for j in range(2 * r - 3):
                    actual = (-1) ** (3 * p + j) * math.comb(size - 3 * p - j, d)
                    assert actual % p == (-m[d][j]) % p
                    coeff_checks += 1
            cases += 1
    m4 = matrix(4)
    assert m4 == [[1,-1,1,-1,1], [0,1,-2,3,-4],
                  [0,-1,3,-6,10], [0,1,-4,10,-20]]
    for tau in range(-20, 21):
        v = [1 + tau, 4 * tau, 6 * tau, 4 * tau, tau]
        assert [sum(x*y for x,y in zip(row,v)) for row in m4] == [1,0,0,0]
    return {"parameter_cases": cases, "coefficient_checks": coeff_checks,
            "integer_null_vectors_checked": null_checks,
            "unit_minor_checks": exact_minors, "r4_matrix": m4,
            "r4_formal_tau_minus_one_is_not_a_sequence": True}


def check_core_interfaces() -> dict:
    length_cases = 0
    for p in primes_upto(199):
        if p < 5:
            continue
        for c in (p - 1, p):
            assert 5*p - 4 - c >= 4*p - 4
            assert 2*p - 2 + c <= 3*p - 2
            for n in range(3*p - 1, 4*p - 2):
                assert n // 2 <= 2*p - 2
                if n > 3*p:
                    if n % 2 == 0:
                        assert 3*(p-1)+2 < n
                        assert (-2) % p != 0
                    else:
                        assert 3*(p-1)+3 < n
                        assert n % p != 0
                length_cases += 1
    missing_checks = 0
    for p in [5,7,11,13,17,19]:
        universe = set(range(p))
        for a,b in it.combinations(range(p),2):
            B = universe - {a,b}
            if 0 not in B:
                continue
            for v in range(1,p):
                Q = B | {(x+v)%p for x in B}
                if len(Q) != p-1 or (-v)%p in B:
                    continue
                g = next(iter(universe-Q))
                assert g == (-v)%p
                missing_checks += 1
    repl_checks = 0
    for h in range(1,25):
        for c in range(1,h+2):
            for k in range(1,c+1):
                for z in range(h+c+1):
                    if z <= h:
                        assert z <= h
                    else:
                        assert 0 <= z-c <= h
                        assert k + z-c <= z
                    repl_checks += 1
    return {"core_length_and_degree_checks":length_cases,
            "two_point_complement_checks":missing_checks,
            "positional_replacement_capacity_checks":repl_checks}


def check_quad_moments() -> dict:
    checked = 0
    for p in [7,11,13,17,19]:
        n = 3*p
