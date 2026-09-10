#!/usr/bin/env python3
"""Exact checks for the L=3 and L=4 short-exchange degree models.

The eight-position core models and the core-killing extensions are checked
separately.  The extension is an interface model, not a test that the ambient
sequence is a zero-sum atom or that it satisfies the complete Hasse design.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations


def primes_through(limit: int):
    output = []
    for number in range(2, limit + 1):
        if all(number % divisor for divisor in range(2, int(number**0.5) + 1)):
            output.append(number)
    return output


def add(*vectors, p: int):
    return tuple(sum(vector[index] for vector in vectors) % p for index in range(4))


def neg(vector, p: int):
    return tuple(-coordinate % p for coordinate in vector)


def sub(first, second, p: int):
    return add(first, neg(second, p), p=p)


def quotient(vector):
    return vector[:3]


def vector(quotient_value, height, p: int):
    return tuple(coordinate % p for coordinate in quotient_value) + (height % p,)


def block_sum(block, values, p: int):
    total = (0, 0, 0, 0)
    for position in block:
        total = add(total, values[position], p=p)
    return total


def quotient_sum(block, values, p: int):
    return quotient(block_sum(block, values, p))


def all_nonquotient_zero_values(p: int):
    for first in range(p):
        for second in range(p):
            for third in range(p):
                if (first, second, third) == (0, 0, 0):
                    continue
                for height in range(p):
                    yield (first, second, third, height)


def fresh_pair(target, used, p: int):
    for first in all_nonquotient_zero_values(p):
        if first in used:
            continue
        second = sub(target, first, p)
        if quotient(second) == (0, 0, 0):
            continue
        if second in used or second == first:
            continue
        return first, second
    raise AssertionError("no fresh two-term decomposition")


def fresh_triple(target, used, p: int):
    for first in all_nonquotient_zero_values(p):
        if first in used:
            continue
        try:
            second, third = fresh_pair(sub(target, first, p), used | {first}, p)
        except AssertionError:
            continue
        return first, second, third
    raise AssertionError("no fresh three-term decomposition")


def zero_sum_position_subsets(positions, values, p: int):
    output = set()
    position_list = tuple(positions)
    for mask in range(1, 1 << len(position_list)):
        block = frozenset(
            position_list[index]
            for index in range(len(position_list))
            if mask & (1 << index)
        )
        if quotient_sum(block, values, p) == (0, 0, 0):
            output.add(block)
    return output


def assert_signed_atom(left, right, values, p: int):
    left = tuple(left)
    right = tuple(right)
    solutions = set()
    for left_mask in range(1 << len(left)):
        left_block = frozenset(
            left[index] for index in range(len(left)) if left_mask & (1 << index)
        )
        for right_mask in range(1 << len(right)):
            right_block = frozenset(
                right[index]
                for index in range(len(right))
                if right_mask & (1 << index)
            )
            if block_sum(left_block, values, p) == block_sum(right_block, values, p):
                solutions.add((left_mask, right_mask))
    assert solutions == {
        (0, 0),
        ((1 << len(left)) - 1, (1 << len(right)) - 1),
    }


def l3_core(p: int):
    e1 = (1, 0, 0)
    e2 = (0, 1, 0)
    e3 = (0, 0, 1)
    values = {
        "c1": vector(e1, 0, p),
        "c2": vector(e1, 0, p),
        "d1": vector(e2, 0, p),
        "d2": vector(e2, 0, p),
        "e": vector(e3, 0, p),
        "x": vector((-2, -2, -1), 3, p),
        "y": vector(e3, -1, p),
        "z": vector((-2, -2, -2), 4, p),
    }
    core = frozenset(("c1", "c2", "d1", "d2", "e"))
    first = core | {"x"}
    second = core | {"y", "z"}
    alternative = (core - {"e"}) | {"x", "y"}
    assert block_sum(first, values, p) == (0, 0, 0, 3 % p)
    assert block_sum(second, values, p) == (0, 0, 0, 3 % p)
    assert block_sum(alternative, values, p) == (0, 0, 0, 2 % p)
    assert quotient_sum(core, values, p) != (0, 0, 0)
    assert block_sum({"x"}, values, p) == block_sum({"y", "z"}, values, p)
    assert_signed_atom({"x"}, {"y", "z"}, values, p)
    assert zero_sum_position_subsets(values, values, p) == {
        first,
        second,
        alternative,
    }
    return values, core


def l4_core(p: int):
    e1 = (1, 0, 0)
    e2 = (0, 1, 0)
    values = {
        "c1": vector(e1, 0, p),
        "c2": vector(e1, 0, p),
        "d1": vector(e2, 0, p),
        "d2": vector(e2, 0, p),
        "r": vector((0, 0, 1), 1, p),
        "s": vector((-2, -2, -1), 2, p),
        "t": vector((0, 0, 2), 0, p),
        "u": vector((-2, -2, -2), 3, p),
    }
    core = frozenset(("c1", "c2", "d1", "d2"))
    first = core | {"r", "s"}
    second = core | {"t", "u"}
    assert block_sum(first, values, p) == (0, 0, 0, 3 % p)
    assert block_sum(second, values, p) == (0, 0, 0, 3 % p)
    assert quotient_sum(core, values, p) != (0, 0, 0)
    assert block_sum({"r", "s"}, values, p) == block_sum({"t", "u"}, values, p)
    assert_signed_atom({"r", "s"}, {"t", "u"}, values, p)
    assert zero_sum_position_subsets(values, values, p) == {first, second}
    return values, core


def add_core_killers(kind: int, values, core, target_tail, p: int):
    used = set(values.values())
    blocks = []
    for index, core_position in enumerate(sorted(core)):
        target = add(target_tail, values[core_position], p=p)
        if kind == 3:
            filler_values = fresh_pair(target, used, p)
        else:
            filler_values = fresh_triple(target, used, p)
        filler_positions = []
        for offset, filler_value in enumerate(filler_values):
            position = f"h{kind}_{index}_{offset}"
            assert position not in values
            values[position] = filler_value
            used.add(filler_value)
            filler_positions.append(position)
        block = (core - {core_position}) | set(filler_positions)
        assert len(block) == 6
        assert block_sum(block, values, p) == (0, 0, 0, 3 % p)
        blocks.append((core_position, frozenset(block)))
    return blocks


def assert_nonzero(block, values, p: int):
    assert block
    assert quotient_sum(block, values, p) != (0, 0, 0)


def check_l3_extension(p: int):
    core_values, core = l3_core(p)
    values = {position: value for position, value in core_values.items() if position not in {"y", "z"}}
    height = p - 4
    y_value = core_values["y"]
    z_value = core_values["z"]
    y_positions = tuple(f"y{index}" for index in range(height))
    z_positions = tuple(f"z{index}" for index in range(height))
    for position in y_positions:
        values[position] = y_value
    for position in z_positions:
        values[position] = z_value

    fixed = core | {"x"}
    representative = core | {y_positions[0], z_positions[0]}
    assert len(y_positions) * len(z_positions) == (p - 4) ** 2
    assert block_sum(fixed, values, p) == (0, 0, 0, 3 % p)
    assert block_sum(representative, values, p) == (0, 0, 0, 3 % p)
    assert_signed_atom({"x"}, {y_positions[0], z_positions[0]}, values, p)
    assert_nonzero(fixed & representative, values, p)

    # These are all intersection types between two distinct copied blocks.
    block_00 = core | {y_positions[0], z_positions[0]}
    block_01 = core | {y_positions[0], z_positions[1]}
    block_10 = core | {y_positions[1], z_positions[0]}
    block_11 = core | {y_positions[1], z_positions[1]}
    assert block_00 & block_11 == core
    assert block_00 & block_01 == core | {y_positions[0]}
    assert block_00 & block_10 == core | {z_positions[0]}
    for intersection in (
        block_00 & block_11,
        block_00 & block_01,
        block_00 & block_10,
    ):
        assert_nonzero(intersection, values, p)

    killers = add_core_killers(3, values, core, values["x"], p)
    killer_blocks = [block for _, block in killers]
    assert set.intersection(*(set(block) for block in killer_blocks)) == set()
    for omitted, block in killers:
        expected = core - {omitted}
        assert block & fixed == expected
        assert block & representative == expected
        assert_nonzero(expected, values, p)
        assert all(position not in block for position in y_positions + z_positions)
    for (first_omitted, first), (second_omitted, second) in combinations(killers, 2):
        expected = core - {first_omitted, second_omitted}
        assert first & second == expected
        assert_nonzero(expected, values, p)

    multiplicities = Counter(values.values())
    assert multiplicities[y_value] == height
    assert multiplicities[z_value] == height
    assert max(multiplicities.values()) == height
    assert len(values) == 2 * p + 8
    assert len(values) <= 3 * p + 4
    assert (p - 4) ** 2 + 1 + len(killers) == (p - 4) ** 2 + 6


def check_l4_extension(p: int):
    core_values, core = l4_core(p)
    values = {position: value for position, value in core_values.items() if position not in {"t", "u"}}
    height = p - 4
    t_value = core_values["t"]
    u_value = core_values["u"]
    t_positions = tuple(f"t{index}" for index in range(height))
    u_positions = tuple(f"u{index}" for index in range(height))
    for position in t_positions:
        values[position] = t_value
    for position in u_positions:
        values[position] = u_value

    fixed = core | {"r", "s"}
    representative = core | {t_positions[0], u_positions[0]}
    assert len(t_positions) * len(u_positions) == (p - 4) ** 2
    assert block_sum(fixed, values, p) == (0, 0, 0, 3 % p)
    assert block_sum(representative, values, p) == (0, 0, 0, 3 % p)
    assert_signed_atom({"r", "s"}, {t_positions[0], u_positions[0]}, values, p)
    assert_nonzero(fixed & representative, values, p)

    # These are all intersection types between two distinct copied blocks.
    block_00 = core | {t_positions[0], u_positions[0]}
    block_01 = core | {t_positions[0], u_positions[1]}
    block_10 = core | {t_positions[1], u_positions[0]}
    block_11 = core | {t_positions[1], u_positions[1]}
    assert block_00 & block_11 == core
    assert block_00 & block_01 == core | {t_positions[0]}
    assert block_00 & block_10 == core | {u_positions[0]}
    for intersection in (
        block_00 & block_11,
        block_00 & block_01,
        block_00 & block_10,
    ):
        assert_nonzero(intersection, values, p)

    target_tail = block_sum({"r", "s"}, values, p)
    killers = add_core_killers(4, values, core, target_tail, p)
    killer_blocks = [block for _, block in killers]
    assert set.intersection(*(set(block) for block in killer_blocks)) == set()
    for omitted, block in killers:
        expected = core - {omitted}
        assert block & fixed == expected
        assert block & representative == expected
        assert_nonzero(expected, values, p)
        assert all(position not in block for position in t_positions + u_positions)
    for (first_omitted, first), (second_omitted, second) in combinations(killers, 2):
        expected = core - {first_omitted, second_omitted}
        assert first & second == expected
        assert_nonzero(expected, values, p)

    multiplicities = Counter(values.values())
    assert multiplicities[t_value] == height
    assert multiplicities[u_value] == height
    assert max(multiplicities.values()) == height
    assert len(values) == 2 * p + 10
    assert len(values) <= 3 * p + 4
    assert (p - 4) ** 2 + 1 + len(killers) == (p - 4) ** 2 + 5


def main():
    checked = [prime for prime in primes_through(500) if prime >= 7]
    for prime in checked:
        l3_core(prime)
        l4_core(prime)
        check_l3_extension(prime)
        check_l4_extension(prime)
    print(
        "PASS: exact L=3/L=4 core subset enumeration, signed atomicity, "
        "quadratic replication, and all core-killer intersection types"
    )
    print(f"Checked {len(checked)} primes, 7 <= p <= 500")
    print(
        "SCOPE: the core-killing extensions are interface models only; "
        "they are not ambient zero-sum atoms and do not implement Hasse designs"
    )


if __name__ == "__main__":
    main()
