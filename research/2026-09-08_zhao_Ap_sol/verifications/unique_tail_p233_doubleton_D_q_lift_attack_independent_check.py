#!/usr/bin/env python3
"""Fresh reconstruction of the fixed Model-D endpoint-internal lift.

This checker imports no author module and does not execute the author script.
It rebuilds all literal positions from the displayed construction, verifies
the claimed local mathematics, and only then compares its reconstruction with
the frozen author report.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


P = 233
X_COUNT = 229
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPORT_PATH = HERE / "unique_tail_p233_doubleton_D_q_lift_attack_independent_report.json"
AUTHOR_REPORT_PATH = BASE / "unique_tail_p233_doubleton_D_q_lift_attack_report.json"

AUTHOR_BINDINGS = {
    "proofs/unique_tail_p233_doubleton_D_q_lift_attack.md":
        "a6413cbccf122e2f040f428e3569018f35f6942eafbbc9f80c776430e5f9114d",
    "unique_tail_p233_doubleton_D_q_lift_attack.py":
        "19e6d555a5424780fc3ab176e2e0d1318e1907d2142c587d422d412b5be0885c",
    "unique_tail_p233_doubleton_D_q_lift_attack_report.json":
        "ba15376e50590abe95620ffe3568f0ec2b1eb5a964ae934b82d47e38f7a3b58c",
}

Vec = tuple[int, int]


def vec_sum(values: list[Vec]) -> Vec:
    return (
        sum(value[0] for value in values) % P,
        sum(value[1] for value in values) % P,
    )


def add(left: Vec, right: Vec) -> Vec:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def scale(coefficient: int, value: Vec) -> Vec:
    return ((coefficient * value[0]) % P, (coefficient * value[1]) % P)


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return sha256(payload).hexdigest()


def file_hash(relative: str) -> str:
    return sha256((BASE / relative).read_bytes()).hexdigest()


def build_positions() -> tuple[
    dict[str, dict[str, object]],
    dict[str, set[str]],
    dict[str, set[str]],
    dict[str, dict[str, object]],
]:
    """Construct Model D from the proof's cell table, not from author code."""

    e = (1, 0)
    f = (0, 1)
    t = (P - 1, P - 1)
    h = (2, 1)
    z = (3, 1)
    r = (5, 1)
    y = (P - 8, P - 3)

    records: dict[str, dict[str, object]] = {}

    def insert(name: str, part: str, rho: Vec) -> None:
        assert name not in records
        records[name] = {
            "part": part,
            "rho": rho,
            "q_coordinate": 0,
            "height": 0,
        }

    for index in range(1, 230):
        insert(f"d_k_g_{index:03d}", "K", e)
    for index in range(1, 228):
        insert(f"d_k_h_{index:03d}", "K", h)
    for index in range(1, 5):
        insert(f"d_p13_h_{index:03d}", "L", h)

    for name, value in [
        ("d_p23_g", e),
        ("d_p23_h", h),
        ("d_p23_z1", z),
        ("d_p23_z2", z),
        ("d_p12_g1", e),
        ("d_p12_g2", e),
        ("d_p12_f", f),
        ("d_p12_r", r),
        ("u_e", e),
        ("u_f", f),
        ("u_t", t),
        ("d_y", y),
    ]:
        insert(name, "L", value)

    for name, value in {
        "u_e": -4,
        "d_p23_g": 1,
        "d_y": -1,
        "d_p13_h_001": 5,
        "d_p12_g1": 5,
        "d_k_g_001": -5,
    }.items():
        records[name]["q_coordinate"] = value % P

    for name, value in {
        "u_e": 3,
        "d_p23_g": 2,
        "d_y": 1,
        "d_p13_h_001": -1,
        "d_p13_h_002": 1,
        "d_p13_h_003": -1,
        "d_p12_g1": -1,
        "d_k_h_001": -3,
    }.items():
        records[name]["height"] = value % P

    K = {name for name, row in records.items() if row["part"] == "K"}
    p13 = {f"d_p13_h_{index:03d}" for index in range(1, 5)}
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
    q_sets = {
        endpoint_name: W - endpoint
        for endpoint_name, endpoint in endpoints.items()
    }
    groups = {"K": K, "L": L, "W": W, "U": U}

    packing = {
        "p_1": {
            "rho": (7, 11),
            "q_coordinate": 0,
            "height": 0,
        },
        "p_2": {
            "rho": (P - 7, P - 11),
            "q_coordinate": 3,
            "height": P - 1,
        },
    }

    assert len(records) == len(W) == 472
    assert len(K) == 456 and len(L) == 16
    assert set().union(*endpoints.values()) == L
    assert set.intersection(*q_sets.values()) == K
    assert all(len(endpoint) == 7 for endpoint in endpoints.values())
    assert all(len(q_set) == 465 for q_set in q_sets.values())
    assert {name: endpoint & U for name, endpoint in endpoints.items()} == {
        "H_doubleton_ft": {"u_f", "u_t"},
        "H_doubleton_et": {"u_e", "u_t"},
        "H_doubleton_ef": {"u_e", "u_f"},
    }
    return records, groups, endpoints, q_sets, packing


def group_sum(
    names: set[str], records: dict[str, dict[str, object]]
) -> dict[str, object]:
    return {
        "size": len(names),
        "q_coordinate_sum": sum(
            int(records[name]["q_coordinate"]) for name in names
        ) % P,
        "rho_sum": list(
            vec_sum([records[name]["rho"] for name in names])  # type: ignore[list-item]
        ),
        "height_sum": sum(int(records[name]["height"]) for name in names) % P,
    }


def packing_sum(packing: dict[str, dict[str, object]]) -> dict[str, object]:
    return {
        "size": len(packing),
        "q_coordinate_sum": sum(
            int(row["q_coordinate"]) for row in packing.values()
        ) % P,
        "rho_sum": list(
            vec_sum([row["rho"] for row in packing.values()])  # type: ignore[list-item]
        ),
        "height_sum": sum(int(row["height"]) for row in packing.values()) % P,
    }


def solve_line_coefficient(value: Vec, base: Vec, heavy: Vec) -> int:
    difference = ((value[0] - base[0]) % P, (value[1] - base[1]) % P)
    if heavy[0]:
        coefficient = difference[0] * pow(heavy[0], -1, P) % P
    else:
        assert heavy[1]
        coefficient = difference[1] * pow(heavy[1], -1, P) % P
    assert add(base, scale(coefficient, heavy)) == value
    return coefficient


def verify_maximal_atoms(
    records: dict[str, dict[str, object]], q_sets: dict[str, set[str]]
) -> dict[str, object]:
    e, f, h = (1, 0), (0, 1), (2, 1)
    standards = {
        "H_doubleton_ft": (e, f),
        "H_doubleton_et": (e, f),
        "H_doubleton_ef": (h, e),
    }
    expected_histograms = {
        "H_doubleton_ft": {0: 1, 2: 231, 5: 1},
        "H_doubleton_et": {0: 2, 2: 228, 3: 2, 5: 1},
        "H_doubleton_ef": {0: 230, 1: 2, P - 1: 1},
    }
    result: dict[str, object] = {}
    for endpoint_name, q_set in q_sets.items():
        heavy, base = standards[endpoint_name]
        rho_sequence = [records[name]["rho"] for name in sorted(q_set)]
        heavy_count = rho_sequence.count(heavy)
        assert heavy_count == P - 1
        coefficients = [
            solve_line_coefficient(value, base, heavy)  # type: ignore[arg-type]
            for value in rho_sequence
            if value != heavy
        ]
        histogram = Counter(coefficients)
        assert len(coefficients) == P
        assert dict(sorted(histogram.items())) == expected_histograms[endpoint_name]
        assert sum(coefficients) % P == 1
        assert vec_sum(rho_sequence) == (0, 0)  # type: ignore[arg-type]

        # Direct simple-atom argument: a zero-sum subsequence has either zero
        # or p affine-line terms.  The first case forces zero heavy terms; the
        # second uses every line term and then forces p-1 heavy terms.
        line_term_count_options = [0, P]
        forced_heavy_counts = [0, P - 1]
        result[endpoint_name] = {
            "length": len(q_set),
            "heavy": list(heavy),
            "base": list(base),
            "heavy_count": heavy_count,
            "line_count": len(coefficients),
            "coefficient_histogram": {
                str(key): histogram[key] for key in sorted(histogram)
            },
            "coefficient_sum_mod_p": sum(coefficients) % P,
            "zero_subsequence_line_term_options": line_term_count_options,
            "corresponding_forced_heavy_counts": forced_heavy_counts,
            "atomicity_conclusion": "only empty and full zero-sum subsequences",
        }
    return result


def allowed_sum_classes(length: int) -> set[int]:
    windows = {1: range(2, 7), 2: range(4, 8), 3: range(6, 9)}
    return {
        sum_class
        for sum_class, allowed_lengths in windows.items()
        if length in allowed_lengths
    }


def enumerate_endpoint_subsets(
    records: dict[str, dict[str, object]],
    endpoints: dict[str, set[str]],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    zero_rows: list[dict[str, object]] = []
    total_scanned = 0
    middle_violations: list[dict[str, object]] = []
    short_violations: list[dict[str, object]] = []

    for endpoint_name, endpoint in endpoints.items():
        ordered = sorted(endpoint)
        for mask in range(1 << len(ordered)):
            total_scanned += 1
            subset = [
                ordered[index]
                for index in range(len(ordered))
                if mask & (1 << index)
            ]
            rho_sum = vec_sum(
                [records[name]["rho"] for name in subset]  # type: ignore[list-item]
            )
            if rho_sum != (0, 0):
                continue
            q_sum = sum(int(records[name]["q_coordinate"]) for name in subset) % P
            height_sum = sum(int(records[name]["height"]) for name in subset) % P
            x_needed = (-q_sum) % P
            available = x_needed <= X_COUNT
            total_length = len(subset) + x_needed if available else None
            actual_sum = height_sum if available else None

            if not subset:
                decision = "EMPTY"
            elif not available:
                decision = "NO_AVAILABLE_X_COMPLETION"
            elif total_length is not None and total_length <= 8:
                if actual_sum not in allowed_sum_classes(total_length):
                    short_violations.append(
                        {
                            "endpoint": endpoint_name,
                            "subset": subset,
                            "length": total_length,
                            "actual_sum": actual_sum,
                        }
                    )
                decision = f"ALLOWED_SHORT_F{actual_sum}"
            elif total_length is not None and 9 <= total_length <= 2 * P + 2:
                decision = "FORBIDDEN_MIDDLE_BLOCK"
                middle_violations.append(
                    {
                        "endpoint": endpoint_name,
                        "subset": subset,
                        "length": total_length,
                    }
                )
            else:
                decision = "OUTSIDE_CHECKED_LENGTH_RANGE"

            zero_rows.append(
                {
                    "endpoint": endpoint_name,
                    "subset": subset,
                    "subset_size": len(subset),
                    "is_full_endpoint": set(subset) == endpoint,
                    "q_sum": q_sum,
                    "height_sum": height_sum,
                    "x_needed": x_needed,
                    "x_available": available,
                    "total_length": total_length,
                    "actual_sum_class": actual_sum,
                    "decision": decision,
                }
            )

    assert total_scanned == 3 * (1 << 7) == 384
    assert not short_violations
    assert not middle_violations
    assert len(zero_rows) == 8
    nonempty = [row for row in zero_rows if row["subset_size"]]
    assert len(nonempty) == 5
    assert Counter(row["decision"] for row in nonempty) == Counter(
        {
            "ALLOWED_SHORT_F3": 3,
            "ALLOWED_SHORT_F1": 1,
            "NO_AVAILABLE_X_COMPLETION": 1,
        }
    )
    proper = [row for row in nonempty if not row["is_full_endpoint"]]
    assert {
        (
            tuple(row["subset"]),
            row["q_sum"],
            row["height_sum"],
            row["x_needed"],
            row["total_length"],
            row["decision"],
        )
        for row in proper
    } == {
        (
            ("d_p23_g", "u_f", "u_t"),
            1,
            2,
            232,
            None,
            "NO_AVAILABLE_X_COMPLETION",
        ),
        (
            ("d_p23_h", "d_p23_z1", "d_p23_z2", "d_y"),
            232,
            1,
            1,
            5,
            "ALLOWED_SHORT_F1",
        ),
    }
    summary = {
        "literal_subsets_scanned": total_scanned,
        "rho_zero_subset_occurrences": len(zero_rows),
        "nonempty_rho_zero_subset_occurrences": len(nonempty),
        "proper_nonempty_rho_zero_subset_occurrences": len(proper),
        "allowed_short_blocks": Counter(
            row["decision"]
            for row in nonempty
            if str(row["decision"]).startswith("ALLOWED_SHORT")
        ),
        "no_available_X_completion": sum(
            row["decision"] == "NO_AVAILABLE_X_COMPLETION" for row in nonempty
        ),
        "short_window_violations": len(short_violations),
        "middle_gap_violations": len(middle_violations),
    }
    summary["allowed_short_blocks"] = dict(
        sorted(summary["allowed_short_blocks"].items())  # type: ignore[union-attr]
    )
    return zero_rows, summary


def actual_multiplicities(
    records: dict[str, dict[str, object]],
    packing: dict[str, dict[str, object]],
) -> dict[str, object]:
    counter: Counter[tuple[int, int, int, int]] = Counter()
    counter[(1, 0, 0, 0)] = X_COUNT
    for row in records.values():
        rho = row["rho"]
        counter[
            (
                int(row["q_coordinate"]),
                rho[0],  # type: ignore[index]
                rho[1],  # type: ignore[index]
                int(row["height"]),
            )
        ] += 1
    for row in packing.values():
        rho = row["rho"]
        counter[
            (
                int(row["q_coordinate"]),
                rho[0],  # type: ignore[index]
                rho[1],  # type: ignore[index]
                int(row["height"]),
            )
        ] += 1

    maximum = max(counter.values())
    cap_classes = [
        {"actual_label": list(label), "multiplicity": count}
        for label, count in sorted(counter.items())
        if count == maximum
    ]
    assert maximum == X_COUNT
    assert cap_classes == [
        {"actual_label": [0, 1, 0, 0], "multiplicity": 229},
        {"actual_label": [1, 0, 0, 0], "multiplicity": 229},
    ]
    distribution = Counter(counter.values())
    return {
        "positions_counted": X_COUNT + len(records) + len(packing),
        "distinct_actual_labels": len(counter),
        "maximum": maximum,
        "required_upper_bound": X_COUNT,
        "classes_at_upper_bound": cap_classes,
        "multiplicity_value_distribution": {
            str(key): distribution[key] for key in sorted(distribution)
        },
    }


def compare_author_report(
    author: dict[str, object],
    records: dict[str, dict[str, object]],
    packing: dict[str, dict[str, object]],
    atom_rows: dict[str, object],
    first_moments: dict[str, object],
    zero_rows: list[dict[str, object]],
    multiplicity: dict[str, object],
) -> dict[str, object]:
    assert author["schema"] == "unique_tail_p233_doubleton_D_q_lift_attack_v1"
    assert author["status"] == (
        "FIXED_MODEL_D_ENDPOINT_INTERNAL_Q_LIFT_SAT/RELAXED/GLOBAL_INCOMPLETE"
    )
    assert author["p"] == P

    fixed_model = author["fixed_model"]
    assert fixed_model["K_size"] == 456  # type: ignore[index]
    assert fixed_model["L_size"] == 16  # type: ignore[index]
    assert fixed_model["W_size"] == 472  # type: ignore[index]
    for name, row in atom_rows.items():
        author_atom = fixed_model["rho_atom_checks"][name]  # type: ignore[index]
        assert author_atom == {
            "heavy": row["heavy"],
            "base": row["base"],
            "heavy_count": row["heavy_count"],
            "line_count": row["line_count"],
            "line_coefficient_sum_mod_p": row["coefficient_sum_mod_p"],
        }

    author_moments = author["first_moments"]
    author_to_independent = {
        "U": "U",
        "W": "W",
        "P": "P",
        "Y_equals_W_union_P": "Y",
        "Z_equals_X_union_Y": "Z",
    }
    for author_name, independent_name in author_to_independent.items():
        row = first_moments[independent_name]
        assert author_moments[author_name] == {  # type: ignore[index]
            "q_coordinate_sum": row["q_coordinate_sum"],
            "rho_sum": row["rho_sum"],
            "height_sum": row["height_sum"],
        }
    for endpoint_name in [
        "H_doubleton_ft",
        "H_doubleton_et",
        "H_doubleton_ef",
    ]:
        for author_name, prefix in [
            ("every_H", "H:"),
            ("every_Q_H", "Q:"),
        ]:
            row = first_moments[prefix + endpoint_name]
            assert author_moments[author_name] == {  # type: ignore[index]
                "q_coordinate_sum": row["q_coordinate_sum"],
                "rho_sum": row["rho_sum"],
                "height_sum": row["height_sum"],
            }

    expected_position_rows = [
        {
            "position": name,
            "part": row["part"],
            "rho": list(row["rho"]),
            "q_coordinate": row["q_coordinate"],
            "height": row["height"],
        }
        for name, row in sorted(records.items())
    ]
    assert author["position_lift_rows"] == expected_position_rows
    expected_packing_rows = [
        {
            "position": name,
            "rho": list(row["rho"]),
            "q_coordinate": row["q_coordinate"],
            "height": row["height"],
        }
        for name, row in sorted(packing.items())
    ]
    assert author["packing_rows"] == expected_packing_rows

    def row_map(rows: list[dict[str, object]]) -> dict[tuple[object, ...], dict[str, object]]:
        return {
            (row["endpoint"], tuple(row["subset"])): row
            for row in rows
        }

    assert row_map(author["endpoint_internal_rho_zero_rows"]) == row_map(zero_rows)  # type: ignore[arg-type]
    assert author["actual_multiplicity"] == {
        "maximum": multiplicity["maximum"],
        "required_upper_bound": multiplicity["required_upper_bound"],
        "classes_at_upper_bound": multiplicity["classes_at_upper_bound"],
    }
    return {
        "full_position_table_match": True,
        "packing_table_match": True,
        "first_moment_table_match": True,
        "rho_atom_summary_match": True,
        "endpoint_zero_subset_rows_match": True,
        "actual_cap_summary_match": True,
    }


def main() -> None:
    actual_bindings = {relative: file_hash(relative) for relative in AUTHOR_BINDINGS}
    assert actual_bindings == AUTHOR_BINDINGS

    author_report = json.loads(AUTHOR_REPORT_PATH.read_text(encoding="utf-8"))
    author_certificate = author_report.pop("certificate_sha256")
    assert canonical_hash(author_report) == author_certificate

    records, groups, endpoints, q_sets, packing = build_positions()
    atom_rows = verify_maximal_atoms(records, q_sets)

    first_moments: dict[str, object] = {
        "U": group_sum(groups["U"], records),
        "W": group_sum(groups["W"], records),
        "P": packing_sum(packing),
    }
    first_moments["Y"] = {
        "size": 474,
        "q_coordinate_sum": (
            first_moments["W"]["q_coordinate_sum"]
            + first_moments["P"]["q_coordinate_sum"]
        ) % P,
        "rho_sum": list(
            add(
                tuple(first_moments["W"]["rho_sum"]),  # type: ignore[arg-type]
                tuple(first_moments["P"]["rho_sum"]),  # type: ignore[arg-type]
            )
        ),
        "height_sum": (
            first_moments["W"]["height_sum"]
            + first_moments["P"]["height_sum"]
        ) % P,
    }
    first_moments["Z"] = {
        "size": X_COUNT + first_moments["Y"]["size"],
        "q_coordinate_sum": (
            X_COUNT + first_moments["Y"]["q_coordinate_sum"]
        ) % P,
        "rho_sum": first_moments["Y"]["rho_sum"],
        "height_sum": first_moments["Y"]["height_sum"],
    }
    for name, endpoint in endpoints.items():
        first_moments["H:" + name] = group_sum(endpoint, records)
        first_moments["Q:" + name] = group_sum(q_sets[name], records)

    assert first_moments["U"] == {
        "size": 3, "q_coordinate_sum": 229, "rho_sum": [0, 0], "height_sum": 3
    }
    assert first_moments["W"] == {
        "size": 472, "q_coordinate_sum": 1, "rho_sum": [0, 0], "height_sum": 1
    }
    assert first_moments["P"] == {
        "size": 2, "q_coordinate_sum": 3, "rho_sum": [0, 0], "height_sum": 232
    }
    assert first_moments["Y"] == {
        "size": 474, "q_coordinate_sum": 4, "rho_sum": [0, 0], "height_sum": 0
    }
    assert first_moments["Z"] == {
        "size": 703, "q_coordinate_sum": 0, "rho_sum": [0, 0], "height_sum": 0
    }
    for name in endpoints:
        assert first_moments["H:" + name] == {
            "size": 7, "q_coordinate_sum": 0, "rho_sum": [0, 0], "height_sum": 3
        }
        assert first_moments["Q:" + name] == {
            "size": 465, "q_coordinate_sum": 1, "rho_sum": [0, 0], "height_sum": 231
        }

    assert packing["p_1"]["rho"] != (0, 0)
    assert add(packing["p_1"]["rho"], packing["p_2"]["rho"]) == (0, 0)  # type: ignore[arg-type]

    multiplicity = actual_multiplicities(records, packing)
    zero_rows, endpoint_summary = enumerate_endpoint_subsets(records, endpoints)

    # Two explicit probes outside the endpoint-internal closure quantify the
    # omission without pretending to enumerate the whole Y power set.
    U = groups["U"]
    U_q = sum(int(records[name]["q_coordinate"]) for name in U) % P
    U_height = sum(int(records[name]["height"]) for name in U) % P
    U_x_needed = (-U_q) % P
    assert (U_x_needed, len(U) + U_x_needed, U_height) == (4, 7, 3)
    assert 3 in allowed_sum_classes(7)
    P_q = sum(int(row["q_coordinate"]) for row in packing.values()) % P
    P_x_needed = (-P_q) % P
    assert P_x_needed == 230 > X_COUNT

    comparison = compare_author_report(
        author_report,
        records,
        packing,
        atom_rows,
        first_moments,
        zero_rows,
        multiplicity,
    )

    independent = {
        "schema": (
            "unique_tail_p233_doubleton_D_q_lift_attack/"
            "independent-audit-v1"
        ),
        "status": "CORRECT_WITHIN_EXPLICIT_RELAXED_SCOPE",
        "method": (
            "fresh literal reconstruction; no author-module import or execution"
        ),
        "p": P,
        "author_bindings_sha256": actual_bindings,
        "author_semantic_certificate": author_certificate,
        "incidence": {
            "K_size": len(groups["K"]),
            "L_size": len(groups["L"]),
            "W_size": len(groups["W"]),
            "endpoint_sizes": {
                name: len(endpoint) for name, endpoint in endpoints.items()
            },
            "Q_sizes": {name: len(q_set) for name, q_set in q_sets.items()},
            "Q_triple_intersection_size": len(set.intersection(*q_sets.values())),
        },
        "rho_maximal_atoms": atom_rows,
        "first_moments": first_moments,
        "actual_multiplicity": multiplicity,
        "endpoint_internal_zero_subset_rows": zero_rows,
        "endpoint_internal_summary": endpoint_summary,
        "outside_scope_probes": {
            "U_plus_X": {
                "contained_in_one_displayed_H": False,
                "x_needed": U_x_needed,
                "total_length": len(U) + U_x_needed,
                "actual_sum_class": U_height,
                "decision": "allowed_F3_but_not_part_of_endpoint-internal_enumeration",
            },
            "P_plus_X": {
                "rho_zero": True,
                "x_needed": P_x_needed,
                "available_X_positions": X_COUNT,
                "decision": "no_X_completion",
            },
        },
        "author_report_comparison": comparison,
        "strict_scope_confirmed": [
            "fixed Model-D W/K/L/H/Q literal incidence and rho labels",
            "three length-465 rho(Q_H) maximal atoms",
            "one shared q-coordinate and height per displayed W or P position",
            "first moments of U, W, P, Y, Z, every H, and every Q_H",
            "actual multiplicity at most 229 on X disjoint_union Y",
            "all rho-zero subsets contained in one displayed H, with X completion, short windows, and lengths 9 through 468 rejected",
        ],
        "omitted_scope_confirmed": [
            "rho-zero subsets of Y not contained in one displayed H",
            "the globally induced short spectrum and disjoint-short-block constraints",
            "proper-subset mixed P-Q_H target fibres",
            "Hasse rows and four-edge/all-endpoint completion",
            "actual Z atomicity",
        ],
        "verdict": (
            "The explicit fixed Model-D endpoint-internal q/height lift is a "
            "valid relaxed SAT witness. It is not a full 474-position labelled "
            "candidate and supplies no SAT result for the p=233 slice."
        ),
    }
    independent["certificate_sha256"] = canonical_hash(independent)
    REPORT_PATH.write_text(
        json.dumps(independent, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("STATUS CORRECT_WITHIN_EXPLICIT_RELAXED_SCOPE")
    print("PASS fresh 472-position and two-position packing reconstruction")
    print("PASS three rho maximal atoms and all first moments")
    print("PASS actual multiplicity cap 229")
    print("PASS 384 endpoint subsets scanned independently")
    print(f"CERTIFICATE {independent['certificate_sha256']}")


if __name__ == "__main__":
    main()
