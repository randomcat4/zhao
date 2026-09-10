#!/usr/bin/env python3
"""Unified q-lift boundary for relaxed mixed-trace Models N and C.

The script is standalone and position-sensitive.  It proves a short universal
exclusion for the fixed Model N.  For the fixed Model C it constructs one
literal lift to C_233^4 and exhausts (i) every rho-zero subset internal to
either displayed endpoint, including its available X-completion, and (ii) all
P-mixed target fibres for both displayed Q_H and both singleton choices in P.

The Model-C witness is deliberately RELAXED.  In particular it is not a global
automatic-short-block witness: an explicit quotient-zero length-three block
outside the endpoints has the wrong actual sum, and is recorded as the exact
next boundary rather than hidden.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json
from pathlib import Path


P = 233
Actual = tuple[int, int, int, int]  # (a-height, q-axis, rho-e, rho-f)
Rho = tuple[int, int]


def vadd(*vectors: tuple[int, ...]) -> tuple[int, ...]:
    if not vectors:
        raise ValueError("vadd needs at least one vector")
    dimension = len(vectors[0])
    assert all(len(vector) == dimension for vector in vectors)
    return tuple(sum(vector[index] for vector in vectors) % P for index in range(dimension))


def vmul(coefficient: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * coordinate % P for coordinate in vector)


def signed(vector: tuple[int, ...]) -> list[int]:
    return [coordinate if coordinate <= P // 2 else coordinate - P for coordinate in vector]


A: Actual = (1, 0, 0, 0)
X: Actual = (0, 1, 0, 0)
E: Rho = (1, 0)
F: Rho = (0, 1)
T: Rho = (-1 % P, -1 % P)
G: Rho = T
H: Rho = (-2 % P, -1 % P)  # t-e


def actual(height: int, q_axis: int, rho: Rho) -> Actual:
    return (height % P, q_axis % P, rho[0], rho[1])


def rho_of(label: Actual) -> Rho:
    return (label[2], label[3])


def quotient_of(label: Actual) -> tuple[int, int, int]:
    return (label[1], label[2], label[3])


def sum_positions(labels: dict[str, Actual], positions: set[str] | frozenset[str]) -> Actual:
    if not positions:
        return (0, 0, 0, 0)
    return vadd(*(labels[position] for position in positions))  # type: ignore[return-value]


def add_clones(
    labels: dict[str, Actual], prefix: str, count: int, label: Actual
) -> set[str]:
    positions = {f"{prefix}:{index:03d}" for index in range(1, count + 1)}
    assert not (positions & set(labels))
    labels.update({position: label for position in positions})
    return positions


def compressed(labels: dict[str, Actual], positions: set[str] | frozenset[str]) -> list[tuple[Actual, int]]:
    return sorted(Counter(labels[position] for position in positions).items())


def bounded_zero_vectors(
    atoms: list[tuple[tuple[int, ...], int]], target: tuple[int, ...]
) -> list[list[int]]:
    answers: list[list[int]] = []
    for choice in itertools.product(*(range(bound + 1) for _, bound in atoms)):
        total = tuple(
            sum(count * atom[index] for count, (atom, _) in zip(choice, atoms)) % P
            for index in range(len(target))
        )
        if total == target:
            answers.append(list(choice))
    return answers


def model_n_symbolic_certificate() -> dict[str, object]:
    """The equal-sum endpoint equations force a second positive-core F3 tail."""
    U = frozenset({"u_e", "u_f", "u_t"})
    alternative = frozenset({"u_e", "x_f", "x_t"})
    H_s = alternative | {"y", "e_prime", "e_double_prime", "c"}
    H_ef = frozenset({"u_e", "u_f", "x_t", "y", "e_prime", "e_double_prime", "c"})
    H_et = frozenset({"u_e", "u_t", "x_f", "y", "e_prime", "e_double_prime", "c"})

    # All three endpoint sums are the same actual vector 3a.  Cancelling their
    # literal common positions gives these label equalities in the actual group.
    symmetric_difference_s_ef = (sorted(H_s - H_ef), sorted(H_ef - H_s))
    symmetric_difference_s_et = (sorted(H_s - H_et), sorted(H_et - H_s))
    assert symmetric_difference_s_ef == (["x_f"], ["u_f"])
    assert symmetric_difference_s_et == (["x_t"], ["u_t"])
    assert alternative != U
    assert len(alternative) == len(U) == 3
    return {
        "endpoint_equalities": [
            {
                "comparison": "H_s versus H_ef",
                "cancelled_positions_leave": ["x_f", "u_f"],
                "forced_actual_label_equality": "gamma(x_f)=gamma(u_f)",
            },
            {
                "comparison": "H_s versus H_et",
                "cancelled_positions_leave": ["x_t", "u_t"],
                "forced_actual_label_equality": "gamma(x_t)=gamma(u_t)",
            },
        ],
        "unique_tail": sorted(U),
        "forced_second_tail": sorted(alternative),
        "tails_are_distinct_literal_sets": True,
        "core_count": 4,
        "block_length": 7,
        "forced_sum": "sigma(X_4 union {u_e,x_f,x_t})=3a",
        "conclusion": "UNSAT for every actual lift satisfying the unique positive-core F3-tail interface",
        "independent_of": [
            "the q-coordinate choices",
            "the packing P",
            "the common kernel labels",
            "the multiplicity cap",
        ],
    }


def build_model_c_lift() -> dict[str, object]:
    labels: dict[str, Actual] = {}

    # K: 231 copies in each rho fibre.  The small splittings make every actual
    # value occur at most 229 times while fixing sigma_a(K)=-4 and sigma_q(K)=1.
    k_g_ordinary = add_clones(labels, "C:K:g:ordinary", 229, actual(0, 0, G))
    labels["C:K:g:height2"] = actual(2, 0, G)
    labels["C:K:g:q_spike"] = actual(0, 1, G)
    k_g = k_g_ordinary | {"C:K:g:height2", "C:K:g:q_spike"}

    k_h_ordinary = add_clones(labels, "C:K:h:ordinary", 229, actual(0, 0, H))
    labels["C:K:h:height1"] = actual(1, 0, H)
    labels["C:K:h:height226"] = actual(226, 0, H)
    k_h = k_h_ordinary | {"C:K:h:height1", "C:K:h:height226"}
    K = frozenset(k_g | k_h)
    assert len(K) == 462

    # Literal local positions.  These shared q/height choices close every
    # rho-zero subset internal to either displayed endpoint; see the exhaustive
    # endpoint-internal audit below.
    rho_xs = vadd(H, vmul(3, G))  # type: ignore[assignment]
    rho_xd = vadd(G, vmul(2, H))  # type: ignore[assignment]
    labels.update(
        {
            "u_e": actual(2, -1, E),
            "u_f": actual(0, -3, F),
            "u_t": actual(1, 0, T),
            "C:L:x_s": actual(1, 3, rho_xs),  # type: ignore[arg-type]
            "C:L:x_h": actual(0, 1, H),
            "C:L:x_d": actual(0, 0, rho_xd),  # type: ignore[arg-type]
            "C:L:y": actual(0, 0, (4, 3)),
            "C:L:c_e_1": actual(1, 0, E),
            "C:L:c_e_2": actual(1, 0, E),
            "C:L:c_f": actual(-1, 0, F),
        }
    )
    tails = frozenset({"u_e", "u_f", "u_t"})
    block_s = frozenset({"u_t", "u_f", "C:L:x_s"})
    block_d = frozenset({"C:L:x_h", "u_e", "C:L:x_d"})
    common = frozenset({"C:L:y", "C:L:c_e_1", "C:L:c_e_2", "C:L:c_f"})
    L = frozenset(tails | block_s | block_d | common)
    # block_s/block_d both include tail positions already in tails.
    assert len(L) == 10
    endpoints = {
        "C:H_singleton_e": block_d | common,
        "C:H_doubleton_ft": block_s | common,
    }

    # Type-(3), |P|=2, kappa=1 packing: rho labels are opposite, q sum 3,
    # and actual sum is 3x-a.
    rho_p_left = vmul(-1, G)
    labels["P:left"] = actual(0, 2, rho_p_left)  # type: ignore[arg-type]
    labels["P:right"] = actual(-1, 1, G)
    packing = frozenset({"P:left", "P:right"})

    W = frozenset(K | L)
    Y = frozenset(W | packing)
    q_sets = {
        endpoint_name: frozenset(K | (L - endpoint))
        for endpoint_name, endpoint in endpoints.items()
    }
    return {
        "labels": labels,
        "K": K,
        "L": L,
        "W": W,
        "Y": Y,
        "tails": tails,
        "block_s": block_s,
        "block_d": block_d,
        "common": common,
        "endpoints": endpoints,
        "packing": packing,
        "q_sets": q_sets,
    }


def rho_atom_check(labels: dict[str, Actual], positions: frozenset[str]) -> dict[str, object]:
    counts = sorted(Counter(rho_of(labels[position]) for position in positions).items())
    zeros = bounded_zero_vectors(counts, (0, 0))
    full = [count for _, count in counts]
    assert zeros == [[0] * len(counts), full]
    return {
        "compressed_rho_multiplicities": [
            {"rho": signed(label), "count": count} for label, count in counts
        ],
        "zero_submultisets": zeros,
        "minimal_zero_sum": True,
    }


def mixed_target_values(
    labels: dict[str, Actual], q_positions: frozenset[str], target_rho: Rho
) -> dict[str, object]:
    quotient_counts = sorted(
        Counter(quotient_of(labels[position]) for position in q_positions).items()
    )
    target_values: set[int] = set()
    witness_count_vectors = 0
    for choice in itertools.product(*(range(bound + 1) for _, bound in quotient_counts)):
        rho_sum = (
            sum(count * label[1] for count, (label, _) in zip(choice, quotient_counts)) % P,
            sum(count * label[2] for count, (label, _) in zip(choice, quotient_counts)) % P,
        )
        if rho_sum != target_rho:
            continue
        witness_count_vectors += 1
        q_sum = sum(
            count * label[0] for count, (label, _) in zip(choice, quotient_counts)
        ) % P
        target_values.add(q_sum)
    assert witness_count_vectors > 0
    return {
        "target_rho": signed(target_rho),
        "reachable_q_axis_sums": sorted(target_values),
        "compressed_count_vector_count": witness_count_vectors,
    }


def allowed_actual_heights(length: int) -> set[int]:
    allowed: set[int] = set()
    if 2 <= length <= 6:
        allowed.add(1)
    if 4 <= length <= 7:
        allowed.add(2)
    if 6 <= length <= 8:
        allowed.add(3)
    return allowed


def endpoint_internal_closure(model: dict[str, object]) -> dict[str, object]:
    """Exhaust every rho-zero subset of each displayed seven-position H.

    For a subset S, its unique possible X-completion uses
    c=-sigma_q(S) mod p copies.  If c<=p-4, the exact slice requires either an
    allowed block of length at most eight or (for lengths 9..2p+2) a
    contradiction.  Thus this is more than a hand-picked list of short blocks:
    it checks the complete endpoint-internal closure.
    """
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    endpoints: dict[str, frozenset[str]] = model["endpoints"]  # type: ignore[assignment]
    rows: list[dict[str, object]] = []
    short_rows: list[dict[str, object]] = []

    for endpoint_name, endpoint in sorted(endpoints.items()):
        ordered = sorted(endpoint)
        for size in range(len(ordered) + 1):
            for subset_tuple in itertools.combinations(ordered, size):
                subset = frozenset(subset_tuple)
                subtotal = sum_positions(labels, subset) if subset else (0, 0, 0, 0)
                if subtotal[2:] != (0, 0):
                    continue
                q_sum = subtotal[1]
                height_sum = subtotal[0]
                x_needed = (-q_sum) % P
                x_available = x_needed <= P - 4
                total_length = size + x_needed if x_available else None

                if not subset:
                    decision = "EMPTY"
                elif not x_available:
                    decision = "NO_AVAILABLE_X_COMPLETION"
                elif total_length is not None and total_length <= 8:
                    allowed = allowed_actual_heights(total_length)
                    assert height_sum in allowed
                    family = f"F{height_sum}"
                    # A competing positive-core F3 would already contradict
                    # the unique-tail interface.  None occurs in this closure.
                    assert not (family == "F3" and x_needed > 0)
                    decision = f"ALLOWED_SHORT_{family}"
                    short_rows.append(
                        {
                            "endpoint": endpoint_name,
                            "subset": sorted(subset),
                            "subset_size": size,
                            "x_needed": x_needed,
                            "total_length": total_length,
                            "actual_height": height_sum,
                            "family": family,
                        }
                    )
                elif total_length is not None and total_length <= 2 * P + 2:
                    raise AssertionError(
                        f"endpoint-internal middle-gap block: {endpoint_name}, {sorted(subset)}"
                    )
                else:
                    decision = "OUTSIDE_CHECKED_RANGE"

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
                        "decision": decision,
                    }
                )

    decisions = Counter(row["decision"] for row in rows)
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
    assert len(short_rows) == 13
    assert sum(row["is_full_endpoint"] for row in rows) == 2
    assert all(
        row["x_needed"] == 0
        for row in short_rows
        if row["family"] == "F3"
    )
    return {
        "rho_zero_subset_rows": rows,
        "row_count_including_empty": len(rows),
        "nonempty_row_count": len(rows) - 2,
        "induced_allowed_short_block_count": len(short_rows),
        "decision_counts": dict(sorted(decisions.items())),
        "all_endpoint_internal_rho_zero_subsets_exhausted": True,
        "all_available_X_completions_pass_short_windows": True,
        "no_endpoint_internal_middle_gap_block": True,
        "no_endpoint_internal_competing_positive_core_F3": True,
    }


def global_short_boundary(model: dict[str, object]) -> dict[str, object]:
    """Record a literal global short-block failure of this particular lift."""
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    positions = frozenset(
        {"C:L:c_e_1", "C:K:g:height2", "C:L:c_f"}
    )
    total = sum_positions(labels, positions)
    assert total == vmul(2, A)
    assert quotient_of(total) == (0, 0, 0)
    assert len(positions) == 3
    assert allowed_actual_heights(3) == {1}
    assert total[0] not in allowed_actual_heights(3)
    return {
        "positions": sorted(positions),
        "literal_actual_labels": {
            position: signed(labels[position]) for position in sorted(positions)
        },
        "length": 3,
        "quotient_sum": [0, 0, 0],
        "actual_sum": signed(total),
        "required_actual_height_set": [1],
        "passes": False,
        "meaning": (
            "this explicit Model-C lift is not SAT for the global automatic-short-block "
            "interface; existence of a different globally short-compatible lift is not decided"
        ),
    }


def audit_model_c() -> dict[str, object]:
    model = build_model_c_lift()
    labels: dict[str, Actual] = model["labels"]  # type: ignore[assignment]
    K: frozenset[str] = model["K"]  # type: ignore[assignment]
    L: frozenset[str] = model["L"]  # type: ignore[assignment]
    W: frozenset[str] = model["W"]  # type: ignore[assignment]
    Y: frozenset[str] = model["Y"]  # type: ignore[assignment]
    tails: frozenset[str] = model["tails"]  # type: ignore[assignment]
    packing: frozenset[str] = model["packing"]  # type: ignore[assignment]
    endpoints: dict[str, frozenset[str]] = model["endpoints"]  # type: ignore[assignment]
    q_sets: dict[str, frozenset[str]] = model["q_sets"]  # type: ignore[assignment]

    assert K.isdisjoint(L)
    assert len(K) == 462 and len(L) == 10 and len(W) == 472 and len(Y) == 474
    assert W == K | L and Y == W | packing
    assert sum_positions(labels, tails) == vadd(vmul(3, A), vmul(-4, X))
    assert sum_positions(labels, packing) == vadd(vmul(3, X), vmul(-1, A))
    assert sum_positions(labels, W) == vadd(X, A)
    assert sum_positions(labels, Y) == vmul(4, X)
    assert all(len(endpoint) == 7 for endpoint in endpoints.values())
    assert all(sum_positions(labels, endpoint) == vmul(3, A) for endpoint in endpoints.values())
    assert set.intersection(*(set(q_set) for q_set in q_sets.values())) == set(K)
    assert all(len(q_set) == 465 for q_set in q_sets.values())
    assert all(
        sum_positions(labels, q_set) == vadd(X, vmul(-2, A))
        for q_set in q_sets.values()
    )

    atom_rows = {
        endpoint_name: rho_atom_check(labels, q_set)
        for endpoint_name, q_set in q_sets.items()
    }

    p_left = labels["P:left"]
    p_right = labels["P:right"]
    assert rho_of(p_left) != (0, 0)
    assert rho_of(p_right) == vmul(-1, rho_of(p_left))
    assert (p_left[1] + p_right[1]) % P == 3
    mixed_rows: dict[str, object] = {}
    for endpoint_name, q_set in q_sets.items():
        left_target = mixed_target_values(labels, q_set, vmul(-1, rho_of(p_left)))  # type: ignore[arg-type]
        right_target = mixed_target_values(labels, q_set, vmul(-1, rho_of(p_right)))  # type: ignore[arg-type]
        left_combined = sorted((p_left[1] + value) % P for value in left_target["reachable_q_axis_sums"])
        right_combined = sorted((p_right[1] + value) % P for value in right_target["reachable_q_axis_sums"])
        assert set(left_combined) <= {1, 2, 3}
        assert set(right_combined) <= {1, 2, 3}
        mixed_rows[endpoint_name] = {
            "P_left": left_target,
            "P_left_combined_allowed_coefficients": left_combined,
            "P_right": right_target,
            "P_right_combined_allowed_coefficients": right_combined,
            "full_P_mixed_target_passes": True,
        }
    assert mixed_rows["C:H_singleton_e"]["P_left"]["reachable_q_axis_sums"] == [0, 1]  # type: ignore[index]
    assert mixed_rows["C:H_singleton_e"]["P_right"]["reachable_q_axis_sums"] == [0, 1]  # type: ignore[index]
    assert mixed_rows["C:H_doubleton_ft"]["P_left"]["reachable_q_axis_sums"] == [0, 1, 232]  # type: ignore[index]
    assert mixed_rows["C:H_doubleton_ft"]["P_right"]["reachable_q_axis_sums"] == [0, 1, 2]  # type: ignore[index]

    z_counter = Counter({X: P - 4})
    z_counter.update(labels[position] for position in Y)
    maximum_actual_multiplicity = max(z_counter.values())
    maximum_values = sorted(
        signed(label)
        for label, count in z_counter.items()
        if count == maximum_actual_multiplicity
    )
    assert maximum_actual_multiplicity == P - 4

    endpoint_closure = endpoint_internal_closure(model)
    prescribed_tail_total = vadd(vmul(4, X), sum_positions(labels, tails))
    assert prescribed_tail_total == vmul(3, A)
    global_boundary = global_short_boundary(model)
    position_binding = {
        "labels": [[position, signed(labels[position])] for position in sorted(labels)],
        "K": sorted(K),
        "L": sorted(L),
        "P": sorted(packing),
        "endpoints": {
            endpoint_name: sorted(endpoint)
            for endpoint_name, endpoint in sorted(endpoints.items())
        },
    }
    return {
        "status": (
            "EXPLICIT_RELAXED_SAT_AT_FIRST_MOMENTS_RHO_ATOMS_ALL_P_MIXED_TARGETS_"
            "AND_COMPLETE_ENDPOINT_INTERNAL_SHORT_CLOSURE; NOT_GLOBAL_SHORT_SAT"
        ),
        "quantifiers": {
            "existential": (
                "there exists the displayed actual lift and the displayed two-position P"
            ),
            "universal_inside_witness": [
                "for each of the two displayed Q_H",
                "for each nonempty proper A subset P (the two singleton choices)",
                "for every T subset Q_H with rho(T)=-rho(A)",
                "for every rho-zero subset of either displayed endpoint H",
            ],
            "not_decided": (
                "whether some different lift of fixed Model C satisfies the global automatic-short-block spectrum"
            ),
        },
        "sizes": {"K": len(K), "L": len(L), "W": len(W), "P": len(packing), "Y": len(Y)},
        "sums": {
            "U": signed(sum_positions(labels, tails)),
            "P": signed(sum_positions(labels, packing)),
            "W": signed(sum_positions(labels, W)),
            "Y": signed(sum_positions(labels, Y)),
            "endpoints": {
                endpoint_name: signed(sum_positions(labels, endpoint))
                for endpoint_name, endpoint in endpoints.items()
            },
            "Q_H": {
                endpoint_name: signed(sum_positions(labels, q_set))
                for endpoint_name, q_set in q_sets.items()
            },
        },
        "rho_atoms": atom_rows,
        "P_mixed_targets": mixed_rows,
        "actual_multiplicity": {
            "maximum": maximum_actual_multiplicity,
            "required_upper_bound": P - 4,
            "values_at_maximum": maximum_values,
            "passes": True,
        },
        "prescribed_unique_tail_block": {
            "tail": sorted(tails),
            "x_count": 4,
            "length": 7,
            "actual_sum": signed(prescribed_tail_total),
            "family": "F3",
            "note": "existence of the prescribed block only; global uniqueness is not claimed",
        },
        "endpoint_internal_short_closure": endpoint_closure,
        "global_automatic_short_boundary": global_boundary,
        "literal_position_binding_sha256": sha256(
            json.dumps(position_binding, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "explicit_full_labels": {
            position: signed(label) for position, label in sorted(labels.items())
        },
        "omitted_interfaces": [
            "a concrete four-edge outer-shard endpoint incidence beyond the two displayed endpoints",
            "global automatic-short compatibility (the displayed witness explicitly fails it)",
            "the global no quotient-zero subset window of lengths 9 through 2p+2",
            "the complete real intersection network among all automatically induced short blocks",
            "the long-complement oracle for every automatically induced F3 block",
            "the separate length-697 complement atom forced by X_1 union U union P",
            "Hasse congruence rows",
            "minimal zero-sum of the actual length-3p+4 sequence Z",
        ],
        "not_claimed": [
            "SAT for all automatically induced short blocks in X union Y",
            "a full exact-slice candidate",
            "a realization of any one of the 720 outer survivors",
            "fixed-p SAT",
        ],
    }


def main() -> None:
    n_result = model_n_symbolic_certificate()
    c_result = audit_model_c()
    core = {
        "schema": "unique_tail_p233_doubleton_NC_lift_attack/v2",
        "p": P,
        "coordinates": ["a-height", "q-axis", "rho-e", "rho-f"],
        "frozen_slice": {
            "packing_type": [3],
            "packing_size": 2,
            "kappa": 1,
            "unique_tail": {"core_count": 4, "tail_size": 3},
        },
        "model_N": n_result,
        "model_C": c_result,
        "conclusion": (
            "For fixed Model N, every actual lift satisfying the common endpoint sums and the "
            "unique positive-core F3-tail interface is impossible. Fixed Model C has an explicit "
            "unified lift passing first moments, both rho atoms, every P-mixed target, the actual "
            "multiplicity cap, and the complete endpoint-internal rho-zero/X-completion closure. "
            "That same witness fails the global short spectrum at an explicit length-three block; "
            "existence of a different globally short-compatible Model-C lift remains open."
        ),
        "global_status": "INCOMPLETE",
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report = dict(core)
    report["certificate_sha256"] = sha256(canonical).hexdigest()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    destination = Path(__file__).with_name(
        "unique_tail_p233_doubleton_NC_lift_attack_report.json"
    )
    destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
