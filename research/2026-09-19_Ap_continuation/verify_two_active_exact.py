"""Replay the complete certificate catalogue with exact rational arithmetic.

No LP solver is imported or called. The mathematical input model is shared
with the generator; this is independent arithmetic replay, not external review.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import gzip
import hashlib
import json
from star_exact_model import collision_cases, make_values, exact_system, reduce_vec, largest_prime_factor


def mod_basis(vectors,p):
    rows=[list(x%p for x in v) for v in vectors if any(x%p for x in v)]
    row=0
    for col in range(4):
        pivot=next((j for j in range(row,len(rows)) if rows[j][col]),None)
        if pivot is None:continue
        rows[row],rows[pivot]=rows[pivot],rows[row]
        mul=pow(rows[row][col],-1,p)
        rows[row]=[x*mul%p for x in rows[row]]
        for j in range(len(rows)):
            if j==row:continue
            mul=rows[j][col]
            rows[j]=[(x-mul*y)%p for x,y in zip(rows[j],rows[row])]
        row+=1
        if row==len(rows):break
    return tuple(tuple(v) for v in rows[:row])


def mod_reduce(v,basis,p):
    v=list(v)
    for row in basis:
        k=next(k for k,x in enumerate(row) if x)
        mul=v[k]
        v=[(x-mul*y)%p for x,y in zip(v,row)]
    return tuple(v)


def independent_mod_catalogue(values,p):
    diffs=set()
    for x,y in combinations(values.values(),2):
        d=tuple((a-b)%p for a,b in zip(x,y))
        diffs.add(mod_basis([d],p)[0])
    candidates={}
    for d in diffs:
        a=(-2*d[0]+2*d[1])%p
        b=(-d[0]-6*d[1]-d[2]-4*d[3])%p
        if a:
            candidates.setdefault(-b*pow(a,-1,p)%p,[]).append(d)
        else:
            assert b!=0
    catalogue=set()
    cores={"y","b1","b2","b3"}
    pos={"t","u1","u2","v1","v2"}
    zeros={"u3","v3"}
    for residue,eligible in candidates.items():
        bases={()}
        bases.update(mod_basis([v],p) for v in eligible)
        bases.update(mod_basis([v,w],p) for v,w in combinations(eligible,2))
        for basis in bases:
            groups={}
            for name,v in values.items():groups.setdefault(mod_reduce(v,basis,p),[]).append(name)
            classes=tuple(sorted(tuple(sorted(g)) for g in groups.values()))
            if any(len(set(g)&cores)>1 or len(set(g)&pos)>1 or
                   (set(g)&pos and set(g)&(cores|zeros)) for g in classes):continue
            catalogue.add((residue,classes))
    return catalogue


def verify_tail(pattern):
    vals=make_values();r=pattern["residue"];basis=pattern["basis"]
    merged=[g for g in pattern["classes"] if len(g)>1]
    assert len(merged)==1 and len(merged[0])==2
    hnames=merged[0]
    rn=next(n for n in hnames if n.startswith("r"))
    nn=next(n for n in hnames if n.startswith("n"))
    active=int(nn[1])
    h=vals[rn]
    qs=[tuple((1,1,1,1)[j]-int(j==i) for j in range(4)) for i in range(3)]
    partners=[tuple(a-b for a,b in zip(q,h)) for q in qs]
    reduced=[reduce_vec(v,basis) for v in partners]
    targets=[reduce_vec(vals["t"],basis),reduce_vec(vals[f"v{active}"],basis)]
    assert all(reduced.count(v)==1 for v in targets)
    z=partners[next(i for i,v in enumerate(reduced) if v not in targets)]
    weights=[F(-1,2)-r,r-3,F(-1,2),F(-2)]
    def ell(v):return F(3,2)+sum(a*b for a,b in zip(v,weights))
    zval=ell(z)
    differences=[]
    for name,v in vals.items():
        diff=zval-ell(v)
        assert diff!=0
        assert largest_prime_factor(diff.numerator)<149
        assert largest_prime_factor(diff.denominator)<149
        differences.append(abs(diff.numerator))
    # The exact universal capacity argument, in affine (p,constant) form:
    # old named mass = 3p-1-H, H<=s; new mass = rho+1.
    # Thus total >=3p+1, exceeding 3p-4 by five.
    assert (F(3),F(-1))==(F(2)+F(1,2)+1-F(1,2),F(1)-F(1,2)+F(1)-F(5,2))
    return {"residue":str(r),"overlap":list(hnames),"new_value_ell":str(zval),
            "maximum_separation_numerator":max(differences),"capacity_margin":5}


def main():
    patterns,meta=collision_cases(make_values())
    assert meta["max_exception_prime"]==71
    assert meta["maximum_raw_difference_norm_squared"]==18
    assert 18**3 < 149**2 # Hadamard bound for every 3x3 minor.
    assert meta["permanent_difference_count"]==0
    assert len(patterns)==81
    for p in [149,151,257]:
        expected={(r["residue"].numerator*pow(r["residue"].denominator,-1,p)%p,r["classes"]) for r in patterns}
        actual=independent_mod_catalogue(make_values(),p)
        assert actual==expected,(p,len(actual),len(expected))
    expected_keys={(j,k,ks) for j,pattern in enumerate(patterns)
                   for k in range(pattern["residue"].denominator+1) for ks in product(range(3),repeat=3)}
    seen=set();certified=0;tail=[]
    path=Path(__file__).with_name("two_active_exact_certificates.jsonl.gz")
    with gzip.open(path,"rt") as f:
        header=json.loads(next(f));assert header["metadata"]==meta
        for line in f:
            item=json.loads(line)
            j,k,ks=item["pattern_index"],item["lift"],tuple(item["quotients"])
            key=j,k,ks
            assert key in expected_keys and key not in seen
            seen.add(key)
            assert item["residue"]==str(patterns[j]["residue"])
            if item["status"]=="requires_hand_closure":
                assert ks==(0,0,0)
                tail.append({**verify_tail(patterns[j]),"lift":k})
                continue
            assert item["status"]=="exact_farkas"
            rows,labels,_=exact_system(patterns[j],meta["threshold"],k,ks)
            total=[F(0)]*len(rows[0])
            used=set()
            for i,wt in item["weights"]:
                assert i not in used and 0<=i<len(rows)
                used.add(i);wt=F(wt);assert wt>0
                total=[x+wt*y for x,y in zip(total,rows[i])]
            assert all(x==0 for x in total[:-1])
            assert total[-1]>0 and total[-1]==F(item["positive_constant"])
            certified+=1
    assert seen==expected_keys
    assert len(seen)==9828 and certified==9823 and len(tail)==5
    report={"status":"PASS","scope":"Exact certificate replay plus modular catalogue checks and four symbolic hand closures; mathematical input reductions remain explicit dependencies.",
            "critical_residues":41,"collision_patterns":81,"total_cases":len(seen),
            "exact_farkas_certificates":certified,"hand_closed_cases":tail,
            "independent_modular_catalogues":[149,151,257],
            "certificate_sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
    Path(__file__).with_name("two_active_exact_verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":main()
