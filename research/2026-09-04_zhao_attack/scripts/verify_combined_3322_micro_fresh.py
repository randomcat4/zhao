"""Fresh full 3322 length-16 leaf and four-outside-position witness audit.

Uses only this auditor's own exact-length bitset helpers. Does not execute or
import the author's leaf-profile or witness-generation implementation.
"""
from collections import Counter
from functools import reduce
from itertools import combinations, product
from operator import or_
import json
import time

from verify_combined_scope_fresh import BASE, BIT, M, NEG, Q, V, W, digest, one_position, safe_blocks


def main():
    start = time.monotonic()
    profile_path = BASE / "evidence" / "atom_3322_leaf_profiles.jsonl"
    cert_path = BASE / "evidence" / "atom_3322_outside_micro.json"
    tree_path = BASE / "evidence" / "atom_3322_m13_blocks.jsonl"
    profiles = [json.loads(s) for s in profile_path.read_text(encoding="utf-8").splitlines()]
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    old_tree = [json.loads(s) for s in tree_path.read_text(encoding="utf-8").splitlines()]
    profile_meta, old_meta = profiles[0], old_tree[0]
    assert profile_meta["mode"] == "3322" and profile_meta["m"] == M
    assert profile_meta["target"] == 16 and profiles[-1]["all_roots_completed"]
    assert cert["source_sha256"] == digest(profile_path)
    assert cert["script_sha256"] == digest(BASE / "scripts" / "atom_3322_outside_micro.py")
    assert cert["status"] == "EXHAUSTIVE_NO_SURVIVORS" and not cert["survivors"]

    leaf_rows = [r for r in profiles if r["type"] == "leaf_profile"]
    leaf_table = {tuple(r["blocks"]): r for r in leaf_rows}
    assert len(leaf_table) == len(leaf_rows) == 15684
    certificate_rows = cert["all_checks_with_explicit_witness"]
    certificate = {(tuple(r["blocks"]), tuple(r["chosen_outside"])): r for r in certificate_rows}
    assert len(certificate) == len(certificate_rows) == 8709

    basis_sequence = [1]*3 + [5]*3 + [25]*2 + [125]*2
    assert basis_sequence == cert["core_basis_encoded"]
    state = [0]*(M+1)
    for coeffs in product(range(4), range(4), range(3), range(3)):
        state[sum(coeffs)] |= BIT[sum(x*w for x,w in zip(coeffs,W))]
    state = tuple(state)
    initial = safe_blocks(state, [g for g in range(1,Q) if g not in W])
    permutations = [(a,b,c,d) for a,b in ((0,1),(1,0)) for c,d in ((2,3),(3,2))]
    roots = [g for g in initial if g == min(sum(V[g][p[j]]*W[j] for j in range(4)) for p in permutations)]
    assert roots == profile_meta["canonical_roots"] == old_meta["canonical_roots"]
    assert initial == profile_meta["initial_safe_candidates"] == old_meta["initial_safe_candidates"]

    found_leaves, found_checks = set(), set()
    distribution, witness_lengths = Counter(), Counter()
    levels, per_root = Counter(), {}
    eligible = 0

    def walk(current, candidates, blocks, root_levels):
        nonlocal eligible
        length = 10+2*len(blocks)
        levels[length] += 1
        root_levels[length] += 1
        if length == 16:
            assert blocks not in found_leaves
            found_leaves.add(blocks)
            record = leaf_table[blocks]
            # ALL 625 elements, including zero and elements already in the core.
            upto12 = reduce(or_, current[:M], 0)
            unary = [g for g in range(Q) if not (upto12 & BIT[NEG[g]])]
            assert unary == record["safe_single_additions"], blocks
            support = set(W) | set(blocks)
            outside = [g for g in unary if g not in support]
            distribution[len(outside)] += 1
            eligible += len(outside) >= 4
            core = basis_sequence + [g for g in blocks for _ in range(2)]
            for chosen in combinations(outside, 4):
                key = (blocks, chosen)
                assert key not in found_checks
                found_checks.add(key)
                row = certificate[key]
                full = core + list(chosen)
                positions = row["zero_sum_positions_zero_based"]
                assert positions is not None and 1 <= len(positions) <= M
                assert len(set(positions)) == len(positions)
                assert all(type(i) is int and 0 <= i < 20 for i in positions)
                assert all(sum(V[full[i]][j] for i in positions) % 5 == 0 for j in range(4)), key
                witness_lengths[len(positions)] += 1
            return
        for i, g in enumerate(candidates):
            added = one_position(one_position(current,g),g)
            walk(added, safe_blocks(added,candidates[i+1:]), blocks+(g,), root_levels)

    for root in roots:
        root_levels = Counter()
        added = one_position(one_position(state,root),root)
        walk(added,safe_blocks(added,[g for g in initial if g>root]),(root,),root_levels)
        per_root[root] = {str(k):v for k,v in sorted(root_levels.items())}
    assert found_leaves == set(leaf_table)
    assert found_checks == set(certificate)
    assert len(found_checks) == cert["four_subset_denominator"] == cert["checked_four_subsets"] == 8709
    assert len(found_leaves) == cert["leaf_denominator"] == 15684
    assert eligible == cert["eligible_leaf_count"] == 6437
    assert {str(k):v for k,v in sorted(distribution.items())} == cert["outside_safe_count_distribution"]
    tree_rows = {r["root"]: r for r in old_tree if r["type"] == "root"}
    for root in roots:
        assert per_root[root] == tree_rows[root]["nodes_by_length"]
    result = {"status":"PASS", "independent_full_leaf_regeneration":True,
              "all_safe_single_lists_match":True, "all_witnesses_direct_coordinate_checked":True,
              "root_count":len(roots), "node_count":sum(levels.values()),
              "nodes_by_length":dict(sorted(levels.items())), "leaf_count":len(found_leaves),
              "outside_safe_count_distribution":dict(sorted(distribution.items())),
              "eligible_leaves":eligible, "four_subset_count":len(found_checks),
              "witness_length_distribution":dict(sorted(witness_lengths.items())),
              "script_sha256":digest(__import__("pathlib").Path(__file__)),
              "inputs_sha256": {str(p.relative_to(BASE)):digest(p) for p in
                  (profile_path,cert_path,tree_path,BASE/"scripts"/"verify_combined_scope_fresh.py")},
              "elapsed_seconds":time.monotonic()-start,
              "mathematical_scope":"3322-basis core with three extra distinct double blocks and four distinct outside single positions; no endpoint solution"}
    output = BASE/"evidence"/"verify_combined_3322_micro_fresh.json"
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
