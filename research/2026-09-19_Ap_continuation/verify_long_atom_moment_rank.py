"""Exact independent expansion of all low-degree monomial moments."""
from fractions import Fraction as F
from pathlib import Path
import json


def rref(rows, width):
    rows=[[F(x) for x in r] for r in rows]
    pivot=0
    for j in range(width):
        k=next((k for k in range(pivot,len(rows)) if rows[k][j]),None)
        if k is None:continue
        rows[pivot],rows[k]=rows[k],rows[pivot]
        d=rows[pivot][j];rows[pivot]=[x/d for x in rows[pivot]]
        for k in range(len(rows)):
            if k!=pivot and rows[k][j]:
                t=rows[k][j];rows[k]=[x-t*y for x,y in zip(rows[k],rows[pivot])]
        pivot+=1
    return rows,pivot


def main():
    # Each tuple is (short length, actual coefficient, signed parity).
    types=[(2,1,1),(3,1,-1),(4,2,1),(4,3,1),(5,3,-1)]
    rows=[]
    for degree in range(4):
        for a in range(degree+1):
            b=degree-a
            row=[s*(c**a*m**b+(-c)**a*(1-m)**b) for m,c,s in types]
            constant=(0**a*0**b)+(0**a*1**b)
            rows.append(row+[-constant])
    reduced,rank=rref(rows,5)
    assert rank==4
    expected=[[-1,-1], [F(1,3),F(7,3)], [F(1,3),F(16,3)], [0,1], [0,3]]
    for row in rows:
        assert sum(F(row[i])*expected[i][0] for i in range(5))==row[-1]
        assert sum(F(row[i])*expected[i][1] for i in range(5))==0
    # Marked moment expansion after one deletion: short subsets avoiding i
    # and complementary subsets containing i contribute separately.
    marked=[]
    for degree in range(3):
        for a in range(degree+1):
            b=degree-a
            coeff=[s*((-c)**a*(1-m)**b-c**a*m**b) for m,c,s in types]
            total0=F(0**a*0**b)
            total1=F(0)
            for i,(m,c,s) in enumerate(types):
                total0+=s*c**a*m**b*expected[i][0]
                total1+=s*c**a*m**b*expected[i][1]
            marked.append(coeff+[-total0,-total1])
    _,marked_rank=rref(marked,5)
    assert marked_rank==2
    targets=[[1,-1,2,3,-3,F(-1,3),F(2,3)],
             [3,-5,7,7,-9,F(-5,3),F(4,3)]]
    assert rref(marked+targets,7)[1]==2
    report={"status":"PASS","global_monomials_checked":len(rows),"global_constraint_rank":rank,
            "marked_monomials_checked":len(marked),"marked_constraint_rank":marked_rank,
            "count_parameterization_as_constant_and_D_coefficients":[[str(x) for x in row] for row in expected],
            "scope":"Exact rational monomial expansion and row rank; verifies the moment interface, not realizability or exclusion of x0=0."}
    Path(__file__).with_name("long_atom_moment_verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":main()
