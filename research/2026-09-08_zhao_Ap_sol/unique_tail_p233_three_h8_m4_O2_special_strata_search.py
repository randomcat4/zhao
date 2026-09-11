#!/usr/bin/env python3
"""Exact special-strata census for the p=233, m=4, O2 mask orbit.

This verifier has three logically separate parts.

1. It computes the ranks of the O2 z-block and of the six tail rows on the
   nine-dimensional even-quartic space.
2. It exhausts the exceptional z and exceptional tau strata and applies the
   common-core deletion odd-quintic gate to every resulting (z,tau) pair.
3. It independently checks the four O1-quartic states inherited by O2,
   enumerates their Z1 solutions, and applies first the F2/F3 deletion gate
   and then the one additional, z1-independent F1 tail-pair condition.

All arithmetic is exact in F_233.  No candidate list from another script is
used to determine the exceptional rank strata or their compatible partners.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


P = 233
HALF = 117
POINT_COUNT = P * P
INVERSES = np.asarray([0] + [pow(value, P - 2, P) for value in range(1, P)], dtype=np.int64)
W = ((1, 0), (0, 1), (-1, -1))
EVEN_BASIS = (
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
ODD_BASIS = (
    (1, 0),
    (0, 1),
    (3, 0),
    (2, 1),
    (1, 2),
    (0, 3),
    (5, 0),
    (4, 1),
    (3, 2),
    (2, 3),
    (1, 4),
    (0, 5),
)
B_SHIFTS = ((0, 0), (0, 1), (-1, -1), (-1, 0), (0, -1), (1, 1))
TAIL_SHIFTS = ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1))
# F2 and F3 together supply five tail centers; tau+w1 is the sixth center and
# comes from the fixed tail pair {w2,w3} in F1, independently of z1.
F23_TAIL_SHIFTS = ((-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1))

O1_Q = (74, 201, 35, 201, 109, 146, 189, 146, 109)
O1_STATES = (
    ((58, 174), (59, 174)),
    ((58, 174), (174, 59)),
    ((60, 176), (59, 174)),
    ((60, 176), (174, 59)),
)


def inv_mod(value: int) -> int:
    return pow(int(value) % P, P - 2, P)


def point_index(x: int, y: int) -> int:
    return (x % P) * P + (y % P)


def evaluation_table(basis: tuple[tuple[int, int], ...]) -> np.ndarray:
    x, y = np.meshgrid(
        np.arange(P, dtype=np.int64),
        np.arange(P, dtype=np.int64),
        indexing="ij",
    )
    columns = []
    for x_degree, y_degree in basis:
        columns.append(pow_array(x, x_degree) * pow_array(y, y_degree) % P)
    return np.stack(columns, axis=-1).reshape(POINT_COUNT, len(basis))


def pow_array(values: np.ndarray, exponent: int) -> np.ndarray:
    if exponent == 0:
        return np.ones_like(values)
    result = np.ones_like(values)
    factor = values.copy()
    power = exponent
    while power:
        if power & 1:
            result = result * factor % P
        factor = factor * factor % P
        power >>= 1
    return result


def shifted_indices(shifts: tuple[tuple[int, int], ...]) -> np.ndarray:
    x = np.repeat(np.arange(P, dtype=np.int64), P)
    y = np.tile(np.arange(P, dtype=np.int64), P)
    return np.stack(
        [((x + dx) % P) * P + (y + dy) % P for dx, dy in shifts],
        axis=1,
    )


def rank_mod(rows: np.ndarray) -> int:
    matrix = [[int(value) % P for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        source = next(
            (r for r in range(pivot_row, len(matrix)) if matrix[r][column]),
            None,
        )
        if source is None:
            continue
        matrix[pivot_row], matrix[source] = matrix[source], matrix[pivot_row]
        scale = inv_mod(matrix[pivot_row][column])
        matrix[pivot_row] = [(scale * value) % P for value in matrix[pivot_row]]
        for r in range(pivot_row + 1, len(matrix)):
            factor = matrix[r][column]
            if factor:
                matrix[r] = [
                    (matrix[r][c] - factor * matrix[pivot_row][c]) % P
                    for c in range(len(matrix[0]))
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def rank_histogram(rows: np.ndarray, batch_size: int) -> tuple[dict[str, int], np.ndarray]:
    ranks = np.empty(rows.shape[0], dtype=np.int16)
    for start in range(0, rows.shape[0], batch_size):
        stop = min(start + batch_size, rows.shape[0])
        for offset, matrix in enumerate(rows[start:stop]):
            ranks[start + offset] = rank_mod(matrix)
    values, counts = np.unique(ranks, return_counts=True)
    return {str(int(v)): int(c) for v, c in zip(values, counts)}, ranks


def compatible(coefficients: np.ndarray, rhs: np.ndarray) -> tuple[bool, int]:
    coefficient_rank = rank_mod(coefficients)
    augmented_rank = rank_mod(np.concatenate((coefficients, rhs[:, None]), axis=1))
    return coefficient_rank == augmented_rank, coefficient_rank


def batch_compatible(
    coefficients: np.ndarray, rhs: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Exact batched consistency and coefficient rank over F_233."""
    augmented = np.concatenate((coefficients % P, rhs[:, :, None] % P), axis=2)
    batch_count, row_count, column_count_plus_one = augmented.shape
    column_count = column_count_plus_one - 1
    ranks = np.zeros(batch_count, dtype=np.int16)
    row_numbers = np.arange(row_count, dtype=np.int16)[None, :]
    for column in range(column_count):
        eligible = row_numbers >= ranks[:, None]
        nonzero = eligible & (augmented[:, :, column] != 0)
        found = np.any(nonzero, axis=1)
        selected = np.flatnonzero(found)
        if selected.size == 0:
            continue
        pivot_sources = np.argmax(nonzero[selected], axis=1)
        pivot_targets = ranks[selected].astype(np.int64)
        saved = augmented[selected, pivot_targets, :].copy()
        augmented[selected, pivot_targets, :] = augmented[
            selected, pivot_sources, :
        ]
        augmented[selected, pivot_sources, :] = saved
        pivot_rows = augmented[selected, pivot_targets, :]
        scales = INVERSES[pivot_rows[:, column]]
        pivot_rows = pivot_rows * scales[:, None] % P
        augmented[selected, pivot_targets, :] = pivot_rows
        factors = augmented[selected, :, column].copy()
        factors[np.arange(selected.size), pivot_targets] = 0
        augmented[selected] = (
            augmented[selected] - factors[:, :, None] * pivot_rows[:, None, :]
        ) % P
        ranks[selected] += 1
    inconsistent = np.any(
        np.all(augmented[:, :, :column_count] == 0, axis=2)
        & (augmented[:, :, column_count] != 0),
        axis=1,
    )
    return ~inconsistent, ranks


def b_points(z: tuple[int, int]) -> list[tuple[int, int]]:
    return [((z[0] + dx) % P, (z[1] + dy) % P) for dx, dy in B_SHIFTS]


def tail_points(tau: tuple[int, int]) -> list[tuple[int, int]]:
    return [((tau[0] + dx) % P, (tau[1] + dy) % P) for dx, dy in TAIL_SHIFTS]


def even_compatible(
    z: tuple[int, int], tau: tuple[int, int], even_values: np.ndarray
) -> tuple[bool, int]:
    points = b_points(z) + tail_points(tau) + [tau]
    coefficients = even_values[[point_index(*point) for point in points]]
    rhs = np.asarray([0] * 12 + [1], dtype=np.int64)
    return compatible(coefficients, rhs)


def compatible_tau_for_z(
    z: tuple[int, int], even_values: np.ndarray
) -> list[dict[str, object]]:
    result = []
    base = even_values[[point_index(*point) for point in b_points(z)]]
    tail_indices = shifted_indices(TAIL_SHIFTS)
    all_indices = np.arange(1, POINT_COUNT, dtype=np.int64)
    for start in range(0, all_indices.size, 2048):
        indices = all_indices[start : start + 2048]
        coefficients = np.concatenate(
            (
                np.broadcast_to(base, (indices.size, 6, 9)),
                even_values[tail_indices[indices]],
                even_values[indices][:, None, :],
            ),
            axis=1,
        )
        rhs = np.zeros((indices.size, 13), dtype=np.int64)
        rhs[:, -1] = 1
        ok, ranks = batch_compatible(coefficients, rhs)
        for local_index in np.flatnonzero(ok):
            index = int(indices[int(local_index)])
            result.append(
                {
                    "tau": [index // P, index % P],
                    "quartic_affine_dimension": 9 - int(ranks[int(local_index)]),
                }
            )
    return result


def compatible_z_for_tau(
    tau: tuple[int, int], even_values: np.ndarray
) -> list[dict[str, object]]:
    result = []
    tail = even_values[[point_index(*point) for point in tail_points(tau)]]
    center = even_values[point_index(*tau)]
    b_indices = shifted_indices(B_SHIFTS)
    all_indices = np.arange(POINT_COUNT, dtype=np.int64)
    for start in range(0, all_indices.size, 2048):
        indices = all_indices[start : start + 2048]
        coefficients = np.concatenate(
            (
                even_values[b_indices[indices]],
                np.broadcast_to(tail, (indices.size, 6, 9)),
                np.broadcast_to(center, (indices.size, 1, 9)),
            ),
            axis=1,
        )
        rhs = np.zeros((indices.size, 13), dtype=np.int64)
        rhs[:, -1] = 1
        ok, ranks = batch_compatible(coefficients, rhs)
        for local_index in np.flatnonzero(ok):
            index = int(indices[int(local_index)])
            result.append(
                {
                    "z": [index // P, index % P],
                    "quartic_affine_dimension": 9 - int(ranks[int(local_index)]),
                }
            )
    return result


def known_centers(
    z: tuple[int, int], tau: tuple[int, int], include_f1_tail_pair: bool
) -> list[tuple[int, int]]:
    shifts = TAIL_SHIFTS if include_f1_tail_pair else F23_TAIL_SHIFTS
    points = [((tau[0] + dx) % P, (tau[1] + dy) % P) for dx, dy in shifts]
    points.extend(b_points(z))
    # Evaluation conditions merge equal quotient targets, never literal positions.
    return list(dict.fromkeys(points))


def deletion_gate_for_g(
    z: tuple[int, int],
    tau: tuple[int, int],
    g: tuple[int, int],
    odd_values: np.ndarray,
    include_f1_tail_pair: bool,
) -> tuple[bool, int]:
    hx, hy = g[0] * HALF % P, g[1] * HALF % P
    rows: list[np.ndarray] = []
    rhs: list[int] = []
    for vx, vy in known_centers(z, tau, include_f1_tail_pair):
        rows.append(odd_values[point_index(vx + hx, vy + hy)])
        rows.append(odd_values[point_index(vx - hx, vy - hy)])
        rhs.extend((0, 0))
    rows.append(odd_values[point_index(tau[0] + hx, tau[1] + hy)])
    rhs.append(1)
    rows.append(odd_values[point_index(tau[0] - hx, tau[1] - hy)])
    rhs.append(0)
    ok, rank = compatible(np.asarray(rows), np.asarray(rhs, dtype=np.int64))
    return ok, 12 - rank


def deletion_survivors(
    z: tuple[int, int],
    tau: tuple[int, int],
    odd_values: np.ndarray,
    include_f1_tail_pair: bool = True,
) -> list[dict[str, object]]:
    survivors = []
    centers = known_centers(z, tau, include_f1_tail_pair)
    all_indices = np.arange(1, POINT_COUNT, dtype=np.int64)
    for start in range(0, all_indices.size, 512):
        indices = all_indices[start : start + 512]
        gx = indices // P
        gy = indices % P
        hx = gx * HALF % P
        hy = gy * HALF % P
        row_blocks = []
        for vx, vy in centers:
            plus = ((vx + hx) % P) * P + (vy + hy) % P
            minus = ((vx - hx) % P) * P + (vy - hy) % P
            row_blocks.extend((odd_values[plus][:, None, :], odd_values[minus][:, None, :]))
        center_plus = ((tau[0] + hx) % P) * P + (tau[1] + hy) % P
        center_minus = ((tau[0] - hx) % P) * P + (tau[1] - hy) % P
        row_blocks.extend(
            (odd_values[center_plus][:, None, :], odd_values[center_minus][:, None, :])
        )
        coefficients = np.concatenate(row_blocks, axis=1)
        rhs = np.zeros((indices.size, coefficients.shape[1]), dtype=np.int64)
        rhs[:, -2] = 1
        ok, ranks = batch_compatible(coefficients, rhs)
        for local_index in np.flatnonzero(ok):
            index = int(indices[int(local_index)])
            survivors.append(
                {
                    "g": [index // P, index % P],
                    "odd_quintic_affine_dimension": 12 - int(ranks[int(local_index)]),
                }
            )
    return survivors


def q_value(point: tuple[int, int], coefficients: tuple[int, ...]) -> int:
    x, y = point
    total = 0
    for coefficient, (x_degree, y_degree) in zip(coefficients, EVEN_BASIS):
        total += coefficient * pow(x % P, x_degree, P) * pow(y % P, y_degree, P)
    return total % P


def o1_z1_solutions() -> list[list[int]]:
    solutions = []
    shifts = ((0, 0), (1, 0), (0, -1), (1, 1))
    for x in range(P):
        for y in range(P):
            if all(q_value((x + dx, y + dy), O1_Q) == 0 for dx, dy in shifts):
                solutions.append([x, y])
    return solutions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank-batch-size", type=int, default=2048)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(__file__).with_name(
            "unique_tail_p233_three_h8_m4_O2_special_strata_exclusion_report.json"
        ),
    )
    args = parser.parse_args()

    even_values = evaluation_table(EVEN_BASIS)
    odd_values = evaluation_table(ODD_BASIS)
    b_indices = shifted_indices(B_SHIFTS)
    tail_indices = shifted_indices(TAIL_SHIFTS)

    z_rank_histogram, z_ranks = rank_histogram(
        even_values[b_indices], args.rank_batch_size
    )
    tail_rank_histogram, tail_ranks = rank_histogram(
        even_values[tail_indices], args.rank_batch_size
    )
    tail_plus_center_rows = np.concatenate(
        (even_values[tail_indices], even_values[:, None, :]), axis=1
    )
    tail_plus_center_histogram, tail_plus_center_ranks = rank_histogram(
        tail_plus_center_rows, args.rank_batch_size
    )

    expected_z_histogram = {"4": 4, "5": 7, "6": 54278}
    expected_tail_histogram = {"3": 1, "5": 12, "6": 54276}
    expected_tail_plus_center_histogram = {"4": 1, "5": 6, "6": 6, "7": 54276}
    if z_rank_histogram != expected_z_histogram:
        raise AssertionError((z_rank_histogram, expected_z_histogram))
    if tail_rank_histogram != expected_tail_histogram:
        raise AssertionError((tail_rank_histogram, expected_tail_histogram))
    if tail_plus_center_histogram != expected_tail_plus_center_histogram:
        raise AssertionError(
            (tail_plus_center_histogram, expected_tail_plus_center_histogram)
        )

    exceptional_z_indices = np.flatnonzero(z_ranks < 6)
    exceptional_z_rows = []
    low_z_pairs = []
    for index in exceptional_z_indices:
        z = (int(index) // P, int(index) % P)
        partners = compatible_tau_for_z(z, even_values)
        pair_rows = []
        for item in partners:
            tau = tuple(item["tau"])
            gamma = deletion_survivors(z, tau, odd_values)
            pair = {"z": list(z), **item, "known_gamma": gamma}
            pair_rows.append(pair)
            low_z_pairs.append(pair)
        exceptional_z_rows.append(
            {
                "z": list(z),
                "z_block_rank": int(z_ranks[int(index)]),
                "compatible_tau_count": len(partners),
                "pairs": pair_rows,
            }
        )

    inconsistent_tau = []
    compatible_exceptional_tau = []
    for index in range(1, POINT_COUNT):
        tail_rank = int(tail_ranks[index])
        extended_rank = int(tail_plus_center_ranks[index])
        if tail_rank == 5 and extended_rank == 5:
            inconsistent_tau.append([index // P, index % P])
        elif tail_rank == 5 and extended_rank == 6:
            tau = (index // P, index % P)
            partners = compatible_z_for_tau(tau, even_values)
            pair_rows = []
            for item in partners:
                z = tuple(item["z"])
                gamma = deletion_survivors(z, tau, odd_values)
                pair_rows.append({"tau": list(tau), **item, "known_gamma": gamma})
            compatible_exceptional_tau.append(
                {
                    "tau": list(tau),
                    "compatible_z_count": len(partners),
                    "pairs": pair_rows,
                }
            )

    if len(low_z_pairs) != 14:
        raise AssertionError(len(low_z_pairs))
    if any(len(item["known_gamma"]) != 1 for item in low_z_pairs):
        raise AssertionError("a low-z pair did not have exactly one known-gamma label")
    if len(inconsistent_tau) != 6 or len(compatible_exceptional_tau) != 6:
        raise AssertionError((inconsistent_tau, compatible_exceptional_tau))
    exceptional_tau_pairs = [
        pair for item in compatible_exceptional_tau for pair in item["pairs"]
    ]
    if len(exceptional_tau_pairs) != 6:
        raise AssertionError(len(exceptional_tau_pairs))
    if any(len(item["known_gamma"]) != 1 for item in exceptional_tau_pairs):
        raise AssertionError("an exceptional-tau pair did not have one gamma label")

    z1_solutions = o1_z1_solutions()
    if len(z1_solutions) != P or any((y - x) % P != 117 for x, y in z1_solutions):
        raise AssertionError(z1_solutions[:20])
    inherited_rows = []
    for z, tau in O1_STATES:
        for point in b_points(z) + tail_points(tau):
            if q_value(point, O1_Q) != 0:
                raise AssertionError((z, tau, point))
        if q_value(tau, O1_Q) != 1:
            raise AssertionError((z, tau, "normalization"))
        gamma_f23 = deletion_survivors(
            z, tau, odd_values, include_f1_tail_pair=False
        )
        gamma_known = deletion_survivors(
            z, tau, odd_values, include_f1_tail_pair=True
        )
        inherited_rows.append(
            {
                "z": list(z),
                "tau": list(tau),
                "gamma_F2_F3": gamma_f23,
                "gamma_after_F1_tail_pair": gamma_known,
            }
        )
    if [len(row["gamma_F2_F3"]) for row in inherited_rows] != [2, 0, 2, 0]:
        raise AssertionError(inherited_rows)
    if any(row["gamma_after_F1_tail_pair"] for row in inherited_rows):
        raise AssertionError(inherited_rows)

    report = {
        "status": "PROVED_REDUCTION",
        "scope": (
            "p=233, three length-eight singleton endpoints, m=4, "
            "O2=(1,1,2,3), exceptional z/tau strata and inherited O1-q slice only"
        ),
        "even_basis": [f"x^{a}y^{b}" for a, b in EVEN_BASIS],
        "odd_basis": [f"x^{a}y^{b}" for a, b in ODD_BASIS],
        "z_block_rank_histogram": z_rank_histogram,
        "exceptional_z_count": len(exceptional_z_rows),
        "exceptional_z_rows": exceptional_z_rows,
        "low_z_atomic_pair_count": len(low_z_pairs),
        "low_z_pairs_with_known_gamma_size_one": len(low_z_pairs),
        "tail_rank_histogram_all_tau_including_zero": tail_rank_histogram,
        "tail_plus_center_rank_histogram_all_tau_including_zero": (
            tail_plus_center_histogram
        ),
        "tail_inconsistent_nonzero_tau": inconsistent_tau,
        "tail_compatible_exceptional_rows": compatible_exceptional_tau,
        "tail_compatible_exceptional_pair_count": len(exceptional_tau_pairs),
        "tail_exceptional_pairs_with_known_gamma_size_one": len(
            exceptional_tau_pairs
        ),
        "inherited_O1_q": list(O1_Q),
        "inherited_O1_z1_solution_count_per_state": len(z1_solutions),
        "inherited_O1_z1_solutions": z1_solutions,
        "inherited_O1_rows": inherited_rows,
        "inherited_O1_state_count_closed": len(O1_STATES) * len(z1_solutions),
        "capacity_argument": {
            "core_length": 460,
            "maximum_multiplicity_per_nonzero_quotient_label": 232,
            "minimum_support_size": 2,
            "reason": "p copies of one nonzero quotient label form a zero sum",
        },
        "generic_frontier": {
            "required_z_block_rank": 6,
            "required_tail_rank": 6,
            "required_tail_plus_center_rank": 7,
            "method": (
                "For each generic z, take a 3-dimensional kernel basis K_z. "
                "The six tail evaluations form a 6x3 polynomial matrix in tau; "
                "all 3x3 minors have degree at most 12.  Use finite-field gcd/"
                "resultant elimination and then require center evaluation to "
                "increase rank.  Apply the q-free deletion Gamma gate before z1."
            ),
            "closed": False,
        },
        "logical_boundary": {
            "ordinary_atom_nonrepresentation_used_before_signed_zero": True,
            "different_literal_positions_merged": False,
            "completion_pointing_used": False,
            "mixed_fibre_gates_used": False,
            "generic_O2_closed": False,
            "m4_closed": False,
            "global_A_p_claimed": False,
        },
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    args.report.write_bytes(rendered.encode("utf-8"))
    print(
        json.dumps(
            {
                "status": report["status"],
                "z_block_rank_histogram": z_rank_histogram,
                "low_z_atomic_pair_count": len(low_z_pairs),
                "inconsistent_tau_count": len(inconsistent_tau),
                "compatible_exceptional_tau_pair_count": len(
                    exceptional_tau_pairs
                ),
                "inherited_O1_state_count_closed": report[
                    "inherited_O1_state_count_closed"
                ],
                "report_sha256": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
