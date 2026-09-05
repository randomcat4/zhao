"""Check the canonical affine coefficient functional and high-distance residues."""
import collections
import itertools
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'evidence/atom_h11_core_profiles.json').read_text(encoding='utf-8'))
digits=[tuple(g//5**i%5 for i in range(3)) for g in range(125)]
records=[]
for c in data['cores']:
    x,y=[digits[g] for g in c['added']]
    a=tuple((x[(i+1)%3]*y[(i+2)%3]+x[(i+2)%3]*y[(i+1)%3])%5 for i in range(3))
    lin=[sum(v*w for v,w in zip(a,t))%5 for t in digits]
    s=tuple((3+x[i]+y[i])%5 for i in range(3))
    assert sum(u*v for u,v in zip(a,s))%5==3
    assert all(lin[g]==4 for g in c['unreachable_points'])
    d=c['distance_table']
    projections={str(k):sorted({lin[g] for g in range(125) if d[g]>=k}) for k in range(5,13)}
    counts={str(k):dict(collections.Counter(lin[g] for g in range(125) if d[g]>=k)) for k in range(5,13)}
    records.append({'id':c['id'],'a':a,'sigma':s,'projections':projections,'counts':counts})
result={'status':'EXACT_FINITE_PROBE','records':records,'summary':{
    str(k):dict(collections.Counter(str(r['projections'][str(k)]) for r in records)) for k in range(5,13)}}
(ROOT/'h11_continue_polynomial.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result['summary']))
print('E10 residue0',[(r['id'],r['counts']['10']) for r in records if 0 in r['projections']['10']])
