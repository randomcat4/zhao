#!/usr/bin/env python3
"""Continue the exact p=7 support-nine collinear quotient search.

The first four full signatures are frozen in
``p7_support9_collinear_real_search.py``.  This driver independently rebuilds
the seven remaining unlabelled multiplicity signatures and their collinear
profile denominators, then reuses the frozen actual-position kernel without
editing it.  A full-signature run may use the weighted S3 action on the three
collinear points; every proper profile shard automatically uses all 36 scalar
frames.

Each finished profile is appended to a JSONL checkpoint.  The final report is
assembled only after the whole requested profile interval is present.  A
full-signature zero-survivor report is therefore one finite certificate; an
individual checkpoint row is not.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Sequence

import p7_m34_support9_search as OLD
import p7_support9_collinear_real_search as FROZEN


ALL_SIGNATURES = tuple(
    sorted(
        {
            tuple(sorted(profile, reverse=True))
            for profile in product(range(1, 5), repeat=9)
            if sum(profile) == 19
        }
    )
)
assert len(ALL_SIGNATURES) == 13

CLOSED_SIGNATURES = frozenset(
    {
        (3, 2, 2, 2, 2, 2, 2, 2, 2),
        (4, 2, 2, 2, 2, 2, 2, 2, 1),
        *FROZEN.TARGET_SIGNATURES,
    }
)
REMAINING_SIGNATURES = tuple(
    signature for signature in ALL_SIGNATURES if signature not in CLOSED_SIGNATURES
)
assert len(REMAINING_SIGNATURES) == 7

EXPECTED_REMAINING_DENOMINATORS = (410, 410, 543, 1370, 785, 410, 1110)
EXPECTED_REMAINING_TOTAL = 5_038
EXPECTED_CLOSED_TOTAL = 703
EXPECTED_ALL_TOTAL = 5_741


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_profiles(signature: Sequence[int]):
    """Rebuild the collinear-normalized profile set from the unlabelled type.

    Entries are ``(m_Q,m_E2,m_C,m_E3,m_1,...,m_5)``.  The collinear triple is
    sorted, E3 takes every multiplicity still present, and the five remaining
    multiplicities are attached to the increasing actual-vector labels in all
    distinct orders.
    """
    signature = tuple(signature)
    answer = set()
    for triple_indices in combinations(range(9), 3):
        triple = tuple(
            sorted((signature[index] for index in triple_indices), reverse=True)
        )
        remainder = list(signature)
        for multiplicity in triple:
            remainder.remove(multiplicity)
        for outside_multiplicity in sorted(set(remainder), reverse=True):
            tail = remainder.copy()
            tail.remove(outside_multiplicity)
            for ordered_tail in set(permutations(tail)):
                answer.add(triple + (outside_multiplicity,) + ordered_tail)
    return tuple(sorted(answer, reverse=True))


REMAINING_DENOMINATORS = tuple(
    len(independent_profiles(signature)) for signature in REMAINING_SIGNATURES
)
assert REMAINING_DENOMINATORS == EXPECTED_REMAINING_DENOMINATORS
assert sum(REMAINING_DENOMINATORS) == EXPECTED_REMAINING_TOTAL
assert sum(len(independent_profiles(signature)) for signature in CLOSED_SIGNATURES) == EXPECTED_CLOSED_TOTAL
assert sum(len(independent_profiles(signature)) for signature in ALL_SIGNATURES) == EXPECTED_ALL_TOTAL


def global_signature_index(signature: Sequence[int]) -> int:
    return ALL_SIGNATURES.index(tuple(signature)) + 1


def dependency_hashes(root: Path):
    names = (
        "p7_support9_collinear_real_search.py",
        "p7_m34_support9_search.py",
        "p7_length19_support7_escape_search.py",
    )
    return {name: sha256(root / name) for name in names}


def run_profile(task):
    (
        signature,
        signature_global_index,
        profile_index,
        profile,
        prefix_tail_depth,
        use_c_symmetry,
    ) = task
    report = FROZEN.search_profile(
        signature_global_index,
        profile_index,
        profile,
        prefix_tail_depth,
        use_c_symmetry,
    )
    assert tuple(report["signature"]) == tuple(signature)
    return report


def load_checkpoints(
    path: Path, signature: Sequence[int], profiles: Sequence[Sequence[int]],
    prefix_tail_depth: int, use_c_symmetry: bool, expected_dependencies,
):
    loaded = {}
    if not path.exists():
        return loaded
    expected_signature = tuple(signature)
    expected_mode = "full-signature-S3-closure" if use_c_symmetry else "none"
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("dependency_sha256") != expected_dependencies:
            continue
        report = row["report"]
        profile_index = int(report["profile_index"])
        if not 1 <= profile_index <= len(profiles):
            continue
        if tuple(report["signature"]) != expected_signature:
            continue
        if tuple(report["profile"]) != tuple(profiles[profile_index - 1]):
            continue
        if report["prefix_tail_depth"] != prefix_tail_depth:
            continue
        if report["c_symmetry_mode"] != expected_mode:
            continue
        compact = json.dumps(report, sort_keys=True, separators=(",", ":"))
        if hashlib.sha256(compact.encode("ascii")).hexdigest() != row["sha256"]:
            raise AssertionError(f"corrupt checkpoint line {line_number}")
        loaded[profile_index] = report
    return loaded


def append_checkpoint(path: Path, report, dependencies) -> None:
    compact = json.dumps(report, sort_keys=True, separators=(",", ":"))
    row = {
        "dependency_sha256": dependencies,
        "sha256": hashlib.sha256(compact.encode("ascii")).hexdigest(),
        "report": report,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def assemble_report(
    root: Path,
    signature_number: int,
    signature: Sequence[int],
    profiles: Sequence[Sequence[int]],
    reports_by_index,
    start: int,
    stop: int,
    prefix_tail_depth: int,
    full_signature: bool,
    checkpoint_path: Path,
):
    reports = []
    aggregate = Counter()
    position_reports = []
    profile_hasher = hashlib.sha256()
    for profile_index in range(start, stop + 1):
        raw = reports_by_index[profile_index]
        position_reports.extend(raw["position_reports"])
        report = {key: value for key, value in raw.items() if key != "position_reports"}
        aggregate.update(report["counts"])
        compact = json.dumps(report, sort_keys=True, separators=(",", ":"))
        profile_hasher.update(compact.encode("ascii"))
        reports.append(report)

    ledger = tuple(
        {
            "remaining_signature_number": index + 1,
            "global_signature_index": global_signature_index(item),
            "signature": item,
            "collinear_profile_denominator": len(independent_profiles(item)),
        }
        for index, item in enumerate(REMAINING_SIGNATURES)
    )
    result = {
        "schema": "p7-support9-collinear-real-remaining-v1",
        "scope": (
            "exact quotient-position search for one remaining collinear-normalized "
            "support-nine signature; full B atomicity, exact unordered six-tail "
            "L1/L2/L3 gate, all induced length-2..8 quotient-zero blocks, direct "
            "length-9..16 gap, and atomic-complement flags; no heights, Hasse, or "
            "actual-C7^4 conclusion"
        ),
        "signature_number_within_remaining": signature_number,
        "global_signature_index": global_signature_index(signature),
        "signature": tuple(signature),
        "signature_profile_denominator": len(profiles),
        "completed_profile_interval": (start, stop),
        "full_signature": full_signature,
        "c_symmetry_mode": (
            "full-signature-S3-closure" if full_signature else "none"
        ),
        "profile_count": len(reports),
        "prefix_tail_depth": prefix_tail_depth,
        "aggregate": dict(sorted(aggregate.items())),
        "profile_report_sha256": profile_hasher.hexdigest(),
        "exact_tail_survivor_count": len(position_reports),
        "exact_tail_survivor_sha256": FROZEN.payload_digest(position_reports),
        "remaining_signature_ledger": ledger,
        "remaining_profile_denominator_total": EXPECTED_REMAINING_TOTAL,
        "previously_closed_profile_denominator_total": EXPECTED_CLOSED_TOTAL,
        "all_profile_denominator_total": EXPECTED_ALL_TOTAL,
        "dependency_sha256": dependency_hashes(root),
        "checkpoint_file": str(checkpoint_path),
        "profiles": reports,
        "position_reports": position_reports,
    }
    return result


def self_test() -> None:
    assert set(CLOSED_SIGNATURES) | set(REMAINING_SIGNATURES) == set(ALL_SIGNATURES)
    assert set(CLOSED_SIGNATURES).isdisjoint(REMAINING_SIGNATURES)
    for signature in ALL_SIGNATURES:
        independent = set(independent_profiles(signature))
        frozen = set(FROZEN.profiles_for_signature(signature))
        assert independent == frozen
    chosen = min(
        zip(REMAINING_DENOMINATORS, REMAINING_SIGNATURES),
        key=lambda item: (item[0], item[1]),
    )
    assert chosen == (410, (3, 3, 3, 2, 2, 2, 2, 1, 1))
    FROZEN.self_test()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signature", type=int, choices=range(1, 8), default=1)
    parser.add_argument("--start-profile", type=int, default=1)
    parser.add_argument("--stop-profile", type=int)
    parser.add_argument("--prefix-tail-depth", type=int, default=2)
    parser.add_argument("--workers", type=int, default=max(1, min(16, os.cpu_count() or 1)))
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--skip-self-test", action="store_true")
    args = parser.parse_args()
    if args.prefix_tail_depth not in range(1, 5):
        raise ValueError("prefix-tail-depth must lie in 1..4")
    if not args.skip_self_test:
        self_test()

    root = Path(__file__).resolve().parent
    dependencies = dependency_hashes(root)
    signature = REMAINING_SIGNATURES[args.signature - 1]
    profiles = independent_profiles(signature)
    stop = len(profiles) if args.stop_profile is None else min(args.stop_profile, len(profiles))
    if not 1 <= args.start_profile <= stop:
        raise ValueError("invalid profile interval")
    full_signature = args.start_profile == 1 and stop == len(profiles)
    checkpoint_path = args.checkpoint or (
        Path(tempfile.gettempdir())
        / f"p7_support9_collinear_real_remaining_sig{args.signature}_"
          f"{'full' if full_signature else f'{args.start_profile}_{stop}'}.jsonl"
    )
    report_path = args.report or (
        root / f"p7_support9_collinear_real_remaining_sig{args.signature}_report.json"
    )

    reports_by_index = load_checkpoints(
        checkpoint_path,
        signature,
        profiles,
        args.prefix_tail_depth,
        full_signature,
        dependencies,
    )
    wanted = tuple(range(args.start_profile, stop + 1))
    missing = tuple(index for index in wanted if index not in reports_by_index)
    print(
        "REMAINING LEDGER",
        json.dumps(
            tuple((list(item), denominator) for item, denominator in zip(REMAINING_SIGNATURES, REMAINING_DENOMINATORS)),
            separators=(",", ":"),
        ),
        flush=True,
    )
    print(
        f"SIGNATURE {args.signature}/7 global={global_signature_index(signature)} "
        f"profiles={len(profiles)} interval={args.start_profile}..{stop} "
        f"resume={len(wanted) - len(missing)} missing={len(missing)} "
        f"workers={args.workers} symmetry={'S3-full' if full_signature else 'all-36'}",
        flush=True,
    )

    tasks = tuple(
        (
            signature,
            global_signature_index(signature),
            profile_index,
            profiles[profile_index - 1],
            args.prefix_tail_depth,
            full_signature,
        )
        for profile_index in missing
    )
    if args.workers == 1:
        for completed, task in enumerate(tasks, 1):
            report = run_profile(task)
            reports_by_index[report["profile_index"]] = report
            append_checkpoint(checkpoint_path, report, dependencies)
            print(
                f"CHECKPOINT {completed}/{len(tasks)} profile={report['profile_index']} "
                f"tails={len(report['position_reports'])}",
                flush=True,
            )
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(run_profile, task): task[2] for task in tasks}
            for completed, future in enumerate(as_completed(futures), 1):
                report = future.result()
                reports_by_index[report["profile_index"]] = report
                append_checkpoint(checkpoint_path, report, dependencies)
                print(
                    f"CHECKPOINT {completed}/{len(tasks)} profile={report['profile_index']} "
                    f"tails={len(report['position_reports'])}",
                    flush=True,
                )

    missing_after = [index for index in wanted if index not in reports_by_index]
    assert not missing_after
    result = assemble_report(
        root,
        args.signature,
        signature,
        profiles,
        reports_by_index,
        args.start_profile,
        stop,
        args.prefix_tail_depth,
        full_signature,
        checkpoint_path,
    )
    serial = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, default=list)
    report_path.write_text(serial + "\n", encoding="utf-8", newline="\n")
    summary = {
        key: value
        for key, value in result.items()
        if key not in {"profiles", "position_reports", "remaining_signature_ledger"}
    }
    print("REMAINING TOTAL", json.dumps(summary, separators=(",", ":"), default=list), flush=True)
    print("REPORT:", report_path, flush=True)
    print("REPORT SHA256:", sha256(report_path), flush=True)
    if full_signature and not result["position_reports"]:
        print("CERTIFIED: complete signature has no exact six-tail quotient extension", flush=True)
    elif full_signature:
        print("CERTIFIED: complete signature quotient survivors include full position spectra", flush=True)
    else:
        print("COVERAGE: exact profile shard only; no whole-signature claim", flush=True)
    print("STATUS: exact finite quotient-position slice; global A_p remains incomplete", flush=True)


if __name__ == "__main__":
    main()
