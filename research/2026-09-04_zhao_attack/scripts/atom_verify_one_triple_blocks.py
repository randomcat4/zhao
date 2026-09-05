"""Independent NumPy/gather implementation checking every recorded double-block root.

The search uses two consecutive one-position updates, rather than the C#
two-position scatter update. Group arithmetic and orbit minima are rebuilt.
"""
import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument('--evidence',nargs='+',required=True)
parser.add_argument('--output',required=True)
parser.add_argument('--seconds',type=float,default=45)
args=parser.parse_args()
start=time.monotonic()
Q=625
digits=np.array([[(g//5**i)%5 for i in range(4)] for g in range(Q)],dtype=np.int16)
weight=np.array([1,5,25,125],dtype=np.int16)
subtract=((digits[None,:,:]-digits[:,None,:])%5)@weight
negative=((-digits)%5)@weight
neg_twice=((-2*digits)%5)@weight
basis=(1,5,25,125)
def add_one(d,g): return np.minimum(d,d[subtract[g]]+1)
summaries=[]
for filename in args.evidence:
    lines=[json.loads(s) for s in Path(filename).read_text(encoding='utf-8').splitlines()]
    meta=lines[0]
    mode=meta.get('mode','3322')
    m=meta['m']
    assert mode=='3222'
    mult=(3,2,2,2)
    core_length=sum(mult)
    d=np.full(Q,99,dtype=np.int16)
    d[0]=0
    for g,n in zip(basis,mult):
        for _ in range(n):
            assert d[negative[g]]==99
            d=add_one(d,g)
    def safe(ds,candidates):
        candidates=np.asarray(candidates,dtype=np.int16)
        one=ds[negative[candidates]]
        after_one=np.minimum(one,1+ds[neg_twice[candidates]])
        return candidates[(one>=m)&(after_one>=m)]
    universe=np.array([g for g in range(1,Q) if g not in basis],dtype=np.int16)
    initial=safe(d,universe)
    assert initial.tolist()==meta['initial_safe_candidates']
    permutations=[(0,)+p for p in itertools.permutations((1,2,3))]
    orbit_min=np.min(np.array([(digits[:,p]@weight) for p in permutations]),axis=0)
    roots=[int(g) for g in initial if orbit_min[g]==g]
    assert roots==meta['canonical_roots']
    records={r['root']:r for r in lines if r['type']=='root'}
    assert set(records)==set(roots)
    assert all(r['completed_exhaustively'] for r in records.values())
    checked=[]
    for root in roots:
        levels=Counter()
        leaves=Counter()
        def dfs(ds,candidates,depth):
            if time.monotonic()-start>args.seconds: raise TimeoutError('bounded verification did not finish')
            length=core_length+2*depth
            levels[length]+=1
            if length==meta['target']: return
            if len(candidates)==0:
                leaves[length]+=1
                return
            for i,g in enumerate(candidates):
                assert ds[negative[g]]>=m
                once=add_one(ds,g)
                assert once[negative[g]]>=m
                twice=add_one(once,g)
                following=safe(twice,candidates[i+1:])
                dfs(twice,following,depth+1)
        once=add_one(d,root)
        assert d[negative[root]]>=m and once[negative[root]]>=m
        root_dist=add_one(once,root)
        dfs(root_dist,safe(root_dist,initial[initial>root]),1)
        actual={'nodes':sum(levels.values()),'nodes_by_length':{str(k):v for k,v in levels.items()},
                'leaves_by_length':{str(k):v for k,v in leaves.items()},'max_reached_length':max(levels),
                'terminal_count':levels.get(meta['target'],0)}
        for key,value in actual.items(): assert records[root][key]==value,(filename,root,key,records[root][key],value)
        checked.append({'root':root,**actual})
    summary={'source':filename,'source_sha256':hashlib.sha256(Path(filename).read_bytes()).hexdigest(),
             'mode':mode,'m':m,'root_count':len(roots),'all_roots_identical':True,
             'nodes':sum(r['nodes'] for r in checked),'maximum_length':max(r['max_reached_length'] for r in checked),
             'checked_roots':checked}
    summaries.append(summary)
    print(json.dumps({k:summary[k] for k in ('source','mode','m','root_count','all_roots_identical','nodes','maximum_length')}),flush=True)
result={'status':'ALL_COMPARISONS_PASSED','verification':'separate NumPy gather implementation and explicit orbit minima',
        'seconds':time.monotonic()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'runs':summaries}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'seconds':result['seconds']}))
