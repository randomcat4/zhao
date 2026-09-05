"""Finite sanity checker for the 16-atom pair-star paper proof.

This enumerates only tiny abstract graph and multiplicity types. It is not a
search for a B20 counterexample and imports no project search implementation.
"""
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def digest(name):
    return sha256((BASE / name).read_bytes()).hexdigest()


def integer_partitions_four(max_part=3):
    result = []
    def visit(left, ceiling, row):
        if left == 0:
            result.append(tuple(row))
            return
        for value in range(min(left, ceiling, max_part), 0, -1):
            visit(left-value, value, row+[value])
    visit(4, 4, [])
    return result


def star(center, leaves):
    return frozenset(frozenset((center, leaf)) for leaf in leaves)


def cross_intersect(first, second):
    return all(a & b for a in first for b in second)


def main():
    # All nonempty value-component types possible under multiplicity at most 3.
    components = []
    for r in range(1, 4):
        for s in range(r, 4):
            components.append({'kind': f'K{r},{s}', 'edges': r*s,
                               'matching': r, 'triangle': False,
                               'star': r == 1})
    for r in (2, 3):
        components.append({'kind': f'half_K{r}', 'edges': r*(r-1)//2,
                           'matching': r//2, 'triangle': r == 3,
                           'star': False})
    # A matching budget of 2 permits at most two nonempty components.
    compound = []
    for count in (1, 2):
        for indices in combinations(range(len(components)), count):
            # Add repeated types separately below.
            row = [components[i] for i in indices]
            compound.append(row)
    compound += [[c, c] for c in components]
    seen = set()
    possibilities = []
    for row in compound:
        key = tuple(sorted(c['kind'] for c in row))
        if key in seen:
            continue
        seen.add(key)
        edges = sum(c['edges'] for c in row)
        matching = sum(c['matching'] for c in row)
        if matching > 2:
            continue
        for m in range(3):
            if edges % 5 == (m+2) % 5:
                possibilities.append({'m': m, 'components': key,
                                      'edges': edges, 'matching': matching})
    assert possibilities and all(row['edges'] <= 6 for row in possibilities)
    survivors = [row for row in possibilities
                 if row['matching'] <= 1
                 and not any(name == 'half_K3' for name in row['components'])]
    assert survivors == [
        {'m': 0, 'components': ('K1,2',), 'edges': 2, 'matching': 1},
        {'m': 1, 'components': ('K1,3',), 'edges': 3, 'matching': 1},
    ]

    # Set-system check behind the common-center lemma.
    vertices = range(7)
    stars = []
    for center in vertices:
        rest = [v for v in vertices if v != center]
        for degree in (2, 3):
            for leaves in combinations(rest, degree):
                stars.append((center, leaves, star(center, leaves)))
    cross_pairs = 0
    different_center_pairs = 0
    for i, first in enumerate(stars):
        for second in stars[i+1:]:
            if not cross_intersect(first[2], second[2]):
                continue
            cross_pairs += 1
            if first[0] != second[0]:
                different_center_pairs += 1
                assert first[2] & second[2]  # shared positional edge => equal sum label

    # Squarefree matching alternatives.
    f2 = frozenset((frozenset((0, 1)), frozenset((2, 3))))
    all_edges4 = [frozenset(e) for e in combinations(range(4), 2)]
    cross_matchings = []
    for pair in combinations(all_edges4, 2):
        family = frozenset(pair)
        if pair[0] & pair[1]:
            continue
        if cross_intersect(f2, family):
            cross_matchings.append(sorted(sorted(e) for e in family))
    assert cross_matchings == [[[0, 2], [1, 3]], [[0, 3], [1, 2]]]
    f3 = frozenset((frozenset((0, 1)), frozenset((2, 3)), frozenset((4, 5))))
    assert not any(all(edge & old for old in f3) for edge in map(frozenset, combinations(range(6), 2)))

    residual_types = []
    quotient_types = set()
    for ks in integer_partitions_four():
        for ms in product((0, 1), repeat=len(ks)):
            if any(k+m > 3 for k, m in zip(ks, ms)):
                continue
            M = sum(ms)
            forced_excess = 4+2*M
            if forced_excess > 7:
                continue
            d = len(ks)
            row = {'R_multiplicities': ks, 'm_in_T': ms, 'M': M,
                   'forced_excess': forced_excess,
                   'remaining_excess_budget': 7-forced_excess,
                   'forced_T_positions': 1+2*d+2*M,
                   'W_length': 15-2*d-2*M}
            assert row['forced_T_positions'] + row['W_length'] == 16
            residual_types.append(row)
            quotient_types.add((ks, tuple(sorted(zip(ks, ms), reverse=True))))
    assert integer_partitions_four() == [(3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)]
    assert len(residual_types) == 14
    # Canonicalize m placements within equal k parts.
    canonical = {(row['R_multiplicities'], tuple(sorted(zip(row['R_multiplicities'], row['m_in_T']), reverse=True)))
                 for row in residual_types}
    assert len(canonical) == 9
    assert all(row['M'] <= 1 for row in residual_types)

    inputs = [
        'frozen_theorem_v1.md', 'proofs/atom_structure.md',
        'proofs/global_continue_squarefree_B.md',
        'proofs/global_continue_support18_B.md',
        'proofs/continue_atom16_star.md',
        'scripts/continue_atom16_star_graphs.py',
    ]
    output = {
        'status': 'TINY_GRAPH_AND_RESIDUAL_ACCOUNTING_PASS',
        'scope': 'Abstract graph types and integer accounting only; not an F5^4 search',
        'component_possibilities_before_structural_exclusions': possibilities,
        'surviving_pair_graph_types': survivors,
        'cross_intersecting_star_pairs_checked': cross_pairs,
        'different_center_cross_pairs_all_share_an_edge': different_center_pairs,
        'squarefree_two_by_two_cross_matchings': cross_matchings,
        'squarefree_three_edge_family_has_crossing_edge': False,
        'labelled_residual_types': residual_types,
        'labelled_type_count': len(residual_types),
        'types_mod_equal_multiplicity_symmetry': len(canonical),
        'input_sha256': {name: digest(name) for name in inputs},
    }
    target = BASE/'evidence/continue_atom16_star_graphs.json'
    target.write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    for name, expected in output['input_sha256'].items():
        assert digest(name) == expected
    print(json.dumps({k: output[k] for k in (
        'status', 'cross_intersecting_star_pairs_checked',
        'labelled_type_count', 'types_mod_equal_multiplicity_symmetry')}))


if __name__ == '__main__':
    main()
