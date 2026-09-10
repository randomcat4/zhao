#!/usr/bin/env python3
"""Finite checks for the special-deletion and second-branch notes.

The local construction checked here is deliberately not a test that Z is an
atom, and it does not implement the complete seven-point/Hasse design.
"""

from collections import Counter


def primes_through(limit):
    ans = []
    for n in range(2, limit + 1):
        if all(n % d for d in range(2, int(n**0.5) + 1)):
            ans.append(n)
    return ans


def frac(num, den, p):
    return num * pow(den, -1, p) % p


def vec_add(*vectors, p):
    return tuple(sum(v[j] for v in vectors) % p for j in range(3))


def vec_neg(v, p):
    return tuple(-x % p for x in v)


def vec_scale(c, v, p):
    return tuple(c * x % p for x in v)


def r3(x, p):
    return (x + 3) * (1 - 2 * x) * pow(3, -1, p) % p


def r4(x, lam, p):
    return (
        -(x + 3) * pow(3, -1, p)
        + lam * x * (x - 1) * (x + 3)
    ) % p


def check_interpolation(p):
    q1 = frac(-3, 4, p)
    q2 = frac(3, 10, p)
    q3 = frac(-1, 20, p)

    assert r3(0, p) == 1 % p
    assert r3(1, p) == frac(-4, 3, p)
    assert r3(-3, p) == 0
    assert q2 * r3(2, p) % p == frac(-3, 2, p)
    assert q3 * r3(3, p) % p == frac(1, 2, p)

    for lam in range(p):
        assert r4(0, lam, p) == -1 % p
        assert r4(1, lam, p) == frac(-4, 3, p)
        assert r4(-3, lam, p) == 0
        g2 = q2 * r4(2, lam, p) % p
        g3 = q3 * r4(3, lam, p) % p
        assert g2 == (frac(-1, 2, p) + 3 * lam) % p
        assert g3 == (frac(1, 10, p) - frac(9, 5, p) * lam) % p
        assert (3 * g2 + 5 * g3) % p == -1 % p

    if p == 7:
        assert q1 == q2 == q3 == 1


def fixed_e_coordinates(u6, u7, p):
    v8 = (3 - 3 * u6 + 9 * u7) * pow(5, -1, p) % p
    u4 = (u6 - 2 * u7 - frac(5, 2, p)) % p
    u5 = (2 * u6 - 3 * u7 - 2) % p
    v6 = (v8 + frac(9, 10, p)) % p
    v7 = (2 * v8 + frac(4, 5, p)) % p
    return u4, u5, u6, u7, v6, v7, v8


def check_fixed_e(p):
    for u6 in range(p):
        for u7 in range(p):
            u4, u5, u6x, u7x, v6, v7, v8 = fixed_e_coordinates(
                u6, u7, p
            )
            assert (u4 - u5 + u6x - u7x) % p == frac(-1, 2, p)
            assert (
                2 * u4 - 3 * u5 + 4 * u6x - 5 * u7x
            ) % p == 1
            assert (v6 - v7 + v8) % p == frac(1, 10, p)
            assert (4 * v6 - 5 * v7 + 6 * v8) % p == frac(-2, 5, p)

            f2 = u4 - 3 * u5 + 6 * u6x - 10 * u7x
            f3 = 6 * v6 - 10 * v7 + 15 * v8
            assert (6 * f2 + 10 * f3) % p == 1

    explicit = fixed_e_coordinates(0, 0, p)
    u4, u5, u6, u7, v6, v7, v8 = explicit
    assert u6 == u7 == 0
    assert u4 == (p - 5) // 2
    assert u4 <= 2 * (p - 4)
    assert v8 == frac(3, 5, p)
    assert v6 == frac(3, 2, p)
    assert v7 == 2 % p


def check_b_prime_atom(p):
    solutions = []
    for t in range(3):
        required = -t % p
        if required <= p - 2:
            solutions.append((t, required))
    assert solutions == [(0, 0), (2, p - 2)]
    assert 3 * (p - 2) + 2 == 3 * p - 4


def add_position(counter, quotient, height, copies, p):
    counter[(tuple(x % p for x in quotient), height % p)] += copies


def quotient_sum(counter, p):
    total = (0, 0, 0)
    for (q, _height), copies in counter.items():
        total = vec_add(total, vec_scale(copies, q, p), p=p)
    return total


def height_sum(counter, p):
    return sum(height * copies for (_q, height), copies in counter.items()) % p


def size(counter):
    return sum(counter.values())


def combine(*counters):
    ans = Counter()
    for counter in counters:
        ans.update(counter)
    return ans


def check_common_e_model(p):
    zero = (0, 0, 0)
    e1 = (1, 0, 0)
    e2 = (0, 1, 0)
    e3 = (0, 0, 1)
    g = (1, 1, 1)
    minus_g = vec_neg(g, p)
    m = (p - 1) // 2
    delta = (-m - 9) % p

    z_all = Counter()
    add_position(z_all, e1, 0, m, p)

    e_block = Counter()
    add_position(e_block, vec_scale(2, e1, p), 0, 1, p)
    add_position(e_block, vec_scale(-2, e1, p), 1, 1, p)

    p_block = Counter()
    add_position(p_block, vec_scale(3, e1, p), 0, 1, p)
    add_position(p_block, vec_scale(-3, e1, p), 1, 1, p)

    t_block = Counter()
    add_position(t_block, e2, 0, 1, p)
    add_position(t_block, e3, 0, 1, p)
    add_position(t_block, minus_g, 1, 1, p)

    x_block = Counter()
    add_position(x_block, e1, 1, m, p)
    add_position(x_block, e2, 0, p - 5, p)
    add_position(x_block, e2, 1, 3, p)
    add_position(x_block, e3, 0, p - 5, p)
    add_position(x_block, e3, 1, 3, p)
    add_position(x_block, g, 0, 1, p)
    add_position(x_block, g, delta, 1, p)

    assert m <= p - 4
    assert quotient_sum(e_block, p) == zero
    assert quotient_sum(p_block, p) == zero
    assert quotient_sum(t_block, p) == vec_neg(e1, p)
    assert height_sum(e_block, p) == 1
    assert height_sum(p_block, p) == 1
    assert height_sum(t_block, p) == 1
    assert height_sum(x_block, p) == -3 % p

    one_z = Counter()
    add_position(one_z, e1, 0, 1, p)
    other_z = Counter()
    add_position(other_z, e1, 0, m - 1, p)

    d_i = combine(t_block, one_z)
    c_i = combine(e_block, d_i)
    a_i = combine(c_i, p_block)
    b_i = combine(x_block, other_z)
    z_model = combine(e_block, t_block, p_block, z_all, x_block)
    a_zero = combine(e_block, t_block, p_block)

    assert size(d_i) == 4
    assert size(c_i) == 6
    assert size(a_i) == 8
    assert size(b_i) == 3 * p - 4
    assert size(z_model) == 3 * p + 4

    assert quotient_sum(d_i, p) == zero
    assert quotient_sum(c_i, p) == zero
    assert quotient_sum(a_i, p) == zero
    assert quotient_sum(b_i, p) == zero
    assert quotient_sum(z_model, p) == zero
    assert quotient_sum(a_zero, p) == vec_neg(e1, p)

    assert height_sum(d_i, p) == 1
    assert height_sum(c_i, p) == 2
    assert height_sum(a_i, p) == 3
    assert height_sum(b_i, p) == -3 % p
    assert height_sum(z_model, p) == 0

    assert max(z_model.values()) <= p - 4
    assert z_model[(e1, 0)] == m

    expected_b = Counter()
    add_position(expected_b, e1, 0, m - 1, p)
    expected_b.update(x_block)
    assert b_i == expected_b

    quotient_multiset = Counter()
    for (q, _height), copies in b_i.items():
        quotient_multiset[q] += copies
    assert quotient_multiset[e1] == p - 2
    assert quotient_multiset[e2] == p - 2
    assert quotient_multiset[e3] == p - 2
    assert quotient_multiset[g] == 2
    assert sum(quotient_multiset.values()) == 3 * p - 4

    assert e1 != zero
    assert vec_add(e1, vec_neg(e1, p), p=p) == zero
    assert e1 != zero and vec_neg(e1, p) != zero


def main():
    primes = [p for p in primes_through(500) if p >= 7]
    for p in primes:
        check_interpolation(p)
        check_fixed_e(p)
        check_b_prime_atom(p)
        check_common_e_model(p)

    print(
        "PASS: t=3/4 interpolation, fixed-E length coordinates, "
        "B' atomicity, and common-E local models"
    )
    print(
        "Checked every prime 7 <= p <= 500. "
        "The local model does not assert that Z is an atom and does not "
        "implement the full seven-point/Hasse design."
    )


if __name__ == "__main__":
    main()
