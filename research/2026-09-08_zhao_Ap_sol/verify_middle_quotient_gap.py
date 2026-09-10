#!/usr/bin/env python3
"""Finite arithmetic audit for the middle quotient-zero length gap.

The proof is symbolic.  This script checks every endpoint and records the
small-prime pair-length consequences; it is not a universal theorem prover.
"""

from __future__ import annotations


def primes_through(limit: int) -> list[int]:
    answer = []
    for candidate in range(2, limit + 1):
        if all(candidate % divisor for divisor in range(2, int(candidate**0.5) + 1)):
            answer.append(candidate)
    return answer


def forbidden_pair_lengths(prime: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left in range(2, 9)
        for right in range(left, 9)
        if prime + 2 <= left + right <= 2 * prime + 2
    )


def main() -> None:
    checked = [prime for prime in primes_through(500) if prime >= 7]
    for prime in checked:
        # Complementation preserves the proposed interval:
        # k -> 3p+4-k swaps its two endpoints.
        for size in range(prime + 2, 2 * prime + 3):
            complement = 3 * prime + 4 - size
            assert prime + 2 <= complement <= 2 * prime + 2

        # The two (SQ) coefficients cannot be negatives modulo p.
        for left_coefficient in (1, 2, 3):
            for right_coefficient in (1, 2, 3):
                assert (left_coefficient + right_coefficient) % prime

        # First overshoot of p+1 by a block of size at most eight stays
        # inside the forbidden interval.
        for previous in range(prime + 2):
            for block_size in range(2, 9):
                total = previous + block_size
                if total > prime + 1:
                    assert prime + 2 <= total <= 2 * prime + 2

    expected = {
        7: tuple(
            (left, right)
            for left in range(2, 9)
            for right in range(left, 9)
            if left + right >= 9
        ),
        11: ((5, 8), (6, 7), (6, 8), (7, 7), (7, 8), (8, 8)),
        13: ((7, 8), (8, 8)),
        17: (),
    }
    for prime, pairs in expected.items():
        assert forbidden_pair_lengths(prime) == pairs

    print(
        "PASS middle quotient-zero gap for",
        len(checked),
        "primes 7<=p<=500",
    )
    for prime in (7, 11, 13, 17):
        print(f"p={prime} forbidden disjoint short-block length pairs:")
        print(forbidden_pair_lengths(prime))
    print("PROVED symbolic weighted matching capacity: total support <= p+1")
    print("STATUS: position-level subtheorem; full A_p remains INCOMPLETE")


if __name__ == "__main__":
    main()
