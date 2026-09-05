"""Exact zero-sum-free extensions of e_1^3 e_2^3 e_3^3 within C_5^3.

All additional multiplicities are <=2; this isolates the case of exactly three
tripled elements. No conclusion about the outside positions is asserted.
"""

import json
from pathlib import Path

SIZE = 125
INF = 99
BASE = (1, 5, 25)
digits = [tuple((g // 5**i) % 5 for i in range(3)) for g in range(SIZE)]
def encode(v):
    return sum(v[i]*5**i for i in range(3))
plus = [[encode(tuple((a[i]+b[i])%5 for i in range(3))) for b in digits] for a in digits]
neg = [encode(tuple((-a[i])%5 for i in range(3))) for a in digits]
def add(dist, g):
    out = dist[:]
    for h, length in enumerate(dist):
        if length < INF:
            v = plus[g][h]
            out[v] = min(out[v], length+1)
    return out

dist = [INF]*SIZE
dist[0] = 0
counts = [0]*SIZE
for g in BASE:
    for _ in range(3):
        assert dist[neg[g]] == INF
        dist = add(dist, g)
        counts[g] += 1
initial = [g for g in range(1,SIZE) if g not in BASE and dist[neg[g]]==INF]
levels = [0]*13
full = []
leaves = []
def dfs(d, candidates, added):
    length = 9+len(added)
    levels[length] += 1
    if length==12:
        assert INF not in d
        full.append(added[:])
        return
    has_child = False
    for i,g in enumerate(candidates):
        if counts[g]>=2:
            continue
        assert d[neg[g]]==INF
        counts[g] += 1
        updated=add(d,g)
        following=[h for h in candidates[i:] if counts[h]<2 and updated[neg[h]]==INF]
        has_child=True
        dfs(updated,following,added+[g])
        counts[g] -= 1
    if not has_child:
        leaves.append(added[:])
dfs(dist,initial,[])
result={
    "group":"C_5^3", "core_multiplicities":[3,3,3],
    "additional_capacity":2, "completed_exhaustively":True,
    "initial_safe_candidates":initial,
    "nodes_by_length":{str(i):c for i,c in enumerate(levels) if c},
    "length12_extensions":full,
    "max_reached_length":max(i for i,c in enumerate(levels) if c),
    "other_leaf_extensions":leaves,
}
profiles={}
for added in full:
    d=dist
    for g in added:
        d=add(d,g)
    profile=tuple(d.count(k) for k in range(13))
    if profile not in profiles:
        profiles[profile]={"count":0,"one_extension":added}
    profiles[profile]["count"]+=1
result["length12_distance_profiles"]=[{"counts_by_distance":p,**record} for p,record in profiles.items()]
output=Path(__file__).resolve().parent.parent/'evidence/atom_three_hyperplane.json'
output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('nodes_by_length','max_reached_length','length12_distance_profiles')}))
