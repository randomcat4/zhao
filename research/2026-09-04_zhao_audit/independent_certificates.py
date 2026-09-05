"""Independent subset DP audit; does not execute the supplied checker."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json

def histogram(seq, moduli):
    # Each index is one occurrence, including repeated group elements.
    sums = [(0,) * len(moduli)] * (1 << len(seq))
    result = Counter()
    for mask in range(1, 1 << len(seq)):
        bit = mask & -mask
        prior = sums[mask ^ bit]
        x = seq[bit.bit_length() - 1]
        value = tuple((a + b) % q for a, b, q in zip(prior, x, moduli))
        sums[mask] = value
        if not any(value):
            result[mask.bit_count()] += 1
    return dict(sorted(result.items()))

a,b,c = (0,1,0,0),(0,0,1,0),(0,0,0,1)
s1 = [a]*3 + [b]*3 + [c]*3 + [(1,2,3,3),(1,3,2,3),(1,3,3,2)]
s2 = [(0,0,1,2)]*3 + [(1,0,1,3),(1,0,2,1),(0,1,2,1),(0,0,1,1),(1,1,1,3)] + [(0,1,1,3)]*3 + [(1,1,2,1),(0,0,2,3)]
h = [1,2,4,8,15,16,32,64,53,90,108]
six = [0,1,2,3,4,5,8,9,16,17,32,33,64,65,128,129,254,255]
golay = [1,3,6,12,24,49,99,199,398,797,1594,3189,2282,468,936,1872,3744,3392,2688,1280,2560,1024,2048,4095]
def vectors(values,d):
    return [tuple((x>>j)&1 for j in range(d)) for x in values]

out = {
    'C2+C4^3_all_zero_sums': histogram(s1,(2,4,4,4)),
    'C2^2+C4^2_all_zero_sums': histogram(s2,(2,2,4,4)),
    'C2^7_length11_all_zero_sums': histogram(vectors(h,7),(2,)*7),
    'C2^7_length14_all_zero_sums': histogram(vectors(h+[0]*3,7),(2,)*7),
    'C2^8_length18_all_zero_sums': histogram(vectors(six,8),(2,)*8),
}
# Independent Golay check through the kernel, instead of small-subset enumeration.
basis = {}
dependencies = []
for i, column in enumerate(golay):
    x,mask = column,1<<i
    while x:
        pivot=x.bit_length()-1
        if pivot not in basis:
            basis[pivot]=(x,mask)
            break
        y,other=basis[pivot]
        x^=y;mask^=other
    if not x:
        dependencies.append(mask)
words=[0]
for word in dependencies:
    words += [x^word for x in words]
out['Golay_rank']=len(basis)
out['Golay_kernel_weight_distribution']=dict(sorted(Counter(x.bit_count() for x in words).items()))
assert out['C2+C4^3_all_zero_sums']=={10:9}
assert min(out['C2^2+C4^2_all_zero_sums'])>=6
assert min(out['C2^7_length11_all_zero_sums'])>=5
assert 4 not in out['C2^7_length14_all_zero_sums']
assert 6 not in out['C2^8_length18_all_zero_sums']
assert len(basis)==12 and min(x.bit_count() for x in words if x)==8
out['status']='ALL_INDEPENDENT_CERTIFICATES_PASS'
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
