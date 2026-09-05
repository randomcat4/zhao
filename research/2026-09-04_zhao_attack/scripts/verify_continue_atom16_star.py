"""Independent finite checks for proofs/continue_atom16_star.md.

The checks here concern only the small position-graph classifications, the
F_5 linear identities used in the matching argument, and the residual
multiplicity bookkeeping.  They do not search for sequences in F_5^4.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]


def file_hash(relative: str) -> str:
    return sha256((BASE / relative).read_bytes()).hexdigest()


def cross_intersect(first, second) -> bool:
    return all(set(edge_a) & set(edge_b) for edge_a in first for edge_b in second)


def make_star(center: int, leaves) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(sorted((center, leaf))) for leaf in leaves)


def graph_classification() -> dict:
    # Directly enumerate every simple graph on six labelled positions.  A graph
    # of matching number one has all pairs of edges intersecting.
    vertices = range(6)
    all_edges = list(combinations(vertices, 2))
    checked = 0
    pairwise_intersecting = 0
    stars = 0
    triangles = 0
    for mask in range(1 << len(all_edges)):
        edges = [all_edges[i] for i in range(len(all_edges)) if mask >> i & 1]
        if len(edges) < 2:
            continue
        checked += 1
        if not all(set(a) & set(b) for a, b in combinations(edges, 2)):
            continue
        pairwise_intersecting += 1
        common = set(edges[0])
        for edge in edges[1:]:
            common &= set(edge)
        if common:
            stars += 1
            continue
        support = set().union(*(set(edge) for edge in edges))
        assert len(edges) == 3
        assert len(support) == 3
        assert set(edges) == set(combinations(sorted(support), 2))
        triangles += 1
    return {
        "graphs_with_at_least_two_edges_checked": checked,
        "matching_number_one_graphs": pairwise_intersecting,
        "stars": stars,
        "triangles": triangles,
    }


def component_and_congruence_check() -> dict:
    # Nonempty fixed-sum components under value-class capacity at most three.
    components = []
    for r in range(1, 4):
        for s in range(r, 4):
            components.append((f"K{r},{s}", r * s, r, False))
    components.extend(
        [
            ("half_K2", 1, 1, False),
            ("half_K3", 3, 1, True),
        ]
    )

    admissible = []
    for number_of_components in (1, 2):
        for rows in combinations_with_replacement(components, number_of_components):
            matching = sum(row[2] for row in rows)
            if matching > 2:
                continue
            edges = sum(row[1] for row in rows)
            assert edges <= 6
            for multiplicity_in_atom in range(3):
                if edges % 5 == (multiplicity_in_atom + 2) % 5:
                    admissible.append(
                        {
                            "m": multiplicity_in_atom,
                            "components": tuple(row[0] for row in rows),
                            "edges": edges,
                            "matching": matching,
                            "contains_triangle": any(row[3] for row in rows),
                        }
                    )

    survivors = [
        row
        for row in admissible
        if row["matching"] == 1 and not row["contains_triangle"]
    ]
    assert survivors == [
        {
            "m": 0,
            "components": ("K1,2",),
            "edges": 2,
            "matching": 1,
            "contains_triangle": False,
        },
        {
            "m": 1,
            "components": ("K1,3",),
            "edges": 3,
            "matching": 1,
            "contains_triangle": False,
        },
    ]
    return {
        "congruence_compatible_component_types": len(admissible),
        "survivors_after_matching_two_and_triangle_exclusions": survivors,
    }


def matching_algebra_over_f5() -> dict:
    adjacent = 0
    disjoint_one = 0
    disjoint_two = 0
    triangles = 0
    for a, b, c, d in product(range(5), repeat=4):
        g = (a + b) % 5
        if (c + d) % 5 != g:
            continue

        # Adjacent cross edges {a,c} and {a,d} have a common target sum.
        if (a + c) % 5 == (a + d) % 5:
            adjacent += 1
            assert c == d
            assert g == 2 * c % 5

        # The two possible disjoint cross perfect matchings force h=g.
        if (a + c) % 5 == (b + d) % 5:
            disjoint_one += 1
            assert (a + c) % 5 == g
            assert b == c and a == d
        if (a + d) % 5 == (b + c) % 5:
            disjoint_two += 1
            assert (a + d) % 5 == g
            assert b == d and a == c

    for a, b, c in product(range(5), repeat=3):
        if (a + b) % 5 == (a + c) % 5 == (b + c) % 5:
            triangles += 1
            assert a == b == c
            assert (a + b) % 5 == 2 * a % 5

    return {
        "adjacent_cross_equation_solutions": adjacent,
        "first_cross_perfect_matching_solutions": disjoint_one,
        "second_cross_perfect_matching_solutions": disjoint_two,
        "triangle_equation_solutions": triangles,
    }


def common_center_check() -> dict:
    vertices = range(7)
    stars = []
    for center in vertices:
        others = [vertex for vertex in vertices if vertex != center]
        for degree in (2, 3):
            for leaves in combinations(others, degree):
                stars.append((center, make_star(center, leaves)))

    cross_pairs = 0
    distinct_target_pairs = 0
    distinct_target_different_centers = 0
    for first, second in combinations(stars, 2):
        if not cross_intersect(first[1], second[1]):
            continue
        cross_pairs += 1
        # Distinct target sums cannot label the same positional edge.
        if first[1].isdisjoint(second[1]):
            distinct_target_pairs += 1
            if first[0] != second[0]:
                distinct_target_different_centers += 1
    assert distinct_target_different_centers == 0
    return {
        "cross_intersecting_star_pairs": cross_pairs,
        "cross_intersecting_edge_disjoint_pairs": distinct_target_pairs,
        "edge_disjoint_pairs_with_different_centers": 0,
    }


def residual_accounting_check() -> dict:
    partitions = [(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)]
    rows = []
    canonical = set()
    for ks in partitions:
        for ms in product((0, 1), repeat=len(ks)):
            if any(k + m > 3 for k, m in zip(ks, ms)):
                continue
            M = sum(ms)
            forced_excess = 4 + 2 * M
            if forced_excess > 7:
                continue
            d = len(ks)
            forced_positions = 1 + 2 * d + 2 * M
            w_length = 15 - 2 * d - 2 * M
            assert forced_positions + w_length == 16
            assert M <= 1

            # Symbolic coefficients in the forced part of T:
            # x + sum m_i(x+y_i) + sum(m_i+2)y_i.
            assert 1 + sum(ms) == M + 1
            assert all(m + (m + 2) == 2 * (m + 1) for m in ms)

            rows.append(
                {
                    "k": ks,
                    "m": ms,
                    "M": M,
                    "forced_excess": forced_excess,
                    "remaining_excess_budget": 7 - forced_excess,
                    "W_length": w_length,
                }
            )
            canonical.add((ks, tuple(sorted(zip(ks, ms), reverse=True))))

    assert len(rows) == 14
    assert len(canonical) == 9
    return {
        "labelled_rows": len(rows),
        "rows_mod_equal_part_symmetry": len(canonical),
        "rows": rows,
    }


def squarefree_matching_check() -> dict:
    first_two = frozenset({(0, 1), (2, 3)})
    candidates = []
    all_edges = list(combinations(range(6), 2))
    for two_edges in combinations(all_edges, 2):
        if set(two_edges[0]) & set(two_edges[1]):
            continue
        family = frozenset(two_edges)
        if cross_intersect(first_two, family):
            candidates.append(sorted(family))
    assert candidates == [[(0, 2), (1, 3)], [(0, 3), (1, 2)]]

    first_three = frozenset({(0, 1), (2, 3), (4, 5)})
    assert not any(cross_intersect(first_three, [edge]) for edge in all_edges)
    return {
        "two_by_two_cross_matchings": candidates,
        "edges_meeting_three_disjoint_edges": 0,
    }


def main() -> None:
    audited_inputs = [
        "proofs/continue_atom16_star.md",
        "proofs/atom_structure.md",
        "scripts/continue_atom16_star_graphs.py",
        "scripts/verify_continue_atom16_star.py",
    ]
    output = {
        "status": "PASS_WITH_SCOPE_LIMIT",
        "scope": (
            "Independent small finite checks only; the actual-position use of "
            "the three-position line lemma is audited in the prose report"
        ),
        "graph_classification": graph_classification(),
        "component_and_congruence": component_and_congruence_check(),
        "matching_algebra_over_f5": matching_algebra_over_f5(),
        "common_center": common_center_check(),
        "residual_accounting": residual_accounting_check(),
        "squarefree_matching": squarefree_matching_check(),
        "input_sha256": {name: file_hash(name) for name in audited_inputs},
    }
    target = BASE / "evidence/verify_continue_atom16_star.json"
    target.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": output["status"],
                "matching_number_one_graphs": output["graph_classification"][
                    "matching_number_one_graphs"
                ],
                "common_center_edge_disjoint_counterexamples": output[
                    "common_center"
                ]["edge_disjoint_pairs_with_different_centers"],
                "labelled_residual_rows": output["residual_accounting"][
                    "labelled_rows"
                ],
            }
        )
    )


if __name__ == "__main__":
    main()
