"""Complete C5 occupancy linear certificates for a candidate dense-H12 lemma."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json

root=Path(__file__).resolve().parents[1]

def solve(rows,n):
    a=[r[:] for r in rows]; piv=[]; rr=0
    for c in range(n):
        at=next((i for i in range(rr,len(a)) if a[i][c]%5),None)
        if at is None: continue
        a[rr],a[at]=a[at],a[rr]; inv=pow(a[rr][c]%5,-1,5)
        a[rr]=[(v*inv)%5 for v in a[rr]]
        for i in range(len(a)):
            if i!=rr:
                fac=a[i][c]%5
                if fac: a[i]=[(a[i][j]-fac*a[rr][j])%5 for j in range(n+1)]
        piv.append(c); rr+=1
    if any(not any(row[:n]) and row[n]%5 for row in a): return None
    particular=[0]*n
    for i,c in enumerate(piv): particular[c]=a[i][n]
    bases=[]
    for c in range(n):
        if c in piv: continue
        b=[0]*n; b[c]=1
        for i,cc in enumerate(piv): b[cc]=-a[i][c]%5
        bases.append(b)
    return particular,bases

out=[]
for length in [8,9]:
  for bound in [4,5,6]:
    rows=[]
    for a in range(length+1):
      for b in range(length+1-a):
        for c in range(length+1-a-b):
          counts=(a,b,c,length-a-b-c)
          q=[v for v,m in enumerate(counts,1) for _ in range(m)]
          eq=[]
          for k in range(2,bound+1):
            for sub in combinations(range(length),k):
              if sum(q[i] for i in sub)%5==0:
                eq.append([int(i in sub) for i in range(length)]+[1])
          sol=solve(eq,length)
          if sol is None: result={'status':'inconsistent'}
          else:
            # Forced equalities must hold coordinatewise, including the homogeneous
            # coordinates where t=0; affine and all free-coordinate rows are kept.
            p,bs=sol
            groups={}
            for i in range(length):
              key=(q[i],p[i],tuple(v[i] for v in bs));groups.setdefault(key,[]).append(i)
            result={'status':'forces_height4' if max(map(len,groups.values()))>=4 else 'remaining','dimension':len(bs),'max_forced_multiplicity':max(map(len,groups.values())),'groups':list(groups.values()),'particular':p,'basis':bs}
          rows.append({'counts':counts,'equations':len(eq),**result})
    out.append({'length':length,'bound':bound,'histogram':dict(Counter(r['status'] for r in rows)),'patterns':len(rows),'rows':rows})
(root/'evidence/root_continue_quotient.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in item.items() if k!='rows'} for item in out]))
