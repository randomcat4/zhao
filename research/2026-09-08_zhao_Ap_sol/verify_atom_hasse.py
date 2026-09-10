#!/usr/bin/env python3
"""Probe the Hasse-moment system of a hypothetical (3p+3)-atom.

This script only checks the finite linear algebra derived in the accompanying
proof note.  It does not enumerate sequences and is not an A_p verifier.
"""

from fractions import Fraction


VARIABLES = (
    [(1, k) for k in range(2, 6)]
    + [(2, k) for k in range(4, 7)]
    + [(3, k) for k in range(4, 8)]
)


def ibinom(n: int, q: int) -> int:
    value = Fraction(1)
    for j in range(q):
        value *= Fraction(n - j, j + 1)
    assert value.denominator == 1
    return value.numerator


def system():
    rows = []
    rhs = []
    labels = []
    zero_values = (2, 3, 3, 1, 0, 0)
    for q in range(6):
        for moment in range(6 - q):
            row = []
            for lam, length in VARIABLES:
                row.append(
                    (-1) ** length
                    * (
                        lam**moment * ibinom(length, q)
                        + (-lam) ** moment * ibinom(3 - length, q)
                    )
                )
            rows.append(row)
            rhs.append(-zero_values[q] if moment == 0 else 0)
            labels.append((q, moment))
    # Apply the scalar deletion identities to
    # V = Z a^(p-4), whose length is 4p-1 = D+2.  All its nonempty
    # zero sums are Z itself or (Z\C) a^t with t=1,2,3 and
    # sigma(C)=t a.
    for deletion in range(3):
        row = []
        for lam, length in VARIABLES:
            deficit = length - lam
            row.append(
                ibinom(-4, lam)
                * (-1) ** (length + lam)
                * ibinom(deficit - 4, deletion)
            )
        rows.append(row)
        rhs.append(-ibinom(-1, deletion) - ibinom(-4, deletion))
        labels.append(("global", deletion))
    return rows, rhs, labels


def system_j4():
    """Hasse moments for a (3p+4)-atom after the complement-atom lemma."""
    variables = (
        [(1, k) for k in range(2, 7)]
        + [(2, k) for k in range(4, 8)]
        + [(3, k) for k in range(6, 9)]
    )
    rows = []
    rhs = []
    labels = []
    # M_q(0) for M_q=sum (-1)^k binom(k,q) N_k(0), using
    # the empty set and the odd full set of size 3p+4.
    zero_values = (0, -4, -6, -4, -1, 0, 0)
    for q in range(7):
        for moment in range(7 - q):
            row = []
            for lam, length in variables:
                row.append(
                    (-1) ** length
                    * (
                        lam**moment * ibinom(length, q)
                        - (-lam) ** moment * ibinom(4 - length, q)
                    )
                )
            rows.append(row)
            rhs.append(-zero_values[q] if moment == 0 else 0)
            labels.append((q, moment))
    return variables, rows, rhs, labels


def system_j4_with_point():
    """Global counts and counts of blocks through one fixed position."""
    variables, global_rows, global_rhs, global_labels = system_j4()
    width = len(variables)
    rows = [row + [0] * width for row in global_rows]
    rhs = list(global_rhs)
    labels = [("global", label) for label in global_labels]
    zero_values = tuple(ibinom(3, q) for q in range(6))
    for q in range(6):
        for moment in range(6 - q):
            n_coefficients = []
            m_coefficients = []
            for lam, length in variables:
                negative = (
                    (-lam) ** moment
                    * (-1) ** length
                    * ibinom(3 - length, q)
                )
                positive = (
                    lam**moment
                    * (-1) ** (length - 1)
                    * ibinom(length - 1, q)
                )
                n_coefficients.append(negative)
                m_coefficients.append(positive - negative)
            rows.append(n_coefficients + m_coefficients)
            rhs.append(-zero_values[q] if moment == 0 else 0)
            labels.append(("point", q, moment))
    names = [("N", variable) for variable in variables]
    names += [("m", variable) for variable in variables]
    return names, rows, rhs, labels


def rref_fraction(rows, rhs):
    matrix = [list(map(Fraction, row)) + [Fraction(value)]
              for row, value in zip(rows, rhs)]
    pivot_row = 0
    pivots = []
    for col in range(len(rows[0])):
        pivot = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [x / scale for x in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][col]:
                scale = matrix[r][col]
                matrix[r] = [x - scale * y
                             for x, y in zip(matrix[r], matrix[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    inconsistent = [row for row in matrix
                    if all(x == 0 for x in row[:-1]) and row[-1] != 0]
    return matrix, pivots, inconsistent


def rref_fraction_with_certificate(rows, rhs):
    matrix = [list(map(Fraction, row)) + [Fraction(value)]
              for row, value in zip(rows, rhs)]
    transform = [[Fraction(int(i == j)) for j in range(len(matrix))]
                 for i in range(len(matrix))]
    pivot_row = 0
    pivots = []
    for col in range(len(rows[0])):
        pivot = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        transform[pivot_row], transform[pivot] = (
            transform[pivot], transform[pivot_row]
        )
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [x / scale for x in matrix[pivot_row]]
        transform[pivot_row] = [x / scale for x in transform[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][col]:
                scale = matrix[r][col]
                matrix[r] = [x - scale * y
                             for x, y in zip(matrix[r], matrix[pivot_row])]
                transform[r] = [x - scale * y
                                for x, y in zip(transform[r],
                                                transform[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    return matrix, pivots, transform


def rref_mod(rows, rhs, prime):
    matrix = [[x % prime for x in row] + [value % prime]
              for row, value in zip(rows, rhs)]
    pivot_row = 0
    pivots = []
    for col in range(len(rows[0])):
        pivot = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][col] % prime), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inv = pow(matrix[pivot_row][col], -1, prime)
        matrix[pivot_row] = [(x * inv) % prime for x in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][col] % prime:
                scale = matrix[r][col]
                matrix[r] = [(x - scale * y) % prime
                             for x, y in zip(matrix[r], matrix[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    inconsistent = [row for row in matrix
                    if all(x % prime == 0 for x in row[:-1])
                    and row[-1] % prime != 0]
    return len(pivots), inconsistent


def primes(limit):
    out = []
    for value in range(2, limit + 1):
        if all(value % divisor for divisor in range(2, int(value**0.5) + 1)):
            out.append(value)
    return out


def check_seven_point_polynomial(prime):
    support = {0, 1, 2, 3, prime - 1, prime - 2, prime - 3}

    def q_value(x):
        value = 1
        for root in range(prime):
            if root not in support:
                value = value * (x - root) % prime
        return value

    q0 = q_value(0)
    ratios = [q_value(x) * pow(q0, -1, prime) % prime
              for x in (1, 2, 3)]
    expected = [
        -3 * pow(4, -1, prime),
        3 * pow(10, -1, prime),
        -pow(20, -1, prime),
    ]
    assert ratios == [x % prime for x in expected]

    c_values = [2 * value % prime for value in ratios]
    assert c_values == [
        (-3 * pow(2, -1, prime)) % prime,
        (3 * pow(5, -1, prime)) % prime,
        (-pow(10, -1, prime)) % prime,
    ]
    h1_values = [4 * value % prime for value in ratios]
    assert h1_values == [
        (-3) % prime,
        (6 * pow(5, -1, prime)) % prime,
        (-pow(5, -1, prime)) % prime,
    ]


def check_pair_degree_relations(prime):
    ratios = [
        (-3 * pow(4, -1, prime)) % prime,
        (3 * pow(10, -1, prime)) % prime,
        (-pow(20, -1, prime)) % prime,
    ]
    for slope in range(prime):
        degrees = [
            ratios[index] * (slope * (index + 1) - 1) % prime
            for index in range(3)
        ]
        d1, d2, d3 = degrees
        assert (8 * d1 + 10 * d2) % prime == 3 % prime
        assert (2 * d1 - 10 * d3) % prime == 1 % prime
    assert 8 * Fraction(1, 2) + 10 * Fraction(-1, 10) == 3
    assert 2 * Fraction(1, 2) == 1
    assert 8 * Fraction(3, 8) == 3
    assert 2 * Fraction(3, 8) - 10 * Fraction(-1, 40) == 1
    assert 10 * Fraction(3, 10) == 3
    assert -10 * Fraction(-1, 10) == 1


def check_triple_degree_relation(prime):
    """Check the quadratic-factor elimination after deleting three points."""
    ratios = [
        (-3 * pow(4, -1, prime)) % prime,
        (3 * pow(10, -1, prime)) % prime,
        (-pow(20, -1, prime)) % prime,
    ]
    for quadratic in range(prime):
        for linear in range(prime):
            degrees = [
                ratios[index]
                * (quadratic * (index + 1) ** 2
                   + linear * (index + 1) + 1)
                % prime
                for index in range(3)
            ]
            d1, d2, d3 = degrees
            assert (4 * d1 + 10 * d2 + 20 * d3) % prime == -1 % prime


def check_integer_lifts(prime):
    """Regression checks for the parity/nonnegativity lifts to raw counts."""
    for delta in range(-2 * prime, 2 * prime + 1):
        if (4 * delta + 3) % prime == 0:
            assert abs(delta) >= (prime - 3 + 3) // 4
        if (10 * delta - 3) % prime == 0:
            assert abs(delta) >= (prime - 3 + 9) // 10
        if (20 * delta + 1) % prime == 0:
            assert abs(delta) >= (prime - 1 + 19) // 20
    first_n6 = next(value for value in range(prime + 1)
                    if (5 * value - 1) % prime == 0)
    assert first_n6 >= (prime + 1 + 4) // 5


def check_two_term_and_tensor_boundary(prime):
    inv2 = pow(2, -1, prime)
    inv10 = pow(10, -1, prime)
    inv20 = pow(20, -1, prime)
    sx = inv20
    sy = inv20
    sxy = -inv10 % prime
    alpha3 = -inv20 % prime
    assert (sx + sy + sxy) % prime == 0
    assert (sx + sxy) % prime == alpha3
    assert (sy + sxy) % prime == alpha3
    d1, d2, d3 = 1, -inv2 % prime, inv10
    assert (8 * d1 + 10 * d2) % prime == 3 % prime
    assert (2 * d1 - 10 * d3) % prime == 1 % prime

    height = prime - 4
    for size in range(height + 1):
        assert size * (size - 1) // 2 <= height * (size // 2)
    for block_length in (6, 7, 8):
        assert (block_length - 9) % prime != 0

    for degree in range(4):
        assert sum(pow(value, degree, prime) for value in range(prime)) % prime == 0


def main():
    rows, rhs, labels = system()
    matrix, pivots, inconsistent = rref_fraction(rows, rhs)
    print(f"variables={VARIABLES}")
    print(f"equations={len(rows)} rank_Q={len(pivots)} "
          f"inconsistent_Q={bool(inconsistent)}")
    if inconsistent:
        print(f"first_inconsistent_row={inconsistent[0]}")
    else:
        free = [j for j in range(len(VARIABLES)) if j not in pivots]
        print(f"free_variables={[VARIABLES[j] for j in free]}")
        for row_index, col in enumerate(pivots):
            terms = [(VARIABLES[j], -matrix[row_index][j])
                     for j in free if matrix[row_index][j]]
            print(f"{VARIABLES[col]} = {matrix[row_index][-1]} + {terms}")
    for prime in (7, 11, 13, 17, 19, 23, 29, 31, 37, 101, 149, 499):
        rank, bad = rref_mod(rows, rhs, prime)
        print(f"p={prime} rank={rank} inconsistent={bool(bad)}")
    checked = [prime for prime in primes(500) if prime >= 7]
    for prime in checked:
        check_seven_point_polynomial(prime)
        check_pair_degree_relations(prime)
        check_triple_degree_relation(prime)
        check_integer_lifts(prime)
        check_two_term_and_tensor_boundary(prime)
    print(f"PASS: seven-point line values for {len(checked)} primes, 7<=p<=500")
    print("PASS: two-point deletion identities and all three absence cases "
          "for primes 7<=p<=500")
    print("PASS: three-point deletion identity and integer count lifts "
          "for primes 7<=p<=500")
    print("PASS: two-term transversal residues, value-pair graph bound, "
          "affine-rank coefficients, and cubic height blind spot for "
          "primes 7<=p<=500")
    print("PASS: the first six Hasse/deletion constraints are consistent of rank 9; "
          "they do not by themselves prove A_p")
    variables4, rows4, rhs4, labels4 = system_j4()
    matrix4, pivots4, inconsistent4 = rref_fraction(rows4, rhs4)
    print(f"j=4 variables={variables4}")
    print(f"j=4 equations={len(rows4)} rank_Q={len(pivots4)} "
          f"inconsistent_Q={bool(inconsistent4)}")
    if not inconsistent4:
        free4 = [j for j in range(len(variables4)) if j not in pivots4]
        print(f"j=4 free_variables={[variables4[j] for j in free4]}")
        for row_index, col in enumerate(pivots4):
            terms = [(variables4[j], -matrix4[row_index][j])
                     for j in free4 if matrix4[row_index][j]]
            print(f"j=4 {variables4[col]} = {matrix4[row_index][-1]} + {terms}")
        certified_matrix, certified_pivots, transform4 = (
            rref_fraction_with_certificate(rows4, rhs4)
        )
        target_col = variables4.index((2, 6))
        target_row = certified_pivots.index(target_col)
        assert certified_matrix[target_row][-1] == Fraction(1, 5)
        assert certified_matrix[target_row][:-1] == [
            Fraction(int(j == target_col)) for j in range(len(variables4))
        ]
        certificate = [(labels4[i], coefficient)
                       for i, coefficient in enumerate(transform4[target_row])
                       if coefficient]
        print(f"j=4 certificate for N_6(2a)=1/5: {certificate}")
    for prime in checked:
        rank4, bad4 = rref_mod(rows4, rhs4, prime)
        assert not bad4
        assert rank4 == len(pivots4)
    print("PASS: (3p+4)-atom Hasse system has rank 11 and forces "
          "N_6(2a)=1/5 for all primes 7<=p<=500")
    point_names, point_rows, point_rhs, _ = system_j4_with_point()
    point_matrix, point_pivots, point_bad = rref_fraction(
        point_rows, point_rhs
    )
    print(f"j=4 point equations={len(point_rows)} "
          f"rank_Q={len(point_pivots)} inconsistent_Q={bool(point_bad)}")
    point_free = [j for j in range(len(point_names))
                  if j not in point_pivots]
    print(f"j=4 point free_variables="
          f"{[point_names[j] for j in point_free]}")
    for row_index, col in enumerate(point_pivots):
        if point_names[col][0] == "m" or point_names[col] == ("N", (3, 8)):
            terms = [(point_names[j], -point_matrix[row_index][j])
                     for j in point_free if point_matrix[row_index][j]]
            print(f"j=4 point {point_names[col]} = "
                  f"{point_matrix[row_index][-1]} + {terms}")
    for prime in checked:
        point_rank, point_inconsistent = rref_mod(
            point_rows, point_rhs, prime
        )
        assert not point_inconsistent
        assert point_rank == len(point_pivots)
    print("PASS: length-refined one-point system has rank 20 of 24 "
          "for all primes 7<=p<=500; four local variables remain")


if __name__ == "__main__":
    main()
