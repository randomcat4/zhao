#!/usr/bin/env python3
"""Independent-interface checks for the support-eight frontier program.

This is a same-work-unit differential, not an independent audit of the full
462-profile computation.  It reconstructs the profile denominator by a
different recursion and checks the three load-bearing local interfaces against
direct position/coefficient enumeration.
"""

from __future__ import annotations

import json
from itertools import combinations_with_replacement, product
from pathlib import Path

import p7_m3_full_support8_frontier as search
import verify_p7_maximal_atom_escape_algebra as algebra


def recursive_compositions(length, total, prefix=()):
    if length == 0:
        if total == 0:
            yield prefix
        return
    for value in range(1, 5):
        remaining = total - value
        if length - 1 <= remaining <= 4 * (length - 1):
            yield from recursive_compositions(length - 1, remaining, prefix + (value,))


def direct_prefix_safe(values, multiplicities, basis_bounds):
    for basis in product(*(range(bound + 1) for bound in basis_bounds)):
        for extra in product(*(range(bound + 1) for bound in multiplicities)):
            if not any(basis) and not any(extra):
                continue
            total = tuple(entry % search.P for entry in basis)
            for coefficient, value in zip(extra, values):
                total = search.old.add(total, search.old.scale(coefficient, value))
            if total == search.ZERO:
                return False
    return True


def strict_state(values, multiplicities, basis_bounds):
    forbidden = {
        search.VECTOR_ID[((-c1) % search.P, (-c2) % search.P, (-c3) % search.P)]
        for c1 in range(basis_bounds[0] + 1)
        for c2 in range(basis_bounds[1] + 1)
        for c3 in range(basis_bounds[2] + 1)
    } - {search.ZERO_ID}
    state = frozenset((search.ZERO_ID,))
    for value, multiplicity in zip(values, multiplicities):
        state = search.strict_extend_reachable(state, value, multiplicity, forbidden)
        if state is None:
            return False
    return True


def audit_strict_prefix():
    basis_bounds = (3, 4, 1)
    values = tuple(
        value for value in search.old.EXTRA_VALUES
        if value[2] == 0 and search.line_key(value) not in search.FIXED_LINES
    )[:12]
    probes = 0
    for left_index, left in enumerate(values):
        for right in values[left_index + 1:]:
            if search.line_key(left) == search.line_key(right):
                continue
            for multiplicities in ((4, 1), (3, 2), (2, 2)):
                expected = direct_prefix_safe((left, right), multiplicities, basis_bounds)
                observed = strict_state((left, right), multiplicities, basis_bounds)
                assert observed == expected
                probes += 1
    assert probes > 0
    return probes


def audit_position_layers():
    labels = next(entry[1] for entry in algebra.ATOMS if entry[0] == "support7_escape_1")
    counts = {}
    for value in labels:
        counts[value] = counts.get(value, 0) + 1
    blocks = tuple(sorted(counts.items()))
    block_layers = search.position_layers_for_blocks(blocks)
    direct_layers = algebra.fixed_size_supports(labels, 11)
    converted = tuple(
        frozenset(algebra.VECTORS[value_id] for value_id in layer)
        for layer in direct_layers
    )
    assert block_layers == converted
    return tuple(len(layer) for layer in block_layers)


def brute_six_tail(escape):
    return any(
        search.old.total(tail) == search.ZERO
        for tail in combinations_with_replacement(escape, 6)
    )


def audit_six_tail():
    pool = search.ALL_NONZERO[:8]
    probes = 0
    for mask in range(1 << len(pool)):
        escape = tuple(pool[index] for index in range(len(pool)) if mask & (1 << index))
        assert search.six_tail_possible(escape) == brute_six_tail(escape)
        probes += 1
    return probes


def audit_report():
    profiles = tuple(
        profile for profile in recursive_compositions(7, 16)
        if profile[0] == max(profile)
    )
    assert profiles == search.support_eight_profiles()
    assert len(profiles) == search.EXPECTED_PROFILES
    report_path = Path(__file__).parent / "verifications" / "p7_m3_full_support8_frontier_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["canonical_profiles"] == search.EXPECTED_PROFILES
    assert report["aggregate_counts"] == search.EXPECTED_FULL_AGGREGATE
    assert report["report_stream_sha256"] == search.EXPECTED_FULL_REPORT_SHA256
    assert report["empty_orbit_report_sha256"] == search.EXPECTED_EMPTY_ORBIT_SHA256
    assert report["tail_viable_candidates"] == 0
    return len(profiles)


def main():
    profiles = audit_report()
    prefix_probes = audit_strict_prefix()
    layers = audit_position_layers()
    tail_probes = audit_six_tail()
    print("PASS recursive profile reconstruction:", profiles)
    print("PASS direct bounded-coefficient prefix differentials:", prefix_probes)
    print("PASS block-vs-position fixed-size layers:", layers)
    print("PASS ordered-DP vs unordered six-tail differentials:", tail_probes)
    print("STATUS: local interface differential; full 462-profile result still requires full replay")


if __name__ == "__main__":
    main()
