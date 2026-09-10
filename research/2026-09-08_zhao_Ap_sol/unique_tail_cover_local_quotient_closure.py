#!/usr/bin/env python3
"""All automatically induced quotient-zero blocks inside X union L.

For each fixed canonical cover-incidence skeleton, jointly choose the axis
coordinate and two projection coordinates from the exact common affine/kernel
systems.  Every nonempty subset of L is checked against every available number
of identical X positions.  Forbidden middle lengths, the singleton case, and
the unique positive-core length-eight F3 gate are enforced simultaneously,
along with every Q_E internal proper subset and every non-cover endpoint
intersection.

This still omits R, actual heights, Hasse equations, and C_p^4 atomicity.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import hashlib
import importlib.util
import json


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "unique_tail_cover_unified_projection_labels.py"
REPORT_PATH = HERE / "unique_tail_cover_local_quotient_closure_report.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def is_forbidden_x_closure(
    p_value: int,
    b_value: int,
    u_mask: int,
    support_mask: int,
    axis_sum: int,
) -> bool:
    core = (-axis_sum) % p_value
    if core > p_value - 4:
        return False
    total_length = core + support_mask.bit_count()
    if total_length == 1 or 9 <= total_length <= 2 * p_value + 2:
        return True
    if total_length == 8 and core > 0:
        return not (core == b_value and support_mask == u_mask)
    return False


def vector_sum(vector: tuple[int, ...], mask: int, p_value: int) -> int:
    return sum(
        value for index, value in enumerate(vector) if mask >> index & 1
    ) % p_value


def in_rref_row_space(
    vector: tuple[int, ...],
    row_basis: tuple[tuple[int, ...], ...],
    pivots: tuple[int, ...],
    p_value: int,
) -> bool:
    remainder = list(vector)
    for row, pivot in zip(row_basis, pivots):
        factor = remainder[pivot]
        if factor:
            remainder = [
                (left - factor * right) % p_value
                for left, right in zip(remainder, row)
            ]
    return not any(remainder)


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
            [key, attempt, coordinate, block, "full_local_closure"],
            separators=(",", ":"),
        ).encode("ascii")
        digest = hashlib.sha256(payload).digest()
        for offset in range(0, len(digest), 4):
            values.append(int.from_bytes(digest[offset : offset + 4], "big") % p_value)
            if len(values) == count:
                break
        block += 1
    return tuple(values)


def analyse(base, source, key: tuple[int, int, int, tuple[int, ...]]) -> dict[str, object]:
    p_value, left_trace, right_trace, other_traces = key
    b_value = 4 if p_value == 233 else 5
    colouring = (left_trace, right_trace, *other_traces)
    witness = source.build_incidence_witness(p_value, colouring, (0, 1))
    endpoints = witness["endpoints"]
    u_set = witness["u_set"]
    assert isinstance(endpoints, tuple) and isinstance(u_set, frozenset)
    width = len(witness["universe_names"])
    full_mask = (1 << width) - 1
    u_mask = base.set_mask(u_set)
    endpoint_masks = tuple(base.set_mask(endpoint) for endpoint in endpoints)
    equation_masks = (*endpoint_masks, u_mask, full_mask)
    equation_rows = tuple(base.mask_vector(mask, width) for mask in equation_masks)
    row_basis, pivots = base.rref_rows(equation_rows, p_value)
    kernel_basis = base.nullspace_basis(equation_rows, p_value)
    axis_rhs = tuple((*([0] * len(endpoints)), -b_value, 1))
    axis_base = base.affine_solution(equation_rows, axis_rhs, p_value)
    outside_tail_mask = full_mask ^ u_mask
    assert in_rref_row_space(
        base.mask_vector(outside_tail_mask, width), row_basis, pivots, p_value
    )
    outside_tail_axis_sum = vector_sum(axis_base, outside_tail_mask, p_value)
    assert outside_tail_axis_sum == b_value + 1
    assert is_forbidden_x_closure(
        p_value,
        b_value,
        u_mask,
        outside_tail_mask,
        outside_tail_axis_sum,
    )

    mandatory_nonaxis = set()
    for endpoint_mask in endpoint_masks:
        q_mask = full_mask ^ endpoint_mask
        mandatory_nonaxis.update(base.proper_nonempty_submasks(q_mask))
    for left in range(len(endpoint_masks)):
        for right in range(left + 1, len(endpoint_masks)):
            if endpoint_masks[left] | endpoint_masks[right] != full_mask:
                intersection = endpoint_masks[left] & endpoint_masks[right]
                assert intersection
                mandatory_nonaxis.add(intersection)

    forced_mandatory = []
    forced_forbidden_x = []
    forced_permitted_short = []
    for mask in range(1, full_mask + 1):
        functional = base.mask_vector(mask, width)
        if not in_rref_row_space(functional, row_basis, pivots, p_value):
            continue
        if mask in mandatory_nonaxis:
            forced_mandatory.append(mask)
            continue
        axis_sum = vector_sum(axis_base, mask, p_value)
        if is_forbidden_x_closure(p_value, b_value, u_mask, mask, axis_sum):
            forced_forbidden_x.append(mask)
        else:
            forced_permitted_short.append(mask)

    exact_obstruction = bool(forced_mandatory or forced_forbidden_x)

    def describe_mask(mask: int) -> dict[str, object]:
        axis_sum = vector_sum(axis_base, mask, p_value)
        core = (-axis_sum) % p_value
        return {
            "mask": mask,
            "position_indices": [index for index in range(width) if mask >> index & 1],
            "position_names": [
                witness["universe_names"][index]
                for index in range(width)
                if mask >> index & 1
            ],
            "support_size": mask.bit_count(),
            "axis_sum": axis_sum,
            "x_core_size": core,
            "total_length": core + mask.bit_count(),
        }

    first_forced_mandatory = (
        describe_mask(min(forced_mandatory, key=lambda mask: (mask.bit_count(), mask)))
        if forced_mandatory
        else None
    )
    first_forced_forbidden_x = (
        describe_mask(
            min(forced_forbidden_x, key=lambda mask: (mask.bit_count(), mask))
        )
        if forced_forbidden_x
        else None
    )
    labels = None
    label_attempt = None
    automatically_induced_allowed_short_blocks = None
    if not exact_obstruction:
        nullity = len(kernel_basis)
        for attempt in range(10000):
            axis_delta_coefficients = deterministic_coefficients(
                key, attempt, "axis_delta", nullity, p_value
            )
            first_coefficients = deterministic_coefficients(
                key, attempt, "rho_first", nullity, p_value
            )
            second_coefficients = deterministic_coefficients(
                key, attempt, "rho_second", nullity, p_value
            )
            axis_delta = base.combine_basis(
                kernel_basis, axis_delta_coefficients, p_value
            )
            first = base.combine_basis(kernel_basis, first_coefficients, p_value)
            second = base.combine_basis(kernel_basis, second_coefficients, p_value)
            axis = tuple(
                (left + right) % p_value
                for left, right in zip(axis_base, axis_delta)
            )
            if any(
                vector_sum(first, mask, p_value) == 0
                and vector_sum(second, mask, p_value) == 0
                for mask in mandatory_nonaxis
            ):
                continue
            bad = False
            allowed_short = []
            for mask in range(1, full_mask + 1):
                if not (
                    vector_sum(first, mask, p_value) == 0
                    and vector_sum(second, mask, p_value) == 0
                ):
                    continue
                axis_sum = vector_sum(axis, mask, p_value)
                if is_forbidden_x_closure(p_value, b_value, u_mask, mask, axis_sum):
                    bad = True
                    break
                core = (-axis_sum) % p_value
                if core <= p_value - 4:
                    total_length = core + mask.bit_count()
                    if 2 <= total_length <= 8:
                        allowed_short.append([mask, core, total_length])
            if bad:
                continue
            labels = [
                [axis[index], first[index], second[index]]
                for index in range(width)
            ]
            label_attempt = attempt
            automatically_induced_allowed_short_blocks = allowed_short
            break
        assert labels is not None

    event_count = full_mask
    assert event_count < p_value * p_value
    return {
        "p": p_value,
        "colouring": list(colouring),
        "universe_names": list(witness["universe_names"]),
        "endpoint_position_indices": [sorted(endpoint) for endpoint in endpoints],
        "position_count": width,
        "endpoint_count": len(endpoints),
        "equation_rank": len(row_basis),
        "nullity": len(kernel_basis),
        "mandatory_nonaxis_subset_count": len(mandatory_nonaxis),
        "forced_mandatory_nonaxis_violations": len(forced_mandatory),
        "forced_forbidden_x_closures": len(forced_forbidden_x),
        "forced_permitted_short_blocks": len(forced_permitted_short),
        "universal_outside_tail_obstruction": describe_mask(outside_tail_mask),
        "first_forced_mandatory_nonaxis_violation": first_forced_mandatory,
        "first_forced_forbidden_x_closure": first_forced_forbidden_x,
        "union_bound_event_count": event_count,
        "union_bound_denominator": p_value * p_value,
        "exact_fixed_skeleton_obstruction": exact_obstruction,
        "local_quotient_closure_labels_exist": not exact_obstruction,
        "deterministic_label_search_attempt": label_attempt,
        "unified_quotient_label_values": labels,
        "automatically_induced_allowed_short_blocks": automatically_induced_allowed_short_blocks,
    }


def build_report() -> dict[str, object]:
    base = load_module(BASE_PATH, "unified_projection_base")
    source = base.load_source_module()
    keys = base.canonical_keys(source)
    rows = [analyse(base, source, key) for key in keys]
    assert len(rows) == 744
    per_prime = {}
    for p_value in source.PRIMES:
        prime_rows = [row for row in rows if row["p"] == p_value]
        obstructed = [row for row in prime_rows if row["exact_fixed_skeleton_obstruction"]]
        survivors = [row for row in prime_rows if row["local_quotient_closure_labels_exist"]]
        assert len(obstructed) + len(survivors) == 372
        per_prime[str(p_value)] = {
            "fixed_skeletons": 372,
            "fixed_skeletons_exactly_obstructed": len(obstructed),
            "fixed_skeletons_with_local_quotient_closure_labels": len(survivors),
            "obstructed_by_mandatory_nonaxis": sum(
                bool(row["forced_mandatory_nonaxis_violations"])
                for row in obstructed
            ),
            "obstructed_by_forbidden_x_closure": sum(
                bool(row["forced_forbidden_x_closures"])
                for row in obstructed
            ),
            "all_have_universal_outside_tail_obstruction": all(
                row["universal_outside_tail_obstruction"] is not None
                for row in prime_rows
            ),
            "first_forced_forbidden_total_length_distribution": dict(
                sorted(
                    Counter(
                        int(row["first_forced_forbidden_x_closure"]["total_length"])
                        for row in obstructed
                        if row["first_forced_forbidden_x_closure"] is not None
                    ).items()
                )
            ),
            "max_deterministic_label_search_attempt": max(
                (int(row["deterministic_label_search_attempt"]) for row in survivors),
                default=None,
            ),
            "allowed_short_block_count_distribution": dict(
                sorted(
                    Counter(
                        len(row["automatically_induced_allowed_short_blocks"])
                        for row in survivors
                    ).items()
                )
            ),
        }
    report: dict[str, object] = {
        "schema": "unique_tail_cover_local_quotient_closure_v1",
        "scope": {
            "included": [
                "one fixed actual-position incidence skeleton per canonical trace class",
                "one unified C_p^3 label per actual L position",
                "all nonempty subsets of L and every available identical-X core",
                "all Q_E internal proper subsets and all non-cover endpoint intersections",
                "the singleton, middle-length, and unique positive-core length-eight quotient gates",
            ],
            "excluded": [
                "all actual positions and labels in R",
                "actual a-heights and the F1/F2 height classification of allowed short blocks",
                "new F3 long complements, Hasse rows, and C_p^4 atomicity of Z",
                "other incidences in the same trace class and packing-type closure",
            ],
        },
        "dependencies_sha256": {
            BASE_PATH.name: hashlib.sha256(BASE_PATH.read_bytes()).hexdigest(),
            base.SOURCE_PATH.name: hashlib.sha256(base.SOURCE_PATH.read_bytes()).hexdigest(),
        },
        "per_prime": per_prime,
        "rows_sha256": canonical_hash(rows),
        "rows": rows,
        "status": "FIXED_SKELETON_LOCAL_QUOTIENT_CLOSURE_CLASSIFIED__R_HEIGHT_HASSE_OPEN",
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
