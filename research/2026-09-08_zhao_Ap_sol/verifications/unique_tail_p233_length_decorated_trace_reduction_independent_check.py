#!/usr/bin/env python3
"""Fresh no-import audit of the p=233 length-decorated trace reduction.

No candidate module is imported.  Four-edge graphs are reconstructed from all
simple labelled graphs on 4..8 vertices and deduplicated componentwise up to
isomorphism.  Trace assignments and every {7,8} decoration are then enumerated
from definitions.  The candidate JSON is read only after the independent
counts have been formed, in order to validate its rows and certificate.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from hashlib import sha256
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CANDIDATE_PROOF = ROOT / "proofs" / "unique_tail_p233_length_decorated_trace_reduction.md"
CANDIDATE_SCRIPT = ROOT / "unique_tail_p233_length_decorated_trace_reduction.py"
CANDIDATE_REPORT = ROOT / "unique_tail_p233_length_decorated_trace_reduction_report.json"
AUDIT_REPORT = HERE / "unique_tail_p233_length_decorated_trace_reduction_independent_report.json"

EXPECTED_HASHES = {
    "proof": "3f7c85cec10a8c497a8e1f1e561b71869edec607c4fa01c00dbafd9fc71292ea",
    "script": "16bfc8ffc121de0e5f11565d85df4811b28d1ac7331a003d64b5ba61db8a7704",
    "report": "3c2f2c0405842b75c47fbf7fcedf09f0ef5275e9fe2a0339e1e9e71d47e4df47",
    "certificate": "37a86e2606fe21329a1cfb663d70528420648b042817600ecf0e62e18a548c02",
}

REQUIRED_DEPENDENCIES = {
    "unique_tail_p233_type3_p2_trace_shards_report.json",
    "proofs/unique_tail_p233_singleton_tail_fringe.md",
    "verifications/unique_tail_p233_singleton_tail_fringe_independent_review.md",
    "proofs/unique_tail_property_b_two_max_mixed_exclusion.md",
    "unique_tail_property_b_two_max_mixed_exclusion.py",
    "unique_tail_property_b_two_max_mixed_exclusion_report.json",
    "proofs/unique_tail_property_b_three_domain_general.md",
    "unique_tail_property_b_three_domain_general.py",
    "unique_tail_property_b_three_domain_general_report.json",
    "verifications/unique_tail_property_b_three_domain_general_independent_review.md",
    "verifications/unique_tail_property_b_three_domain_general_independent_check.py",
    "verifications/unique_tail_property_b_three_domain_general_independent_report.json",
}

TRACE_MASKS = tuple(range(1, 7))
SINGLETONS = frozenset((1, 2, 4))


def file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def components(n: int, edges: frozenset[tuple[int, int]]) -> list[list[int]]:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    ans = []
    seen = set()
    for start in range(n):
        if start in seen:
            continue
        todo = deque([start])
        seen.add(start)
        comp = []
        while todo:
            v = todo.popleft()
            comp.append(v)
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    todo.append(w)
        ans.append(sorted(comp))
    return ans


def canonical_component(comp: list[int], edges: frozenset[tuple[int, int]]) -> tuple[int, tuple[int, ...]]:
    codes = []
    for order in itertools.permutations(comp):
        code = tuple(
            int(tuple(sorted((order[i], order[j]))) in edges)
            for i in range(len(order))
            for j in range(i + 1, len(order))
        )
        codes.append(code)
    return (len(comp), min(codes))


def graph_key(n: int, edges: frozenset[tuple[int, int]]) -> tuple[tuple[int, tuple[int, ...]], ...]:
    return tuple(sorted(canonical_component(comp, edges) for comp in components(n, edges)))


def graph_signature(n: int, edges: frozenset[tuple[int, int]]) -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    degrees = [0] * n
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    rows = []
    for comp in components(n, edges):
        edge_count = sum(1 for a, b in edges if a in comp and b in comp)
        rows.append((len(comp), edge_count, tuple(sorted(degrees[v] for v in comp))))
    return tuple(sorted(rows))


SIGNATURE_NAMES = {
    ((4, 4, (1, 2, 2, 3)),): "paw",
    ((4, 4, (2, 2, 2, 2)),): "C4",
    ((5, 4, (1, 1, 2, 2, 2)),): "P5",
    ((5, 4, (1, 1, 1, 2, 3)),): "T5",
    ((5, 4, (1, 1, 1, 1, 4)),): "K1_4",
    ((2, 1, (1, 1)), (4, 3, (1, 1, 2, 2))): "P4_plus_K2",
    ((2, 1, (1, 1)), (4, 3, (1, 1, 1, 3))): "K1_3_plus_K2",
    ((2, 1, (1, 1)), (3, 3, (2, 2, 2))): "K3_plus_K2",
    ((3, 2, (1, 1, 2)), (3, 2, (1, 1, 2))): "two_P3",
    ((2, 1, (1, 1)), (2, 1, (1, 1)), (3, 2, (1, 1, 2))): "P3_plus_two_K2",
    ((2, 1, (1, 1)),) * 4: "four_K2",
}


def reconstruct_unlabelled_graphs() -> dict[str, tuple[int, tuple[tuple[int, int], ...]]]:
    representatives = {}
    seen_keys = set()
    for n in range(4, 9):
        possible_edges = tuple(itertools.combinations(range(n), 2))
        for raw in itertools.combinations(possible_edges, 4):
            edges = frozenset(tuple(sorted(edge)) for edge in raw)
            used = {v for edge in edges for v in edge}
            if len(used) != n:
                continue
            key = graph_key(n, edges)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            signature = graph_signature(n, edges)
            if signature not in SIGNATURE_NAMES:
                raise AssertionError((n, raw, signature))
            name = SIGNATURE_NAMES[signature]
            if name in representatives:
                raise AssertionError(("signature collision", name))
            representatives[name] = (n, tuple(sorted(edges)))
    if set(representatives) != set(SIGNATURE_NAMES.values()):
        raise AssertionError(set(SIGNATURE_NAMES.values()) - set(representatives))
    return representatives


def valid_trace(assignment: tuple[int, ...], edges: tuple[tuple[int, int], ...]) -> bool:
    return all((assignment[a] & assignment[b]) == 0 for a, b in edges)


def colored_parent_key(
    shape: str,
    assignment: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
) -> tuple[str, tuple[int, ...], tuple[tuple[int, int], ...]]:
    """Canonical colored graph key; distinct trace colors fix every vertex."""
    return (
        shape,
        tuple(sorted(assignment)),
        tuple(sorted(tuple(sorted((assignment[a], assignment[b]))) for a, b in edges)),
    )


def decorated_key(
    parent_key: tuple[str, tuple[int, ...], tuple[tuple[int, int], ...]],
    assignment: tuple[int, ...],
    lengths: tuple[int, ...],
) -> tuple[object, tuple[tuple[int, int], ...]]:
    return (parent_key, tuple(sorted(zip(assignment, lengths))))


def independent_enumeration() -> dict[str, object]:
    graphs = reconstruct_unlabelled_graphs()
    trace_table = {}
    distinct_rows = []
    for name, (n, edges) in graphs.items():
        valid = repeated = distinct = 0
        for assignment in itertools.product(TRACE_MASKS, repeat=n):
            if not valid_trace(assignment, edges):
                continue
            valid += 1
            if len(set(assignment)) == n:
                distinct += 1
                if not SINGLETONS <= set(assignment):
                    raise AssertionError((name, assignment))
                distinct_rows.append((name, n, edges, assignment))
            else:
                repeated += 1
        trace_table[name] = {"valid": valid, "repeated": repeated, "distinct": distinct}

    all_count = eliminated_count = surviving_count = 0
    all_by_shape = Counter()
    eliminated_by_shape = Counter()
    surviving_by_shape = Counter()
    singleton_sevens = Counter()
    total_sevens = Counter()
    all_eight_by_shape = Counter()
    # The frozen 36-shard convention keeps assignments on a fixed graph
    # representative, so automorphic colored assignments retain multiplicity.
    parent_keys = Counter()
    survivor_keys = Counter()
    for name, n, _edges, assignment in distinct_rows:
        parent_key = colored_parent_key(name, assignment, _edges)
        parent_keys[parent_key] += 1
        singleton_vertices = tuple(i for i, mask in enumerate(assignment) if mask in SINGLETONS)
        if len(singleton_vertices) != 3:
            raise AssertionError((name, assignment, singleton_vertices))
        for lengths in itertools.product((7, 8), repeat=n):
            all_count += 1
            all_by_shape[name] += 1
            singleton_count = sum(lengths[i] == 7 for i in singleton_vertices)
            if singleton_count >= 2:
                eliminated_count += 1
                eliminated_by_shape[name] += 1
            else:
                surviving_count += 1
                surviving_by_shape[name] += 1
                survivor_key = decorated_key(parent_key, assignment, lengths)
                survivor_keys[survivor_key] += 1
                singleton_sevens[singleton_count] += 1
                total_sevens[sum(length == 7 for length in lengths)] += 1
                if all(length == 8 for length in lengths):
                    all_eight_by_shape[name] += 1

    return {
        "unlabelled_graph_count": len(graphs),
        "graph_vertex_distribution": dict(sorted(Counter(n for n, _ in graphs.values()).items())),
        "trace_table": dict(sorted(trace_table.items())),
        "valid_trace_total": sum(row["valid"] for row in trace_table.values()),
        "repeated_trace_total": sum(row["repeated"] for row in trace_table.values()),
        "distinct_trace_total": len(distinct_rows),
        "distinct_by_shape": dict(sorted(Counter(row[0] for row in distinct_rows).items())),
        "decorated_total": all_count,
        "eliminated_total": eliminated_count,
        "surviving_total": surviving_count,
        "decorated_by_shape": dict(sorted(all_by_shape.items())),
        "eliminated_by_shape": dict(sorted(eliminated_by_shape.items())),
        "surviving_by_shape": dict(sorted(surviving_by_shape.items())),
        "surviving_singleton_sevens": {str(k): v for k, v in sorted(singleton_sevens.items())},
        "surviving_total_sevens": {str(k): v for k, v in sorted(total_sevens.items())},
        "all_eight_by_shape": dict(sorted(all_eight_by_shape.items())),
        "_parent_keys": parent_keys,
        "_survivor_keys": survivor_keys,
    }


def validate_candidate_report(
    independent: dict[str, object],
    expected_parent_keys: Counter[tuple[object, ...]],
    expected_survivor_keys: Counter[tuple[object, ...]],
) -> dict[str, object]:
    report = json.loads(CANDIDATE_REPORT.read_text(encoding="utf-8"))
    claimed = report.pop("certificate_sha256")
    if claimed != EXPECTED_HASHES["certificate"] or canonical_hash(report) != claimed:
        raise AssertionError("candidate report certificate mismatch")
    report["certificate_sha256"] = claimed

    dependencies = report["dependencies_sha256"]
    if set(dependencies) != REQUIRED_DEPENDENCIES:
        raise AssertionError(
            ("dependency manifest mismatch", sorted(REQUIRED_DEPENDENCIES - set(dependencies)),
             sorted(set(dependencies) - REQUIRED_DEPENDENCIES))
        )
    for relative_path, expected_hash in dependencies.items():
        if file_hash(ROOT / relative_path) != expected_hash:
            raise AssertionError(("stale dependency hash", relative_path))

    if report["counts"] != {
        "all_length_decorated_shards": independent["decorated_total"],
        "eliminated_at_least_two_singletons_length_7": independent["eliminated_total"],
        "parent_trace_shards": independent["distinct_trace_total"],
        "surviving_outer_shards": independent["surviving_total"],
    }:
        raise AssertionError("candidate summary counts differ from independent counts")

    expected_shape = {
        name: {
            "decorated_total": independent["decorated_by_shape"].get(name, 0),
            "eliminated": independent["eliminated_by_shape"].get(name, 0),
            "surviving": independent["surviving_by_shape"].get(name, 0),
        }
        for name in independent["decorated_by_shape"]
    }
    if report["counts_by_shape"] != expected_shape:
        raise AssertionError((report["counts_by_shape"], expected_shape))
    if report["surviving_singleton_length_7_distribution"] != independent["surviving_singleton_sevens"]:
        raise AssertionError("singleton-seven distribution mismatch")
    if report["surviving_total_length_7_distribution"] != independent["surviving_total_sevens"]:
        raise AssertionError("total-seven distribution mismatch")

    rows = report["surviving_shards"]
    if len(rows) != independent["surviving_total"]:
        raise AssertionError("wrong survivor row denominator")
    ids = set()
    parents = set()
    recomputed_singleton = Counter()
    recomputed_total = Counter()
    all_eight_parents = set()
    candidate_parent_keys = {}
    candidate_survivor_keys = Counter()
    for row in rows:
        rid = row["decorated_shard_id"]
        if rid in ids:
            raise AssertionError(("duplicate decorated id", rid))
        ids.add(rid)
        parents.add(row["parent_shard_id"])
        traces = tuple(row["endpoint_trace_masks"])
        lengths = tuple(row["endpoint_lengths"])
        edges = tuple(tuple(edge) for edge in row["edges"])
        singleton_vertices = tuple(i for i, mask in enumerate(traces) if mask in SINGLETONS)
        if len(traces) != row["vertex_count"] or len(set(traces)) != len(traces):
            raise AssertionError(("bad trace row", rid))
        if not valid_trace(traces, edges):
            raise AssertionError(("edge traces not disjoint", rid))
        signature = graph_signature(row["vertex_count"], frozenset(edges))
        if SIGNATURE_NAMES.get(signature) != row["shape"]:
            raise AssertionError(("wrong graph shape", rid, signature, row["shape"]))
        parent_key = colored_parent_key(row["shape"], traces, edges)
        old_parent_key = candidate_parent_keys.setdefault(row["parent_shard_id"], parent_key)
        if old_parent_key != parent_key:
            raise AssertionError(("parent id changes colored shard", row["parent_shard_id"]))
        if singleton_vertices != tuple(row["singleton_vertices"]) or len(singleton_vertices) != 3:
            raise AssertionError(("singleton index mismatch", rid))
        if any(length not in (7, 8) for length in lengths):
            raise AssertionError(("bad endpoint length", rid))
        singleton_count = sum(lengths[i] == 7 for i in singleton_vertices)
        total_count = sum(length == 7 for length in lengths)
        if singleton_count >= 2 or singleton_count != row["singleton_length_7_count"]:
            raise AssertionError(("eliminated row retained", rid))
        if total_count != row["total_length_7_count"]:
            raise AssertionError(("bad total-seven count", rid))
        survivor_key = decorated_key(parent_key, traces, lengths)
        candidate_survivor_keys[survivor_key] += 1
        recomputed_singleton[singleton_count] += 1
        recomputed_total[total_count] += 1
        if total_count == 0:
            all_eight_parents.add(row["parent_shard_id"])

    if len(parents) != 36 or len(all_eight_parents) != 36:
        raise AssertionError((len(parents), len(all_eight_parents)))
    if Counter(candidate_parent_keys.values()) != expected_parent_keys:
        raise AssertionError("candidate parent shards differ from independent colored shards")
    if candidate_survivor_keys != expected_survivor_keys:
        raise AssertionError("candidate survivor rows differ from independent decorations")
    if dict(report["surviving_singleton_length_7_distribution"]) != {
        str(k): v for k, v in sorted(recomputed_singleton.items())
    }:
        raise AssertionError("row-level singleton distribution mismatch")
    if dict(report["surviving_total_length_7_distribution"]) != {
        str(k): v for k, v in sorted(recomputed_total.items())
    }:
        raise AssertionError("row-level total distribution mismatch")
    return {
        "candidate_certificate_recomputed": claimed,
        "candidate_survivor_rows_checked": len(rows),
        "unique_decorated_ids": len(ids),
        "unique_parent_ids": len(parents),
        "all_eight_parent_ids": len(all_eight_parents),
        "dependency_hashes_checked": len(dependencies),
        "abstract_survivor_rows_matched_with_multiplicity": sum(candidate_survivor_keys.values()),
    }


def add(u: tuple[int, int], v: tuple[int, int], p: int) -> tuple[int, int]:
    return ((u[0] + v[0]) % p, (u[1] + v[1]) % p)


def sub(u: tuple[int, int], v: tuple[int, int], p: int) -> tuple[int, int]:
    return ((u[0] - v[0]) % p, (u[1] - v[1]) % p)


def scale(c: int, u: tuple[int, int], p: int) -> tuple[int, int]:
    return ((c * u[0]) % p, (c * u[1]) % p)


def det(u: tuple[int, int], v: tuple[int, int], p: int) -> int:
    return (u[0] * v[1] - u[1] * v[0]) % p


def support_domains_for_tail_pair(
    a: tuple[int, int], b: tuple[int, int], p: int
) -> dict[tuple[int, int], frozenset[tuple[int, int]]]:
    """Rebuild every Property-B support {g} union (h+<g>) containing a,b."""
    zero = (0, 0)
    difference = sub(b, a, p)
    domains = {}
    for gx in range(p):
        for gy in range(p):
            g = (gx, gy)
            if g == zero:
                continue
            if g == a:
                base = b
            elif g == b:
                base = a
            elif det(g, difference, p) == 0:
                base = a
            else:
                continue
            line = frozenset(add(base, scale(c, g, p), p) for c in range(p))
            if zero in line:
                continue
            domain = frozenset(set(line) | {g})
            if a not in domain or b not in domain or len(domain) != p + 1:
                raise AssertionError(("malformed Property-B domain", a, b, g))
            domains[g] = domain
    return domains


def independent_property_b_application() -> dict[str, object]:
    """Audit both singleton-h7 branches directly, without importing either theorem script."""
    p = 233
    e, f = (1, 0), (0, 1)
    t = sub((0, 0), add(e, f, p), p)
    domains_1 = support_domains_for_tail_pair(f, t, p)
    domains_2 = support_domains_for_tail_pair(e, t, p)
    domains_3 = support_domains_for_tail_pair(e, f, p)
    if tuple(map(len, (domains_1, domains_2, domains_3))) != (p + 1, p + 1, p + 1):
        raise AssertionError("wrong Property-B domain count")

    compatible = {
        (g1, g2)
        for g1, domain_1 in domains_1.items()
        for g2, domain_2 in domains_2.items()
        if g1 in domain_2 and g2 in domain_1
    }
    inv3 = pow(3, -1, p)
    expected = {
        (t, t),
        (t, sub(t, e, p)),
        (sub(t, f, p), t),
        (scale(inv3, sub(t, f, p), p), scale(inv3, sub(t, e, p), p)),
    }
    if compatible != expected:
        raise AssertionError(("wrong two-max compatibility locus", compatible, expected))
    mixed_contradictions = Counter()
    for g1, g2 in compatible:
        if t in (g1, g2):
            mixed_contradictions["e+f+t"] += 1
        elif g1 != g2 and add(g1, g2, p) == t:
            mixed_contradictions["e+f+g1+g2"] += 1
        else:
            raise AssertionError(("unclosed compatible pair", g1, g2))
    if mixed_contradictions != Counter({"e+f+t": 3, "e+f+g1+g2": 1}):
        raise AssertionError(mixed_contradictions)

    three_domain_intersection = (
        set().union(*domains_1.values())
        & set().union(*domains_2.values())
        & set().union(*domains_3.values())
    )
    if three_domain_intersection:
        raise AssertionError(("nonempty three-domain intersection", three_domain_intersection))

    ambient = 2 * p + 6
    union_778 = 1 + 6 + 6 + 7
    union_777 = 1 + 6 + 6 + 6
    intersection_778 = ambient - union_778
    intersection_777 = ambient - union_777
    if (ambient, intersection_778, intersection_777) != (472, 452, 453):
        raise AssertionError("wrong literal-intersection arithmetic")
    if intersection_778 < 435:
        raise AssertionError("mixed theorem kernel threshold not met")
    heavy_in_452_kernel = (p - 1) - ((2 * p - 1) - intersection_778)
    if heavy_in_452_kernel != 219:
        raise AssertionError(heavy_in_452_kernel)

    return {
        "p": p,
        "tail_coordinates": {"e": list(e), "f": list(f), "t": list(t)},
        "property_b_domains_per_tail_pair": p + 1,
        "two_max_compatible_heavy_pairs": len(compatible),
        "two_max_zero_sum_closures": dict(sorted(mixed_contradictions.items())),
        "three_domain_common_points": len(three_domain_intersection),
        "ambient_literal_positions": ambient,
        "shared_endpoint_position_union_bounds": {"7,7,8": union_778, "7,7,7": union_777},
        "literal_intersection_lower_bounds": {"7,7,8": intersection_778, "7,7,7": intersection_777},
        "directional_difference_upper_bound_for_two_length_7_endpoints": 6,
        "heavy_copies_forced_into_452_kernel": heavy_in_452_kernel,
        "all_common_position_labels_nonzero": "a zero label would be a proper one-term zero-sum in each atom",
    }


def main() -> None:
    actual_hashes = {
        "proof": file_hash(CANDIDATE_PROOF),
        "script": file_hash(CANDIDATE_SCRIPT),
        "report": file_hash(CANDIDATE_REPORT),
    }
    if actual_hashes != {k: EXPECTED_HASHES[k] for k in ("proof", "script", "report")}:
        raise AssertionError((actual_hashes, EXPECTED_HASHES))

    independent = independent_enumeration()
    expected_parent_keys = independent.pop("_parent_keys")
    expected_survivor_keys = independent.pop("_survivor_keys")
    report_validation = validate_candidate_report(
        independent, expected_parent_keys, expected_survivor_keys
    )
    property_b_application = independent_property_b_application()
    if independent["unlabelled_graph_count"] != 11:
        raise AssertionError(independent["unlabelled_graph_count"])
    if independent["distinct_trace_total"] != 36:
        raise AssertionError(independent["distinct_trace_total"])
    if (independent["decorated_total"], independent["eliminated_total"], independent["surviving_total"]) != (
        1440,
        720,
        720,
    ):
        raise AssertionError("wrong decorated denominator")

    audit_core = {
        "schema": "unique_tail_p233_length_decorated_trace_reduction/independent-audit-v1",
        "method": "fresh no-import graph, trace, and length-decoration reconstruction",
        "bound_candidate_hashes": actual_hashes,
        "bound_candidate_certificate": EXPECTED_HASHES["certificate"],
        "independent_enumeration": independent,
        "candidate_report_validation": report_validation,
        "independent_property_b_application": property_b_application,
        "literal_intersection_quantifiers": {
            "ambient_positions": 472,
            "three_endpoints_share_one_literal_position": True,
            "lengths_7_7_8_union_upper_bound": 20,
            "lengths_7_7_8_intersection_lower_bound": 452,
            "lengths_7_7_7_union_upper_bound": 19,
            "lengths_7_7_7_intersection_lower_bound": 453,
            "mixed_theorem_required_kernel": 435,
            "tail_pairs_follow_from_singleton_traces": True,
        },
        "outer_all_eight_scope": (
            "36 all-eight decorations satisfy only the outer graph/trace/length rules; "
            "they do not instantiate endpoint masks, shared labels, or atom oracles"
        ),
        "review_finding": (
            "All enumeration, row-completeness, literal-kernel quantifiers, Property-B support-domain "
            "applications, dependency hashes, and outer-witness scope check independently."
        ),
        "status": "CORRECT",
    }
    audit_core["certificate_sha256"] = canonical_hash(audit_core)
    AUDIT_REPORT.write_text(
        json.dumps(audit_core, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit_core, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
