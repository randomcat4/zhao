"""Integer histogram relaxation for B; a feasible solution is not a sequence."""
from pathlib import Path
import sys,json,math,itertools,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'local_deps'))
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_matrix
from projection_lp import cyclic_counts,canon

N=20;hs=[];seen=set();cs=[]
for a in range(13):
 for b in range(N-a+1):
  for c in range(N-a-b+1):
   for d in range(N-a-b-c+1):
    h=canon((a,b,c,d,N-a-b-c-d))
    if h in seen:continue
    seen.add(h);hs.append(h);cs.append(cyclic_counts(h))
H=len(hs)
# x histograms, Z15=1+5q15, Z16=5q16, Z17=5q17, collinear L,
# collinear count with total sum M, modulus-25 auxiliary t.
dim=H+6;qi={15:H,16:H+1,17:H+2};Li=H+3;Mi=H+4;ti=H+5
rows=[];los=[];his=[]
def row(coeffs,lo,hi=None):
    r=np.zeros(dim,dtype=np.int64)
    for i,v in coeffs.items():r[i]=v
    rows.append(r);los.append(lo);his.append(lo if hi is None else hi)
for j in range(N+1):
    coeff={i:c[j] for i,c in enumerate(cs)}
    if j in qi:coeff[qi[j]]=-625
    rhs=31*math.comb(N,j)+(125 if j in(0,15) else 0)
    row(coeff,rhs)
row({**{i:math.comb(h[0],2) for i,h in enumerate(hs)},Li:-25},6*math.comb(N,2))
row({**{i:h[0] for i,h in enumerate(hs) if sum(a*h[a] for a in range(5))%5==0},Mi:-25},6*N)
row({qi[15]:50,qi[16]:-20,qi[17]:5},1130,np.inf)
row({qi[15]:50,qi[17]:-15},1130,np.inf)
prod=[]
for h in hs:
    v=0 if h[0] else math.prod(pow(a,h[a],5) for a in range(1,5))%5
    prod.append(v)
# 1-Z15+Z16-Z17 - 5 sum x_h prod_h = 25t.
row({**{i:-p for i,p in enumerate(prod)},qi[15]:-1,qi[16]:1,qi[17]:-1,ti:-5},0)
lb=np.zeros(dim);ub=np.full(dim,np.inf);ub[:H]=156
lb[qi[15]]=25;ub[Li]=14;ub[Mi]=3;lb[ti]=-1e6;ub[ti]=1e6
t0=time.time()
ans=milp(np.zeros(dim),integrality=np.ones(dim),bounds=Bounds(lb,ub),
 constraints=LinearConstraint(csc_matrix(np.array(rows,dtype=float)),np.array(los),np.array(his)),
 options={'time_limit':45.,'mip_rel_gap':0.})
out={'status':int(ans.status),'message':ans.message,'seconds':time.time()-t0,
 'scope':'Integer projection-histogram relaxation only. At-most-three-triples and B counting lemmas are assumptions. Not actual-sequence feasibility.'}
if ans.x is not None:
    v=np.rint(ans.x).astype(np.int64);val=np.array(rows,dtype=np.int64)@v
    good=bool(np.all(val>=np.array(los)) and np.all(val<=np.array(his)) and np.all(v>=lb) and np.all(v<=ub))
    out['exact_integer_rows_pass']=good;out['zero_counts']={str(j):int(5*v[i]+(j==15)) for j,i in qi.items()}
    out['auxiliary']={'L':int(v[Li]),'M':int(v[Mi]),'t':int(v[ti])}
    out['histograms']=[{'h':h,'count':int(v[i])} for i,h in enumerate(hs) if v[i]]
(ROOT/'evidence'/'projection_milp_B.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='histograms'}),flush=True)
