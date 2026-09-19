"""Exact standalone path and capacity audit for four small-star models.

Mathematical modelling is documented in two_leaf_small_star_constant_exclusion.md.
This program enumerates every containing-x path and works uniformly over p>=149.
"""
from itertools import combinations, permutations
from fractions import Fraction as F
from pathlib import Path
import json
import time

MODELS = {
    "M2_merged": {"mass": {"x": 2, "u": 2, "t": 4, "v": -5},
                  "degree": {"x": 9, "u": 2, "t": -3, "v": -3}},
    "M2_distinct": {"mass": {"x": 2, "u": 2, "t": 4, "v": -5, "z": -5},
                    "degree": {"x": 9, "u": 2, "t": -3, "v": -1, "z": -1}},
    "M1_merged": {"mass": {"x": 2, "u": 2, "t": 2, "v": -3},
                  "degree": {"x": 7, "u": 2, "t": -1, "v": -3}},
    "M1_one_active": {"mass": {"x": 2, "u": 2, "t": 2, "v": -3, "z": -3},
                      "degree": {"x": 7, "u": 2, "t": -1, "v": -1, "z": -1}},
}


def affine_residue(twice):
    assert isinstance(twice, int) and abs(twice) < 149
    if twice % 2:
        return F(1, 2), F(twice, 2)
    return (F(int(twice < 0)), F(twice, 2))


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def capacity_interval(masses, missing):
    inequalities = []
    for a, b in masses:
        inequalities += [(a, b-1), (1-a, -4-b)]
    total = (F(0), F(0))
    for val in masses+missing:
        total = add(total, val)
    inequalities.append((3-total[0], -3-total[1]))
    lo, hi = F(149), None
    for a, b in inequalities:
        if a > 0:
            lo = max(lo, -b/a)
        elif a < 0:
            bound = -b/a
            hi = bound if hi is None else min(hi, bound)
        elif b < 0:
            return None
    if hi is not None and lo > hi:
        return None
    return str(lo), str(hi)


def main():
    root = Path(__file__).parent
    reports = {}
    start = time.monotonic()
    for model, data in MODELS.items():
        mass, degree = data["mass"], data["degree"]
        others = [name for name in mass if name != "x"]
        limit = 11+len(mass)
        total, bad_count, largest, fixed_count = 0, 0, 0, 0
        survivors = []
        for size in range(len(others)+1):
            for extra in combinations(others, size):
                names = ("x",)+extra
                for n in range(len(names), limit+1):
                    for indices in permutations(range(n), len(names)):
                        pos = dict(zip(names, indices))
                        for loop in [False, True]:
                            targets = [1]*n
                            for name, i in pos.items():
                                targets[i] = degree[name]
                            targets[0] += 2*loop
                            previous, current, forms = (0, 0), (1, 0), []
                            for i in range(n):
                                forms.append(current)
                                nxt = (-previous[0], targets[i]-previous[1])
                                if i == 0 and loop:
                                    nxt = (nxt[0]-current[0], nxt[1]-current[1])
                                previous, current = current, nxt
                            equations = [current]
                            equations += [(forms[i][0], forms[i][1]-mass[name]) for name, i in pos.items()]
                            nonzero = [abs(c) for a, c in equations if not a and c]
                            pivot = next((r for r in equations if r[0]), None)
                            if pivot:
                                a, c = pivot
                                assert abs(a) == 1
                                nonzero += [abs(a*cc-aa*c) for aa, cc in equations if a*cc-aa*c]
                            total += 1
                            if nonzero:
                                witness = min(nonzero)
                                assert witness < 149
                                largest = max(largest, witness)
                                bad_count += 1
                                continue
                            if pivot is None:
                                survivors.append({"n": n, "positions": pos, "loop": loop, "T": "free"})
                                continue
                            T = -c//a
                            fixed_count += 1
                            masses = [affine_residue(a*T+c) for a, c in forms]
                            missing = [affine_residue(value) for name, value in mass.items() if name not in pos]
                            possible = capacity_interval(masses, missing)
                            if possible is not None:
                                survivors.append({"n": n, "positions": pos, "loop": loop, "T": T,
                                                  "p_interval": possible, "forms": forms})
                print(model, "".join(names), total, "remaining",len(survivors), flush=True)
        reports[model] = {"arrangements": total, "bounded_integer_contradictions": bad_count,
                          "maximum_contradiction_integer": largest, "fixed_capacity_checks": fixed_count,
                          "remaining": survivors, "input_twice_mass_degree": data}
        (root/"small_star_constant_verification.json").write_text(json.dumps(reports, indent=2)+"\n")
    print("seconds",time.monotonic()-start)
    assert all(not r["remaining"] for r in reports.values()), "Unresolved scalar cases remain"
    print("PASS: all four constant small-star models excluded for every prime p>=149")


if __name__ == "__main__":
    main()
