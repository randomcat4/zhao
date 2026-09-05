"""Independent exhaustive certificate for the 3,3,2,2,2 H cores.

No import or execution of the audited source.  Every one of the 7,260
candidate pairs is examined via all 4*4*3*3*3 = 432 count choices.
The two outputs retain all rejected pairs with zero-sum witnesses and all
125 shortest distances, with attaining witnesses, for every accepted pair.
Only Python standard library and exact integer arithmetic are used.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import platform


ROOT = Path(__file__).resolve().parents[1]
AUDITED_PROOF = ROOT / "proofs/hyperplane_core_A_support8.md"
AUDITED_SCRIPT = ROOT / "scripts/root_33222_hyperplane_profile.py"
AUDITED_JSON = ROOT / "evidence/root_33222_hyperplane_profile.json"
SUMMARY_OUT = ROOT / "evidence/verify_support8_fresh.json"
REJECTED_OUT = ROOT / "evidence/verify_support8_rejected.json"


def code(vector):
    return vector[0] * 25 + vector[1] * 5 + vector[2]


def decode(value):
    return value // 25, value // 5 % 5, value % 5


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    vectors = list(product(range(5), repeat=3))
    basis = {(1, 0, 0), (0, 1, 0), (0, 0, 1)}
    pool = [w for w in vectors if w != (0, 0, 0) and w not in basis]
    assert len(pool) == 121
    assignments = list(product(range(4), range(4), range(3), range(3), range(3)))
    assert len(assignments) == 432
    accepted = []
    rejected = []
    pair_count = 0
    representation_count = 0
    for first, second in combinations(pool, 2):
        pair_count += 1
        distances = [99] * 125
        attaining_counts = [None] * 125
        first_zero = None
        for counts in assignments:
            a, b, c, p, q = counts
            target = code(((a + p * first[0] + q * second[0]) % 5,
                           (b + p * first[1] + q * second[1]) % 5,
                           (c + p * first[2] + q * second[2]) % 5))
            length = a + b + c + p + q
            representation_count += 1
            if length < distances[target]:
                distances[target] = length
                attaining_counts[target] = list(counts)
            if target == 0 and length > 0 and first_zero is None:
                first_zero = list(counts)
        first_code, second_code = code(first), code(second)
        if first_zero is not None:
            rejected.append({"u": first_code, "v": second_code,
                             "nonempty_zero_counts": first_zero})
            continue
        total = code(((3 + 2 * first[0] + 2 * second[0]) % 5,
                      (3 + 2 * first[1] + 2 * second[1]) % 5,
                      (2 + 2 * first[2] + 2 * second[2]) % 5))
        max_except_total = max(d for i, d in enumerate(distances) if i != total)
        high_10 = [i for i, d in enumerate(distances) if d >= 10]
        high_9 = [i for i, d in enumerate(distances) if d >= 9]
        conditions = {
            "A1_full_coverage_unique_gt10_total_at_12": (
                max(distances) < 99 and total != 0 and distances[total] == 12
                and [i for i, d in enumerate(distances) if d > 10] == [total]),
            "A2_E10_at_most3": len(high_10) <= 3,
            "A3_E9_at_most5": len(high_9) <= 5,
            "B1_except_total_at_most10": max_except_total <= 10,
            "B2_E10_at_most3": len(high_10) <= 3,
        }
        assert all(conditions.values()), (first, second, conditions)
        accepted.append({
            "u": first_code, "v": second_code, "sigma": total,
            "max_distance_except_total": max_except_total,
            "E10": len(high_10), "E9": len(high_9),
            "E10_targets": high_10, "E9_targets": high_9,
            "distances_by_target_code": distances,
            "attaining_counts_by_target_code": attaining_counts,
            "conditions": conditions,
        })

    # Verify the original JSON only after independently constructing the domain.
    original = json.loads(AUDITED_JSON.read_text(encoding="utf-8-sig"))
    scalar_keys = ("u", "v", "sigma", "max_distance_except_total", "E10", "E9")
    reproduced_rows = [{key: row[key] for key in scalar_keys} for row in accepted]
    original_rows = original["rows"]
    original_pairs = [(row["u"], row["v"]) for row in original_rows]
    assert len(set(original_pairs)) == len(original_pairs), "duplicate source rows"
    assert sorted(original_rows, key=lambda r: (r["u"], r["v"])) == reproduced_rows
    histogram = dict(sorted(Counter(row["max_distance_except_total"] for row in accepted).items()))
    e10_histogram = dict(sorted(Counter(row["E10"] for row in accepted).items()))
    e9_histogram = dict(sorted(Counter(row["E9"] for row in accepted).items()))
    assert pair_count == 7260
    assert representation_count == 7260 * 432
    assert len(accepted) == 75
    assert len(rejected) == 7185
    assert original["candidate_pairs"] == pair_count
    assert original["zero_free_cores"] == len(accepted)
    assert original["distance_histogram"] == {str(k): v for k, v in histogram.items()}
    assert original["max_E10"] == max(e10_histogram)
    assert original["max_E9"] == max(e9_histogram)

    # Independent checks of the tiny algebraic normalizations used in the prose.
    nonzero_scalars = (1, 2, 3, 4)
    triple_normalizations = []
    for values in combinations(nonzero_scalars, 3):
        good_scales = [s for s in nonzero_scalars if {s * q % 5 for q in values} == {1, 2, 4}]
        assert good_scales
        triple_normalizations.append({"values": list(values), "scales_to_124": good_scales})
    nonopposite_normalizations = []
    for values in combinations(nonzero_scalars, 2):
        if sum(values) % 5 == 0:
            continue
        good_scales = [s for s in nonzero_scalars if {s * q % 5 for q in values} == {1, 2}]
        assert good_scales
        nonopposite_normalizations.append({"values": list(values), "scales_to_12": good_scales})
    dependent_triple_witnesses = []
    for scalar in (2, 3, 4):
        witnesses = [(a, b) for a, b in product(range(4), repeat=2)
                     if 0 < a + b <= 5 and (a + scalar * b) % 5 == 0]
        assert witnesses
        dependent_triple_witnesses.append({"second_vector_is_scalar_times_first": scalar,
                                          "zero_counts": list(min(witnesses, key=lambda ab: (sum(ab), ab)))})

    write_json(REJECTED_OUT, {
        "scope": "All rejected unordered pairs, with an actual nonempty zero-sum count witness.",
        "encoding": "code(x,y,z)=25*x+5*y+z; counts=(e1,e2,e3,u,v)",
        "rejected_count": len(rejected), "rows": rejected,
    })
    summary = {
        "status": "INDEPENDENT_EXHAUSTIVE_FINITE_VERIFICATION_PASSED",
        "scope": "Only fixed 3,3,2 basis and two distinct nonzero nonbasis double blocks; no GL quotient.",
        "method": "Examine every count vector (a,b,c,p,q) in [0,3]^2 x [0,2]^3 for every unordered pair; no source DP or pruning.",
        "encoding": "code(x,y,z)=25*x+5*y+z; witnesses use (e1,e2,e3,u,v) counts",
        "python_version": platform.python_version(),
        "candidate_vector_count": len(pool),
        "candidate_pairs": pair_count,
        "count_vectors_per_pair": len(assignments),
        "total_count_vectors_examined": representation_count,
        "zero_free_cores": len(accepted),
        "rejected_pairs": len(rejected),
        "distances_verified": len(accepted) * 125,
        "distance_histogram_except_total": histogram,
        "E10_histogram": e10_histogram,
        "E9_histogram": e9_histogram,
        "original_all_scalar_rows_match": True,
        "condition_pass_counts": {key: sum(row["conditions"][key] for row in accepted)
                                  for key in accepted[0]["conditions"]},
        "quotient_triple_normalizations": triple_normalizations,
        "quotient_nonopposite_pair_normalizations": nonopposite_normalizations,
        "dependent_triple_zero_witnesses": dependent_triple_witnesses,
        "input_sha256": {
            str(AUDITED_PROOF.relative_to(ROOT)): file_hash(AUDITED_PROOF),
            str(AUDITED_SCRIPT.relative_to(ROOT)): file_hash(AUDITED_SCRIPT),
            str(AUDITED_JSON.relative_to(ROOT)): file_hash(AUDITED_JSON),
        },
        "independent_script_sha256": file_hash(Path(__file__)),
        "rejected_evidence_sha256": file_hash(REJECTED_OUT),
        "rows": accepted,
    }
    write_json(SUMMARY_OUT, summary)
    print(json.dumps({key: value for key, value in summary.items()
                      if key not in ("rows", "quotient_triple_normalizations",
                                     "quotient_nonopposite_pair_normalizations")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
