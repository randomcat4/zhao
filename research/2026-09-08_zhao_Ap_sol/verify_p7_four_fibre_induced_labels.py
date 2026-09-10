"""Audit all short blocks induced by the old p=7,m=4 local labels.

The older witness checked only the three named tails.  This script enumerates
every subset of the labelled positions of length 2 through 8, rebuilds its
family from quotient sum and height, and checks every distinct F3-block pair.
It is a finite audit of that candidate only, not of the 84-scalar CSP.
"""

from itertools import combinations


P = 7
ZERO = (0, 0, 0)


def add(*vectors):
    return tuple(sum(vector[i] for vector in vectors) % P for i in range(3))


def subset_sum(labels, subset):
    return add(*(labels[position] for position in subset))


def induced_blocks(labels, heights):
    positions = tuple(labels)
    blocks = {1: [], 2: [], 3: []}
    for size in range(2, min(8, len(positions)) + 1):
        for subset in combinations(positions, size):
            if subset_sum(labels, subset) != ZERO:
                continue
            family = sum(heights[position] for position in subset) % P
            if family in blocks:
                blocks[family].append(frozenset(subset))
    return blocks


def exceptional_candidate():
    q = (1, 0, 0)
    profile = (0, 0, 0, 1)
    labels = {f"x{i}": q for i in range(4)}
    heights = {f"x{i}": profile[i] for i in range(4)}

    tail_labels = {
        0: (0, 1, 0),
        1: (0, 0, 1),
        2: (0, 0, 2),
        3: (0, 0, 3),
        4: (0, 0, 4),
        5: (6, 6, 4),
        6: (0, 0, 1),
        7: (0, 0, 2),
        8: (5, 6, 4),
        9: (0, 0, 3),
        10: (0, 0, 4),
        11: (4, 6, 0),
    }
    tail_heights = {index: 0 for index in tail_labels}
    tail_heights[1] = tail_heights[6] = tail_heights[9] = 2
    labels.update({f"y{i}": value for i, value in tail_labels.items()})
    heights.update({f"y{i}": value for i, value in tail_heights.items()})
    return labels, heights


def first_zero_intersection(labels, f3_blocks):
    for first_index, first in enumerate(f3_blocks):
        for second in f3_blocks[first_index + 1 :]:
            intersection = first & second
            if subset_sum(labels, intersection) == ZERO:
                return first, second, intersection
    return None


def main():
    labels, heights = exceptional_candidate()
    blocks = induced_blocks(labels, heights)
    collision = first_zero_intersection(labels, blocks[3])
    print(
        "INDUCED_COUNTS "
        + " ".join(f"F{family}={len(blocks[family])}" for family in (1, 2, 3))
    )
    if collision is None:
        print("NO_COLLISION among all induced F3 blocks on the labelled positions")
        return
    first, second, intersection = collision
    print("EXPECTED_REJECTION old p=7,m=4 exceptional labels")
    print(f"F3_A={sorted(first)}")
    print(f"F3_B={sorted(second)}")
    print(f"INTERSECTION={sorted(intersection)}")
    print(f"INTERSECTION_QUOTIENT_SUM={subset_sum(labels, intersection)}")


if __name__ == "__main__":
    main()
