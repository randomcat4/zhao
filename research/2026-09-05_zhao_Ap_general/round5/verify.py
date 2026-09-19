#!/usr/bin/env python3
"""Exact checks for the accompanying A_p follow-up note.

This is NOT an A_p verifier and does NOT certify h(S) <= p-5.
The actual-sequence check uses a meet-in-the-middle enumeration of all
multiplicity patterns, independently of the closed formulas in the note.
The graph/algebra checks are finite regression checks for the hand proofs.
Only the Python standard library is required.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable


def primes_upto(n: int) -> list[int]:
    out = []
    for k in range(2, n + 1):
        if all(k % p for p in out if p * p <= k):
            out.append(k)
    return out


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def prod(xs: Iterable[int]) -> int:
    return math.prod(xs)


def vectors(p: int) -> tuple[tuple[int, ...], ...]:
    return ((1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1), (1,1,1,(-3) % p))


def enumerate_zero_patterns_mitm(p: int) -> list[tuple[int, ...]]:
    """All zero patterns in e1^(p-1)...e4^(p-1)v^4.

    No prescribed zero lengths or formulas for the coordinates of a zero
    pattern are used. Enumerate the two halves and match their actual sums.
    """
    if p < 5 or p not in primes_upto(p):
        raise ValueError("p must be a prime >= 5")
    vv = vectors(p)
    left = {}
    for i, j in itertools.product(range(p), repeat=2):
        s = tuple((i*vv[0][d] + j*vv[1][d]) % p for d in range(4))
        assert s not in left
        left[s] = (i, j)
    found = []
    for k, l, j in itertools.product(range(p), range(p), range(5)):
        s = tuple((k*vv[2][d] + l*vv[3][d] + j*vv[4][d]) % p for d in range(4))
        need = tuple((-c) % p for c in s)
        if need in left:
            found.append(left[need] + (k, l, j))
    return sorted(found, key=lambda pat: (sum(pat), pat))


def count_pattern(pattern: tuple[int, ...], multiplicities: tuple[int, ...],
                  marked: tuple[int, ...] = (0,0,0,0,0),
                  deleted: tuple[int, ...] = (0,0,0,0,0)) -> int:
    return prod(choose(m-d-a, k-a)
                for m, k, a, d in zip(multiplicities, pattern, marked, deleted))


def small_vectors(total: int, dimensions: int = 5):
    if dimensions == 1:
        yield (total,)
    else:
        for x in range(total + 1):
            for rest in small_vectors(total-x, dimensions-1):
                yield (x,) + rest


def check_real_sequence(p: int) -> dict:
    mult = (p-1, p-1, p-1, p-1, 4)
    vv = vectors(p)
    patterns = enumerate_zero_patterns_mitm(p)
    assert patterns[0] == (0,0,0,0,0)
    nonempty = patterns[1:]
    if p < 13:
        return {"p": p, "height": max(mult),
                "zero_patterns": [list(k) for k in nonempty],
                "zero_lengths": sorted({sum(k) for k in nonempty}),
                "four_layer_claim_applies": False}
    expected = [(p-j,p-j,p-j,3*j,j) for j in range(1,5)]
    assert nonempty == expected
    x = [0] + [count_pattern(k, mult) for k in nonempty]
    formula = [0] + [math.comb(4,j)*math.comb(p-1,j-1)**3*math.comb(p-1,3*j)
                     for j in range(1,5)]
    assert x == formula
    assert [z % p for z in x] == [0, (-4)%p, (-6)%p, (-4)%p, (-1)%p]
    assert max(mult) == p-1 > p-4  # crucial scope check
    assert min(map(sum, nonempty)) == 3*p+1
    ds = [[0] * 5 for _ in range(5)]
    d2 = [[[0] * 5 for _ in range(5)] for _ in range(5)]
    for j, pat in enumerate(nonempty, 1):
        for t in range(5):
            mark = tuple(int(i == t) for i in range(5))
            ds[j][t] = count_pattern(pat, mult, mark)
            assert ds[j][t]*mult[t] == x[j]*pat[t]
            for u in range(5):
                mark2 = tuple(int(i == t)+int(i == u) for i in range(5))
                d2[j][t][u] = count_pattern(pat, mult, mark2)
                assert d2[j][t][u] == d2[j][u][t] or u > t
                denom = mult[t]*(mult[u]-int(t == u))
                numerator = x[j]*pat[t]*(pat[u]-int(t == u))
                assert d2[j][t][u]*denom == numerator
        length = 3*p+j
        assert sum(mult[t]*ds[j][t] for t in range(5)) == length*x[j]
        for t in range(5):
            assert sum((mult[u]-int(t == u))*d2[j][t][u] for u in range(5)) == (length-1)*ds[j][t]
        for coord in range(4):
            assert sum(mult[t]*ds[j][t]*vv[t][coord] for t in range(5)) % p == 0
            for t in range(5):
                assert (sum((mult[u]-int(t == u))*d2[j][t][u]*vv[u][coord]
                            for u in range(5)) + ds[j][t]*vv[t][coord]) % p == 0
    beta = [ds[1][t] % p for t in range(5)]
    for t in range(5):
        assert [ds[j][t] % p for j in range(1,5)] == [beta[t],3*beta[t]%p,3*beta[t]%p,beta[t]]
        for u in range(5):
            delta, eps = d2[1][t][u] % p, d2[4][t][u] % p
            assert [d2[j][t][u] % p for j in range(1,5)] == [delta,(2*delta+eps)%p,(delta+2*eps)%p,eps]
        assert sum((mult[u]-int(t == u))*d2[1][t][u] for u in range(5)) % p == 0
        assert (sum((mult[u]-int(t == u))*d2[4][t][u] for u in range(5))-3*beta[t]) % p == 0
        for coord in range(4):
            for j in (1,4):
                assert (sum((mult[u]-int(t == u))*d2[j][t][u]*vv[u][coord]
                            for u in range(5))+beta[t]*vv[t][coord]) % p == 0
    assert sum(mult[t]*beta[t] for t in range(5)) % p == (-4) % p
    for coord in range(4):
        assert sum(mult[t]*beta[t]*vv[t][coord] for t in range(5)) % p == 0
    # Every positional deletion orbit through size 3, not just averaged deletion.
    deletion_orbits = 0
    for d in range(4):
        for de in small_vectors(d):
            if any(a > m for a, m in zip(de, mult)):
                continue
            total = sum((-1)**sum(pat)*count_pattern(pat, mult, deleted=de)
                        for pat in patterns)
            assert total % p == 0
            deletion_orbits += 1
    lifts = [(x[j] - (p - [0,4,6,4,1][j]))//p for j in range(1,5)]
    assert min(lifts) >= 0
    assert lifts[0]+lifts[3] >= 1 and lifts[1]+lifts[2] >= 1
    return {"p": p, "length": 4*p, "height": p-1, "zero_lengths": [3*p+j for j in range(1,5)],
            "x": x, "theta_mod_p": p-1, "all_point_pair_and_vector_checks": True,
            "exact_deletion_orbits_checked": deletion_orbits,
            "satisfies_required_height": False, "is_Ap_counterexample": False}


def pair_graph(values: tuple[int, ...], q: int, p: int) -> tuple[frozenset[int], ...]:
    return tuple(frozenset((i,j)) for i in range(len(values)) for j in range(i+1,len(values))
                 if (values[i]+values[j]) % p == q)


def degree(edges: tuple[frozenset[int], ...], i: int) -> int:
    return sum(i in e for e in edges)


def check_cross_pair_lemma(p: int = 7, max_n: int = 7) -> dict:
    cases = 0
    for n in range(2, max_n+1):
        for vals in itertools.combinations_with_replacement(range(p), n):
            gg = [pair_graph(vals, q, p) for q in range(p)]
            for q1 in range(p):
                for q2 in range(q1, p):
                    aa, bb = gg[q1], gg[q2]
                    if not aa or not bb or any(not (a & b) for a in aa for b in bb):
                        continue
                    # Independent search for a witness set of <= 4 positions.
                    good = False
                    for r in range(min(4,n)+1):
                        for u in itertools.combinations(range(n), r):
                            uu = set(u)
                            if all(degree(aa,v)+degree(bb,v) <= 3 for v in range(n) if v not in uu):
                                good = True
                                break
                        if good:
                            break
                    assert good, (p, vals, q1, q2)
                    cases += 1
    return {"p": p, "max_n": max_n, "cross_intersecting_complete_pair_graph_cases": cases}


def check_structural_arithmetic(max_p: int) -> dict:
    ps = [p for p in primes_upto(max_p) if p >= 7]
    for p in ps:
        h, rho, s = p-4, (p+1)//2, (p-1)//2
        assert 8+2*h < 3*p  # K2,2 witness plus two value classes
        assert 3 < rho
        if p >= 17:
            assert 8 < rho  # induced 2K2, including duplicate core values
        if p >= 29:
            assert rho-4 > 4
            assert (3*p-4)//(p-7) <= 3
            assert 3*p-21 > 2*p-2
        if p >= 11:
            m = (p+5)//2
            assert (3-m-rho) % p == 0
            if m <= h:
                assert p >= 13
                assert (m-rho) % p != 0  # u=d loop impossible
                # d != t: 2(m_r-loop) == -2 is impossible.
                for loop in (0,1):
                    for mr in range(h+1):
                        if loop and mr != s:
                            continue
                        assert (2*(mr-loop)+2) % p != 0
    # p=7: the additional y+t^3 block must NOT be discarded.
    p, h, rho = 7, 3, 4
    for delta in (0,1):
        possible_m = [m for m in range(h+1) if (m-(delta-1)) % p == 0]
        assert possible_m == ([] if delta == 0 else [0])
    for me in range(h+1):
        for loop in (0,1):
            assert (6+me-loop) % p != rho  # r cannot occur
            assert (3+2*(me-loop)) % p != rho  # d cannot occur
    # Covers of K2,2 and P4 checked on all core subsets.
    vertices = set(range(4))
    k22 = {(0,2),(0,3),(1,2),(1,3)}
    path = {(0,1),(1,2),(2,3)}
    for r in range(5):
        for c in itertools.combinations(range(4),r):
            cc=set(c)
            is_cover = all(cc.intersection(e) for e in k22)
            assert is_cover == ({0,1}.issubset(cc) or {2,3}.issubset(cc))
    path_covers2 = {tuple(c) for c in itertools.combinations(range(4),2)
                    if all(set(c).intersection(e) for e in path)}
    assert path_covers2 == {(0,2),(1,2),(1,3)}
    return {"primes_checked": len(ps), "maximum_prime_bound": max_p,
            "p7_exceptional_block_checked": True,
            "universal_proof_source": "research_note_zh.md (hand proof, not finite enumeration)"}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=Path(__file__).with_name("verification_report.json"))
    ap.add_argument("--max-prime", type=int, default=2000)
    args = ap.parse_args()
    report = {
        "status": "PARTIAL: neither A_p nor the entire h=p-4 branch is proved",
        "construction_scope": "Actual x0=0 sequence, but height p-1; NOT an A_p counterexample",
        "real_sequences": [check_real_sequence(p) for p in (7,11,13,17,23,31,47,101,149)],
        "cross_pair_lemma_regression": check_cross_pair_lemma(),
        "structural_arithmetic": check_structural_arithmetic(args.max_prime),
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": report["status"],
                      "real_sequence_parameters_checked": len(report["real_sequences"]),
                      "cross_pair_cases": report["cross_pair_lemma_regression"]["cross_intersecting_complete_pair_graph_cases"],
                      "arithmetic_primes": report["structural_arithmetic"]["primes_checked"],
                      "report": str(args.output)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
