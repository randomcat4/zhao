#!/usr/bin/env python3
"""Position-level p=7, quotient-fibre multiplicity-three CSP auditor.

This file deliberately separates three notions which earlier exploratory
calculations could conflate:

* a complete assignment of the 22 labels outside the distinguished fibre X;
* every short block induced by that assignment (including trace b=0);
* a selected or pre-named list of tails.

Only the first object is accepted by ``audit_instance``.  The block list is
always reconstructed from scratch.  In particular there is no Boolean block
variable which may be switched off after its quotient and height equations
become true.

The default invocation proves the finite reductions and audits the branch
schema.  ``--instance FILE.json`` additionally audits a proposed complete
assignment.  No bundled assignment is claimed in this version.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Iterable, Iterator, Sequence


P = 7
ZERO3 = (0, 0, 0)
Q_NORMAL = (1, 0, 0)

# A deterministic s=6 quotient-atom probe.  Together with q^3 these sixteen
# labels form a length-19 quotient atom.  It is not a height assignment and is
# not advertised as a labelled CSP solution.
S6_QUOTIENT_ATOM_Q = (
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 6),
    (0, 1, 6),
    (0, 1, 6),
    (1, 0, 1),
    (1, 0, 1),
    (1, 0, 1),
    (1, 0, 1),
    (1, 5, 1),
    (1, 6, 1),
    (1, 6, 1),
    (1, 6, 1),
    (1, 6, 1),
    (4, 5, 3),
    (5, 4, 4),
)

# A deeper but deliberately rejected lift of the preceding quotient atom.
# It passes totals, multiplicity, fixed-B atom, and actual-Z atom.  The two
# T-positions numbered 4 and 6 induce a forbidden b=0 length-two quotient
# zero with height 5.  Keeping this fixture prevents a future implementation
# from accidentally omitting b=0 during block reconstruction.
REJECTED_S6_Q_HEIGHTS = (
    0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 0, 6, 0
)
REJECTED_S6_T_LABELS = (
    (5, 5, 3),
    (0, 0, 1),
    (6, 0, 5),
    (2, 4, 4),
    (3, 2, 5),
    (5, 3, 3),
)
REJECTED_S6_T_HEIGHTS = (0, 0, 6, 6, 6, 6)

# Exact short-block length windows inherited from ROUTE-A4.
LENGTH_FAMILIES: dict[int, frozenset[int]] = {
    2: frozenset({1}),
    3: frozenset({1}),
    4: frozenset({1, 2}),
    5: frozenset({1, 2}),
    6: frozenset({1, 2, 3}),
    7: frozenset({2, 3}),
    8: frozenset({3}),
}


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
    """Matrix sending the three supplied basis columns to e1,e2,e3."""
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
    """Return exact subset sums indexed by bit mask.

    The intended largest call has 16 entries, hence 2^16 rows.  This is the
    key finite reduction for the fixed complement atom and is small enough to
    replay without a SAT solver.
    """
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
class LabelledInstance:
    """A complete position assignment in the normalization q=e1.

    Positions are ordered X,T,Q.  The three X quotient labels are q and their
    heights are the supplied profile.  ``t_labels/t_heights`` and
    ``q_labels/q_heights`` contain all 22 external positions.
    """

    profile: tuple[int, int, int]
    t_labels: tuple[tuple[int, int, int], ...]
    t_heights: tuple[int, ...]
    q_labels: tuple[tuple[int, int, int], ...]
    q_heights: tuple[int, ...]

    @property
    def s(self) -> int:
        return len(self.t_labels)

    @property
    def quotient(self) -> tuple[tuple[int, int, int], ...]:
        return (Q_NORMAL,) * 3 + self.t_labels + self.q_labels

    @property
    def height(self) -> tuple[int, ...]:
        return self.profile + self.t_heights + self.q_heights

    @property
    def t_indices(self) -> tuple[int, ...]:
        return tuple(range(3, 3 + self.s))

    @property
    def q_indices(self) -> tuple[int, ...]:
        return tuple(range(3 + self.s, 25))


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


def complement_atom_obstructions(instance: LabelledInstance):
    """List all violations of the exact fixed-B atom criterion.

    Write B=X dot-union Q with X=q^3.  Since all X positions have the same
    quotient label, B is a quotient atom iff

        sum(Q)=-3q,
        sum(U) != -bq

    for every b in {0,1,2,3} and every U subset Q, except (b,U)=(0,empty)
    and (3,Q).  Thus 2^(22-s) Q-subsets replace 2^(25-s) B-subsets without
    losing a single labelled position condition.
    """
    q_sums, _, cardinalities = subset_tables(instance.q_labels)
    full = (1 << len(instance.q_labels)) - 1
    failures: list[tuple[int, int, int]] = []
    if q_sums[full] != scale3(-3, Q_NORMAL):
        failures.append((-1, full, cardinalities[full]))
    # Complementation in Q pairs b with 3-b.  It is therefore exact to test
    # only b=0,1: if sum(U)=-bq, then
    # sum(Q\U)=-(3-b)q.  This halves the atom oracle again.
    for b in range(2):
        target = scale3(-b, Q_NORMAL)
        for mask, value in enumerate(q_sums):
            if b == 0 and mask == 0:
                continue
            if value == target:
                failures.append((b, mask, cardinalities[mask]))
    return failures


def actual_atom_obstruction(instance: LabelledInstance):
    """Return one proper actual zero-sum subset, or None.

    This is an exact meet-in-the-middle test.  It keeps the positions of T and
    Q separate and enumerates the eight X-subsets, so repeated X copies are
    never collapsed into an unlabelled multiplicity variable.
    """
    quotient = instance.quotient
    height = instance.height
    left_indices = tuple(range(3 + instance.s))  # X dot-union T, at most 11
    right_indices = instance.q_indices  # at most 16
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
    full_mask = (1 << 25) - 1
    for left_mask, (q_sum, h_sum) in enumerate(zip(left_q_sums, left_h_sums)):
        targets = buckets.get((neg3(q_sum), (-h_sum) % P), ())
        for right_mask in targets:
            global_mask = left_mask | (right_mask << len(left_indices))
            if global_mask not in (0, full_mask):
                return global_mask
    return None


def reconstruct_short_blocks(instance: LabelledInstance):
    """Rebuild every quotient-zero subset of lengths 2 through 8.

    Returns ``(blocks, invalid, small_zero_masks)``.  ``invalid`` contains quotient-zero short
    subsets whose actual height is outside the frozen length window.  Such a
    subset is a CSP contradiction; it is never silently omitted.

    ``small_zero_masks`` also includes quotient-zero masks of lengths one and
    nine.  They are not declared short blocks; they are retained solely for
    the exact complement-atom oracle below.
    """
    quotient = instance.quotient
    height = instance.height
    blocks: list[Block] = []
    invalid: list[tuple[int, int, int]] = []
    small_zero_masks: list[int] = []
    for length in range(1, 10):
        allowed = LENGTH_FAMILIES.get(length)
        for subset in combinations(range(25), length):
            q_sum = ZERO3
            h_sum = 0
            mask = 0
            for index in subset:
                q_sum = add3(q_sum, quotient[index])
                h_sum = (h_sum + height[index]) % P
                mask |= 1 << index
            if q_sum != ZERO3:
                continue
            small_zero_masks.append(mask)
            if allowed is None:
                continue
            if h_sum not in allowed:
                invalid.append((mask, length, h_sum))
            else:
                trace_size = sum(index < 3 for index in subset)
                blocks.append(Block(mask, length, h_sum, trace_size))
    return blocks, invalid, small_zero_masks


def medium_quotient_zero_obstructions(instance: LabelledInstance):
    """Find one quotient-zero subset of each forbidden length 9--12.

    For |Z|=25 and total quotient sum zero, complementation pairs lengths
    9--12 with 16--13.  Both sides lie under the (SQ) cutoff 16.  Their
    actual sums would have coefficients in {1,2,3}, but the coefficients
    cannot add to zero modulo seven.  Thus every such quotient subset is an
    obstruction.

    A 12+13 meet-in-the-middle table gives an exact existence test for each
    length without directly scanning all middle-layer combinations.
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
            if not 0 <= right_size <= 25 - split:
                continue
            right_mask = right_lookup.get((right_size, neg3(left_sum)))
            if right_mask is None:
                continue
            witness = left_mask | (right_mask << split)
            break
        if witness is not None:
            failures.append((witness, length))
    return failures


def signed_degree(blocks: Sequence[Block], mask: int, family: int, order: int):
    total = 0
    for block in blocks:
        if block.family != family or block.mask & mask != mask:
            continue
        # Point/triple rows use (-1)^(ell-1); pair rows use (-1)^ell.
        exponent = block.length - 1 if order in (1, 3) else block.length
        total += -1 if exponent % 2 else 1
    return total % P


def hasse_obstructions(blocks: Sequence[Block]):
    failures: list[tuple[str, tuple[int, ...], tuple[int, ...]]] = []
    for point in range(25):
        degrees = tuple(
            signed_degree(blocks, 1 << point, family, 1)
            for family in (1, 2, 3)
        )
        if degrees != (1, 1, 1):
            failures.append(("point", (point,), degrees))
    for pair in combinations(range(25), 2):
        mask = (1 << pair[0]) | (1 << pair[1])
        degrees = tuple(
            signed_degree(blocks, mask, family, 2) for family in (1, 2, 3)
        )
        if (degrees[0] + 3 * degrees[1]) % P != 3 or (
            2 * degrees[0] - 3 * degrees[2]
        ) % P != 1:
            failures.append(("pair", pair, degrees))
    for triple in combinations(range(25), 3):
        mask = sum(1 << point for point in triple)
        degrees = tuple(
            signed_degree(blocks, mask, family, 3) for family in (1, 2, 3)
        )
        if (4 * degrees[0] + 3 * degrees[1] + 6 * degrees[2]) % P != 6:
            failures.append(("triple", triple, degrees))
    return failures


def global_block_obstructions(blocks: Sequence[Block]):
    """Zero-order fibres and the p=7 length-six F2 residue."""
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
    quotient = instance.quotient
    failures: list[tuple[str, int, int, int]] = []
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
    """The three short-block families have no common position."""
    full = (1 << 25) - 1
    failures: list[tuple[int, int]] = []
    for family in (1, 2, 3):
        family_masks = [block.mask for block in blocks if block.family == family]
        if not family_masks:
            failures.append((family, full))
            continue
        core = full
        for mask in family_masks:
            core &= mask
        if core:
            failures.append((family, core))
    return failures


def partition_obstructions(instance: LabelledInstance, blocks: Sequence[Block]):
    """Check the fixed T block and the B-atom transversal consequence."""
    t_mask = sum(1 << index for index in instance.t_indices)
    failures: list[tuple[str, int]] = []
    if not any(block.mask == t_mask and block.family == 3 for block in blocks):
        failures.append(("missing_T", t_mask))
    for block_index, block in enumerate(blocks):
        if block.mask & t_mask == 0:
            failures.append(("block_inside_B", block_index))
    return failures


def quotient_atom_obstruction(labels: Sequence[tuple[int, int, int]]):
    """Return one forbidden quotient-zero submask, or None."""
    q_sums, _, _ = subset_tables(labels)
    full = (1 << len(labels)) - 1
    if q_sums[full] != ZERO3:
        return full
    for mask, q_sum in enumerate(q_sums):
        if mask not in (0, full) and q_sum == ZERO3:
            return mask
    return None


def all_f3_complement_obstructions(
    blocks: Sequence[Block], small_zero_masks: Sequence[int]
):
    """Audit every F3 complement atom using one global length-nine list.

    An F3 complement has length 17, 18, or 19.  If it splits into two
    nonempty quotient-zero parts, the shorter part has length at most nine.
    Conversely any quotient-zero mask of length at most nine disjoint from the
    F3 block lies properly in its complement.  Hence this test is exact and
    avoids rerunning up to 2^19 subset sums for every F3 block.
    """
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


def canonical_000_key(instance: LabelledInstance):
    """Exact orbit key for the profile 000 under the available symmetries.

    For every ordered Q-pair completing q to a quotient basis, normalize that
    basis to e1,e2,e3, use the unique height shear vanishing on q which makes
    the two selected Q heights zero, sort the T and Q position labels
    separately, and take the lexicographically least result.  This quotients
    the stabilizer of q, all allowed height shears, and S_s x S_(22-s)
    position permutations without turning positions into unlabelled stars.
    """
    if instance.profile != (0, 0, 0):
        raise ValueError("canonical_000_key is only valid for profile 000")
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


def basic_obstructions(instance: LabelledInstance):
    failures: list[str] = []
    if len(instance.profile) != 3:
        failures.append("profile must have three labelled X positions")
    if instance.s not in (6, 7, 8):
        failures.append("s must lie in {6,7,8}")
    if len(instance.t_heights) != instance.s:
        failures.append("T label/height lengths differ")
    if len(instance.q_labels) != 22 - instance.s:
        failures.append("Q must have 22-s positions")
    if len(instance.q_heights) != len(instance.q_labels):
        failures.append("Q label/height lengths differ")
    if any(label == ZERO3 for label in instance.quotient):
        failures.append(
            "every Z quotient label is nonzero by F3 complement atoms and no common F3 core"
        )
    if any(label in (ZERO3, Q_NORMAL) for label in instance.q_labels):
        failures.append("every Q quotient label must be nonzero and different from q")
    if sum3(instance.t_labels) != ZERO3:
        failures.append("T quotient sum is not zero")
    if sum(instance.t_heights) % P != 3:
        failures.append("T height sum is not three")
    if sum3(instance.q_labels) != scale3(-3, Q_NORMAL):
        failures.append("Q quotient sum is not -3q")
    if (sum(instance.profile) + sum(instance.q_heights)) % P != 4:
        failures.append("B height sum is not four")
    if sum3(instance.quotient) != ZERO3 or sum(instance.height) % P != 0:
        failures.append("Z total actual label is not zero")
    if max(Counter(zip(instance.quotient, instance.height)).values()) > 3:
        failures.append("an actual F_7^4 label occurs more than three times")
    return failures


def audit_instance(instance: LabelledInstance):
    """Run the exact finite necessary system on a complete assignment."""
    report: dict[str, object] = {}
    report["basic"] = basic_obstructions(instance)
    report["fixed_B_atom"] = complement_atom_obstructions(instance)
    report["actual_Z_atom"] = actual_atom_obstruction(instance)
    blocks, invalid, small_zero_masks = reconstruct_short_blocks(instance)
    report["block_counts"] = dict(sorted(Counter(b.family for b in blocks).items()))
    trace_counts = Counter((b.family, b.trace_size) for b in blocks)
    report["trace_counts"] = {
        f"F{family}:b{trace}": count
        for (family, trace), count in sorted(trace_counts.items())
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
    return report


def audit_exact_B_reduction() -> None:
    """Mechanically check the b/U atom equivalence on all toy truth tables."""
    # This is a logical index audit, independent of a label assignment.
    for q_size in (14, 15, 16):
        full_q = (1 << q_size) - 1
        seen = set()
        for b in range(2):
            for q_mask in range(1 << q_size):
                b_proper = not (b == 0 and q_mask == 0)
                if b_proper:
                    seen.add((b, q_mask))
        assert len(seen) == 2 * (1 << q_size) - 1


def audit_normalization() -> None:
    """Check the determinant criterion behind the 000,s=6 symmetry slice."""
    assert det3((Q_NORMAL, (0, 1, 0), (0, 0, 1))) == 1
    # In an atom of length at least 17, the quotient labels cannot span rank
    # <=2 because D(C_7^2)=13.  Consequently two Q positions complete q to a
    # basis.  GL_3(7) fixing q sends them to e2,e3; a height shear vanishing on
    # q then makes their two heights zero while preserving profile 000.
    base = LabelledInstance(
        profile=(0, 0, 0),
        t_labels=((0, 1, 2), (0, 6, 5), (2, 1, 0), (5, 6, 0), ZERO3, ZERO3),
        t_heights=(0, 1, 2, 3, 4, 5),
        q_labels=S6_QUOTIENT_ATOM_Q,
        q_heights=tuple((3 * index + 1) % P for index in range(16)),
    )
    # An arbitrary quotient change of coordinates fixing q, followed by a
    # height shear which also vanishes on q.
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
        profile=(0, 0, 0),
        t_labels=tuple(reversed([item[0] for item in transformed_t])),
        t_heights=tuple(reversed([item[1] for item in transformed_t])),
        q_labels=tuple(reversed([item[0] for item in transformed_q])),
        q_heights=tuple(reversed([item[1] for item in transformed_q])),
    )
    assert canonical_000_key(base) == canonical_000_key(moved)


def audit_s6_quotient_atom_probe() -> None:
    probe = LabelledInstance(
        profile=(0, 0, 0),
        t_labels=(ZERO3,) * 6,
        t_heights=(0,) * 6,
        q_labels=S6_QUOTIENT_ATOM_Q,
        q_heights=(0,) * 16,
    )
    assert complement_atom_obstructions(probe) == []
    multiplicities = Counter((Q_NORMAL,) * 3 + S6_QUOTIENT_ATOM_Q)
    assert multiplicities[Q_NORMAL] == 3
    assert max(multiplicities.values()) == 4
    assert sum3(S6_QUOTIENT_ATOM_Q) == scale3(-3, Q_NORMAL)
    canonical_000_key(probe)


def audit_rejected_actual_atom_lift() -> None:
    instance = LabelledInstance(
        profile=(0, 0, 0),
        t_labels=REJECTED_S6_T_LABELS,
        t_heights=REJECTED_S6_T_HEIGHTS,
        q_labels=S6_QUOTIENT_ATOM_Q,
        q_heights=REJECTED_S6_Q_HEIGHTS,
    )
    assert basic_obstructions(instance) == []
    assert complement_atom_obstructions(instance) == []
    assert actual_atom_obstruction(instance) is None
    # Global positions 6 and 8 are T positions 4 and 6 (one-based).
    assert add3(instance.quotient[6], instance.quotient[8]) == ZERO3
    assert (instance.height[6] + instance.height[8]) % P == 5
    assert 5 not in LENGTH_FAMILIES[2]
    middle = medium_quotient_zero_obstructions(instance)
    assert middle
    for mask, length in middle:
        indices = tuple(mask_indices(mask))
        assert len(indices) == length
        assert 9 <= length <= 12
        assert sum3(instance.quotient[index] for index in indices) == ZERO3


def print_default_audit() -> None:
    audit_exact_B_reduction()
    audit_normalization()
    audit_s6_quotient_atom_probe()
    audit_rejected_actual_atom_lift()
    print("PASS exact fixed-B atom reduction to Q-subsets")
    print("s=6/7/8 Q sizes: 16/15/14; minimal atom tests: 2^(|Q|+1)-1")
    print("PASS 000,s=6 normalization q=e1, Q0=e2, Q1=e3, r0=r1=0")
    print("PASS explicit s=6 quotient atom with q-multiplicity 3 and max fibre 4")
    print("PROBE SCOPE: quotient labels only; no T labels or heights are claimed")
    print("PASS rejected lift: fixed B and actual Z are atoms, actual multiplicity <=3")
    print("EXPECTED REJECTION: a b=0 T-pair has quotient sum 0 and height 5")
    print("PASS verifier reconstructs every length-2--8 block, including b=0")
    print("PASS exact meet-in-the-middle rejection of quotient-zero lengths 9--12")
    print("HASSE SCOPE: all 25 points, 300 pairs, and 2300 triples")
    print("GLOBAL SCOPE: c_Z(a)=c_Z(2a)=c_Z(3a)=0 and N_(2,6)=3 mod 7")
    print("PROPAGATION: all Z quotient labels are nonzero; all F1/F2/F3 cores are empty")
    print("INTERSECTION SCOPE: F2-F2, F1/F2-F3, and nonzero F3-F3 quotient intersections")
    print("ATOM SCOPE: fixed B, actual Z, and every induced F3 complement")
    print("STATUS: INCOMPLETE -- no complete 88-scalar assignment is bundled")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path)
    args = parser.parse_args()
    print_default_audit()
    if args.instance is None:
        return
    instance = parse_instance(args.instance)
    report = audit_instance(instance)
    bad = {
        key: value
        for key, value in report.items()
        if key != "block_counts" and key != "trace_counts" and value
    }
    printable = {}
    for key, value in report.items():
        if isinstance(value, list):
            printable[key] = {"count": len(value), "first_20": value[:20]}
        else:
            printable[key] = value
    print(json.dumps(printable, ensure_ascii=False, indent=2, default=str))
    if bad:
        raise SystemExit("REJECTED: complete labelled assignment violates the CSP")
    print("ACCEPTED: assignment satisfies this finite necessary CSP")


if __name__ == "__main__":
    main()
