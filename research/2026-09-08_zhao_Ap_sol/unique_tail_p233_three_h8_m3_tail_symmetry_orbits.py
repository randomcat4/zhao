from __future__ import annotations

from collections import Counter


P = 233


def tau(point: tuple[int, int]) -> tuple[int, int]:
    alpha, beta = point
    return beta, alpha


def kappa(point: tuple[int, int]) -> tuple[int, int]:
    alpha, beta = point
    return (beta - alpha) % P, (-alpha) % P


def orbit(seed: tuple[int, int], generators) -> frozenset[tuple[int, int]]:
    seen = {seed}
    stack = [seed]
    while stack:
        point = stack.pop()
        for generator in generators:
            image = generator(point)
            if image not in seen:
                seen.add(image)
                stack.append(image)
    return frozenset(seen)


def main() -> None:
    points = {
        (alpha, beta)
        for alpha in range(P)
        for beta in range(P)
        if (alpha * alpha - alpha * beta + beta * beta - 3) % P == 0
    }
    assert len(points) == 234

    unpointed = {orbit(point, (tau, kappa)) for point in points}
    assert all(candidate <= points for candidate in unpointed)
    assert Counter(map(len, unpointed)) == Counter({6: 39})

    # After fixing endpoint 1, its stabilizer exchanges tails 2 and 3.
    def swap_23(point: tuple[int, int]) -> tuple[int, int]:
        alpha, beta = point
        return (alpha - beta) % P, (-beta) % P

    pointed = {orbit(point, (swap_23,)) for point in points}
    assert all(candidate <= points for candidate in pointed)
    assert Counter(map(len, pointed)) == Counter({2: 117})

    fixed_transposition = sum(
        alpha == beta or alpha == 0 or beta == 0 for alpha, beta in points
    )
    fixed_three_cycle = sum(kappa(point) == point for point in points)
    assert fixed_transposition == fixed_three_cycle == 0

    print("PASS three-h8 m=3 tail-symmetry orbits")
    print("curve points", len(points))
    print("unpointed S3 orbits", len(unpointed))
    print("pointed stabilizer orbits", len(pointed))
    print("nontrivial fixed points", fixed_transposition + fixed_three_cycle)


if __name__ == "__main__":
    main()
