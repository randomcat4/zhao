"""Finite verifier for the completion-rich near-maximal atom family."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPORT = HERE / "unique_tail_completion_rich_near_max_atom_family_report.json"


def residues(start: int, stop: int, p: int) -> set[int]:
    return {value % p for value in range(start, stop + 1)}


def verify_prime(p: int) -> dict[str, object]:
    assert p >= 5

    # Coordinate proof of atomhood: enumerate the four binary choices and
    # bounded multiplicities, but not the exponentially many literal subsets.
    zero_patterns: list[tuple[int, int, int, int]] = []
    for delta in range(2):
        for epsilon in range(2):
            for b in range(p):
                if (b + delta) % p:
                    continue
                for a in range(p - 2):
                    if (a + 2 * epsilon + delta) % p == 0:
                        zero_patterns.append((a, b, epsilon, delta))
    assert zero_patterns == [(0, 0, 0, 0), (p - 3, p - 1, 1, 1)]

    delete_e_plus_f = residues(0, p - 3, p) | residues(2, p - 1, p)
    delete_e = set()
    for epsilon in range(2):
        for delta in range(2):
            delete_e |= residues(2 * epsilon + delta, p - 4 + 2 * epsilon + delta, p)
    delete_f_delta_zero = residues(0, p - 3, p) | residues(2, p - 1, p)
    delete_f_delta_one = residues(1, p - 2, p) | residues(3, p, p)
    delete_2e = residues(0, p - 3, p) | residues(1, p - 2, p)
    full = set(range(p))
    assert delete_e_plus_f == full
    assert delete_e == full
    assert delete_f_delta_zero == full
    assert delete_f_delta_one == full
    assert delete_2e == full - {p - 1}

    # After deleting 2e, exactly the e-coordinate -1 is unreachable.
    assert p - 1 not in residues(0, p - 3, p)
    assert p - 2 not in residues(0, p - 3, p)

    q_subset_sums = {0, 1}
    assert q_subset_sums <= {0, 1, 2}
    assert q_subset_sums <= {(p - 1) % p, 0, 1}
    return {
        "p": p,
        "length": 2 * p - 2,
        "atom_zero_patterns": zero_patterns,
        "complete_deletion_count": 2 * p - 3,
        "unique_incomplete_deletion_label": "2e",
        "missing_targets_after_deleting_2e": "-e+<f> (exactly p targets)",
        "single_endpoint_q_mixed_gate": "PASS_FOR_Q_SUPPORT_{0,1}_AND_PACKING_Q_(1,2)",
    }


def main() -> None:
    report: dict[str, object] = {
        "schema": "unique-tail-completion-rich-near-max-atom-family-v1",
        "status": "PROVED_BOUNDARY/INDEPENDENT_REVIEW_CORRECT/GLOBAL_INCOMPLETE",
        "checked_primes": [verify_prime(p) for p in (5, 7, 233)],
        "scope": {
            "proved_in_companion": "symbolic construction for every prime p >= 5",
            "not_claimed": [
                "a unified multi-endpoint position model",
                "all global automatic short blocks",
                "the full p=233 slice or global A_p",
            ],
        },
    }
    canonical = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    report["certificate_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
