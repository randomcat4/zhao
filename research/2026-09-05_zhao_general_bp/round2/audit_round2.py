#!/usr/bin/env python3
"""Exact checks for the round-2 atom-descent and sparse-spectrum lemmas.

These are implementation/identity checks, NOT an exhaustive proof of B_p.
The universal mathematical proofs are in ROUND2_THEOREMS.md.

Requirements: Python 3.10+, NumPy.
Run: python audit_round2.py --output audit_results.json
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
import hashlib
import json
from math import comb
from pathlib import Path
from time import perf_counter
from typing import Sequence
import numpy as np

Vector = tuple[int, ...]


def grid(p: int, rank: int) -> tuple[np.ndarray, np.ndarray]:
    digits = np.array(list(product(range(p), repeat=rank)), dtype=np.int64)
    weights = np.array([p**i for i in range(rank - 1, -1, -1)], dtype=np.int64)
    return digits, weights


def position_counts(seq: Sequence[Vector], p: int, rank: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """dp[k,h] counts k-position subsets with sum h, over the INTEGERS."""
    n = len(seq)
    # All checks use n <= 49. This also protects later signed first moments.
    if n > 49:
        raise ValueError("This exact int64 implementation deliberately rejects n > 49.")
    digits, weights = grid(p, rank)
    dp = np.zeros((n + 1, len(digits)), dtype=np.int64)
    dp[0, 0] = 1
    for used, g in enumerate(seq, 1):
        if len(g) != rank or any(not (0 <= x < p) for x in g):
            raise ValueError("Invalid group vector")
        src = ((digits - np.array(g, dtype=np.int64)) % p) @ weights
        # Advanced indexing makes a copy: one position is used at most once.
        dp[1:used+1] += dp[:used, src]
    for k in range(n + 1):
        assert int(dp[k].sum()) == comb(n, k), (p, rank, n, k)
    return dp, digits, weights


def is_atom(dp: np.ndarray) -> bool:
    n = len(dp) - 1
    return int(dp[n, 0]) == 1 and not np.any(dp[1:n, 0])


def audit_max_atom(seq: Sequence[Vector], p: int, rank: int, label: str) -> dict:
    D = rank * (p - 1) + 1
    assert len(seq) == D and D % p != 0
    dp, digits, weights = position_counts(seq, p, rank)
    assert is_atom(dp), (label, "not an atom")
    signs = np.array([(-1)**k for k in range(D + 1)], dtype=np.int64)
    orders = np.arange(D + 1, dtype=np.int64)
    # Independent group-ring checks for EVERY actual sum fibre.
    assert np.all((signs @ dp) % p == 0)
    assert np.all(((signs * orders) @ dp) % p == (-D) % p)
    neg = ((-digits) % p) @ weights
    ext = np.zeros((D + 2, len(digits)), dtype=np.int64)
    ext[:D+1] += dp[:, 0, None]  # zero subsets not using the added position
    ext[1:] += dp[:, neg]       # zero subsets using the added position
    n = D + 1
    mobius = np.array([((-1)**(n-k))*k for k in range(n+1)], dtype=np.int64)
    assert np.all((mobius @ ext) % p == 0)
    mult = Counter(seq)
    eligible = local_bad = 0
    local_examples = []
    for ix, gg in enumerate(digits):
        g = tuple(map(int, gg))
        if ix == 0:
            continue  # g=0 already gives a one-term zero sum
        m = mult[g]
        assert int(ext[D, ix]) == 1 + m
        if m <= p - 2:
            eligible += 1
            assert any(int(ext[k, ix]) > 0 for k in range(1, D) if k % p), (label, g)
        if rank == 4 and not np.any(ext[1:3*p, ix]):
            local_bad += 1
            assert m <= p - 2
            lhs = sum((-1)**j * j * int(ext[3*p+j, ix]) for j in range(1, p-3))
            assert (lhs - 3 * (m + 1)) % p == 0
            witnesses = [3*p+j for j in range(1, p-3) if int(ext[3*p+j, ix]) > 0]
            assert witnesses
            if len(local_examples) < 3:
                local_examples.append({"added_value": g, "smaller_nonpure_lengths": witnesses})
    return {"label": label, "prime": p, "rank": rank, "atom_length": D,
            "height": max(mult.values()), "all_fibres": len(digits),
            "eligible_nonzero_extensions": eligible,
            "extensions_with_no_zero_below_3p": local_bad if rank == 4 else None,
            "local_examples": local_examples, "atom_positions": [list(v) for v in seq]}


def canonical(p: int, rank: int) -> list[Vector]:
    seq = []
    for i in range(rank):
        e = tuple(int(j == i) for j in range(rank))
        seq.extend([e] * (p - 1))
    seq.append((1,) * rank)
    return seq


def glued_rank4(p: int, diffuse: bool) -> list[Vector]:
    # Join two explicitly constructed rank-two atoms after deleting one e_1
    # and one e_3. Each component's p coset coefficients have total 1.
    A = list(range(p)) if diffuse else [0] * (p - 2) + [2, p - 1]
    if diffuse:
        A[0] = 1
    assert len(A) == p and sum(A) % p == 1
    seq = [(1,0,0,0)]*(p-2) + [(0,0,1,0)]*(p-2) + [(1,0,1,0)]
    seq += [(a,1,0,0) for a in A]
    seq += [(0,0,a,1) for a in A]
    return seq


def det_mod(matrix: list[list[int]], p: int) -> int:
    a = [[x % p for x in row] for row in matrix]
    n = len(a); result = 1
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            result = -result
        val = a[k][k]; result = result * val % p
        inv = pow(val, -1, p)
        for i in range(k + 1, n):
            q = a[i][k] * inv % p
            for j in range(k, n):
                a[i][j] = (a[i][j] - q * a[k][j]) % p
    return result % p


def sparse_spectrum_checks() -> dict:
    matrices = 0
    for p in (5,7,11):
        allowed = list(range(1, p - 2))
        for bits in range(1 << len(allowed)):
            J = [r for i, r in enumerate(allowed) if bits >> i & 1]
            E = [0] + J; s = len(E)
            mat = [[comb(e, k) if e >= k else 0 for e in E] for k in range(s)]
            actual = det_mod(mat, p)
            expected = 1
            for i in range(s):
                for j in range(i + 1, s):
                    expected = expected * (E[j] - E[i]) % p
            for k in range(s):
                fac = 1
                for t in range(1, k + 1): fac = fac * t % p
                expected = expected * pow(fac, -1, p) % p
            assert actual == expected and actual != 0
            # Deleting at most p-2-|J| leaves at least |J|+1 root conditions.
            delta = p - 2 - len(J)
            assert (5*p-5-delta) - 4*(p-1) == s
            matrices += 1
    return {"complete_residue_set_checks_for_primes": [5,7,11], "matrices": matrices}


def rounded_covering_checks() -> dict:
    records = []
    for p in (5,7,11,13,17,19,23,29,31):
        N, size = 5*p-5, 2*p-5
        for delta in range(1,p-1):
            a = [0]*(delta+1); a[delta] = 1
            for e in range(delta-1,-1,-1):
                num = (N-e)*a[e+1]-(size-e)
                den = p*(size-e)
                a[e] = 1+p*((num+den-1)//den)
                assert a[e] % p == 1
                assert (size-e)*a[e] >= (N-e)*a[e+1]
                assert (size-e)*(a[e]-p) < (N-e)*a[e+1]
            if delta <= 4:
                records.append({"prime":p,"deletion_depth":delta,"Z_3p_lower_bound":a[0]})
    return {"scope":"exact arithmetic checks of the rounded recursion, not existence of bad sequences",
            "examples": records}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("audit_results.json"))
    args = parser.parse_args()
    start = perf_counter()
    # Exhaust ALL position multisets of length five in C_3^2 with no zero
    # value and multiplicities <= 2, filtering atoms by integer subset DP.
    pts = [v for v in product(range(3), repeat=2) if v != (0,0)]
    exhaustive_atoms = 0; exhaustive_inputs = 0; exhaustive_extensions = 0
    for inds in combinations_with_replacement(range(len(pts)), 5):
        if max(Counter(inds).values()) > 2: continue
        exhaustive_inputs += 1
        seq = [pts[i] for i in inds]
        dp, _, _ = position_counts(seq, 3, 2)
        if not is_atom(dp): continue
        rec = audit_max_atom(seq, 3, 2, "exhaustive_C3_squared")
        exhaustive_atoms += 1
        exhaustive_extensions += rec["eligible_nonzero_extensions"]
    families = []
    for p in (5,7,11,13):
        families.append(audit_max_atom(canonical(p,4), p,4,"canonical_rank4"))
        families.append(audit_max_atom(glued_rank4(p,True), p,4,"glued_diffuse_rank4"))
        families.append(audit_max_atom(glued_rank4(p,False),p,4,"glued_concentrated_rank4"))
    result = {"status": "PASS", "scope": "Exact local-identity checks; not a proof or counterexample to B_p",
              "exhaustive_C3_squared": {"multisets_checked": exhaustive_inputs,
                    "maximal_atoms": exhaustive_atoms, "eligible_extensions": exhaustive_extensions},
              "rank4_test_families": families, "sparse_spectrum": sparse_spectrum_checks(),
              "rounded_covering": rounded_covering_checks(),
              "seconds": perf_counter()-start,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "rank4_test_families"},ensure_ascii=False,indent=2))
    print("Rank-four family local-safe extension counts:")
    for rec in families:
        print(rec["prime"],rec["label"],rec["height"],rec["extensions_with_no_zero_below_3p"])

if __name__ == "__main__":
    main()
