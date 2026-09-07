#!/usr/bin/env python3
"""Exact checks for the third independent audit of the Zhao A_p/B_p relaxations.

This verifies only the explicit certificates/models recorded in the companion JSON.
It is not a verifier of either endpoint and does not turn finite checks into all-prime proofs.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SECOND = HERE.parent / "round2" / "models.json"
OUT = HERE / "verification.json"
MODEL_OUT = HERE / "models.json"


def add(a, b, p):
    return tuple((x + y) % p for x, y in zip(a, b))


def sub(a, b, p):
    return tuple((x - y) % p for x, y in zip(a, b))


def vsum(seq, p):
    if not seq:
        return (0, 0, 0, 0)
    return tuple(sum(v[c] for v in seq) % p for c in range(4))


def pair_index(pairs):
    return {tuple(x): i for i, x in enumerate(pairs)}


def a7_psd_certificate(second):
    m = second["A7_two_link_model"]
    layer = 0
    i, j, k = 2, 7, 19
    idx = pair_index(m["pairs"])
    deg = m["vertex_degrees"][layer]
    cod = m["pair_codegrees"][layer]
    dij = cod[idx[(min(i, j), max(i, j))]]
    dik = cod[idx[(min(i, k), max(i, k))]]
    djk = cod[idx[(min(j, k), max(j, k))]]
    assert deg[i] == deg[j] == deg[k] == 554
    assert (dij, dik, djk) == (0, 554, 554)
    q = deg[i] + deg[j] + deg[k] + 2*dij - 2*dik - 2*djk
    assert q == -554
    det = -(554 ** 3)
    assert det == -170031464
    return {
        "layer_length": 22,
        "positions_zero_based": [i, j, k],
        "positions_one_based": [i+1, j+1, k+1],
        "degrees": [deg[i], deg[j], deg[k]],
        "codegrees_ij_ik_jk": [dij, dik, djk],
        "test_vector": [1, 1, -1],
        "quadratic_form": q,
        "principal_determinant": det,
        "status": "INFEASIBLE_AT_PAIR_GRAM_LEVEL",
    }


def w_value(p, r):
    if r == 0:
        return 1
    if r == 1:
        return 0
    return (r - 1) if r % 2 else (p - r + 1)


def b_local_mobius(p):
    k = p - 1
    w = [w_value(p, r) for r in range(k + 1)]
    d = []
    for r in range(k + 1):
        val = sum(math.comb(r, q) * w[q] for q in range(r + 1))
        d.append(val)
        if r < 2:
            assert val == 1
        else:
            assert val % p == 0
    assert d[2] == p
    number_pair_indices = math.comb(k, 2)
    eig_small = p - 1
    eig_large = (p - 1) + number_pair_indices
    assert eig_small > 0 and eig_large > 0
    return {
        "p": p,
        "w_exact_missing": w,
        "d_links": d,
        "pair_missing_gram": {
            "form": "(p-1) I + J",
            "dimension": number_pair_indices,
            "eigenvalues": {"p-1": number_pair_indices - 1, "p-1+dimension": 1},
        },
        "status": "ALL_LOCAL_MOBIUS_COUNTS_NONNEGATIVE_AND_PAIR_GRAM_PSD",
    }


def moment_curve_R(p):
    return [(1, t, pow(t, 2, p), pow(t, 3, p)) for t in range(1, p)]


def verify_sidon(R, p):
    seen = {}
    for i, j in itertools.combinations(range(len(R)), 2):
        s = add(R[i], R[j], p)
        assert s not in seen, (seen[s], (i, j), s)
        seen[s] = (i, j)
    return len(seen)


def sidon_threshold(primes=(7, 11, 13, 17, 19, 23, 29, 31, 37)):
    rows = []
    for p in primes:
        R = moment_curve_R(p)
        distinct = verify_sidon(R, p)
        lower = p * distinct
        upper = math.comb(5*p - 5, 2)
        rows.append({"p": p, "distinct_pair_sums": distinct,
                     "required_pair_incidences": lower,
                     "available_pairs": upper,
                     "contradiction": lower > upper})
    assert all(not r["contradiction"] for r in rows if r["p"] <= 23)
    assert all(r["contradiction"] for r in rows if r["p"] >= 29)
    return rows


def b_p7_pair_completion():
    p = 7
    R = moment_curve_R(p)
    sumR = vsum(R, p)
    h = tuple((-2*x) % p for x in sumR)
    Rp = [add(g, h, p) for g in R]
    Rm = [sub(g, h, p) for g in R]
    S = R + Rp + Rm + Rm + Rm
    assert len(S) == 30
    assert vsum(S, p) == sumR
    assert max(Counter(S).values()) == 3

    target = sumR
    blocks = []
    for B in itertools.combinations(range(30), 6):
        if vsum([S[i] for i in B], p) == target:
            blocks.append(B)
    assert tuple(range(6)) in blocks
    assert len(blocks) == 1441

    block_sets = [set(B) for B in blocks]
    local_degrees = {}
    base = set(range(6))
    for i, j in itertools.combinations(range(6), 2):
        E = base - {i, j}
        d = sum(E.issubset(B) for B in block_sets)
        assert d == 7
        local_degrees[f"{i},{j}"] = d

    zero6 = (0, 1, 2, 15, 16, 17)
    assert vsum([S[i] for i in zero6], p) == (0, 0, 0, 0)
    assert add(sumR, tuple((-3*x) % p for x in h), p) == (0,0,0,0)

    return {
        "p": p,
        "R": R,
        "translation_h": h,
        "S": S,
        "sigma_R_equals_sigma_S": list(sumR),
        "height": 3,
        "R_profile": "squarefree",
        "complete_fixed_sum_6_fibre_size": len(blocks),
        "fibre_size_mod_7": len(blocks) % 7,
        "all_R_minus_pair_link_degrees": sorted(set(local_degrees.values())),
        "explicit_short_zero_sum_zero_based": list(zero6),
        "explicit_short_zero_sum_one_based": [x+1 for x in zero6],
        "explicit_short_zero_sum_values": [S[i] for i in zero6],
        "status": "PAIR_EXCHANGE_COMPLETION_REALIZED_BUT_GLOBAL_B_CONDITIONS_FAIL",
        "failures": [
            "Z_L complement count is 1441 == 6 mod 7, not 0 mod 7",
            "there is a six-position zero sum"
        ]
    }


def unique_double_local_labels(p):
    g0 = (1,0,0,0)
    ts = list(range(1, p-2))
    R = [g0, g0] + [(1,t,pow(t,2,p),pow(t,3,p)) for t in ts]
    assert len(R) == p-1
    assert len(set(R)) == p-2
    assert max(Counter(R).values()) == 2
    assert all(b % p for b in range(1,p))
    return {"p":p,"R":R,"support_size":p-2,"height":2,
            "status":"LOCAL_UNIQUE_DOUBLE_PROFILE_SURVIVES_LOW_ORDER_LENGTH_FUNCTIONAL"}


def main():
    second = json.loads(SECOND.read_text(encoding="utf-8"))
    cert_a = a7_psd_certificate(second)
    mobius = [b_local_mobius(p) for p in (7,11,13)]
    threshold = sidon_threshold()
    p7 = b_p7_pair_completion()
    unique = unique_double_local_labels(7)

    model = {
        "status": "THIRD_AUDIT_EXPLICIT_MODELS_NOT_ENDPOINT_COUNTEREXAMPLES",
        "A7_pair_gram_certificate": cert_a,
        "B_local_mobius_models": mobius,
        "B_moment_curve_pair_count_rows": threshold,
        "B_p7_common_label_pair_completion": p7,
        "B_p7_unique_double_local_labels": unique,
    }
    MODEL_OUT.write_text(json.dumps(model, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    result = {
        "status": "PASS_EXPLICIT_CERTIFICATES_AND_LOCAL_MODELS",
        "A7_pair_gram_infeasible": cert_a["quadratic_form"] < 0,
        "B_local_mobius_checked_primes": [x["p"] for x in mobius],
        "B_sidon_count_first_checked_prime_contradiction": next(r["p"] for r in threshold if r["contradiction"]),
        "B_p7_pair_completion_degree": p7["all_R_minus_pair_link_degrees"],
        "B_p7_complete_fibre_mod": p7["fibre_size_mod_7"],
        "B_p7_short_zero_length": len(p7["explicit_short_zero_sum_zero_based"]),
        "scope": "Exact verification of the displayed finite certificates; all-prime claims require the symbolic proofs in the audit note."
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
