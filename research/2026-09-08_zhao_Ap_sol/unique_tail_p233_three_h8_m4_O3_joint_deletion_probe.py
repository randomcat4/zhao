#!/usr/bin/env python3
"""Exact representative probe for the p=233, m=4, O3 joint-deletion gate.

The program has three logically separate parts.

1. It exhausts every nonzero tail centre tau and records the rank of the six
   common tail evaluation rows in the nine-dimensional even-quartic space.
2. At four frozen representative tau values it enumerates all three oriented
   O3 blocks Z_i(z), joins them by the *same normalized quartic q*, and never
   enumerates z_1 x z_2 x z_3 blindly.
3. For every common q it scans all nonzero possible labels g of a deleted
   common-core position.  The equation Delta_g D=q is solved exactly in the
   twelve-dimensional odd-quintic space.  The remaining kernel is
   <Y,Y^3,Y^5>; normalization and all nonempty subsets of all three literal
   fringes are imposed on the same three affine parameters.

All arithmetic is exact in F_233.  The output is a representative finite
probe, not an exhaustion of all tau and hence not a proof that O3 is empty.
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

REPRESENTATIVE_TAU = ((0, 1), (17, 31), (59, 174), (1, 117))

EXPECTED_COMMON_DATA = {
    (0, 1): (2, 16),
    (17, 31): (0, 0),
    (59, 174): (2, 217_172),
    (1, 117): (3, 24),
}

EXPECTED_Q = {
    (0, 1): {
        (0, 39, 115, 79, 194, 195, 232, 156, 155),
        (0, 0, 193, 79, 0, 117, 232, 156, 155),
    },
    (17, 31): set(),
    (59, 174): {
        (131, 221, 169, 221, 142, 14, 148, 14, 142),
        (74, 201, 35, 201, 109, 146, 189, 146, 109),
    },
    (1, 117): {
        (0, 132, 88, 0, 87, 117, 58, 116, 0),
        (0, 220, 145, 0, 145, 118, 173, 117, 0),
        (113, 132, 88, 145, 87, 117, 58, 116, 175),
    },
}

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


def evaluate_coefficients(coefficients: Vector, point: Point) -> int:
    return dot(coefficients, evaluation_row(point))


def rref(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    if not matrix:
        return [], []
    result = [[value % P for value in row] for row in matrix]
    row_count = len(result)
    column_count = len(result[0])
    pivot_columns: list[int] = []
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
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return result, pivot_columns


def rank(matrix: list[list[int]]) -> int:
    return len(rref(matrix)[1])


def nullspace_basis(matrix: list[list[int]]) -> list[list[int]]:
    reduced, pivots = rref(matrix)
    column_count = len(matrix[0])
    free = [column for column in range(column_count) if column not in pivots]
    basis: list[list[int]] = []
    for free_column in free:
        vector = [0] * column_count
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % P
        basis.append(vector)
    return basis


def tail_rows(tau: Point) -> list[list[int]]:
    return [
        evaluation_row(add(tau, scalar(sign, w)))
        for w in W
        for sign in (1, -1)
    ]


def z_block(z: Point, endpoint: int) -> tuple[Point, Point, Point, Point]:
    other_1 = (endpoint + 1) % 3
    other_2 = (endpoint + 2) % 3
    return (
        z,
        add(z, W[endpoint]),
        sub(z, W[other_1]),
        sub(z, W[other_2]),
    )


def oriented_fringe(tau: Point, z: Point, endpoint: int) -> tuple[Point, ...]:
    other_1 = (endpoint + 1) % 3
    other_2 = (endpoint + 2) % 3
    return (
        W[other_1],
        W[other_2],
        sub(tau, z),
        add(add(tau, W[endpoint]), z),
    )


def flip_z(z: Point, endpoint: int) -> Point:
    return neg(add(W[endpoint], z))


def affine_normalized_vectors(
    kernel: list[list[int]], functional: list[int]
) -> list[list[int]]:
    """Return every alpha in span(kernel) with functional.alpha=1."""
    coefficients = [dot(functional, vector) for vector in kernel]
    pivot = next((index for index, value in enumerate(coefficients) if value), None)
    if pivot is None:
        return []
    free = [index for index in range(len(kernel)) if index != pivot]
    output: list[list[int]] = []
    for values in itertools.product(range(P), repeat=len(free)):
        beta = [0] * len(kernel)
        for index, value in zip(free, values):
            beta[index] = value
        rhs = 1 - sum(coefficients[index] * beta[index] for index in free)
        beta[pivot] = rhs * pow(coefficients[pivot], P - 2, P) % P
        output.append(
            [
                sum(beta[index] * kernel[index][coordinate] for index in range(len(kernel)))
                % P
                for coordinate in range(len(kernel[0]))
            ]
        )
    return output


def quartic_catalogue(
    tau: Point, endpoint: int
) -> tuple[dict[Vector, list[Point]], dict[str, object]]:
    tails = tail_rows(tau)
    tail_kernel = nullspace_basis(tails)
    anchor = [dot(evaluation_row(tau), vector) for vector in tail_kernel]
    catalogue: dict[Vector, list[Point]] = {}
    compatible_z = 0
    kernel_dimension_histogram: dict[int, int] = {}

    for x in range(P):
        for y in range(P):
            z = (x, y)
            block_matrix = [
                [dot(evaluation_row(point), vector) for vector in tail_kernel]
                for point in z_block(z, endpoint)
            ]
            block_rank = rank(block_matrix)
            if rank(block_matrix + [anchor]) != block_rank + 1:
                continue
            compatible_z += 1
            kernel = nullspace_basis(block_matrix)
            kernel_dimension_histogram[len(kernel)] = (
                kernel_dimension_histogram.get(len(kernel), 0) + 1
            )
            for alpha in affine_normalized_vectors(kernel, anchor):
                q = tuple(
                    sum(
                        alpha[index] * tail_kernel[index][coordinate]
                        for index in range(len(tail_kernel))
                    )
                    % P
                    for coordinate in range(len(EVEN_MONOMIALS))
                )
                assert evaluate_coefficients(q, tau) == 1
                catalogue.setdefault(q, []).append(z)

    diagnostics = {
        "tail_kernel_dimension": len(tail_kernel),
        "compatible_oriented_z": compatible_z,
        "normalized_q_keys": len(catalogue),
        "q_z_incidences": sum(len(values) for values in catalogue.values()),
        "block_kernel_dimension_histogram": {
            str(key): value for key, value in sorted(kernel_dimension_histogram.items())
        },
        "maximum_z_per_q": max((len(values) for values in catalogue.values()), default=0),
    }
    return catalogue, diagnostics


def polynomial_add_term(poly: Polynomial, exponent: tuple[int, int], value: int) -> None:
    poly[exponent] = (poly.get(exponent, 0) + value) % P
    if poly[exponent] == 0:
        del poly[exponent]


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


def pullback_q(q: Vector, g: Point) -> Polynomial:
    """Return q(Xg+Yh), using h=(0,1) or h=(1,0)."""
    a, b = g
    result: Polynomial = {}
    if a:
        for (x_degree, y_degree), coefficient in zip(EVEN_MONOMIALS, q):
            for y_power in range(y_degree + 1):
                x_power = x_degree + y_degree - y_power
                value = (
                    coefficient
                    * comb(y_degree, y_power)
                    * pow(a, x_degree, P)
                    * pow(b, y_degree - y_power, P)
                )
                polynomial_add_term(result, (x_power, y_power), value)
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
    assert all((x_degree + y_degree) % 2 for x_degree, y_degree in result)
    return result


def coordinates(g: Point, shifted_without_half: Point) -> Point:
    """Coordinates of shifted_without_half+g/2 in the pullback basis."""
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


class AffineThreeSystem:
    def __init__(self, rows: list[list[int]] | None = None) -> None:
        self.rows = [] if rows is None else [row[:] for row in rows]
        self.consistent = True

    def add(self, coefficients: tuple[int, int, int], rhs: int) -> bool:
        row = [value % P for value in coefficients] + [rhs % P]
        for old in self.rows:
            pivot = next(index for index in range(3) if old[index])
            if row[pivot]:
                factor = row[pivot]
                row = [
                    (left - factor * right) % P for left, right in zip(row, old)
                ]
        pivot = next((index for index in range(3) if row[index]), None)
        if pivot is None:
            self.consistent = row[3] == 0
            return self.consistent
        inverse = pow(row[pivot], P - 2, P)
        row = [value * inverse % P for value in row]
        for index, old in enumerate(self.rows):
            if old[pivot]:
                factor = old[pivot]
                self.rows[index] = [
                    (left - factor * right) % P for left, right in zip(old, row)
                ]
        self.rows.append(row)
        self.rows.sort(key=lambda item: next(index for index in range(3) if item[index]))
        return True

    def solutions(self) -> list[tuple[int, int, int]]:
        if not self.consistent:
            return []
        pivots = [next(index for index in range(3) if row[index]) for row in self.rows]
        free = [index for index in range(3) if index not in pivots]
        output: list[tuple[int, int, int]] = []
        for values in itertools.product(range(P), repeat=len(free)):
            solution = [0, 0, 0]
            for index, value in zip(free, values):
                solution[index] = value
            for row, pivot in zip(self.rows, pivots):
                solution[pivot] = (
                    row[3] - sum(row[index] * solution[index] for index in free)
                ) % P
            output.append(tuple(solution))
        return output


def add_d_value(
    system: AffineThreeSystem,
    particular: Polynomial,
    g: Point,
    tau: Point,
    target: Point,
    desired: int,
) -> bool:
    point = coordinates(g, add(target, tau))
    y = point[1]
    row = (y, pow(y, 3, P), pow(y, 5, P))
    rhs = desired - evaluate_polynomial(particular, point)
    return system.add(row, rhs)


def nonempty_subset_targets(fringe: tuple[Point, ...]) -> list[Point]:
    targets: list[Point] = []
    for mask in range(1, 1 << len(fringe)):
        total = (0, 0)
        for index, point in enumerate(fringe):
            if mask & (1 << index):
                total = add(total, point)
        targets.append(neg(total))
    return targets


def common_tail_deletion_targets() -> list[Point]:
    targets: list[Point] = []
    for w in W:
        for target in (w, neg(w)):
            if target not in targets:
                targets.append(target)
    assert len(targets) == 6
    return targets


def joint_deletion_diagnostics(
    tau: Point,
    q: Vector,
    z_lists: list[list[Point]],
) -> dict[str, object]:
    """Join the three endpoint systems by the same kernel parameters."""
    base_candidates: list[tuple[Point, Polynomial, AffineThreeSystem]] = []
    normalization_failures = 0
    tail_targets = common_tail_deletion_targets()

    for gx in range(P):
        for gy in range(P):
            if gx == 0 and gy == 0:
                continue
            g = (gx, gy)
            particular = odd_antiderivative(q, g)
            system = AffineThreeSystem()
            if not add_d_value(system, particular, g, tau, (0, 0), 1):
                normalization_failures += 1
                continue
            if all(
                add_d_value(system, particular, g, tau, target, 0)
                for target in tail_targets
            ):
                base_candidates.append((g, particular, system))

    state_to_labels: dict[tuple[Point, Point, Point], set[Point]] = {}
    for g, particular, base in base_candidates:
        endpoint_maps: list[dict[tuple[int, int, int], list[Point]]] = []
        for endpoint in range(3):
            solution_map: dict[tuple[int, int, int], list[Point]] = {}
            for z in z_lists[endpoint]:
                system = AffineThreeSystem(base.rows)
                for target in nonempty_subset_targets(oriented_fringe(tau, z, endpoint)):
                    if not add_d_value(system, particular, g, tau, target, 0):
                        break
                if not system.consistent:
                    continue
                for solution in system.solutions():
                    solution_map.setdefault(solution, []).append(z)
            endpoint_maps.append(solution_map)
            if not solution_map:
                break
        if len(endpoint_maps) != 3:
            continue
        common_solutions = (
            set(endpoint_maps[0]) & set(endpoint_maps[1]) & set(endpoint_maps[2])
        )
        for solution in common_solutions:
            for triple in itertools.product(
                endpoint_maps[0][solution],
                endpoint_maps[1][solution],
                endpoint_maps[2][solution],
            ):
                state_to_labels.setdefault(triple, set()).add(g)

    quartic_oriented_states = (
        len(z_lists[0]) * len(z_lists[1]) * len(z_lists[2])
    )
    histogram: dict[int, int] = {}
    if state_to_labels:
        if quartic_oriented_states > 100_000:
            raise AssertionError("large state family unexpectedly survived the tail base")
        for triple in itertools.product(*z_lists):
            count = len(state_to_labels.get(triple, set()))
            histogram[count] = histogram.get(count, 0) + 1
    else:
        histogram[0] = quartic_oriented_states

    return {
        "quartic_oriented_states": quartic_oriented_states,
        "normalization_failures": normalization_failures,
        "labels_surviving_common_tail_deletion_rows": [
            list(item[0]) for item in base_candidates
        ],
        "oriented_states_with_a_joint_deletion_label": len(state_to_labels),
        "allowed_label_count_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "maximum_allowed_labels_per_oriented_state": max(histogram),
        "sample_state_labels": [
            {
                "z": [list(point) for point in triple],
                "labels": [list(point) for point in sorted(labels)],
            }
            for triple, labels in list(sorted(state_to_labels.items()))[:8]
        ],
    }


def matrix_multiply_2(left: tuple[Point, Point], right: tuple[Point, Point]):
    return tuple(
        tuple(
            sum(left[row][index] * right[index][column] for index in range(2)) % P
            for column in range(2)
        )
        for row in range(2)
    )


def matrix_vector_2(matrix: tuple[Point, Point], vector: Point) -> Point:
    return (
        (matrix[0][0] * vector[0] + matrix[0][1] * vector[1]) % P,
        (matrix[1][0] * vector[0] + matrix[1][1] * vector[1]) % P,
    )


def tail_s3() -> set[tuple[Point, Point]]:
    identity = ((1, 0), (0, 1))
    swap = ((0, 1), (1, 0))
    cycle = ((P - 1, 1), (P - 1, 0))
    group = {identity}
    pending = [identity]
    while pending:
        current = pending.pop()
        for generator in (swap, cycle):
            product = matrix_multiply_2(current, generator)
            if product not in group:
                group.add(product)
                pending.append(product)
    assert len(group) == 6
    assert all({matrix_vector_2(matrix, w) for w in W} == set(W) for matrix in group)
    return group


def symmetry_checks() -> dict[str, object]:
    group = tail_s3()
    test_tau = (17, 31)
    test_z = ((9, 20), (30, 40), (50, 60))
    for endpoint in range(3):
        before = oriented_fringe(test_tau, test_z[endpoint], endpoint)[2:]
        after = oriented_fringe(test_tau, flip_z(test_z[endpoint], endpoint), endpoint)[2:]
        assert after == (before[1], before[0])
        assert set(z_block(flip_z(test_z[endpoint], endpoint), endpoint)) == {
            neg(point) for point in z_block(test_z[endpoint], endpoint)
        }
    return {
        "tail_s3_order": len(group),
        "independent_internal_flips": 3,
        "semidirect_product_order": len(group) * 2**3,
        "tail_s3_generators": ["(x,y)->(y,x)", "(x,y)->(y-x,-x)"],
        "flip_formula": "z_i -> -w_i-z_i",
    }


def tail_rank_exhaustion() -> dict[str, object]:
    histogram: dict[int, int] = {}
    exceptional: list[dict[str, object]] = []
    for x in range(P):
        for y in range(P):
            if x == 0 and y == 0:
                continue
            tau = (x, y)
            rows = tail_rows(tau)
            tail_rank = rank(rows)
            anchor_rank = rank(rows + [evaluation_row(tau)])
            histogram[tail_rank] = histogram.get(tail_rank, 0) + 1
            if tail_rank < 6:
                exceptional.append(
                    {
                        "tau": list(tau),
                        "tail_rank": tail_rank,
                        "rank_with_anchor": anchor_rank,
                    }
                )
    assert histogram == {6: 54_276, 5: 12}
    impossible_orbits = [
        {(0, 116), (116, 0), (117, 117)},
        {(0, 117), (116, 116), (117, 0)},
    ]
    compatible_orbit = {
        (1, 117),
        (116, 117),
        (116, 232),
        (117, 1),
        (117, 116),
        (232, 116),
    }
    impossible = {
        tuple(item["tau"])
        for item in exceptional
        if item["rank_with_anchor"] == item["tail_rank"]
    }
    compatible = {tuple(item["tau"]) for item in exceptional} - impossible
    assert impossible == set().union(*impossible_orbits)
    assert compatible == compatible_orbit
    return {
        "nonzero_tau": P * P - 1,
        "tail_rank_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "rank5_anchor_in_rowspace_s3_orbits": [
            [list(point) for point in sorted(orbit)] for orbit in impossible_orbits
        ],
        "rank5_anchor_independent_s3_orbit": [
            list(point) for point in sorted(compatible_orbit)
        ],
    }


def representative_probe() -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for tau in REPRESENTATIVE_TAU:
        catalogues: list[dict[Vector, list[Point]]] = []
        endpoint_diagnostics: list[dict[str, object]] = []
        for endpoint in range(3):
            catalogue, diagnostics = quartic_catalogue(tau, endpoint)
            catalogues.append(catalogue)
            endpoint_diagnostics.append(diagnostics)

        common_q = set(catalogues[0]) & set(catalogues[1]) & set(catalogues[2])
        oriented_triples = sum(
            len(catalogues[0][q])
            * len(catalogues[1][q])
            * len(catalogues[2][q])
            for q in common_q
        )
        assert (len(common_q), oriented_triples) == EXPECTED_COMMON_DATA[tau]
        assert common_q == EXPECTED_Q[tau]

        q_rows: list[dict[str, object]] = []
        for q in sorted(common_q):
            z_lists = [catalogue[q] for catalogue in catalogues]
            deletion = joint_deletion_diagnostics(tau, q, z_lists)
            assert deletion["maximum_allowed_labels_per_oriented_state"] <= 1
            q_rows.append(
                {
                    "coefficients": list(q),
                    "oriented_z_per_endpoint": [len(values) for values in z_lists],
                    "quartic_oriented_triples": (
                        len(z_lists[0]) * len(z_lists[1]) * len(z_lists[2])
                    ),
                    "joint_deletion": deletion,
                }
            )

        output.append(
            {
                "tau": list(tau),
                "endpoint_catalogues": endpoint_diagnostics,
                "common_normalized_q": len(common_q),
                "quartic_oriented_triples": oriented_triples,
                "q_families": q_rows,
                "representative_layer_eliminated_by_quartic_or_capacity_gate": True,
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(__file__).with_name(
            "unique_tail_p233_three_h8_m4_O3_joint_deletion_probe_report.json"
        ),
    )
    args = parser.parse_args()

    report = {
        "status": "PASS_REPRESENTATIVE_PROBE_GLOBAL_INCOMPLETE",
        "field_prime": P,
        "scope": "p=233, m=4, O3=(2,2,2,2), four frozen tau representatives",
        "symmetry": symmetry_checks(),
        "tail_rank_exhaustion": tail_rank_exhaustion(),
        "joint_linear_system": {
            "odd_quintic_unknowns": 12,
            "quartic_zero_rows": 18,
            "quartic_normalization_rows": 1,
            "deletion_normalization_rows": 1,
            "literal_nonempty_fringe_subset_rows": 45,
            "total_rows_before_merging_duplicates": 65,
            "residual_kernel_basis_after_Delta_g_D_equals_q": ["Y", "Y^3", "Y^5"],
        },
        "support_capacity_gate": {
            "common_core_length": 460,
            "maximum_projected_multiplicity_in_a_zero_sum_free_sequence": P - 1,
            "necessary_minimum_allowed_labels": 2,
            "formula": "460 <= 232*|G(state)|",
        },
        "representatives": representative_probe(),
        "global_claims": {
            "all_tau_exhausted_for_tail_rank_only": True,
            "all_tau_exhausted_for_O3_blocks": False,
            "O3_closed": False,
            "full_A_p_claimed": False,
        },
    }

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    args.report.write_bytes(rendered.encode("utf-8"))
    print("PASS")
    print("tail-rank: 54276 rank-six, 12 rank-five")
    for item in report["representatives"]:
        print(
            "tau=",
            tuple(item["tau"]),
            "common-q=",
            item["common_normalized_q"],
            "oriented-triples=",
            item["quartic_oriented_triples"],
            "representative-layer-eliminated=",
            item["representative_layer_eliminated_by_quartic_or_capacity_gate"],
        )


if __name__ == "__main__":
    main()
