#!/usr/bin/env python3
"""Exact support-eight quotient frontier for p=7,m=4,0001,s=6.

The frozen multiplicity-three support-seven theorem handles every support-eight
signature containing a three-fold fibre only after a new classification, so
this file deliberately makes the smaller precise claim requested here: it
exhausts the two support-eight signatures which contain a pointed q^4, have
maximum multiplicity four, and contain no multiplicity-three fibre.

Every E1-nonempty atom hit is passed to the exact proper-T-subset middle-gap
and 0001 quotient-trace propagation implemented by
``p7_m4_full68_short_support_search.search_profile``.  This is a quotient
necessary layer.  A T survivor, if one appears, still requires all heights,
automatically induced short blocks, Hasse/intersection equations, actual-Z
atomicity, and every F3-complement atom check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import p7_m4_full68_short_support_search as SEARCH


SIGNATURES = (
    (4, 4, 4, 2, 2, 1, 1, 1),
    (4, 4, 2, 2, 2, 2, 2, 1),
)


def add_counters(target, source):
    for key in SEARCH.empty_counters():
        target[key] += source[key]


def write_report(path: Path, result):
    payload = json.dumps(
        SEARCH.jsonable(result), ensure_ascii=False, indent=2, sort_keys=True
    )
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--signature", type=int, choices=(1, 2))
    parser.add_argument("--start-profile", type=int, default=1)
    parser.add_argument("--stop-profile", type=int)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    expected_profile_counts = (60, 6)
    assert tuple(len(SEARCH.profile_list(signature)) for signature in SIGNATURES) == (
        expected_profile_counts
    )
    indices = (args.signature - 1,) if args.signature is not None else range(2)
    aggregate = SEARCH.empty_counters()
    profiles_done = []
    profile_reports = []
    hits = []
    for signature_index in indices:
        signature = SIGNATURES[signature_index]
        profiles = SEARCH.profile_list(signature)
        stop = len(profiles) if args.stop_profile is None else min(
            args.stop_profile, len(profiles)
        )
        if not 1 <= args.start_profile <= stop + 1:
            raise ValueError("invalid profile interval")
        profiles_done.append((signature, len(profiles), (args.start_profile, stop)))
        for profile_index in range(args.start_profile, stop + 1):
            report, new_hits = SEARCH.search_profile(
                signature, profile_index, profiles[profile_index - 1]
            )
            profile_reports.append(report)
            hits.extend(new_hits)
            add_counters(aggregate, report)
            if not args.quiet:
                print(
                    "FULL68 SUPPORT8 PROFILE",
                    json.dumps(SEARCH.jsonable(report), separators=(",", ":")),
                    flush=True,
                )

    orbit_groups = defaultdict(list)
    for hit in hits:
        orbit_groups[SEARCH.BASE.canonical_q_key(hit["atom_ids"])].append(hit)
    orbit_keys = tuple(sorted(orbit_groups))
    result = {
        "schema": "p7-m4-full68-support8-v1",
        "scope": (
            "all normalized support-eight, no-multiplicity-three length-19 "
            "atoms with pointed q^4 and maximum fibre four; quotient necessary "
            "layer only"
        ),
        "completed": profiles_done,
        "profile_count": len(profile_reports),
        **aggregate,
        "hit_sha256": SEARCH.payload_digest(hits),
        "orbit_count": len(orbit_keys),
        "orbit_sha256": SEARCH.BASE.payload_digest(orbit_keys),
        "profiles_sha256": SEARCH.payload_digest(profile_reports),
        "profiles": profile_reports,
        "hits": hits,
    }
    print(
        "FULL68 SUPPORT8 TOTAL",
        json.dumps(SEARCH.jsonable({key: value for key, value in result.items() if key not in {"profiles", "hits"}}), separators=(",", ":")),
        flush=True,
    )
    full_run = args.signature is None and args.start_profile == 1 and args.stop_profile is None
    if full_run:
        assert result["profile_count"] == 66
        assert result["target_with_T_survivor"] == 0
        print("CERTIFIED: both no-three support-eight signatures exhausted")
        print("CERTIFIED: every E1-nonempty atom hit fails the six-position T layer")
        print("STATUS: PROVED no-three support-eight quotient exclusion; full 68-scalar slice incomplete")
    else:
        print("STATUS: deterministic profile shard only")
    if args.report is not None:
        digest = write_report(args.report, result)
        print("REPORT:", args.report)
        print("REPORT SHA256:", digest)


if __name__ == "__main__":
    main()
