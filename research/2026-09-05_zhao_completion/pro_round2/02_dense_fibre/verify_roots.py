"""Independent orbit coverage and rank-three enumeration, Python integers only.
No compiled search code is imported. Translation of the subset-sum bitset uses
coordinate rotations rather than the generator's element-by-element update.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError("Run without -O; assertions are part of this checker.")
from pathlib import Path
from itertools import permutations
from collections import Counter
import json,time

BASE=(25,5,1);E=frozenset(BASE);ALL=(1<<125)-1
V=[(x//25,x//5%5,x%5) for x in range(125)]
def enc(v):return 25*v[0]+5*v[1]+v[2]
def add(x,y):return enc(tuple((a+b)%5 for a,b in zip(V[x],V[y])))
def scale(x,c):return enc(tuple(c*a%5 for a in V[x]))
NEG=[scale(x,4) for x in range(125)]
PROP=[sum(1<<scale(x,c) for c in range(1,5)) if x else 1 for x in range(125)]
BAD=[[0]*125 for _ in range(125)]
for x in range(1,125):
 for y in range(1,125):
  vals={scale(add(x,y),2),scale(add(x,y),3),add(scale(x,2),NEG[y]),add(scale(x,3),NEG[y]),add(scale(y,2),NEG[x]),add(scale(y,3),NEG[x])}
  BAD[x][y]=sum(1<<z for z in vals)
ROT=[]
for x in range(125):
 ops=[]
 for axis,stride in ((0,25),(1,5),(2,1)):
  k=V[x][axis]
  if k:
   mask=sum(1<<g for g in range(125) if V[g][axis]+k<5)
   ops.append((mask,ALL^mask,k*stride,(5-k)*stride))
 ROT.append(ops)
def shift(bits,x):
 for m,n,a,b in ROT[x]:bits=((bits&m)<<a)|((bits&n)>>b)
 return bits
for x in range(125):
 for y in range(125):assert shift(1<<y,x)==1<<add(x,y)

def inverse_columns(basis):
    a,b,c=(V[x] for x in basis)
    cross=lambda x,y:((x[1]*y[2]-x[2]*y[1])%5,(x[2]*y[0]-x[0]*y[2])%5,(x[0]*y[1]-x[1]*y[0])%5)
    bc=cross(b,c);det=sum(x*y for x,y in zip(a,bc))%5
    if not det:return None
    f=pow(det,-1,5)
    return tuple(tuple(f*x%5 for x in row) for row in (bc,cross(c,a),cross(a,b)))
def image(root,inv):
    return tuple(sorted(enc(tuple(sum(u*v for u,v in zip(row,V[g]))%5 for row in inv)) for g in root))

def validate(rootdir):
    roots=[]
    for line in (rootdir/'rank3_roots.txt').read_text().splitlines():
      a=tuple(map(int,line.split()));assert a[0]==len(a)-1 and a[0] in (7,8,9)
      root=a[1:];assert tuple(sorted(set(root)))==root and all(0<x<125 for x in root)
      roots.append(root)
    assert len(roots)==len(set(roots))==1786
    lookup={};orbit_sizes=Counter();root_counts=Counter()
    for idx,root in enumerate(roots):
      images=set()
      for basis in permutations(root,3):
       inv=inverse_columns(basis)
       if inv is None:continue
       assert image(basis,inv)==tuple(sorted(BASE))
       im=image(root,inv);assert E.issubset(im);images.add(im)
      assert images
      root_counts[len(root)]+=1;orbit_sizes[len(root)]+=len(images)
      for im in images:
       assert im not in lookup,('duplicate orbit',idx,lookup.get(im));lookup[im]=idx
    assert root_counts=={7:1084,8:659,9:43}
    assert orbit_sizes=={7:195462,8:193464,9:17490}
    counts=Counter();seen_roots=Counter();max_len=0
    negsums=1
    for g in BASE:negsums|=shift(negsums,NEG[g])
    forbidden=negsums
    for g in BASE:forbidden|=PROP[g]
    for x,y in permutations(BASE,2):forbidden|=BAD[x][y]
    candidates=ALL&~forbidden
    def rec(S,ns,cand):
      nonlocal max_len
      n=len(S);counts[n]+=1;max_len=max(max_len,n)
      assert n<=12
      if n>=7:
       key=tuple(sorted(S));assert key in lookup,('uncovered normalized set',key)
       seen_roots[lookup.pop(key)]+=1
      while cand:
       bit=cand&-cand;cand^=bit;v=bit.bit_length()-1
       new_ns=ns|shift(ns,NEG[v]);bad=PROP[v]|new_ns
       for x in S:bad|=BAD[x][v]
       rec(S+(v,),new_ns,cand&~bad)
    rec(BASE,negsums,candidates)
    assert max_len==9 and not lookup and len(seen_roots)==1786
    assert counts=={3:1,4:90,5:3000,6:41247,7:195462,8:193464,9:17490}
    return {'rank3_nodes':sum(counts.values()),'counts_by_size':dict(counts),'maximum':max_len,'orbit_counts':dict(root_counts),'normalized_counts':dict(orbit_sizes),'normalized_denominator':sum(orbit_sizes.values()),'normalized_processed':sum(orbit_sizes.values()),'roots_processed':len(seen_roots),'uncovered':len(lookup),'translation_unit_tests':125*125,'exit':'NORMAL'}
if __name__=='__main__':
    t=time.monotonic();out=validate(Path(__file__).resolve().parent);out['seconds']=time.monotonic()-t
    print(json.dumps(out,indent=2))
