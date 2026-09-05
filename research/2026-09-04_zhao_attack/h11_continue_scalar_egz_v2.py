"""Corrected 715-case certificate; the earlier stronger lemma is false."""
import itertools
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def compositions(n,k):
    if k==1:
        yield (n,); return
    for z in range(n+1):
        for tail in compositions(n-z,k-1): yield (z,)+tail
records=[]; failures=[]
for n in compositions(9,5):
    good=[]
    for k in itertools.product(*(range(min(v,5)+1) for v in n)):
        if sum(k)!=5: continue
        residue=sum(i*k[i] for i in range(5))%5
        partial=[i for i in range(5) if 0<k[i]<n[i]]
        if residue==0 and (any(n[i]>=3 for i in partial) or len(partial)>=2):
            good.append((0,k))
        if residue==2 and partial:
            good.append((2,k))
    if good:
        res,k=min(good); records.append({'n':n,'k':k,'residue':res})
    else: failures.append(n)
out={'status':'ALL_CASES_CERTIFIED' if not failures else 'FAILED',
     'statement':'For 9 distinct H vectors: >=3 distinct 5-sums in ell=0, or >=2 in ell=2.',
     'count_vectors':len(records)+len(failures),'certificates':records,'failures':failures}
(ROOT/'h11_continue_scalar_egz_v2.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='certificates'}))

# Separate certificate check, using a Cartesian enumeration rather than the
# generator's recursion and recomputing every local witness inequality.
lookup={tuple(r['n']):r for r in records}
all_counts={n for n in itertools.product(range(10),repeat=5) if sum(n)==9}
assert len(records)==len(lookup)==len(all_counts)==715
assert set(lookup)==all_counts and not failures
for n,r in lookup.items():
    k=r['k']; assert len(k)==5 and sum(k)==5
    assert all(0<=k[i]<=n[i] for i in range(5))
    res=sum(i*k[i] for i in range(5))%5
    assert res==r['residue']
    ps=[i for i in range(5) if 0<k[i]<n[i]]
    assert ((res==0 and (len(ps)>=2 or any(n[i]>=3 for i in ps)))
            or (res==2 and len(ps)>=1))
print('Independent certificate pass: 715/715')
