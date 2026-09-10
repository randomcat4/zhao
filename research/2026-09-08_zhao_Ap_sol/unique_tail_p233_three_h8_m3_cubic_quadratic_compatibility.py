from __future__ import annotations

import argparse
import json
from collections import Counter


P = 233
TAILS = ((1, 0), (0, 1), (P - 1, P - 1))
TAIL_BASES = (
    (TAILS[1], TAILS[2]),
    (TAILS[0], TAILS[2]),
    (TAILS[0], TAILS[1]),
)


def inv(value: int) -> int:
    return pow(value % P, -1, P)


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def sub(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return ((left[0] - right[0]) % P, (left[1] - right[1]) % P)


def scale(value: int, vector: tuple[int, int]) -> tuple[int, int]:
    return (value * vector[0] % P, value * vector[1] % P)


def cubic_parameters(alpha: int, beta: int) -> tuple[int, int, int]:
    g = inv(alpha - beta)
    f = (-2 - g * beta) * inv(3 * alpha) % P
    i = (-2 + g * alpha) * inv(3 * beta) % P
    return f, i, g


def core_coefficient(
    point: tuple[int, int], parameters: tuple[int, int, int]
) -> int:
    x, y = point
    f, i, g = parameters
    return (
        1
        - x * x
        + x * y
        - y * y
        + f * (x**3 - x)
        + i * (y**3 - y)
        + g * (x * x * y - x * y * y)
    ) % P


def deleted_tail_coefficient(
    point: tuple[int, int],
    fringe_point: tuple[int, int],
    parameters: tuple[int, int, int],
) -> int:
    return (
        core_coefficient(point, parameters)
        - core_coefficient(sub(point, fringe_point), parameters)
    ) % P


def from_basis(
    coordinates: tuple[int, int],
    basis: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    u, v = coordinates
    return add(scale(u, basis[0]), scale(v, basis[1]))


def canonical_quadratic(u: int, v: int, a: int, b: int) -> int:
    return (1 - (u - v) ** 2 + a * u * (u + 1) + b * v * (v + 1)) % P


def global_coordinates_in_tail_bases(x: int, y: int) -> tuple[tuple[int, int], ...]:
    # Bases are (f,-e-f), (e,-e-f), (e,f), respectively.
    return ((y - x, -x), (x - y, -y), (x, y))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full-census",
        action="store_true",
        help="also classify all 12,701,988 admissible (delta,s) pairs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    curve = [
        (alpha, beta)
        for alpha in range(P)
        for beta in range(P)
        if (alpha * alpha - alpha * beta + beta * beta - 3) % P == 0
    ]
    assert len(curve) == P + 1 == 234
    assert all(alpha and beta and alpha != beta for alpha, beta in curve)

    exceptional = {
        sub(TAILS[j], TAILS[i])
        for i in range(3)
        for j in range(3)
        if i != j
    }
    assert len(exceptional) == 6

    excluded_packing_directions = set(TAILS) | {
        ((-x) % P, (-y) % P) for x, y in TAILS
    }
    admissible_directions = [
        (x, y)
        for x in range(P)
        for y in range(P)
        if (x, y) != (0, 0) and (x, y) not in excluded_packing_directions
    ]
    off_tail_line_directions = [
        (x, y) for x, y in admissible_directions if x != 0 and y != 0 and x != y
    ]
    residual_tail_line_directions = [
        (x, y) for x, y in admissible_directions if x == 0 or y == 0 or x == y
    ]
    assert len(admissible_directions) == P * P - 1 - 6 == 54282
    assert len(off_tail_line_directions) == (P - 1) * (P - 2) == 53592
    assert len(residual_tail_line_directions) == 3 * (P - 3) == 690

    # Six triangular-grid points determine a total-degree-at-most-two polynomial.
    quadratic_probes = ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2))
    inv2 = inv(2)
    rank_histogram: Counter[int] = Counter()
    pair_minor_zero_counts = [0, 0, 0]
    parameter_table: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {}

    for delta in curve:
        parameters = cubic_parameters(*delta)
        fringe_points = [add(delta, tail) for tail in TAILS]
        canonical_parameters: list[tuple[int, int]] = []

        # Bind each finite difference of the common cubic to the canonical
        # deleted-tail quadratic, without importing any earlier verifier.
        for index, basis in enumerate(TAIL_BASES):
            fringe_point = fringe_points[index]

            def in_tail_basis(u: int, v: int) -> int:
                return deleted_tail_coefficient(
                    from_basis((u, v), basis), fringe_point, parameters
                )

            assert in_tail_basis(0, 0) == 1
            a = in_tail_basis(1, 0) * inv2 % P
            b = in_tail_basis(0, 1) * inv2 % P
            canonical_parameters.append((a, b))
            for u, v in quadratic_probes:
                assert in_tail_basis(u, v) == canonical_quadratic(u, v, a, b)

        parameter_table[delta] = tuple(canonical_parameters)

        # The odd part of each quadratic is a global linear form in s=(x,y).
        rows: list[tuple[int, int]] = []
        for fringe_point in fringe_points:
            e_plus = deleted_tail_coefficient((1, 0), fringe_point, parameters)
            e_minus = deleted_tail_coefficient((P - 1, 0), fringe_point, parameters)
            f_plus = deleted_tail_coefficient((0, 1), fringe_point, parameters)
            f_minus = deleted_tail_coefficient((0, P - 1), fringe_point, parameters)
            rows.append(
                (
                    (e_plus - e_minus) * inv2 % P,
                    (f_plus - f_minus) * inv2 % P,
                )
            )

        minors = (
            (rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]) % P,
            (rows[0][0] * rows[2][1] - rows[0][1] * rows[2][0]) % P,
            (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0]) % P,
        )
        for index, minor in enumerate(minors):
            pair_minor_zero_counts[index] += int(minor == 0)
        rank = 2 if any(minors) else (1 if any(rows) else 0)
        rank_histogram[rank] += 1

    assert rank_histogram == Counter({2: 234})
    assert pair_minor_zero_counts == [2, 2, 2]

    report: dict[str, object] = {
        "status": "PASS",
        "prime": P,
        "curve_points": len(curve),
        "generic_curve_points": len(curve) - len(exceptional),
        "exceptional_curve_points": len(exceptional),
        "admissible_directions_per_curve_point": len(admissible_directions),
        "off_tail_line_directions_per_curve_point": len(off_tail_line_directions),
        "residual_tail_line_directions_per_curve_point": len(
            residual_tail_line_directions
        ),
        "admissible_delta_direction_pairs": len(curve) * len(admissible_directions),
        "odd_part_rank_histogram": dict(sorted(rank_histogram.items())),
        "pair_minor_zero_counts": pair_minor_zero_counts,
        "simultaneous_six_signed_zero_survivors": 0,
        "conclusion": (
            "the simultaneous-six-signed-zero subbranch is empty; "
            "this alone does not eliminate the m=3 singleton-mask state"
        ),
        "scope": "exact p=233 m=3 signed-coefficient reduction; global A_p remains open",
    }

    if args.full_census:
        bad_difference_histogram: Counter[int] = Counter()
        off_tail_bad_difference_histogram: Counter[int] = Counter()
        tail_line_bad_difference_histogram: Counter[int] = Counter()
        fringe_difference_forced_pairs = 0

        for delta in curve:
            canonical_parameters = parameter_table[delta]
            for direction in admissible_directions:
                coordinates = global_coordinates_in_tail_bases(*direction)
                signed_values = tuple(
                    (
                        canonical_quadratic(u, v, a, b),
                        canonical_quadratic(-u, -v, a, b),
                    )
                    for (u, v), (a, b) in zip(coordinates, canonical_parameters)
                )
                bad_differences = 0
                for sign_index in (0, 1):
                    for left_endpoint in range(3):
                        for right_endpoint in range(left_endpoint + 1, 3):
                            difference = (
                                signed_values[left_endpoint][sign_index]
                                - signed_values[right_endpoint][sign_index]
                            ) % P
                            if difference not in {0, 1, P - 1}:
                                bad_differences += 1
                assert bad_differences >= 1
                fringe_difference_forced_pairs += 1
                bad_difference_histogram[bad_differences] += 1
                x, y = direction
                if x != 0 and y != 0 and x != y:
                    off_tail_bad_difference_histogram[bad_differences] += 1
                else:
                    tail_line_bad_difference_histogram[bad_differences] += 1

        total_pairs = len(curve) * len(admissible_directions)
        assert total_pairs == 12701988
        assert fringe_difference_forced_pairs == total_pairs
        assert bad_difference_histogram == Counter(
            {2: 132, 3: 4236, 4: 20688, 5: 929628, 6: 11747304}
        )
        report["full_census"] = {
            "bad_inter_endpoint_difference_count_histogram": dict(
                sorted(bad_difference_histogram.items())
            ),
            "off_tail_line_histogram": dict(
                sorted(off_tail_bad_difference_histogram.items())
            ),
            "residual_tail_line_histogram": dict(
                sorted(tail_line_bad_difference_histogram.items())
            ),
            "pairs_forcing_a_fringe_touching_two_to_one_exchange": (
                fringe_difference_forced_pairs
            ),
        }
        report["conclusion"] = (
            "every admissible (delta,s) pair forces a fringe-touching "
            "two-to-one exchange; the m=3 mask state itself remains open"
        )
        report["scope"] = (
            "exact p=233 m=3 fringe-exchange reduction; global A_p remains open"
        )

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
