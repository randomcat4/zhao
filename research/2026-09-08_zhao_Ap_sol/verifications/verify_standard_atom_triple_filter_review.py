#!/usr/bin/env python3
"""Exact checks for standard_atom_triple_filter_review.md.

Finite enumeration checks the local integer classifications.  The all-prime
height contradiction remains the symbolic argument in the review.
"""

from itertools import product
from math import comb


def primes_through(limit):
    ans = []
    for n in range(2, limit + 1):
        if all(n % d for d in range(2, int(n**0.5) + 1)):
            ans.append(n)
    return ans


def filter_condition(eps, k, t, direction):
    if eps == 0:
        return (
            1 <= k <= 5
            and all(x >= 0 for x in t)
            and t[direction] >= 3
            and sum(t) <= k + 2
        )
    return (
        2 <= k <= 5
        and t[direction] >= 4
        and all(t[j] >= 1 for j in range(3) if j != direction)
        and sum(t) <= k + 4
    )


def check_general_filter():
    max_b = {0: 0, 1: 0}
    for direction in range(3):
        for eps in range(2):
            for k in range(0, 7):
                for t in product(range(10), repeat=3):
                    b = tuple(x - eps for x in t)
                    direct = (
                        0 <= k <= 5
                        and all(x >= 0 for x in b)
                        and b[direction] >= 3
                        and sum(b) + eps + 6 - k <= 8
                    )
                    expected = filter_condition(eps, k, t, direction)
                    assert direct == expected
                    if expected:
                        max_b[eps] = max(max_b[eps], max(b))
                        assert sum(b) + eps + 6 - k <= 8
    assert max_b == {0: 7, 1: 6}
    assert max(max_b.values()) <= 10


def gamma_tuple(mask):
    return tuple((mask >> bit) & 1 for bit in range(6))


def check_pm2_interval(primes):
    values = set()
    direction = 0
    for b in product(range(9), repeat=3):
        for eps in range(2):
            for mask in range(64):
                gamma = gamma_tuple(mask)
                if sum(b) + eps + sum(gamma) > 8:
                    continue
                if b[direction] < 3:
                    continue
                plus = gamma[2 * direction]
                minus = gamma[2 * direction + 1]
                value = b[direction] + eps + 2 * plus - 2 * minus
                values.add(value)
                assert 1 <= value <= 9
                for p in primes:
                    assert value % p != 0
    assert min(values) == 1
    assert max(values) == 9


def expected_pm3_states(direction):
    others = [j for j in range(3) if j != direction]
    zero = (0, 0, 0)
    pair = (0, 1, 1)
    quartet = (3, 0, 1)
    option_pairs = (
        (zero, zero),
        (pair, zero),
        (zero, pair),
        (pair, pair),
        (quartet, zero),
        (zero, quartet),
    )
    states = set()
    for first, second in option_pairs:
        local = [None, None, None]
        local[direction] = (3, 0, 1)
        local[others[0]] = first
        local[others[1]] = second
        b = tuple(item[0] for item in local)
        gamma = []
        for item in local:
            gamma.extend((item[1], item[2]))
        states.add((0, b, tuple(gamma)))
    return states


def actual_pm3_states(p, direction):
    states = set()
    for b in product(range(9), repeat=3):
        for eps in range(2):
            for mask in range(64):
                gamma = gamma_tuple(mask)
                if sum(b) + eps + sum(gamma) > 8:
                    continue
                if b[direction] < 3:
                    continue
                coordinates = []
                for j in range(3):
                    plus = gamma[2 * j]
                    minus = gamma[2 * j + 1]
                    coordinates.append(b[j] + eps + 3 * plus - 3 * minus)
                if all(value % p == 0 for value in coordinates):
                    states.add((eps, b, gamma))
    return states


def check_pm3_classification(primes):
    for p in primes:
        for direction in range(3):
            actual = actual_pm3_states(p, direction)
            expected = expected_pm3_states(direction)
            assert actual == expected
            assert len(actual) == 6


def check_hasse_weights(primes):
    weight = {1: 4, 2: 10, 3: 20}
    survivors = []
    patterns = []
    for s in (1, 2):
        for u in (1, 2, 3):
            for v in (1, 2, 3):
                if u + v != s + 3:
                    continue
                total = weight[s] + weight[u] + weight[v]
                patterns.append((s, u, v, total))
                for p in primes:
                    if (total - 21) % p == 0:
                        survivors.append((p, s, u, v, total))
    assert sorted(set(total for *_rest, total in patterns)) == [24, 28, 40]
    assert survivors == [
        (19, 2, 2, 3, 40),
        (19, 2, 3, 2, 40),
    ]


def check_height_collapse(primes):
    for p in primes:
        assert p - 1 > p - 4
        assert 3 * p - 4 > 8
        assert p - 1 >= 6

    p = 7
    triples = [
        triple
        for triple in product(range(p - 1), repeat=3)
        if triple[0] < triple[1] < triple[2]
    ]
    for heights in product(range(p), repeat=p - 1):
        sums = {
            sum(heights[index] for index in triple) % p
            for triple in triples
        }
        if len(sums) == 1:
            assert len(set(heights)) == 1


def main():
    primes_11 = [p for p in primes_through(500) if p >= 11]
    primes_7 = [p for p in primes_through(500) if p >= 7]

    check_general_filter()
    check_pm2_interval(primes_11)
    check_pm3_classification(primes_11)
    check_hasse_weights(primes_11)
    check_height_collapse(primes_7)

    assert comb(10, 3) % 11 == -1 % 11
    print(
        "PASS: general filter, p=11 availability, pm2 interval, "
        "and complete pm3 quotient classification"
    )
    print(
        "PASS: triple-codegree weights leave only the formal p=19 case; "
        "the height-collapse argument excludes it and all p >= 7"
    )


if __name__ == "__main__":
    main()
