"""Check the integral group-ring p^2 identity on explicitly recorded inputs."""

from itertools import product
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]


def multiply_group_ring(sequence, p):
    elements = list(product(range(p), repeat=4))
    index = {g: i for i, g in enumerate(elements)}
    coefficients = [0] * len(elements)
    coefficients[index[(0, 0, 0, 0)]] = 1
    for g in sequence:
        updated = coefficients.copy()
        for i, h in enumerate(elements):
            dest = tuple((h[j] + g[j]) % p for j in range(4))
            updated[index[dest]] -= coefficients[i]
        coefficients = [x % (p * p) for x in updated]
    return coefficients


def finite_field_product_sum(sequence, p):
    value = 0
    for t in product(range(p), repeat=4):
        term = 1
        for g in sequence:
            term = term * sum(t[j] * g[j] for j in range(4)) % p
        value += term
    return value % p


def main():
    rng = random.Random(20260904)
    records = []
    for p in [5, 7]:
        basis = [tuple(int(i == j) for i in range(4)) for j in range(4)]
        n = 5 * (p - 1)
        socle_nonzero = [basis[0]] * (2 * (p - 1))
        for b in basis[1:]:
            socle_nonzero.extend([b] * (p - 1))
        bounded_multiplicity = []
        for b in basis + [(1, 1, 1, 1)]:
            bounded_multiplicity.extend([b] * (p - 1))
        random_sequence = [tuple(rng.randrange(p) for _ in range(4)) for _ in range(n)]
        for name, sequence in [("sharp_socle", socle_nonzero),
                               ("bounded_multiplicity", bounded_multiplicity),
                               ("recorded_random", random_sequence)]:
            c = finite_field_product_sum(sequence, p)
            coeffs = multiply_group_ring(sequence, p)
            expected = (-p * c) % (p * p)
            assert all(v == expected for v in coeffs)
            extended = sequence + [(2, 1, 0, 3)]
            extension_coeffs = multiply_group_ring(extended, p)
            assert not any(extension_coeffs)
            records.append({"p": p, "name": name, "sequence": sequence,
                            "length": n, "c_mod_p": c,
                            "all_group_coefficients_mod_p2": expected,
                            "extension": extended[-1],
                            "all_extension_coefficients_zero_mod_p2": True})
    path = ROOT / "evidence" / "algebra_padic_checks.json"
    path.write_text(json.dumps({"status": "FINITE_SANITY_CHECK_NOT_GENERAL_PROOF",
                                "records": records}, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(path), "cases_checked": len(records),
                      "all_passed": True}))


if __name__ == "__main__":
    main()
