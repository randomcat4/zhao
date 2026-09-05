"""Independent finite audit for h11_continue_B_proof.md.

This checker deliberately does not import h11_continue_certify.py and does not
use its four-choice distance formula.  It enumerates all subsets of the eleven
actual positions for every candidate unordered pair (x,y).
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "verify_h11_final_fresh_recompute.json"
FIVE = range(5)
POINTS = [tuple((g // (5**i)) % 5 for i in range(3)) for g in range(125)]
ZERO = (0, 0, 0)
BASIS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
PERMS = list(itertools.permutations(range(3)))


def add(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((a[i] + b[i]) % 5 for i in range(3))


def neg(a: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((-z) % 5 for z in a)


def scale(c: int, a: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((c * z) % 5 for z in a)


def enc(a: tuple[int, int, int]) -> int:
    return a[0] + 5 * a[1] + 25 * a[2]


def dot(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return sum(a[i] * b[i] for i in range(3)) % 5


def actual_subset_profile(x: tuple[int, int, int], y: tuple[int, int, int]):
    """Return zero-freeness, distances and signed subset coefficients.

    The 2^11 subsets are built from the actual position list, so repeated group
    values remain separate positions (including the case x == y).
    """

    positions = [BASIS[0]] * 3 + [BASIS[1]] * 3 + [BASIS[2]] * 3 + [x, y]
    sums = [ZERO]
    sizes = [0]
    for p in positions:
        old = len(sums)
        for j in range(old):
            sums.append(add(sums[j], p))
            sizes.append(sizes[j] + 1)

    zero_free = not any(s == ZERO and k > 0 for s, k in zip(sums, sizes))
    distance = [99] * 125
    signed = [0] * 125
    for s, k in zip(sums, sizes):
        g = enc(s)
        if k < distance[g]:
            distance[g] = k
        signed[g] = (signed[g] + (1 if k % 2 == 0 else -1)) % 5
    return zero_free, distance, signed


def canonical_pair(x: tuple[int, int, int], y: tuple[int, int, int]) -> tuple[int, int]:
    images = []
    for p in PERMS:
        xp = tuple(x[i] for i in p)
        yp = tuple(y[i] for i in p)
        images.append(tuple(sorted((enc(xp), enc(yp)))))
    return min(images)


def normalized_directions():
    result = []
    for v in POINTS[1:]:
        first = next(z for z in v if z)
        result.append(scale(pow(first, -1, 5), v))
    return sorted(set(result), key=enc)


DIRECTIONS = normalized_directions()
ALL_LINES = {
    frozenset(enc(add(p, scale(j, v))) for j in FIVE)
    for p in POINTS
    for v in DIRECTIONS
}


def main_line_in_shape(m: set[int]) -> frozenset[int]:
    candidates = [line for line in ALL_LINES if line <= m]
    assert candidates
    for line in candidates:
        off = m - line
        if not off:
            return line
        if len(off) == 2:
            u, v = (POINTS[g] for g in off)
            midpoint = enc(scale(3, add(u, v)))  # (u+v)/2 in F_5
            if midpoint in line:
                return line
    raise AssertionError(f"not a line/symmetric-pair shape: {sorted(m)}")


def direction_of_line(line: frozenset[int]) -> tuple[int, int, int]:
    pts = [POINTS[g] for g in line]
    base = pts[0]
    for p in pts[1:]:
        d = add(p, neg(base))
        if d != ZERO:
            first = next(z for z in d if z)
            return scale(pow(first, -1, 5), d)
    raise AssertionError("degenerate line")


def check_geometry_properties(m: set[int]):
    line = main_line_in_shape(m)
    direction = direction_of_line(line)
    parallel_lines = {
        frozenset(enc(add(p, scale(j, direction))) for j in FIVE) for p in POINTS
    }

    # Property I reduces two translates to M and M+d.
    large_intersections = 0
    for d in POINTS[1:]:
        shifted = {enc(add(POINTS[g], d)) for g in m}
        inter = frozenset(m & shifted)
        if len(inter) >= 5:
            large_intersections += 1
            assert len(inter) == 5 and inter in parallel_lines

    # Property II: translate A by -b/2 to reduce T+b to T.  Five-point
    # solutions are precisely 5-cliques in the graph a~b iff a+b lies in T.
    neighbors = []
    for a in range(125):
        neighbors.append(
            {b for b in range(125) if b != a and enc(add(POINTS[a], POINTS[b])) in m}
        )

    clique_count = 0

    def extend(prefix: tuple[int, ...], candidates: list[int]):
        nonlocal clique_count
        if len(prefix) == 5:
            clique_count += 1
            assert frozenset(prefix) in parallel_lines
            return
        needed = 5 - len(prefix)
        if len(candidates) < needed:
            return
        for j, v in enumerate(candidates):
            tail = candidates[j + 1 :]
            next_candidates = [w for w in tail if w in neighbors[v]]
            extend(prefix + (v,), next_candidates)

    extend((), list(range(125)))
    return {
        "main_line": sorted(line),
        "direction": list(direction),
        "large_translate_intersections": large_intersections,
        "five_cliques_for_untranslated_target": clique_count,
    }


def compositions_of_n(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions_of_n(total - first, parts - 1):
            yield (first,) + tail


def valid_scalar_choice(n: tuple[int, ...], k: tuple[int, ...], residue: int) -> bool:
    if sum(k) != 5 or any(k[i] > n[i] for i in FIVE):
        return False
    if sum(i * k[i] for i in FIVE) % 5 != residue:
        return False
    partial = [i for i in FIVE if 0 < k[i] < n[i]]
    if residue == 0:
        return len(partial) >= 2 or any(n[i] >= 3 for i in partial)
    return residue == 2 and bool(partial)


def scalar_audit():
    counts = list(compositions_of_n(9, 5))
    assert len(counts) == 715 and len(set(counts)) == 715
    independently_found = {}
    no_residue_zero = []
    for n in counts:
        choices = itertools.product(*(range(z + 1) for z in n))
        valid_zero = []
        valid_two = []
        for k in choices:
            if valid_scalar_choice(n, k, 0):
                valid_zero.append(k)
            if valid_scalar_choice(n, k, 2):
                valid_two.append(k)
        if valid_zero:
            independently_found[n] = (0, valid_zero[0])
        else:
            no_residue_zero.append(n)
            assert valid_two
            independently_found[n] = (2, valid_two[0])

    expected_exceptions = {
        tuple(5 if c == i else 4 if c == j else 0 for c in FIVE)
        for i in FIVE
        for j in FIVE
        if i != j
    }
    assert set(no_residue_zero) == expected_exceptions

    supplied = json.loads((ROOT / "h11_continue_scalar_egz_v2.json").read_text(encoding="utf-8"))
    supplied_rows = supplied["certificates"]
    lookup = {tuple(row["n"]): row for row in supplied_rows}
    assert len(supplied_rows) == len(lookup) == 715 and set(lookup) == set(counts)
    supplied_residues = Counter()
    for n, row in lookup.items():
        k = tuple(row["k"])
        residue = row["residue"]
        assert valid_scalar_choice(n, k, residue)
        supplied_residues[residue] += 1
    assert supplied_residues == Counter({0: 695, 2: 20})
    return {
        "count_vectors": len(counts),
        "independent_residue0_vectors": len(counts) - len(no_residue_zero),
        "forced_residue2_exception_vectors": len(no_residue_zero),
        "supplied_residue_counts": dict(supplied_residues),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    nonbasis = [POINTS[g] for g in range(125) if POINTS[g] not in BASIS]
    raw = []
    representatives = {}
    orbit_sizes = Counter()
    for x, y in itertools.combinations_with_replacement(nonbasis, 2):
        zero_free, distance, signed = actual_subset_profile(x, y)
        if not zero_free:
            continue

        # Recover ell from the signed subset polynomial itself, rather than
        # using the cross-term formula in the candidate checker.
        assert signed[0] == 1
        a = tuple((signed[enc(e)] - 1) % 5 for e in BASIS)
        assert a != ZERO
        assert all(signed[g] == (1 + dot(a, POINTS[g])) % 5 for g in range(125))
        sigma = ZERO
        for p in [BASIS[0]] * 3 + [BASIS[1]] * 3 + [BASIS[2]] * 3 + [x, y]:
            sigma = add(sigma, p)
        assert dot(a, sigma) == 3

        m = {g for g, d in enumerate(distance) if d == 99}
        e11 = {g for g, d in enumerate(distance) if d >= 11}
        e10_0 = {g for g, d in enumerate(distance) if d >= 10 and dot(a, POINTS[g]) == 0}
        e10_3 = {g for g, d in enumerate(distance) if d >= 10 and dot(a, POINTS[g]) == 3}
        assert all(dot(a, POINTS[g]) == 4 for g in m)
        assert e11 == m | {enc(sigma)}
        assert len(e10_0) <= 2 and e10_3 == {enc(sigma)}

        case = "F0_empty" if not e10_0 else "M_at_most_4" if len(m) <= 4 else "line_geometry"
        pair = tuple(sorted((enc(x), enc(y))))
        key = canonical_pair(x, y)
        raw.append((pair, case, key))
        orbit_sizes[key] += 1
        if pair == key:
            representatives[key] = {
                "a": list(a),
                "sigma": enc(sigma),
                "M": sorted(m),
                "E10_fiber0": sorted(e10_0),
                "case": case,
            }

    assert len(raw) == 738
    assert len(orbit_sizes) == len(representatives) == 131
    raw_cases = Counter(case for _, case, _ in raw)
    orbit_cases = Counter(row["case"] for row in representatives.values())
    assert raw_cases == Counter({"F0_empty": 519, "M_at_most_4": 195, "line_geometry": 24})
    assert orbit_cases == Counter({"F0_empty": 94, "M_at_most_4": 33, "line_geometry": 4})

    final_keys = sorted(key for key, row in representatives.items() if row["case"] == "line_geometry")
    assert final_keys == [(9, 31), (9, 49), (38, 47), (38, 108)]
    expected_m = {
        (9, 31): {enc((4, 0, z)) for z in FIVE} | {enc((3, 4, 0)), enc((0, 1, 4))},
        (9, 49): {enc((3, 4, z)) for z in FIVE} | {enc((4, 0, 0)), enc((2, 3, 4))},
        (38, 47): {enc((4, z, 0)) for z in FIVE},
        (38, 108): {enc((2, z, 4)) for z in FIVE},
    }
    geometry = {}
    for key in final_keys:
        m = set(representatives[key]["M"])
        assert m == expected_m[key]
        geometry[",".join(map(str, key))] = {
            "M": sorted(m),
            "property_checks_for_M": check_geometry_properties(m),
            "property_checks_for_minus_M": check_geometry_properties({enc(neg(POINTS[g])) for g in m}),
        }

    # Compare independent output to the frozen supplied classification only
    # after all independent assertions have passed.
    supplied = json.loads((ROOT / "h11_continue_certificate.json").read_text(encoding="utf-8"))
    supplied_raw = {
        (tuple(row["added"]), row["case"], tuple(row["orbit"])) for row in supplied["raw_coverage"]
    }
    assert supplied_raw == set(raw)
    supplied_reps = {tuple(row["added"]): row for row in supplied["orbits"]}
    assert set(supplied_reps) == set(representatives)
    for key, row in representatives.items():
        other = supplied_reps[key]
        assert row["a"] == other["a"]
        assert row["sigma"] == other["sigma"]
        assert row["M"] == other["M"]
        assert row["E10_fiber0"] == other["E10_fiber0"]
        assert row["case"] == other["case"]
        assert orbit_sizes[key] == other["orbit_size"]

    scalar = scalar_audit()
    frozen = {
        "h11_continue_B_proof.md": sha256(ROOT / "h11_continue_B_proof.md"),
        "h11_continue_certify.py": sha256(ROOT / "h11_continue_certify.py"),
        "h11_continue_certificate.json": sha256(ROOT / "h11_continue_certificate.json"),
        "h11_continue_scalar_egz_v2.json": sha256(ROOT / "h11_continue_scalar_egz_v2.json"),
        "formal/H11ScalarCertificate.lean": sha256(ROOT / "formal" / "H11ScalarCertificate.lean"),
    }
    result = {
        "status": "INDEPENDENT_FINITE_RECOMPUTATION_PASSED",
        "method": "all 2^11 actual-position subsets for every unordered nonbasis pair; no import of author checker",
        "raw_core_count": len(raw),
        "orbit_core_count": len(orbit_sizes),
        "raw_cases": dict(raw_cases),
        "orbit_cases": dict(orbit_cases),
        "final_orbit_keys": [list(key) for key in final_keys],
        "geometry": geometry,
        "scalar": scalar,
        "frozen_sha256": frozen,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "geometry"}, sort_keys=True))


if __name__ == "__main__":
    main()
