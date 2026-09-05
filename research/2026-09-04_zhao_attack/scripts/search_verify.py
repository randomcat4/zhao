"""Independent indexed-subset enumeration of saved search output.

No DP over the 625 group sums is reused: every one of the 2**N subsets is
materialized as a four-coordinate residue vector and its cardinality.
"""
from pathlib import Path
import json
import re
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def coords(code):
    return [(code // (5**j)) % 5 for j in range(4)]


def rank_mod5(sequence):
    a = [coords(code) for code in sequence]
    rank = 0
    for col in range(4):
        pivot = next((i for i in range(rank, len(a)) if a[i][col] % 5), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, 5)
        a[rank] = [(x * inv) % 5 for x in a[rank]]
        for i in range(len(a)):
            if i != rank:
                c = a[i][col]
                a[i] = [(x - c * y) % 5 for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank


def verify(sequence):
    sums = np.zeros((1, 4), dtype=np.uint8)
    lengths = np.zeros(1, dtype=np.uint8)
    for code in sequence:
        v = np.asarray(coords(code), dtype=np.uint8)
        sums = np.concatenate((sums, (sums + v) % 5), axis=0)
        lengths = np.concatenate((lengths, lengths + 1))
    zero_masks = np.flatnonzero(np.all(sums == 0, axis=1))
    zero_masks = zero_masks[1:]  # mask 0 is the empty subset
    histogram = np.bincount(lengths[zero_masks], minlength=len(sequence) + 1)
    spectrum = {str(k): int(c) for k, c in enumerate(histogram) if k and c}
    witnesses = {}
    for mask in zero_masks:
        k = str(int(lengths[mask]))
        if k not in witnesses:
            witnesses[k] = [i + 1 for i in range(len(sequence)) if int(mask) >> i & 1]
    return {
        "subset_count": 2 ** len(sequence),
        "sequence_codes": sequence,
        "sequence_coordinates": [coords(code) for code in sequence],
        "support": len(set(sequence)),
        "max_multiplicity": max(sequence.count(x) for x in set(sequence)),
        "rank_mod5": rank_mod5(sequence),
        "affine_sum_coordinates_1": all(sum(coords(x)) % 5 == 1 for x in sequence),
        "spectrum": spectrum,
        "shortest_nonempty_zero": min(map(int, spectrum), default=None),
        "witness_positions_by_length": witnesses,
    }


results = []
for log in sorted((ROOT / "evidence").glob("search_*.log")):
    lines = log.read_text(encoding="utf-8").splitlines()
    finals = [line for line in lines if line.startswith("FINAL ") and " seq=" in line]
    if not finals:
        continue
    line = finals[-1]
    match = re.search(r" seq=([\d,]+) spectrum=(.*)$", line)
    if not match:
        raise ValueError(f"Cannot parse final line in {log.name}")
    sequence = list(map(int, match.group(1).split(",")))
    expected = dict((k, int(c)) for k, c in (part.split(":") for part in match.group(2).split(",") if part))
    item = verify(sequence)
    item.update(log=log.name, config=lines[0], final_line=line)
    if item["spectrum"] != expected:
        raise AssertionError((log.name, expected, item["spectrum"]))
    item["spectra_match"] = True
    results.append(item)
    print(f"VERIFIED {log.name} N={len(sequence)} min={item['shortest_nonempty_zero']} support={item['support']} subsets={2**len(sequence)} spectrum={item['spectrum']}")

out = ROOT / "evidence" / "search_independent_verification.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Verified {len(results)} sequences; wrote {out}")
