"""Complete scalar obstruction probe for H10's quadratic signed-sum polynomial."""
from itertools import combinations
from pathlib import Path
from collections import Counter
import json

def consistency(rows,n):
 piv={}
 for row in rows:
  row=[v%5 for v in row]
  while True:
   c=next((i for i,x in enumerate(row[:n]) if x),None)
   if c is None:
    if row[-1]:return False,len(piv)
    break
   if c in piv:
    fac=row[c];row=[(x-fac*y)%5 for x,y in zip(row,piv[c])]
   else:
    inv=pow(row[c],-1,5);piv[c]=[x*inv%5 for x in row];break
 return True,len(piv)

rows=[];n=10;mon=[(i,) for i in range(n)]+list(combinations(range(n),2))
for a in range(n+1):
 for b in range(n+1-a):
  for c in range(n+1-a-b):
   counts=(a,b,c,n-a-b-c);q=[j for j,m in enumerate(counts,1) for _ in range(m)]
   eq=[]
   for k in range(2,5):
    for sub in combinations(range(n),k):
     if sum(q[i] for i in sub)%5==0:
      I=set(sub);eq.append([int(all(i in I for i in m)) for m in mon]+[4])
   yes,r=consistency(eq,len(mon));rows.append({'counts':counts,'consistent':yes,'rank':r,'equations':len(eq),'max_count':max(counts)})
out={'status':'LINEAR_RELAXATION_ONLY','variables':len(mon),'patterns':len(rows),'histogram':dict(Counter((str(r['consistent'])+':'+str(r['max_count'])) for r in rows)),'remaining_with_max7':[r for r in rows if r['consistent'] and r['max_count']<=7],'rows':rows}
p=Path(__file__).resolve().parents[1]/'evidence/root_continue_h10_polynomial.json';p.write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
