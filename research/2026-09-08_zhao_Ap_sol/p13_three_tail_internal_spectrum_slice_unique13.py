#!/usr/bin/env python3
"""Exact p=13 unique-tail internal-spectrum slices.

The slice is deliberately local and exact.  For every normalized template from
the 42/534 cover in ``proofs/p13_unique_tail_labelled_attack.md`` it enumerates
every nonempty positional subset of U and all 0..9 available copies of q from
X.  Every induced quotient-zero block is checked against the complete short
length spectrum, the forbidden 9..28 interval, and uniqueness of the positive
core F3 tail.

No labels on the exterior ``Y minus U`` are introduced, so a survivor is only
a checkpoint for the 31- or 29-position exterior solver, never a local or
global counterexample.

The second slice treats the decomposable five-point projected tail.  It joins
the seven surviving axis coefficients with the actual height sum on its
two-point component and leaves only nine coefficient-height patterns.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from dataclasses import dataclass


P = 13
M = P - 4
Q = (1, 0, 0)

LENGTH_FAMILIES = {
    2: (1,),
    3: (1,),
    4: (1, 2),
    5: (1, 2),
    6: (1, 2, 3),
    7: (2, 3),
    8: (3,),
}

RANK_ONE_PROFILES = (
    (1, 1, 11),
    (1, 2, 10),
    (1, 3, 9),
)


@dataclass(frozen=True)
class Template:
    kind: str
    parameters: tuple[int, ...]
    # Each label is (q-axis coordinate, projection coordinate 1,
    # projection coordinate 2, actual a-height).
    labels: tuple[tuple[int, int, int, int], ...]


@dataclass(frozen=True)
class InducedBlock:
    tail: tuple[int, ...]
    core: int
    length: int
    family: int


def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a + b) % P for a, b in zip(left, right))


def vector_sum(values: list[tuple[int, ...]], dimension: int) -> tuple[int, ...]:
    total = (0,) * dimension
    for value in values:
        total = add(total, value[:dimension])
    return total


def normalized_templates() -> tuple[Template, ...]:
    templates: list[Template] = []

    # Rank-two projected atom.  Quotient and height shears kill the first two
    # axial/height coordinates; the total U-label is (-3q,3a).
    templates.append(
        Template(
            "rank2",
            (),
            (
                (0, 1, 0, 0),
                (0, 0, 1, 0),
                (10, 12, 12, 3),
            ),
        )
    )

    # Three rank-one projected atoms.  delta is the residual quotient-axis
    # coordinate and eta is the residual actual-height coordinate.
    for profile_index, profile in enumerate(RANK_ONE_PROFILES):
        for delta in range(P):
            for eta in range(P):
                templates.append(
                    Template(
                        "rank1",
                        (profile_index, delta, eta),
                        (
                            (0, profile[0], 0, 0),
                            (delta, profile[1], 0, eta),
                            ((10 - delta) % P, profile[2], 0, (3 - eta) % P),
                        ),
                    )
                )

    # One axial point alpha*q and a projected pair e,-e.  The axial point's
    # height cannot be removed by a shear through the rank-two projection.
    for alpha in (1, 2):
        for axis_height in range(P):
            templates.append(
                Template(
                    "axis_pair",
                    (alpha, axis_height),
                    (
                        (alpha, 0, 0, axis_height),
                        (0, 1, 0, 0),
                        ((10 - alpha) % P, 12, 0, (3 - axis_height) % P),
                    ),
                )
            )

    assert len(templates) == 534
    assert Counter(template.kind for template in templates) == {
        "rank2": 1,
        "rank1": 507,
        "axis_pair": 26,
    }
    return tuple(templates)


def audit_normal_form(template: Template) -> None:
    labels = template.labels
    assert len(labels) == 3
    assert vector_sum([label[:3] for label in labels], 3) == (10, 0, 0)
    assert sum(label[3] for label in labels) % P == 3


def induced_blocks(template: Template) -> tuple[tuple[InducedBlock, ...], tuple[str, ...]]:
    labels = template.labels
    blocks: list[InducedBlock] = []
    failures: list[str] = []

    for tail_size in range(1, 4):
        for tail in itertools.combinations(range(3), tail_size):
            quotient = vector_sum([labels[index][:3] for index in tail], 3)
            height = sum(labels[index][3] for index in tail) % P
            for core in range(M + 1):
                total = add(quotient, (core, 0, 0))
                if total != (0, 0, 0):
                    continue

                length = tail_size + core
                if 9 <= length <= 2 * P + 2:
                    failures.append(
                        f"forbidden_middle:tail={tail},core={core},length={length}"
                    )
                    continue
                if length not in LENGTH_FAMILIES:
                    failures.append(
                        f"missing_short_window:tail={tail},core={core},"
                        f"length={length},height={height}"
                    )
                    continue
                if height not in LENGTH_FAMILIES[length]:
                    failures.append(
                        f"wrong_actual_family:tail={tail},core={core},"
                        f"length={length},height={height}"
                    )
                    continue

                block = InducedBlock(tail, core, length, height)
                blocks.append(block)
                if height == 3 and core > 0 and not (
                    tail == (0, 1, 2) and core == 3
                ):
                    failures.append(
                        f"second_positive_F3:tail={tail},core={core},length={length}"
                    )

    intended = InducedBlock((0, 1, 2), 3, 6, 3)
    if intended not in blocks:
        failures.append("declared_positive_F3_missing")
    return tuple(blocks), tuple(failures)


def classify() -> dict[str, object]:
    survivors: list[Template] = []
    rejected: list[tuple[Template, tuple[str, ...]]] = []
    failure_counts: Counter[str] = Counter()

    for template in normalized_templates():
        audit_normal_form(template)
        _, failures = induced_blocks(template)
        if failures:
            rejected.append((template, failures))
            failure_counts.update(failure.split(":", 1)[0] for failure in failures)
        else:
            survivors.append(template)

    by_kind_before = Counter(template.kind for template in normalized_templates())
    by_kind_after = Counter(template.kind for template in survivors)
    axis_survivors = sorted(
        template.parameters
        for template in survivors
        if template.kind == "axis_pair"
    )

    assert len(survivors) == 511
    assert len(rejected) == 23
    assert by_kind_after == {"rank2": 1, "rank1": 507, "axis_pair": 3}
    assert axis_survivors == [(1, 1), (1, 2), (2, 1)]

    # For every rejected axis template the unique quotient-zero proper tail is
    # {1,2}; failures are therefore caused by its actual family or by its being
    # a second positive-core F3 tail, not by a hidden aggregate condition.
    assert all(template.kind == "axis_pair" for template, _ in rejected)

    return {
        "p": P,
        "type": [6, 3],
        "scope": "all U-internal positional subsets and all 0..9 X-core counts",
        "templates_before": len(normalized_templates()),
        "templates_after": len(survivors),
        "templates_rejected": len(rejected),
        "by_kind_before": dict(sorted(by_kind_before.items())),
        "by_kind_after": dict(sorted(by_kind_after.items())),
        "axis_pair_survivors_alpha_height": [
            list(item) for item in axis_survivors
        ],
        "failure_counts": dict(sorted(failure_counts.items())),
        "status": "PROVED_FINITE_SLICE_STRICT_REDUCTION",
        "boundary": (
            "Y\\U labels, zero-core F3 blocks, their long complements, and "
            "TOP/CONST are not searched"
        ),
    }


def surviving_three_tail_templates() -> tuple[Template, ...]:
    return tuple(
        template
        for template in normalized_templates()
        if not induced_blocks(template)[1]
    )


def component_failure(size: int, core: int, height: int) -> str | None:
    """Failure of one projected-zero component completed with X_core."""
    if core > M:
        return None
    length = size + core
    if 9 <= length <= 2 * P + 2:
        return "forbidden_middle"
    if length not in LENGTH_FAMILIES or height not in LENGTH_FAMILIES[length]:
        return "wrong_actual_family"
    if height == 3 and core > 0:
        return "second_positive_F3"
    return None


def five_tail_decomposable_height_slice() -> dict[str, object]:
    """Join the P+Q coefficient table to the actual component height."""
    survivors: list[tuple[int, int, int]] = []
    coefficients_before: list[int] = []
    for coefficient in range(P):
        other = (3 - coefficient) % P
        coefficient_has_survivor = False
        for p_height in range(P):
            q_height = (3 - p_height) % P
            failures = tuple(
                failure
                for failure in (
                    component_failure(2, coefficient, p_height),
                    component_failure(3, other, q_height),
                )
                if failure is not None
            )
            if not failures:
                survivors.append((coefficient, p_height, q_height))
                coefficient_has_survivor = True
        if coefficient_has_survivor:
            coefficients_before.append(coefficient)

    expected = [
        (0, 1, 2),
        (1, 1, 2),
        (2, 1, 2),
        (2, 2, 1),
        (3, 2, 1),
        (4, 1, 2),
        (4, 2, 1),
        (5, 2, 1),
        (12, 1, 2),
    ]
    assert coefficients_before == [0, 1, 2, 3, 4, 5, 12]
    assert survivors == expected
    return {
        "p": P,
        "type": [8, 3],
        "projected_branch": "rho(U) splits as projected atoms P+Q (2+3)",
        "coefficient_height_pairs_before": 7 * P,
        "coefficient_height_pairs_after": len(survivors),
        "survivors_c_hP_hQ": [list(item) for item in survivors],
        "status": "PROVED_FINITE_SLICE_STRICT_REDUCTION",
        "boundary": (
            "internal labels inside P and Q, the projected-atom branch, "
            "Y\\U labels, zero-core F3 blocks, and long complements are not searched"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--emit-three-survivors",
        action="store_true",
        help="emit the 511 normalized three-point survivor records as JSONL",
    )
    parser.add_argument(
        "--emit-five-patterns",
        action="store_true",
        help="emit the nine decomposable five-point component patterns as JSONL",
    )
    args = parser.parse_args()

    if args.emit_three_survivors:
        for index, template in enumerate(surviving_three_tail_templates()):
            print(
                json.dumps(
                    {
                        "checkpoint_index": index,
                        "p": P,
                        "unique_type": [6, 3],
                        "kind": template.kind,
                        "parameters": list(template.parameters),
                        "normalized_U": [list(label) for label in template.labels],
                        "exterior_position_count": 31,
                    },
                    sort_keys=True,
                )
            )
        return

    if args.emit_five_patterns:
        result = five_tail_decomposable_height_slice()
        for index, pattern in enumerate(result["survivors_c_hP_hQ"]):
            print(
                json.dumps(
                    {
                        "checkpoint_index": index,
                        "p": P,
                        "unique_type": [8, 3],
                        "projected_branch": "2+3",
                        "c_hP_hQ": pattern,
                        "exterior_position_count": 29,
                    },
                    sort_keys=True,
                )
            )
        return

    result = {
        "three_point_tail": classify(),
        "five_point_decomposable_tail": five_tail_decomposable_height_slice(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
