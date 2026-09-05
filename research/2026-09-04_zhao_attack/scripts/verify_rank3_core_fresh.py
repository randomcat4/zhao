"""Independent exact audit of the rank-three, four-triple obstruction.

Only writes verify_rank3_* files in this run's evidence directory.  No third
party modules, numerical tolerances, random sampling, or author script imports.
"""

from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import csv
import hashlib
import json
import platform


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence"
PREFIX = "verify_rank3_core_fresh"
OUT.mkdir(exist_ok=True)


def write_csv(suffix, rows):
    path = OUT / f"{PREFIX}_{suffix}.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path.name


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def small_compositions(total):
    if total == 0:
        yield ()
        return
    for first in range(1, min(3, total) + 1):
        for rest in small_compositions(total - first):
            yield (first,) + rest


def affine_signatures(rows, n):
    """Solve A u = C over F5 with symbolic nonzero vector C.

    A signature records the coefficient of C and of each free vector.  Equal
    signatures are exact vector equalities.  An inconsistent row asserts a
    nonzero multiple of C is zero, which is impossible.
    """
    matrix = [row[:] for row in rows]
    pivots = []
    next_row = 0
    for col in range(n):
        pivot = next((j for j in range(next_row, len(matrix))
                      if matrix[j][col] % 5), None)
        if pivot is None:
            continue
        matrix[next_row], matrix[pivot] = matrix[pivot], matrix[next_row]
        inverse = pow(matrix[next_row][col], -1, 5)
        matrix[next_row] = [(inverse * value) % 5
                            for value in matrix[next_row]]
        for j, row in enumerate(matrix):
            if j != next_row and row[col]:
                factor = row[col]
                matrix[j] = [(v - factor * w) % 5
                             for v, w in zip(row, matrix[next_row])]
        pivots.append(col)
        next_row += 1
    if any(not any(row[:n]) and row[n] for row in matrix):
        return None
    free = [j for j in range(n) if j not in pivots]
    signatures = [None] * n
    for j in free:
        signatures[j] = (0,) + tuple(int(k == j) for k in free)
    for row, col in zip(matrix, pivots):
        signatures[col] = (row[n],) + tuple((-row[k]) % 5 for k in free)
    return signatures


sources = {}
for label, path in {
    "proof": ROOT / "proofs" / "four_triples_rank3.md",
    "frozen_v1": ROOT / "frozen_theorem_v1.md",
}.items():
    raw = path.read_bytes()
    sources[label] = {"relative_path": str(path.relative_to(ROOT)),
                      "sha256": hashlib.sha256(raw).hexdigest()}
    (OUT / f"{PREFIX}_{label}_snapshot.md").write_bytes(raw)

# First enumeration: forward through exactly 4^4 physical multiplicities.
forward = defaultdict(list)
for x, y, z, t in product(range(4), repeat=4):
    target = ((x + t) % 5, (y + 2*t) % 5, (z + 3*t) % 5)
    forward[target].append((x+y+z+t, (x, y, z, t)))
assert len(forward) == 125
assert forward[(0, 0, 0)] == [(0, (0, 0, 0, 0))]

# Second enumeration: for every one of 5^3 targets, the value of t forces
# all three basis multiplicities, so there are only four possible witnesses.
core_rows = []
distances = {}
for target in product(range(5), repeat=3):
    candidates = []
    lengths = []
    for t in range(4):
        triple = tuple((target[j] - (j+1)*t) % 5 for j in range(3))
        if 4 not in triple:
            witness = triple + (t,)
            candidates.append((sum(witness), witness))
            lengths.append(sum(witness))
        else:
            lengths.append(None)
    assert sorted(candidates) == sorted(forward[target])
    minimum, witness = min(candidates)
    assert all(0 <= value <= 3 for value in witness)
    assert tuple((witness[j] + (j+1)*witness[3]) % 5
                 for j in range(3)) == target
    distances[target] = minimum
    core_rows.append({"x": target[0], "y": target[1], "z": target[2],
                      "min_length": minimum,
                      "witness_x": witness[0], "witness_y": witness[1],
                      "witness_z": witness[2], "witness_t": witness[3],
                      **{f"length_at_t_{t}": lengths[t] for t in range(4)}})
v = (1, 4, 2)
expected_long = {v, (4, 0, 0), (0, 4, 0), (0, 0, 4), (4, 3, 2)}
assert {point for point, length in distances.items() if length > 8} == expected_long
assert {point for point, length in distances.items() if length > 9} == {v}
assert distances[v] == 12
distribution = dict(sorted(Counter(distances.values()).items()))
assert distribution == {0:1, 1:4, 2:10, 3:18, 4:21, 5:24,
                        6:21, 7:14, 8:7, 9:4, 12:1}
core_csv = write_csv("125_targets", core_rows)

# Check the claimed normal form against all 125 choices of the fourth vector.
zero_free_fourth_vectors = []
normal_rows = []
for a in product(range(5), repeat=3):
    zeros = []
    for coeff in product(range(4), repeat=4):
        if any(coeff) and all((coeff[j] + coeff[3]*a[j]) % 5 == 0
                              for j in range(3)):
            zeros.append(coeff)
    if not zeros:
        zero_free_fourth_vectors.append(a)
    normal_rows.append({"a1":a[0], "a2":a[1], "a3":a[2],
                        "zero_free":not zeros,
                        "zero_witness":str(min(zeros, key=sum)) if zeros else ""})
assert set(zero_free_fourth_vectors) == {
    a for a in product((1, 2, 3), repeat=3) if len(set(a)) == 3}
normal_csv = write_csv("normal_forms", normal_rows)

# Independently enumerate every quotient multiplicity pattern.  We do not
# import or translate the author's classification script.  All short quotient
# zero sums give exact equations whose right side is the common vector C.
quotient_rows = []
quotient_summary = {}
for label, n, cutoff in (("A", 9, 4), ("B", 8, 5)):
    counts = Counter()
    support_counts = Counter()
    for multiplicities in compositions(n, 4):
        qs = [q for q, count in enumerate(multiplicities, 1)
              for _ in range(count)]
        support = {q for q in qs}
        support_counts[len(support)] += 1
        opposite = any(5-q in support for q in support)
        if label == "B" and opposite:
            disposition = "opposite_pair_gives_length_at_most_14"
            forced = 0
            equations = 0
        else:
            rows = []
            for size in range(1, cutoff+1):
                for indices in combinations(range(n), size):
                    if sum(qs[j] for j in indices) % 5 == 0:
                        rows.append([int(j in indices) for j in range(n)] + [1])
            equations = len(rows)
            signatures = affine_signatures(rows, n)
            if signatures is None:
                disposition = "inconsistent_with_C_nonzero"
                forced = 0
            else:
                classes = Counter((q, sig) for q, sig in zip(qs, signatures))
                forced = max(classes.values())
                if forced >= 4:
                    disposition = "forces_multiplicity_at_least_4"
                else:
                    disposition = "needs_five_point_sumset_argument"
                    assert label == "A" and len(support) == 1
        counts[disposition] += 1
        quotient_rows.append({"endpoint":label,
                              **{f"n{q}":multiplicities[q-1] for q in range(1, 5)},
                              "support_size":len(support),
                              "equations":equations,
                              "forced_equal_block":forced,
                              "disposition":disposition})
    assert sum(counts.values()) == (220 if label == "A" else 165)
    assert counts["needs_five_point_sumset_argument"] == (4 if label == "A" else 0)
    quotient_summary[label] = {"total":sum(counts.values()),
                               "support_size_counts":dict(sorted(support_counts.items())),
                               "dispositions":dict(sorted(counts.items()))}
quotient_csv = write_csv("quotient_patterns", quotient_rows)

# Sorted eight-position multisets: their equality patterns are precisely the
# ordered compositions of 8 into parts <= 3.  A fixed gap of four cannot join
# equal values; in fact that would require a run of at least five values.
pairing_patterns = list(small_compositions(8))
for multiplicities in pairing_patterns:
    values = [j for j, count in enumerate(multiplicities) for _ in range(count)]
    assert all(values[i] != values[i+4] for i in range(4))
assert len(pairing_patterns) == 81

# Supplementary bounded check only.  The proof in the audit report, rather
# than this two-dimensional check, covers arbitrary F5 vector spaces.
nonzero2 = [p for p in product(range(5), repeat=2) if p != (0, 0)]
sumset_distribution = Counter()
sumset_rank2_minimum = 25
for directions in combinations_with_replacement(nonzero2, 4):
    sums = {(0, 0)}
    for d in directions:
        sums |= {((s[0]+d[0]) % 5, (s[1]+d[1]) % 5) for s in sums}
    rank1 = all((directions[0][0]*d[1] - directions[0][1]*d[0]) % 5 == 0
                for d in directions)
    assert len(sums) >= 5
    if len(sums) == 5:
        assert rank1
    if not rank1:
        sumset_rank2_minimum = min(sumset_rank2_minimum, len(sums))
    sumset_distribution[len(sums)] += 1
assert sum(sumset_distribution.values()) == 17550

summary = {
    "status":"PASS",
    "python":platform.python_version(),
    "sources":sources,
    "core":{"targets":125, "forward_coefficients":256,
            "reverse_target_t_pairs":500, "distribution":distribution,
            "zero_free_fourth_vectors":zero_free_fourth_vectors,
            "witness_csv":core_csv, "normal_form_csv":normal_csv},
    "quotient_patterns":quotient_summary,
    "quotient_csv":quotient_csv,
    "sorted_pairing":{"equality_patterns":81, "tested_pairs":324,
                      "all_pairs_have_distinct_values":True},
    "two_dimensional_sumset_check":{
        "scope":"Supplementary bounded check; general statement audited by proof",
        "direction_multisets":17550,
        "cardinality_distribution":dict(sorted(sumset_distribution.items())),
        "rank_two_minimum":sumset_rank2_minimum},
}
(OUT / f"{PREFIX}_summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
