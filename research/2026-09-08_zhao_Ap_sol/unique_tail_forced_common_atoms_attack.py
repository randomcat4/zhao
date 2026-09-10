#!/usr/bin/env python3
"""Finite certificate for proofs/unique_tail_forced_common_atoms_attack.md.

The script checks three things, all at the explicitly local interface used in
that note.

1. It enumerates the trace colourings of the eleven four-edge endpoint graph
   representatives and records exactly when an axial cover-pair can still have
   the only possible trace type: two distinct doubleton traces.
2. For p=233 and p=1399 it checks an explicit ten-position local endpoint
   model with five simultaneous projected complement atoms.  The model has a
   surviving doubleton/doubleton cover-pair and its induced X_1-block is an
   allowed length-five F_2 block.
3. It attaches, for each of the three strong packing types (3), (1,2), and
   (1,1,1), an explicit K=empty projected packing of the required length.

This is not a model of the full labelled A_p constraints: in particular it
does not certify every alternative atom factorisation of an endpoint
complement, all automatically generated F_3 blocks, their complements, the
full Hasse system, or actual atomicity of Z.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
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

TRACE_MASKS = tuple(range(1, 7))
SINGLETON_MASKS = frozenset((1, 2, 4))
DOUBLETON_MASKS = frozenset((3, 5, 6))
EXPECTED_TRACE_TOTALS = {
    "valid": 28584,
    "repeated": 28548,
    "all_distinct": 36,
    "forced_complete_nonaxial_trace_gate": 15072,
    "has_doubleton_cover_candidate": 13512,
    "candidate_pair_occurrences": 24468,
}
EXPECTED_CERTIFICATE_SHA256 = (
    "4eebafc1497d110e25ac82fe8825f1579fc4957ddd666a5ebd83cdf3f5a749c3"
)
EXPECTED_TRACE_TOTALS = {
    "valid": 28584,
    "repeated": 28548,
    "all_distinct": 36,
    "has_doubleton_cover_candidate": 13512,
    "forced_complete_nonaxial_trace_gate": 15072,
    "candidate_pair_occurrences": 24468,
}
EXPECTED_CERTIFICATE_SHA256 = (
    "4eebafc1497d110e25ac82fe8825f1579fc4957ddd666a5ebd83cdf3f5a749c3"
)


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def add2(left: tuple[int, int], right: tuple[int, int], p: int) -> tuple[int, int]:
    return ((left[0] + right[0]) % p, (left[1] + right[1]) % p)


def sum2(values: list[tuple[int, int]] | tuple[tuple[int, int], ...], p: int) -> tuple[int, int]:
    total = (0, 0)
    for value in values:
        total = add2(total, value, p)
    return total


def is_trace_edge(left: int, right: int) -> bool:
    return not (left & right)


def trace_colour_stats() -> dict[str, object]:
    per_shape: dict[str, dict[str, int]] = {}
    totals = Counter()
    candidate_pair_histogram = Counter()
    for name, (vertex_count, edges) in SHAPES.items():
        local = Counter()
        for colouring in product(TRACE_MASKS, repeat=vertex_count):
            if not all(is_trace_edge(colouring[u], colouring[v]) for u, v in edges):
                continue
            local["valid"] += 1
            repeated = len(set(colouring)) < vertex_count
            if repeated:
                local["repeated"] += 1
            else:
                local["all_distinct"] += 1
                assert SINGLETON_MASKS.issubset(colouring)

            candidate_pairs = sum(
                1
                for i in range(vertex_count)
                for j in range(i + 1, vertex_count)
                if colouring[i] in DOUBLETON_MASKS
                and colouring[j] in DOUBLETON_MASKS
                and colouring[i] != colouring[j]
            )
            if candidate_pairs:
                local["has_doubleton_cover_candidate"] += 1
                if repeated:
                    local["repeated_with_candidate"] += 1
                else:
                    local["all_distinct_with_candidate"] += 1
            else:
                local["forced_complete_nonaxial_trace_gate"] += 1
            local["candidate_pair_occurrences"] += candidate_pairs
            candidate_pair_histogram[candidate_pairs] += 1

        per_shape[name] = dict(sorted(local.items()))
        totals.update(local)

    assert totals["valid"] == 28584
    assert totals["repeated"] == 28548
    assert totals["all_distinct"] == 36
    for key, expected in EXPECTED_TRACE_TOTALS.items():
        assert totals[key] == expected
    return {
        "per_shape": per_shape,
        "totals": dict(sorted(totals.items())),
        "candidate_pair_histogram": {
            str(key): value for key, value in sorted(candidate_pair_histogram.items())
        },
    }


def subset_is_projected_zero(
    names: tuple[str, ...], values: dict[str, tuple[int, int]], p: int
) -> bool:
    return sum2([values[name] for name in names], p) == (0, 0)


def is_projected_atom(
    names: tuple[str, ...], values: dict[str, tuple[int, int]], p: int
) -> bool:
    if not subset_is_projected_zero(names, values, p):
        return False
    for mask in range(1, (1 << len(names)) - 1):
        subset = tuple(names[index] for index in range(len(names)) if mask >> index & 1)
        if subset_is_projected_zero(subset, values, p):
            return False
    return True


def local_endpoint_model(p: int) -> dict[str, object]:
    # U={u1,u2,u3}; y is the fixed nonaxial position shared by the four edges.
    projection = {
        "u1": (1, 0),
        "u2": (0, 1),
        "u3": (1, 1),
        "v1": (-1 % p, -2 % p),
        "v2": (-2 % p, -1 % p),
        "v3": (-1 % p, -1 % p),
        "w1": (0, 2),
        "w2": (2, 0),
        "y": (3, 4),
        "z": (-3 % p, -4 % p),
    }
    axis = {
        "u1": 0,
        "u2": 0,
        "u3": 0,
        "v1": 1,
        "v2": 1,
        "v3": 1,
        "w1": 0,
        "w2": 0,
        "y": 0,
        "z": -2 % p,
    }
    kernel = {
        "u1": 0,
        "u2": 0,
        "u3": 0,
        "v1": 1,
        "v2": 1,
        "v3": 1,
        "w1": 0,
        "w2": 0,
        "y": 0,
        "z": 1,
    }
    L = tuple(projection)
    U = frozenset(("u1", "u2", "u3"))
    q_atoms = {
        "s1": ("u2", "u3", "v1"),
        "s2": ("u1", "u3", "v2"),
        "s3": ("u1", "u2", "v3"),
        "d1": ("u1", "v1", "w1"),
        "d2": ("u2", "v2", "w2"),
    }
    trace_masks = {"s1": 1, "s2": 2, "s3": 4, "d1": 6, "d2": 5}
    endpoints = {
        name: tuple(position for position in L if position not in atom)
        for name, atom in q_atoms.items()
    }
    selected_edges = (("s1", "s2"), ("s2", "s3"), ("s1", "d1"), ("s2", "d2"))

    assert sum2(list(projection.values()), p) == (0, 0)
    assert sum(axis[name] for name in L) % p == 1
    assert sum(kernel[name] for name in L) % p == 4
    assert projection["y"] != (0, 0)

    for name, atom in q_atoms.items():
        assert is_projected_atom(atom, projection, p)
        assert sum(axis[position] for position in atom) % p == 1
        assert sum(kernel[position] for position in atom) % p == 1
        endpoint = endpoints[name]
        assert len(endpoint) == 7
        assert "y" in endpoint
        assert sum2([projection[position] for position in endpoint], p) == (0, 0)
        assert sum(axis[position] for position in endpoint) % p == 0
        assert sum(kernel[position] for position in endpoint) % p == 3
        trace = frozenset(endpoint) & U
        computed_mask = sum(1 << (int(position[1]) - 1) for position in trace)
        assert computed_mask == trace_masks[name]

    edge_intersection_sums = {}
    for left, right in selected_edges:
        assert is_trace_edge(trace_masks[left], trace_masks[right])
        intersection = tuple(sorted(set(endpoints[left]) & set(endpoints[right])))
        assert "y" in intersection
        total = sum2([projection[position] for position in intersection], p)
        assert total != (0, 0)
        edge_intersection_sums[f"{left}-{right}"] = list(total)

    left, right = "d1", "d2"
    assert set(endpoints[left]) | set(endpoints[right]) == set(L)
    cover_intersection = tuple(sorted(set(endpoints[left]) & set(endpoints[right])))
    assert set(cover_intersection) == {"u3", "v3", "y", "z"}
    assert sum2([projection[position] for position in cover_intersection], p) == (0, 0)
    assert sum(axis[position] for position in cover_intersection) % p == (-1) % p
    assert sum(kernel[position] for position in cover_intersection) % p == 2
    # X_1 plus the cover intersection has quotient sum zero and actual sum 2a.
    induced_length = 1 + len(cover_intersection)
    induced_axis = (1 + sum(axis[position] for position in cover_intersection)) % p
    induced_projection = sum2([projection[position] for position in cover_intersection], p)
    induced_kernel = sum(kernel[position] for position in cover_intersection) % p
    assert induced_length == 5
    assert induced_axis == 0
    assert induced_projection == (0, 0)
    assert induced_kernel == 2

    return {
        "p": p,
        "local_position_count": len(L),
        "endpoint_count": len(endpoints),
        "endpoint_lengths": {name: len(value) for name, value in endpoints.items()},
        "trace_masks": trace_masks,
        "selected_edges": [list(edge) for edge in selected_edges],
        "selected_edge_intersection_projection_sums": edge_intersection_sums,
        "cover_pair": [left, right],
        "cover_intersection": list(cover_intersection),
        "cover_intersection_size": len(cover_intersection),
        "induced_block": {
            "length": induced_length,
            "actual_family": "F2",
            "actual_multiple_of_a": induced_kernel,
        },
        "L_total": {"axis": 1, "projection": [0, 0], "a": 4},
        "Q_H_total": {"axis": 1, "projection": [0, 0], "a": 1},
        "H_total": {"axis": 0, "projection": [0, 0], "a": 3},
    }


def cyclic_atom(direction: tuple[int, int], length: int, p: int) -> list[tuple[int, int]]:
    assert 2 <= length <= p
    last_multiplier = (-(length - 1)) % p
    return [direction] * (length - 1) + [
        ((last_multiplier * direction[0]) % p, (last_multiplier * direction[1]) % p)
    ]


def rank_two_atom(length: int, p: int) -> list[tuple[int, int]]:
    # e1^(p-1) e2^(length-p) (e1-(length-p)e2), for p+1 <= length <= 2p-1.
    assert p + 1 <= length <= 2 * p - 1
    e2_count = length - p
    return [(1, 0)] * (p - 1) + [(0, 1)] * e2_count + [
        (1, (-e2_count) % p)
    ]


def packing_models(p: int) -> dict[str, object]:
    e1, e2 = (1, 0), (0, 1)
    packings = {
        "3": [rank_two_atom(2 * p - 2, p)],
        "1,2": [cyclic_atom(e1, p - 1, p), cyclic_atom(e2, p - 1, p)],
        "1,1,1": [
            cyclic_atom(e1, p - 1, p),
            cyclic_atom(e2, p - 2, p),
            [(0, 0)],
        ],
    }
    coefficients = {"3": [3], "1,2": [1, 2], "1,1,1": [1, 1, 1]}
    kernel_totals = {"3": [-4], "1,2": [-2, -2], "1,1,1": [-2, -1, -1]}
    result = {}
    for name, atoms in packings.items():
        assert sum(len(atom) for atom in atoms) == 2 * p - 2
        for atom in atoms:
            assert sum2(atom, p) == (0, 0)
        assert sum(coefficients[name]) == 3
        assert sum(kernel_totals[name]) == -4
        result[name] = {
            "atom_lengths": [len(atom) for atom in atoms],
            "R_length": sum(len(atom) for atom in atoms),
            "axis_coefficient_sum": sum(coefficients[name]),
            "a_coefficient_sum": sum(kernel_totals[name]),
            "K_length": 0,
            "maximum_disjoint_atom_count": len(atoms),
            "maximum_reason": (
                "one projected atom"
                if name == "3"
                else "two independent cyclic lines"
                if name == "1,2"
                else "two independent cyclic lines plus one zero singleton"
            ),
        }
    return result


def main() -> None:
    trace_stats = trace_colour_stats()
    local_models = [local_endpoint_model(p) for p in (233, 1399)]
    packings = {str(p): packing_models(p) for p in (233, 1399)}
    certificate = {
        "scope": "forced-Q local interface; not the full labelled A_p CSP",
        "trace_exchange_gate": {
            "axial_intersection_implies": "K empty and L=H union J",
            "only_surviving_trace_pair": "two distinct doubleton traces",
            "repeated_trace_axial_branch": "forbidden",
        },
        "trace_colourings": trace_stats,
        "local_models": local_models,
        "packing_models": packings,
        "status": "PROVED_EXCHANGE_GATE/LOCAL_COVER_SURVIVOR/GLOBAL_INCOMPLETE",
    }
    certificate_hash = canonical_hash(certificate)
    assert certificate_hash == EXPECTED_CERTIFICATE_SHA256
    output = {**certificate, "certificate_sha256": certificate_hash}
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
