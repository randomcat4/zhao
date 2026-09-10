from __future__ import annotations

from itertools import permutations, product


P = 233
W = ((1, 0), (0, 1), (-1, -1))
PAIRS = ((0, 1), (0, 2), (1, 2))
EVEN_MONOMIALS = (
    (0, 0),
    (2, 0),
    (1, 1),
    (0, 2),
    (4, 0),
    (3, 1),
    (2, 2),
    (1, 3),
    (0, 4),
)


def valid(state: tuple[int, int, int, int]) -> bool:
    a, b, c, d = state
    return (
        a + b + d <= 6
        and a + c + d <= 6
        and b + c + d <= 6
        and max(a + d, b + d, c + d) <= 5
    )


def act(state, permutation):
    a, b, c, d = state
    values = {(0, 1): a, (0, 2): b, (1, 2): c}
    inverse = {permutation[index]: index for index in range(3)}
    image = []
    for pair in PAIRS:
        old_pair = tuple(sorted((inverse[pair[0]], inverse[pair[1]])))
        image.append(values[old_pair])
    return *image, d


def canonical(state, group):
    return min(act(state, permutation) for permutation in group)


def evaluate_monomials(point):
    x, y = point
    return [pow(x % P, a, P) * pow(y % P, b, P) % P for a, b in EVEN_MONOMIALS]


def determinant(matrix):
    matrix = [row[:] for row in matrix]
    result = 1
    for column in range(len(matrix)):
        pivot = next(
            (row for row in range(column, len(matrix)) if matrix[row][column] % P),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        value = matrix[column][column] % P
        result = result * value % P
        inverse = pow(value, -1, P)
        matrix[column] = [entry * inverse % P for entry in matrix[column]]
        for row in range(column + 1, len(matrix)):
            factor = matrix[row][column] % P
            if factor:
                matrix[row] = [
                    (left - factor * right) % P
                    for left, right in zip(matrix[row], matrix[column])
                ]
    return result % P


def q1(point):
    x, y = point
    half = pow(2, -1, P)
    return (half * x * x - x * y - half * x**4 + x**3 * y) % P


def q2(point):
    x, y = point
    return (2 * x * y - y * y - 2 * x * y**3 + y**4) % P


def add(left, right):
    return (left[0] + right[0]) % P, (left[1] + right[1]) % P


def main() -> None:
    labelled = [
        state
        for state in product(range(7), repeat=4)
        if valid(state) and 450 + state[0] + state[1] + state[2] + 2 * state[3] == 460
    ]
    s3 = list(permutations(range(3)))
    orbits = {canonical(state, s3) for state in labelled}
    assert len(labelled) == 8
    assert orbits == {
        (0, 0, 0, 5),
        (0, 1, 1, 4),
        (1, 1, 2, 3),
        (2, 2, 2, 2),
    }

    fixed_points = [
        (0, 0),
        *W,
        ((W[0][0] - W[1][0]) % P, (W[0][1] - W[1][1]) % P),
        ((W[0][0] - W[2][0]) % P, (W[0][1] - W[2][1]) % P),
        ((W[1][0] - W[2][0]) % P, (W[1][1] - W[2][1]) % P),
    ]
    assert all(q1(point) == q2(point) == 0 for point in fixed_points)
    minor_columns = (0, 1, 2, 3, 4, 6, 7)
    minor = [
        [evaluate_monomials(point)[column] for column in minor_columns]
        for point in fixed_points
    ]
    assert determinant(minor) == 144

    generic = boundary = survivors = 0
    for x in range(P):
        for y in range(P):
            if (x, y) == (0, 0):
                continue
            t = (x, y)
            rows = [
                (q1(add(t, sign_w)), q2(add(t, sign_w)))
                for w in W
                for sign_w in (w, ((-w[0]) % P, (-w[1]) % P))
            ]
            rank_two = any(
                (left[0] * right[1] - left[1] * right[0]) % P
                for left in rows
                for right in rows
            )
            if x and y and x != y:
                generic += 1
                assert rank_two
                continue
            boundary += 1
            assert not rank_two
            nonzero_row = next(row for row in rows if row != (0, 0))
            at_t = q1(t), q2(t)
            assert (at_t[0] * nonzero_row[1] - at_t[1] * nonzero_row[0]) % P == 0
            # Every vector in the row kernel also annihilates evaluation at t.
            kernel = nonzero_row[1], (-nonzero_row[0]) % P
            if (
                all((row[0] * kernel[0] + row[1] * kernel[1]) % P == 0 for row in rows)
                and (at_t[0] * kernel[0] + at_t[1] * kernel[1]) % P
            ):
                survivors += 1

    assert generic == (P - 1) * (P - 2) == 53592
    assert boundary == 3 * (P - 1) == 696
    assert survivors == 0

    print("PASS three-h8 m=4 O0 even-quartic exclusion")
    print("labelled/orbits at m=4", len(labelled), len(orbits))
    print("generic/boundary centers", generic, boundary)
    print("survivors", survivors)


if __name__ == "__main__":
    main()
