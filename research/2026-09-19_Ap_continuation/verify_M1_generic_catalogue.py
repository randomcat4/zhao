"""Independent all-prime coverage audit for the final M1 generic catalogue.

No imports from either generator. Integer determinants certify rational/mod-p
equivalence for every p>=149. Capacity and component completion are separate.
"""
from itertools import combinations, permutations
from fractions import Fraction as F
from pathlib import Path
import gzip
import json
import time


def main():
    root=Path(__file__).parent
    records=json.loads(gzip.decompress((root/"M1_generic_survivors.json.gz").read_bytes()))
    indexed={}
    for r in records:
        key=(r["n"],tuple(sorted(r["positions"].items())),r["loop"])
        assert key not in indexed
        indexed[key]=r
    seen=set()
    count=badcount=maxbad=maxdet=0
    families={}
    start=time.monotonic()
    for k in range(6):
        for extra in combinations(["u","t","v","z","h"],k):
            names=("x",)+extra
            local=0
            for n in range(len(names),18):
                for places in permutations(range(n),len(names)):
                    pos=dict(zip(names,places))
                    for loop in [False,True]:
                        targets=[[0,1] for _ in range(n)]
                        for name,i in pos.items():
                            targets[i]={"x":[0,7],"u":[-1,-1],"t":[1,2],
                                        "v":[0,-1],"z":[0,-1],"h":[0,-1]}[name]
                        targets[0][1]+=2*loop
                        before=(0,0,0)
                        current=(1,0,0)
                        forms=[]
                        for i in range(n):
                            forms.append(current)
                            nextrow=(-before[0],targets[i][0]-before[1],targets[i][1]-before[2])
                            if i==0 and loop:
                                nextrow=tuple(a-b for a,b in zip(nextrow,current))
                            before,current=current,nextrow
                        eq=[current]
                        for name,i in pos.items():
                            rv,rc={"x":(0,2),"u":(0,2),"t":(0,2),"v":(0,-3),
                                   "z":(1,0),"h":(-1,-3)}[name]
                            a,b,c=forms[i]
                            eq.append((a,b-rv,c-rc))
                        count+=1
                        local+=1
                        key=(n,tuple(sorted(pos.items())),loop)
                        constants=[abs(c) for a,b,c in eq if not a and not b and c]
                        contradiction=min(constants) if constants else 0
                        pivot=next((r for r in eq if r[0] or r[1]),None)
                        unique=None
                        if pivot and not contradiction:
                            a,b,c=pivot
                            assert max(abs(a),abs(b))<149
                            other=next((r for r in eq if a*r[1]-b*r[0]),None)
                            if other:
                                d,e,f=other
                                determinant=a*e-b*d
                                assert 0<abs(determinant)<149
                                maxdet=max(maxdet,abs(determinant))
                                nt,nv=b*f-c*e,c*d-a*f
                                residuals=[abs(aa*nt+bb*nv+cc*determinant) for aa,bb,cc in eq
                                           if aa*nt+bb*nv+cc*determinant]
                                if residuals:contradiction=min(residuals)
                                else:unique=(F(nv,determinant),F(nt,determinant))
                            else:
                                residuals=[abs(a*cc-aa*c) if a else abs(b*cc-bb*c) for aa,bb,cc in eq]
                                nonzero=[r for r in residuals if r]
                                if nonzero:contradiction=min(nonzero)
                        if contradiction:
                            assert contradiction<149
                            maxbad=max(maxbad,contradiction)
                            assert key not in indexed
                            badcount+=1
                            continue
                        assert pivot is not None and key in indexed
                        saved=indexed[key]
                        assert saved["multiplicity_forms"]==[list(r) for r in forms]
                        if unique is not None:
                            assert tuple(map(F,saved["parameters"]))==unique
                        else:
                            par=saved["parameters"]
                            assert par[0]=="V_free"
                            A,B,C=par[1:]
                            assert 0<abs(A)<149
                            assert all(-aa*B+bb*A==0 and -aa*C+cc*A==0 for aa,bb,cc in eq)
                        seen.add(key)
            families["".join(names)]=local
            print("".join(names),local,"verified",flush=True)
    assert seen==set(indexed)
    report={"status":"PASS","path_arrangements":count,"bounded_integer_contradictions":badcount,
            "surviving_parameter_cases":len(seen),"maximum_contradiction_integer":maxbad,
            "maximum_pivot_determinant":maxdet,"family_counts":families,
            "scope":"Independent complete enumeration using integer recurrences and small determinant certificates for every p>=149; does not alone prove capacity/completion exclusion."}
    (root/"M1_generic_catalogue_verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    print("elapsed_seconds",time.monotonic()-start)


if __name__=="__main__":main()
