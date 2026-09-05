"""Bounded profile of zero-free 3,3,2,2,2 cores in F5^3, not an endpoint proof."""
from itertools import product
from pathlib import Path
import json
import numpy as np

out = Path(__file__).resolve().parents[1] / 'evidence' / 'root_33222_hyperplane_profile.json'
vec = np.array(list(product(range(5), repeat=3)), dtype=np.int16)
# Coordinate code is 25*x+5*y+z in this stand-alone probe.
weights = np.array([25, 5, 1], dtype=np.int16)
sub = ((vec[:, None, :] - vec[None, :, :]) % 5) @ weights
neg = ((-vec) % 5) @ weights
twice = ((2*vec) % 5) @ weights
basis = [25, 5, 1]
seq0 = [25]*3 + [5]*3 + [1]*2
d0 = np.full(125, 99, dtype=np.int16)
d0[0] = 0
for g in seq0:
    d0 = np.minimum(d0, 1+d0[sub[:, g]])

def safe2(d, g):
    return d[neg[g]]+1>12 and d[neg[twice[g]]]+2>12

def add2(d, g):
    return np.minimum(np.minimum(d, 1+d[sub[:, g]]), 2+d[sub[:, twice[g]]])

rows = []
pool = [x for x in range(1,125) if x not in basis]
for i,u in enumerate(pool):
    if not safe2(d0, u): continue
    du = add2(d0,u)
    for v in pool[i+1:]:
        if not safe2(du, v): continue
        dv = add2(du,v)
        sigma = int(((3*vec[25]+3*vec[5]+2*vec[1]+2*vec[u]+2*vec[v])%5)@weights)
        assert sigma != 0 and dv[sigma] == 12 and max(dv)<99
        mx = int(np.max(np.delete(dv,sigma)))
        rows.append({'u':u,'v':v,'sigma':sigma,'max_distance_except_total':mx,'E10':int(np.sum(dv>=10)),'E9':int(np.sum(dv>=9))})
hist = {str(k):sum(r['max_distance_except_total']==k for r in rows) for k in sorted({r['max_distance_except_total'] for r in rows})}
result = {'scope':'fixed independent 3,3,2 basis and two distinct nonbasis double blocks; full candidate domain; no GL quotient used', 'candidate_pairs':len(pool)*(len(pool)-1)//2,'zero_free_cores':len(rows),'distance_histogram':hist,'max_E10':max(r['E10'] for r in rows),'max_E9':max(r['E9'] for r in rows),'rows':rows,'status':'COMPUTED_PROFILE_NOT_INDEPENDENTLY_VERIFIED'}
out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
