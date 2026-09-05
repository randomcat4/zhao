"""715 explicit certificates for a three-value restricted EGZ lemma."""
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
        if sum(k)!=5 or sum(i*k[i] for i in range(5))%5: continue
        # A partially selected class with >=3 points gives >=3 distinct sums;
        # two partially selected classes give a sum of two nontrivial 2-sets.
        partial=[i for i in range(5) if 0<k[i]<n[i]]
        if any(n[i]>=3 for i in partial) or len(partial)>=2:
            good.append(k)
    if good: records.append({'n':n,'k':min(good)})
    else: failures.append(n)
out={'status':'ALL_CASES_CERTIFIED' if not failures else 'FAILED',
     'count_vectors':len(records)+len(failures),'certificates':records,'failures':failures}
(ROOT/'h11_continue_scalar_egz.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='certificates'}))
