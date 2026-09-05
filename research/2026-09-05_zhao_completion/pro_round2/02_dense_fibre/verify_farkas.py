"""Independent exact validation. Standard library only; no optimizer or NumPy.
Expands every scalar label as a distinct position, and checks all 9,590 profiles.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError("Run without -O; assertions are part of this checker.")
from pathlib import Path
from math import comb
import json

def validate(root: Path) -> dict:
    c=json.loads((root/'farkas_certificate.json').read_text())
    a=c['multipliers']
    assert len(a)==24 and a[14:18]==[0,0,0,0]
    expected=[156]+[31*comb(21,k) for k in range(1,22)]+[31*comb(21,2),6*comb(21,2)]
    rhs=sum(x*y for x,y in zip(a,expected))
    assert rhs==c['right_hand_side'] and rhs<0
    minimum=None;processed=0;canonical=set();zero_profiles=[]
    for n0 in range(7):
      for n1 in range(22-n0):
       for n2 in range(22-n0-n1):
        for n3 in range(22-n0-n1-n2):
         n4=21-n0-n1-n2-n3;n=(n0,n1,n2,n3,n4)
         dp=[[0]*5 for _ in range(22)];dp[0][0]=1;length=0
         for value,repeats in enumerate(n):
          for _ in range(repeats):
           for k in range(length+1,0,-1):
            for residue in range(5):
             dp[k][(residue+value)%5]+=dp[k-1][residue]
           length+=1
         assert length==21 and all(sum(dp[k])==comb(21,k) for k in range(22))
         values=[1]+[dp[k][0] for k in range(1,22)]+[sum(comb(x,2) for x in n),comb(n0,2)]
         score=sum(x*y for x,y in zip(a,values));assert score>=0,(n,score)
         if score==0:zero_profiles.append(n)
         minimum=score if minimum is None else min(minimum,score)
         canonical.add(min(tuple(n[(u*j)%5] for j in range(5)) for u in (1,2,3,4)))
         processed+=1
    denominator=comb(25,4)-comb(18,4)
    assert processed==denominator==9590 and len(canonical)==c['profiles']==2406
    assert minimum==c['minimum_coefficient']==0
    return {'unquotiented_denominator':denominator,'processed':processed,'scalar_orbits':len(canonical),'minimum_score':minimum,'rhs':rhs,'zero_score_profiles':zero_profiles,'exit':'NORMAL'}

if __name__=='__main__':
    out=validate(Path(__file__).resolve().parent)
    print(json.dumps(out,indent=2))
