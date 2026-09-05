#!/usr/bin/env python3
"""Independent finite-interface checker for the double-only Zhao proof.

This program was written for the second audit.  It does not import either
checker in the submitted package.  It verifies package integrity, recomputes
all finite congruence/sign tables used by the hand proof, and records the
remaining purely universal graph/set-system arguments as manual obligations.
It is not an exhaustive search over sequences in F_5^4.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import pathlib
import tempfile
import zipfile

P = 5
EXPECTED_ZIP_SHA256 = "99451451102aa38ff1959fe375510ae4deed4558886d8ca3edc3ba4b8de5fad3"


def require(cond: bool, message: str) -> None:
    if not cond:
        raise AssertionError(message)


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_manifest(path: pathlib.Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        digest, name = raw.split(None, 1)
        name = name.lstrip(" *")
        rows.append((digest, name))
    return rows


def matching_number(vertices: int, edges: tuple[tuple[int, int], ...]) -> int:
    best = 0

    def rec(index: int, used: int, size: int) -> None:
        nonlocal best
        if size + (len(edges) - index) <= best:
            return
        if index == len(edges):
            best = max(best, size)
            return
        rec(index + 1, used, size)
        u, v = edges[index]
        mask = (1 << u) | (1 << v)
        if used & mask == 0:
            rec(index + 1, used | mask, size + 1)

    rec(0, 0, 0)
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=pathlib.Path)
    parser.add_argument("--json", type=pathlib.Path, default=pathlib.Path("independent_check.json"))
    args = parser.parse_args()

    package = args.package.resolve()
    result: dict[str, object] = {
        "scope": "finite interfaces and integrity; universal proof audited separately",
        "package": str(package),
    }

    digest = sha256_file(package)
    require(digest == EXPECTED_ZIP_SHA256, "outer zip SHA-256 mismatch")
    result["outer_zip_sha256"] = digest

    with tempfile.TemporaryDirectory(prefix="zhao-independent-") as td:
        root = pathlib.Path(td)
        with zipfile.ZipFile(package) as zf:
            zf.extractall(root)
        candidates = list(root.glob("*/SHA256SUMS.txt"))
        require(len(candidates) == 1, "exactly one manifest expected")
        manifest = candidates[0]
        base = manifest.parent
        checked: list[dict[str, str]] = []
        for expected, name in parse_manifest(manifest):
            target = base / name
            require(target.is_file(), f"manifest target missing: {name}")
            actual = sha256_file(target)
            require(actual == expected, f"manifest hash mismatch: {name}")
            checked.append({"name": name, "sha256": actual})
        result["manifest_files"] = checked

    # Augmentation-ideal top degrees for d=3,4.
    nilpotency = {}
    for d in (3, 4):
        degrees = [sum(alpha) for alpha in itertools.product(range(P), repeat=d)]
        require(len(degrees) == P**d, "truncated monomial dimension")
        require(max(degrees) == 4 * d, "top augmentation degree")
        nilpotency[str(d)] = {"dimension": P**d, "top_degree": max(degrees), "vanishing_power": 4*d+1}
    result["augmentation"] = nilpotency

    # 18-position lemma: only (Z16,Z17)=(0,1) survives exact range plus mod 5.
    eighteen = []
    for z16 in range(3):
        for z17 in range(2):
            value = 1 + z16 - z17
            if value % P == 0:
                eighteen.append((z16, z17, value))
    require(eighteen == [(0, 1, 0)], "18-position residue classification")
    result["eighteen_position"] = eighteen

    # The actual three-position core a,a,2a covers every residue on <a>.
    core = (1, 1, 2)
    core_witness: dict[int, dict[str, object]] = {}
    for mask in range(1 << len(core)):
        residue = sum(core[j] for j in range(3) if mask & (1 << j)) % P
        size = mask.bit_count()
        old = core_witness.get(residue)
        if old is None or size < int(old["size"]):
            core_witness[residue] = {"mask": format(mask, "03b"), "size": size}
    require(set(core_witness) == set(range(P)), "core does not cover anchor line")
    require(max(int(v["size"]) for v in core_witness.values()) == 3, "core capacity exceeds three")
    result["core_subsum_witnesses"] = core_witness

    # With 0,1,2 reserved anchors, residues 0,3,4 lift to a short zero-sum;
    # only 1 and 2 can remain for quotient-zero subsets of length <=11.
    allowed = []
    cancelled = {}
    for c in range(P):
        ks = [k for k in range(3) if (c + k) % P == 0]
        if ks:
            k = min(ks)
            require(11 + k <= 13, "anchor lift length failure")
            cancelled[c] = k
        else:
            allowed.append(c)
    require(allowed == [1, 2], "wrong surviving anchor-line residues")
    require(set(allowed).isdisjoint({(-x) % P for x in allowed}), "surviving residues meet their negatives")
    result["two_anchor_lift"] = {"cancelled": cancelled, "allowed": allowed}

    # Forbidden balanced quotient-zero lengths.
    balanced = {n: [k for k in range(1, n) if k <= 11 and n-k <= 11] for n in (14, 15)}
    require(balanced[14] == list(range(3, 12)), "n=14 balanced interval")
    require(balanced[15] == list(range(4, 12)), "n=15 balanced interval")
    result["balanced_intervals"] = balanced

    # Fixed-sum graph component types at height <=2.
    components = []
    for left in (1, 2):
        for right in (1, 2):
            edges = tuple((u, left+v) for u in range(left) for v in range(right))
            nu = matching_number(left + right, edges)
            require(len(edges) <= 2*nu, "fixed-sum K_{r,s} bound")
            components.append({"type": f"K_{{{left},{right}}}", "edges": len(edges), "matching": nu})
    half_edges = ((0, 1),)
    require(matching_number(2, half_edges) == 1, "half-value component")
    components.append({"type": "half-value K_2", "edges": 1, "matching": 1})
    result["fixed_sum_components"] = components

    # n=14 quotient congruence: 2+2e=0 has no e in {0,1,2}.
    n14 = [e for e in range(3) if (2 + 2*e) % P == 0]
    require(n14 == [], "n=14 branch was not eliminated")
    result["n14_survivors"] = n14

    # Direct deletion-incidence enumeration for n=15, without using binomial formulas.
    full = (1 << 15) - 1
    records = 0
    totals = {2: set(), 3: set()}
    for k in (2, 3):
        for block_tuple in itertools.combinations(range(15), k):
            block = sum(1 << j for j in block_tuple)
            comp = full ^ block
            total = 0
            for deleted in range(15):
                bit = 1 << deleted
                contribution = 0
                if block & bit == 0:
                    contribution += (-1) ** k
                if comp & bit == 0:
                    contribution += (-1) ** (15-k)
                expected = (1 - 2*int(bool(block & bit))) if k == 2 else (-1 + 2*int(bool(block & bit)))
                require(contribution == expected, "deleted-position sign mismatch")
                total += contribution
                records += 1
            totals[k].add(total % P)
    require(records == (math.comb(15,2)+math.comb(15,3))*15, "deleted incidence denominator")
    require(totals == {2: {1}, 3: {1}}, "summed deletion residues")
    result["n15_deleted_incidences"] = {"records": records, "total_residues": {str(k): sorted(v) for k,v in totals.items()}}

    # Solve the two modular equations directly for every possible e.
    branch_rows = []
    for e in range(5):
        sols = []
        for fmod in range(5):
            for dmod in range(5):
                if (fmod + e) % P == 0 and (1 + e - fmod + 2*dmod) % P == 0:
                    sols.append((fmod, dmod))
        require(len(sols) == 1, "n=15 modular branch not unique")
        fmod, dmod = sols[0]
        branch_rows.append({"e": e, "f_mod_5": fmod, "fi_minus_ei_mod_5": dmod})
    require(branch_rows == [
        {"e":0,"f_mod_5":0,"fi_minus_ei_mod_5":2},
        {"e":1,"f_mod_5":4,"fi_minus_ei_mod_5":1},
        {"e":2,"f_mod_5":3,"fi_minus_ei_mod_5":0},
        {"e":3,"f_mod_5":2,"fi_minus_ei_mod_5":4},
        {"e":4,"f_mod_5":1,"fi_minus_ei_mod_5":3},
    ], "n=15 branch table")
    result["n15_modular_branches"] = branch_rows

    # Arithmetic endpoints of the five hand branches.
    branch_checks = {
        "e0_all_degrees_2": {"f": (15*2)//3, "block_pairs": math.comb(10,2), "available_shared_point_counts": 15*math.comb(2,2)},
        "e0_degree_7": {"outside_degree_lower_sum": 14*2, "outside_incidence_if_star": 2*7},
        "e1": {"outside_points": 13, "incidences_per_block": 2, "parity_obstruction": 13 % 2},
        "e2": {"outside_degree_upper": 3, "forced_residue": 0, "f_mod_5": 3},
        "e3": {"outside_degree_upper": 2, "forced_residue": 4},
        "e4": {"outside_degree_upper": 2, "forced_residue": 3},
    }
    require(branch_checks["e0_all_degrees_2"]["block_pairs"] > branch_checks["e0_all_degrees_2"]["available_shared_point_counts"], "e=0 pair count")
    require(branch_checks["e0_degree_7"]["outside_degree_lower_sum"] > branch_checks["e0_degree_7"]["outside_incidence_if_star"], "e=0 degree-seven count")
    require(branch_checks["e1"]["parity_obstruction"] == 1, "e=1 parity")
    require([x for x in range(4) if x % 5 == 0] == [0], "e=2 outside degree")
    require([x for x in range(3) if x % 5 == 4] == [], "e=3 outside degree")
    require([x for x in range(3) if x % 5 == 3] == [], "e=4 outside degree")
    result["branch_arithmetic"] = branch_checks

    # Original 17..21 deletion coefficient matrices.
    matrices = {}
    for n in range(17, 22):
        rows = []
        for retained in range(17, n+1):
            coeff = []
            for zlen in range(14, 18):
                coeff.append(((-1)**zlen * math.comb(n-zlen, retained-zlen)) % P if retained >= zlen else 0)
            rows.append({"retained": retained, "constant": math.comb(n, retained) % P, "coeff_Z14_to_Z17": coeff})
        matrices[str(n)] = rows
    result["deletion_matrices"] = matrices

    result["manual_universal_obligations_checked_in_report"] = [
        "triangle-free pair graph with matching number at most one is a star",
        "link graph at a triple-center has at least four disjoint edges when it has seven edges",
        "all five e-branches use only legal positional intersections and codegree at most two",
        "the quotient and complement length arguments preserve nonempty positional blocks",
    ]
    result["status"] = "PASS"
    args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("INDEPENDENT_FINITE_INTERFACE_CHECK_PASS")
    print(f"outer_zip_sha256={digest}")
    print(f"manifest_files={len(result['manifest_files'])}; deleted_position_records={records}; n15_branches={len(branch_rows)}")
    print("This is independent of the submitted Python checkers and is not a global sequence enumeration.")


if __name__ == "__main__":
    main()
