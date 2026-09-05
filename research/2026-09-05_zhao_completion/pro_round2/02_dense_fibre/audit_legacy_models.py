"""Red-team controls from the pinned old squarefree thread.
These are countermodels to weakened intermediate assertions, not to the theorem.
Checks every positional subset by Gray traversal and a separate length DP.
"""
import sys
if sys.flags.optimize: raise RuntimeError('Run without -O.')
from pathlib import Path
from math import comb
from collections import Counter
from itertools import combinations
import json
P=Path(__file__).resolve().parent
V=[(x//125,x//25%5,x//5%5,x%5) for x in range(625)]
def enc(v):return sum(a*b for a,b in zip(v,(125,25,5,1)))
def add(x,y):return enc(tuple((a+b)%5 for a,b in zip(V[x],V[y])))
NEG=[enc(tuple(-a%5 for a in v)) for v in V]

def two_algorithms(vectors):
    labels=[enc(v) for v in vectors];n=len(labels)
    plus=[[add(v,g) for g in range(625)] for v in labels]
    minus=[[add(NEG[v],g) for g in range(625)] for v in labels]
    a=[[0]*625 for _ in range(n+1)];a[0][0]=1
    minlen=[n+1]*625;minmask=[None]*625;minlen[0]=0;minmask[0]=0
    value=0;weight=0
    for i in range(1,1<<n):
        bit=i&-i;j=bit.bit_length()-1;gray=i^(i>>1)
        if gray&bit:value=plus[j][value];weight+=1
        else:value=minus[j][value];weight-=1
        a[weight][value]+=1
        if weight<minlen[value]:minlen[value]=weight;minmask[value]=gray
    b=[[0]*625 for _ in range(n+1)];b[0][0]=1
    for j in range(n):
        for k in range(j+1,0,-1):
            old=b[k-1];new=b[k]
            for g in range(625):new[plus[j][g]]+=old[g]
    assert a==b and sum(map(sum,a))==1<<n
    assert all(sum(a[k])==comb(n,k) for k in range(n+1))
    return labels,a,minlen,minmask

rows=[
[4,2,2,3,1,4,2,2,3,1,4,3,1,0,1,0,2,4,4,3,4],
[0,4,4,1,3,1,0,0,2,4,4,1,4,4,1,2,4,4,3,0,0],
[1,2,4,0,0,4,0,2,3,3,2,2,2,2,1,0,1,2,2,3,2],
[0,4,0,2,0,4,3,4,1,4,1,1,4,0,1,0,1,3,3,2,1]]
blocks=[
[0,4,6,7,13,16,20],[0,1,7,8,14,17,20],[1,2,8,9,10,18,20],[2,3,5,9,11,19,20],[3,4,5,6,12,15,20],
[0,3,7,12,14,15,18],[1,4,8,10,13,16,19],[0,2,9,11,14,15,17],[1,3,5,10,12,16,18],[2,4,6,11,13,17,19],
[4,6,8,10,14,15,17],[0,7,9,10,11,16,18],[1,5,8,11,12,17,19],[2,6,9,12,13,15,18],[3,5,7,13,14,16,19]]
vectors=list(zip(*rows));labels,hist,_,_=two_algorithms(vectors)
assert len(set(labels))==21 and 0 not in labels
s=enc(tuple(sum(row)%5 for row in rows));assert V[s]==(0,1,3,4)
for b in blocks:assert len(b)==len(set(b))==7 and enc(tuple(sum(vectors[i][j] for i in b)%5 for j in range(4)))==s
assert [sum(x in b for b in blocks) for x in range(21)]==[5]*21
inter=Counter(len(set(a)&set(b)) for a,b in combinations(blocks,2))
assert inter=={0:10,1:25,2:25,3:45} and hist[7][s]==238
assert add(add(labels[0],labels[7]),labels[20])==0
atom=[(1,3,2,4),(2,3,0,1),(0,1,0,1),(1,1,3,3),(4,4,3,3),(2,1,4,0),(4,4,3,0),(4,0,3,1),(4,1,3,2),(4,3,3,2),(3,3,0,0),(3,3,1,3),(2,4,4,1),(1,4,1,4)]
al,ah,ml,mm=two_algorithms(atom)
assert len(set(al))==14 and 0 not in al and ah[14][0]==1 and all(ah[k][0]==0 for k in range(1,14))
holes=[g for g in range(625) if all(ah[k][g]==0 for k in range(15))]
assert holes==[42,64,91,113,129,178,247,280,312,468,495,501,533,577]
pair_witnesses=[]
for b,c in combinations(holes,2):
    target=NEG[add(b,c)];assert ml[target]<=11
    positions=[i for i in range(14) if mm[target]>>i&1]
    assert len(positions)==ml[target]
    result=0
    for i in positions:result=add(result,al[i])
    assert add(add(result,b),c)==0
    pair_witnesses.append({'outside_codes':[b,c],'atom_positions':positions,'zero_sum_length':len(positions)+2})
assert len(pair_witnesses)==91
out={'provenance':{'repository':'randomcat4/zhao','commit':'9d33328880a13609f047905af14e530172b42ae3','path':'research/2026-09-05_zhao_completion/pro_round1/01_squarefree.md'},
     'formal_15_blocks':{'vectors':vectors,'blocks':blocks,'intersection_counts':dict(inter),'sum':V[s], 'complete_C7_size':238,'short_zero_positions':[0,7,20], 'all_zero_counts':[hist[k][0] for k in range(22)],'subset_denominator_per_algorithm':1<<21,'algorithms_agree':True},
     'fourteen_atom':{'vectors':atom,'holes':holes,'all_zero_counts':[ah[k][0] for k in range(15)],'subset_denominator_per_algorithm':1<<14,'algorithms_agree':True,'outside_pair_denominator':91,'outside_pairs_checked':pair_witnesses},
     'exit':'NORMAL'}
print(json.dumps(out,indent=2))
