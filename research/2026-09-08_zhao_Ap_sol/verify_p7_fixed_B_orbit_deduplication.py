#!/usr/bin/env python3
"""Exact orbit deduplication for the two old fixed p=7 length-19 atoms."""

from collections import Counter
from itertools import combinations

import p7_m3_next_heavy_fibre_solver as M3
import p7_m4_unified_quotient_search as M4


P = 7
MATRIX = ((1, 0, 0), (0, 1, 0), (1, 0, 1))


def transform(value):
    return tuple(
        sum(MATRIX[row][column] * value[column] for column in range(3)) % P
        for row in range(3)
    )


def determinant(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % P


def spectra(sequence):
    answer = {}
    for size in range(8, 12):
        answer[size] = {
            M4.sum3(sequence[index] for index in subset)
            for subset in combinations(range(len(sequence)), size)
        }
    return answer


def main():
    assert determinant(MATRIX) == 1
    transformed = tuple(transform(value) for value in M4.BASE_B)
    assert Counter(transformed) == Counter(M3.BASE_B)

    left = spectra(M4.BASE_B)
    right = spectra(M3.BASE_B)
    for size in range(8, 12):
        assert {transform(value) for value in left[size]} == right[size]

    q = (1, 0, 0)
    assert transform(q) == (1, 0, 1)
    m4_counts = Counter(M4.BASE_B)
    m3_counts = Counter(M3.BASE_B)
    assert m4_counts[q] == 4
    assert m3_counts[q] == 3
    assert m3_counts[transform(q)] == 4

    print("PASS A(x,y,z)=(x,y,x+z) maps the m=4 fixed B onto the m=3 fixed B")
    print("PASS sizes 8..11 spectra are exact linear images")
    print("POINTED DISTINCTION: designated X multiplicities are 4 versus 3")
    print("STATUS: orbit deduplication only; both full p=7 branches remain INCOMPLETE")


if __name__ == "__main__":
    main()
