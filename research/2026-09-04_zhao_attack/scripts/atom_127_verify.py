"""Verify the nine-core finite certificate by plain modular integer arithmetic."""
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

base=Path(__file__).resolve().parent.parent
source=base/'evidence/atom_127_classification.json'
data=json.loads(source.read_text(encoding='utf-8'))
reference={tuple(v) for v in data['reference_support_h']}
def det(m):
    total=0
    for p in itertools.permutations(range(3)):
        inversions=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        product=1
        for i in range(3): product*=m[i][p[i]]
        total+=(-1 if inversions%2 else 1)*product
    return total%5
checked=[]
for record in data['records']:
    support=[tuple(v) for v in record['support_h']]
    sigma=tuple(record['sigma_h'])
    assert sigma!=tuple(0 for _ in range(3))
    assert sigma==tuple(2*sum(v[j] for v in support)%5 for j in range(3))
    attainable={}
    zero_tuples=0
    tuples=0
    for coefficients in itertools.product((0,1,2),repeat=6):
        tuples+=1
        value=tuple(sum(coefficients[i]*support[i][j] for i in range(6))%5 for j in range(3))
        length=sum(coefficients)
        if value==(0,0,0):
            zero_tuples+=1
            assert length==0
        attainable[value]=min(attainable.get(value,100),length)
    assert tuples==729 and zero_tuples==1 and len(attainable)==125
    assert attainable[sigma]==12
    assert all(length<=6 for value,length in attainable.items() if value!=sigma)
    listed=record['all_125_minimum_representations']
    assert len(listed)==125 and len({tuple(r['target_h']) for r in listed})==125
    for r in listed:
        value=tuple(r['target_h'])
        coefficients=r['coefficients']
        assert len(coefficients)==6 and all(c in (0,1,2) for c in coefficients)
        assert tuple(sum(coefficients[i]*support[i][j] for i in range(6))%5 for j in range(3))==value
        assert sum(coefficients)==r['minimum_length']==attainable[value]
    assert {str(k):v for k,v in sorted(Counter(attainable.values()).items())}==record['distance_histogram']
    matrix=record['matrix_h_to_reference']
    determinant=det(matrix)
    assert determinant!=0 and determinant==record['matrix_h_determinant']
    assert {tuple(sum(matrix[i][j]*v[j] for j in range(3))%5 for i in range(3)) for v in support}==reference
    def global_distance(g):
        coordinates=tuple(g//5**i%5 for i in range(4))
        if coordinates[0]==4: return 99
        return coordinates[0]+attainable[coordinates[1:]]
    negative=[sum((-(g//5**i%5))%5*5**i for i in range(4)) for g in range(625)]
    for name,m in (('a',13),('b',14)):
        safe=[g for g in range(625) if global_distance(negative[g])>=m]
        assert safe==record['safe_all_'+name]
        core_support={1,5,25,125}|set(record['blocks_encoded'])
        assert [g for g in safe if g not in core_support]==record['safe_outside_core_'+name]
    checked.append({'blocks':record['blocks_encoded'],'matrix_to_reference':matrix,'determinant':determinant,
                    'all_729_coefficients_checked':True,'all_125_representations_validated':True})
assert len(checked)==9
result={'status':'ALL_NINE_FINITE_PROFILE_AND_EQUIVALENCE_CERTIFICATES_VERIFIED',
    'core_count':9,'coefficient_tuples_checked':9*729,'target_representations_checked':9*125,
    'reference_support_h':data['reference_support_h'],'checks':checked,
    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(base/'evidence/atom_127_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
