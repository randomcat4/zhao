#!/usr/bin/env python3
"""Two exact prototypes for the affine-subspace O3 full-scan design.

This is deliberately not a full O3 scan.  It proves by exact F_233
calculation that:

* the x-slice / degree-12 minor-GCD method recovers the 9/11/13 compatible
  oriented z blocks at tau=(17,31), with no all-zero vertical slice; and
* the dual tail-deletion catalogue H_{tau,g} at tau=(0,1) has type histogram
  empty/point/line/plane = 54058/224/4/2.  Each of the two frozen common
  quartics is incident with exactly g=(1,2),(-1,1).

All arithmetic and interpolation are exact.  The accompanying design note
explains how these components fit into an output-sensitive global algorithm.
"""

from __future__ import annotations

import argparse
import itertools
import json
from math import comb
from pathlib import Path


P = 233
INV2 = pow(2, -1, P)
W = ((1, 0), (0, 1), (P - 1, P - 1))

EVEN_MONOMIALS = (
    (0, 0),
    (2, 0),
    (1, 1),
    (0, 2),
    (4, 0),
    (3, 1),
    (2, 2),
    (1, 3),
    (0, 4),
)

TAU_SLICE = (17, 31)
TAU_DUAL = (0, 1)
FROZEN_Q = (
    (0, 39, 115, 79, 194, 195, 232, 156, 155),
    (0, 0, 193, 79, 0, 117, 232, 156, 155),
)

EXPECTED_Z = (
    (
        (15, 30),
        (16, 32),
        (17, 30),
        (18, 32),
        (116, 0),
        (214, 201),
        (215, 203),
        (216, 201),
        (217, 203),
    ),
    (
        (0, 116),
        (16, 29),
        (16, 31),
        (18, 30),
        (18, 32),
        (116, 116),
        (117, 116),
        (215, 200),
        (215, 202),
        (217, 201),
        (217, 203),
    ),
    (
        (16, 31),
        (17, 30),
        (18, 33),
        (19, 32),
        (76, 59),
        (112, 104),
        (117, 117),
        (122, 130),
        (158, 175),
        (215, 202),
        (216, 201),
        (217, 204),
        (218, 203),
    ),
)

Point = tuple[int, int]
Vector = tuple[int, ...]
Polynomial = dict[tuple[int, int], int]


def add(left: Point, right: Point) -> Point:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def neg(point: Point) -> Point:
    return (-point[0] % P, -point[1] % P)


def sub(left: Point, right: Point) -> Point:
    return add(left, neg(right))


def scalar(value: int, point: Point) -> Point:
    return (value * point[0] % P, value * point[1] % P)


def dot(left: list[int] | Vector, right: list[int] | Vector) -> int:
    return sum(x * y for x, y in zip(left, right)) % P


def evaluation_row(point: Point) -> list[int]:
    x, y = point
    return [pow(x, a, P) * pow(y, b, P) % P for a, b in EVEN_MONOMIALS]


def rref(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    if not matrix:
        return [], []
    result = [[value % P for value in row] for row in matrix]
    row_count = len(result)
    column_count = len(result[0])
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if result[row][column]),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = result[selected], result[pivot_row]
        inverse = pow(result[pivot_row][column], P - 2, P)
        result[pivot_row] = [value * inverse % P for value in result[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or result[row][column] == 0:
                continue
            factor = result[row][column]
            result[row] = [
                (left - factor * right) % P
                for left, right in zip(result[row], result[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return result, pivots


def rank(matrix: list[list[int]]) -> int:
    return len(rref(matrix)[1])


def nullspace_basis(matrix: list[list[int]]) -> list[list[int]]:
    reduced, pivots = rref(matrix)
    column_count = len(matrix[0])
    free = [column for column in range(column_count) if column not in pivots]
    output: list[list[int]] = []
    for free_column in free:
        vector = [0] * column_count
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % P
        output.append(vector)
    return output


def inverse_matrix(matrix: list[list[int]]) -> list[list[int]]:
    size = len(matrix)
    augmented = [
        [value % P for value in matrix[row]]
        + [int(row == column) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        selected = next(
            row for row in range(column, size) if augmented[row][column]
        )
        augmented[column], augmented[selected] = augmented[selected], augmented[column]
        inverse = pow(augmented[column][column], P - 2, P)
        augmented[column] = [value * inverse % P for value in augmented[column]]
        for row in range(size):
            if row == column or augmented[row][column] == 0:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                (left - factor * right) % P
                for left, right in zip(augmented[row], augmented[column])
            ]
    return [row[size:] for row in augmented]


def tail_rows(tau: Point) -> list[list[int]]:
    return [
        evaluation_row(add(tau, scalar(sign, w)))
        for w in W
        for sign in (1, -1)
    ]


def normalized_tail_plane(tau: Point) -> tuple[Vector, tuple[Vector, Vector]]:
    kernel = nullspace_basis(tail_rows(tau))
    assert len(kernel) == 3
    anchor = [dot(evaluation_row(tau), vector) for vector in kernel]
    pivot = next(index for index, value in enumerate(anchor) if value)
    inverse = pow(anchor[pivot], P - 2, P)
    q0 = tuple(value * inverse % P for value in kernel[pivot])
    directions: list[Vector] = []
    for index, vector in enumerate(kernel):
        if index == pivot:
            continue
        factor = anchor[index] * inverse % P
        directions.append(
            tuple(
                (vector[coordinate] - factor * kernel[pivot][coordinate]) % P
                for coordinate in range(len(EVEN_MONOMIALS))
            )
        )
    assert dot(evaluation_row(tau), q0) == 1
    assert all(dot(evaluation_row(tau), direction) == 0 for direction in directions)
    return q0, (directions[0], directions[1])


def determinant_three(rows: list[list[int]]) -> int:
    a, b, c = rows
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) % P


def block_augmented_matrix(
    z: Point, endpoint: int, q0: Vector, directions: tuple[Vector, Vector]
) -> list[list[int]]:
    other_1 = (endpoint + 1) % 3
    other_2 = (endpoint + 2) % 3
    points = (z, add(z, W[endpoint]), sub(z, W[other_1]), sub(z, W[other_2]))
    return [
        [
            dot(evaluation_row(point), directions[0]),
            dot(evaluation_row(point), directions[1]),
            -dot(evaluation_row(point), q0) % P,
        ]
        for point in points
    ]


def trim(poly: list[int]) -> list[int]:
    result = [value % P for value in poly]
    while result and result[-1] == 0:
        result.pop()
    return result


def polynomial_remainder(dividend: list[int], divisor: list[int]) -> list[int]:
    result = trim(dividend)
    divisor = trim(divisor)
    if not divisor:
        raise ZeroDivisionError
    inverse = pow(divisor[-1], P - 2, P)
    while len(result) >= len(divisor):
        factor = result[-1] * inverse % P
        offset = len(result) - len(divisor)
        for index, value in enumerate(divisor):
            result[offset + index] = (result[offset + index] - factor * value) % P
        result = trim(result)
    return result


def polynomial_gcd(left: list[int], right: list[int]) -> list[int]:
    left = trim(left)
    right = trim(right)
    while right:
        left, right = right, polynomial_remainder(left, right)
    if not left:
        return []
    inverse = pow(left[-1], P - 2, P)
    return [value * inverse % P for value in left]


def polynomial_value(poly: list[int], value: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * value + coefficient) % P
    return result


INTERPOLATION_NODES = tuple(range(13))
VANDERMONDE_INVERSE = inverse_matrix(
    [[pow(value, degree, P) for degree in range(13)] for value in INTERPOLATION_NODES]
)


def interpolate_degree_twelve(values: list[int]) -> list[int]:
    assert len(values) == 13
    return trim(
        [
            sum(VANDERMONDE_INVERSE[row][column] * values[column] for column in range(13))
            % P
            for row in range(13)
        ]
    )


def slice_catalogue(tau: Point, endpoint: int) -> dict[str, object]:
    q0, directions = normalized_tail_plane(tau)
    row_triples = tuple(itertools.combinations(range(4), 3))
    compatible: list[Point] = []
    all_zero_slices: list[int] = []

    for x in range(P):
        sampled = [[] for _ in row_triples]
        for y in INTERPOLATION_NODES:
            matrix = block_augmented_matrix((x, y), endpoint, q0, directions)
            for index, triple in enumerate(row_triples):
                sampled[index].append(
                    determinant_three([matrix[row] for row in triple])
                )
        minors = [interpolate_degree_twelve(values) for values in sampled]
        common = []
        for minor in minors:
            common = polynomial_gcd(common, minor) if common else minor
        common = trim(common)
        if not common:
            roots = range(P)
            all_zero_slices.append(x)
        else:
            # The production design replaces this fixed-p loop by exact
            # finite-field factorization of the degree-at-most-12 gcd.
            roots = [y for y in range(P) if polynomial_value(common, y) == 0]

        for y in roots:
            augmented = block_augmented_matrix((x, y), endpoint, q0, directions)
            coefficients = [row[:2] for row in augmented]
            if rank(coefficients) == rank(augmented):
                compatible.append((x, y))

    assert tuple(compatible) == EXPECTED_Z[endpoint]
    assert not all_zero_slices
    return {
        "endpoint": endpoint + 1,
        "compatible_oriented_z": len(compatible),
        "z": [list(point) for point in compatible],
        "all_zero_vertical_slices": all_zero_slices,
        "interpolation_values_per_slice": 13,
        "minor_degree_bound": 12,
    }


CENTRAL_ANTIDERIVATIVE = {
    0: {1: 1},
    1: {2: pow(2, -1, P)},
    2: {3: pow(3, -1, P), 1: -pow(12, -1, P) % P},
    3: {4: pow(4, -1, P), 2: -pow(8, -1, P) % P},
    4: {
        5: pow(5, -1, P),
        3: -pow(6, -1, P) % P,
        1: 7 * pow(240, -1, P) % P,
    },
}


def polynomial_add_term(poly: Polynomial, exponent: tuple[int, int], value: int) -> None:
    poly[exponent] = (poly.get(exponent, 0) + value) % P
    if poly[exponent] == 0:
        del poly[exponent]


def pullback_q(q: Vector, g: Point) -> Polynomial:
    a, b = g
    result: Polynomial = {}
    if a:
        for (x_degree, y_degree), coefficient in zip(EVEN_MONOMIALS, q):
            for y_power in range(y_degree + 1):
                polynomial_add_term(
                    result,
                    (x_degree + y_degree - y_power, y_power),
                    coefficient
                    * comb(y_degree, y_power)
                    * pow(a, x_degree, P)
                    * pow(b, y_degree - y_power, P),
                )
    else:
        assert b
        for (x_degree, y_degree), coefficient in zip(EVEN_MONOMIALS, q):
            polynomial_add_term(
                result,
                (y_degree, x_degree),
                coefficient * pow(b, y_degree, P),
            )
    return result


def odd_antiderivative(q: Vector, g: Point) -> Polynomial:
    result: Polynomial = {}
    for (x_degree, y_degree), coefficient in pullback_q(q, g).items():
        for antiderivative_degree, multiplier in CENTRAL_ANTIDERIVATIVE[x_degree].items():
            polynomial_add_term(
                result,
                (antiderivative_degree, y_degree),
                coefficient * multiplier,
            )
    return result


def coordinates(g: Point, shifted_without_half: Point) -> Point:
    a, b = g
    if a:
        inverse_a = pow(a, P - 2, P)
        return (
            (shifted_without_half[0] * inverse_a + INV2) % P,
            (shifted_without_half[1] - b * inverse_a * shifted_without_half[0]) % P,
        )
    assert b
    return (
        (shifted_without_half[1] * pow(b, P - 2, P) + INV2) % P,
        shifted_without_half[0],
    )


def evaluate_polynomial(poly: Polynomial, point: Point) -> int:
    x, y = point
    return sum(
        coefficient * pow(x, x_degree, P) * pow(y, y_degree, P)
        for (x_degree, y_degree), coefficient in poly.items()
    ) % P


def affine_plane_coordinates(
    q: Vector, q0: Vector, directions: tuple[Vector, Vector]
) -> Point:
    for first in range(len(q)):
        for second in range(first + 1, len(q)):
            determinant = (
                directions[0][first] * directions[1][second]
                - directions[1][first] * directions[0][second]
            ) % P
            if determinant == 0:
                continue
            inverse = pow(determinant, P - 2, P)
            rhs_first = (q[first] - q0[first]) % P
            rhs_second = (q[second] - q0[second]) % P
            u = (
                rhs_first * directions[1][second]
                - directions[1][first] * rhs_second
            ) * inverse % P
            v = (
                directions[0][first] * rhs_second
                - rhs_first * directions[0][second]
            ) * inverse % P
            assert all(
                (q0[index] + u * directions[0][index] + v * directions[1][index])
                % P
                == q[index]
                for index in range(len(q))
            )
            return u, v
    raise AssertionError("tail-plane directions are dependent")


def canonical_affine_key(rows: list[list[int]]) -> tuple[object, ...]:
    matrix = [[value % P for value in row] for row in rows]
    pivot_row = 0
    for column in range(2):
        selected = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], P - 2, P)
        matrix[pivot_row] = [value * inverse % P for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % P
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1

    if any(row[0] == row[1] == 0 and row[2] for row in matrix):
        return ("empty",)
    nonzero = [tuple(matrix[row]) for row in range(pivot_row)]
    if not nonzero:
        return ("plane",)
    if len(nonzero) == 1:
        return ("line",) + nonzero[0]
    return ("point", nonzero[0][2], nonzero[1][2])


def key_contains(key: tuple[object, ...], point: Point) -> bool:
    kind = key[0]
    if kind == "empty":
        return False
    if kind == "plane":
        return True
    if kind == "point":
        return point == (key[1], key[2])
    assert kind == "line"
    return (key[1] * point[0] + key[2] * point[1] - key[3]) % P == 0


def common_tail_targets() -> tuple[Point, ...]:
    targets: list[Point] = []
    for w in W:
        for point in (w, neg(w)):
            if point not in targets:
                targets.append(point)
    assert len(targets) == 6
    return tuple(targets)


def dual_deletion_catalogue(tau: Point) -> dict[str, object]:
    q0, directions = normalized_tail_plane(tau)
    query_coordinates = [affine_plane_coordinates(q, q0, directions) for q in FROZEN_Q]
    query_labels: list[list[Point]] = [[] for _ in FROZEN_Q]
    histogram = {"empty": 0, "point": 0, "line": 0, "plane": 0}
    targets = ((0, 0),) + common_tail_targets()
    desired = (1, 0, 0, 0, 0, 0, 0)

    for gx in range(P):
        for gy in range(P):
            if gx == 0 and gy == 0:
                continue
            g = (gx, gy)
            particular = (
                odd_antiderivative(q0, g),
                odd_antiderivative(directions[0], g),
                odd_antiderivative(directions[1], g),
            )
            kernel_matrix: list[list[int]] = []
            q_matrix: list[list[int]] = []
            rhs: list[int] = []
            for target, value in zip(targets, desired):
                point = coordinates(g, add(target, tau))
                y = point[1]
                kernel_matrix.append([y, pow(y, 3, P), pow(y, 5, P)])
                q_matrix.append(
                    [
                        evaluate_polynomial(particular[1], point),
                        evaluate_polynomial(particular[2], point),
                    ]
                )
                rhs.append((value - evaluate_polynomial(particular[0], point)) % P)

            left_kernel = nullspace_basis(
                [list(column) for column in zip(*kernel_matrix)]
            )
            projected_rows = [
                [
                    dot(vector, [row[0] for row in q_matrix]),
                    dot(vector, [row[1] for row in q_matrix]),
                    dot(vector, rhs),
                ]
                for vector in left_kernel
            ]
            key = canonical_affine_key(projected_rows)
            histogram[str(key[0])] += 1
            for index, point in enumerate(query_coordinates):
                if key_contains(key, point):
                    query_labels[index].append(g)

    assert histogram == {"empty": 54_058, "point": 224, "line": 4, "plane": 2}
    expected_labels = [(1, 2), (P - 1, 1)]
    assert all(labels == expected_labels for labels in query_labels)
    return {
        "tau": list(tau),
        "scope_note": (
            "pure-tail rows only; this is a necessary fixed-q gate, not the "
            "complete fringe scan"
        ),
        "normalized_plane_origin": list(q0),
        "normalized_plane_directions": [list(direction) for direction in directions],
        "candidate_nonzero_g": P * P - 1,
        "affine_subspace_type_histogram": histogram,
        "queries": [
            {
                "quartic_coefficients": list(q),
                "plane_coordinates": list(point),
                "incident_labels": [list(label) for label in labels],
            }
            for q, point, labels in zip(FROZEN_Q, query_coordinates, query_labels)
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(__file__).with_name(
            "unique_tail_p233_three_h8_m4_O3_affine_subspace_prototype_report.json"
        ),
    )
    args = parser.parse_args()

    report = {
        "status": "PROVED_ALGORITHM_PROTOTYPE_GLOBAL_INCOMPLETE",
        "field_prime": P,
        "scope": "two exact O3 prototypes; not a full tau scan",
        "slice_minor_gcd_prototype": {
            "tau": list(TAU_SLICE),
            "catalogues": [slice_catalogue(TAU_SLICE, endpoint) for endpoint in range(3)],
        },
        "dual_deletion_affine_subspace_prototype": dual_deletion_catalogue(TAU_DUAL),
        "global_boundary": {
            "all_generic_tau_scanned": False,
            "high_dimensional_q_fibres_expanded": False,
            "positive_dimensional_minor_loci_require_exception_routing": True,
            "runtime_is_output_sensitive": True,
            "O3_closed": False,
        },
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    args.report.write_bytes(rendered.encode("utf-8"))
    print("PASS")
    print("slice counts: 9/11/13; all-zero vertical slices: 0/0/0")
    print("dual H histogram: empty=54058 point=224 line=4 plane=2")
    print("under pure-tail rows, both frozen q queries hit exactly [(1,2),(232,1)]")


if __name__ == "__main__":
    main()
