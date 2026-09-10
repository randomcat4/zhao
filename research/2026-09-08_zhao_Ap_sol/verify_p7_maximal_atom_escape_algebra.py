#!/usr/bin/env python3
"""Exact checks for the p=7 maximal-atom escape algebra lemmas.

The mathematical proof is in proofs/p7_maximal_atom_escape_algebra.md.
This verifier uses actual positions throughout.  It checks seven frozen
length-19 atoms, including the four support-seven atoms with nonempty escape.
It is a finite regression for the general lemmas, not their proof.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import product


P = 7
ORDER = P**3
ZERO = (0, 0, 0)
Q = (1, 0, 0)
E1 = Q
E2 = (0, 1, 0)
E3 = (0, 0, 1)
VECTORS = tuple(product(range(P), repeat=3))
VECTOR_ID = {value: index for index, value in enumerate(VECTORS)}
ZERO_ID = VECTOR_ID[ZERO]


def add(left, right):
    return tuple((left[index] + right[index]) % P for index in range(3))


def scale(coefficient, value):
    return tuple((coefficient * entry) % P for entry in value)


def neg(value):
    return scale(-1, value)


def total(values):
    answer = ZERO
    for value in values:
        answer = add(answer, value)
    return answer


ADD_ID = tuple(
    tuple(VECTOR_ID[add(left, right)] for right in VECTORS)
    for left in VECTORS
)
NEG_ID = tuple(VECTOR_ID[neg(value)] for value in VECTORS)
SCALE_ID = tuple(
    tuple(VECTOR_ID[scale(coefficient, value)] for coefficient in range(P))
    for value in VECTORS
)


def expanded(entries):
    return tuple(
        sorted(value for value, multiplicity in entries for _ in range(multiplicity))
    )


ATOMS = (
    (
        "prior_B0",
        expanded((
            (Q, 3), ((0, 0, 1), 1), ((0, 1, 0), 1),
            ((0, 1, 6), 3), ((1, 0, 1), 4), ((1, 5, 1), 1),
            ((1, 6, 1), 4), ((4, 5, 3), 1), ((5, 4, 4), 1),
        )),
        (),
    ),
    (
        "support6_plus",
        expanded((
            (Q, 3), (E2, 4), (E3, 4), ((0, 1, 6), 1),
            ((1, 1, 0), 3), ((2, 5, 1), 4),
        )),
        (),
    ),
    (
        "support6_minus",
        expanded((
            (Q, 3), (E2, 4), (E3, 4), ((0, 1, 6), 1),
            ((1, 6, 0), 3), ((2, 3, 1), 4),
        )),
        (),
    ),
    (
        "support7_escape_1",
        expanded((
            (E3, 4), (E2, 4), ((0, 1, 6), 2), (Q, 3),
            ((1, 0, 6), 1), ((1, 2, 1), 4), ((6, 0, 2), 1),
        )),
        ((6, 5, 6),),
    ),
    (
        "support7_escape_2",
        expanded((
            (E3, 4), (E2, 4), ((0, 1, 6), 2), (Q, 3),
            ((1, 1, 1), 3), ((1, 6, 0), 2), ((6, 0, 2), 1),
        )),
        ((6, 6, 6),),
    ),
    (
        "support7_escape_3",
        expanded((
            (E3, 4), (E2, 4), ((0, 1, 6), 2), (Q, 3),
            ((1, 1, 6), 1), ((1, 2, 1), 4), ((6, 6, 2), 1),
        )),
        ((6, 5, 6),),
    ),
    (
        "support7_escape_4",
        expanded((
            (E3, 4), (E2, 4), ((0, 1, 6), 2), (Q, 3),
            ((1, 5, 6), 2), ((1, 6, 6), 3), ((6, 1, 3), 1),
        )),
        ((6, 0, 0),),
    ),
)

EXPECTED_REPORT_SHA256 = "4460a569e44cf7753af45550098191611e0ca33db943059c3332eb1f2262592c"


def fixed_size_supports(labels, maximum):
    layers = [set() for _ in range(maximum + 1)]
    layers[0].add(ZERO_ID)
    for index, label in enumerate(labels):
        label_id = VECTOR_ID[label]
        for size in range(min(maximum, index + 1), 0, -1):
            layers[size].update(ADD_ID[old_sum][label_id] for old_sum in layers[size - 1])
    return tuple(frozenset(layer) for layer in layers)


def fixed_size_counts(labels, maximum):
    layers = [[0] * ORDER for _ in range(maximum + 1)]
    layers[0][ZERO_ID] = 1
    for index, label in enumerate(labels):
        label_id = VECTOR_ID[label]
        for size in range(min(maximum, index + 1), 0, -1):
            previous = layers[size - 1]
            current = layers[size]
            for old_sum, count in enumerate(previous):
                if count:
                    new_sum = ADD_ID[old_sum][label_id]
                    current[new_sum] = (current[new_sum] + count) % P
    return tuple(tuple(layer) for layer in layers)


def group_algebra_product(labels):
    coefficients = [0] * ORDER
    coefficients[ZERO_ID] = 1
    for label in labels:
        label_id = VECTOR_ID[label]
        updated = coefficients.copy()
        for old_sum, coefficient in enumerate(coefficients):
            if coefficient:
                new_sum = ADD_ID[old_sum][label_id]
                updated[new_sum] = (updated[new_sum] - coefficient) % P
        coefficients = updated
    return tuple(coefficients)


def all_subset_data(labels):
    count = 1 << len(labels)
    sums = [ZERO_ID] * count
    sizes = bytearray(count)
    label_ids = tuple(VECTOR_ID[label] for label in labels)
    for mask in range(1, count):
        bit = mask & -mask
        index = bit.bit_length() - 1
        previous = mask ^ bit
        sums[mask] = ADD_ID[sums[previous]][label_ids[index]]
        sizes[mask] = sizes[previous] + 1
    return sums, sizes


def is_projectively_simple(labels):
    support = tuple(sorted(set(labels)))
    if ZERO in support:
        return False
    for left_index, left in enumerate(support):
        for right in support[left_index + 1:]:
            if any(scale(coefficient, left) == right for coefficient in range(1, P)):
                return False
    return True


def is_atom_by_position_dp(labels):
    if len(labels) != 19 or total(labels) != ZERO:
        return False
    supports = fixed_size_supports(labels, 9)
    return all(ZERO_ID not in supports[size] for size in range(1, 10))


def escape_values(labels):
    supports = fixed_size_supports(labels, 11)
    covered = set().union(*(supports[size] for size in range(4, 12)))
    return tuple(VECTORS[value_id] for value_id in range(1, ORDER) if value_id not in covered)


def signed_sum(masks, sizes):
    return sum((-1 if sizes[mask] % 2 else 1) for mask in masks) % P


def representation_families(labels, target, sums, sizes):
    target_id = VECTOR_ID[target]
    negative_id = NEG_ID[target_id]
    low = tuple(
        mask for mask in range(1, len(sums))
        if sizes[mask] <= 3 and sums[mask] == target_id
    )
    negative = tuple(
        mask for mask in range(1, len(sums))
        if sizes[mask] <= 7 and sums[mask] == negative_id
    )
    return low, negative


def audit_deleted_identities(labels, target, sums, sizes):
    low, negative = representation_families(labels, target, sums, sizes)
    rho = signed_sum(low, sizes)
    kappa = signed_sum(negative, sizes)
    target_id = VECTOR_ID[target]
    negative_id = NEG_ID[target_id]
    all_target = tuple(
        mask for mask in range(1, len(sums)) if sums[mask] == target_id
    )
    all_negative = tuple(
        mask for mask in range(1, len(sums)) if sums[mask] == negative_id
    )
    full_mask = (1 << len(labels)) - 1
    assert rho == kappa
    for index in range(19):
        bit = 1 << index
        low_avoiding = {mask for mask in low if not mask & bit}
        negative_avoiding = {mask for mask in negative if not mask & bit}
        low_containing = {mask for mask in low if mask & bit}
        negative_containing = {mask for mask in negative if mask & bit}
        high_target = {full_mask ^ mask for mask in negative_containing}
        high_negative = {full_mask ^ mask for mask in low_containing}
        actual_target = {mask for mask in all_target if not mask & bit}
        actual_negative = {mask for mask in all_negative if not mask & bit}

        # These exact set equalities audit the deleted-position condition and
        # the odd complement sign, not merely the resulting congruence.
        assert actual_target == low_avoiding | high_target
        assert actual_negative == negative_avoiding | high_negative
        assert all(12 <= sizes[mask] <= 18 for mask in high_target)
        assert all(16 <= sizes[mask] <= 18 for mask in high_negative)

        rho_i = signed_sum(low_containing, sizes)
        kappa_i = signed_sum(negative_containing, sizes)
        assert signed_sum(high_target, sizes) == (-kappa_i) % P
        assert signed_sum(high_negative, sizes) == (-rho_i) % P
        assert signed_sum(actual_target, sizes) == 1
        assert signed_sum(actual_negative, sizes) == 1
        assert (rho - rho_i - kappa_i) % P == 1
        assert (kappa - kappa_i - rho_i) % P == 1
        assert (rho_i + kappa_i) % P == (rho - 1) % P
    for low_mask in low:
        for negative_mask in negative:
            assert low_mask & negative_mask
    first_moment = (
        sum(sizes[mask] * (-1 if sizes[mask] % 2 else 1) for mask in low)
        + sum(sizes[mask] * (-1 if sizes[mask] % 2 else 1) for mask in negative)
    ) % P
    assert first_moment == (19 * (rho - 1)) % P
    return low, negative, rho


def ladder_escape(labels, target, fibre_value):
    multiplicity = labels.count(fibre_value)
    outside = tuple(label for label in labels if label != fibre_value)
    outside_supports = fixed_size_supports(outside, 11)
    target_id = VECTOR_ID[target]
    for copies in range(multiplicity + 1):
        lower = max(0, 4 - copies)
        upper = min(len(outside), 11 - copies)
        shifted_target = ADD_ID[target_id][NEG_ID[SCALE_ID[VECTOR_ID[fibre_value]][copies % P]]]
        if any(shifted_target in outside_supports[size] for size in range(lower, upper + 1)):
            return False
    return True


def signed_fibre_ladder(labels, target, fibre_value):
    multiplicity = labels.count(fibre_value)
    assert multiplicity in (3, 4)
    outside = tuple(label for label in labels if label != fibre_value)
    counts = fixed_size_counts(outside, 7)
    target_id = VECTOR_ID[target]
    negative_target_id = NEG_ID[target_id]
    value_id = VECTOR_ID[fibre_value]

    alpha = []
    beta = []
    for copies in range(multiplicity + 1):
        positive_shift = NEG_ID[SCALE_ID[value_id][copies % P]]
        positive_target = ADD_ID[target_id][positive_shift]
        negative_target = ADD_ID[negative_target_id][positive_shift]
        alpha_value = 0
        if copies <= 3:
            for size in range(0, 3 - copies + 1):
                sign = -1 if (copies + size) % 2 else 1
                alpha_value += sign * counts[size][positive_target]
        beta_value = 0
        for size in range(0, 7 - copies + 1):
            sign = -1 if (copies + size) % 2 else 1
            beta_value += sign * counts[size][negative_target]
        alpha.append(alpha_value % P)
        beta.append(beta_value % P)

    if multiplicity == 3:
        first = alpha[0] + 2 * alpha[1] + alpha[2] - beta[1] - 2 * beta[2] - beta[3]
        second = beta[0] + 2 * beta[1] + beta[2] - alpha[1] - 2 * alpha[2] - alpha[3]
    else:
        first = (
            alpha[0] + 3 * alpha[1] + 3 * alpha[2] + alpha[3]
            - beta[1] - 3 * beta[2] - 3 * beta[3] - beta[4]
        )
        second = (
            beta[0] + 3 * beta[1] + 3 * beta[2] + beta[3]
            - alpha[1] - 3 * alpha[2] - 3 * alpha[3]
        )
    assert first % P == 1
    assert second % P == 1
    return tuple(alpha), tuple(beta)


def audit_fibre_tail_intersections(labels, target, low, negative):
    for fibre_value, multiplicity in Counter(labels).items():
        if multiplicity not in (3, 4):
            continue
        fibre_mask = sum(1 << index for index, label in enumerate(labels) if label == fibre_value)
        outside_mask = ((1 << 19) - 1) ^ fibre_mask
        for low_mask in low:
            low_copies = (low_mask & fibre_mask).bit_count()
            low_tail = low_mask & outside_mask
            for negative_mask in negative:
                negative_copies = (negative_mask & fibre_mask).bit_count()
                negative_tail = negative_mask & outside_mask
                if low_copies + negative_copies <= multiplicity:
                    assert low_tail & negative_tail

        for copies in range(1, min(3, multiplicity) + 1):
            if target != scale(copies, fibre_value):
                continue
            minimum_negative_copies = multiplicity - copies + 1
            assert all(
                (mask & fibre_mask).bit_count() >= minimum_negative_copies
                for mask in negative
            )


def audit_truncated_group_algebra():
    top_labels = (E1,) * 6 + (E2,) * 6 + (E3,) * 6
    omega = (1,) * ORDER
    exponent_triples = tuple(product(range(P), repeat=3))
    assert tuple(triple for triple in exponent_triples if sum(triple) >= 18) == ((6, 6, 6),)
    assert not any(sum(triple) >= 19 for triple in exponent_triples)
    assert group_algebra_product(top_labels) == omega
    for value in VECTORS:
        if value == ZERO:
            continue
        assert group_algebra_product(top_labels + (value,)) == (0,) * ORDER


def audit_atom(name, labels, expected_escape):
    assert len(labels) == 19
    assert total(labels) == ZERO
    assert is_atom_by_position_dp(labels)
    assert is_projectively_simple(labels)
    assert escape_values(labels) == expected_escape

    omega = (1,) * ORDER
    for deleted in range(19):
        remaining = labels[:deleted] + labels[deleted + 1:]
        assert group_algebra_product(remaining) == omega
    assert group_algebra_product(labels) == (0,) * ORDER

    global_escape = set(expected_escape)
    for fibre_value, multiplicity in Counter(labels).items():
        if multiplicity not in (3, 4):
            continue
        for target in VECTORS[1:]:
            assert ladder_escape(labels, target, fibre_value) == (target in global_escape)

    sums, sizes = all_subset_data(labels)
    escape_reports = []
    for target in expected_escape:
        low, negative, signed_total = audit_deleted_identities(
            labels, target, sums, sizes
        )
        for fibre_value, multiplicity in Counter(labels).items():
            if multiplicity in (3, 4):
                signed_fibre_ladder(labels, target, fibre_value)
        audit_fibre_tail_intersections(labels, target, low, negative)
        escape_reports.append((target, len(low), len(negative), signed_total))
    return {
        "name": name,
        "support": len(set(labels)),
        "fibre_signature": tuple(sorted(Counter(labels).values(), reverse=True)),
        "escape_reports": tuple(escape_reports),
    }


def main():
    audit_truncated_group_algebra()
    reports = tuple(audit_atom(*atom) for atom in ATOMS)
    payload = json.dumps(reports, sort_keys=True, separators=(",", ":"), default=list).encode("ascii")
    digest = hashlib.sha256(payload).hexdigest()
    assert digest == EXPECTED_REPORT_SHA256
    print("PASS truncated group algebra: I^18 top product is Omega and I^19 vanishes")
    print("PASS exact atoms/projective simplicity/deleted products:", len(reports))
    for report in reports:
        print("ATOM", json.dumps(report, separators=(",", ":"), default=list))
    print("PASS exact gap ladders for every three/four-fold fibre and all 342 nonzero targets")
    print("PASS deleted-point alternating identities and R-C cross-intersection on all escape targets")
    print("REPORT SHA256:", digest)
    print("STATUS: finite regression for general necessary lemmas; no support>=8 closure claim")


if __name__ == "__main__":
    main()
