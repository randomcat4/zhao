from __future__ import annotations

from collections import Counter


P = 233
W = ((1, 0), (0, 1), (-1, -1))


def add(*vectors: tuple[int, int]) -> tuple[int, int]:
    return (
        sum(vector[0] for vector in vectors) % P,
        sum(vector[1] for vector in vectors) % P,
    )


def q0(vector: tuple[int, int]) -> int:
    alpha, beta = vector
    return (alpha * alpha - alpha * beta + beta * beta) % P


def orbit(seed: tuple[int, int]) -> set[tuple[int, int]]:
    def tau(point):
        alpha, beta = point
        return beta, alpha

    def kappa(point):
        alpha, beta = point
        return (beta - alpha) % P, (-alpha) % P

    seen = {seed}
    stack = [seed]
    while stack:
        point = stack.pop()
        for generator in (tau, kappa):
            image = generator(point)
            if image not in seen:
                seen.add(image)
                stack.append(image)
    return seen


def main() -> None:
    curve = {
        (alpha, beta)
        for alpha in range(P)
        for beta in range(P)
        if q0((alpha, beta)) == 3
    }
    original_tail_mask = 0b000111
    candidate_values = {size: Counter() for size in (1, 2, 3)}
    for j_mask in range(1, 1 << 3):
        size = j_mask.bit_count()
        inverse = pow(size, -1, P)
        for i_mask in range(1 << 3):
            numerator = add(
                *(W[index] for index in range(3) if i_mask >> index & 1),
                *(W[index] for index in range(3) if j_mask >> index & 1),
            )
            delta = (-numerator[0] * inverse) % P, (-numerator[1] * inverse) % P
            candidate_values[size][q0(delta)] += 1
    assert candidate_values == {
        1: Counter({0: 3, 1: 12, 3: 6, 4: 3}),
        2: Counter({0: 3, pow(4, -1, P): 12, 3 * pow(4, -1, P) % P: 6, 1: 3}),
        3: Counter({0: 2, pow(9, -1, P): 6}),
    }

    zero_masks = {}
    for delta in curve:
        labels = [
            *W,
            *(add(W[index], delta) for index in range(3)),
        ]
        masks = []
        for mask in range(1, 1 << 6):
            if mask == original_tail_mask:
                continue
            total = add(*(labels[index] for index in range(6) if mask >> index & 1))
            if total == (0, 0):
                masks.append(mask)
        zero_masks[delta] = masks

    exceptional = {delta for delta, masks in zero_masks.items() if masks}
    expected = {
        add(W[j], ((-W[i][0]) % P, (-W[i][1]) % P))
        for i in range(3)
        for j in range(3)
        if i != j
    }
    assert exceptional == expected
    assert len(exceptional) == 6
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            delta = add(W[j], ((-W[i][0]) % P, (-W[i][1]) % P))
            expected_mask = (1 << (3 + i)) | sum(
                1 << index for index in range(3) if index != j
            )
            assert zero_masks[delta] == [expected_mask]
    assert all(not zero_masks[delta] for delta in curve - exceptional)
    assert orbit(next(iter(exceptional))) == exceptional

    allowed = []
    for theta in range(P):
        for eta in range(P):
            c = (4 - theta) % P
            if c >= 230:
                allowed.append((theta, eta))
                continue
            allowed_eta = {
                0: {P - 2},
                1: {P - 2, P - 1},
                2: {P - 2, P - 1},
                3: {P - 2, P - 1},
                4: {P - 1},
            }.get(c, set())
            if eta in allowed_eta:
                allowed.append((theta, eta))

    fibres = {
        theta: sum(candidate_theta == theta for candidate_theta, _ in allowed)
        for theta in range(P)
    }
    assert len(allowed) == 707
    assert [fibres[theta] for theta in (4, 3, 2, 1, 0)] == [1, 2, 2, 2, 1]
    assert all(fibres[theta] == P for theta in (5, 6, 7))
    assert all(
        fibres[theta] == 0
        for theta in range(P)
        if theta not in {0, 1, 2, 3, 4, 5, 6, 7}
    )

    print("PASS three-h8 m=3 U-union-V short gate")
    print("curve generic/exceptional", len(curve - exceptional), len(exceptional))
    print("exceptional S3 orbits", 1)
    print("allowed actual lift pairs", len(allowed))


if __name__ == "__main__":
    main()
