"""Explore two-reflection paths for double stars with both leaf counts >=3.

This is a necessary scalar relaxation, not a construction or proof of A_p.
"""
from itertools import combinations, permutations
from fractions import Fraction
from pathlib import Path
import argparse
import json
import time

DEG = {"x": (-1, 4), "u": (1, 5), "v": (0, -1), "t": (0, -1), "z": (0, -1)}
MASS = {"x": (0, 2), "u": (0, 2), "v": (1, 0), "t": (-1, -1), "z": (0, -3)}


def equations(n, pos, loop):
    labels = {i: name for name, i in pos.items()}
    seq = [(1, 0, 0)]
    pv, pc = DEG.get(labels.get(0), (0, 1))
    seq.append((-int(loop), pv, pc + 2 * loop))
    for i in range(1, n):
        pv, pc = DEG.get(labels.get(i), (0, 1))
        a, b, c = seq[i - 1]
        seq.append((-a, pv - b, pc - c))
    eqs = [seq[-1]]
    for name, idx in pos.items():
        a, b, c = seq[idx]
        mv, mc = MASS[name]
        eqs.append((a, b - mv, c - mc))
    return eqs, seq[:-1]


def classify(eqs):
    first = next((r for r in eqs if r[0] or r[1]), None)
    bad = [abs(c) for a, b, c in eqs if not a and not b and c]
    if bad:
        return None, min(bad)
    if first is None:
        return ("free",), 0
    a, b, c = first
    other = next((r for r in eqs if a * r[1] != b * r[0]), None)
    if other:
        d, e, f = other
        den = a * e - b * d
        nt, nv = b * f - c * e, c * d - a * f
        residues = [abs(aa * nt + bb * nv + cc * den) for aa, bb, cc in eqs
                    if aa * nt + bb * nv + cc * den]
        if residues:
            return None, min(residues)
        return (str(Fraction(nv, den)), str(Fraction(nt, den))), 0
    residues = [abs(a * cc - aa * c) if a else abs(b * cc - bb * c)
                for aa, bb, cc in eqs]
    residues = [v for v in residues if v]
    if residues:
        return None, min(residues)
    if not a:
        return (str(Fraction(-c, b)), "T_free"), 0
    return ("V_free", a, b, c), 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-special", type=int, default=5)
    args = ap.parse_args()
    results = {}
    survivors = []
    start = time.monotonic()
    for k in range(args.max_special):
        for rest in combinations(["u", "v", "t", "z"], k):
            names = ("x",) + rest
            counts = {}
            tested, residual_bound = 0, 0
            examples = {}
            for n in range(len(names), 17):
                for indices in permutations(range(n), len(names)):
                    pos = dict(zip(names, indices))
                    for loop in [False, True]:
                        eqs, seq = equations(n, pos, loop)
                        key, residual = classify(eqs)
                        tested += 1
                        residual_bound = max(residual_bound, residual)
                        if key is not None:
                            survivors.append({"n": n, "positions": pos, "loop": loop,
                                              "parameters": key, "multiplicity_forms": seq})
                            label = key[0]
                            counts[label] = counts.get(label, 0) + 1
                            examples.setdefault(label, {"n": n, "positions": pos, "loop": loop,
                                                        "parameters": key, "multiplicity_forms": seq})
            result = {"tested": tested, "consistent_V_residues": counts,
                      "max_inconsistency_residual": residual_bound, "examples": examples}
            results["".join(names)] = result
            print("".join(names), tested, counts, "residual<=", residual_bound, flush=True)
            Path(__file__).with_name("double_star_scalar_probe.json").write_text(json.dumps(results, indent=2) + "\n")
    print("seconds", time.monotonic() - start)
    Path(__file__).with_name("double_star_scalar_survivors.json").write_text(json.dumps(survivors, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
