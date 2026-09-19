"""Finite interface audit for the general three-leaf reduction, not A_p."""
from itertools import product
import json
from pathlib import Path
import random


def primes(limit):
    return [p for p in range(2, limit+1) if all(p%d for d in range(2, int(p**0.5)+1))]


def coefficient_function(p, seq):
    d = len(seq[0])
    c = {(0,)*d: 1}
    for v in seq:
        nxt = dict(c)
        for g, wt in c.items():
            h = tuple((x+y)%p for x, y in zip(g, v))
            nxt[h] = (nxt.get(h, 0) - wt) % p
        c = {g: wt for g, wt in nxt.items() if wt}
    return c


def main():
    rng = random.Random(6192026)
    affine_fixtures = 0
    for p in [3, 5, 7, 11]:
        for d in [2, 3]:
            for _ in range(5):
                seq = []
                for j in range(d):
                    for i in range(p-1-int(j == d-1)):
                        seq.append(tuple(rng.randrange(p) if k < j else int(k == j) for k in range(d)))
                assert len(seq) == d*(p-1)-1
                c = coefficient_function(p, seq)
                assert c[(0,)*d] == 1
                ell = []
                for j in range(d):
                    e = tuple(int(k == j) for k in range(d))
                    ell.append((c.get(e, 0)-1)%p)
                for g in product(range(p), repeat=d):
                    assert c.get(g, 0) == (1+sum(x*y for x, y in zip(ell, g)))%p
                sigma = tuple(sum(v[j] for v in seq)%p for j in range(d))
                assert sum(x*y for x, y in zip(ell, sigma))%p == p-2
                affine_fixtures += 1

    small_exceptions = {}
    for p in primes(1000):
        if p < 11:
            continue
        rho, s = (p+1)//2, (p-1)//2
        one = [-1, -7, 7, 1, -4, -12]
        collision = [-1, -3, -6, 5, 0, -4, -9, -10]
        if p >= 23:
            assert len({x%p for x in one}) == len(one)
            assert len({x%p for x in collision}) == len(collision)
            assert s+(rho+2)+s+s+(p-2) == 3*p-1
            assert s+rho+2+s+(p-1)+(rho-2) == 3*p-1
        else:
            small_exceptions[p] = {
                "one_active_distinct": len({x%p for x in one}) == len(one),
                "t_collision_distinct": len({x%p for x in collision}) == len(collision),
            }
        assert (s+3*rho)%p == 1
        assert (rho+s)%p != (rho+2)%p
        assert rho+2+p+3*s == 3*p+1
    report = {
        "status": "PASS",
        "scope": "Group-algebra affine-coefficient fixtures, scalar separations and arithmetic identities; not a proof-assistant certificate or exhaustive sequence search.",
        "affine_group_algebra_fixtures": affine_fixtures,
        "prime_interfaces_checked": len([p for p in primes(1000) if p >= 11]),
        "small_prime_separation_checks": small_exceptions,
    }
    Path(__file__).with_name("general_star_verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
