#!/usr/bin/env python3
"""Exact local checks for ROUND3_THEOREMS.md, not a complete search for B_p.

Requires Python >=3.10 and NumPy. Run:
  python audit_round3.py --output audit_results.json

The group computations count position subsets over the integers. The capacity
checks solve finite-field systems using an inverse recurrence, not the closed
root formula in the manuscript. No previous audit tables are read.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
from time import perf_counter
import numpy as np


def primes_up_to(n: int) -> list[int]:
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[:2] = b'\x00\x00'
    for a in range(2, int(n**0.5) + 1):
        if sieve[a]:
            sieve[a*a:n+1:a] = b'\x00' * (((n-a*a)//a)+1)
    return [a for a in range(2, n+1) if sieve[a]]


def rank_mod(rows: list[list[int]], p: int) -> int:
    if not rows:
        return 0
    a = [[int(x) % p for x in row] for row in rows]
    nr, nc, rr = len(a), len(a[0]), 0
    for c in range(nc):
        pivot = next((i for i in range(rr, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[rr], a[pivot] = a[pivot], a[rr]
        inv = pow(a[rr][c], -1, p)
        a[rr] = [(x*inv) % p for x in a[rr]]
        for i in range(rr+1, nr):
            fac = a[i][c]
            if fac:
                a[i] = [(x-fac*y) % p for x,y in zip(a[i], a[rr])]
        rr += 1
        if rr == nr:
            break
    return rr


def inverse_convolution(q: list[int], m: int, p: int) -> list[int]:
    """Solve q=(1-z)^m h coefficient by coefficient, in F_p."""
    h: list[int] = []
    for b, val in enumerate(q):
        val -= sum(((-1)**u)*comb(m,u)*h[b-u]
                   for u in range(1, min(m,b)+1))
        h.append(val % p)
    return h


def capacity_checks() -> dict:
    closed_cases = 0
    for p in primes_up_to(101):
        if p < 5:
            continue
        for m in range(p-2):
            r = p-2-m
            q = [(1-(m+1)*b) % p for b in range(r+1)]
            h = inverse_convolution(q, m, p)
            for t in range(r+1):
                assert h[t] == ((1-t)*comb(m+t,t)) % p
                closed_cases += 1
    systems = 0
    by_prime = []
    for p in primes_up_to(31):
        if p < 5:
            continue
        per_p = 0
        for n in range(1, p-1):
            c = p-n
            for r in range(1, n+1):
                m = n-r
                for d in range(1, p-3):
                    if r < c+d-1:
                        continue
                    cols = []
                    for s in range(d+1):
                        q = [pow(b,s,p) for b in range(r+1)]
                        cols.append(inverse_convolution(q,m,p))
                    rows = [[1]+[0]*d, [1]*(d+1)]
                    rhs = [1, (-m) % p]
                    for t in range(c, r+1):
                        rows.append([col[t] for col in cols])
                        rhs.append(0)
                    rk = rank_mod(rows,p)
                    augmented = [row+[v] for row,v in zip(rows,rhs)]
                    assert rank_mod(augmented,p) > rk, (p,n,r,d)
                    systems += 1
                    per_p += 1
        by_prime.append({'p':p, 'inconsistent_systems':per_p})
    return {'linear_closed_form_entries':closed_cases,
            'linear_closed_form_primes_max':101,
            'all_violating_parameter_systems_primes_max':31,
            'inconsistent_systems':systems, 'by_prime':by_prime}


def graph_checks() -> dict:
    es = [((1<<a)|(1<<b)) for a,b in combinations(range(6),2)]
    qualified = 0
    all_intersecting = 0
    for mask in range(1<<len(es)):
        chosen = [e for i,e in enumerate(es) if (mask>>i)&1]
        if any(not (a&b) for a,b in combinations(chosen,2)):
            continue
        all_intersecting += 1
        if len(chosen) >= 4:
            common = (1<<6)-1
            for e in chosen:
                common &= e
            assert common
            qualified += 1
    pools = [e for e in es if e&0b0011 and e&0b1100]
    assert len(pools) == 4
    colourings = 0
    for assignments in product(range(4),repeat=4):
        counts = [assignments.count(i) for i in range(4)]
        if min(counts) == 0:
            continue
        assert counts == [1]*4
        colourings += 1
    assert (4*pow(3,-1,7)-1) % 7 == 5 > 7-5
    return {'all_simple_graphs_on_six_positions':1<<15,
            'pairwise_intersecting_graphs':all_intersecting,
            'at_least_four_edges_all_have_common_position':qualified,
            'cross_pool_size':len(pools),
            'p7_surjective_four_colour_assignments':colourings,
            'p7_single_edge_forces_m':5,
            'p7_proved_m_upper_bound':2}


def star_and_cover_checks() -> dict:
    examples = []
    checks = 0
    for p in primes_up_to(10000):
        if p < 7:
            continue
        D, r = 4*p-3, p-2
        t = pow(3,-1,p)
        lower = p-1+(p-3)*t
        assert lower > D
        for one_two in (False,True):
            m1 = (4*pow(3,-1,p)-1) % p
            m2 = (8*pow(3,-1,p)-1) % p
            n1 = r-int(one_two)
            admissible_m = (m1 <= p-5 and (not one_two or m2 <= p-5))
            forced_size = 1 + r + int(one_two) + n1*m1 + int(one_two)*m2
            assert not admissible_m or forced_size > D
        n,k = 5*p-5,2*p-5
        aa = [0]*4; aa[3] = 1
        for e in (2,1,0):
            numerator = (n-e)*aa[e+1] - (k-e)
            denominator = p*(k-e)
            aa[e] = 1+p*((numerator+denominator-1)//denominator)
            assert aa[e] % p == 1
            assert (k-e)*aa[e] >= (n-e)*aa[e+1]
            assert (k-e)*(aa[e]-p) < (n-e)*aa[e+1]
        assert aa[0] >= 8*p+1
        if p <= 43:
            examples.append({'p':p,'inverse_3':t,'star_forced_positions':lower,
                             'D':D,'depth3_Z3p_bound':aa[0],
                             'eight_p_plus_one':8*p+1})
        checks += 1
    return {'all_primes_from_7_to_10000':checks,
            'star_profiles_checked_per_prime':2,
            'examples':examples}


def lattice(p: int) -> tuple[np.ndarray,np.ndarray]:
    pts = np.asarray(list(product(range(p),repeat=4)),dtype=np.int64)
    weights = np.asarray([p**3,p**2,p,1],dtype=np.int64)
    return pts,weights


def subset_table(seq: list[tuple[int,...]], p: int,
                 pts: np.ndarray, weights: np.ndarray) -> np.ndarray:
    n = len(seq)
    if n > 49:
        raise ValueError('This int64 audit only supports n<=49.')
    ans = np.zeros((n+1,len(pts)),dtype=np.int64)
    ans[0,0] = 1
    for i,g in enumerate(seq,1):
        src = ((pts-np.asarray(g)) % p) @ weights
        ans[1:i+1] += ans[:i,src]
    for k in range(n+1):
        assert int(ans[k].sum()) == comb(n,k)
    return ans


def group_product(seq: list[tuple[int,...]], p: int,
                  pts: np.ndarray,weights: np.ndarray) -> np.ndarray:
    out = np.zeros(len(pts),dtype=np.int64); out[0] = 1
    for g in seq:
        src = ((pts-np.asarray(g)) % p) @ weights
        out = (out-out[src]) % p
    return out


def max_atom(p: int, diffuse: bool) -> list[tuple[int,...]]:
    aa = list(range(p)) if diffuse else [0]*(p-2)+[2,p-1]
    if diffuse:
        aa[0] = 1
    assert sum(aa)%p == 1
    return ([(1,0,0,0)]*(p-2)+[(0,0,1,0)]*(p-2)+[(1,0,1,0)]
            +[(a,1,0,0) for a in aa]+[(0,0,a,1) for a in aa])


def group_checks() -> dict:
    records = []
    affine_deletions = 0
    total_fibres = 0
    affine_even_derivatives = 0
    for p in (5,7,11,13):
        pts,ww = lattice(p)
        for diffuse in (False,True):
            U = max_atom(p,diffuse)
            dpU = subset_table(U,p,pts,ww)
            D = len(U)
            assert int(dpU[D,0]) == 1 and not np.any(dpU[1:D,0])
            signs = np.asarray([(-1)**k for k in range(D+1)],dtype=np.int64)
            orders = np.arange(D+1,dtype=np.int64)
            assert np.all((signs@dpU)%p == 0)
            assert np.all(((signs*orders)@dpU)%p == 3)
            a,b = U[0],U[-1]
            T = U[1:-1]+[tuple((x+y)%p for x,y in zip(a,b))]
            dp = subset_table(T,p,pts,ww)
            L = len(T)
            assert int(dp[L,0]) == 1 and not np.any(dp[1:L,0])
            sgn = np.asarray([(-1)**k for k in range(L+1)],dtype=np.int64)
            assert np.all((sgn@dp)%p == 2)
            assert np.all(group_product(T,p,pts,ww)==2)
            derivative = ((sgn*np.arange(L+1,dtype=np.int64))@dp)%p
            assert int(derivative[0]) == L%p
            derivative_linear = np.asarray([
                (int(derivative[int(w)])-L)%p for w in ww])
            assert np.all(derivative == (L+pts@derivative_linear)%p)
            affine_even_derivatives += 1
            for val in set(T):
                V = T.copy(); V.remove(val)
                coeff = group_product(V,p,pts,ww)
                assert coeff[0] == 1
                linear = np.asarray([(int(coeff[int(w)])-1)%p for w in ww])
                assert np.all(coeff == (1+pts@linear)%p)
                assert int(np.asarray(val)@linear)%p == 2
                affine_deletions += 1
            outside = [(1,2%p,3%p,4%p),(1,2%p,3%p,4%p),(2%p,0,1,3%p)]
            vals = []
            for mask in range(8):
                chosen = [outside[i] for i in range(3) if (mask>>i)&1]
                bsize = len(chosen)
                target = (-sum((np.asarray(x) for x in chosen),np.zeros(4,dtype=np.int64)))%p
                ix = int(target@ww)
                weighted = sgn*(np.arange(L+1,dtype=np.int64)+bsize)
                vals.append(int(weighted@dp[:,ix])%p)
            for mask in range(8):
                expect = vals[0]+sum(vals[1<<i]-vals[0] for i in range(3) if mask>>i&1)
                assert vals[mask] == expect%p
            total_fibres += len(pts)
            records.append({'p':p,'family':'diffuse' if diffuse else 'concentrated',
                            'max_atom_length':D,'even_atom_length':L,
                            'height':max(Counter(T).values()),'fibres':len(pts),
                            'positions_T':[list(v) for v in T]})
    return {'families':records,'even_atoms':len(records),
            'all_sum_fibres_per_even_atom_total':total_fibres,
            'distinct_value_deletions_affine_checked':affine_deletions,
            'even_atom_derivatives_affine_checked':affine_even_derivatives,
            'Q_T_cubes_per_even_atom':8,
            'warning':'These atoms are test inputs, not B_p counterexamples.'}


def complement_length_checks() -> dict:
    support_cases = 0
    equal_sum_pairs = 0
    reduced_unequal_pairs = 0
    for p in primes_up_to(101):
        if p < 5:
            continue
        for b in range(2,p):
            intersection = {1,p-3} & {b,b+p-4}
            assert bool(intersection) == (b == p-3)
            support_cases += 1
        for b in range(1,p):
            for c in range(1,p):
                intersection = {b,b+p-4} & {c,c+p-4}
                assert bool(intersection) == (b == c or abs(b-c) == p-4)
                equal_sum_pairs += 1
                if b > c and b-c == p-4 and b+c <= p-1:
                    assert c == 1 and b == p-3
                    reduced_unequal_pairs += 1
    return {'primes_max':101, 'support_length_cases':support_cases,
            'equal_sum_length_pairs':equal_sum_pairs,
            'disjoint_unequal_pairs_all_reduce_to_single_vs_p_minus_3':reduced_unequal_pairs}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('audit_results.json'))
    args = parser.parse_args()
    start = perf_counter()
    result = {'status':'PASS',
              'scope':'Exact local algebra, graph and arithmetic checks. NOT a complete B_p search or a formal/third-party proof.',
              'capacity':capacity_checks(),
              'graphs':graph_checks(),
              'star_and_cover':star_and_cover_checks(),
              'group_fibres':group_checks(),
              'complement_lengths':complement_length_checks()}
    result['elapsed_seconds'] = round(perf_counter()-start,6)
    result['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'elapsed_seconds':result['elapsed_seconds'],
                      'capacity_inconsistent_systems':result['capacity']['inconsistent_systems'],
                      'even_atoms':result['group_fibres']['even_atoms'],
                      'output':str(args.output)},ensure_ascii=False))


if __name__ == '__main__':
    main()
