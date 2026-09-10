#!/usr/bin/env python3
"""Finite checks for the ROUTE-A4 quotient exchange models.

The models live only in C_p^3.  Passing this script does not construct a
counterexample to A_p and does not verify a common C_p^4 lift.
"""

from itertools import product


def primes(limit):
    return [
        value
        for value in range(2, limit + 1)
        if all(value % divisor for divisor in range(2, int(value**0.5) + 1))
    ]


def add(*vectors, prime):
    return tuple(sum(vector[i] for vector in vectors) % prime for i in range(3))


def scale(coefficient, vector, prime):
    return tuple(coefficient * entry % prime for entry in vector)


def sequence_sum(vectors, multiplicities, prime):
    return tuple(
        sum(multiplicity * vector[i]
            for vector, multiplicity in zip(vectors, multiplicities)) % prime
        for i in range(3)
    )


def assert_small_atom(vectors, multiplicities, prime):
    solutions = []
    for counts in product(*(range(multiplicity + 1)
                            for multiplicity in multiplicities)):
        if sequence_sum(vectors, counts, prime) == (0, 0, 0):
            solutions.append(counts)
    assert solutions == [tuple(0 for _ in multiplicities), tuple(multiplicities)]


def assert_standard_and_near_atoms(prime):
    standard_solutions = []
    for exceptional in (0, 1):
        count = (-exceptional) % prime
        if count <= prime - 1:
            standard_solutions.append((count, count, count, exceptional))
    assert standard_solutions == [
        (0, 0, 0, 0),
        (prime - 1, prime - 1, prime - 1, 1),
    ]

    near7_solutions = []
    for epsilon, delta in product(range(2), repeat=2):
        x12 = (-epsilon - delta) % prime
        x3 = (-epsilon) % prime
        if x12 <= prime - 2 and x3 <= prime - 1:
            near7_solutions.append((x12, x12, x3, epsilon, delta))
    assert near7_solutions == [
        (0, 0, 0, 0, 0),
        (prime - 2, prime - 2, prime - 1, 1, 1),
    ]

    near8_solutions = []
    for copies_g in range(3):
        count = (-copies_g) % prime
        if count <= prime - 2:
            near8_solutions.append((count, count, count, copies_g))
    assert near8_solutions == [
        (0, 0, 0, 0),
        (prime - 2, prime - 2, prime - 2, 2),
    ]


def check_models(prime):
    e1 = (1, 0, 0)
    e2 = (0, 1, 0)
    e3 = (0, 0, 1)
    g = (1, 1, 1)
    zero = (0, 0, 0)

    assert_standard_and_near_atoms(prime)

    inv3 = pow(3, -1, prime)
    x = scale(-inv3, g, prime)
    assert_small_atom([x, e1, e2, e3], [3, 1, 1, 1], prime)
    assert add(scale(3, x, prime), g, prime=prime) == zero

    h = (1, 1, 0)
    q7 = (-1 % prime, -3 % prime, -2 % prime)
    assert_small_atom([h, e2, e3, q7], [1, 2, 2, 1], prime)
    assert_small_atom([e1, e2, e3, q7], [1, 3, 2, 1], prime)
    assert sequence_sum([e2, e3, q7], [2, 2, 1], prime) == scale(-1, h, prime)

    q8 = (-1 % prime, -3 % prime, -3 % prime)
    assert_small_atom([g, e2, e3, q8], [1, 2, 2, 1], prime)
    assert_small_atom([e1, e2, e3, q8], [1, 3, 3, 1], prime)
    assert sequence_sum([e2, e3, q8], [2, 2, 1], prime) == scale(-1, g, prime)

    assert 6 + 3 * prime - 2 == 3 * prime + 4
    assert (0 + 2 - 5 + 3) % prime == 0


def main():
    checked = [prime for prime in primes(500) if prime >= 7]
    for prime in checked:
        check_models(prime)
    print(
        "PASS: all three quotient exchange models and their atom equations "
        f"for {len(checked)} primes, 7<=p<=500"
    )
    print("SCOPE: quotient-only method countermodels; not A_p counterexamples")


if __name__ == "__main__":
    main()
