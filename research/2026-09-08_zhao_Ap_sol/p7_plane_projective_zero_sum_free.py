#!/usr/bin/env python3
"""Exact rank-two weighted projective zero-sum-free frontier for p=7.

The support contains at most one nonzero value from each one-dimensional
subspace of C_7^2, and every chosen value has multiplicity at most four.
After normalizing two independent chosen values to e1,e2, the remaining six
projective lines are searched by memoized exact subset-sum states.
"""

from __future__ import annotations

from functools import lru_cache
import hashlib
import json


P = 7
ZERO = 0
E1 = 7
E2 = 1
ALL_MASK = (1 << (P * P)) - 1
PROJECTIVE_REPRESENTATIVES = tuple((1, slope) for slope in range(1, P))
EXPECTED_MAXIMUM = 11
EXPECTED_WITNESS_SHA256 = "699d7242e87d63d8246bd36225b7c65fb9e0bb2148fed3b75d7df00ce222157e"


def vector_id(value: tuple[int, int]) -> int:
    return (value[0] % P) * P + value[1] % P


def add_id(left: int, right: int) -> int:
    lx, ly = divmod(left, P)
    rx, ry = divmod(right, P)
    return vector_id((lx + rx, ly + ry))


ADD = tuple(
    tuple(add_id(left, right) for right in range(P * P))
    for left in range(P * P)
)


def scale_id(coefficient: int, value: int) -> int:
    x, y = divmod(value, P)
    return vector_id((coefficient * x, coefficient * y))


def translate(mask: int, offset: int) -> int:
    answer = 0
    while mask:
        least = mask & -mask
        current = least.bit_length() - 1
        answer |= 1 << ADD[current][offset]
        mask ^= least
    return answer


def extend(mask: int, value: int, multiplicity: int) -> int | None:
    """Adjoin value^multiplicity or reject a nonempty zero-sum subset."""
    answer = mask
    for count in range(1, multiplicity + 1):
        shifted = translate(mask, scale_id(count, value))
        if shifted & 1:
            return None
        answer |= shifted
    return answer


LINE_OPTIONS = tuple(
    tuple(
        (vector_id((scalar * x, scalar * y)), multiplicity)
        for scalar in range(1, P)
        for multiplicity in range(1, 5)
    )
    for x, y in PROJECTIVE_REPRESENTATIVES
)


def solve_for_basis_multiplicities(m1: int, m2: int):
    mask = 1
    mask = extend(mask, E1, m1)
    assert mask is not None
    mask = extend(mask, E2, m2)
    assert mask is not None

    @lru_cache(maxsize=None)
    def visit(line_index: int, reachable: int):
        if line_index == len(LINE_OPTIONS):
            return 0, ()
        best_length, best_suffix = visit(line_index + 1, reachable)
        for value, multiplicity in LINE_OPTIONS[line_index]:
            next_reachable = extend(reachable, value, multiplicity)
            if next_reachable is None:
                continue
            tail_length, tail_suffix = visit(line_index + 1, next_reachable)
            candidate_length = multiplicity + tail_length
            candidate_suffix = ((value, multiplicity),) + tail_suffix
            if (candidate_length, candidate_suffix) > (best_length, best_suffix):
                best_length, best_suffix = candidate_length, candidate_suffix
        return best_length, best_suffix

    extra_length, suffix = visit(0, mask)
    witness = ((E1, m1), (E2, m2)) + suffix
    return m1 + m2 + extra_length, witness, visit.cache_info()


def expanded(witness):
    return tuple(value for value, multiplicity in witness for _ in range(multiplicity))


def direct_zero_sum_free(witness) -> bool:
    mask = 1
    for value, multiplicity in witness:
        mask = extend(mask, value, multiplicity)
        if mask is None:
            return False
    return True


def main() -> None:
    records = []
    maximum = -1
    witnesses = []
    for m1 in range(1, 5):
        for m2 in range(1, 5):
            length, witness, cache = solve_for_basis_multiplicities(m1, m2)
            assert direct_zero_sum_free(witness)
            record = {
                "basis_multiplicities": [m1, m2],
                "maximum_length": length,
                "witness": [list(item) for item in witness],
                "cache_misses": cache.misses,
            }
            records.append(record)
            if length > maximum:
                maximum = length
                witnesses = [record]
            elif length == maximum:
                witnesses.append(record)
    payload = json.dumps(witnesses, sort_keys=True, separators=(",", ":")).encode("ascii")
    digest = hashlib.sha256(payload).hexdigest()
    if EXPECTED_MAXIMUM:
        assert maximum == EXPECTED_MAXIMUM
    if EXPECTED_WITNESS_SHA256:
        assert digest == EXPECTED_WITNESS_SHA256
    print(json.dumps({
        "status": "EXACT_RANK_TWO_FINITE_FRONTIER",
        "maximum_length": maximum,
        "maximum_basis_cases": len(witnesses),
        "witness_sha256": digest,
        "records": records,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
