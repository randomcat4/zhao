"""Enumerate zero-sum-free H cores and quotient only by S_3 coordinates."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--h-length',type=int,choices=(9,10,11,12),default=11)
parser.add_argument('--output',required=True)
args=parser.parse_args()
Q=125
INF=99
base=(1,5,25)
digit=[tuple(g//5**i%5 for i in range(3)) for g in range(Q)]
def enc(v): return sum(v[i]*5**i for i in range(3))
plus=[[enc(tuple((a[i]+b[i])%5 for i in range(3))) for b in digit] for a in digit]
neg=[enc(tuple(-x%5 for x in a)) for a in digit]
perms=list(itertools.permutations(range(3)))
transform=[[enc(tuple(digit[g][i] for i in p)) for g in range(Q)] for p in perms]
def adjoin(d,g):
    out=d[:]
    for h,k in enumerate(d):
        if k<INF: out[plus[g][h]]=min(out[plus[g][h]],k+1)
    return out
d=[INF]*Q
d[0]=0
counts=[0]*Q
for g in base:
    for _ in range(3):
        assert d[neg[g]]==INF
        d=adjoin(d,g)
        counts[g]+=1
raw=[]
def dfs(dist,candidates,path):
    if len(path)==args.h_length-9:
        raw.append(tuple(path))
        return
    for i,g in enumerate(candidates):
        if counts[g]>=2: continue
        counts[g]+=1
        nxt=adjoin(dist,g)
        following=[h for h in candidates[i:] if counts[h]<2 and nxt[neg[h]]==INF]
        dfs(nxt,following,path+[g])
        counts[g]-=1
dfs(d,[g for g in range(1,Q) if g not in base and d[neg[g]]==INF],[])
def canonical(xs):
    return min(tuple(sorted(t[g] for g in xs)) for t in transform)
orbits=Counter(canonical(xs) for xs in raw)
assert sum(orbits.values())==len(raw)
for xs,n in orbits.items():
    assert n==len({tuple(sorted(t[g] for g in xs)) for t in transform})
core_records=[]
for xs,n in sorted(orbits.items()):
    dx=d
    for g in xs: dx=adjoin(dx,g)
    record={'id':','.join(map(str,xs)),'added':xs,'orbit_size':n,
            'distance_counts':{str(k):dx.count(k) for k in range(13) if dx.count(k)},
            'unreachable_points':[g for g in range(Q) if dx[g]==INF],
            'distance_at_least':{str(k):sum(v>=k for v in dx) for k in range(8,13)},
            'distance_table':dx}
    core_records.append(record)
result={
    'group':'C_5^3','h_length':args.h_length,'base_multiplicities':[3,3,3],
    'new_capacity':2,'zero_sum_free':True,'completed_exhaustively':True,
    'raw_core_count':len(raw),'symmetry_group':'S_3 coordinate permutations',
    'canonical_core_count':len(orbits),'raw_extensions':raw,
    'cores':core_records,
    'coverage_minimum':min(Q-len(r['unreachable_points']) for r in core_records),
    'unreachable_maximum':max(len(r['unreachable_points']) for r in core_records),
    'distance_at_least_maxima':{str(k):max(r['distance_at_least'][str(k)] for r in core_records) for k in range(8,13)},
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('h_length','raw_core_count','canonical_core_count','completed_exhaustively','coverage_minimum','unreachable_maximum','distance_at_least_maxima')}))
