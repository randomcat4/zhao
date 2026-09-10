#!/usr/bin/env python3
"""Independent arithmetic and certificate checks for the collinear search.

The verifier does not reuse the searcher's profile generator or its closed
forms for the S3 action.  It rebuilds both from elementary multiset choices
and two-dimensional changes of basis, then audits every frozen report row and
the exact L1/L2/L3 subset-sum interface.  ``--replay`` additionally reruns the
expensive full search.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

import p7_length19_support7_escape_search as FAST
import p7_support9_collinear_real_search as SEARCH


P = 7
ZERO_ID = FAST.ZERO_ID
REPORTS = {
    1: (
        "p7_support9_collinear_real_sig1_report.json",
        "01a9dbe03f381de8164f5a7a4a40a526cff684242bc655a6fb4170cfbc954505",
        "367170e0ecd77967318c24e341cbfcaddd8f76fa69731b4ee39e43d190967dbf",
    ),
    2: (
        "p7_support9_collinear_real_sig2_report.json",
        "c655c8b571e17141aaa7dc4bf439b7277e96e82f328a261cde7363025352ff86",
        "67724ed94c1ff1b635a2cf42b884e4246ad5a272f6d18172b7fcb1a667a7a47d",
    ),
    3: (
        "p7_support9_collinear_real_sig3_report.json",
        "2d7bfacfb46a20b3cc8501b45575c326e23102c3a4c8f9e13cf9d98a6df2df57",
        "873d5d25cf596846fb6976f6e4533626b70481b41c879d0ddb0ab32b66ad9d0f",
    ),
    4: (
        "p7_support9_collinear_real_sig4_report.json",
        "cbdd160451f8ac9cf98573792c69bdb804c14bd1d73c91968b37feb3dacca87a",
        "9a4b9eb28e714e5a82dfd574c7a832291b81cef4ecdc525e360fe87d109e589f",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_profiles(signature):
    """Rebuild the raw collinear profile denominator without OLD helpers."""
    signature = tuple(signature)
    answer = set()
    for triple_indices in combinations(range(9), 3):
        triple = tuple(sorted((signature[i] for i in triple_indices), reverse=True))
        remainder = list(signature)
        for multiplicity in triple:
            remainder.remove(multiplicity)
        for outside in sorted(set(remainder), reverse=True):
            tail = remainder.copy()
            tail.remove(outside)
            for ordered_tail in set(permutations(tail)):
                answer.add(triple + (outside,) + ordered_tail)
    return tuple(sorted(answer, reverse=True))


def add2(left, right):
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def scale2(coefficient, value):
    return ((coefficient * value[0]) % P, (coefficient * value[1]) % P)


def det2(left, right):
    return (left[0] * right[1] - left[1] * right[0]) % P


def coordinates2(first, second, value):
    determinant = det2(first, second)
    assert determinant
    inverse = pow(determinant, -1, P)
    return (
        (value[0] * second[1] - value[1] * second[0]) * inverse % P,
        (first[0] * value[1] - first[1] * value[0]) * inverse % P,
    )


def independent_c_orbits(weights):
    """Compute orbits by explicit weighted point permutations and bases."""
    universe = {(u, v) for u in range(1, P) for v in range(1, P)}
    unseen = set(universe)
    answer = []
    for seed in sorted(universe):
        if seed not in unseen:
            continue
        points = ((1, 0), (0, 1), seed)
        orbit = set()
        for order in permutations(range(3)):
            if tuple(weights[index] for index in order) != tuple(weights):
                continue
            first, second, third = (points[index] for index in order)
            image = coordinates2(first, second, third)
            assert image in universe
            orbit.add(image)
        unseen -= orbit
        answer.append(tuple(sorted(orbit)))
    assert not unseen
    return tuple(answer)


def direct_fixed_sums(labels, multiplicities):
    sums = set()
    zero_relation = False
    for coefficients in product(*(range(m + 1) for m in multiplicities)):
        if not any(coefficients):
            continue
        subtotal = ZERO_ID
        for label, coefficient in zip(labels, coefficients):
            subtotal = FAST.add_id(subtotal, FAST.SCALE_ID[label][coefficient])
        sums.add(FAST.NEG_ID[subtotal])
        zero_relation |= subtotal == ZERO_ID
    return sums, zero_relation


def direct_position_sums(labels, size):
    answer = set()
    for indices in combinations(range(len(labels)), size):
        subtotal = ZERO_ID
        for index in indices:
            subtotal = FAST.add_id(subtotal, labels[index])
        answer.add(subtotal)
    return answer


def audit_local_arithmetic():
    c_values = tuple(
        FAST.vector_id((u, v, 0))
        for u in range(1, P)
        for v in range(1, P)
    )
    for c_id in c_values:
        labels = (FAST.Q_ID, FAST.E2_ID, FAST.E3_ID, c_id)
        for multiplicities in ((1, 1, 1, 1), (3, 2, 1, 3), (4, 4, 2, 1)):
            expected, expected_zero = direct_fixed_sums(labels, multiplicities)
            packed, actual_zero = SEARCH.fixed_forbidden_mask(labels, multiplicities)
            assert set(FAST.mask_ids(packed)) == expected
            assert actual_zero == expected_zero

    probes = (
        (FAST.Q_ID, FAST.E2_ID, FAST.E3_ID),
        (FAST.Q_ID, FAST.Q_ID, FAST.E2_ID, FAST.E3_ID),
        (FAST.vector_id((1, 1, 0)), FAST.vector_id((2, 3, 1)), FAST.E3_ID),
    )
    for labels in probes:
        layers = SEARCH.position_layers(labels, len(labels))
        for size in range(len(labels) + 1):
            assert set(FAST.mask_ids(layers[size])) == direct_position_sums(labels, size)

    # Directly compare the three conditioned rows with the compiled masks.
    labels = tuple(
        FAST.vector_id(value)
        for value in (
            (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 1), (2, 3, 1), (4, 1, 2), (3, 5, 6),
            (6, 2, 4), (5, 6, 3), (2, 1, 5), (4, 4, 1),
            (1, 5, 2), (6, 3, 2), (3, 2, 6), (5, 1, 4),
        )
    )
    layers = SEARCH.position_layers(labels, 15)
    forbidden = SEARCH.tail_forbidden_masks(layers)
    for tail_size in (1, 2, 3):
        direct = set()
        for b_size in range(9 - tail_size, 17 - tail_size):
            direct.update(FAST.NEG_ID[value] for value in direct_position_sums(labels, b_size))
        assert set(FAST.mask_ids(forbidden[tail_size])) == direct


def audit_profiles_and_symmetry():
    for signature, expected_count in zip(
        SEARCH.TARGET_SIGNATURES, SEARCH.EXPECTED_PROFILE_COUNTS
    ):
        independent = independent_profiles(signature)
        assert len(independent) == expected_count
        assert set(independent) == set(SEARCH.profiles_for_signature(signature))
    for weights in ((3, 3, 3), (3, 3, 1), (3, 2, 1)):
        independent = independent_c_orbits(weights)
        direct = SEARCH.c_orbits(*weights)
        assert {frozenset(orbit) for orbit in independent} == {
            frozenset(orbit) for orbit in direct
        }
    assert sorted(map(len, independent_c_orbits((3, 3, 3)))) == [1, 2, 3, 3, 3, 3, 3, 6, 6, 6]


def audit_report(root: Path, signature_index: int, specification):
    name, expected_file_hash, expected_profile_hash = specification
    path = root / name
    assert sha256(path) == expected_file_hash
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["schema"] == "p7-support9-collinear-real-v1"
    assert report["full_signature"] is True
    assert report["c_symmetry_mode"] == "full-signature-S3-closure"
    assert report["signature_index"] == signature_index
    assert tuple(report["signature"]) == SEARCH.TARGET_SIGNATURES[signature_index - 1]
    assert report["signature_profile_denominator"] == SEARCH.EXPECTED_PROFILE_COUNTS[signature_index - 1]
    assert report["completed_profile_interval"] == [1, report["signature_profile_denominator"]]
    assert report["profile_count"] == report["signature_profile_denominator"]
    assert report["profile_report_sha256"] == expected_profile_hash
    assert report["exact_tail_survivor_count"] == len(report["position_reports"])

    aggregate = Counter()
    profile_hasher = hashlib.sha256()
    for profile in report["profiles"]:
        assert profile["c_symmetry_mode"] == "full-signature-S3-closure"
        counts = profile["counts"]
        assert counts["raw_collinear_c_frames"] == 36
        assert counts["collinear_c_entered"] == counts["collinear_c_orbits"]
        for depth in range(1, 5):
            entered = counts.get(f"depth{depth}_entered", 0)
            rejected = sum(
                counts.get(f"depth{depth}_{reason}", 0)
                for reason in ("atomic_pruned", "plane_pruned", "tail_pruned")
            )
            survived = counts.get(f"depth{depth}_survived", 0)
            assert entered == rejected + survived
        aggregate.update(counts)
        serial = json.dumps(profile, sort_keys=True, separators=(",", ":"))
        profile_hasher.update(serial.encode("ascii"))
    assert dict(sorted(aggregate.items())) == report["aggregate"]
    assert profile_hasher.hexdigest() == expected_profile_hash
    assert report["exact_tail_survivor_sha256"] == SEARCH.payload_digest(report["position_reports"])
    return report


def replay(root: Path, signature_indices):
    for signature_index in signature_indices:
        name, expected_hash, _profile_hash = REPORTS[signature_index]
        temporary = root / (Path(name).stem + "_replay.json")
        subprocess.run(
            [
                sys.executable,
                str(root / "p7_support9_collinear_real_search.py"),
                "--signature", str(signature_index),
                "--prefix-tail-depth", "2",
                "--quiet", "--skip-self-test",
                "--report", str(temporary),
            ],
            check=True,
            cwd=root,
        )
        assert sha256(temporary) == expected_hash
        temporary.unlink()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    audit_local_arithmetic()
    audit_profiles_and_symmetry()
    reports = [audit_report(root, index, specification) for index, specification in sorted(REPORTS.items())]
    if args.replay:
        replay(root, sorted(REPORTS))
    print("PASS independent collinear profile denominators:", tuple(report["profile_count"] for report in reports))
    print("PASS explicit weighted-S3 change-of-basis orbits")
    print("PASS fixed-part, position-layer, and L1/L2/L3 differentials")
    print("PASS frozen report hashes and per-depth conservation")
    if args.replay:
        print("PASS full deterministic replay")
    print("STATUS: exact listed finite signatures only; global support-nine and A_p incomplete")


if __name__ == "__main__":
    main()
