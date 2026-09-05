"""Exact exhaustive extension of the five possible five-triple cores in F_5^4.

Run with a local Python 3 interpreter. No external packages or randomness.
All group elements are base-five encoded, low coordinate first.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time


ORDER = 625
INF = 99
BASIS = (1, 5, 25, 125)
CORE_TYPES = ((0, 1, 2, 3), (1, 1, 2, 3), (1, 2, 2, 3),
              (1, 2, 3, 3), (1, 2, 3, 4))


def encode(v):
    return sum(x * 5 ** i for i, x in enumerate(v))


def decode(x):
    return tuple((x // (5 ** i)) % 5 for i in range(4))


def make_tables():
    ds = tuple(decode(x) for x in range(ORDER))
    plus = [[encode(tuple((a[i] + b[i]) % 5 for i in range(4)))
             for b in ds] for a in ds]
    neg = [encode(tuple((-a[i]) % 5 for i in range(4))) for a in ds]
    return plus, neg


def extend_distances(dist, g, plus):
    """Return exact minimum subsequence lengths after adjoining one position g."""
    out = dist.copy()
    translate = plus[g]
    for h, length in enumerate(dist):
        if length < INF and length + 1 < out[translate[h]]:
            out[translate[h]] = length + 1
    return out


def check_core(x, plus, neg):
    seq = tuple(g for g in (*BASIS, x) for _ in range(3))
    dist = [INF] * ORDER
    dist[0] = 0
    for g in seq:
        # Stronger than endpoint safety: these 15 positions are zero-sum-free.
        assert dist[neg[g]] == INF, ("core has a nonempty zero sum", decode(x))
        dist = extend_distances(dist, g, plus)
    return seq, dist


def search(core_type, n, m, plus, neg, node_limit):
    started = time.monotonic()
    x = encode(core_type)
    core, initial_dist = check_core(x, plus, neg)
    multiplicity = [0] * ORDER
    for g in core:
        multiplicity[g] += 1
    # A bad endpoint has height <=3 by the subgroup lemma. Only these capacities
    # are imposed, so no support-size restriction or guessed ordering is used.
    initial = [g for g in range(1, ORDER)
               if multiplicity[g] < 3 and initial_dist[neg[g]] + 1 > m]
    records = []
    nodes_by_length = [0] * (n + 1)
    leaves_by_length = [0] * (n + 1)
    terminal = []
    longest = tuple()
    nodes = 0
    complete = True

    def dfs(dist, candidates, added):
        nonlocal longest, nodes, complete
        nodes += 1
        if node_limit and nodes > node_limit:
            complete = False
            return
        length = len(core) + len(added)
        nodes_by_length[length] += 1
        if len(added) > len(longest):
            longest = tuple(added)
        if length == n:
            terminal.append(list(added))
            return
        any_child = False
        for i, g in enumerate(candidates):
            if multiplicity[g] >= 3:
                continue
            assert dist[neg[g]] + 1 > m
            new_dist = extend_distances(dist, g, plus)
            multiplicity[g] += 1
            next_candidates = [h for h in candidates[i:]
                               if multiplicity[h] < 3 and new_dist[neg[h]] + 1 > m]
            any_child = True
            dfs(new_dist, next_candidates, added + [g])
            multiplicity[g] -= 1
            if not complete:
                return
        if not any_child:
            leaves_by_length[length] += 1

    dfs(initial_dist, initial, [])
    return {
        "core_type": list(core_type), "n": n, "m": m,
        "core_sequence_encoded": list(core),
        "core_is_zero_sum_free": True,
        "initial_safe_candidates": initial,
        "initial_safe_candidates_coordinates": [list(decode(g)) for g in initial],
        "nodes_by_length": {str(i): v for i, v in enumerate(nodes_by_length) if v},
        "leaves_by_length": {str(i): v for i, v in enumerate(leaves_by_length) if v},
        "max_reached_length": len(core) + len(longest),
        "one_longest_extension_encoded": list(longest),
        "terminal_extensions": terminal,
        "completed_exhaustively": complete,
        "nodes": nodes,
        "seconds": round(time.monotonic() - started, 6),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--node-limit", type=int, default=1000000)
    args = parser.parse_args()
    plus, neg = make_tables()
    runs = []
    for n, m in ((21, 13), (20, 14)):
        for core_type in CORE_TYPES:
            result = search(core_type, n, m, plus, neg, args.node_limit)
            runs.append(result)
            print(json.dumps({k: result[k] for k in
                              ("core_type", "n", "m", "nodes_by_length",
                               "max_reached_length", "completed_exhaustively", "seconds")}),
                  flush=True)
    output = {
        "scope": "F_5^4, five distinct elements of multiplicity three, height at most three",
        "arithmetic": "exact integers modulo five",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "all_runs_completed": all(r["completed_exhaustively"] for r in runs),
        "counterexample_count": sum(len(r["terminal_extensions"]) for r in runs),
        "runs": runs,
    }
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
