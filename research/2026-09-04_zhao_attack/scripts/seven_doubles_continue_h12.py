"""Complete finite classification of exactly the 15 graph residuals.

No assumption that arbitrary H12 cores belong to the older nine-core list.
For each residual enumerate all 156 hyperplanes, then all 3^6 coefficient
tuples. Save a GL(4,5) map onto one explicit representative and all 125
minimum-length representations. This is producer evidence, not an independent
review of the proof.
"""
from collections import Counter
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time

BASE = Path(__file__).resolve().parents[1]
E = (1, 5, 25, 125)
V = tuple(tuple(g // 5**j % 5 for j in range(4)) for g in range(625))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enc(v):
    return sum(x * 5**i for i, x in enumerate(v))


def inverse(matrix):
    n = len(matrix)
    a = [[x % 5 for x in row] + [int(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    determinant = 1
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None, 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            determinant = -determinant
        determinant = determinant * a[j][j] % 5
        scale = pow(a[j][j], -1, 5)
        a[j] = [x * scale % 5 for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [(x - scale * y) % 5 for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a], determinant % 5


def apply(matrix, value):
    return tuple(sum(x*y for x, y in zip(row, value)) % 5 for row in matrix)


def multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right))) % 5
             for j in range(len(right[0]))] for i in range(len(left))]


def main():
    started = time.perf_counter()
    summary_path = BASE / 'evidence/seven_doubles_continue_probe.json'
    cores_path = BASE / 'evidence/seven_doubles_continue_probe_cores.jsonl'
    summary = json.loads(summary_path.read_text(encoding='utf-8'))
    assert summary['status'] == 'COMPLETE_PROBE_WITH_EXACT_COLORING_RESIDUAL'
    assert summary['processed_cores'] == 166195 and summary['colored_cores'] == 166180
    residuals = []
    with cores_path.open(encoding='utf-8') as stream:
        for line in stream:
            row = json.loads(line)
            if row['type'] == 'core' and not row['no_six_extension_by_coloring']:
                residuals.append(row)
    assert [row['blocks'] for row in residuals] == summary['residual_keys']
    assert len(residuals) == len({tuple(row['blocks']) for row in residuals}) == 15
    functionals = [v for v in V[1:] if next(x for x in v if x) == 1]
    hyperplanes = [{g for g, v in enumerate(V) if sum(a*b for a, b in zip(f, v)) % 5 == 0}
                  for f in functionals]
    assert len(functionals) == len(set(map(frozenset, hyperplanes))) == 156
    assert all(len(h) == 125 for h in hyperplanes)
    reference = ((1, 0, 0), (0, 1, 0), (0, 0, 1),
                 (1, 1, 0), (3, 2, 1), (3, 2, 2))
    reference4 = {(0, *v) for v in reference}
    records = []
    for row in residuals:
        blocks = row['blocks']
        support = list(E) + blocks
        assert len(set(support)) == 7 and len(row['candidates']) == 251
        counts = [2 * len(set(support) & h) for h in hyperplanes]
        h12 = [i for i, count in enumerate(counts) if count == 12]
        assert max(counts) == 12 and len(h12) == 1
        index = h12[0]
        inside = [g for g in support if g in hyperplanes[index]]
        outside, = [g for g in support if g not in hyperplanes[index]]
        assert len(inside) == 6
        distance = {}
        witnesses = {}
        zero_tuples = 0
        for coefficients in product(range(3), repeat=6):
            target = tuple(sum(c * V[g][j] for c, g in zip(coefficients, inside)) % 5 for j in range(4))
            code, length = enc(target), sum(coefficients)
            if code == 0:
                zero_tuples += 1
                assert length == 0
            if length < distance.get(code, 99):
                distance[code] = length
                witnesses[code] = coefficients
        sigma = enc(tuple(2 * sum(V[g][j] for g in inside) % 5 for j in range(4)))
        assert zero_tuples == 1 and set(distance) == hyperplanes[index]
        assert sigma != 0 and distance[sigma] == 12
        assert all(d <= 6 for g, d in distance.items() if g != sigma)
        assert dict(sorted(Counter(distance.values()).items())) == {0: 1, 1: 6, 2: 19, 3: 36, 4: 35, 5: 19, 6: 8, 12: 1}

        # Source basis: outside vector followed by three H vectors.
        for selected in combinations(inside, 3):
            source_basis = [outside, *selected]
            to_coordinates, determinant = inverse([list(r) for r in zip(*(V[g] for g in source_basis))])
            if determinant:
                break
        assert determinant
        local_support = [apply(to_coordinates, V[g])[1:] for g in inside]
        for columns in permutations(reference, 3):
            local_matrix = [list(r) for r in zip(*columns)]
            _, local_det = inverse(local_matrix)
            if local_det and {apply(local_matrix, v) for v in local_support} == set(reference):
                break
        else:
            raise AssertionError('no reference equivalence')
        extended = [[1, 0, 0, 0]] + [[0, *r] for r in local_matrix]
        matrix = multiply(extended, to_coordinates)
        _, matrix_det = inverse(matrix)
        assert matrix_det and apply(matrix, V[outside]) == (1, 0, 0, 0)
        assert {apply(matrix, V[g]) for g in inside} == reference4
        records.append({
            'blocks': blocks, 'candidate_count': 251, 'hyperplane_counts': counts,
            'unique_h12_functional': functionals[index], 'inside_support': inside,
            'inside_sequence': [g for g in inside for _ in range(2)], 'outside_double_value': outside,
            'coefficient_tuples_checked': 729, 'nonempty_zero_tuples': 0,
            'sigma_encoded': sigma, 'distance_histogram': dict(sorted(Counter(distance.values()).items())),
            'all_125_minimum_representations': [
                {'target_encoded': g, 'minimum_length': distance[g], 'coefficients': witnesses[g]}
                for g in sorted(distance)],
            'source_basis_encoded': source_basis, 'matrix_to_reference': matrix,
            'matrix_determinant_mod5': matrix_det,
            'mapped_support_encoded': sorted(enc(apply(matrix, V[g])) for g in support)})
    output = {
        'status': 'ALL_15_RESIDUALS_DENSE12_AND_ONE_GL4_ORBIT_PRODUCER_CERTIFICATE',
        'independent_verification': 'required', 'expected_residual_count': 15,
        'records': records, 'all_156_hyperplanes_checked_per_core': True,
        'coefficient_tuples_checked': 15*729, 'target_representations_saved': 15*125,
        'reference_h12_support_coordinates': list(reference4),
        'reference_core_support_encoded': [1, 5, 25, 30, 125, 190, 315],
        'one_gl4_orbit': True, 'seconds': time.perf_counter() - started,
        'input_sha256': {str(p.relative_to(BASE)).replace('\\', '/'): sha(p) for p in (
            summary_path, cores_path, Path(__file__), BASE/'proofs/hyperplane_dense12.md',
            BASE/'proofs/atom_127_core.md', BASE/'scripts/atom_double_blocks.ps1',
            BASE/'evidence/atom_2222_m13_blocks.jsonl')}}
    output_path = BASE/'evidence/seven_doubles_continue_h12.json'
    output_path.write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: output[k] for k in ('status', 'expected_residual_count', 'coefficient_tuples_checked', 'target_representations_saved', 'seconds')}))


if __name__ == '__main__':
    main()
