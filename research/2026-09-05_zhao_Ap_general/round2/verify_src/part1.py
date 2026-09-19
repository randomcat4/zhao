#!/usr/bin/env python3
"""Exact finite-interface checks for the round-2 A_p proof.

These checks do not enumerate F_p^4 sequences and are not the universal proof.
The universal arguments and their inherited assumptions are in research_note.md.
Only Python's standard library is used. No numerical solver/tolerance is used.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import comb, isqrt
from pathlib import Path
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parent


def primes_through(n: int) -> list[int]:
    return [p for p in range(5, n + 1)
            if all(p % d for d in range(2, isqrt(p) + 1))]


def det3(a: list[list[int]]) -> int:
    return (a[0][0] * (a[1][1]*a[2][2] - a[1][2]*a[2][1])
            - a[0][1] * (a[1][0]*a[2][2] - a[1][2]*a[2][0])
            + a[0][2] * (a[1][0]*a[2][1] - a[1][1]*a[2][0]))


def solve_mod(a: list[list[int]], b: list[int], p: int) -> list[int]:
    rows = [[x % p for x in row] + [rhs % p] for row, rhs in zip(a, b)]
    n = len(a)
    for j in range(n):
        k = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[k] = rows[k], rows[j]
        inv = pow(rows[j][j], -1, p)
        rows[j] = [(v * inv) % p for v in rows[j]]
        for i in range(n):
            if i != j:
                f = rows[i][j]
                rows[i] = [(u - f*v) % p for u, v in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def check_parameter_interfaces(ps: list[int]) -> dict:
    expected = [[-1, 1, -1], [1, -2, 3], [-1, 3, -6]]
    assert det3(expected) == -1
    compressed_lengths_checked = 0
    for p in ps:
        h, m = p-3, 4*p-1
        lengths = [3*p, 3*p+1, 3*p+2]
        a = [[(-1)**k * comb(m-k, d) % p for k in lengths] for d in range(3)]
        b = [-comb(m, d) % p for d in range(3)]
        assert a == [[x % p for x in row] for row in expected]
        assert solve_mod(a, b, p) == [1, 0, 0]
        represented = set(range(h+1)) | {(2+j) % p for j in range(h+1)}
        assert represented == set(range(p))
        g = lambda x: (x*x-1)*(x*x-4) % p
        assert g(0) == 4 % p
        assert all(g(x) == 0 for x in [1, -1, 2, -2])
        for n in range(3*p+3, 4*p-2):
            assert n % p != 0
            if n % 2 == 0:
                assert n > 3*(p-1)+4
                assert (2*g(0)) % p != 0
            else:
                assert n > 3*(p-1)+5
                assert (-n*g(0)) % p != 0
            compressed_lengths_checked += 1
        assert solve_mod([[1, -2], [2, -3]], [0, 0], p) == [0, 0]
        r = (p-1)//2
        assert (2*r + 1) % p == 0
        assert 0 < r <= h < p
        assert [d for d in range(1, h+1) if d % p == r] == [r]
        solutions = [(t, eps) for t in range((3*p-1)//(p-1)+1)
                     for eps in [0, 1]
                     if (p-1)*t + ((p+1)//2)*eps == 3*p-1]
        assert not solutions
    return {
        'prime_count': len(ps), 'prime_range': [ps[0], ps[-1]],
        'deletion_matrix_over_Z': expected, 'deletion_matrix_determinant': -1,
        'forced_residues': [1, 0, 0],
        'compression_length_cases': compressed_lengths_checked,
        'local_moment_matrix': [[1, -2], [2, -3]],
        'local_moment_determinant': 1,
        'star_size_equation_solutions': 0,
        'universal_support': 'The symbolic argument, not this finite prime range.'
    }


def check_positional_complement_formulas() -> dict:
    rng = random.Random(26090502)
    tests = 0
    for p in [5, 7, 11]:
        n = 3*p
        universe = frozenset(range(n))
        all_pairs = list(combinations(range(n), 2))
        all_triples = list(combinations(range(n), 3))
        for _ in range(40):
            pp = [frozenset(x) for x in rng.sample(all_pairs, rng.randrange(1, 12))]
            ff = [frozenset(x) for x in rng.sample(all_triples, rng.randrange(1, 12))]
            terms = [(frozenset(), 0), (universe, 0)]
            for block in pp:
                terms += [(block, 1), (universe-block, -1)]
            for block in ff:
                terms += [(block, 2), (universe-block, -2)]
            assert sum((-1)**len(u)*c for u, c in terms) == 2*len(pp)-4*len(ff)
            for i in range(n):
                ei = sum(i in u for u in pp)
                fi = sum(i in u for u in ff)
                literal = sum((-1)**len(u) for u, _ in terms if i not in u)
                assert literal == 1+len(pp)-len(ff)-2*ei+2*fi
                tests += 1
    return {'literal_single_deletion_checks': tests,
            'first_moment_family_checks': 120,
            'positional_subsets_not_value_sets': True}


def check_empty_intersection_witnesses() -> dict:
    triples = [frozenset(t) for t in combinations(range(7), 3)]
    minimal = {3: 0, 4: 0}
    graphs: set[tuple[tuple[int, int], ...]] = set()
    for t in [3, 4]:
        for fam in combinations(triples, t):
            if any(not (x & y) for x, y in combinations(fam, 2)):
                continue
            if set.intersection(*(set(e) for e in fam)):
                continue
            if t == 4 and any(not set.intersection(*(set(e) for j, e in enumerate(fam) if j != i))
                              for i in range(t)):
                continue
            minimal[t] += 1
            union = set.union(*(set(e) for e in fam))
            assert len(union) <= (6 if t == 3 else 4)
            pairs = tuple(pair for pair in combinations(sorted(union), 2)
                          if all(set(pair) & e for e in fam))
            degrees = Counter(v for pair in pairs for v in pair)
            assert max(degrees.values(), default=0) <= 3
            graphs.add(pairs)
    four_clique_tests = 0
    for pairs in graphs:
        for four in combinations(pairs, 4):
            assert not all(set(a) & set(b) for a, b in combinations(four, 2))
            four_clique_tests += 1
    return {
        'abstract_ground_set_size': 7,
        'minimal_witness_counts': minimal,
        'distinct_pair_transversal_graphs': len(graphs),
        'four_edge_clique_tests': four_clique_tests,
        'maximum_pair_transversal_degree': 3,
        'scope': 'Finite checks of the witness/graph interface, not a proof by exhaustion.'
    }


def check_link_involution() -> dict:
    results = []
    for p in [5, 7]:
        h, r = p-3, (p-1)//2
