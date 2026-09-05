from itertools import combinations, product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def rref(rows,n):
 a=[r[:] for r in rows];pivs=[];rr=0
 for c in range(n):
  k=next((k for k in range(rr,len(a)) if a[k][c]%5),None)
  if k is None:continue
  a[rr],a[k]=a[k],a[rr];inv=pow(a[rr][c]%5,-1,5);a[rr]=[(v*inv)%5 for v in a[rr]]
  for k in range(len(a)):
   if k!=rr:
    fac=a[k][c];a[k]=[(a[k][j]-fac*a[rr][j])%5 for j in range(n+1)]
  pivs.append(c);rr+=1
 if any(not any(r[:n]) and r[n]%5 for r in a):return None
 p=[0]*n
 for i,c in enumerate(pivs):p[c]=a[i][n]
 bs=[]
 for c in range(n):
  if c in pivs:continue
  v=[0]*n;v[c]=1
  for i,cc in enumerate(pivs):v[cc]=-a[i][c]%5
  bs.append(v)
 return p,bs

def main():
 outcomes=[];survive=[]
 for a in range(10):
  for b in range(10-a):
   for c in range(10-a-b):
    counts=(a,b,c,9-a-b-c);q=sum(([i+1]*v for i,v in enumerate(counts)),[]);rows=[]
    for ell in range(2,5):
     for inds in combinations(range(9),ell):
      if sum(q[i] for i in inds)%5==0:
       rows.append([int(i in inds) for i in range(9)]+[1])
    # Affine shear sets the H-coordinate of the first outside point to zero.
    rows.append([1]+[0]*8+[0])
    sol=rref(rows,9)
    if sol is None:status='inconsistent'
    else:
     p,bs=sol;classes={}
     for i in range(9):
      key=(q[i],p[i],tuple(v[i] for v in bs));classes.setdefault(key,[]).append(i)
     maxclass=max(map(len,classes.values()))
     if maxclass>=4:status='forced_height4'
     else:
      status='remaining';survive.append({'counts':counts,'dimension':len(bs),'particular':p,'basis':bs,'equations':len(rows)})
    outcomes.append({'counts':counts,'status':status})
 out={'patterns':len(outcomes),'outcomes':outcomes,'remaining':survive}
 (ROOT/'evidence'/'rank3_projection_patterns.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 print(json.dumps({'patterns':len(outcomes),'remaining':survive},indent=2))
if __name__=='__main__':main()
