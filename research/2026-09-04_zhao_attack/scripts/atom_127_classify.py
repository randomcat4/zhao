"""Classify only the nine saved 127-candidate cores and certify their profiles.

Uses bounded coefficient enumeration, not extension search. Automorphisms fix e1
and act on H by explicit invertible 3-by-3 matrices over F5.
"""
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

base=Path(__file__).resolve().parent.parent
frozen_blocks=[(345,455,505),(215,225,565),(160,185,505),
               (45,180,305),(45,220,345),(45,415,485),
               (30,190,315),(30,210,335),(30,420,480)]
source=base/'evidence/atom_3222_len15_scan_check.json'
saved=json.loads(source.read_text(encoding='utf-8'))
assert [tuple(r['blocks']) for r in saved['extreme_nodes_with_more_than20_candidates']]==frozen_blocks

def vec(g,rank): return tuple(g//5**i%5 for i in range(rank))
def enc(v): return sum(x*5**i for i,x in enumerate(v))
def neg(g,rank): return enc(tuple(-x%5 for x in vec(g,rank)))
def determinant(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))%5
def mat_apply(m,v): return tuple(sum(a*b for a,b in zip(row,v))%5 for row in m)

reference_blocks=(30,190,315)
reference_h=[(1,0,0),(0,1,0),(0,0,1)]+[vec(g//5,3) for g in reference_blocks]
reference_set=set(reference_h)
records=[]
for blocks in frozen_blocks:
    assert all(g%5==0 for g in blocks)
    support_h=[(1,0,0),(0,1,0),(0,0,1)]+[vec(g//5,3) for g in blocks]
    assert len(set(support_h))==6
    distance=[99]*125
    witnesses=[None]*125
    coefficient_count=0
    nonempty_zeros=[]
    for coeff in itertools.product(range(3),repeat=6):
        coefficient_count+=1
        h=tuple(sum(c*v[j] for c,v in zip(coeff,support_h))%5 for j in range(3))
        code=enc(h)
        length=sum(coeff)
        if code==0 and length: nonempty_zeros.append(coeff)
        if length<distance[code]: distance[code]=length;witnesses[code]=coeff
    sigma=tuple(2*sum(v[j] for v in support_h)%5 for j in range(3))
    sigma_code=enc(sigma)
    c=tuple(-x%5 for x in sigma)
    assert coefficient_count==729 and not nonempty_zeros
    assert sigma_code!=0 and distance[sigma_code]==12
    assert all(d<=6 for h,d in enumerate(distance) if h!=sigma_code)
    assert max(distance)==12 and 99 not in distance
    matrix=None
    for columns in itertools.permutations(reference_h,3):
        proposed=[list(row) for row in zip(*columns)]
        if determinant(proposed) and {mat_apply(proposed,v) for v in support_h}==reference_set:
            matrix=proposed
            break
    assert matrix is not None
    full_matrix=[[1,0,0,0]]+[[0]+row for row in matrix]
    # Separate enumeration of all 4*3^6 coefficient tuples for e1^3 U.
    global_distance=[99]*625
    for t in range(4):
        for coeff in itertools.product(range(3),repeat=6):
            h=tuple(sum(c0*v[j] for c0,v in zip(coeff,support_h))%5 for j in range(3))
            g=t+5*enc(h)
            global_distance[g]=min(global_distance[g],t+sum(coeff))
    for g in range(625):
        expected=99 if g%5==4 else g%5+distance[g//5]
        assert global_distance[g]==expected
    safe_a=[g for g in range(625) if global_distance[neg(g,4)]>=13]
    safe_b=[g for g in range(625) if global_distance[neg(g,4)]>=14]
    coset=[g for g in range(625) if g%5==1]
    exceptions=[k+5*enc(c) for k in (2,3,4)]
    assert safe_a==sorted(coset+exceptions)
    assert safe_b==sorted(coset+exceptions[:2])
    core_support={1,5,25,125}|set(blocks)
    outside_a=[g for g in safe_a if g not in core_support]
    outside_b=[g for g in safe_b if g not in core_support]
    assert len(safe_a)==128 and len(outside_a)==127
    assert len(safe_b)==127 and len(outside_b)==126
    records.append({'blocks_encoded':blocks,'support_h':support_h,'h_multiplicities':[2]*6,
        'coefficient_tuples_checked':coefficient_count,'zero_sum_free':True,
        'sigma_h':sigma,'negative_sigma_h':c,
        'distance_histogram':dict(sorted(Counter(distance).items())),
        'all_125_minimum_representations':[{'target_h':vec(h,3),'minimum_length':distance[h],'coefficients':witnesses[h]} for h in range(125)],
        'matrix_h_to_reference':matrix,'matrix_h_determinant':determinant(matrix),'matrix_c5_4_to_reference':full_matrix,
        'global_coefficient_tuples_checked':4*729,'safe_all_a':safe_a,'safe_outside_core_a':outside_a,
        'safe_all_b':safe_b,'safe_outside_core_b':outside_b,'exceptional_values_encoded':exceptions})
result={'status':'NINE_CORES_ONE_ORBIT_AND_PROFILES_CERTIFIED','group':'C_5^4',
    'h_equation':'first coordinate = 0','outside_tripled_element':[1,0,0,0],
    'reference_blocks_encoded':reference_blocks,'reference_support_h':reference_h,
    'core_count':len(records),'single_GL_H_orbit':True,'records':records,
    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
output=base/'evidence/atom_127_classification.json'
output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'core_count':len(records),
    'reference_support_h':reference_h,'distance_histogram':records[0]['distance_histogram'],
    'safe_all_a':128,'safe_outside_core_a':127,'safe_all_b':127,'safe_outside_core_b':126}))
