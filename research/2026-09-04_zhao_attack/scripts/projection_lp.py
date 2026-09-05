from pathlib import Path
import sys, json, math, itertools, time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'local_deps'))
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

def cyclic_counts(h):
    n=sum(h); dp=[[0]*5 for _ in range(n+1)]; dp[0][0]=1; seen=0
    for a,num in enumerate(h):
        for _ in range(num):
            seen+=1
            for j in range(seen,0,-1):
                old=dp[j-1]
                for s in range(5): dp[j][(s+a)%5]+=old[s]
    return [v[0] for v in dp]

def canon(h):
    return min(tuple(h[(pow(t,-1,5)*a)%5] for a in range(5)) for t in range(1,5))

def run(N,m):
    hs=[]; seen=set(); counts=[]
    for a in range(13):
      for b in range(N-a+1):
       for c in range(N-a-b+1):
        for d in range(N-a-b-c+1):
          h=(a,b,c,d,N-a-b-c-d)
          k=canon(h)
          if k in seen: continue
          seen.add(k); hs.append(k); counts.append(cyclic_counts(k))
    H=len(hs); allowed=list(range(m+1,18)); rows=[]; rhs=[]
    # Sum over 156 projective classes B_phi = 125 B_S + 31(1+z)^N.
    for j in range(N+1):
      row=[float(cs[j]) for cs in counts]+[(-125. if j==q else 0.) for q in allowed]
      target=31*math.comb(N,j)+(125 if j==0 else 0)
      scale=max(1.,abs(target),max(abs(x) for x in row))
      rows.append([x/scale for x in row]); rhs.append(target/scale)
    bounds=[(0,None)]*H+[(6 if q==15 else 0,None) for q in allowed]
    res=linprog(np.zeros(H+len(allowed)),A_eq=np.array(rows),b_eq=np.array(rhs),bounds=bounds,method='highs')
    out={'N':N,'m':m,'histogram_types':H,'status':int(res.status),'message':res.message,
         'interpretation':'Numerical necessary-constraint probe only; neither a proof nor an actual sequence.'}
    if res.success:
       out['zero_counts']={str(q):float(res.x[H+i]) for i,q in enumerate(allowed)}
       out['nonzero_histograms']=[{'histogram':h,'value':float(res.x[i])} for i,h in enumerate(hs) if res.x[i]>1e-7]
       out['max_scaled_residual']=float(np.max(np.abs(np.array(rows)@res.x-np.array(rhs))))
       out['linear_extrema']={}
       objectives={str(q):[1 if t==q else 0 for t in allowed] for q in allowed}
       objectives['alternating']=[(-1)**q for q in allowed]
       for name,coeffs in objectives.items():
         objective=np.array([0.]*H+coeffs)
         vals=[]
         for sign in (1,-1):
           rr=linprog(sign*objective,A_eq=np.array(rows),b_eq=np.array(rhs),bounds=bounds,method='highs')
           vals.append(float(objective@rr.x) if rr.success else rr.message)
         out['linear_extrema'][name]=vals
    (ROOT/'evidence').mkdir(exist_ok=True)
    (ROOT/'evidence'/f'projection_lp_{N}.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='nonzero_histograms'}),flush=True)

if __name__=='__main__':
    run(20,14);run(21,13)
