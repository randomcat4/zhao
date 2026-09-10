#!/usr/bin/env python3
r"""Search alternative real-position incidences for unified projection labels.

This program starts from the 372 canonical cover trace classes per prime in
``unique_tail_cover_forbidden_block_generalization.py``.  It keeps the frozen
three-point tail, endpoint lengths, one common outside point, a cover pair
whose union is L, three-slice transversality, endpoint distinctness, and the
existing unit/dense forbidden-block gates.  Unlike the old uniform witness,
all non-tail positions of a third endpoint may be chosen freely from the two
cover-exclusive outside pools.

For every candidate incidence it then imposes the common linear equations

    sum(E) = 0 for every endpoint E,  sum(U) = 0,  sum(L) = 0

over F_p on one projection coordinate.  A candidate is retained only if no
proper nonempty subset of any Q_E=L\E and no intersection of a non-cover
endpoint pair lies in the row space.  This is precisely the forced-zero
obstruction at the projection layer.  The affine axis-coordinate system with
right sides (0,...,0,-b,1) is checked separately.

A survivor is only a unified projection-label candidate.  No actual height,
common-R partition, induced short block, Hasse row, or full labelled SAT claim
is made here.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "unique_tail_cover_forbidden_block_generalization.py"
REPORT_PATH = HERE / "unique_tail_cover_projection_incidence_search_report.json"


def load_source_module():
    spec = importlib.util.spec_from_file_location("cover_generalization", SOURCE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def mask_from_positions(positions) -> int:
    answer = 0
    for position in positions:
        answer |= 1 << position
    return answer


def mask_row(mask: int, width: int) -> tuple[int, ...]:
    return tuple((mask >> position) & 1 for position in range(width))


def positions_from_mask(mask: int, width: int) -> tuple[int, ...]:
    return tuple(position for position in range(width) if mask >> position & 1)


def proper_nonempty_submasks(mask: int):
    submask = (mask - 1) & mask
    while submask:
        yield submask
        submask = (submask - 1) & mask


def rref_rows(
    rows: tuple[tuple[int, ...], ...] | list[tuple[int, ...]], p_value: int
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
    nonzero = tuple(tuple(row) for row in matrix if any(row))
    return nonzero, tuple(pivots)


def rowspace_contains(
    vector: tuple[int, ...],
    basis: tuple[tuple[int, ...], ...],
    pivots: tuple[int, ...],
    p_value: int,
) -> bool:
    reduced = [entry % p_value for entry in vector]
    for row, pivot in zip(basis, pivots):
        factor = reduced[pivot]
        if not factor:
            continue
        reduced = [
            (left - factor * right) % p_value
            for left, right in zip(reduced, row)
        ]
    return not any(reduced)


def rank(rows: tuple[tuple[int, ...], ...], p_value: int) -> int:
    return len(rref_rows(rows, p_value)[0])


def affine_consistent(
    rows: tuple[tuple[int, ...], ...], rhs: tuple[int, ...], p_value: int
) -> bool:
    augmented = tuple(row + (value % p_value,) for row, value in zip(rows, rhs))
    return rank(rows, p_value) == rank(augmented, p_value)


def canonical_keys(module) -> tuple[tuple[int, int, int, tuple[int, ...]], ...]:
    keys = set()
    from itertools import product

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
    answer = tuple(sorted(keys))
    assert len(answer) == 744
    return answer


def incidence_template(p_value: int, left_trace: int, right_trace: int) -> dict:
    endpoint_length = 7 if p_value == 233 else 8
    outside_per_side = endpoint_length - 3
    width = 4 + 2 * outside_per_side
    u_mask = 0b111
    y_position = 3
    y_mask = 1 << y_position
    a_outside = tuple(range(4, 4 + outside_per_side))
    b_outside = tuple(range(4 + outside_per_side, width))
    outside_mask = mask_from_positions((*a_outside, *b_outside))
    left_mask = left_trace | y_mask | mask_from_positions(a_outside)
    right_mask = right_trace | y_mask | mask_from_positions(b_outside)
    full_mask = (1 << width) - 1
    assert left_mask.bit_count() == right_mask.bit_count() == endpoint_length
    assert left_mask | right_mask == full_mask
    assert (left_mask & right_mask).bit_count() == 2

    left_only_u = left_trace & ~right_trace
    right_only_u = right_trace & ~left_trace
    assert left_only_u.bit_count() == right_only_u.bit_count() == 1
    a_slice = left_only_u | mask_from_positions(a_outside)
    b_slice = right_only_u | mask_from_positions(b_outside)
    c_slice = full_mask ^ a_slice ^ b_slice
    assert c_slice == (left_trace & right_trace) | y_mask

    names = ["u1", "u2", "u3", "y"]
    names.extend(f"a{index}" for index in range(outside_per_side))
    names.extend(f"b{index}" for index in range(outside_per_side))
    assert len(names) == width
    return {
        "p": p_value,
        "b": 4 if p_value == 233 else 5,
        "endpoint_length": endpoint_length,
        "outside_per_side": outside_per_side,
        "width": width,
        "u_mask": u_mask,
        "y_mask": y_mask,
        "outside_mask": outside_mask,
        "full_mask": full_mask,
        "a_slice": a_slice,
        "b_slice": b_slice,
        "c_slice": c_slice,
        "left_mask": left_mask,
        "right_mask": right_mask,
        "names": tuple(names),
    }


def candidate_masks(template: dict, trace: int) -> tuple[int, ...]:
    needed = template["endpoint_length"] - trace.bit_count() - 1
    answer = []
    outside_positions = positions_from_mask(
        template["outside_mask"], template["width"]
    )
    for selected in combinations(outside_positions, needed):
        mask = trace | template["y_mask"] | mask_from_positions(selected)
        if not mask & template["a_slice"]:
            continue
        if not mask & template["b_slice"]:
            continue
        if not mask & template["c_slice"]:
            continue
        answer.append(mask)
    return tuple(answer)


def unit_pair_rejected(module, template: dict, left: int, right: int) -> bool:
    return module.unit_pair_has_determined_rejection(
        template["p"],
        frozenset(positions_from_mask(left, template["width"])),
        frozenset(positions_from_mask(right, template["width"])),
        template["width"],
        frozenset(positions_from_mask(template["u_mask"], template["width"])),
    )


def dense_subset_is_indicator(
    endpoint_masks: tuple[int, ...],
    selected_indices: tuple[int, ...],
    m_value: int,
    template: dict,
) -> bool:
    k_value = len(selected_indices)
    for position in range(template["width"]):
        degree = sum(
            bool(endpoint_masks[index] >> position & 1)
            for index in selected_indices
        )
        coefficient = k_value - degree
        if template["u_mask"] >> position & 1:
            coefficient -= m_value
        if coefficient not in (0, 1):
            return False
    return True


def has_large_core_dense_rejection(
    endpoint_masks: tuple[int, ...], template: dict, newest_only: bool
) -> bool:
    endpoint_count = len(endpoint_masks)
    newest = endpoint_count - 1
    for subset_mask in range(1, 1 << endpoint_count):
        if newest_only and not (subset_mask >> newest & 1):
            continue
        indices = tuple(
            index for index in range(endpoint_count) if subset_mask >> index & 1
        )
        k_value = len(indices)
        for m_value in range(k_value + 1):
            if k_value + m_value * template["b"] < 4:
                continue
            if dense_subset_is_indicator(
                endpoint_masks, indices, m_value, template
            ):
                return True
    return False


def projection_analysis(endpoint_masks: tuple[int, ...], template: dict) -> dict:
    width = template["width"]
    p_value = template["p"]
    equation_masks = (*endpoint_masks, template["u_mask"], template["full_mask"])
    rows = tuple(mask_row(mask, width) for mask in equation_masks)
    basis, pivots = rref_rows(rows, p_value)
    rhs = (*([0] * len(endpoint_masks)), -template["b"], 1)
    axis_ok = affine_consistent(rows, tuple(rhs), p_value)

    atomic_masks: set[int] = set()
    for endpoint in endpoint_masks:
        q_mask = template["full_mask"] ^ endpoint
        atomic_masks.update(proper_nonempty_submasks(q_mask))

    intersection_masks: set[int] = set()
    cover_intersections = 0
    for left, right in combinations(endpoint_masks, 2):
        intersection = left & right
        assert intersection
        if left | right == template["full_mask"]:
            cover_intersections += 1
        else:
            intersection_masks.add(intersection)

    forced_atomic = tuple(
        sorted(
            mask
            for mask in atomic_masks
            if rowspace_contains(mask_row(mask, width), basis, pivots, p_value)
        )
    )
    forced_intersections = tuple(
        sorted(
            mask
            for mask in intersection_masks
            if rowspace_contains(mask_row(mask, width), basis, pivots, p_value)
        )
    )
    forbidden = atomic_masks | intersection_masks
    return {
        "equation_rank": len(basis),
        "nullity": width - len(basis),
        "axis_coordinate_consistent": axis_ok,
        "atomic_functionals": len(atomic_masks),
        "required_intersection_functionals": len(intersection_masks),
        "joint_forbidden_functionals": len(forbidden),
        "forced_atomic_masks": forced_atomic,
        "forced_intersection_masks": forced_intersections,
        "forced_zero_count": len(set(forced_atomic) | set(forced_intersections)),
        "cover_intersections": cover_intersections,
        "union_bound_numerator": len(forbidden),
        "union_bound_denominator": p_value * p_value,
    }


def partial_projection_ok(endpoint_masks: tuple[int, ...], template: dict) -> bool:
    analysis = projection_analysis(endpoint_masks, template)
    return bool(
        analysis["axis_coordinate_consistent"]
        and not analysis["forced_zero_count"]
    )


def complete_incidence_ok(module, endpoint_masks: tuple[int, ...], template: dict) -> bool:
    if len(set(endpoint_masks)) != len(endpoint_masks):
        return False
    for left, right in combinations(endpoint_masks, 2):
        if unit_pair_rejected(module, template, left, right):
            return False
    if has_large_core_dense_rejection(endpoint_masks, template, newest_only=False):
        return False
    analysis = projection_analysis(endpoint_masks, template)
    return bool(
        analysis["axis_coordinate_consistent"]
        and not analysis["forced_zero_count"]
        and analysis["union_bound_numerator"] < analysis["union_bound_denominator"]
    )


def deterministic_candidate_order(
    masks: tuple[int, ...], key: tuple, trace: int, baseline: tuple[int, ...]
) -> tuple[int, ...]:
    baseline_set = set(baseline)

    def order(mask: int):
        baseline_distance = min(
            ((mask ^ other).bit_count() for other in baseline_set), default=10**9
        )
        digest = hashlib.sha256(
            canonical_bytes([list(key), trace, mask])
        ).digest()
        return baseline_distance, digest, mask

    return tuple(sorted(masks, key=order))


def source_baseline(module, key: tuple, template: dict) -> tuple[int, ...]:
    p_value, left_trace, right_trace, other_traces = key
    witness = module.build_incidence_witness(
        p_value, (left_trace, right_trace, *other_traces), (0, 1)
    )
    source_names = tuple(witness["universe_names"])
    # The source uses a0 as a private position and a1,... as shared positions.
    # Our pool merely renumbers the same cover-exclusive positions.
    mapping = {"u1": 0, "u2": 1, "u3": 2, "y": 3}
    a_names = [name for name in source_names if name.startswith("a")]
    b_names = [name for name in source_names if name.startswith("b")]
    for index, name in enumerate(a_names):
        mapping[name] = 4 + index
    for index, name in enumerate(b_names):
        mapping[name] = 4 + len(a_names) + index
    answer = tuple(
        mask_from_positions(mapping[source_names[position]] for position in endpoint)
        for endpoint in witness["endpoints"]
    )
    assert answer[0] == template["left_mask"]
    assert answer[1] == template["right_mask"]
    return answer


def search_key(module, key: tuple, max_nodes: int) -> dict:
    p_value, left_trace, right_trace, other_traces = key
    template = incidence_template(p_value, left_trace, right_trace)
    baseline = source_baseline(module, key, template)
    baseline_analysis = projection_analysis(baseline, template)
    if not baseline_analysis["forced_zero_count"]:
        assert complete_incidence_ok(module, baseline, template)
        return {
            "status": "SOURCE_FIXED_SURVIVOR",
            "nodes": 0,
            "prunes": {},
            "endpoint_masks": baseline,
            "analysis": baseline_analysis,
        }

    pools = {}
    for trace in set(other_traces):
        baselines = tuple(
            baseline[index + 2]
            for index, value in enumerate(other_traces)
            if value == trace
        )
        pools[trace] = deterministic_candidate_order(
            candidate_masks(template, trace), key, trace, baselines
        )

    endpoint_masks = [template["left_mask"], template["right_mask"]]
    prunes = Counter()
    nodes = 0
    stopped = False

    assert partial_projection_ok(tuple(endpoint_masks), template)
    assert not has_large_core_dense_rejection(
        tuple(endpoint_masks), template, newest_only=False
    )

    def visit(index: int) -> tuple[int, ...] | None:
        nonlocal nodes, stopped
        if index == len(other_traces):
            answer = tuple(endpoint_masks)
            assert complete_incidence_ok(module, answer, template)
            return answer
        trace = other_traces[index]
        previous_same = None
        for earlier in range(index - 1, -1, -1):
            if other_traces[earlier] == trace:
                previous_same = endpoint_masks[earlier + 2]
                break

        for candidate in pools[trace]:
            if nodes >= max_nodes:
                stopped = True
                return None
            nodes += 1
            if candidate in endpoint_masks:
                prunes["duplicate"] += 1
                continue
            # Endpoints with the same trace are unlabeled.  Strict ordering
            # removes their permutation symmetry without removing incidences.
            if previous_same is not None and candidate <= previous_same:
                prunes["same_trace_symmetry"] += 1
                continue
            if any(
                unit_pair_rejected(module, template, candidate, assigned)
                for assigned in endpoint_masks
            ):
                prunes["unit_gate"] += 1
                continue
            endpoint_masks.append(candidate)
            current = tuple(endpoint_masks)
            if has_large_core_dense_rejection(current, template, newest_only=True):
                prunes["dense_gate"] += 1
                endpoint_masks.pop()
                continue
            if not partial_projection_ok(current, template):
                prunes["projection_forced_zero_or_axis"] += 1
                endpoint_masks.pop()
                continue
            answer = visit(index + 1)
            if answer is not None:
                return answer
            endpoint_masks.pop()
            if stopped:
                return None
        return None

    survivor = visit(0)
    if survivor is None:
        return {
            "status": "NODE_CAP_REACHED" if stopped else "FINITE_DOMAIN_UNSAT",
            "nodes": nodes,
            "prunes": dict(sorted(prunes.items())),
            "endpoint_masks": tuple(),
            "analysis": {},
            "baseline_forced_zero_count": baseline_analysis["forced_zero_count"],
        }
    analysis = projection_analysis(survivor, template)
    return {
        "status": "ALTERNATIVE_INCIDENCE_SURVIVOR",
        "nodes": nodes,
        "prunes": dict(sorted(prunes.items())),
        "endpoint_masks": survivor,
        "analysis": analysis,
        "baseline_forced_zero_count": baseline_analysis["forced_zero_count"],
    }


def serialise_row(key: tuple, result: dict) -> dict:
    p_value, left_trace, right_trace, other_traces = key
    template = incidence_template(p_value, left_trace, right_trace)
    masks = tuple(result["endpoint_masks"])
    row = {
        "p": p_value,
        "colouring": [left_trace, right_trace, *other_traces],
        "status": result["status"],
        "nodes": result["nodes"],
        "prunes": result["prunes"],
    }
    if "baseline_forced_zero_count" in result:
        row["source_fixed_forced_zero_count"] = result[
            "baseline_forced_zero_count"
        ]
    if masks:
        row["position_names"] = list(template["names"])
        row["endpoint_masks"] = list(masks)
        row["endpoint_positions"] = [
            [template["names"][position] for position in positions_from_mask(mask, template["width"])]
            for mask in masks
        ]
        analysis = dict(result["analysis"])
        analysis["forced_atomic_masks"] = list(analysis["forced_atomic_masks"])
        analysis["forced_intersection_masks"] = list(
            analysis["forced_intersection_masks"]
        )
        row["projection_analysis"] = analysis
        row["witness_sha256"] = canonical_hash(
            [p_value, row["colouring"], row["endpoint_masks"]]
        )
    return row


def self_test(module) -> dict:
    assert tuple(proper_nonempty_submasks(0b1011)) == (
        0b1010,
        0b1001,
        0b1000,
        0b0011,
        0b0010,
        0b0001,
    )
    basis, pivots = rref_rows(((1, 1, 0), (0, 1, 1)), 233)
    assert rowspace_contains((1, 0, -1), basis, pivots, 233)
    assert not rowspace_contains((1, 0, 0), basis, pivots, 233)

    dense_rows = 0
    for p_value in module.PRIMES:
        template = incidence_template(p_value, 3, 5)
        candidates = candidate_masks(template, 1)[:12]
        u_set = frozenset(positions_from_mask(template["u_mask"], template["width"]))
        for left, right in combinations(candidates, 2):
            endpoint_sets = tuple(
                frozenset(positions_from_mask(mask, template["width"]))
                for mask in (left, right)
            )
            for m_value in range(3):
                direct = dense_subset_is_indicator(
                    (left, right), (0, 1), m_value, template
                )
                source_direct = module.is_indicator(
                    module.dense_form_coefficients(
                        endpoint_sets,
                        template["width"],
                        u_set,
                        m_value,
                    )
                )
                assert direct == source_direct
                dense_rows += 1
    return {
        "proper_submask_test": True,
        "finite_field_rowspace_test": True,
        "dense_indicator_crosscheck_rows": dense_rows,
    }


def build_report(max_nodes: int, only_obstructed: bool) -> dict:
    module = load_source_module()
    tests = self_test(module)
    keys = canonical_keys(module)

    rows = []
    source_fixed_obstructed = Counter()
    source_fixed_unobstructed = Counter()
    for ordinal, key in enumerate(keys, start=1):
        data = incidence_template(key[0], key[1], key[2])
        baseline = source_baseline(module, key, data)
        if projection_analysis(baseline, data)["forced_zero_count"]:
            source_fixed_obstructed[key[0]] += 1
        else:
            source_fixed_unobstructed[key[0]] += 1
            if only_obstructed:
                continue
        result = search_key(module, key, max_nodes)
        row = serialise_row(key, result)
        row["canonical_ordinal"] = ordinal
        rows.append(row)

    per_prime = {}
    for p_value in module.PRIMES:
        assert source_fixed_obstructed[p_value] == 210
        assert source_fixed_unobstructed[p_value] == 162
        prime_rows = [row for row in rows if row["p"] == p_value]
        statuses = Counter(row["status"] for row in prime_rows)
        alternative_survivors = statuses["ALTERNATIVE_INCIDENCE_SURVIVOR"]
        per_prime[str(p_value)] = {
            "canonical_classes_total": 372,
            "source_fixed_obstructed_classes": source_fixed_obstructed[p_value],
            "source_fixed_unobstructed_classes": source_fixed_unobstructed[p_value],
            "classes_searched": len(prime_rows),
            "status_counts": dict(sorted(statuses.items())),
            "combined_unified_projection_candidate_classes": (
                source_fixed_unobstructed[p_value] + alternative_survivors
                if only_obstructed
                else statuses["SOURCE_FIXED_SURVIVOR"] + alternative_survivors
            ),
            "nodes": sum(row["nodes"] for row in prime_rows),
            "maximum_nodes_for_one_class": max(
                (row["nodes"] for row in prime_rows), default=0
            ),
            "unresolved_classes": [
                row["colouring"]
                for row in prime_rows
                if row["status"] in ("NODE_CAP_REACHED", "FINITE_DOMAIN_UNSAT")
            ],
        }

    report = {
        "schema": "unique_tail_cover_projection_incidence_search_v1",
        "scope": {
            "finite_fields": [233, 1399],
            "canonical_trace_classes_per_prime": 372,
            "search_subset": (
                "only_the_210_source_fixed_obstructed_classes"
                if only_obstructed
                else "all_372_classes"
            ),
            "endpoint_lengths": {"233": 7, "1399": 8},
            "position_universe": (
                "U of size 3, common y, and two freely selectable cover-exclusive "
                "outside pools of sizes 4+4 or 5+5"
            ),
            "included_gates": [
                "cover pair union equals L",
                "all endpoints contain y; every third endpoint meets all three cover slices",
                "all endpoints are distinct and have their prescribed U trace",
                "all existing unit-form determined length rejections",
                "all dense indicator forms with k+m*b at least 4",
                "axis-coordinate affine consistency",
                "no row-space forced-zero proper subset of any Q_E",
                "no row-space forced-zero non-cover endpoint intersection",
            ],
            "excluded": [
                "the later stronger universal identity O=L\\U that closes axial cover pairs",
                "actual a-heights or C_p^4 atomicity of Z",
                "common R partition and P_i labels",
                "new induced short blocks or Hasse rows",
                "long-complement internal subset sums",
                "complete labelled SAT or a counterexample",
            ],
            "max_nodes_per_class": max_nodes,
            "current_global_relevance": (
                "superseded for closure by the stronger universal identity "
                "O=L\\U; witnesses remain valid only in this weaker interface"
            ),
        },
        "self_test": tests,
        "dependencies": {
            "source_sha256": hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        },
        "per_prime": per_prime,
        "rows_sha256": canonical_hash(rows),
        "rows": rows,
    }
    report["status"] = (
        "ALL_SEARCHED_CLASSES_HAVE_UNIFIED_PROJECTION_LABEL_CANDIDATE_INCIDENCES"
        if all(not data["unresolved_classes"] for data in per_prime.values())
        else "EXACT_SURVIVOR_SUBCLASS_WITH_REMAINING_CLASSES_LISTED"
    )
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-nodes", type=int, default=200_000)
    parser.add_argument("--all-classes", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        print(json.dumps(self_test(load_source_module()), sort_keys=True))
        return

    report = build_report(args.max_nodes, not args.all_classes)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": report["status"],
        "per_prime": report["per_prime"],
        "rows_sha256": report["rows_sha256"],
        "certificate_sha256": report["certificate_sha256"],
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
