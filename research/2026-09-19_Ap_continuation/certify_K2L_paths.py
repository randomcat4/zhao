"""Exact integer contradiction certificates for every possible x component."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
from math import gcd, lcm
import gzip
import hashlib
import json

SPECIAL = {"x": (8, 9), "v": (-1, -6), "z": (-6, -2)}


def rows(n, positions, loop):
    labels = {i: name for name, i in positions.items()}
    a = []
    for i in range(n):
        row = [0] * (n + 1)
        if i:
            row[i - 1] = 1
        if i + 1 < n:
            row[i + 1] = 1
        if loop and i == 0:
            row[0] = 1
        row[-1] = (SPECIAL[labels[i]][1] if i in labels else 2) + 4 * int(loop and i == 0)
        a.append(row)
    for name in sorted(positions):
        row = [0] * (n + 1)
        row[positions[name]] = 1
        row[-1] = SPECIAL[name][0]
        a.append(row)
    return a


def witness(original, n):
    count = len(original)
    mat = [[F(x) for x in row] for row in original]
    weights = [[F(int(i == j)) for j in range(count)] for i in range(count)]
    r = 0
    for j in range(n):
        pick = next((k for k in range(r, count) if mat[k][j]), None)
        if pick is None:
            continue
        mat[r], mat[pick] = mat[pick], mat[r]
        weights[r], weights[pick] = weights[pick], weights[r]
        den = mat[r][j]
        mat[r] = [v / den for v in mat[r]]
        weights[r] = [v / den for v in weights[r]]
        for k in range(count):
            if k != r and mat[k][j]:
                t = mat[k][j]
                mat[k] = [a - t * b for a, b in zip(mat[k], mat[r])]
                weights[k] = [a - t * b for a, b in zip(weights[k], weights[r])]
        r += 1
    for row, w in zip(mat, weights):
        if any(row[:-1]) or not row[-1]:
            continue
        den = lcm(*(x.denominator for x in w))
        integers = [int(x * den) for x in w]
        common = gcd(*integers)
        integers = [x // common for x in integers]
        check = [sum(wi * original[i][j] for i, wi in enumerate(integers)) for j in range(n + 1)]
        assert not any(check[:-1]) and check[-1]
        assert 0 < abs(check[-1]) < 149
        return {"weights": [[i, v] for i, v in enumerate(integers) if v], "residual": check[-1]}
    raise AssertionError("No contradiction for candidate")


def main():
    path = Path(__file__).with_name("K2L_path_certificates.jsonl.gz")
    totals, largest = {}, 0
    with path.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as f:
        for names in [("x",), ("x", "v"), ("x", "z"), ("x", "v", "z")]:
            count = 0
            for n in range(len(names), 15):
                for indices in permutations(range(n), len(names)):
                    positions = dict(zip(names, indices))
                    for loop in [False, True]:
                        w = witness(rows(n, positions, loop), n)
                        record = {"n": n, "positions": positions, "loop": loop, **w}
                        f.write((json.dumps(record, separators=(",", ":")) + "\n").encode())
                        count += 1
                        largest = max(largest, abs(w["residual"]))
            totals["".join(names)] = count
            print("".join(names), count, flush=True)
    report = {"status": "PASS", "cases": sum(totals.values()), "case_counts": totals,
              "largest_absolute_integer_residual": largest,
              "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "scope": "Every path with at most 14 value vertices containing x, with zero or one endpoint loop; exact integer row identities exclude every prime p>=149."}
    Path(__file__).with_name("K2L_path_certificate_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
