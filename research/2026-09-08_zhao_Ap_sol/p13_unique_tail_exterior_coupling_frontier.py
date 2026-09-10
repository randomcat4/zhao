#!/usr/bin/env python3
"""Finite exterior-position frontier for the two p=13 unique-tail slices.

This program does two separate jobs.

* In its default mode it classifies every possible coefficient pattern in an
  atom decomposition of the projection of V=Y minus U and every compatible vector
  of *actual factor sizes*.  The classification uses the full axial subset-sum
  criterion for the positive-core F3 complement, the automatically induced
  quotient-zero length spectrum, and uniqueness of the positive-core tail.
* It emits one resumable position-level shard and validates a filled shard by
  passing its 34 unified quotient/height labels to the exact labelled-instance
  validator.  That final call reconstructs all short blocks, all zero-core F3
  blocks, Hasse rows, intersections, the actual Z atom, and every long F3
  complement's internal subset sums.

Default-mode survivors and emitted shards are necessary-condition frontiers.
They are not compatible models and never counterexamples to A_13.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from p13_three_tail_internal_spectrum_slice_unique13 import (
    P,
    five_tail_decomposable_height_slice,
    surviving_three_tail_templates,
)
from verify_unique_tail_labelled_position_next import validate_instance


Q = (1, 0, 0)
EXTERIOR_TOTAL = (7, 0, 0)
EXTERIOR_HEIGHT = 10
MAX_PROJECTED_ATOM_LENGTH = 2 * P - 1

EXPECTED_FRONTIERS = {
    31: {
        "count": 118,
        "hash": "e1177f8567aa77c3d1385346bfeceb73582a384727b6ae373156e1f3d7ee4aaf",
        "by_pattern": {
            "1,6": 4,
            "2,5": 5,
            "3,4": 6,
            "1,1,5": 19,
            "1,2,4": 44,
            "1,3,3": 1,
            "2,2,3": 1,
            "1,1,1,4": 37,
            "1,2,2,2": 1,
        },
    },
    29: {
        "count": 83,
        "hash": "f7f5d931537ccc2bad6f08d1d93808805c0a60156c7e1bc6996afefd552bf827",
        "by_pattern": {
            "1,6": 4,
            "2,5": 5,
            "3,4": 6,
            "1,1,5": 14,
            "1,2,4": 32,
            "1,1,1,4": 22,
        },
    },
}


def add(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple((a + b) % P for a, b in zip(left, right))


def vector_sum(values: Iterable[Sequence[int]], dimension: int) -> tuple[int, ...]:
    total = (0,) * dimension
    for value in values:
        total = add(total, tuple(value[:dimension]))
    return total


def projected_atom(values: Sequence[Sequence[int]]) -> bool:
    """Whether the last two quotient coordinates form a positional atom."""
    projection = [(value[1] % P, value[2] % P) for value in values]
    if vector_sum(projection, 2) != (0, 0):
        return False
    reachable = {(0, 0)}
    for index, value in enumerate(projection):
        if index and (0, 0) in reachable:
            # The empty subset is always present; test only newly formed sums.
            pass
        new_sums = {add(total, value) for total in reachable}
        if index < len(projection) - 1 and (0, 0) in new_sums:
            return False
        reachable |= new_sums
    # The loop above catches every zero-sum subset whose last selected position
    # is not the last sequence position.  Check all proper masks directly for
    # the small U-components and by prefix DP for larger exterior factors.
    states = {(0, 0): 1}
    for value in projection:
        updated = dict(states)
        for total, sizes in states.items():
            target = add(total, value)
            updated[target] = updated.get(target, 0) | (sizes << 1)
        states = updated
    zero_sizes = states.get((0, 0), 0)
    allowed = 1 | (1 << len(projection))
    return zero_sizes & ~allowed == 0


def coefficient_patterns() -> tuple[tuple[int, ...], ...]:
    """All projected-atom axis patterns allowed by the long complement."""
    patterns: list[tuple[int, ...]] = []
    # Every factor has coefficient 1..6.  Seven factors is the absolute
    # maximum: eight positive coefficients contain a proper subfamily summing
    # to 7 or more before reduction modulo 13.
    for factor_count in range(2, 8):
        for coefficients in itertools.combinations_with_replacement(
            range(1, 7), factor_count
        ):
            if sum(coefficients) % P != 7:
                continue
            valid = True
            for subset_size in range(1, factor_count):
                for indices in itertools.combinations(range(factor_count), subset_size):
                    residue = sum(coefficients[index] for index in indices) % P
                    if residue not in range(1, 7):
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                patterns.append(coefficients)
    expected = (
        (1, 6), (2, 5), (3, 4),
        (1, 1, 5), (1, 2, 4), (1, 3, 3), (2, 2, 3),
        (1, 1, 1, 4), (1, 1, 2, 3), (1, 2, 2, 2),
        (1, 1, 1, 1, 3), (1, 1, 1, 2, 2),
        (1, 1, 1, 1, 1, 2),
        (1, 1, 1, 1, 1, 1, 1),
    )
    assert tuple(patterns) == expected
    return tuple(patterns)


def subfamily_constraint(
    coefficients: Sequence[int], sizes: Sequence[int]
) -> bool:
    """Automatic middle-spectrum constraint for every proper factor union.

    A proper factor union has quotient sum d*q with d in 1..6.  If d>=4,
    then adding 13-d available X positions makes it quotient-zero.  Lengths
    9..28 are forbidden.  The sole possible shorter case is d=6 and union
    size one, but that would be a second positive-core F3 tail, so it is also
    forbidden.  Consequently its union size must be at least 16+d.
    """
    factor_count = len(coefficients)
    for subset_size in range(1, factor_count):
        for indices in itertools.combinations(range(factor_count), subset_size):
            coefficient = sum(coefficients[index] for index in indices) % P
            assert coefficient in range(1, 7)
            position_count = sum(sizes[index] for index in indices)
            if coefficient >= 4 and position_count < 16 + coefficient:
                return False
    return True


def size_profiles(
    coefficients: tuple[int, ...], exterior_count: int
) -> tuple[tuple[int, ...], ...]:
    """All canonical factor-size vectors for one coefficient pattern."""
    profiles: list[tuple[int, ...]] = []
    factor_count = len(coefficients)

    def extend(prefix: tuple[int, ...], remaining: int) -> None:
        index = len(prefix)
        if index == factor_count:
            if remaining == 0 and subfamily_constraint(coefficients, prefix):
                profiles.append(prefix)
            return
        factors_left = factor_count - index - 1
        lower = 1
        if index and coefficients[index] == coefficients[index - 1]:
            lower = prefix[-1]
        upper = min(MAX_PROJECTED_ATOM_LENGTH, remaining - factors_left)
        for size in range(lower, upper + 1):
            extend(prefix + (size,), remaining - size)

    extend((), exterior_count)
    return tuple(profiles)


def exterior_frontier(exterior_count: int) -> tuple[dict[str, object], ...]:
    frontier: list[dict[str, object]] = []
    for coefficients in coefficient_patterns():
        for sizes in size_profiles(coefficients, exterior_count):
            frontier.append(
                {
                    "coefficients": list(coefficients),
                    "factor_sizes": list(sizes),
                }
            )
    return tuple(frontier)


def digest(records: object) -> str:
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def tail_checkpoints(branch: str) -> tuple[dict[str, object], ...]:
    if branch == "three":
        return tuple(
            {
                "checkpoint_index": index,
                "kind": template.kind,
                "parameters": list(template.parameters),
                "U": [list(label) for label in template.labels],
            }
            for index, template in enumerate(surviving_three_tail_templates())
        )
    assert branch == "five"
    patterns = five_tail_decomposable_height_slice()["survivors_c_hP_hQ"]
    return tuple(
        {
            "checkpoint_index": index,
            "c_hP_hQ": list(pattern),
            "U_partition": {"P": [0, 1], "Q": [2, 3, 4]},
        }
        for index, pattern in enumerate(patterns)
    )


def make_shard(branch: str, checkpoint_index: int, frontier_index: int) -> dict[str, object]:
    exterior_count = 31 if branch == "three" else 29
    checkpoints = tail_checkpoints(branch)
    frontier = exterior_frontier(exterior_count)
    if not 0 <= checkpoint_index < len(checkpoints):
        raise ValueError("checkpoint index outside branch")
    if not 0 <= frontier_index < len(frontier):
        raise ValueError("frontier index outside exterior frontier")
    factor_sizes = frontier[frontier_index]["factor_sizes"]
    factor_ranges = []
    start = 0
    for size in factor_sizes:
        factor_ranges.append(list(range(start, start + size)))
        start += size
    assert start == exterior_count
    tail_size = 3 if branch == "three" else 5
    return {
        "schema": "P13_UNIQUE_TAIL_EXTERIOR_SHARD_V1",
        "status": "NECESSARY_CONDITION_SHARD_NOT_A_MODEL",
        "branch": branch,
        "unique_type": [6, 3] if branch == "three" else [8, 3],
        "x_height": 0,
        "checkpoint": checkpoints[checkpoint_index],
        "exterior_frontier_index": frontier_index,
        "exterior_position_count": exterior_count,
        "exterior_positions": [f"v{index}" for index in range(exterior_count)],
        "exterior_factorization": {
            **frontier[frontier_index],
            "factor_position_indices": factor_ranges,
        },
        "zero_core_f3_network": {
            "block_lengths": [6, 7, 8],
            "block_sign_by_length": {"6": -1, "7": 1, "8": -1},
            "signed_total_mod_13": 6,
            "signed_containing_each_tail_position_mod_13": 4,
            "signed_avoiding_each_tail_position_mod_13": 2,
            "signed_containing_each_exterior_position_mod_13": 11,
            "signed_avoiding_each_exterior_position_mod_13": 8,
            "ordinary_block_lower_bound": 10 if tail_size == 3 else 9,
            "proper_axial_trace_steps_by_trace_size": {
                str(trace_size): list(range(1, min(3, 4 - trace_size) + 1))
                for trace_size in range(1, tail_size)
            },
            "each_block": [
                "has quotient sum 0 and height sum 3",
                "meets U with nonzero quotient trace",
                "has an all-subsets axial-atom complement with allowed coefficients 1,2,3",
            ],
            "each_distinct_pair": [
                "intersects",
                "has nonzero quotient sum on its intersection",
            ],
        },
        "unassigned": {
            "exterior_labels": "one (q-axis,projection-1,projection-2,height) label per exterior position",
            "T": "one zero-core F3 position block; the full validator regenerates all such blocks",
            **(
                {"U_labels": "five labels satisfying the checkpoint component constraints"}
                if branch == "five" else {}
            ),
        },
        "automatic_constraints_on_fill": [
            "unified labels and total sums on all 34 Y positions",
            "declared projection factors are positional C13^2 atoms with the stated q-axis sums",
            "all induced quotient-zero short blocks of total length 2..8 and their actual families",
            "no quotient-zero block of total length 9..28",
            "unique positive-core F3 tail and all zero-core F3 blocks",
            "all point, pair, and triple Hasse rows and the F3 intersection network",
            "actual Z is an atom and every F3 long quotient-complement passes all internal subset sums",
        ],
        "outside_scope": ["TOP", "CONST", "the positions of R outside Z"],
    }


def validate_five_u(labels: Sequence[Sequence[int]], checkpoint: dict[str, object]) -> None:
    if len(labels) != 5 or any(len(label) != 4 for label in labels):
        raise ValueError("five-tail branch needs five four-coordinate U labels")
    normalized = [tuple(entry % P for entry in label) for label in labels]
    if vector_sum([label[:3] for label in normalized], 3) != (10, 0, 0):
        raise ValueError("five-tail U quotient total is not -3q")
    if sum(label[3] for label in normalized) % P != 3:
        raise ValueError("five-tail U height total is not 3")
    coefficient, p_height, q_height = checkpoint["c_hP_hQ"]
    left, right = normalized[:2], normalized[2:]
    if vector_sum([label[:3] for label in left], 3) != ((-coefficient) % P, 0, 0):
        raise ValueError("P component has wrong unified quotient sum")
    if vector_sum([label[:3] for label in right], 3) != (
        (-(3 - coefficient)) % P, 0, 0
    ):
        raise ValueError("Q component has wrong unified quotient sum")
    if sum(label[3] for label in left) % P != p_height:
        raise ValueError("P component has wrong height sum")
    if sum(label[3] for label in right) % P != q_height:
        raise ValueError("Q component has wrong height sum")
    if not projected_atom(left) or not projected_atom(right):
        raise ValueError("P and Q must be positional projected atoms")
    if any(label[1:3] == (0, 0) for label in normalized):
        raise ValueError("five-tail U has a forbidden axial singleton")


def validate_filled(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    shard = data["shard"]
    if shard.get("schema") != "P13_UNIQUE_TAIL_EXTERIOR_SHARD_V1":
        raise ValueError("unknown shard schema")
    branch = shard["branch"]
    expected = make_shard(
        branch,
        int(shard["checkpoint"]["checkpoint_index"]),
        int(shard["exterior_frontier_index"]),
    )
    if shard != expected:
        raise ValueError("filled record altered the canonical shard")

    exterior = [tuple(int(entry) % P for entry in label) for label in data["exterior_labels"]]
    if len(exterior) != expected["exterior_position_count"]:
        raise ValueError("wrong number of exterior labels")
    if any(len(label) != 4 for label in exterior):
        raise ValueError("each exterior label must have four coordinates")
    if vector_sum([label[:3] for label in exterior], 3) != EXTERIOR_TOTAL:
        raise ValueError("exterior quotient total is not 7q")
    if sum(label[3] for label in exterior) % P != EXTERIOR_HEIGHT:
        raise ValueError("exterior height total is not -3")

    factorization = expected["exterior_factorization"]
    for coefficient, indices in zip(
        factorization["coefficients"], factorization["factor_position_indices"]
    ):
        factor = [exterior[index] for index in indices]
        if len(factor) > MAX_PROJECTED_ATOM_LENGTH:
            raise ValueError("projected atom factor exceeds Davenport bound")
        if not projected_atom(factor):
            raise ValueError("declared exterior factor is not a projected atom")
        if vector_sum([label[:3] for label in factor], 3) != (
            coefficient % P, 0, 0
        ):
            raise ValueError("declared exterior factor has wrong unified quotient sum")

    if branch == "three":
        u_labels = [tuple(label) for label in expected["checkpoint"]["U"]]
    else:
        u_labels = [tuple(int(entry) % P for entry in label) for label in data["U_labels"]]
        validate_five_u(u_labels, expected["checkpoint"])

    instance = {
        "p": P,
        "unique_type": expected["unique_type"],
        "x_height": 0,
        "Y": [list(label) for label in u_labels + exterior],
        "U": list(range(len(u_labels))),
        "T": [int(index) for index in data["T"]],
    }
    temporary = path.with_name(path.name + ".exact-instance.tmp.json")
    try:
        temporary.write_text(json.dumps(instance), encoding="utf-8")
        validate_instance(temporary)
    finally:
        temporary.unlink(missing_ok=True)


def summary() -> dict[str, object]:
    patterns = coefficient_patterns()
    by_exterior_count = {}
    for exterior_count in (31, 29):
        frontier = exterior_frontier(exterior_count)
        counts: dict[str, int] = {}
        for record in frontier:
            key = ",".join(map(str, record["coefficients"]))
            counts[key] = counts.get(key, 0) + 1
        frontier_hash = digest(frontier)
        expected = EXPECTED_FRONTIERS[exterior_count]
        assert len(frontier) == expected["count"]
        assert frontier_hash == expected["hash"]
        assert counts == expected["by_pattern"]
        by_exterior_count[str(exterior_count)] = {
            "size_profile_count": len(frontier),
            "size_profile_hash": frontier_hash,
            "counts_by_coefficient_pattern": counts,
        }
    result = {
        "p": P,
        "positive_complement": "q^6 V is a quotient atom and sigma_bar(V)=7q",
        "coefficient_pattern_count": len(patterns),
        "coefficient_patterns": [list(pattern) for pattern in patterns],
        "coefficient_pattern_hash": digest(patterns),
        "frontiers": by_exterior_count,
        "three_tail_checkpoint_count": len(tail_checkpoints("three")),
        "five_tail_checkpoint_count": len(tail_checkpoints("five")),
        "three_tail_shard_count": len(tail_checkpoints("three")) * 118,
        "five_tail_shard_count": len(tail_checkpoints("five")) * 83,
        "status": "PROVED_FINITE_EXTERIOR_POSITION_FRONTIER_GLOBAL_INCOMPLETE",
        "warning": "Every shard is necessary-only; a survivor is not a compatible model.",
    }
    inverse_20 = pow(20, -1, P)
    assert inverse_20 == 2
    assert (-pow(5 * 3, -1, P)) % P == 6
    assert (-(3 + 4) * pow(20 * 3, -1, P)) % P == 4
    assert (-inverse_20) % P == 11
    assert ((3 - 4) * pow(20 * 3, -1, P)) % P == 8
    assert result["coefficient_pattern_count"] == 14
    assert result["three_tail_checkpoint_count"] == 511
    assert result["five_tail_checkpoint_count"] == 9
    assert result["three_tail_shard_count"] == 60_298
    assert result["five_tail_shard_count"] == 747
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-shard", choices=("three", "five"))
    parser.add_argument("--checkpoint-index", type=int, default=0)
    parser.add_argument("--frontier-index", type=int, default=0)
    parser.add_argument("--validate-filled", type=Path)
    args = parser.parse_args()
    if args.validate_filled:
        validate_filled(args.validate_filled)
        return
    if args.emit_shard:
        print(
            json.dumps(
                make_shard(args.emit_shard, args.checkpoint_index, args.frontier_index),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return
    print(json.dumps(summary(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
