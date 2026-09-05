"""Bounded, resumable-by-root search of the (3,3,3,2) basis core.

Scope: exactly three tripled elements and a doubled element outside their
rank-three span. This does NOT cover cases with all doubles inside that span.
The no-four-triples reduction is an explicitly tagged external dependency.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time

from atom_five_triples import BASIS, INF, ORDER, decode, extend_distances, make_tables


def explore(root, initial, dist0, n, m, plus, neg, node_limit, deadline):
    counts = [0] * ORDER
    for i, g in enumerate(BASIS):
        counts[g] = 3 if i < 3 else 2
    levels = [0] * (n + 1)
    leaves = [0] * (n + 1)
    nodes = 0
    complete = True
    longest = []
    terminal = []
    started = time.monotonic()

    def dfs(dist, candidates, added):
        nonlocal nodes, complete, longest
        nodes += 1
        if nodes > node_limit or time.monotonic() >= deadline:
            complete = False
            return
        length = 11 + len(added)
        levels[length] += 1
        if len(added) > len(longest):
            longest = added[:]
        if length == n:
            terminal.append(added[:])
            return
        any_child = False
        for i, g in enumerate(candidates):
            if counts[g] >= 2:
                continue
            assert dist[neg[g]] + 1 > m
            updated = extend_distances(dist, g, plus)
            counts[g] += 1
            following = [h for h in candidates[i:]
                         if counts[h] < 2 and updated[neg[h]] + 1 > m]
            any_child = True
            dfs(updated, following, added + [g])
            counts[g] -= 1
            if not complete:
                return
        if not any_child:
            leaves[length] += 1

    d1 = extend_distances(dist0, root, plus)
    counts[root] = 1
    candidates = [h for h in initial if h >= root and d1[neg[h]] + 1 > m]
    dfs(d1, candidates, [root])
    return {
        "root": root, "root_coordinates": decode(root),
        "completed_exhaustively": complete,
        "nodes": nodes, "node_limit": node_limit,
        "nodes_by_length": {str(i): c for i, c in enumerate(levels) if c},
        "leaves_by_length": {str(i): c for i, c in enumerate(leaves) if c},
        "max_reached_length": 11 + len(longest),
        "one_longest_extension": longest,
        "terminal_extensions": terminal,
        "seconds": round(time.monotonic() - started, 6),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("A", "B"), default="A")
    parser.add_argument("--output", required=True)
    parser.add_argument("--seconds", type=float, default=45)
    parser.add_argument("--node-limit", type=int, default=100000)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--root-index", type=int)
    args = parser.parse_args()
    n, m = (21, 13) if args.case == "A" else (20, 14)
    plus, neg = make_tables()
    dist = [INF] * ORDER
    dist[0] = 0
    for i, g in enumerate(BASIS):
        for _ in range(3 if i < 3 else 2):
            assert dist[neg[g]] == INF
            dist = extend_distances(dist, g, plus)
    initial = [g for g in range(1, ORDER) if g not in BASIS and dist[neg[g]] + 1 > m]
    # Only permutations of the first three coordinates preserve this core.
    roots = [g for g in initial if tuple(sorted(decode(g)[:3], reverse=True)) == decode(g)[:3]]
    # Larger roots usually leave fewer remaining numerical candidates. This
    # changes run order only, not the symmetry coverage or branch definition.
    selected = list(reversed(roots)) if args.root_index is None else [roots[args.root_index]]
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "scope": "exactly three tripled elements and an independent doubled element",
        "uncovered_scope": "all doubled elements lie in the span of the three tripled elements",
        "dependency": "root candidate exclusion of four tripled elements, pending independent verification",
        "case": args.case, "n": n, "m": m, "core_multiplicities": [3, 3, 3, 2],
        "script_sha256": script_hash,
        "helper_sha256": hashlib.sha256(Path(__file__).with_name("atom_five_triples.py").read_bytes()).hexdigest(),
        "initial_safe_candidates": initial,
        "canonical_roots": roots,
        "runs": [],
        "attempt_history": [],
    }
    output = Path(args.output)
    if args.resume and output.exists():
        old = json.loads(output.read_text(encoding="utf-8"))
        assert old["script_sha256"] == script_hash
        assert old["case"] == args.case
        result = old
    by_root = {r["root"]: r for r in result["runs"]}
    deadline = time.monotonic() + args.seconds
    for root in selected:
        if root in by_root and by_root[root]["completed_exhaustively"]:
            continue
        if time.monotonic() >= deadline:
            break
        record = explore(root, initial, dist, n, m, plus, neg, args.node_limit, deadline)
        if root in by_root:
            result["attempt_history"].append(by_root[root])
        by_root[root] = record
        result["runs"] = [by_root[g] for g in roots if g in by_root]
        result["completed_roots"] = sum(r["completed_exhaustively"] for r in result["runs"])
        result["all_roots_completed"] = result["completed_roots"] == len(roots)
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({k: record[k] for k in
                          ("root_coordinates", "completed_exhaustively", "nodes",
                           "max_reached_length", "seconds")}), flush=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
