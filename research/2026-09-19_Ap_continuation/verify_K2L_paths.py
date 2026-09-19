"""Standalone standard-library replay; does not import the search/generator."""
from itertools import permutations
from pathlib import Path
import gzip
import hashlib
import json


def main():
    path = Path(__file__).with_name("K2L_path_certificates.jsonl.gz")
    seen = set()
    max_residual = 0
    with gzip.open(path, "rt") as f:
        for line in f:
            q = json.loads(line)
            n, pos, loop = q["n"], q["positions"], q["loop"]
            assert 1 <= n <= 14 and "x" in pos and set(pos) <= {"x", "v", "z"}
            assert len(set(pos.values())) == len(pos) and all(0 <= v < n for v in pos.values())
            key = (n, tuple(sorted(pos.items())), loop)
            assert key not in seen
            seen.add(key)
            # Unknowns are four times the actual multiplicities. Rebuild
            # equations from position degree residues, with loop correction.
            rhs = [2] * n
            for name, idx in pos.items():
                rhs[idx] = {"x": 9, "v": -6, "z": -2}[name]
            if loop:
                rhs[0] += 4
            rows = []
            for idx in range(n):
                row = [0] * n
                for neighbor in [idx - 1, idx + 1]:
                    if 0 <= neighbor < n:
                        row[neighbor] = 1
                if loop and idx == 0:
                    row[0] = 1
                rows.append((row, rhs[idx]))
            for name in sorted(pos):
                row = [0] * n
                row[pos[name]] = 1
                rows.append((row, {"x": 8, "v": -1, "z": -6}[name]))
            total = [0] * n
            residual = 0
            used = set()
            for idx, wt in q["weights"]:
                assert idx not in used and 0 <= idx < len(rows) and isinstance(wt, int)
                used.add(idx)
                row, b = rows[idx]
                total = [a + wt * v for a, v in zip(total, row)]
                residual += wt * b
            assert not any(total)
            assert residual == q["residual"] and 0 < abs(residual) < 149
            max_residual = max(max_residual, abs(residual))

    expected = set()
    counts = {}
    for names in [("x",), ("x", "v"), ("x", "z"), ("x", "v", "z")]:
        count = 0
        for n in range(len(names), 15):
            for locations in permutations(range(n), len(names)):
                pos = tuple(sorted(zip(names, locations)))
                for loop in [False, True]:
                    expected.add((n, pos, loop))
                    count += 1
        counts["".join(names)] = count
    assert seen == expected
    report = {"status": "PASS", "cases_replayed": len(seen), "case_counts": counts,
              "coverage": "All paths with <=14 vertices, containing x and any subset of v,z, and zero or one endpoint loop.",
              "largest_absolute_integer_residual": max_residual,
              "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "scope": "Independent equation reconstruction and integer witness replay; common mathematical input is stated in two_leaf_K2L_exclusion.md. Not proof-assistant certification."}
    Path(__file__).with_name("K2L_path_verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
