#!/usr/bin/env python3
"""Finite checks for p_minus_four_two_tail_exchange.md.

The script checks the small core-count algebra, the sharp nesting residue
classification, and the formal two-tail interface assignment for every prime
11 <= p <= 500.  It does not construct a global atom Z.
"""


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


PRIMES = tuple(p for p in range(11, 501) if is_prime(p))


def add(u, v, p):
    return tuple((a + b) % p for a, b in zip(u, v))


def sub(u, v, p):
    return tuple((a - b) % p for a, b in zip(u, v))


def scale(c, u, p):
    return tuple(c * a % p for a in u)


def feasible_k(m, b, bp):
    return tuple(range(max(0, b + bp - m), min(b, bp) + 1))


def verify_core_compression(p):
    m = p - 4
    for b in range(1, 8):
        for bp in range(1, 8):
            ks = feasible_k(m, b, bp)
            k0 = max(0, b + bp - m)
            assert ks[0] == k0

            all_d = set()
            for k in ks:
                direct_d = {
                    beta - alpha
                    for alpha in range(b - k + 1)
                    for beta in range(bp - k + 1)
                }
                interval_d = set(range(-(b - k), bp - k + 1))
                assert direct_d == interval_d
                all_d.update(direct_d)

                # Direct core count agrees with b* = b' - d.
                for alpha in range(b - k + 1):
                    for beta in range(bp - k + 1):
                        d = beta - alpha
                        direct_bstar = k + alpha + (bp - k - beta)
                        assert direct_bstar == bp - d
                        assert 0 <= direct_bstar <= m

            compressed = set(range(-b + k0, bp - k0 + 1))
            assert all_d == compressed


def verify_length_formula():
    # These variables are just cardinalities; the identity is integral.
    for ell in (6, 7, 8):
        for b in range(1, ell):
            usize = ell - b
            for ellp in (6, 7, 8):
                for bp in range(1, ellp):
                    upsize = ellp - bp
                    for wsize in range(min(usize, upsize) + 1):
                        rsize = usize - wsize
                        ssize = upsize - wsize
                        for esize in range(rsize + 1):
                            for fsize in range(ssize + 1):
                                for d in range(-b, bp + 1):
                                    bstar = bp - d
                                    direct = (
                                        bstar + wsize + esize
                                        + (ssize - fsize)
                                    )
                                    formula = ellp - d + esize - fsize
                                    assert direct == formula


def verify_nesting_residues(p):
    # For U' proper-subset U, sigma(U-U')=(b'-b)x.
    for b in range(1, 8):
        for bp in range(1, 8):
            if b == bp:
                allowed = False
            else:
                residue = (bp - b) % p
                allowed = residue in (1, 2, 3)
            theorem_form = bp > b and 1 <= bp - b <= 3
            assert allowed == theorem_form


def verify_local_twin_state(p):
    m = p - 4
    b = bp = 4
    ell = ellp = 6
    assert b <= m

    q = (1, 0, 0)
    q4 = (1, 0, 0, 0)
    x = q4
    w = ((-4) % p, (-1) % p, 0, 3)
    r = (0, 1, 0, 0)
    s = r

    # Both tails have actual sum 3a - 4x and quotient sum -4q.
    tail_sum = add(w, r, p)
    target = ((-4) % p, 0, 0, 3)
    assert tail_sum == target == add(w, s, p)

    # Their common T-part is w and is quotient-nonzero.
    wq = w[:3]
    assert wq != (0, 0, 0)

    # All realizable core intersections have nonzero quotient intersection.
    for k in feasible_k(m, b, bp):
        intersection_sum = add(wq, scale(k, q, p), p)
        assert intersection_sum != (0, 0, 0)

    k0 = max(0, b + bp - m)
    d_interval = range(-b + k0, bp - k0 + 1)

    # E and F are encoded by bits, since R={r}, S={s}.
    exchange_hits = []
    for ebit in (0, 1):
        for fbit in (0, 1):
            e = r if ebit else (0, 0, 0, 0)
            f = s if fbit else (0, 0, 0, 0)
            qdiff = sub(e[:3], f[:3], p)
            for d in d_interval:
                if qdiff != scale(d, q, p):
                    continue
                # Only d=0 can occur, and actual defect delta is zero.
                assert d == 0
                defect = sub(sub(e, f, p), scale(d, x, p), p)
                assert defect == (0, 0, 0, 0)
                bstar = bp - d
                length = ellp - d + ebit - fbit
                assert bstar == 4
                assert length == 6
                # Empty pair returns U'; full pair returns U.
                assert ebit == fbit
                exchange_hits.append((ebit, fbit, d))

    assert exchange_hits == [(0, 0, 0), (1, 1, 0)]
    assert 2 <= p - 4  # multiplicity of the repeated value r=s is legal.


def main():
    verify_length_formula()
    for p in PRIMES:
        verify_core_compression(p)
        verify_nesting_residues(p)
        verify_local_twin_state(p)

    print(f"PASS all {len(PRIMES)} primes 11 <= p <= 500")
    print("PASS exact k-to-d compression and exchange length formula")
    print("PASS sharp nested-tail residue classification")
    print("PASS formal pair-interface twin-tail assignment")
    print("SCOPE no induced short-spectrum audit, global T/B, complement atoms, or atom Z")


if __name__ == "__main__":
    main()
