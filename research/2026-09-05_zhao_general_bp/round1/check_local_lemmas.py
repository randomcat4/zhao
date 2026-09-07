#!/usr/bin/env python3
"""Finite implementation checks accompanying the symbolic proofs.

No test here establishes B_p, and no B_p counterexample is included.
The universal conclusions are proved in Bp_parameterized_review.md.
"""
from collections import Counter
from itertools import combinations, permutations
import json
from pathlib import Path
from verify_bp_candidate import is_prime, self_test


def main():
    primes = [p for p in range(5, 44) if is_prime(p)]
    triples = equalities = 0
    for p in primes:
        for A in combinations(range(p), 3):
            total = sum(A)
            lhs = Counter((total-a) % p for a in A)
            for s in range(p):
                triples += 1
                rhs = Counter((s+2*total+a) % p for a in A)
                if lhs == rhs:
                    equalities += 1
                    assert any((s+5*a) % p == 0 for a in A)
    near_period_checks = 0
    collinear_capacity_checks = 0
    for p in primes:
        k = p-3
        for h in range(1, p):
            segment = {(j*h) % p for j in range(k+1)}
            for extra in (False, True):
                X = segment | ({(-h) % p} if extra else set())
                shifted = {(x+h) % p for x in X}
                assert shifted-X == {(-2*h) % p}
                assert X-shifted == ({(-h) % p} if extra else {0})
                near_period_checks += 1
        for t in range(2, p):
            if t == 2:
                coefficients = (2, p-4, 2)
            elif t == p-1:
                coefficients = (p-4, 2, 2)
            else:
                coefficients = (t-1, p-t, 1)
            assert sum(coefficients) == p
            assert all(0 <= c <= k for c in coefficients)
            assert (coefficients[1]+t*coefficients[2]) % p == 0
            collinear_capacity_checks += 1
        # If 2a=b+c, (p-4)a+2b+2c is an admissible p-zero.
        assert 0 <= p-4 <= k and 2 <= k
    # Each collision vector has exactly four nonzero entries and one zero.
    relations = sorted(set(permutations((2, -1, -2, 1, 0))))
    independent_pairs = 0
    for u in relations:
        j = u.index(0)
        i = next(k for k in range(5) if u[k])
        for v in relations:
            if v[j]:
                # The indicated 2x2 determinant is ±1, ±2, or ±4.
                determinant = u[i]*v[j]
                assert abs(determinant) in (1, 2, 4)
                assert all(determinant % p != 0 for p in primes)
                independent_pairs += 1
    for p in primes:
        for r in range(5, (5*p-5)//(p-3)+1):
            remaining = 5*p-5-r*(p-3)
            lhs = r*(r-1)
            rhs = remaining*(r//2)
            assert (lhs <= rhs) == (r == 5)
            if r == 5:
                assert remaining == 10 and lhs == rhs
    report = {
        "status": "PASS",
        "endpoint_status": "NOT_PROVED_NO_COUNTEREXAMPLE",
        "prime_range": primes,
        "root_interpolation_cases": triples,
        "root_multiset_equalities": equalities,
        "near_period_orbit_checks": near_period_checks,
        "collinear_capacity_checks": collinear_capacity_checks,
        "integer_collision_vectors": len(relations),
        "rank_minor_checks": independent_pairs,
        "candidate_verifier_self_test": self_test(),
        "scope": "finite checks only; universal lemmas have separate symbolic proofs",
    }
    print(json.dumps(report, indent=2))
    Path(__file__).with_name("local_checks.json").write_text(
        json.dumps(report, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
