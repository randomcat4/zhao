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


def main() -> None:
    points = [
        (alpha, beta)
        for alpha in range(P)
        for beta in range(P)
        if (alpha * alpha - alpha * beta + beta * beta - 3) % P == 0
    ]
    assert len(points) == P + 1 == 234
    assert all(alpha and beta and alpha != beta for alpha, beta in points)

    inv2 = pow(2, -1, P)
    # Ten triangular-grid points are unisolvent for total degree at most three.
    probes = [(x, y) for x in range(4) for y in range(4 - x)]
    for alpha, beta in points:
        g = pow((alpha - beta) % P, -1, P)
        f = (-2 - g * beta) * pow(3 * alpha, -1, P) % P
        i = (-2 + g * alpha) * pow(3 * beta, -1, P) % P
        assert coeff(-alpha * inv2 % P, -beta * inv2 % P, f, i, g) == 0
        for x, y in probes:
            assert coeff(-alpha - x, -beta - y, f, i, g) == (-coeff(x, y, f, i, g)) % P
        for x, y in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)):
            assert coeff(x, y, f, i, g) == 0

    print("PASS three-h8 m=3 cubic-core curve")
    print("curve points", len(points))
    print("excluded-line points", sum(alpha == 0 or beta == 0 or alpha == beta for alpha, beta in points))


if __name__ == "__main__":
    main()
