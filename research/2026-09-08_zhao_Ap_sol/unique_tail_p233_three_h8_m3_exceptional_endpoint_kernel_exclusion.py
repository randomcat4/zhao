from __future__ import annotations


P = 233
W = ((1, 0), (0, 1), (-1, -1))


def add(*vectors):
    return (
        sum(vector[0] for vector in vectors) % P,
        sum(vector[1] for vector in vectors) % P,
    )


def q0(vector):
    alpha, beta = vector
    return (alpha * alpha - alpha * beta + beta * beta) % P


def mask_sum(labels, mask):
    return add(*(labels[index] for index in range(6) if mask >> index & 1))


def main() -> None:
    curve = {
        (alpha, beta)
        for alpha in range(P)
        for beta in range(P)
        if q0((alpha, beta)) == 3
    }
    exceptional = {
        add(W[j], ((-W[i][0]) % P, (-W[i][1]) % P))
        for i in range(3)
        for j in range(3)
        if i != j
    }
    e_masks = {
        (1 << i) | sum(1 << (3 + index) for index in range(3) if index != i)
        for i in range(3)
    }

    for delta in curve:
        labels = [*W, *(add(W[index], delta) for index in range(3))]
        target = add(delta, delta)
        masks = {
            mask
            for mask in range(1, 1 << 6)
            if mask.bit_count() <= 3 and mask_sum(labels, mask) == target
        }
        if delta not in exceptional:
            assert masks == e_masks
            continue
        expected_extra = set()
        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                if delta == add(W[j], ((-W[i][0]) % P, (-W[i][1]) % P)):
                    expected_extra.add(
                        (1 << (3 + j))
                        | sum(1 << index for index in range(3) if index != i)
                    )
        assert len(expected_extra) == 1
        assert masks == e_masks | expected_extra

    gate_a = {
        (theta, eta)
        for theta in range(P)
        for eta in range(P)
        if (theta == 0 and eta == 0) or theta in {230, 231, 232}
    }

    def gate_r_allows(theta, eta):
        c = (4 - theta) % P
        if c >= 230:
            return True
        allowed_eta = {
            0: {P - 2},
            1: {P - 2, P - 1},
            2: {P - 2, P - 1},
            3: {P - 2, P - 1},
            4: {P - 1},
        }.get(c, set())
        return eta in allowed_eta

    gate_r = {
        (theta, eta)
        for theta in range(P)
        for eta in range(P)
        if gate_r_allows(theta, eta)
    }
    assert len(gate_a) == 700
    assert len(gate_r) == 707
    assert not gate_a & gate_r

    remaining = curve - exceptional
    assert len(remaining) == 228
    assert len(remaining) // 6 == 38
    assert len(remaining) // 2 == 114

    print("PASS three-h8 m=3 exceptional endpoint-kernel exclusion")
    print("curve before/after", len(curve), len(remaining))
    print("unpointed orbits before/after", 39, 38)
    print("pointed orbits before/after", 117, 114)
    print("gate sizes/intersection", len(gate_a), len(gate_r), len(gate_a & gate_r))


if __name__ == "__main__":
    main()
