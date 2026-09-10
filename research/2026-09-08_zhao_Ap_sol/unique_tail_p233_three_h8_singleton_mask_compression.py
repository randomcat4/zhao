from __future__ import annotations

from collections import Counter
from itertools import permutations, product


PAIRS = ((0, 1), (0, 2), (1, 2))


def valid(q: tuple[int, int, int, int], pair_gate: bool) -> bool:
    a, b, c, d = q
    if a + b + d > 6 or a + c + d > 6 or b + c + d > 6:
        return False
    return not pair_gate or max(a + d, b + d, c + d) <= 5


def act(q: tuple[int, int, int, int], perm: tuple[int, int, int]):
    a, b, c, d = q
    pair_value = {(0, 1): a, (0, 2): b, (1, 2): c}
    inverse = {perm[i]: i for i in range(3)}
    values = []
    for pair in PAIRS:
        old_pair = tuple(sorted((inverse[pair[0]], inverse[pair[1]])))
        values.append(pair_value[old_pair])
    return (*values, d)


def canonical(q, group):
    return min(act(q, perm) for perm in group)


def main() -> None:
    labelled = [q for q in product(range(7), repeat=4) if valid(q, False)]
    gated = [q for q in labelled if valid(q, True)]
    s3 = list(permutations(range(3)))
    s2 = [(0, 1, 2), (0, 2, 1)]
    initial_orbits = {canonical(q, s3) for q in labelled}
    gated_orbits = {canonical(q, s3) for q in gated}
    pointed_orbits = {canonical(q, s2) for q in gated}
    distribution = Counter(450 + a + b + c + 2 * d for a, b, c, d in gated_orbits)
    unique_top = [q for q in gated_orbits if 450 + q[0] + q[1] + q[2] + 2 * q[3] == 461]

    assert (len(labelled), len(initial_orbits)) == (256, 80)
    assert (len(gated), len(gated_orbits)) == (237, 73)
    assert len(pointed_orbits) == 147
    assert [distribution[k] for k in range(450, 462)] == [1, 1, 3, 4, 7, 9, 13, 12, 11, 7, 4, 1]
    assert unique_top == [(1, 1, 1, 4)]

    print("PASS three-h8 singleton mask compression")
    print("labelled/orbits before gate", len(labelled), len(initial_orbits))
    print("labelled/orbits after gate", len(gated), len(gated_orbits))
    print("pointed witness states", len(pointed_orbits))
    print("common-core distribution", [distribution[k] for k in range(450, 462)])


if __name__ == "__main__":
    main()
