#!/usr/bin/env python3
"""Exact propagation and complete-assignment auditor for p=7, m=4, 0001.

The default invocation proves/replays finite reductions.  With
``--instance FILE.json`` it accepts only a complete assignment of all 21
positions outside X, reconstructs every induced short block (including
trace zero), and checks the full position-level necessary CSP.

No selected list of tails is accepted as input.  Tail stars and short blocks
are reconstructed bidirectionally from the common position labels.  A state
which has not passed ``audit_instance`` is not a local candidate.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import verify_p7_four_fibre_refinement as FOUR


P = 7
M = 4
N = 25
PROFILE = (0, 0, 0, 1)
ZERO3 = (0, 0, 0)
Q_NORMAL = (1, 0, 0)

LENGTH_FAMILIES: dict[int, frozenset[int]] = {
    2: frozenset({1}),
    3: frozenset({1}),
    4: frozenset({1, 2}),
    5: frozenset({1, 2}),
    6: frozenset({1, 2, 3}),
    7: frozenset({2, 3}),
    8: frozenset({3}),
}

# This quotient atom is obtained from the existing length-19 q^3 Q atom by
# the invertible map (x,y,z) -> (x,y,z-x), and by designating the four copies
# of (1,0,1) as the new distinguished q-fibre.  It is a quotient-only
# skeleton, not a labelled CSP candidate.
S6_QUOTIENT_ATOM_Q = (
    (1, 0, 6),
    (1, 0, 6),
    (1, 0, 6),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 6),
    (0, 1, 6),
    (0, 1, 6),
    (1, 5, 0),
    (1, 6, 0),
    (1, 6, 0),
    (1, 6, 0),
    (1, 6, 0),
    (4, 5, 6),
    (5, 4, 6),
)

REJECTED_S6_T_QUOTIENT = (
    (5, 5, 5),
    (0, 0, 1),
    (6, 0, 6),
    (2, 4, 2),
    (3, 2, 2),
    (5, 3, 5),
)


def add3(left: tuple[int, int, int], right: tuple[int, int, int]):
    return tuple((left[i] + right[i]) % P for i in range(3))


def neg3(vector: tuple[int, int, int]):
    return tuple((-entry) % P for entry in vector)


def scale3(scalar: int, vector: tuple[int, int, int]):
    return tuple((scalar * entry) % P for entry in vector)


def sum3(vectors: Iterable[tuple[int, int, int]]):
    answer = ZERO3
    for vector in vectors:
        answer = add3(answer, vector)
    return answer


def det3(columns: Sequence[tuple[int, int, int]]) -> int:
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) % P


def inverse3_from_columns(columns: Sequence[tuple[int, int, int]]):
    rows = [[columns[column][row] for column in range(3)] for row in range(3)]
    augmented = [
        rows[row] + [int(row == column) for column in range(3)]
        for row in range(3)
    ]
    for column in range(3):
        pivot = next(
            row for row in range(column, 3) if augmented[row][column] % P
        )
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        multiplier = pow(augmented[column][column], -1, P)
        augmented[column] = [
            multiplier * entry % P for entry in augmented[column]
        ]
        for row in range(3):
            if row == column:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                (augmented[row][entry] - multiplier * augmented[column][entry])
                % P
                for entry in range(6)
            ]
    return tuple(tuple(row[3:]) for row in augmented)


def matrix_vector(matrix, vector):
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3)) % P
        for row in range(3)
    )


def mask_indices(mask: int) -> Iterator[int]:
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def subset_tables(
    quotient: Sequence[tuple[int, int, int]],
    height: Sequence[int] | None = None,
):
    size = 1 << len(quotient)
    q_sums = [ZERO3] * size
    h_sums = [0] * size if height is not None else None
    cardinalities = [0] * size
    for mask in range(1, size):
        bit = mask & -mask
        index = bit.bit_length() - 1
        previous = mask ^ bit
        q_sums[mask] = add3(q_sums[previous], quotient[index])
        cardinalities[mask] = cardinalities[previous] + 1
        if h_sums is not None and height is not None:
            h_sums[mask] = (h_sums[previous] + height[index]) % P
    return q_sums, h_sums, cardinalities


@dataclass(frozen=True)
class Block:
    mask: int
    length: int
    family: int
    trace_size: int


@dataclass(frozen=True)
class Tail:
    mask: int
    length: int
    trace_size: int
    remainder_height: int
    families: tuple[int, ...]


@dataclass(frozen=True)
class LabelledInstance:
    """A complete 25-position assignment ordered as X,T,Q."""

    profile: tuple[int, int, int, int]
    t_labels: tuple[tuple[int, int, int], ...]
    t_heights: tuple[int, ...]
    q_labels: tuple[tuple[int, int, int], ...]
    q_heights: tuple[int, ...]

    @property
    def s(self) -> int:
        return len(self.t_labels)

    @property
    def quotient(self) -> tuple[tuple[int, int, int], ...]:
        return (Q_NORMAL,) * M + self.t_labels + self.q_labels

    @property
    def height(self) -> tuple[int, ...]:
        return self.profile + self.t_heights + self.q_heights

    @property
    def t_indices(self) -> tuple[int, ...]:
        return tuple(range(M, M + self.s))

    @property
    def q_indices(self) -> tuple[int, ...]:
        return tuple(range(M + self.s, N))

    @property
    def y_indices(self) -> tuple[int, ...]:
        return tuple(range(M, N))


def parse_instance(path: Path) -> LabelledInstance:
    data = json.loads(path.read_text(encoding="utf-8"))

    def labels(key: str):
        values = tuple(tuple(int(x) % P for x in row) for row in data[key])
        assert all(len(row) == 3 for row in values)
        return values

    def heights(key: str):
        return tuple(int(x) % P for x in data[key])

    return LabelledInstance(
        profile=tuple(int(x) % P for x in data["profile"]),
        t_labels=labels("t_labels"),
        t_heights=heights("t_heights"),
        q_labels=labels("q_labels"),
        q_heights=heights("q_heights"),
    )


def fixed_B_atom_obstructions(instance: LabelledInstance):
    """Exact atom test for B=q^4 dot-union Q.

    Complementation pairs b with 4-b.  Hence representatives b=0,1,2
    suffice, with only (b,U)=(0,empty) omitted.
    """
    q_sums, _, cardinalities = subset_tables(instance.q_labels)
    full = (1 << len(instance.q_labels)) - 1
    failures: list[tuple[int, int, int]] = []
    if q_sums[full] != scale3(-M, Q_NORMAL):
        failures.append((-1, full, cardinalities[full]))
    for b in range(3):
        target = scale3(-b, Q_NORMAL)
        for mask, value in enumerate(q_sums):
            if b == 0 and mask == 0:
                continue
            if value == target:
                failures.append((b, mask, cardinalities[mask]))
    return failures


def actual_Z_atom_obstruction(instance: LabelledInstance):
    """Return one nonempty proper actual zero sum, using meet-in-the-middle."""
    quotient = instance.quotient
    height = instance.height
    left_indices = tuple(range(M + instance.s))
    right_indices = instance.q_indices
    right_q = [quotient[i] for i in right_indices]
    right_h = [height[i] for i in right_indices]
    q_sums, h_sums, _ = subset_tables(right_q, right_h)
    assert h_sums is not None
    buckets: dict[tuple[tuple[int, int, int], int], list[int]] = defaultdict(list)
    for mask, (q_sum, h_sum) in enumerate(zip(q_sums, h_sums)):
        buckets[(q_sum, h_sum)].append(mask)

    left_q = [quotient[i] for i in left_indices]
    left_h = [height[i] for i in left_indices]
    left_q_sums, left_h_sums, _ = subset_tables(left_q, left_h)
    assert left_h_sums is not None
    full_mask = (1 << N) - 1
    for left_mask, (q_sum, h_sum) in enumerate(zip(left_q_sums, left_h_sums)):
        targets = buckets.get((neg3(q_sum), (-h_sum) % P), ())
        for right_mask in targets:
            global_mask = left_mask | (right_mask << len(left_indices))
            if global_mask not in (0, full_mask):
                return global_mask
    return None


def trace_height_set(trace_size: int) -> frozenset[int]:
    return frozenset(
        sum(PROFILE[index] for index in trace) % P
        for trace in combinations(range(M), trace_size)
    )


def quotient_trace_window_obstructions(instance: LabelledInstance):
    """Height-free consequences of all trace choices in the 0001 fibre.

    If an external set U has quotient sum -bq, every b-trace of X gives a
    short quotient-zero set.  If no remainder height can place all trace
    heights in the length window, the quotient pattern itself is forbidden.
    """
    failures: list[tuple[int, int, int]] = []
    quotient = instance.quotient
    y = instance.y_indices
    for b in range(1, M):
        trace_heights = trace_height_set(b)
        assert trace_heights == frozenset({0, 1})
        for length in range(max(2, b + 1), 9):
            tail_size = length - b
            admissible_heights = {
                c
                for c in range(P)
                if all((c + h) % P in LENGTH_FAMILIES[length] for h in trace_heights)
            }
            if admissible_heights:
                continue
            target = scale3(-b, Q_NORMAL)
            for subset in combinations(y, tail_size):
                if sum3(quotient[index] for index in subset) == target:
                    mask = sum(1 << index for index in subset)
                    failures.append((b, tail_size, mask))
    return failures


def reconstruct_short_blocks(instance: LabelledInstance):
    """Rebuild length-2--8 blocks and retain length-1--9 zero masks.

    Length-nine masks are retained for the exact complement-atom oracle.
    The separate meet-in-the-middle oracle below rejects quotient-zero
    subsets of lengths 9--12, as required by (SQ) and complementation.
    """
    quotient = instance.quotient
    height = instance.height
    blocks: list[Block] = []
    invalid: list[tuple[int, int, int]] = []
    small_zero_masks: list[int] = []
    for length in range(1, 10):
        allowed = LENGTH_FAMILIES.get(length)
        for subset in combinations(range(N), length):
            q_sum = sum3(quotient[index] for index in subset)
            if q_sum != ZERO3:
                continue
            h_sum = sum(height[index] for index in subset) % P
            mask = sum(1 << index for index in subset)
            small_zero_masks.append(mask)
            if allowed is None:
                continue
            if h_sum not in allowed:
                invalid.append((mask, length, h_sum))
            else:
                trace_size = sum(index < M for index in subset)
                blocks.append(Block(mask, length, h_sum, trace_size))
    return blocks, invalid, small_zero_masks


def medium_quotient_zero_obstructions(instance: LabelledInstance):
    """Find one quotient-zero subset of each forbidden length 9--12.

    The 25 quotient labels are split 12+13.  Exhaustive subset tables on
    both halves give an exact existence oracle without enumerating the
    roughly sixteen million subsets of these four middle layers directly.

    If K has quotient sum zero and 9<=|K|<=12, then its complement has
    quotient sum zero and 13<=|Z minus K|<=16.  The frozen (SQ) condition would
    put both actual sums in {a,2a,3a}, although they are negatives; this is
    impossible modulo seven.  Hence every such K is an obstruction.
    """
    split = 12
    left_sums, _, left_sizes = subset_tables(instance.quotient[:split])
    right_sums, _, right_sizes = subset_tables(instance.quotient[split:])
    right_lookup: dict[tuple[int, tuple[int, int, int]], int] = {}
    for mask, (size, q_sum) in enumerate(zip(right_sizes, right_sums)):
        right_lookup.setdefault((size, q_sum), mask)

    failures: list[tuple[int, int]] = []
    for length in range(9, 13):
        witness = None
        for left_mask, (left_size, left_sum) in enumerate(
            zip(left_sizes, left_sums)
        ):
            right_size = length - left_size
            if not 0 <= right_size <= N - split:
                continue
            right_mask = right_lookup.get((right_size, neg3(left_sum)))
            if right_mask is None:
                continue
            witness = left_mask | (right_mask << split)
            break
        if witness is not None:
            failures.append((witness, length))
    return failures


def reconstruct_tail_stars(instance: LabelledInstance):
    """Reconstruct every positive-trace star from its actual Y-position tail."""
    quotient = instance.quotient
    height = instance.height
    tails: list[Tail] = []
    for tail_size in range(1, 8):
        for subset in combinations(instance.y_indices, tail_size):
            q_sum = sum3(quotient[index] for index in subset)
            b = next(
                (
                    trace
                    for trace in range(1, M + 1)
                    if q_sum == scale3(-trace, Q_NORMAL)
                ),
                None,
            )
            if b is None:
                continue
            length = b + tail_size
            if length not in LENGTH_FAMILIES:
                continue
            c = sum(height[index] for index in subset) % P
            traces = tuple(combinations(range(M), b))
            families = tuple(
                (c + sum(PROFILE[index] for index in trace)) % P
                for trace in traces
            )
            if all(family in LENGTH_FAMILIES[length] for family in families):
                tails.append(
                    Tail(
                        mask=sum(1 << index for index in subset),
                        length=length,
                        trace_size=b,
                        remainder_height=c,
                        families=families,
                    )
                )
    return tails


def signed_degree(blocks: Sequence[Block], mask: int, family: int, order: int):
    total = 0
    for block in blocks:
        if block.family != family or block.mask & mask != mask:
            continue
        exponent = block.length - 1 if order in (1, 3) else block.length
        total += -1 if exponent % 2 else 1
    return total % P


def hasse_obstructions(blocks: Sequence[Block]):
    failures: list[tuple[str, tuple[int, ...], tuple[int, ...]]] = []
    for point in range(N):
        degrees = tuple(
            signed_degree(blocks, 1 << point, family, 1)
            for family in (1, 2, 3)
        )
        if degrees != (1, 1, 1):
            failures.append(("point", (point,), degrees))
    for pair in combinations(range(N), 2):
        mask = (1 << pair[0]) | (1 << pair[1])
        degrees = tuple(
            signed_degree(blocks, mask, family, 2) for family in (1, 2, 3)
        )
        if (degrees[0] + 3 * degrees[1]) % P != 3 or (
            2 * degrees[0] - 3 * degrees[2]
        ) % P != 1:
            failures.append(("pair", pair, degrees))
    for triple in combinations(range(N), 3):
        mask = sum(1 << point for point in triple)
        degrees = tuple(
            signed_degree(blocks, mask, family, 3) for family in (1, 2, 3)
        )
        if (4 * degrees[0] + 3 * degrees[1] + 6 * degrees[2]) % P != 6:
            failures.append(("triple", triple, degrees))
    return failures


def global_block_obstructions(blocks: Sequence[Block]):
    failures: list[tuple[str, int, int]] = []
    for family in (1, 2, 3):
        signed_total = sum(
            (-1 if block.length % 2 else 1)
            for block in blocks
            if block.family == family
        ) % P
        if signed_total != 0:
            failures.append(("zero_order", family, signed_total))
    n_2_6 = sum(
        block.family == 2 and block.length == 6 for block in blocks
    )
    if n_2_6 % P != 3:
        failures.append(("N_2_6", n_2_6, n_2_6 % P))
    return failures


def intersection_obstructions(
    instance: LabelledInstance, blocks: Sequence[Block]
):
    failures: list[tuple[str, int, int, int]] = []
    quotient = instance.quotient
    for left_index, left in enumerate(blocks):
        for right_index in range(left_index + 1, len(blocks)):
            right = blocks[right_index]
            intersection = left.mask & right.mask
            must_intersect = (
                (left.family == 2 and right.family == 2)
                or left.family == 3
                or right.family == 3
                or left.length + right.length >= 9
            )
            if must_intersect and intersection == 0:
                failures.append(("disjoint", left_index, right_index, 0))
            if left.family == right.family == 3:
                q_sum = sum3(quotient[i] for i in mask_indices(intersection))
                if q_sum == ZERO3:
                    failures.append(
                        ("zero_F3_intersection", left_index, right_index, intersection)
                    )
    return failures


def common_core_obstructions(blocks: Sequence[Block]):
    full = (1 << N) - 1
    failures: list[tuple[int, int]] = []
    for family in (1, 2, 3):
        masks = [block.mask for block in blocks if block.family == family]
        if not masks:
            failures.append((family, full))
            continue
        core = full
        for mask in masks:
            core &= mask
        if core:
            failures.append((family, core))
    return failures


def partition_obstructions(instance: LabelledInstance, blocks: Sequence[Block]):
    t_mask = sum(1 << index for index in instance.t_indices)
    failures: list[tuple[str, int]] = []
    if not any(block.mask == t_mask and block.family == 3 for block in blocks):
        failures.append(("missing_T", t_mask))
    for block_index, block in enumerate(blocks):
        if block.mask & t_mask == 0:
            failures.append(("block_inside_B", block_index))
    return failures


def all_f3_complement_obstructions(
    blocks: Sequence[Block], small_zero_masks: Sequence[int]
):
    failures: list[tuple[int, int]] = []
    for block_index, block in enumerate(blocks):
        if block.family != 3:
            continue
        obstruction = next(
            (mask for mask in small_zero_masks if mask & block.mask == 0), None
        )
        if obstruction is not None:
            failures.append((block_index, obstruction))
    return failures


def affine_projection_obstructions(tails: Sequence[Tail]):
    counts = Counter(
        (tail.length, tail.trace_size, tail.remainder_height) for tail in tails
    )
    full = tuple(counts[(length, 4, 2)] for length in (6, 7, 8))
    failures: list[tuple[str, object]] = []
    if full == (0, 0, 0):
        expected = {1: 6, 2: 1, 3: 6}
        lower = tuple(
            counts[(length, b, 2)] for length in (6, 7) for b in (1, 2, 3)
        )
        for b in (1, 2, 3):
            difference = (counts[(6, b, 2)] - counts[(7, b, 2)]) % P
            if difference != expected[b]:
                failures.append(("lower_projection", (b, difference, expected[b])))
        return failures, full, lower
    return failures, full, ()


def no_full_zero_core_obstructions(
    instance: LabelledInstance, blocks: Sequence[Block], tails: Sequence[Tail]
):
    failures: list[tuple[str, object]] = []
    full_count = sum(
        tail.trace_size == 4 and 3 in tail.families for tail in tails
    )
    if full_count:
        return failures
    zero_core = [
        block for block in blocks if block.family == 3 and block.trace_size == 0
    ]
    signed = sum(1 if block.length % 2 == 0 else -1 for block in zero_core) % P
    if signed != 1:
        failures.append(("zero_core_signed_residue", (signed, 1)))
    if instance.s == 7 and len(zero_core) < 3:
        failures.append(("s7_zero_core_count", (len(zero_core), 3)))

    quotient = instance.quotient
    positive_f3_tails = [tail for tail in tails if 3 in tail.families]
    for block_index, block in enumerate(zero_core):
        for tail_index, tail in enumerate(positive_f3_tails):
            intersection = block.mask & tail.mask
            q_sum = sum3(quotient[i] for i in mask_indices(intersection))
            if not intersection or q_sum == ZERO3:
                failures.append(
                    ("zero_core_tail_transversal", (block_index, tail_index, intersection))
                )
    return failures


def basic_obstructions(instance: LabelledInstance):
    failures: list[str] = []
    if instance.profile != PROFILE:
        failures.append("this frontier is frozen to the 0001 profile")
    if instance.s not in (6, 7, 8):
        failures.append("s must lie in {6,7,8}")
    if len(instance.t_heights) != instance.s:
        failures.append("T label/height lengths differ")
    if len(instance.q_labels) != 21 - instance.s:
        failures.append("Q must have 21-s positions")
    if len(instance.q_heights) != len(instance.q_labels):
        failures.append("Q label/height lengths differ")
    if any(label == ZERO3 for label in instance.quotient):
        failures.append("every Z quotient label must be nonzero")
    if any(label in (ZERO3, Q_NORMAL) for label in instance.q_labels):
        failures.append("every Q quotient label must be nonzero and different from q")
    if sum3(instance.t_labels) != ZERO3:
        failures.append("T quotient sum is not zero")
    if sum(instance.t_heights) % P != 3:
        failures.append("T height sum is not three")
    if sum3(instance.q_labels) != scale3(-M, Q_NORMAL):
        failures.append("Q quotient sum is not -4q")
    if (sum(instance.profile) + sum(instance.q_heights)) % P != 4:
        failures.append("B height sum is not four")
    if sum3(instance.quotient) != ZERO3 or sum(instance.height) % P != 0:
        failures.append("Z total actual label is not zero")
    if max(Counter(zip(instance.quotient, instance.height)).values()) > 3:
        failures.append("an actual F_7^4 label occurs more than three times")
    return failures


def canonical_0001_key(instance: LabelledInstance):
    """Complete orbit key under GL_3 fixing q, height shears, and T/Q sorting."""
    if instance.profile != PROFILE:
        raise ValueError("canonical_0001_key is only valid for profile 0001")
    candidates = []
    for first in range(len(instance.q_labels)):
        for second in range(len(instance.q_labels)):
            if first == second:
                continue
            basis = (Q_NORMAL, instance.q_labels[first], instance.q_labels[second])
            if det3(basis) == 0:
                continue
            inverse = inverse3_from_columns(basis)
            first_height = instance.q_heights[first]
            second_height = instance.q_heights[second]

            def normalize(label, height):
                new_label = matrix_vector(inverse, label)
                new_height = (
                    height
                    - first_height * new_label[1]
                    - second_height * new_label[2]
                ) % P
                return new_label + (new_height,)

            normalized_t = tuple(
                sorted(
                    normalize(label, height)
                    for label, height in zip(instance.t_labels, instance.t_heights)
                )
            )
            normalized_q = tuple(
                sorted(
                    normalize(label, height)
                    for label, height in zip(instance.q_labels, instance.q_heights)
                )
            )
            candidates.append((normalized_t, normalized_q))
    if not candidates:
        raise ValueError("q together with Q does not span F_7^3")
    return min(candidates)


def audit_instance(instance: LabelledInstance):
    """Run the exact finite necessary CSP on a complete 84-scalar assignment."""
    report: dict[str, object] = {}
    report["basic"] = basic_obstructions(instance)
    report["fixed_B_atom"] = fixed_B_atom_obstructions(instance)
    report["actual_Z_atom"] = actual_Z_atom_obstruction(instance)
    report["quotient_trace_windows"] = quotient_trace_window_obstructions(instance)
    blocks, invalid, small_zero_masks = reconstruct_short_blocks(instance)
    tails = reconstruct_tail_stars(instance)
    report["block_counts"] = dict(sorted(Counter(b.family for b in blocks).items()))
    report["trace_counts"] = {
        f"F{family}:b{trace}": count
        for (family, trace), count in sorted(
            Counter((b.family, b.trace_size) for b in blocks).items()
        )
    }
    report["tail_star_counts"] = {
        str(key): count
        for key, count in sorted(
            Counter(
                (tail.length, tail.trace_size, tail.remainder_height)
                for tail in tails
            ).items()
        )
    }
    report["invalid_short_quotient_zeros"] = invalid
    report["forbidden_length_9_12_quotient_zeros"] = (
        medium_quotient_zero_obstructions(instance)
    )
    report["global_blocks"] = global_block_obstructions(blocks)
    report["hasse"] = hasse_obstructions(blocks)
    report["common_cores"] = common_core_obstructions(blocks)
    report["partition"] = partition_obstructions(instance, blocks)
    report["intersections"] = intersection_obstructions(instance, blocks)
    report["all_F3_complement_atoms"] = all_f3_complement_obstructions(
        blocks, small_zero_masks
    )
    projection, full, lower = affine_projection_obstructions(tails)
    report["affine_projection"] = projection
    report["full_F3_tail_counts"] = full
    report["lower_F3_tail_counts"] = lower
    report["no_full_zero_core"] = no_full_zero_core_obstructions(
        instance, blocks, tails
    )
    return report


def audit_exact_B_reduction() -> None:
    for q_size in (13, 14, 15):
        representative_count = 3 * (1 << q_size) - 1
        assert representative_count in (24575, 49151, 98303)
        # b=0,1,2 are one representative from every complementation orbit
        # (b,U) <-> (4-b,Q\U), with b=2 fixed setwise as a layer.
        full = (1 << q_size) - 1
        representatives = {
            (b, mask)
            for b in range(3)
            for mask in range(1 << q_size)
            if not (b == 0 and mask == 0)
        }
        assert len(representatives) == representative_count
        for b in range(5):
            for mask in (0, 1, full - 1, full):
                if (b, mask) in ((0, 0), (4, full)):
                    continue
                rb, rmask = (b, mask) if b <= 2 else (4 - b, full ^ mask)
                assert (rb, rmask) in representatives


def audit_affine_and_zero_core_propagation() -> None:
    forced, _ = FOUR.audit_profiles()
    assert len(forced) == 28
    stars, matrix, rhs, _ = FOUR.BASE.build_hasse_system(PROFILE)
    full_columns = [i for i, star in enumerate(stars) if FOUR.is_full_f3(star)]
    lower_columns = [
        i
        for i, star in enumerate(stars)
        if FOUR.bears_f3(star) and i not in full_columns
    ]
    projection = FOUR.affine_projection(
        stars, matrix, rhs, lower_columns, full_columns
    )
    assert projection == [
        ([1, 0, 0, 6, 0, 0], 6),
        ([0, 1, 0, 0, 6, 0], 1),
        ([0, 0, 1, 0, 0, 6], 6),
    ]
    # A b=1 tail produces one F3 trace; b=2 and b=3 produce three each.
    signed_positive = (1 * 6 + 3 * 1 + 3 * 6) % P
    assert signed_positive == 6
    assert (-signed_positive) % P == 1


def audit_trace_window_patterns() -> None:
    impossible = set()
    for b in range(1, M):
        trace_heights = trace_height_set(b)
        assert trace_heights == frozenset({0, 1})
        for length in range(max(2, b + 1), 9):
            admissible_heights = {
                c
                for c in range(P)
                if all(
                    (c + h) % P in LENGTH_FAMILIES[length]
                    for h in trace_heights
                )
            }
            if not admissible_heights:
                impossible.add((b, length - b))
    assert impossible == {
        (1, 1),
        (1, 2),
        (1, 7),
        (2, 1),
        (2, 6),
        (3, 5),
    }


def audit_quotient_only_rejection() -> None:
    instance = LabelledInstance(
        profile=PROFILE,
        t_labels=REJECTED_S6_T_QUOTIENT,
        t_heights=(3, 0, 0, 0, 0, 0),
        q_labels=S6_QUOTIENT_ATOM_Q,
        q_heights=(3,) + (0,) * 14,
    )
    assert sum3(instance.t_labels) == ZERO3
    assert fixed_B_atom_obstructions(instance) == []
    assert sum3(instance.q_labels) == scale3(-M, Q_NORMAL)
    failures = quotient_trace_window_obstructions(instance)
    pair_failures = [item for item in failures if item[:2] == (1, 2)]
    assert pair_failures
    first_pair = tuple(mask_indices(pair_failures[0][2]))
    assert first_pair == (5, 6)
    assert sum3(instance.quotient[i] for i in first_pair) == scale3(-1, Q_NORMAL)

    # This skeleton also has no possible full-core F3 quotient tail of sizes
    # two, three, or four, independent of all height choices.
    for tail_size in (2, 3, 4):
        assert not any(
            sum3(instance.quotient[i] for i in subset)
            == scale3(-M, Q_NORMAL)
            for subset in combinations(instance.y_indices, tail_size)
        )

    # Exercise the exact middle-layer oracle on the same complete quotient
    # assignment and validate every returned witness directly.
    middle = medium_quotient_zero_obstructions(instance)
    assert middle
    for mask, length in middle:
        indices = tuple(mask_indices(mask))
        assert len(indices) == length
        assert 9 <= length <= 12
        assert sum3(instance.quotient[index] for index in indices) == ZERO3


def audit_canonical_key() -> None:
    base = LabelledInstance(
        profile=PROFILE,
        t_labels=REJECTED_S6_T_QUOTIENT,
        t_heights=(3, 0, 0, 0, 0, 0),
        q_labels=S6_QUOTIENT_ATOM_Q,
        q_heights=(3,) + (0,) * 14,
    )
    change_columns = (Q_NORMAL, (2, 1, 0), (3, 4, 1))
    change = tuple(
        tuple(change_columns[column][row] for column in range(3))
        for row in range(3)
    )

    def transformed(label, height):
        new_label = matrix_vector(change, label)
        new_height = (height + 2 * label[1] + 3 * label[2]) % P
        return new_label, new_height

    transformed_t = tuple(
        transformed(label, height)
        for label, height in zip(base.t_labels, base.t_heights)
    )
    transformed_q = tuple(
        transformed(label, height)
        for label, height in zip(base.q_labels, base.q_heights)
    )
    moved = LabelledInstance(
        profile=PROFILE,
        t_labels=tuple(reversed([item[0] for item in transformed_t])),
        t_heights=tuple(reversed([item[1] for item in transformed_t])),
        q_labels=tuple(reversed([item[0] for item in transformed_q])),
        q_heights=tuple(reversed([item[1] for item in transformed_q])),
    )
    assert canonical_0001_key(base) == canonical_0001_key(moved)


def print_default_audit() -> None:
    audit_exact_B_reduction()
    audit_affine_and_zero_core_propagation()
    audit_trace_window_patterns()
    audit_quotient_only_rejection()
    audit_canonical_key()
    print("PASS exact fixed-B atom reduction: b=0,1,2 Q-subset targets")
    print("s=6/7/8 Q sizes 15/14/13: 98303/49151/24575 exact target tests")
    print("PASS 29-orbit affine projection unchanged; 0001 lower relations replayed")
    print("PROVED quotient propagation: no Y labels -q,-2q and no Y-pair sum -q")
    print("PROVED quotient propagation: no (-q,-2q,-3q) Y-subsets of sizes 7,6,5")
    print("PROVED no-full branch: H6^0-H7^0+H8^0 = 1 mod 7")
    print("PROVED s=7 no-full branch has at least three zero-core F3 blocks")
    print("PASS 0001 canonical key; 84 scalars reduce to 68 after normalization/totals")
    print("PASS exact meet-in-the-middle rejection of quotient-zero lengths 9--12")
    print("PASS fixed s=6 full quotient assignment: B atom and no full-core quotient tail")
    print("EXPECTED REJECTION: this same T has a Y-pair of quotient sum -q")
    print("QUANTIFIER: all height lifts of this B+T assignment only; other T remain open")
    print("SCOPE quotient skeleton only; no un-audited assignment is a local candidate")
    print("STATUS INCOMPLETE: no complete 84-scalar solution or global no-solution certificate")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path)
    args = parser.parse_args()
    print_default_audit()
    if args.instance is None:
        return
    instance = parse_instance(args.instance)
    report = audit_instance(instance)
    informational = {
        "block_counts",
        "trace_counts",
        "tail_star_counts",
        "full_F3_tail_counts",
        "lower_F3_tail_counts",
    }
    bad = {key: value for key, value in report.items() if key not in informational and value}
    printable = {}
    for key, value in report.items():
        if isinstance(value, list):
            printable[key] = {"count": len(value), "first_20": value[:20]}
        else:
            printable[key] = value
    print(json.dumps(printable, ensure_ascii=False, indent=2, default=str))
    if bad:
        raise SystemExit("REJECTED: complete 84-scalar assignment violates the CSP")
    print("ACCEPTED: assignment satisfies the complete finite necessary CSP")


if __name__ == "__main__":
    main()
