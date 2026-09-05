"""Replay candidate certificates through a different implementation.

Written by the producing instance: this is NOT a fresh-context independent
review. It imports only the previously audited exact-length engine/helpers,
never the new C# producer or the H12 producer. A fresh reviewer may inspect
and use it as a reproduction entry point.
"""
from collections import Counter
import hashlib
from itertools import permutations
import json
import math
from pathlib import Path
import time

from verify_finite_cores_fresh import ExactLengths, E, VECTORS, FULL, Q, elements, number
from verify_finite_double_blocks import append_two, block_candidates, canonical, allowed_permutations

BASE = Path(__file__).resolve().parents[1]
NEG = [number(tuple((-x) % 5 for x in v)) for v in VECTORS]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def union_lengths(state, maximum):
    result = 0
    for _ in range(maximum + 1):
        result |= state & FULL
        state >>= Q
    return result


def main():
    started = time.perf_counter()
    original = BASE/'evidence/atom_2222_m13_blocks.jsonl'
    original_rows = [json.loads(line) for line in original.read_text(encoding='utf-8').splitlines()]
    old_meta = original_rows[0]
    expected = {row['root']: row['nodes_by_length'].get('14', 0) for row in original_rows if row['type'] == 'root'}
    assert len(expected) == 44 and sum(expected.values()) == 166195
    assert all(row['completed_exhaustively'] for row in original_rows if row['type'] == 'root')
    probe_path = BASE/'evidence/seven_doubles_continue_probe.json'
    cores_path = BASE/'evidence/seven_doubles_continue_probe_cores.jsonl'
    h12_path = BASE/'evidence/seven_doubles_continue_h12.json'
    probe = json.loads(probe_path.read_text(encoding='utf-8'))
    assert probe['status'] == 'COMPLETE_PROBE_WITH_EXACT_COLORING_RESIDUAL'
    assert probe['input_sha256'] == sha(original)
    assert probe['original_script_sha256'] == old_meta['script_sha256'] == sha(BASE/'scripts/atom_double_blocks.ps1')
    assert probe['producer_sha256'] == sha(BASE/'scripts/seven_doubles_continue_probe.cs')
    engine = ExactLengths(13)
    fixed = tuple(g for g in E for _ in range(2))
    base = engine.build(fixed)
    used_base = sum(1 << g for g in E)
    initial = elements(block_candidates(base, used_base, 1))
    assert initial == old_meta['initial_safe_candidates'] and len(initial) == 475
    roots = sorted({canonical(g, allowed_permutations('2222')) for g in initial})
    assert roots == old_meta['canonical_roots'] == sorted(expected)
    negsum = [[NEG[number(tuple((a[j]+b[j]) % 5 for j in range(4)))] for b in VECTORS] for a in VECTORS]
    candidate_hist, color_hist, by_root = Counter(), Counter(), Counter()
    count = pair_checks = excluded = six = seven = residual_six = residual_seven = 0
    residual_keys = []
    with cores_path.open(encoding='utf-8') as stream:
        metadata = json.loads(next(stream))
        assert metadata['type'] == 'metadata' and metadata['expected_cores'] == 166195
        assert metadata['canonical_roots'] == roots and metadata['fixed_sequence'] == list(fixed)
        assert metadata['cutoff'] == 13 and metadata['core_length'] == 14
        for root in roots:
            s10 = append_two(engine, base, root)
            used10 = used_base | (1 << root)
            for second in elements(block_candidates(s10, used10, root+1)):
                s12 = append_two(engine, s10, second)
                used12 = used10 | (1 << second)
                for third in elements(block_candidates(s12, used12, second+1)):
                    state = append_two(engine, s12, third)
                    row = json.loads(next(stream))
                    assert row['type'] == 'core' and row['index'] == count
                    assert row['blocks'] == [root, second, third]
                    candidates = elements(engine.candidates(state, used12 | (1 << third), 1))
                    assert candidates == row['candidates']
                    n = len(candidates)
                    colors = row['colors']
                    k = max(colors)+1 if colors else 0
                    assert len(colors) == n and set(colors) == set(range(k))
                    assert k == row['color_count']
                    reachable11 = union_lengths(state, 11)
                    # Rebuild every edge by exact lengths and test the claimed coloring.
                    for i, g in enumerate(candidates):
                        for j in range(i+1, n):
                            edge = not (reachable11 >> negsum[g][candidates[j]]) & 1
                            assert not edge or colors[i] != colors[j]
                    assert row['pair_checks'] == n*(n-1)//2
                    c6, c7 = math.comb(n, 6), math.comb(n, 7)
                    assert (row['six_subset_count'], row['seven_subset_count']) == (c6, c7)
                    assert row['no_six_extension_by_coloring'] == (k <= 5)
                    count += 1
                    by_root[root] += 1
                    candidate_hist[n] += 1
                    color_hist[k] += 1
                    pair_checks += n*(n-1)//2
                    six += c6
                    seven += c7
                    if k <= 5:
                        excluded += 1
                    else:
                        residual_keys.append(row['blocks'])
                        residual_six += c6
                        residual_seven += c7
            assert by_root[root] == expected[root]
        trailer = json.loads(next(stream))
        assert trailer['type'] == 'summary' and trailer['processed_cores'] == count
        assert trailer['colored_cores'] == excluded and trailer['residual_cores'] == len(residual_keys)
        assert not trailer['time_limit_reached'] and not stream.read().strip()
    assert count == 166195 and excluded == 166180 and len(residual_keys) == 15
    assert residual_keys == probe['residual_keys']
    assert dict(by_root) == {int(k):v for k,v in probe['generated_cores_by_root'].items()}
    assert dict(candidate_hist) == {int(k):v for k,v in probe['candidate_histogram'].items()}
    assert dict(color_hist) == {int(k):v for k,v in probe['color_histogram'].items()}
    assert pair_checks == probe['pair_checks'] == 35295586
    assert [six, seven, residual_six, residual_seven] == [int(probe[k]) for k in (
        'six_subset_denominator', 'seven_subset_denominator', 'residual_six_subset_denominator', 'residual_seven_subset_denominator')]

    # Check H12 certificates by literal position subsets, rather than 3^6 coefficients.
    h12 = json.loads(h12_path.read_text(encoding='utf-8'))
    assert [row['blocks'] for row in h12['records']] == residual_keys
    for name, digest in h12['input_sha256'].items():
        assert sha(BASE/name) == digest
    reference = {5, 25, 125, 30, 190, 315}
    position_subsets = 0
    for row in h12['records']:
        support = list(E) + row['blocks']
        functionals = [v for v in VECTORS[1:] if next(x for x in v if x) == 1]
        counts = [2*sum(sum(x*y for x,y in zip(f,VECTORS[g])) % 5 == 0 for g in support) for f in functionals]
        assert counts == row['hyperplane_counts'] and counts.count(12) == 1 and max(counts) == 12
        f = functionals[counts.index(12)]
        assert list(f) == row['unique_h12_functional']
        inside = [g for g in support if sum(x*y for x,y in zip(f,VECTORS[g])) % 5 == 0]
        assert inside == row['inside_support'] and len(inside) == 6
        sequence = [g for g in inside for _ in range(2)]
        assert sequence == row['inside_sequence']
        attainable = {}
        zero_subsets = 0
        for mask in range(1 << 12):
            positions = [sequence[j] for j in range(12) if mask >> j & 1]
            target = number(tuple(sum(VECTORS[g][j] for g in positions) % 5 for j in range(4)))
            length = len(positions)
            attainable[target] = min(attainable.get(target, 100), length)
            if target == 0:
                zero_subsets += 1
                assert mask == 0
            position_subsets += 1
        sigma = number(tuple(sum(VECTORS[g][j] for g in sequence) % 5 for j in range(4)))
        assert zero_subsets == 1 and len(attainable) == 125 and sigma == row['sigma_encoded'] != 0
        assert attainable[sigma] == 12 and all(d <= 6 for g,d in attainable.items() if g != sigma)
        saved = row['all_125_minimum_representations']
        assert len(saved) == len({r['target_encoded'] for r in saved}) == 125
        for witness in saved:
            coefficients = witness['coefficients']
            assert len(coefficients) == 6 and all(c in (0,1,2) for c in coefficients)
            target = number(tuple(sum(c*VECTORS[g][j] for c,g in zip(coefficients,inside)) % 5 for j in range(4)))
            assert target == witness['target_encoded']
            assert sum(coefficients) == witness['minimum_length'] == attainable[target]
        matrix = row['matrix_to_reference']
        determinant = 0
        for permutation in permutations(range(4)):
            sign = (-1)**sum(permutation[i] > permutation[j] for i in range(4) for j in range(i+1,4))
            term = sign
            for i in range(4):
                term *= matrix[i][permutation[i]]
            determinant += term
        assert determinant % 5 == row['matrix_determinant_mod5'] != 0
        def transform(g):
            return number(tuple(sum(a*b for a,b in zip(r,VECTORS[g])) % 5 for r in matrix))
        assert {transform(g) for g in inside} == reference
        outside, = set(support) - set(inside)
        assert outside == row['outside_double_value'] and transform(outside) == 1
    output = {'status':'DIFFERENT_IMPLEMENTATION_FULL_REPLAY_PASS',
              'fresh_context_independent_review':'still required; checker written by producer instance',
              'expected_cores':166195, 'reconstructed_cores':count, 'graph_colored_cores':excluded,
              'residuals_verified':15, 'all_pair_checks':pair_checks,
              'literal_h12_position_subsets_checked':position_subsets,
              'six_subset_denominator':six, 'seven_subset_denominator':seven,
              'seconds':time.perf_counter()-started,
              'input_sha256':{str(p.relative_to(BASE)).replace('\\','/'):sha(p) for p in (
                  original, probe_path, cores_path, h12_path, Path(__file__),
                  BASE/'scripts/verify_finite_cores_fresh.py', BASE/'scripts/verify_finite_double_blocks.py')}}
    (BASE/'evidence/seven_doubles_continue_replay.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:output[k] for k in ('status','reconstructed_cores','residuals_verified','all_pair_checks','seconds')}))


if __name__ == '__main__':
    main()
