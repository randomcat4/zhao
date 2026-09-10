#!/usr/bin/env python3
"""Fresh no-import audit of the three p=233 relaxed mixed-trace models.

The models are rebuilt with literal position IDs and one common label table.
Every displayed Q is checked both against its elementary standard parameters
and by exhaustive enumeration of all compressed submultisets.  The latter
proves minimal zero-sum directly and does not appeal to Property B.

This checker imports no author module and reads no author report.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
import itertools
import json
from pathlib import Path


P = 233
Vec = tuple[int, int]
TAIL_IDS = frozenset({"tail:e", "tail:f", "tail:t"})


def add(*vectors: Vec) -> Vec:
    return (
        sum(vector[0] for vector in vectors) % P,
        sum(vector[1] for vector in vectors) % P,
    )


def mul(coefficient: int, vector: Vec) -> Vec:
    return (coefficient * vector[0] % P, coefficient * vector[1] % P)


def neg(vector: Vec) -> Vec:
    return mul(-1, vector)


def det(left: Vec, right: Vec) -> int:
    return (left[0] * right[1] - left[1] * right[0]) % P


E: Vec = (1, 0)
F: Vec = (0, 1)
T: Vec = neg(add(E, F))
TAIL_LABELS = {"tail:e": E, "tail:f": F, "tail:t": T}


def signed(vector: Vec) -> list[int]:
    return [coordinate if coordinate <= P // 2 else coordinate - P for coordinate in vector]


def vector_sum(position_ids: set[str] | frozenset[str], labels: dict[str, Vec]) -> Vec:
    return add(*(labels[position_id] for position_id in position_ids))


def add_clones(
    labels: dict[str, Vec], prefix: str, count: int, label: Vec
) -> frozenset[str]:
    ids = frozenset(f"{prefix}:{index:03d}" for index in range(1, count + 1))
    assert not (set(ids) & set(labels))
    labels.update({position_id: label for position_id in ids})
    return ids


@dataclass(frozen=True)
class AtomParameters:
    heavy: Vec
    affine_base: Vec


@dataclass
class LiteralModel:
    key: str
    description: str
    labels: dict[str, Vec]
    K: frozenset[str]
    L: frozenset[str]
    endpoints: dict[str, frozenset[str]]
    traces: dict[str, frozenset[str]]
    atom_parameters: dict[str, AtomParameters]
    advertised_common_non_tail: str


def compressed_counts(position_ids: set[str] | frozenset[str], labels: dict[str, Vec]) -> list[tuple[Vec, int]]:
    counter = Counter(labels[position_id] for position_id in position_ids)
    return sorted(counter.items())


def zero_submultisets(compressed: list[tuple[Vec, int]]) -> list[list[int]]:
    """Enumerate every bounded count vector and return exactly the zero sums."""
    answers: list[list[int]] = []
    for choice in itertools.product(*(range(bound + 1) for _, bound in compressed)):
        total = add(*(mul(count, label) for count, (label, _) in zip(choice, compressed)))
        if total == (0, 0):
            answers.append(list(choice))
    return answers


def proper_zero_position_subsets(
    endpoint: frozenset[str], labels: dict[str, Vec]
) -> list[list[str]]:
    ordered = sorted(endpoint)
    answers: list[list[str]] = []
    for size in range(1, len(ordered)):
        for subset in itertools.combinations(ordered, size):
            if add(*(labels[position_id] for position_id in subset)) == (0, 0):
                answers.append(list(subset))
    return answers


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def make_model_n() -> LiteralModel:
    labels: dict[str, Vec] = dict(TAIL_LABELS)
    minus_e = neg(E)
    k_f = add_clones(labels, "N:K:f", 231, F)
    k_t = add_clones(labels, "N:K:t", 231, T)
    k_minus_e = add_clones(labels, "N:K:-e", 1, minus_e)
    K = k_f | k_t | k_minus_e

    labels.update(
        {
            "N:L:x_f": F,
            "N:L:x_t": T,
            "N:L:y": E,
            "N:L:e_prime": E,
            "N:L:e_double_prime": E,
            "N:L:c": mul(-3, E),
        }
    )
    L = frozenset(TAIL_IDS | {
        "N:L:x_f",
        "N:L:x_t",
        "N:L:y",
        "N:L:e_prime",
        "N:L:e_double_prime",
        "N:L:c",
    })
    common = frozenset({
        "tail:e",
        "N:L:y",
        "N:L:e_prime",
        "N:L:e_double_prime",
        "N:L:c",
    })
    endpoints = {
        "N:H_singleton_e": common | {"N:L:x_f", "N:L:x_t"},
        "N:H_doubleton_ef": common | {"tail:f", "N:L:x_t"},
        "N:H_doubleton_et": common | {"tail:t", "N:L:x_f"},
    }
    traces = {
        "N:H_singleton_e": frozenset({"tail:e"}),
        "N:H_doubleton_ef": frozenset({"tail:e", "tail:f"}),
        "N:H_doubleton_et": frozenset({"tail:e", "tail:t"}),
    }
    parameters = {
        name: AtomParameters(heavy=F, affine_base=T) for name in endpoints
    }
    return LiteralModel(
        key="N",
        description="one singleton and two nested doubletons",
        labels=labels,
        K=K,
        L=L,
        endpoints=endpoints,
        traces=traces,
        atom_parameters=parameters,
        advertised_common_non_tail="N:L:y",
    )


def make_model_c() -> LiteralModel:
    labels: dict[str, Vec] = dict(TAIL_LABELS)
    g = T
    h = add(T, neg(E))
    special_s = add(h, mul(3, g))
    special_d = add(g, mul(2, h))
    k_g = add_clones(labels, "C:K:g", 231, g)
    k_h = add_clones(labels, "C:K:h", 231, h)
    K = k_g | k_h

    labels.update(
        {
            "C:L:x_s": special_s,
            "C:L:x_h": h,
            "C:L:x_d": special_d,
            "C:L:y": add(mul(4, E), mul(3, F)),
            "C:L:c_e_1": E,
            "C:L:c_e_2": E,
            "C:L:c_f": F,
        }
    )
    L = frozenset(TAIL_IDS | {
        "C:L:x_s",
        "C:L:x_h",
        "C:L:x_d",
        "C:L:y",
        "C:L:c_e_1",
        "C:L:c_e_2",
        "C:L:c_f",
    })
    block_s = frozenset({"tail:t", "tail:f", "C:L:x_s"})
    block_d = frozenset({"C:L:x_h", "tail:e", "C:L:x_d"})
    common = frozenset({"C:L:y", "C:L:c_e_1", "C:L:c_e_2", "C:L:c_f"})
    endpoints = {
        "C:H_singleton_e": block_d | common,
        "C:H_doubleton_ft": block_s | common,
    }
    traces = {
        "C:H_singleton_e": frozenset({"tail:e"}),
        "C:H_doubleton_ft": frozenset({"tail:f", "tail:t"}),
    }
    parameters = {
        "C:H_singleton_e": AtomParameters(heavy=g, affine_base=h),
        "C:H_doubleton_ft": AtomParameters(heavy=h, affine_base=g),
    }
    return LiteralModel(
        key="C",
        description="complementary singleton-doubleton pair",
        labels=labels,
        K=K,
        L=L,
        endpoints=endpoints,
        traces=traces,
        atom_parameters=parameters,
        advertised_common_non_tail="C:L:y",
    )


def make_model_d() -> LiteralModel:
    labels: dict[str, Vec] = dict(TAIL_LABELS)
    g = E
    h = add(mul(2, E), F)
    z = add(g, h)
    r = add(mul(5, E), F)

    k_g = add_clones(labels, "D:K:g", 229, g)
    k_h = add_clones(labels, "D:K:h", 227, h)
    K = k_g | k_h

    p13 = add_clones(labels, "D:L:P13:h", 4, h)
    labels.update(
        {
            "D:L:P23:g": g,
            "D:L:P23:h": h,
            "D:L:P23:z1": z,
            "D:L:P23:z2": z,
            "D:L:P12:g1": g,
            "D:L:P12:g2": g,
            "D:L:P12:f": F,
            "D:L:P12:r": r,
            "D:L:y": add(mul(-8, E), mul(-3, F)),
        }
    )
    p23 = frozenset({
        "D:L:P23:g", "D:L:P23:h", "D:L:P23:z1", "D:L:P23:z2"
    })
    p12 = frozenset({
        "D:L:P12:g1", "D:L:P12:g2", "D:L:P12:f", "D:L:P12:r"
    })
    L = frozenset(p13 | p23 | p12 | TAIL_IDS | {"D:L:y"})
    endpoints = {
        "D:H_doubleton_ft": p23 | {"tail:f", "tail:t", "D:L:y"},
        "D:H_doubleton_et": p13 | {"tail:e", "tail:t", "D:L:y"},
        "D:H_doubleton_ef": p12 | {"tail:e", "tail:f", "D:L:y"},
    }
    traces = {
        "D:H_doubleton_ft": frozenset({"tail:f", "tail:t"}),
        "D:H_doubleton_et": frozenset({"tail:e", "tail:t"}),
        "D:H_doubleton_ef": frozenset({"tail:e", "tail:f"}),
    }
    parameters = {
        "D:H_doubleton_ft": AtomParameters(heavy=g, affine_base=F),
        "D:H_doubleton_et": AtomParameters(heavy=g, affine_base=F),
        "D:H_doubleton_ef": AtomParameters(heavy=h, affine_base=g),
    }
    return LiteralModel(
        key="D",
        description="three doubletons",
        labels=labels,
        K=K,
        L=L,
        endpoints=endpoints,
        traces=traces,
        atom_parameters=parameters,
        advertised_common_non_tail="D:L:y",
    )


def audit_atom(
    q_positions: frozenset[str], labels: dict[str, Vec], parameters: AtomParameters
) -> dict[str, object]:
    compressed = compressed_counts(q_positions, labels)
    heavy = parameters.heavy
    base = parameters.affine_base
    assert det(heavy, base) != 0
    counts = dict(compressed)
    assert counts[heavy] == P - 1

    affine_coefficients: list[tuple[int, int]] = []
    for label, count in compressed:
        if label == heavy:
            continue
        solutions = [
            coefficient
            for coefficient in range(P)
            if add(base, mul(coefficient, heavy)) == label
        ]
        assert len(solutions) == 1
        affine_coefficients.append((solutions[0], count))
    assert sum(count for _, count in affine_coefficients) == P
    coefficient_sum = sum(coefficient * count for coefficient, count in affine_coefficients) % P
    assert coefficient_sum == 1
    assert vector_sum(q_positions, labels) == (0, 0)

    zero_vectors = zero_submultisets(compressed)
    full_vector = [count for _, count in compressed]
    assert zero_vectors == [[0] * len(compressed), full_vector]
    return {
        "size": len(q_positions),
        "sum": [0, 0],
        "heavy": signed(heavy),
        "affine_base": signed(base),
        "heavy_count": counts[heavy],
        "affine_count": P,
        "affine_coefficient_sum_mod_233": coefficient_sum,
        "compressed_multiplicities": [
            {"label": signed(label), "count": count} for label, count in compressed
        ],
        "exhaustive_compressed_zero_submultisets": zero_vectors,
        "minimal_zero_sum_directly_verified": True,
    }


def position_binding(model: LiteralModel) -> dict[str, object]:
    return {
        "labels": [[position_id, signed(model.labels[position_id])] for position_id in sorted(model.labels)],
        "K": sorted(model.K),
        "L": sorted(model.L),
        "endpoints": {
            endpoint_name: sorted(endpoint)
            for endpoint_name, endpoint in sorted(model.endpoints.items())
        },
    }


def audit_model(model: LiteralModel) -> dict[str, object]:
    assert model.K
    assert model.L
    assert model.K.isdisjoint(model.L)
    assert set(model.labels) == set(model.K | model.L)
    W = model.K | model.L
    assert len(W) == 472
    assert len(model.K) + len(model.L) == 472
    assert model.advertised_common_non_tail in model.L - TAIL_IDS
    assert all(model.labels[position_id] != (0, 0) for position_id in W)
    assert {position_id: model.labels[position_id] for position_id in TAIL_IDS} == TAIL_LABELS

    q_sets: dict[str, frozenset[str]] = {}
    endpoint_rows: dict[str, object] = {}
    atom_rows: dict[str, object] = {}
    for endpoint_name, endpoint in model.endpoints.items():
        assert endpoint <= model.L
        assert len(endpoint) == 7
        assert model.advertised_common_non_tail in endpoint
        trace = endpoint & TAIL_IDS
        assert trace == model.traces[endpoint_name]
        assert vector_sum(endpoint, model.labels) == (0, 0)

        q_positions = model.K | (model.L - endpoint)
        assert model.K.isdisjoint(model.L - endpoint)
        assert len(q_positions) == 465
        assert q_positions == W - endpoint
        q_sets[endpoint_name] = q_positions
        atom_rows[endpoint_name] = audit_atom(
            q_positions, model.labels, model.atom_parameters[endpoint_name]
        )
        zero_subsets = proper_zero_position_subsets(endpoint, model.labels)
        endpoint_rows[endpoint_name] = {
            "positions": sorted(endpoint),
            "size": len(endpoint),
            "trace_position_ids": sorted(trace),
            "sum": [0, 0],
            "Q_position_set_sha256": canonical_hash(sorted(q_positions)),
            "proper_rho_zero_subsets": zero_subsets,
            "proper_rho_zero_subset_count": len(zero_subsets),
        }

    assert set.intersection(*(set(q_set) for q_set in q_sets.values())) == set(model.K)
    assert set.union(*(set(endpoint) for endpoint in model.endpoints.values())) == set(model.L)
    common_endpoint_positions = set.intersection(
        *(set(endpoint) for endpoint in model.endpoints.values())
    )
    common_non_tail = common_endpoint_positions - TAIL_IDS
    assert model.advertised_common_non_tail in common_non_tail

    k_compressed = compressed_counts(model.K, model.labels)
    k_zero_vectors = zero_submultisets(k_compressed)
    assert k_zero_vectors == [[0] * len(k_compressed)]

    if model.key == "D":
        witness = frozenset({"D:L:P23:g", "tail:f", "tail:t"})
        assert witness < model.endpoints["D:H_doubleton_ft"]
        assert len(witness) == 3
        assert vector_sum(witness, model.labels) == (0, 0)
        assert witness in {
            frozenset(row)
            for row in endpoint_rows["D:H_doubleton_ft"]["proper_rho_zero_subsets"]
        }

    binding = position_binding(model)
    return {
        "key": model.key,
        "description": model.description,
        "W_size": len(W),
        "K_size": len(model.K),
        "L_size": len(model.L),
        "K_L_disjoint": True,
        "tail_labels": {
            position_id: signed(model.labels[position_id]) for position_id in sorted(TAIL_IDS)
        },
        "endpoint_count": len(model.endpoints),
        "common_non_tail_positions": sorted(common_non_tail),
        "K_is_exact_literal_intersection_of_all_Q": True,
        "K_compressed_multiplicities": [
            {"label": signed(label), "count": count} for label, count in k_compressed
        ],
        "K_exhaustive_compressed_zero_submultisets": k_zero_vectors,
        "K_zero_sum_free_directly_verified": True,
        "endpoints": endpoint_rows,
        "atoms": atom_rows,
        "literal_position_binding_sha256": canonical_hash(binding),
    }


def main() -> None:
    models = [audit_model(builder()) for builder in (make_model_n, make_model_c, make_model_d)]
    assert [model["key"] for model in models] == ["N", "C", "D"]
    assert [model["K_size"] for model in models] == [463, 462, 456]
    assert [model["L_size"] for model in models] == [9, 10, 16]
    assert [model["endpoint_count"] for model in models] == [3, 2, 3]

    model_d = models[2]
    d_ft = model_d["endpoints"]["D:H_doubleton_ft"]
    assert ["D:L:P23:g", "tail:f", "tail:t"] in d_ft["proper_rho_zero_subsets"]

    core = {
        "schema": "unique_tail_p233_property_b_mixed_trace_relaxed_models/independent-audit-v1",
        "method": "fresh no-import literal-position reconstruction plus exhaustive compressed atom checks",
        "p": P,
        "models": models,
        "model_D_required_short_zero_witness": {
            "endpoint": "D:H_doubleton_ft",
            "positions": ["D:L:P23:g", "tail:f", "tail:t"],
            "labels": [signed(E), signed(F), signed(T)],
            "sum": [0, 0],
            "distinct_literal_positions": True,
            "proper_subset_of_length_seven_endpoint": True,
        },
        "verified_scope": [
            "one unified literal position universe and one C_233^2 label per position",
            "W=K disjoint_union L with size 472",
            "length-seven endpoint traces, common non-tail positions, and rho(H)=0",
            "Q_H=K disjoint_union (L minus H), size 465, maximal minimal zero-sum",
            "K is the exact literal intersection of all displayed Q_H and is zero-sum-free",
        ],
        "omitted_scope": [
            "the two-position packing P and all mixed targets",
            "the q-coordinate lift and unified actual labels",
            "the complete automatically induced short-zero/core-block spectrum",
            "internal subset sums of actual long complement atoms",
            "actual heights, multiplicity cap, Hasse rows, and actual Z atom",
            "completion to every endpoint and edge of an outer survivor",
        ],
        "not_claimed": [
            "a full exact-slice model",
            "a realizable outer survivor",
            "a candidate for the actual Z atom",
            "fixed-p or global A_p satisfiability",
        ],
        "conclusion": (
            "All three N/C/D models satisfy exactly the advertised unified C_233^2 "
            "relaxation. Model D already has a proper three-position rho-zero subset "
            "inside H, so none is promoted to a complete-slice candidate."
        ),
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report = dict(core)
    report["certificate_sha256"] = sha256(canonical).hexdigest()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    destination = Path(__file__).with_name(
        "unique_tail_p233_property_b_mixed_trace_relaxed_models_independent_report.json"
    )
    destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
