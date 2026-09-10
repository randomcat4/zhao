#!/usr/bin/env python3
"""Unified projection-label feasibility for every canonical cover skeleton.

This is a quotient-layer theorem, not a full labelled candidate search.  For
each canonical incidence witness constructed by
``unique_tail_cover_forbidden_block_generalization.py`` it checks the exact
linear equations shared by all actual positions:

* every endpoint has projection sum zero;
* U and L have projection sum zero;
* one common axis coordinate makes every endpoint sum zero, U sum -b, and
  L sum one.

It then places *all* proper nonempty subsets of every Q_E, together with all
non-cover endpoint intersections, in one simultaneous forbidden-functional
family.  A row-space obstruction is exact.  If none occurs and the number N
of distinct nonzero functionals is less than p^2, two independently chosen
vectors in the common nullspace avoid all N codimension-two bad events by the
union bound.  Hence a single C_p^2 projection labelling exists in which every
Q_E is an atom and every required endpoint intersection is nonaxial.

No actual a-height, R partition, long-complement atom, induced short block,
or Hasse constraint is asserted here.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import importlib.util
import json


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "unique_tail_cover_forbidden_block_generalization.py"
REPORT_PATH = HERE / "unique_tail_cover_unified_projection_labels_report.json"


def load_source_module():
    spec = importlib.util.spec_from_file_location("cover_generalization", SOURCE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def mask_vector(mask: int, width: int) -> tuple[int, ...]:
    return tuple((mask >> index) & 1 for index in range(width))


def set_mask(values: frozenset[int] | set[int]) -> int:
    answer = 0
    for value in values:
        answer |= 1 << value
    return answer


def rref_rows(
    rows: list[tuple[int, ...]] | tuple[tuple[int, ...], ...], p_value: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    if not rows:
        return tuple(), tuple()
    matrix = [[entry % p_value for entry in row] for row in rows]
    width = len(matrix[0])
    pivots: list[int] = []
    pivot_row = 0
    for column in range(width):
        found = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, p_value)
        matrix[pivot_row] = [
            entry * inverse % p_value for entry in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % p_value
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    nonzero = tuple(
        tuple(row) for row in matrix if any(entry % p_value for entry in row)
    )
    return nonzero, tuple(pivots)


def rank(rows: list[tuple[int, ...]] | tuple[tuple[int, ...], ...], p_value: int) -> int:
    return len(rref_rows(rows, p_value)[0])


def in_row_space(
    vector: tuple[int, ...], basis: tuple[tuple[int, ...], ...], p_value: int
) -> bool:
    return rank([*basis, vector], p_value) == len(basis)


def affine_consistent(
    rows: tuple[tuple[int, ...], ...], rhs: tuple[int, ...], p_value: int
) -> bool:
    augmented = tuple(row + (value % p_value,) for row, value in zip(rows, rhs))
    return rank(list(rows), p_value) == rank(list(augmented), p_value)


def affine_solution(
    rows: tuple[tuple[int, ...], ...], rhs: tuple[int, ...], p_value: int
) -> tuple[int, ...]:
    augmented = [
        tuple(entry % p_value for entry in row) + (value % p_value,)
        for row, value in zip(rows, rhs)
    ]
    reduced, pivots = rref_rows(augmented, p_value)
    width = len(rows[0])
    assert all(pivot < width for pivot in pivots)
    answer = [0] * width
    for row, pivot in zip(reduced, pivots):
        answer[pivot] = row[-1]
    assert all(
        sum(coefficient * value for coefficient, value in zip(row, answer))
        % p_value
        == target % p_value
        for row, target in zip(rows, rhs)
    )
    return tuple(answer)


def nullspace_basis(
    rows: tuple[tuple[int, ...], ...], p_value: int
) -> tuple[tuple[int, ...], ...]:
    reduced, pivots = rref_rows(rows, p_value)
    width = len(rows[0])
    free_columns = tuple(column for column in range(width) if column not in pivots)
    basis = []
    for free in free_columns:
        vector = [0] * width
        vector[free] = 1
        for row, pivot in zip(reduced, pivots):
            vector[pivot] = -row[free] % p_value
        basis.append(tuple(vector))
    assert len(basis) == width - len(pivots)
    assert all(
        sum(coefficient * value for coefficient, value in zip(row, vector))
        % p_value
        == 0
        for row in rows
        for vector in basis
    )
    return tuple(basis)


def deterministic_coefficients(
    key: tuple[int, int, int, tuple[int, ...]],
    attempt: int,
    coordinate: str,
    count: int,
    p_value: int,
) -> tuple[int, ...]:
    values = []
    block = 0
    while len(values) < count:
        payload = json.dumps(
            [key, attempt, coordinate, block], separators=(",", ":")
        ).encode("ascii")
        digest = hashlib.sha256(payload).digest()
        for offset in range(0, len(digest), 4):
            values.append(int.from_bytes(digest[offset : offset + 4], "big") % p_value)
            if len(values) == count:
                break
        block += 1
    return tuple(values)


def combine_basis(
    basis: tuple[tuple[int, ...], ...], coefficients: tuple[int, ...], p_value: int
) -> tuple[int, ...]:
    if not basis:
        return tuple()
    return tuple(
        sum(coefficient * vector[index] for coefficient, vector in zip(coefficients, basis))
        % p_value
        for index in range(len(basis[0]))
    )


def subset_sum(vector: tuple[int, ...], mask: int, p_value: int) -> int:
    return sum(
        value for index, value in enumerate(vector) if mask >> index & 1
    ) % p_value


def canonical_keys(module) -> tuple[tuple[int, int, int, tuple[int, ...]], ...]:
    keys = set()
    for _shape_name, (vertex_count, edges) in module.SHAPES.items():
        for colouring in product(module.TRACE_MASKS, repeat=vertex_count):
            if not all(
                module.is_trace_edge(colouring[left], colouring[right])
                for left, right in edges
            ):
                continue
            for left, right in module.candidate_cover_pairs(colouring):
                other_traces = tuple(
                    sorted(
                        colouring[vertex]
                        for vertex in range(vertex_count)
                        if vertex not in (left, right)
                    )
                )
                for p_value in module.PRIMES:
                    keys.add(
                        (p_value, colouring[left], colouring[right], other_traces)
                    )
    return tuple(sorted(keys))


def proper_nonempty_submasks(mask: int):
    submask = (mask - 1) & mask
    while submask:
        yield submask
        submask = (submask - 1) & mask


def analyse_witness(module, key: tuple[int, int, int, tuple[int, ...]]) -> dict[str, object]:
    p_value, left_trace, right_trace, other_traces = key
    colouring = (left_trace, right_trace, *other_traces)
    witness = module.build_incidence_witness(p_value, colouring, (0, 1))
    endpoints = witness["endpoints"]
    assert isinstance(endpoints, tuple)
    u_set = witness["u_set"]
    assert isinstance(u_set, frozenset)
    width = len(witness["universe_names"])
    full_mask = (1 << width) - 1
    endpoint_masks = tuple(set_mask(endpoint) for endpoint in endpoints)
    u_mask = set_mask(u_set)

    equation_masks = (*endpoint_masks, u_mask, full_mask)
    equation_rows = tuple(mask_vector(mask, width) for mask in equation_masks)
    row_basis, _pivots = rref_rows(equation_rows, p_value)
    equation_rank = len(row_basis)
    nullity = width - equation_rank

    b_value = 4 if p_value == 233 else 5
    axis_rhs = (*([0] * len(endpoints)), -b_value, 1)
    axis_ok = affine_consistent(equation_rows, tuple(axis_rhs), p_value)

    atomic_masks: set[int] = set()
    for endpoint_mask in endpoint_masks:
        q_mask = full_mask ^ endpoint_mask
        atomic_masks.update(proper_nonempty_submasks(q_mask))

    intersection_masks: set[int] = set()
    axial_cover_intersections = 0
    for left, right in combinations(range(len(endpoint_masks)), 2):
        union_mask = endpoint_masks[left] | endpoint_masks[right]
        intersection_mask = endpoint_masks[left] & endpoint_masks[right]
        assert intersection_mask
        if union_mask == full_mask:
            axial_cover_intersections += 1
        else:
            intersection_masks.add(intersection_mask)

    forbidden_masks = atomic_masks | intersection_masks
    forced_atomic_masks = tuple(
        sorted(
            mask
            for mask in atomic_masks
            if in_row_space(mask_vector(mask, width), row_basis, p_value)
        )
    )
    forced_intersection_masks = tuple(
        sorted(
            mask
            for mask in intersection_masks
            if in_row_space(mask_vector(mask, width), row_basis, p_value)
        )
    )
    forced_zero_masks = tuple(
        sorted(
            mask
            for mask in forbidden_masks
            if in_row_space(mask_vector(mask, width), row_basis, p_value)
        )
    )
    live_functionals = len(forbidden_masks) - len(forced_zero_masks)
    union_bound_ok = not forced_zero_masks and live_functionals < p_value * p_value

    label_attempt = None
    label_values = None
    if axis_ok and union_bound_ok:
        axis_values = affine_solution(equation_rows, tuple(axis_rhs), p_value)
        kernel_basis = nullspace_basis(equation_rows, p_value)
        assert len(kernel_basis) == nullity
        for attempt in range(10000):
            left_coefficients = deterministic_coefficients(
                key, attempt, "left", nullity, p_value
            )
            right_coefficients = deterministic_coefficients(
                key, attempt, "right", nullity, p_value
            )
            left_values = combine_basis(kernel_basis, left_coefficients, p_value)
            right_values = combine_basis(kernel_basis, right_coefficients, p_value)
            if all(
                not (
                    subset_sum(left_values, mask, p_value) == 0
                    and subset_sum(right_values, mask, p_value) == 0
                )
                for mask in forbidden_masks
            ):
                label_attempt = attempt
                label_values = [
                    [axis_values[index], left_values[index], right_values[index]]
                    for index in range(width)
                ]
                break
        assert label_values is not None

    # Each Q_E and every actual cover intersection must be forced projection
    # zero by the common equations.  This is an independent consistency check
    # on the row-space interpretation.
    for endpoint_mask in endpoint_masks:
        q_mask = full_mask ^ endpoint_mask
        assert in_row_space(mask_vector(q_mask, width), row_basis, p_value)
    for left, right in combinations(range(len(endpoint_masks)), 2):
        if endpoint_masks[left] | endpoint_masks[right] == full_mask:
            intersection_mask = endpoint_masks[left] & endpoint_masks[right]
            assert in_row_space(
                mask_vector(intersection_mask, width), row_basis, p_value
            )

    return {
        "p": p_value,
        "colouring": list(colouring),
        "position_count": width,
        "endpoint_count": len(endpoints),
        "equation_rank": equation_rank,
        "nullity": nullity,
        "axis_coordinate_consistent": axis_ok,
        "distinct_atomic_proper_subset_functionals": len(atomic_masks),
        "distinct_required_intersection_functionals": len(intersection_masks),
        "distinct_joint_forbidden_functionals": len(forbidden_masks),
        "forced_zero_atomic_subset_functionals": len(forced_atomic_masks),
        "forced_zero_required_intersection_functionals": len(
            forced_intersection_masks
        ),
        "forced_zero_forbidden_functionals": len(forced_zero_masks),
        "axial_cover_intersections": axial_cover_intersections,
        "union_bound_numerator": live_functionals,
        "union_bound_denominator": p_value * p_value,
        "unified_projection_labels_exist": axis_ok and union_bound_ok,
        "deterministic_label_search_attempt": label_attempt,
        "universe_names": list(witness["universe_names"]),
        "endpoint_position_indices": [
            sorted(endpoint) for endpoint in endpoints
        ],
        "unified_quotient_label_values": label_values,
    }


def build_report() -> dict[str, object]:
    module = load_source_module()
    keys = canonical_keys(module)
    assert len(keys) == 744
    rows = [analyse_witness(module, key) for key in keys]

    per_prime: dict[str, dict[str, object]] = {}
    for p_value in module.PRIMES:
        prime_rows = [row for row in rows if row["p"] == p_value]
        assert len(prime_rows) == 372
        counts = Counter(
            (
                row["position_count"],
                row["endpoint_count"],
                row["equation_rank"],
                row["nullity"],
            )
            for row in prime_rows
        )
        assert all(row["axis_coordinate_consistent"] for row in prime_rows)
        obstructed_rows = [
            row for row in prime_rows if row["forced_zero_forbidden_functionals"]
        ]
        feasible_rows = [
            row for row in prime_rows if row["unified_projection_labels_exist"]
        ]
        assert len(obstructed_rows) + len(feasible_rows) == len(prime_rows)
        per_prime[str(p_value)] = {
            "canonical_classes": len(prime_rows),
            "all_axis_coordinate_systems_consistent": True,
            "fixed_skeletons_with_forced_zero_forbidden_functional": len(
                obstructed_rows
            ),
            "fixed_skeletons_with_forced_atomic_subset": sum(
                bool(row["forced_zero_atomic_subset_functionals"])
                for row in obstructed_rows
            ),
            "fixed_skeletons_with_forced_required_intersection": sum(
                bool(row["forced_zero_required_intersection_functionals"])
                for row in obstructed_rows
            ),
            "fixed_skeletons_with_unified_projection_labels": len(feasible_rows),
            "max_joint_forbidden_functionals": max(
                int(row["distinct_joint_forbidden_functionals"])
                for row in prime_rows
            ),
            "min_nullity": min(int(row["nullity"]) for row in prime_rows),
            "max_deterministic_label_search_attempt": max(
                int(row["deterministic_label_search_attempt"])
                for row in feasible_rows
            ),
            "rank_nullity_distribution": [
                {
                    "position_count": key[0],
                    "endpoint_count": key[1],
                    "equation_rank": key[2],
                    "nullity": key[3],
                    "class_count": value,
                }
                for key, value in sorted(counts.items())
            ],
        }

    report: dict[str, object] = {
        "schema": "unique_tail_cover_unified_projection_labels_v1",
        "scope": {
            "interface": "canonical_cover_incidence_plus_one_unified_Cp3_quotient_labelling",
            "included": [
                "the fixed constructed actual-position L skeleton chosen for each of the 372 canonical cover trace classes per prime",
                "one shared axis coordinate satisfying every endpoint, U, and L sum equation",
                "one shared two-coordinate projection labelling satisfying every endpoint, U, and L sum equation",
                "all proper nonempty internal subset sums of every Q_E simultaneously",
                "all non-cover endpoint intersections simultaneously",
            ],
            "excluded": [
                "actual a-heights and C_p^4 atomicity of Z",
                "a common R partition and its P_i labels",
                "new induced short zero-sum blocks and Hasse rows",
                "long complements of newly induced F_3 blocks",
                "packing-type closure or a full counterexample",
            ],
        },
        "source_dependency_sha256": hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        "canonical_class_count": len(rows),
        "per_prime": per_prime,
        "rows_sha256": canonical_hash(rows),
        "rows": rows,
        "status": "FIXED_INCIDENCE_SKELETONS_CLASSIFIED_AT_UNIFIED_PROJECTION_LAYER__TRACE_CLASSES_AND_FULL_LABELLED_INTERFACE_OPEN",
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
