from __future__ import annotations


P = 233


def coeff(x: int, y: int, f: int, i: int, g: int) -> int:
    return (
        1
        - x * x
        + x * y
        - y * y
        + f * (x**3 - x)
        + i * (y**3 - y)
        + g * (x * x * y - x * y * y)
    ) % P


def parameters(alpha: int, beta: int) -> tuple[int, int, int]:
    g = pow((alpha - beta) % P, -1, P)
    f = (-2 - g * beta) * pow(3 * alpha, -1, P) % P
    i = (-2 + g * alpha) * pow(3 * beta, -1, P) % P
    return f, i, g


def homogeneous(direction: tuple[int, int], f: int, i: int, g: int) -> int:
    x, y = direction
    return (f * x**3 + i * y**3 + g * (x * x * y - x * y * y)) % P


def main() -> None:
    points = [
        (alpha, beta)
        for alpha in range(P)
        for beta in range(P)
        if (alpha * alpha - alpha * beta + beta * beta - 3) % P == 0
    ]
    data = {
        point: parameters(*point)
        for point in points
    }

    assert [
        point
        for point, (f, i, g) in data.items()
        if homogeneous((1, 2), f, i, g) == 0
    ] == []
    assert {
        point
        for point, (f, i, g) in data.items()
        if homogeneous((0, 1), f, i, g) == 0
    } == {(2, 1), (P - 2, P - 1)}
    assert {
        point
        for point, (f, i, g) in data.items()
        if homogeneous((-1, -1), f, i, g) == 0
    } == {(1, P - 1), (P - 1, 1)}

    # Normalize i=1, g=w_2=f and h=w_3=-e-f.
    survivors = []
    for m in (P - 3, P - 2, P - 1):
        n = 2 * P - 3 - m
        for alpha, beta in points:
            if (n - (1 + alpha)) % P:
                continue
            f, i, g = data[(alpha, beta)]
            if m >= P - 2 and homogeneous((0, 1), f, i, g):
                continue
            if m == P - 3 and (3 - beta) % P not in {1, 2}:
                continue
            survivors.append((m, alpha, beta))
    assert survivors == [(P - 3, P - 1, 1), (P - 2, P - 2, P - 1)]

    # Ten points are unisolvent for polynomials of total degree at most three.
    probes = [(x, y) for x in range(4) for y in range(4 - x)]
    for alpha, beta in points:
        f, i, g = data[(alpha, beta)]
        for x, y in probes:
            second_difference = (
                coeff(x, y, f, i, g)
                - coeff(x, y - 1, f, i, g)
                - coeff(x + 1, y + 1, f, i, g)
                + coeff(x + 1, y, f, i, g)
            ) % P
            assert second_difference == (1 + 2 * y * pow(beta, -1, P)) % P

    for a_zero in range(P):
        reachable = {(2 - a_zero + r) % P for r in range(P - 1)}
        assert (1 - a_zero) % P not in reachable

    print("PASS three-h8 m=3 complete-witness cancellation line")
    print("curve points", len(points))
    print("two-line-tail homogeneous survivors", 0)
    print("one-heavy-tail Property-B survivors", len(survivors))
    print("cancellation-line targets", P)


if __name__ == "__main__":
    main()
