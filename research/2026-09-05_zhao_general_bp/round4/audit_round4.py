#!/usr/bin/env python3
"""Local exact checks for the round-four moment and affine-line lemmas.

This is NOT a verifier of B_p and does not enumerate the remaining branch.
It imports no previous-round verification code.  All subsequences are positional.
Run: python audit_round4.py [--output audit_results.json]
Requires Python 3 and numpy.  No network or external data service is used.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import product, combinations
from math import comb
from pathlib import Path
import hashlib
import json
import time
import numpy as np


def prime(p: int) -> bool:
    return p >= 2 and all(p % d for d in range(2, int(p**0.5) + 1))


def rank_mod(matrix, p: int) -> int:
    a = [[int(x) % p for x in row] for row in matrix]
    r = 0
    for c in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [(x * inv) % p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                b = a[i][c]
                a[i] = [(x - b*y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def grid(p: int):
    pts = np.array(list(product(range(p), repeat=4)), dtype=np.int64)
    weights = np.array([p**3, p**2, p, 1], dtype=np.int64)
    assert np.all(pts @ weights == np.arange(p**4))
    return pts, weights


def positional_counts(T, p: int, pts, weights):
    """Exact integer counts by length and group sum, with independent row totals."""
    n = len(T)
    if n > 48:
        raise ValueError("This exact-int64 audit intentionally limits n to 48.")
    dp = np.zeros((n + 1, p**4), dtype=np.int64)
    dp[0, 0] = 1
    for used, g in enumerate(T):
        back = ((pts - np.array(g, dtype=np.int64)) % p) @ weights
        for k in range(used, -1, -1):
            dp[k + 1] += dp[k, back]
    for k in range(n + 1):
        assert int(dp[k].sum()) == comb(n, k), (p, n, k)
    return dp


def standard_atom(p: int, diffuse: bool):
    a = list(range(p)) if diffuse else [0]*(p-2) + [2, p-1]
    if diffuse:
        a[0] = 1
    assert len(a) == p and sum(a) % p == 1
    U = ([(1,0,0,0)]*(p-2) + [(0,0,1,0)]*(p-2)
         + [(1,0,1,0)] + [(x,1,0,0) for x in a]
         + [(0,0,x,1) for x in a])
    merged = tuple((x+y) % p for x, y in zip(U[0], U[-1]))
    return U[1:-1] + [merged]


def audit_atom(T, p: int, label: str):
    T = [tuple(map(int, x)) for x in T]
    assert prime(p) and len(T) == 4*p-4
    assert all(len(g) == 4 and all(0 <= x < p for x in g) for g in T)
    pts, weights = grid(p)
    dp = positional_counts(T, p, pts, weights)
    zero = dp[:, 0].tolist()
    assert zero == [1] + [0]*(len(T)-1) + [1], (label, zero)
    residues = dp % p
    signs = np.array([1 if k % 2 == 0 else p-1 for k in range(len(T)+1)])
    degrees = np.arange(len(T)+1, dtype=np.int64)
    F0 = (signs @ residues) % p
    F1 = (((signs*degrees) % p) @ residues) % p
    F2 = (((signs*degrees*(degrees-1)) % p) @ residues) % p
    assert np.all(F0 == 2)
    inv2 = pow(2, -1, p)
    lam_values = ((-4-F1)*inv2) % p
    lam = lam_values[weights]
    assert np.all(lam_values == (pts @ lam) % p)
    q_values = ((20+10*lam_values-F2)*inv2) % p
    Q = np.zeros((4,4), dtype=np.int64)
    for i in range(4):
        Q[i,i] = q_values[weights[i]]
        for j in range(i):
            Q[i,j] = Q[j,i] = ((q_values[weights[i]+weights[j]]
                                -Q[i,i]-Q[j,j])*inv2) % p
    assert np.all(q_values == np.sum((pts @ Q)*pts, axis=1) % p)
    neg = ((-pts) % p) @ weights
    assert np.all((F2-F2[neg]-20*lam_values) % p == 0)
    K = (Q + np.outer(lam, lam)) % p
    m = Counter(T)
    allowed_rows = {1, p-3}
    prohibited = [k for k in range(len(T)+1) if k not in allowed_rows]
    candidate_indices = np.flatnonzero(~np.any(dp[prohibited] != 0, axis=0))
    candidates = []
    for idx in candidate_indices:
        g = tuple(map(int, pts[idx]))
        if m[g] + 1 <= p-2:
            assert int(lam_values[idx]) == (2*m[g]+1) % p
            assert int(q_values[idx]) == (1+2*int(lam_values[idx])) % p
            candidates.append(g)
    valid_pairs = 0
    for i, g in enumerate(candidates):
        for h in candidates[i:]:
            extra = Counter([g,h])
            if any(m[a]+b > p-2 for a,b in extra.items()):
                continue
            z = tuple((a+b) % p for a,b in zip(g,h))
            zi = int(np.array(z) @ weights)
            if any(dp[k,zi] for k in range(len(T)+1) if k not in (2,p-2)):
                continue
            gv, hv = np.array(g), np.array(h)
            assert int(gv @ Q @ hv) % p == (1+int(gv @ lam)+int(hv @ lam)) % p
            valid_pairs += 1
    return {
        "label": label, "p": p, "length": len(T),
        "height": max(m.values()), "atom_verified": True,
        "group_fibres_checked": p**4,
        "lambda": lam.tolist(), "Q": Q.tolist(), "K": K.tolist(),
        "rank_Q": rank_mod(Q.tolist(), p), "rank_K": rank_mod(K.tolist(), p),
        "single_extension_fibre_cases": len(candidates),
        "two_extension_fibre_cases": valid_pairs,
    }


def rotate(mask: int, value: int, p: int) -> int:
    value %= p
    full = (1 << p)-1
    return ((mask << value) | (mask >> (p-value))) & full if value else mask


def no_p_sum(seq, p: int) -> bool:
    sums = [0]*(p+1)
    sums[0] = 1
    used = 0
    for x in seq:
        for k in range(min(used,p-1), -1, -1):
            sums[k+1] |= rotate(sums[k], x, p)
        used += 1
        if sums[p] & 1:
            return False
    return True


def scalar_counts(seq, p: int):
    d = [[0]*p for _ in range(len(seq)+1)]
    d[0][0] = 1
    for used,x in enumerate(seq):
        for k in range(used,-1,-1):
            for s in range(p):
                d[k+1][(s+x) % p] += d[k][s]
    assert all(sum(row) == comb(len(seq), k) for k,row in enumerate(d))
    return d


def pair_count(profile, target: int, p: int) -> int:
    count = 0
    for a in range(p):
        b = (target-a) % p
        if a < b:
            count += profile[a]*profile[b]
        elif a == b:
            count += comb(profile[a], 2)
    return count


def exact_affine_line_audit(p: int):
    """All scalar multiplicity profiles; not an enumeration of S in C_p^4."""
    k, t = p-1, p-3
    profiles = zero_free_profiles = nonempty_fibres = divisible_fibres = 0
    high_designs = 0
    for profile in product(range(p-1), repeat=p):
        M = sum(profile)
        if not (k <= M <= 2*p-2):
            continue
        profiles += 1
        seq = [a for a,n in enumerate(profile) for _ in range(n)]
        if not no_p_sum(seq, p):
            continue
        zero_free_profiles += 1
        counts = scalar_counts(seq, p)
        for target,z in enumerate(counts[k]):
            if not z:
                continue
            nonempty_fibres += 1
            if z % p:
                continue
            divisible_fibres += 1
            all_zero = True
            for E in product(*(range(min(n,t)+1) for n in profile)):
                if sum(E) != t:
                    continue
                remaining = [n-e for n,e in zip(profile,E)]
                needed = (target-sum(a*e for a,e in enumerate(E))) % p
                degree = pair_count(remaining, needed, p)
                if degree % p:
                    all_zero = False
                    break
            if all_zero:
                high_designs += 1
                raise AssertionError(("Unexpected affine-line design",p,profile,target))
    return dict(p=p, multiplicity_profiles=profiles,
                zero_free_affine_line_profiles=zero_free_profiles,
                nonempty_target_fibres=nonempty_fibres,
                fibres_with_degree_zero_mod_p=divisible_fibres,
                nonempty_high_order_designs=high_designs)


def audit_linear_algebra():
    """Exhaustive small-field coefficient relations in constructed Gram models."""
    out = []
    for p in (5,7,11):
        ell = np.array([1,0,0,0],dtype=np.int64)
        lam = np.array([2,3,1,0],dtype=np.int64)
        Q = (np.outer(ell,ell)+np.outer(ell,lam)+np.outer(lam,ell)) % p
        G = np.array([[1,0,0,0],[1,1,0,0],[1,0,1,0],[1,0,0,1],[1,1,1,1]],dtype=np.int64)
        checked = relations = 0
        for coefficients in product(range(p),repeat=len(G)):
            c = np.array(coefficients,dtype=np.int64)
            z = (c @ G) % p
            total = int(c.sum()) % p
            lhs = int(z @ Q @ z) % p
            rhs = (total*total+2*total*int(z @ lam)) % p
            assert lhs == rhs
            if not np.any(z):
                relations += 1
                assert total == 0
            checked += 1
        out.append(dict(p=p,coefficient_vectors=checked,linear_relations=relations))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('audit_results.json'))
    args = parser.parse_args()
    start = time.time()
    atoms = []
    for p in (5,7,11,13):
        for diffuse in (False,True):
            atoms.append(audit_atom(standard_atom(p,diffuse),p,
                                    f"standard_p{p}_{'diffuse' if diffuse else 'concentrated'}"))
    fixtures_path = Path(__file__).with_name('fixtures.json')
    fixtures = json.loads(fixtures_path.read_text(encoding='utf-8'))
    for fixture in fixtures['atoms']:
        atoms.append(audit_atom(fixture['T'],fixture['p'],fixture['label']))
    line = [exact_affine_line_audit(p) for p in (5,7)]
    linear = audit_linear_algebra()
    result = {
        "status": "PASS_LOCAL_CHECKS_NOT_Bp_PROOF",
        "scope": "Exact integer moment identities, finite affine-line lemma checks, and coefficient algebra; not branch exclusion.",
        "atoms": atoms,
        "affine_line_checks": line,
        "coefficient_algebra_checks": linear,
        "elapsed_seconds": round(time.time()-start,3),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fixtures_sha256": hashlib.sha256(fixtures_path.read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({"status":result['status'],"atoms":len(atoms),
                      "group_fibres":sum(x['group_fibres_checked'] for x in atoms),
                      "affine_line_checks":line,"elapsed_seconds":result['elapsed_seconds']},
                     ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
