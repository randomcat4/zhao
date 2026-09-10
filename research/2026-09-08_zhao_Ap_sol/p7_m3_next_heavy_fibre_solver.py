#!/usr/bin/env python3
"""Exact next-step propagation for the p=7, m=3 labelled CSP.

This script proves two necessary quotient-level rules from the singleton
short-block windows L_2={1}, L_3={1}, L_8={3} and actual multiplicity <= 3:

1. every quotient fibre in Z has at most seven positions;
2. a quotient fibre of multiplicity at least four forbids six explicit
   tail-sum patterns outside that fibre.

It then exhausts all S_6-orbits of possible nonzero T quotient labels for the
explicit length-19 B atom in p7_three_fibre_labelled_csp.md.  No orbit survives
the two rules together with sum(T)=0.  Hence that whole B skeleton, not merely
the previously bundled height lift, is unliftable to the full labelled CSP.

The search deliberately omits height sums, actual-Z atomicity, Hasse equations,
intersections, and the other F3 complements.  It is therefore a weaker
necessary filter; infeasibility here is a valid fixed-skeleton certificate.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from typing import Iterable, Sequence


P = 7
ZERO3 = (0, 0, 0)
Q_NORMAL = (1, 0, 0)

# The quotient atom from equation (16) of the labelled-CSP note.
BASE_Q = (
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
BASE_B = (Q_NORMAL,) * 3 + BASE_Q

# If a heavy fibre contributes j positions and an outside tail contributes k
# positions, these are exactly the non-vacuous cases with j <= 3 and
# j+k in {2,3,8}, the three singleton length windows.
HEAVY_TAIL_PATTERNS = (
    (1, 1),
    (1, 2),
    (1, 7),
    (2, 1),
    (2, 6),
    (3, 5),
)

REJECTED_T_LABELS = (
    (5, 5, 3),
    (0, 0, 1),
    (6, 0, 5),
    (2, 4, 4),
    (3, 2, 5),
    (5, 3, 3),
)

EXPECTED_BAN_SHA256 = (
    "77567cdffd23c28471619d6f59d908e7860d5d41ef73a2fc56a9d16f538a4841"
)
EXPECTED_LEVEL_COUNTS = (1, 71, 1147, 7572, 28171, 72306)
EXPECTED_ATTEMPTS = {1: 71, 2: 2556, 3: 31683, 4: 182402, 5: 621860}
EXPECTED_VALID_EXTENSIONS = {
    1: 71,
    2: 1147,
    3: 7572,
    4: 28171,
    5: 72306,
}
EXPECTED_CLOSURE = {
    "prefixes": 72306,
    "last_not_unary": 69457,
    "last_breaks_order": 1381,
    "last_propagation": 1468,
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


def audit_base_B_atom() -> int:
    """Replay the exact Q-subset criterion for B=q^3 Q."""
    size = 1 << len(BASE_Q)
    sums = [ZERO3] * size
    for mask in range(1, size):
        bit = mask & -mask
        index = bit.bit_length() - 1
        sums[mask] = add3(sums[mask ^ bit], BASE_Q[index])
    assert sums[-1] == scale3(-3, Q_NORMAL)
    zero_hits = [mask for mask in range(1, size) if sums[mask] == ZERO3]
    minus_q_hits = [mask for mask in range(size) if sums[mask] == neg3(Q_NORMAL)]
    assert zero_hits == []
    assert minus_q_hits == []
    return (size - 1) + size


def valid_same_fibre_height_profiles(size: int) -> int:
    """Count height multisets satisfying multiplicity <=3 and every 7-window."""
    count = 0
    for multiplicities in product(range(4), repeat=P):
        if sum(multiplicities) != size:
            continue
        heights = tuple(
            height
            for height, multiplicity in enumerate(multiplicities)
            for _ in range(multiplicity)
        )
        if all(
            sum(heights[index] for index in subset) % P in (2, 3)
            for subset in combinations(range(size), 7)
        ):
            count += 1
    return count


def heavy_fibres():
    counts = Counter(BASE_B)
    return counts, tuple(sorted(label for label, count in counts.items() if count >= 4))


def build_forbidden_T_subset_sums(
    heavy: Sequence[tuple[int, int, int]],
):
    """Build exact tail-sum tables after splitting a tail between B and T.

    For a fixed heavy value g and pattern (j,k), a forbidden outside tail U
    has k positions and sum(U)=-j*g.  If a of those positions lie in T, their
    sum is forbidden whenever the remaining k-a B positions can complete it.
    Positions carrying g are excluded from both sides because U is outside the
    g-fibre.
    """
    forbidden = {}
    for g in heavy:
        outside_B = tuple(label for label in BASE_B if label != g)
        by_T_size: dict[int, set[tuple[int, int, int]]] = defaultdict(set)
        for j, tail_size in HEAVY_TAIL_PATTERNS:
            target = scale3(-j, g)

            # A zero-T tail would already contradict the known B atom.
            assert not any(
                sum3(subset) == target
                for subset in combinations(outside_B, tail_size)
            )

            for T_size in range(1, min(6, tail_size) + 1):
                B_size = tail_size - T_size
                for B_part in combinations(outside_B, B_size):
                    needed_T_sum = add3(target, neg3(sum3(B_part)))
                    by_T_size[T_size].add(needed_T_sum)
        forbidden[g] = dict(by_T_size)
    return forbidden


def table_digest(forbidden) -> str:
    serial = []
    for g in sorted(forbidden):
        for size in sorted(forbidden[g]):
            serial.append((g, size, sorted(forbidden[g][size])))
    payload = json.dumps(serial, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def full_prefix_valid(
    T_prefix: Sequence[tuple[int, int, int]],
    base_counts: Counter,
    heavy,
    forbidden,
) -> bool:
    """Direct necessary-filter check, used to audit incremental propagation."""
    T_counts = Counter(T_prefix)
    if any(base_counts[label] + count > 7 for label, count in T_counts.items()):
        return False
    for g in heavy:
        outside_T = tuple(label for label in T_prefix if label != g)
        for size in range(1, len(outside_T) + 1):
            forbidden_sums = forbidden[g].get(size)
            if forbidden_sums is None:
                continue
            if any(
                sum3(subset) in forbidden_sums
                for subset in combinations(outside_T, size)
            ):
                return False
    return True


def extension_valid(
    prefix: tuple[tuple[int, int, int], ...],
    new_label: tuple[int, int, int],
    base_counts: Counter,
    heavy,
    forbidden,
) -> bool:
    """Check only new obstructions containing the appended T position."""
    if base_counts[new_label] + prefix.count(new_label) + 1 > 7:
        return False
    for g in heavy:
        if new_label == g:
            continue
        previous_outside = tuple(label for label in prefix if label != g)
        for size in range(1, len(previous_outside) + 2):
            forbidden_sums = forbidden[g].get(size)
            if forbidden_sums is None:
                continue
            for old_part in combinations(previous_outside, size - 1):
                if add3(sum3(old_part), new_label) in forbidden_sums:
                    return False
    return True


def exhaust_T_multisets(base_counts, heavy, forbidden):
    """Enumerate every S_6-orbit of T labels surviving the necessary filter."""
    nonzero_labels = tuple(
        sorted(label for label in product(range(P), repeat=3) if label != ZERO3)
    )
    unary = tuple(
        label
        for label in nonzero_labels
        if extension_valid((), label, base_counts, heavy, forbidden)
    )
    unary_index = {label: index for index, label in enumerate(unary)}

    # The direct and incremental formulations must agree on every unary state.
    assert all(
        full_prefix_valid((label,), base_counts, heavy, forbidden)
        == (label in unary_index)
        for label in nonzero_labels
    )

    level_counts = [1, 0, 0, 0, 0, 0]
    attempts: Counter[int] = Counter()
    valid_extensions: Counter[int] = Counter()
    closure: Counter[str] = Counter()
    solutions = []

    def walk(prefix, start, total):
        depth = len(prefix)
        if depth == 5:
            # Independent direct replay of every terminal prefix guards the
            # incremental "new subsets only" optimization used above.
            assert full_prefix_valid(prefix, base_counts, heavy, forbidden)
            closure["prefixes"] += 1
            last = neg3(total)
            last_index = unary_index.get(last)
            if last_index is None:
                closure["last_not_unary"] += 1
                return
            if last_index < start:
                closure["last_breaks_order"] += 1
                return
            if not extension_valid(prefix, last, base_counts, heavy, forbidden):
                closure["last_propagation"] += 1
                return
            completed = prefix + (last,)
            assert sum3(completed) == ZERO3
            assert full_prefix_valid(completed, base_counts, heavy, forbidden)
            solutions.append(completed)
            return

        for index in range(start, len(unary)):
            attempts[depth + 1] += 1
            label = unary[index]
            if not extension_valid(prefix, label, base_counts, heavy, forbidden):
                continue
            extended = prefix + (label,)
            if depth <= 2:
                assert full_prefix_valid(extended, base_counts, heavy, forbidden)
            valid_extensions[depth + 1] += 1
            level_counts[depth + 1] += 1
            walk(extended, index, add3(total, label))

    walk((), 0, ZERO3)
    return (
        unary,
        tuple(level_counts),
        dict(attempts),
        dict(valid_extensions),
        dict(closure),
        tuple(solutions),
    )


def audit_rejected_support_witness():
    """Show that the old JSON quotient support has no height lift at all."""
    heavy_value = (1, 0, 1)
    assert Counter(BASE_B)[heavy_value] == 4
    first = REJECTED_T_LABELS[1]
    second = REJECTED_T_LABELS[2]
    assert add3(first, second) == neg3(heavy_value)

    # The four length-three blocks force all four heavy-fibre heights equal.
    window_lifts = 0
    multiplicity_valid_lifts = 0
    for first_height in range(P):
        for second_height in range(P):
            for heavy_heights in product(range(P), repeat=4):
                if not all(
                    (first_height + second_height + height) % P == 1
                    for height in heavy_heights
                ):
                    continue
                window_lifts += 1
                if max(Counter(heavy_heights).values()) <= 3:
                    multiplicity_valid_lifts += 1
    assert window_lifts == 49
    assert multiplicity_valid_lifts == 0
    return window_lifts, multiplicity_valid_lifts


def main() -> None:
    atom_tests = audit_base_B_atom()
    assert atom_tests == 131071

    # Seven copies can satisfy their sole seven-subset window; eight cannot.
    profiles_7 = valid_same_fibre_height_profiles(7)
    profiles_8 = valid_same_fibre_height_profiles(8)
    assert profiles_7 == 322
    assert profiles_8 == 0

    base_counts, heavy = heavy_fibres()
    assert tuple((g, base_counts[g]) for g in heavy) == (
        ((1, 0, 1), 4),
        ((1, 6, 1), 4),
    )
    forbidden = build_forbidden_T_subset_sums(heavy)
    ban_counts = {
        str(g): {size: len(forbidden[g][size]) for size in sorted(forbidden[g])}
        for g in heavy
    }
    assert ban_counts == {
        "(1, 0, 1)": {1: 232, 2: 186, 3: 136, 4: 82, 5: 35, 6: 9},
        "(1, 6, 1)": {1: 241, 2: 193, 3: 140, 4: 83, 5: 35, 6: 9},
    }
    digest = table_digest(forbidden)
    assert digest == EXPECTED_BAN_SHA256

    (
        unary,
        levels,
        attempts,
        valid_extensions,
        closure,
        solutions,
    ) = exhaust_T_multisets(base_counts, heavy, forbidden)
    assert len(unary) == 71
    assert levels == EXPECTED_LEVEL_COUNTS
    assert attempts == EXPECTED_ATTEMPTS
    assert valid_extensions == EXPECTED_VALID_EXTENSIONS
    assert closure == EXPECTED_CLOSURE
    assert solutions == ()

    old_window_lifts, old_valid_lifts = audit_rejected_support_witness()

    print("PASS explicit B=q^3Q is a quotient atom; target tests:", atom_tests)
    print("PASS quotient-fibre cap: valid height profiles at sizes 7/8:",
          profiles_7, profiles_8)
    print("HEAVY B FIBRES:", tuple((g, base_counts[g]) for g in heavy))
    print("FORBIDDEN T-SUBSET SUM COUNTS:", ban_counts)
    print("FORBIDDEN TABLE SHA256:", digest)
    print("UNARY NONZERO T LABELS: 342 ->", len(unary))
    print("VALID SORTED PREFIX COUNTS (length 0..5):", levels)
    print("EXTENSION ATTEMPTS:", attempts)
    print("VALID EXTENSIONS:", valid_extensions)
    print("ZERO-SUM CLOSURE OF 5-PREFIXES:", closure)
    print("SURVIVING SIX-POSITION T MULTISETS:", len(solutions))
    print("PASS old quotient support height lifts before/after multiplicity:",
          old_window_lifts, old_valid_lifts)
    print("CERTIFIED: the explicit length-19 B skeleton has no T quotient lift")
    print("STATUS: INCOMPLETE -- other B atoms and the full p=7,m=3 branch remain")


if __name__ == "__main__":
    main()
