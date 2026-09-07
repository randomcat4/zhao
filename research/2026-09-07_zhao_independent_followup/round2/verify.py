#!/usr/bin/env python3
"""Verify the abstract relaxation certificates used in the second Zhao audit.

This script deliberately verifies only the stated marginal/design/fibre equations.
It does not claim that the data arise from one labelled sequence in F_p^4, nor
that they prove or refute either endpoint.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Iterable, Sequence


def vadd(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple((x + y) % p for x, y in zip(a, b))


def vscale(c: int, a: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple((c * x) % p for x in a)


def vsum(weighted: Iterable[tuple[int, Sequence[int]]], p: int, dim: int = 4) -> tuple[int, ...]:
    out = [0] * dim
    for c, v in weighted:
        for r in range(dim):
            out[r] = (out[r] + c * v[r]) % p
    return tuple(out)


def verify_a7(model: dict) -> dict:
    p = int(model["p"])
    n = int(model["n_positions"])
    assert p == 7 and n == 28

    lengths = list(map(int, model["zero_sum_lengths"]))
    counts = list(map(int, model["x"]))
    beta = [int(x) % p for x in model["beta"]]
    labels = [tuple(int(x) % p for x in row) for row in model["labels_Fp4"]]
    degrees = [[int(x) for x in row] for row in model["vertex_degrees"]]
    pairs = [tuple(map(int, row)) for row in model["pairs"]]
    codegrees = [[int(x) for x in row] for row in model["pair_codegrees"]]

    assert lengths == [3 * p + j for j in range(1, 5)]
    assert len(counts) == len(lengths) == 4
    assert len(beta) == len(labels) == n
    assert all(len(v) == 4 for v in labels)
    assert all(v != (0, 0, 0, 0) for v in labels)
    assert len(set(labels)) == n, "The supplied model intentionally uses distinct nonzero labels."

    expected_x_residues = [(-4) % p, (-6) % p, (-4) % p, (-1) % p]
    assert [x % p for x in counts] == expected_x_residues
    assert sum(beta) % p == (-4) % p
    assert vsum(zip(beta, labels), p) == (0, 0, 0, 0)

    assert len(degrees) == len(codegrees) == 4
    assert all(len(row) == n for row in degrees)
    assert len(pairs) == math.comb(n, 2)
    assert len(set(pairs)) == len(pairs)
    assert set(pairs) == {(i, j) for i in range(n) for j in range(i + 1, n)}
    assert all(len(row) == len(pairs) for row in codegrees)

    pair_index = {e: q for q, e in enumerate(pairs)}
    coeff = [1, 3, 3, 1]
    family_checks = []

    for fam, (k, x, deg, codeg, c) in enumerate(zip(lengths, counts, degrees, codegrees, coeff), start=1):
        assert x >= 0
        assert all(0 <= d <= x for d in deg)
        assert sum(deg) == k * x
        assert all((deg[i] - c * beta[i]) % p == 0 for i in range(n))
        assert vsum(zip(deg, labels), p) == (0, 0, 0, 0)

        assert all(q >= 0 for q in codeg)
        assert sum(codeg) == math.comb(k, 2) * x
        row_sums = [0] * n
        pair_vector = [0] * 4
        for q, ((i, j), cij) in enumerate(zip(pairs, codeg)):
            assert cij <= min(deg[i], deg[j], x)
            row_sums[i] += cij
            row_sums[j] += cij
            for r in range(4):
                pair_vector[r] = (pair_vector[r] + cij * (labels[i][r] + labels[j][r])) % p
        assert all(row_sums[i] == (k - 1) * deg[i] for i in range(n))
        assert tuple(pair_vector) == (0, 0, 0, 0)
        assert all(x - d >= 0 for d in deg)
        family_checks.append({
            "family": fam,
            "length": k,
            "count": x,
            "count_mod_p": x % p,
            "degree_sum": sum(deg),
            "pair_sum": sum(codeg),
        })

    d1, d2, d3, d4 = codegrees
    delta = [x % p for x in d1]
    epsilon = [x % p for x in d4]
    for q in range(len(pairs)):
        assert d2[q] % p == (2 * delta[q] + epsilon[q]) % p
        assert d3[q] % p == (delta[q] + 2 * epsilon[q]) % p

    for i in range(n):
        neigh_delta = 0
        neigh_epsilon = 0
        weighted_delta = [0] * 4
        weighted_epsilon = [0] * 4
        for j in range(n):
            if i == j:
                continue
            e = (i, j) if i < j else (j, i)
            q = pair_index[e]
            neigh_delta = (neigh_delta + delta[q]) % p
            neigh_epsilon = (neigh_epsilon + epsilon[q]) % p
            for r in range(4):
                weighted_delta[r] = (weighted_delta[r] + delta[q] * labels[j][r]) % p
                weighted_epsilon[r] = (weighted_epsilon[r] + epsilon[q] * labels[j][r]) % p
        assert neigh_delta == 0
        assert neigh_epsilon == (3 * beta[i]) % p
        rhs = tuple((-beta[i] * labels[i][r]) % p for r in range(4))
        assert tuple(weighted_delta) == rhs
        assert tuple(weighted_epsilon) == rhs

    return {
        "status": "PASS_A7_TWO_LINK_RELAXATION",
        "scope": "scalar + vertex + pair-link + vector moment equations only",
        "families": family_checks,
        "missing_semantics": [
            "0/1 clique decomposition of every degree/codegree table into distinct subsets",
            "each selected subset has actual group sum zero under the one common label map",
            "the quotient-sum and near-complete-core restrictions",
            "third and higher link compatibility",
        ],
    }


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False
    return True


def verify_b_symbolic(model: dict, primes: Sequence[int]) -> dict:
    pure = model["pure_3p_low_multiplicity_profile_p7"]
    assert pure["p"] == 7
    assert sum(pure["multiplicity_profile"]) == 5 * pure["p"] - 5
    assert max(pure["multiplicity_profile"]) == pure["height"] == 3
    assert pure["height"] <= pure["p"] - 2
    assert sum(1 for m in pure["multiplicity_profile"] if m >= pure["p"] - 3) == 0

    checked = []
    for p in primes:
        assert p >= 7 and is_prime(p)
        N = 5 * p - 5
        k0 = 2 * p - 5
        kL = p - 1
        core = p - 4
        X = 2 * p - 2

        c0_total = math.comb(N - core, k0 - core)
        assert c0_total > 0
        for e in range(0, p - 2):
            for q in range(0, e + 1):
                if q > k0 - core:
                    continue
                degree = math.comb((N - core) - q, (k0 - core) - q)
                assert degree % p == 1

        cL_total = math.comb(X, kL)
        assert cL_total % p == 0
        for e in range(0, p - 2):
            degree = math.comb(X - e, kL - e)
            assert degree % p == 0
        assert math.comb(X - 1, kL - 1) < cL_total

        R = [(1, t, pow(t, 2, p), pow(t, 3, p)) for t in range(1, p)]
        assert len(set(R)) == p - 1
        for b in range(1, p):
            assert b % p != 0
            c0 = (1 - b) % p
            c1 = (1 + b) % p
            unsigned0 = (((-1) ** b) * c0) % p
            unsigned1 = (((-1) ** (b + 1)) * c1) % p
            assert 0 <= unsigned0 < p and 0 <= unsigned1 < p
            K0 = (c0 + c1) % p
            K1 = (b * c0 + (b - 4) * c1) % p
            K2 = (b * (b - 1) * c0 + (b - 4) * (b - 5) * c1) % p
            lam = b % p
            Q = (3 * b * b) % p
            assert K0 == 2 % p
            assert K1 == (-4 - 2 * lam) % p
            assert K2 == (20 + 10 * lam - 2 * Q) % p

        assert X - 2 >= p - 2
        assert X > p - 2

        checked.append({
            "p": p,
            "N": N,
            "three_p_family_blocks": c0_total,
            "L_family_blocks": cL_total,
            "R_size": p - 1,
            "exchange_component_size": X,
        })

    return {
        "status": "PASS_B_SYMBOLIC_DESIGN_AND_LOCAL_FIBRE_RELAXATIONS",
        "scope": "exact incidence designs plus formal per-atom fibres, without a global fixed-sum label gluing",
        "checked_primes": checked,
        "pure_3p_profile_p7": pure,
        "known_failure": model["known_failure"],
    }


def verify_a_analytic_multihypergraph(primes: Sequence[int]) -> dict:
    uv_raw = {1: (-3, 1), 2: (9, 3), 3: (-9, -5), 4: (3, 2)}
    target_raw = {1: -4, 2: -6, 3: -4, 4: -1}
    checked = []
    for p in primes:
        assert p >= 7 and is_prime(p)
        n = 4 * p
        uv = {j: (u % p, v % p) for j, (u, v) in uv_raw.items()}
        counts = {}
        for j in range(1, 5):
            k = 3 * p + j
            u, v = uv[j]
            counts[j] = u * math.comb(n - 1, k - 1) + v * math.comb(n - 1, k)
            assert counts[j] >= 0
            assert counts[j] % p == target_raw[j] % p

        link_rows = []
        for r in range(0, 4):
            cases = [False] if r == 0 else [False, True]
            for contains_o in cases:
                vals = []
                for j in range(1, 5):
                    k = 3 * p + j
                    u, v = uv[j]
                    if contains_o:
                        val = u * math.comb(n - r, k - r)
                    else:
                        val = (
                            u * math.comb(n - r - 1, k - r - 1)
                            + v * math.comb(n - r - 1, k - r)
                        )
                    vals.append(val)
                signed = sum(((-1) ** j) * vals[j - 1] for j in range(1, 5)) % p
                assert signed == (1 if r == 0 else 0)
                link_rows.append({
                    "r": r,
                    "contains_distinguished_position": contains_o,
                    "d_mod_p": [x % p for x in vals],
                    "signed_sum_mod_p": signed,
                })

        checked.append({
            "p": p,
            "multiplicities": {str(j): list(uv[j]) for j in range(1, 5)},
            "counts_mod_p": [counts[j] % p for j in range(1, 5)],
            "link_rows": link_rows,
        })
    return {
        "status": "PASS_A_ALL_PRIME_3_LINK_MULTIHYPERGRAPH_RELAXATION",
        "checked_primes": checked,
        "construction": {
            "through_o_multiplicity_raw": [-3, 9, -9, 3],
            "away_o_multiplicity_raw": [1, 3, -5, 2],
            "block_sizes": "3p+1,3p+2,3p+3,3p+4",
        },
        "known_failure": "Repeated abstract blocks are allowed and no block is required to be a zero-sum subset under one common label map.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", default="models.json")
    parser.add_argument("--output", default="verification.json")
    args = parser.parse_args()

    cert_path = Path(args.certificate)
    data = json.loads(cert_path.read_text(encoding="utf-8"))
    assert data["status"] == "ABSTRACT_RELAXATION_CERTIFICATE_NOT_A_SEQUENCE_AND_NOT_AN_ENDPOINT_COUNTEREXAMPLE"

    report = {
        "status": "PASS_ABSTRACT_RELAXATIONS_ONLY_NOT_ENDPOINT_PROOF",
        "certificate": str(cert_path),
        "A": {
            "analytic_multihypergraph": verify_a_analytic_multihypergraph([7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]),
            "p7_two_link_integer_model": verify_a7(data["A7_two_link_model"]),
        },
        "B": verify_b_symbolic(data["B_symbolic_incidence_model"], [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]),
        "interpretation": (
            "The audited modular/nonnegative marginal systems are feasible. "
            "What remains unverified is the common labelled-subset realization/gluing condition."
        ),
    }
    out = Path(args.output)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
