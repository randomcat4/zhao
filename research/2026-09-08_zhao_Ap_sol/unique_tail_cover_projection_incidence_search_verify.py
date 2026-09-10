#!/usr/bin/env python3
"""Independent replay of the projection-incidence witness certificate.

The verifier deliberately does not import the search program or the existing
unified-projection program.  It rebuilds canonical trace classes, finite-field
row spaces, forbidden functionals, unit-form length gates, dense gates, and
all witness hashes from the report.  The older incidence constructor is used
only to identify, by an independently recomputed row-space test, the 210
source-fixed obstructed classes per prime.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import importlib.util
import json


HERE = Path(__file__).resolve().parent
SEARCH_PATH = HERE / "unique_tail_cover_projection_incidence_search.py"
SOURCE_PATH = HERE / "unique_tail_cover_forbidden_block_generalization.py"
REPORT_PATH = HERE / "unique_tail_cover_projection_incidence_search_report.json"
VERIFY_REPORT_PATH = (
    HERE / "unique_tail_cover_projection_incidence_search_verification_report.json"
)

SHAPES = {
    "P5": (5, ((0, 1), (1, 2), (2, 3), (3, 4))),
    "K1_4": (5, ((0, 1), (0, 2), (0, 3), (0, 4))),
    "T5": (5, ((0, 1), (0, 2), (0, 3), (1, 4))),
    "C4": (4, ((0, 1), (1, 2), (2, 3), (3, 0))),
    "paw": (4, ((0, 1), (1, 2), (2, 0), (0, 3))),
    "P4_plus_K2": (6, ((0, 1), (1, 2), (2, 3), (4, 5))),
    "K1_3_plus_K2": (6, ((0, 1), (0, 2), (0, 3), (4, 5))),
    "K3_plus_K2": (5, ((0, 1), (1, 2), (2, 0), (3, 4))),
    "two_P3": (6, ((0, 1), (1, 2), (3, 4), (4, 5))),
    "P3_plus_two_K2": (7, ((0, 1), (1, 2), (3, 4), (5, 6))),
    "four_K2": (8, ((0, 1), (2, 3), (4, 5), (6, 7))),
}
TRACE_MASKS = tuple(range(1, 7))
DOUBLETON_MASKS = frozenset((3, 5, 6))
PRIMES = (233, 1399)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask_from_positions(positions) -> int:
    answer = 0
    for position in positions:
        answer |= 1 << position
    return answer


def mask_row(mask: int, width: int) -> tuple[int, ...]:
    return tuple((mask >> position) & 1 for position in range(width))


def positions(mask: int, width: int) -> tuple[int, ...]:
    return tuple(position for position in range(width) if mask >> position & 1)


def proper_nonempty_submasks(mask: int):
    submask = (mask - 1) & mask
    while submask:
        yield submask
        submask = (submask - 1) & mask


def rref(rows, p_value: int):
    if not rows:
        return tuple(), tuple()
    matrix = [[entry % p_value for entry in row] for row in rows]
    pivot_row = 0
    pivots = []
    for column in range(len(matrix[0])):
        found = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, p_value)
        matrix[pivot_row] = [
            value * inverse % p_value for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    (left - factor * right) % p_value
                    for left, right in zip(matrix[row], matrix[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return (
        tuple(tuple(row) for row in matrix if any(row)),
        tuple(pivots),
    )


def rowspace_contains(vector, basis, pivots, p_value: int) -> bool:
    work = [entry % p_value for entry in vector]
    for row, pivot in zip(basis, pivots):
        factor = work[pivot]
        if factor:
            work = [
                (left - factor * right) % p_value
                for left, right in zip(work, row)
            ]
    return not any(work)


def rank(rows, p_value: int) -> int:
    return len(rref(rows, p_value)[0])


def affine_consistent(rows, rhs, p_value: int) -> bool:
    augmented = tuple(row + (value % p_value,) for row, value in zip(rows, rhs))
    return rank(rows, p_value) == rank(augmented, p_value)


def canonical_keys():
    keys = set()
    for vertex_count, edges in SHAPES.values():
        for colouring in product(TRACE_MASKS, repeat=vertex_count):
            if not all(not (colouring[left] & colouring[right]) for left, right in edges):
                continue
            cover_pairs = tuple(
                (left, right)
                for left, right in combinations(range(vertex_count), 2)
                if colouring[left] in DOUBLETON_MASKS
                and colouring[right] in DOUBLETON_MASKS
                and colouring[left] != colouring[right]
            )
            for left, right in cover_pairs:
                others = tuple(
                    sorted(
                        colouring[index]
                        for index in range(vertex_count)
                        if index not in (left, right)
                    )
                )
                for p_value in PRIMES:
                    keys.add((p_value, colouring[left], colouring[right], others))
    answer = tuple(sorted(keys))
    assert len(answer) == 744
    assert Counter(key[0] for key in answer) == {233: 372, 1399: 372}
    return answer


def template(p_value: int, left_trace: int, right_trace: int):
    length = 7 if p_value == 233 else 8
    side = length - 3
    width = 4 + 2 * side
    u_mask = 0b111
    y_mask = 1 << 3
    a_out = mask_from_positions(range(4, 4 + side))
    b_out = mask_from_positions(range(4 + side, width))
    left = left_trace | y_mask | a_out
    right = right_trace | y_mask | b_out
    full = (1 << width) - 1
    a_slice = (left_trace & ~right_trace) | a_out
    b_slice = (right_trace & ~left_trace) | b_out
    c_slice = full ^ a_slice ^ b_slice
    return {
        "p": p_value,
        "b": 4 if p_value == 233 else 5,
        "length": length,
        "side": side,
        "width": width,
        "u": u_mask,
        "y": y_mask,
        "a": a_slice,
        "bb": b_slice,
        "c": c_slice,
        "left": left,
        "right": right,
        "full": full,
    }


def projection_analysis(endpoint_masks, data):
    rows = tuple(
        mask_row(mask, data["width"])
        for mask in (*endpoint_masks, data["u"], data["full"])
    )
    basis, pivots = rref(rows, data["p"])
    rhs = (*([0] * len(endpoint_masks)), -data["b"], 1)
    axis_ok = affine_consistent(rows, rhs, data["p"])
    atomic = set()
    for endpoint in endpoint_masks:
        atomic.update(proper_nonempty_submasks(data["full"] ^ endpoint))
    intersections = set()
    cover_count = 0
    for left, right in combinations(endpoint_masks, 2):
        assert left & right
        if left | right == data["full"]:
            cover_count += 1
        else:
            intersections.add(left & right)
    forced_atomic = {
        mask
        for mask in atomic
        if rowspace_contains(mask_row(mask, data["width"]), basis, pivots, data["p"])
    }
    forced_intersections = {
        mask
        for mask in intersections
        if rowspace_contains(mask_row(mask, data["width"]), basis, pivots, data["p"])
    }
    return {
        "rank": len(basis),
        "nullity": data["width"] - len(basis),
        "axis_ok": axis_ok,
        "atomic": len(atomic),
        "intersections": len(intersections),
        "joint": len(atomic | intersections),
        "forced_atomic": forced_atomic,
        "forced_intersections": forced_intersections,
        "cover_count": cover_count,
    }


def independent_unit_gate(left: int, right: int, data) -> bool:
    q_left = data["full"] ^ left
    q_right = data["full"] ^ right
    for alpha, beta, gamma in product((-1, 0, 1), repeat=3):
        if (alpha, beta, gamma) == (0, 0, 0):
            continue
        support = 0
        indicator = True
        for position in range(data["width"]):
            coefficient = (
                alpha * bool(q_left >> position & 1)
                + beta * bool(q_right >> position & 1)
                + gamma * bool(data["u"] >> position & 1)
            )
            if coefficient not in (0, 1):
                indicator = False
                break
            if coefficient:
                support |= 1 << position
        if not indicator:
            continue
        t_value = alpha + beta - data["b"] * gamma
        if t_value == 0:
            if support:
                return False
            continue
        core = (-(t_value % data["p"])) % data["p"]
        if core > data["p"] - 4:
            continue
        total_length = core + support.bit_count()
        if total_length == 1 or 9 <= total_length <= 2 * data["p"] + 2:
            return False
        if total_length == 8 and core > 0:
            if not (core == data["b"] and support == data["u"]):
                return False
    return True


def independent_dense_gate(endpoint_masks, data) -> bool:
    count = len(endpoint_masks)
    for chosen_mask in range(1, 1 << count):
        chosen = tuple(index for index in range(count) if chosen_mask >> index & 1)
        k_value = len(chosen)
        for m_value in range(k_value + 1):
            if k_value + m_value * data["b"] < 4:
                continue
            indicator = True
            for position in range(data["width"]):
                degree = sum(
                    bool(endpoint_masks[index] >> position & 1) for index in chosen
                )
                coefficient = k_value - degree
                if data["u"] >> position & 1:
                    coefficient -= m_value
                if coefficient not in (0, 1):
                    indicator = False
                    break
            if indicator:
                return False
    return True


def load_source_module():
    spec = importlib.util.spec_from_file_location("source_constructor", SOURCE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_baseline(module, key, data):
    p_value, left_trace, right_trace, others = key
    witness = module.build_incidence_witness(
        p_value, (left_trace, right_trace, *others), (0, 1)
    )
    source_names = tuple(witness["universe_names"])
    mapping = {"u1": 0, "u2": 1, "u3": 2, "y": 3}
    a_names = [name for name in source_names if name.startswith("a")]
    b_names = [name for name in source_names if name.startswith("b")]
    for index, name in enumerate(a_names):
        mapping[name] = 4 + index
    for index, name in enumerate(b_names):
        mapping[name] = 4 + len(a_names) + index
    masks = tuple(
        mask_from_positions(mapping[source_names[position]] for position in endpoint)
        for endpoint in witness["endpoints"]
    )
    assert masks[:2] == (data["left"], data["right"])
    return masks


def verify_witness(row, key):
    p_value, left_trace, right_trace, others = key
    data = template(p_value, left_trace, right_trace)
    masks = tuple(row["endpoint_masks"])
    traces = (left_trace, right_trace, *others)
    assert len(masks) == len(traces)
    assert masks[:2] == (data["left"], data["right"])
    assert masks[0] | masks[1] == data["full"]
    assert len(set(masks)) == len(masks)
    for index, (mask, trace) in enumerate(zip(masks, traces)):
        assert mask.bit_count() == data["length"]
        assert mask & data["u"] == trace
        assert mask & data["y"]
        if index >= 2:
            assert mask & data["a"]
            assert mask & data["bb"]
            assert mask & data["c"]
    for left, right in combinations(masks, 2):
        assert independent_unit_gate(left, right, data)
    assert independent_dense_gate(masks, data)

    analysis = projection_analysis(masks, data)
    assert analysis["axis_ok"]
    assert not analysis["forced_atomic"]
    assert not analysis["forced_intersections"]
    assert analysis["joint"] < p_value * p_value
    reported = row["projection_analysis"]
    assert reported["equation_rank"] == analysis["rank"]
    assert reported["nullity"] == analysis["nullity"]
    assert reported["atomic_functionals"] == analysis["atomic"]
    assert reported["required_intersection_functionals"] == analysis["intersections"]
    assert reported["joint_forbidden_functionals"] == analysis["joint"]
    assert reported["cover_intersections"] == analysis["cover_count"]
    assert reported["forced_zero_count"] == 0
    assert reported["union_bound_numerator"] == analysis["joint"]
    assert reported["union_bound_denominator"] == p_value * p_value
    expected_hash = canonical_hash([p_value, list(traces), list(masks)])
    assert row["witness_sha256"] == expected_hash
    return analysis


def verify():
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    keys = canonical_keys()
    module = load_source_module()

    obstructed = set()
    baseline_counts = Counter()
    baseline_unobstructed_counts = Counter()
    baseline_unit_pairs = 0
    baseline_dense_rows = 0
    for key in keys:
        data = template(key[0], key[1], key[2])
        baseline = source_baseline(module, key, data)
        for left, right in combinations(baseline, 2):
            assert independent_unit_gate(left, right, data)
            baseline_unit_pairs += 1
        assert independent_dense_gate(baseline, data)
        baseline_dense_rows += sum(
            (k_value + 1)
            for k_value in range(1, len(baseline) + 1)
            for _ in combinations(range(len(baseline)), k_value)
        )
        analysis = projection_analysis(baseline, data)
        if analysis["forced_atomic"] or analysis["forced_intersections"]:
            obstructed.add(key)
            baseline_counts[key[0]] += 1
        else:
            baseline_unobstructed_counts[key[0]] += 1
    assert baseline_counts == {233: 210, 1399: 210}
    assert baseline_unobstructed_counts == {233: 162, 1399: 162}

    rows = report["rows"]
    assert canonical_hash(rows) == report["rows_sha256"]
    certificate = report.pop("certificate_sha256")
    assert canonical_hash(report) == certificate
    report["certificate_sha256"] = certificate

    report_keys = set()
    distributions = {p_value: Counter() for p_value in PRIMES}
    total_unit_pairs = 0
    total_dense_families = 0
    for row in rows:
        colouring = tuple(row["colouring"])
        key = (row["p"], colouring[0], colouring[1], colouring[2:])
        assert key in obstructed
        assert key not in report_keys
        assert row["status"] == "ALTERNATIVE_INCIDENCE_SURVIVOR"
        report_keys.add(key)
        analysis = verify_witness(row, key)
        distributions[key[0]][
            (len(colouring), analysis["rank"], analysis["nullity"])
        ] += 1
        total_unit_pairs += len(colouring) * (len(colouring) - 1) // 2
        total_dense_families += sum(
            (k_value + 1)
            for k_value in range(1, len(colouring) + 1)
            for _ in combinations(range(len(colouring)), k_value)
        )
    assert report_keys == obstructed

    assert report["dependencies"]["source_sha256"] == file_sha256(SOURCE_PATH)
    result = {
        "schema": "unique_tail_cover_projection_incidence_search_verification_v1",
        "status": "VERIFIED_ALL_420_ALTERNATIVE_INCIDENCE_WITNESSES",
        "finite_fields": list(PRIMES),
        "canonical_classes_rebuilt": len(keys),
        "source_fixed_obstructed_classes": {
            str(p_value): baseline_counts[p_value] for p_value in PRIMES
        },
        "source_fixed_unobstructed_classes": {
            str(p_value): baseline_unobstructed_counts[p_value]
            for p_value in PRIMES
        },
        "source_fixed_unit_endpoint_pairs_rechecked": baseline_unit_pairs,
        "source_fixed_dense_selected_family_m_rows_rechecked": baseline_dense_rows,
        "alternative_witnesses_verified": len(rows),
        "unit_endpoint_pairs_rechecked": total_unit_pairs,
        "dense_selected_family_m_rows_rechecked": total_dense_families,
        "per_prime_rank_nullity_distribution": {
            str(p_value): [
                {
                    "endpoint_count": key[0],
                    "equation_rank": key[1],
                    "nullity": key[2],
                    "class_count": value,
                }
                for key, value in sorted(distributions[p_value].items())
            ]
            for p_value in PRIMES
        },
        "per_prime_joint_forbidden_functional_range": {
            str(p_value): {
                "minimum": min(
                    row["projection_analysis"]["joint_forbidden_functionals"]
                    for row in rows
                    if row["p"] == p_value
                ),
                "maximum": max(
                    row["projection_analysis"]["joint_forbidden_functionals"]
                    for row in rows
                    if row["p"] == p_value
                ),
                "union_bound_denominator": p_value * p_value,
            }
            for p_value in PRIMES
        },
        "search_script_sha256": file_sha256(SEARCH_PATH),
        "source_script_sha256": file_sha256(SOURCE_PATH),
        "search_report_sha256": file_sha256(REPORT_PATH),
        "search_certificate_sha256": certificate,
        "verified_scope": (
            "real-position incidence plus exact F_p row-space obstruction and "
            "union-bound projection-label existence only; this weaker interface "
            "is superseded for closure by O=L\\U"
        ),
        "not_verified": [
            "the later stronger universal identity O=L\\U closing axial cover pairs",
            "actual height coordinate",
            "common R partition or P_i labels",
            "induced short-block and Hasse closure",
            "complete labelled SAT",
            "A_p or K(C_p^4)=2p",
        ],
    }
    result["certificate_sha256"] = canonical_hash(result)
    return result


def main():
    result = verify()
    VERIFY_REPORT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
