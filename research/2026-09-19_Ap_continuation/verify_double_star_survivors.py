"""Exact all-prime audit of the residual scalar catalogue.

Catalogue completeness is checked by probe_double_star.py's exhaustive pass;
this file checks each recorded residual and the final capacity/completion step.
"""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json
import gzip


def residue_affine(r, modulus):
    r = F(r)
    assert r.denominator in [1, 2, 4] and abs(r.numerator) < 149
    a, d = r.numerator, r.denominator
    if not a:
        return F(0), F(0)
    k = (-a * pow(modulus % d, -1, d)) % d if d > 1 else 0
    if k == 0 and a < 0:
        k = d
    return F(k, d), F(a, d)


def add(*pairs):
    return tuple(sum(q[i] for q in pairs) for i in range(2))


def neg(pair):
    return tuple(-x for x in pair)


def interval(inequalities):
    lo, hi = F(149), None
    for a, b in inequalities:  # a*p+b >=0
        if a > 0:
            lo = max(lo, -b/a)
        elif a < 0:
            bound = -b/a
            hi = bound if hi is None else min(hi, bound)
        elif b < 0:
            return None
    return None if hi is not None and lo > hi else (lo, hi)


def main():
    root = Path(__file__).parent
    source = root / "double_star_scalar_survivors.json"
    records = json.loads(source.read_text() if source.exists() else gzip.decompress(source.with_suffix(".json.gz").read_bytes()))
    free, fixed, remaining = 0, 0, []
    base = Counter({(0, F(-1, 2)): 3, (0, F(2)): 2, (0, F(1)): 2,
                    (-1, F(0)): 1, (1, F(1, 2)): 1, (0, F(-3, 2)): 1})
    for q in records:
        par = q["parameters"]
        if par[0] == "V_free":
            assert par == ["V_free", -1, 0, -1]  # T=-1
            assert set(q["positions"]) == {"x", "u", "z"}
            multiset = Counter((b, F(c-a, 2)) for a, b, c in q["multiplicity_forms"])
            assert all(multiset[k] >= count for k, count in base.items())
            # These ten entries plus the missing v,t classes already total
            # 3s + 6 + (p-L) + (p-M) + (s-1) + L + M = 4p+3.
            free += 1
            continue
        V, T = map(F, par)
        fixed += 1
        for mod in [1, 3]:
            L = residue_affine(V/2, mod)
            M = residue_affine((-1-V)/2, mod)
            known = {"x": (F(0), F(1)), "u": (F(0), F(1)), "v": L, "t": M,
                     "z": (F(1, 2), F(-3, 2))}
            masses = [residue_affine((a*T+b*V+c)/2, mod) for a, b, c in q["multiplicity_forms"]]
            conditions = [add(L, neg(M)), add(M, (0, -2)), add((1, -4), neg(L))]
            for mass in masses:
                conditions.extend([add(mass, (0, -1)), add((1, -4), neg(mass))])
            total = add(*masses, *(mass for name, mass in known.items() if name not in q["positions"]))
            conditions.append(add((1*3, -3), neg(total)))
            possible = interval(conditions)
            if possible is not None:
                assert set(q["positions"]) == {"x", "t"}
                assert V in [F(1, 2), F(5, 2)] and mod == 3
                remaining.append({"V": str(V), "mod4": mod, "n": q["n"], "positions": q["positions"],
                                  "loop": q["loop"], "p_interval": [str(x) for x in possible]})

    # A distinct component containing u can contain v,z but not x,t.
    # Swap x<->u and v<->t. Its parameter is V'=-1-V. Only the x,
    # xt, xz, xtz subcatalogues apply. Neither target occurs even modulo
    # a prime >=149: every rational difference has nonzero small numerator.
    for V in [F(1, 2), F(5, 2)]:
        target = -1-V
        for q in records:
            if set(q["positions"]) <= {"x", "t", "z"}:
                assert q["parameters"][0] != "V_free"
                diff = F(q["parameters"][0])-target
                assert diff and abs(diff.numerator) < 149 and diff.denominator < 149

    report = {"status": "PASS", "fixed_scalar_cases": fixed, "free_scalar_cases": free,
              "all_prime_capacity_checks": 2*fixed,
              "cases_after_individual_capacity": remaining,
              "cases_after_second_center_completion": 0,
              "free_case_mandatory_mass_lower_bound": "4p+3 > 3p-3",
              "scope": "Exact affine-in-p inequalities for both odd residue classes modulo 4, and rational second-component incompatibility. Conditional on the exhaustive scalar catalogue and the stated graph model."}
    (root/"double_star_survivor_verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
