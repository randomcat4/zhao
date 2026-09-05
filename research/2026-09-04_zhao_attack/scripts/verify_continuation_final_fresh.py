#!/usr/bin/env python3
"""Independent finite checker for the continued 16-atom star arguments.

This program is deliberately self-contained.  It does not import, execute, or read
any author checker/certificate.  Its only inputs are the mathematical constants
written below.  Outputs use the verify_continuation_final_fresh prefix.
"""

from __future__ import annotations

from array import array
from dataclasses import dataclass
from hashlib import sha256
from itertools import product
import gzip
import json
from pathlib import Path
import platform
import sys
import time


P = 5
Q4 = P ** 4
INF = 255

HERE = Path(__file__).resolve()
RUN = HERE.parent.parent
PROOFS = RUN / "proofs"
EVIDENCE = RUN / "evidence"

SOURCE_NAMES = (
    "continue_atom16_star.md",
    "continue_atom16_star_addendum.md",
    "root_continue_star_d2.md",
    "root_continue_atom17_integrity.md",
    "root_continue_support17_exclusion.md",
    "root_continue_atom16_single_complements.md",
    "continue_rainbow17.md",
)


def file_hash(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def encode(v: tuple[int, ...]) -> int:
    z = 0
    for x in v:
        z = P * z + (x % P)
    return z


def decode(z: int, dim: int = 4) -> tuple[int, ...]:
    out = [0] * dim
    for i in range(dim - 1, -1, -1):
        out[i] = z % P
        z //= P
    return tuple(out)


V4 = tuple(decode(z, 4) for z in range(Q4))


def vadd_code(a: int, b: int) -> int:
    av, bv = V4[a], V4[b]
    return encode(tuple((av[i] + bv[i]) % P for i in range(4)))


def vneg_code(a: int) -> int:
    av = V4[a]
    return encode(tuple((-x) % P for x in av))


NEG4 = tuple(vneg_code(z) for z in range(Q4))
ADD4 = tuple(array("H", (vadd_code(a, b) for b in range(Q4))) for a in range(Q4))
SUB4 = tuple(array("H", (ADD4[t][NEG4[g]] for t in range(Q4))) for g in range(Q4))


def add4(a: int, b: int) -> int:
    return ADD4[a][b]


def vec4(*xs: int) -> int:
    assert len(xs) == 4
    return encode(tuple(xs))


E4 = (
    vec4(1, 0, 0, 0),
    vec4(0, 1, 0, 0),
    vec4(0, 0, 1, 0),
    vec4(0, 0, 0, 1),
)


def multiset_sequence(parts: list[tuple[int, int]]) -> list[int]:
    ans: list[int] = []
    for value, multiplicity in parts:
        ans.extend([value] * multiplicity)
    return ans


def raw_subset_audit(seq: list[int]) -> dict:
    """Enumerate every position subset and return exact zero-sum information."""
    size = 1 << len(seq)
    sums = array("H", [0]) * size
    zero_masks: list[int] = []
    for mask in range(1, size):
        bit = mask & -mask
        i = bit.bit_length() - 1
        prev = mask ^ bit
        sums[mask] = ADD4[sums[prev]][seq[i]]
        if sums[mask] == 0:
            zero_masks.append(mask)
    return {
        "subset_count": size,
        "nonempty_zero_masks": zero_masks,
        "sum_table": sums,
    }


def initial_distance_state(seq: list[int]) -> tuple[bytes, tuple[int, ...]]:
    dist = bytearray([INF] * Q4)
    masks = [0] * Q4
    dist[0] = 0
    for pos, value in enumerate(seq):
        old = bytes(dist)
        old_masks = tuple(masks)
        for target in range(Q4):
            source = SUB4[value][target]
            ds = old[source]
            if ds != INF and ds + 1 < dist[target]:
                dist[target] = ds + 1
                masks[target] = old_masks[source] | (1 << pos)
    return bytes(dist), tuple(masks)


def extend_distance_state(
    dist: bytes, masks: tuple[int, ...], value: int, pos: int
) -> tuple[bytes, tuple[int, ...]]:
    new_dist = bytearray(dist)
    new_masks = list(masks)
    source_row = SUB4[value]
    pos_bit = 1 << pos
    for target in range(Q4):
        source = source_row[target]
        ds = dist[source]
        if ds != INF and ds + 1 < new_dist[target]:
            new_dist[target] = ds + 1
            new_masks[target] = masks[source] | pos_bit
    return bytes(new_dist), tuple(new_masks)


def mask_sum(seq: list[int], mask: int) -> int:
    total = 0
    for i, value in enumerate(seq):
        if (mask >> i) & 1:
            total = ADD4[total][value]
    return total


@dataclass
class D3Stats:
    level_nodes: list[int]
    parent_records: int = 0
    extension_attempts: int = 0
    accepted_edges: int = 0
    rejected_edges: int = 0
    structurally_forbidden_edges: int = 0


def d3_core(kind: str) -> list[int]:
    x, y1, y2, y3 = E4
    g1, g2, g3 = add4(x, y1), add4(x, y2), add4(x, y3)
    if kind == "VA":
        return multiset_sequence(
            [(x, 1), (g1, 3), (y1, 3), (g2, 1), (y2, 2), (g3, 1), (y3, 2)]
        )
    if kind == "VB":
        return multiset_sequence(
            [(x, 1), (g1, 2), (y1, 3), (g2, 2), (y2, 2), (g3, 1), (y3, 2)]
        )
    raise ValueError(kind)


def enumerate_d3_tree(kind: str, gzout: gzip.GzipFile) -> dict:
    core = d3_core(kind)
    assert len(core) == 13
    raw = raw_subset_audit(core)
    assert raw["subset_count"] == 8192
    assert not raw["nonempty_zero_masks"], (kind, raw["nonempty_zero_masks"][:3])
    dist0, masks0 = initial_distance_state(core)
    forced_support = set(core)
    stats = D3Stats([1, 0, 0, 0, 0, 0])

    def visit(path: tuple[int, ...], dist: bytes, masks: tuple[int, ...]) -> None:
        depth = len(path)
        assert depth <= 4
        # Canonical nondecreasing multisets.  Equality is permitted exactly once,
        # hence only while the current path has no repeated value.
        has_repeat = len(set(path)) != len(path)
        start = 0 if not path else path[-1] + (1 if has_repeat else 0)
        outcomes: list[int] = []
        safe_values: list[int] = []
        seq = core + list(path)
        for value in range(start, Q4):
            stats.extension_attempts += 1
            if value in forced_support:
                # W is disjoint in value from the seven forced support classes.
                outcomes.append(-2)
                stats.structurally_forbidden_edges += 1
                continue
            old_mask = masks[NEG4[value]]
            old_distance = dist[NEG4[value]]
            if old_distance != INF and old_distance + 1 <= 14:
                # Exact rejecting witness: a subset of the current positions plus
                # the candidate value is a zero sum of length at most fourteen.
                assert old_mask.bit_count() == old_distance
                assert mask_sum(seq, old_mask) == NEG4[value]
                outcomes.append(old_mask)
                stats.rejected_edges += 1
            else:
                outcomes.append(-1)
                safe_values.append(value)
                stats.accepted_edges += 1

        record = {
            "core": kind,
            "path": list(path),
            "depth": depth,
            "candidate_start": start,
            "candidate_stop_exclusive": Q4,
            "outcomes": outcomes,
            "outcome_convention": "-2=forced-support value forbidden to W; -1=safe; nonnegative=current-sequence subset mask rejecting candidate",
        }
        gzout.write((json.dumps(record, separators=(",", ":")) + "\n").encode("utf-8"))
        stats.parent_records += 1

        if depth == 4:
            assert not safe_values, (kind, path, safe_values[:5])
            return
        for value in safe_values:
            child_path = path + (value,)
            stats.level_nodes[depth + 1] += 1
            child_dist, child_masks = extend_distance_state(
                dist, masks, value, len(core) + depth
            )
            # A safe extension has no nonempty zero sum of length <= 14.
            assert child_dist[0] == 0
            visit(child_path, child_dist, child_masks)

    visit((), dist0, masks0)
    assert stats.level_nodes[5] == 0
    return {
        "core": kind,
        "fixed_core_positions": len(core),
        "fixed_core_subset_denominator": raw["subset_count"],
        "level_nodes": stats.level_nodes,
        "parent_records": stats.parent_records,
        "canonical_extension_attempts": stats.extension_attempts,
        "accepted_edges": stats.accepted_edges,
        "rejected_edges": stats.rejected_edges,
        "structurally_forbidden_edges": stats.structurally_forbidden_edges,
        "root_candidates": Q4,
        "max_allowed_multiplicity_pattern": "at most one value twice; all others once",
        "terminal_statement": "every safe canonical path has length at most four",
    }


def d4_generators(chart: str, omitted: int) -> tuple[int, list[int]]:
    if chart == "omit_x":
        x = omitted
        ys = [E4[0], E4[1], E4[2], E4[3]]
    elif chart == "omit_y1":
        x = E4[0]
        ys = [omitted, E4[1], E4[2], E4[3]]
    elif chart == "omit_ordinary":
        x = E4[0]
        ys = [E4[1], E4[2], E4[3], omitted]
    else:
        raise ValueError(chart)
    return x, ys


def first_short_zero_mask(seq: list[int], cap: int = 14) -> int | None:
    assert len(seq) == 15
    sums = array("H", [0]) * (1 << len(seq))
    for mask in range(1, 1 << len(seq)):
        bit = mask & -mask
        i = bit.bit_length() - 1
        prev = mask ^ bit
        sums[mask] = ADD4[sums[prev]][seq[i]]
        if sums[mask] == 0 and mask.bit_count() <= cap:
            return mask
    return None


def enumerate_d4_tables() -> tuple[dict, dict]:
    charts = ("omit_x", "omit_y1", "omit_ordinary")
    output: dict[str, list[dict]] = {}
    summary: dict[str, dict] = {}
    for chart in charts:
        rows: list[dict] = []
        eligible = 0
        invalid_zero = 0
        invalid_collision = 0
        witnesses = 0
        for omitted in range(Q4):
            x, ys = d4_generators(chart, omitted)
            gs = [add4(x, y) for y in ys]
            support = [x] + ys + gs
            zero_indices = [i for i, z in enumerate(support) if z == 0]
            by_value: dict[int, list[int]] = {}
            for i, z in enumerate(support):
                by_value.setdefault(z, []).append(i)
            collisions = [inds for inds in by_value.values() if len(inds) > 1]
            if zero_indices or collisions:
                invalid_zero += bool(zero_indices)
                invalid_collision += bool(collisions)
                rows.append(
                    {
                        "omitted": omitted,
                        "omitted_vector": list(V4[omitted]),
                        "eligible": False,
                        "zero_support_indices": zero_indices,
                        "collision_index_sets": collisions,
                    }
                )
                continue
            eligible += 1
            ordinary_parts: list[tuple[int, int]] = []
            for i in range(1, 4):
                ordinary_parts.extend([(gs[i], 1), (ys[i], 2)])
            seq = multiset_sequence(
                [(x, 1), (gs[0], 2), (ys[0], 3)] + ordinary_parts
            )
            assert len(seq) == 15
            mask = first_short_zero_mask(seq, 14)
            assert mask is not None, (chart, omitted)
            assert 1 <= mask.bit_count() <= 14
            assert mask_sum(seq, mask) == 0
            witnesses += 1
            positions = [i for i in range(15) if (mask >> i) & 1]
            rows.append(
                {
                    "omitted": omitted,
                    "omitted_vector": list(V4[omitted]),
                    "eligible": True,
                    "sequence_codes": seq,
                    "witness_mask": mask,
                    "witness_positions_zero_based": positions,
                    "witness_length": len(positions),
                    "witness_values": [list(V4[seq[i]]) for i in positions],
                }
            )
        assert len(rows) == Q4
        assert witnesses == eligible
        output[chart] = rows
        summary[chart] = {
            "omitted_vector_denominator": Q4,
            "eligible_distinct_nonzero_supports": eligible,
            "ineligible_with_zero": invalid_zero,
            "ineligible_with_collision": invalid_collision,
            "eligible_with_verified_short_zero_witness": witnesses,
            "safe_eligible_cores": eligible - witnesses,
        }
    return output, summary


def encode3(v: tuple[int, int, int]) -> int:
    return (v[0] * P + v[1]) * P + v[2]


def decode3(z: int) -> tuple[int, int, int]:
    return (z // 25, (z // 5) % 5, z % 5)


V3 = tuple(decode3(z) for z in range(125))


def add3(a: int, b: int) -> int:
    x, y = V3[a], V3[b]
    return encode3(((x[0] + y[0]) % 5, (x[1] + y[1]) % 5, (x[2] + y[2]) % 5))


def neg3(a: int) -> int:
    x = V3[a]
    return encode3(((-x[0]) % 5, (-x[1]) % 5, (-x[2]) % 5))


def ell3(a: int) -> int:
    x = V3[a]
    return (3 * x[0] + x[1] + x[2]) % 5


def audit_d2_core() -> dict:
    x = encode3((1, 0, 0))
    y1 = encode3((0, 1, 0))
    y2 = encode3((0, 0, 1))
    g1, g2 = add3(x, y1), add3(x, y2)
    seq = multiset_sequence([(x, 1), (g1, 3), (y1, 3), (g2, 2), (y2, 2)])
    assert len(seq) == 11
    subset_count = 1 << len(seq)
    sums = array("B", [0]) * subset_count
    distances = [INF] * 125
    distance_masks = [0] * 125
    signed = [0] * 125
    distances[0] = 0
    for mask in range(subset_count):
        if mask:
            bit = mask & -mask
            i = bit.bit_length() - 1
            prev = mask ^ bit
            sums[mask] = add3(sums[prev], seq[i])
        s = sums[mask]
        length = mask.bit_count()
        if length < distances[s]:
            distances[s] = length
            distance_masks[s] = mask
        signed[s] = (signed[s] + (1 if length % 2 == 0 else -1)) % 5
    nonempty_zero_masks = [m for m in range(1, subset_count) if sums[m] == 0]
    assert not nonempty_zero_masks
    sigma = sums[subset_count - 1]
    unreachable = {t for t, d in enumerate(distances) if d == INF}
    e10 = {t for t, d in enumerate(distances) if d == INF or d >= 10}
    e11 = {t for t, d in enumerate(distances) if d == INF or d >= 11}
    expected_m = {
        encode3((0, 4, 0)),
        encode3((1, 2, 4)),
        encode3((2, 4, 4)),
        encode3((4, 2, 0)),
    }
    expected_e10 = expected_m | {
        encode3((0, 1, 4)),
        encode3((1, 0, 4)),
        encode3((1, 1, 4)),
    }
    assert sigma == encode3((1, 1, 4))
    assert unreachable == expected_m
    assert e10 == expected_e10
    assert e11 == expected_m | {sigma}
    assert ell3(sigma) == 3
    assert {ell3(t) for t in unreachable} == {4}
    assert len([t for t in e10 if ell3(t) == 0]) == 1
    assert {t for t in e10 if ell3(t) == 3} == {sigma}
    polynomial_failures = [t for t in range(125) if signed[t] != (1 + ell3(t)) % 5]
    assert not polynomial_failures
    rows = []
    for t in range(125):
        rows.append(
            {
                "code": t,
                "vector": list(V3[t]),
                "ell": ell3(t),
                "distance": None if distances[t] == INF else distances[t],
                "distance_witness_mask": None if distances[t] == INF else distance_masks[t],
                "signed_subset_coefficient_mod5": signed[t],
                "one_plus_ell_mod5": (1 + ell3(t)) % 5,
            }
        )
    return {
        "position_sequence_codes": seq,
        "position_sequence_vectors": [list(V3[t]) for t in seq],
        "position_subset_denominator": subset_count,
        "zero_sum_free": True,
        "sigma": list(V3[sigma]),
        "unreachable_M": [list(V3[t]) for t in sorted(unreachable)],
        "E10": [list(V3[t]) for t in sorted(e10)],
        "E11": [list(V3[t]) for t in sorted(e11)],
        "ell_formula": "3*t1+t2+t3 mod 5",
        "polynomial_identity": "signed_subset_coefficient(t) = 1 + ell(t) mod 5",
        "polynomial_failure_count": len(polynomial_failures),
        "point_rows": rows,
    }


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def certificate_for_counts(n: tuple[int, ...], repeated_class: int | None):
    for k in product(*(range(x + 1) for x in n)):
        if sum(k) != 5:
            continue
        scalar = sum(c * k[c] for c in range(5)) % 5
        if scalar not in (0, 2):
            continue
        for c in range(5):
            if not (0 < k[c] < n[c]):
                continue
            class_has_two_distinct = repeated_class is None or c != repeated_class or n[c] >= 3
            if class_has_two_distinct:
                return k, scalar, c
    return None


def audit_scalar_table() -> dict:
    patterns: list[dict] = []
    count_vectors = list(compositions(9, 5))
    assert len(count_vectors) == 715
    for n in count_vectors:
        cert = certificate_for_counts(n, None)
        assert cert is not None, ("distinct", n)
        k, scalar, c = cert
        patterns.append(
            {
                "case": "all_actual_values_distinct",
                "n": list(n),
                "repeated_class": None,
                "k": list(k),
                "scalar_sum_mod5": scalar,
                "partially_selected_class": c,
            }
        )
    repeated_patterns = 0
    for n in count_vectors:
        for r in range(5):
            if n[r] < 2:
                continue
            repeated_patterns += 1
            cert = certificate_for_counts(n, r)
            assert cert is not None, ("one_pair", n, r)
            k, scalar, c = cert
            assert not (c == r and n[c] == 2)
            patterns.append(
                {
                    "case": "exactly_one_repeated_actual_value_pair",
                    "n": list(n),
                    "repeated_class": r,
                    "k": list(k),
                    "scalar_sum_mod5": scalar,
                    "partially_selected_class": c,
                }
            )
    assert repeated_patterns == 1650
    assert len(patterns) == 2365
    # Replay every certificate from the serialized mathematical interface.
    for row in patterns:
        n, k, c = row["n"], row["k"], row["partially_selected_class"]
        assert sum(n) == 9 and sum(k) == 5
        assert all(0 <= k[i] <= n[i] for i in range(5))
        assert sum(i * k[i] for i in range(5)) % 5 in (0, 2)
        assert 0 < k[c] < n[c]
        r = row["repeated_class"]
        assert r is None or c != r or n[c] >= 3
    return {
        "all_distinct_count_vectors": 715,
        "one_pair_count_vector_and_class_patterns": repeated_patterns,
        "complete_denominator": len(patterns),
        "certificate_rows": patterns,
    }


def audit_rainbow_counterexample() -> dict:
    u = [
        vec4(1, 0, 0, 0),
        vec4(4, 1, 1, 0),
        vec4(0, 1, 0, 0),
        vec4(0, 0, 1, 0),
        vec4(2, 0, 4, 0),
        vec4(4, 0, 2, 0),
    ]
    targets = {
        "g": vec4(0, 1, 1, 0),
        "h": vec4(1, 1, 0, 0),
        "k": vec4(1, 0, 1, 0),
    }
    all_values = u + list(targets.values())
    assert 0 not in all_values
    assert len(set(all_values)) == 9

    pair_representations: dict[str, list[list[int]]] = {}
    for name, target in targets.items():
        pairs = []
        for i in range(6):
            for j in range(i + 1, 6):
                if ADD4[u[i]][u[j]] == target:
                    pairs.append([i, j])
        pair_representations[name] = pairs
    assert pair_representations == {
        "g": [[0, 1], [2, 3]],
        "h": [[0, 2], [1, 4]],
        "k": [[0, 3], [4, 5]],
    }
    for pairs in pair_representations.values():
        assert set(pairs[0]).isdisjoint(pairs[1])
    all_edges = [tuple(edge) for pairs in pair_representations.values() for edge in pairs]
    assert len(set(all_edges)) == 6
    rainbow_choices = []
    for eg in pair_representations["g"]:
        for eh in pair_representations["h"]:
            for ek in pair_representations["k"]:
                disjoint = (
                    set(eg).isdisjoint(eh)
                    and set(eg).isdisjoint(ek)
                    and set(eh).isdisjoint(ek)
                )
                rainbow_choices.append({"edges": [eg, eh, ek], "pairwise_disjoint": disjoint})
    assert len(rainbow_choices) == 8
    assert not any(row["pairwise_disjoint"] for row in rainbow_choices)

    subset_sums = []
    zero_masks = []
    for mask in range(1, 1 << 9):
        s = mask_sum(all_values, mask)
        subset_sums.append(s)
        if s == 0:
            zero_masks.append(mask)
    assert len(subset_sums) == 511
    assert not zero_masks

    replacement_tests = 0
    replacement_equalities = []
    for dmask in range(1, 1 << 6):
        dsize = dmask.bit_count()
        dsum = mask_sum(u, dmask)
        for qmask in range(1, 1 << 3):
            if dsize - qmask.bit_count() < 3:
                continue
            replacement_tests += 1
            qsum = mask_sum(list(targets.values()), qmask)
            if dsum == qsum:
                replacement_equalities.append([dmask, qmask])
    assert replacement_tests == 88
    assert not replacement_equalities
    return {
        "u_vectors": [list(V4[z]) for z in u],
        "target_vectors": {name: list(V4[z]) for name, z in targets.items()},
        "nine_values_nonzero_and_distinct": True,
        "pair_representations": pair_representations,
        "rainbow_choice_denominator": 8,
        "rainbow_choices": rainbow_choices,
        "pairwise_disjoint_rainbows": 0,
        "nonempty_subset_denominator": 511,
        "nonempty_subset_sum_codes": subset_sums,
        "zero_sum_subsets": zero_masks,
        "size_qualified_replacement_denominator": replacement_tests,
        "replacement_equalities": replacement_equalities,
        "scope": "local nine-value configuration only; no 17-atom or B20 extension is asserted",
    }


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    source_hashes_before = {name: file_hash(PROOFS / name) for name in SOURCE_NAMES}

    d3_path = EVIDENCE / "verify_continuation_final_fresh_d3_tree.jsonl.gz"
    with gzip.GzipFile(filename=d3_path, mode="wb", compresslevel=9, mtime=0) as gzout:
        d3_summary = [enumerate_d3_tree(kind, gzout) for kind in ("VA", "VB")]

    d4_tables, d4_summary = enumerate_d4_tables()
    d4_path = EVIDENCE / "verify_continuation_final_fresh_d4_tables.json"
    d4_path.write_text(json.dumps(d4_tables, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    d2_core = audit_d2_core()
    scalar = audit_scalar_table()
    d2_path = EVIDENCE / "verify_continuation_final_fresh_d2.json"
    d2_path.write_text(
        json.dumps({"core_2048": d2_core, "scalar_2365": scalar}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    rainbow = audit_rainbow_counterexample()
    rainbow_path = EVIDENCE / "verify_continuation_final_fresh_rainbow.json"
    rainbow_path.write_text(json.dumps(rainbow, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    source_hashes_after = {name: file_hash(PROOFS / name) for name in SOURCE_NAMES}
    assert source_hashes_before == source_hashes_after
    elapsed = time.perf_counter() - started
    summary = {
        "status": "PASS",
        "checker": HERE.name,
        "checker_sha256": file_hash(HERE),
        "python": sys.executable,
        "python_version": platform.python_version(),
        "elapsed_seconds": elapsed,
        "timed_out": False,
        "source_sha256": source_hashes_after,
        "d3": d3_summary,
        "d4": d4_summary,
        "d2": {
            "position_subset_denominator": d2_core["position_subset_denominator"],
            "zero_sum_free": d2_core["zero_sum_free"],
            "unreachable_count": len(d2_core["unreachable_M"]),
            "E10_count": len(d2_core["E10"]),
            "polynomial_failure_count": d2_core["polynomial_failure_count"],
            "scalar_all_distinct": scalar["all_distinct_count_vectors"],
            "scalar_one_pair": scalar["one_pair_count_vector_and_class_patterns"],
            "scalar_complete_denominator": scalar["complete_denominator"],
        },
        "rainbow_counterexample": {
            "pair_targets": rainbow["pair_representations"],
            "rainbow_choice_denominator": rainbow["rainbow_choice_denominator"],
            "pairwise_disjoint_rainbows": rainbow["pairwise_disjoint_rainbows"],
            "nonempty_subset_denominator": rainbow["nonempty_subset_denominator"],
            "zero_sum_subsets": len(rainbow["zero_sum_subsets"]),
            "size_qualified_replacement_denominator": rainbow["size_qualified_replacement_denominator"],
            "replacement_equalities": len(rainbow["replacement_equalities"]),
        },
        "evidence_sha256": {
            d3_path.name: file_hash(d3_path),
            d4_path.name: file_hash(d4_path),
            d2_path.name: file_hash(d2_path),
            rainbow_path.name: file_hash(rainbow_path),
        },
    }
    summary_path = EVIDENCE / "verify_continuation_final_fresh_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
