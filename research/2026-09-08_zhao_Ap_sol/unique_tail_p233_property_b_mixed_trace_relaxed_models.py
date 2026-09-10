#!/usr/bin/env python3
r"""Certificates for unified C_233^2 mixed singleton/doubleton models.

The three witnesses keep literal positions, a common K, a common L, endpoint
sets H, the identity Q_H = K disjoint_union (L \ H), the rank-two tail
normal form, and maximal-atom standard forms.  They deliberately omit the
q-coordinate lift, P, actual heights, the full induced short spectrum, Hasse
rows, and the actual Z atom.  Consequently they are relaxed witnesses, not
instances of the full p=233 exact slice.

Reiher's external Property B theorem is not needed to prove that the displayed
standard forms are atoms.  It is the external theorem that makes these forms
the correct exhaustive domain for arbitrary maximal atoms.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path


P = 233
HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_p233_property_b_mixed_trace_relaxed_models_report.json"

Vector = tuple[int, int]


def add(*values: Vector) -> Vector:
    return (
        sum(value[0] for value in values) % P,
        sum(value[1] for value in values) % P,
    )


def neg(value: Vector) -> Vector:
    return (-value[0] % P, -value[1] % P)


def smul(coefficient: int, value: Vector) -> Vector:
    return (coefficient * value[0] % P, coefficient * value[1] % P)


def det(left: Vector, right: Vector) -> int:
    return (left[0] * right[1] - left[1] * right[0]) % P


E: Vector = (1, 0)
F: Vector = (0, 1)
T: Vector = neg(add(E, F))
TAIL_LABELS = {"u_e": E, "u_f": F, "u_t": T}


@dataclass(frozen=True)
class StandardAtom:
    heavy: Vector
    base: Vector


@dataclass
class Model:
    name: str
    labels: dict[str, Vector]
    K: set[str]
    L: set[str]
    endpoints: dict[str, set[str]]
    traces: dict[str, set[str]]
    standards: dict[str, StandardAtom]
    shared_position: str
    description: str


def positions(prefix: str, count: int, label: Vector, labels: dict[str, Vector]) -> set[str]:
    result = {f"{prefix}_{index:03d}" for index in range(1, count + 1)}
    for position in result:
        assert position not in labels
        labels[position] = label
    return result


def standard_atom_check(sequence: list[Vector], standard: StandardAtom) -> dict[str, object]:
    """Check the complete simple form and its elementary atom proof."""

    g = standard.heavy
    h = standard.base
    assert g != (0, 0) and det(g, h) != 0
    heavy_count = sequence.count(g)
    assert heavy_count == P - 1

    coefficients: list[int] = []
    for value in sequence:
        if value == g:
            continue
        candidates = [a for a in range(P) if add(h, smul(a, g)) == value]
        assert len(candidates) == 1
        coefficients.append(candidates[0])

    assert len(coefficients) == P
    assert sum(coefficients) % P == 1
    assert add(*sequence) == (0, 0)

    # Projecting modulo <g>, a zero-sum subsequence uses either zero or all p
    # affine-line terms.  In the first case fewer than p copies of g sum to
    # zero only when none is used.  In the second case the g-coordinate is
    # 1+k, so k=p-1 and the whole sequence is used.
    return {
        "length": len(sequence),
        "heavy": list(g),
        "base": list(h),
        "heavy_count": heavy_count,
        "line_count": len(coefficients),
        "line_coefficient_sum_mod_p": sum(coefficients) % P,
        "minimal_zero_sum_proof": (
            "projection modulo <g> forces 0 or p line terms; the two cases force "
            "respectively the empty subsequence or all p-1 heavy terms"
        ),
    }


def proper_zero_subsets(positions_: set[str], labels: dict[str, Vector]) -> list[list[str]]:
    ordered = sorted(positions_)
    result: list[list[str]] = []
    for size in range(1, len(ordered)):
        for subset in itertools.combinations(ordered, size):
            if add(*(labels[position] for position in subset)) == (0, 0):
                result.append(list(subset))
    return result


def validate_model(model: Model) -> dict[str, object]:
    assert model.K and model.L and model.K.isdisjoint(model.L)
    assert set(model.labels) == model.K | model.L
    assert len(model.K | model.L) == 2 * P + 6 == 472
    assert model.shared_position in model.L
    assert model.labels[model.shared_position] != (0, 0)
    for tail_position, tail_label in TAIL_LABELS.items():
        assert model.labels[tail_position] == tail_label

    atom_rows: dict[str, object] = {}
    endpoint_rows: dict[str, object] = {}
    q_sets: dict[str, set[str]] = {}
    for endpoint_name, endpoint in model.endpoints.items():
        assert endpoint <= model.L
        assert len(endpoint) == 7
        assert model.shared_position in endpoint
        actual_trace = endpoint & set(TAIL_LABELS)
        assert actual_trace == model.traces[endpoint_name]
        assert add(*(model.labels[position] for position in endpoint)) == (0, 0)

        q_set = model.K | (model.L - endpoint)
        q_sets[endpoint_name] = q_set
        assert len(q_set) == 2 * P - 1 == 465
        sequence = [model.labels[position] for position in sorted(q_set)]
        atom_rows[endpoint_name] = standard_atom_check(
            sequence, model.standards[endpoint_name]
        )
        endpoint_rows[endpoint_name] = {
            "size": len(endpoint),
            "trace": sorted(actual_trace),
            "sum": list(add(*(model.labels[position] for position in endpoint))),
            "Q_size": len(q_set),
            "Q_outside_K": len(q_set - model.K),
            "proper_rho_zero_subsets": proper_zero_subsets(endpoint, model.labels),
        }

    assert set.intersection(*q_sets.values()) == model.K
    assert set.union(*model.endpoints.values()) == model.L
    assert all(model.K < q_set for q_set in q_sets.values())
    # Since every Q is an atom and K is a proper literal subsequence of every
    # Q, K is zero-sum-free.  This is an exact implication, not a sample check.

    return {
        "name": model.name,
        "description": model.description,
        "K_size": len(model.K),
        "L_size": len(model.L),
        "universe_size": len(model.K | model.L),
        "endpoint_count": len(model.endpoints),
        "shared_position": model.shared_position,
        "shared_position_label": list(model.labels[model.shared_position]),
        "K_is_exact_full_Q_intersection": True,
        "K_zero_sum_free_reason": "K is a proper literal subsequence of each certified maximal atom Q_H",
        "endpoints": endpoint_rows,
        "atoms": atom_rows,
        "position_labels": {
            position: list(model.labels[position]) for position in sorted(model.labels)
        },
        "K_positions": sorted(model.K),
        "L_positions": sorted(model.L),
        "endpoint_positions": {
            name: sorted(value) for name, value in model.endpoints.items()
        },
    }


def nested_singleton_two_doubletons() -> Model:
    labels: dict[str, Vector] = dict(TAIL_LABELS)
    # A = f^(p-1) t^(p-1) (t+f), in standard form with base t and direction f.
    minus_e = add(T, F)
    k_f = positions("n_k_f", 231, F, labels)
    k_t = positions("n_k_t", 231, T, labels)
    k_m = positions("n_k_minus_e", 1, minus_e, labels)
    K = k_f | k_t | k_m

    labels["n_x_f"] = F
    labels["n_x_t"] = T
    labels["n_y"] = E
    labels["n_c2"] = E
    labels["n_c3"] = E
    labels["n_c4"] = smul(-3, E)
    L = set(TAIL_LABELS) | {"n_x_f", "n_x_t", "n_y", "n_c2", "n_c3", "n_c4"}
    common = {"u_e", "n_y", "n_c2", "n_c3", "n_c4"}
    endpoints = {
        "H_singleton_e": common | {"n_x_f", "n_x_t"},
        "H_doubleton_ef": common | {"u_f", "n_x_t"},
        "H_doubleton_et": common | {"u_t", "n_x_f"},
    }
    traces = {
        "H_singleton_e": {"u_e"},
        "H_doubleton_ef": {"u_e", "u_f"},
        "H_doubleton_et": {"u_e", "u_t"},
    }
    standard = StandardAtom(heavy=F, base=T)
    return Model(
        name="one_singleton_plus_two_nested_doubletons",
        labels=labels,
        K=K,
        L=L,
        endpoints=endpoints,
        traces=traces,
        standards={name: standard for name in endpoints},
        shared_position="n_y",
        description=(
            "three literally different complements carry the identical maximal atom "
            "f^(p-1) t^(p-1) (t+f); this covers one singleton-h7 and two "
            "nested doubleton-h7 traces"
        ),
    )


def complementary_singleton_doubleton() -> Model:
    labels: dict[str, Vector] = dict(TAIL_LABELS)
    g = T
    h = add(T, neg(E))
    rs = add(h, smul(3, g))
    rd = add(g, smul(2, h))
    k_g = positions("c_k_g", 231, g, labels)
    k_h = positions("c_k_h", 231, h, labels)
    K = k_g | k_h

    labels["c_x_s"] = rs
    labels["c_x_h"] = h
    labels["c_x_d"] = rd
    labels["c_y"] = add(smul(4, E), smul(3, F))
    labels["c_c2"] = E
    labels["c_c3"] = E
    labels["c_c4"] = F
    L = set(TAIL_LABELS) | {
        "c_x_s", "c_x_h", "c_x_d", "c_y", "c_c2", "c_c3", "c_c4"
    }
    b_singleton = {"u_t", "u_f", "c_x_s"}
    b_doubleton = {"c_x_h", "u_e", "c_x_d"}
    common = {"c_y", "c_c2", "c_c3", "c_c4"}
    endpoints = {
        "H_singleton_e": b_doubleton | common,
        "H_complementary_doubleton_ft": b_singleton | common,
    }
    traces = {
        "H_singleton_e": {"u_e"},
        "H_complementary_doubleton_ft": {"u_f", "u_t"},
    }
    return Model(
        name="singleton_plus_complementary_doubleton",
        labels=labels,
        K=K,
        L=L,
        endpoints=endpoints,
        traces=traces,
        standards={
            "H_singleton_e": StandardAtom(heavy=g, base=h),
            "H_complementary_doubleton_ft": StandardAtom(heavy=h, base=g),
        },
        shared_position="c_y",
        description=(
            "the complementary trace pair is realized by two distinct Property-B "
            "standard atoms sharing 462 literal positions"
        ),
    )


def three_doubletons() -> Model:
    labels: dict[str, Vector] = dict(TAIL_LABELS)
    g = E
    h = add(smul(2, E), F)
    z = add(g, h)
    r = add(F, smul(5, E))

    k_g = positions("d_k_g", 229, g, labels)
    k_h = positions("d_k_h", 227, h, labels)
    K = k_g | k_h

    p13 = positions("d_p13_h", 4, h, labels)
    labels["d_p23_g"] = g
    labels["d_p23_h"] = h
    labels["d_p23_z1"] = z
    labels["d_p23_z2"] = z
    p23 = {"d_p23_g", "d_p23_h", "d_p23_z1", "d_p23_z2"}
    labels["d_p12_g1"] = g
    labels["d_p12_g2"] = g
    labels["d_p12_f"] = F
    labels["d_p12_r"] = r
    p12 = {"d_p12_g1", "d_p12_g2", "d_p12_f", "d_p12_r"}
    labels["d_y"] = add(smul(-8, E), smul(-3, F))
    L = p13 | p23 | p12 | set(TAIL_LABELS) | {"d_y"}

    endpoints = {
        "H_doubleton_ft": p23 | {"u_f", "u_t", "d_y"},
        "H_doubleton_et": p13 | {"u_e", "u_t", "d_y"},
        "H_doubleton_ef": p12 | {"u_e", "u_f", "d_y"},
    }
    traces = {
        "H_doubleton_ft": {"u_f", "u_t"},
        "H_doubleton_et": {"u_e", "u_t"},
        "H_doubleton_ef": {"u_e", "u_f"},
    }
    return Model(
        name="three_doubletons",
        labels=labels,
        K=K,
        L=L,
        endpoints=endpoints,
        traces=traces,
        standards={
            "H_doubleton_ft": StandardAtom(heavy=g, base=F),
            "H_doubleton_et": StandardAtom(heavy=g, base=F),
            "H_doubleton_ef": StandardAtom(heavy=h, base=g),
        },
        shared_position="d_y",
        description=(
            "all three doubleton-h7 traces coexist with exact literal incidence; "
            "two atoms have heavy label e and the third has heavy label 2e+f"
        ),
    )


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def build_report() -> dict[str, object]:
    models = [
        validate_model(nested_singleton_two_doubletons()),
        validate_model(complementary_singleton_doubleton()),
        validate_model(three_doubletons()),
    ]
    assert [row["K_size"] for row in models] == [463, 462, 456]
    assert [row["L_size"] for row in models] == [9, 10, 16]
    assert [row["endpoint_count"] for row in models] == [3, 2, 3]

    report: dict[str, object] = {
        "schema": "unique_tail_p233_property_b_mixed_trace_relaxed_models_v1",
        "p": P,
        "tail_normal_form": {name: list(value) for name, value in TAIL_LABELS.items()},
        "status": "UNIFIED_C2332_RELAXED_SAT/PROPERTY_B_LAYER_INSUFFICIENT/GLOBAL_INCOMPLETE",
        "models": models,
        "strictly_verified_interfaces": [
            "one common 472-position universe W=K disjoint_union L",
            "one unified C_233^2 label per literal position",
            "three tail positions labelled e,f,-e-f",
            "every endpoint has length seven, the declared singleton/doubleton trace, rho-sum zero, and a common non-tail position",
            "every Q_H is literally K disjoint_union (L minus H), has length 465, and is a certified maximal atom",
            "K is the exact full intersection of the displayed Q_H and is zero-sum-free",
        ],
        "omitted_exact_slice_interfaces": [
            "the two-position packing P and its mixed P-Q targets",
            "the q-coordinate lift from C_233^2 to the unified quotient and actual labels",
            "all automatically induced short zero/core blocks outside the displayed Q_H",
            "actual heights and the multiplicity cap",
            "all Hasse congruence rows",
            "the actual long atom Z",
            "completion to all endpoints and all four edges of any one of the 720 outer survivors",
        ],
        "external_property_b_dependency": {
            "author": "Christian Reiher",
            "title": "A Proof of the Theorem According to Which Every Prime Number Possesses Property B",
            "result_used_for_exhaustive_interpretation": "every length 2p-1 minimal zero-sum sequence over C_p^2 is simple",
            "url": "https://www.math.uni-rostock.de/math/pub/preprints/preprint/2010/pre10_01.pdf",
            "role": (
                "not needed for validity of the displayed witnesses; needed only when treating simple standard forms as the exhaustive domain of arbitrary maximal atoms"
            ),
        },
        "conclusion": (
            "Property B, fixed tail labels, a common zero-sum-free K, unified literal incidence, and maximality of all displayed Q_H do not exclude one singleton with nested or complementary doubletons, nor three doubletons.  Any further strict exclusion must use at least one omitted exact-slice interface."
        ),
        "not_claimed": [
            "any model satisfies the full p=233 exact schema",
            "any of the 720 outer shards is realizable",
            "the mixed 7/8 slice is SAT",
            "the fixed p=233 problem is solved",
            "global A_p",
        ],
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("PASS unified literal C_233^2 relaxed models: nested, complementary, three-doubleton")
    print("PASS K sizes: 463, 462, 456; all displayed Q_H are length-465 atoms")
    print(f"CERTIFICATE {report['certificate_sha256']}")
    print("SCOPE RELAXED: q-lifts, P-mixed targets, full short closure, heights, Hasse, and Z remain omitted")


if __name__ == "__main__":
    main()
