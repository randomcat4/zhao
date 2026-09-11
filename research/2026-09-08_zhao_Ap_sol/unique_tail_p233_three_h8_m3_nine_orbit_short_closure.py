"""Finite certificate closing the nine surviving p=233, m=3 orbits.

The program is independent of the earlier survivor report.  Starting from the
nine published orbit representatives, it recomputes the common cubic, all six
ordinary C-fibre multiplicities, the S3 x {+/-} orbit cover, the 27 pointed
roles, the opposite-fibre transversal gate, and the last four-label conflict.
"""

from __future__ import annotations

import hashlib
import json
from itertools import permutations
from pathlib import Path


P = 233
HEIGHT_CAP = P - 4
CORE_LENGTH = 2 * P - 5
TAILS = ((1, 0), (0, 1), (P - 1, P - 1))

# Only the nine unpointed orbit representatives from the proved core-fibre
# recovery are input.  Capacities and every later classification are recomputed.
ORBIT_REPRESENTATIVES = (
    ((10, 193), (69, 197)),
    ((12, 25), (12, 25)),
    ((18, 181), (18, 181)),
    ((29, 78), (1, 2)),
    ((29, 184), (8, 199)),
    ((33, 168), (29, 191)),
    ((44, 154), (39, 33)),
    ((56, 128), (56, 128)),
    ((66, 142), (3, 60)),
)


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def sub(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return ((left[0] - right[0]) % P, (left[1] - right[1]) % P)


def neg(vector: tuple[int, int]) -> tuple[int, int]:
    return ((-vector[0]) % P, (-vector[1]) % P)


def scale(value: int, vector: tuple[int, int]) -> tuple[int, int]:
    return (value * vector[0] % P, value * vector[1] % P)


def q0(vector: tuple[int, int]) -> int:
    x, y = vector
    return (x * x - x * y + y * y) % P


def cubic_parameters(delta: tuple[int, int]) -> tuple[int, int, int]:
    alpha, beta = delta
    g = pow((alpha - beta) % P, -1, P)
    f = (-2 - g * beta) * pow(3 * alpha, -1, P) % P
    i = (-2 + g * alpha) * pow(3 * beta, -1, P) % P
    return f, i, g


def core_coefficient(
    target: tuple[int, int], parameters: tuple[int, int, int]
) -> int:
    """The proved signed coefficient [X^target] Psi_C."""
    x, y = target
    f, i, g = parameters
    return (
        1
        - x * x
        + x * y
        - y * y
        + f * (x * x * x - x)
        + i * (y * y * y - y)
        + g * (x * x * y - x * y * y)
    ) % P


def recovered_fibre(
    target: tuple[int, int], parameters: tuple[int, int, int]
) -> int:
    """Recover the ordinary singleton-fibre multiplicity at a mixed target."""
    return (-core_coefficient(target, parameters) + int(target == (0, 0))) % P


def fibre_data(
    delta: tuple[int, int], s: tuple[int, int]
) -> tuple[tuple[tuple[int, int], ...], tuple[int, ...]]:
    parameters = cubic_parameters(delta)
    fringe = tuple(add(delta, tail) for tail in TAILS)
    targets = tuple(
        sub(direction, endpoint)
        for direction in (s, neg(s))
        for endpoint in fringe
    )
    capacities = tuple(recovered_fibre(target, parameters) for target in targets)
    assert all(target != (0, 0) for target, cap in zip(targets, capacities) if cap)
    assert all(0 <= cap <= HEIGHT_CAP for cap in capacities)
    assert sum(dict(zip(targets, capacities)).values()) <= CORE_LENGTH
    return targets, capacities


def tail_permutation_image(
    vector: tuple[int, int], permutation: tuple[int, int, int]
) -> tuple[int, int]:
    """Apply the unique linear map T_pi with T_pi(w_i)=w_{pi(i)}."""
    x, y = vector
    image_e = TAILS[permutation[0]]
    image_f = TAILS[permutation[1]]
    return (
        (x * image_e[0] + y * image_f[0]) % P,
        (x * image_e[1] + y * image_f[1]) % P,
    )


def unpointed_orbit(
    delta: tuple[int, int], s: tuple[int, int]
) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    result = set()
    for permutation in permutations(range(3)):
        delta_image = tail_permutation_image(delta, permutation)
        s_image = tail_permutation_image(s, permutation)
        result.add((delta_image, s_image))
        result.add((delta_image, neg(s_image)))
    return result


def pointed_orbit(
    delta: tuple[int, int], s: tuple[int, int], endpoint: int
) -> set[tuple[tuple[int, int], tuple[int, int], int]]:
    result = set()
    for permutation in permutations(range(3)):
        delta_image = tail_permutation_image(delta, permutation)
        s_image = tail_permutation_image(s, permutation)
        endpoint_image = permutation[endpoint]
        result.add((delta_image, s_image, endpoint_image))
        result.add((delta_image, neg(s_image), endpoint_image))
    return result


def pointed_transversal_gate(
    delta: tuple[int, int], s: tuple[int, int], endpoint: int
) -> dict[str, object]:
    """Apply the necessary opposite-fibre gate at one pointed endpoint.

    If c_delta(r) is nonzero, a literal C-representation F_r exists.  The
    mixed separator gives |F_r|<=2.  It must intersect every opposite-sign
    pair {v_i,c}; because F_r is contained in C, it must contain every such c.
    Hence A_{-r,i}<=2, and equality forces 2*t_{-r,i}=r.
    """
    parameters = cubic_parameters(delta)
    targets, capacities = fibre_data(delta, s)
    directions = (s, neg(s))
    checks = []
    passed = True
    for sign_index, direction in enumerate(directions):
        coefficient = core_coefficient(direction, parameters)
        opposite_sign_index = 1 - sign_index
        fibre_index = 3 * opposite_sign_index + endpoint
        target = targets[fibre_index]
        capacity = capacities[fibre_index]
        active = coefficient != 0
        capacity_ok = (not active) or capacity <= 2
        resonance_ok = (not active) or capacity != 2 or scale(2, target) == direction
        passed = passed and capacity_ok and resonance_ok
        checks.append(
            {
                "r": direction,
                "c_delta_r": coefficient,
                "active": active,
                "opposite_fibre_target": target,
                "opposite_fibre_capacity": capacity,
                "capacity_at_most_two": capacity_ok,
                "double_fibre_resonance": resonance_ok,
            }
        )
    return {
        "passed": passed,
        "checks": checks,
        "targets_order_plus_then_minus": targets,
        "capacities_order_plus_then_minus": capacities,
    }


def verify_last_role(
    delta: tuple[int, int], s: tuple[int, int], endpoint: int
) -> dict[str, object]:
    """Verify the forced disjoint F_+,F_- contradiction in the sole gate survivor."""
    parameters = cubic_parameters(delta)
    targets, capacities = fibre_data(delta, s)
    assert core_coefficient(s, parameters) != 0
    assert core_coefficient(neg(s), parameters) != 0

    t_minus = targets[3 + endpoint]
    t_plus = targets[endpoint]
    assert capacities[3 + endpoint] == capacities[endpoint] == 1

    # F_+ contains the unique t_minus position and has total projection s.
    # F_- contains the unique t_plus position and has total projection -s.
    f_plus = (t_minus, sub(s, t_minus))
    f_minus = (t_plus, sub(neg(s), t_plus))
    labels = f_plus + f_minus
    assert f_plus[0] != s and f_minus[0] != neg(s), "both representations are doubletons"
    assert len(set(labels)) == 4, "different rho labels force four different literal positions"
    assert add(f_plus[0], f_plus[1]) == s
    assert add(f_minus[0], f_minus[1]) == neg(s)
    assert add(add(labels[0], labels[1]), add(labels[2], labels[3])) == (0, 0)
    return {
        "delta": delta,
        "s": s,
        "completion_endpoint_one_based": endpoint + 1,
        "c_delta_plus_s": core_coefficient(s, parameters),
        "c_delta_minus_s": core_coefficient(neg(s), parameters),
        "F_plus_projection_labels": f_plus,
        "F_minus_projection_labels": f_minus,
        "four_labels_pairwise_distinct": len(set(labels)) == 4,
        "four_label_sum": (0, 0),
        "contradiction": (
            "F_plus and F_minus are disjoint nonempty C-subsets with opposite sums; "
            "equivalently they violate the mixed cross-intersection gate and C zero-sum-freeness"
        ),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report() -> dict[str, object]:
    curve = [
        (alpha, beta)
        for alpha in range(P)
        for beta in range(P)
        if q0((alpha, beta)) == 3
    ]
    exceptional = {
        sub(TAILS[j], TAILS[i])
        for i in range(3)
        for j in range(3)
        if i != j
    }
    generic_curve = set(curve) - exceptional
    excluded = set(TAILS) | {neg(tail) for tail in TAILS}
    directions = {
        (x, y)
        for x in range(P)
        for y in range(P)
        if (x, y) != (0, 0) and (x, y) not in excluded
    }
    assert len(curve) == 234
    assert len(exceptional) == 6
    assert len(generic_curve) == 228
    assert len(directions) == 54_282

    representative_rows = []
    unpointed_orbits = []
    pointed_orbits = []
    pointed_rows = []
    basic_survivors = []
    rejection_counts = {"capacity_gt_2": 0, "failed_double_resonance": 0}

    for orbit_index, (delta, s) in enumerate(ORBIT_REPRESENTATIVES, 1):
        assert delta in generic_curve
        assert s in directions
        parameters = cubic_parameters(delta)
        targets, capacities = fibre_data(delta, s)
        orbit = unpointed_orbit(delta, s)
        assert len(orbit) == 12
        assert all(d in generic_curve and direction in directions for d, direction in orbit)
        unpointed_orbits.append(orbit)
        representative_rows.append(
            {
                "orbit": orbit_index,
                "delta": delta,
                "s": s,
                "c_delta_plus_minus_s": (
                    core_coefficient(s, parameters),
                    core_coefficient(neg(s), parameters),
                ),
                "targets_plus_then_minus": targets,
                "capacities_plus_then_minus": capacities,
                "unique_forced_capacity": sum(dict(zip(targets, capacities)).values()),
            }
        )
        for endpoint in range(3):
            role_orbit = pointed_orbit(delta, s, endpoint)
            assert len(role_orbit) == 12
            pointed_orbits.append(role_orbit)
            gate = pointed_transversal_gate(delta, s, endpoint)
            row = {
                "orbit": orbit_index,
                "completion_endpoint_one_based": endpoint + 1,
                **gate,
            }
            pointed_rows.append(row)
            if gate["passed"]:
                basic_survivors.append((orbit_index, delta, s, endpoint))
            else:
                failed_checks = [check for check in gate["checks"] if check["active"]]
                if any(not check["capacity_at_most_two"] for check in failed_checks):
                    rejection_counts["capacity_gt_2"] += 1
                else:
                    assert any(not check["double_fibre_resonance"] for check in failed_checks)
                    rejection_counts["failed_double_resonance"] += 1

    assert all(len(orbit) == 12 for orbit in unpointed_orbits)
    assert not any(
        left_index < right_index and left & right
        for left_index, left in enumerate(unpointed_orbits)
        for right_index, right in enumerate(unpointed_orbits)
    )
    prior_survivor_pairs = set().union(*unpointed_orbits)
    assert len(prior_survivor_pairs) == 108

    assert all(len(orbit) == 12 for orbit in pointed_orbits)
    assert not any(
        left_index < right_index and left & right
        for left_index, left in enumerate(pointed_orbits)
        for right_index, right in enumerate(pointed_orbits)
    )
    prior_pointed_pairs = set().union(*pointed_orbits)
    assert len(prior_pointed_pairs) == 324 == 108 * 3

    # Check covariance on every pointed S3 x {+/-} image rather than assume it.
    for row, orbit in zip(pointed_rows, pointed_orbits):
        expected = row["passed"]
        for delta, s, endpoint in orbit:
            assert pointed_transversal_gate(delta, s, endpoint)["passed"] == expected

    assert rejection_counts == {"capacity_gt_2": 25, "failed_double_resonance": 1}
    assert len(basic_survivors) == 1
    assert basic_survivors[0][0] == 6 and basic_survivors[0][3] == 2
    last_conflict = verify_last_role(
        basic_survivors[0][1], basic_survivors[0][2], basic_survivors[0][3]
    )

    generic_pair_denominator = len(generic_curve) * len(directions)
    generic_pointed_denominator = 3 * generic_pair_denominator
    assert generic_pair_denominator == 12_376_296
    assert generic_pointed_denominator == 37_128_888

    return {
        "status": "PROVED",
        "scope": "p=233, three length-eight singleton endpoints, unique m=3 mask",
        "quantifier_denominators": {
            "generic_delta": 228,
            "admissible_directed_s_per_delta": 54_282,
            "generic_delta_s_pairs_before_core_fibre_recovery": generic_pair_denominator,
            "generic_completion_pointed_pairs_before_core_fibre_recovery": generic_pointed_denominator,
            "prior_nine_orbit_delta_s_survivors": 108,
            "prior_completion_pointed_survivors": 324,
            "prior_unpointed_orbits": 9,
            "prior_pointed_orbits": 27,
        },
        "new_gate_counts_on_27_pointed_orbits": {
            "capacity_gt_2_rejections": rejection_counts["capacity_gt_2"],
            "failed_double_resonance_rejections": rejection_counts["failed_double_resonance"],
            "survivors": 1,
        },
        "new_gate_counts_on_324_pointed_pairs": {
            "basic_rejections": 26 * 12,
            "basic_survivors": 12,
            "last_four_label_rejections": 12,
            "final_survivors": 0,
        },
        "representatives": representative_rows,
        "pointed_gate_table": pointed_rows,
        "last_role_conflict": last_conflict,
        "logical_boundary": {
            "signed_coefficient_use": (
                "c_delta(r) != 0 is used only to infer existence of at least one literal representation F_r"
            ),
            "literal_bridge": (
                "the mixed separator bounds every such F_r by two literal positions; "
                "cross-intersection with every opposite fringe pair then bounds an ordinary fibre"
            ),
            "q_height_needed": False,
            "automatic_short_closure_needed": False,
            "quotient_lift_claimed": False,
        },
        "final_survivors": 0,
    }


def main() -> None:
    report = build_report()
    script_path = Path(__file__)
    report["script_sha256"] = sha256(script_path)
    output_path = script_path.with_name(script_path.stem + "_report.json")
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
