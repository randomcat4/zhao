"""Exact algebra checks for the split-fiber and star counting interfaces.

This verifies the scalar elimination, not the combinatorial classification.
All arithmetic is rational; no finite-prime search is used as a proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def main():
    # Linear expressions are (coefficient of c, coefficient of d, constant).
    models = {
        "low_value_repeated": {
            "P": (F(1,2), -1, 0), "Q": (F(-1,2), 1, 0),
            "e": (F(7,6), 0, F(1,3)),
        },
        "high_value_repeated": {
            "P": (-1, 2, 0), "Q": (1, -2, 0),
            "e": (0, F(7,3), F(1,3)),
        },
    }
    def dot(v,c,d): return v[0]*c+v[1]*d+v[2]
    checked=0
    # An affine identity is determined by its values at these three points.
    for name,m in models.items():
        for c,d in [(0,0),(1,0),(0,1)]:
            P,Q,e=[dot(m[k],c,d) for k in ["P","Q","e"]]
            if name=="low_value_repeated":
                C_r,D_r=P+Q+c,P+d
                C_s,D_s=c,2*P+Q+d
            else:
                C_r,D_r=2*P+Q+c,d
                C_s,D_s=P+c,P+Q+d
            assert C_r==2*D_r and C_s==2*D_s
            assert 7*D_r-3*e==-1 and 7*D_s-3*e==-1
            checked+=4
    # All possible positive adjacent-value multiplicities after exclusion.
    pairs=[(1,1),(1,2),(2,1)]
    assert all(c-2*d not in [1,7] for c,d in pairs)
    assert max(abs(c-2*d-k) for c,d in pairs for k in [1,7])<149
    # For p >=149 prime, p=1 or 5 mod6. Check universal affine representatives
    # of 1/3, 3/2 and 8/3, and their lower bound (p+1)/3.
    reps={
        "1/3": {1:(F(2,3),F(1,3)),5:(F(1,3),F(1,3))},
        "3/2": {1:(F(1,2),F(3,2)),5:(F(1,2),F(3,2))},
        "8/3": {1:(F(1,3),F(8,3)),5:(F(2,3),F(8,3))},
    }
    for target,rs in reps.items():
        val=F(target)
        for residue,(a,b) in rs.items():
            assert b==val
            assert (a*6).denominator==1
            assert (a*residue+b).denominator==1
            assert (a-F(1,3))*149+b-F(1,3)>=0 and a>=F(1,3)
            assert a*149+b>0 and (1-a)*149-b>0 and a<1
    # At a three-leaf center, B_Y=-2,C_Y=-5-c,D_Y=-1-d,E_Y=-3-e.
    for c,d,e in [(F(1),F(0),F(1)),(F(0),F(-1,2),F(-1,6))]:
        assert -5-c==2*(-2)+2*(-1-d)
        assert -(-2)+2*(-5-c)+3*(-1-d)-3*(-3-e)==-1
    # Split-fiber final count: low repeated gives c0-2*d0=0 identically;
    # high repeated gives q=-1/3 and e0=-5/9, incompatible with e0=0 or 1.
    assert 2-2*1==0
    q=F(-1,3)
    assert q-2*(2*q)==1
    e0=(1+2*q+3*(2*q))/3
    assert e0==F(-5,9)
    assert [9*k+5 for k in [0,1]]==[5,14]
    report={"status":"PASS","exact_position_identities_checked":checked,
            "models":{k:{q:[str(x) for x in v] for q,v in m.items()} for k,m in models.items()},
            "three_leaf_noncenter_CD_cases":["(1,0)","(0,(p-1)/2)"],
            "split_fiber_final_obstructions":["0=1","p divides 5 or 14"],
            "scope":"Exact rational scalar interfaces only; hand proofs supply graph and subset arguments; x0=0 remains open."}
    Path(__file__).with_name("x0_fiber_algebra_verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":main()
