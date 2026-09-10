#!/usr/bin/env python3
"""Unified quotient search for the p=7, m=4, 0001, s=6 frontier.

The decisive certificate is a middle-layer saturation test on a fixed
length-19 complement B.  The same position labels also feed exact oracles for
all quotient-zero short sets, the forbidden 9--12 layers, conditional F3
complement atomicity, and every heavy quotient fibre.  No selected tail list
is accepted as input.

The default run proves that the explicit B from ``p7_m4_next_frontier.md``
has no six-position T extension satisfying the inherited full-F3-network
conditions, which force every position label to be nonzero.  It does not
exclude arbitrary bare T multisets containing quotient zero, classify other
length-19 quotient atoms, or solve the full 0001 orbit.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations, product
from typing import Iterable, Sequence

import verify_p7_m4_next_csp as FRONTIER


P = 7
ZERO3 = (0, 0, 0)
Q = (1, 0, 0)
PROFILE = (0, 0, 0, 1)
LENGTH_FAMILIES = FRONTIER.LENGTH_FAMILIES

# The fixed length-19 complement B=q^4 Q of equations (23)--(24).
BASE_Q = FRONTIER.S6_QUOTIENT_ATOM_Q
BASE_B = (Q,) * 4 + BASE_Q

# Retained only as a rejected-interface regression.  The theorem below
# quantifies over every six-position T satisfying the inherited full-F3
# network, not merely this old rejected assignment.
REJECTED_T = FRONTIER.REJECTED_S6_T_QUOTIENT

EXPECTED_SPECTRUM_COUNTS = {8: 305, 9: 312, 10: 312, 11: 305}
EXPECTED_FIRST_WITNESS_HISTOGRAM = {8: 305, 9: 23, 10: 11, 11: 3}
EXPECTED_WITNESS_SHA256 = (
    "7fefc772ca2ad2f70ac2f64491ccd317c38b93f88bc30f07a35349b6dbd7dfdd"
)

HEAVY_PATTERNS = (
    (1, 1),
    (1, 2),
    (1, 7),
    (2, 1),
    (2, 6),
    (3, 5),
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


def mask_sum(labels: Sequence[tuple[int, int, int]], mask: int):
    return sum3(labels[index] for index in range(len(labels)) if mask >> index & 1)


def subset_tables(labels: Sequence[tuple[int, int, int]]):
    sums = [ZERO3] * (1 << len(labels))
    sizes = [0] * (1 << len(labels))
    for mask in range(1, 1 << len(labels)):
        bit = mask & -mask
        index = bit.bit_length() - 1
        previous = mask ^ bit
        sums[mask] = add3(sums[previous], labels[index])
        sizes[mask] = sizes[previous] + 1
    return sums, sizes


def audit_fixed_B_atom() -> int:
    """Replay the exact b=0,1,2 criterion for B=q^4 dot-union Q."""
    sums, _ = subset_tables(BASE_Q)
    assert sums[-1] == scale3(-4, Q)
    tests = 0
    for b in range(3):
        target = scale3(-b, Q)
        for mask, value in enumerate(sums):
            if b == 0 and mask == 0:
                continue
            tests += 1
            assert value != target
    assert tests == 3 * (1 << len(BASE_Q)) - 1 == 98303
    return tests


def middle_internal_spectrum(labels: Sequence[tuple[int, int, int]]):
    """Return exact position-subset spectra Sigma_k(B), k=8,9,10,11.

    The first witness for a sum is ordered first by cardinality and then by
    the integer bit mask.  This makes the finite certificate deterministic.
    """
    sums, sizes = subset_tables(labels)
    spectra: dict[int, set[tuple[int, int, int]]] = {
        size: set() for size in range(8, 12)
    }
    witnesses: dict[tuple[int, int, int], tuple[int, int]] = {}
    for size in range(8, 12):
        for mask, (value, cardinality) in enumerate(zip(sums, sizes)):
            if cardinality != size:
                continue
            spectra[size].add(value)
            witnesses.setdefault(value, (size, mask))
    return spectra, witnesses


def witness_digest(witnesses) -> str:
    serial = [
        (list(value), size, mask)
        for value, (size, mask) in sorted(witnesses.items())
    ]
    payload = json.dumps(serial, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def independent_spectrum_replay(labels: Sequence[tuple[int, int, int]]):
    """Recompute the certificate through combinations, independently of DP."""
    spectra = {size: set() for size in range(8, 12)}
    witnesses = {}
    for size in range(8, 12):
        for subset in combinations(range(len(labels)), size):
            value = sum3(labels[index] for index in subset)
            mask = sum(1 << index for index in subset)
            spectra[size].add(value)
            previous = witnesses.get(value)
            if previous is None or (size, mask) < previous:
                witnesses[value] = (size, mask)
    return spectra, witnesses


def audit_middle_saturation():
    spectra, witnesses = middle_internal_spectrum(BASE_B)
    replay_spectra, replay_witnesses = independent_spectrum_replay(BASE_B)
    assert replay_spectra == spectra
    assert replay_witnesses == witnesses
    nonzero = {
        value for value in product(range(P), repeat=3) if value != ZERO3
    }
    assert {size: len(values) for size, values in spectra.items()} == (
        EXPECTED_SPECTRUM_COUNTS
    )
    assert set(witnesses) == nonzero
    assert ZERO3 not in witnesses
    histogram = Counter(size for size, _ in witnesses.values())
    assert dict(sorted(histogram.items())) == EXPECTED_FIRST_WITNESS_HISTOGRAM
    assert witness_digest(witnesses) == EXPECTED_WITNESS_SHA256

    # Validate every canonical witness against the original 19 positions.
    for value, (size, mask) in witnesses.items():
        assert mask.bit_count() == size
        assert 8 <= size <= 11
        assert mask_sum(BASE_B, mask) == value

    # Every possible nonzero T label is killed by a B-internal subset.  The
    # union has size 9--12 and quotient sum zero, exactly the forbidden middle
    # layer of the frozen SQ interface.
    extension_domain = [
        t_label for t_label in sorted(nonzero) if neg3(t_label) not in witnesses
    ]
    for t_label in sorted(nonzero):
        target = neg3(t_label)
        size, mask = witnesses[target]
        assert add3(mask_sum(BASE_B, mask), t_label) == ZERO3
        assert 9 <= size + 1 <= 12
    assert extension_domain == []
    return spectra, witnesses, tuple(extension_domain)


def zero_masks_by_size(labels: Sequence[tuple[int, int, int]], max_size: int = 12):
    """Enumerate all quotient-zero position masks through ``max_size``.

    A 12+13 meet-in-the-middle join is used for 25 labels.  Returned masks are
    exact position subsets, not support subsets and not preselected tails.
    """
    split = len(labels) // 2
    left_sums, left_sizes = subset_tables(labels[:split])
    right_sums, right_sizes = subset_tables(labels[split:])
    right: dict[tuple[int, tuple[int, int, int]], list[int]] = defaultdict(list)
    for mask, (size, value) in enumerate(zip(right_sizes, right_sums)):
        if size <= max_size:
            right[(size, value)].append(mask)

    answer: dict[int, list[int]] = {size: [] for size in range(1, max_size + 1)}
    for left_mask, (left_size, left_value) in enumerate(zip(left_sizes, left_sums)):
        for size in range(max(1, left_size), max_size + 1):
            right_size = size - left_size
            if right_size < 0:
                continue
            for right_mask in right.get((right_size, neg3(left_value)), ()):
                answer[size].append(left_mask | (right_mask << split))
    for size, masks in answer.items():
        assert len(masks) == len(set(masks))
        assert all(mask.bit_count() == size for mask in masks)
        assert all(mask_sum(labels, mask) == ZERO3 for mask in masks)
    return answer


@dataclass(frozen=True)
class ShortConstraint:
    mask: int
    length: int
    allowed_height_sums: frozenset[int]
    complement_zero_witness: int | None


def conditional_short_constraints(labels: Sequence[tuple[int, int, int]]):
    """Rebuild every automatic short block and every F3 complement oracle.

    For lengths 6--8, family 3 is retained only when the long complement is a
    quotient atom.  A non-atomic complement supplies an internal quotient-zero
    subset disjoint from the short block, so that short block cannot be F3.
    The output is a system of exact height-sum domains, not a list of chosen
    blocks.
    """
    zero = zero_masks_by_size(labels, 12)
    small_zero = [mask for size in range(1, 10) for mask in zero[size]]
    constraints: list[ShortConstraint] = []
    for length in range(2, 9):
        for mask in zero[length]:
            allowed = set(LENGTH_FAMILIES[length])
            obstruction = None
            if 3 in allowed:
                obstruction = next(
                    (other for other in small_zero if other & mask == 0), None
                )
                if obstruction is not None:
                    allowed.remove(3)
            constraints.append(
                ShortConstraint(mask, length, frozenset(allowed), obstruction)
            )
    medium = tuple(mask for size in range(9, 13) for mask in zero[size])
    return tuple(constraints), medium


def disjoint_short_gap_closure(
    labels: Sequence[tuple[int, int, int]],
    constraints: Sequence[ShortConstraint],
):
    """Close every disjoint short-block pair against the 9--16 gap.

    For p=7, two disjoint quotient-zero blocks of total length at least nine
    already have union length 9--16.  If the union is longer than twelve, its
    complement has length 9--12 and quotient sum zero because the 25 labels
    sum to zero.  The same incremental argument shows that every pairwise
    disjoint family of automatic short blocks has total support at most eight.
    """
    assert sum3(labels) == ZERO3
    count = 0
    first = None
    for left_index, left in enumerate(constraints):
        for right in constraints[left_index + 1 :]:
            total_length = left.length + right.length
            if total_length < 9 or left.mask & right.mask:
                continue
            union = left.mask | right.mask
            assert union.bit_count() == total_length
            assert 9 <= total_length <= 16
            assert mask_sum(labels, union) == ZERO3
            if total_length > 12:
                full = (1 << len(labels)) - 1
                complement = full ^ union
                assert 9 <= complement.bit_count() <= 12
                assert mask_sum(labels, complement) == ZERO3
            count += 1
            if first is None:
                first = (left.mask, right.mask, total_length)
    return count, first


def heavy_fibre_obstructions(labels: Sequence[tuple[int, int, int]]):
    """Check all six singleton-window patterns for every current heavy fibre."""
    failures = []
    counts = Counter(labels)
    for value, multiplicity in sorted(counts.items()):
        if multiplicity < 4:
            continue
        outside = tuple(index for index, label in enumerate(labels) if label != value)
        for core_size, tail_size in HEAVY_PATTERNS:
            target = scale3(-core_size, value)
            witness = next(
                (
                    subset
                    for subset in combinations(outside, tail_size)
                    if sum3(labels[index] for index in subset) == target
                ),
                None,
            )
            if witness is not None:
                failures.append((value, multiplicity, core_size, tail_size, witness))
    return tuple(failures)


def diagnose_unified_interface(t_labels):
    """Return exact unified-oracle diagnostics for one six-position T."""
    if len(t_labels) != 6:
        raise ValueError("the p=7,m=4,s=6 interface requires six T labels")
    if sum3(t_labels) != ZERO3:
        raise ValueError("the six T quotient labels must sum to zero")
    labels = (Q,) * 4 + tuple(t_labels) + BASE_Q
    assert len(labels) == 25
    assert sum3(labels) == ZERO3
    constraints, medium = conditional_short_constraints(labels)
    disjoint_gap_pairs, first_gap_pair = disjoint_short_gap_closure(
        labels, constraints
    )
    by_length = Counter(constraint.length for constraint in constraints)
    empty_domains = sum(not constraint.allowed_height_sums for constraint in constraints)
    complement_cuts = sum(
        constraint.complement_zero_witness is not None
        for constraint in constraints
    )
    heavy = heavy_fibre_obstructions(labels)
    return {
        "short_zero_counts": dict(sorted(by_length.items())),
        "medium_zero_count": len(medium),
        "disjoint_short_gap_pairs": disjoint_gap_pairs,
        "first_disjoint_short_gap_pair": first_gap_pair,
        "conditional_complement_cuts": complement_cuts,
        "empty_short_height_domains": empty_domains,
        "heavy_fibre_obstructions": len(heavy),
        "rejected": bool(
            medium or disjoint_gap_pairs or empty_domains or heavy
        ),
    }


def audit_rejected_unified_interface():
    """Exercise the parameterized diagnostic on the old rejected skeleton."""
    report = diagnose_unified_interface(REJECTED_T)
    assert report["medium_zero_count"]
    assert report["disjoint_short_gap_pairs"]
    assert report["first_disjoint_short_gap_pair"] is not None
    assert report["heavy_fibre_obstructions"]
    assert (
        report["empty_short_height_domains"]
        <= report["conditional_complement_cuts"]
    )
    assert report["rejected"]
    return report


def main() -> None:
    atom_tests = audit_fixed_B_atom()
    spectra, witnesses, extension_domain = audit_middle_saturation()
    interface = audit_rejected_unified_interface()

    print("PASS fixed B=q^4Q quotient atom; exact target tests:", atom_tests)
    print(
        "B INTERNAL SUM SPECTRUM COUNTS (sizes 8..11):",
        {size: len(values) for size, values in spectra.items()},
    )
    print(
        "FIRST-WITNESS SIZE HISTOGRAM:",
        dict(sorted(Counter(size for size, _ in witnesses.values()).items())),
    )
    print("MIDDLE-SPECTRUM UNION:", len(witnesses), "nonzero values; zero absent")
    print("WITNESS TABLE SHA256:", witness_digest(witnesses))
    print("SURVIVING NONZERO T LABELS AFTER INTERNAL-SUM COVERAGE:", len(extension_domain))
    print("UNIFIED REJECTED-SKELETON DIAGNOSTIC:", interface)
    print(
        "CERTIFIED: the explicit length-19 B orbit has no "
        "full-F3-network T extension"
    )
    print(
        "QUANTIFIER: fixed B, every T satisfying inherited "
        "nonzero-position conditions"
    )
    print("STATUS: PROVED fixed-B exclusion; full p=7,m=4,0001 remains INCOMPLETE")


if __name__ == "__main__":
    main()
