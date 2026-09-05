#!/usr/bin/env python3
"""Independent positional incidence audit. Uses bitmasks, not binomial formulas.

No import of audit_arithmetic.py and no reading of its output is performed.
No claim of global sequence enumeration is made.
"""
from itertools import combinations, product


def check(ok, msg):
    if not ok:
        raise AssertionError(msg)


def masks(n, k):
    for c in combinations(range(n), k):
        yield sum(1 << i for i in c)


def matching_number(n, edges):
    # Independent recursive maximum matching, adequate for components <=4 vertices.
    edges = tuple(edges)
    def rec(used, start):
        best = 0
        for j in range(start, len(edges)):
            mask = (1 << edges[j][0]) | (1 << edges[j][1])
            if not used & mask:
                best = max(best, 1 + rec(used | mask, j+1))
        return best
    return rec(0, 0)


def main():
    # n=14: pairs and their 12-position complements have equal positive signs.
    full14 = (1 << 14) - 1
    pairs14 = 0
    for pair in masks(14, 2):
        complement = full14 ^ pair
        check(complement.bit_count() == 12, '14 complement length')
        check((-1)**pair.bit_count() + (-1)**complement.bit_count() == 2,
              '14 pair-orbit contribution')
        pairs14 += 1
    check(pairs14 == 91, '14 pair denominator')

    # n=15: deletion of a particular position changes pair contribution to
    # 1-2*incidence, and triple contribution to -1+2*incidence.
    full15 = (1 << 15) - 1
    records = 0
    for k, expected_total_mod in ((2, 1), (3, 1)):
        for block in masks(15, k):
            complement = full15 ^ block
            total = 0
            for p in range(15):
                bit = 1 << p
                contribution = 0
                if not block & bit:
                    contribution += (-1)**block.bit_count()
                if not complement & bit:
                    contribution += (-1)**complement.bit_count()
                incident = int(bool(block & bit))
                expected = (1-2*incident) if k == 2 else (-1+2*incident)
                check(contribution == expected, '15 deletion coefficient')
                total += contribution
                records += 1
            check(total % 5 == expected_total_mod, 'sum over deleted positions')
    check(records == 8400, '15 incidence denominator')

    # Check all small fixed-sum component capacities independently by matching.
    component_count = 0
    for left in (1, 2):
        for right in (1, 2):
            edges = [(i, left+j) for i in range(left) for j in range(right)]
            nu = matching_number(left+right, edges)
            check(len(edges) <= 2*nu, 'bipartite component matching bound')
            component_count += 1
    check(matching_number(2, [(0, 1)]) == 1, 'half-value component')
    component_count += 1

    # Audit characteristic-five branch residues without modular inverses.
    rows = []
    for e in range(5):
        alternatives = []
        for f in range(5):
            for c in range(5):
                if (3*f-2*e) % 5 == 0 and (1+e-f+2*c) % 5 == 0:
                    alternatives.append((f, c))
        check(len(alternatives) == 1, 'unique degree residue')
        rows.append((e,) + alternatives[0])
    check(rows == [(0, 0, 2), (1, 4, 1), (2, 3, 0), (3, 2, 4), (4, 1, 3)],
          'all five pair-count branches')

    # Every pair of triples meets at a position. The incidence argument at e=0
    # counts unordered pairs of triples at each common vertex.
    intersections_needed = sum(1 for _ in combinations(range(10), 2))
    intersections_available = sum(sum(1 for _ in combinations(range(2), 2))
                                  for _ in range(15))
    check(intersections_needed == 45 and intersections_available == 15,
          'intersecting-triple incidence counts')

    print('POSITIONAL_AUDIT_OK')
    print(f'n14_pair_orbits={pairs14}; n15_deleted_position_incidences={records}')
    print(f'fixed_sum_component_types={component_count}; e_branches={len(rows)}')
    print('No global sequence-enumeration claim is made.')


if __name__ == '__main__':
    main()
