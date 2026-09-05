"""Checkpointed exact extension of e_1^3 e_2^3 e_3^3 e_4^3.

This uses the proved height bound and the separately computed exclusion of
five tripled elements. Every new support vector therefore has capacity two.
Incomplete root branches are explicitly reported and are never exclusions.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time

from atom_five_triples import BASIS, INF, ORDER, decode, encode, extend_distances, make_tables


def run_root(root, core_dist, n, m, initial, plus, neg, node_limit, deadline):
    multiplicity = [0] * ORDER
    for g in BASIS:
        multiplicity[g] = 3
    levels = [0] * (n + 1)
    leaves = [0] * (n + 1)
    nodes = 0
    max_added = []
    terminal = []
    complete = True
    started = time.monotonic()

    def dfs(dist, candidates, added):
        nonlocal nodes, complete, max_added
        nodes += 1
        if nodes > node_limit or time.monotonic() >= deadline:
            complete = False
            return
        length = 12 + len(added)
        levels[length] += 1
        if len(added) > len(max_added):
            max_added = added[:]
        if length == n:
            terminal.append(added[:])
            return
        any_child = False
        for i, g in enumerate(candidates):
            if multiplicity[g] >= 2:
                continue
            assert dist[neg[g]] + 1 > m
            new_dist = extend_distances(dist, g, plus)
            multiplicity[g] += 1
            next_candidates = [h for h in candidates[i:]
                               if multiplicity[h] < 2 and new_dist[neg[h]] + 1 > m]
            any_child = True
            dfs(new_dist, next_candidates, added + [g])
            multiplicity[g] -= 1
            if not complete:
                return
        if not any_child:
            leaves[length] += 1

    root_dist = extend_distances(core_dist, root, plus)
    multiplicity[root] = 1
    remaining = [h for h in initial if h >= root and root_dist[neg[h]] + 1 > m]
    dfs(root_dist, remaining, [root])
    return {
        "root": root, "root_coordinates": list(decode(root)),
        "completed_exhaustively": complete, "nodes": nodes,
        "nodes_by_length": {str(i): k for i, k in enumerate(levels) if k},
        "leaves_by_length": {str(i): k for i, k in enumerate(leaves) if k},
        "max_reached_length": 12 + len(max_added),
        "one_longest_extension": max_added,
        "terminal_extensions": terminal,
        "seconds": round(time.monotonic() - started, 6),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("A", "B"), required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--node-limit", type=int, default=100000)
    parser.add_argument("--seconds", type=float, default=45)
    parser.add_argument("--root-index", type=int)
    args = parser.parse_args()
    n, m = (21, 13) if args.case == "A" else (20, 14)
    plus, neg = make_tables()
    dist = [INF] * ORDER
    dist[0] = 0
    for g in BASIS:
        for _ in range(3):
            assert dist[neg[g]] == INF
            dist = extend_distances(dist, g, plus)
    initial = [g for g in range(1, ORDER) if g not in BASIS and dist[neg[g]] + 1 > m]
    # Any extension has a coordinate-permutation image whose numerically least
    # member is the least member of its coordinate orbit. Retain these roots.
    roots = [g for g in initial if tuple(sorted(decode(g), reverse=True)) == decode(g)]
    selected = roots if args.root_index is None else [roots[args.root_index]]
    result = {
        "case": args.case, "n": n, "m": m,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency": "five-triple exclusion; new support capacities at most two",
        "initial_safe_candidates": initial,
        "canonical_roots": roots,
        "selected_roots": selected,
        "all_selected_roots_completed": False,
        "all_roots_selected": args.root_index is None,
        "runs": [],
    }
    deadline = time.monotonic() + args.seconds
    out = Path(args.output)
    for root in selected:
        if time.monotonic() >= deadline:
            break
        record = run_root(root, dist, n, m, initial, plus, neg, args.node_limit, deadline)
        result["runs"].append(record)
        result["all_selected_roots_completed"] = (
            len(result["runs"]) == len(selected)
            and all(r["completed_exhaustively"] for r in result["runs"]))
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({k: record[k] for k in
                          ("root_coordinates", "completed_exhaustively", "nodes",
                           "max_reached_length", "seconds")}), flush=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
