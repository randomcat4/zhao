"""Bounded exact H12 scan, exactly one/two tripled values, other heights<=2."""
from pathlib import Path
from itertools import permutations
from collections import Counter
import time,json

root=Path(__file__).resolve().parents[1]
vec=[(i%5,(i//5)%5,i//25) for i in range(125)]
neg=[sum((-x%5)*5**j for j,x in enumerate(v)) for v in vec]
full=(1<<125)-1;masks={}
for j in range(3):
 for k in range(1,5):
  lo=sum(1<<i for i in range(125) if vec[i][j]<5-k)
  masks[j,k]=(lo,full^lo,k*5**j,(5-k)*5**j)
def shift(bits,g):
 for j,k in enumerate(vec[g]):
  if k:
   lo,hi,s,t=masks[j,k];bits=((bits&lo)<<s)|((bits&hi)>>t)
 return bits
class Stop(Exception):pass

def run(a):
 basis=[1,5,25];base=[g for j,g in enumerate(basis) for _ in range(3 if j<a else 1)]
 bits=1
 for g in base:bits|=shift(bits,g)
 caps=[2 for _ in range(125)]
 for j,g in enumerate(basis):caps[g]=0 if j<a else 1
 pool=[g for g in range(1,125) if caps[g] and not (bits>>neg[g])&1]
 perms=[p for p in permutations(range(3)) if set(p[:a])==set(range(a))]
 canon=lambda g:min(sum(vec[g][p[j]]*5**j for j in range(3)) for p in perms)
 roots=[g for g in pool if canon(g)==g]
 start=time.monotonic();nodes=0;leaves=0;hist=Counter();depths=Counter();profiles=[];complete=[]
 def dfs(seq,reach,candidates,last_count=1):
  nonlocal nodes,leaves
  nodes+=1;depths[len(seq)]+=1
  if nodes%2048==0 and time.monotonic()-start>50:raise Stop()
  if len(seq)==12:
   leaves+=1;assert reach==full
   layers=[1]+[0]*12
   for i,g in enumerate(seq):
    for k in range(i+1,0,-1):layers[k]|=shift(layers[k-1],g)
   sig=sum((sum(vec[g][j] for g in seq)%5)*5**j for j in range(3))
   seen=0;dist=[99]*125
   for k,layer in enumerate(layers):
    new=layer&~seen&full;seen|=layer
    while new:
     low=new&-new;dist[low.bit_length()-1]=k;new-=low
   mx=max(v for h,v in enumerate(dist) if h!=sig);hist[mx]+=1
   profiles.append({'sequence':seq,'sigma':sig,'max_except_total':mx,'E9':sum(x>=9 for x in dist),'E10':sum(x>=10 for x in dist),'distances':dist})
   return
  for ix,g in enumerate(candidates):
   if (reach>>neg[g])&1:continue
   count=last_count+1 if g==seq[-1] else 1
   if count>caps[g]:continue
   nxt=reach|shift(reach,g)
   child=[x for x in candidates[ix:] if not (nxt>>neg[x])&1 and (x!=g or count<caps[g])]
   dfs(seq+[g],nxt,child,count)
 status='COMPLETE'
 try:
  for g in roots:
   nxt=bits|shift(bits,g)
   candidates=[x for x in pool if x>=g and not (nxt>>neg[x])&1 and (caps[g]>1 or x!=g)]
   before=nodes;dfs(base+[g],nxt,candidates);complete.append({'root':g,'nodes':nodes-before})
 except Stop:status='INCOMPLETE_TIMEOUT'
 out={'scope':f'H12 with exactly {a} triples, other heights<=2, basis containing all triples','status':status,'base':base,'initial_pool':len(pool),'roots':roots,'completed_roots':complete,'nodes':nodes,'leaves':leaves,'depth_counts':dict(depths),'max_distance_except_total_histogram':dict(hist),'E9_histogram':dict(Counter(r['E9'] for r in profiles)),'E10_histogram':dict(Counter(r['E10'] for r in profiles)),'seconds':time.monotonic()-start}
 (root/f'evidence/root_continue_h12_triples{a}.json').write_text(json.dumps(out,indent=2),encoding='utf8')
 (root/f'evidence/root_continue_h12_triples{a}_profiles.jsonl').write_text('\n'.join(json.dumps(r) for r in profiles)+'\n',encoding='utf8')
 print(json.dumps(out),flush=True)
for a in [2,1]:run(a)
