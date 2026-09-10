#!/usr/bin/env python3
"""Exact next-layer separators for the frozen Model-D q/height lift.

The program keeps every literal position of the frozen rho skeleton.  For the
length-at-most-eight spectrum it compresses positions only when their complete
actual labels (q, rho_1, rho_2, height) agree, and it retains the exact
capacity of every such class.  Count-vector enumeration is therefore exactly
equivalent to literal subset enumeration for short labels and for the
existence of two disjoint representatives.

The result rejects the *displayed* q/height lift.  It does not quantify over
all possible q/height relabellings of the same rho skeleton.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
from typing import Callable, Iterable


P = 233
X_COUNT = P - 4
HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_p233_doubleton_D_full_short_closure_report.json"

DEPENDENCY_SHA256 = {
    "proofs/unique_tail_p233_doubleton_D_q_lift_attack.md": (
        "a6413cbccf122e2f040f428e3569018f35f6942eafbbc9f80c776430e5f9114d"
    ),
    "unique_tail_p233_doubleton_D_q_lift_attack.py": (
        "19e6d555a5424780fc3ab176e2e0d1318e1907d2142c587d422d412b5be0885c"
    ),
    "unique_tail_p233_doubleton_D_q_lift_attack_report.json": (
        "ba15376e50590abe95620ffe3568f0ec2b1eb5a964ae934b82d47e38f7a3b58c"
    ),
}

ActualLabel = tuple[int, int, int, int]
Rho = tuple[int, int]


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
            "ascii"
        )
    ).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_dependencies() -> dict[str, str]:
    actual = {relative: file_sha256(HERE / relative) for relative in DEPENDENCY_SHA256}
    assert actual == DEPENDENCY_SHA256
    return actual


def load_base():
    path = HERE / "unique_tail_p233_doubleton_D_q_lift_attack.py"
    spec = importlib.util.spec_from_file_location("doubleton_d_q_lift_base", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_rho(left: Rho, right: Rho) -> Rho:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def sum_rho(positions: Iterable[str], rho: dict[str, Rho]) -> Rho:
    result = (0, 0)
    for position in positions:
        result = add_rho(result, rho[position])
    return result


def allowed_actual_sums(length: int) -> set[int]:
    allowed: set[int] = set()
    if 2 <= length <= 6:
        allowed.add(1)
    if 4 <= length <= 7:
        allowed.add(2)
    if 6 <= length <= 8:
        allowed.add(3)
    return allowed


@dataclass(frozen=True)
class ActualType:
    label: ActualLabel
    positions: tuple[str, ...]

    @property
    def capacity(self) -> int:
        return len(self.positions)


@dataclass(frozen=True)
class ShortProfile:
    counts: tuple[int, ...]
    x_count: int
    y_size: int
    length: int
    q_sum_y: int
    height_sum_y: int
    family: int
    allowed_families: tuple[int, ...]
    allowed: bool


def build_actual_types(model, lift) -> tuple[list[ActualType], dict[str, int]]:
    rho: dict[str, Rho] = model["rho"]
    q_coordinate: dict[str, int] = lift["q_coordinate"]
    height: dict[str, int] = lift["height"]
    packing_rho: dict[str, Rho] = lift["packing_rho"]
    packing_q: dict[str, int] = lift["packing_q"]
    packing_height: dict[str, int] = lift["packing_height"]

    grouped: dict[ActualLabel, list[str]] = defaultdict(list)
    for position in sorted(model["W"]):
        grouped[
            (
                q_coordinate[position] % P,
                rho[position][0] % P,
                rho[position][1] % P,
                height[position] % P,
            )
        ].append(position)
    for position in sorted(lift["packing"]):
        grouped[
            (
                packing_q[position] % P,
                packing_rho[position][0] % P,
                packing_rho[position][1] % P,
                packing_height[position] % P,
            )
        ].append(position)

    types = [
        ActualType(label=label, positions=tuple(sorted(positions)))
        for label, positions in sorted(grouped.items())
    ]
    type_of_position = {
        position: index
        for index, row in enumerate(types)
        for position in row.positions
    }
    assert len(type_of_position) == 474
    assert set(type_of_position) == set(model["W"]) | set(lift["packing"])
    return types, type_of_position


def enumerate_short_profiles(types: list[ActualType]) -> tuple[list[ShortProfile], int]:
    """Enumerate every bounded Y count vector of size at most eight."""

    counts = [0] * len(types)
    profiles: list[ShortProfile] = []
    count_vectors_visited = 0

    def visit(
        index: int,
        remaining: int,
        y_size: int,
        q_sum: int,
        rho_1_sum: int,
        rho_2_sum: int,
        height_sum: int,
    ) -> None:
        nonlocal count_vectors_visited
        if index == len(types):
            count_vectors_visited += 1
            if rho_1_sum % P or rho_2_sum % P:
                return
            x_needed = (-q_sum) % P
            length = y_size + x_needed
            if not (1 <= length <= 8 and x_needed <= X_COUNT):
                return
            family = height_sum % P
            allowed_families = tuple(sorted(allowed_actual_sums(length)))
            profiles.append(
                ShortProfile(
                    counts=tuple(counts),
                    x_count=x_needed,
                    y_size=y_size,
                    length=length,
                    q_sum_y=q_sum % P,
                    height_sum_y=height_sum % P,
                    family=family,
                    allowed_families=allowed_families,
                    allowed=family in allowed_families,
                )
            )
            return

        q_value, rho_1, rho_2, height = types[index].label
        for multiplicity in range(min(types[index].capacity, remaining) + 1):
            counts[index] = multiplicity
            visit(
                index + 1,
                remaining - multiplicity,
                y_size + multiplicity,
                (q_sum + multiplicity * q_value) % P,
                (rho_1_sum + multiplicity * rho_1) % P,
                (rho_2_sum + multiplicity * rho_2) % P,
                (height_sum + multiplicity * height) % P,
            )
        counts[index] = 0

    visit(0, 8, 0, 0, 0, 0, 0)
    profiles.sort(
        key=lambda row: (
            row.length,
            not row.allowed,
            row.family,
            row.x_count,
            row.counts,
        )
    )
    assert len({(row.counts, row.x_count) for row in profiles}) == len(profiles)
    return profiles, count_vectors_visited


def representative_block(profile: ShortProfile, types: list[ActualType]) -> list[str]:
    positions: list[str] = []
    for index, multiplicity in enumerate(profile.counts):
        positions.extend(types[index].positions[:multiplicity])
    positions.extend(f"X_{index:03d}" for index in range(1, profile.x_count + 1))
    return sorted(positions)


def literal_profile_counts(
    positions: Iterable[str], type_of_position: dict[str, int], number_of_types: int
) -> tuple[int, ...]:
    counts = [0] * number_of_types
    for position in positions:
        counts[type_of_position[position]] += 1
    return tuple(counts)


def profile_to_json(profile: ShortProfile, types: list[ActualType]) -> dict[str, object]:
    sparse_counts = [
        {"actual_type_index": index, "count": count}
        for index, count in enumerate(profile.counts)
        if count
    ]
    number_of_literal_realizations = comb(X_COUNT, profile.x_count)
    for index, count in enumerate(profile.counts):
        number_of_literal_realizations *= comb(types[index].capacity, count)
    return {
        "x_count": profile.x_count,
        "y_size": profile.y_size,
        "length": profile.length,
        "q_sum_y": profile.q_sum_y,
        "rho_sum_y": [0, 0],
        "height_sum_y": profile.height_sum_y,
        "actual_sum_class": profile.family,
        "allowed_actual_sum_classes": list(profile.allowed_families),
        "decision": (
            f"ALLOWED_SHORT_F{profile.family}"
            if profile.allowed
            else "FORBIDDEN_AUTOMATIC_SHORT_BLOCK"
        ),
        "actual_type_counts": sparse_counts,
        "representative_literal_block": representative_block(profile, types),
        "number_of_literal_realizations": str(number_of_literal_realizations),
    }


def validate_short_literal_witness(model, lift, profiles, types, type_of_position):
    rho: dict[str, Rho] = model["rho"]
    q_coordinate: dict[str, int] = lift["q_coordinate"]
    height: dict[str, int] = lift["height"]
    witness = ("d_k_g_002", "u_f", "u_t")
    assert set(witness) <= set(model["W"])
    assert sum_rho(witness, rho) == (0, 0)
    assert sum(q_coordinate[position] for position in witness) % P == 0
    assert sum(height[position] for position in witness) % P == 0

    witness_counts = literal_profile_counts(witness, type_of_position, len(types))
    matches = [
        row
        for row in profiles
        if row.counts == witness_counts and row.x_count == 0
    ]
    assert len(matches) == 1
    profile = matches[0]
    assert profile.length == 3 and profile.family == 0 and not profile.allowed
    return {
        "literal_positions": list(witness),
        "q_sum": 0,
        "rho_sum": [0, 0],
        "height_sum": 0,
        "length": 3,
        "allowed_actual_sum_classes_at_length_3": [1],
        "actual_sum_class": 0,
        "decision": "EXACT_FORBIDDEN_AUTOMATIC_SHORT_BLOCK",
    }


def disjoint_pair_representatives(
    left: ShortProfile, right: ShortProfile, types: list[ActualType]
) -> tuple[list[str], list[str]]:
    left_positions: list[str] = []
    right_positions: list[str] = []
    for index, actual_type in enumerate(types):
        left_count = left.counts[index]
        right_count = right.counts[index]
        assert left_count + right_count <= actual_type.capacity
        left_positions.extend(actual_type.positions[:left_count])
        right_positions.extend(
            actual_type.positions[left_count : left_count + right_count]
        )
    assert left.x_count + right.x_count <= X_COUNT
    left_positions.extend(f"X_{index:03d}" for index in range(1, left.x_count + 1))
    right_positions.extend(
        f"X_{index:03d}"
        for index in range(left.x_count + 1, left.x_count + right.x_count + 1)
    )
    assert set(left_positions).isdisjoint(right_positions)
    return sorted(left_positions), sorted(right_positions)


def disjoint_pair_audit(profiles: list[ShortProfile], types: list[ActualType]):
    allowed_rows = [(index, row) for index, row in enumerate(profiles) if row.allowed]
    profile_pairs = 0
    disjoint_feasible_pairs = 0
    forbidden_pairs: list[dict[str, object]] = []

    for offset, (left_index, left) in enumerate(allowed_rows):
        for right_index, right in allowed_rows[offset:]:
            profile_pairs += 1
            if left.x_count + right.x_count > X_COUNT:
                continue
            if any(
                left.counts[index] + right.counts[index] > types[index].capacity
                for index in range(len(types))
            ):
                continue
            disjoint_feasible_pairs += 1
            reasons: list[str] = []
            if left.family == 3 or right.family == 3:
                reasons.append("F3_MUST_INTERSECT_EVERY_SHORT_BLOCK")
            if left.family == right.family == 2:
                reasons.append("F2_BLOCKS_MUST_PAIRWISE_INTERSECT")
            if left.length + right.length >= P + 2:
                reasons.append("DISJOINT_UNION_ENTERED_MIDDLE_GAP")
            if reasons:
                left_literal, right_literal = disjoint_pair_representatives(left, right, types)
                forbidden_pairs.append(
                    {
                        "left_profile_index": left_index,
                        "right_profile_index": right_index,
                        "left_family": left.family,
                        "right_family": right.family,
                        "left_length": left.length,
                        "right_length": right.length,
                        "reasons": reasons,
                        "left_literal_representative": left_literal,
                        "right_literal_representative": right_literal,
                    }
                )

    return {
        "allowed_profile_count": len(allowed_rows),
        "profile_pairs_checked_with_repetition": profile_pairs,
        "disjoint_feasible_profile_pairs": disjoint_feasible_pairs,
        "forbidden_disjoint_profile_pair_count": len(forbidden_pairs),
        "first_forbidden_disjoint_pair": forbidden_pairs[0] if forbidden_pairs else None,
        "all_forbidden_disjoint_profile_pairs": forbidden_pairs,
        "p_plus_2_middle_gap_threshold": P + 2,
        "largest_two_short_block_length_sum": 16,
        "middle_gap_pair_rule_is_vacuous_at_p233": True,
    }


def pack(value: Rho) -> int:
    return value[0] * P + value[1]


def unpack(value: int) -> Rho:
    return divmod(value, P)


def add_packed(left: int, right: int) -> int:
    lx, ly = unpack(left)
    rx, ry = unpack(right)
    return ((lx + rx) % P) * P + ((ly + ry) % P)


def bounded_rho_reachability(values: Counter[Rho]) -> set[int]:
    """Exact support of a bounded C_p^2 multiset via binary splitting."""

    reachable = {0}
    for rho, count in sorted(values.items()):
        chunk = 1
        remaining = count
        while remaining:
            take = min(chunk, remaining)
            remaining -= take
            chunk *= 2
            item = pack(((take * rho[0]) % P, (take * rho[1]) % P))
            previous = tuple(reachable)
            reachable.update(add_packed(value, item) for value in previous)
    return reachable


def target_q_oracle(
    q_set: set[str], rho: dict[str, Rho], q_coordinate: dict[str, int]
) -> tuple[Callable[[Rho], set[int]], int, int]:
    """Return every q-sum attained at a requested rho target, exactly."""

    defects = sorted(position for position in q_set if q_coordinate[position] % P)
    zero_counter = Counter(
        rho[position] for position in q_set if q_coordinate[position] % P == 0
    )
    reachable = bounded_rho_reachability(zero_counter)
    signatures: list[tuple[Rho, int]] = []
    for mask in range(1 << len(defects)):
        rho_sum = (0, 0)
        q_sum = 0
        for index, position in enumerate(defects):
            if mask >> index & 1:
                rho_sum = add_rho(rho_sum, rho[position])
                q_sum = (q_sum + q_coordinate[position]) % P
        signatures.append((rho_sum, q_sum))

    def oracle(target: Rho) -> set[int]:
        values: set[int] = set()
        for defect_rho, defect_q in signatures:
            residual = (
                (target[0] - defect_rho[0]) % P,
                (target[1] - defect_rho[1]) % P,
            )
            if pack(residual) in reachable:
                values.add(defect_q)
        return values

    return oracle, len(reachable), len(defects)


def validate_mixed_targets(model, lift):
    rho: dict[str, Rho] = model["rho"]
    q_coordinate: dict[str, int] = lift["q_coordinate"]
    packing_rho: dict[str, Rho] = lift["packing_rho"]
    packing_q: dict[str, int] = lift["packing_q"]

    t_common = {
        *(f"d_k_g_{index:03d}" for index in range(2, 17)),
        *(f"d_k_h_{index:03d}" for index in range(1, 223)),
    }
    assert len(t_common) == 237
    assert t_common <= model["K"]
    assert sum_rho(t_common, rho) == ((-7) % P, (-11) % P)
    assert sum(q_coordinate[position] for position in t_common) % P == 0

    endpoint_rows: list[dict[str, object]] = []
    literal_witness_rows: list[dict[str, object]] = []
    for endpoint_name, q_set in sorted(model["q_sets"].items()):
        oracle, reachable_size, defect_count = target_q_oracle(
            q_set, rho, q_coordinate
        )
        row: dict[str, object] = {
            "endpoint": endpoint_name,
            "q_set_size": len(q_set),
            "zero_q_rho_reachable_state_count": reachable_size,
            "nonzero_q_literal_position_count": defect_count,
            "packing_singletons": [],
        }
        assert t_common < q_set

        for packing_position in sorted(lift["packing"]):
            p_rho = packing_rho[packing_position]
            target = ((-p_rho[0]) % P, (-p_rho[1]) % P)
            reachable_q_sums = sorted(oracle(target))
            allowed_q_sums_for_q_subset = sorted(
                {(value - packing_q[packing_position]) % P for value in (1, 2, 3)}
            )
            bad_q_sums = sorted(set(reachable_q_sums) - set(allowed_q_sums_for_q_subset))
            row["packing_singletons"].append(
                {
                    "packing_position": packing_position,
                    "packing_rho": list(p_rho),
                    "packing_q": packing_q[packing_position],
                    "target_rho_for_Q_subset": list(target),
                    "reachable_Q_subset_q_sums": reachable_q_sums,
                    "allowed_Q_subset_q_sums": allowed_q_sums_for_q_subset,
                    "violating_Q_subset_q_sums": bad_q_sums,
                    "decision": "VIOLATION_EXISTS" if bad_q_sums else "CLEAR",
                }
            )

        complement = set(q_set) - t_common
        assert 0 < len(complement) < len(q_set)
        assert sum_rho(complement, rho) == (7, 11)
        assert sum(q_coordinate[position] for position in complement) % P == 1

        p1_total_rho = add_rho(packing_rho["p_1"], sum_rho(t_common, rho))
        p1_total_q = (
            packing_q["p_1"]
            + sum(q_coordinate[position] for position in t_common)
        ) % P
        assert p1_total_rho == (0, 0) and p1_total_q == 0
        literal_witness_rows.append(
            {
                "endpoint": endpoint_name,
                "packing_position": "p_1",
                "Q_subset": "T_common",
                "Q_subset_size": len(t_common),
                "Q_subset_rho_sum": [P - 7, P - 11],
                "Q_subset_q_sum": 0,
                "union_quotient_sum_class": 0,
                "allowed_union_quotient_sum_classes": [1, 2, 3],
                "decision": "EXACT_MIXED_TARGET_VIOLATION",
            }
        )

        p2_total_rho = add_rho(packing_rho["p_2"], sum_rho(complement, rho))
        p2_total_q = (
            packing_q["p_2"]
            + sum(q_coordinate[position] for position in complement)
        ) % P
        assert p2_total_rho == (0, 0) and p2_total_q == 4
        literal_witness_rows.append(
            {
                "endpoint": endpoint_name,
                "packing_position": "p_2",
                "Q_subset": "Q_endpoint_minus_T_common",
                "Q_subset_size": len(complement),
                "Q_subset_rho_sum": [7, 11],
                "Q_subset_q_sum": 1,
                "union_quotient_sum_class": 4,
                "allowed_union_quotient_sum_classes": [1, 2, 3],
                "decision": "EXACT_MIXED_TARGET_VIOLATION",
            }
        )
        endpoint_rows.append(row)

    assert len(literal_witness_rows) == 6
    assert all(
        singleton["decision"] == "VIOLATION_EXISTS"
        for row in endpoint_rows
        for singleton in row["packing_singletons"]
    )
    return {
        "oracle_method": (
            "binary-split exact bounded reachability on all q=0 literal positions, "
            "crossed with every subset of the nonzero-q literal positions"
        ),
        "endpoint_target_fibres": endpoint_rows,
        "T_common_positions": sorted(t_common),
        "T_common_description": "15 e-positions d_k_g_002..016 and 222 h-positions d_k_h_001..222",
        "literal_mixed_target_violations": literal_witness_rows,
    }


def build_report() -> dict[str, object]:
    dependencies = verify_dependencies()
    base = load_base()
    base.verify_dependencies()
    model = base.build_fixed_model()
    lift = base.build_lift(model)
    base.endpoint_internal_closure(model, lift)

    types, type_of_position = build_actual_types(model, lift)
    profiles, count_vectors_visited = enumerate_short_profiles(types)
    assert profiles
    bad_profiles = [row for row in profiles if not row.allowed]
    assert bad_profiles
    short_witness = validate_short_literal_witness(
        model, lift, profiles, types, type_of_position
    )
    disjoint_audit = disjoint_pair_audit(profiles, types)
    mixed_audit = validate_mixed_targets(model, lift)

    type_rows = [
        {
            "actual_type_index": index,
            "actual_label_q_rho1_rho2_height": list(row.label),
            "capacity": row.capacity,
            "literal_positions": list(row.positions),
        }
        for index, row in enumerate(types)
    ]
    profile_rows = [profile_to_json(row, types) for row in profiles]

    report: dict[str, object] = {
        "schema": "unique_tail_p233_doubleton_D_full_short_closure_v1",
        "status": (
            "FIXED_MODEL_D_Q_LIFT_REJECTED/FULL_SHORT_AND_MIXED_SEPARATORS/"
            "SKELETON_RELABEL_SEARCH_OPEN/GLOBAL_INCOMPLETE"
        ),
        "p": P,
        "dependencies_sha256": dependencies,
        "frozen_candidate": {
            "rho_skeleton": "three-doubleton Model D",
            "Y_size": 474,
            "W_size": 472,
            "packing_P_size": 2,
            "X_size": X_COUNT,
            "q_height_lift": "the exact lift frozen by the three dependency files",
        },
        "strict_full_Y_compression": {
            "equivalence_statement": (
                "Y positions are merged iff their complete actual labels "
                "(q,rho1,rho2,height) agree; exact capacities are retained. "
                "Thus bounded count vectors are equivalent to literal subsets "
                "for label sums and to literal disjoint pairs for capacity feasibility."
            ),
            "actual_type_count": len(types),
            "actual_types": type_rows,
            "bounded_count_vectors_of_Y_size_at_most_8_visited": count_vectors_visited,
            "quotient_zero_short_profile_count": len(profiles),
            "allowed_short_profile_count": len(profiles) - len(bad_profiles),
            "forbidden_short_profile_count": len(bad_profiles),
            "all_quotient_zero_short_profiles": profile_rows,
        },
        "first_exact_short_conflict": short_witness,
        "disjoint_short_intersection_audit": disjoint_audit,
        "mixed_P_Q_target_audit": mixed_audit,
        "strictly_checked_scope": [
            "the frozen 474 literal Y positions, their rho labels, q coordinates, and heights",
            "every automatically induced quotient-zero block of total length at most eight, including 0..229 copies of X as allowed by the length bound",
            "exact same-label capacities, hence exact existence of two disjoint representatives of any two allowed short profiles",
            "the F3-versus-all-short and F2-versus-F2 disjoint intersection rules",
            "both nonempty proper singleton subsets of the two-position packing P against every one of the three Q_H, using an exact target-rho/q-sum oracle",
            "six direct literal mixed-target counterexamples sharing one common subset T of K",
        ],
        "open_or_omitted_scope": [
            "all alternative q-coordinate and height assignments on the same fixed rho skeleton",
            "a complete SAT/UNSAT search over those relabellings and over alternative two-position packing labels",
            "the full length 9..2p+2 quotient-zero separator for arbitrary Y subsets (the displayed candidate is already rejected at length three)",
            "multi-block disjoint matching capacity beyond pairwise intersection rules; at p=233 no pair of length-at-most-eight blocks reaches the p+2=235 middle-gap threshold",
            "Hasse congruences, all long-complement internal subset sums, and actual Z atomicity",
            "all other incidence skeletons, all 720 outer shards, the complete fixed-p slice, and global A_p",
        ],
        "conclusion": (
            "The previously displayed endpoint-internal q/height lift is not a full-Y survivor. "
            "It has an exact forbidden length-three automatic block and six exact P-Q_H mixed-target violations. "
            "The underlying rho skeleton has not been proved UNSAT because alternative unified q/height/P relabellings were not quantified."
        ),
        "external_dependency_note": (
            "The maximal-atom status of the three rho(Q_H) uses the frozen Property-B construction inherited through the dependency chain; this script replays the base module's simple-form checks but does not prove Property B."
        ),
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    with REPORT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    compression = report["strict_full_Y_compression"]
    disjoint = report["disjoint_short_intersection_audit"]
    print(
        "PASS exact full-Y short compression:",
        compression["actual_type_count"],
        "types,",
        compression["bounded_count_vectors_of_Y_size_at_most_8_visited"],
        "count vectors",
    )
    print(
        "REJECT frozen q-lift by",
        compression["forbidden_short_profile_count"],
        "forbidden automatic short profiles",
    )
    print(
        "PASS exact disjoint-pair audit:",
        disjoint["forbidden_disjoint_profile_pair_count"],
        "forbidden feasible profile pairs",
    )
    print("REJECT frozen q-lift by six literal P-Q_H mixed-target violations")
    print(f"CERTIFICATE {report['certificate_sha256']}")
    print("BOUNDARY alternative unified q/height/P relabellings remain open")


if __name__ == "__main__":
    main()
