#!/usr/bin/env python3
"""Recoverable layered search for the p=7,m=4,0001,s=6 CSP.

The full 68-free-scalar slice is too large for a flat enumeration.  This
program therefore exposes exact monotone layers.  Its certified default
search exhausts the radius-two equal-sum pair-mutation neighbourhood of the
frozen length-19 quotient atom.  Every quotient atom in that neighbourhood
which can carry a distinguished four-fold fibre is tested against

* the fixed-B quotient atom condition (by the atom test itself),
* the full p=7 middle gap for every one-, two-, and three-position T subset,
* in fact the same induced gap test for every proper T subset of size 1..5,
* the 0001 quotient-trace windows, and
* sum(T)=0 up to S_6 permutation.

Only a quotient survivor is eligible for the height/Hasse/actual-atom layer.
Complete assignments can be sent through ``--instance`` to the existing
position-level auditor, which reconstructs every length-2--8 block, rejects
lengths 9--12, and checks Hasse/intersection/actual-Z/all-F3-complement
constraints.  Thus no weak layer is ever reported as a complete candidate.

The neighbourhood theorem is finite and exact.  It is not a classification
of all length-19 atoms and not a proof of the whole 68-scalar slice.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Sequence

import p7_length19_pair_mutation_frontier as MUT
import verify_p7_m4_next_csp as FULL


P = 7
ZERO = (0, 0, 0)
ALL = MUT.ALL
ALL_NONZERO = MUT.ALL_NONZERO
BASE_B = MUT.BASE_B


def add(left: tuple[int, int, int], right: tuple[int, int, int]):
    return tuple((left[i] + right[i]) % P for i in range(3))


def neg(value: tuple[int, int, int]):
    return tuple((-entry) % P for entry in value)


def total(values: Iterable[tuple[int, int, int]]):
    answer = ZERO
    for value in values:
        answer = add(answer, value)
    return answer


def canonical_payload(collection: Iterable[Sequence[tuple[int, int, int]]]):
    serial = [[list(value) for value in sequence] for sequence in sorted(collection)]
    return json.dumps(serial, separators=(",", ":")).encode("ascii")


def digest(collection: Iterable[Sequence[tuple[int, int, int]]]):
    return hashlib.sha256(canonical_payload(collection)).hexdigest()


def pair_mutation_candidates(atom: Sequence[tuple[int, int, int]]):
    """All distinct nontrivial equal-sum two-position replacements.

    Positions are used when deleting.  Replacement labels may be zero at
    this stage; the exact atom test subsequently rejects them.  This matches
    the already audited one-step generator.
    """
    atom = tuple(atom)
    answer = set()
    for left, right in combinations(range(len(atom)), 2):
        target = add(atom[left], atom[right])
        remainder = [
            value for index, value in enumerate(atom) if index not in (left, right)
        ]
        for first in ALL:
            second = add(target, neg(first))
            candidate = tuple(sorted((*remainder, first, second)))
            if candidate != atom:
                answer.add(candidate)
    return answer


def supports_through_15(atom):
    return MUT.fixed_size_supports(atom, 15)


def forbidden_T_sum_tables(atom):
    """Compile all B-internal witnesses which extend a T subset into [9,16].

    For a T subset U of size r, 1<=r<=5, a B subset W would make a
    forbidden quotient-zero set precisely when |W| is in [9-r,16-r] and
    sum(W)=-sum(U).  The returned set stores the forbidden value sum(U).
    """
    supports = supports_through_15(atom)
    tables = {}
    for t_size in range(1, 6):
        lower = 9 - t_size
        upper = 16 - t_size
        b_sums = frozenset().union(*(supports[size] for size in range(lower, upper + 1)))
        tables[t_size] = frozenset(neg(value) for value in b_sums)
    return tables, supports


def trace_window_ok(q, subset: Sequence[tuple[int, int, int]]):
    """Height-free 0001 quotient restrictions for an s=6 T."""
    size = len(subset)
    value = total(subset)
    if size == 1:
        # Global (13), plus its s=6 complement consequence (14).
        return value not in (neg(q), add(neg(q), neg(q)), add(q, add(q, q)))
    if size == 2:
        return value != neg(q)
    return True


def incremental_T_ok(prefix, label, forbidden, q):
    extended = prefix + (label,)
    for size in range(1, min(5, len(extended)) + 1):
        for old in combinations(prefix, size - 1):
            subset = old + (label,)
            value = total(subset)
            if value in forbidden[size]:
                return False
            if size <= 2 and not trace_window_ok(q, subset):
                return False
    return True


def enumerate_T_multisets(atom, q, forbidden):
    """Exhaust S_6-orbits after all proper-subset middle-gap tests."""
    unary = tuple(
        value
        for value in ALL_NONZERO
        if incremental_T_ok((), value, forbidden, q)
    )
    index = {value: i for i, value in enumerate(unary)}
    levels = [1, 0, 0, 0, 0, 0]
    closure = Counter()
    survivors = []

    def walk(prefix, start, subtotal):
        if len(prefix) == 5:
            closure["prefixes"] += 1
            last = neg(subtotal)
            last_index = index.get(last)
            if last_index is None:
                closure["last_not_unary"] += 1
                return
            if last_index < start:
                closure["last_breaks_order"] += 1
                return
            if not incremental_T_ok(prefix, last, forbidden, q):
                closure["last_propagation"] += 1
                return
            completed = prefix + (last,)
            assert total(completed) == ZERO
            survivors.append(completed)
            return
        for i in range(start, len(unary)):
            value = unary[i]
            if not incremental_T_ok(prefix, value, forbidden, q):
                continue
            levels[len(prefix) + 1] += 1
            walk(prefix + (value,), i, add(subtotal, value))

    walk((), 0, ZERO)
    return unary, tuple(levels), dict(closure), tuple(survivors)


def pointed_four_fibres(atom):
    counts = Counter(atom)
    if max(counts.values()) > 4:
        return ()
    return tuple(sorted(value for value, count in counts.items() if count == 4))


def exact_neighbourhood(max_depth: int):
    """Return atoms by exact graph distance and candidate statistics."""
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    seen = {tuple(sorted(BASE_B))}
    frontier = {tuple(sorted(BASE_B))}
    by_depth = [tuple(sorted(frontier))]
    candidate_counts = []
    candidate_hashes = []
    for _depth in range(1, max_depth + 1):
        candidates = set()
        for atom in sorted(frontier):
            candidates.update(pair_mutation_candidates(atom))
        candidate_counts.append(len(candidates))
        candidate_hashes.append(digest(candidates))
        new_atoms = {
            candidate
            for candidate in candidates
            if candidate not in seen and MUT.is_length_19_atom(candidate)
        }
        seen.update(new_atoms)
        frontier = new_atoms
        by_depth.append(tuple(sorted(frontier)))
    return tuple(by_depth), tuple(candidate_counts), tuple(candidate_hashes)


def analyse_atoms(by_depth):
    pointed = []
    for depth, atoms in enumerate(by_depth):
        for atom in atoms:
            q_values = pointed_four_fibres(atom)
            if not q_values:
                continue
            forbidden, supports = forbidden_T_sum_tables(atom)
            single_escape = tuple(
                value for value in ALL_NONZERO if value not in forbidden[1]
            )
            layer_sizes = tuple(len(supports[size]) for size in range(4, 16))
            for q in q_values:
                unary, levels, closure, tails = enumerate_T_multisets(
                    atom, q, forbidden
                )
                pointed.append(
                    {
                        "depth": depth,
                        "atom": atom,
                        "q": q,
                        "signature": tuple(
                            sorted(Counter(atom).values(), reverse=True)
                        ),
                        "sigma_4_15_sizes": layer_sizes,
                        "single_escape": single_escape,
                        "unary_after_0001": unary,
                        "prefix_levels": levels,
                        "closure": closure,
                        "T_survivors": tails,
                    }
                )
    return tuple(pointed)


def jsonable(value):
    if isinstance(value, tuple):
        return [jsonable(item) for item in value]
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    return value


def write_report(path: Path, report):
    payload = json.dumps(jsonable(report), ensure_ascii=False, indent=2, sort_keys=True)
    # Pin LF bytes on Windows so the printed digest is the digest of the
    # actual certificate file rather than of a pre-translation string.
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_existing_full_instance(path: Path):
    instance = FULL.parse_instance(path)
    report = FULL.audit_instance(instance)
    informational = {
        "block_counts",
        "trace_counts",
        "tail_star_counts",
        "full_F3_tail_counts",
        "lower_F3_tail_counts",
    }
    bad = {
        key: value
        for key, value in report.items()
        if key not in informational and value
    }
    return report, bad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--instance", type=Path)
    args = parser.parse_args()

    if args.instance is not None:
        report, bad = audit_existing_full_instance(args.instance)
        print(json.dumps(jsonable(report), ensure_ascii=False, indent=2))
        if bad:
            raise SystemExit("REJECTED by the complete 25-position CSP layer")
        print("ACCEPTED by the complete 25-position CSP layer")
        return

    by_depth, candidate_counts, candidate_hashes = exact_neighbourhood(args.max_depth)
    # The depth-one layer must reproduce the independent frozen computation.
    if args.max_depth >= 1:
        assert candidate_counts[0] == MUT.EXPECTED_CANDIDATES
        assert candidate_hashes[0] == MUT.EXPECTED_CANDIDATE_SHA256
        assert set(by_depth[1]) == set(MUT.FROZEN_ATOMS)

    pointed = analyse_atoms(by_depth)
    survivors = [item for item in pointed if item["T_survivors"]]
    report = {
        "schema": "p7-m4-0001-s6-layered-v1",
        "max_depth": args.max_depth,
        "base_atom_sha256": digest((tuple(sorted(BASE_B)),)),
        "atom_counts_by_exact_depth": tuple(len(layer) for layer in by_depth),
        "atom_sha256_by_exact_depth": tuple(digest(layer) for layer in by_depth),
        "candidate_counts_by_expansion": candidate_counts,
        "candidate_sha256_by_expansion": candidate_hashes,
        "pointed_four_fibre_branches": len(pointed),
        "pointed_branch_sha256": hashlib.sha256(
            json.dumps(jsonable(pointed), separators=(",", ":"), sort_keys=True).encode(
                "ascii"
            )
        ).hexdigest(),
        "quotient_survivor_count": len(survivors),
        "survivors": survivors,
        "pointed": pointed,
        "scope": (
            "exact radius-N equal-sum pair-mutation neighbourhood; "
            "not all length-19 atoms and not the whole 68-scalar slice"
        ),
    }
    print("EXACT ATOMS BY DEPTH:", report["atom_counts_by_exact_depth"])
    print("EXPANSION CANDIDATE COUNTS:", candidate_counts)
    print("POINTED MAX-FIBRE-FOUR BRANCHES:", len(pointed))
    print("QUOTIENT T SURVIVORS AFTER ALL 1..5 SUBSET GAP TESTS:", len(survivors))
    print("POINTED-BRANCH SHA256:", report["pointed_branch_sha256"])
    if args.report is not None:
        report_hash = write_report(args.report, report)
        print("REPORT:", args.report)
        print("REPORT SHA256:", report_hash)
    print("STATUS: exact layered neighbourhood classification; global slice incomplete")


if __name__ == "__main__":
    main()
