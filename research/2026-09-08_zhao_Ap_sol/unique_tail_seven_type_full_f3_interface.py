#!/usr/bin/env python3
"""Exact marked-position interface for the two large-prime unique-tail types.

The default run verifies the seven common-R packing types, their fourteen
endpoint remainder rows, the forced-Q local gate, and two position-marked
spectra on exhaustive small examples.  With ``--instance`` it first validates
the supplied common-R decomposition and then delegates the full labelled
instance to ``verify_unique_tail_labelled_position_next.py``.  That mode is an
exact finite verifier if it terminates; the default run does not enumerate an
actual p=233 or p=1399 exterior sequence and makes no SAT/UNSAT claim.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Iterable


PACKING_TYPES = ((), (1,), (2,), (3,), (1, 1), (1, 2), (1, 1, 1))
GLOBAL_FACTOR_PATTERNS = ((1, 3), (2, 2), (1, 1, 2), (1, 1, 1, 1))
FORCED_Q_TYPES = frozenset(((3,), (1, 2), (1, 1, 1)))
LARGE_TYPES = {(233, 7, 4), (1399, 8, 5)}

EXPECTED_TYPE_SHA256 = (
    "ab485b1affe4916404af0fe0d659f709a6f85eb98a7beccf14bc6091f672301a"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "9dfe70ad3c9693d5048b3deb4ec28d12c990e98bf62aff6612494ed65d11ccd5"
)


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def add(left: tuple[int, ...], right: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + b) % p for a, b in zip(left, right))


def vector_sum(
    values: Iterable[tuple[int, ...]], p: int, dimension: int
) -> tuple[int, ...]:
    total = (0,) * dimension
    for value in values:
        total = add(total, value, p)
    return total


def mask_sum(
    values: tuple[tuple[int, ...], ...], mask: int, p: int
) -> tuple[int, ...]:
    return vector_sum(
        (value for index, value in enumerate(values) if mask >> index & 1),
        p,
        len(values[0]),
    )


def multiset_subtract(
    whole: tuple[int, ...], part: tuple[int, ...]
) -> tuple[int, ...] | None:
    remainder = Counter(whole)
    for value in part:
        if remainder[value] == 0:
            return None
        remainder[value] -= 1
    return tuple(
        value for value in sorted(remainder) for _ in range(remainder[value])
    )


def residual_patterns(packing: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(
            remainder
            for whole in GLOBAL_FACTOR_PATTERNS
            if (remainder := multiset_subtract(whole, packing)) is not None
        )
    )


def packing_records() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    for packing in PACKING_TYPES:
        residuals = residual_patterns(packing)
        forced = packing in FORCED_Q_TYPES
        records.append(
            {
                "packing": list(packing),
                "total_axis_coefficient": sum(packing),
                "q_axis_coefficient": 4 - sum(packing),
                "endpoint_remainders": [list(row) for row in residuals],
                "q_forced_projected_atom": forced,
                "forced_local_zero_gate": (
                    "no_nonempty_projected_zero_E_subset_L_minus_H_unless_"
                    "K_empty_and_E_equals_L_minus_H"
                    if forced
                    else "not_forced_by_coefficient_pattern"
                ),
            }
        )
        for residual in residuals:
            rows.append(
                {
                    "packing": list(packing),
                    "endpoint_remainder": list(residual),
                }
            )
    return records, rows


def disjoint_marked_records(
    values: tuple[tuple[int, ...], ...], p: int
) -> Counter[tuple[object, ...]]:
    """Three states per position: unused, in block F, in complement subset G."""
    result: Counter[tuple[object, ...]] = Counter()
    for states in product(range(3), repeat=len(values)):
        f_mask = sum(1 << i for i, state in enumerate(states) if state == 1)
        g_mask = sum(1 << i for i, state in enumerate(states) if state == 2)
        result[
            (
                f_mask,
                g_mask,
                f_mask.bit_count(),
                g_mask.bit_count(),
                mask_sum(values, f_mask, p),
                mask_sum(values, g_mask, p),
            )
        ] += 1
    return result


def direct_disjoint_records(
    values: tuple[tuple[int, ...], ...], p: int
) -> Counter[tuple[object, ...]]:
    result: Counter[tuple[object, ...]] = Counter()
    full = (1 << len(values)) - 1
    for f_mask in range(full + 1):
        available = full ^ f_mask
        g_mask = available
        while True:
            result[
                (
                    f_mask,
                    g_mask,
                    f_mask.bit_count(),
                    g_mask.bit_count(),
                    mask_sum(values, f_mask, p),
                    mask_sum(values, g_mask, p),
                )
            ] += 1
            if g_mask == 0:
                break
            g_mask = (g_mask - 1) & available
    return result


def venn_marked_records(
    values: tuple[tuple[int, ...], ...], p: int
) -> Counter[tuple[object, ...]]:
    """Four Venn states: neither, first only, second only, both."""
    result: Counter[tuple[object, ...]] = Counter()
    for states in product(range(4), repeat=len(values)):
        first = sum(1 << i for i, state in enumerate(states) if state in (1, 3))
        second = sum(1 << i for i, state in enumerate(states) if state in (2, 3))
        common = first & second
        result[
            (
                first,
                second,
                first.bit_count(),
                second.bit_count(),
                common.bit_count(),
                mask_sum(values, first, p),
                mask_sum(values, second, p),
                mask_sum(values, common, p),
            )
        ] += 1
    return result


def direct_venn_records(
    values: tuple[tuple[int, ...], ...], p: int
) -> Counter[tuple[object, ...]]:
    result: Counter[tuple[object, ...]] = Counter()
    full = 1 << len(values)
    for first in range(full):
        for second in range(full):
            common = first & second
            result[
                (
                    first,
                    second,
                    first.bit_count(),
                    second.bit_count(),
                    common.bit_count(),
                    mask_sum(values, first, p),
                    mask_sum(values, second, p),
                    mask_sum(values, common, p),
                )
            ] += 1
    return result


def is_projected_zero_sum_free(
    values: tuple[tuple[int, int], ...], p: int
) -> bool:
    zero = (0, 0)
    reachable = {zero}
    for value in values:
        translated = {add(total, value, p) for total in reachable}
        if zero in translated:
            return False
        reachable |= translated
    return True


def is_projected_atom(values: tuple[tuple[int, int], ...], p: int) -> bool:
    if not values or vector_sum(values, p, 2) != (0, 0):
        return False
    if len(values) == 1:
        return True
    return is_projected_zero_sum_free(values[:-1], p)


def audit_forced_local_gate() -> dict[str, int]:
    """Exhaust the atom gate in C_3^2 for all ordered atoms of length <= 5."""
    p = 3
    alphabet = tuple(product(range(p), repeat=2))
    atom_count = 0
    partition_count = 0
    local_zero_subset_count = 0
    exceptional_count = 0
    for length in range(1, 6):
        for values in product(alphabet, repeat=length):
            if not is_projected_atom(values, p):
                continue
            atom_count += 1
            full = (1 << length) - 1
            for k_mask in range(full + 1):
                local_mask = full ^ k_mask
                k_values = tuple(
                    values[i] for i in range(length) if k_mask >> i & 1
                )
                if not is_projected_zero_sum_free(k_values, p):
                    continue
                partition_count += 1
                submask = local_mask
                while submask:
                    if mask_sum(values, submask, p) == (0, 0):
                        local_zero_subset_count += 1
                        assert k_mask == 0 and submask == local_mask
                        exceptional_count += 1
                    submask = (submask - 1) & local_mask
    assert local_zero_subset_count == exceptional_count
    return {
        "atom_count": atom_count,
        "admissible_K_local_partitions": partition_count,
        "local_projected_zero_subsets": local_zero_subset_count,
        "whole_Q_exceptions": exceptional_count,
    }


def audit_marked_spectra() -> dict[str, int]:
    cases = 0
    disjoint_records = 0
    venn_records = 0
    for seed in range(12):
        p = 5 if seed < 6 else 7
        length = 4 + seed % 3
        values = tuple(
            (
                (seed + 2 * index + 1) % p,
                (seed * (index + 1) + index * index + 3) % p,
            )
            for index in range(length)
        )
        marked_disjoint = disjoint_marked_records(values, p)
        direct_disjoint = direct_disjoint_records(values, p)
        assert marked_disjoint == direct_disjoint
        marked_venn = venn_marked_records(values, p)
        direct_venn = direct_venn_records(values, p)
        assert marked_venn == direct_venn
        assert sum(marked_disjoint.values()) == 3**length
        assert sum(marked_venn.values()) == 4**length
        disjoint_records += len(marked_disjoint)
        venn_records += len(marked_venn)
        cases += 1
    return {
        "case_count": cases,
        "disjoint_marked_record_count": disjoint_records,
        "venn_marked_record_count": venn_records,
    }


def load_labelled_verifier():
    path = Path(__file__).with_name("verify_unique_tail_labelled_position_next.py")
    spec = importlib.util.spec_from_file_location("unique_tail_labelled", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load labelled verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def projected_values(
    y_values: list[tuple[int, int, int, int]], indices: Iterable[int]
) -> tuple[tuple[int, int], ...]:
    return tuple((y_values[i][1], y_values[i][2]) for i in indices)


def validate_full_instance(path: Path) -> None:
    """Validate a supplied split/decomposition, then run the exact labelled CSP."""
    data = json.loads(path.read_text(encoding="utf-8"))
    p = int(data["p"])
    ell, b = (int(value) for value in data["unique_type"])
    if (p, ell, b) not in LARGE_TYPES:
        raise ValueError("instance is not one of the p=233,1399 three-tail types")
    y_values = [tuple(int(entry) % p for entry in row) for row in data["Y"]]
    if len(y_values) != 2 * p + 8 or any(len(row) != 4 for row in y_values):
        raise ValueError("Y must contain 2p+8 four-coordinate position labels")
    universe = set(range(len(y_values)))
    u_set = set(int(i) for i in data["U"])
    endpoints = [frozenset(int(i) for i in row) for row in data["endpoints"]]
    if not 4 <= len(set(endpoints)) <= 8:
        raise ValueError("the four-edge endpoint family must have 4..8 blocks")
    endpoints = list(dict.fromkeys(endpoints))
    l_set = u_set | set().union(*(set(row) for row in endpoints))
    if l_set != set(int(i) for i in data["L"]):
        raise ValueError("L is not U union all selected endpoint blocks")
    r_set = universe - l_set
    if r_set != set(int(i) for i in data["R"]):
        raise ValueError("R is not Y minus L")

    quotient = lambda indices: vector_sum(
        (y_values[i][:3] for i in indices), p, 3
    )
    height = lambda indices: sum(y_values[i][3] for i in indices) % p
    for endpoint in endpoints:
        if not 6 <= len(endpoint) <= 8:
            raise ValueError("endpoint length is not 6..8")
        if quotient(endpoint) != (0, 0, 0) or height(endpoint) != 3:
            raise ValueError("endpoint is not a zero-core F3 block")
        trace = endpoint & u_set
        if not trace or trace == u_set:
            raise ValueError("endpoint trace is not a nonempty proper U subset")

    edge_rows = [tuple(int(i) for i in row) for row in data["four_edges"]]
    if len(edge_rows) != 4 or len(set(tuple(sorted(row)) for row in edge_rows)) != 4:
        raise ValueError("four_edges must list four distinct endpoint pairs")
    witness = int(data["shared_nonaxial_position"])
    if witness not in l_set - u_set or y_values[witness][1:3] == (0, 0):
        raise ValueError("shared witness is not a nonaxial tail-exterior position")
    for left, right in edge_rows:
        if left == right or not 0 <= left < len(endpoints) or not 0 <= right < len(endpoints):
            raise ValueError("invalid endpoint edge")
        if (endpoints[left] & u_set) & (endpoints[right] & u_set):
            raise ValueError("edge endpoint traces are not disjoint")
        common = endpoints[left] & endpoints[right]
        if witness not in common:
            raise ValueError("edge does not contain the shared witness")
        common_projection = projected_values(y_values, common)
        if vector_sum(common_projection, p, 2) == (0, 0):
            raise ValueError("edge intersection has zero C_p^2 projection")

    components = [frozenset(int(i) for i in row) for row in data["P"]]
    k_set = frozenset(int(i) for i in data["K"])
    if any(not component or not component <= r_set for component in components):
        raise ValueError("each P_i must be a nonempty subset of R")
    seen: set[int] = set(k_set)
    if not k_set <= r_set:
        raise ValueError("K is not contained in R")
    for component in components:
        if seen & component:
            raise ValueError("P_i and K are not pairwise disjoint")
        seen.update(component)
    if seen != r_set:
        raise ValueError("P_i and K do not partition R")
    if not is_projected_zero_sum_free(projected_values(y_values, k_set), p):
        raise ValueError("K is not projected zero-sum-free")

    coefficients: list[int] = []
    for component in components:
        values = projected_values(y_values, component)
        if not is_projected_atom(values, p):
            raise ValueError("a P_i is not a projected zero-sum atom")
        total = quotient(component)
        if total[1:] != (0, 0) or total[0] not in (1, 2, 3):
            raise ValueError("a P_i has an invalid q-axis coefficient")
        coefficients.append(total[0])
    packing = tuple(sorted(coefficients))
    if packing not in PACKING_TYPES:
        raise ValueError("common-R packing type is not one of the seven types")
    if tuple(sorted(int(i) for i in data["packing_coefficients"])) != packing:
        raise ValueError("declared packing coefficients do not match P_i")

    if packing in FORCED_Q_TYPES:
        for endpoint in endpoints:
            q_indices = k_set | frozenset(l_set - set(endpoint))
            if not is_projected_atom(projected_values(y_values, q_indices), p):
                raise ValueError("a forced Q_H is not a projected atom")

    # The inherited validator reconstructs every length-2..8 block, checks all
    # external-block intersections, every derived F3 complement, Hasse rows,
    # the middle gap, uniqueness, and actual Z atomicity from the same labels.
    labelled = load_labelled_verifier()
    labelled.validate_instance(path)
    print(
        "PASS seven-type decomposition and full labelled F3 interface: "
        f"packing={packing}, endpoints={len(endpoints)}, |L|={len(l_set)}, |R|={len(r_set)}"
    )


def build_report() -> dict[str, object]:
    records, rows = packing_records()
    assert len(records) == 7
    assert len(rows) == 14
    assert [tuple(row["packing"]) for row in records if row["q_forced_projected_atom"]] == [
        (3,),
        (1, 2),
        (1, 1, 1),
    ]
    marked = audit_marked_spectra()
    forced_gate = audit_forced_local_gate()
    obligations = {
        "short_blocks": (
            "all tuples (c,F,E) with 0<=c<=p-4, F subset R, E subset L, "
            "2<=c+|F|+|E|<=8 and quotient sum zero"
        ),
        "new_external_F3": (
            "core c=0; endpoint intersections use E cap H; pair intersections "
            "use the exact four-state R Venn spectrum"
        ),
        "each_F3_complement": (
            "the three-state R spectrum jointly marks block part F and every "
            "internal subset G subset R\\F; apply the complete axial criterion"
        ),
        "forced_Q_local_gate": (
            "in the three forced types, a nonempty projected-zero E subset "
            "L\\H is impossible except K empty and E=L\\H"
        ),
        "forced_Q_endpoint_exchange": (
            "two distinct selected endpoints have projected-zero intersection "
            "iff K is empty and L is their union; then both exchange petals are "
            "coefficient-one projected atoms and the intersection coefficient is "
            "-1. Repeated traces are impossible, and the only surviving axial "
            "trace pair is two distinct doubleton traces"
        ),
        "global_boundary": (
            "no actual p=233 or p=1399 labelled instance was enumerated; "
            "TOP/CONST outside Z remain out of scope"
        ),
    }
    type_hash = canonical_hash(records)
    certificate = {
        "status": (
            "PROVED_EXACT_MARKED_INTERFACE/"
            "FORCED_TYPES_REPEATED_TRACE_AXIS_BRANCH_CLOSED/"
            "NO_PACKING_TYPE_CLOSED/FOURTH_BLOCK_NOT_FORCED/GLOBAL_INCOMPLETE"
        ),
        "packing_records": records,
        "expanded_rows": rows,
        "marked_spectrum_audit": marked,
        "forced_local_gate_audit": forced_gate,
        "obligations": obligations,
    }
    certificate_hash = canonical_hash(certificate)
    if EXPECTED_TYPE_SHA256:
        assert type_hash == EXPECTED_TYPE_SHA256
    if EXPECTED_CERTIFICATE_SHA256:
        assert certificate_hash == EXPECTED_CERTIFICATE_SHA256
    return {
        "packing_type_count": len(records),
        "expanded_endpoint_row_count": len(rows),
        "forced_q_type_count": sum(row["q_forced_projected_atom"] for row in records),
        "marked_spectrum_small_case_count": marked["case_count"],
        "forced_local_gate_atom_count": forced_gate["atom_count"],
        "type_sha256": type_hash,
        "certificate_sha256": certificate_hash,
        "status": certificate["status"],
        "certificate": certificate,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path)
    args = parser.parse_args()
    if args.instance:
        validate_full_instance(args.instance)
        return
    print(json.dumps(build_report(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
