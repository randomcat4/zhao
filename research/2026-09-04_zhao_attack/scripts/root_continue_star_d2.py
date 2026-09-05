"""Complete small certificates for the d=2, M=1 star branch.

Only scalar count patterns and 2048 subsets of one fixed H11 core are used.
No search over outside extensions or over endpoint sequences is performed.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
grid = list(product(range(5), repeat=3))
x, y, z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
g, h = (1, 1, 0), (1, 0, 1)
V = [x] + [g] * 3 + [y] * 3 + [h] * 2 + [z] * 2
d = {t: 99 for t in grid}
signed = Counter()
zeros = []
for mask in range(1 << 11):
    w = mask.bit_count()
    t = tuple(sum(V[j][i] for j in range(11) if mask >> j & 1) % 5 for i in range(3))
    d[t] = min(d[t], w)
    signed[t] += (-1) ** w
    if mask and not any(t):
        zeros.append(mask)
assert not zeros
ell = lambda t: (3 * t[0] + t[1] + t[2]) % 5
assert all(signed[t] % 5 == (1 + ell(t)) % 5 for t in grid)
missing = [t for t in grid if d[t] == 99]
e10 = [t for t in grid if d[t] >= 10]
f0 = [t for t in e10 if ell(t) == 0]
f3 = [t for t in e10 if ell(t) == 3]
assert missing == [(0, 4, 0), (1, 2, 4), (2, 4, 4), (4, 2, 0)]
assert f0 == [(0, 1, 4)] and f3 == [(1, 1, 4)]

# r=-1 means all nine positions have distinct actual vectors.
# Otherwise r is the scalar class containing the sole repeated actual vector.
# Within every other class the vectors are distinct. Within class r there is
# exactly one double value and all remaining values are single.
rows = []
for n in product(range(10), repeat=5):
    if sum(n) != 9:
        continue
    marks = [-1] + [r for r in range(5) if n[r] >= 2]
    candidates = []
    for k in product(*(range(v + 1) for v in n)):
        if sum(k) != 5:
            continue
        residue = sum(c * k[c] for c in range(5)) % 5
        if residue in (0, 2):
            candidates.append((k, residue))
    for r in marks:
        for k, residue in candidates:
            partial = [c for c in range(5) if 0 < k[c] < n[c]
                       and not (c == r and n[c] == 2)]
            if partial:
                rows.append({'n': n, 'repeat_class': r, 'k': k,
                             'residue': residue, 'vary_class': partial[0]})
                break
        else:
            raise AssertionError(('No scalar certificate', n, r))
assert len(rows) == 2365
assert sum(r['repeat_class'] == -1 for r in rows) == 715
assert sum(r['repeat_class'] != -1 for r in rows) == 1650

result = {
    'status': 'COMPLETE_SMALL_CERTIFICATES_ONLY',
    'core': V, 'position_subsets': 2048,
    'sigma': (1, 1, 4), 'ell': (3, 1, 1),
    'missing': missing, 'E10': e10,
    'E10_fiber_0': f0, 'E10_fiber_3': f3,
    'distance_and_signed': [{'t': t, 'd': d[t], 'P': signed[t] % 5} for t in grid],
    'scalar_count': len(rows), 'scalar_certificates': rows,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
out = ROOT / 'evidence' / 'root_continue_star_d2.json'
out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in result.items()
                  if k not in ('distance_and_signed', 'scalar_certificates')}, ensure_ascii=False))
