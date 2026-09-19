"""Independent exhaustive integer verifier of the double-star scalar catalogue.

No imports from the catalogue generator. All consistency operations use integer
2x2 determinants, with explicitly checked bounds valid for every p>=149.
"""
from itertools import combinations, permutations
from fractions import Fraction as F
from pathlib import Path
import json
import gzip
import time


def main():
    root = Path(__file__).parent
    source = root / "double_star_scalar_survivors.json"
    recorded = json.loads(source.read_text() if source.exists() else gzip.decompress(source.with_suffix(".json.gz").read_bytes()))
    catalogue = {}
    for q in recorded:
        key = (q["n"], tuple(sorted(q["positions"].items())), q["loop"])
        assert key not in catalogue
        catalogue[key] = q
    seen = set()
    count, inconsistent, maximum, maxdet = 0, 0, 0, 0
    family_counts = {}
    start = time.monotonic()
    for size in range(5):
        for extra in combinations("uvtz", size):
            names = ("x",) + extra
            local = 0
            for n in range(len(names), 17):
                for places in permutations(range(n), len(names)):
                    pos = dict(zip(names, places))
                    for loop in (False, True):
                        # Equations use unknowns T=2m_0 and V=2L.
                        # Build each degree target independently.
                        targets = [[0, 1] for _ in range(n)]
                        for name, idx in pos.items():
                            targets[idx] = {"x": [-1, 4], "u": [1, 5],
                                            "v": [0, -1], "t": [0, -1], "z": [0, -1]}[name]
                        targets[0][1] += 2*loop
                        previous = (0, 0, 0)
                        current = (1, 0, 0)
                        forms = []
                        for idx in range(n):
                            forms.append(current)
                            nxt = (-previous[0], targets[idx][0]-previous[1], targets[idx][1]-previous[2])
                            if idx == 0 and loop:
                                nxt = tuple(a-b for a, b in zip(nxt, current))
                            previous, current = current, nxt
                        eqs = [current]
                        for name, idx in pos.items():
                            a, b, c = forms[idx]
                            rv, rc = {"x": (0, 2), "u": (0, 2), "v": (1, 0),
                                      "t": (-1, -1), "z": (0, -3)}[name]
                            eqs.append((a, b-rv, c-rc))
                        key = (n, tuple(sorted(pos.items())), loop)
                        count += 1
                        local += 1
                        constants = [abs(c) for a, b, c in eqs if a == b == 0 and c]
                        contradiction = min(constants) if constants else 0
                        first = next((e for e in eqs if e[0] or e[1]), None)
                        if first is None:
                            assert contradiction and contradiction < 149, (n, pos, loop, eqs)
                            maximum = max(maximum, contradiction)
                            assert key not in catalogue
                            inconsistent += 1
                            continue
                        a, b, c = first
                        assert max(abs(a), abs(b)) < 149
                        second = next((e for e in eqs if a*e[1]-b*e[0]), None)
                        unique = None
                        if not contradiction and second is not None:
                            d, e, f = second
                            determinant = a*e-b*d
                            assert 0 < abs(determinant) < 149
                            maxdet = max(maxdet, abs(determinant))
                            nt, nv = b*f-c*e, c*d-a*f
                            residues = [abs(aa*nt+bb*nv+cc*determinant) for aa, bb, cc in eqs
                                        if aa*nt+bb*nv+cc*determinant]
                            if residues:
                                contradiction = min(residues)
                            else:
                                unique = (F(nv, determinant), F(nt, determinant))
                        elif not contradiction:
                            residues = [abs(a*cc-aa*c) if a else abs(b*cc-bb*c) for aa, bb, cc in eqs]
                            nonzero = [r for r in residues if r]
                            if nonzero:
                                contradiction = min(nonzero)
                        if contradiction:
                            assert 0 < contradiction < 149
                            maximum = max(maximum, contradiction)
                            assert key not in catalogue
                            inconsistent += 1
                            continue
                        assert key in catalogue
                        q = catalogue[key]
                        assert q["multiplicity_forms"] == [list(row) for row in forms]
                        if unique:
                            assert tuple(map(F, q["parameters"])) == unique
                        else:
                            assert q["parameters"] == ["V_free", -1, 0, -1]
                            assert a and b == 0 and F(-c, a) == -1
                        seen.add(key)
            family_counts["".join(names)] = local
            print("".join(names), local, flush=True)
    assert seen == set(catalogue)
    report = {"status": "PASS", "path_arrangements": count,
              "inconsistent_over_every_prime_ge149": inconsistent,
              "surviving_rational_parameter_cases": len(seen),
              "largest_contradiction_integer": maximum,
              "largest_pivot_determinant": maxdet,
              "family_counts": family_counts,
              "scope": "Independent exhaustive recurrence reconstruction with bounded integer determinants; covers all p>=149, not a finite-prime extrapolation."}
    (root/"double_star_catalogue_verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))
    print("elapsed_seconds", time.monotonic()-start)


if __name__ == "__main__":
    main()
