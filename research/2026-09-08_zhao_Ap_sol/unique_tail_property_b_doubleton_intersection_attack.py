#!/usr/bin/env python3
"""Independent checks for the Property-B doubleton intersection attack.

This script imports no production module.  It reconstructs the two explicit
position-level countermodels, enumerates the p+1 cross-domain normal forms for
the complementary singleton/doubleton tail pattern, and checks the finite
coordinate obstruction for three doubletons at common-kernel length 2p-3.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import product
from pathlib import Path


P = 233
HERE = Path(__file__).resolve().parent
REPORT = HERE / "unique_tail_property_b_doubleton_intersection_attack_report.json"
OUTER_REPORT = HERE / "unique_tail_p233_kernel_lower_by_outer_row_report.json"
MASK_REPORT = HERE / "unique_tail_p233_endpoint_mask_frontier_report.json"

Vec = tuple[int, int]


def add(u: Vec, v: Vec) -> Vec:
    return ((u[0] + v[0]) % P, (u[1] + v[1]) % P)


def neg(u: Vec) -> Vec:
    return ((-u[0]) % P, (-u[1]) % P)


def sub(u: Vec, v: Vec) -> Vec:
    return add(u, neg(v))


def mul(a: int, u: Vec) -> Vec:
    return (a * u[0] % P, a * u[1] % P)


def det(u: Vec, v: Vec) -> int:
    return (u[0] * v[1] - u[1] * v[0]) % P


def inv(a: int) -> int:
    return pow(a % P, P - 2, P)


def in_span(u: Vec, g: Vec) -> bool:
    return det(u, g) == 0


def line_coeff(u: Vec, base: Vec, direction: Vec) -> int | None:
    delta = sub(u, base)
    if not in_span(delta, direction):
        return None
    if direction[0]:
        return delta[0] * inv(direction[0]) % P
    return delta[1] * inv(direction[1]) % P


def domain(heavy: Vec, base: Vec) -> frozenset[Vec]:
    assert det(heavy, base) != 0
    return frozenset([heavy] + [add(base, mul(a, heavy)) for a in range(P)])


def vector_sum(values: list[Vec]) -> Vec:
    answer = (0, 0)
    for value in values:
        answer = add(answer, value)
    return answer


def assert_standard_atom(values: list[Vec], heavy: Vec, base: Vec) -> None:
    counts = Counter(values)
    assert len(values) == 2 * P - 1
    assert counts[heavy] == P - 1
    coefficients: list[int] = []
    for value, multiplicity in counts.items():
        if value == heavy:
            continue
        coefficient = line_coeff(value, base, heavy)
        assert coefficient is not None
        coefficients.extend([coefficient] * multiplicity)
    assert len(coefficients) == P
    assert sum(coefficients) % P == 1
    assert vector_sum(values) == (0, 0)
    assert max(counts.values()) <= P - 1


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


E: Vec = (1, 0)
F: Vec = (0, 1)
T: Vec = neg(add(E, F))


def check_model_n() -> dict[str, object]:
    # All names are literal positions; repeated labels remain different names.
    labels: dict[str, Vec] = {}
    for i in range(231):
        labels[f"Kf{i}"] = F
        labels[f"Kt{i}"] = T
    labels["Km"] = neg(E)
    labels.update(
        {
            "u_e": E,
            "u_f": F,
            "u_t": T,
            "x_f": F,
            "x_t": T,
            "y": E,
            "e1": E,
            "e2": E,
            "c": mul(-3, E),
        }
    )
    K = {name for name in labels if name.startswith("K")}
    C = {"y", "e1", "e2", "c"}
    endpoints = {
        "singleton_e": {"u_e", "x_f", "x_t"} | C,
        "doubleton_ef": {"u_e", "u_f", "x_t"} | C,
        "doubleton_et": {"u_e", "u_t", "x_f"} | C,
    }
    W = set(labels)
    complements = {}
    for name, endpoint in endpoints.items():
        assert len(endpoint) == 7
        assert vector_sum([labels[position] for position in endpoint]) == (0, 0)
        Q = W - endpoint
        values = [labels[position] for position in sorted(Q)]
        assert_standard_atom(values, F, T)
        complements[name] = Q
    assert set.intersection(*complements.values()) == K
    assert len(K) == 2 * P - 3
    return {
        "common_kernel_size": len(K),
        "endpoint_traces": [["e"], ["e", "f"], ["e", "t"]],
        "exact_literal_intersection": True,
        "all_three_complements_are_the_same_label_multisequence": True,
    }


def check_model_c() -> dict[str, object]:
    g = T
    h = sub(T, E)
    labels: dict[str, Vec] = {}

    def put(prefix: str, values: list[Vec]) -> set[str]:
        names = set()
        for i, value in enumerate(values):
            name = f"{prefix}{i}"
            labels[name] = value
            names.add(name)
        return names

    K = put("K", [g] * 231 + [h] * 231)
    B_s = put("Bs_", [T, F, add(h, mul(3, g))])
    B_d = put("Bd_", [h, E, add(g, mul(2, h))])
    C = put("C_", [E, E, F, add(mul(4, E), mul(3, F))])
    H_s = B_d | C
    H_d = B_s | C
    W = set(labels)
    assert len(H_s) == len(H_d) == 7
    assert vector_sum([labels[position] for position in H_s]) == (0, 0)
    assert vector_sum([labels[position] for position in H_d]) == (0, 0)
    Q_s = W - H_s
    Q_d = W - H_d
    assert Q_s == K | B_s
    assert Q_d == K | B_d
    assert_standard_atom([labels[position] for position in sorted(Q_s)], g, h)
    assert_standard_atom([labels[position] for position in sorted(Q_d)], h, g)
    assert Q_s & Q_d == K
    assert len(K) == 2 * P - 4
    return {
        "common_kernel_size": len(K),
        "endpoint_traces": [["e"], ["f", "t"]],
        "exact_literal_intersection": True,
        "attains_complementary_pair_upper_bound": True,
    }


def check_model_d() -> dict[str, object]:
    g = E
    h = add(mul(2, E), F)
    z = add(g, h)
    r = add(mul(5, E), F)
    y = add(mul(-8, E), mul(-3, F))
    labels: dict[str, Vec] = {}

    def put(prefix: str, values: list[Vec]) -> set[str]:
        names = set()
        for i, value in enumerate(values):
            name = f"{prefix}{i}"
            labels[name] = value
            names.add(name)
        return names

    K = put("K", [g] * 229 + [h] * 227)
    P13 = put("P13_", [h] * 4)
    P23 = put("P23_", [g, h, z, z])
    P12 = put("P12_", [g, g, F, r])
    E1 = put("E1_", [E])
    E2 = put("E2_", [F])
    E3 = put("E3_", [T])
    O = put("O_", [y])
    W = set(labels)
    endpoints = {
        "doubleton_ft": P23 | E2 | E3 | O,
        "doubleton_et": P13 | E1 | E3 | O,
        "doubleton_ef": P12 | E1 | E2 | O,
    }
    complement_data = [
        ("doubleton_ft", g, F),
        ("doubleton_et", g, F),
        ("doubleton_ef", h, E),
    ]
    complements = {}
    for name, heavy, base in complement_data:
        endpoint = endpoints[name]
        assert len(endpoint) == 7
        assert vector_sum([labels[position] for position in endpoint]) == (0, 0)
        Q = W - endpoint
        assert_standard_atom([labels[position] for position in sorted(Q)], heavy, base)
        complements[name] = Q
    assert set.intersection(*complements.values()) == K
    assert len(K) == 456
    assert domain(g, F) & domain(h, E) == frozenset({g, h, z})
    return {
        "common_kernel_size": len(K),
        "endpoint_traces": [["f", "t"], ["e", "t"], ["e", "f"]],
        "exact_literal_intersection": True,
        "distinct_standard_domains": 2,
        "common_support": [list(g), list(h), list(z)],
    }


def enumerate_complementary_cross_pairs() -> list[tuple[Vec, Vec]]:
    # Orient the pair so D_x contains e,f and D_y contains t.  Mutual crossing
    # means y lies on D_x's affine line and x lies on D_y's affine line.
    answers: set[tuple[Vec, Vec]] = set()
    nonzero = [(a, b) for a in range(P) for b in range(P) if (a, b) != (0, 0)]
    for x in nonzero:
        line_base = None
        if x == E:
            line_base = F
        elif x == F:
            line_base = E
        elif in_span(sub(F, E), x):
            line_base = E
        if line_base is None:
            continue
        for a in range(P):
            y = add(line_base, mul(a, x))
            if det(x, y) == 0:
                continue
            if T in domain(y, x):
                answers.add((x, y))
    return sorted(answers)


def formula_cross_pairs() -> set[tuple[Vec, Vec]]:
    answers = {
        (F, add(E, mul(2, F))),
        (E, add(mul(2, E), F)),
    }
    two_inverse = inv(2)
    for c in range(1, P):
        x = mul(c, sub(F, E))
        a = (c + 1) * inv(2 * c) % P
        y = add(E, mul(a, x))
        # Equivalent closed form: y=((1-c)/2)e+((1+c)/2)f.
        expected = add(mul((1 - c) * two_inverse, E), mul((1 + c) * two_inverse, F))
        assert y == expected
        answers.add((x, y))
    return answers


def complement_pair_boundary(cross_pairs: list[tuple[Vec, Vec]]) -> dict[str, object]:
    # If |K|=2p-3, both complements have exactly two positions outside K.
    # Search all triangle multiplicities and require the fixed tails to fit the
    # heavy deficit, line-slot deficit, and coefficient-sum equation.
    feasible_at_boundary = []
    feasible_one_below = []
    feasible_two_below = []

    def required_metadata(required: tuple[Vec, ...], heavy: Vec, base: Vec):
        heavy_count = 0
        coefficients = []
        for value in required:
            if value == heavy:
                heavy_count += 1
            else:
                coefficient = line_coeff(value, base, heavy)
                assert coefficient is not None
                coefficients.append(coefficient)
        return heavy_count, coefficients

    def completion_possible(
        outside_size: int,
        heavy_in_K: int,
        triangle_third_count: int,
        metadata: tuple[int, list[int]],
    ) -> bool:
        required_heavy, required_coefficients = metadata
        outside_heavy = P - 1 - heavy_in_K
        outside_line = outside_size - outside_heavy
        if outside_heavy < required_heavy or outside_line < len(required_coefficients):
            return False
        if outside_heavy < 0 or outside_line < 0:
            return False
        free_line_slots = outside_line - len(required_coefficients)
        if free_line_slots == 0:
            return (triangle_third_count + sum(required_coefficients) - 1) % P == 0
        return True

    for pair_index, (x, y) in enumerate(cross_pairs):
        metadata_x = required_metadata((E, F), x, y)
        metadata_y = required_metadata((T,), y, x)
        for kernel_size, destination in (
            (2 * P - 3, feasible_at_boundary),
            (2 * P - 4, feasible_one_below),
            (2 * P - 5, feasible_two_below),
        ):
            outside_size = 2 * P - 1 - kernel_size
            found = None
            for a in range(P):
                for b in range(P):
                    c = kernel_size - a - b
                    if not 0 <= c < P:
                        continue
                    # Exact zero-sum-free criterion for x^a y^b (x+y)^c.
                    if c + min(a, b) >= P:
                        continue
                    if not completion_possible(outside_size, a, c, metadata_x):
                        continue
                    if not completion_possible(outside_size, b, c, metadata_y):
                        continue
                    found = (a, b, c)
                    break
                if found is not None:
                    break
            if found is not None:
                destination.append((pair_index, found))
    assert not feasible_at_boundary
    assert len(feasible_one_below) == 2
    assert len(feasible_two_below) == P + 1
    return {
        "kernel_size_2p_minus_3_feasible_pair_count": len(feasible_at_boundary),
        "kernel_size_2p_minus_4_feasible_pair_count": len(feasible_one_below),
        "kernel_size_2p_minus_5_feasible_pair_count": len(feasible_two_below),
        "sharp_upper_bound": 2 * P - 4,
        "first_boundary_witness": {
            "pair_index": feasible_one_below[0][0],
            "triangle_multiplicities": list(feasible_one_below[0][1]),
        },
    }


def allowed_g(alpha: int, beta: int) -> list[Vec]:
    if alpha == 0:
        return [(c, 1) for c in range(P)]
    if alpha == 1:
        return sorted({(1, 0), ((1 - beta) % P, 1)})
    if alpha == 2 and beta == 0:
        return [(1, 0)]
    return []


def allowed_h(alpha: int, beta: int) -> list[Vec]:
    if beta == 0:
        return [(1, c) for c in range(P)]
    if beta == 1:
        return sorted({(0, 1), (1, (1 - alpha) % P)})
    if beta == 2 and alpha == 0:
        return [(0, 1)]
    return []


def three_doubleton_boundary() -> dict[str, object]:
    # Coordinates are in the independent heavy basis (g,h).  The three tails
    # are assigned to g-heavy or h-heavy atoms, with both domain types used.
    tested_cases = []
    solutions = []
    for alpha, beta in product(range(3), repeat=2):
        c = alpha + beta - 1
        if not 0 <= c <= 3:
            continue
        G = allowed_g(alpha, beta)
        H = allowed_h(alpha, beta)
        for assignment in product("gh", repeat=3):
            if len(set(assignment)) != 2:
                continue
            sets = [G if kind == "g" else H for kind in assignment]
            if any(not values for values in sets):
                continue
            tested_cases.append((alpha, beta, "".join(assignment)))
            third_set = set(sets[2])
            for e_coordinate in sets[0]:
                for f_coordinate in sets[1]:
                    if det(e_coordinate, f_coordinate) == 0:
                        continue
                    t_coordinate = neg(add(e_coordinate, f_coordinate))
                    if t_coordinate in third_set:
                        solutions.append(
                            (alpha, beta, "".join(assignment), e_coordinate, f_coordinate, t_coordinate)
                        )
    assert not solutions
    return {
        "kernel_size_2p_minus_3_coordinate_solutions": 0,
        "tested_alpha_beta_assignment_cases": len(tested_cases),
        "exceptional_characteristic_in_hand_proof": 3,
        "consequence_for_p233": "common kernel size at most 462",
    }


def first_outer_row() -> dict[str, object]:
    payload = json.loads(OUTER_REPORT.read_text(encoding="utf-8"))
    row = next(item for item in payload["rows"] if item["decorated_shard_id"] == "decorated-0011")
    assert row["endpoint_trace_masks"] == [3, 4, 1, 6, 2, 5]
    assert row["endpoint_lengths"] == [7, 7, 8, 7, 8, 7]
    assert row["K_size_lower"] == 439
    assert row["length_seven_maximal_complement_count"] == 4
    return {
        "source_sha256": sha256(OUTER_REPORT),
        "decorated_shard_id": row["decorated_shard_id"],
        "endpoint_trace_masks": row["endpoint_trace_masks"],
        "endpoint_lengths": row["endpoint_lengths"],
        "K_size_interval_after_this_attack": [439, 462],
        "reason_for_upper_bound": "singleton trace 4 and complementary doubleton trace 3",
    }


def current_mask_frontier() -> dict[str, object]:
    # This is an arithmetic reconstruction of the displayed first literal
    # instance, not an audit of the upstream 27,172-orbit enumeration.
    payload = json.loads(MASK_REPORT.read_text(encoding="utf-8"))
    shard = payload["canonical_shard"]
    instance = payload["canonical_enumeration"]["first_survivor_literal_instance"]
    assert shard["decorated_shard_id"] == "decorated-1356"
    assert shard["endpoint_trace_masks"] == [1, 2, 4, 6]
    assert shard["endpoint_lengths"] == [8, 7, 8, 8]
    U = {"u_e", "u_f", "u_t"}
    anonymous = {f"z_{i:03d}" for i in range(1, 469)}
    Y = U | {"y"} | anonymous | {"p_1", "p_2"}
    P_positions = set(instance["packing_P"])
    endpoints = [set(endpoint) for endpoint in instance["endpoint_masks"]]
    L = U | set().union(*endpoints)
    K = Y - L - P_positions
    complements = [Y - endpoint - P_positions for endpoint in endpoints]
    assert len(Y) == 474 and len(L) == 26 and len(K) == 446
    assert [len(Q) for Q in complements] == [464, 465, 464, 464]
    assert K == {f"z_{i:03d}" for i in range(23, 469)}
    return {
        "dependency_status": "upstream mask enumeration not independently audited here",
        "source_sha256": sha256(MASK_REPORT),
        "decorated_shard_id": shard["decorated_shard_id"],
        "traces": shard["endpoint_trace_masks"],
        "lengths": shard["endpoint_lengths"],
        "displayed_literal_instance_reconstructed": True,
        "K_size": len(K),
        "Q_sizes": [len(Q) for Q in complements],
        "heavy_multiplicity_for_any_max_or_incomplete_h8_completion_inside_K_at_least": len(K) - P,
        "conditional_cross_trigger": (
            "if a non-tail deletion from h8 Q_0 or Q_2 has a missing nonzero subsum, "
            "its Property-B completion and the actual h7 atom force the cross-triangle normal form"
        ),
        "row_eliminated": False,
    }


def main() -> None:
    model_n = check_model_n()
    model_c = check_model_c()
    model_d = check_model_d()
    cross_pairs = enumerate_complementary_cross_pairs()
    formula_pairs = formula_cross_pairs()
    assert set(cross_pairs) == formula_pairs
    assert len(cross_pairs) == P + 1
    for x, y in cross_pairs:
        D_x = domain(x, y)
        D_y = domain(y, x)
        assert E in D_x and F in D_x and T in D_y
        assert D_x & D_y == frozenset({x, y, add(x, y)})

    report = {
        "schema": "unique-tail-property-b-doubleton-intersection-attack-v1",
        "status": "PROVED_REDUCTION/INDEPENDENT_REVIEW_CORRECT/GLOBAL_INCOMPLETE",
        "scope": {
            "main_lemmas": "all primes p >= 5 possessing Property B",
            "instantiated_slice": "p=233, type-(3), |P|=2",
            "not_claimed": [
                "no claim that any outer survivor is a complete exact-slice model",
                "no elimination of decorated-0011",
                "no unified endpoint-mask gluing for the displayed 234 first-row domains",
            ],
        },
        "position_level_counterexamples": {
            "model_N": model_n,
            "model_C": model_c,
            "model_D": model_d,
        },
        "rigidity": {
            "large_common_kernel_alternatives": [
                "all Property-B support domains coincide",
                "exactly two cross domains with common support {g,h,g+h}",
            ],
            "common_support_sizes_1_2_and_p_are_impossible_for_distinct_domains": True,
        },
        "complementary_singleton_doubleton": {
            "oriented_cross_domain_count": len(cross_pairs),
            "expected_count": P + 1,
            "boundary_search": complement_pair_boundary(cross_pairs),
        },
        "three_doubleton": three_doubleton_boundary(),
        "first_outer_row": first_outer_row(),
        "current_literal_mask_frontier": current_mask_frontier(),
        "length_2p_minus_2_atom_dichotomy": {
            "statement_checked_in_proof": True,
            "use": "a missing-nonzero-subsum branch embeds K in one more Property-B domain",
            "remaining_branch": "all nonzero targets occur as nonempty subsums",
            "row_eliminations_from_this_dichotomy_alone": 0,
        },
    }
    canonical = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    report["certificate_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
