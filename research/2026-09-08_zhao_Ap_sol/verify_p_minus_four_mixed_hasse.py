from fractions import Fraction as F
from math import gcd


def choose(n, k):
    """Polynomial binomial coefficient, also for negative n."""
    if k < 0:
        return F(0)
    ans = F(1)
    for i in range(k):
        ans *= F(n - i, i + 1)
    return ans


WINDOWS = {
    1: range(2, 7),
    2: range(4, 8),
    3: range(6, 9),
}
POINT = {1: F(-3, 4), 2: F(3, 10), 3: F(-1, 20)}

# A key (lam, ell, b, j) assigns the displayed weight to every tail U with
# |U|=ell-b and |U intersect T|=j.  Unlisted orbit weights are zero.
TABLES = {
    6: {
        (1, 2, 0, 1): F(-203, 18),
        (1, 2, 0, 2): F(4699, 1440),
        (1, 3, 0, 1): F(-233, 18),
        (1, 3, 1, 1): F(1381, 1152),
        (1, 3, 1, 2): F(-37, 60),
        (1, 4, 1, 1): F(2245, 1152),
        (1, 4, 2, 1): F(-53, 576),
        (1, 4, 2, 2): F(257, 2880),
        (1, 5, 2, 1): F(-161, 576),
        (1, 5, 3, 1): F(-1, 48),
        (2, 4, 0, 2): F(23, 50),
        (2, 4, 0, 3): F(509, 4800),
        (2, 4, 1, 1): F(1, 60),
        (2, 4, 1, 2): F(-7, 1440),
        (2, 4, 2, 1): F(-7, 2880),
        (2, 5, 0, 3): F(8, 15),
        (2, 5, 1, 2): F(2, 75),
        (3, 6, 0, 4): F(43, 7200),
        (3, 6, 0, 5): F(-1, 360),
        (3, 6, 1, 3): F(-37, 19200),
        (3, 6, 2, 2): F(-17, 14400),
    },
    7: {
        (1, 2, 0, 1): F(-6221, 672),
        (1, 2, 0, 2): F(-37, 36),
        (1, 3, 0, 2): F(-233, 63),
        (1, 3, 1, 1): F(493, 672),
        (1, 4, 1, 2): F(2245, 4032),
        (1, 4, 2, 1): F(15, 448),
        (1, 5, 2, 2): F(-23, 288),
        (1, 5, 3, 1): F(-1, 28),
        (2, 4, 0, 3): F(71, 280),
        (2, 4, 0, 4): F(34, 525),
        (2, 4, 1, 2): F(-11, 5040),
        (2, 4, 2, 1): F(-1, 240),
        (2, 5, 0, 4): F(32, 105),
        (2, 5, 1, 3): F(2, 175),
        (3, 6, 0, 5): F(1, 288),
        (3, 6, 0, 6): F(-1, 420),
        (3, 6, 1, 4): F(-37, 33600),
        (3, 6, 2, 3): F(-17, 33600),
    },
    8: {
        (1, 2, 0, 1): F(21, 32),
        (1, 2, 0, 2): F(-8293, 2688),
        (1, 3, 0, 3): F(-233, 168),
        (1, 3, 1, 1): F(-7, 32),
        (1, 3, 1, 2): F(493, 2688),
        (1, 4, 1, 3): F(2245, 10752),
        (1, 4, 2, 1): F(1, 32),
        (1, 4, 2, 2): F(15, 1792),
        (1, 5, 2, 3): F(-23, 768),
        (1, 5, 3, 2): F(-1, 112),
        (2, 4, 0, 1): F(-7, 80),
        (2, 4, 0, 4): F(191, 1200),
        (2, 4, 1, 1): F(1, 80),
        (2, 4, 1, 3): F(-11, 13440),
        (2, 4, 2, 2): F(-1, 960),
        (2, 5, 0, 5): F(4, 21),
        (2, 5, 1, 4): F(1, 175),
        (3, 6, 0, 1): F(1, 160),
        (3, 6, 0, 6): F(9, 4480),
        (3, 6, 1, 5): F(-37, 53760),
        (3, 6, 2, 4): F(-17, 67200),
    },
}


def orbit_total(s, ell, b, j):
    r = ell - b
    return choose(s, j) * choose(8 - s, r - j)


def orbit_degree(s, side, ell, b, j):
    r = ell - b
    if side == "T":
        return choose(s - 1, j - 1) * choose(8 - s, r - j)
    return choose(s, j) * choose(7 - s, r - j - 1)


def linear_checks(s, table):
    def sum_terms(term):
        return sum((weight * term(key) for key, weight in table.items()), F(0))

    values = {}
    for lam in (1, 2, 3):
        values[f"zero_{lam}"] = sum_terms(
            lambda z: (-1) ** (z[1] - 1) * orbit_total(s, *z[1:])
            if z[0] == lam else F(0)
        )
        values[f"x_point_{lam}"] = sum_terms(
            lambda z: (-1) ** (z[1] - 1)
            * choose(-5, z[2] - 1) * orbit_total(s, *z[1:])
            if z[0] == lam and z[2] >= 1 else F(0)
        )

    values["x_pair_12"] = sum_terms(
        lambda z: {1: 8, 2: 10}.get(z[0], 0) * (-1) ** z[1]
        * choose(-6, z[2] - 2) * orbit_total(s, *z[1:])
        if z[2] >= 2 else F(0)
    )
    values["x_pair_13"] = sum_terms(
        lambda z: {1: 2, 3: -10}.get(z[0], 0) * (-1) ** z[1]
        * choose(-6, z[2] - 2) * orbit_total(s, *z[1:])
        if z[2] >= 2 else F(0)
    )
    values["x_triple"] = sum_terms(
        lambda z: {1: 4, 2: 10, 3: 20}[z[0]] * (-1) ** (z[1] - 1)
        * choose(-7, z[2] - 3) * orbit_total(s, *z[1:])
        if z[2] >= 3 else F(0)
    )

    for side in ("T", "Q"):
        for lam in (1, 2, 3):
            values[f"{side}_point_{lam}"] = sum_terms(
                lambda z: (-1) ** (z[1] - 1) * choose(-4, z[2])
                * orbit_degree(s, side, *z[1:]) if z[0] == lam else F(0)
            )
        values[f"{side}_pair_12"] = sum_terms(
            lambda z: {1: 8, 2: 10}.get(z[0], 0) * (-1) ** z[1]
            * choose(-5, z[2] - 1) * orbit_degree(s, side, *z[1:])
            if z[2] >= 1 else F(0)
        )
        values[f"{side}_pair_13"] = sum_terms(
            lambda z: {1: 2, 3: -10}.get(z[0], 0) * (-1) ** z[1]
            * choose(-5, z[2] - 1) * orbit_degree(s, side, *z[1:])
            if z[2] >= 1 else F(0)
        )
        values[f"{side}_triple"] = sum_terms(
            lambda z: {1: 4, 2: 10, 3: 20}[z[0]] * (-1) ** (z[1] - 1)
            * choose(-6, z[2] - 2) * orbit_degree(s, side, *z[1:])
            if z[2] >= 2 else F(0)
        )

    expected = {f"zero_{lam}": F(0) for lam in (1, 2, 3)}
    expected.update({f"x_point_{lam}": POINT[lam] for lam in (1, 2, 3)})
    expected.update({"x_pair_12": F(3), "x_pair_13": F(1), "x_triple": F(-1)})
    for side in ("T", "Q"):
        expected.update({f"{side}_point_{lam}": POINT[lam] for lam in (1, 2, 3)})
        expected.update({
            f"{side}_pair_12": F(3),
            f"{side}_pair_13": F(1),
            f"{side}_triple": F(-1),
        })
    assert values == expected, (
        s,
        {key: (values[key], expected[key]) for key in values if values[key] != expected[key]},
    )

    high_x = sum(
        weight * orbit_total(s, ell, b, j)
        for (lam, ell, b, j), weight in table.items()
        if b >= 3
    )
    assert high_x != 0


def mixed_sums(model):
    pair = {lam: F(0) for lam in (1, 2, 3)}
    triple = {lam: F(0) for lam in (1, 2, 3)}
    for (lam, ell, b), count in model.items():
        r = ell - b
        if b >= 1:
            pair[lam] += (-1) ** ell * r * choose(-5, b - 1) * count
        if b >= 2:
            triple[lam] += (-1) ** (ell - 1) * r * choose(-6, b - 2) * count
    return (
        8 * pair[1] + 10 * pair[2],
        2 * pair[1] - 10 * pair[3],
        4 * triple[1] + 10 * triple[2] + 20 * triple[3],
    )


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


for s, table in TABLES.items():
    for (lam, ell, b, j), weight in table.items():
        r = ell - b
        assert ell in WINDOWS[lam]
        assert 0 <= b <= ell - 2
        assert 2 <= r and 1 <= j <= min(r, s)
        assert r - j <= 2 * 11 + 8 - s
        for p in range(11, 501):
            if is_prime(p):
                assert gcd(weight.denominator, p) == 1
    linear_checks(s, table)

old_sparse = {
    (1, 6, 1): F(3, 4),
    (2, 6, 1): F(6, 5),
    (2, 7, 2): F(-3, 10),
    (3, 6, 1): F(3, 10),
    (3, 7, 2): F(-1, 5),
    (3, 8, 3): F(1, 20),
}
surviving_sparse = {
    (1, 5, 1): F(-9, 2),
    (1, 5, 2): F(-3, 2),
    (1, 5, 3): F(-1, 4),
    (2, 6, 1): F(6, 5),
    (2, 6, 2): F(3, 10),
    (3, 7, 1): F(9, 20),
    (3, 7, 2): F(1, 10),
}

assert mixed_sums(old_sparse) == (F(15), F(5), F(-5))
assert mixed_sums(surviving_sparse) == (F(24), F(8), F(-8))

print("PASS: all three T-size orbit certificates satisfy 21 exact equations")
print("PASS: every displayed tail meets T and has size at least two")
print("PASS: old sparse mixed sums are (15, 5, -5), not (24, 8, -8)")
print("PASS: surviving aggregate mixed sums are (24, 8, -8)")
print("SCOPE: weighted F_p incidence certificates, not actual quotient-labelled block families")
