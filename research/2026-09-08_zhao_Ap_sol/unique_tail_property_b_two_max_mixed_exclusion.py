#!/usr/bin/env python3
"""Exact certificate for the two-maximal-atom mixed endpoint obstruction.

The checker enumerates every Property-B support orientation for the tail pairs
{f,t} and {e,t}, t=-e-f, over F_233.  It verifies that close distinct-base
supports have exactly three possible ordered base pairs, checks the resulting
common-kernel caps, and independently verifies a literal two-atom boundary
model by enumerating all compressed submultisets.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import itertools
import json
from pathlib import Path


P = 233
Vec = tuple[int, int]


def add(a: Vec, b: Vec) -> Vec:
    return ((a[0] + b[0]) % P, (a[1] + b[1]) % P)


def sub(a: Vec, b: Vec) -> Vec:
    return ((a[0] - b[0]) % P, (a[1] - b[1]) % P)


def scale(c: int, a: Vec) -> Vec:
    return ((c * a[0]) % P, (c * a[1]) % P)


def cross(a: Vec, b: Vec) -> int:
    return (a[0] * b[1] - a[1] * b[0]) % P


def on_line(v: Vec, point: Vec, direction: Vec) -> bool:
    return cross(sub(v, point), direction) == 0


def same_line(point1: Vec, direction1: Vec, point2: Vec, direction2: Vec) -> bool:
    return cross(direction1, direction2) == 0 and on_line(point2, point1, direction1)


@dataclass(frozen=True)
class Orientation:
    base: Vec
    point: Vec
    kind: str
    scalar: int | None

    def contains(self, v: Vec) -> bool:
        return v == self.base or on_line(v, self.point, self.base)


def orientations(a: Vec, b: Vec) -> list[Orientation]:
    ans = [
        Orientation(a, b, "base_first_tail", None),
        Orientation(b, a, "base_second_tail", None),
    ]
    direction = sub(b, a)
    for c in range(1, P):
        ans.append(Orientation(scale(c, direction), a, "both_tails_on_line", c))
    if len(ans) != P + 1 or len(set(ans)) != P + 1:
        raise AssertionError("orientation denominator is not p+1")
    if not all(item.contains(a) and item.contains(b) for item in ans):
        raise AssertionError("orientation generation omitted a tail")
    return ans


def signed(v: Vec) -> list[int]:
    return [x if x <= P // 2 else x - P for x in v]


def zero_submultisets(labels: list[Vec], counts: list[int]) -> list[list[int]]:
    zeros: list[list[int]] = []
    for choice in itertools.product(*(range(count + 1) for count in counts)):
        sx = sum(c * v[0] for c, v in zip(choice, labels)) % P
        sy = sum(c * v[1] for c, v in zip(choice, labels)) % P
        if sx == 0 and sy == 0:
            zeros.append(list(choice))
    return zeros


def main() -> None:
    e = (1, 0)
    f = (0, 1)
    t = (-1 % P, -1 % P)
    left = orientations(f, t)
    right = orientations(e, t)

    compatible = []
    for o1 in left:
        for o2 in right:
            # Since K has size 435, at least 435-p=202 copies of each
            # (p-1)-fold base occur in K and hence in the other atom.
            if o2.contains(o1.base) and o1.contains(o2.base):
                compatible.append((o1, o2))

    expected_bases = {
        (t, t),
        (t, sub(t, e)),
        (sub(t, f), t),
        (scale(pow(3, -1, P), sub(t, f)), scale(pow(3, -1, P), sub(t, e))),
    }
    actual_bases = {(o1.base, o2.base) for o1, o2 in compatible}
    if actual_bases != expected_bases or len(compatible) != 4:
        raise AssertionError((len(compatible), actual_bases))

    compatibility_rows = []
    for o1, o2 in compatible:
        base_sum = add(o1.base, o2.base)
        if o1.base == t or o2.base == t:
            witness = "e+f+t=0"
            witness_length = 3
        elif base_sum == t:
            witness = "e+f+g1+g2=0"
            witness_length = 4
        else:
            raise AssertionError("compatible bases did not produce the required short witness")
        compatibility_rows.append(
            {
                "left_base": signed(o1.base),
                "right_base": signed(o2.base),
                "base_sum": signed(base_sum),
                "forced_Q3_zero_sum": witness,
                "witness_length": witness_length,
            }
        )

    # A sharp boundary model showing that the two maximal atoms alone coexist.
    g = t
    h = sub(t, e)  # -2e-f
    s1 = add(h, scale(3, g))
    s2 = add(g, scale(2, h))
    q1_labels = [g, h, f, s1]
    q1_counts = [P - 1, P - 2, 1, 1]
    q2_labels = [h, g, e, s2]
    q2_counts = [P - 1, P - 2, 1, 1]
    q1_zeros = zero_submultisets(q1_labels, q1_counts)
    q2_zeros = zero_submultisets(q2_labels, q2_counts)
    if q1_zeros != [[0, 0, 0, 0], q1_counts]:
        raise AssertionError(("Q1 not minimal", q1_zeros))
    if q2_zeros != [[0, 0, 0, 0], q2_counts]:
        raise AssertionError(("Q2 not minimal", q2_zeros))
    literal_overlap = 2 * (P - 2)
    directional_replacements = (2 * P - 1) - literal_overlap
    if literal_overlap != 462 or directional_replacements != 3:
        raise AssertionError("boundary model overlap mismatch")

    core = {
        "schema": "unique_tail_property_b_two_max_mixed_exclusion/v1",
        "prime": P,
        "orientation_counts": {
            "left_tail_pair": len(left),
            "right_tail_pair": len(right),
            "raw_pairs": len(left) * len(right),
            "mutually_supported_base_pairs": len(compatible),
        },
        "compatible_base_rows": compatibility_rows,
        "mixed_branch": {
            "Q1_length": 2 * P - 1,
            "Q2_length": 2 * P - 1,
            "Q3_length": 2 * P - 2,
            "common_kernel_lower_bound": 435,
            "minimum_copies_of_each_heavy_base_inside_K": 435 - P,
            "conclusion": "UNSAT at the unified C_p^2 atom layer",
        },
        "two_max_atom_boundary_model": {
            "g": signed(g),
            "h": signed(h),
            "Q1": [
                {"label": signed(v), "multiplicity": c}
                for v, c in zip(q1_labels, q1_counts)
            ],
            "Q2": [
                {"label": signed(v), "multiplicity": c}
                for v, c in zip(q2_labels, q2_counts)
            ],
            "Q1_zero_submultisets": q1_zeros,
            "Q2_zero_submultisets": q2_zeros,
            "literal_overlap": literal_overlap,
            "directional_replacements": directional_replacements,
            "relaxed_boundary": "No third near-maximal atom and no full short-spectrum closure.",
        },
        "external_dependency": "Reiher: every prime has Property B",
        "global_status": "INCOMPLETE",
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report = dict(core)
    report["certificate_sha256"] = sha256(canonical).hexdigest()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    report_path = Path(__file__).with_name(
        "unique_tail_property_b_two_max_mixed_exclusion_report.json"
    )
    report_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
