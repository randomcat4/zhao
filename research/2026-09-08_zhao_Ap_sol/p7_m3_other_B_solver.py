#!/usr/bin/env python3
"""Exact/reproducible frontier for other p=7,m=3 quotient atoms.

The ``--probe`` path performs a deterministic sum-preserving local search
starting from the already known atom. It is exploration only. The default
path is reserved for replaying frozen finite certificates and proved lemmas.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter, defaultdict
from itertools import combinations, product
from typing import Iterable, Sequence


P = 7
ZERO = (0, 0, 0)
Q_NORMAL = (1, 0, 0)
OLD_Q = (
    (0, 0, 1), (0, 1, 0),
    (0, 1, 6), (0, 1, 6), (0, 1, 6),
    (1, 0, 1), (1, 0, 1), (1, 0, 1), (1, 0, 1),
    (1, 5, 1),
    (1, 6, 1), (1, 6, 1), (1, 6, 1), (1, 6, 1),
    (4, 5, 3), (5, 4, 4),
)
OTHER_Q = (
    (0, 0, 1), (0, 1, 0),
    (0, 1, 6), (0, 1, 6), (0, 1, 6),
    (1, 0, 1), (5, 4, 4), (1, 0, 1), (1, 0, 1),
    (1, 5, 1),
    (1, 6, 1), (1, 6, 1), (1, 6, 1), (1, 6, 1),
    (0, 1, 0), (5, 4, 4),
)
OTHER_Q_2 = (
    (5, 5, 3), (1, 6, 1), (1, 6, 1), (0, 0, 1),
    (0, 1, 6), (1, 6, 1), (1, 0, 1), (0, 1, 6),
    (5, 4, 4), (0, 0, 1), (1, 5, 1), (0, 1, 0),
    (1, 0, 1), (0, 1, 6), (1, 6, 1), (1, 0, 1),
)
OTHER_Q_3 = (
    (0, 0, 1), (1, 6, 1), (0, 1, 6), (1, 6, 1),
    (0, 0, 1), (5, 5, 3), (1, 6, 1), (1, 0, 1),
    (0, 0, 1), (5, 5, 3), (1, 5, 1), (0, 1, 6),
    (1, 0, 1), (1, 0, 1), (0, 1, 6), (1, 6, 1),
)
OTHER_Q_CERTIFICATES = (OTHER_Q, OTHER_Q_2, OTHER_Q_3)
EXPECTED_SIGNATURES = (
    (4, 3, 3, 3, 2, 2, 1, 1),
    (4, 3, 3, 3, 2, 1, 1, 1, 1),
    (4, 3, 3, 3, 3, 2, 1),
)
EXPECTED_MIDDLE_LAYERS = (
    (291, 302, 302, 291),
    (313, 322, 322, 313),
    (305, 312, 312, 305),
)
EXPECTED_MISSING = (
    ((1, 6, 1), (6, 1, 6)),
    (),
    (),
)
HEAVY_PATTERNS = ((1, 1), (1, 2), (1, 7), (2, 1), (2, 6), (3, 5))
ALL_NONZERO = tuple(v for v in product(range(P), repeat=3) if v != ZERO)


def add(left: tuple[int, int, int], right: tuple[int, int, int]):
    return tuple((left[i] + right[i]) % P for i in range(3))


def neg(vector: tuple[int, int, int]):
    return tuple((-entry) % P for entry in vector)


def scale(scalar: int, vector: tuple[int, int, int]):
    return tuple((scalar * entry) % P for entry in vector)


def total(vectors: Iterable[tuple[int, int, int]]):
    answer = ZERO
    for vector in vectors:
        answer = add(answer, vector)
    return answer


def atom_obstruction(q_labels: Sequence[tuple[int, int, int]]):
    """Return a forbidden Q submask, or None, for B=q^3 Q."""
    sums = [ZERO] * (1 << len(q_labels))
    for mask in range(1, len(sums)):
        bit = mask & -mask
        index = bit.bit_length() - 1
        sums[mask] = add(sums[mask ^ bit], q_labels[index])
        if sums[mask] == ZERO or sums[mask] == neg(Q_NORMAL):
            return mask
    if sums[-1] != scale(-3, Q_NORMAL):
        return -1
    return None


def is_atom_fast(q_labels: Sequence[tuple[int, int, int]]):
    """Exact reachable-sum version of the same two-target atom test."""
    if total(q_labels) != scale(-3, Q_NORMAL):
        return False
    reachable = {ZERO}
    forbidden = {ZERO, neg(Q_NORMAL)}
    for label in q_labels:
        added = {add(old, label) for old in reachable}
        if added & forbidden:
            return False
        reachable |= added
    return True


def subset_sum_witness(
    labels: Sequence[tuple[int, int, int]], size: int, target
):
    """Exact DP witness for one prescribed subset size and quotient sum."""
    states: list[dict[tuple[int, int, int], int]] = [dict() for _ in range(size + 1)]
    states[0][ZERO] = 0
    for index, label in enumerate(labels):
        upper = min(size, index + 1)
        for count in range(upper, 0, -1):
            for old_sum, mask in tuple(states[count - 1].items()):
                new_sum = add(old_sum, label)
                states[count].setdefault(new_sum, mask | (1 << index))
    return states[size].get(target)


def medium_zero_witness(labels: Sequence[tuple[int, int, int]]):
    for size in range(9, 13):
        witness = subset_sum_witness(labels, size, ZERO)
        if witness is not None:
            return size, witness
    return None


def fixed_cardinality_sum_supports(labels, maximum: int):
    supports = [set() for _ in range(maximum + 1)]
    supports[0].add(ZERO)
    for index, label in enumerate(labels):
        for size in range(min(maximum, index + 1), 0, -1):
            supports[size].update(add(old, label) for old in supports[size - 1])
    return tuple(frozenset(support) for support in supports)


def middle_spectrum(base):
    """Return |Sigma_k(B)| for k=8..11 and their nonzero union."""
    supports = fixed_cardinality_sum_supports(base, 11)
    layers = tuple(len(supports[size]) for size in range(8, 12))
    union = frozenset().union(*(supports[size] for size in range(8, 12)))
    return layers, union - {ZERO}


def explicit_middle_supports(base):
    """Independent combinations replay of the four DP support layers."""
    return tuple(
        frozenset(total(base[index] for index in subset)
                  for subset in combinations(range(len(base)), size))
        for size in range(8, 12)
    )


def heavy_obstruction(labels: Sequence[tuple[int, int, int]]):
    counts = Counter(labels)
    for heavy, multiplicity in counts.items():
        if multiplicity < 4:
            continue
        outside = tuple(label for label in labels if label != heavy)
        for copies, size in HEAVY_PATTERNS:
            witness = subset_sum_witness(outside, size, scale(-copies, heavy))
            if witness is not None:
                return heavy, copies, size, witness
    return None


def build_forbidden_t_sums(base):
    """Compile all old-heavy-fibre singleton-window obstructions."""
    counts = Counter(base)
    heavy = tuple(sorted(label for label, count in counts.items() if count >= 4))
    tables = {}
    for value in heavy:
        outside_base = tuple(label for label in base if label != value)
        by_size: dict[int, set[tuple[int, int, int]]] = defaultdict(set)
        for copies, tail_size in HEAVY_PATTERNS:
            target = scale(-copies, value)
            assert subset_sum_witness(outside_base, tail_size, target) is None
            for t_size in range(1, min(6, tail_size) + 1):
                base_size = tail_size - t_size
                for base_part in combinations(outside_base, base_size):
                    by_size[t_size].add(add(target, neg(total(base_part))))
        tables[value] = dict(by_size)
    return counts, heavy, tables


def prefix_valid(prefix, base_counts, heavy, tables):
    prefix_counts = Counter(prefix)
    if any(base_counts[label] + count > 7 for label, count in prefix_counts.items()):
        return False
    for value in heavy:
        outside = tuple(label for label in prefix if label != value)
        for size in range(1, len(outside) + 1):
            forbidden = tables[value].get(size)
            if forbidden is None:
                continue
            if any(total(part) in forbidden for part in combinations(outside, size)):
                return False
    return True


def extension_valid(prefix, label, base_counts, heavy, tables):
    if base_counts[label] + prefix.count(label) + 1 > 7:
        return False
    for value in heavy:
        if label == value:
            continue
        outside = tuple(old for old in prefix if old != value)
        for size in range(1, len(outside) + 2):
            forbidden = tables[value].get(size)
            if forbidden is None:
                continue
            if any(
                add(total(old_part), label) in forbidden
                for old_part in combinations(outside, size - 1)
            ):
                return False
    return True


def exhaust_t_for_base(q_labels, solution_limit=10):
    """Enumerate S6 orbits under all heavy rules already present in B."""
    base = (Q_NORMAL,) * 3 + tuple(q_labels)
    base_counts, heavy, tables = build_forbidden_t_sums(base)
    unary = tuple(
        label
        for label in ALL_NONZERO
        if extension_valid((), label, base_counts, heavy, tables)
    )
    unary_index = {label: index for index, label in enumerate(unary)}
    levels = [1, 0, 0, 0, 0, 0]
    closure = Counter()
    solutions = []

    def walk(prefix, start, subtotal):
        if len(prefix) == 5:
            closure["prefixes"] += 1
            last = neg(subtotal)
            index = unary_index.get(last)
            if index is None:
                closure["last_not_unary"] += 1
                return
            if index < start:
                closure["last_breaks_order"] += 1
                return
            if not extension_valid(prefix, last, base_counts, heavy, tables):
                closure["last_propagation"] += 1
                return
            completed = prefix + (last,)
            assert prefix_valid(completed, base_counts, heavy, tables)
            closure["heavy_solutions"] += 1
            medium = medium_zero_witness(base + completed)
            if medium is not None:
                closure[f"medium_{medium[0]}"] += 1
                return
            closure["medium_survivors"] += 1
            if len(solutions) < solution_limit:
                solutions.append(completed)
            return
        for index in range(start, len(unary)):
            label = unary[index]
            if not extension_valid(prefix, label, base_counts, heavy, tables):
                continue
            levels[len(prefix) + 1] += 1
            walk(prefix + (label,), index, add(subtotal, label))

    walk((), 0, ZERO)
    return heavy, tables, unary, tuple(levels), dict(closure), tuple(solutions)


def q_signature(q_labels):
    return tuple(sorted(Counter((Q_NORMAL,) * 3 + tuple(q_labels)).values(), reverse=True))


def atom_target_audit(q_labels):
    """Replay every Q-position submask and return the two forbidden hit lists."""
    sums = [ZERO] * (1 << len(q_labels))
    for mask in range(1, len(sums)):
        bit = mask & -mask
        index = bit.bit_length() - 1
        sums[mask] = add(sums[mask ^ bit], q_labels[index])
    zero_hits = tuple(mask for mask in range(1, len(sums)) if sums[mask] == ZERO)
    minus_q_hits = tuple(mask for mask, value in enumerate(sums) if value == neg(Q_NORMAL))
    return sums[-1], zero_hits, minus_q_hits


def escape_support_audit(base, middle_union):
    """Audit the allowed single-position T labels after the middle-gap rule."""
    escape = tuple(
        label for label in ALL_NONZERO if neg(label) not in middle_union
    )
    zero_sum_multisets = []
    if len(escape) <= 12:
        def walk(prefix, start, subtotal):
            if len(prefix) == 6:
                if subtotal == ZERO:
                    zero_sum_multisets.append(prefix)
                return
            for index in range(start, len(escape)):
                walk(prefix + (escape[index],), index, add(subtotal, escape[index]))
        walk((), 0, ZERO)
    heavy_failures = tuple(heavy_obstruction(base + tail) for tail in zero_sum_multisets)
    return escape, tuple(zero_sum_multisets), heavy_failures


def audit_frozen_certificates():
    old_signature = q_signature(OLD_Q)
    assert old_signature == (4, 4, 3, 3, 1, 1, 1, 1, 1)
    reports = []
    for index, q_labels in enumerate(OTHER_Q_CERTIFICATES):
        base = (Q_NORMAL,) * 3 + q_labels
        full_sum, zero_hits, minus_q_hits = atom_target_audit(q_labels)
        assert full_sum == scale(-3, Q_NORMAL)
        assert zero_hits == () and minus_q_hits == ()
        signature = q_signature(q_labels)
        assert signature == EXPECTED_SIGNATURES[index]
        layers, middle_union = middle_spectrum(base)
        direct_supports = explicit_middle_supports(base)
        dp_supports = fixed_cardinality_sum_supports(base, 11)
        assert direct_supports == tuple(dp_supports[size] for size in range(8, 12))
        missing = tuple(sorted(set(ALL_NONZERO) - middle_union))
        assert layers == EXPECTED_MIDDLE_LAYERS[index]
        assert missing == EXPECTED_MISSING[index]
        escape, zero_tails, heavy_failures = escape_support_audit(base, middle_union)
        if index == 0:
            heavy = (1, 6, 1)
            assert escape == (heavy, neg(heavy))
            assert zero_tails == ((heavy,) * 3 + (neg(heavy),) * 3,)
            assert heavy_failures[0] is not None
            obstruction = heavy_failures[0]
            assert obstruction[:3] == (heavy, 1, 1)
        else:
            assert escape == () and zero_tails == () and heavy_failures == ()
        reports.append((signature, layers, missing, escape, len(zero_tails)))
    assert len({old_signature, *EXPECTED_SIGNATURES}) == 4
    return old_signature, tuple(reports)


def mutate_q(q_labels, rng: random.Random):
    candidate = list(q_labels)
    move_size = 2 if rng.random() < 0.4 else 3
    indices = rng.sample(range(len(candidate)), move_size)
    old_total = total(candidate[index] for index in indices)
    replacements = [rng.choice(ALL_NONZERO) for _ in range(move_size - 1)]
    replacements.append(add(old_total, neg(total(replacements))))
    if any(value in (ZERO, Q_NORMAL) for value in replacements):
        return None
    for index, value in zip(indices, replacements):
        candidate[index] = value
    return tuple(candidate)


def random_t(rng: random.Random):
    prefix = tuple(rng.choice(ALL_NONZERO) for _ in range(5))
    last = neg(total(prefix))
    return None if last == ZERO else prefix + (last,)


def probe(seed: int, atom_steps: int, t_trials: int):
    rng = random.Random(seed)
    current = OLD_Q
    assert atom_obstruction(current) is None
    atoms = {}
    accepted = 0
    for _ in range(atom_steps):
        candidate = mutate_q(current, rng)
        if candidate is None or not is_atom_fast(candidate):
            continue
        current = candidate
        accepted += 1
        key = tuple(sorted(candidate))
        if key == tuple(sorted(OLD_Q)):
            continue
        signature = q_signature(candidate)
        if signature[0] <= 4:
            atoms.setdefault(key, candidate)
    print("PROBE accepted atom moves:", accepted)
    print("PROBE distinct other atoms with max fibre <=4:", len(atoms))
    print("PROBE signatures:", Counter(q_signature(q) for q in atoms.values()))
    for index, q_labels in enumerate(atoms.values()):
        if index == 3:
            break
        print("PROBE atom", index + 1, "Q =", q_labels)

    heavy_pass = 0
    medium_pass = 0
    best = None
    for q_labels in atoms.values():
        base = (Q_NORMAL,) * 3 + q_labels
        for _ in range(t_trials):
            t_labels = random_t(rng)
            if t_labels is None:
                continue
            z = base + t_labels
            if max(Counter(z).values()) > 7:
                continue
            heavy = heavy_obstruction(z)
            if heavy is not None:
                continue
            heavy_pass += 1
            medium = medium_zero_witness(z)
            if medium is None:
                medium_pass += 1
                print("PROBE FOUND quotient support")
                print("Q =", q_labels)
                print("T =", t_labels)
                print("signature =", q_signature(q_labels))
                return
            score = medium[0]
            if best is None or score > best[0]:
                best = (score, q_labels, t_labels, medium)
    print("PROBE heavy-rule passes:", heavy_pass)
    print("PROBE medium-layer passes:", medium_pass)
    if best:
        print("PROBE best still has medium zero:", best[3])
        print("Q =", best[1])
        print("T =", best[2])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--seed", type=int, default=730031)
    parser.add_argument("--atom-steps", type=int, default=2000)
    parser.add_argument("--t-trials", type=int, default=200)
    parser.add_argument("--exhaust-other", action="store_true")
    parser.add_argument("--exhaust-index", type=int, default=1)
    parser.add_argument("--spectrum-only", action="store_true")
    args = parser.parse_args()
    if args.probe:
        probe(args.seed, args.atom_steps, args.t_trials)
        return
    if args.spectrum_only:
        for index, q_labels in enumerate(OTHER_Q_CERTIFICATES, 1):
            assert atom_obstruction(q_labels) is None
            layers, middle_union = middle_spectrum((Q_NORMAL,) * 3 + q_labels)
            missing = tuple(sorted(set(ALL_NONZERO) - middle_union))
            print(index, q_signature(q_labels), layers, len(middle_union), missing)
        return
    if args.exhaust_other:
        q_labels = OTHER_Q_CERTIFICATES[args.exhaust_index - 1]
        assert atom_obstruction(q_labels) is None
        heavy, tables, unary, levels, closure, solutions = exhaust_t_for_base(q_labels)
        print("OTHER B certificate index:", args.exhaust_index)
        print("OTHER B signature:", q_signature(q_labels))
        layers, middle_union = middle_spectrum((Q_NORMAL,) * 3 + q_labels)
        print("OTHER B middle layer support sizes:", layers)
        print("OTHER B middle nonzero union:", len(middle_union))
        print("OTHER B heavy fibres:", heavy)
        print("OTHER B forbidden counts:", {
            str(value): {size: len(sums) for size, sums in sorted(tables[value].items())}
            for value in heavy
        })
        print("OTHER B unary labels:", len(unary))
        print("OTHER B prefix levels:", levels)
        print("OTHER B closure:", closure)
        print("OTHER B medium survivors:", solutions)
        return
    old_signature, reports = audit_frozen_certificates()
    print("PASS old fixed-B signature kept separate:", old_signature)
    for index, (signature, layers, missing, escape, tail_count) in enumerate(reports, 1):
        print(f"PASS other-B certificate {index} atom; signature:", signature)
        print("  |Sigma_k(B)| for k=8,9,10,11:", layers)
        print("  missing nonzero middle sums:", missing)
        print("  allowed T singleton support after middle gap:", escape)
        print("  zero-sum T multisets on escape support:", tail_count)
    print(
        "CERTIFIED: three pairwise inequivalent other-B orbits have no "
        "admissible full-position extension"
    )
    print("SCOPE: fixed certificates only; multiplicity partitions are not classified")
    print("STATUS: PROVED fixed-skeleton exclusions / global p=7,m=3 INCOMPLETE")


if __name__ == "__main__":
    main()
