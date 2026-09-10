#!/usr/bin/env python3
"""Merge and independently replay the p7_m4_full68 support-eight shards."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import p7_m4_68_layered_solver as LAYERED
import p7_m4_full68_short_support_search as SEARCH
import p7_m4_full68_support8_search as SUPPORT8
import verify_p7_maximal_atom_escape_algebra as ALGEBRA


SHARDS = (
    ("p7_m4_full68_support8_s1_1_15_report.json", "e4d34a518a239d0abd1ff20c05f30023493cef0f43ecc13e32eebdb29f232da1"),
    ("p7_m4_full68_support8_s1_16_30_report.json", "dd059cdcc58f353345ede4f39b1850dba4787a70989133ca65b28bd352563a98"),
    ("p7_m4_full68_support8_s1_31_31_report.json", "2ac486855082809b166ddcf70d890a346dcdf9193d7bc179df99b586c631c18c"),
    ("p7_m4_full68_support8_s1_32_32_report.json", "fe2f787a89cf26421266c2f887950b39db6d7677b3dc7b0ad980867678c3d5ad"),
    ("p7_m4_full68_support8_s1_33_33_report.json", "2a7776fcffd696b06f6214045053421781ab302f00f2751a320cd44b8a43d991"),
    ("p7_m4_full68_support8_s1_34_34_report.json", "0c734eb98cf13c35ca4917e02af625cc884d53302f4a5d72e8674118623b1fe0"),
    ("p7_m4_full68_support8_s1_35_35_report.json", "363754dbadf183bcf6d8a8b60daf941e77de75e263af4eb773aca970ed5c6128"),
    ("p7_m4_full68_support8_s1_36_40_report.json", "8422f6af865fc4dca509ffcec3cdaf64905d685da335dca05f2f24ed23c28eda"),
    ("p7_m4_full68_support8_s1_41_45_report.json", "b6964b9d4a26c8e38eab12c6a0f69678b630bb9c14fbf954fb599073e9038d4c"),
    ("p7_m4_full68_support8_s1_46_60_report.json", "49ed14264c24540806613d283d251b0867a8f25b9dd510992192359ad7c3ea33"),
    ("p7_m4_full68_support8_s2_1_6_report.json", "c9588dc8892bcfd5c55cb3ada4d99183a6cee84ffb93fc0cf7ac6016c32c16bb"),
)

EXPECTED_AGGREGATE = {
    "ordered_prefix_nodes": 349_910_371,
    "atomic_prefix_pruned": 336_630_802,
    "escape_prefix_pruned": 0,
    "forced_last_rejected": 7_152_580,
    "final_zero_sum_candidates": 224_101,
    "final_escape_pruned": 210_468,
    "final_nonatoms": 13_630,
    "target_atom_hits": 3,
    "target_with_T_survivor": 0,
}
EXPECTED_PROFILES_SHA256 = "89cd3ce9003efe4cdf5265fac0afb9a7d539a912884b9a6b7f537ab34b502177"
EXPECTED_HIT_SHA256 = "20a112d9a299524d888855c9e8ff1da4dac33e3379fd7e4aaea55bf9a36f1f13"
EXPECTED_DIRECT_HIT_SHA256 = "696dc6aaf5ed680b9b8011ea5bfa7801ba22c1325502d9397c008e091532c23d"
EXPECTED_ORBIT_SHA256 = "38e581cb067ca585fe27173e6b75bf8b4f4dbe102716f4195dc5e1f030d70993"
# Updated after adding the explicitly conditional exact-three splice metadata.
EXPECTED_REPORT_SHA256 = "2527c44f0ae8285c03de232a39c51a866dc208207aeaa538825e54d6f1fd6160"


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tupleize(value):
    if isinstance(value, list):
        return tuple(tupleize(item) for item in value)
    if isinstance(value, dict):
        return {key: tupleize(item) for key, item in value.items()}
    return value


def write_report(path: Path, result):
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload + "\n")
    return sha256(path)


def main():
    root = Path(__file__).resolve().parent
    reports = []
    for name, expected in SHARDS:
        path = root / name
        assert sha256(path) == expected
        report = json.loads(path.read_text(encoding="utf-8"))
        assert report["schema"] == "p7-m4-full68-support8-v1"
        assert report["hit_sha256"] == SEARCH.payload_digest(report["hits"])
        assert report["profiles_sha256"] == SEARCH.payload_digest(report["profiles"])
        reports.append(report)

    profile_reports = []
    hits = []
    for report in reports:
        profile_reports.extend(report["profiles"])
        hits.extend(report["hits"])
    profile_reports.sort(
        key=lambda item: (
            SUPPORT8.SIGNATURES.index(tuple(item["signature"])),
            item["profile_index"],
        )
    )
    expected_pairs = tuple(
        (signature, index, profile)
        for signature in SUPPORT8.SIGNATURES
        for index, profile in enumerate(SEARCH.profile_list(signature), 1)
    )
    actual_pairs = tuple(
        (tuple(item["signature"]), item["profile_index"], tuple(item["profile"]))
        for item in profile_reports
    )
    assert actual_pairs == expected_pairs
    assert len(actual_pairs) == len(set(actual_pairs)) == 66

    counter_keys = tuple(SEARCH.empty_counters())
    aggregate = {
        key: sum(item[key] for item in profile_reports) for key in counter_keys
    }
    for item in profile_reports:
        assert item["final_zero_sum_candidates"] == (
            item["final_escape_pruned"]
            + item["final_nonatoms"]
            + item["target_atom_hits"]
        )
        assert item["target_with_T_survivor"] <= item["target_atom_hits"]
    assert aggregate["target_atom_hits"] == len(hits)

    direct_hits = []
    orbit_groups = defaultdict(list)
    for hit in hits:
        atom_ids = tuple(hit["atom_ids"])
        labels = tuple(ALGEBRA.VECTORS[value_id] for value_id in atom_ids)
        signature = tuple(sorted(Counter(atom_ids).values(), reverse=True))
        assert signature in SUPPORT8.SIGNATURES
        assert len(atom_ids) == 19 and len(set(atom_ids)) == 8
        assert Counter(atom_ids)[SEARCH.Q_ID] == 4
        assert max(Counter(atom_ids).values()) == 4
        assert ALGEBRA.total(labels) == ALGEBRA.ZERO
        assert ALGEBRA.is_projectively_simple(labels)
        assert ALGEBRA.is_atom_by_position_dp(labels)

        escape = tuple(ALGEBRA.VECTOR_ID[value] for value in ALGEBRA.escape_values(labels))
        assert escape == tuple(hit["escape_ids"])
        zero_sum_tail_count = SEARCH.BASE.zero_sum_tail_multiset_count(escape)
        forbidden, _ = LAYERED.forbidden_T_sum_tables(labels)
        unary, levels, closure, tails = LAYERED.enumerate_T_multisets(
            labels, SEARCH.VECTORS[SEARCH.Q_ID], forbidden
        )
        unary_ids = tuple(ALGEBRA.VECTOR_ID[value] for value in unary)
        assert unary_ids == tuple(hit["unary_after_0001_ids"])
        assert tuple(levels) == tuple(hit["prefix_levels"])
        assert closure == hit["closure"]
        assert tuple(tails) == ()
        assert zero_sum_tail_count == 0
        orbit_key = SEARCH.BASE.canonical_q_key(atom_ids)
        orbit_groups[orbit_key].append(atom_ids)
        direct_hits.append(
            {
                "atom_ids": atom_ids,
                "signature": signature,
                "escape_ids": escape,
                "zero_sum_six_tail_multisets": zero_sum_tail_count,
            }
        )

    orbit_keys = tuple(sorted(orbit_groups))
    result = {
        "schema": "p7-m4-full68-support8-unified-v1",
        "scope": (
            "complete union of the two no-multiplicity-three support-eight "
            "signatures; exact quotient necessary layer, not a height or "
            "full-68-scalar classification"
        ),
        "profile_count": len(profile_reports),
        **aggregate,
        "profiles_sha256": SEARCH.payload_digest(profile_reports),
        "hit_sha256": SEARCH.payload_digest(hits),
        "direct_hit_sha256": SEARCH.payload_digest(direct_hits),
        "orbit_count": len(orbit_keys),
        "orbit_sha256": SEARCH.BASE.payload_digest(orbit_keys),
        "orbit_preimages": tuple(len(orbit_groups[key]) for key in orbit_keys),
        "direct_hits": direct_hits,
        "shard_sha256": tuple(expected for _, expected in SHARDS),
        "conditional_exact_three_splice": {
            "dependency": "proofs/p7_m3_full_support8_frontier.md",
            "dependency_status": "PROVED_HERE; independent audit CORRECT",
            "dependency_report_stream_sha256": "25cdd6726db7605d5981e6c024d8ea6b7885ee2d4c87953700f852550559c0f5",
            "scope": (
                "support eight with a distinguished exact-three fibre and "
                "all other multiplicities at most four"
            ),
            "application": (
                "for a pointed-q^4 atom having an exact-three fibre r, use r "
                "as the dependency's distinguished value; the original q^4 "
                "is an allowed other fibre"
            ),
            "invariance": (
                "E1(B) and existence of a six-position zero-sum tail do not "
                "depend on which fibre is named distinguished and are GL(3,7)-invariant"
            ),
            "conditional_consequence": (
                "together with the no-three certificate and the support-at-most-seven "
                "splice, pointed-q^4 support at most eight is closed; next support "
                "boundary is at least nine"
            ),
            "nonclaim": "not a full 68-scalar UNSAT certificate",
        },
    }
    assert result["profile_count"] == 66
    assert aggregate == EXPECTED_AGGREGATE
    assert result["target_atom_hits"] == 3
    assert result["target_with_T_survivor"] == 0
    assert result["orbit_count"] == 2
    assert result["profiles_sha256"] == EXPECTED_PROFILES_SHA256
    assert result["hit_sha256"] == EXPECTED_HIT_SHA256
    assert result["direct_hit_sha256"] == EXPECTED_DIRECT_HIT_SHA256
    assert result["orbit_sha256"] == EXPECTED_ORBIT_SHA256
    output = root / "p7_m4_full68_support8_unified_report.json"
    digest = write_report(output, SEARCH.jsonable(result))
    assert digest == EXPECTED_REPORT_SHA256
    print("PASS exact shard hashes and disjoint 60+6 profile coverage")
    print("PASS independent direct atom/projective/position-spectrum replay on hits:", len(hits))
    print("PASS exact six-tail rejection on every hit")
    print("AGGREGATE", json.dumps(SEARCH.jsonable(aggregate), separators=(",", ":")))
    print("PROFILE SHA256:", result["profiles_sha256"])
    print("HIT SHA256:", result["hit_sha256"])
    print("DIRECT-HIT SHA256:", result["direct_hit_sha256"])
    print("ORBIT SHA256:", result["orbit_sha256"])
    print("UNIFIED REPORT SHA256:", digest)
    print("CONDITIONAL SPLICE: exact-three support-eight theorem; independent audit CORRECT")
    print("CONSEQUENCE AFTER SPLICE: pointed-q^4 support at most eight closed; next support at least nine")
    print("STATUS: strict support subbranches proved; full 68-scalar slice incomplete")


if __name__ == "__main__":
    main()
