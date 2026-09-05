#!/usr/bin/env python3
"""Finite certificates quoted in zhaonote02.tex (Python 3, no dependencies)."""
from itertools import combinations
def addzero(seq, mods, sizes):
    return {q: sum(all(sum(x[j] for x in c) % mods[j] == 0
                       for j in range(len(mods)))
                    for c in combinations(seq, q)) for q in sizes}
def xorzero(seq, sizes):
    def xorsum(c):
        s = 0
        for x in c:
            s ^= x
        return s
    return {q: sum(xorsum(c) == 0 for c in combinations(seq, q)) for q in sizes}
# C_2 + C_4^3: length 12, no zero sum of length <= 9.
A, B, C, T = (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 3, 3, 3)
sub = lambda x, y: tuple((a-b) % m for a, b, m in zip(x, y, (2, 4, 4, 4)))
S1 = [A]*3 + [B]*3 + [C]*3 + [sub(T, A), sub(T, B), sub(T, C)]
# C_2^2 + C_4^2: length 13, no zero sum of length <= 5.
S2 = [(0,0,1,2),(1,0,1,3),(1,0,2,1),(0,1,2,1),(0,0,1,1),
(1,1,1,3),(0,1,1,3),(0,1,1,3),(1,1,2,1),(0,0,2,3),
(0,0,1,2),(0,0,1,2),(0,1,1,3)]
# C_2^7: 11 columns have no zero sum of length <= 4; adding three zeros
# produces a 14-term sequence with no zero sum of length exactly 4.
H = [1, 2, 4, 8, 15, 16, 32, 64, 53, 90, 108]
S3 = H + [0, 0, 0]
# C_2^8: A x F_2, where A={0,e_1,...,e_7,1}; no zero six-subset.
base = [0] + [1 << i for i in range(7)] + [127]
S4 = [(x << 1) | b for x in base for b in (0, 1)]
# Extended binary Golay parity-check columns; no dependence of size <= 7.
S5 = [1,3,6,12,24,49,99,199,398,797,1594,3189,2282,468,936,1872,
3744,3392,2688,1280,2560,1024,2048,4095]
checks = {
"C2+C4^3 lengths 1..9": addzero(S1, (2,4,4,4), range(1,10)),
"C2^2+C4^2 lengths 1..5": addzero(S2, (2,2,4,4), range(1,6)),
"C2^7 length-11, sizes 1..4": xorzero(H, range(1,5)),
"C2^7 length-14, size 4": xorzero(S3, (4,)),
"C2^8 length-18, size 6": xorzero(S4, (6,)),
"Golay columns, sizes 1..7": xorzero(S5, range(1,8)),
}
assert all(v == 0 for row in checks.values() for v in row.values())
for name, result in checks.items():
    print(name, result)
print("ALL_CERTIFICATES_PASS")