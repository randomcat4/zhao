#!/usr/bin/env python3
"""Exact arithmetic checks for p_minus_two_survivor_refinement.md.

This script verifies the three finite survivor closures.  It deliberately does
not re-prove the structural classification in p_minus_two_height_fibre.md.
"""

CASES = (
    {
        "name": "p=11 plus",
        "p": 11,
        "m5": 5,
        "t0_x": 25,
        "t0_a": -2,
        "selected_x": 8,
        "selected_a": 1,
        "anchors": 1,
        "core_used": 7,
        "plus_used": 1,
        "minus_used": 0,
        "expected_lengths": (10, 11, 12),
    },
    {
        "name": "p=11 minus",
        "p": 11,
        "m5": 3,
        "t0_x": 15,
        "t0_a": -6,
        "selected_x": 7,
        "selected_a": 0,
        "anchors": 6,
        "core_used": 7,
        "plus_used": 0,
        "minus_used": 0,
        "expected_lengths": (16, 17, 18),
    },
    {
        "name": "p=19 plus",
        "p": 19,
        "m5": 1,
        "t0_x": 5,
        "t0_a": 2,
        "selected_x": 14,
        "selected_a": 2,
        "anchors": 15,
        "core_used": 12,
        "plus_used": 2,
        "minus_used": 0,
        "expected_lengths": (34, 35, 36),
    },
)


def verify_case(case):
    p = case["p"]
    assert 1 <= case["m5"] <= 8 < p
    assert case["anchors"] <= p - 4
    assert case["core_used"] <= p - 4
    assert case["plus_used"] <= 2
    assert case["minus_used"] <= 2

    x_coefficient = case["t0_x"] + case["selected_x"]
    a_coefficient = (
        case["t0_a"] + case["selected_a"] + case["anchors"]
    )
    assert x_coefficient % p == 0
    assert a_coefficient % p == 0

    lengths = []
    for s in (6, 7, 8):
        t0_size = s - case["m5"]
        assert t0_size >= 1
        length = (
            t0_size
            + case["core_used"]
            + case["plus_used"]
            + case["minus_used"]
            + case["anchors"]
        )
        assert length <= 3 * p - 2
        lengths.append(length)
    assert tuple(lengths) == case["expected_lengths"]
    return x_coefficient, a_coefficient, tuple(lengths)


def main():
    for case in CASES:
        x_coefficient, a_coefficient, lengths = verify_case(case)
        print(
            "PASS",
            case["name"],
            f"coefficients=({x_coefficient},{a_coefficient})",
            f"lengths={lengths}",
        )
    print("PASS exact survivor arithmetic and resource bounds")
    print("SCOPE structural classification is assumed, not re-proved here")


if __name__ == "__main__":
    main()
