"""Bounded exact DFS for H12, height2, containing three independent doubled values.

Incomplete output is explicitly not a classification. Position-subset sums use exact
125-bit sets and coordinatewise translation, not cyclic base-125 arithmetic.
"""
from pathlib import Path
from itertools import permutations
from collections import Counter
import time,json

root=Path(__file__).resolve().parents[1]
vec=[(i%5,(i//5)%5,i//25) for i in range(125)]
neg=[sum((-x%5)*5**j for j,x in enumerate(v)) for v in vec]
full=(1<<125)-1
masks={}
for j in range(3):
 for k in range(1,5):
  lo=sum(1<<i for i in range(125) if vec[i][j]<5-k)
  masks[j,k]=(lo,full^lo,k*5**j,(5-k)*5**j)

def shift(bits,g):
 for j,k in enumerate(vec[g]):
  if k:
   lo,hi,s,t=masks[j,k];bits=((bits&lo)<<s)|((bits&hi)>>t)
 return bits

base=[1,1,5,5,25,25];basis={1,5,25}
reachable=1
for g in base:reachable |= shift(reachable,g)
pool=[g for g in range(1,125) if g not in basis and not (reachable>>neg[g])&1]
perms=list(permutations(range(3)))
canonical=lambda g:min(sum(vec[g][p[j]]*5**j for j in range(3)) for p in perms)
roots=[g for g in pool if canonical(g)==g]
start=time.monotonic();nodes=0;leaves=0;hist=Counter();bad=[];completed=[];depths=Counter();profiles=[]

class Stop(Exception):pass

def profile(seq):
 d=[99]*125;d[0]=0
 for g in seq:
  old=d[:]
  for h in range(125):
   at=sum(((vec[h][j]-vec[g][j])%5)*5**j for j in range(3))
   d[h]=min(old[h],old[at]+1)
 sig=sum((sum(vec[g][j] for g in seq)%5)*5**j for j in range(3))
 assert max(d)==12 and d[sig]==12
 return max(v for h,v in enumerate(d) if h!=sig),sig,d

def dfs(seq,bits,candidates,last_count=1):
 global nodes,leaves
 nodes+=1;depths[len(seq)]+=1
 if nodes%2048==0 and time.monotonic()-start>50:raise Stop()
 if len(seq)==12:
  leaves+=1
  assert bits==full
  # Distances by simultaneous length-bitset layers, allowing previous layers only.
  layers=[1]+[0]*12
  for i,g in enumerate(seq):
   for k in range(i+1,0,-1):layers[k] |= shift(layers[k-1],g)
  sig=sum((sum(vec[g][j] for g in seq)%5)*5**j for j in range(3))
  seen=0;mx=0;dist=[99]*125
  for k,layer in enumerate(layers):
   new=layer&~seen&full;seen|=layer
   if new&~(1<<sig):mx=k
   while new:
    bit=new&-new;dist[bit.bit_length()-1]=k;new-=bit
  hist[mx]+=1
  profiles.append({'sequence':seq,'sigma':sig,'max_except_total':mx,'E9':sum(v>=9 for v in dist),'E10':sum(v>=10 for v in dist),'distances':dist})
  if mx>8:bad.append({'sequence':seq,'max_except_total':mx,'sigma':sig})
  return
 for ix,g in enumerate(candidates):
  if (bits>>neg[g])&1:continue
  count=(last_count+1 if g==seq[-1] else 1)
  if count>2:continue
  more=bits|shift(bits,g)
  child=[x for x in candidates[ix:] if not (more>>neg[x])&1 and (x!=g or count<2)]
  dfs(seq+[g],more,child,count)

status='COMPLETE'
try:
 for g in roots:
  more=reachable|shift(reachable,g)
  candidates=[x for x in pool if x>=g and not (more>>neg[x])&1]
  before=nodes;dfs(base+[g],more,candidates)
  completed.append({'root':g,'nodes':nodes-before})
except Stop:status='INCOMPLETE_TIMEOUT'
out={'scope':'H12 height<=2 containing three independent doubled values; normalize those values and first new value under S3 only','status':status,'initial_pool':len(pool),'roots':roots,'completed_roots':completed,'nodes':nodes,'leaves':leaves,'depth_counts':dict(depths),'max_distance_except_total_histogram':dict(hist),'counterexamples_to_L8':bad,'seconds':time.monotonic()-start}
(root/'evidence/root_continue_h12_height2.json').write_text(json.dumps(out,indent=2),encoding='utf8')
(root/'evidence/root_continue_h12_height2_profiles.jsonl').write_text('\n'.join(json.dumps(r) for r in profiles)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k!='counterexamples_to_L8'}));print('counterexamples',len(bad))
print('E10 hist',dict(Counter(r['E10'] for r in profiles)),'E9 hist',dict(Counter(r['E9'] for r in profiles)))
