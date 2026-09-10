#!/usr/bin/env python3
"""Finite certificate for proofs/unique_tail_common_R_next.md.

This verifies the maximal disjoint projected-zero-atom decomposition of the
common external sequence R at the coefficient-pattern level.  It does not
enumerate or claim an actual labelled R.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json


GLOBAL_FACTOR_PATTERNS = (
    (1, 3),
    (2, 2),
    (1, 1, 2),
    (1, 1, 1, 1),
)

PACKING_TYPES = (
    (),
    (1,),
    (2,),
    (3,),
    (1, 1),
    (1, 2),
    (1, 1, 1),
)

EXPECTED_TYPE_SHA256 = (
    "5f5f08a41a90fba288ba84b397dafa73f90028fb4982d421c297ab6f4af95027"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "24ffe43612df8927e3d192cf0dcde34629ed5de0dfa4ba1eaacc8080b8963169"
)


def multiset_subtract(
    whole: tuple[int, ...], part: tuple[int, ...]
) -> tuple[int, ...] | None:
    remainder = Counter(whole)
    for value in part:
        if not remainder[value]:
            return None
        remainder[value] -= 1
    return tuple(
        value
        for value in sorted(remainder)
        for _ in range(remainder[value])
    )


def residual_patterns(part: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    observed = {
        remainder
        for whole in GLOBAL_FACTOR_PATTERNS
        if (remainder := multiset_subtract(whole, part)) is not None
    }
    return tuple(sorted(observed))


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def zero_sum_free_witness(p: int) -> dict[str, object]:
    # e1^(p-1) e2^(p-43): any projected-zero subset would use a multiple
    # of p copies in both independent coordinates, hence must be empty.
    first = p - 1
    second = p - 43
    assert 0 < first < p
    assert 0 < second < p
    return {
        "p": p,
        "multiplicities": [first, second],
        "length": first + second,
        "target_lower_bound": 2 * p - 44,
        "sum": [(first % p), (second % p)],
        "projected_zero_sum_free": True,
    }


def main() -> None:
    expected_residuals = {
        (): ((1, 1, 1, 1), (1, 1, 2), (1, 3), (2, 2)),
        (1,): ((1, 1, 1), (1, 2), (3,)),
        (2,): ((1, 1), (2,)),
        (3,): ((1,),),
        (1, 1): ((1, 1), (2,)),
        (1, 2): ((1,),),
        (1, 1, 1): ((1,),),
    }
    records = []
    expanded_rows = []
    for packing in PACKING_TYPES:
        residuals = residual_patterns(packing)
        assert residuals == expected_residuals[packing]
        total_coefficient = sum(packing)
        assert total_coefficient <= 3
        record = {
            "packing_coefficients": list(packing),
            "packing_count": len(packing),
            "packing_total_coefficient": total_coefficient,
            "common_remainder_total_coefficient": 4 - total_coefficient,
            "residual_factor_patterns": [list(row) for row in residuals],
            "common_remainder_forced_atom": residuals == ((4 - total_coefficient,),),
        }
        records.append(record)
        for residual in residuals:
            expanded_rows.append(
                {
                    "packing_coefficients": list(packing),
                    "residual_factor_pattern": list(residual),
                }
            )

    assert len(records) == 7
    assert len(expanded_rows) == 14
    assert [
        tuple(row["packing_coefficients"])
        for row in records
        if row["common_remainder_forced_atom"]
    ] == [(3,), (1, 2), (1, 1, 1)]

    sizes = {}
    witnesses = {}
    for p in (233, 1399):
        sizes[p] = {
            "R_min": 2 * p - 44,
            "D_Cp2": 2 * p - 1,
            "zero_sum_free_max": 2 * p - 2,
            "gap_R_min_to_D": 43,
        }
        witness = zero_sum_free_witness(p)
        assert witness["length"] == sizes[p]["R_min"]
        witnesses[p] = witness

    type_hash = canonical_hash(records)
    certificate = {
        "status": "PROVED_DECOMPOSITION/FOURTH_BLOCK_NOT_FORCED/GLOBAL_INCOMPLETE",
        "records": records,
        "expanded_rows": expanded_rows,
        "sizes": sizes,
        "zero_sum_free_length_witnesses": witnesses,
    }
    certificate_hash = canonical_hash(certificate)
    if EXPECTED_TYPE_SHA256:
        assert type_hash == EXPECTED_TYPE_SHA256
    if EXPECTED_CERTIFICATE_SHA256:
        assert certificate_hash == EXPECTED_CERTIFICATE_SHA256

    report = {
        "packing_type_count": len(records),
        "expanded_survivor_row_count": len(expanded_rows),
        "forced_common_remainder_atom_type_count": sum(
            row["common_remainder_forced_atom"] for row in records
        ),
        "type_sha256": type_hash,
        "certificate_sha256": certificate_hash,
        "status": certificate["status"],
        "types": records,
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
