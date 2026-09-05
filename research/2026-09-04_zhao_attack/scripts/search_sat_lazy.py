"""Exact lazy SAT encoding; only UNSAT with all valid cuts or an audited model decides.

A Boolean x[g,r] says multiplicity(g) >= r. Every discovered short-zero
multiset a gives the globally valid clause OR_g NOT x[g,a[g]].
The candidate models cover every normalized full-rank sequence in the chosen
domain and cap, not just a fixed small-support family. A timeout is INCOMPLETE.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "local_deps" / "search_z3"))
import z3

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=20)
parser.add_argument("--m", type=int, default=14)
parser.add_argument("--cap", type=int, default=3)
parser.add_argument("--mode", choices=("full", "affine"), default="affine")
parser.add_argument("--seed", type=int, default=17)
parser.add_argument("--seconds", type=float, default=120)
parser.add_argument("--max-iterations", type=int, default=5000)
args = parser.parse_args()


def coords(code):
    return [(code // (5**j)) % 5 for j in range(4)]


def short_zeros(sequence):
    sums = np.zeros((1, 4), dtype=np.uint8)
    lengths = np.zeros(1, dtype=np.uint8)
    positions = {}
    for i, code in enumerate(sequence):
        positions[code] = positions.get(code, 0) | (1 << i)
        sums = np.concatenate((sums, (sums + np.asarray(coords(code), dtype=np.uint8)) % 5))
        lengths = np.concatenate((lengths, lengths + 1))
    masks = np.flatnonzero(np.all(sums == 0, axis=1) & (lengths > 0) & (lengths <= args.m))
    cuts = set()
    for mask in masks:
        mask = int(mask)
        cut = tuple((g, (mask & pos).bit_count()) for g, pos in positions.items() if mask & pos)
        cuts.add(cut)
    return cuts, len(masks)


domain = [g for g in range(1, 625) if args.mode == "full" or sum(coords(g)) % 5 == 1]
z3.set_param(proof=True)
solver = z3.Solver()
solver.set(random_seed=args.seed)
variables = {(g, r): z3.Bool(f"x_{g}_{r}") for g in domain for r in range(1, args.cap + 1)}
for g in domain:
    for r in range(2, args.cap + 1):
        solver.add(z3.Implies(variables[g, r], variables[g, r - 1]))
for g in (1, 5, 25, 125):
    solver.add(variables[g, 1])
solver.add(z3.PbEq([(x, 1) for x in variables.values()], args.n))

prefix = ROOT / "evidence" / f"search_sat_{args.mode}{args.n}_{args.seed}"
prefix.parent.mkdir(exist_ok=True, parents=True)
seen = set()
start = time.monotonic()
status = "INCOMPLETE"
candidate = None
reason = "iteration_budget"
iteration = 0
with prefix.with_suffix(".log").open("w", encoding="utf-8") as logfile, prefix.with_suffix(".cuts.jsonl").open("w", encoding="utf-8") as cutfile:
    def log(text):
        print(text, flush=True)
        logfile.write(text + "\n")
        logfile.flush()

    log(f"CONFIG {vars(args)} z3={z3.get_version_string()} variables={len(variables)}")
    for iteration in range(1, args.max_iterations + 1):
        remain = args.seconds - (time.monotonic() - start)
        if remain <= 0:
            reason = "wallclock_budget"
            break
        solver.set(timeout=max(1, int(min(remain, 20) * 1000)))
        answer = solver.check()
        if answer == z3.unsat:
            status = "UNSAT_RESTRICTED_FAMILY"
            reason = "solver_unsat"
            prefix.with_suffix(".proof.sexpr").write_text(solver.proof().sexpr(), encoding="utf-8")
            break
        if answer == z3.unknown:
            reason = solver.reason_unknown()
            break
        model = solver.model()
        sequence = [g for (g, r), x in variables.items() if z3.is_true(model.eval(x))]
        assert len(sequence) == args.n
        cuts, indexed = short_zeros(sequence)
        newcuts = sorted(cuts - seen)
        if not cuts:
            status = "CANDIDATE_COUNTEREXAMPLE"
            reason = "exact_subset_enumeration_passed"
            candidate = sequence
            break
        assert newcuts, "Model violates a previously added clause"
        for cut in newcuts:
            solver.add(z3.Or([z3.Not(variables[g, r]) for g, r in cut]))
            cutfile.write(json.dumps(cut) + "\n")
        cutfile.flush()
        seen.update(newcuts)
        if iteration <= 10 or iteration % 25 == 0:
            log(f"ITERATION i={iteration} cuts={len(seen)} new={len(newcuts)} support={len(set(sequence))} indexed_short_zeros={indexed} elapsed={time.monotonic()-start:.3f}")
    result = dict(status=status, reason=reason, config=vars(args), z3=z3.get_version_string(), iterations=iteration, cuts=len(seen), elapsed_seconds=time.monotonic()-start, candidate_sequence=candidate)
    log("FINAL " + json.dumps(result))
    prefix.with_suffix(".result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
