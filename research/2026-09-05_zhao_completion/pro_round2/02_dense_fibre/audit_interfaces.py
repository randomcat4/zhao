"""Exact symbolic interfaces; does not search four-dimensional configurations."""
import sys
if sys.flags.optimize:
    raise RuntimeError("Run without -O; assertions are part of this checker.")
from itertools import product
from math import comb
from pathlib import Path
import json

def C(n,r):
    return comb(n,r) if 0 <= r <= n else 0

def expected(n):
    if n in (20,21): return {(0,1,0,0)}
    if n == 19: return {(t,(1+3*t)%5,3*t%5,t) for t in range(5)}
    if n == 18: return {((c+3*d)%5,(1+2*c+2*d)%5,c,d) for c in range(5) for d in range(5)}
    if n == 17: return {(a,(1+a+c-d)%5,c,d) for a,c,d in product(range(5),repeat=3)}
    raise ValueError(n)

report={};tested=0;matrices={}
for n in range(17,22):
    mat=[[C(n,r)]+[(-1)**k*C(n-k,r) for k in range(14,18)] for r in range(n-16)]
    matrices[n]=mat
    sol=set()
    for t in product(range(5),repeat=4):
        tested+=1
        if all((row[0]+sum(x*y for x,y in zip(row[1:],t)))%5==0 for row in mat):sol.add(t)
    assert sol==expected(n)
    report[n]={'residue_tuples':625,'solutions':len(sol),'integer_coefficient_rows':mat}
assert tested==5*625
assert {t for t in expected(19) if t[0]==0}=={(0,1,0,0)}
assert {t for t in expected(18) if t[0]==t[3]==0}=={(0,1,0,0)}
assert {t for t in expected(17) if t[0]==t[2]==t[3]==0}=={(0,1,0,0)}
assert comb(19,2)==171 and comb(4,2)==6 and comb(19,2)%comb(4,2)!=0
core=tuple(range(3));petals=[tuple(range(3+3*i,6+3*i)) for i in range(6)]
blocks=[set(core+p) for p in petals]
codegrees={}
for x in range(21):
 for y in range(x+1,21):
    l6=sum({x,y}<=b for b in blocks)
    possible=[t for t in range(5) if (1+3*t-l6)%5==0]
    assert len(possible)==1
    codegrees[x,y]=possible[0]
assert len(codegrees)==comb(21,2)
deg4=[]
for x in range(21):
    total=sum(v for xy,v in codegrees.items() if x in xy)
    assert total%3==0
    deg4.append(total//3)
assert deg4==[0]*3+[15]*18 and sum(deg4)==270 and sum(deg4)%4==2
quotient_cases=[]
for p in (0,1):
    h=(4*p+2)%5
    nonpair=[d for d in range(5) if d%5==h]
    pair=[d for d in range(5) if (d-1)%5==h]
    assert len(nonpair)==len(pair)==1
    degree_sum=(15-2*p)*nonpair[0]+2*p*pair[0]
    if p==0:
        assert degree_sum==30 and degree_sum//3==10
        assert 3*(nonpair[0]-1)!=degree_sum//3-1
    else: assert degree_sum==17 and degree_sum%3!=0
    quotient_cases.append({'pairs':p,'h':h,'ordinary_degree':nonpair[0],'pair_endpoint_degree':pair[0],'degree_sum':degree_sum})
D_subsets=sum(comb(21,d) for d in range(5))
D_equations=sum(comb(21,d)*(5-d) for d in range(5))
assert D_subsets==7547 and D_equations==9364
m_max=comb(21,7);m_values=list(range(20,m_max+1,5))
assert m_max==116280 and len(m_values)==23253
raw_by_h={h:comb(499,20-h)*r for h,r in ((7,1084),(8,659),(9,43))}
raw=sum(raw_by_h.values())
assert raw==17972093794219884182340301482 and raw.bit_length()==94
out={'residue_tuple_denominator':3125,'residue_tuples_processed':tested,'deletion_matrices':report,
     'position_deletion_sets':D_subsets,'position_deletion_equations':D_equations,
     'B_squarefree_design':{'pairs_through_point':171,'pairs_per_block':6,'remainder':3},
     'six_block_pair_types_processed':210,'forced_C4_degrees':deg4,'degree_sum':270,
     'quotient_fifteen_pair_cases':quotient_cases,'m_denominator':len(m_values),
     'm_min':m_values[0],'m_max':m_values[-1],
     'raw_extension_by_h':raw_by_h,'raw_extension_total':raw,'raw_extension_bits':94,
     'exit':'NORMAL'}
print(json.dumps(out,indent=2))
