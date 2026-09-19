"""Independent finite interface checks for the affine-independent star lemma.

This does not enumerate A_p sequences and does not prove the all-prime endpoint.
Run from any directory; the report is written next to this script.
"""

from collections import Counter
from itertools import combinations, combinations_with_replacement
import json
from math import comb
from pathlib import Path
import random


def add(*vs):
    return tuple(sum(v[d] for v in vs) for d in range(4))


def scale(k, v):
    return tuple(k * x for x in v)


def main():
    e = [tuple(int(i == j) for j in range(4)) for i in range(4)]
    b = add(*e[:3])
    core = {"y": (0, 0, 0, 0), **{f"b{i}": e[i] for i in range(3)}}
    vals = {"t": e[3]}
    for i in range(3):
        vals[f"u{i}"] = add(e[i], e[3])
        vals[f"v{i}"] = add(b, scale(-2, e[i]))
        vals[f"r{i}"] = add(b, scale(-1, e[i]))
        for j in range(3):
            if i != j:
                vals[f"n{i}{j}"] = add(e[3], scale(2, e[i]), scale(-1, e[j]))
    assert len(vals) == 16
    assert len(set(vals.values())) == 16
    assert not set(core.values()) & set(vals.values())
    primes = [11, 13, 17, 19, 23, 29, 31, 47, 101, 149, 251]
    for p in primes:
        coords = [tuple(x % p for x in v) for v in {**core, **vals}.values()]
        assert len(set(coords)) == 20

    # Enumerate all four-value multisets from the named alphabet from scratch.
    # Only keep the block types permitted by the star and the p>=11 argument.
    alphabet = {**core, **vals}
    target = add(b, e[3])
    allowed = []
    forbidden_actual_blocks = []
    for tup in combinations_with_replacement(alphabet, 4):
        counts = Counter(tup)
        if any(counts[x] > 1 for x in core):
            continue
        if add(*(alphabet[x] for x in tup)) != target:
            continue
        leaves = sum(counts[f"b{i}"] for i in range(3))
        permitted = (counts["y"] == 0 and leaves == 3) or (
            counts["y"] == 1 and leaves in (1, 2)
        )
        (allowed if permitted else forbidden_actual_blocks).append(dict(counts))

    # Positional multiplicities are counted with binomial coefficients, not
    # by treating repeated values as one position.
    rng = random.Random(20260919)
    degree_checks = 0
    for _ in range(100):
        capacities = {**{x: 1 for x in core}, **{x: rng.randrange(1, 8) for x in vals}}
        deg = dict.fromkeys(alphabet, 0)
        total = 0
        for block in allowed:
            ways = 1
            for x, k in block.items():
                ways *= comb(capacities[x], k) if capacities[x] >= k else 0
            total += ways
            for x, k in block.items():
                # Degree of one specified position with actual value x.
                prod = comb(capacities[x] - 1, k - 1) if capacities[x] >= k else 0
                for z, kz in block.items():
                    if z != x:
                        prod *= comb(capacities[z], kz) if capacities[z] >= kz else 0
                deg[x] += prod
        assert deg["t"] == 1 + sum(capacities[f"r{i}"] for i in range(3))
        for i in range(3):
            assert deg[f"u{i}"] == 1 + capacities[f"v{i}"]
            assert deg[f"v{i}"] == capacities[f"u{i}"] + sum(
                capacities[f"n{i}{j}"] for j in range(3) if j != i
            )
        m = sum(capacities[f"u{i}"] for i in range(3))
        assert sum(deg[f"b{i}"] for i in range(3)) - deg["y"] == 3 * capacities["t"] + m
        assert sum(capacities[x] * deg[x] for x in alphabet) == 4 * total
        degree_checks += 1

    # Exhaust all multiplicity triples obeying the actual cap and the core
    # congruence for the listed primes. Compute the lower bound by summing
    # separate disjoint classes before comparing with the simplified formula.
    arithmetic = []
    for p in primes:
        rho, s, h = (p + 1) // 2, (p - 1) // 2, p - 4
        checked = 0
        min_margin = None
        for m0 in range(h + 1):
            for m1 in range(h + 1):
                m2 = (rho + 2 - m0 - m1) % p
                if m2 > h:
                    continue
                ms = [m0, m1, m2]
                active = [m for m in ms if m]
                lower = s + sum(ms) + len(active) * s + s
                lower += sum((rho - m) % p for m in active)
                simplified = (len(active) + sum(m > rho for m in active) + 1) * p - 1
                assert lower == simplified
                assert lower >= 3 * p - 1
                margin = lower - (3 * p - 4)
                min_margin = margin if min_margin is None else min(min_margin, margin)
                checked += 1
        arithmetic.append({"p": p, "triples_checked": checked, "minimum_capacity_margin": min_margin})

    # An extra structural identity: all three v-types plus t themselves form
    # a forbidden no-core four-block, if all three u-types occur.
    assert add(vals["t"], *(vals[f"v{i}"] for i in range(3))) == target
    report = {
        "status": "PASS",
        "scope": "Finite coordinate, positional-incidence, and integer-capacity interfaces only; not an exhaustive A_p search.",
        "named_external_value_count": len(vals),
        "allowed_four_block_templates": allowed,
        "forbidden_actual_templates_in_named_alphabet": forbidden_actual_blocks,
        "random_positional_degree_checks": degree_checks,
        "arithmetic_checks": arithmetic,
        "total_triples_checked": sum(x["triples_checked"] for x in arithmetic),
    }
    out = Path(__file__).with_name("three_leaf_verification.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if "templates" not in k}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
