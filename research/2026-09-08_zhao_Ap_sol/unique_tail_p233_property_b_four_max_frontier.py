#!/usr/bin/env python3
"""Search the Property-B support frontier for one singleton and three doubletons.

This is a support-level diagnostic only.  It asks whether four maximal
``C_233^2`` atoms with endpoint traces ``1,3,5,6`` can have heavy bases that
lie in every other atom's Property-B support.  Atomic multiplicities, the
q-coordinate, induced short blocks, Hasse rows, and the actual Z atom are not
encoded, so a surviving tuple is RELAXED and is never a slice candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path


P = 233
Vec = tuple[int, int]


def add(a: Vec, b: Vec) -> Vec:
    return ((a[0] + b[0]) % P, (a[1] + b[1]) % P)


def sub(a: Vec, b: Vec) -> Vec:
    return ((a[0] - b[0]) % P, (a[1] - b[1]) % P)


def scale(c: int, a: Vec) -> Vec:
    return ((c * a[0]) % P, (c * a[1]) % P)


def dot(phi: Vec, v: Vec) -> int:
    return (phi[0] * v[0] + phi[1] * v[1]) % P


def cross(a: Vec, b: Vec) -> int:
    return (a[0] * b[1] - a[1] * b[0]) % P


def signed(v: Vec) -> list[int]:
    return [x if x <= P // 2 else x - P for x in v]


@dataclass(frozen=True)
class Support:
    base: Vec
    phi: Vec

    def contains(self, v: Vec) -> bool:
        return v == self.base or dot(self.phi, v) == 1

    def points(self) -> tuple[Vec, ...]:
        ans = []
        for x in range(P):
            for y in range(P):
                v = (x, y)
                if self.contains(v):
                    ans.append(v)
        if len(ans) != P + 1 or (0, 0) in ans:
            raise AssertionError("invalid Property-B support")
        return tuple(ans)


def normalized_phi(base: Vec, point_on_line: Vec) -> Vec:
    denominator = cross(base, point_on_line)
    if denominator == 0:
        raise ValueError("the affine line would contain zero")
    inverse = pow(denominator, -1, P)
    return ((-base[1] * inverse) % P, (base[0] * inverse) % P)


def pair_tail_supports(a: Vec, b: Vec) -> tuple[Support, ...]:
    ans = [
        Support(a, normalized_phi(a, b)),
        Support(b, normalized_phi(b, a)),
    ]
    direction = sub(b, a)
    phi = normalized_phi(direction, a)
    ans.extend(Support(scale(c, direction), phi) for c in range(1, P))
    result = tuple(ans)
    if len(result) != P + 1 or len(set(result)) != P + 1:
        raise AssertionError("pair-tail denominator mismatch")
    if not all(s.contains(a) and s.contains(b) for s in result):
        raise AssertionError("pair-tail support omitted a tail")
    return result


def one_tail_supports_with_base(tail: Vec, base: Vec) -> tuple[Support, ...]:
    if base == tail:
        perpendicular = ((-base[1]) % P, base[0] % P)
        return tuple(Support(base, scale(c, perpendicular)) for c in range(1, P))
    if cross(base, tail) == 0:
        return ()
    return (Support(base, normalized_phi(base, tail)),)


def mutually_supported(left: Support, right: Support) -> bool:
    return left.contains(right.base) and right.contains(left.base)


def candidate_supports(anchor: Support, tail: Vec) -> tuple[Support, ...]:
    rows = []
    for base in anchor.points():
        for support in one_tail_supports_with_base(tail, base):
            if support.contains(anchor.base):
                rows.append(support)
    return tuple(dict.fromkeys(rows))


def main() -> None:
    e = (1, 0)
    f = (0, 1)
    t = (-1 % P, -1 % P)

    # H trace {e} leaves {f,t}; the three doubleton traces leave t,f,e.
    anchors = pair_tail_supports(f, t)
    tail_rows = (t, f, e)
    anchor_candidate_counts: list[list[int]] = []
    first_witness: dict[str, object] | None = None
    first_two_label_witness: dict[str, object] | None = None
    anchors_with_clique = 0

    for anchor_index, anchor in enumerate(anchors):
        candidates = tuple(candidate_supports(anchor, tail) for tail in tail_rows)
        anchor_candidate_counts.append([len(rows) for rows in candidates])

        adjacency_12 = {
            i: {j for j, row in enumerate(candidates[1]) if mutually_supported(left, row)}
            for i, left in enumerate(candidates[0])
        }
        adjacency_13 = {
            i: {k for k, row in enumerate(candidates[2]) if mutually_supported(left, row)}
            for i, left in enumerate(candidates[0])
        }
        adjacency_23 = {
            j: {k for k, row in enumerate(candidates[2]) if mutually_supported(left, row)}
            for j, left in enumerate(candidates[1])
        }

        witness = None
        two_label_witness = None
        for i, js in adjacency_12.items():
            for j in js:
                common = adjacency_13[i] & adjacency_23[j]
                if common:
                    if witness is None:
                        witness = (i, j, min(common))
                    for k in common:
                        bases = {anchor.base, candidates[0][i].base, candidates[1][j].base, candidates[2][k].base}
                        if len(bases) >= 2:
                            two_label_witness = (i, j, k)
                            break
                if two_label_witness is not None:
                    break
            if two_label_witness is not None:
                break
        if witness is None:
            continue
        anchors_with_clique += 1
        if first_witness is None:
            selected = [candidates[k][witness[k]] for k in range(3)]
            all_supports = [anchor, *selected]
            common_points = [
                v for v in anchor.points() if all(row.contains(v) for row in selected)
            ]
            first_witness = {
                "anchor_index": anchor_index,
                "supports": [
                    {"base": signed(row.base), "phi": signed(row.phi)}
                    for row in all_supports
                ],
                "common_points": [signed(v) for v in common_points],
                "all_heavy_bases_in_every_support": all(
                    row.contains(other.base)
                    for row in all_supports
                    for other in all_supports
                ),
            }
        if two_label_witness is not None and first_two_label_witness is None:
            selected = [candidates[k][two_label_witness[k]] for k in range(3)]
            all_supports = [anchor, *selected]
            common_points = [
                v for v in anchor.points() if all(row.contains(v) for row in selected)
            ]
            first_two_label_witness = {
                "anchor_index": anchor_index,
                "supports": [
                    {"base": signed(row.base), "phi": signed(row.phi)}
                    for row in all_supports
                ],
                "distinct_heavy_bases": len({row.base for row in all_supports}),
                "common_points": [signed(v) for v in common_points],
            }

    core = {
        "schema": "unique_tail_p233_property_b_four_max_frontier/v1",
        "p": P,
        "trace_family": {
            "singleton_endpoint_trace": ["e"],
            "singleton_Q_tail": ["f", "t"],
            "doubleton_endpoint_traces": [["e", "f"], ["e", "t"], ["f", "t"]],
            "doubleton_Q_tails": ["t", "f", "e"],
        },
        "anchor_support_count": len(anchors),
        "candidate_count_minmax_by_doubleton_Q_tail": [
            [min(row[k] for row in anchor_candidate_counts), max(row[k] for row in anchor_candidate_counts)]
            for k in range(3)
        ],
        "anchors_with_four_support_clique": anchors_with_clique,
        "first_support_level_witness": first_witness,
        "first_two_common_label_witness": first_two_label_witness,
        "status": (
            "RELAXED_PROPERTY_B_SUPPORT_COMPATIBLE/GLOBAL_INCOMPLETE"
            if first_witness is not None
            else "PROPERTY_B_FOUR_MAX_SUPPORT_UNSAT"
        ),
        "omitted": [
            "maximal-atom coefficient multiplicities",
            "literal common-kernel capacity beyond mutual heavy-base membership",
            "q-coordinate lift and automatically induced short blocks",
            "P-mixed targets, Hasse rows, and actual Z atomicity",
        ],
    }
    canonical = json.dumps(core, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    report = dict(core)
    report["certificate_sha256"] = sha256(canonical).hexdigest()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    path = Path(__file__).with_name("unique_tail_p233_property_b_four_max_frontier_report.json")
    path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
