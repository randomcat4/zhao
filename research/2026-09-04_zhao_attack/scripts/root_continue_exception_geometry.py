"""Classify affine/linear geometry of exact high-distance sets; no endpoint claim."""
from pathlib import Path
from collections import Counter
import json

root=Path(__file__).resolve().parents[1]
vec=[(i%5,(i//5)%5,i//25) for i in range(125)]
def rank(rows):
 a=[list(r) for r in rows];rr=0
 if not a:return 0
 for c in range(len(a[0])):
  ix=next((i for i in range(rr,len(a)) if a[i][c]%5),None)
  if ix is None:continue
  a[rr],a[ix]=a[ix],a[rr];s=pow(a[rr][c]%5,-1,5);a[rr]=[x*s%5 for x in a[rr]]
  for i in range(len(a)):
   if i!=rr:
    s=a[i][c];a[i]=[(x-s*y)%5 for x,y in zip(a[i],a[rr])]
  rr+=1
 return rr

out=[]
for a in [1,2]:
 path=root/f'evidence/root_continue_h12_triples{a}_profiles.jsonl'
 hist=Counter();remaining=[]
 for line in path.open(encoding='utf8'):
  r=json.loads(line);ex=[vec[i] for i,d in enumerate(r['distances']) if d>=9]
  lin=rank(ex);aff=rank([[(x-y)%5 for x,y in zip(v,ex[0])] for v in ex[1:]])
  # 0 is in affine hull iff linear rank equals affine dimension.
  if lin<=1:kind='linear_line'
  elif lin>aff:kind='affine_separated_from_zero'
  else:kind='remaining';remaining.append({'sequence':r['sequence'],'exception_vectors':ex,'linear_rank':lin,'affine_dimension':aff})
  hist[kind]+=1
 item={'triples':a,'histogram':dict(hist),'remaining':remaining}
 out.append(item)
 print(json.dumps({'triples':a,'histogram':dict(hist),'first_remaining':remaining[:2]}))
(root/'evidence/root_continue_exception_geometry.json').write_text(json.dumps(out,indent=2),encoding='utf8')
