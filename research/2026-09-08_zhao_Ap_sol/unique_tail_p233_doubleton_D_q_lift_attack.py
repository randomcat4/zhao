#!/usr/bin/env python3
"""A local q-coordinate and height lift of relaxed three-doubleton Model D.

This is exact for the fixed Model-D literal positions, its rho labels, the
first-moment equations, the actual multiplicity cap, and every rho-zero subset
contained in one of the three displayed endpoints.  It deliberately does not
enumerate rho-zero subsets of the whole 474-position Y, mixed P-Q target
fibres, Hasse rows, or actual-Z atomicity.  The result is therefore RELAXED.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


P = 233
X_COUNT = P - 4
HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_p233_doubleton_D_q_lift_attack_report.json"

DEPENDENCY_SHA256 = {
    "unique_tail_p233_property_b_mixed_trace_relaxed_models.py": (
        "39b561a9adad3ea1ff554fc8140e77a1d8dda87c43270cb680f7212793cb920a"
    ),
    "unique_tail_p233_property_b_mixed_trace_relaxed_models_report.json": (
        "b362d1462eb839196df9c25c0753f50582fc52e82683392d03f089954cd8673e"
    ),
    "proofs/unique_tail_p233_property_b_mixed_trace_relaxed_models.md": (
        "7f5db5647e631e4d36d7f961d89fa7e01e765893aa5920ca73ccb2ab01722692"
    ),
}

Rho = tuple[int, int]


def add_rho(*values: Rho) -> Rho:
    return (
        sum(value[0] for value in values) % P,
        sum(value[1] for value in values) % P,
    )


def smul(coefficient: int, value: Rho) -> Rho:
    return (coefficient * value[0] % P, coefficient * value[1] % P)


def det(left: Rho, right: Rho) -> int:
    return (left[0] * right[1] - left[1] * right[0]) % P


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_dependencies() -> dict[str, str]:
    actual = {relative: file_sha256(HERE / relative) for relative in DEPENDENCY_SHA256}
    assert actual == DEPENDENCY_SHA256
    return actual


def add_positions(
    labels: dict[str, Rho], prefix: str, count: int, value: Rho
) -> set[str]:
    result = {f"{prefix}_{index:03d}" for index in range(1, count + 1)}
    for position in result:
        assert position not in labels
        labels[position] = value
    return result


def build_fixed_model() -> dict[str, object]:
    e: Rho = (1, 0)
    f: Rho = (0, 1)
    t: Rho = (-1 % P, -1 % P)
    h = add_rho(smul(2, e), f)
    z = add_rho(e, h)
    r = add_rho(smul(5, e), f)
    y = add_rho(smul(-8, e), smul(-3, f))

    rho: dict[str, Rho] = {"u_e": e, "u_f": f, "u_t": t}
    k_g = add_positions(rho, "d_k_g", 229, e)
    k_h = add_positions(rho, "d_k_h", 227, h)
    K = k_g | k_h

    p13 = add_positions(rho, "d_p13_h", 4, h)
    rho.update(
        {
            "d_p23_g": e,
            "d_p23_h": h,
            "d_p23_z1": z,
            "d_p23_z2": z,
            "d_p12_g1": e,
            "d_p12_g2": e,
            "d_p12_f": f,
            "d_p12_r": r,
            "d_y": y,
        }
    )
    p23 = {"d_p23_g", "d_p23_h", "d_p23_z1", "d_p23_z2"}
    p12 = {"d_p12_g1", "d_p12_g2", "d_p12_f", "d_p12_r"}
    U = {"u_e", "u_f", "u_t"}
    L = p13 | p23 | p12 | U | {"d_y"}
    W = K | L
    endpoints = {
        "H_doubleton_ft": p23 | {"u_f", "u_t", "d_y"},
        "H_doubleton_et": p13 | {"u_e", "u_t", "d_y"},
        "H_doubleton_ef": p12 | {"u_e", "u_f", "d_y"},
    }
    q_sets = {name: K | (L - endpoint) for name, endpoint in endpoints.items()}

    assert len(K) == 456 and len(L) == 16 and len(W) == 472
    assert set(rho) == W
    assert set.union(*endpoints.values()) == L
    assert set.intersection(*q_sets.values()) == K
    assert all(len(endpoint) == 7 for endpoint in endpoints.values())
    assert all("d_y" in endpoint for endpoint in endpoints.values())
    assert {
        name: endpoint & U for name, endpoint in endpoints.items()
    } == {
        "H_doubleton_ft": {"u_f", "u_t"},
        "H_doubleton_et": {"u_e", "u_t"},
        "H_doubleton_ef": {"u_e", "u_f"},
    }
    assert all(len(q_set) == 465 for q_set in q_sets.values())
    assert all(add_rho(*(rho[position] for position in endpoint)) == (0, 0) for endpoint in endpoints.values())

    # Recheck the three simple maximal-atom forms without importing the source
    # construction.  The returned coefficient vectors are also useful to a
    # fresh auditor.
    standards = {
        "H_doubleton_ft": (e, f),
        "H_doubleton_et": (e, f),
        "H_doubleton_ef": (h, e),
    }
    atom_rows: dict[str, object] = {}
    for name, q_set in q_sets.items():
        heavy, base = standards[name]
        assert det(heavy, base) != 0
        sequence = [rho[position] for position in sorted(q_set)]
        assert sequence.count(heavy) == P - 1
        coefficients: list[int] = []
        for value in sequence:
            if value == heavy:
                continue
            candidates = [a for a in range(P) if add_rho(base, smul(a, heavy)) == value]
            assert len(candidates) == 1
            coefficients.append(candidates[0])
        assert len(coefficients) == P
        assert sum(coefficients) % P == 1
        atom_rows[name] = {
            "heavy": list(heavy),
            "base": list(base),
            "heavy_count": P - 1,
            "line_count": P,
            "line_coefficient_sum_mod_p": 1,
        }

    return {
        "rho": rho,
        "K": K,
        "L": L,
        "W": W,
        "U": U,
        "endpoints": endpoints,
        "q_sets": q_sets,
        "atom_rows": atom_rows,
    }


def allowed_actual_sums(length: int) -> set[int]:
    result: set[int] = set()
    if 2 <= length <= 6:
        result.add(1)
    if 4 <= length <= 7:
        result.add(2)
    if 6 <= length <= 8:
        result.add(3)
    return result


def build_lift(model: dict[str, object]) -> dict[str, object]:
    rho: dict[str, Rho] = model["rho"]  # type: ignore[assignment]
    W: set[str] = model["W"]  # type: ignore[assignment]
    U: set[str] = model["U"]  # type: ignore[assignment]
    endpoints: dict[str, set[str]] = model["endpoints"]  # type: ignore[assignment]
    q_sets: dict[str, set[str]] = model["q_sets"]  # type: ignore[assignment]

    q_coordinate = {position: 0 for position in W}
    q_coordinate.update(
        {
            "u_e": -4 % P,
            "d_p23_g": 1,
            "d_y": -1 % P,
            "d_p13_h_001": 5,
            "d_p12_g1": 5,
            "d_k_g_001": -5 % P,
        }
    )

    height = {position: 0 for position in W}
    height.update(
        {
            "u_e": 3,
            "d_p23_g": 2,
            "d_y": 1,
            "d_p13_h_001": -1 % P,
            "d_p13_h_002": 1,
            "d_p13_h_003": -1 % P,
            "d_p12_g1": -1 % P,
            "d_k_h_001": -3 % P,
        }
    )

    # A compatible two-position type-(3), kappa=1 packing is included only to
    # close the first-moment equations.  Its mixed target fibre is not checked.
    packing_rho = {"p_1": (7, 11), "p_2": (-7 % P, -11 % P)}
    packing_q = {"p_1": 0, "p_2": 3}
    packing_height = {"p_1": 0, "p_2": -1 % P}
    packing = set(packing_rho)

    h_x = 0
    assert sum(q_coordinate[position] for position in U) % P == -4 % P
    assert sum(height[position] for position in U) % P == 3
    assert add_rho(*(rho[position] for position in U)) == (0, 0)

    assert sum(q_coordinate.values()) % P == 1
    assert sum(height.values()) % P == 1
    assert add_rho(*rho.values()) == (0, 0)

    assert add_rho(*packing_rho.values()) == (0, 0)
    assert sum(packing_q.values()) % P == 3
    assert sum(packing_height.values()) % P == -1 % P
    assert (sum(q_coordinate.values()) + sum(packing_q.values())) % P == 4
    assert (sum(height.values()) + sum(packing_height.values())) % P == 4 * h_x
    assert (X_COUNT + sum(q_coordinate.values()) + sum(packing_q.values())) % P == 0
    assert (
        X_COUNT * h_x + sum(height.values()) + sum(packing_height.values())
    ) % P == 0

    for name, endpoint in endpoints.items():
        assert sum(q_coordinate[position] for position in endpoint) % P == 0
        assert sum(height[position] for position in endpoint) % P == 3
        q_set = q_sets[name]
        assert sum(q_coordinate[position] for position in q_set) % P == 1
        assert sum(height[position] for position in q_set) % P == -2 % P

    actual_counter: Counter[tuple[int, int, int, int]] = Counter()
    actual_counter[(1, 0, 0, h_x)] += X_COUNT
    for position in W:
        actual_counter[(q_coordinate[position], *rho[position], height[position])] += 1
    for position in packing:
        actual_counter[(packing_q[position], *packing_rho[position], packing_height[position])] += 1
    maximum_actual_multiplicity = max(actual_counter.values())
    assert maximum_actual_multiplicity == X_COUNT == 229

    return {
        "q_coordinate": q_coordinate,
        "height": height,
        "packing_rho": packing_rho,
        "packing_q": packing_q,
        "packing_height": packing_height,
        "packing": packing,
        "h_x": h_x,
        "actual_counter": actual_counter,
        "maximum_actual_multiplicity": maximum_actual_multiplicity,
    }


def endpoint_internal_closure(
    model: dict[str, object], lift: dict[str, object]
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rho: dict[str, Rho] = model["rho"]  # type: ignore[assignment]
    endpoints: dict[str, set[str]] = model["endpoints"]  # type: ignore[assignment]
    q_coordinate: dict[str, int] = lift["q_coordinate"]  # type: ignore[assignment]
    height: dict[str, int] = lift["height"]  # type: ignore[assignment]
    h_x: int = lift["h_x"]  # type: ignore[assignment]

    rows: list[dict[str, object]] = []
    induced_short_rows: list[dict[str, object]] = []
    for endpoint_name, endpoint in endpoints.items():
        ordered = sorted(endpoint)
        for size in range(0, len(ordered) + 1):
            for subset_tuple in itertools.combinations(ordered, size):
                subset = set(subset_tuple)
                if add_rho(*(rho[position] for position in subset)) != (0, 0):
                    continue
                q_sum = sum(q_coordinate[position] for position in subset) % P
                height_sum = sum(height[position] for position in subset) % P
                x_needed = (-q_sum) % P
                x_available = x_needed <= X_COUNT
                total_length = size + x_needed if x_available else None
                actual_sum = (
                    (height_sum + x_needed * h_x) % P if x_available else None
                )

                if not subset:
                    decision = "EMPTY"
                elif not x_available:
                    decision = "NO_AVAILABLE_X_COMPLETION"
                elif total_length is not None and 1 <= total_length <= 8:
                    allowed = allowed_actual_sums(total_length)
                    assert actual_sum in allowed
                    decision = f"ALLOWED_SHORT_F{actual_sum}"
                    induced_short_rows.append(
                        {
                            "endpoint": endpoint_name,
                            "subset": sorted(subset),
                            "x_needed": x_needed,
                            "total_length": total_length,
                            "actual_sum_class": actual_sum,
                        }
                    )
                elif total_length is not None and 9 <= total_length <= 2 * P + 2:
                    raise AssertionError(
                        f"middle-gap block in {endpoint_name}: {sorted(subset)} length {total_length}"
                    )
                else:
                    decision = "OUTSIDE_LOCAL_SHORT_OR_MIDDLE_RANGE"

                rows.append(
                    {
                        "endpoint": endpoint_name,
                        "subset": sorted(subset),
                        "subset_size": size,
                        "is_full_endpoint": subset == endpoint,
                        "q_sum": q_sum,
                        "height_sum": height_sum,
                        "x_needed": x_needed,
                        "x_available": x_available,
                        "total_length": total_length,
                        "actual_sum_class": actual_sum,
                        "decision": decision,
                    }
                )

    nonempty_rows = [row for row in rows if row["subset_size"]]
    assert len(rows) == 8  # empty/full for all three endpoints, plus one proper complementary pair
    assert len(nonempty_rows) == 5
    assert Counter(row["decision"] for row in nonempty_rows) == Counter(
        {"ALLOWED_SHORT_F3": 3, "ALLOWED_SHORT_F1": 1, "NO_AVAILABLE_X_COMPLETION": 1}
    )
    assert len(induced_short_rows) == 4

    proper = [row for row in nonempty_rows if not row["is_full_endpoint"]]
    assert len(proper) == 2
    assert {(row["subset_size"], row["q_sum"], row["decision"]) for row in proper} == {
        (3, 1, "NO_AVAILABLE_X_COMPLETION"),
        (4, P - 1, "ALLOWED_SHORT_F1"),
    }
    return rows, induced_short_rows


def build_report() -> dict[str, object]:
    dependencies = verify_dependencies()
    model = build_fixed_model()
    lift = build_lift(model)
    closure_rows, induced_short_rows = endpoint_internal_closure(model, lift)

    rho: dict[str, Rho] = model["rho"]  # type: ignore[assignment]
    q_coordinate: dict[str, int] = lift["q_coordinate"]  # type: ignore[assignment]
    height: dict[str, int] = lift["height"]  # type: ignore[assignment]
    packing_rho: dict[str, Rho] = lift["packing_rho"]  # type: ignore[assignment]
    packing_q: dict[str, int] = lift["packing_q"]  # type: ignore[assignment]
    packing_height: dict[str, int] = lift["packing_height"]  # type: ignore[assignment]
    actual_counter: Counter[tuple[int, int, int, int]] = lift["actual_counter"]  # type: ignore[assignment]

    position_rows = [
        {
            "position": position,
            "part": "K" if position in model["K"] else "L",
            "rho": list(rho[position]),
            "q_coordinate": q_coordinate[position],
            "height": height[position],
        }
        for position in sorted(model["W"])
    ]
    packing_rows = [
        {
            "position": position,
            "rho": list(packing_rho[position]),
            "q_coordinate": packing_q[position],
            "height": packing_height[position],
        }
        for position in sorted(model["packing"] if "packing" in model else lift["packing"])
    ]

    report: dict[str, object] = {
        "schema": "unique_tail_p233_doubleton_D_q_lift_attack_v1",
        "status": "FIXED_MODEL_D_ENDPOINT_INTERNAL_Q_LIFT_SAT/RELAXED/GLOBAL_INCOMPLETE",
        "p": P,
        "dependencies_sha256": dependencies,
        "fixed_model": {
            "K_size": len(model["K"]),
            "L_size": len(model["L"]),
            "W_size": len(model["W"]),
            "endpoint_names": sorted(model["endpoints"]),
            "rho_atom_checks": model["atom_rows"],
        },
        "normalization": {
            "x": {"q_coordinate": 1, "rho": [0, 0], "height": lift["h_x"]},
            "a": {"q_coordinate": 0, "rho": [0, 0], "height": 1},
            "X_multiplicity": X_COUNT,
        },
        "first_moments": {
            "U": {"q_coordinate_sum": P - 4, "rho_sum": [0, 0], "height_sum": 3},
            "W": {"q_coordinate_sum": 1, "rho_sum": [0, 0], "height_sum": 1},
            "P": {"q_coordinate_sum": 3, "rho_sum": [0, 0], "height_sum": P - 1},
            "Y_equals_W_union_P": {"q_coordinate_sum": 4, "rho_sum": [0, 0], "height_sum": 0},
            "Z_equals_X_union_Y": {"q_coordinate_sum": 0, "rho_sum": [0, 0], "height_sum": 0},
            "every_H": {"q_coordinate_sum": 0, "rho_sum": [0, 0], "height_sum": 3},
            "every_Q_H": {"q_coordinate_sum": 1, "rho_sum": [0, 0], "height_sum": P - 2},
        },
        "actual_multiplicity": {
            "maximum": lift["maximum_actual_multiplicity"],
            "required_upper_bound": X_COUNT,
            "classes_at_upper_bound": [
                {"actual_label": list(label), "multiplicity": count}
                for label, count in sorted(actual_counter.items())
                if count == X_COUNT
            ],
        },
        "endpoint_internal_rho_zero_rows": closure_rows,
        "induced_allowed_short_blocks": induced_short_rows,
        "key_switch": {
            "rho_zero_triple": ["d_p23_g", "u_f", "u_t"],
            "triple_q_sum": 1,
            "x_needed_for_triple": P - 1,
            "available_X_positions": X_COUNT,
            "consequence": "the triple has no X-completion because 232>229",
            "rho_zero_four_point_complement": [
                "d_p23_h", "d_p23_z1", "d_p23_z2", "d_y"
            ],
            "complement_q_sum": P - 1,
            "x_needed_for_complement": 1,
            "induced_block_length": 5,
            "induced_actual_sum_class": 1,
        },
        "position_lift_rows": position_rows,
        "packing_rows": packing_rows,
        "strictly_checked_scope": [
            "the exact Model-D W,K,L,H,Q literal incidence and all fixed rho labels",
            "all three length-465 Q_H remain the same certified C_233^2 maximal atoms",
            "one shared q-coordinate and one shared height for every literal W position",
            "the unique-tail, W, type-(3) two-position packing, Y, and Z first-moment equations",
            "actual-label multiplicity at most p-4=229 on X disjoint_union Y",
            "every rho-zero subset contained in one displayed H, including short windows and the full middle gap",
        ],
        "relaxed_omissions": [
            "rho-zero subsets of Y that are not contained in a single displayed H",
            "all globally induced short blocks and all disjoint-short-pair constraints",
            "the proper-subset mixed target fibre between the two-position P and each Q_H",
            "Hasse rows and the four-edge/all-endpoint completion",
            "actual Z atomicity",
        ],
        "conclusion": (
            "The fixed three-doubleton Model D survives a unified local q-coordinate/height lift with the exact actual multiplicity cap and complete endpoint-internal rho-zero closure.  Hence this local layer alone does not exclude Model D; the next load-bearing attack must add global short closure or the P-Q mixed target."
        ),
        "not_claimed": [
            "the full Model-D 474-position labelled schema is SAT",
            "any one of the 720 outer shards is realizable",
            "the p=233 fixed slice is SAT",
            "the fixed p=233 problem or global A_p is solved",
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
    print("PASS fixed Model D has a unified endpoint-internal q/height lift")
    print("PASS exact first moments and actual multiplicity cap 229")
    print("PASS one induced length-5 F1 block; no endpoint-internal middle-gap block")
    print(f"CERTIFICATE {report['certificate_sha256']}")
    print("SCOPE RELAXED: global short closure, P-Q mixed target, Hasse, and Z atomicity omitted")


if __name__ == "__main__":
    main()
