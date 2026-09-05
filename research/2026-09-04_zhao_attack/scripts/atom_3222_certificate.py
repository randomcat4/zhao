"""Check an actual length-17 survivor by all bounded coefficient tuples."""
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

root=Path(__file__).resolve().parent.parent
source=root/'evidence/atom_3222_m13_blocks.jsonl'
rows=[json.loads(s) for s in source.read_text(encoding='utf-8').splitlines()]
record=next(r for r in rows if r.get('type')=='root' and r['root']==6)
blocks=record['first_terminal_blocks']
assert blocks is not None and len(blocks)==4
encoded=[1,5,25,125]+blocks
vectors=[tuple(g//5**i%5 for i in range(4)) for g in encoded]
mult=[3]+[2]*7
zero_by_length=Counter()
relations=[]
visited=0
for coeff in itertools.product(*(range(n+1) for n in mult)):
    visited+=1
    length=sum(coeff)
    if length==0: continue
    if all(sum(c*v[j] for c,v in zip(coeff,vectors))%5==0 for j in range(4)):
        position_count=math.prod(math.comb(n,c) for n,c in zip(mult,coeff))
        zero_by_length[length]+=position_count
        relations.append({'coefficients':coeff,'length':length,'position_subsequence_count':position_count})
assert visited==4*3**7
assert min(zero_by_length)>=14
assert sum(mult)==17
certificate={'status':'CERTIFIED_LENGTH_17_SURVIVOR_NOT_AN_ENDPOINT_COUNTEREXAMPLE',
    'group':'C_5^4','sequence_length':17,'support_vectors':vectors,'multiplicities':mult,
    'expanded_vectors':[v for v,n in zip(vectors,mult) for _ in range(n)],
    'coefficient_tuples_checked_including_empty':visited,'position_subsets_covered_including_empty':2**17,
    'zero_sum_counts_by_length':dict(sorted(zero_by_length.items())),
    'all_nonempty_zero_sum_coefficient_tuples':relations,
    'minimum_zero_sum_length':min(zero_by_length),
    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(root/'evidence/atom_3222_length17_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:certificate[k] for k in ('status','support_vectors','multiplicities','coefficient_tuples_checked_including_empty','zero_sum_counts_by_length','minimum_zero_sum_length')}))
