"""Fresh-context literal-position audit and complete supplied hash binding.

Imports no producer or prior verifier. Does not overwrite frozen artifacts.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

BASE = Path(__file__).resolve().parents[1]
BOUND = {}
CHECKS = []


def path(name):
    result = (BASE / name).resolve()
    assert result.is_relative_to(BASE), name
    return result


def digest(name):
    actual = hashlib.sha256(path(name).read_bytes()).hexdigest()
    if name in BOUND:
        assert BOUND[name] == actual, ('input changed during audit', name)
    BOUND[name] = actual
    return actual


def read(name):
    digest(name)
    return json.loads(path(name).read_text(encoding='utf-8'))


def bind(mapping, origin):
    for name, expected in mapping.items():
        actual = digest(name)
        assert actual == expected, (origin, name, expected, actual)
        CHECKS.append({'declared_by': origin, 'path': name, 'sha256': actual})


def vector(code):
    return tuple((code // (5 ** j)) % 5 for j in range(4))


def encode(v):
    return sum(a * 5 ** j for j, a in enumerate(v))


def add(a, b):
    return tuple((x + y) % 5 for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b)) % 5


def determinant(matrix):
    """Independent Gaussian elimination over F5 (not permutation formula)."""
    a = [[x % 5 for x in row] for row in matrix]
    n = len(a)
    assert all(len(row) == n for row in a)
    det = 1
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        value = a[col][col]
        det = det * value % 5
        inverse = pow(value, -1, 5)
        for row in range(col + 1, n):
            scale = a[row][col] * inverse % 5
            a[row] = [(x - scale * y) % 5 for x, y in zip(a[row], a[col])]
    return det % 5


def main():
    started = time.perf_counter()
    self_name = 'scripts/verify_seven_fresh_bindings_h12.py'
    digest(self_name)
    manifest_name = 'evidence/seven_doubles_continue_frozen_manifest.json'
    manifest = read(manifest_name)
    assert manifest['all_prior_input_hashes_unchanged'] is True
    bind(manifest['prior_input_sha256'], manifest_name + ':prior_input_sha256')
    bind(manifest['frozen_file_sha256'], manifest_name + ':frozen_file_sha256')
    core_name = 'evidence/verify_seven_fresh_core.json'
    core = read(core_name)
    assert core['status'] == 'INDEPENDENT_COEFFICIENT_ENUMERATION_FULL_PASS'
    bind(core['input_sha256'], core_name)
    assert core['length14_cores'] == 166195 and core['colored_cores'] == 166180
    assert core['all_candidate_pairs'] == 35295586

    h12_name = 'evidence/seven_doubles_continue_h12.json'
    h12 = read(h12_name)
    bind(h12['input_sha256'], h12_name)
    replay_name = 'evidence/seven_doubles_continue_replay.json'
    replay = read(replay_name)
    bind(replay['input_sha256'], replay_name)
    # Hashing the producer's replay is provenance checking, not a new audit.
    assert replay['expected_cores'] == replay['reconstructed_cores'] == 166195
    assert replay['residuals_verified'] == 15

    dense_name = 'evidence/verify_dense12_fresh.json'
    dense = read(dense_name)
    assert dense['status'] == 'CORRECT_FOR_ASSIGNED_LOCAL_CLAIMS'
    snapshot_name = 'evidence/dense12_audited_snapshot.md'
    assert digest(snapshot_name) == dense['inputsSha256']['proofs/hyperplane_dense12.md']
    assert digest('scripts/verify_dense12_fresh.js') == dense['verifierSha256']
    bind({'evidence/atom_127_classification.json':
          dense['inputsSha256']['evidence/atom_127_classification.json']}, dense_name)
    # The same old report also covered an unrelated 18-term lower bound.
    # Audit its stale hash explicitly without making that independent claim
    # into a prerequisite for the accepted manual dense12 theorem.
    nondependency_hash_checks = []
    for name, expected in dense['inputsSha256'].items():
        if name in ('proofs/hyperplane_dense12.md', 'evidence/atom_127_classification.json'):
            continue
        actual = digest(name)
        nondependency_hash_checks.append({'path': name, 'recorded_sha256': expected,
                                          'current_sha256': actual, 'matches': actual == expected,
                                          'used_by_this_candidate': False})
    digest('proofs/verify_dense12_fresh.md')
    snapshot = path(snapshot_name).read_text(encoding='utf-8').splitlines()
    current = path('proofs/hyperplane_dense12.md').read_text(encoding='utf-8').splitlines()
    assert len(snapshot) == len(current)
    changed = [i + 1 for i, (a, b) in enumerate(zip(snapshot, current)) if a != b]
    assert changed == [3]
    assert snapshot[2].startswith('状态：候选完整证明')
    assert current[2].startswith('状态：新上下文审计 CORRECT')

    residual = [tuple(k) for k in core['residual_keys']]
    assert len(residual) == len(set(residual)) == 15
    assert [tuple(r['blocks']) for r in h12['records']] == residual
    big_keys = []
    residual_counts = {}
    with path('evidence/seven_doubles_continue_probe_cores.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            row = json.loads(line)
            if row['type'] != 'core':
                continue
            key = tuple(row['blocks'])
            if len(row['candidates']) > 45:
                big_keys.append(key)
                assert len(row['candidates']) == 251
            if key in residual:
                residual_counts[key] = len(row['candidates'])
    assert big_keys == residual and all(n == 251 for n in residual_counts.values())

    vectors = tuple(vector(g) for g in range(625))
    functionals = [f for f in vectors[1:] if next(x for x in f if x) == 1]
    kernels = [frozenset(g for g, v in enumerate(vectors) if dot(f, v) == 0)
               for f in functionals]
    assert len(kernels) == len(set(kernels)) == 156
    assert all(len(kernel) == 125 for kernel in kernels)
    # Cover all 624 nonzero linear functionals, not merely 156 listed ones.
    for f in vectors[1:]:
        scale = pow(next(x for x in f if x), -1, 5)
        normalized = tuple(scale * x % 5 for x in f)
        assert normalized in functionals
        assert frozenset(g for g, v in enumerate(vectors) if dot(f, v) == 0) == kernels[functionals.index(normalized)]

    basis = [1, 5, 25, 125]
    reference = {5, 25, 125, 30, 190, 315}
    assert {encode(v) for v in h12['reference_h12_support_coordinates']} == reference
    assert set(h12['reference_core_support_encoded']) == reference | {1}
    assert h12['coefficient_tuples_checked'] == 15 * 729
    assert h12['target_representations_saved'] == 15 * 125
    assert h12['expected_residual_count'] == 15
    output_records = []
    masks_checked = 0
    for row in h12['records']:
        support = basis + row['blocks']
        assert len(set(support)) == 7
        counts = [2 * len(set(support) & kernel) for kernel in kernels]
        assert counts == row['hyperplane_counts']
        assert counts.count(12) == 1 and max(counts) == 12
        index = counts.index(12)
        assert list(functionals[index]) == row['unique_h12_functional']
        inside = [g for g in support if g in kernels[index]]
        outside, = [g for g in support if g not in kernels[index]]
        sequence = [g for g in inside for _ in range(2)]
        assert inside == row['inside_support'] and len(inside) == 6
        assert sequence == row['inside_sequence'] and len(sequence) == 12
        assert outside == row['outside_double_value']
        distances, best_masks = {}, {}
        all_coefficients = set()
        nonempty_zero_masks = []
        for mask in range(1 << 12):
            value = (0, 0, 0, 0)
            coefficients = [0] * 6
            for position in range(12):
                if mask & (1 << position):
                    value = add(value, vectors[sequence[position]])
                    coefficients[position // 2] += 1
            code, length = encode(value), mask.bit_count()
            all_coefficients.add(tuple(coefficients))
            if code == 0 and mask:
                nonempty_zero_masks.append(mask)
            if length < distances.get(code, 99):
                distances[code] = length
                best_masks[code] = mask
            masks_checked += 1
        assert len(all_coefficients) == row['coefficient_tuples_checked'] == 729
        assert not nonempty_zero_masks and row['nonempty_zero_tuples'] == 0
        assert set(distances) == kernels[index]
        sigma_vector = (0, 0, 0, 0)
        for g in sequence:
            sigma_vector = add(sigma_vector, vectors[g])
        sigma = encode(sigma_vector)
        assert sigma == row['sigma_encoded'] != 0 and distances[sigma] == 12
        assert all(d <= 6 for g, d in distances.items() if g != sigma)
        histogram = dict(Counter(distances.values()))
        assert histogram == {0: 1, 1: 6, 2: 19, 3: 36, 4: 35, 5: 19, 6: 8, 12: 1}
        assert {int(k): v for k, v in row['distance_histogram'].items()} == histogram
        saved = row['all_125_minimum_representations']
        assert len(saved) == len({item['target_encoded'] for item in saved}) == 125
        assert {item['target_encoded'] for item in saved} == set(distances)
        for item in saved:
            coefficients = item['coefficients']
            assert len(coefficients) == 6 and all(c in (0, 1, 2) for c in coefficients)
            value = tuple(sum(c * vectors[g][j] for c, g in zip(coefficients, inside)) % 5 for j in range(4))
            assert encode(value) == item['target_encoded']
            assert sum(coefficients) == item['minimum_length'] == distances[encode(value)]
        matrix = row['matrix_to_reference']
        assert len(matrix) == 4 and all(len(r) == 4 for r in matrix)
        assert all(isinstance(x, int) and 0 <= x < 5 for r in matrix for x in r)
        det = determinant(matrix)
        assert det == row['matrix_determinant_mod5'] != 0
        def transform(g):
            return encode(tuple(dot(r, vectors[g]) for r in matrix))
        assert {transform(g) for g in inside} == reference
        assert transform(outside) == 1
        assert sorted(transform(g) for g in support) == row['mapped_support_encoded']
        source_basis = row['source_basis_encoded']
        assert len(source_basis) == len(set(source_basis)) == 4 and source_basis[0] == outside
        assert set(source_basis[1:]) <= set(inside)
        assert determinant([list(r) for r in zip(*(vectors[g] for g in source_basis))]) != 0
        output_records.append({
            'blocks': row['blocks'], 'hyperplane_counts': counts,
            'unique_h12_functional': functionals[index], 'inside_sequence': sequence,
            'outside_double_value': outside, 'position_subsets_checked': 4096,
            'nonempty_zero_subsets': 0, 'coefficient_patterns_covered': len(all_coefficients),
            'sigma_encoded': sigma, 'distance_histogram': histogram,
            'all_minimum_distances_and_position_masks': [
                {'target_encoded': g, 'minimum_length': distances[g], 'position_mask': best_masks[g]}
                for g in sorted(distances)],
            'matrix_to_reference': matrix, 'determinant_mod5': det,
            'all_supplied_witnesses_and_matrix_fields_verified': True,
        })
    assert masks_checked == 61440

    # Small C5 check independently witnesses the accepted manual interface.
    # Enumerate all 165 multiplicity vectors of eight nonzero positions.
    quotient_patterns = 0
    for a in range(9):
        for b in range(9-a):
            for c in range(9-a-b):
                counts = (a, b, c, 8-a-b-c)
                quotient_patterns += 1
                if max(counts) >= 6:
                    continue
                positions = [value for value, count in enumerate(counts, 1) for _ in range(count)]
                zero_masks = [m for m in range(1, 256)
                              if sum(positions[j] for j in range(8) if m & (1 << j)) % 5 == 0]
                assert any(x & y == 0 and x.bit_count() + y.bit_count() <= 7
                           for x in zero_masks for y in zero_masks)
    assert quotient_patterns == 165
    for name, expected in list(BOUND.items()):
        assert digest(name) == expected
    output = {
        'status': 'INDEPENDENT_H12_POSITION_ENUMERATION_AND_HASH_BINDINGS_PASS',
        'literal_position_subsets_checked': masks_checked, 'hyperplanes_per_core': 156,
        'all_nonzero_functionals_covered': 624, 'minimum_target_representations_checked': 1875,
        'old_dense12_only_changed_line': changed, 'old_dense12_mathematical_body_identical': True,
        'old_dense12_unrelated_input_hash_checks': nondependency_hash_checks,
        'candidate_count_above45_exactly_residual_keys': True, 'quotient_patterns_checked': quotient_patterns,
        'records': output_records, 'all_bound_inputs_unchanged_during_check': True,
        'checked_hash_edges': CHECKS, 'input_sha256': BOUND,
        'seconds': time.perf_counter()-started,
    }
    path('evidence/verify_seven_fresh_bindings_h12.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: output[k] for k in ('status','literal_position_subsets_checked','minimum_target_representations_checked','seconds')}))


if __name__ == '__main__':
    main()
