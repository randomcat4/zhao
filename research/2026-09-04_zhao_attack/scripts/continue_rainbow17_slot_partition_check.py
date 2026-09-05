"""Independent slot-partition check of the six-edge graph classification.

The primary classifier grows two matchings after fixing the first one.  This
checker instead enumerates restricted-growth set partitions of the twelve
ordered endpoint slots, then quotients the surviving partitions by the 512
within-colour edge/orientation symmetries.
"""

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
PRIMARY = BASE / "evidence/continue_rainbow17_classify.json"
OUT = BASE / "evidence/continue_rainbow17_slot_partition_check.json"

# Slot pairs, grouped by colour.  The first four slots must represent four
# different vertices, so their restricted-growth labels are fixed as 0,1,2,3.
PAIRS = (((0, 1), (2, 3)), ((4, 5), (6, 7)), ((8, 9), (10, 11)))


def slot_permutations():
    result = []
    for swap_edges in product((0, 1), repeat=3):
        for flip in product((0, 1), repeat=6):
            order = []
            for color in range(3):
                edge_order = (1, 0) if swap_edges[color] else (0, 1)
                for edge in edge_order:
                    slots = list(PAIRS[color][edge])
                    if flip[2 * color + edge]:
                        slots.reverse()
                    order.extend(slots)
            result.append(tuple(order))
    assert len(result) == 512
    return tuple(result)


SLOT_PERMS = slot_permutations()


def canonical(labels):
    best = None
    for perm in SLOT_PERMS:
        relabel = {}
        word = []
        for slot in perm:
            old = labels[slot]
            if old not in relabel:
                relabel[old] = len(relabel)
            word.append(relabel[old])
        word = tuple(word)
        if best is None or word < best:
            best = word
    return best


def edge(labels, pair):
    return frozenset((labels[pair[0]], labels[pair[1]]))


def valid_completed_edge(labels, slot):
    """Reject an edge as soon as it duplicates an earlier-colour edge."""
    if slot not in (5, 7, 9, 11):
        return True
    current_color = 1 if slot <= 7 else 2
    current_edge = 0 if slot in (5, 9) else 1
    made = edge(labels, PAIRS[current_color][current_edge])
    for color in range(current_color):
        for earlier in PAIRS[color]:
            if made == edge(labels, earlier):
                return False
    return True


def has_rainbow(labels):
    colored = [[edge(labels, pair) for pair in row] for row in PAIRS]
    return any(not (red & green or red & blue or green & blue)
               for red in colored[0] for green in colored[1] for blue in colored[2])


def enumerate_partitions():
    canonical_types = set()
    survivors = 0
    by_vertex_count = Counter()
    labels = [0, 1, 2, 3]

    def visit(slot, maximum):
        nonlocal survivors
        if slot == 12:
            if has_rainbow(labels):
                return
            survivors += 1
            by_vertex_count[maximum + 1] += 1
            canonical_types.add(canonical(tuple(labels)))
            return

        color_start = 4 if slot < 8 else 8
        used_in_color = set(labels[color_start:slot])
        for value in range(maximum + 2):
            # Each colour is a matching: all four endpoint vertices differ.
            if value in used_in_color:
                continue
            labels.append(value)
            if valid_completed_edge(labels, slot):
                visit(slot + 1, max(maximum, value))
            labels.pop()

    visit(4, 3)
    return canonical_types, survivors, dict(sorted(by_vertex_count.items()))


def main():
    types, survivors, partition_histogram = enumerate_partitions()
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    primary_types = {tuple(row["canonical_slot_partition"]) for row in primary["records"]}
    assert types == primary_types
    type_histogram = Counter(1 + max(word) for word in types)
    output = {
        "status": "INDEPENDENT_CLASSIFICATION_MATCH",
        "method": "restricted-growth partitions of 12 ordered endpoint slots",
        "ordered_slot_partitions_without_rainbow": survivors,
        "ordered_slot_partition_vertex_count_histogram": partition_histogram,
        "color_preserving_isomorphism_types": len(types),
        "isomorphism_type_vertex_count_histogram": dict(sorted(type_histogram.items())),
        "primary_evidence_sha256": sha256(PRIMARY.read_bytes()).hexdigest(),
        "canonical_type_sets_equal": True,
        "script_sha256_before_output": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    OUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    assert sha256(Path(__file__).read_bytes()).hexdigest() == output["script_sha256_before_output"]
    print(json.dumps(output))


if __name__ == "__main__":
    main()
