"""Exact affine verification of the conditional short-zero construction.

Does not certify the preceding reduction to the rank-one model.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def add(*vs): return tuple(sum(x) for x in zip(*vs))
def scale(k,v): return tuple(k*x for x in v)
def val(v,p): return v[0]*p+v[1]
def nonnegative(v): return v[0]>=0 and val(v,149)>=0


def main():
    p=(F(1),F(0)); zero=(F(0),F(0)); cases=[]
    for residue in [1,5,7,11]:
        j=3 if residue%4==1 else 1
        ell=(F(1,4),F(j,4))
        k=add(p,scale(-1,ell))
        for kappa in [2,3]:
            if kappa==2:
                mass=(F(2,3),F(1,3)) if residue%3==1 else (F(1,3),F(1,3))
            else:
                mass=(F(1,6),F(-1,6)) if residue%6==1 else (F(5,6),F(-1,6))
            anchor=add(p,scale(-kappa,ell))
            applicable=nonnegative(add(mass,scale(-1,ell)))
            assert applicable==(kappa==2 or residue%6==5)
            if not applicable:
                cases.append({'p_mod_12':residue,'tail_type':'D','status':'OPEN: tail mass insufficient'})
                continue
            # For p=12n+residue, all four counts are integers.
            for v in [ell,k,anchor,mass]:
                assert (12*v[0]).denominator==1 and val(v,residue).denominator==1
            assert nonnegative(k) and nonnegative(ell) and nonnegative(anchor)
            assert nonnegative(add((F(1),F(-5)),scale(-1,k)))
            assert nonnegative(add((F(1),F(-4)),scale(-1,anchor)))
            assert 0<=j<=3
            # Coordinates in the formal basis (a,b,z):
            # w=2b-z, u=kappa*a-2b-z.
            a_coef=add(scale(kappa,ell),anchor)
            b_coef=add(scale(2,k),scale(-2,ell),(F(0),F(j)))
            z_coef=scale(-1,add(k,ell))
            assert a_coef==p and b_coef==p and z_coef==scale(-1,p)
            length=add(k,ell,anchor,(F(0),F(j)))
            assert nonnegative(add((F(3),F(-2)),scale(-1,length)))
            cases.append({'p_mod_12':residue,'tail_type':'C' if kappa==2 else 'D','status':'PASS',
                          'counts_as_affine_p':{name:[str(x) for x in v] for name,v in [('w',k),('tail',ell),('anchors',anchor)]},'b_count':j})
    report={'status':'PASS','universal_residue_cases':cases,
            'scope':'Exact count bounds and actual zero-sum identity under the stated rank-one model assumptions; does not certify model completeness; D tail with p=1 mod6 remains open.'}
    Path(__file__).with_name('rank_one_short_zero_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
