"""Independent exact audit of the 891 twelve-term hyperplane cores.

This program neither imports nor executes atom_three_hyperplane.py.  It exhausts
all multisets of one, two, or three elements from the 121 nonzero non-basis
vectors, with additional multiplicity at most two.  It uses no DFS and no
shortest-distance dynamic program.

For B=e1^3 e2^3 e3^3 the base subsequences have exactly the coordinate vectors
(a,b,c), 0 <= a,b,c <= 3.  B plus an extra-position subsequence X has a zero sum
iff -sum(X) lies in this box.  Thus B plus extra terms is zero-sum-free exactly
when every nonempty subset of extra POSITIONS has a sum with a coordinate 1.
The base alone is zero-sum-free.  Distances are computed independently by
enumerating all 64 base multiplicity choices and all extra-position subsets.

All file access stays under the supplied run directory (the default is the
script's parent-parent).  C:\\canglan is never accessed.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


RUN = Path(__file__).resolve().parent.parent
SOURCE_SCRIPT = RUN / "scripts" / "atom_three_hyperplane.py"
SOURCE_DATA = RUN / "evidence" / "atom_three_hyperplane.json"
OUTPUT = RUN / "evidence" / "verify_hyperplane_criteria_fresh.json"
ZERO = (0, 0, 0)
E1, E2, E3 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
BASE = (E1, E2, E3)
VECTORS = tuple(itertools.product(range(5), repeat=3))


def add(a, b):
    return tuple((x + y) % 5 for x, y in zip(a, b))


def sub(a, b):
    return tuple((x - y) % 5 for x, y in zip(a, b))


def negate(a):
    return tuple((-x) % 5 for x in a)


def encode(a):
    # Only an output/comparison convention, not the group arithmetic.
    return a[0] + 5 * a[1] + 25 * a[2]


def decode(a):
    return (a % 5, (a // 5) % 5, a // 25)


ALLOWED = tuple(sorted((v for v in VECTORS if v != ZERO and v not in BASE), key=encode))
NONZERO = tuple(v for v in VECTORS if v != ZERO)
BASE_CHOICES = tuple((v, sum(v)) for v in itertools.product(range(4), repeat=3))


def positional_sums(extra):
    """Direct enumeration, including repeated equal elements as separate positions."""
    result = []
    for mask in range(1 << len(extra)):
        value = ZERO
        for index, vector in enumerate(extra):
            if (mask >> index) & 1:
                value = add(value, vector)
        result.append((value, mask.bit_count()))
    return result


def is_zero_sum_free(extra):
    return all(1 in value for value, length in positional_sums(extra) if length)


def direct_distances(extra):
    distance = {v: 99 for v in VECTORS}
    for extra_sum, extra_length in positional_sums(extra):
        for base_sum, base_length in BASE_CHOICES:
            total = add(base_sum, extra_sum)
            distance[total] = min(distance[total], base_length + extra_length)
    return distance


def tuple_ids(extra):
    return tuple(encode(v) for v in extra)


def parallel(a, b):
    return any(tuple((c * x) % 5 for x in a) == b for c in range(1, 5))


def subset_sumset(directions):
    return {value for value, _ in positional_sums(directions)}


def geometry_audit():
    # An invertible linear map normalizes the first nonzero direction to e1.
    three_sizes = Counter()
    three_witness = {}
    for second, third in itertools.product(NONZERO, repeat=2):
        size = len(subset_sumset((E1, second, third)))
        three_sizes[size] += 1
        three_witness.setdefault(size, [E1, second, third])
    # With the first two independent, normalize those directions to e1,e2.
    four_sizes = Counter()
    four_witness = {}
    for third, fourth in itertools.product(NONZERO, repeat=2):
        size = len(subset_sumset((E1, E2, third, fourth)))
        four_sizes[size] += 1
        four_witness.setdefault(size, [E1, E2, third, fourth])
    pairing_cases = []
    for w in VECTORS:
        if w in (ZERO, E1, E2):
            continue
        good = [
            not parallel(E1, sub(w, E2)),
            not parallel(E2, sub(w, E1)),
            not parallel(w, sub(E2, E1)),
        ]
        assert any(good), (w, good)
        pairing_cases.append({"fourth_point": w, "good_pairings": good})
    assert min(three_sizes) == 4
    assert min(four_sizes) >= 6
    assert len(pairing_cases) == 122
    return {
        "three_two_point_sets": {
            "normalization": "first difference = e1 by GL(3,5)",
            "denominator": sum(three_sizes.values()),
            "size_distribution": dict(sorted(three_sizes.items())),
            "minimum": min(three_sizes),
            "minimum_witness_directions": three_witness[min(three_sizes)],
        },
        "four_two_point_sets_first_two_independent": {
            "normalization": "first two differences = e1,e2 by GL(3,5)",
            "denominator": sum(four_sizes.values()),
            "size_distribution": dict(sorted(four_sizes.items())),
            "minimum": min(four_sizes),
            "minimum_witness_directions": four_witness[min(four_sizes)],
        },
        "four_point_pairing": {
            "normalization": "three noncollinear points = 0,e1,e2",
            "denominator": len(pairing_cases),
            "passed": len(pairing_cases),
            "cases": pairing_cases,
        },
    }


def main():
    source = json.loads(SOURCE_DATA.read_text(encoding="utf-8"))
    valid = {0: [()]}
    enumeration = {"9": {"enumerated_multisets": 1, "zero_sum_free": 1}}
    for length in (1, 2, 3):
        valid[length] = []
        tested = rejected = cap_rejected = 0
        for extra in itertools.combinations_with_replacement(ALLOWED, length):
            if max(Counter(extra).values()) > 2:
                cap_rejected += 1
                continue
            tested += 1
            if is_zero_sum_free(extra):
                valid[length].append(extra)
            else:
                rejected += 1
        enumeration[str(9 + length)] = {
            "enumerated_multisets": tested,
            "excluded_multiplicity_three_multisets": cap_rejected,
            "zero_sum_free": len(valid[length]),
            "rejected_with_zero_sum": rejected,
        }

    expected_ids = sorted(tuple_ids(extra) for extra in valid[3])
    source_ids = [tuple(row) for row in source["length12_extensions"]]
    checks = {
        "source_extensions_have_no_duplicates": len(source_ids) == len(set(source_ids)),
        "source_extensions_equal_independent_enumeration": sorted(source_ids) == expected_ids,
        "source_initial_candidates_exact": source["initial_safe_candidates"] == [encode(e[0]) for e in valid[1]],
        "source_nodes_by_length_exact": source["nodes_by_length"] == {str(9 + k): len(v) for k, v in valid.items()},
    }

    # These are terminal prefixes in the canonical sorted search, not a claim
    # that a multiset has no extension using an element smaller than its last.
    canonical_leaves = []
    for k in (0, 1, 2):
        next_prefixes = {tuple_ids(e[:-1]) for e in valid[k + 1]}
        canonical_leaves.extend(tuple_ids(e) for e in valid[k] if tuple_ids(e) not in next_prefixes)
    checks["source_other_leaf_extensions_exact_as_canonical_prefix_leaves"] = (
        sorted(map(tuple, source["other_leaf_extensions"])) == sorted(canonical_leaves)
    )

    profiles = Counter()
    rows = []
    pass_counts = Counter()
    e9_counts, e10_counts, d10_counts = Counter(), Counter(), Counter()
    for extra in valid[3]:
        dist = direct_distances(extra)
        total = (3, 3, 3)
        for term in extra:
            total = add(total, term)
        profile = tuple(Counter(dist.values())[k] for k in range(13))
        profiles[profile] += 1
        e9 = [encode(v) for v in VECTORS if dist[v] >= 9]
        e10 = [encode(v) for v in VECTORS if dist[v] >= 10]
        greater10 = [v for v in VECTORS if dist[v] > 10]
        conditions = {
            "A1_coverage_unique_distance_above_10_is_sigma_at_12": max(dist.values()) <= 12 and greater10 == [total] and dist[total] == 12,
            "A2_at_most_2_targets_with_distance_ge_10": len(e10) <= 2,
            "A3_at_most_5_targets_with_distance_ge_9": len(e9) <= 5,
            "B1_every_non_sigma_target_has_distance_le_10": all(d <= 10 for v, d in dist.items() if v != total),
            "B2_at_most_3_targets_with_distance_ge_10": len(e10) <= 3,
        }
        for name, passed in conditions.items():
            pass_counts[name] += int(passed)
        e9_counts[len(e9)] += 1
        e10_counts[len(e10)] += 1
        d10_counts[profile[10]] += 1
        rows.append({
            "extension": tuple_ids(extra),
            "sigma": encode(total),
            "counts_by_distance": profile,
            "distance_9_or_more_targets": sorted(e9),
            "distance_10_or_more_targets": sorted(e10),
            "distances_by_encoded_target": [dist[decode(i)] for i in range(125)],
            "five_conditions": conditions,
        })
    source_profiles = Counter()
    source_examples_valid = True
    direct_row_by_extension = {tuple(r["extension"]): r for r in rows}
    for row in source["length12_distance_profiles"]:
        profile = tuple(row["counts_by_distance"])
        source_profiles[profile] += row["count"]
        example = tuple(row["one_extension"])
        source_examples_valid &= example in direct_row_by_extension and tuple(direct_row_by_extension[example]["counts_by_distance"]) == profile
    checks["source_distance_profile_counts_exact"] = profiles == source_profiles
    checks["source_distance_profile_examples_exact"] = source_examples_valid

    perms = list(itertools.permutations(range(3)))
    orbits = {}
    for extra in valid[3]:
        orbit = {
            tuple(sorted(encode(tuple(v[i] for i in perm)) for v in extra))
            for perm in perms
        }
        assert orbit <= set(expected_ids)
        key = min(orbit)
        orbits[key] = orbit
    orbit_sizes = Counter(len(orbit) for orbit in orbits.values())
    assert sum(size * count for size, count in orbit_sizes.items()) == len(expected_ids)

    all_good = all(checks.values()) and len(expected_ids) == 891 and all(c == 891 for c in pass_counts.values())
    assert all_good, checks
    report = {
        "status": "CORRECT",
        "scope": "exactly e1^3 e2^3 e3^3 plus 3 extra positions; each nonbasis element has multiplicity <= 2",
        "independent_method": "all multisets, direct base-box zero-sum criterion, direct 64 times 8 representation enumeration; no DFS, no distance DP",
        "source_sha256": {
            str(p.relative_to(RUN)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (SOURCE_SCRIPT, SOURCE_DATA)
        },
        "allowed_nonzero_nonbasis_vectors": len(ALLOWED),
        "enumeration": enumeration,
        "checks_against_source": checks,
        "twelve_term_core_count_before_S3": len(expected_ids),
        "S3_orbit_count": len(orbits),
        "S3_orbit_size_distribution": dict(sorted(orbit_sizes.items())),
        "distinct_distance_profiles": len(profiles),
        "distance_table_entries_checked": len(expected_ids) * 125,
        "representations_checked_for_distances": len(expected_ids) * 64 * 8,
        "five_criterion_denominators": {name: {"passed": value, "denominator": len(expected_ids)} for name, value in sorted(pass_counts.items())},
        "number_of_targets_at_distance_10_distribution": dict(sorted(d10_counts.items())),
        "number_of_targets_at_distance_ge_10_distribution": dict(sorted(e10_counts.items())),
        "number_of_targets_at_distance_ge_9_distribution": dict(sorted(e9_counts.items())),
        "distance_11_total_targets": sum(row["counts_by_distance"][11] for row in rows),
        "distance_12_total_targets": sum(row["counts_by_distance"][12] for row in rows),
        "canonical_other_leaf_count": len(canonical_leaves),
        "geometry": geometry_audit(),
        "all_core_distance_tables": rows,
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {k: v for k, v in report.items() if k not in ("all_core_distance_tables", "geometry")}
    summary["geometry_summary"] = {k: {a: b for a, b in v.items() if a != "cases"} for k, v in report["geometry"].items()}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
