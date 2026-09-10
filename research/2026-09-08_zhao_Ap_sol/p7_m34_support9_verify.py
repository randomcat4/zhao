#!/usr/bin/env python3
"""Verify and merge the two support-nine light-signature shards."""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from pathlib import Path

import p7_length19_support7_escape_search as FAST
import p7_m34_support9_search as SEARCH
import p7_plane_projective_zero_sum_free as PLANE


SHARDS = (
    (
        "p7_m34_support9_m3_light_report.json",
        "ca874fd34041a1f1de45d8136d4b1ade3cbd19f1ca31d93f078c906ae71f1fce",
        (3, 1, 1),
    ),
    (
        "p7_m34_support9_m4_light_report.json",
        "66cf710bb2d5fd7b0ca2cd13e96b7bdd49dfa8d20a8f7185712d8e45a84bd4bf",
        (4, 1, 7),
    ),
)
EXPECTED_PLANE_MAXIMUM = 11
EXPECTED_PLANE_WITNESS_SHA256 = "699d7242e87d63d8246bd36225b7c65fb9e0bb2148fed3b75d7df00ce222157e"
EXPECTED_UNIFIED_SHA256 = "de0ccf6ba3a0c44b49437f030ef952e8f6a34a8fa098366b3f861f95536fa4f1"


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recursive_profiles(anchor: int):
    answer = []

    def visit(prefix, remaining):
        if len(prefix) == 8:
            if remaining == 0 and prefix[0] == max(prefix):
                answer.append(tuple(prefix))
            return
        slots = 8 - len(prefix)
        for value in range(1, anchor + 1):
            next_remaining = remaining - value
            if slots - 1 <= next_remaining <= anchor * (slots - 1):
                visit(prefix + [value], next_remaining)

    visit([], 19 - anchor)
    return tuple(answer)


def profile_stream_digest(profiles):
    hasher = hashlib.sha256()
    for profile in profiles:
        serial = json.dumps(profile, sort_keys=True, separators=(",", ":"), default=list)
        hasher.update(serial.encode("ascii"))
    return hasher.hexdigest()


def rank_over_f2(rows):
    rows = list(rows)
    rank = 0
    for column in range(57):
        pivot = next(
            (index for index in range(rank, len(rows)) if (rows[index] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for index in range(len(rows)):
            if index != rank and (rows[index] >> column) & 1:
                rows[index] ^= rows[rank]
        rank += 1
    return rank


def verify_incidence_rank():
    rows = []
    for normal in SEARCH.PROJECTIVE_POINTS:
        mask = 0
        for point_index, point in enumerate(SEARCH.PROJECTIVE_POINTS):
            if sum(normal[i] * point[i] for i in range(3)) % 7 == 0:
                mask |= 1 << point_index
        assert mask.bit_count() == 8
        rows.append(mask)
    assert rank_over_f2(rows) == 56
    all_points = (1 << 57) - 1
    assert all((row & all_points).bit_count() % 2 == 0 for row in rows)


def verify_plane_frontier():
    records = []
    maximum = -1
    witnesses = []
    for m1 in range(1, 5):
        for m2 in range(1, 5):
            length, witness, cache = PLANE.solve_for_basis_multiplicities(m1, m2)
            assert PLANE.direct_zero_sum_free(witness)
            record = {
                "basis_multiplicities": [m1, m2],
                "maximum_length": length,
                "witness": [list(item) for item in witness],
                "cache_misses": cache.misses,
            }
            records.append(record)
            if length > maximum:
                maximum = length
                witnesses = [record]
            elif length == maximum:
                witnesses.append(record)
    payload = json.dumps(witnesses, sort_keys=True, separators=(",", ":")).encode("ascii")
    assert maximum == EXPECTED_PLANE_MAXIMUM
    assert hashlib.sha256(payload).hexdigest() == EXPECTED_PLANE_WITNESS_SHA256
    return records


def verify_local_interfaces():
    rng = random.Random(0x349)
    for _ in range(256):
        chosen_lines = rng.sample(SEARCH.PROJECTIVE_POINTS, rng.randrange(1, 10))
        chosen_ids = []
        for line in chosen_lines:
            scalar = rng.randrange(1, 7)
            value = FAST.scale_value(scalar, line)
            chosen_ids.append(FAST.vector_id(value))
        multiplicities = [rng.randrange(1, 5) for _ in chosen_ids]
        packed = 0
        rejected = False
        for value_id, multiplicity in zip(chosen_ids, multiplicities):
            packed = SEARCH.add_plane_weight(packed, value_id, multiplicity)
            if packed is None:
                rejected = True
                break
        direct_maximum = max(
            sum(
                multiplicity
                for value_id, multiplicity in zip(chosen_ids, multiplicities)
                if plane_index in SEARCH.PLANES_CONTAINING[value_id]
            )
            for plane_index in range(57)
        )
        assert rejected == (direct_maximum > SEARCH.PLANE_WEIGHT_CAP)

    for _ in range(256):
        allowed = tuple(sorted(rng.sample(range(1, 343), rng.randrange(0, 10))))
        mask = sum(1 << value_id for value_id in allowed)
        direct = FAST.zero_sum_tail_multiset_count(allowed) > 0
        assert SEARCH.six_tail_possible_mask(mask) == direct


def main():
    root = Path(__file__).resolve().parent
    assert tuple(len(recursive_profiles(anchor)) for anchor in (3, 4)) == (358, 476)
    assert recursive_profiles(3) == SEARCH.normalized_profiles(3)
    assert recursive_profiles(4) == SEARCH.normalized_profiles(4)
    assert len(SEARCH.unpointed_signatures()) == 13
    collinear = SEARCH.collinear_multiplicity_profiles()
    assert len(collinear) == 5_741
    light_signatures = {
        (3,) + (2,) * 8,
        (4,) + (2,) * 7 + (1,),
    }
    assert sum(profile[0] in light_signatures for profile in collinear) == 50

    verify_incidence_rank()
    plane_records = verify_plane_frontier()
    verify_local_interfaces()

    reports = []
    profile_reports = []
    aggregate = Counter()
    for name, expected_hash, shard_key in SHARDS:
        path = root / name
        assert sha256(path) == expected_hash
        report = json.loads(path.read_text(encoding="utf-8"))
        assert report["schema"] == "p7-m34-support9-frontier-v1"
        assert report["prefix_tail_depth"] == 3
        jobs = tuple(tuple(job[:2]) for job in report["jobs"])
        assert jobs == tuple(
            (shard_key[0], index)
            for index in range(shard_key[1], shard_key[2] + 1)
        )
        expected = SEARCH.EXPECTED_LIGHT_SHARDS[shard_key]
        assert report["aggregate"] == expected["aggregate"]
        assert report["profile_report_sha256"] == expected["profile_report_sha256"]
        assert report["tail_viable_unpointed_orbits"] == 0
        assert report["tail_viable_orbit_sha256"] == SEARCH.EXPECTED_EMPTY_SHA256
        assert not report["tail_viable_orbits"]
        assert profile_stream_digest(report["profiles"]) == report["profile_report_sha256"]
        reports.append(report)
        profile_reports.extend(report["profiles"])
        aggregate.update(report["aggregate"])

    assert len(profile_reports) == 8
    assert {tuple(profile["signature"]) for profile in profile_reports} == light_signatures
    assert aggregate["tail_viable_atoms"] == 0
    assert aggregate["complete_zero_sum_candidates"] == 2
    assert aggregate["complete_empty_escape_pruned"] == 2

    result = {
        "schema": "p7-m34-support9-light-unified-v1",
        "scope": "complete two-signature light slice; full support nine incomplete",
        "closed_signatures": tuple(sorted(light_signatures)),
        "anchor_profile_denominator": 834,
        "closed_anchor_profiles": 8,
        "remaining_anchor_profiles": 826,
        "unpointed_signature_denominator": 13,
        "closed_signatures_count": 2,
        "remaining_signatures_count": 11,
        "collinear_profile_denominator": 5_741,
        "closed_collinear_profiles": 50,
        "remaining_collinear_profiles": 5_691,
        "profile_count": len(profile_reports),
        "aggregate": dict(sorted(aggregate.items())),
        "profile_report_sha256": profile_stream_digest(profile_reports),
        "tail_viable_unpointed_orbits": 0,
        "tail_viable_orbit_sha256": SEARCH.EXPECTED_EMPTY_SHA256,
        "plane_maximum": EXPECTED_PLANE_MAXIMUM,
        "plane_witness_sha256": EXPECTED_PLANE_WITNESS_SHA256,
        "incidence_rank_mod_two": 56,
        "shard_sha256": tuple(expected for _name, expected, _key in SHARDS),
        "profiles": profile_reports,
        "plane_records": plane_records,
    }
    output = root / "p7_m34_support9_light_unified_report.json"
    serial = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, default=list)
    output.write_text(serial + "\n", encoding="utf-8", newline="\n")
    digest = sha256(output)
    if EXPECTED_UNIFIED_SHA256:
        assert digest == EXPECTED_UNIFIED_SHA256
    print("PASS independent recursive anchor profiles: 358+476=834")
    print("PASS two complete light signatures: 1+7 anchor profiles")
    print("PASS plane cap 11 finite frontier and packed-weight differentials")
    print("PASS exact six-tail sumset differentials")
    print("PASS PG(2,7) incidence rank 56 and 5,741 collinear profiles")
    print("AGGREGATE", json.dumps(result["aggregate"], separators=(",", ":")))
    print("PROFILE REPORT SHA256:", result["profile_report_sha256"])
    print("UNIFIED REPORT SHA256:", digest)
    print("STATUS: two signatures closed; eleven support-nine signatures remain")


if __name__ == "__main__":
    main()
