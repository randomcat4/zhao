"""Short exact structural probe. No outside-extension DFS."""
import collections
import hashlib
import itertools
import json
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
V=list(itertools.product(range(5),repeat=3))
digits=[tuple(g//5**i%5 for i in range(3)) for g in range(125)]
def enc(v): return sum(v[i]*5**i for i in range(3))
def sub(a,b): return tuple((x-y)%5 for x,y in zip(a,b))
def rank(vs):
    a=[list(v) for v in vs]; r=0
    for c in range(3):
        p=next((p for p in range(r,len(a)) if a[p][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        inv=pow(a[r][c],-1,5); a[r]=[x*inv%5 for x in a[r]]
        for p in range(r+1,len(a)):
            z=a[p][c]; a[p]=[(x-z*y)%5 for x,y in zip(a[p],a[r])]
        r+=1
    return r
normals=[v for v in V if any(v) and next(x for x in v if x)==1]
def describe(xs):
    if not xs: return {'size':0,'affine_rank':-1,'min_projection_size':0}
    pts=[digits[g] for g in xs]; ar=rank([sub(p,pts[0]) for p in pts])
    ss=[]
    for n in normals:
        vals=sorted({sum(x*y for x,y in zip(n,p))%5 for p in pts})
        ss.append((len(vals),n,vals))
    m=min(x[0] for x in ss)
    return {'size':len(xs),'affine_rank':ar,'min_projection_size':m,
            'min_projections':[(n,vs) for k,n,vs in ss if k==m]}

def main():
    start=time.monotonic()
    source=ROOT/'evidence/atom_h11_core_profiles.json'
    data=json.loads(source.read_text(encoding='utf-8'))
    rows=[]
    for core in data['cores']:
        x,y=[digits[g] for g in core['added']]
        d=core['distance_table']
        row={'id':core['id'],'added_vectors':[x,y],
             'common_zero_coordinates':[i for i in range(3) if x[i]==y[i]==0],
             'profiles':{str(k):describe([g for g in range(125) if d[g]>=k]) for k in (8,9,10,11,12,99)}}
        rows.append(row)
    summary={str(k):dict(collections.Counter(
        (r['profiles'][str(k)]['size'],r['profiles'][str(k)]['affine_rank'],r['profiles'][str(k)]['min_projection_size'])
        for r in rows)) for k in (8,9,10,11,12,99)}
    summary={k:{str(t):v for t,v in ctr.items()} for k,ctr in summary.items()}
    result={'status':'STRUCTURAL_PROBE_ONLY','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'core_count':len(rows),'elapsed_seconds':time.monotonic()-start,'summary':summary,'cores':rows}
    (ROOT/'h11_continue_structure.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('core_count','elapsed_seconds','summary')}))
    print('common_zero',[r['id'] for r in rows if r['common_zero_coordinates']])
    print('unreach_affine_plane',[(r['id'],r['profiles']['99']['size']) for r in rows if r['profiles']['99']['affine_rank']<=2])
if __name__=='__main__': main()
