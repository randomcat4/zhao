"""Exact finite checks for proofs/standard_atom_full_exclusion.md.

The proof itself is symbolic.  This script checks every parameter edge for
primes 11..500, exhausts all two-height multiplicity patterns in that range,
and exhausts all normalized three-height patterns for primes 11..101.
"""

from __future__ import annotations


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


PRIMES_500 = [p for p in range(11, 501) if is_prime(p)]
PRIMES_101 = [p for p in PRIMES_500 if p <= 101]

WINDOWS = {
    4: {1, 2},
    5: {1, 2},
    6: {1, 2, 3},
    7: {2, 3},
    8: {3},
}


def target_bound(ell: int) -> int:
    return len(WINDOWS[ell])


def two_value_sums(p: int, alpha: int, beta: int, t: int) -> set[int]:
    """Values 0 and 1 with multiplicities alpha and beta."""
    lo = max(0, t - alpha)
    hi = min(t, beta)
    return {s % p for s in range(lo, hi + 1)}


def three_value_sums(
    p: int, multiplicities: tuple[int, int, int], t: int, w: int
) -> set[int]:
    """Values normalized to 0, 1, w, with w not in {0,1}."""
    a, b, c = multiplicities
    out: set[int] = set()
    for i in range(min(a, t) + 1):
        for j in range(min(b, t - i) + 1):
            k = t - i - j
            if 0 <= k <= c:
                out.add((j + k * w) % p)
    return out


def check_parameter_edges() -> int:
    checked = 0
    expected = {
        4: range(3, 4),
        5: range(3, 5),
        6: range(3, 6),
        7: range(3, 7),
        8: range(3, 8),
    }
    for p in PRIMES_500:
        n = p - 1
        assert 3 * p - 4 > 8
        assert 3 * p - 4 > p
        for ell, b_values in expected.items():
            r = target_bound(ell)
            for b in b_values:
                assert 3 <= b <= ell - 1
                assert n >= b + r
                assert b < p
                if r == 1:
                    assert 3 <= b <= 7
                elif r == 2:
                    assert 3 <= b <= 6
                else:
                    assert r == 3 and 3 <= b <= 5
                checked += 1
    return checked


def check_two_value_patterns() -> int:
    checked = 0
    for p in PRIMES_500:
        n = p - 1
        cap = n - 3
        for alpha in range(1, n):
            beta = n - alpha
            if max(alpha, beta) > cap:
                continue
            assert alpha >= 3 and beta >= 3
            for t in range(3, 7):
                sums = two_value_sums(p, alpha, beta, t)
                formula = 1 + min(t, alpha, beta, n - t)
                assert len(sums) == formula
                assert len(sums) >= 4
                checked += 1
    return checked


def check_three_value_patterns() -> int:
    checked = 0
    for p in PRIMES_101:
        n = p - 1
        cap = n - 3
        for a in range(1, n - 1):
            for b in range(1, n - a):
                c = n - a - b
                if c < 1 or max(a, b, c) > cap:
                    continue
                for w in range(2, p):
                    for t in (3, 4, 5):
                        sums = three_value_sums(p, (a, b, c), t, w)
                        assert len(sums) >= 4, (p, (a, b, c), w, t, sums)
                        checked += 1
    return checked


def check_symbolic_collision_denominators() -> int:
    # Both exceptional collision systems reduce to 3 times a nonzero
    # difference.  Thus every prime in the theorem range must invert 3.
    for p in PRIMES_500:
        assert 3 % p != 0
        assert pow(3, -1, p) * 3 % p == 1
    return len(PRIMES_500)


def main() -> None:
    edge_count = check_parameter_edges()
    two_count = check_two_value_patterns()
    three_count = check_three_value_patterns()
    collision_count = check_symbolic_collision_denominators()
    print(
        "PASS: full-fiber exclusion checks; "
        f"parameter cases={edge_count}, "
        f"two-value cases={two_count}, "
        f"three-value cases={three_count}, "
        f"collision primes={collision_count}"
    )


if __name__ == "__main__":
    main()
