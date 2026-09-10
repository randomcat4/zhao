#!/usr/bin/env python3
"""Audit the standard-atom three-point obstruction and pair-height system.

The p=11,13 exhaustion is for the three-direction symmetric ansatz.  The
optional p=17,19,23 exhaustion also imposes support size at most four.  Any
fixed-seed asymmetric search is printed as a probe, never as a proof.
"""

from __future__ import annotations

import argparse
import itertools
import random
import time


def pair_counts_from_multiplicities(multiplicities, prime):
    counts = [0] * prime
    support = [value for value, count in enumerate(multiplicities) if count]
    for index, first in enumerate(support):
        count = multiplicities[first]
        counts[2 * first % prime] += count * (count - 1) // 2
        for second in support[index + 1 :]:
            counts[(first + second) % prime] += count * multiplicities[second]
    return counts


def symmetric_d_values(pair_counts, prime, pair_sum):
    """Return (d1,d2,d3) after the harmless normalization beta=0."""
    pair_height = 2 * pow(3, -1, prime) % prime
    d1 = (
        -int(pair_sum == 1)
        - 2 * int((pair_sum + pair_height) % prime == 1)
        + 2 * pair_counts[(1 - pair_sum) % prime]
    )
    d2 = (
        -2 * int((pair_sum + pair_height) % prime == 2)
        + 2 * pair_counts[(2 - pair_sum) % prime]
        - int((pair_sum + 2 * pair_height) % prime == 2)
    )
    d3 = (
        2 * pair_counts[(3 - pair_sum) % prime]
        - int((pair_sum + 2 * pair_height) % prime == 3)
        + 2 * pair_counts[(3 - pair_sum - pair_height) % prime]
    )
    return d1, d2, d3


def symmetric_codegrees(multiplicities, prime):
    """All occurring pair sums after the harmless normalization beta=0."""
    pair_counts = pair_counts_from_multiplicities(multiplicities, prime)
    output = []
    for pair_sum, actual_count in enumerate(pair_counts):
        if actual_count == 0:
            continue
        d1, d2, d3 = symmetric_d_values(pair_counts, prime, pair_sum)
        output.append((pair_sum, actual_count, d1, d2, d3))
    return output


def symmetric_solution(multiplicities, prime):
    for _, _, d1, d2, d3 in symmetric_codegrees(multiplicities, prime):
        if (8 * d1 + 10 * d2 - 3) % prime:
            return False
        if (2 * d1 - 10 * d3 - 1) % prime:
            return False
    return True


def pair_counts_solution(pair_counts, prime):
    """Check (1), using positive integer counts as the actual support."""
    for pair_sum, actual_count in enumerate(pair_counts):
        if actual_count == 0:
            continue
        d1, d2, d3 = symmetric_d_values(pair_counts, prime, pair_sum)
        if (8 * d1 + 10 * d2 - 3) % prime:
            return False
        if (2 * d1 - 10 * d3 - 1) % prime:
            return False
    return True


def exhaustive_symmetric_audit(prime):
    cap = prime - 4
    multiplicities = [0] * prime
    tested = 0
    witness = None

    def visit(index, remaining):
        nonlocal tested, witness
        if witness is not None:
            return
        if index == prime - 1:
            if remaining <= cap:
                multiplicities[index] = remaining
                tested += 1
                if symmetric_solution(multiplicities, prime):
                    witness = tuple(multiplicities)
            return
        for count in range(min(cap, remaining) + 1):
            multiplicities[index] = count
            visit(index + 1, remaining - count)
            if witness is not None:
                return

    visit(0, prime - 1)
    return tested, witness


def verify_three_point_obstruction():
    """Enumerate every relevant coordinate choice under the length-eight cap."""
    reachable = set()
    cases = 0
    for b_i in range(3, 9):
        for epsilon, gamma_plus, gamma_minus in itertools.product((0, 1), repeat=3):
            if b_i + epsilon + gamma_plus + gamma_minus > 8:
                continue
            coordinate = b_i + epsilon + 2 * gamma_plus - 2 * gamma_minus
            assert 1 <= coordinate <= 9
            reachable.add(coordinate)
            cases += 1
    assert reachable == set(range(1, 10))
    return cases, tuple(sorted(reachable))


def verify_direction_sum_identity(prime):
    """Check the exact cyclic-shift coefficient count behind (5)."""
    # Every map z -> c-z is a permutation, so every R_j(t) or R_k(t)
    # receives coefficient one in each shifted sum.  We still audit this
    # explicitly for every possible shift c.
    for shift in range(prime):
        multiplicity = [0] * prime
        for z in range(prime):
            multiplicity[(shift - z) % prime] += 1
        assert multiplicity == [1] * prime

    pair_mass = ((prime - 1) * (prime - 2) // 2) % prime
    assert pair_mass == 1
    sum_d1 = (-3 + 2 * pair_mass) % prime
    sum_d2 = (-3 + 2 * pair_mass) % prime
    assert sum_d1 == -1 % prime
    assert sum_d2 == -1 % prime
    contradiction = (8 * sum_d1 + 10 * sum_d2) % prime
    assert contradiction == -18 % prime
    assert contradiction != 0  # valid for every prime in this audit (>= 11)
    return sum_d1, sum_d2, contradiction


def polynomial_add(polynomial, monomial, coefficient, prime):
    """Add a coefficient to a commutative sparse polynomial over F_p."""
    monomial = tuple(sorted(monomial))
    value = (polynomial.get(monomial, 0) + coefficient) % prime
    if value:
        polynomial[monomial] = value
    else:
        polynomial.pop(monomial, None)


def direct_weighted_polynomials(prime):
    """Expand sum_z R(z)(8d1+10d2) and sum_z R(z)(2d1-10d3)."""
    pair_height = 2 * pow(3, -1, prime) % prime
    first = {}
    second = {}
    for z in range(prime):
        # Linear indicator terms.
        polynomial_add(first, (z,), -8 * int(z == 1), prime)
        polynomial_add(
            first, (z,), -16 * int((z + pair_height) % prime == 1), prime
        )
        polynomial_add(
            first, (z,), -20 * int((z + pair_height) % prime == 2), prime
        )
        polynomial_add(
            first, (z,), -10 * int((z + 2 * pair_height) % prime == 2), prime
        )
        polynomial_add(second, (z,), -2 * int(z == 1), prime)
        polynomial_add(
            second, (z,), -4 * int((z + pair_height) % prime == 1), prime
        )
        polynomial_add(
            second, (z,), 10 * int((z + 2 * pair_height) % prime == 3), prime
        )

        # Quadratic shifted-pair-count terms.
        polynomial_add(first, (z, (1 - z) % prime), 16, prime)
        polynomial_add(first, (z, (2 - z) % prime), 20, prime)
        polynomial_add(second, (z, (1 - z) % prime), 4, prime)
        polynomial_add(second, (z, (3 - z) % prime), -20, prime)
        polynomial_add(
            second, (z, (3 - z - pair_height) % prime), -20, prime
        )
    return first, second


def formula_weighted_polynomials(prime):
    """Expand the claimed convolution formulas (10) and (11)."""
    pair_height = 2 * pow(3, -1, prime) % prime
    first = {}
    second = {}

    # Linear terms in (10).
    polynomial_add(first, (1,), -8, prime)
    polynomial_add(first, ((1 - pair_height) % prime,), -16, prime)
    polynomial_add(first, ((2 - pair_height) % prime,), -20, prime)
    polynomial_add(first, ((2 - 2 * pair_height) % prime,), -10, prime)

    # Linear terms in (11).
    polynomial_add(second, (1,), -2, prime)
    polynomial_add(second, ((1 - pair_height) % prime,), -4, prime)
    polynomial_add(second, ((3 - 2 * pair_height) % prime,), 10, prime)

    # K(c)=sum_z R(z)R(c-z).
    for z in range(prime):
        polynomial_add(first, (z, (1 - z) % prime), 16, prime)
        polynomial_add(first, (z, (2 - z) % prime), 20, prime)
        polynomial_add(second, (z, (1 - z) % prime), 4, prime)
        polynomial_add(second, (z, (3 - z) % prime), -20, prime)
        polynomial_add(
            second, (z, (3 - pair_height - z) % prime), -20, prime
        )
    return first, second


def verify_convolution_polynomials(prime):
    """Compare (10)-(11) coefficient by coefficient, without evaluation."""
    direct = direct_weighted_polynomials(prime)
    formula = formula_weighted_polynomials(prime)
    assert direct == formula
    return len(direct[0]), len(direct[1])


def positive_compositions(total, parts, cap):
    """Yield positive ordered compositions, each part at most cap."""
    current = [0] * parts

    def visit(index, remaining):
        if index == parts - 1:
            if 1 <= remaining <= cap:
                current[index] = remaining
                yield tuple(current)
            return
        lower = max(1, remaining - cap * (parts - index - 1))
        upper = min(cap, remaining - (parts - index - 1))
        for value in range(lower, upper + 1):
            current[index] = value
            yield from visit(index + 1, remaining - value)

    yield from visit(0, total)


def pair_counts_from_sparse_support(support, multiplicities, prime):
    counts = [0] * prime
    for index, first in enumerate(support):
        count = multiplicities[index]
        counts[2 * first % prime] += count * (count - 1) // 2
        for second_index in range(index + 1, len(support)):
            counts[(first + support[second_index]) % prime] += (
                count * multiplicities[second_index]
            )
    return counts


def exhaustive_small_support_audit(prime, maximum_support=4):
    """Strictly exhaust symmetric vectors with actual support <= maximum_support."""
    cap = prime - 4
    tested_by_size = {}
    witness = None
    for support_size in range(1, maximum_support + 1):
        compositions = tuple(
            positive_compositions(prime - 1, support_size, cap)
        )
        tested = 0
        for support in itertools.combinations(range(prime), support_size):
            for multiplicities in compositions:
                tested += 1
                pair_counts = pair_counts_from_sparse_support(
                    support, multiplicities, prime
                )
                if pair_counts_solution(pair_counts, prime):
                    witness = (support, multiplicities)
                    return tested_by_size, witness
        tested_by_size[support_size] = tested
    return tested_by_size, witness


def pair_counts_from_heights(heights, prime):
    multiplicities = [0] * prime
    for height in heights:
        multiplicities[height] += 1
    if max(multiplicities) > prime - 4:
        return None
    return pair_counts_from_multiplicities(multiplicities, prime)


def asymmetric_solution(pair_counts, betas, pair_heights, prime):
    for direction in range(3):
        first, second = [index for index in range(3) if index != direction]
        for pair_sum, actual_count in enumerate(pair_counts[direction]):
            if actual_count == 0:
                continue
            base = (pair_sum + betas[direction]) % prime
            d1 = -int(base == 1)
            d2 = 0
            d3 = 0
            for index in (first, second):
                d1 -= int((base + pair_heights[index]) % prime == 1)
                d1 += pair_counts[index][(1 - base - betas[index]) % prime]
                d2 -= int((base + pair_heights[index]) % prime == 2)
                d2 += pair_counts[index][(2 - base - betas[index]) % prime]
                d3 += pair_counts[index][(3 - base - betas[index]) % prime]
            d2 -= int(
                (base + pair_heights[first] + pair_heights[second]) % prime == 2
            )
            d3 -= int(
                (base + pair_heights[first] + pair_heights[second]) % prime == 3
            )
            d3 += pair_counts[second][
                (3 - base - pair_heights[first] - betas[second]) % prime
            ]
            d3 += pair_counts[first][
                (3 - base - pair_heights[second] - betas[first]) % prime
            ]
            if (8 * d1 + 10 * d2 - 3) % prime:
                return False
            if (2 * d1 - 10 * d3 - 1) % prime:
                return False
    return True


def deterministic_asymmetric_probe(prime, attempts=250_000):
    rng = random.Random(130_000 + prime)
    cap_valid = 0
    for _ in range(attempts):
        pair_counts = []
        for _direction in range(3):
            heights = [rng.randrange(prime) for _ in range(prime - 1)]
            counts = pair_counts_from_heights(heights, prime)
            if counts is None:
                break
            pair_counts.append(counts)
        if len(pair_counts) != 3:
            continue
        cap_valid += 1
        betas = [rng.randrange(prime) for _ in range(3)]
        pair_heights = [rng.randrange(prime), rng.randrange(prime), 0]
        pair_heights[2] = (2 - pair_heights[0] - pair_heights[1]) % prime
        if asymmetric_solution(pair_counts, betas, pair_heights, prime):
            return cap_valid, (pair_counts, betas, pair_heights)
    return cap_valid, None


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--extended",
        action="store_true",
        help="also exhaust p=17,19,23 with symmetric support size at most four",
    )
    parser.add_argument(
        "--random-probe",
        action="store_true",
        help="run fixed-seed asymmetric probes (diagnostic only, never a proof)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    started = time.perf_counter()

    cases, reachable = verify_three_point_obstruction()
    assert max(reachable) < 11
    print(
        f"PASS all p>=11: {cases} relevant length-cap choices give "
        f"integer coordinate set {reachable}, never 0 mod p"
    )

    for prime in (11, 13, 17, 19, 23):
        sum_d1, sum_d2, contradiction = verify_direction_sum_identity(prime)
        first_terms, second_terms = verify_convolution_polynomials(prime)
        print(
            f"PASS p={prime}: per-direction sums d1={sum_d1}, d2={sum_d2}, "
            f"first sum={contradiction}; convolution polynomials "
            f"match ({first_terms}/{second_terms} monomials)"
        )

    expected_counts = {11: 184_030, 13: 2_702_973}
    for prime in (11, 13):
        tested, witness = exhaustive_symmetric_audit(prime)
        assert tested == expected_counts[prime]
        assert witness is None
        print(
            f"PASS p={prime}: rejected all {tested} symmetric multiplicity "
            "vectors after normalizing beta=0"
        )

    if args.extended:
        expected_small_support = {
            17: 1_153_756,
            19: 2_766_780,
            23: 12_148_048,
        }
        for prime in (17, 19, 23):
            tested_by_size, witness = exhaustive_small_support_audit(prime)
            tested = sum(tested_by_size.values())
            assert tested == expected_small_support[prime]
            assert witness is None
            if prime == 23:
                assert sum(
                    count
                    for size, count in tested_by_size.items()
                    if size <= 3
                ) == 370_898
                assert tested_by_size[4] == 11_777_150
            print(
                f"PASS p={prime}: rejected all {tested} symmetric vectors "
                f"with support <=4; breakdown={tested_by_size}"
            )

    if args.random_probe:
        for prime in (11, 13):
            cap_valid, witness = deterministic_asymmetric_probe(prime)
            assert witness is None
            print(
                f"PROBE ONLY (NOT A PROOF) p={prime}: 250000 asymmetric "
                f"attempts; {cap_valid} passed the cap; 0 hits"
            )

    elapsed = time.perf_counter() - started
    print(
        "SCOPE: the triple obstruction proves only the fixed +/-2e_i template; "
        "pair exhaustions have the stated symmetry/support restrictions"
    )
    print(f"elapsed: {elapsed:.3f} s")


if __name__ == "__main__":
    main()
