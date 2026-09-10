#!/usr/bin/env python3
"""Exact sparse-defect relabel exhaustion for the fixed Model-C/D rho skeletons.

This is deliberately *not* an exhaustion of every q/height labelling of either
rho skeleton.  It closes two explicitly frozen, symmetry-normalized sparse
q-support families.  Within those families every field value, every nonzero
ordered packing direction, and every packing q-coordinate is covered.

Model C is first filtered by the complete mixed P--Q target fibres.  Every
survivor is then rejected by the rigid part of the global automatic short
spectrum (lengths 2, 3, and 8).  Heights are literal-position variables: no
constant-height assumption is made on a q/rho fibre.

Model D is already rejected by the complete mixed target fibres.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


P = 233
X_COUNT = P - 4
HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_p233_doubleton_CD_relabel_exhaustion_report.json"

Rho = tuple[int, int]


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
            "ascii"
        )
    ).hexdigest()


def signed(value: int) -> int:
    value %= P
    return value if value <= P // 2 else value - P


def signed_rho(value: Rho) -> list[int]:
    return [signed(value[0]), signed(value[1])]


def add_rho(left: Rho, right: Rho) -> Rho:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def smul(coefficient: int, value: Rho) -> Rho:
    return ((coefficient * value[0]) % P, (coefficient * value[1]) % P)


def sum_rho(positions: Iterable[str], rho: dict[str, Rho]) -> Rho:
    result = (0, 0)
    for position in positions:
        result = add_rho(result, rho[position])
    return result


def add_positions(
    rho: dict[str, Rho], prefix: str, count: int, value: Rho
) -> set[str]:
    positions = {f"{prefix}{index:03d}" for index in range(1, count + 1)}
    assert not (set(rho) & positions)
    for position in positions:
        rho[position] = value
    return positions


@dataclass(frozen=True)
class Model:
    name: str
    rho: dict[str, Rho]
    K: frozenset[str]
    L: frozenset[str]
    W: frozenset[str]
    U: frozenset[str]
    endpoints: dict[str, frozenset[str]]
    q_sets: dict[str, frozenset[str]]


def build_model_c() -> Model:
    e: Rho = (1, 0)
    f: Rho = (0, 1)
    g: Rho = (-1 % P, -1 % P)
    h: Rho = (-2 % P, -1 % P)
    rho: dict[str, Rho] = {}

    k_g = add_positions(rho, "C:K:g:ordinary:", 229, g)
    rho["C:K:g:height2"] = g
    rho["C:K:g:q_spike"] = g
    k_g |= {"C:K:g:height2", "C:K:g:q_spike"}

    k_h = add_positions(rho, "C:K:h:ordinary:", 229, h)
    rho["C:K:h:height1"] = h
    rho["C:K:h:height226"] = h
    k_h |= {"C:K:h:height1", "C:K:h:height226"}
    K = frozenset(k_g | k_h)

    rho.update(
        {
            "u_e": e,
            "u_f": f,
            "u_t": g,
            "C:L:x_s": add_rho(h, smul(3, g)),
            "C:L:x_h": h,
            "C:L:x_d": add_rho(g, smul(2, h)),
            "C:L:y": (4, 3),
            "C:L:c_e_1": e,
            "C:L:c_e_2": e,
            "C:L:c_f": f,
        }
    )
    U = frozenset({"u_e", "u_f", "u_t"})
    block_s = frozenset({"u_t", "u_f", "C:L:x_s"})
    block_d = frozenset({"C:L:x_h", "u_e", "C:L:x_d"})
    common = frozenset({"C:L:y", "C:L:c_e_1", "C:L:c_e_2", "C:L:c_f"})
    L = frozenset(U | block_s | block_d | common)
    endpoints = {
        "C:H_singleton_e": frozenset(block_d | common),
        "C:H_doubleton_ft": frozenset(block_s | common),
    }
    W = frozenset(K | L)
    q_sets = {
        name: frozenset(K | (L - endpoint))
        for name, endpoint in endpoints.items()
    }
    assert len(K) == 462 and len(L) == 10 and len(W) == 472
    assert all(len(endpoint) == 7 for endpoint in endpoints.values())
    assert all(sum_rho(endpoint, rho) == (0, 0) for endpoint in endpoints.values())
    assert all(len(q_set) == 465 for q_set in q_sets.values())
    return Model("C", rho, K, L, W, U, endpoints, q_sets)


def build_model_d() -> Model:
    e: Rho = (1, 0)
    f: Rho = (0, 1)
    t: Rho = (-1 % P, -1 % P)
    h = add_rho(smul(2, e), f)
    z = add_rho(e, h)
    r = add_rho(smul(5, e), f)
    y = add_rho(smul(-8, e), smul(-3, f))
    rho: dict[str, Rho] = {"u_e": e, "u_f": f, "u_t": t}
    K = frozenset(
        add_positions(rho, "d_k_g_", 229, e)
        | add_positions(rho, "d_k_h_", 227, h)
    )
    p13 = add_positions(rho, "d_p13_h_", 4, h)
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
    p23 = frozenset({"d_p23_g", "d_p23_h", "d_p23_z1", "d_p23_z2"})
    p12 = frozenset({"d_p12_g1", "d_p12_g2", "d_p12_f", "d_p12_r"})
    U = frozenset({"u_e", "u_f", "u_t"})
    L = frozenset(p13 | p23 | p12 | U | {"d_y"})
    endpoints = {
        "D:H_doubleton_ft": frozenset(p23 | {"u_f", "u_t", "d_y"}),
        "D:H_doubleton_et": frozenset(p13 | {"u_e", "u_t", "d_y"}),
        "D:H_doubleton_ef": frozenset(p12 | {"u_e", "u_f", "d_y"}),
    }
    W = frozenset(K | L)
    q_sets = {
        name: frozenset(K | (L - endpoint))
        for name, endpoint in endpoints.items()
    }
    assert len(K) == 456 and len(L) == 16 and len(W) == 472
    assert all(len(endpoint) == 7 for endpoint in endpoints.values())
    assert all(sum_rho(endpoint, rho) == (0, 0) for endpoint in endpoints.values())
    assert all(len(q_set) == 465 for q_set in q_sets.values())
    return Model("D", rho, K, L, W, U, endpoints, q_sets)


def verify_simple_atoms(model: Model) -> dict[str, object]:
    if model.name == "C":
        standards = {
            "C:H_singleton_e": ((-1 % P, -1 % P), (0, 1)),
            "C:H_doubleton_ft": ((-2 % P, -1 % P), (-1 % P, -1 % P)),
        }
    else:
        standards = {
            "D:H_doubleton_ft": ((1, 0), (0, 1)),
            "D:H_doubleton_et": ((1, 0), (0, 1)),
            "D:H_doubleton_ef": ((2, 1), (1, 0)),
        }
    rows: dict[str, object] = {}
    for name, q_set in sorted(model.q_sets.items()):
        heavy, base = standards[name]
        determinant = (heavy[0] * base[1] - heavy[1] * base[0]) % P
        assert determinant
        sequence = [model.rho[position] for position in sorted(q_set)]
        assert sequence.count(heavy) == P - 1
        coefficients: list[int] = []
        for value in sequence:
            if value == heavy:
                continue
            candidates = [
                coefficient
                for coefficient in range(P)
                if add_rho(base, smul(coefficient, heavy)) == value
            ]
            assert len(candidates) == 1
            coefficients.append(candidates[0])
        assert len(coefficients) == P and sum(coefficients) % P == 1
        rows[name] = {
            "heavy": signed_rho(heavy),
            "base": signed_rho(base),
            "heavy_count": P - 1,
            "line_count": P,
            "line_coefficient_sum_mod_p": 1,
        }
    return rows


def pack_rho(value: Rho) -> int:
    return (value[0] % P) * P + value[1] % P


def unpack_rho(value: int) -> Rho:
    return divmod(value, P)


def add_packed(left: int, right: int) -> int:
    lx, ly = unpack_rho(left)
    rx, ry = unpack_rho(right)
    return ((lx + rx) % P) * P + (ly + ry) % P


def bounded_rho_reachability(
    positions: Iterable[str], rho: dict[str, Rho]
) -> frozenset[int]:
    """Exact bounded submultiset-sum support, using binary splitting."""

    reachable = {0}
    for value, count in sorted(Counter(rho[position] for position in positions).items()):
        chunk = 1
        remaining = count
        while remaining:
            take = min(chunk, remaining)
            remaining -= take
            chunk *= 2
            item = pack_rho(smul(take, value))
            previous = tuple(reachable)
            reachable.update(add_packed(old, item) for old in previous)
    return frozenset(reachable)


@dataclass(frozen=True)
class TargetData:
    q_set_name: str
    defects: tuple[str, ...]
    zero_base_reachable: frozenset[int]
    defect_rho_sums: tuple[Rho, ...]


def make_target_data(
    model: Model, defect_orders: dict[str, tuple[str, ...]]
) -> tuple[TargetData, ...]:
    result: list[TargetData] = []
    for name, q_set in sorted(model.q_sets.items()):
        defects = tuple(position for position in defect_orders[name] if position in q_set)
        assert len(defects) <= 4
        reachable = bounded_rho_reachability(set(q_set) - set(defects), model.rho)
        signatures: list[Rho] = []
        for mask in range(1 << len(defects)):
            signatures.append(
                sum_rho(
                    (position for index, position in enumerate(defects) if mask >> index & 1),
                    model.rho,
                )
            )
        result.append(TargetData(name, defects, reachable, tuple(signatures)))
    return tuple(result)


def target_mask_groups(
    data: tuple[TargetData, ...]
) -> dict[tuple[tuple[int, ...], ...], tuple[Rho, ...]]:
    groups: dict[tuple[tuple[int, ...], ...], list[Rho]] = defaultdict(list)
    for target_1 in range(P):
        for target_2 in range(P):
            patterns: list[tuple[int, ...]] = []
            for row in data:
                masks = tuple(
                    mask
                    for mask, subtotal in enumerate(row.defect_rho_sums)
                    if pack_rho(
                        (
                            (target_1 - subtotal[0]) % P,
                            (target_2 - subtotal[1]) % P,
                        )
                    )
                    in row.zero_base_reachable
                )
                patterns.append(masks)
            groups[tuple(patterns)].append((target_1, target_2))
    assert sum(len(targets) for targets in groups.values()) == P * P
    return {pattern: tuple(targets) for pattern, targets in groups.items()}


def allowed_target_q_values(alpha: int) -> frozenset[int]:
    return frozenset((value - alpha) % P for value in (1, 2, 3))


def compatible_alphas(values: set[int]) -> tuple[int, ...]:
    return tuple(
        alpha
        for alpha in range(P)
        if values <= allowed_target_q_values(alpha)
    )


def dot(row: tuple[int, ...], values: tuple[int, ...]) -> int:
    return sum(coefficient * value for coefficient, value in zip(row, values)) % P


def independent_extension_rows(
    exact_rows: list[tuple[tuple[int, ...], int]],
    membership_rows: list[tuple[int, int, tuple[int, ...]]],
) -> list[tuple[int, int, tuple[int, ...]]]:
    basis: list[tuple[int, list[int]]] = []

    def add(row: tuple[int, ...]) -> bool:
        reduced = list(row)
        for pivot, basis_row in basis:
            if reduced[pivot]:
                coefficient = reduced[pivot]
                reduced = [
                    (left - coefficient * right) % P
                    for left, right in zip(reduced, basis_row)
                ]
        if not any(reduced):
            return False
        pivot = next(index for index, value in enumerate(reduced) if value)
        inverse = pow(reduced[pivot], -1, P)
        basis.append((pivot, [value * inverse % P for value in reduced]))
        return True

    for row, _ in exact_rows:
        assert add(row)
    chosen: list[tuple[int, int, tuple[int, ...]]] = []
    for item in membership_rows:
        if add(item[2]):
            chosen.append(item)
    return chosen


def solve_unique_linear_system(
    equations: list[tuple[tuple[int, ...], int]], number_of_variables: int
) -> tuple[int, ...] | None:
    matrix = [list(row) + [rhs % P] for row, rhs in equations]
    rank = 0
    pivots: list[int] = []
    for column in range(number_of_variables):
        pivot_row = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column] % P),
            None,
        )
        if pivot_row is None:
            continue
        matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
        inverse = pow(matrix[rank][column] % P, -1, P)
        matrix[rank] = [value * inverse % P for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column] % P:
                continue
            coefficient = matrix[row][column] % P
            matrix[row] = [
                (left - coefficient * right) % P
                for left, right in zip(matrix[row], matrix[rank])
            ]
        pivots.append(column)
        rank += 1
    if any(
        not any(value % P for value in row[:number_of_variables])
        and row[number_of_variables] % P
        for row in matrix
    ):
        return None
    if rank != number_of_variables:
        return None
    answer = [0] * number_of_variables
    for row, column in enumerate(pivots):
        answer[column] = matrix[row][number_of_variables] % P
    return tuple(answer)


def c_membership_row(side: int, mask: int) -> tuple[int, ...]:
    # Variables are (k, f, t, x_s, e, x_h, x_d).
    indices = (0, 1, 2, 3) if side == 0 else (0, 4, 5, 6)
    row = [0] * 7
    for bit, variable in enumerate(indices):
        if mask >> bit & 1:
            row[variable] = 1
    return tuple(row)


def c_mixed_candidates(
    groups: dict[tuple[tuple[int, ...], ...], tuple[Rho, ...]]
) -> tuple[list[dict[str, object]], list[tuple[Rho, int, tuple[int, ...]]]]:
    exact_rows = [
        ((1, 1, 1, 1, 0, 0, 0), 1),
        ((1, 0, 0, 0, 1, 1, 1), 1),
        ((0, 1, 1, 0, 1, 0, 0), -4),
    ]
    summaries: list[dict[str, object]] = []
    expanded: list[tuple[Rho, int, tuple[int, ...]]] = []
    for patterns, all_targets in sorted(groups.items()):
        targets = tuple(target for target in all_targets if target != (0, 0))
        if not targets:
            continue
        membership_rows = [
            (side, mask, c_membership_row(side, mask))
            for side, masks in enumerate(patterns)
            for mask in masks
        ]
        chosen = independent_extension_rows(exact_rows, membership_rows)
        assert len(chosen) == 4
        alphas: Iterable[int] = range(P)
        if any(0 in masks for masks in patterns):
            alphas = (1, 2, 3)
        solutions: set[tuple[int, tuple[int, ...]]] = set()
        for alpha in alphas:
            allowed = allowed_target_q_values(alpha)
            for right_sides in itertools.product(sorted(allowed), repeat=len(chosen)):
                candidate = solve_unique_linear_system(
                    exact_rows
                    + [
                        (row, rhs)
                        for (_, _, row), rhs in zip(chosen, right_sides)
                    ],
                    7,
                )
                if candidate is None:
                    continue
                if all(
                    dot(c_membership_row(side, mask), candidate) in allowed
                    for side, masks in enumerate(patterns)
                    for mask in masks
                ):
                    solutions.add((alpha, candidate))
        if not solutions:
            continue
        ordered_solutions = sorted(solutions)
        summaries.append(
            {
                "target_count": len(targets),
                "first_target": signed_rho(targets[0]),
                "defect_mask_counts": [len(masks) for masks in patterns],
                "independent_membership_rows_after_three_first_moments": len(chosen),
                "mixed_compatible_q_alpha_count_per_target": len(ordered_solutions),
            }
        )
        for target in targets:
            for alpha, candidate in ordered_solutions:
                expanded.append((target, alpha, candidate))
    expanded.sort()
    return summaries, expanded


def c_q_labels(candidate: tuple[int, ...]) -> dict[str, int]:
    k, q_f, q_t, q_xs, q_e, q_xh, q_xd = candidate
    result = {
        "C:K:g:q_spike": k,
        "u_f": q_f,
        "u_t": q_t,
        "C:L:x_s": q_xs,
        "u_e": q_e,
        "C:L:x_h": q_xh,
        "C:L:x_d": q_xd,
        # The common endpoint compensation is forced by sigma_q(W)=1.
        "C:L:c_e_1": (k - 1) % P,
    }
    return result


class SparseGauss:
    """Incremental exact Gaussian elimination over F_p."""

    def __init__(self) -> None:
        self.basis: dict[int, tuple[dict[int, int], int, str]] = {}
        self.rank = 0
        self.conflict: dict[str, object] | None = None

    def add(self, row: dict[int, int], rhs: int, source: str) -> bool:
        reduced = {index: value % P for index, value in row.items() if value % P}
        value = rhs % P
        while reduced:
            pivot = min(reduced)
            coefficient = reduced[pivot]
            if pivot not in self.basis:
                inverse = pow(coefficient, -1, P)
                normalized = {
                    index: entry * inverse % P for index, entry in reduced.items()
                }
                normalized_rhs = value * inverse % P
                self.basis[pivot] = (normalized, normalized_rhs, source)
                self.rank += 1
                return True
            basis_row, basis_rhs, _ = self.basis[pivot]
            del reduced[pivot]
            for index, entry in basis_row.items():
                if index == pivot:
                    continue
                new_value = (reduced.get(index, 0) - coefficient * entry) % P
                if new_value:
                    reduced[index] = new_value
                else:
                    reduced.pop(index, None)
            value = (value - coefficient * basis_rhs) % P
        if value:
            self.conflict = {
                "trigger_source": source,
                "nonzero_reduced_rhs": signed(value),
                "rank_before_conflict": self.rank,
            }
            return False
        return True


def enumerate_qrho_short_profiles(
    types: list[tuple[tuple[int, int, int], tuple[str, ...]]]
) -> tuple[list[tuple[tuple[int, ...], int, int]], int]:
    counts = [0] * len(types)
    profiles: list[tuple[tuple[int, ...], int, int]] = []
    visited = 0

    def visit(
        index: int,
        remaining: int,
        y_size: int,
        q_sum: int,
        rho_1_sum: int,
        rho_2_sum: int,
    ) -> None:
        nonlocal visited
        if index == len(types):
            visited += 1
            if rho_1_sum % P or rho_2_sum % P:
                return
            x_needed = (-q_sum) % P
            length = y_size + x_needed
            if x_needed <= X_COUNT and 1 <= length <= 8:
                profiles.append((tuple(counts), x_needed, length))
            return
        (q_value, rho_1, rho_2), positions = types[index]
        for multiplicity in range(min(len(positions), remaining) + 1):
            counts[index] = multiplicity
            visit(
                index + 1,
                remaining - multiplicity,
                y_size + multiplicity,
                q_sum + multiplicity * q_value,
                rho_1_sum + multiplicity * rho_1,
                rho_2_sum + multiplicity * rho_2,
            )
        counts[index] = 0

    visit(0, 8, 0, 0, 0, 0)
    profiles.sort(key=lambda item: (item[2], item[1], item[0]))
    return profiles, visited


def rigid_height_rejection(
    model: Model, target: Rho, alpha: int, candidate: tuple[int, ...]
) -> dict[str, object]:
    """Reject a C mixed survivor using only forced-height short lengths.

    Lengths 2 and 3 have forced height 1, and length 8 has forced height 3.
    For a q/rho count profile, all literal realizations obey the same equation.
    One representative equation plus the swap differences inside every used
    non-full type generate exactly the affine span of all those equations.
    """

    q = {position: 0 for position in model.W}
    q.update(c_q_labels(candidate))
    p_left = "P:left"
    p_right = "P:right"
    packing = frozenset({p_left, p_right})
    all_positions = tuple(sorted(model.W)) + (p_left, p_right)
    rho = dict(model.rho)
    rho[p_left] = smul(-1, target)
    rho[p_right] = target
    q[p_left] = alpha % P
    q[p_right] = (3 - alpha) % P

    assert sum(q[position] for position in model.U) % P == -4 % P
    assert sum(q[position] for position in model.W) % P == 1
    assert sum(q[position] for position in packing) % P == 3
    assert all(
        sum(q[position] for position in endpoint) % P == 0
        for endpoint in model.endpoints.values()
    )
    assert all(
        sum(q[position] for position in q_set) % P == 1
        for q_set in model.q_sets.values()
    )

    grouped: dict[tuple[int, int, int], list[str]] = defaultdict(list)
    for position in all_positions:
        grouped[(q[position] % P, rho[position][0], rho[position][1])].append(position)
    types = [
        (label, tuple(sorted(positions)))
        for label, positions in sorted(grouped.items())
    ]
    profiles, count_vectors_visited = enumerate_qrho_short_profiles(types)
    variable = {position: index for index, position in enumerate(all_positions)}
    gauss = SparseGauss()

    def add_position_set(positions: Iterable[str], rhs: int, source: str) -> bool:
        return gauss.add(
            dict(Counter(variable[position] for position in positions)), rhs, source
        )

    exact_equations = [
        ("FIRST_MOMENT_U", model.U, 3),
        ("FIRST_MOMENT_W", model.W, 1),
        ("FIRST_MOMENT_P", packing, -1),
    ] + [
        (f"ENDPOINT_{name}", endpoint, 3)
        for name, endpoint in sorted(model.endpoints.items())
    ]
    for source, positions, rhs in exact_equations:
        if not add_position_set(positions, rhs, source):
            assert gauss.conflict is not None
            return {
                "decision": "RIGID_HEIGHT_LINEAR_CONTRADICTION",
                "q_rho_type_count": len(types),
                "short_profile_count": len(profiles),
                "count_vectors_visited": count_vectors_visited,
                "rigid_profile_equation_count": 0,
                "swap_equation_count": 0,
                "conflict": gauss.conflict,
            }

    swap_types: set[int] = set()
    rigid_profile_count = 0
    for profile_index, (profile_counts, _x_needed, length) in enumerate(profiles):
        if length == 1:
            return {
                "decision": "FORBIDDEN_QUOTIENT_ZERO_LENGTH_ONE",
                "q_rho_type_count": len(types),
                "short_profile_count": len(profiles),
                "count_vectors_visited": count_vectors_visited,
                "rigid_profile_equation_count": rigid_profile_count,
                "swap_equation_count": 0,
                "conflict": {
                    "trigger_source": f"SHORT_PROFILE_{profile_index}_LENGTH_1",
                    "nonzero_reduced_rhs": None,
                    "rank_before_conflict": gauss.rank,
                },
            }
        if length not in (2, 3, 8):
            continue
        rhs = 1 if length in (2, 3) else 3
        representative: list[str] = []
        for type_index, multiplicity in enumerate(profile_counts):
            positions = types[type_index][1]
            representative.extend(positions[:multiplicity])
            if 0 < multiplicity < len(positions):
                swap_types.add(type_index)
        rigid_profile_count += 1
        if not add_position_set(
            representative,
            rhs,
            f"SHORT_PROFILE_{profile_index}_LENGTH_{length}_REPRESENTATIVE",
        ):
            assert gauss.conflict is not None
            return {
                "decision": "RIGID_HEIGHT_LINEAR_CONTRADICTION",
                "q_rho_type_count": len(types),
                "short_profile_count": len(profiles),
                "count_vectors_visited": count_vectors_visited,
                "rigid_profile_equation_count": rigid_profile_count,
                "swap_equation_count": 0,
                "conflict": gauss.conflict,
            }

    swap_equation_count = 0
    for type_index in sorted(swap_types):
        positions = types[type_index][1]
        anchor = positions[0]
        for position in positions[1:]:
            swap_equation_count += 1
            if not gauss.add(
                {variable[position]: 1, variable[anchor]: -1},
                0,
                f"SHORT_PROFILE_SWAP_TYPE_{type_index}_{position}",
            ):
                assert gauss.conflict is not None
                return {
                    "decision": "RIGID_HEIGHT_LINEAR_CONTRADICTION",
                    "q_rho_type_count": len(types),
                    "short_profile_count": len(profiles),
                    "count_vectors_visited": count_vectors_visited,
                    "rigid_profile_equation_count": rigid_profile_count,
                    "swap_equation_count": swap_equation_count,
                    "conflict": gauss.conflict,
                }
    return {
        "decision": "RIGID_HEIGHT_LINEAR_SYSTEM_SURVIVOR",
        "q_rho_type_count": len(types),
        "short_profile_count": len(profiles),
        "count_vectors_visited": count_vectors_visited,
        "rigid_profile_equation_count": rigid_profile_count,
        "swap_equation_count": swap_equation_count,
        "rank": gauss.rank,
    }


def audit_model_c(model: Model) -> dict[str, object]:
    defect_orders = {
        "C:H_singleton_e": (
            "C:K:g:q_spike",
            "u_f",
            "u_t",
            "C:L:x_s",
        ),
        "C:H_doubleton_ft": (
            "C:K:g:q_spike",
            "u_e",
            "C:L:x_h",
            "C:L:x_d",
        ),
    }
    target_data = make_target_data(model, defect_orders)
    groups = target_mask_groups(target_data)
    group_summaries, mixed_survivors = c_mixed_candidates(groups)
    assert len(groups) == 54
    assert len(group_summaries) == 8
    assert len(mixed_survivors) == 9798

    outcome_counter: Counter[str] = Counter()
    conflict_counter: Counter[str] = Counter()
    samples: list[dict[str, object]] = []
    semantic_rows: list[object] = []
    survivors_after_rigid_height: list[tuple[Rho, int, tuple[int, ...]]] = []
    for target, alpha, candidate in mixed_survivors:
        outcome = rigid_height_rejection(model, target, alpha, candidate)
        decision = str(outcome["decision"])
        outcome_counter[decision] += 1
        if decision.endswith("SURVIVOR"):
            survivors_after_rigid_height.append((target, alpha, candidate))
        conflict = outcome.get("conflict")
        trigger = str(conflict["trigger_source"]) if isinstance(conflict, dict) else "NONE"
        conflict_counter[trigger.split("_")[0]] += 1
        semantic_rows.append(
            [
                list(target),
                alpha,
                list(candidate),
                decision,
                outcome.get("q_rho_type_count"),
                outcome.get("short_profile_count"),
                outcome.get("rigid_profile_equation_count"),
                outcome.get("swap_equation_count"),
                conflict,
            ]
        )
        if len(samples) < 12:
            samples.append(
                {
                    "packing_target_minus_rho_P_left": signed_rho(target),
                    "packing_q_left_alpha": signed(alpha),
                    "q_variables_k_f_t_xs_e_xh_xd": [signed(value) for value in candidate],
                    "outcome": outcome,
                }
            )
    assert not survivors_after_rigid_height
    return {
        "sparse_support_definition": {
            "free_q_positions": [
                "C:K:g:q_spike",
                "u_f",
                "u_t",
                "C:L:x_s",
                "u_e",
                "C:L:x_h",
                "C:L:x_d",
            ],
            "forced_common_compensation": "q(C:L:c_e_1)=q(C:K:g:q_spike)-1",
            "all_other_W_q_coordinates": 0,
            "packing_rho": "ordered pair (-target,target), for every nonzero target in C_233^2",
            "packing_q": "ordered pair (alpha,3-alpha), for every alpha in C_233",
            "first_moment_q_equations": [
                "k+f+t+x_s=1",
                "k+e+x_h+x_d=1",
                "e+f+t=-4",
            ],
            "q_first_moment_dimension": 4,
        },
        "raw_labelled_assignment_denominator_before_mixed": str(
            P**4 * (P**2 - 1) * P
        ),
        "target_mask_group_count_including_zero_target": len(groups),
        "zero_base_reachable_sizes": {
            row.q_set_name: len(row.zero_base_reachable) for row in target_data
        },
        "mixed_surviving_group_summaries": group_summaries,
        "mixed_survivor_count": len(mixed_survivors),
        "mixed_survivor_semantic_digest_sha256": canonical_hash(
            [[list(target), alpha, list(candidate)] for target, alpha, candidate in mixed_survivors]
        ),
        "rigid_height_outcome_counts": dict(sorted(outcome_counter.items())),
        "coarse_conflict_trigger_counts": dict(sorted(conflict_counter.items())),
        "rigid_height_survivor_count": len(survivors_after_rigid_height),
        "all_mixed_survivors_rejected_before_flexible_short_families": True,
        "elimination_semantic_digest_sha256": canonical_hash(semantic_rows),
        "first_elimination_samples": samples,
    }


def d_q_labels(parameter: int) -> dict[str, int]:
    # Endpoint sums, U=-4, and W=1 reduce the author's six-position support to
    # this single parameter c=q(d_y).
    return {
        "u_e": -4 % P,
        "d_p23_g": -parameter % P,
        "d_y": parameter % P,
        "d_p13_h_001": (4 - parameter) % P,
        "d_p12_g1": (4 - parameter) % P,
        "d_k_g_001": (2 * parameter - 3) % P,
    }


def audit_model_d(model: Model) -> dict[str, object]:
    all_support = (
        "u_e",
        "d_p23_g",
        "d_p13_h_001",
        "d_p12_g1",
        "d_k_g_001",
    )
    defect_orders = {
        name: tuple(position for position in all_support if position in q_set)
        for name, q_set in model.q_sets.items()
    }
    target_data = make_target_data(model, defect_orders)
    groups = target_mask_groups(target_data)
    assert len(groups) == 21
    survivor_rows: list[object] = []
    pattern_parameter_checks = 0
    nonzero_target_parameter_checks = 0
    for parameter in range(P):
        q = d_q_labels(parameter)
        assert sum(q.get(position, 0) for position in model.U) % P == -4 % P
        assert sum(q.get(position, 0) for position in model.W) % P == 1
        assert all(
            sum(q.get(position, 0) for position in endpoint) % P == 0
            for endpoint in model.endpoints.values()
        )
        for patterns, all_targets in groups.items():
            targets = tuple(target for target in all_targets if target != (0, 0))
            if not targets:
                continue
            pattern_parameter_checks += 1
            nonzero_target_parameter_checks += len(targets)
            target_values: set[int] = set()
            for row, masks in zip(target_data, patterns):
                target_values.update(
                    sum(
                        q.get(position, 0)
                        for bit, position in enumerate(row.defects)
                        if mask >> bit & 1
                    )
                    % P
                    for mask in masks
                )
            alphas = compatible_alphas(target_values)
            if alphas:
                survivor_rows.append(
                    {
                        "parameter": parameter,
                        "target_count": len(targets),
                        "first_target": list(targets[0]),
                        "target_q_values": sorted(target_values),
                        "compatible_alphas": list(alphas),
                    }
                )
    assert not survivor_rows
    assert nonzero_target_parameter_checks == P * (P * P - 1)
    return {
        "sparse_support_definition": {
            "possibly_nonzero_W_q_positions": [
                "u_e",
                "d_p23_g",
                "d_y",
                "d_p13_h_001",
                "d_p12_g1",
                "d_k_g_001",
            ],
            "all_other_W_q_coordinates": 0,
            "one_parameter_formula": {
                position: f"{signed(value)} at parameter c=0; see script d_q_labels(c)"
                for position, value in d_q_labels(0).items()
            },
            "packing_rho": "ordered pair (-target,target), for every nonzero target in C_233^2",
            "packing_q": "ordered pair (alpha,3-alpha), for every alpha in C_233",
            "q_first_moment_dimension": 1,
        },
        "raw_labelled_assignment_denominator_before_mixed": str(
            P * (P**2 - 1) * P
        ),
        "target_mask_group_count_including_zero_target": len(groups),
        "zero_base_reachable_sizes": {
            row.q_set_name: len(row.zero_base_reachable) for row in target_data
        },
        "pattern_parameter_checks": pattern_parameter_checks,
        "nonzero_target_parameter_checks": nonzero_target_parameter_checks,
        "mixed_survivor_count": len(survivor_rows),
        "mixed_survivors": survivor_rows,
        "all_candidates_rejected_by_complete_mixed_target_fibres": True,
    }


def build_report() -> dict[str, object]:
    model_c = build_model_c()
    model_d = build_model_d()
    report: dict[str, object] = {
        "schema": "unique_tail_p233_doubleton_CD_relabel_exhaustion_v1",
        "status": (
            "TWO_CANONICAL_SPARSE_DEFECT_RELABEL_FAMILIES_EXHAUSTED/"
            "FIXED_RHO_SKELETON_FULL_RELABEL_OPEN/GLOBAL_INCOMPLETE"
        ),
        "p": P,
        "fixed_rho_atom_rechecks": {
            "model_C": verify_simple_atoms(model_c),
            "model_D": verify_simple_atoms(model_d),
        },
        "model_C": audit_model_c(model_c),
        "model_D": audit_model_d(model_d),
        "gate_order_and_vacuity": {
            "model_C": [
                "first moments and fixed maximal rho-atoms",
                "all mixed P--Q target fibres, hence the complete type-(3) long-complement internal subset-sum criterion",
                "all literal global automatic short blocks of rigid lengths 2, 3, and 8",
                "zero candidates remain before flexible length-4..7 families, disjoint-short incidence, or actual-label multiplicity",
            ],
            "model_D": [
                "first moments and fixed maximal rho-atoms",
                "all mixed P--Q target fibres",
                "zero candidates remain before height, global-short, disjoint-short incidence, or actual-label multiplicity",
            ],
            "later_gate_survivor_denominator": 0,
            "meaning": (
                "The later gates are vacuous only inside the two frozen sparse-support families, "
                "because every candidate has already failed a necessary earlier gate."
            ),
        },
        "strictly_checked_scope": [
            "the literal fixed Model-C and Model-D rho incidences reconstructed in this script",
            "the simple-form maximal-rho-atom equations for every displayed Q_H",
            "every field assignment in the two explicitly frozen sparse q-support families",
            "every nonzero ordered two-position packing rho direction and every packing q split alpha,3-alpha",
            "exact bounded rho reachability outside the potential q-defect positions",
            "all mixed P--Q_H target subsets, with the second packing singleton supplied by complement symmetry",
            "for all 9798 Model-C mixed survivors, all literal realizations of every quotient-zero rigid short profile of length 2, 3, or 8",
            "arbitrary literal-position heights subject to the named first moments; heights are not assumed constant on q/rho types",
        ],
        "open_or_omitted_scope": [
            "q relabellings whose nonzero support is not contained in the displayed canonical sparse-defect supports",
            "moving the Model-C common q compensation from the chosen c_e clone to a rho-inequivalent common position",
            "a proof that every mixed-compatible q labelling is gauge-equivalent to one of the two sparse-support families",
            "therefore all q/height/P relabellings of either fixed rho skeleton",
            "all other incidence skeletons, all outer shards, the fixed-p slice, and global A_p",
        ],
        "first_irreducible_frontier": (
            "Prove a support-compression theorem for mixed-compatible q labels on a Property-B maximal rho-atom, "
            "or enlarge the exact defect support.  Without that theorem, this finite exhaustion cannot be promoted "
            "to fixed-Model-C/D rho-skeleton UNSAT."
        ),
        "conclusion": (
            "The two canonical sparse-defect relabel families contain no survivor.  Model D dies at the mixed long-complement gate; "
            "Model C has exactly 9798 mixed survivors and every one dies already in the rigid global-short height equations. "
            "The unrestricted fixed-skeleton relabel problem remains open."
        ),
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    with REPORT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(
        "PASS Model C exact sparse-family exhaustion:",
        report["model_C"]["mixed_survivor_count"],
        "mixed survivors,",
        report["model_C"]["rigid_height_survivor_count"],
        "after rigid height",
    )
    print(
        "PASS Model D exact sparse-family exhaustion:",
        report["model_D"]["mixed_survivor_count"],
        "mixed survivors",
    )
    print("CERTIFICATE", report["certificate_sha256"])
    print("BOUNDARY unrestricted fixed-rho-skeleton relabelling remains open")


if __name__ == "__main__":
    main()
