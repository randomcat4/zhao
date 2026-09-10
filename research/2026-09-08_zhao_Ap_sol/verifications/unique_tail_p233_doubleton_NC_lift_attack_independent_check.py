#!/usr/bin/env python3
"""No-import audit of the fixed Model-N/Model-C lift attack.

The author module is neither imported nor executed.  This checker reconstructs
the symbolic Model-N cancellation and every displayed Model-C position from
the proof, performs its own bounded enumerations, and only afterwards compares
the resulting tables with the frozen author report.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path


P = 233
X_COUNT = P - 4
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUTPUT = HERE / "unique_tail_p233_doubleton_NC_lift_attack_independent_report.json"
AUTHOR_REPORT = BASE / "unique_tail_p233_doubleton_NC_lift_attack_report.json"

AUTHOR_BINDINGS = {
    "proofs/unique_tail_p233_doubleton_NC_lift_attack.md":
        "754e3fc772cf0d8b3b3ca614ee4cfcb55f3e1c2f0c5658d841837b50c824e34a",
    "unique_tail_p233_doubleton_NC_lift_attack.py":
        "99fde2260e6b748e797f88f94147975ebe9caf1bbeebc00a9ef952a144b4d478",
    "unique_tail_p233_doubleton_NC_lift_attack_report.json":
        "8f922fbcbf436a3d935582df25821721964d229eaca556542f11f8885a416204",
}

Actual = tuple[int, int, int, int]
Rho = tuple[int, int]

A: Actual = (1, 0, 0, 0)
X: Actual = (0, 1, 0, 0)
E: Rho = (1, 0)
F: Rho = (0, 1)
G: Rho = (P - 1, P - 1)
H: Rho = (P - 2, P - 1)


def canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def file_hash(relative: str) -> str:
    return sha256((BASE / relative).read_bytes()).hexdigest()


def control_scan(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    carriage_returns = [index for index, byte in enumerate(data) if byte == 13]
    embedded = [
        index
        for index in carriage_returns
        if index + 1 == len(data) or data[index + 1] != 10
    ]
    other_c0 = [
        [index, byte]
        for index, byte in enumerate(data)
        if byte < 32 and byte not in (9, 10, 13)
    ]
    return {
        "byte_count": len(data),
        "cr_count": len(carriage_returns),
        "crlf_count": len(carriage_returns) - len(embedded),
        "embedded_cr_offsets": embedded,
        "other_c0_controls": other_c0,
    }


def add(*vectors: tuple[int, ...]) -> tuple[int, ...]:
    if not vectors:
        raise ValueError("at least one vector is required")
    dimension = len(vectors[0])
    assert all(len(vector) == dimension for vector in vectors)
    return tuple(
        sum(vector[index] for vector in vectors) % P
        for index in range(dimension)
    )


def scale(coefficient: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * coordinate % P for coordinate in vector)


def signed(vector: tuple[int, ...]) -> list[int]:
    return [
        coordinate if coordinate <= P // 2 else coordinate - P
        for coordinate in vector
    ]


def actual(height: int, q_axis: int, rho: Rho) -> Actual:
    return (height % P, q_axis % P, rho[0] % P, rho[1] % P)


def rho(label: Actual) -> Rho:
    return (label[2], label[3])


def quotient(label: Actual) -> tuple[int, int, int]:
    return (label[1], label[2], label[3])


def set_sum(labels: dict[str, Actual], positions: set[str] | frozenset[str]) -> Actual:
    if not positions:
        return (0, 0, 0, 0)
    return add(*(labels[position] for position in positions))  # type: ignore[return-value]


def audit_model_n_symbolically() -> dict[str, object]:
    """Check the universal implication using only formal incidence cancellation."""

    U = frozenset({"u_e", "u_f", "u_t"})
    V = frozenset({"u_e", "x_f", "x_t"})
    common = frozenset({"y", "e_prime", "e_double_prime", "c"})
    H_s = V | common
    H_ef = frozenset({"u_e", "u_f", "x_t"}) | common
    H_et = frozenset({"u_e", "u_t", "x_f"}) | common

    difference_rows = []
    for left_name, left, right_name, right, expected in [
        ("H_s", H_s, "H_ef", H_ef, (["x_f"], ["u_f"])),
        ("H_s", H_s, "H_et", H_et, (["x_t"], ["u_t"])),
    ]:
        literal_difference = (sorted(left - right), sorted(right - left))
        assert literal_difference == expected
        difference_rows.append(
            {
                "equal_sum_comparison": [left_name, right_name],
                "positive_literal_coefficients": literal_difference[0],
                "negative_literal_coefficients": literal_difference[1],
                "forced_actual_label_equality": (
                    f"gamma({literal_difference[0][0]})="
                    f"gamma({literal_difference[1][0]})"
                ),
            }
        )

    assert len(U) == len(V) == 3
    assert U != V
    assert V - U == {"x_f", "x_t"}
    assert U - V == {"u_f", "u_t"}

    # The two equalities above make sigma(V)-sigma(U) the zero vector for
    # every target abelian group and every actual labelling.
    substitution_balance = Counter({"x_f": 1, "x_t": 1, "u_f": -1, "u_t": -1})
    substitutions = {"x_f": "u_f", "x_t": "u_t"}
    reduced = Counter()
    for symbol, coefficient in substitution_balance.items():
        reduced[substitutions.get(symbol, symbol)] += coefficient
    reduced += Counter()
    assert not reduced

    return {
        "quantifier": (
            "for every actual labelling of the fixed Model-N literal positions "
            "with sigma(H_s)=sigma(H_ef)=sigma(H_et)=3a, "
            "sigma(U)=3a-4x, and U the unique positive-core F3 tail"
        ),
        "endpoint_sizes": {"H_s": len(H_s), "H_ef": len(H_ef), "H_et": len(H_et)},
        "common_literal_part_size": len(common),
        "cancellation_rows": difference_rows,
        "unique_tail": sorted(U),
        "forced_second_tail": sorted(V),
        "tails_are_distinct_literal_sets": True,
        "forced_tail_sum_identity": "sigma(V)=sigma(U)=3a-4x",
        "forced_block": {
            "positions": "four X positions disjoint_union V",
            "length": 7,
            "actual_sum": "3a",
            "family": "F3",
        },
        "uses_no_additional_lift_assumption": True,
        "conclusion": "UNSAT for every actual lift satisfying the stated fixed-Model-N interface",
    }


def build_model_c() -> dict[str, object]:
    """Reconstruct every Model-C literal label from the displayed lift table."""

    labels: dict[str, Actual] = {}

    def insert(name: str, value: Actual) -> None:
        assert name not in labels
        labels[name] = value

    for index in range(1, 230):
        insert(f"C:K:g:ordinary:{index:03d}", actual(0, 0, G))
    insert("C:K:g:height2", actual(2, 0, G))
    insert("C:K:g:q_spike", actual(0, 1, G))

    for index in range(1, 230):
        insert(f"C:K:h:ordinary:{index:03d}", actual(0, 0, H))
    insert("C:K:h:height1", actual(1, 0, H))
    insert("C:K:h:height226", actual(-7, 0, H))

    rho_xs = add(H, scale(3, G))
    rho_xd = add(G, scale(2, H))
    for name, value in [
        ("u_e", actual(2, -1, E)),
        ("u_f", actual(0, -3, F)),
        ("u_t", actual(1, 0, G)),
        ("C:L:x_s", actual(1, 3, rho_xs)),  # type: ignore[arg-type]
        ("C:L:x_h", actual(0, 1, H)),
        ("C:L:x_d", actual(0, 0, rho_xd)),  # type: ignore[arg-type]
        ("C:L:y", actual(0, 0, (4, 3))),
        ("C:L:c_e_1", actual(1, 0, E)),
        ("C:L:c_e_2", actual(1, 0, E)),
        ("C:L:c_f", actual(-1, 0, F)),
        ("P:left", actual(0, 2, scale(-1, G))),  # type: ignore[arg-type]
        ("P:right", actual(-1, 1, G)),
    ]:
        insert(name, value)

    K = frozenset(name for name in labels if name.startswith("C:K:"))
    tails = frozenset({"u_e", "u_f", "u_t"})
    B_s = frozenset({"u_t", "u_f", "C:L:x_s"})
    B_d = frozenset({"C:L:x_h", "u_e", "C:L:x_d"})
    C0 = frozenset({"C:L:y", "C:L:c_e_1", "C:L:c_e_2", "C:L:c_f"})
    L = frozenset(tails | B_s | B_d | C0)
    P_positions = frozenset({"P:left", "P:right"})
    W = frozenset(K | L)
    Y = frozenset(W | P_positions)
    endpoints = {
        "C:H_singleton_e": frozenset(B_d | C0),
        "C:H_doubleton_ft": frozenset(B_s | C0),
    }
    q_sets = {
        endpoint_name: frozenset(K | (L - endpoint))
        for endpoint_name, endpoint in endpoints.items()
    }

    assert len(K) == 462 and len(L) == 10 and len(W) == 472
    assert len(P_positions) == 2 and len(Y) == 474
    assert K.isdisjoint(L) and W.isdisjoint(P_positions)
    assert all(len(endpoint) == 7 for endpoint in endpoints.values())
    assert all(len(q_set) == 465 for q_set in q_sets.values())
    assert set.intersection(*(set(q_set) for q_set in q_sets.values())) == set(K)
    return {
        "labels": labels,
        "K": K,
        "L": L,
        "W": W,
        "Y": Y,
        "P": P_positions,
        "tails": tails,
        "B_s": B_s,
        "B_d": B_d,
        "C0": C0,
        "endpoints": endpoints,
        "q_sets": q_sets,
    }


def zero_submultisets(counts: list[tuple[Rho, int]]) -> list[list[int]]:
    answers: list[list[int]] = []
    for choice in itertools.product(*(range(bound + 1) for _, bound in counts)):
        total = (
            sum(number * value[0] for number, (value, _) in zip(choice, counts)) % P,
            sum(number * value[1] for number, (value, _) in zip(choice, counts)) % P,
        )
        if total == (0, 0):
            answers.append(list(choice))
    return answers


def audit_rho_atoms(
    labels: dict[str, Actual], q_sets: dict[str, frozenset[str]]
) -> dict[str, object]:
    expected_simple = {
        "C:H_singleton_e": {
            "heavy": G,
            "base": H,
            "coefficient_histogram": {0: 231, P - 2: 1, 3: 1},
        },
        "C:H_doubleton_ft": {
            "heavy": H,
            "base": G,
            "coefficient_histogram": {0: 231, P - 1: 1, 2: 1},
        },
    }
    result: dict[str, object] = {}
    for name, q_set in q_sets.items():
        counts = sorted(Counter(rho(labels[position]) for position in q_set).items())
        zeros = zero_submultisets(counts)
        full = [bound for _, bound in counts]
        assert zeros == [[0] * len(counts), full]

        heavy = expected_simple[name]["heavy"]
        base = expected_simple[name]["base"]
        sequence = [rho(labels[position]) for position in q_set]
        assert sequence.count(heavy) == P - 1
        coefficient_histogram: Counter[int] = Counter()
        for value in sequence:
            if value == heavy:
                continue
            difference = (
                (value[0] - base[0]) % P,
                (value[1] - base[1]) % P,
            )
            if heavy[0]:
                coefficient = difference[0] * pow(heavy[0], -1, P) % P
            else:
                coefficient = difference[1] * pow(heavy[1], -1, P) % P
            assert add(base, scale(coefficient, heavy)) == value
            coefficient_histogram[coefficient] += 1
        assert dict(sorted(coefficient_histogram.items())) == expected_simple[name][
            "coefficient_histogram"
        ]
        assert sum(
            coefficient * count for coefficient, count in coefficient_histogram.items()
        ) % P == 1
        result[name] = {
            "length": len(q_set),
            "compressed_rho_multiplicities": [
                {"rho": signed(value), "count": bound}
                for value, bound in counts
            ],
            "zero_submultisets": zeros,
            "simple_form": {
                "heavy": signed(heavy),
                "base": signed(base),
                "heavy_count": P - 1,
                "line_count": P,
                "coefficient_histogram": {
                    str(coefficient): count
                    for coefficient, count in sorted(coefficient_histogram.items())
                },
                "coefficient_sum_mod_p": 1,
            },
            "minimal_zero_sum": True,
            "atomicity_reason": (
                "projection modulo the heavy direction forces 0 or p line terms; "
                "the two cases force respectively 0 or p-1 heavy terms"
            ),
        }
    return result


def mixed_reachable(
    labels: dict[str, Actual],
    q_set: frozenset[str],
    targets: set[Rho],
) -> dict[Rho, dict[str, object]]:
    types = sorted(Counter(quotient(labels[position]) for position in q_set).items())
    values = {
        target: {"q_sums": set(), "compressed_vectors": 0}
        for target in targets
    }
    for choice in itertools.product(*(range(bound + 1) for _, bound in types)):
        rho_sum = (
            sum(number * value[1] for number, (value, _) in zip(choice, types)) % P,
            sum(number * value[2] for number, (value, _) in zip(choice, types)) % P,
        )
        if rho_sum not in targets:
            continue
        q_sum = sum(
            number * value[0] for number, (value, _) in zip(choice, types)
        ) % P
        values[rho_sum]["compressed_vectors"] += 1
        values[rho_sum]["q_sums"].add(q_sum)
    for target in targets:
        assert values[target]["compressed_vectors"] > 0
        values[target]["q_sums"] = sorted(values[target]["q_sums"])
    return values


def audit_mixed_targets(model: dict[str, object]) -> dict[str, object]:
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    q_sets: dict[str, frozenset[str]] = model["q_sets"]  # type: ignore[assignment]
    P_positions: frozenset[str] = model["P"]  # type: ignore[assignment]
    assert len(P_positions) == 2
    singleton_As = [{position} for position in sorted(P_positions)]
    assert len(singleton_As) == 2

    p_left = labels["P:left"]
    p_right = labels["P:right"]
    assert rho(p_left) == scale(-1, G)
    assert rho(p_right) == G
    targets = {G, scale(-1, G)}

    result: dict[str, object] = {}
    for q_name, q_set in q_sets.items():
        reachable = mixed_reachable(labels, q_set, targets)
        left_target = scale(-1, rho(p_left))
        right_target = scale(-1, rho(p_right))
        left_q = reachable[left_target]["q_sums"]
        right_q = reachable[right_target]["q_sums"]
        left_combined = sorted((p_left[1] + value) % P for value in left_q)
        right_combined = sorted((p_right[1] + value) % P for value in right_q)
        assert set(left_combined) <= {1, 2, 3}
        assert set(right_combined) <= {1, 2, 3}
        result[q_name] = {
            "P_left": {
                "target_rho": signed(left_target),
                "reachable_q_axis_sums": left_q,
                "compressed_count_vector_count": reachable[left_target][
                    "compressed_vectors"
                ],
            },
            "P_left_combined_allowed_coefficients": left_combined,
            "P_right": {
                "target_rho": signed(right_target),
                "reachable_q_axis_sums": right_q,
                "compressed_count_vector_count": reachable[right_target][
                    "compressed_vectors"
                ],
            },
            "P_right_combined_allowed_coefficients": right_combined,
            "full_P_mixed_target_passes": True,
        }

    assert result["C:H_singleton_e"]["P_left"]["reachable_q_axis_sums"] == [0, 1]  # type: ignore[index]
    assert result["C:H_singleton_e"]["P_right"]["reachable_q_axis_sums"] == [0, 1]  # type: ignore[index]
    assert result["C:H_doubleton_ft"]["P_left"]["reachable_q_axis_sums"] == [0, 1, 232]  # type: ignore[index]
    assert result["C:H_doubleton_ft"]["P_right"]["reachable_q_axis_sums"] == [0, 1, 2]  # type: ignore[index]
    assert result["C:H_singleton_e"]["P_left"]["compressed_count_vector_count"] == 3  # type: ignore[index]
    assert result["C:H_singleton_e"]["P_right"]["compressed_count_vector_count"] == 3  # type: ignore[index]
    assert result["C:H_doubleton_ft"]["P_left"]["compressed_count_vector_count"] == 6  # type: ignore[index]
    assert result["C:H_doubleton_ft"]["P_right"]["compressed_count_vector_count"] == 6  # type: ignore[index]
    return result


def allowed_heights(length: int) -> set[int]:
    windows = {1: range(2, 7), 2: range(4, 8), 3: range(6, 9)}
    return {
        height
        for height, allowed_lengths in windows.items()
        if length in allowed_lengths
    }


def audit_endpoint_closure(model: dict[str, object]) -> tuple[list[dict[str, object]], dict[str, object]]:
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    endpoints: dict[str, frozenset[str]] = model["endpoints"]  # type: ignore[assignment]
    rows: list[dict[str, object]] = []
    subsets_scanned = 0
    short_violations: list[object] = []
    middle_violations: list[object] = []
    competing_positive_f3: list[object] = []

    for endpoint_name, endpoint in sorted(endpoints.items()):
        ordered = sorted(endpoint)
        for mask in range(1 << len(ordered)):
            subsets_scanned += 1
            subset = frozenset(
                ordered[index]
                for index in range(len(ordered))
                if mask & (1 << index)
            )
            subtotal = set_sum(labels, subset)
            if rho(subtotal) != (0, 0):
                continue
            q_sum = subtotal[1]
            height_sum = subtotal[0]
            x_needed = (-q_sum) % P
            x_available = x_needed <= X_COUNT
            total_length = len(subset) + x_needed if x_available else None

            if not subset:
                decision = "EMPTY"
            elif not x_available:
                decision = "NO_AVAILABLE_X_COMPLETION"
            elif total_length is not None and total_length <= 8:
                if height_sum not in allowed_heights(total_length):
                    short_violations.append([endpoint_name, sorted(subset)])
                family = f"F{height_sum}"
                if family == "F3" and x_needed > 0:
                    competing_positive_f3.append([endpoint_name, sorted(subset)])
                decision = f"ALLOWED_SHORT_{family}"
            elif total_length is not None and 9 <= total_length <= 2 * P + 2:
                decision = "FORBIDDEN_MIDDLE"
                middle_violations.append([endpoint_name, sorted(subset)])
            else:
                decision = "OUTSIDE_CHECKED_RANGE"

            rows.append(
                {
                    "endpoint": endpoint_name,
                    "subset": sorted(subset),
                    "subset_size": len(subset),
                    "is_full_endpoint": subset == endpoint,
                    "q_sum": q_sum,
                    "height_sum": height_sum,
                    "x_needed": x_needed,
                    "x_available": x_available,
                    "total_length": total_length,
                    "decision": decision,
                }
            )

    decisions = Counter(row["decision"] for row in rows)
    assert subsets_scanned == 256
    assert len(rows) == 18
    assert decisions == Counter(
        {
            "ALLOWED_SHORT_F2": 7,
            "ALLOWED_SHORT_F1": 4,
            "ALLOWED_SHORT_F3": 2,
            "NO_AVAILABLE_X_COMPLETION": 3,
            "EMPTY": 2,
        }
    )
    assert not short_violations and not middle_violations
    assert not competing_positive_f3
    return rows, {
        "literal_subsets_scanned": subsets_scanned,
        "rho_zero_subset_occurrences": len(rows),
        "nonempty_rho_zero_subset_occurrences": len(rows) - 2,
        "decision_counts": dict(sorted(decisions.items())),
        "short_window_violations": 0,
        "middle_gap_violations": 0,
        "competing_positive_core_F3_blocks": 0,
    }


def actual_multiplicity(model: dict[str, object]) -> dict[str, object]:
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    Y: frozenset[str] = model["Y"]  # type: ignore[assignment]
    counter: Counter[Actual] = Counter({X: X_COUNT})
    counter.update(labels[position] for position in Y)
    maximum = max(counter.values())
    cap_values = sorted(
        signed(label) for label, count in counter.items() if count == maximum
    )
    assert maximum == X_COUNT
    assert cap_values == [[0, 0, -2, -1], [0, 0, -1, -1], [0, 1, 0, 0]]
    distribution = Counter(counter.values())
    return {
        "positions_counted": X_COUNT + len(Y),
        "distinct_actual_labels": len(counter),
        "maximum": maximum,
        "required_upper_bound": X_COUNT,
        "values_at_maximum": cap_values,
        "multiplicity_value_distribution": {
            str(value): distribution[value] for value in sorted(distribution)
        },
        "passes": True,
    }


def global_bad_block(model: dict[str, object]) -> dict[str, object]:
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    positions = frozenset(
        {"C:L:c_e_1", "C:K:g:height2", "C:L:c_f"}
    )
    total = set_sum(labels, positions)
    assert quotient(total) == (0, 0, 0)
    assert len(positions) == 3 and total == scale(2, A)
    assert allowed_heights(3) == {1}
    assert total[0] == 2 not in allowed_heights(3)
    endpoints: dict[str, frozenset[str]] = model["endpoints"]  # type: ignore[assignment]
    assert all(not positions <= endpoint for endpoint in endpoints.values())
    return {
        "positions": sorted(positions),
        "literal_actual_labels": {
            position: signed(labels[position]) for position in sorted(positions)
        },
        "length": 3,
        "quotient_sum": [0, 0, 0],
        "actual_sum": signed(total),
        "required_actual_height_set": [1],
        "contained_in_either_displayed_endpoint": False,
        "passes": False,
        "meaning": (
            "this explicit lift fails global automatic-short compatibility; "
            "no statement is made about every lift of the fixed Model-C skeleton"
        ),
    }


def position_binding(model: dict[str, object]) -> tuple[dict[str, object], str]:
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    binding = {
        "labels": [[position, signed(labels[position])] for position in sorted(labels)],
        "K": sorted(model["K"]),
        "L": sorted(model["L"]),
        "P": sorted(model["P"]),
        "endpoints": {
            name: sorted(endpoint)
            for name, endpoint in sorted(model["endpoints"].items())  # type: ignore[union-attr]
        },
    }
    digest = sha256(
        json.dumps(binding, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return binding, digest


def compare_author(
    author: dict[str, object],
    model_n: dict[str, object],
    model_c: dict[str, object],
) -> dict[str, object]:
    assert author["schema"] == "unique_tail_p233_doubleton_NC_lift_attack/v2"
    assert author["p"] == P and author["global_status"] == "INCOMPLETE"
    author_n = author["model_N"]
    assert author_n["block_length"] == 7  # type: ignore[index]
    assert author_n["core_count"] == 4  # type: ignore[index]
    assert author_n["unique_tail"] == model_n["unique_tail"]  # type: ignore[index]
    assert author_n["forced_second_tail"] == model_n["forced_second_tail"]  # type: ignore[index]
    assert author_n["tails_are_distinct_literal_sets"] is True  # type: ignore[index]

    author_c = author["model_C"]
    assert author_c["sizes"] == model_c["sizes"]  # type: ignore[index]
    assert author_c["sums"] == model_c["sums"]  # type: ignore[index]
    assert author_c["P_mixed_targets"] == model_c["P_mixed_targets"]  # type: ignore[index]
    author_multiplicity = author_c["actual_multiplicity"]  # type: ignore[index]
    independent_multiplicity = model_c["actual_multiplicity"]  # type: ignore[index]
    for key in ["maximum", "required_upper_bound", "passes"]:
        assert author_multiplicity[key] == independent_multiplicity[key]
    assert sorted(author_multiplicity["values_at_maximum"]) == sorted(
        independent_multiplicity["values_at_maximum"]
    )
    assert author_c["literal_position_binding_sha256"] == model_c[  # type: ignore[index]
        "literal_position_binding_sha256"
    ]
    assert author_c["explicit_full_labels"] == model_c["explicit_full_labels"]  # type: ignore[index]

    for q_name, independent_row in model_c["rho_atoms"].items():  # type: ignore[union-attr]
        assert author_c["rho_atoms"][q_name] == {  # type: ignore[index]
            "compressed_rho_multiplicities": independent_row[
                "compressed_rho_multiplicities"
            ],
            "zero_submultisets": independent_row["zero_submultisets"],
            "minimal_zero_sum": True,
        }

    author_rows = {
        (row["endpoint"], tuple(row["subset"])): row
        for row in author_c["endpoint_internal_short_closure"][  # type: ignore[index]
            "rho_zero_subset_rows"
        ]
    }
    independent_rows = {
        (row["endpoint"], tuple(row["subset"])): row
        for row in model_c["endpoint_internal_zero_rows"]  # type: ignore[index]
    }
    assert author_rows == independent_rows
    author_boundary = author_c["global_automatic_short_boundary"]  # type: ignore[index]
    independent_boundary = model_c["global_automatic_short_boundary"]  # type: ignore[index]
    for key in [
        "positions",
        "literal_actual_labels",
        "length",
        "quotient_sum",
        "actual_sum",
        "required_actual_height_set",
        "passes",
    ]:
        assert author_boundary[key] == independent_boundary[key]
    return {
        "model_N_symbolic_incidence_match": True,
        "model_C_sizes_and_first_moments_match": True,
        "model_C_full_literal_label_table_match": True,
        "two_rho_atom_tables_match": True,
        "four_P_singleton_mixed_target_tables_match": True,
        "endpoint_internal_zero_subset_rows_match": True,
        "actual_multiplicity_summary_match": True,
        "global_bad_block_match": True,
    }


def main() -> None:
    bindings = {relative: file_hash(relative) for relative in AUTHOR_BINDINGS}
    assert bindings == AUTHOR_BINDINGS
    author_control_scans = {
        relative: control_scan(BASE / relative)
        for relative in AUTHOR_BINDINGS
    }
    assert all(
        not row["embedded_cr_offsets"] and not row["other_c0_controls"]
        for row in author_control_scans.values()
    )

    author = json.loads(AUTHOR_REPORT.read_text(encoding="utf-8"))
    author_certificate = author.pop("certificate_sha256")
    assert canonical_hash(author) == author_certificate

    model_n = audit_model_n_symbolically()
    model = build_model_c()
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    endpoints: dict[str, frozenset[str]] = model["endpoints"]  # type: ignore[assignment]
    q_sets: dict[str, frozenset[str]] = model["q_sets"]  # type: ignore[assignment]
    tails: frozenset[str] = model["tails"]  # type: ignore[assignment]

    sums = {
        "U": signed(set_sum(labels, tails)),
        "P": signed(set_sum(labels, model["P"])),  # type: ignore[arg-type]
        "W": signed(set_sum(labels, model["W"])),  # type: ignore[arg-type]
        "Y": signed(set_sum(labels, model["Y"])),  # type: ignore[arg-type]
        "endpoints": {
            name: signed(set_sum(labels, endpoint))
            for name, endpoint in endpoints.items()
        },
        "Q_H": {
            name: signed(set_sum(labels, q_set))
            for name, q_set in q_sets.items()
        },
    }
    assert sums == {
        "U": [3, -4, 0, 0],
        "P": [-1, 3, 0, 0],
        "W": [1, 1, 0, 0],
        "Y": [0, 4, 0, 0],
        "endpoints": {
            "C:H_singleton_e": [3, 0, 0, 0],
            "C:H_doubleton_ft": [3, 0, 0, 0],
        },
        "Q_H": {
            "C:H_singleton_e": [-2, 1, 0, 0],
            "C:H_doubleton_ft": [-2, 1, 0, 0],
        },
    }
    z_sum = add(scale(X_COUNT, X), set_sum(labels, model["Y"]))  # type: ignore[arg-type]
    assert z_sum == (0, 0, 0, 0)

    atoms = audit_rho_atoms(labels, q_sets)
    mixed = audit_mixed_targets(model)
    zero_rows, closure_summary = audit_endpoint_closure(model)
    multiplicity = actual_multiplicity(model)
    boundary = global_bad_block(model)
    binding_payload, binding_digest = position_binding(model)

    prescribed = add(scale(4, X), set_sum(labels, tails))
    assert prescribed == scale(3, A)

    model_c = {
        "quantifiers": {
            "existential": "the displayed actual lift and displayed two-position P",
            "universal_inside_witness": {
                "displayed_Q_H_count": 2,
                "nonempty_proper_P_subset_count": 2,
                "all_target_T_count_vectors_checked": True,
                "endpoint_literal_subsets_scanned": 256,
            },
            "not_decided": (
                "whether another lift of the fixed Model-C skeleton satisfies "
                "the global automatic-short spectrum"
            ),
        },
        "sizes": {"K": 462, "L": 10, "W": 472, "P": 2, "Y": 474},
        "sums": sums,
        "Z_sum": signed(z_sum),
        "rho_atoms": atoms,
        "P_mixed_targets": mixed,
        "actual_multiplicity": multiplicity,
        "prescribed_tail": {
            "tail": sorted(tails),
            "x_count": 4,
            "length": 7,
            "actual_sum": signed(prescribed),
            "family": "F3",
            "uniqueness_checked": False,
        },
        "endpoint_internal_zero_rows": zero_rows,
        "endpoint_internal_summary": closure_summary,
        "global_automatic_short_boundary": boundary,
        "literal_position_binding_sha256": binding_digest,
        "explicit_full_labels": {
            position: signed(label) for position, label in sorted(labels.items())
        },
    }
    comparison = compare_author(author, model_n, model_c)

    report = {
        "schema": "unique_tail_p233_doubleton_NC_lift_attack/independent-audit-v1",
        "status": "CORRECT_WITH_EXPLICIT_SPLIT_QUANTIFIERS/GLOBAL_INCOMPLETE",
        "method": "fresh reconstruction with no author-module import or execution",
        "p": P,
        "author_bindings_sha256": bindings,
        "author_control_scans": author_control_scans,
        "author_semantic_certificate": author_certificate,
        "model_N": model_n,
        "model_C": model_c,
        "author_report_comparison": comparison,
        "scope_verdict": {
            "model_N": (
                "universal UNSAT is valid for every actual lift of the fixed "
                "Model-N incidence satisfying the three endpoint sums and the "
                "unique positive-core F3-tail interface"
            ),
            "model_C_local": (
                "the displayed existential lift and P pass exactly the stated "
                "first-moment, rho-atom, multiplicity, mixed-target, and "
                "endpoint-internal closure interfaces"
            ),
            "model_C_global": (
                "the displayed lift is killed by the explicit global length-3 "
                "block, but fixed Model C is not proved UNSAT because other "
                "lifts are not quantified over"
            ),
        },
        "confirmed_omissions": [
            "a four-edge outer-shard completion beyond the two displayed endpoints",
            "global automatic-short compatibility",
            "the global quotient-zero length gap 9 through 468",
            "the full short-block intersection network",
            "long-complement atoms for every induced F3 block",
            "the separate length-697 complement atom",
            "Hasse congruences",
            "actual Z minimal zero-sum",
        ],
        "not_claimed": [
            "fixed Model-C skeleton UNSAT",
            "a globally short-compatible Model-C lift",
            "a full exact-slice candidate",
            "fixed-p SAT or global A_p",
        ],
    }
    report["certificate_sha256"] = canonical_hash(report)
    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("STATUS CORRECT_WITH_EXPLICIT_SPLIT_QUANTIFIERS")
    print("PASS Model N universal cancellation")
    print("PASS Model C explicit local lift and four mixed target fibres")
    print("PASS 256 endpoint subsets and global bad length-three block")
    print("PASS no embedded CR in frozen author artifacts")
    print(f"CERTIFICATE {report['certificate_sha256']}")


if __name__ == "__main__":
    main()
