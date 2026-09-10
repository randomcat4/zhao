"""Heuristic search for a fully induced local state in the p=7,m=4 0001 branch.

This is deliberately only a probe.  A found state would realize the three
forced tail types on their assigned positions, be zero-sum-free there, make
the already assigned part of B quotient-zero-sum-free, classify every short
quotient-zero subset through the exact length windows, and pass all induced
short-block intersection tests.  It would not complete T, the quotient atom
B, the Hasse counts, or a ROUTE-A4 sequence.
"""

from collections import Counter
from itertools import combinations
from math import exp
from random import Random


P = 7
ZERO4 = (0, 0, 0, 0)
Q = (1, 0, 0, 0)
TARGETS = ((6, 0, 0, 2), (5, 0, 0, 2), (4, 0, 0, 2))
TAIL_UNIQUE_SIZES = (5, 3, 3)
ALLOWED_FAMILIES = {
    2: {1},
    3: {1},
    4: {1, 2},
    5: {1, 2},
    6: {1, 2, 3},
    7: {2, 3},
    8: {3},
}


def add(left, right):
    return tuple((left[i] + right[i]) % P for i in range(4))


def neg(vector):
    return tuple(-value % P for value in vector)


def sub(left, right):
    return add(left, neg(right))


def random_vector(rng):
    return tuple(rng.randrange(P) for _ in range(4))


def build_state(free):
    t = free[0]
    cursor = 1
    tails = []
    positions = []
    for target, unique_size in zip(TARGETS, TAIL_UNIQUE_SIZES):
        chosen = list(free[cursor : cursor + unique_size - 1])
        cursor += unique_size - 1
        partial = t
        for vector in chosen:
            partial = add(partial, vector)
        chosen.append(sub(target, partial))
        start = len(positions)
        positions.extend(chosen)
        tails.append((15, *range(4 + start, 4 + len(positions))))
    # Three height-zero q cores, then the exceptional height-one q core.
    core = [(1, 0, 0, 0)] * 3 + [(1, 0, 0, 1)]
    return core + positions + [t], tails


def half_sums(vectors):
    sums = [ZERO4]
    for vector in vectors:
        sums += [add(value, vector) for value in sums]
    return sums


def zero_subset_count(vectors):
    split = len(vectors) // 2
    left = Counter(half_sums(vectors[:split]))
    right = Counter(half_sums(vectors[split:]))
    count = sum(multiplicity * right[neg(value)] for value, multiplicity in left.items())
    return count - 1


def quotient_zero_subset_count(vectors):
    lifted = [vector[:3] + (0,) for vector in vectors]
    return zero_subset_count(lifted)


def elementary_penalty(vectors):
    penalty = sum(max(0, multiplicity - 3) for multiplicity in Counter(vectors).values())
    # Tail position 15 is the common T point.  All other tail positions are Q.
    for vector in vectors[4:15]:
        if vector[:3] in ((0, 0, 0), (1, 0, 0)):
            penalty += 10
    if vectors[15][:3] == (0, 0, 0):
        penalty += 10
    return penalty


def induced_blocks(vectors):
    blocks = {1: [], 2: [], 3: []}
    invalid = []
    n = len(vectors)
    for size in range(2, 9):
        for subset in combinations(range(n), size):
            total = ZERO4
            mask = 0
            for position in subset:
                total = add(total, vectors[position])
                mask |= 1 << position
            if total[:3] != (0, 0, 0):
                continue
            if total[3] in ALLOWED_FAMILIES[size]:
                blocks[total[3]].append(mask)
            else:
                invalid.append((mask, size, total[3]))
    return blocks, invalid


def quotient_sum(vectors, mask):
    total = ZERO4
    position = 0
    while mask:
        if mask & 1:
            total = add(total, vectors[position])
        position += 1
        mask >>= 1
    return total[:3]


def intersection_penalty(vectors, blocks):
    violations = 0
    for first_index, first in enumerate(blocks[2]):
        for second in blocks[2][first_index + 1 :]:
            violations += first & second == 0
    for family in (1, 2):
        for first in blocks[family]:
            for second in blocks[3]:
                violations += first & second == 0
    for first_index, first in enumerate(blocks[3]):
        for second in blocks[3][first_index + 1 :]:
            intersection = first & second
            if intersection == 0 or quotient_sum(vectors, intersection) == (0, 0, 0):
                violations += 1
    return violations


def score(free, full=False):
    vectors, tails = build_state(free)
    # Positions 0--14 are the assigned X union Q portion of B.  Any quotient
    # zero sum there already prevents extension to a quotient atom.
    basic = (
        zero_subset_count(vectors)
        + quotient_zero_subset_count(vectors[:15])
        + elementary_penalty(vectors)
    )
    if not full or basic:
        return basic, vectors, tails, None
    blocks, invalid = induced_blocks(vectors)
    return (
        len(invalid) + intersection_penalty(vectors, blocks),
        vectors,
        tails,
        (blocks, invalid),
    )


def main():
    rng = Random(20260908)
    free_count = 1 + sum(size - 1 for size in TAIL_UNIQUE_SIZES)
    best = None
    zero_free_seen = 0
    for restart in range(80):
        free = [random_vector(rng) for _ in range(free_count)]
        current, _, _, _ = score(free)
        temperature = 4.0
        for step in range(2500):
            candidate = list(free)
            index = rng.randrange(free_count)
            coordinate = rng.randrange(4)
            mutable = list(candidate[index])
            mutable[coordinate] = rng.randrange(P)
            candidate[index] = tuple(mutable)
            trial, vectors, tails, _ = score(candidate)
            if trial <= current or rng.random() < exp((current - trial) / temperature):
                free, current = candidate, trial
            temperature = max(0.08, temperature * 0.998)
            if current == 0:
                local, vectors, tails, payload = score(free, full=True)
                zero_free_seen += 1
                if local == 0:
                    blocks, invalid = payload
                    assert not invalid
                    print("FOUND_LOCAL_STATE")
                    print(f"VECTORS={vectors}")
                    print(f"TAILS={tails}")
                    print(
                        "VALID_BLOCK_COUNTS="
                        + str({family: len(blocks[family]) for family in (1, 2, 3)})
                    )
                    print("PASS all short quotient-zero subsets lie in exact windows")
                    print("PASS assigned X union Q is quotient-zero-sum-free")
                    print("SCOPE assigned positions only; no completed T/B/Hasse realization")
                    return
                # Move away from this zero-free state to sample another basin.
                current += local
            if best is None or current < best:
                best = current
        print(f"RESTART={restart + 1} BEST={best} ZERO_FREE_SEEN={zero_free_seen}")
    print(f"NO_LOCAL_STATE_FOUND best={best} zero_free_seen={zero_free_seen}")
    print("SCOPE heuristic non-existence is not a proof")


if __name__ == "__main__":
    main()
