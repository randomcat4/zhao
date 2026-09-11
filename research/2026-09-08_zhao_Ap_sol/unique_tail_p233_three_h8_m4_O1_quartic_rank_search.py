#!/usr/bin/env python3
"""Exact O1 even-quartic compatibility census over F_233.

The O1 fringe incidence forces an even quartic q to vanish on eight points
P_z.  The common tail positions force q(tau +/- e), q(tau +/- f), and
q(tau +/- (e+f)) to vanish, while q(tau) must be nonzero (and can then be
scaled to one).  This program exhausts all z and all nonzero tau without
importing any candidate list from an earlier search.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np


P = 233
BASIS_SIZE = 9
POINT_COUNT = P * P
P_SHIFTS = (
    (0, 0),
    (0, 1),
    (-1, 0),
    (1, 1),
    (-1, -1),
    (0, -1),
    (-2, -1),
    (-2, -2),
)
TAIL_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1))


def inv_mod(a: int) -> int:
    return pow(int(a) % P, P - 2, P)


def evaluation_table() -> np.ndarray:
    x, y = np.meshgrid(
        np.arange(P, dtype=np.int64),
        np.arange(P, dtype=np.int64),
        indexing="ij",
    )
    x2 = x * x % P
    y2 = y * y % P
    return np.stack(
        (
            np.ones_like(x),
            x2,
            x * y % P,
            y2,
            x2 * x2 % P,
            x2 * x % P * y % P,
            x2 * y2 % P,
            x * y2 % P * y % P,
            y2 * y2 % P,
        ),
        axis=-1,
    ).reshape(POINT_COUNT, BASIS_SIZE)


def point_index(x: int, y: int) -> int:
    return (x % P) * P + (y % P)


def rref_nullspace(rows: np.ndarray) -> tuple[int, list[list[int]]]:
    column_count = int(rows.shape[1])
    a = [[int(v) % P for v in row] for row in rows]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        source = next(
            (r for r in range(pivot_row, len(a)) if a[r][column] != 0),
            None,
        )
        if source is None:
            continue
        a[pivot_row], a[source] = a[source], a[pivot_row]
        scale = inv_mod(a[pivot_row][column])
        a[pivot_row] = [(scale * v) % P for v in a[pivot_row]]
        for r in range(len(a)):
            if r == pivot_row or a[r][column] == 0:
                continue
            factor = a[r][column]
            a[r] = [
                (a[r][c] - factor * a[pivot_row][c]) % P
                for c in range(column_count)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(a):
            break

    free_columns = [c for c in range(column_count) if c not in pivot_columns]
    basis: list[list[int]] = []
    for free in free_columns:
        vector = [0] * column_count
        vector[free] = 1
        for r in range(len(pivot_columns) - 1, -1, -1):
            column = pivot_columns[r]
            vector[column] = -sum(
                a[r][c] * vector[c] for c in free_columns
            ) % P
        basis.append(vector)
    return len(pivot_columns), basis


def det2(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]) % P


def det3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return (
        a[:, 0] * (b[:, 1] * c[:, 2] - b[:, 2] * c[:, 1])
        - a[:, 1] * (b[:, 0] * c[:, 2] - b[:, 2] * c[:, 0])
        + a[:, 2] * (b[:, 0] * c[:, 1] - b[:, 1] * c[:, 0])
    ) % P


def determinant_batch(rows: list[np.ndarray]) -> np.ndarray:
    dimension = len(rows)
    total = np.zeros(rows[0].shape[0], dtype=np.int64)
    for permutation in itertools.permutations(range(dimension)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(dimension)
            for j in range(i + 1, dimension)
        )
        term = np.ones(rows[0].shape[0], dtype=np.int64)
        for r, c in enumerate(permutation):
            term = term * rows[r][:, c] % P
        total = total + (-term if inversions % 2 else term)
    return total % P


def exceptional_compatibility(
    values: np.ndarray, neighbor_indices: np.ndarray
) -> np.ndarray:
    """Return tau mask where ker(U_tau) contains q with q(tau) != 0."""
    dimension = values.shape[1]
    u = [values[neighbor_indices[:, k], :] for k in range(6)]
    center = values
    rank_at_least_one = np.any(np.stack(u, axis=1) != 0, axis=(1, 2))

    if dimension == 2:
        rank_at_least_two = np.zeros(POINT_COUNT, dtype=bool)
        center_increases_rank = np.zeros(POINT_COUNT, dtype=bool)
        for i, j in itertools.combinations(range(6), 2):
            rank_at_least_two |= det2(u[i], u[j]) != 0
        for row in u:
            center_increases_rank |= det2(row, center) != 0
        return (~rank_at_least_two) & (
            (rank_at_least_one & center_increases_rank)
            | ((~rank_at_least_one) & np.any(center != 0, axis=1))
        )

    if dimension == 3:
        rank_at_least_two = np.zeros(POINT_COUNT, dtype=bool)
        rank_at_least_three = np.zeros(POINT_COUNT, dtype=bool)
        center_over_rank_one = np.zeros(POINT_COUNT, dtype=bool)
        center_over_rank_two = np.zeros(POINT_COUNT, dtype=bool)
        for i, j in itertools.combinations(range(6), 2):
            cross = np.stack(
                (
                    u[i][:, 1] * u[j][:, 2] - u[i][:, 2] * u[j][:, 1],
                    u[i][:, 2] * u[j][:, 0] - u[i][:, 0] * u[j][:, 2],
                    u[i][:, 0] * u[j][:, 1] - u[i][:, 1] * u[j][:, 0],
                ),
                axis=1,
            ) % P
            rank_at_least_two |= np.any(cross != 0, axis=1)
            center_over_rank_two |= np.sum(cross * center, axis=1) % P != 0
        for i, j, k in itertools.combinations(range(6), 3):
            rank_at_least_three |= det3(u[i], u[j], u[k]) != 0
        for row in u:
            cross = np.stack(
                (
                    row[:, 1] * center[:, 2] - row[:, 2] * center[:, 1],
                    row[:, 2] * center[:, 0] - row[:, 0] * center[:, 2],
                    row[:, 0] * center[:, 1] - row[:, 1] * center[:, 0],
                ),
                axis=1,
            ) % P
            center_over_rank_one |= np.any(cross != 0, axis=1)
        rank_zero = ~rank_at_least_one
        rank_one = rank_at_least_one & ~rank_at_least_two
        rank_two = rank_at_least_two & ~rank_at_least_three
        return (
            (rank_zero & np.any(center != 0, axis=1))
            | (rank_one & center_over_rank_one)
            | (rank_two & center_over_rank_two)
        )

    if dimension == 4:
        rank_at_least_two = np.zeros(POINT_COUNT, dtype=bool)
        rank_at_least_three = np.zeros(POINT_COUNT, dtype=bool)
        rank_at_least_four = np.zeros(POINT_COUNT, dtype=bool)
        center_over_rank_one = np.zeros(POINT_COUNT, dtype=bool)
        center_over_rank_two = np.zeros(POINT_COUNT, dtype=bool)
        center_over_rank_three = np.zeros(POINT_COUNT, dtype=bool)

        for i, j in itertools.combinations(range(6), 2):
            for c1, c2 in itertools.combinations(range(4), 2):
                minor = (
                    u[i][:, c1] * u[j][:, c2]
                    - u[i][:, c2] * u[j][:, c1]
                ) % P
                rank_at_least_two |= minor != 0
                center_minor = (
                    u[i][:, c1] * center[:, c2]
                    - u[i][:, c2] * center[:, c1]
                ) % P
                center_over_rank_one |= center_minor != 0
            for columns in itertools.combinations(range(4), 3):
                with_center = [u[i][:, columns], u[j][:, columns], center[:, columns]]
                center_over_rank_two |= det3(*with_center) != 0

        for i, j, k in itertools.combinations(range(6), 3):
            rows3 = (u[i], u[j], u[k])
            for columns in itertools.combinations(range(4), 3):
                projected = [row[:, columns] for row in rows3]
                rank_at_least_three |= det3(*projected) != 0
            center_over_rank_three |= determinant_batch(
                [u[i], u[j], u[k], center]
            ) != 0

        for indices in itertools.combinations(range(6), 4):
            rank_at_least_four |= determinant_batch([u[i] for i in indices]) != 0

        rank_zero = ~rank_at_least_one
        rank_one = rank_at_least_one & ~rank_at_least_two
        rank_two = rank_at_least_two & ~rank_at_least_three
        rank_three = rank_at_least_three & ~rank_at_least_four
        return (
            (rank_zero & np.any(center != 0, axis=1))
            | (rank_one & center_over_rank_one)
            | (rank_two & center_over_rank_two)
            | (rank_three & center_over_rank_three)
        )

    raise AssertionError(f"unexpected exceptional nullity {dimension}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(__file__).with_name(
            "unique_tail_p233_three_h8_m4_O1_quartic_rank_search_report.json"
        ),
    )
    args = parser.parse_args()

    evaluations = evaluation_table()
    x = np.repeat(np.arange(P, dtype=np.int64), P)
    y = np.tile(np.arange(P, dtype=np.int64), P)
    neighbor_indices = np.stack(
        [((x + dx) % P) * P + (y + dy) % P for dx, dy in TAIL_DIRECTIONS],
        axis=1,
    )

    rank_histogram = {str(rank): 0 for rank in range(5, 9)}
    generic_z: list[list[int]] = []
    generic_q: list[list[int]] = []
    exceptional: list[dict[str, object]] = []

    for zx in range(P):
        for zy in range(P):
            indices = [point_index(zx + dx, zy + dy) for dx, dy in P_SHIFTS]
            rank, basis = rref_nullspace(evaluations[indices])
            if rank not in (5, 6, 7, 8):
                raise AssertionError((zx, zy, rank))
            rank_histogram[str(rank)] += 1
            if rank == 8:
                generic_z.append([zx, zy])
                generic_q.append(basis[0])
            else:
                exceptional.append(
                    {"z": [zx, zy], "rank": rank, "nullspace_basis": basis}
                )

    expected_histogram = {"5": 3, "6": 233, "7": 237, "8": 53816}
    if rank_histogram != expected_histogram:
        raise AssertionError((rank_histogram, expected_histogram))

    generic_survivors: list[dict[str, object]] = []
    q_array = np.asarray(generic_q, dtype=np.int64)
    for start in range(0, len(generic_q), args.batch_size):
        stop = min(start + args.batch_size, len(generic_q))
        values = evaluations @ q_array[start:stop].T % P
        compatible = values != 0
        for k in range(6):
            compatible &= values[neighbor_indices[:, k], :] == 0
        compatible[0, :] = False  # tau=0 is excluded because delta=2*tau != 0.
        tau_indices, local_q_indices = np.nonzero(compatible)
        for tau_index, local_q_index in zip(tau_indices, local_q_indices):
            q_index = start + int(local_q_index)
            generic_survivors.append(
                {
                    "z": generic_z[q_index],
                    "tau": [int(tau_index) // P, int(tau_index) % P],
                    "q": generic_q[q_index],
                    "q_tau": int(values[int(tau_index), int(local_q_index)]),
                }
            )

    exceptional_summary: list[dict[str, object]] = []
    exceptional_survivor_count = 0
    exceptional_witnesses: list[dict[str, object]] = []
    for item in exceptional:
        basis = np.asarray(item["nullspace_basis"], dtype=np.int64)
        values = evaluations @ basis.T % P
        compatible = exceptional_compatibility(values, neighbor_indices)
        compatible[0] = False
        tau_indices = np.flatnonzero(compatible)
        exceptional_survivor_count += int(tau_indices.size)
        exceptional_summary.append(
            {
                "z": item["z"],
                "rank": item["rank"],
                "nullity": int(basis.shape[0]),
                "compatible_tau_count": int(tau_indices.size),
            }
        )
        for tau_index in tau_indices[:10]:
            u_rows = values[neighbor_indices[int(tau_index)], :]
            _, coefficient_basis = rref_nullspace(u_rows)
            center_row = values[int(tau_index), :]
            coefficients = next(
                vector
                for vector in coefficient_basis
                if int(np.dot(center_row, np.asarray(vector, dtype=np.int64)) % P)
                != 0
            )
            q_tau = int(
                np.dot(center_row, np.asarray(coefficients, dtype=np.int64)) % P
            )
            scale = inv_mod(q_tau)
            normalized_coefficients = np.asarray(coefficients, dtype=np.int64) * scale % P
            normalized_q = normalized_coefficients @ basis % P
            exceptional_witnesses.append(
                {
                    "z": item["z"],
                    "rank": item["rank"],
                    "tau": [int(tau_index) // P, int(tau_index) % P],
                    "q": [int(value) for value in normalized_q],
                    "q_tau": 1,
                }
            )

    report = {
        "status": "PROVED" if not generic_survivors and not exceptional_survivor_count else "SURVIVORS",
        "scope": "p=233, three length-eight singleton endpoints, m=4 mask orbit O1=(0,1,1,4), even-quartic atomic compatibility only",
        "basis": ["1", "x^2", "xy", "y^2", "x^4", "x^3y", "x^2y^2", "xy^3", "y^4"],
        "P_shifts": [list(v) for v in P_SHIFTS],
        "rank_histogram": rank_histogram,
        "generic_z_count": len(generic_z),
        "exceptional_z_count": len(exceptional),
        "generic_compatible_pair_count": len(generic_survivors),
        "generic_witnesses": generic_survivors[:100],
        "exceptional_compatible_pair_count": exceptional_survivor_count,
        "exceptional_witnesses": exceptional_witnesses[:100],
        "exceptional_rows": exceptional_summary,
        "total_compatible_pair_count": len(generic_survivors) + exceptional_survivor_count,
        "denominator": {
            "z": POINT_COUNT,
            "nonzero_tau_per_z": POINT_COUNT - 1,
            "ordered_z_nonzero_tau_pairs": POINT_COUNT * (POINT_COUNT - 1),
        },
        "logical_boundary": {
            "q_tau_nonzero_is_normalized_to_one": True,
            "literal_fringe_incidence_used": True,
            "mixed_fibre_gates_used": False,
            "completion_pointing_used": False,
            "other_m4_orbits_used": False,
            "global_A_p_claimed": False,
        },
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    args.report.write_bytes(rendered.encode("utf-8"))
    report_hash = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
    print(
        json.dumps(
            {
                "status": report["status"],
                "rank_histogram": report["rank_histogram"],
                "generic_compatible_pair_count": report[
                    "generic_compatible_pair_count"
                ],
                "exceptional_compatible_pair_count": report[
                    "exceptional_compatible_pair_count"
                ],
                "total_compatible_pair_count": report["total_compatible_pair_count"],
                "exceptional_witnesses": report["exceptional_witnesses"],
                "report_sha256": report_hash,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
