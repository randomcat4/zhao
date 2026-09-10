#!/usr/bin/env python3
"""Fresh no-import audit of the p=233 two-maximal-atom mixed obstruction.

The checker rebuilds the full Property-B orientation metadata (heavy label,
affine-line point, direction, case, and scalar), rather than only the union of
allowed support points.  It enumerates all 234^2 orientation pairs, checks the
short zero-sum witnesses inside Q3 with distinct literal position tokens, and
independently checks the relaxed two-maximal-atom survivor.

It does not import either author checker or consume either author report.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
import itertools
import json
from pathlib import Path


P = 233
Vec = tuple[int, int]


def add(x: Vec, y: Vec) -> Vec:
    return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)


def neg(x: Vec) -> Vec:
    return ((-x[0]) % P, (-x[1]) % P)


def sub(x: Vec, y: Vec) -> Vec:
    return add(x, neg(y))


def mul(c: int, x: Vec) -> Vec:
    return ((c * x[0]) % P, (c * x[1]) % P)


def det(x: Vec, y: Vec) -> int:
    return (x[0] * y[1] - x[1] * y[0]) % P


def affine_line(point: Vec, direction: Vec) -> frozenset[Vec]:
    return frozenset(add(point, mul(c, direction)) for c in range(P))


def signed(x: Vec) -> list[int]:
    return [a if a <= P // 2 else a - P for a in x]


@dataclass(frozen=True)
class PBMetadata:
    """One possible simple-support envelope forced by a specified tail pair."""

    heavy: Vec
    line_point: Vec
    direction: Vec
    case: str
    scalar: int | None

    @property
    def line(self) -> frozenset[Vec]:
        return affine_line(self.line_point, self.direction)

    @property
    def envelope(self) -> frozenset[Vec]:
        return self.line | {self.heavy}

    def contains(self, label: Vec) -> bool:
        return label == self.heavy or det(sub(label, self.line_point), self.direction) == 0


def property_b_metadata(first: Vec, second: Vec) -> list[PBMetadata]:
    """Rebuild the exhaustive three cases for two independent tail labels."""
    delta = sub(second, first)
    records = [
        PBMetadata(first, second, first, "heavy_is_first_tail", None),
        PBMetadata(second, first, second, "heavy_is_second_tail", None),
    ]
    records.extend(
        PBMetadata(mul(c, delta), first, delta, "both_tails_on_affine_line", c)
        for c in range(1, P)
    )

    assert det(first, second) != 0
    assert len(records) == P + 1
    assert len(set(records)) == P + 1
    for record in records:
        assert record.heavy != (0, 0)
        assert (0, 0) not in record.line
        assert record.heavy not in record.line
        assert len(record.line) == P
        assert len(record.envelope) == P + 1
        assert record.contains(first) and record.contains(second)
    return records


def metadata_row(record: PBMetadata) -> dict[str, object]:
    return {
        "heavy": signed(record.heavy),
        "line_point": signed(record.line_point),
        "direction": signed(record.direction),
        "case": record.case,
        "scalar_mod_233": record.scalar,
    }


def zero_submultisets(labels: list[Vec], bounds: list[int]) -> list[list[int]]:
    zeros: list[list[int]] = []
    for counts in itertools.product(*(range(bound + 1) for bound in bounds)):
        total = (0, 0)
        for count, label in zip(counts, labels):
            total = add(total, mul(count, label))
        if total == (0, 0):
            zeros.append(list(counts))
    return zeros


def multiset_intersection_size(
    left_labels: list[Vec], left_counts: list[int], right_labels: list[Vec], right_counts: list[int]
) -> int:
    left = Counter(dict(zip(left_labels, left_counts)))
    right = Counter(dict(zip(right_labels, right_counts)))
    return sum((left & right).values())


def main() -> None:
    e: Vec = (1, 0)
    f: Vec = (0, 1)
    t: Vec = neg(add(e, f))
    assert add(add(e, f), t) == (0, 0)
    assert len({e, f, t}) == 3

    left = property_b_metadata(f, t)
    right = property_b_metadata(e, t)
    raw_pair_count = len(left) * len(right)
    assert raw_pair_count == 54_756

    compatible = [
        (one, two)
        for one in left
        for two in right
        if two.contains(one.heavy) and one.contains(two.heavy)
    ]
    inverse_three = pow(3, -1, P)
    expected = [
        (t, t),
        (t, sub(t, e)),
        (sub(t, f), t),
        (mul(inverse_three, sub(t, f)), mul(inverse_three, sub(t, e))),
    ]
    assert len(compatible) == 4
    assert [(one.heavy, two.heavy) for one, two in compatible] == expected

    # Preserve and check the metadata behind the four cross-membership pairs.
    compatibility_rows: list[dict[str, object]] = []
    for index, (one, two) in enumerate(compatible):
        assert two.contains(one.heavy)
        assert one.contains(two.heavy)
        base_sum = add(one.heavy, two.heavy)

        if one.heavy == t or two.heavy == t:
            # The token names represent literal positions.  Distinct labels force
            # the K-position carrying t to differ from the e- and f-tail positions.
            witness_positions = ["tail_e", "tail_f", "kernel_t_0"]
            witness_labels = [e, f, t]
        else:
            assert base_sum == t
            assert one.heavy != two.heavy
            witness_positions = ["tail_e", "tail_f", "kernel_g1_0", "kernel_g2_0"]
            witness_labels = [e, f, one.heavy, two.heavy]

        assert len(witness_positions) == len(set(witness_positions))
        assert len(witness_labels) == len(set(witness_labels))
        witness_sum = (0, 0)
        for label in witness_labels:
            witness_sum = add(witness_sum, label)
        assert witness_sum == (0, 0)
        assert 0 < len(witness_positions) < 2 * P - 2

        compatibility_rows.append(
            {
                "index": index,
                "left": metadata_row(one),
                "right": metadata_row(two),
                "left_heavy_in_right_as": (
                    "heavy" if one.heavy == two.heavy else "affine_line"
                ),
                "right_heavy_in_left_as": (
                    "heavy" if two.heavy == one.heavy else "affine_line"
                ),
                "heavy_sum": signed(base_sum),
                "Q3_witness_positions": witness_positions,
                "Q3_witness_labels": [signed(label) for label in witness_labels],
                "Q3_witness_length": len(witness_positions),
                "Q3_witness_sum": signed(witness_sum),
                "Q3_witness_is_proper": True,
            }
        )

    atom_length = 2 * P - 1
    kernel_lower_bound = 435
    outside_kernel_upper_bound = atom_length - kernel_lower_bound
    heavy_multiplicity = P - 1
    heavy_in_kernel_lower_bound = heavy_multiplicity - outside_kernel_upper_bound
    assert (atom_length, outside_kernel_upper_bound, heavy_in_kernel_lower_bound) == (465, 30, 202)
    assert heavy_in_kernel_lower_bound > 0

    # Independent relaxed boundary construction: it has only Q1 and Q2.
    g = t
    h = sub(t, e)
    q1_exception = add(h, mul(3, g))
    q2_exception = add(g, mul(2, h))
    q1_labels = [g, h, f, q1_exception]
    q1_counts = [P - 1, P - 2, 1, 1]
    q2_labels = [h, g, e, q2_exception]
    q2_counts = [P - 1, P - 2, 1, 1]
    assert len(set(q1_labels)) == len(q1_labels)
    assert len(set(q2_labels)) == len(q2_labels)
    assert sum(q1_counts) == atom_length == sum(q2_counts)
    assert f == add(h, mul(-2, g))
    assert e == add(g, mul(-1, h))
    assert (-2 + 3) % P == 1 and (-1 + 2) % P == 1

    q1_sum = (0, 0)
    q2_sum = (0, 0)
    for label, count in zip(q1_labels, q1_counts):
        q1_sum = add(q1_sum, mul(count, label))
    for label, count in zip(q2_labels, q2_counts):
        q2_sum = add(q2_sum, mul(count, label))
    assert q1_sum == q2_sum == (0, 0)

    q1_zeros = zero_submultisets(q1_labels, q1_counts)
    q2_zeros = zero_submultisets(q2_labels, q2_counts)
    assert q1_zeros == [[0, 0, 0, 0], q1_counts]
    assert q2_zeros == [[0, 0, 0, 0], q2_counts]

    overlap = multiset_intersection_size(q1_labels, q1_counts, q2_labels, q2_counts)
    left_only = atom_length - overlap
    right_only = atom_length - overlap
    assert overlap == 462
    assert left_only == right_only == 3 <= 6
    assert overlap >= kernel_lower_bound

    core = {
        "schema": "unique_tail_property_b_two_max_mixed_exclusion/independent-audit-v1",
        "method": "fresh no-import reconstruction with full Property-B metadata",
        "prime": P,
        "property_b_metadata": {
            "left_tail_pair": [signed(f), signed(t)],
            "right_tail_pair": [signed(e), signed(t)],
            "left_record_count": len(left),
            "right_record_count": len(right),
            "raw_ordered_pairs": raw_pair_count,
            "mutual_cross_membership_pairs": len(compatible),
            "compatible_rows": compatibility_rows,
        },
        "common_kernel": {
            "maximal_atom_length": atom_length,
            "kernel_lower_bound": kernel_lower_bound,
            "outside_kernel_upper_bound": outside_kernel_upper_bound,
            "heavy_multiplicity": heavy_multiplicity,
            "heavy_positions_in_kernel_lower_bound": heavy_in_kernel_lower_bound,
        },
        "Q3": {
            "length": 2 * P - 2,
            "contains_tail_labels": [signed(e), signed(f)],
            "all_four_compatible_rows_have_distinct_proper_zero_sum_position_witnesses": True,
            "conclusion": "mixed three-atom branch UNSAT at the unified C_p^2 atom layer",
        },
        "two_max_only_relaxed_survivor": {
            "g": signed(g),
            "h": signed(h),
            "Q1": [
                {"label": signed(label), "multiplicity": count}
                for label, count in zip(q1_labels, q1_counts)
            ],
            "Q2": [
                {"label": signed(label), "multiplicity": count}
                for label, count in zip(q2_labels, q2_counts)
            ],
            "Q1_zero_submultisets": q1_zeros,
            "Q2_zero_submultisets": q2_zeros,
            "literal_multiset_overlap": overlap,
            "left_only_positions": left_only,
            "right_only_positions": right_only,
            "can_select_common_435_position_kernel": overlap >= kernel_lower_bound,
            "scope": "two maximal atoms only; Q3 and the complete exact-slice constraints are absent",
        },
        "conclusion": (
            "The p=233 two-maximal-plus-Q3 mixed branch is excluded; the explicitly "
            "feasible survivor applies only after deleting Q3 and other full-slice constraints."
        ),
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report = dict(core)
    report["certificate_sha256"] = sha256(canonical).hexdigest()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    destination = Path(__file__).with_name(
        "unique_tail_property_b_two_max_mixed_exclusion_independent_report.json"
    )
    destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
