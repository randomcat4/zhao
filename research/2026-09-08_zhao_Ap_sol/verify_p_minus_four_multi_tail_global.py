#!/usr/bin/env python3
"""Exact audits for the p-4 multi-tail/global-count interface.

This script checks four finite pieces used in
``proofs/p_minus_four_multi_tail_global.md``:

1. the containment-type poset has height at most three;
2. every surviving three-chain has the advertised diamond partner type;
3. a fixed 20 by 20 minor of the safe aggregate Hasse system is
   -2^12*5^3, so the aggregates impose only the F3 X-point equation;
4. FORMAL_TAIL_INTERFACE_COMPATIBILITY holds for every prime in a
   regression range: the named tails satisfy the exact X-point equation and
   all named-pair interfaces.

The formal object does not enumerate all short blocks induced by its assigned
labels, does not construct B or Z, and does not realize the free aggregate
variables as nonnegative incidences.  It is not a local candidate or a
counterexample to the frozen theorem.
"""

from __future__ import annotations

from itertools import combinations, permutations
from math import ceil, comb


WINDOWS = {
    1: tuple(range(2, 7)),
    2: tuple(range(4, 8)),
    3: tuple(range(6, 9)),
}

TAIL_TYPES = tuple(
    (length, b, length - b)
    for length in WINDOWS[3]
    for b in range(1, length - 1)  # positive core, no singleton tail
)


def neg_binom(shift: int, k: int) -> int:
    """Return binom(-shift,k) as an ordinary integer."""
    if k < 0:
        return 0
    return (-1) ** k * comb(shift + k - 1, k)


def nested_type_possible(top, bottom) -> bool:
    """All type-only necessary conditions for bottom subsetneq top."""
    _lt, bt, rt = top
    _lb, bb, rb = bottom
    db = bb - bt
    dr = rt - rb
    if not (1 <= db <= 3 and dr >= 1):
        return False
    # A one-position difference of sum x would be an extra copy of x.
    if db == 1 and dr == 1:
        return False
    return True


def audit_containment_types():
    assert len(TAIL_TYPES) == 15

    four_chains = []
    for chain in permutations(TAIL_TYPES, 4):
        if all(nested_type_possible(chain[i], chain[i + 1]) for i in range(3)):
            # The nesting theorem also applies to the extreme pair.
            if nested_type_possible(chain[0], chain[-1]):
                four_chains.append(chain)
    assert not four_chains

    raw_three_chains = []
    surviving_three_chains = []
    rejected_by_exchange_window = []
    for chain in permutations(TAIL_TYPES, 3):
        top, middle, bottom = chain
        if not (
            nested_type_possible(top, middle)
            and nested_type_possible(middle, bottom)
            and nested_type_possible(top, bottom)
        ):
            continue
        raw_three_chains.append(chain)
        d1 = middle[1] - top[1]
        partner_b = bottom[1] - d1
        partner_r = bottom[2] + top[2] - middle[2]
        partner = (partner_b + partner_r, partner_b, partner_r)
        if partner in TAIL_TYPES:
            surviving_three_chains.append((chain, partner))
            assert bottom[2] < partner_r < top[2]
            assert top[1] < partner_b < bottom[1]
            # The partner position set is different from the middle one even
            # when their parameter triples happen to agree.
        else:
            rejected_by_exchange_window.append((chain, partner))

    assert len(raw_three_chains) == 23
    assert len(surviving_three_chains) == 16
    assert len(rejected_by_exchange_window) == 7

    containment_caps = {}
    for top in TAIL_TYPES:
        child_sizes = {
            bottom[2]
            for bottom in TAIL_TYPES
            if nested_type_possible(top, bottom)
        }
        containment_caps[top] = sum(comb(top[2], r) for r in child_sizes)
    assert max(containment_caps.values()) == 112
    assert containment_caps[(8, 1, 7)] == 112
    return raw_three_chains, surviving_three_chains, containment_caps


def variable_keys():
    keys = []
    for family in (1, 2):
        for length in WINDOWS[family]:
            for b in range(length):
                keys.extend((('N', family, length, b), ('J', family, length, b)))
    for length in WINDOWS[3]:
        keys.extend((('N', 3, length, 0), ('J', 3, length, 0)))
    return tuple(keys)


VARIABLES = variable_keys()
INDEX = {key: i for i, key in enumerate(VARIABLES)}


def aggregate_free_matrix():
    """Build the p-independent free-variable matrix of the 21 safe equations."""
    rows = []
    names = []

    def new_row(name):
        names.append(name)
        rows.append([0] * len(VARIABLES))
        return rows[-1]

    def add(row, kind, family, length, b, value):
        key = (kind, family, length, b)
        if key in INDEX:
            row[INDEX[key]] += value

    for family in (1, 2, 3):
        row = new_row(f'zero_{family}')
        for length in WINDOWS[family]:
            for b in range(length):
                add(row, 'N', family, length, b,
                    (-1) ** (length - 1) * neg_binom(4, b))
        row = new_row(f'x_point_{family}')
        for length in WINDOWS[family]:
            for b in range(1, length):
                add(row, 'N', family, length, b,
                    (-1) ** (length - 1) * neg_binom(5, b - 1))

    for name, family_coefficients in (
        ('x_pair_12', {1: 8, 2: 10}),
        ('x_pair_13', {1: 2, 3: -10}),
    ):
        row = new_row(name)
        for family in (1, 2, 3):
            for length in WINDOWS[family]:
                for b in range(2, length):
                    add(row, 'N', family, length, b,
                        family_coefficients.get(family, 0)
                        * (-1) ** length * neg_binom(6, b - 2))

    row = new_row('x_triple')
    for family, fc in ((1, 4), (2, 10), (3, 20)):
        for length in WINDOWS[family]:
            for b in range(3, length):
                add(row, 'N', family, length, b,
                    fc * (-1) ** (length - 1) * neg_binom(7, b - 3))

    for family in (1, 2, 3):
        row = new_row(f'T_point_{family}')
        for length in WINDOWS[family]:
            for b in range(length):
                add(row, 'J', family, length, b,
                    (-1) ** (length - 1) * neg_binom(4, b))

    for name, family_coefficients in (
        ('T_pair_12', {1: 8, 2: 10}),
        ('T_pair_13', {1: 2, 3: -10}),
    ):
        row = new_row(name)
        for family in (1, 2, 3):
            for length in WINDOWS[family]:
                for b in range(1, length):
                    add(row, 'J', family, length, b,
                        family_coefficients.get(family, 0)
                        * (-1) ** length * neg_binom(5, b - 1))

    row = new_row('T_triple')
    for family, fc in ((1, 4), (2, 10), (3, 20)):
        for length in WINDOWS[family]:
            for b in range(2, length):
                add(row, 'J', family, length, b,
                    fc * (-1) ** (length - 1) * neg_binom(6, b - 2))

    def add_q_row(name, order, family_coefficients, shift, sign_power):
        row = new_row(name)
        for family in (1, 2, 3):
            fc = family_coefficients.get(family, 0)
            for length in WINDOWS[family]:
                for b in range(order, length):
                    base = fc * (-1) ** (length + sign_power) * neg_binom(
                        shift, b - order
                    )
                    remainder_size = length - b
                    add(row, 'N', family, length, b, base * remainder_size)
                    add(row, 'J', family, length, b, -base)

    for family in (1, 2, 3):
        add_q_row(
            f'Q_point_{family}', 0, {family: 1}, 4, -1
        )
    add_q_row('Q_pair_12', 1, {1: 8, 2: 10}, 5, 0)
    add_q_row('Q_pair_13', 1, {1: 2, 3: -10}, 5, 0)
    add_q_row('Q_triple', 2, {1: 4, 2: 10, 3: 20}, 6, -1)

    assert len(rows) == 21
    assert all(value == 0 for value in rows[names.index('x_point_3')])
    return rows, names


MINOR_KEYS = (
    ('N', 1, 2, 0), ('J', 1, 2, 0),
    ('N', 1, 2, 1), ('J', 1, 2, 1),
    ('N', 1, 3, 0), ('N', 1, 3, 1),
    ('N', 1, 3, 2), ('J', 1, 3, 2),
    ('N', 1, 4, 2), ('N', 1, 4, 3),
    ('N', 2, 4, 0), ('J', 2, 4, 0),
    ('N', 2, 4, 1), ('J', 2, 4, 1),
    ('N', 2, 4, 2), ('N', 2, 5, 0),
    ('N', 2, 5, 1),
    ('N', 3, 6, 0), ('J', 3, 6, 0),
    ('N', 3, 7, 0),
)


def bareiss_det(matrix):
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next(i for i in range(k + 1, n) if a[i][k])
            a[k], a[swap] = a[swap], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (
                    a[i][j] * pivot - a[i][k] * a[k][j]
                ) // previous
        previous = pivot
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[-1][-1]


def audit_aggregate_rank():
    rows, names = aggregate_free_matrix()
    kept_rows = [row for row, name in zip(rows, names) if name != 'x_point_3']
    columns = [INDEX[key] for key in MINOR_KEYS]
    minor = [[row[column] for column in columns] for row in kept_rows]
    determinant = bareiss_det(minor)
    assert determinant == -512000
    assert abs(determinant) == 2 ** 12 * 5 ** 3
    return determinant


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def add_vec(left, right, p):
    return tuple((x + y) % p for x, y in zip(left, right))


def sub_vec(left, right, p):
    return tuple((x - y) % p for x, y in zip(left, right))


def scalar_vec(value, vector, p):
    return tuple(value * x % p for x in vector)


def audit_formal_tail_interface(prime: int):
    assert prime >= 11 and is_prime(prime)
    m = prime - 4
    t = pow(700, -1, prime)
    n5, n4 = divmod(t, 2)
    counts = {4: n4, 5: n5}
    tail_count = n4 + n5

    # Exact fixed-X F3 point degree.
    x_degree = sum(
        counts[b] * (-1) ** ((b + 3) - 1) * comb(m - 1, b - 1)
        for b in (4, 5)
    ) % prime
    target = -pow(20, -1, prime) % prime
    assert x_degree == target
    assert tail_count >= ceil((prime - 1) / 2520)
    assert n4 <= prime - 4 and n5 <= prime - 4

    q = (1, 0, 0)
    w = (0, 1, 0)
    z = (0, 0, 1)
    common = add_vec(w, z, prime)
    leaf = {
        b: (-b % prime, -1 % prime, -1 % prime)
        for b in (4, 5)
    }

    for b, c in combinations((4, 5, 4, 5), 2):
        # Repetitions represent two different position copies of the same leaf.
        k0 = max(0, b + c - m)
        for k in range(k0, min(b, c) + 1):
            assert add_vec(common, scalar_vec(k, q, prime), prime) != (0, 0, 0)

        # The only quotient-equal subexchanges are the empty and full ones.
        qualifying = []
        for use_left in (0, 1):
            for use_right in (0, 1):
                difference = sub_vec(
                    scalar_vec(use_left, leaf[b], prime),
                    scalar_vec(use_right, leaf[c], prime),
                    prime,
                )
                d_low = -b + k0
                d_high = c - k0
                ds = [
                    d for d in range(d_low, d_high + 1)
                    if scalar_vec(d, q, prime) == difference
                ]
                qualifying.extend((use_left, use_right, d) for d in ds)
        assert qualifying == [(0, 0, 0), (1, 1, c - b)]

    # The common T-part has nonzero quotient sum and is proper in a 6-set T.
    assert common != (0, 0, 0)
    return tail_count


def main():
    raw, surviving, caps = audit_containment_types()
    determinant = audit_aggregate_rank()
    tested_primes = [p for p in range(11, 20001) if is_prime(p)]
    tail_counts = [audit_formal_tail_interface(p) for p in tested_primes]
    print(f'tail_types={len(TAIL_TYPES)}')
    print(f'raw_three_chain_types={len(raw)}')
    print(f'exchange_feasible_three_chain_types={len(surviving)}')
    print(f'max_proper_contained_tails={max(caps.values())}')
    print(f'aggregate_minor_det={determinant}')
    print(f'formal_tail_interfaces_checked={len(tested_primes)} primes through 20000')
    print(f'formal_tail_count_range={min(tail_counts)}..{max(tail_counts)}')
    print('PASS')


if __name__ == '__main__':
    main()
