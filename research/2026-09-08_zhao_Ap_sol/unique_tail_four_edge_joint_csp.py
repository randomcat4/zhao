#!/usr/bin/env python3
"""Finite checks for proofs/unique_tail_four_edge_joint_csp.md.

The program classifies the four-edge endpoint graphs and their six possible
nonempty proper traces on a three-point tail.  It verifies the exact structural
dichotomy used by the proof.  It does not solve the external labelled sequence
R and therefore does not report SAT or UNSAT for the global problem.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
from math import comb
import hashlib
import json


SHAPES: dict[str, tuple[int, tuple[tuple[int, int], ...]]] = {
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

# A trace is a nonempty proper subset of U={0,1,2}.
TRACE_MASKS = tuple(range(1, 7))
SINGLETON_MASKS = frozenset((1, 2, 4))
TRACE_GRAPH_EDGES = tuple(
    (left, right)
    for left, right in combinations(TRACE_MASKS, 2)
    if not (left & right)
)

EXPECTED_SHAPE_SHA256 = (
    "5cdf95e68b0d842a90a07d06ffd42abb705a14579c4a4e6efc5cb9ec4a7c6afb"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "2f32fdd668cc854a33b499513f8a0336a67536d157a0ac1c03b29a2ce69dd051"
)


def connected_components(
    n: int, edges: tuple[tuple[int, int], ...]
) -> list[tuple[int, ...]]:
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(range(n))
    components: list[tuple[int, ...]] = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        unseen.remove(seed)
        component = []
        while stack:
            u = stack.pop()
            component.append(u)
            for v in adjacency[u]:
                if v in unseen:
                    unseen.remove(v)
                    stack.append(v)
        components.append(tuple(sorted(component)))
    return components


def component_code(
    component: tuple[int, ...], edges: tuple[tuple[int, int], ...]
) -> str:
    local_edges = {
        frozenset((component.index(u), component.index(v)))
        for u, v in edges
        if u in component and v in component
    }
    size = len(component)
    best: str | None = None
    for order in permutations(range(size)):
        bits = []
        for i in range(size):
            for j in range(i + 1, size):
                bits.append(
                    "1" if frozenset((order[i], order[j])) in local_edges else "0"
                )
        code = "".join(bits)
        if best is None or code < best:
            best = code
    assert best is not None
    return best


def graph_code(n: int, edges: tuple[tuple[int, int], ...]) -> tuple[tuple[int, str], ...]:
    components = connected_components(n, edges)
    return tuple(
        sorted((len(component), component_code(component, edges)) for component in components)
    )


def enumerate_all_four_edge_shape_codes() -> set[tuple[tuple[int, str], ...]]:
    codes: set[tuple[tuple[int, str], ...]] = set()
    for n in range(4, 9):
        possible_edges = tuple(combinations(range(n), 2))
        for edge_set in combinations(possible_edges, 4):
            used = {vertex for edge in edge_set for vertex in edge}
            if len(used) != n:
                continue
            codes.add(graph_code(n, edge_set))
    return codes


def trace_colourings(
    n: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, int, int]:
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    order = sorted(range(n), key=lambda vertex: (-len(adjacency[vertex]), vertex))
    assigned = [0] * n
    total = 0
    repeated_endpoint_trace = 0
    all_distinct_endpoint_trace = 0

    def visit(index: int) -> None:
        nonlocal total, repeated_endpoint_trace, all_distinct_endpoint_trace
        if index == n:
            traces = tuple(assigned)
            total += 1
            if len(set(traces)) < n:
                repeated_endpoint_trace += 1
            else:
                # Any four-edge subgraph of the six-vertex trace-disjointness
                # graph contains all three singleton traces.
                assert SINGLETON_MASKS.issubset(traces)
                all_distinct_endpoint_trace += 1
            return

        vertex = order[index]
        for mask in TRACE_MASKS:
            if all(
                not assigned[neighbour] or not (mask & assigned[neighbour])
                for neighbour in adjacency[vertex]
            ):
                assigned[vertex] = mask
                visit(index + 1)
                assigned[vertex] = 0

    visit(0)
    assert total == repeated_endpoint_trace + all_distinct_endpoint_trace
    return total, repeated_endpoint_trace, all_distinct_endpoint_trace


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def add(left: tuple[int, ...], right: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + b) % p for a, b in zip(left, right))


def subset_spectrum(
    values: tuple[tuple[int, ...], ...], p: int
) -> Counter[tuple[int, tuple[int, ...]]]:
    zero = (0,) * len(values[0])
    spectrum: Counter[tuple[int, tuple[int, ...]]] = Counter({(0, zero): 1})
    for value in values:
        updated = Counter(spectrum)
        for (size, total), multiplicity in spectrum.items():
            updated[(size + 1, add(total, value, p))] += multiplicity
        spectrum = updated
    return spectrum


def direct_subset_counter(
    values: tuple[tuple[int, ...], ...], p: int
) -> Counter[tuple[int, tuple[int, ...]]]:
    dimension = len(values[0])
    result: Counter[tuple[int, tuple[int, ...]]] = Counter()
    for mask in range(1 << len(values)):
        total = (0,) * dimension
        size = 0
        for index, value in enumerate(values):
            if mask >> index & 1:
                total = add(total, value, p)
                size += 1
        result[(size, total)] += 1
    return result


def profile_convolution_counter(
    x: tuple[int, ...],
    x_copies: int,
    external: tuple[tuple[int, ...], ...],
    local: tuple[tuple[int, ...], ...],
    p: int,
) -> Counter[tuple[int, tuple[int, ...]]]:
    dimension = len(x)
    external_spectrum = subset_spectrum(external, p)
    local_spectrum = subset_spectrum(local, p)
    result: Counter[tuple[int, tuple[int, ...]]] = Counter()
    core_total = (0,) * dimension
    for core_count in range(x_copies + 1):
        for (external_size, external_total), external_count in external_spectrum.items():
            for (local_size, local_total), local_count in local_spectrum.items():
                total = add(core_total, add(external_total, local_total, p), p)
                size = core_count + external_size + local_size
                result[(size, total)] += (
                    comb(x_copies, core_count) * external_count * local_count
                )
        core_total = add(core_total, x, p)
    return result


def audit_profile_convolution() -> int:
    p = 7
    dimension = 3
    checked = 0
    for seed in range(12):
        x = (1, 0, seed % p)
        external = tuple(
            (
                (seed + 2 * index + 1) % p,
                (seed * (index + 1) + 3) % p,
                (index * index + seed + 2) % p,
            )
            for index in range(5)
        )
        local = tuple(
            (
                (3 * seed + index + 1) % p,
                (2 * index + seed + 4) % p,
                (seed * index + 5) % p,
            )
            for index in range(4)
        )
        direct = direct_subset_counter((x,) * 3 + external + local, p)
        convolved = profile_convolution_counter(x, 3, external, local, p)
        assert direct == convolved
        assert sum(direct.values()) == 2 ** 12
        checked += 1
    return checked


def main() -> None:
    manual_codes = {graph_code(n, edges) for n, edges in SHAPES.values()}
    exhaustive_codes = enumerate_all_four_edge_shape_codes()
    assert len(SHAPES) == 11
    assert len(manual_codes) == 11
    assert manual_codes == exhaustive_codes
    assert len(TRACE_GRAPH_EDGES) == 6
    trace_four_edge_records = []
    for edge_set in combinations(TRACE_GRAPH_EDGES, 4):
        vertices = {mask for edge in edge_set for mask in edge}
        assert SINGLETON_MASKS.issubset(vertices)
        trace_four_edge_records.append(
            {
                "edges": [list(edge) for edge in edge_set],
                "vertices": sorted(vertices),
            }
        )
    assert len(trace_four_edge_records) == 15

    shape_records = []
    for name, (n, edges) in SHAPES.items():
        total, repeated, all_distinct = trace_colourings(n, edges)
        shape_records.append(
            {
                "name": name,
                "vertices": n,
                "trace_colourings": total,
                "repeated_endpoint_trace": repeated,
                "all_distinct_endpoint_trace": all_distinct,
            }
        )

    shape_records.sort(key=lambda row: row["name"])
    arithmetic = {
        "p233": {
            "edges": 1628,
            "outside_positions": 471,
            "congestion": (1628 + 471 - 1) // 471,
        },
        "p1399": {
            "edges": 9310,
            "outside_positions": 2803,
            "congestion": (9310 + 2803 - 1) // 2803,
        },
        "intersection_size_max": 7,
        "four_intersection_union_size_max": 25,
        "endpoint_blocks_max": 8,
        "endpoint_union_with_U_size_max": 52,
    }
    assert arithmetic["p233"]["congestion"] == 4
    assert arithmetic["p1399"]["congestion"] == 4
    assert arithmetic["four_intersection_union_size_max"] == 1 + 4 * (7 - 1)
    assert arithmetic["endpoint_union_with_U_size_max"] == 3 + 1 + 8 * 6

    branch_geometry = {
        "repeated_trace": {
            "trace_size_1_petal_size_max": 6,
            "trace_size_2_petal_size_max": 5,
            "axis_intersection_coefficient_set": [1, 2, 3],
            "axis_intersection_induced_short_length_max": 7,
        },
        "all_distinct_traces": {
            "forced_singleton_trace_blocks": 3,
            "pairwise_tail_disjoint": True,
            "pairwise_intersection_projected_nonzero": True,
            "p233_no_old_collision_block_lengths": [7, 8],
            "p1399_no_old_collision_block_lengths": [8],
            "p1399_remainder_after_y_and_tail_size": 6,
        },
    }
    external_packing = {
        "R_size_min": {233: 2 * 233 - 44, 1399: 2 * 1399 - 44},
        "C_p2_Davenport": {233: 2 * 233 - 1, 1399: 2 * 1399 - 1},
        "gap_below_Davenport": 43,
        "one_projected_zero_subset_coefficients": [1, 2, 3],
        "two_disjoint_coefficients_unordered": [[1, 1], [1, 2]],
        "three_disjoint_coefficients": [[1, 1, 1]],
        "four_disjoint_projected_zero_subsets_possible": False,
    }
    for p in (233, 1399):
        assert external_packing["R_size_min"][p] == 2 * p - 44
        assert (
            external_packing["C_p2_Davenport"][p]
            - external_packing["R_size_min"][p]
            == 43
        )
    convolution_cases = audit_profile_convolution()
    assert convolution_cases == 12

    certificate = {
        "status": "PROVED_INTERFACE/JOINT_UNSAT_NOT_ESTABLISHED/GLOBAL_INCOMPLETE",
        "shape_records": shape_records,
        "trace_four_edge_records": trace_four_edge_records,
        "arithmetic": arithmetic,
        "branch_geometry": branch_geometry,
        "external_packing": external_packing,
        "external_interface": "single_exact_group_algebra_subset_spectrum_M_R(k,g)",
        "profile_convolution_exhaustive_small_cases": convolution_cases,
    }
    shape_hash = canonical_hash(shape_records)
    certificate_hash = canonical_hash(certificate)
    if EXPECTED_SHAPE_SHA256:
        assert shape_hash == EXPECTED_SHAPE_SHA256
    if EXPECTED_CERTIFICATE_SHA256:
        assert certificate_hash == EXPECTED_CERTIFICATE_SHA256

    report = {
        "shape_count": len(shape_records),
        "trace_graph_edge_count": len(TRACE_GRAPH_EDGES),
        "trace_graph_four_edge_subgraph_count": len(trace_four_edge_records),
        "profile_convolution_exhaustive_small_cases": convolution_cases,
        "trace_colouring_count": sum(row["trace_colourings"] for row in shape_records),
        "repeated_endpoint_trace_count": sum(
            row["repeated_endpoint_trace"] for row in shape_records
        ),
        "all_distinct_endpoint_trace_count": sum(
            row["all_distinct_endpoint_trace"] for row in shape_records
        ),
        "shape_sha256": shape_hash,
        "certificate_sha256": certificate_hash,
        "status": certificate["status"],
        "shapes": shape_records,
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
