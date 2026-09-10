#!/usr/bin/env python3
"""Exact finite interfaces for the labelled unique-tail continuation.

The default run checks the symbolic tables and the axial atom criterion on
small exhaustive instances.  With ``--instance FILE`` the program validates
one fully labelled local unique-tail instance, reconstructing every induced
short block and checking every F3 complement by an exact subset-sum DP.

A passing instance is only a local-interface candidate, never a counterexample
to the frozen theorem: TOP/CONST and the rest of R are outside this schema.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path


SURVIVORS = (
    (11, 7, 2),
    (13, 6, 3),
    (13, 8, 3),
    (19, 6, 1),
    (19, 8, 1),
    (23, 6, 3),
    (23, 8, 3),
    (43, 7, 3),
    (101, 6, 2),
    (101, 8, 2),
    (233, 7, 4),
    (701, 8, 4),
    (1399, 8, 5),
)

LENGTH_FAMILIES = {
    2: (1,),
    3: (1,),
    4: (1, 2),
    5: (1, 2),
    6: (1, 2, 3),
    7: (2, 3),
    8: (3,),
}


def add(left, right, prime):
    return tuple((a + b) % prime for a, b in zip(left, right))


def neg(value, prime):
    return tuple((-entry) % prime for entry in value)


def scalar(coefficient, value, prime):
    return tuple((coefficient * entry) % prime for entry in value)


def vector_sum(values, prime, dimension):
    total = (0,) * dimension
    for value in values:
        total = add(total, value, prime)
    return total


def mod_fraction(value, prime):
    value = Fraction(value)
    return value.numerator * pow(value.denominator, -1, prime) % prime


def reachable_size_masks(values, prime):
    """Map each subset sum to a bit mask of its achievable cardinalities."""
    dimension = len(values[0]) if values else 3
    zero = (0,) * dimension
    reachable = {zero: 1}
    for value in values:
        updated = dict(reachable)
        for total, size_mask in reachable.items():
            target = add(total, value, prime)
            updated[target] = updated.get(target, 0) | (size_mask << 1)
        reachable = updated
    return reachable


def axial_atom_violations(prime, remainder, core_count):
    """Violations for q^(p-(core_count+4)) * remainder, q=(1,0,0)."""
    expected = ((core_count + 4) % prime, 0, 0)
    if vector_sum(remainder, prime, 3) != expected:
        return ["remainder total is not (core_count+4)q"]
    if not 0 <= core_count <= prime - 4:
        return ["core_count outside 0..p-4"]

    reachable = reachable_size_masks(remainder, prime)
    proper_nonempty_sizes = ((1 << len(remainder)) - 1) & ~1
    forbidden_coefficients = (0, *range(core_count + 4, prime))
    violations = []
    for coefficient in forbidden_coefficients:
        target = (coefficient, 0, 0)
        sizes = reachable.get(target, 0) & proper_nonempty_sizes
        if sizes:
            witnesses = [
                size for size in range(1, len(remainder)) if sizes >> size & 1
            ]
            violations.append((coefficient, tuple(witnesses)))
    return violations


def brute_is_atom(prime, remainder, core_count):
    q = (1, 0, 0)
    copies = prime - (core_count + 4)
    sequence = [q] * copies + list(remainder)
    if vector_sum(sequence, prime, 3) != (0, 0, 0):
        return False
    for mask in range(1, (1 << len(sequence)) - 1):
        subset = [sequence[i] for i in range(len(sequence)) if mask >> i & 1]
        if vector_sum(subset, prime, 3) == (0, 0, 0):
            return False
    return True


def allowed_axis_trace_steps(core_count, trace_size):
    """t with trace sum -(core_count+t)q not yet ruled out."""
    return tuple(range(1, min(3, 7 - core_count - trace_size) + 1))


def trace_table():
    table = {}
    for prime, length, core_count in SURVIVORS:
        remainder_size = length - core_count
        rows = {}
        for trace_size in range(1, remainder_size):
            rows[trace_size] = allowed_axis_trace_steps(core_count, trace_size)
        table[(prime, length, core_count)] = rows
    return table


def audit_trace_table():
    for (prime, length, core_count), rows in trace_table().items():
        assert core_count + 3 <= prime - 4
        remainder_size = length - core_count
        for trace_size, steps in rows.items():
            assert 1 <= trace_size < remainder_size
            for step in steps:
                induced_length = trace_size + core_count + step
                assert induced_length <= 7
                assert any(
                    family in (1, 2)
                    for family in LENGTH_FAMILIES[induced_length]
                )
            for step in set((1, 2, 3)) - set(steps):
                induced_length = trace_size + core_count + step
                assert induced_length >= 8


def audit_factor_patterns():
    expected = {
        2: {(1, 3), (2, 2)},
        3: {(1, 1, 2)},
        4: {(1, 1, 1, 1)},
    }
    for prime in (11, 13, 19):
        observed = defaultdict(set)
        for factor_count in range(2, 7):
            for coefficients in itertools.product((1, 2, 3), repeat=factor_count):
                if sum(coefficients) % prime != 4:
                    continue
                valid = True
                for mask in range(1, (1 << factor_count) - 1):
                    subtotal = sum(
                        coefficients[index]
                        for index in range(factor_count)
                        if mask >> index & 1
                    ) % prime
                    if subtotal not in (1, 2, 3):
                        valid = False
                        break
                if valid:
                    observed[factor_count].add(tuple(sorted(coefficients)))
        assert dict(observed) == expected


def audit_atom_equivalence():
    checked = 0
    prime = 11
    for core_count in range(6):
        for seed in range(12):
            first = []
            for index in range(5):
                first.append(
                    (
                        (seed + 2 * index + 1) % prime,
                        (seed * (index + 1) + index + 1) % prime,
                        (seed + index * index + 3) % prime,
                    )
                )
            target = ((core_count + 4) % prime, 0, 0)
            last = add(target, neg(vector_sum(first, prime, 3), prime), prime)
            remainder = first + [last]
            criterion = not axial_atom_violations(prime, remainder, core_count)
            brute = brute_is_atom(prime, remainder, core_count)
            assert criterion == brute, (core_count, seed, remainder)
            checked += 1
    return checked


def enumerate_short_stars(prime, y_values, x_height):
    """Rebuild every short quotient-zero tail and its unique core count."""
    m = prime - 4
    stars = []
    indices = range(len(y_values))
    for tail_size in range(1, 9):
        for tail in itertools.combinations(indices, tail_size):
            quotient = vector_sum([y_values[i][:3] for i in tail], prime, 3)
            height = sum(y_values[i][3] for i in tail) % prime
            for core_count in range(0, min(m, 8 - tail_size) + 1):
                if add(quotient, (core_count % prime, 0, 0), prime) != (0, 0, 0):
                    continue
                length = tail_size + core_count
                family = (height + core_count * x_height) % prime
                if length not in LENGTH_FAMILIES or family not in LENGTH_FAMILIES[length]:
                    raise ValueError(
                        "short quotient-zero subset violates SQ/length window: "
                        f"tail={tail}, core={core_count}, length={length}, "
                        f"height={family}"
                    )
                stars.append((family, length, core_count, tail))
    return stars


def has_actual_zero_subsequence(prime, y_values, x_height):
    m = prime - 4
    actual_values = [tuple(value) for value in y_values]
    reachable = reachable_size_masks(actual_values, prime)
    y_count = len(actual_values)
    x = (1, 0, 0, x_height % prime)
    for core_count in range(m + 1):
        target = neg(scalar(core_count, x, prime), prime)
        sizes = reachable.get(target, 0)
        for tail_size in range(y_count + 1):
            if not (sizes >> tail_size & 1):
                continue
            if core_count == 0 and tail_size == 0:
                continue
            if core_count == m and tail_size == y_count:
                continue
            return True
    return False


def quotient_middle_gap_violations(prime, y_values):
    """Return forbidden quotient-zero cardinalities from 9 through 2p+2.

    Sizes 9..p+1 are excluded by (SQ) together with the proved short-block
    length windows.  Only sizes p+2..2p+2 use the middle quotient gap.
    """
    m = prime - 4
    reachable = reachable_size_masks([value[:3] for value in y_values], prime)
    violations = []
    for core_count in range(m + 1):
        target = ((-core_count) % prime, 0, 0)
        sizes = reachable.get(target, 0)
        for tail_size in range(len(y_values) + 1):
            total_size = core_count + tail_size
            if 9 <= total_size <= 2 * prime + 2 and sizes >> tail_size & 1:
                violations.append(total_size)
    return sorted(set(violations))


def star_moments(prime, stars, y_count):
    m = prime - 4
    zero_order = [0, 0, 0, 0]
    moments = {1: defaultdict(lambda: [0, 0, 0, 0]),
               2: defaultdict(lambda: [0, 0, 0, 0]),
               3: defaultdict(lambda: [0, 0, 0, 0])}
    for family, length, core_count, tail in stars:
        tail_set = set(tail)
        zero_order[family] += (-1) ** (length - 1) * comb(m, core_count)
        for fixed_size in (1, 2, 3):
            for tail_fixed_size in range(fixed_size + 1):
                x_fixed = fixed_size - tail_fixed_size
                if x_fixed > core_count or tail_fixed_size > len(tail):
                    continue
                coefficient = (
                    (-1) ** (length - fixed_size)
                    * comb(m - x_fixed, core_count - x_fixed)
                )
                for fixed_tail in itertools.combinations(tail_set, tail_fixed_size):
                    key = (x_fixed, tuple(sorted(fixed_tail)))
                    moments[fixed_size][key][family] += coefficient
    return zero_order, moments


def validate_hasse(prime, stars, y_count):
    zero_order, moments = star_moments(prime, stars, y_count)
    for family in (1, 2, 3):
        if zero_order[family] % prime:
            raise ValueError(f"zero-order Hasse failure in family {family}")

    point_targets = {
        1: mod_fraction(Fraction(-3, 4), prime),
        2: mod_fraction(Fraction(3, 10), prime),
        3: mod_fraction(Fraction(-1, 20), prime),
    }
    point_keys = [(1, ())] + [(0, (index,)) for index in range(y_count)]
    for key in point_keys:
        values = moments[1][key]
        for family in (1, 2, 3):
            if values[family] % prime != point_targets[family]:
                raise ValueError(f"point Hasse failure at {key}, family {family}")

    pair_keys = [(2, ())]
    pair_keys += [(1, (index,)) for index in range(y_count)]
    pair_keys += [(0, pair) for pair in itertools.combinations(range(y_count), 2)]
    for key in pair_keys:
        values = moments[2][key]
        if (8 * values[1] + 10 * values[2] - 3) % prime:
            raise ValueError(f"first pair Hasse failure at {key}")
        if (2 * values[1] - 10 * values[3] - 1) % prime:
            raise ValueError(f"second pair Hasse failure at {key}")

    triple_keys = [(3, ())]
    triple_keys += [(2, (index,)) for index in range(y_count)]
    triple_keys += [(1, pair) for pair in itertools.combinations(range(y_count), 2)]
    triple_keys += [
        (0, triple) for triple in itertools.combinations(range(y_count), 3)
    ]
    for key in triple_keys:
        values = moments[3][key]
        if (4 * values[1] + 10 * values[2] + 20 * values[3] + 1) % prime:
            raise ValueError(f"triple Hasse failure at {key}")


def validate_intersections(prime, stars, y_values):
    m = prime - 4
    f3 = [star for star in stars if star[0] == 3]
    all_stars = list(stars)
    for left_index, left in enumerate(all_stars):
        _, left_length, left_core, left_tail = left
        left_tail = set(left_tail)
        for right in all_stars[left_index:]:
            right_family, right_length, right_core, right_tail = right
            right_tail = set(right_tail)
            disjoint_possible = (
                not left_tail.intersection(right_tail)
                and left_core + right_core <= m
            )
            if left[0] == 3 and disjoint_possible:
                raise ValueError("an induced short block can be disjoint from F3")
            if right_family == 3 and disjoint_possible:
                raise ValueError("an induced short block can be disjoint from F3")
            if left[0] == right_family == 2 and disjoint_possible:
                raise ValueError("two induced F2 blocks can be disjoint")
            if disjoint_possible and left_length + right_length > prime + 1:
                raise ValueError("middle quotient gap violated")

    for index, left in enumerate(f3):
        _, _, left_core, left_tail_tuple = left
        left_tail = set(left_tail_tuple)
        for right_index in range(index, len(f3)):
            right = f3[right_index]
            _, _, right_core, right_tail_tuple = right
            right_tail = set(right_tail_tuple)
            same_star = index == right_index
            lower = max(0, left_core + right_core - m)
            upper = min(left_core, right_core)
            if same_star:
                upper -= 1
            if lower > upper:
                continue
            intersection_sum = vector_sum(
                [y_values[i][:3] for i in left_tail.intersection(right_tail)],
                prime,
                3,
            )
            for core_intersection in range(lower, upper + 1):
                total = add(
                    intersection_sum,
                    (core_intersection % prime, 0, 0),
                    prime,
                )
                if total == (0, 0, 0):
                    raise ValueError("two different F3 blocks have zero quotient intersection")


def validate_instance(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    prime = int(data["p"])
    length = int(data["unique_type"][0])
    core_count = int(data["unique_type"][1])
    if (prime, length, core_count) not in SURVIVORS:
        raise ValueError("unique_type is not one of the 13 surviving types")
    x_height = int(data["x_height"]) % prime
    y_values = [tuple(int(entry) % prime for entry in item) for item in data["Y"]]
    if any(len(item) != 4 for item in y_values):
        raise ValueError("each Y label must have three quotient coordinates and one height")
    if len(y_values) != 2 * prime + 8:
        raise ValueError("Y must have 2p+8 positions")
    t_set = frozenset(int(index) for index in data["T"])
    u_set = frozenset(int(index) for index in data["U"])
    if len(t_set) not in (6, 7, 8):
        raise ValueError("T length must be 6, 7, or 8")
    if len(u_set) != length - core_count:
        raise ValueError("U has the wrong size")
    if not t_set <= set(range(len(y_values))) or not u_set <= set(range(len(y_values))):
        raise ValueError("T/U index outside Y")

    quotient_total = vector_sum([value[:3] for value in y_values], prime, 3)
    if quotient_total != (4 % prime, 0, 0):
        raise ValueError("Y quotient total is not 4q")
    if sum(value[3] for value in y_values) % prime != 4 * x_height % prime:
        raise ValueError("Y height total does not cancel X")

    t_values = [y_values[index] for index in t_set]
    if vector_sum([value[:3] for value in t_values], prime, 3) != (0, 0, 0):
        raise ValueError("T quotient sum is nonzero")
    if sum(value[3] for value in t_values) % prime != 3:
        raise ValueError("T actual height sum is not 3")

    u_values = [y_values[index] for index in u_set]
    if vector_sum([value[:3] for value in u_values], prime, 3) != (
        (-core_count) % prime,
        0,
        0,
    ):
        raise ValueError("U quotient sum is not -bq")
    if sum(value[3] for value in u_values) % prime != (
        3 - core_count * x_height
    ) % prime:
        raise ValueError("U actual height is wrong")

    x = (1, 0, 0, x_height)
    multiplicities = Counter(y_values)
    multiplicities[x] += prime - 4
    if max(multiplicities.values()) > prime - 4:
        raise ValueError("actual value multiplicity exceeds p-4")
    for index, value in enumerate(y_values):
        if index not in t_set and value[:3] == (1, 0, 0):
            raise ValueError("B contains a quotient-q position outside the fixed X fibre")
    if has_actual_zero_subsequence(prime, y_values, x_height):
        raise ValueError("Z is not an actual zero-sum atom")

    stars = enumerate_short_stars(prime, y_values, x_height)
    gap_violations = quotient_middle_gap_violations(prime, y_values)
    if gap_violations:
        raise ValueError(
            "a quotient-zero subset lies in the forbidden 9..2p+2 range "
            "(short windows followed by the middle gap): "
            f"{gap_violations[:8]}"
        )
    f3 = [star for star in stars if star[0] == 3]
    if (3, len(t_set), 0, tuple(sorted(t_set))) not in f3:
        raise ValueError("T was not reconstructed as a zero-core F3 block")
    positive = [star for star in f3 if star[2] > 0]
    for _, star_length, star_core, star_tail in positive:
        if (star_length, star_core, frozenset(star_tail)) != (
            length,
            core_count,
            u_set,
        ):
            raise ValueError("a second positive-core F3 tail was induced")
    if not positive:
        raise ValueError("the declared positive-core F3 tail was not induced")

    for _, _, star_core, star_tail in f3:
        if not u_set.intersection(star_tail):
            raise ValueError("an F3 block misses the unique tail U")
        remainder = [
            y_values[index][:3]
            for index in range(len(y_values))
            if index not in set(star_tail)
        ]
        violations = axial_atom_violations(prime, remainder, star_core)
        if violations:
            raise ValueError(
                "an F3 complement is not a quotient atom: "
                f"core={star_core}, tail={star_tail}, violations={violations[:3]}"
            )

    validate_hasse(prime, stars, len(y_values))
    validate_intersections(prime, stars, y_values)
    print(
        "PASS exact labelled local instance: "
        f"p={prime}, stars={len(stars)}, F3 stars={len(f3)}"
    )
    print(
        "SCOPE: all induced short blocks, all point/pair/triple Hasse rows, "
        "actual Z atom, unique positive F3 tail, F3 intersections, and every "
        "F3 quotient-complement atom; TOP/CONST outside Z are not asserted"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path)
    args = parser.parse_args()
    if args.instance:
        validate_instance(args.instance)
        return

    audit_trace_table()
    audit_factor_patterns()
    checked = audit_atom_equivalence()
    print(f"PASS axial atom equivalence on {checked} exhaustive small cases")
    print("PASS projected factor patterns: 2:(1,3)/(2,2), 3:(1,1,2), 4:(1,1,1,1)")
    for key, rows in trace_table().items():
        compact = ", ".join(
            f"j={trace_size}:t={steps or '-'}"
            for trace_size, steps in rows.items()
        )
        print(f"TRACE {key}: {compact}")
    print(
        "SCOPE: default mode audits symbolic consequences only; use "
        "--instance for the exact labelled local validator"
    )


if __name__ == "__main__":
    main()
