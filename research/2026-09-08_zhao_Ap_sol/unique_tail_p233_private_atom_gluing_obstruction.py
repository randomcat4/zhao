#!/usr/bin/env python3
"""Exact checks for the decoupled-atom gluing obstruction at p=233.

This is deliberately a RELAXED model.  The three maximal atoms use private
C_p^2 label maps which agree on the tail positions but not on the common
kernel.  A separate global C_p^3 label map realizes the endpoint incidence
and has no quotient-zero block of length eight.  Thus the script does not
claim a model of the exact slice.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


P = 233
HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_p233_private_atom_gluing_obstruction_report.json"


def add2(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)


def add3(x: tuple[int, int, int], y: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((a + b) % P for a, b in zip(x, y))  # type: ignore[return-value]


def sum3(labels: dict[str, tuple[int, int, int]], positions: set[str]) -> tuple[int, int, int]:
    out = (0, 0, 0)
    for position in positions:
        out = add3(out, labels[position])
    return out


def span(g: tuple[int, int]) -> set[tuple[int, int]]:
    return {((c * g[0]) % P, (c * g[1]) % P) for c in range(P)}


def translate(a: tuple[int, int], subset: set[tuple[int, int]]) -> set[tuple[int, int]]:
    return {add2(a, x) for x in subset}


def standard_domains(a: tuple[int, int], b: tuple[int, int]) -> list[frozenset[tuple[int, int]]]:
    """All support domains for a p-1 repeated-term normal form containing a,b."""
    out: set[frozenset[tuple[int, int]]] = set()

    # Repeated term is one of the two prescribed terms.
    out.add(frozenset({a} | translate(b, span(a))))
    out.add(frozenset({b} | translate(a, span(b))))

    # Otherwise the two terms lie on the same affine line parallel to g.
    delta = ((b[0] - a[0]) % P, (b[1] - a[1]) % P)
    affine = translate(a, span(delta))
    for c in range(1, P):
        g = ((c * delta[0]) % P, (c * delta[1]) % P)
        out.add(frozenset({g} | affine))
    return sorted(out, key=lambda domain: sorted(domain))


def main() -> None:
    u = {f"u{i}" for i in range(1, 4)}
    petals = {i: {f"a{i}_{j}" for j in range(1, 6)} for i in range(1, 4)}
    y = "y"
    pset = {"p1", "p2"}
    kernel = {f"k{j:03d}" for j in range(1, 454)}
    universe = u | {y} | pset | kernel | set().union(*petals.values())

    endpoints = {i: {f"u{i}", y} | petals[i] for i in range(1, 4)}
    long_atoms = {i: universe - endpoints[i] - pset for i in range(1, 4)}
    common_kernel = set.intersection(*(long_atoms[i] for i in range(1, 4)))

    assert len(universe) == 474
    assert all(len(endpoints[i]) == 7 for i in range(1, 4))
    assert common_kernel == kernel and len(common_kernel) == 453
    assert all(len(long_atoms[i]) == 465 for i in range(1, 4))
    for i, j in itertools.combinations(range(1, 4), 2):
        assert len(long_atoms[i] - long_atoms[j]) == 6
        assert len(long_atoms[i] ^ long_atoms[j]) == 12
        assert endpoints[i] & endpoints[j] == {y}

    w = {1: (1, 0), 2: (0, 1), 3: (P - 1, P - 1)}
    assert add2(add2(w[1], w[2]), w[3]) == (0, 0)

    # A single global C_p^3 table.  Its q-coordinate is chosen so that the
    # endpoints sum to zero, P sums to 3q, and Y sums to 4q.
    c = pow(451, -1, P)
    assert c == 31
    global_labels: dict[str, tuple[int, int, int]] = {}
    for position in universe - u - pset:
        global_labels[position] = (c, 0, 0)
    for i in range(1, 4):
        global_labels[f"u{i}"] = ((-6 * c) % P, w[i][0], w[i][1])
    global_labels["p1"] = (4, 0, 0)
    global_labels["p2"] = (P - 1, 0, 0)

    # Give the common intersection y nonzero tail projection, then compensate
    # once inside each petal and once inside K.
    r = (1, 0)
    global_labels[y] = (c, r[0], r[1])
    for i in range(1, 4):
        first = f"a{i}_1"
        global_labels[first] = (
            c,
            (-w[i][0] - r[0]) % P,
            (-w[i][1] - r[1]) % P,
        )
    global_labels["k001"] = (c, (2 * r[0]) % P, (2 * r[1]) % P)

    assert all(sum3(global_labels, endpoints[i]) == (0, 0, 0) for i in range(1, 4))
    assert sum3(global_labels, pset) == (3, 0, 0)
    assert sum3(global_labels, universe) == (4, 0, 0)
    assert global_labels[y][1:] != (0, 0)

    # The q-coordinate alone excludes every global quotient-zero 8-block.
    q_coordinate_cases: list[dict[str, object]] = []
    for tail_subset_size in range(0, 4):
        for picked_p1 in (0, 1):
            for picked_p2 in (0, 1):
                special_count = tail_subset_size + picked_p1 + picked_p2
                ordinary_count = 8 - special_count
                if ordinary_count < 0 or ordinary_count > len(universe - u - pset):
                    continue
                q_sum = (
                    ordinary_count * c
                    + tail_subset_size * ((-6 * c) % P)
                    + 4 * picked_p1
                    - picked_p2
                ) % P
                assert q_sum != 0
                q_coordinate_cases.append(
                    {
                        "tail_count": tail_subset_size,
                        "picked_p1": picked_p1,
                        "picked_p2": picked_p2,
                        "ordinary_count": ordinary_count,
                        "q_sum": q_sum,
                    }
                )
    assert len(q_coordinate_cases) == 16

    # Three private atom tables.  They agree on the prescribed tail positions,
    # but they are not restrictions of the global table on the common kernel.
    tail_pairs = {1: (2, 3), 2: (1, 3), 3: (1, 2)}
    private_labels: dict[int, dict[str, tuple[int, int]]] = {}
    atom_summaries: dict[str, object] = {}
    for i, (j, k) in tail_pairs.items():
        g, h = w[j], w[k]
        labels: dict[str, tuple[int, int]] = {f"u{j}": g, f"u{k}": h}
        remaining = sorted(long_atoms[i] - {f"u{j}", f"u{k}"})
        assert len(remaining) == 463
        for position in remaining[:231]:
            labels[position] = g
        for position in remaining[231:462]:
            labels[position] = h
        labels[remaining[462]] = add2(g, h)
        assert set(labels) == long_atoms[i]

        multiplicities = Counter(labels.values())
        assert multiplicities == Counter({g: 232, h: 232, add2(g, h): 1})
        total = (0, 0)
        for label in labels.values():
            total = add2(total, label)
        assert total == (0, 0)

        # Exact atom check for g^(p-1) h^(p-1) (g+h): c=0 forces
        # a=b=0; c=1 forces a=b=p-1.
        zero_count_solutions = []
        for last in (0, 1):
            a = (-last) % P
            b = (-last) % P
            if 0 <= a <= P - 1 and 0 <= b <= P - 1:
                zero_count_solutions.append((a, b, last))
        assert zero_count_solutions == [(0, 0, 0), (232, 232, 1)]

        private_labels[i] = labels
        atom_summaries[str(i)] = {
            "tail_pair": [f"u{j}", f"u{k}"],
            "basis": [list(g), list(h)],
            "multiplicities": [232, 232, 1],
            "zero_count_solutions": [list(x) for x in zero_count_solutions],
        }

    for tail_index in range(1, 4):
        position = f"u{tail_index}"
        appearances = [private_labels[i][position] for i in range(1, 4) if position in private_labels[i]]
        assert appearances == [w[tail_index], w[tail_index]]

    pairwise_kernel_disagreements = {}
    for i, j in itertools.combinations(range(1, 4), 2):
        disagreements = sum(private_labels[i][position] != private_labels[j][position] for position in kernel)
        assert disagreements > 0
        pairwise_kernel_disagreements[f"{i}-{j}"] = disagreements

    # If all three genuine, globally glued atoms had a term repeated p-1
    # times, their standard support domains would contain every common K label.
    # The three possible-domain unions have empty triple intersection.
    pair_vectors = [(w[2], w[3]), (w[1], w[3]), (w[1], w[2])]
    domains = [standard_domains(a, b) for a, b in pair_vectors]
    possible_support = [set().union(*family) for family in domains]
    triple_support_intersection = set.intersection(*possible_support)
    assert triple_support_intersection == set()

    report = {
        "scope": "RELAXED_PRIVATE_ATOM_LABELS_NOT_GLOBALLY_GLUED",
        "status": "EXPLICIT_RELAXED_MODEL/GLOBAL_INCOMPLETE",
        "p": P,
        "incidence": {
            "universe_size": len(universe),
            "endpoint_sizes": [len(endpoints[i]) for i in range(1, 4)],
            "long_atom_sizes": [len(long_atoms[i]) for i in range(1, 4)],
            "common_kernel_size": len(common_kernel),
            "one_sided_pair_differences": [
                len(long_atoms[i] - long_atoms[j]) for i, j in itertools.combinations(range(1, 4), 2)
            ],
        },
        "global_table": {
            "ordinary_q_coordinate": c,
            "endpoint_sums": [list(sum3(global_labels, endpoints[i])) for i in range(1, 4)],
            "P_sum": list(sum3(global_labels, pset)),
            "Y_sum": list(sum3(global_labels, universe)),
            "tail_projections": [list(w[i]) for i in range(1, 4)],
            "length_8_q_coordinate_cases": q_coordinate_cases,
            "length_8_quotient_zero_count": 0,
        },
        "private_atoms": atom_summaries,
        "private_label_disagreements_on_K": pairwise_kernel_disagreements,
        "p_minus_1_repeated_term_barrier": {
            "domain_family_counts": [len(family) for family in domains],
            "possible_support_union_sizes": [len(support) for support in possible_support],
            "triple_intersection_size": len(triple_support_intersection),
            "consequence": "Any globally glued genuine triple with nonempty K has at least one atom of maximum term multiplicity at most p-2.",
        },
        "missing_gluing_axiom": "For every i and every position v in Q_i, the private atom label eta_i(v) must equal rho(bar_gamma(v)) for one common global label table.",
        "not_checked": [
            "global Q_i atomhood",
            "mixed P-Q targets",
            "the full automatic short spectrum and middle gap",
            "Hasse congruences",
            "actual C_p^4 lifts, multiplicity cap, and Z atomhood",
        ],
        "not_claimed": ["exact-slice SAT", "exact-slice UNSAT", "global A_p"],
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    report["certificate_sha256"] = hashlib.sha256(canonical).hexdigest()
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
