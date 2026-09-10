"""Exact fibre recovery and capacity census for the p=233, m=3 core.

The common cubic is already proved to be the signed coefficient function of
the 461-position zero-sum-free core C.  At each of the six mixed targets this
script recovers the corresponding ordinary singleton-fibre multiplicity and
tests the global height and core-capacity constraints.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, permutations

from unique_tail_p233_three_h8_m3_cubic_quadratic_compatibility import (
    P,
    TAILS,
    add,
    core_coefficient,
    cubic_parameters,
    sub,
)


HEIGHT_CAP = P - 4
CORE_LENGTH = 2 * P - 5
ALL_NONZERO_SCALARS = (1 << (P - 1)) - 1

ORBIT_REPRESENTATIVES = (
    ((10, 193), (69, 197)),
    ((12, 25), (12, 25)),
    ((18, 181), (18, 181)),
    ((29, 78), (1, 2)),
    ((29, 184), (8, 199)),
    ((33, 168), (29, 191)),
    ((44, 154), (39, 33)),
    ((56, 128), (56, 128)),
    ((66, 142), (3, 60)),
)


def recovered_fibre(
    target: tuple[int, int], parameters: tuple[int, int, int]
) -> int:
    """Recover nu_target(C) from the signed core coefficient modulo p."""
    return (
        -core_coefficient(target, parameters)
        + int(target == (0, 0))
    ) % P


def det(left: tuple[int, int], right: tuple[int, int]) -> int:
    return (left[0] * right[1] - left[1] * right[0]) % P


def scalar_interval_masks() -> tuple[tuple[int, ...], ...]:
    """Mask lambdas with the least residue of lambda*kappa at most a."""
    table: list[tuple[int, ...]] = []
    for kappa in range(P):
        if kappa == 0:
            table.append((ALL_NONZERO_SCALARS,) * (HEIGHT_CAP + 1))
            continue
        inverse = pow(kappa, -1, P)
        mask = 0
        row = []
        for bound in range(HEIGHT_CAP + 1):
            if bound:
                lam = bound * inverse % P
                mask |= 1 << (lam - 1)
            row.append(mask)
        table.append(tuple(row))
    return tuple(table)


def has_three_fibre_zero_sum(
    fibres: tuple[tuple[tuple[int, int], int], ...],
    masks: tuple[tuple[int, ...], ...],
) -> bool:
    """Test every determinantal relation supported on three active fibres."""
    for first, second, third in combinations(fibres, 3):
        a, cap_a = first
        b, cap_b = second
        c, cap_c = third
        kappa = (det(b, c), det(c, a), det(a, b))
        if kappa == (0, 0, 0):
            continue
        common = (
            masks[kappa[0]][cap_a]
            & masks[kappa[1]][cap_b]
            & masks[kappa[2]][cap_c]
        )
        if common:
            lam = (common & -common).bit_length()
            coefficients = tuple(lam * value % P for value in kappa)
            assert any(coefficients)
            assert coefficients[0] <= cap_a
            assert coefficients[1] <= cap_b
            assert coefficients[2] <= cap_c
            assert (
                coefficients[0] * a[0]
                + coefficients[1] * b[0]
                + coefficients[2] * c[0]
            ) % P == 0
            assert (
                coefficients[0] * a[1]
                + coefficients[1] * b[1]
                + coefficients[2] * c[1]
            ) % P == 0
            return True
    return False


def balanced_bipartition(
    fibres: tuple[tuple[tuple[int, int], int], ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Choose an exhaustive at-most-three versus at-most-three split."""
    size = len(fibres)
    best = None
    for mask in range(1 << size):
        left = tuple(index for index in range(size) if mask >> index & 1)
        right = tuple(index for index in range(size) if not (mask >> index & 1))
        if len(left) > 3 or len(right) > 3:
            continue
        left_work = 1
        right_work = 1
        for index in left:
            left_work *= fibres[index][1] + 1
        for index in right:
            right_work *= fibres[index][1] + 1
        score = (max(left_work, right_work), left_work + right_work, left)
        if best is None or score < best[0]:
            best = (score, left, right)
    assert best is not None
    return best[1], best[2]


def half_sums(
    fibres: tuple[tuple[tuple[int, int], int], ...],
    indices: tuple[int, ...],
) -> tuple[dict[int, tuple[int, ...]], tuple[int, ...] | None]:
    """Enumerate every bounded coefficient tuple on one half exactly."""
    codes: dict[int, tuple[int, ...]] = {}
    zero_witness = None
    coefficients = [0] * len(indices)

    def visit(position: int, x: int, y: int, nonempty: bool) -> None:
        nonlocal zero_witness
        if zero_witness is not None:
            return
        if position == len(indices):
            code = x * P + y
            if code == 0 and nonempty:
                zero_witness = tuple(coefficients)
            codes.setdefault(code, tuple(coefficients))
            return
        label, cap = fibres[indices[position]]
        for coefficient in range(cap + 1):
            coefficients[position] = coefficient
            visit(
                position + 1,
                (x + coefficient * label[0]) % P,
                (y + coefficient * label[1]) % P,
                nonempty or coefficient != 0,
            )

    visit(0, 0, 0, False)
    return codes, zero_witness


def verify_relation(
    fibres: tuple[tuple[tuple[int, int], int], ...], coefficients: tuple[int, ...]
) -> None:
    assert len(fibres) == len(coefficients)
    assert any(coefficients)
    assert all(0 <= value <= fibres[index][1] for index, value in enumerate(coefficients))
    assert sum(value * fibres[index][0][0] for index, value in enumerate(coefficients)) % P == 0
    assert sum(value * fibres[index][0][1] for index, value in enumerate(coefficients)) % P == 0


def has_bounded_zero_sum(
    fibres: tuple[tuple[tuple[int, int], int], ...]
) -> bool:
    """Exact meet-in-the-middle test for a nonzero bounded relation."""
    if not fibres:
        return False
    left_indices, right_indices = balanced_bipartition(fibres)
    left_codes, left_zero = half_sums(fibres, left_indices)
    if left_zero is not None:
        full = [0] * len(fibres)
        for index, value in zip(left_indices, left_zero):
            full[index] = value
        verify_relation(fibres, tuple(full))
        return True

    found = False
    right_coefficients = [0] * len(right_indices)

    def visit(position: int, x: int, y: int, nonempty: bool) -> None:
        nonlocal found
        if found:
            return
        if position == len(right_indices):
            if x == 0 and y == 0:
                if nonempty:
                    full = [0] * len(fibres)
                    for index, value in zip(right_indices, right_coefficients):
                        full[index] = value
                    verify_relation(fibres, tuple(full))
                    found = True
                return
            opposite = ((-x) % P) * P + (-y) % P
            if opposite in left_codes:
                full = [0] * len(fibres)
                for index, value in zip(left_indices, left_codes[opposite]):
                    full[index] = value
                for index, value in zip(right_indices, right_coefficients):
                    full[index] = value
                verify_relation(fibres, tuple(full))
                found = True
            return
        label, cap = fibres[right_indices[position]]
        for coefficient in range(cap + 1):
            right_coefficients[position] = coefficient
            visit(
                position + 1,
                (x + coefficient * label[0]) % P,
                (y + coefficient * label[1]) % P,
                nonempty or coefficient != 0,
            )

    visit(0, 0, 0, False)
    return found


def tail_permutation_image(
    vector: tuple[int, int], permutation: tuple[int, int, int]
) -> tuple[int, int]:
    """Apply the unique linear map sending w_i to w_permutation(i)."""
    x, y = vector
    image_e = TAILS[permutation[0]]
    image_f = TAILS[permutation[1]]
    return (
        (x * image_e[0] + y * image_f[0]) % P,
        (x * image_e[1] + y * image_f[1]) % P,
    )


def orbit_of(
    pair: tuple[tuple[int, int], tuple[int, int]]
) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    delta, s = pair
    orbit = set()
    for permutation in permutations(range(3)):
        delta_image = tail_permutation_image(delta, permutation)
        s_image = tail_permutation_image(s, permutation)
        orbit.add((delta_image, s_image))
        orbit.add((delta_image, ((-s_image[0]) % P, (-s_image[1]) % P)))
    return orbit


def main() -> None:
    curve = [
        (alpha, beta)
        for alpha in range(P)
        for beta in range(P)
        if (alpha * alpha - alpha * beta + beta * beta - 3) % P == 0
    ]
    exceptional = {
        sub(TAILS[j], TAILS[i])
        for i in range(3)
        for j in range(3)
        if i != j
    }
    generic_curve = [delta for delta in curve if delta not in exceptional]
    assert len(curve) == P + 1 == 234
    assert len(exceptional) == 6
    assert len(generic_curve) == P - 5 == 228

    excluded_directions = set(TAILS) | {
        ((-x) % P, (-y) % P) for x, y in TAILS
    }
    directions = [
        (x, y)
        for x in range(P)
        for y in range(P)
        if (x, y) != (0, 0) and (x, y) not in excluded_directions
    ]
    assert len(directions) == P * P - 7 == 54_282

    rejected_residue = 0
    rejected_repeated_label = 0
    rejected_capacity = 0
    rejected_three_fibre = 0
    rejected_bounded_subset_sum = 0
    capacity_survivors = 0
    triple_survivors = 0
    final_survivors: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    survivor_counts_by_delta: list[int] = []
    examples: dict[str, object] = {}
    masks = scalar_interval_masks()

    for delta in generic_curve:
        parameters = cubic_parameters(*delta)
        fringe = tuple(add(delta, tail) for tail in TAILS)
        delta_survivors = 0

        for s in directions:
            minus_s = ((-s[0]) % P, (-s[1]) % P)
            targets = tuple(sub(r, endpoint) for r in (s, minus_s) for endpoint in fringe)
            recovered = tuple(recovered_fibre(t, parameters) for t in targets)

            if any(value > HEIGHT_CAP for value in recovered):
                rejected_residue += 1
                examples.setdefault(
                    "height_residue_rejection",
                    {"delta": delta, "s": s, "targets": targets, "A": recovered},
                )
                continue

            by_target: dict[tuple[int, int], int] = {}
            inconsistent = False
            for target, value in zip(targets, recovered):
                if target in by_target and by_target[target] != value:
                    inconsistent = True
                    break
                by_target[target] = value
            if inconsistent:
                rejected_repeated_label += 1
                continue

            used_capacity = sum(by_target.values())
            if used_capacity > CORE_LENGTH:
                rejected_capacity += 1
                examples.setdefault(
                    "core_capacity_rejection",
                    {
                        "delta": delta,
                        "s": s,
                        "targets": targets,
                        "A": recovered,
                        "unique_fibre_capacity": used_capacity,
                    },
                )
                continue

            capacity_survivors += 1
            active_fibres = tuple(
                (target, value)
                for target, value in by_target.items()
                if value > 0
            )
            assert all(target != (0, 0) for target, _value in active_fibres)
            if has_three_fibre_zero_sum(active_fibres, masks):
                rejected_three_fibre += 1
                continue

            triple_survivors += 1
            if has_bounded_zero_sum(active_fibres):
                rejected_bounded_subset_sum += 1
                continue

            final_survivors.add((delta, s))
            delta_survivors += 1
            examples.setdefault(
                "survivor",
                {
                    "delta": delta,
                    "s": s,
                    "targets": targets,
                    "A": recovered,
                    "unique_fibre_capacity": used_capacity,
                },
            )

        survivor_counts_by_delta.append(delta_survivors)

    total = len(generic_curve) * len(directions)
    histogram = Counter(survivor_counts_by_delta)
    assert total == 12_376_296
    assert rejected_residue == 926_736
    assert rejected_repeated_label == 0
    assert rejected_capacity == 10_474_932
    assert capacity_survivors == 974_628
    assert rejected_three_fibre == 974_148
    assert triple_survivors == 480
    assert rejected_bounded_subset_sum == 372
    assert len(final_survivors) == 108
    assert (
        rejected_residue
        + rejected_repeated_label
        + rejected_capacity
        + rejected_three_fibre
        + rejected_bounded_subset_sum
        + len(final_survivors)
        == total
    )
    assert min(survivor_counts_by_delta) == 0
    assert max(survivor_counts_by_delta) == 2

    expected_orbits = [orbit_of(pair) for pair in ORBIT_REPRESENTATIVES]
    assert all(len(orbit) == 12 for orbit in expected_orbits)
    assert set().union(*expected_orbits) == final_survivors
    assert sum(len(orbit) for orbit in expected_orbits) == len(final_survivors)
    assert not any(x != y and x & y for x in expected_orbits for y in expected_orbits)

    off_tail_final = sum(
        x != 0 and y != 0 and x != y for _delta, (x, y) in final_survivors
    )
    assert off_tail_final == len(final_survivors)

    report = {
        "status": "PASS",
        "prime": P,
        "generic_curve_points": len(generic_curve),
        "admissible_directions_per_point": len(directions),
        "total_pairs": total,
        "height_cap": HEIGHT_CAP,
        "core_length": CORE_LENGTH,
        "classification_priority": [
            "recovered residue exceeds the height cap",
            "same projection label receives inconsistent recovered values",
            "sum over distinct recovered projection fibres exceeds the core length",
            "a determinantal relation on three forced fibres gives a core zero-sum",
            "the exhaustive bounded subset-sum test gives a core zero-sum",
            "final survivor",
        ],
        "rejected_by_height_residue": rejected_residue,
        "rejected_by_repeated_label_inconsistency": rejected_repeated_label,
        "rejected_by_core_capacity": rejected_capacity,
        "capacity_survivors": capacity_survivors,
        "rejected_by_three_fibre_relation": rejected_three_fibre,
        "three_fibre_survivors": triple_survivors,
        "rejected_by_exhaustive_bounded_subset_sum": rejected_bounded_subset_sum,
        "final_survivors": len(final_survivors),
        "final_survivor_fraction": f"{len(final_survivors)}/{total}",
        "final_survivors_per_delta_min": min(survivor_counts_by_delta),
        "final_survivors_per_delta_max": max(survivor_counts_by_delta),
        "final_survivors_per_delta_histogram": dict(sorted(histogram.items())),
        "final_survivor_orbit_representatives": ORBIT_REPRESENTATIVES,
        "final_survivor_orbit_count": len(expected_orbits),
        "final_survivor_orbit_size": 12,
        "final_survivors_off_tail_lines": off_tail_final,
        "examples": examples,
        "conclusion": (
            "exact core-fibre recovery plus core zero-sumfreeness reduces the "
            "generic m=3 layer to nine tail-S3-by-sign orbits; it does not "
            "eliminate the m=3 state"
        ),
        "scope": "fixed p=233 generic m=3 curve after the six exceptional deltas",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
