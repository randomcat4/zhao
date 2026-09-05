"""Exact three-chart exclusion of the d=4, M=1 forced star core."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
V = tuple(tuple(g // 5**j % 5 for j in range(4)) for g in range(625))


def enc(v): return sum(x*5**j for j, x in enumerate(v))
def add(a, b): return enc(tuple((x+y) % 5 for x, y in zip(V[a], V[b])))
PLUS = tuple(tuple(add(a, b) for b in range(625)) for a in range(625))
NEG = tuple(enc(tuple(-x % 5 for x in V[a])) for a in range(625))


def sequence(x, ys):
    gs = [PLUS[x][y] for y in ys]
    support = {x, *ys, *gs}
    if len(support) != 9 or 0 in support:
        return None
    return [x, gs[0], gs[0], ys[0], ys[0], ys[0],
            gs[1], ys[1], ys[1], gs[2], ys[2], ys[2],
            gs[3], ys[3], ys[3]]


def first_short_zero(seq):
    distance = [99]*625
    masks = [None]*625
    distance[0], masks[0] = 0, 0
    for index, g in enumerate(seq):
        old_mask = masks[NEG[g]]
        if distance[NEG[g]] < 14:
            witness = old_mask | (1 << index)
            values = [seq[j] for j in range(index+1) if witness >> j & 1]
            total = 0
            for value in values: total = PLUS[total][value]
            assert total == 0 and 1 <= len(values) <= 14
            return len(values), witness, values
        new_distance, new_masks = distance[:], masks[:]
        for h in range(625):
            if distance[h] == 99:
                continue
            target = PLUS[h][g]
            if distance[h]+1 < new_distance[target]:
                new_distance[target] = distance[h]+1
                new_masks[target] = masks[h] | (1 << index)
        distance, masks = new_distance, new_masks
    return None


def digest(name): return sha256((BASE/name).read_bytes()).hexdigest()


def main():
    e = (1, 5, 25, 125)
    charts = (
        ('basis_y1_y2_y3_y4', lambda z: (z, list(e))),
        ('basis_x_y2_y3_y4', lambda z: (e[0], [z, e[1], e[2], e[3]])),
        ('basis_x_y1_y2_y3', lambda z: (e[0], [e[1], e[2], e[3], z])),
    )
    records, summaries = [], []
    for name, chart in charts:
        eligible = 0
        histogram = Counter()
        for z in range(625):
            x, ys = chart(z)
            seq = sequence(x, ys)
            if seq is None:
                continue
            eligible += 1
            witness = first_short_zero(seq)
            assert witness is not None
            length, mask, values = witness
            histogram[length] += 1
            records.append({'chart': name, 'free_generator_encoded': z,
                            'forced_sequence': seq, 'short_zero_length': length,
                            'position_mask': mask, 'zero_values': values})
        summaries.append({'chart': name, 'eligible_distinct_supports': eligible,
                          'short_zero_length_histogram': dict(sorted(histogram.items())),
                          'safe_forced_cores': 0})
    assert all(row['eligible_distinct_supports'] > 0 for row in summaries)
    inputs = ('proofs/continue_atom16_star.md',
              'scripts/continue_atom16_star_addendum_d4.py')
    output = {
        'status': 'ALL_THREE_D4_M1_BASIS_CHARTS_EXCLUDED',
        'scope': 'The forced 15-position star core already has a nonempty zero sum of length at most 14',
        'charts': summaries, 'records': records,
        'input_sha256': {name: digest(name) for name in inputs},
    }
    (BASE/'evidence/continue_atom16_star_addendum_d4.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    for name, expected in output['input_sha256'].items(): assert digest(name) == expected
    print(json.dumps({'status': output['status'], 'charts': summaries,
                      'witnesses': len(records)}))


if __name__ == '__main__': main()
