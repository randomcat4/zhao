"""Audit finite graph and group-algebra interfaces; not an A_p proof."""
from itertools import combinations, product, permutations
from fractions import Fraction as F
from pathlib import Path
import json
import random
from verify_general_star import coefficient_function


def covers(n, edges):
    for k in range(n + 1):
        out = [q for q in combinations(range(n), k)
               if all(i in q or j in q for i, j in edges)]
        if out:
            return k, out


def det(a):
    n = len(a)
    out = F(0)
    for q in permutations(range(n)):
        term = F((-1) ** sum(q[i] > q[j] for i in range(n) for j in range(i + 1, n)))
        for i in range(n):
            term *= a[i][q[i]]
        out += term
    return out


def main():
    # Every fixed-sum graph is a disjoint union of these components.
    components = []
    for a in range(1, 4):
        for b in range(a, 5):
            components.append((a + b, [(i, a + j) for i in range(a) for j in range(b)]))
    for a in range(2, 5):
        components.append((a, list(combinations(range(a), 2))))
    checked = 0
    for count in [1, 2, 3]:
        for comps in combinations(range(len(components)), count):
            n, edges = 0, []
            for idx in comps:
                v, es = components[idx]
                edges += [(i + n, j + n) for i, j in es]
                n += v
            if n > 14:
                continue
            tau, cv = covers(n, edges)
            if tau > 3:
                continue
            assert len(cv) <= 2 ** tau
            # Add one isolated d: no minimum cover uses it.
            t2, cv2 = covers(n + 1, edges)
            assert t2 == tau and cv2 == cv
            if tau == 2:
                containing_d = [q for q in combinations(range(n + 1), 3)
                                if n in q and all(i in q or j in q for i, j in edges)]
                assert len(containing_d) <= 4
            checked += 1

    rng = random.Random(19092026)
    fixtures = 0
    for p in [3, 5, 7]:
        for d in [2, 3]:
            for _ in range(3):
                # Triangular maximal zero-free sequences, guaranteed by the
                # last nonzero coordinate argument.
                seq = [tuple(rng.randrange(p) if k < j else int(k == j)
                             for k in range(d))
                       for j in range(d) for i in range(p - 1)]
                c = coefficient_function(p, seq)
                assert all(c.get(x, 0) == 1 for x in product(range(p), repeat=d))
                for idx in [0, len(seq) // 2, len(seq) - 1]:
                    sub = seq[:idx] + seq[idx + 1:]
                    c1 = coefficient_function(p, sub)
                    ell = [(c1.get(tuple(int(k == j) for k in range(d)), 0) - 1) % p
                           for j in range(d)]
                    assert sum(u * v for u, v in zip(ell, seq[idx])) % p == 1
                    assert all(c1.get(x, 0) == (1 + sum(u * v for u, v in zip(ell, x))) % p
                               for x in product(range(p), repeat=d))
                    fixtures += 1

    # Formal deletion-functionals for the K_(2,L) branch. Rational entries
    # mean residues modulo odd p; this is not numerical approximation.
    s, L = F(-1, 2), F(-1, 4)
    matrix = [[F(1), -1 - L, L - 3],
              [s - 4, F(1), 10 - 3 * s],
              [-s / 2, 3 * s / 2 - 2, F(1)]]
    assert det(matrix) == F(-197, 16)
    report = {
        "status": "PASS",
        "scope": "Finite fixed-sum component graph audit, maximal zero-free deletion fixtures, and exact rational determinant. Not exhaustive A_p verification.",
        "graph_fixtures": checked,
        "deleted_maximal_zero_free_fixtures": fixtures,
        "K2L_functional_matrix": [[str(x) for x in row] for row in matrix],
        "K2L_determinant": str(det(matrix)),
        "exceptional_prime_for_this_basis_argument": 197,
    }
    Path(__file__).with_name("two_leaf_verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
