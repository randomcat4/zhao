#!/usr/bin/env python3
r"""Exact finite audit for the cover-pair forbidden-block generalisation.

Scope
-----
This program works only at the labelled endpoint-incidence interface of the
three forced common-R packing types (3), (1,2), and (1,1,1).  If an axial
pair of distinct doubleton traces covers L, then K is empty and every
Q_H=L\H has the same quotient label q and is a projected atom.

The program verifies four finite claims used by the companion proof.

1. It exhausts the 26 nonzero unit-coefficient forms
   alpha Q_E + beta Q_F + gamma U, alpha,beta,gamma in {-1,0,1}, against
   all set incidences on a three-point U and four outside test positions.
2. It checks the exact indicator criterion for the more general form
   sum_{E in S} Q_E - m U.
3. It re-enumerates the 28,584 trace colourings of the eleven four-edge
   endpoint graphs and all 24,468 distinct-doubleton cover-pair occurrences.
4. For every such occurrence and for p=233,1399, it constructs and checks a
   labelled incidence/trace/size skeleton which avoids every large-core form
   in item 2.  These are incidence skeletons, not quotient-label assignments
   and not candidates for A_p.

No relaxed SAT survivor is reported as a counterexample, and no local UNSAT
is promoted beyond the explicitly checked interface.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import argparse
import hashlib
import json
from math import comb
from pathlib import Path


SHAPES: dict[str, tuple[int, tuple[tuple[int, int], ...]]] = {
    "P5": (5, ((0, 1), (1, 2), (2, 3), (3, 4))),
    "K1_4": (5, ((0, 1), (0, 2), (0, 3), (0, 4))),
    "T5": (5, ((0, 1), (0, 2), (0, 3), (1, 4))),
    "C4": (4, ((0, 1), (1, 2), (2, 3), (3, 0))),
    "paw": (4, ((0, 1), (1, 2), (2, 0), (0, 3))),
    "P4_plus_K2": (6, ((0, 1), (1, 2), (2, 3), (4, 5))),
    "K1_3_plus_K2": (6, ((0, 1), (0, 2), (0, 3), (4, 5))),
    "K3_plus_K2": (5, ((0, 1), (1, 2), (2, 0), (3, 4))),
    "two_P3": (6, ((0, 1), (1, 2), (3, 4), (4, 5))),
    "P3_plus_two_K2": (7, ((0, 1), (1, 2), (3, 4), (5, 6))),
    "four_K2": (8, ((0, 1), (2, 3), (4, 5), (6, 7))),
}

TRACE_MASKS = tuple(range(1, 7))
DOUBLETON_MASKS = frozenset((3, 5, 6))
PRIMES = (233, 1399)

EXPECTED_TRACE_TOTALS = {
    "valid_colourings": 28584,
    "colourings_with_cover_candidate": 13512,
    "cover_pair_occurrences": 24468,
}
EXPECTED_CERTIFICATE_SHA256 = (
    "36ed4fe5bbc17e2e7706bc06c02bfc11b85ee321eccd053fad1b77fd2c9e3c10"
)


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def popcount(mask: int) -> int:
    return mask.bit_count()


def is_trace_edge(left: int, right: int) -> bool:
    return not (left & right)


def is_indicator(coefficients: tuple[int, ...]) -> bool:
    return all(value in (0, 1) for value in coefficients)


def form_coefficients(
    universe_size: int,
    q_left: frozenset[int],
    q_right: frozenset[int],
    u_set: frozenset[int],
    alpha: int,
    beta: int,
    gamma: int,
) -> tuple[int, ...]:
    return tuple(
        alpha * (position in q_left)
        + beta * (position in q_right)
        + gamma * (position in u_set)
        for position in range(universe_size)
    )


def predicted_unit_indicator(
    q_left: frozenset[int],
    q_right: frozenset[int],
    u_set: frozenset[int],
    form: tuple[int, int, int],
) -> bool:
    """Set-theoretic classification of all nonzero unit forms.

    The hypotheses that both endpoint traces are nonempty proper subsets of
    U are enforced by the caller.  The difference rows are retained here as
    pure set identities; projected atomicity later rules them out for two
    distinct endpoints.
    """

    alpha, beta, gamma = form
    # Positions outside U that belong to neither Q do not affect any row;
    # the union of the two Q supports is therefore an exact local universe.
    outside = (q_left | q_right) - u_set

    if form in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        return True
    if form == (1, 1, 0):
        return not (q_left & q_right)
    if form == (1, -1, 0):
        return q_right <= q_left
    if form == (-1, 1, 0):
        return q_left <= q_right
    if form == (1, 1, -1):
        return u_set <= (q_left | q_right) and not (
            q_left & q_right & outside
        )
    if form == (-1, 0, 1):
        return q_left <= u_set
    if form == (0, -1, 1):
        return q_right <= u_set
    if form == (-1, -1, 1):
        return (q_left | q_right) <= u_set and not (q_left & q_right)
    if form == (1, -1, 1):
        return (q_right & outside) <= (q_left & outside) and (
            q_left & u_set
        ) <= (q_right & u_set)
    if form == (-1, 1, 1):
        return (q_left & outside) <= (q_right & outside) and (
            q_right & u_set
        ) <= (q_left & u_set)

    # Under nonempty proper endpoint traces, every remaining unit form has a
    # negative coefficient or a coefficient at least two on some U-position.
    assert (alpha, beta, gamma) != (0, 0, 0)
    return False


def audit_unit_pair_forms() -> dict[str, object]:
    """Exhaust the pair-form table independently of the symbolic proof."""

    # U={0,1,2}.  Position 3 is the common y in both endpoints; positions
    # 4,5,6 independently realise the other three outside Venn cells.
    u_set = frozenset((0, 1, 2))
    outside_optional = (4, 5, 6)
    forms = tuple(
        form
        for form in product((-1, 0, 1), repeat=3)
        if form != (0, 0, 0)
    )
    rows_checked = 0
    indicator_hits = Counter()
    large_core_u_admissible = {4: set(), 5: set()}

    for left_trace in TRACE_MASKS:
        for right_trace in TRACE_MASKS:
            for left_bits in range(1 << len(outside_optional)):
                for right_bits in range(1 << len(outside_optional)):
                    left_endpoint = {
                        bit for bit in range(3) if left_trace >> bit & 1
                    }
                    right_endpoint = {
                        bit for bit in range(3) if right_trace >> bit & 1
                    }
                    left_endpoint.add(3)
                    right_endpoint.add(3)
                    for index, position in enumerate(outside_optional):
                        if left_bits >> index & 1:
                            left_endpoint.add(position)
                        if right_bits >> index & 1:
                            right_endpoint.add(position)

                    universe = frozenset(range(7))
                    q_left = universe - frozenset(left_endpoint)
                    q_right = universe - frozenset(right_endpoint)
                    for form in forms:
                        direct = is_indicator(
                            form_coefficients(
                                7,
                                q_left,
                                q_right,
                                u_set,
                                *form,
                            )
                        )
                        predicted = predicted_unit_indicator(
                            q_left, q_right, u_set, form
                        )
                        assert direct == predicted, (
                            left_trace,
                            right_trace,
                            left_bits,
                            right_bits,
                            form,
                        )
                        rows_checked += 1
                        if direct:
                            indicator_hits[str(form)] += 1

                    # For a long X-core, t=alpha+beta-b*gamma must be at
                    # least four.  U-coefficients alone already show that
                    # only Q_E+Q_F-U can survive among unit pair forms.
                    for b_value in (4, 5):
                        for form in forms:
                            alpha, beta, gamma = form
                            t_value = alpha + beta - b_value * gamma
                            if t_value < 4:
                                continue
                            u_coefficients = tuple(
                                alpha * (position in q_left)
                                + beta * (position in q_right)
                                + gamma
                                for position in u_set
                            )
                            if is_indicator(u_coefficients):
                                large_core_u_admissible[b_value].add(form)

    assert large_core_u_admissible[4] == {(1, 1, -1)}
    assert large_core_u_admissible[5] == {(1, 1, -1)}
    return {
        "nonzero_unit_form_count": len(forms),
        "exhaustive_rows_checked": rows_checked,
        "indicator_hit_counts": dict(sorted(indicator_hits.items())),
        "large_core_u_admissible_forms": {
            str(b_value): [list(form) for form in sorted(forms_found)]
            for b_value, forms_found in sorted(large_core_u_admissible.items())
        },
    }


def dense_form_coefficients(
    selected_endpoints: tuple[frozenset[int], ...],
    universe_size: int,
    u_set: frozenset[int],
    m_value: int,
) -> tuple[int, ...]:
    return tuple(
        sum(position not in endpoint for endpoint in selected_endpoints)
        - m_value * (position in u_set)
        for position in range(universe_size)
    )


def dense_indicator_degree_criterion(
    selected_endpoints: tuple[frozenset[int], ...],
    universe_size: int,
    u_set: frozenset[int],
    m_value: int,
) -> bool:
    k_value = len(selected_endpoints)
    for position in range(universe_size):
        degree = sum(position in endpoint for endpoint in selected_endpoints)
        allowed = (
            {k_value - m_value - 1, k_value - m_value}
            if position in u_set
            else {k_value - 1, k_value}
        )
        if degree not in allowed:
            return False
    return True


def audit_dense_degree_criterion() -> int:
    """Finite independent regression of the arbitrary-k degree criterion."""

    # Four positions already realise every local degree 0,...,k.  This is a
    # regression of the coefficient identity, not the large cover audit.
    u_set = frozenset((0, 1))
    universe_size = 4
    endpoints = tuple(
        frozenset(position for position in range(universe_size) if mask >> position & 1)
        for mask in range(1 << universe_size)
    )
    checked = 0
    # Small exhaustive families already realise every per-position degree.
    for k_value in range(1, 5):
        for selected_indices in combinations(range(len(endpoints)), k_value):
            selected = tuple(endpoints[index] for index in selected_indices)
            for m_value in range(0, k_value + 1):
                direct = is_indicator(
                    dense_form_coefficients(
                        selected, universe_size, u_set, m_value
                    )
                )
                predicted = dense_indicator_degree_criterion(
                    selected, universe_size, u_set, m_value
                )
                assert direct == predicted
                checked += 1
    return checked


def candidate_cover_pairs(colouring: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left, right in combinations(range(len(colouring)), 2)
        if colouring[left] in DOUBLETON_MASKS
        and colouring[right] in DOUBLETON_MASKS
        and colouring[left] != colouring[right]
    )


def endpoint_target_size(p_value: int, trace: int) -> int:
    if p_value == 1399:
        # This also respects the strengthened no-old-flower branch in which
        # every singleton-trace endpoint has length eight.
        return 8
    assert p_value == 233
    # Length seven is allowed for both trace sizes and respects the
    # strengthened singleton-trace {7,8} branch.
    return 7


def unit_pair_has_determined_rejection(
    p_value: int,
    left_endpoint: frozenset[int],
    right_endpoint: frozenset[int],
    universe_size: int,
    u_set: frozenset[int],
) -> bool:
    """Use only full-sum equality, frozen length gaps, and F_3 uniqueness."""

    all_positions = frozenset(range(universe_size))
    q_left = all_positions - left_endpoint
    q_right = all_positions - right_endpoint
    b_value = 4 if p_value == 233 else 5
    for form in product((-1, 0, 1), repeat=3):
        if form == (0, 0, 0):
            continue
        coefficients = form_coefficients(
            universe_size, q_left, q_right, u_set, *form
        )
        if not is_indicator(coefficients):
            continue
        support = frozenset(
            position for position, coefficient in enumerate(coefficients) if coefficient
        )
        alpha, beta, gamma = form
        t_value = alpha + beta - b_value * gamma
        if t_value == 0:
            if support:
                return True
            continue
        core = (-(t_value % p_value)) % p_value
        if core > p_value - 4:
            continue
        total_length = core + len(support)
        if total_length == 1 or 9 <= total_length <= 2 * p_value + 2:
            return True
        if total_length == 8 and core > 0:
            if not (core == b_value and support == u_set):
                return True
    return False


def build_incidence_witness(
    p_value: int,
    colouring: tuple[int, ...],
    cover_pair: tuple[int, int],
) -> dict[str, object]:
    """Build a real-position incidence skeleton for one cover occurrence."""

    cover_left, cover_right = cover_pair
    left_trace = colouring[cover_left]
    right_trace = colouring[cover_right]
    assert left_trace in DOUBLETON_MASKS
    assert right_trace in DOUBLETON_MASKS
    assert left_trace != right_trace

    side_count = 3 if p_value == 233 else 4
    u_names = ("u1", "u2", "u3")
    y_name = "y"
    a_private = "a0"
    b_private = "b0"
    a_side = tuple(f"a{index}" for index in range(1, side_count + 1))
    b_side = tuple(f"b{index}" for index in range(1, side_count + 1))
    outside_names = (y_name, a_private, *a_side, b_private, *b_side)
    universe_names = (*u_names, *outside_names)
    name_to_index = {name: index for index, name in enumerate(universe_names)}
    u_set = frozenset(name_to_index[name] for name in u_names)
    outside_set = frozenset(name_to_index[name] for name in outside_names)

    def trace_positions(trace: int) -> set[int]:
        return {
            name_to_index[u_names[bit]] for bit in range(3) if trace >> bit & 1
        }

    endpoints: list[frozenset[int] | None] = [None] * len(colouring)
    endpoints[cover_left] = frozenset(
        trace_positions(left_trace)
        | {name_to_index[y_name], name_to_index[a_private]}
        | {name_to_index[name] for name in a_side}
    )
    endpoints[cover_right] = frozenset(
        trace_positions(right_trace)
        | {name_to_index[y_name], name_to_index[b_private]}
        | {name_to_index[name] for name in b_side}
    )

    a_u_mask = left_trace & ~right_trace
    b_u_mask = right_trace & ~left_trace
    assert popcount(a_u_mask) == popcount(b_u_mask) == 1
    a_region = {
        name_to_index[u_names[bit]] for bit in range(3) if a_u_mask >> bit & 1
    } | {name_to_index[a_private]} | {name_to_index[name] for name in a_side}
    b_region = {
        name_to_index[u_names[bit]] for bit in range(3) if b_u_mask >> bit & 1
    } | {name_to_index[b_private]} | {name_to_index[name] for name in b_side}
    c_region = (
        set(range(len(universe_names))) - a_region - b_region
    )

    # Repeated trace classes receive distinct outside subsets.  All third
    # endpoints omit a0,b0, which is the uniform obstruction to every large
    # dense-cover form.
    candidates_by_trace: dict[int, list[frozenset[int]]] = {}
    selectable_side = tuple(
        name_to_index[name] for name in (*a_side, *b_side)
    )
    for trace in TRACE_MASKS:
        target = endpoint_target_size(p_value, trace)
        outside_needed = target - popcount(trace)
        candidates = []
        for side_choice in combinations(selectable_side, outside_needed - 1):
            endpoint = frozenset(
                trace_positions(trace)
                | {name_to_index[y_name]}
                | set(side_choice)
            )
            if endpoint & a_region and endpoint & b_region and endpoint & c_region:
                candidates.append(endpoint)
        candidates_by_trace[trace] = sorted(candidates, key=lambda item: tuple(sorted(item)))

    third_vertices = tuple(
        vertex for vertex in range(len(colouring)) if vertex not in cover_pair
    )

    def assign_third(index: int) -> bool:
        if index == len(third_vertices):
            return True
        vertex = third_vertices[index]
        trace = colouring[vertex]
        for candidate in candidates_by_trace[trace]:
            if any(
                colouring[earlier] == trace and endpoints[earlier] == candidate
                for earlier in third_vertices[:index]
            ):
                continue
            if any(
                unit_pair_has_determined_rejection(
                    p_value,
                    candidate,
                    assigned,
                    len(universe_names),
                    u_set,
                )
                for assigned in endpoints
                if assigned is not None
            ):
                continue
            endpoints[vertex] = candidate
            if assign_third(index + 1):
                return True
            endpoints[vertex] = None
        return False

    assert assign_third(0), (p_value, colouring, cover_pair)

    actual_endpoints = tuple(endpoint for endpoint in endpoints if endpoint is not None)
    assert len(actual_endpoints) == len(colouring)
    assert len(set(actual_endpoints)) == len(actual_endpoints)
    left_endpoint = actual_endpoints[cover_left]
    right_endpoint = actual_endpoints[cover_right]
    assert left_endpoint | right_endpoint == frozenset(range(len(universe_names)))
    assert left_endpoint & right_endpoint == frozenset(
        trace_positions(left_trace & right_trace) | {name_to_index[y_name]}
    )

    for vertex, endpoint in enumerate(actual_endpoints):
        computed_trace = sum(
            1 << bit
            for bit, name in enumerate(u_names)
            if name_to_index[name] in endpoint
        )
        assert computed_trace == colouring[vertex]
        assert len(endpoint) == endpoint_target_size(p_value, colouring[vertex])
        assert name_to_index[y_name] in endpoint
        if vertex not in cover_pair:
            assert endpoint & a_region
            assert endpoint & b_region
            assert endpoint & c_region
            assert name_to_index[a_private] not in endpoint
            assert name_to_index[b_private] not in endpoint

    return {
        "universe_names": universe_names,
        "u_set": u_set,
        "outside_set": outside_set,
        "endpoints": actual_endpoints,
        "a_region": frozenset(a_region),
        "b_region": frozenset(b_region),
        "c_region": frozenset(c_region),
        "a_private": name_to_index[a_private],
        "b_private": name_to_index[b_private],
    }


def validate_incidence_witness(
    p_value: int,
    colouring: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
    cover_pair: tuple[int, int],
    witness: dict[str, object],
) -> dict[str, int]:
    endpoints = witness["endpoints"]
    assert isinstance(endpoints, tuple)
    u_set = witness["u_set"]
    outside_set = witness["outside_set"]
    assert isinstance(u_set, frozenset)
    assert isinstance(outside_set, frozenset)
    universe_size = len(witness["universe_names"])

    for left, right in edges:
        assert is_trace_edge(colouring[left], colouring[right])
        assert endpoints[left] & endpoints[right]

    b_value = 4 if p_value == 233 else 5
    all_positions = frozenset(range(universe_size))

    unit_forms_checked = 0
    unit_indicators = 0
    determined_unit_rejections = 0
    determined_rejection_examples = []
    forms = tuple(
        form
        for form in product((-1, 0, 1), repeat=3)
        if form != (0, 0, 0)
    )
    for left, right in combinations(range(len(endpoints)), 2):
        q_left = all_positions - endpoints[left]
        q_right = all_positions - endpoints[right]
        for form in forms:
            coefficients = form_coefficients(
                universe_size, q_left, q_right, u_set, *form
            )
            direct = is_indicator(coefficients)
            predicted = predicted_unit_indicator(q_left, q_right, u_set, form)
            assert direct == predicted
            unit_forms_checked += 1
            if not direct:
                continue
            unit_indicators += 1
            support = frozenset(
                position for position, coefficient in enumerate(coefficients) if coefficient
            )
            alpha, beta, gamma = form
            t_value = alpha + beta - b_value * gamma

            # The two difference forms have actual sum zero because all Q_H
            # have the same full actual sum S.  A nonempty indicator would
            # violate actual atomicity of Z; equal-cardinality endpoints in
            # this witness make such an indicator impossible already.
            if t_value == 0:
                if support:
                    determined_unit_rejections += 1
                    determined_rejection_examples.append(
                        (left, right, form, None, len(support))
                    )
                continue

            core = (-(t_value % p_value)) % p_value
            if core > p_value - 4:
                continue
            total_length = core + len(support)
            if total_length == 1 or 9 <= total_length <= 2 * p_value + 2:
                determined_unit_rejections += 1
                determined_rejection_examples.append(
                    (left, right, form, core, len(support), total_length)
                )
                continue
            if total_length == 8:
                # Length eight is necessarily F_3.  Its only positive-core
                # occurrence is the frozen pair (b,U).
                if core > 0 and not (core == b_value and support == u_set):
                    determined_unit_rejections += 1
                    determined_rejection_examples.append(
                        (left, right, form, core, len(support), total_length)
                    )

    assert determined_unit_rejections == 0, (
        p_value,
        colouring,
        cover_pair,
        determined_rejection_examples[:5],
    )

    pair_gate_checks = 0
    for left, right in combinations(range(len(endpoints)), 2):
        if not is_trace_edge(colouring[left], colouring[right]):
            continue
        q_left = frozenset(range(universe_size)) - endpoints[left]
        q_right = frozenset(range(universe_size)) - endpoints[right]
        pair_gate_checks += 1
        # Exact criterion for Q_E+Q_F-U to be an indicator.
        direct = is_indicator(
            form_coefficients(
                universe_size, q_left, q_right, u_set, 1, 1, -1
            )
        )
        predicted = not (colouring[left] & colouring[right]) and not (
            q_left & q_right & outside_set
        )
        assert direct == predicted
        assert not direct

    dense_forms_checked = 0
    dense_indicators = 0
    large_core_dense_indicators = 0
    cover_vertices = frozenset(cover_pair)
    third_vertices = tuple(
        vertex for vertex in range(len(endpoints)) if vertex not in cover_vertices
    )

    # Any selected family containing at least two third endpoints has
    # coefficient at least two at a0 (indeed also at b0), because every third
    # endpoint omits both private positions.  Count those forms exactly but do
    # not expand their full coefficient vectors.
    for third_count in range(2, len(third_vertices) + 1):
        for cover_count in range(0, 3):
            k_value = third_count + cover_count
            if k_value > len(endpoints):
                continue
            family_count = comb(len(third_vertices), third_count) * comb(2, cover_count)
            dense_forms_checked += family_count * (k_value + 1)

    # Only families using zero or one third endpoint need direct expansion.
    small_family_indices = []
    for cover_count in range(0, 3):
        for chosen_cover in combinations(tuple(cover_vertices), cover_count):
            if chosen_cover:
                small_family_indices.append(tuple(chosen_cover))
            for third in third_vertices:
                small_family_indices.append(tuple(chosen_cover) + (third,))

    for selected_indices in small_family_indices:
        k_value = len(selected_indices)
        selected = tuple(endpoints[index] for index in selected_indices)
        for m_value in range(0, k_value + 1):
            direct = is_indicator(
                dense_form_coefficients(
                    selected, universe_size, u_set, m_value
                )
            )
            predicted = dense_indicator_degree_criterion(
                selected, universe_size, u_set, m_value
            )
            assert direct == predicted
            dense_forms_checked += 1
            if not direct:
                continue
            dense_indicators += 1
            t_value = k_value + m_value * b_value
            if t_value >= 4:
                large_core_dense_indicators += 1

    assert large_core_dense_indicators == 0
    expected_dense_forms = sum(
        comb(len(endpoints), k_value) * (k_value + 1)
        for k_value in range(1, len(endpoints) + 1)
    )
    assert dense_forms_checked == expected_dense_forms
    return {
        "unit_forms_checked": unit_forms_checked,
        "unit_indicators": unit_indicators,
        "determined_unit_rejections": determined_unit_rejections,
        "pair_gate_checks": pair_gate_checks,
        "dense_forms_checked": dense_forms_checked,
        "dense_indicators": dense_indicators,
        "large_core_dense_indicators": large_core_dense_indicators,
    }


def enumerate_cover_occurrences() -> dict[str, object]:
    totals = Counter()
    per_shape: dict[str, dict[str, int]] = {}
    per_prime = {
        p_value: Counter() for p_value in PRIMES
    }
    example_witnesses: dict[str, object] = {}
    witness_cache: dict[
        tuple[int, int, int, tuple[int, ...]],
        tuple[tuple[int, ...], dict[str, object], dict[str, int]],
    ] = {}

    for shape_name, (vertex_count, edges) in SHAPES.items():
        local = Counter()
        for colouring in product(TRACE_MASKS, repeat=vertex_count):
            if not all(is_trace_edge(colouring[left], colouring[right]) for left, right in edges):
                continue
            local["valid_colourings"] += 1
            cover_pairs = candidate_cover_pairs(colouring)
            if cover_pairs:
                local["colourings_with_cover_candidate"] += 1
            local["cover_pair_occurrences"] += len(cover_pairs)

            for cover_pair in cover_pairs:
                for p_value in PRIMES:
                    left, right = cover_pair
                    other_traces = tuple(
                        sorted(
                            colouring[vertex]
                            for vertex in range(vertex_count)
                            if vertex not in cover_pair
                        )
                    )
                    cache_key = (
                        p_value,
                        colouring[left],
                        colouring[right],
                        other_traces,
                    )
                    if cache_key not in witness_cache:
                        canonical_colouring = (
                            colouring[left],
                            colouring[right],
                            *other_traces,
                        )
                        canonical_cover = (0, 1)
                        witness = build_incidence_witness(
                            p_value, canonical_colouring, canonical_cover
                        )
                        checked = validate_incidence_witness(
                            p_value,
                            canonical_colouring,
                            tuple(),
                            canonical_cover,
                            witness,
                        )
                        witness_cache[cache_key] = (
                            canonical_colouring,
                            witness,
                            checked,
                        )
                    canonical_colouring, witness, checked = witness_cache[cache_key]
                    per_prime[p_value]["cover_occurrences_checked"] += 1
                    per_prime[p_value]["incidence_survivors"] += 1
                    per_prime[p_value]["pair_gate_checks"] += checked["pair_gate_checks"]
                    per_prime[p_value]["unit_forms_checked"] += checked[
                        "unit_forms_checked"
                    ]
                    per_prime[p_value]["unit_indicators"] += checked[
                        "unit_indicators"
                    ]
                    per_prime[p_value]["determined_unit_rejections"] += checked[
                        "determined_unit_rejections"
                    ]
                    per_prime[p_value]["dense_forms_checked"] += checked["dense_forms_checked"]
                    per_prime[p_value]["dense_indicators"] += checked["dense_indicators"]
                    per_prime[p_value]["large_core_dense_indicators"] += checked[
                        "large_core_dense_indicators"
                    ]
                    key = str(p_value)
                    if key not in example_witnesses:
                        example_witnesses[key] = {
                            "shape": shape_name,
                            "canonical_colouring": list(canonical_colouring),
                            "canonical_cover_pair": [0, 1],
                            "universe_names": list(witness["universe_names"]),
                            "endpoint_positions": [
                                [witness["universe_names"][index] for index in sorted(endpoint)]
                                for endpoint in witness["endpoints"]
                            ],
                        }

        per_shape[shape_name] = dict(sorted(local.items()))
        totals.update(local)

    for key, expected in EXPECTED_TRACE_TOTALS.items():
        assert totals[key] == expected, (key, totals[key], expected)
    for p_value in PRIMES:
        assert per_prime[p_value]["cover_occurrences_checked"] == 24468
        assert per_prime[p_value]["incidence_survivors"] == 24468
        assert per_prime[p_value]["large_core_dense_indicators"] == 0
        assert per_prime[p_value]["determined_unit_rejections"] == 0
        per_prime[p_value]["canonical_cover_trace_classes_checked"] = sum(
            1 for key in witness_cache if key[0] == p_value
        )

    return {
        "totals": dict(sorted(totals.items())),
        "per_shape": per_shape,
        "per_prime": {
            str(p_value): dict(sorted(counts.items()))
            for p_value, counts in sorted(per_prime.items())
        },
        "first_incidence_witness": example_witnesses,
    }


def exclusion_windows() -> dict[str, object]:
    """Exact support-size consequences of every surviving unit form row."""

    rows = {}
    forms = {
        "Q_E+Q_F-U": (1, 1, -1),
        "U": (0, 0, 1),
        "U-Q_E": (-1, 0, 1),
        "U-Q_E-Q_F": (-1, -1, 1),
        "U+Q_E-Q_F": (1, -1, 1),
    }
    for p_value, b_value in ((233, 4), (1399, 5)):
        local = {}
        for name, (alpha, beta, gamma) in forms.items():
            t_value = alpha + beta - b_value * gamma
            residue = t_value % p_value
            core = (-residue) % p_value
            core_available = core <= p_value - 4
            forbidden_support_sizes = []
            unique_f3_support_sizes = []
            if core_available:
                for support_size in range(1, 15):
                    total_length = core + support_size
                    if 9 <= total_length <= 2 * p_value + 2:
                        forbidden_support_sizes.append(support_size)
                    elif total_length == 8:
                        unique_f3_support_sizes.append(support_size)
            local[name] = {
                "axis_coefficient": t_value,
                "neutralising_X_count": core,
                "core_available": core_available,
                "length_forbidden_support_sizes_within_1_to_14": forbidden_support_sizes,
                "length_eight_support_sizes": unique_f3_support_sizes,
            }
        rows[str(p_value)] = local
    return rows


def build_report() -> dict[str, object]:
    report = {
        "scope": {
            "primes": list(PRIMES),
            "forced_packing_types": [[3], [1, 2], [1, 1, 1]],
            "interface": "endpoint_trace_size_incidence_with_real_positions",
            "global_claim": "INCOMPLETE",
        },
        "unit_pair_form_audit": audit_unit_pair_forms(),
        "dense_degree_criterion_small_audit_rows": audit_dense_degree_criterion(),
        "cover_occurrence_audit": enumerate_cover_occurrences(),
        "unit_form_exclusion_windows": exclusion_windows(),
        "conclusion": {
            "proved": [
                "Q_E+Q_F-U is the unique unit pair form with an available large X-core",
                "its exact indicator criterion is trace-disjointness plus outside-union coverage",
                "every such indicator is in the frozen quotient-zero forbidden length range",
                "all 24468 cover-pair occurrences admit an incidence-size skeleton avoiding every large-core dense form",
            ],
            "not_proved": [
                "any cover-pair occurrence has a compatible quotient-label assignment",
                "any of the three forced packing types is empty",
                "the large-prime unique-tail branch is empty",
            ],
            "minimal_missing_data": (
                "quotient sums of the nonempty outside overlap cells "
                "(Q_E intersect Q_F) minus U and their joint incidences"
            ),
        },
    }
    certificate = canonical_hash(report)
    assert certificate == EXPECTED_CERTIFICATE_SHA256
    report["certificate_sha256"] = certificate
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    report = build_report()
    if args.report is not None:
        args.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
