#!/usr/bin/env python3
r"""Exact F_p probe for the exceptional unique-positive-F3-tail types.

The system consists of the 21 necessary aggregate Hasse equations:
three zero-order equations, six pure-X equations, six equations summed
over T, and six equations summed over Q=Y\T.  For every positive-core F3
tail type except the prescribed unique one, both its count N and its
T-incidence J are fixed to zero; the unique type has N=1 and J=j.

A compatible vector is only an F_p aggregate certificate.  It is not a
nonnegative incidence design and does not realize quotient/actual labels.
"""

from __future__ import annotations

from math import comb
from time import perf_counter


WINDOWS = {
    1: tuple(range(2, 7)),
    2: tuple(range(4, 8)),
    3: tuple(range(6, 9)),
}

EXCEPTIONAL_TYPES = (
    (11, 7, 2),
    (13, 6, 3),
    (13, 8, 3),
    (19, 6, 1),
    (19, 8, 1),
    (23, 6, 3),
    (23, 8, 3),
    (43, 7, 3),
    (101, 6, 2),
    (101, 8, 2),
    (233, 7, 4),
    (467, 7, 5),
    (701, 6, 4),
    (701, 8, 4),
    (1399, 8, 5),
    (2521, 8, 6),
)

POINT_NUM_DEN = {1: (-3, 4), 2: (3, 10), 3: (-1, 20)}


def inv(value: int, prime: int) -> int:
    return pow(value % prime, -1, prime)


def frac(number: int, denominator: int, prime: int) -> int:
    return number * inv(denominator, prime) % prime


def c(n: int, k: int, prime: int) -> int:
    if k < 0 or k > n:
        return 0
    return comb(n, k) % prime


def all_variable_keys():
    keys = []
    for family in (1, 2):
        for length in WINDOWS[family]:
            for b in range(length):
                keys.append(("N", family, length, b))
                keys.append(("J", family, length, b))
    # Unique-tail arithmetic fixes every positive-core F3 variable, so only
    # the three zero-core count/incidence pairs remain free.
    for length in WINDOWS[3]:
        keys.append(("N", 3, length, 0))
        keys.append(("J", 3, length, 0))
    return tuple(keys)


VARIABLES = all_variable_keys()
INDEX = {key: index for index, key in enumerate(VARIABLES)}


def allowed_j_values(length: int, b: int, t_size: int):
    r = length - b
    upper = min(r, t_size - 1)  # nonempty proper T-part
    if b >= 4:
        upper = min(upper, r - 1)  # the known U not-subset-T boundary
    if r == 2:
        return (1,)  # exact two-point-tail split
    return tuple(range(1, upper + 1))


def build_system(prime: int, unique_length: int, unique_b: int,
                 t_size: int, unique_j: int):
    m = prime - 4
    q_size_mod = (8 - t_size) % prime
    point = {
        family: frac(*POINT_NUM_DEN[family], prime)
        for family in (1, 2, 3)
    }
    equations = []
    names = []

    def add_equation(name, rhs):
        row = [0] * len(VARIABLES)
        equations.append([row, rhs % prime])
        names.append(name)
        return row

    def add_term(row, kind, family, length, b, coefficient):
        coefficient %= prime
        if family != 3 or b == 0:
            row[INDEX[(kind, family, length, b)]] = (
                row[INDEX[(kind, family, length, b)]] + coefficient
            ) % prime
            return 0
        # All positive-core F3 variables are fixed.  N=1,J=unique_j only for
        # the prescribed type and zero otherwise.
        if (length, b) != (unique_length, unique_b):
            return 0
        fixed = 1 if kind == "N" else unique_j
        return coefficient * fixed % prime

    # A linear form builder moves fixed positive-F3 contributions to rhs.
    def form(name, rhs, terms):
        row = add_equation(name, rhs)
        fixed = 0
        for term in terms:
            fixed += add_term(row, *term)
        equations[-1][1] = (equations[-1][1] - fixed) % prime

    # 3 zero-order equations and 3 pure-X point equations.
    for family in (1, 2, 3):
        form(
            f"zero_{family}",
            0,
            (
                ("N", family, length, b,
                 (-1) ** (length - 1) * c(m, b, prime))
                for length in WINDOWS[family] for b in range(length)
            ),
        )
        form(
            f"x_point_{family}",
            point[family],
            (
                ("N", family, length, b,
                 (-1) ** (length - 1) * c(m - 1, b - 1, prime))
                for length in WINDOWS[family] for b in range(1, length)
            ),
        )

    # Two pure-X pair equations.
    for label, family_coeffs, rhs in (
        ("x_pair_12", {1: 8, 2: 10}, 3),
        ("x_pair_13", {1: 2, 3: -10}, 1),
    ):
        form(
            label,
            rhs,
            (
                ("N", family, length, b,
                 family_coeffs.get(family, 0)
                 * (-1) ** length * c(m - 2, b - 2, prime))
                for family in (1, 2, 3)
                for length in WINDOWS[family]
                for b in range(2, length)
            ),
        )

    # One pure-X triple equation.
    form(
        "x_triple",
        -1,
        (
            ("N", family, length, b,
             {1: 4, 2: 10, 3: 20}[family]
             * (-1) ** (length - 1) * c(m - 3, b - 3, prime))
            for family in (1, 2, 3)
            for length in WINDOWS[family]
            for b in range(3, length)
        ),
    )

    # Six equations summed over T, using J=sum_U |U intersect T|.
    for family in (1, 2, 3):
        form(
            f"T_point_{family}",
            t_size * point[family],
            (
                ("J", family, length, b,
                 (-1) ** (length - 1) * c(m, b, prime))
                for length in WINDOWS[family] for b in range(length)
            ),
        )
    for label, family_coeffs, rhs in (
        ("T_pair_12", {1: 8, 2: 10}, 3 * t_size),
        ("T_pair_13", {1: 2, 3: -10}, t_size),
    ):
        form(
            label,
            rhs,
            (
                ("J", family, length, b,
                 family_coeffs.get(family, 0)
                 * (-1) ** length * c(m - 1, b - 1, prime))
                for family in (1, 2, 3)
                for length in WINDOWS[family]
                for b in range(1, length)
            ),
        )
    form(
        "T_triple",
        -t_size,
        (
            ("J", family, length, b,
             {1: 4, 2: 10, 3: 20}[family]
             * (-1) ** (length - 1) * c(m - 2, b - 2, prime))
            for family in (1, 2, 3)
            for length in WINDOWS[family]
            for b in range(2, length)
        ),
    )

    # Six equations summed over Q.  Its incidence is r*N-J.
    def q_terms(kind_order, family, coefficient):
        for length in WINDOWS[family]:
            for b in range(kind_order, length):
                r = length - b
                yield ("N", family, length, b, coefficient(length, b) * r)
                yield ("J", family, length, b, -coefficient(length, b))

    for family in (1, 2, 3):
        form(
            f"Q_point_{family}",
            q_size_mod * point[family],
            q_terms(
                0,
                family,
                lambda length, b:
                (-1) ** (length - 1) * c(m, b, prime),
            ),
        )
    for label, family_coeffs, rhs in (
        ("Q_pair_12", {1: 8, 2: 10}, 3 * q_size_mod),
        ("Q_pair_13", {1: 2, 3: -10}, q_size_mod),
    ):
        terms = []
        for family in (1, 2, 3):
            fc = family_coeffs.get(family, 0)
            terms.extend(q_terms(
                1,
                family,
                lambda length, b, fc=fc:
                fc * (-1) ** length * c(m - 1, b - 1, prime),
            ))
        form(label, rhs, terms)
    terms = []
    for family in (1, 2, 3):
        fc = {1: 4, 2: 10, 3: 20}[family]
        terms.extend(q_terms(
            2,
            family,
            lambda length, b, fc=fc:
            fc * (-1) ** (length - 1) * c(m - 2, b - 2, prime),
        ))
    form("Q_triple", -q_size_mod, terms)

    assert len(equations) == 21
    return equations, names


def rref_solve(equations, prime):
    matrix = [row[:] + [rhs] for row, rhs in equations]
    pivot_columns = []
    pivot_row = 0
    for column in range(len(VARIABLES)):
        selected = next(
            (row for row in range(pivot_row, len(matrix))
             if matrix[row][column] % prime),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        factor = inv(matrix[pivot_row][column], prime)
        matrix[pivot_row] = [value * factor % prime for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            factor = matrix[row][column] % prime
            if factor:
                matrix[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    for row in matrix:
        if all(value % prime == 0 for value in row[:-1]) and row[-1] % prime:
            return None, len(pivot_columns)
    solution = [0] * len(VARIABLES)
    for row_index, column in enumerate(pivot_columns):
        solution[column] = matrix[row_index][-1] % prime
    return solution, len(pivot_columns)


def verify_solution(equations, solution, prime):
    for row, rhs in equations:
        assert sum(a * x for a, x in zip(row, solution)) % prime == rhs % prime


def support_certificate(solution):
    return tuple(
        (VARIABLES[index], value)
        for index, value in enumerate(solution)
        if value
    )


def main():
    started = perf_counter()
    summaries = []
    for prime, length, b in EXCEPTIONAL_TYPES:
        m = prime - 4
        assert (
            (-1) ** (length - 1) * c(m - 1, b - 1, prime)
            - frac(-1, 20, prime)
        ) % prime == 0
        all_cases = []
        attempted = 0
        for t_size in (6, 7, 8):
            for j in allowed_j_values(length, b, t_size):
                attempted += 1
                equations, names = build_system(prime, length, b, t_size, j)
                solution, rank = rref_solve(equations, prime)
                if solution is not None:
                    verify_solution(equations, solution, prime)
                    all_cases.append((t_size, j, rank, support_certificate(solution)))
        assert len(all_cases) == attempted, (prime, length, b, attempted, all_cases)
        assert all(rank == 20 for _, _, rank, _ in all_cases)
        # The first deterministic witness is always s=6,j=1 in this table.
        witness = all_cases[0]
        assert witness[0:2] == (6, 1)
        summaries.append((prime, length, b, len(all_cases), witness))

    assert len(summaries) == 16
    assert len({prime for prime, _, _ in EXCEPTIONAL_TYPES}) == 11
    print("PASS all 16 exceptional (p,length,b) types are F_p aggregate-compatible")
    for prime, length, b, count, witness in summaries:
        t_size, j, rank, support = witness
        print(
            f"  p={prime:4d} type=({length},{b}) "
            f"compatible_cases={count:2d} witness=(s={t_size},j={j}) "
            f"rank={rank:2d} support={len(support):2d}"
        )
        print("    " + "; ".join(f"{key}={value}" for key, value in support))
    elapsed = perf_counter() - started
    print("SCOPE exact 21-equation F_p aggregate relaxation only")
    print("SCOPE no nonnegative incidence design or quotient/actual-value tail realized")
    print(f"ELAPSED_SECONDS={elapsed:.3f}")


if __name__ == "__main__":
    main()
