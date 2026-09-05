"""Necessary-condition LP; never interpret feasibility as a group sequence."""
from pathlib import Path
import sys, json, math, itertools
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'local_deps'))
import numpy as np
from scipy.optimize import linprog
from projection_lp import cyclic_counts, canon

def run(N,m):
    hs=[]; seen=set(); counts=[]
    for a in range(13):
      for b in range(N-a+1):
       for c in range(N-a-b+1):
        for d in range(N-a-b-c+1):
          h=canon((a,b,c,d,N-a-b-c-d))
          if h in seen: continue
          seen.add(h);hs.append(h);counts.append(cyclic_counts(h))
    H=len(hs); allowed=list(range(m+1,18)); dim=H+len(allowed)+1
    idx={j:H+i for i,j in enumerate(allowed)}; li=dim-1
    rows=[];rhs=[]
    def eq(row,value):
        scale=max(1.,abs(value),max(abs(x) for x in row))
        rows.append(np.array(row)/scale);rhs.append(value/scale)
    for j in range(N+1):
        row=[float(cs[j]) for cs in counts]+[(-125. if j==q else 0.) for q in allowed]+[0.]
        eq(row,31*math.comb(N,j)+(125 if j==0 else 0))
    row=[math.comb(h[0],2) for h in hs]+[0.]*len(allowed)+[-25.]
    eq(row,6*math.comb(N,2))
    # If at most 3 triple values and every line has <=3 positions,
    # with 3 positions only if equal, collinear position pairs obey this bound.
    maxL=max(3*a+(N-3*a)//2 for a in range(4))
    bounds=[(0,None)]*H+[(126 if N==20 and q==15 else (6 if q==15 else 0),None) for q in allowed]+[(0,maxL)]
    ub=[];ubv=[]
    def le(coeff,value):
        row=np.zeros(dim)
        for j,c in coeff.items(): row[idx[j]]=c
        ub.append(row);ubv.append(value)
    if N==20:
        le({15:-10,16:4,17:-1},-1140)
        le({15:-10,17:3},-1140)
    else:
        le({14:-7,15:-4},-294)
    res=linprog(np.zeros(dim),A_eq=np.array(rows),b_eq=np.array(rhs),A_ub=np.array(ub),b_ub=np.array(ubv),bounds=bounds,method='highs')
    out={'N':N,'m':m,'status':res.status,'message':res.message,'max_collinear_pairs':maxL,
         'scope':'Continuous projection-histogram relaxation with integer-derived cuts and conditional at-most-three-triples restriction; not actual-sequence feasibility.'}
    if res.success:
        out['zero_counts']={str(j):float(res.x[i]) for j,i in idx.items()}
        out['collinear_pairs']=float(res.x[li])
        out['histograms']=[{'h':h,'x':float(res.x[i])} for i,h in enumerate(hs) if res.x[i]>1e-8]
        out['max_scaled_residual']=float(np.max(np.abs(np.array(rows)@res.x-np.array(rhs))))
    (ROOT/'evidence'/f'projection_integer_cuts_{N}.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='histograms'}),flush=True)

if __name__=='__main__':
    run(20,14);run(21,13)
