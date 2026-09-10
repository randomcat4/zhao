#!/usr/bin/env python3
r"""Exact-instance/CEGAR interface for the first p=233 unique-tail slice.

This module deliberately does *not* search over endpoint incidences.  It
freezes the first nontrivial slice

    p=233, (ell,b)=(7,4), packing (3), |P|=2, kappa=1,

and validates the literal-position schema for one supplied incidence.  The
remaining universal constraints are exposed as exact separation-oracle
contracts.  With no instance, or without exact CLEAR results from every
oracle, the only allowed statuses are INSTANCE_SCHEMA and RELAXED.

The v1 incidence stage contains only length-seven zero-core endpoints.  A
later schema version may add length-eight endpoints; silently accepting them
here would change the frozen slice.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_p233_type3_p2_exact_slice_report.json"
SCHEMA = "unique_tail_p233_type3_p2_exact_slice_instance_v1"

P = 233
ELL = 7
B = 4
TAIL_SIZE = ELL - B
X_MULTIPLICITY = P - 4
Y_SIZE = 2 * P + 8
PACKING_COEFFICIENT = 3
PACKING_SIZE = 2
KAPPA = 1
Q = (1, 0, 0)
ZERO3 = (0, 0, 0)
ZERO2 = (0, 0)
ENDPOINT_STAGE = "length_7_only"

LENGTH_FAMILIES = {
    2: (1,),
    3: (1,),
    4: (1, 2),
    5: (1, 2),
    6: (1, 2, 3),
    7: (2, 3),
    8: (3,),
}

DEPENDENCY_PATHS = (
    HERE / "proofs" / "unique_tail_labelled_position_next.md",
    HERE / "verify_unique_tail_labelled_position_next.py",
    HERE / "proofs" / "unique_tail_four_edge_joint_csp.md",
    HERE / "proofs" / "unique_tail_common_R_next.md",
    HERE / "proofs" / "unique_tail_all_packing_short_blocks.md",
    HERE / "proofs" / "unique_tail_remaining_long_complement_internal_sums.md",
    HERE / "proofs" / "unique_tail_remaining_six_f2_complements.md",
    HERE / "proofs" / "unique_tail_tail_anchoring.md",
    HERE / "proofs" / "unique_tail_p233_singleton_tail_fringe.md",
    HERE / "verifications" / "unique_tail_p233_singleton_tail_fringe_independent_review.md",
)


class InstanceError(ValueError):
    """The supplied literal-position instance violates the frozen schema."""


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def add(left: Sequence[int], right: Sequence[int], prime: int = P) -> tuple[int, ...]:
    return tuple((a + b) % prime for a, b in zip(left, right))


def neg(value: Sequence[int], prime: int = P) -> tuple[int, ...]:
    return tuple((-entry) % prime for entry in value)


def scalar(coefficient: int, value: Sequence[int], prime: int = P) -> tuple[int, ...]:
    return tuple(coefficient * entry % prime for entry in value)


def vector_sum(
    values: Iterable[Sequence[int]], dimension: int, prime: int = P
) -> tuple[int, ...]:
    total = (0,) * dimension
    for value in values:
        total = add(total, value, prime)
    return total


def rho(value: Sequence[int]) -> tuple[int, int]:
    return int(value[1]) % P, int(value[2]) % P


def trace_mask(endpoint: frozenset[int], u_ordered: tuple[int, ...]) -> int:
    answer = 0
    for bit, position in enumerate(u_ordered):
        if position in endpoint:
            answer |= 1 << bit
    return answer


def rank_two(vectors: Iterable[tuple[int, int]]) -> bool:
    rows = tuple(vectors)
    return any(
        (left[0] * right[1] - left[1] * right[0]) % P
        for left, right in itertools.combinations(rows, 2)
    )


def mod_fraction(value: Fraction, prime: int = P) -> int:
    return value.numerator * pow(value.denominator, -1, prime) % prime


def checked_index_set(
    raw: object, name: str, *, expected_size: int | None = None
) -> frozenset[int]:
    if not isinstance(raw, list) or any(not isinstance(i, int) for i in raw):
        raise InstanceError(f"{name} must be a JSON list of integer position indices")
    result = frozenset(raw)
    if len(result) != len(raw):
        raise InstanceError(f"{name} repeats a literal position")
    if expected_size is not None and len(result) != expected_size:
        raise InstanceError(f"{name} must have size {expected_size}")
    if any(i < 0 or i >= Y_SIZE for i in result):
        raise InstanceError(f"{name} contains an index outside 0..{Y_SIZE - 1}")
    return result


def is_rho_atom_two(values: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    first, second = values
    return first != ZERO2 and second != ZERO2 and add(first, second) == ZERO2


@dataclass(frozen=True)
class SliceInstance:
    x_height: int
    y: tuple[tuple[int, int, int, int], ...]
    t: frozenset[int]
    u: frozenset[int]
    endpoints: tuple[frozenset[int], ...]
    four_edges: tuple[tuple[int, int], ...]
    common_nonaxial_position: int
    l_set: frozenset[int]
    r_set: frozenset[int]
    p_atom: frozenset[int]
    k_set: frozenset[int]

    @property
    def x(self) -> tuple[int, int, int, int]:
        return 1, 0, 0, self.x_height

    def qsum(self, indices: Iterable[int]) -> tuple[int, int, int]:
        return vector_sum((self.y[i][:3] for i in indices), 3)

    def asum(self, indices: Iterable[int]) -> tuple[int, int, int, int]:
        return vector_sum((self.y[i] for i in indices), 4)

    def rhosum(self, indices: Iterable[int]) -> tuple[int, int]:
        return vector_sum((rho(self.y[i]) for i in indices), 2)

    def height(self, indices: Iterable[int]) -> int:
        return sum(self.y[i][3] for i in indices) % P

    def q_h(self, endpoint_index: int) -> frozenset[int]:
        return self.k_set | (self.l_set - self.endpoints[endpoint_index])


def parse_instance(path: Path) -> SliceInstance:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise InstanceError(f"schema must equal {SCHEMA!r}")
    if data.get("p") != P or data.get("unique_type") != [ELL, B]:
        raise InstanceError("the frozen slice requires p=233 and unique_type=[7,4]")
    if data.get("packing_type") != "(3)":
        raise InstanceError("packing_type must be '(3)'")
    if data.get("P_size") != PACKING_SIZE or data.get("kappa") != KAPPA:
        raise InstanceError("the frozen slice requires P_size=2 and kappa=1")
    if data.get("endpoint_length_stage") != ENDPOINT_STAGE:
        raise InstanceError(
            "v1 freezes endpoint_length_stage='length_7_only'; length eight belongs to a later schema"
        )

    x_height = int(data["x_height"]) % P
    raw_y = data.get("Y")
    if not isinstance(raw_y, list) or len(raw_y) != Y_SIZE:
        raise InstanceError(f"Y must contain exactly {Y_SIZE} literal positions")
    y: list[tuple[int, int, int, int]] = []
    for index, raw_value in enumerate(raw_y):
        if not isinstance(raw_value, list) or len(raw_value) != 4:
            raise InstanceError(f"Y[{index}] must have four coordinates")
        y.append(tuple(int(entry) % P for entry in raw_value))
    y_tuple = tuple(y)

    t_set = checked_index_set(data.get("T"), "T")
    if len(t_set) not in (6, 7, 8):
        raise InstanceError("T must have length 6, 7, or 8")
    u_set = checked_index_set(data.get("U"), "U", expected_size=TAIL_SIZE)

    raw_endpoints = data.get("endpoints")
    if not isinstance(raw_endpoints, list):
        raise InstanceError("endpoints must be a JSON list")
    endpoints = tuple(
        checked_index_set(row, f"endpoints[{index}]", expected_size=7)
        for index, row in enumerate(raw_endpoints)
    )
    if not 4 <= len(endpoints) <= 6:
        raise InstanceError("the all-distinct-trace four-edge branch has 4..6 endpoints")
    if len(set(endpoints)) != len(endpoints):
        raise InstanceError("endpoints must be distinct literal blocks")

    raw_edges = data.get("four_edges")
    if not isinstance(raw_edges, list) or len(raw_edges) != 4:
        raise InstanceError("four_edges must contain exactly four endpoint pairs")
    edges: list[tuple[int, int]] = []
    for index, raw_edge in enumerate(raw_edges):
        if (
            not isinstance(raw_edge, list)
            or len(raw_edge) != 2
            or any(not isinstance(i, int) for i in raw_edge)
        ):
            raise InstanceError(f"four_edges[{index}] must be a pair of endpoint indices")
        left, right = sorted(raw_edge)
        if left == right or left < 0 or right >= len(endpoints):
            raise InstanceError(f"four_edges[{index}] is not a valid simple edge")
        edges.append((left, right))
    if len(set(edges)) != 4:
        raise InstanceError("four_edges must be four distinct simple edges")
    if {vertex for edge in edges for vertex in edge} != set(range(len(endpoints))):
        raise InstanceError("endpoints must be exactly the vertices used by four_edges")

    witness = int(data.get("common_nonaxial_position"))
    if witness < 0 or witness >= Y_SIZE or witness in u_set:
        raise InstanceError("common_nonaxial_position must lie in Y\\U")

    l_declared = checked_index_set(data.get("L"), "L")
    l_derived = u_set | frozenset().union(*endpoints)
    if l_declared != l_derived:
        raise InstanceError("L must be the literal union of U and every selected endpoint")
    universe = frozenset(range(Y_SIZE))
    r_declared = checked_index_set(data.get("R"), "R")
    if r_declared != universe - l_derived:
        raise InstanceError("R must be the literal complement Y\\L")
    p_atom = checked_index_set(data.get("P"), "P", expected_size=PACKING_SIZE)
    k_set = checked_index_set(data.get("K"), "K")
    if not p_atom <= r_declared or k_set != r_declared - p_atom:
        raise InstanceError("the single P and K must literally partition R")
    if not k_set:
        raise InstanceError("the surviving forced type (3) requires the common kernel K to be nonempty")

    instance = SliceInstance(
        x_height=x_height,
        y=y_tuple,
        t=t_set,
        u=u_set,
        endpoints=endpoints,
        four_edges=tuple(edges),
        common_nonaxial_position=witness,
        l_set=l_derived,
        r_set=r_declared,
        p_atom=p_atom,
        k_set=k_set,
    )
    validate_static_constraints(instance)
    return instance


def validate_static_constraints(instance: SliceInstance) -> None:
    """Check all polynomial-time equalities and literal incidence constraints."""
    if instance.qsum(range(Y_SIZE)) != (4, 0, 0):
        raise InstanceError("sum(Y) in C_p^3 must be 4q")
    if instance.height(range(Y_SIZE)) != 4 * instance.x_height % P:
        raise InstanceError("the height sum of Y must be 4*h_x")
    if instance.qsum(instance.u) != ((-B) % P, 0, 0):
        raise InstanceError("the unique tail U must have quotient sum -4q")
    if instance.height(instance.u) != (3 - B * instance.x_height) % P:
        raise InstanceError("the unique tail U has the wrong actual-axis sum")

    if instance.qsum(instance.t) != ZERO3 or instance.height(instance.t) != 3:
        raise InstanceError("T must be a zero-core F3 block")
    if not instance.t & instance.u or instance.t & instance.u == instance.u:
        raise InstanceError("T must have a nonempty proper trace on U")

    u_ordered = tuple(sorted(instance.u))
    traces = tuple(trace_mask(endpoint, u_ordered) for endpoint in instance.endpoints)
    if any(trace in (0, 7) for trace in traces) or len(set(traces)) != len(traces):
        raise InstanceError("endpoint traces on U must be nonempty, proper, and all distinct")
    if not {1, 2, 4}.issubset(traces):
        raise InstanceError(
            "the injective four-edge trace graph must contain all three singleton traces"
        )
    if not rank_two(rho(instance.y[position]) for position in u_ordered):
        raise InstanceError(
            "the all-length-seven singleton-tail sub-slice requires rank rho(U)=2"
        )
    for index, endpoint in enumerate(instance.endpoints):
        if instance.qsum(endpoint) != ZERO3 or instance.height(endpoint) != 3:
            raise InstanceError(f"endpoint {index} is not a length-seven zero-core F3 block")
        if instance.common_nonaxial_position not in endpoint:
            raise InstanceError(f"endpoint {index} misses the common four-edge witness")
        q_h = instance.q_h(index)
        if len(q_h) != 2 * P - 1:
            raise InstanceError(f"Q_H for endpoint {index} must have length 2p-1")
        if instance.rhosum(q_h) != ZERO2 or instance.qsum(q_h) != Q:
            raise InstanceError(f"Q_H for endpoint {index} must have quotient sum q")

    if rho(instance.y[instance.common_nonaxial_position]) == ZERO2:
        raise InstanceError("the common four-edge witness must be nonaxial")
    for left, right in instance.four_edges:
        if traces[left] & traces[right]:
            raise InstanceError("each four-edge pair must have disjoint tail traces")
        intersection = instance.endpoints[left] & instance.endpoints[right]
        if instance.common_nonaxial_position not in intersection:
            raise InstanceError("the common witness must lie in every edge intersection")
        if instance.rhosum(intersection) == ZERO2:
            raise InstanceError("each selected edge intersection must have nonzero rho-sum")

    p_values = tuple(rho(instance.y[index]) for index in sorted(instance.p_atom))
    if not is_rho_atom_two(p_values):
        raise InstanceError("P must be a two-position rho-atom")
    if instance.qsum(instance.p_atom) != (PACKING_COEFFICIENT, 0, 0):
        raise InstanceError("P must have quotient sum 3q")
    expected_p_height = (3 * instance.x_height - KAPPA) % P
    if instance.height(instance.p_atom) != expected_p_height:
        raise InstanceError("P must have actual sum 3x-a (kappa=1)")

    # C=X_1 dot_union U dot_union P is the automatic six-term F2 block.
    c_quotient = add(Q, add(instance.qsum(instance.u), instance.qsum(instance.p_atom)))
    c_height = (
        instance.x_height + instance.height(instance.u) + instance.height(instance.p_atom)
    ) % P
    if c_quotient != ZERO3 or c_height != 2:
        raise InstanceError("the automatic X_1+U+P block is not a six-term F2 block")

    # The actual value multiplicity includes all p-4 distinguished X copies.
    multiplicities = Counter(instance.y)
    multiplicities[instance.x] += X_MULTIPLICITY
    if max(multiplicities.values(), default=0) > X_MULTIPLICITY:
        raise InstanceError("an actual C_p^4 label has multiplicity greater than p-4")
    for index, value in enumerate(instance.y):
        if index not in instance.t and value[:3] == Q:
            raise InstanceError("a quotient-q position occurs outside the fixed T block")


def block_data(instance: SliceInstance, block: object) -> tuple[int, frozenset[int], int, int]:
    if not isinstance(block, dict):
        raise InstanceError("a block witness must be a JSON object")
    core = int(block.get("core_count"))
    tail = checked_index_set(block.get("tail"), "block.tail")
    if not 0 <= core <= X_MULTIPLICITY:
        raise InstanceError("block.core_count lies outside 0..p-4")
    quotient = add((core, 0, 0), instance.qsum(tail))
    if quotient != ZERO3:
        raise InstanceError("the supplied block is not quotient-zero")
    length = core + len(tail)
    family = (core * instance.x_height + instance.height(tail)) % P
    return core, tail, length, family


def is_f3(block: tuple[int, frozenset[int], int, int]) -> bool:
    return block[2] in LENGTH_FAMILIES and block[3] == 3 and 3 in LENGTH_FAMILIES[block[2]]


def is_induced_short(block: tuple[int, frozenset[int], int, int]) -> bool:
    """Whether a quotient-zero block belongs to the permitted short spectrum."""
    return block[2] in LENGTH_FAMILIES and block[3] in LENGTH_FAMILIES[block[2]]


def is_f2(block: tuple[int, frozenset[int], int, int]) -> bool:
    return is_induced_short(block) and block[3] == 2


def forbidden_disjoint_short_pair(
    left: tuple[int, frozenset[int], int, int],
    right: tuple[int, frozenset[int], int, int],
) -> bool:
    """Classify a disjoint pair after both blocks have been reconstructed.

    The F3--short and F2--F2 intersection theorems apply only to genuine
    induced short blocks.  Independently, a disjoint union of two short
    quotient-zero blocks is forbidden whenever its length lies in the full
    9..2p+2 quotient gap.
    """
    if not is_induced_short(left) or not is_induced_short(right):
        return False
    return (
        is_f3(left)
        or is_f3(right)
        or (is_f2(left) and is_f2(right))
        or 9 <= left[2] + right[2] <= 2 * P + 2
    )


def audit_short_intersection_classifier() -> int:
    """Regression rows for the exact domain and the full-gap pair rule."""
    rows = (
        # An F3 block and a non-short full complement are not an intersection witness.
        (
            (0, frozenset(range(7)), 7, 3),
            (P - 4, frozenset(range(7, Y_SIZE)), 3 * P - 3, P - 3),
            False,
        ),
        # Two genuine short blocks whose disjoint union has length nine are forbidden.
        ((0, frozenset(range(5)), 5, 1), (0, frozenset(range(5, 9)), 4, 2), True),
        # The ordinary F3--short intersection theorem is active below length nine too.
        ((0, frozenset(range(6)), 6, 3), (0, frozenset(range(6, 8)), 2, 1), True),
        # The F2 family is pairwise intersecting even below the full gap.
        ((0, frozenset(range(4)), 4, 2), (0, frozenset(range(4, 8)), 4, 2), True),
        # No named intersection theorem covers two F1 blocks with union length eight.
        ((0, frozenset(range(5)), 5, 1), (0, frozenset(range(5, 8)), 3, 1), False),
    )
    for left, right, expected in rows:
        assert forbidden_disjoint_short_pair(left, right) is expected
    return len(rows)


def validate_zero_subset(
    instance: SliceInstance,
    allowed_y: frozenset[int],
    core_capacity: int,
    raw: object,
    *,
    quotient_only: bool,
) -> tuple[int, frozenset[int]]:
    if not isinstance(raw, dict):
        raise InstanceError("zero-subset witness must be a JSON object")
    core = int(raw.get("x_count"))
    y_subset = checked_index_set(raw.get("Y_subset"), "zero_subset.Y_subset")
    if not 0 <= core <= core_capacity or not y_subset <= allowed_y:
        raise InstanceError("zero-subset witness is outside the stated complement")
    total_size = core + len(y_subset)
    full_size = core_capacity + len(allowed_y)
    if total_size in (0, full_size):
        raise InstanceError("zero-subset witness must be nonempty and proper")
    if add((core, 0, 0), instance.qsum(y_subset)) != ZERO3:
        raise InstanceError("zero-subset witness does not have quotient sum zero")
    if not quotient_only:
        total = add(scalar(core, instance.x), instance.asum(y_subset))
        if total != (0, 0, 0, 0):
            raise InstanceError("zero-subset witness does not have actual sum zero")
    return core, y_subset


def validate_violation_witness(instance: SliceInstance, witness_path: Path) -> dict[str, object]:
    """Recheck a concrete counterexample returned by a separation oracle.

    Aggregate Hasse residuals require a complete short-star certificate and are
    intentionally not accepted as one-line witnesses by this v1 checker.
    """
    witness = json.loads(witness_path.read_text(encoding="utf-8"))
    oracle = witness.get("oracle")

    if oracle == "short_spectrum":
        block = block_data(instance, witness.get("block"))
        _, _, length, family = block
        bad = length == 1 or (
            2 <= length <= 8
            and (length not in LENGTH_FAMILIES or family not in LENGTH_FAMILIES[length])
        )
        if not bad:
            raise InstanceError("the supplied short_spectrum block is not a violation")
    elif oracle == "middle_gap":
        block = block_data(instance, witness.get("block"))
        if not 9 <= block[2] <= 2 * P + 2:
            raise InstanceError("the supplied block is outside the forbidden middle gap")
    elif oracle == "unique_positive_f3_tail":
        block = block_data(instance, witness.get("block"))
        violation_type = witness.get("violation_type")
        if violation_type == "positive_core_wrong_tail":
            if not is_f3(block) or block[0] == 0:
                raise InstanceError("the supplied block is not a positive-core F3 block")
            if block[0] == B and block[1] == instance.u:
                raise InstanceError("the supplied block is the permitted unique tail")
        elif violation_type == "F3_misses_U":
            if not is_f3(block) or block[1] & instance.u:
                raise InstanceError("the supplied F3 block does not miss U")
        else:
            raise InstanceError("unique_positive_f3_tail needs a recognized violation_type")
    elif oracle == "K_rho_zero_free":
        subset = checked_index_set(witness.get("subset"), "subset")
        if not subset or not subset <= instance.k_set or instance.rhosum(subset) != ZERO2:
            raise InstanceError("the supplied subset does not violate rho-zero-freeness of K")
    elif oracle == "Q_H_rho_atom":
        endpoint_index = int(witness.get("endpoint_index"))
        if not 0 <= endpoint_index < len(instance.endpoints):
            raise InstanceError("invalid endpoint_index")
        q_h = instance.q_h(endpoint_index)
        subset = checked_index_set(witness.get("subset"), "subset")
        if not subset or subset == q_h or not subset <= q_h or instance.rhosum(subset) != ZERO2:
            raise InstanceError("the supplied subset does not violate Q_H rho-atomicity")
    elif oracle == "mixed_P_Q_target":
        endpoint_index = int(witness.get("endpoint_index"))
        if not 0 <= endpoint_index < len(instance.endpoints):
            raise InstanceError("invalid endpoint_index")
        a_set = checked_index_set(witness.get("P_subset"), "P_subset")
        t_set = checked_index_set(witness.get("Q_subset"), "Q_subset")
        q_h = instance.q_h(endpoint_index)
        if not a_set or a_set == instance.p_atom or not a_set <= instance.p_atom:
            raise InstanceError("P_subset must be a nonempty proper subset of P")
        if not t_set <= q_h or add(instance.rhosum(a_set), instance.rhosum(t_set)) != ZERO2:
            raise InstanceError("the supplied mixed subsets do not cancel in rho")
        total = add(instance.qsum(a_set), instance.qsum(t_set))
        if total in ((1, 0, 0), (2, 0, 0), (3, 0, 0)):
            raise InstanceError("the mixed target lies in the allowed axial set")
    elif oracle == "all_F3_complement_internal_sums":
        block = block_data(instance, witness.get("F3_block"))
        if not is_f3(block):
            raise InstanceError("F3_block is not an induced F3 block")
        core, tail, _, _ = block
        validate_zero_subset(
            instance,
            frozenset(range(Y_SIZE)) - tail,
            X_MULTIPLICITY - core,
            witness.get("internal_subset"),
            quotient_only=True,
        )
    elif oracle == "six_F2_extreme_complement_internal_sums":
        allowed = frozenset(range(Y_SIZE)) - instance.u - instance.p_atom
        validate_zero_subset(
            instance,
            allowed,
            X_MULTIPLICITY - 1,
            witness.get("internal_subset"),
            quotient_only=True,
        )
    elif oracle == "Z_actual_atom":
        validate_zero_subset(
            instance,
            frozenset(range(Y_SIZE)),
            X_MULTIPLICITY,
            witness.get("internal_subset"),
            quotient_only=False,
        )
    elif oracle == "short_intersection_network":
        left = block_data(instance, witness.get("left"))
        right = block_data(instance, witness.get("right"))
        violation_type = witness.get("violation_type")
        if violation_type == "forbidden_disjoint_pair":
            disjoint_possible = (
                not left[1] & right[1]
                and left[0] + right[0] <= X_MULTIPLICITY
            )
            forbidden = forbidden_disjoint_short_pair(left, right)
            if not disjoint_possible or not forbidden:
                raise InstanceError("the two blocks do not witness a forbidden disjoint pair")
        elif violation_type == "F3_zero_intersection":
            if (
                not is_f3(left)
                or not is_f3(right)
                or (left[0], left[1]) == (right[0], right[1])
            ):
                raise InstanceError("two distinct induced F3 blocks are required")
            core_intersection = int(witness.get("core_intersection"))
            lower = max(0, left[0] + right[0] - X_MULTIPLICITY)
            upper = min(left[0], right[0])
            if not lower <= core_intersection <= upper:
                raise InstanceError("core_intersection is not positionwise feasible")
            total = add(
                (core_intersection, 0, 0),
                instance.qsum(left[1] & right[1]),
            )
            if total != ZERO3:
                raise InstanceError("the supplied F3 intersection is not quotient-zero")
        else:
            raise InstanceError("short_intersection_network needs a recognized violation_type")
    else:
        raise InstanceError(
            "unknown or non-locally-checkable oracle witness; Hasse requires a complete star certificate"
        )

    return {
        "status": "VERIFIED_VIOLATION",
        "oracle": oracle,
        "candidate_ruled_out": True,
        "scope": "the supplied literal p=233 slice instance only",
    }


def has_nonempty_zero_subset(values: tuple[tuple[int, ...], ...], prime: int) -> bool:
    if not values:
        return False
    zero = (0,) * len(values[0])
    reachable = {zero}
    for value in values:
        translated = {add(total, value, prime) for total in reachable}
        if zero in translated:
            return True
        reachable |= translated
    return False


def compressed_axial_atom(prime: int, core_copies: int, remainder: tuple[tuple[int, ...], ...]) -> bool:
    """Exact atom test for q^core_copies plus a small literal remainder."""
    q = (1,) + (0,) * (len(remainder[0]) - 1)
    whole = (q,) * core_copies + remainder
    if vector_sum(whole, len(q), prime) != (0,) * len(q):
        return False
    reachable: dict[tuple[int, ...], int] = {(0,) * len(q): 1}
    for value in remainder:
        updated = dict(reachable)
        for total, sizes in reachable.items():
            target = add(total, value, prime)
            updated[target] = updated.get(target, 0) | (sizes << 1)
        reachable = updated
    for coefficient in range(prime):
        target = ((-coefficient) % prime,) + (0,) * (len(q) - 1)
        sizes = reachable.get(target, 0)
        for remainder_size in range(len(remainder) + 1):
            if not (sizes >> remainder_size & 1):
                continue
            for x_count in range(core_copies + 1):
                total_size = x_count + remainder_size
                if total_size in (0, len(whole)):
                    continue
                if x_count % prime == coefficient:
                    return False
    return True


def brute_atom(values: tuple[tuple[int, ...], ...], prime: int) -> bool:
    if not values or vector_sum(values, len(values[0]), prime) != (0,) * len(values[0]):
        return False
    for mask in range(1, (1 << len(values)) - 1):
        subset = tuple(values[index] for index in range(len(values)) if mask >> index & 1)
        if vector_sum(subset, len(values[0]), prime) == (0,) * len(values[0]):
            return False
    return True


def audit_small_axial_oracle() -> int:
    """Compare the compressed all-subset quantifier with literal brute force."""
    checked = 0
    prime = 5
    q = (1, 0, 0)
    for core_copies in range(1, 4):
        for seed in range(16):
            prefix = tuple(
                (
                    (seed + 2 * index + 1) % prime,
                    (seed * (index + 1) + 2) % prime,
                    (seed + index * index + 1) % prime,
                )
                for index in range(3)
            )
            target = scalar(-core_copies, q, prime)
            last = add(target, neg(vector_sum(prefix, 3, prime), prime), prime)
            remainder = prefix + (last,)
            assert compressed_axial_atom(prime, core_copies, remainder) == brute_atom(
                (q,) * core_copies + remainder, prime
            )
            checked += 1
    return checked


def hasse_row_counts() -> dict[str, int]:
    point_keys = 1 + Y_SIZE
    pair_keys = 1 + Y_SIZE + comb(Y_SIZE, 2)
    triple_keys = 1 + Y_SIZE + comb(Y_SIZE, 2) + comb(Y_SIZE, 3)
    return {
        "zero_order_congruences": 3,
        "point_keys": point_keys,
        "point_congruences": 3 * point_keys,
        "pair_keys": pair_keys,
        "pair_congruences": 2 * pair_keys,
        "triple_keys": triple_keys,
        "triple_congruences": triple_keys,
        "total_congruences": 3 + 3 * point_keys + 2 * pair_keys + triple_keys,
    }


def oracle_registry() -> list[dict[str, object]]:
    """Frozen universal quantifiers for a future exact CEGAR coordinator."""
    return [
        {
            "id": "K_rho_zero_free",
            "kind": "existential_counterexample",
            "quantifier": "every nonempty literal subset S of K has rho(sum S) != 0",
            "violation_witness": ["subset"],
        },
        {
            "id": "Q_H_rho_atom",
            "kind": "existential_counterexample",
            "quantifier": "for every selected endpoint H, no nonempty proper literal subset of Q_H=K union (L\\H) is rho-zero",
            "violation_witness": ["endpoint_index", "subset"],
        },
        {
            "id": "mixed_P_Q_target",
            "kind": "existential_counterexample",
            "quantifier": "for each H and every nonempty proper A subset P, every T subset Q_H with rho(T)=-rho(A) has quotient sum(A union T) in {q,2q,3q}",
            "independent_P_complement_orbits": 1,
            "violation_witness": ["endpoint_index", "P_subset", "Q_subset"],
        },
        {
            "id": "short_spectrum",
            "kind": "existential_counterexample",
            "quantifier": "all c in 0..p-4 and all literal S subset Y with 1<=c+|S|<=8 and cq+sum(S)=0 obey the complete F1/F2/F3 length window",
            "violation_witness": ["block"],
        },
        {
            "id": "middle_gap",
            "kind": "existential_counterexample",
            "quantifier": "there is no literal quotient-zero X_c union S of total length 9..2p+2",
            "violation_witness": ["block"],
        },
        {
            "id": "unique_positive_f3_tail",
            "kind": "existential_counterexample",
            "quantifier": "every automatically induced positive-core F3 block is exactly X_4 union U, and every F3 tail meets U",
            "violation_witness": ["violation_type", "block"],
        },
        {
            "id": "short_intersection_network",
            "kind": "existential_counterexample",
            "quantifier": "both sides of a pair witness are induced allowed short blocks; all induced F3 blocks meet every induced short block, induced F2 blocks meet one another, disjoint short unions of length 9..2p+2 are forbidden, and distinct F3 intersections are nonzero in the quotient",
            "violation_witness": [
                "violation_type",
                "left",
                "right",
                "optional core_intersection",
            ],
        },
        {
            "id": "all_F3_complement_internal_sums",
            "kind": "existential_counterexample",
            "quantifier": "for every automatically induced F3 block, every nonempty proper literal subset of its X/Y complement has nonzero C_p^3 quotient sum",
            "violation_witness": ["F3_block", "internal_subset"],
        },
        {
            "id": "six_F2_extreme_complement_internal_sums",
            "kind": "existential_counterexample",
            "quantifier": "every nonempty proper literal subset of Z\\(X_1 union U union P) has nonzero C_p^3 quotient sum",
            "violation_witness": ["internal_subset"],
        },
        {
            "id": "Hasse_all_positions",
            "kind": "aggregate_exact",
            "quantifier": "the complete reconstructed short-star family satisfies all zero-, one-, two-, and three-position Hasse congruences, including fixed X positions",
            "row_counts": hasse_row_counts(),
            "clear_certificate_requirement": "complete short-star support/count certificate; an asserted residual is not self-authenticating",
        },
        {
            "id": "Z_actual_atom",
            "kind": "existential_counterexample",
            "quantifier": "no nonempty proper literal position subsequence of X^(p-4) union Y has actual C_p^4 sum zero",
            "violation_witness": ["internal_subset"],
        },
    ]


def dependency_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(HERE)).replace("\\", "/"): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in DEPENDENCY_PATHS
    }


def instance_schema_description() -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "fixed_scalars": {
            "p": P,
            "unique_type": [ELL, B],
            "packing_type": "(3)",
            "P_size": PACKING_SIZE,
            "kappa": KAPPA,
            "endpoint_length_stage": ENDPOINT_STAGE,
            "tail_projection_rank": 2,
            "Y_size": Y_SIZE,
            "X_multiplicity": X_MULTIPLICITY,
            "q": list(Q),
            "a": [0, 0, 0, 1],
        },
        "required_fields": [
            "schema",
            "p",
            "unique_type",
            "packing_type",
            "P_size",
            "kappa",
            "endpoint_length_stage",
            "x_height",
            "Y",
            "T",
            "U",
            "endpoints",
            "four_edges",
            "common_nonaxial_position",
            "L",
            "R",
            "P",
            "K",
        ],
        "literal_identity_rule": "every named block is a set of indices into the one shared 474-row Y array; no endpoint-local labels are accepted",
        "derived_sets": {
            "L": "U union all selected endpoints",
            "R": "Y\\L",
            "K": "R\\P",
            "Q_H": "K union (L\\H) = Y\\(H union P)",
            "automatic_six_F2": "X_1 union U union P",
        },
        "incidence_boundary": "no concrete upstream endpoint incidence is bundled with this file",
        "T_relation": (
            "T is a fixed zero-core F3 block on the shared Y positions; it may or may not equal a selected four-edge endpoint. "
            "L is defined only from U and the selected four-edge endpoints, so no unstated T-incidence assumption is made"
        ),
        "excluded_template": (
            "the historical distinct-doubleton cover witness has K empty and is not an admissible template for this K-nonempty type-(3) slice"
        ),
        "certified_dependency": {
            "name": "unique_tail_p233_singleton_tail_fringe",
            "review_status": "CORRECT",
            "independent_review_sha256": "8487137667255b49f74ce8a0fe79c2d12222e45d54776eb5c8458bce00aed5d1",
            "used_consequence": (
                "three all-length-seven singleton-trace endpoints exclude tail projection rank one"
            ),
        },
    }


def build_report(instance: SliceInstance | None = None) -> dict[str, object]:
    audit_count = audit_small_axial_oracle()
    assert audit_count == 48
    intersection_audit_count = audit_short_intersection_classifier()
    assert intersection_audit_count == 5
    registry = oracle_registry()
    assert len(registry) == 11
    assert hasse_row_counts()["total_congruences"] == 17976380
    assert 2 ** (PACKING_SIZE - 1) - 1 == 1

    if instance is None:
        status = "INSTANCE_SCHEMA/CEGAR_ORACLES_UNINSTANTIATED/GLOBAL_INCOMPLETE"
        instance_summary: dict[str, object] = {
            "loaded": False,
            "reason": "no concrete all-distinct-trace endpoint incidence and no 474-position label assignment were supplied",
        }
    else:
        status = "RELAXED_STATIC_INSTANCE_ONLY/EXACT_ORACLES_PENDING/GLOBAL_INCOMPLETE"
        instance_summary = {
            "loaded": True,
            "static_constraints": "PASS",
            "endpoint_count": len(instance.endpoints),
            "L_size": len(instance.l_set),
            "R_size": len(instance.r_set),
            "K_size": len(instance.k_set),
            "Q_H_sizes": [len(instance.q_h(i)) for i in range(len(instance.endpoints))],
            "pending_exact_oracles": [row["id"] for row in registry],
        }

    report: dict[str, object] = {
        "schema": "unique_tail_p233_type3_p2_exact_slice_report_v1",
        "slice": instance_schema_description()["fixed_scalars"],
        "instance_schema": instance_schema_description(),
        "dependencies_sha256": dependency_hashes(),
        "static_equalities_restored": [
            "all 474 literal C_p^4 labels are shared by T,U,L,R,P,K and every endpoint",
            "sum(Y)=4x, sum(U)=3a-4x, sum(H)=3a, sum(P)=3x-a",
            "P is a two-position rho-atom, L and R are literal complements, and K=R\\P",
            "each length-seven endpoint gives |Q_H|=2p-1 and quotient sum q",
            "X_1 union U union P is the automatic length-six F2 block",
            "four distinct trace-disjoint edges share one literal nonaxial position and all endpoint traces are distinct",
            "the injective four-edge trace graph contains all three singleton traces and the all-length-seven slice has rank rho(U)=2",
        ],
        "exact_separation_oracles": registry,
        "clear_semantics": {
            "candidate_status_if_every_oracle_is_exact_CLEAR": "VERIFIED_INTERFACE_SURVIVOR",
            "certified_rank_two_precondition": (
                "unique_tail_p233_singleton_tail_fringe was independently rederived and reviewed CORRECT; the all-length-seven slice therefore has tail projection rank two"
            ),
            "meaning": "survives this fixed local p=233 slice only; it is not an A_p counterexample and not a global SAT claim",
            "unsat_semantics": "UNSAT is permitted only after all incidence choices admitted by a separately frozen exhaustive incidence generator are eliminated with checkable certificates",
            "current_unsat_claim": False,
        },
        "small_exact_audit": {
            "compressed_axial_atom_vs_literal_subsets": audit_count,
            "short_intersection_classifier_regression_rows": intersection_audit_count,
            "P_mixed_target_complement_orbit_count": 1,
            "Hasse_row_arithmetic": hasse_row_counts(),
        },
        "instance": instance_summary,
        "status": status,
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path)
    parser.add_argument("--violation", type=Path)
    parser.add_argument(
        "--no-write-report",
        action="store_true",
        help="print the report without refreshing the canonical report file",
    )
    args = parser.parse_args()
    if args.violation and not args.instance:
        parser.error("--violation requires --instance")

    instance = parse_instance(args.instance) if args.instance else None
    if args.violation:
        assert instance is not None
        print(
            json.dumps(
                validate_violation_witness(instance, args.violation),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return

    report = build_report(instance)
    if not args.no_write_report:
        REPORT_PATH.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
