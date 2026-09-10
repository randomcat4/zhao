#!/usr/bin/env python3
"""Fresh no-import audit of the displayed Model-D full-short rejection.

This checker never imports or executes either author module.  It reads the
frozen predecessor's literal position table as data, independently reconstructs
the D endpoint incidence, exact-label capacity classes, bounded short profiles,
disjoint-pair feasibility, and P--Q target fibres, and then compares its results
with the author report.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import itertools
import json
from math import comb
from pathlib import Path


P = 233
X_COUNT = 229
HERE = Path(__file__).resolve().parents[1]
BASE_REPORT = HERE / "unique_tail_p233_doubleton_D_q_lift_attack_report.json"
AUTHOR_PROOF = HERE / "proofs" / "unique_tail_p233_doubleton_D_full_short_closure.md"
AUTHOR_SCRIPT = HERE / "unique_tail_p233_doubleton_D_full_short_closure.py"
AUTHOR_REPORT = HERE / "unique_tail_p233_doubleton_D_full_short_closure_report.json"
OUTPUT_REPORT = Path(__file__).with_name(
    "unique_tail_p233_doubleton_D_full_short_closure_independent_report.json"
)

EXPECTED_AUTHOR_SHA256 = {
    "proofs/unique_tail_p233_doubleton_D_full_short_closure.md": (
        "b7b109201d180b68525f6198485db3e20da7fdabc9f855f7bdf820342ecf7691"
    ),
    "unique_tail_p233_doubleton_D_full_short_closure.py": (
        "dda624a6cda9b69e433b395d118176bac44145045bdddddac807cd4aff4a37e2"
    ),
    "unique_tail_p233_doubleton_D_full_short_closure_report.json": (
        "2166824b08e96478970be28d58cdb9d04bb3db3465f73895a6d63eb6365145fb"
    ),
    "unique_tail_p233_doubleton_D_q_lift_attack_report.json": (
        "ba15376e50590abe95620ffe3568f0ec2b1eb5a964ae934b82d47e38f7a3b58c"
    ),
}

Label = tuple[int, int, int, int]  # (q, rho_1, rho_2, height)
Rho = tuple[int, int]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
            "ascii"
        )
    ).hexdigest()


def load_certified_json(path: Path) -> tuple[dict[str, object], str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop("certificate_sha256")
    assert isinstance(claimed, str)
    assert canonical_hash(value) == claimed
    value["certificate_sha256"] = claimed
    return value, claimed


def verify_bindings() -> dict[str, object]:
    paths = {
        "proofs/unique_tail_p233_doubleton_D_full_short_closure.md": AUTHOR_PROOF,
        "unique_tail_p233_doubleton_D_full_short_closure.py": AUTHOR_SCRIPT,
        "unique_tail_p233_doubleton_D_full_short_closure_report.json": AUTHOR_REPORT,
        "unique_tail_p233_doubleton_D_q_lift_attack_report.json": BASE_REPORT,
    }
    actual = {name: file_sha256(path) for name, path in paths.items()}
    assert actual == EXPECTED_AUTHOR_SHA256
    author, author_certificate = load_certified_json(AUTHOR_REPORT)
    base, base_certificate = load_certified_json(BASE_REPORT)
    assert author_certificate == "36cbb4cf0f9fd5497ee0bfd3f219e9cf3a0dad8d206a7b0f9354d86191b1e03a"
    assert base_certificate == "69a434edeb843342b7cd1bde819b64c2cfa7277fea64bd79f4ebe394be411298"
    return {
        "file_sha256": actual,
        "author_report_certificate": author_certificate,
        "base_report_certificate": base_certificate,
        "_author": author,
        "_base": base,
    }


def add_rho(*values: Rho) -> Rho:
    return (
        sum(value[0] for value in values) % P,
        sum(value[1] for value in values) % P,
    )


def sum_labels(positions: set[str] | list[str] | tuple[str, ...], labels: dict[str, Label]) -> Label:
    q = rho_1 = rho_2 = height = 0
    for position in positions:
        label = (1, 0, 0, 0) if position.startswith("X_") else labels[position]
        q = (q + label[0]) % P
        rho_1 = (rho_1 + label[1]) % P
        rho_2 = (rho_2 + label[2]) % P
        height = (height + label[3]) % P
    return q, rho_1, rho_2, height


def reconstruct_literal_model(base: dict[str, object]) -> dict[str, object]:
    position_rows = base["position_lift_rows"]
    packing_rows = base["packing_rows"]
    assert isinstance(position_rows, list) and len(position_rows) == 472
    assert isinstance(packing_rows, list) and len(packing_rows) == 2

    labels: dict[str, Label] = {}
    K: set[str] = set()
    L: set[str] = set()
    for row in position_rows:
        position = str(row["position"])
        rho = row["rho"]
        assert position not in labels
        labels[position] = (
            int(row["q_coordinate"]) % P,
            int(rho[0]) % P,
            int(rho[1]) % P,
            int(row["height"]) % P,
        )
        (K if row["part"] == "K" else L).add(position)

    packing: set[str] = set()
    for row in packing_rows:
        position = str(row["position"])
        rho = row["rho"]
        assert position not in labels
        labels[position] = (
            int(row["q_coordinate"]) % P,
            int(rho[0]) % P,
            int(rho[1]) % P,
            int(row["height"]) % P,
        )
        packing.add(position)

    p13 = {f"d_p13_h_{index:03d}" for index in range(1, 5)}
    p23 = {"d_p23_g", "d_p23_h", "d_p23_z1", "d_p23_z2"}
    p12 = {"d_p12_g1", "d_p12_g2", "d_p12_f", "d_p12_r"}
    U = {"u_e", "u_f", "u_t"}
    endpoints = {
        "H_doubleton_ft": p23 | {"u_f", "u_t", "d_y"},
        "H_doubleton_et": p13 | {"u_e", "u_t", "d_y"},
        "H_doubleton_ef": p12 | {"u_e", "u_f", "d_y"},
    }
    expected_L = p13 | p23 | p12 | U | {"d_y"}
    assert L == expected_L
    q_sets = {name: K | (L - endpoint) for name, endpoint in endpoints.items()}

    assert len(K) == 456 and len(L) == 16 and len(labels) == 474
    assert all(len(endpoint) == 7 for endpoint in endpoints.values())
    assert all(len(q_set) == 465 for q_set in q_sets.values())
    assert set.intersection(*(set(q_set) for q_set in q_sets.values())) == K
    assert all(sum_labels(set(endpoint), labels) == (0, 0, 0, 3) for endpoint in endpoints.values())
    assert all(sum_labels(set(q_set), labels) == (1, 0, 0, P - 2) for q_set in q_sets.values())
    assert sum_labels(U, labels) == (P - 4, 0, 0, 3)
    assert sum_labels(packing, labels) == (3, 0, 0, P - 1)

    return {
        "labels": labels,
        "K": K,
        "L": L,
        "U": U,
        "packing": packing,
        "endpoints": endpoints,
        "q_sets": q_sets,
    }


def simple_atom_check(model: dict[str, object]) -> dict[str, object]:
    labels: dict[str, Label] = model["labels"]  # type: ignore[assignment]
    q_sets: dict[str, set[str]] = model["q_sets"]  # type: ignore[assignment]
    standards = {
        "H_doubleton_ft": ((1, 0), (0, 1)),
        "H_doubleton_et": ((1, 0), (0, 1)),
        "H_doubleton_ef": ((2, 1), (1, 0)),
    }
    answers: dict[str, object] = {}
    for name, q_set in sorted(q_sets.items()):
        heavy, base = standards[name]
        values = [(labels[position][1], labels[position][2]) for position in q_set]
        assert values.count(heavy) == P - 1
        coefficients: list[int] = []
        for value in values:
            if value == heavy:
                continue
            matches = [
                coefficient
                for coefficient in range(P)
                if (
                    (base[0] + coefficient * heavy[0]) % P,
                    (base[1] + coefficient * heavy[1]) % P,
                )
                == value
            ]
            assert len(matches) == 1
            coefficients.append(matches[0])
        assert len(coefficients) == P and sum(coefficients) % P == 1
        answers[name] = {
            "heavy": list(heavy),
            "base": list(base),
            "heavy_count": values.count(heavy),
            "line_count": len(coefficients),
            "line_coefficient_sum": sum(coefficients) % P,
        }
    return answers


@dataclass(frozen=True)
class TypeRow:
    label: Label
    positions: tuple[str, ...]

    @property
    def capacity(self) -> int:
        return len(self.positions)


@dataclass(frozen=True)
class Profile:
    counts: tuple[int, ...]
    x_count: int
    y_size: int
    length: int
    q_sum: int
    height: int
    allowed_classes: tuple[int, ...]
    allowed: bool


def build_types(model: dict[str, object]) -> tuple[list[TypeRow], dict[str, int]]:
    labels: dict[str, Label] = model["labels"]  # type: ignore[assignment]
    grouped: defaultdict[Label, list[str]] = defaultdict(list)
    for position, label in labels.items():
        grouped[label].append(position)
    rows = [
        TypeRow(label, tuple(sorted(positions)))
        for label, positions in sorted(grouped.items())
    ]
    position_type = {
        position: index for index, row in enumerate(rows) for position in row.positions
    }
    assert len(rows) == 17 and len(position_type) == 474
    return rows, position_type


def allowed_classes(length: int) -> tuple[int, ...]:
    values: list[int] = []
    if 2 <= length <= 6:
        values.append(1)
    if 4 <= length <= 7:
        values.append(2)
    if 6 <= length <= 8:
        values.append(3)
    return tuple(values)


def count_vectors_by_polynomial(types: list[TypeRow]) -> int:
    coefficients = [1] + [0] * 8
    for row in types:
        updated = [0] * 9
        for old_degree, old_count in enumerate(coefficients):
            for amount in range(min(row.capacity, 8 - old_degree) + 1):
                updated[old_degree + amount] += old_count
        coefficients = updated
    assert coefficients == [1, 17, 140, 746, 2900, 8798, 21781, 45489, 82353]
    return sum(coefficients)


def enumerate_profiles(types: list[TypeRow]) -> tuple[list[Profile], int, list[int]]:
    counts = [0] * len(types)
    profiles: list[Profile] = []
    size_distribution = [0] * 9
    visited = 0

    def visit(index: int, remaining: int, size: int, q: int, r1: int, r2: int, h: int) -> None:
        nonlocal visited
        if index == len(types):
            visited += 1
            size_distribution[size] += 1
            if r1 % P or r2 % P:
                return
            x_count = (-q) % P
            length = size + x_count
            if not (1 <= length <= 8 and x_count <= X_COUNT):
                return
            allowed = allowed_classes(length)
            profiles.append(
                Profile(
                    tuple(counts),
                    x_count,
                    size,
                    length,
                    q % P,
                    h % P,
                    allowed,
                    h % P in allowed,
                )
            )
            return
        label = types[index].label
        for amount in range(min(types[index].capacity, remaining) + 1):
            counts[index] = amount
            visit(
                index + 1,
                remaining - amount,
                size + amount,
                q + amount * label[0],
                r1 + amount * label[1],
                r2 + amount * label[2],
                h + amount * label[3],
            )
        counts[index] = 0

    visit(0, 8, 0, 0, 0, 0, 0)
    profiles.sort(key=lambda row: (row.length, not row.allowed, row.height, row.x_count, row.counts))
    return profiles, visited, size_distribution


def compare_compression_with_author(
    types: list[TypeRow], profiles: list[Profile], visited: int, size_distribution: list[int], author: dict[str, object]
) -> dict[str, object]:
    section = author["strict_full_Y_compression"]
    author_types = section["actual_types"]
    rebuilt_types = [
        {
            "actual_type_index": index,
            "actual_label_q_rho1_rho2_height": list(row.label),
            "capacity": row.capacity,
            "literal_positions": list(row.positions),
        }
        for index, row in enumerate(types)
    ]
    assert rebuilt_types == author_types
    assert visited == 162225 == section["bounded_count_vectors_of_Y_size_at_most_8_visited"]
    assert size_distribution == [1, 17, 140, 746, 2900, 8798, 21781, 45489, 82353]

    author_profiles = section["all_quotient_zero_short_profiles"]
    assert len(author_profiles) == len(profiles) == 252
    for ours, theirs in zip(profiles, author_profiles):
        counts = [0] * len(types)
        for sparse in theirs["actual_type_counts"]:
            counts[int(sparse["actual_type_index"])] = int(sparse["count"])
        assert tuple(counts) == ours.counts
        assert int(theirs["x_count"]) == ours.x_count
        assert int(theirs["y_size"]) == ours.y_size
        assert int(theirs["length"]) == ours.length
        assert int(theirs["q_sum_y"]) == ours.q_sum
        assert int(theirs["height_sum_y"]) == ours.height
        assert tuple(theirs["allowed_actual_sum_classes"]) == ours.allowed_classes
        assert (theirs["decision"].startswith("ALLOWED")) == ours.allowed

    allowed = [profile for profile in profiles if profile.allowed]
    forbidden = [profile for profile in profiles if not profile.allowed]
    assert len(allowed) == 75 == section["allowed_short_profile_count"]
    assert len(forbidden) == 177 == section["forbidden_short_profile_count"]
    digest_rows = [
        [list(profile.counts), profile.x_count, profile.length, profile.height, profile.allowed]
        for profile in profiles
    ]
    return {
        "actual_type_count": len(types),
        "type_capacities": [row.capacity for row in types],
        "bounded_count_vectors_visited": visited,
        "count_vectors_by_Y_size": size_distribution,
        "quotient_zero_short_profiles": len(profiles),
        "allowed_profiles": len(allowed),
        "forbidden_profiles": len(forbidden),
        "profile_semantic_digest": canonical_hash(digest_rows),
        "exact_type_rows_match_author": True,
        "all_252_profile_rows_match_author": True,
        "compression_equivalence": (
            "a literal subset determines one bounded count vector; every bounded vector is realized "
            "by choosing that many positions from each exact-label class"
        ),
    }


def literal_counts(positions: set[str], position_type: dict[str, int], type_count: int) -> tuple[int, ...]:
    counts = [0] * type_count
    for position in positions:
        counts[position_type[position]] += 1
    return tuple(counts)


def representative(profile: Profile, types: list[TypeRow], x_start: int = 1) -> list[str]:
    positions: list[str] = []
    for index, count in enumerate(profile.counts):
        positions.extend(types[index].positions[:count])
    positions.extend(f"X_{index:03d}" for index in range(x_start, x_start + profile.x_count))
    return sorted(positions)


def audit_short_witness(
    model: dict[str, object], types: list[TypeRow], profiles: list[Profile], position_type: dict[str, int]
) -> dict[str, object]:
    labels: dict[str, Label] = model["labels"]  # type: ignore[assignment]
    witness = {"d_k_g_002", "u_f", "u_t"}
    assert sum_labels(witness, labels) == (0, 0, 0, 0)
    counts = literal_counts(witness, position_type, len(types))
    matches = [row for row in profiles if row.counts == counts and row.x_count == 0]
    assert len(matches) == 1
    row = matches[0]
    assert row.length == 3 and row.height == 0 and not row.allowed
    assert min(profile.length for profile in profiles if not profile.allowed) == 3
    assert not [profile for profile in profiles if not profile.allowed and profile.length < 3]
    return {
        "positions": sorted(witness),
        "full_sum_q_rho1_rho2_height": list(sum_labels(witness, labels)),
        "length": 3,
        "allowed_height_classes": [1],
        "actual_height_class": 0,
        "is_shortest_forbidden_profile_length": True,
        "also_proper_actual_zero_sum_subsequence_of_Z": True,
    }


def audit_disjoint_pairs(
    labels: dict[str, Label], types: list[TypeRow], profiles: list[Profile], author: dict[str, object]
) -> dict[str, object]:
    allowed_indexed = [(index, row) for index, row in enumerate(profiles) if row.allowed]
    checked = feasible = 0
    conflicts: list[tuple[int, int, tuple[str, ...]]] = []
    first_literals: tuple[list[str], list[str]] | None = None
    for offset, (left_index, left) in enumerate(allowed_indexed):
        for right_index, right in allowed_indexed[offset:]:
            checked += 1
            if left.x_count + right.x_count > X_COUNT:
                continue
            if any(
                left.counts[index] + right.counts[index] > types[index].capacity
                for index in range(len(types))
            ):
                continue
            feasible += 1
            left_positions: list[str] = []
            right_positions: list[str] = []
            for index, type_row in enumerate(types):
                left_count = left.counts[index]
                right_count = right.counts[index]
                left_positions.extend(type_row.positions[:left_count])
                right_positions.extend(type_row.positions[left_count : left_count + right_count])
            left_positions.extend(f"X_{index:03d}" for index in range(1, left.x_count + 1))
            right_positions.extend(
                f"X_{index:03d}"
                for index in range(left.x_count + 1, left.x_count + right.x_count + 1)
            )
            assert set(left_positions).isdisjoint(right_positions)
            assert sum_labels(set(left_positions), labels)[0:3] == (0, 0, 0)
            assert sum_labels(set(right_positions), labels)[0:3] == (0, 0, 0)

            reasons: list[str] = []
            if left.height == 3 or right.height == 3:
                reasons.append("F3_MUST_INTERSECT_EVERY_SHORT_BLOCK")
            if left.height == right.height == 2:
                reasons.append("F2_BLOCKS_MUST_PAIRWISE_INTERSECT")
            if left.length + right.length >= P + 2:
                reasons.append("DISJOINT_UNION_ENTERED_MIDDLE_GAP")
            if reasons:
                conflicts.append((left_index, right_index, tuple(reasons)))
                if first_literals is None:
                    first_literals = (sorted(left_positions), sorted(right_positions))

    section = author["disjoint_short_intersection_audit"]
    assert checked == 2850 == section["profile_pairs_checked_with_repetition"]
    assert feasible == 62 == section["disjoint_feasible_profile_pairs"]
    assert len(conflicts) == 53 == section["forbidden_disjoint_profile_pair_count"]
    author_conflicts = [
        (int(row["left_profile_index"]), int(row["right_profile_index"]), tuple(row["reasons"]))
        for row in section["all_forbidden_disjoint_profile_pairs"]
    ]
    assert conflicts == author_conflicts
    first = section["first_forbidden_disjoint_pair"]
    assert first_literals == (
        list(first["left_literal_representative"]),
        list(first["right_literal_representative"]),
    )
    left_literal, right_literal = first_literals
    assert sum_labels(set(left_literal), labels) == (0, 0, 0, 1)
    assert sum_labels(set(right_literal), labels) == (0, 0, 0, 3)
    assert len(left_literal) == 5 and len(right_literal) == 7
    return {
        "allowed_profile_pairs_with_repetition": checked,
        "disjoint_feasible_pairs": feasible,
        "forbidden_disjoint_pairs": len(conflicts),
        "conflict_reason_distribution": dict(
            sorted(Counter(reason for _, _, reasons in conflicts for reason in reasons).items())
        ),
        "first_pair": {
            "left": left_literal,
            "right": right_literal,
            "left_sum": [0, 0, 0, 1],
            "right_sum": [0, 0, 0, 3],
            "disjoint": True,
        },
        "capacity_criterion_is_bidirectional": (
            "two profile representatives are disjoint iff each exact-label demand sum is at most "
            "its class capacity and the two X demands sum to at most 229"
        ),
        "all_53_conflict_records_match_author": True,
    }


def direct_zero_q_rho_support(q_set: set[str], labels: dict[str, Label]) -> tuple[set[Rho], list[str]]:
    zero_counts = Counter(
        (labels[position][1], labels[position][2])
        for position in q_set
        if labels[position][0] == 0
    )
    defects = sorted(position for position in q_set if labels[position][0] != 0)
    types = sorted(zero_counts.items())
    reachable: set[Rho] = set()
    for choice in itertools.product(*(range(capacity + 1) for _, capacity in types)):
        reachable.add(
            (
                sum(count * rho[0] for count, (rho, _) in zip(choice, types)) % P,
                sum(count * rho[1] for count, (rho, _) in zip(choice, types)) % P,
            )
        )
    return reachable, defects


def direct_target_fibre(target: Rho, reachable_zero: set[Rho], defects: list[str], labels: dict[str, Label]) -> list[int]:
    q_values: set[int] = set()
    for mask in range(1 << len(defects)):
        chosen = [position for index, position in enumerate(defects) if mask >> index & 1]
        q, r1, r2, _ = sum_labels(set(chosen), labels)
        residual = ((target[0] - r1) % P, (target[1] - r2) % P)
        if residual in reachable_zero:
            q_values.add(q)
    return sorted(q_values)


def audit_mixed(model: dict[str, object], author: dict[str, object]) -> dict[str, object]:
    labels: dict[str, Label] = model["labels"]  # type: ignore[assignment]
    K: set[str] = model["K"]  # type: ignore[assignment]
    q_sets: dict[str, set[str]] = model["q_sets"]  # type: ignore[assignment]
    T = {
        *(f"d_k_g_{index:03d}" for index in range(2, 17)),
        *(f"d_k_h_{index:03d}" for index in range(1, 223)),
    }
    assert len(T) == 237 and T < K
    assert sum_labels(T, labels)[:3] == (0, P - 7, P - 11)
    assert labels["p_1"][:3] == (0, 7, 11)
    assert labels["p_2"][:3] == (3, P - 7, P - 11)

    expected_fibres = {
        "H_doubleton_ef": [0, 1, 5, 6, 228, 229],
        "H_doubleton_et": [0, 1, 5, 6, 228, 229],
        "H_doubleton_ft": [0, 1, 5, 6, 10, 224, 228, 229],
    }
    expected_state_counts = {
        "H_doubleton_ef": 54054,
        "H_doubleton_et": 54287,
        "H_doubleton_ft": 54283,
    }
    endpoint_rows: dict[str, object] = {}
    literal_witnesses: list[dict[str, object]] = []
    for name, q_set in sorted(q_sets.items()):
        reachable_zero, defects = direct_zero_q_rho_support(q_set, labels)
        assert len(reachable_zero) == expected_state_counts[name]
        negative = direct_target_fibre((P - 7, P - 11), reachable_zero, defects, labels)
        positive = direct_target_fibre((7, 11), reachable_zero, defects, labels)
        assert negative == positive == expected_fibres[name]

        assert T < q_set
        complement = q_set - T
        assert 0 < len(complement) < len(q_set)
        assert sum_labels(complement, labels)[:3] == (1, 7, 11)
        assert sum_labels(T | {"p_1"}, labels)[:3] == (0, 0, 0)
        assert sum_labels(complement | {"p_2"}, labels)[:3] == (4, 0, 0)
        literal_witnesses.extend(
            [
                {"endpoint": name, "packing": "p_1", "Q_subset": "T", "union_q": 0},
                {"endpoint": name, "packing": "p_2", "Q_subset": "Q_minus_T", "union_q": 4},
            ]
        )
        endpoint_rows[name] = {
            "zero_q_reachable_rho_states": len(reachable_zero),
            "nonzero_q_literal_positions": len(defects),
            "target_minus_7_minus_11_q_values": negative,
            "target_7_11_q_values": positive,
        }

    author_rows = {
        row["endpoint"]: row for row in author["mixed_P_Q_target_audit"]["endpoint_target_fibres"]
    }
    for name, row in endpoint_rows.items():
        assert row["zero_q_reachable_rho_states"] == author_rows[name]["zero_q_rho_reachable_state_count"]
        author_values = [entry["reachable_Q_subset_q_sums"] for entry in author_rows[name]["packing_singletons"]]
        assert author_values == [expected_fibres[name], expected_fibres[name]]
    assert len(literal_witnesses) == 6
    return {
        "method": (
            "direct Cartesian enumeration of bounded multiplicities for q=0 rho types, then "
            "direct subset enumeration of nonzero-q literal defects; no binary-split author routine"
        ),
        "T_size": len(T),
        "T_subset_of_common_K": True,
        "T_sum_q_rho1_rho2_height": list(sum_labels(T, labels)),
        "endpoint_target_fibres": endpoint_rows,
        "literal_3_by_2_witnesses": literal_witnesses,
        "all_six_are_violations": True,
    }


def build_report() -> dict[str, object]:
    bindings = verify_bindings()
    author = bindings.pop("_author")
    base = bindings.pop("_base")
    model = reconstruct_literal_model(base)
    atom_rows = simple_atom_check(model)
    types, position_type = build_types(model)
    profiles, visited, size_distribution = enumerate_profiles(types)
    # Independent generating-function check of the enumeration by total Y size.
    polynomial_total = count_vectors_by_polynomial(types)
    assert polynomial_total == sum(size_distribution) == visited
    compression = compare_compression_with_author(
        types, profiles, visited, size_distribution, author
    )
    short = audit_short_witness(model, types, profiles, position_type)
    disjoint = audit_disjoint_pairs(model["labels"], types, profiles, author)  # type: ignore[arg-type]
    mixed = audit_mixed(model, author)

    assert "SKELETON_RELABEL_SEARCH_OPEN" in str(author["status"])
    assert "alternative unified q/height/P relabellings were not quantified" in str(
        author["conclusion"]
    )
    report: dict[str, object] = {
        "schema": "unique_tail_p233_doubleton_D_full_short_closure_independent_review_v1",
        "audit_method": (
            "fresh no-import reconstruction from the predecessor JSON literal table; the author "
            "script was neither imported nor executed"
        ),
        "bindings": bindings,
        "fixed_literal_model": {
            "Y_positions": 474,
            "K_positions": 456,
            "L_positions": 16,
            "P_positions": 2,
            "Q_sizes": {name: len(value) for name, value in model["q_sets"].items()},  # type: ignore[union-attr]
            "simple_maximal_rho_atom_checks": atom_rows,
        },
        "compression_and_short_spectrum": compression,
        "shortest_exact_bad_block": short,
        "disjoint_allowed_short_profiles": disjoint,
        "mixed_P_Q_targets": mixed,
        "scope_audit": {
            "displayed_literal_relabel_rejected": True,
            "fixed_rho_skeleton_all_relabels_rejected": False,
            "author_scope_wording_is_correct": True,
            "typesetting_check": "the equation (13) separator is correctly typeset in the bound proof",
        },
        "verdict": "CORRECT",
        "conclusion": (
            "The displayed Model-D q/height/P lift is rigorously rejected by a length-three bad "
            "block and by six P--Q mixed witnesses; the 53 disjoint-profile conflicts are also exact. "
            "No result here, or in the audited author artifact, quantifies over all relabellings of "
            "the fixed rho skeleton."
        ),
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    OUTPUT_REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("VERDICT", report["verdict"])
    print("PASS 17 exact-label types and 162225 bounded vectors")
    print("PASS 252 short profiles = 75 allowed + 177 forbidden")
    print("PASS 53 exact disjoint-profile conflicts and the first literal pair")
    print("PASS common T gives 3 x 2 literal mixed violations")
    print("CERTIFICATE", report["certificate_sha256"])


if __name__ == "__main__":
    main()
