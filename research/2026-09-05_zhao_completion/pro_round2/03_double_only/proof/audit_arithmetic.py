#!/usr/bin/env python3
"""Auxiliary arithmetic audit of the hand proof. No search over sequences.

This script does NOT certify exhaustion of F_5^4 sequences. The mathematical
proof in proof_zh.md supplies the universal arguments; this script audits
finite arithmetic and positional incidence interfaces only.
"""
from itertools import product
from math import comb
import json
from pathlib import Path

P = 5
OUT = Path(__file__).with_name('arithmetic_audit.json')


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    data = {'purpose': 'auxiliary arithmetic, not a sequence classification',
            'field_characteristic': P}
    data['group_ring'] = []
    for d in (3, 4):
        degrees = [sum(t) for t in product(range(P), repeat=d)]
        check(max(degrees) == 4*d, 'augmentation degree')
        data['group_ring'].append({'rank': d, 'basis_monomials': len(degrees),
                                  'maximum_degree': max(degrees),
                                  'nilpotency_exponent': 4*d+1})

    # An 18-position height-at-most-two sequence with no zero of length <=15.
    alternatives = [(a, b) for a in range(3) for b in range(2)
                    if (1 + a - b) % P == 0]
    check(alternatives == [(0, 1)], '18-position integer/modular interface')
    data['eighteen_position_pairs_Z16_Z17'] = alternatives

    # The three-position core a,a,2a covers the entire anchor line.
    core = (1, 1, 2)
    witnesses = {}
    for mask in range(1 << 3):
        residue = sum(core[i] for i in range(3) if mask >> i & 1) % P
        size = mask.bit_count()
        if residue not in witnesses or size < witnesses[residue]['length']:
            witnesses[residue] = {'mask': mask, 'length': size}
    check(set(witnesses) == set(range(P)), 'anchor core coverage')
    check(max(w['length'] for w in witnesses.values()) == 3, 'anchor core capacity')
    data['core_coverage'] = witnesses

    allowed = []
    for c in range(P):
        cancellers = [k for k in range(3) if (c+k) % P == 0]
        if not cancellers:
            allowed.append(c)
        else:
            check(11 + min(cancellers) <= 13, 'two-anchor length bound')
    check(allowed == [1, 2], 'short quotient-zero lift residues')
    check(not set(allowed).intersection({(-c) % P for c in allowed}),
          'balanced complements')
    data['allowed_short_lifts'] = allowed
    data['balanced_forbidden_intervals'] = {str(n): list(range(n-11, 12))
                                            for n in (14, 15)}
    check(data['balanced_forbidden_intervals']['14'] == list(range(3, 12)), 'n14 range')
    check(data['balanced_forbidden_intervals']['15'] == list(range(4, 12)), 'n15 range')

    # Complete component types of a fixed-sum position graph at height <=2.
    components = []
    for u, v in product((1, 2), repeat=2):
        edges, matching = u*v, min(u, v)
        check(edges <= 2*matching, 'fixed-sum bipartite component bound')
        components.append({'type': f'K{u},{v}', 'edges': edges, 'matching': matching})
    components.append({'type': 'half-value K2', 'edges': 1, 'matching': 1})
    data['fixed_sum_components'] = components

    # Fourteen-position quotient zero: e is at most two and is 4 mod 5.
    possible14 = [e for e in range(3) if (2 + 2*e) % P == 0]
    check(possible14 == [], '14-position contradiction')
    data['n14_possible_pair_counts'] = possible14

    # Fifteen-position quotient zero: f=-e and f_i-e_i=-e+2 (mod 5).
    # These coefficients are independently reconstructed in verify_positions.py.
    branch_data = []
    for e in range(5):
        f_res = (-e) % P
        c = ((f_res-e-1) * pow(2, -1, P)) % P
        check(c == (4*e+2) % P, '15-position degree congruence')
        general_outside_degrees = [d for d in range(9) if d % P == c]
        branch_data.append({'e': e, 'f_mod_5': f_res,
                           '(f_i-e_i)_mod_5': c,
                           'outside_degree_candidates_up_to_8': general_outside_degrees})
    check(branch_data[0]['outside_degree_candidates_up_to_8'] == [2, 7], 'e0')
    check(14*2 > 2*7, 'e0 degree-seven star contradiction')
    check(15*comb(2, 2) < comb(10, 2), 'e0 intersecting-family contradiction')
    check([d for d in range(5) if d % P == 1] == [1], 'e1 outside bound')
    check(13 % 2 == 1, 'e1 parity contradiction')
    check([d for d in range(4) if d % P == 0] == [0], 'e2 outside bound')
    check(0 != (-2) % P, 'e2 total-triple contradiction')
    check([d for d in range(3) if d % P == 4] == [], 'e3 outside bound')
    check([d for d in range(3) if d % P == 3] == [], 'e4 outside bound')
    data['n15_branches'] = branch_data

    # All original deletion-layer equations, independent of b.
    matrices = {}
    for n in range(17, 22):
        rows = []
        for k in range(17, n+1):
            coeffs = [((-1)**j * comb(n-j, k-j)) % P if j <= k else 0
                      for j in range(14, 18)]
            rows.append({'retained_positions': k, 'constant': comb(n, k) % P,
                         'Z14_Z15_Z16_Z17': coeffs})
        matrices[str(n)] = rows
    data['deletion_matrices'] = matrices

    cases = []
    for b in range(1, 7):
        single = 21 - 2*b
        check(2*b + single == 21, 'frozen position denominator')
        cases.append({'b': b, 'single_values': single, 'support': 21-b,
                      'delete_double_position_choices': 2*b,
                      'after_delete_double': {'doubles': b-1, 'singles': single+1},
                      'delete_single_position_choices': single,
                      'after_delete_single': {'doubles': b, 'singles': single-1},
                      'after_remove_both_anchors': {'doubles': b-1, 'singles': single}})
    data['frozen_cases'] = cases
    data['checks_passed'] = True
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ARITHMETIC_AUDIT_OK')
    print('group_ring_ranks=3,4; frozen_b_cases=6; n14_branches=1; n15_branches=5')
    print('This is an auxiliary audit, not an exhaustive sequence search.')


if __name__ == '__main__':
    main()
