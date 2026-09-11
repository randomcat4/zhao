#!/usr/bin/env python3
"""Close the four O1 quartic exceptions with one real-position deletion.

For a possible label g of a position x in the common core C, let d be the
coefficient function after deleting x.  The known even quartic q then forces

    d(t) - d(t-g) = q(t+tau).

After centering, d is an odd polynomial of total degree at most five.  The
solutions of the displayed difference equation form a three-dimensional
affine space.  This program constructs that space exactly over F_233 and
adds all ordinary non-representation equations supplied by the three
literal fringes.  It exhausts every nonzero g for each of the four surviving
(z,tau) states; no candidate label survives.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import comb
from pathlib import Path


P = 233
INV2 = pow(2, -1, P)

W1 = (1, 0)
W2 = (0, 1)
W3 = (P - 1, P - 1)

Q = {
    (0, 0): 74,
    (2, 0): 201,
    (1, 1): 35,
    (0, 2): 201,
    (4, 0): 109,
    (3, 1): 146,
    (2, 2): 189,
    (1, 3): 146,
    (0, 4): 109,
}

EXCEPTIONAL_Z = ((58, 174), (60, 176))
EXCEPTIONAL_TAU = ((59, 174), (174, 59))

# If Delta_X F = F(X+1/2)-F(X-1/2), these are Delta_X^{-1}(X^i).
CENTRAL_ANTIDERIVATIVE = {
    0: {1: 1},
    1: {2: pow(2, -1, P)},
    2: {3: pow(3, -1, P), 1: -pow(12, -1, P) % P},
    3: {4: pow(4, -1, P), 2: -pow(8, -1, P) % P},
    4: {
        5: pow(5, -1, P),
        3: -pow(6, -1, P) % P,
        1: 7 * pow(240, -1, P) % P,
    },
}


Point = tuple[int, int]
Polynomial = dict[tuple[int, int], int]


def add(left: Point, right: Point) -> Point:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def neg(point: Point) -> Point:
    return (-point[0] % P, -point[1] % P)


def scalar(value: int, point: Point) -> Point:
    return (value * point[0] % P, value * point[1] % P)


def polynomial_add_term(poly: Polynomial, exponent: tuple[int, int], value: int) -> None:
    poly[exponent] = (poly.get(exponent, 0) + value) % P
    if poly[exponent] == 0:
        del poly[exponent]


def pullback_q(g: Point) -> Polynomial:
    """Return q(X*g+Y*h), where h makes (g,h) a basis."""
    a, b = g
    result: Polynomial = {}
    if a:
        # h=(0,1): x=aX and y=bX+Y.
        for (x_degree, y_degree), coefficient in Q.items():
            for y_power in range(y_degree + 1):
                x_power = x_degree + y_degree - y_power
                value = (
                    coefficient
                    * comb(y_degree, y_power)
                    * pow(a, x_degree, P)
                    * pow(b, y_degree - y_power, P)
                )
                polynomial_add_term(result, (x_power, y_power), value)
    else:
        # h=(1,0): x=Y and y=bX.
        assert b
        for (x_degree, y_degree), coefficient in Q.items():
            polynomial_add_term(
                result,
                (y_degree, x_degree),
                coefficient * pow(b, y_degree, P),
            )
    return result


def odd_antiderivative(g: Point) -> Polynomial:
    """Construct one odd D with D(X+1/2,Y)-D(X-1/2,Y)=q(Xg+Yh)."""
    result: Polynomial = {}
    for (x_degree, y_degree), coefficient in pullback_q(g).items():
        for antiderivative_degree, multiplier in CENTRAL_ANTIDERIVATIVE[
            x_degree
        ].items():
            polynomial_add_term(
                result,
                (antiderivative_degree, y_degree),
                coefficient * multiplier,
            )
    assert all((x_degree + y_degree) % 2 == 1 for x_degree, y_degree in result)
    assert centered_difference(result) == pullback_q(g)
    return result


def shifted_power_terms(degree: int, shift: int) -> dict[int, int]:
    return {
        exponent: comb(degree, exponent) * pow(shift, degree - exponent, P) % P
        for exponent in range(degree + 1)
    }


def centered_difference(poly: Polynomial) -> Polynomial:
    """Apply F(X,Y) -> F(X+1/2,Y)-F(X-1/2,Y)."""
    result: Polynomial = {}
    for (x_degree, y_degree), coefficient in poly.items():
        plus = shifted_power_terms(x_degree, INV2)
        minus = shifted_power_terms(x_degree, -INV2 % P)
        for exponent in range(x_degree + 1):
            polynomial_add_term(
                result,
                (exponent, y_degree),
                coefficient * (plus[exponent] - minus[exponent]),
            )
    return result


def coordinates(g: Point, s: Point) -> Point:
    """Coordinates of s+g/2 in the basis (g,h) used by pullback_q."""
    a, b = g
    if a:
        inverse_a = pow(a, P - 2, P)
        return (
            (s[0] * inverse_a + INV2) % P,
            (s[1] - b * inverse_a * s[0]) % P,
        )
    assert b
    return ((s[1] * pow(b, P - 2, P) + INV2) % P, s[0] % P)


def evaluate(poly: Polynomial, point: Point) -> int:
    x, y = point
    return sum(
        coefficient * pow(x, x_degree, P) * pow(y, y_degree, P)
        for (x_degree, y_degree), coefficient in poly.items()
    ) % P


class AffineThreeSystem:
    """Incremental exact consistency test for three affine unknowns."""

    def __init__(self) -> None:
        self.rows: list[list[int]] = []
        self.consistent = True

    def add(self, coefficients: tuple[int, int, int], rhs: int) -> bool:
        if not self.consistent:
            return False
        row = [value % P for value in coefficients] + [rhs % P]
        for old in self.rows:
            pivot = next(index for index in range(3) if old[index])
            if row[pivot]:
                factor = row[pivot]
                row = [(left - factor * right) % P for left, right in zip(row, old)]
        pivot = next((index for index in range(3) if row[index]), None)
        if pivot is None:
            self.consistent = row[3] == 0
            return self.consistent
        inverse = pow(row[pivot], P - 2, P)
        row = [value * inverse % P for value in row]
        for index, old in enumerate(self.rows):
            if old[pivot]:
                factor = old[pivot]
                self.rows[index] = [
                    (left - factor * right) % P for left, right in zip(old, row)
                ]
        self.rows.append(row)
        self.rows.sort(key=lambda item: next(index for index in range(3) if item[index]))
        return True


def fringe_data(z: Point, tau: Point) -> dict[str, object]:
    x1 = add(tau, neg(z))
    x2 = add(add(tau, W3), z)
    y13 = add(add(tau, W2), z)
    y23 = add(add(add(tau, W1), neg(W3)), neg(z))
    fringes = (
        (W2, W3, x2, y23),
        (W1, W3, x1, y13),
        (W1, W2, x1, x2),
    )
    expected_sum = scalar(2, tau)
    for fringe in fringes:
        total = (0, 0)
        for point in fringe:
            total = add(total, point)
        assert total == expected_sum
        assert all(point != (0, 0) for point in fringe)
    return {
        "literal_labels": {
            "x1": list(x1),
            "x2": list(x2),
            "y13": list(y13),
            "y23": list(y23),
        },
        "fringes": fringes,
    }


def nonempty_subset_targets(fringe: tuple[Point, ...]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for mask in range(1, 1 << len(fringe)):
        total = (0, 0)
        for index, point in enumerate(fringe):
            if mask & (1 << index):
                total = add(total, point)
        rows.append({"mask": mask, "target": neg(total)})
    return rows


def add_target_equation(
    system: AffineThreeSystem,
    d0: Polynomial,
    g: Point,
    tau: Point,
    target: Point,
    desired_value: int,
) -> bool:
    s = add(target, tau)
    x, y = coordinates(g, s)
    kernel_row = (y, pow(y, 3, P), pow(y, 5, P))
    rhs = (desired_value - evaluate(d0, (x, y))) % P
    return system.add(kernel_row, rhs)


def scan_state(z: Point, tau: Point) -> dict[str, object]:
    data = fringe_data(z, tau)
    fringes = data["fringes"]
    assert isinstance(fringes, tuple)
    endpoint_rows = [nonempty_subset_targets(fringe) for fringe in fringes]
    stage_counts = {"normalization": 0, "F1": 0, "F2": 0, "F3": 0}
    later_stage_labels: dict[str, list[list[int]]] = {"F1": [], "F2": []}
    failure_counts: dict[str, int] = {}
    survivors: list[list[int]] = []

    for gx in range(P):
        for gy in range(P):
            if gx == 0 and gy == 0:
                continue
            g = (gx, gy)
            d0 = odd_antiderivative(g)
            system = AffineThreeSystem()
            if not add_target_equation(system, d0, g, tau, (0, 0), 1):
                failure_counts["normalization"] = failure_counts.get("normalization", 0) + 1
                continue
            stage_counts["normalization"] += 1

            failed = False
            for endpoint_index, rows in enumerate(endpoint_rows, start=1):
                for item in rows:
                    target = item["target"]
                    assert isinstance(target, tuple)
                    if not add_target_equation(system, d0, g, tau, target, 0):
                        key = f"F{endpoint_index}_mask_{item['mask']:02d}"
                        failure_counts[key] = failure_counts.get(key, 0) + 1
                        failed = True
                        break
                if failed:
                    break
                stage_counts[f"F{endpoint_index}"] += 1
                if endpoint_index <= 2:
                    later_stage_labels[f"F{endpoint_index}"].append([gx, gy])
            if not failed:
                survivors.append([gx, gy])

    unique_targets = {
        item["target"] for rows in endpoint_rows for item in rows
    }
    return {
        "z": list(z),
        "tau": list(tau),
        "literal_labels": data["literal_labels"],
        "fringe_nonempty_subset_equations_per_endpoint": [len(rows) for rows in endpoint_rows],
        "unique_nonempty_subset_targets_across_endpoints": len(unique_targets),
        "candidate_nonzero_labels": P * P - 1,
        "stage_survivor_counts": stage_counts,
        "labels_surviving_F1": later_stage_labels["F1"],
        "labels_surviving_F2": later_stage_labels["F2"],
        "failure_equation_histogram": dict(sorted(failure_counts.items())),
        "survivor_count": len(survivors),
        "survivors": survivors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(__file__).with_name(
            "unique_tail_p233_three_h8_m4_O1_single_deletion_quintic_search_report.json"
        ),
    )
    args = parser.parse_args()

    states = [scan_state(z, tau) for z in EXCEPTIONAL_Z for tau in EXCEPTIONAL_TAU]
    assert all(state["survivor_count"] == 0 for state in states)
    report = {
        "status": "PROVED_EXCLUSION",
        "scope": "p=233, three length-eight singleton endpoints, m=4, O1=(0,1,1,4), four quartic exceptions",
        "field_prime": P,
        "quartic_coefficients": {
            f"x^{x_degree}y^{y_degree}": value
            for (x_degree, y_degree), value in sorted(Q.items())
        },
        "odd_quintic_kernel_basis": ["Y", "Y^3", "Y^5"],
        "states": states,
        "total_candidate_state_labels": len(states) * (P * P - 1),
        "total_surviving_state_labels": sum(state["survivor_count"] for state in states),
        "logical_boundary": {
            "real_common_core_position_used": True,
            "all_three_literal_fringes_used": True,
            "all_nonempty_fringe_subsets_used": True,
            "ordinary_nonrepresentation_before_signed_zero_used": True,
            "completion_theorem_used": False,
            "automatic_short_blocks_used": False,
            "other_m4_orbits_used": False,
            "global_A_p_claimed": False,
        },
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    args.report.write_bytes(rendered.encode("utf-8"))
    print(
        json.dumps(
            {
                "status": report["status"],
                "state_stage_counts": [
                    {
                        "z": state["z"],
                        "tau": state["tau"],
                        "stage_survivor_counts": state["stage_survivor_counts"],
                        "survivor_count": state["survivor_count"],
                    }
                    for state in states
                ],
                "total_candidate_state_labels": report["total_candidate_state_labels"],
                "total_surviving_state_labels": report["total_surviving_state_labels"],
                "report_sha256": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
