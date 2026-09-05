"""Counterexample probe for a stronger H12 covering lemma; never a proof by sampling."""
from pathlib import Path
from collections import Counter
from itertools import product
import time, json, random
import numpy as np

root = Path(__file__).resolve().parents[1]
vec = np.array(list(product(range(5), repeat=3)), dtype=np.int16)
w = np.array([25, 5, 1], dtype=np.int16)
sub = ((vec[:, None, :] - vec[None, :, :]) % 5) @ w
neg = ((-vec) % 5) @ w
base = [25,5,1,30,86,87]
seed = tuple(sorted(base*2))
rng = random.Random(9042026)

def distance(seq):
    d = np.full(125, 99, dtype=np.int16); d[0] = 0
    safe = True
    for g in seq:
        if d[neg[g]] < 99: safe = False
        d = np.minimum(d, 1 + d[sub[:,g]])
    return d, safe

start=time.monotonic(); seen={seed}; current=seed; hist=Counter(); bad=None
steps=0
while time.monotonic()-start < 30:
    d, safe=distance(current)
    assert safe
    sigma=int((vec[list(current)].sum(axis=0)%5)@w)
    assert d[sigma]==12 and max(d)<99
    mx=int(np.max(np.delete(d,sigma))); hist[mx]+=1
    if mx>6:
        h=int(next(i for i in range(125) if i!=sigma and d[i]>6))
        bad={'sequence':list(current),'vectors':vec[list(current)].tolist(),'sigma':sigma,'exception':h,'distance':int(d[h]),'table':d.tolist()}
        break
    at=rng.randrange(12); short=current[:at]+current[at+1:]
    ds,ok=distance(short); assert ok
    count=Counter(short)
    candidates=[g for g in range(1,125) if ds[neg[g]]==99 and count[g]<2]
    assert candidates
    current=tuple(sorted(short+(rng.choice(candidates),)))
    seen.add(current); steps+=1

result={'claim_tested':'Every zero-free H12 with height<=2 covers H except total within 6 positions','status':'DISPROVED' if bad else 'INCOMPLETE_PROBE_ONLY','seed':seed,'steps':steps,'distinct_states':len(seen),'profile_visits':dict(hist),'seconds':time.monotonic()-start,'counterexample':bad}
(root/'evidence/root_continue_dense_probe.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
