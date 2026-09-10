"""Strictly reject a former local p=7,m=4 tail-state candidate.

The assignment realizes the three named exceptional-tail types and passes
the intersections among blocks that happen to lie in a valid length window.
The strict audit additionally rebuilds *every* short quotient-zero subset.
It finds illegal height/length spectra and quotient-zero subsets already
inside the assigned part of B, so the assignment is an expected rejection.
"""

from collections import Counter
from itertools import combinations


P = 7
ZERO = (0, 0, 0, 0)
ALLOWED_FAMILIES = {
    2: {1},
    3: {1},
    4: {1, 2},
    5: {1, 2},
    6: {1, 2, 3},
    7: {2, 3},
    8: {3},
}

# Coordinates are (three quotient coordinates, height).
VECTORS = (
    (1, 0, 0, 0),
    (1, 0, 0, 0),
    (1, 0, 0, 0),
    (1, 0, 0, 1),
    (1, 3, 5, 3),
    (5, 6, 2, 6),
    (2, 0, 3, 6),
    (6, 4, 1, 6),
    (2, 3, 0, 4),
    (5, 6, 6, 6),
    (4, 6, 0, 6),
    (6, 4, 5, 6),
    (1, 3, 5, 3),
    (6, 4, 0, 5),
    (0, 2, 6, 3),
    (4, 5, 3, 5),
)

TAILS = (
    frozenset((15, 4, 5, 6, 7, 8)),
    frozenset((15, 9, 10, 11)),
    frozenset((15, 12, 13, 14)),
)
TAIL_TARGETS = ((6, 0, 0, 2), (5, 0, 0, 2), (4, 0, 0, 2))


def add(*vectors):
    return tuple(sum(vector[i] for vector in vectors) % P for i in range(4))


def subset_sum(subset):
    return add(*(VECTORS[position] for position in subset))


def all_subset_sums():
    sums = [ZERO]
    for vector in VECTORS:
        sums += [add(value, vector) for value in sums]
    return sums


def induced_blocks():
    blocks = {1: [], 2: [], 3: []}
    invalid = []
    for size in range(2, 9):
        for subset in combinations(range(len(VECTORS)), size):
            total = subset_sum(subset)
            if total[:3] != (0, 0, 0):
                continue
            if total[3] in ALLOWED_FAMILIES[size]:
                blocks[total[3]].append(frozenset(subset))
            else:
                invalid.append((frozenset(subset), total[3]))
    return blocks, invalid


def assigned_b_quotient_zeros():
    bad = []
    # Positions 0--3 are X and 4--14 are the assigned Q positions.  Position
    # 15 is the assigned T point and hence is not in the fixed complement B.
    for size in range(1, 16):
        for subset in combinations(range(15), size):
            if subset_sum(subset)[:3] == (0, 0, 0):
                bad.append(frozenset(subset))
    return bad


def main():
    assert VECTORS[:4] == ((1, 0, 0, 0),) * 3 + ((1, 0, 0, 1),)
    assert max(Counter(VECTORS).values()) <= 3
    # Positions 4--14 are the currently assigned Q positions.  Position 15
    # is the sole assigned T point, common to all three forced tails.
    assert all(vector[:3] not in ((0, 0, 0), (1, 0, 0)) for vector in VECTORS[4:15])
    assert VECTORS[15][:3] != (0, 0, 0)
    for tail, target in zip(TAILS, TAIL_TARGETS):
        assert subset_sum(tail) == target
        assert tail & {15} == {15}
        assert VECTORS[15][:3] != (0, 0, 0)

    sums = all_subset_sums()
    assert len(sums) == 1 << len(VECTORS)
    assert all(value != ZERO for value in sums[1:])

    blocks, invalid = induced_blocks()
    assert {family: len(family_blocks) for family, family_blocks in blocks.items()} == {
        1: 0,
        2: 17,
        3: 27,
    }
    assert len(invalid) == 31
    assert invalid[0] == (frozenset((7, 9, 11, 14, 15)), 5)

    b_zeros = assigned_b_quotient_zeros()
    assert b_zeros
    b_short = [subset for subset in b_zeros if 2 <= len(subset) <= 8]
    b_valid = [
        subset
        for family in (1, 2, 3)
        for subset in blocks[family]
        if 15 not in subset
    ]
    assert len(b_valid) == 8

    # The three forced mixed stars are genuinely present among the rebuilt
    # blocks: b=1 contributes one F3 trace, and b=2,3 contribute three each.
    required_f3 = [TAILS[0] | {3}]
    required_f3 += [TAILS[1] | {3, index} for index in (0, 1, 2)]
    required_f3 += [
        TAILS[2] | {3, first, second}
        for first, second in combinations((0, 1, 2), 2)
    ]
    assert len(required_f3) == 7
    assert all(block in blocks[3] for block in required_f3)

    f2_pairs = 0
    for first_index, first in enumerate(blocks[2]):
        for second in blocks[2][first_index + 1 :]:
            f2_pairs += 1
            assert first & second

    f23_pairs = 0
    for first in blocks[2]:
        for second in blocks[3]:
            f23_pairs += 1
            assert first & second

    f3_pairs = 0
    for first_index, first in enumerate(blocks[3]):
        for second in blocks[3][first_index + 1 :]:
            f3_pairs += 1
            intersection = first & second
            assert intersection
            assert subset_sum(intersection)[:3] != (0, 0, 0)

    assert f2_pairs == 136
    assert f23_pairs == 459
    assert f3_pairs == 351
    print("EXPECTED REJECTION p=7,m=4 former tail-local assignment")
    print("ASSIGNED_POSITIONS=16 Q_ASSIGNED=11 T_ASSIGNED=1")
    print("VALID_WINDOW_BLOCKS F1=0 F2=17 F3=27")
    print(f"ILLEGAL_SHORT_QUOTIENT_ZEROS={len(invalid)}")
    print(
        "FIRST_ILLEGAL subset=(7,9,11,14,15) length=5 height=5"
    )
    print(
        f"ASSIGNED_B_QUOTIENT_ZEROS={len(b_zeros)} "
        f"SHORT={len(b_short)} VALID_WINDOW={len(b_valid)}"
    )
    print("CHECKED_PAIRS F2F2=136 F2F3=459 F3F3=351")
    print("PASS no nonempty actual zero-sum subset and multiplicity cap three")
    print("STATUS rejected by SQ length windows and fixed-B quotient atomicity")


if __name__ == "__main__":
    main()
